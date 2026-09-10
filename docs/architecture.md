# GitAssist Architecture

## Overview
GitAssist is a modular command-line assistant that wraps Git operations with safety, context awareness, and error intelligence. English and Arabic are both fully supported today (not a future goal) — every user-facing message is centralized in `gitassist/localization/texts.py` and checked by an automated test for completeness in both languages.

## High-Level Components

- **CLI Layer** (`gitassist/cli/`): `output.py` (colored/plain-text messages, auto-disabling color for non-tty/`NO_COLOR`), `input_handler.py` (prompts, including hidden-input `ask_secret` for tokens), `dashboard.py` (repository status box), `voice.py` (optional voice input, lazily imported so a missing dependency can't crash startup).
- **Core Layer** (`gitassist/core/`): `commands.py` (menu-driven workflows: create/open a project, save changes, branches, stash, sync, GitHub, files), `manual_command.py` (free-text command entry with quoting-aware splitting and typo correction), `files.py` (file/directory operations), `next_step.py` (post-action suggestions).
- **Git Layer** (`gitassist/git/`): `executor.py` (the single choke point every command runs through), `repository.py` (state inspection: branch, working tree, remote, ahead/behind), `remote_monitor.py` (throttled, cached remote status checks), `sync.py` (fetch/pull/push), `stash.py`, `branches.py`.
- **Security Layer** (`gitassist/security/`): `parser.py` (structured Git argument parsing), `policy.py` (risk classification rules), `analyzer.py` (thin public wrapper combining the two), `context.py` (repository-appropriateness checks), `redaction.py` (secret masking), `shell_guard.py` (rejects shell syntax in free-text command entry), `risk.py` (the `RiskLevel` enum: SAFE/CAUTION/DANGEROUS/BLOCKED).
- **Error Layer** (`gitassist/errors/`): Pattern-matches common Git failure messages and returns a practical, localized suggestion.
- **GitHub Integration** (`gitassist/github/`): Remote URL parsing (with credential stripping) and GitHub API repository creation with specific error-code handling.
- **AI Layer** (`gitassist/ai/`): `fallback.py` (offline rule-based Arabic/English phrase matching), `assistant.py` (optional Ollama/OpenAI backends), `intent.py` (tries rule-based first, falls back to AI if enabled). Every suggestion produced here is just a candidate command string — it is never executed directly, and goes through the exact same `git/executor.py` pipeline as anything else.
- **Logging** (`gitassist/gitlog/`): `logger.py` sets up file logging and provides `log_security_event()` for a distinguishable `[SECURITY]`-prefixed audit trail.
- **Config** (`gitassist/config/`): Central settings — language, dry-run flag, AI provider, remote-check throttling parameters.
- **Localization** (`gitassist/localization/`): `texts.py`, a single English/Arabic dictionary keyed by message id.

## Data Flow

1. `__main__.py` initializes the environment and enters the main interactive loop, driven by `core/commands.py`.
2. The dynamic menu adapts to repository state, read via `git/repository.py`.
3. The user selects a menu action, types a manual command, or (if enabled) speaks/describes one for the AI layer to interpret.
4. Whatever the source, the resulting command reaches `git/executor.run_git_command()`.
5. The executor parses the command (`security/parser.py`), classifies its risk (`security/policy.py`) — refusing outright if `BLOCKED` — resolves and checks the actual repository context (`security/context.py`), requires confirmation for anything above `SAFE`, then executes via `subprocess` with a list of arguments (never `shell=True`) and an optional timeout.
6. On failure, `errors/analyzer.py` explains the error; on success, `core/next_step.py` may suggest a natural next action.
7. Every attempt is logged, with secrets redacted first.

## Design Principles

- **Safety-first**: no command is executed without validation, and a `BLOCKED` classification cannot be confirmed past.
- **Fail-closed**: if confirmation is required but unavailable, the command is refused rather than run.
- **Context-aware**: menus, checks, and the remote monitor adapt to actual repository state, resolved from any `-C`/`--git-dir` override rather than assumed from the working directory.
- **Modularity**: each concern (parsing, risk policy, context, execution, redaction) is a separate, independently testable module.
- **Localization-complete**: Arabic and English are both first-class today, verified by a static test that scans the codebase for every message key actually used.
- **Extensibility**: a new destructive command pattern is added as one rule in `security/policy.py`'s rule table, not a new regex scattered through the codebase.

## Testing

Unit and integration tests are located in `tests/` and run with:
```bash
python -m unittest discover -s tests
```
Integration tests exercise real temporary Git repositories and local bare repositories used as a stand-in remote — no real network access and no user repositories are touched.

## Known Limitations / Possible Future Work

- The policy is deliberately allow-by-rule: unknown Git subcommands are blocked because Git aliases and git-* executables can otherwise become execution vectors. The parser/policy is not a formally verified implementation of the entire Git CLI grammar.
- No GUI; this is a terminal application by design.
- The remote-update cache is a simple per-repository JSON file — sufficient for a single-user CLI tool, not designed for concurrent multi-process access.
