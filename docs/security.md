# GitAssist Security Model

## Core Security Rule

**Never execute an unvalidated command directly — and never let confirmation be skippable for a command that should be blocked outright.**

Every Git operation — whether triggered from a menu, typed manually, or suggested by the AI assistant — passes through the same pipeline before it runs.

## Pipeline Stages

1. **Parsing** (`security/parser.py`): Turns the raw argv list into a structured representation — global options (`-C`, `--git-dir`, `--work-tree`, `-c key=value`, `--exec-path`, ...), the subcommand, and its arguments. This replaced an earlier implementation that matched regex against a joined string and could not see through global options.

2. **Risk Classification** (`security/policy.py`, exposed via `security/analyzer.py`): Classifies the parsed command into one of four levels:
   - `SAFE` — read-only or clearly non-destructive.
   - `CAUTION` — modifies repository state or talks to a remote, but is recoverable.
   - `DANGEROUS` — can destroy, overwrite, or irreversibly rewrite history/data.
   - `BLOCKED` — matches a known code-execution vector. Cannot be confirmed past, cannot be bypassed with `--dry-run`, and cannot be bypassed by calling the executor non-interactively.

   An **unrecognized subcommand is `BLOCKED`**, not merely cautioned. Git resolves unknown names through aliases and `git-*` executables on PATH, which can become external-command execution vectors.

3. **Context Check** (`security/context.py`): Verifies the command is appropriate for the *actual* repository it targets (resolved from any `-C`/`--git-dir` override, not just the process's working directory).
   - Example: refuses to merge/pull with uncommitted changes present.
   - Example: refuses to push with no remote configured.

4. **User Confirmation**: Required for anything above `SAFE`. If no interactive prompt is available (`interactive=False`) and the command isn't `SAFE`, it is **refused, not silently executed** — there is no path where a risky command runs without either a human confirming it or being flagged `SAFE` by the policy engine.

5. **Execution** (`git/executor.py`): Runs via `subprocess.run` with a list of arguments — never `shell=True`, so shell metacharacters in an argument have no special meaning at the OS level. Network-capable commands (fetch/pull/push, and the remote monitor's status check) carry a timeout so a dead connection fails cleanly instead of hanging. `--dry-run` still performs every step above except the final `subprocess.run` call.

6. **Error Intelligence** (`errors/analyzer.py`): After a failure, known Git error messages are matched and explained with a practical suggestion (push rejected, merge conflict, no upstream branch, auth failure, unmerged files blocking a pull, etc.).

7. **Logging** (`gitlog/logger.py`): Every execution attempt is logged; security-relevant events (a block, a confirmed dangerous command, a refusal due to missing confirmation) are logged with a `[SECURITY]` prefix so they're distinguishable from routine INFO/ERROR lines. Command text and subprocess output are redacted (see below) before being written.

## Hard Blocks (never executable, regardless of confirmation)

These are refused unconditionally because they are known vectors for making Git run an arbitrary external program:

| Construct | Why it's blocked |
|---|---|
| `-c alias.x='!cmd'` / `git config alias.x '!cmd'` | Git aliases starting with `!` run an arbitrary shell command. |
| `-c core.pager=...`, `-c credential.helper=...`, `-c diff.external=...`, and similar exec-capable config keys | These configure Git to invoke an external program. |
| `--exec-path=...` | Changes which `git-*` helper binaries are used — lets a substituted binary run instead of real Git. |
| `ext::...` / `fd::...` (as a remote/transport address) | These transport helpers can run arbitrary commands. |
| `--upload-pack=...` / `--receive-pack=...` | Can make Git run an arbitrary program as part of a clone/fetch/push. |
| An unrecognized option appearing before the subcommand | Its effect can't be verified as safe, so it's refused rather than guessed at. |

## Risk Classification Examples

| Command | Risk Level |
|---|---|
| `git status`, `git add .` | SAFE |
| `git commit`, `git clone`, `git push` | CAUTION |
| `git branch -d feature` | CAUTION |
| `git merge feature`, `git pull` | CAUTION |
| `git branch -D feature` | DANGEROUS |
| `git reset --hard` | DANGEROUS |
| `git push --force` | DANGEROUS |
| `git clean -fd` | DANGEROUS |
| `git checkout -- .` / `git restore .` | DANGEROUS |
| `git -c alias.x='!id' x` | BLOCKED |
| `git --exec-path=/tmp/evil` | BLOCKED |

## Protecting Secrets

- GitHub tokens are entered with terminal echo disabled (`getpass`), so they never appear on screen or in shell history/scrollback.
- Credentials embedded in a remote URL (`https://user:token@host/...`) are masked (`security/redaction.py`) before being displayed or logged.
- Log output is redacted for common secret shapes (GitHub token prefixes, `Authorization: Bearer ...`, `key=value` secrets) before being written to `~/.gitassist.log`.
- No token or password is ever included in an error message shown to the user.

## Limitations

- The policy engine's argument-shape checks cover the destructive commands and bypass patterns this project has specifically tested against (see `tests/test_security_bypass.py` and `tests/test_executor_security.py`) — it is not a formally verified parser for the entirety of Git's command-line grammar, and a genuinely novel argument shape could in principle be misclassified.
- GitAssist trusts the local Git installation; it does not verify the integrity of the `git` binary itself.
- Redaction is pattern-based and best-effort — it cannot mask a secret whose shape it doesn't recognize.
- This is a defense-in-depth design, not a guarantee of complete security. It should meaningfully reduce the chance of an accidental or naively-injected destructive/malicious command running, not be treated as immune to all possible bypass techniques.

## Best Practices

- Review warnings and safer alternatives before confirming a CAUTION/DANGEROUS command.
- Use `--dry-run` when trying an unfamiliar command.
- Use a dedicated GitHub token with the minimum permission scope needed.
