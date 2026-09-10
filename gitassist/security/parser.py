"""
Structured Git command parser.

This replaces naive string matching (`command.startswith("git ")`) and
regex-on-joined-string detection with a real understanding of Git's
argument grammar: global options (-C, --git-dir, --work-tree, -c, ...),
the subcommand, and the subcommand's own arguments.

This module performs NO risk classification itself - see
gitassist.security.policy for that. Its only job is to turn a list of
argv-style tokens into an unambiguous, structured representation (or
flag it as unparsable / structurally unsafe).
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Global options that take a value as a SEPARATE following token
# (e.g. ["-C", "/tmp"]) or as an attached "--long=value" token.
GLOBAL_VALUE_OPTS = {
    "-C",
    "--git-dir",
    "--work-tree",
    "--namespace",
    "--super-prefix",
    "--exec-path",
    "--config-env",
}

# Global options that never take a value.
GLOBAL_NOVALUE_OPTS = {
    "--no-pager",
    "--paginate",
    "-p",
    "--bare",
    "--no-replace-objects",
    "--literal-pathspecs",
    "--no-literal-pathspecs",
    "--no-optional-locks",
    "--no-advice",
    "-v",
    "--version",
    "-h",
    "--help",
}

# Config key prefixes that can cause Git to execute an external program.
# Setting any of these via `-c key=value` (or persisting them via
# `git config key value`) is treated as a code-execution vector, not a
# harmless setting.
EXEC_CAPABLE_CONFIG_PREFIXES = (
    "alias.",
    "core.pager",
    "core.editor",
    "core.sshcommand",
    "core.fsmonitor",
    "core.hookspath",
    "core.gitproxy",
    "core.askpass",
    "credential.helper",
    "diff.external",
    "difftool.",
    "mergetool.",
    "filter.",
    "http.proxy",
    "protocol.",
    "uploadpack.",
    "receivepack.",
    "include.path",
    "includeif.",
)

# URL/transport schemes known to allow arbitrary command execution.
UNSAFE_TRANSPORT_PREFIXES = ("ext::", "fd::")


@dataclass
class ParsedGitCommand:
    raw: list = field(default_factory=list)
    ok: bool = True
    blocked: bool = False
    block_reason_key: str = ""  # localization key describing why blocked
    parse_error_key: str = ""   # localization key describing a parse failure

    git_dir: str = None
    work_tree: str = None
    chdir: str = None            # from -C
    exec_path: str = None
    config_overrides: list = field(default_factory=list)  # list[(key, value)]

    subcommand: str = None
    sub_args: list = field(default_factory=list)

    def resolved_path(self, default: str = ".") -> str:
        """Resolve the working-tree context targeted by this invocation.

        Git permits multiple -C options; each relative -C is interpreted
        relative to the directory established by the previous -C. For
        security checks we also prefer an explicit --work-tree when present.
        A --git-dir pointing at a normal `.git` directory is mapped to its
        parent as a useful best-effort working-tree context.
        """
        import os
        if self.work_tree:
            base = self.chdir or default
            return os.path.abspath(self.work_tree if os.path.isabs(self.work_tree) else os.path.join(base, self.work_tree))
        if self.chdir:
            return os.path.abspath(self.chdir)
        if self.git_dir:
            gd = os.path.abspath(self.git_dir)
            if os.path.basename(os.path.normpath(gd)) == ".git":
                return os.path.dirname(gd)
        return os.path.abspath(default)


def _split_long_opt(token: str):
    """Split a "--opt=value" token into (opt, value) or (opt, None)."""
    if "=" in token:
        opt, _, val = token.partition("=")
        return opt, val
    return token, None


def _block(parsed: ParsedGitCommand, reason_key: str) -> ParsedGitCommand:
    """Mark a parse result as blocked. `ok` and `blocked` are always kept
    in lockstep so a caller that only checks one of them still sees the
    refusal - this is what a previous bug in this module got wrong."""
    parsed.ok = False
    parsed.blocked = True
    parsed.block_reason_key = reason_key
    return parsed


def _parse_error(parsed: ParsedGitCommand, error_key: str) -> ParsedGitCommand:
    parsed.ok = False
    parsed.parse_error_key = error_key
    return parsed


def parse_git_command(command_list) -> ParsedGitCommand:
    """
    Parse a full argv-style Git invocation, e.g.
    ["git", "-C", "/tmp", "-c", "user.name=x", "reset", "--hard"].

    Returns a ParsedGitCommand. Check `.ok` and `.blocked` before trusting
    any other field - a failed/blocked parse must never be treated as SAFE.
    """
    parsed = ParsedGitCommand(raw=list(command_list))

    if not command_list or command_list[0] != "git":
        return _block(parsed, "blocked_not_git_invocation")

    i = 1
    n = len(command_list)
    while i < n:
        tok = command_list[i]

        if tok == "--":
            i += 1
            break

        if tok == "-c":
            i += 1
            if i >= n or "=" not in command_list[i]:
                return _parse_error(parsed, "parse_error_malformed_config")
            key, _, val = command_list[i].partition("=")
            parsed.config_overrides.append((key, val))
            i += 1
            continue

        if tok.startswith("-c") and len(tok) > 2:
            # Glued short-option form: -cfoo=bar
            kv = tok[2:]
            if "=" not in kv:
                return _parse_error(parsed, "parse_error_malformed_config")
            key, _, val = kv.partition("=")
            parsed.config_overrides.append((key, val))
            i += 1
            continue

        if tok.startswith("--") and "=" in tok:
            opt, val = _split_long_opt(tok)
            if opt == "--config-env":
                return _block(parsed, "blocked_config_env")
            if opt in GLOBAL_VALUE_OPTS:
                if opt == "--git-dir":
                    parsed.git_dir = val
                elif opt == "--work-tree":
                    parsed.work_tree = val
                elif opt == "--exec-path":
                    parsed.exec_path = val
                i += 1
                continue

        if tok in GLOBAL_VALUE_OPTS:
            if tok == "--config-env":
                return _block(parsed, "blocked_config_env")
            i += 1
            if i >= n:
                return _parse_error(parsed, "parse_error_missing_value")
            val = command_list[i]
            if tok == "-C":
                # Git applies each relative -C against the directory selected
                # by the previous -C. Keep a normalized final path.
                import os
                base = parsed.chdir or "."
                parsed.chdir = os.path.abspath(val if os.path.isabs(val) else os.path.join(base, val))
            elif tok == "--git-dir":
                parsed.git_dir = val
            elif tok == "--work-tree":
                parsed.work_tree = val
            elif tok == "--exec-path":
                parsed.exec_path = val
            i += 1
            continue

        if tok in GLOBAL_NOVALUE_OPTS:
            i += 1
            continue

        if tok.startswith("-"):
            # An unrecognized option appearing before any subcommand was
            # found. Per policy: unknown constructs are never assumed
            # safe - refuse to guess what this does.
            return _block(parsed, "blocked_unrecognized_global_option")

        parsed.subcommand = tok
        i += 1
        break

    parsed.sub_args = list(command_list[i:])

    if parsed.subcommand is None and not parsed.sub_args:
        return _parse_error(parsed, "parse_error_no_subcommand")

    # --exec-path changes which git-* helper binaries get run for every
    # subsequent internal invocation - a well-known way to substitute a
    # malicious binary. There is no legitimate interactive-CLI use case
    # for allowing this from user/AI input.
    if parsed.exec_path is not None:
        return _block(parsed, "blocked_exec_path")

    for key, val in parsed.config_overrides:
        lowered_key = key.lower()
        if lowered_key.startswith("alias.") and ("!" in val or val.strip().startswith("!")):
            return _block(parsed, "blocked_alias_shell_escape")
        if any(lowered_key.startswith(p) for p in EXEC_CAPABLE_CONFIG_PREFIXES):
            return _block(parsed, "blocked_exec_capable_config")

    for idx, arg in enumerate(parsed.sub_args):
        low = arg.lower()
        if low.startswith(UNSAFE_TRANSPORT_PREFIXES):
            return _block(parsed, "blocked_unsafe_transport")

        # Options that let the caller substitute the Git transport helper
        # with an arbitrary executable. Their meaning is subcommand-specific:
        # `-u` on push means --set-upstream and is NOT an upload-pack option.
        if parsed.subcommand == "clone" and (low in ("-u", "--upload-pack") or low.startswith("--upload-pack=")):
            return _block(parsed, "blocked_upload_receive_pack")
        if parsed.subcommand == "fetch" and low.startswith("--upload-pack"):
            return _block(parsed, "blocked_upload_receive_pack")
        if parsed.subcommand == "push" and (low.startswith("--receive-pack") or low.startswith("--exec")):
            return _block(parsed, "blocked_upload_receive_pack")

    # Also guard persistent configuration writes. A dangerous config key can
    # create a delayed execution primitive even when its immediate value is
    # not prefixed with `!` (e.g. core.hooksPath).
    if parsed.subcommand == "config" and len(parsed.sub_args) >= 1:
        cfg_key = next((a.lower() for a in parsed.sub_args if not a.startswith("-")), "")
        cfg_val = parsed.sub_args[-1] if parsed.sub_args else ""
        if cfg_key.startswith("alias.") and ("!" in cfg_val or cfg_val.strip().startswith("!")):
            return _block(parsed, "blocked_alias_shell_escape")
        if any(cfg_key.startswith(p) for p in EXEC_CAPABLE_CONFIG_PREFIXES):
            return _block(parsed, "blocked_exec_capable_config")

    return parsed
