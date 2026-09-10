"""
Security policy engine.

Classifies an already-PARSED Git command (see gitassist.security.parser)
into SAFE / CAUTION / DANGEROUS / BLOCKED, using structured checks on the
subcommand and its arguments rather than regex over a joined string.

Design rule (see project security spec): an unrecognized subcommand is
NEVER automatically SAFE. It defaults to CAUTION so the user is always
asked to confirm.
"""

from __future__ import annotations

from gitassist.security.risk import RiskLevel


def _has_flag(args, *names) -> bool:
    """True if any arg exactly matches one of names, or is a --long=value
    form whose option part matches."""
    for a in args:
        base = a.split("=", 1)[0]
        if a in names or base in names:
            return True
    return False


def _has_flag_prefix(args, prefix) -> bool:
    return any(a.startswith(prefix) for a in args)


# (warning_key, alternative_key) per rule, looked up by caller via get_text.
RULES = []


def _rule(predicate, level, warning_key, alternative_key=""):
    RULES.append((predicate, level, warning_key, alternative_key))


# ---- DANGEROUS: irreversible or history/data-destroying ----
_rule(lambda sc, a: sc == "reset" and _has_flag(a, "--hard", "--merge"),
      RiskLevel.DANGEROUS, "warning_reset_hard", "alternative_reset_hard")

_rule(lambda sc, a: sc == "push" and _has_flag(a, "--force", "-f", "--force-with-lease"),
      RiskLevel.DANGEROUS, "warning_force_push", "alternative_force_push")

def _clean_is_destructive(a) -> bool:
    # `git clean -n...` / `--dry-run` only previews deletions and is safe.
    if _has_flag(a, "-n", "--dry-run"):
        return False
    if _has_flag(a, "-f", "--force"):
        return True
    return any(
        tok.startswith("-") and not tok.startswith("--") and "f" in tok
        for tok in a
    )


_rule(lambda sc, a: sc == "clean" and _clean_is_destructive(a),
      RiskLevel.DANGEROUS, "warning_clean_fd", "alternative_clean_fd")

_rule(lambda sc, a: sc == "checkout" and _has_flag(a, "--"),
      RiskLevel.DANGEROUS, "warning_checkout_discard", "alternative_checkout_discard")

def _restore_is_worktree_affecting(a) -> bool:
    staged_only = _has_flag(a, "--staged", "-S") and not _has_flag(a, "--worktree", "-W")
    return not staged_only


_rule(lambda sc, a: sc == "restore" and len(a) > 0 and _restore_is_worktree_affecting(a),
      RiskLevel.DANGEROUS, "warning_checkout_discard", "alternative_checkout_discard")

_rule(lambda sc, a: sc == "restore" and len(a) > 0 and not _restore_is_worktree_affecting(a),
      RiskLevel.CAUTION, "warning_restore_staged", "")

_rule(lambda sc, a: sc == "rebase" and _has_flag(a, "-i", "--interactive"),
      RiskLevel.DANGEROUS, "warning_rebase_i", "alternative_rebase_i")

_rule(lambda sc, a: sc == "branch" and _has_flag(a, "-D", "--delete-force"),
      RiskLevel.DANGEROUS, "warning_branch_D", "alternative_branch_D")

_rule(lambda sc, a: sc == "stash" and len(a) > 0 and a[0] in ("drop", "clear"),
      RiskLevel.DANGEROUS, "warning_stash_drop", "alternative_stash_drop")

_rule(lambda sc, a: sc == "tag" and _has_flag(a, "-d", "-D"),
      RiskLevel.DANGEROUS, "warning_tag_delete", "alternative_tag_delete")

_rule(lambda sc, a: sc == "reflog" and len(a) > 0 and a[0] in ("delete", "expire"),
      RiskLevel.DANGEROUS, "warning_reflog_delete", "alternative_reflog_delete")

_rule(lambda sc, a: sc == "gc" and _has_flag_prefix(a, "--prune="),
      RiskLevel.DANGEROUS, "warning_gc_prune", "alternative_gc_prune")

# ---- CAUTION: modifies state or talks to a remote, but recoverable ----
_rule(lambda sc, a: sc == "branch" and _has_flag(a, "-d", "--delete"),
      RiskLevel.CAUTION, "warning_branch_D", "alternative_branch_D")

_rule(lambda sc, a: sc == "merge" and len(a) > 0,
      RiskLevel.CAUTION, "warning_merge", "alternative_merge")

_rule(lambda sc, a: sc == "rebase" and len(a) > 0,
      RiskLevel.CAUTION, "warning_rebase_i", "alternative_rebase_i")

_rule(lambda sc, a: sc == "reset" and len(a) > 0,
      RiskLevel.CAUTION, "warning_reset_soft", "alternative_reset_soft")

_rule(lambda sc, a: sc == "push",
      RiskLevel.CAUTION, "warning_push_generic", "")

_rule(lambda sc, a: sc == "pull",
      RiskLevel.CAUTION, "warning_pull_generic", "")

_rule(lambda sc, a: sc == "revert",
      RiskLevel.CAUTION, "warning_revert_generic", "")

_rule(lambda sc, a: sc == "remote" and len(a) > 0 and a[0] in ("remove", "rm", "set-url"),
      RiskLevel.CAUTION, "warning_remote_remove", "alternative_remote_remove")

_rule(lambda sc, a: sc == "gc",
      RiskLevel.CAUTION, "warning_gc_prune", "alternative_gc_prune")

_rule(lambda sc, a: sc == "config",
      RiskLevel.CAUTION, "warning_config_generic", "")

_rule(lambda sc, a: sc == "checkout" and len(a) > 0 and not _has_flag(a, "--"),
      RiskLevel.CAUTION, "warning_checkout_branch", "")

_rule(lambda sc, a: sc == "switch" and _has_flag(a, "-C", "-c", "--force-create"),
      RiskLevel.CAUTION, "warning_checkout_branch", "")

# ---- CAUTION: local state/configuration changes ----
_rule(lambda sc, a: sc == "commit",
      RiskLevel.CAUTION, "warning_commit_generic", "")

# Fetch updates remote-tracking refs but does not alter the working tree or
# local branch history. It is intentionally SAFE so the throttled remote
# monitor can perform its read-only network check without a confirmation
# prompt. Transport/config execution vectors are still blocked by the parser.

_rule(lambda sc, a: sc == "switch",
      RiskLevel.CAUTION, "warning_checkout_branch", "")

_rule(lambda sc, a: sc == "restore" and len(a) == 0,
      RiskLevel.CAUTION, "warning_unrecognized_shape", "")

# Safe state-changing commands whose effects are reversible and do not
# discard data. More destructive forms are matched by the rules above.
_rule(lambda sc, a: sc == "add",
      RiskLevel.SAFE, "", "")
_rule(lambda sc, a: sc == "init",
      RiskLevel.SAFE, "", "")
_rule(lambda sc, a: sc == "fetch",
      RiskLevel.SAFE, "", "")

# Clone creates a new working tree but does not overwrite an existing one
# unless Git itself permits it; transport execution vectors are blocked by
# the parser. Keep it confirmation-worthy because it performs network I/O.
_rule(lambda sc, a: sc == "clone",
      RiskLevel.CAUTION, "warning_clone_generic", "")

_rule(lambda sc, a: sc == "branch" and not a,
      RiskLevel.SAFE, "", "")
_rule(lambda sc, a: sc == "tag" and not a,
      RiskLevel.SAFE, "", "")
_rule(lambda sc, a: sc == "stash" and (not a or a[0] == "list"),
      RiskLevel.SAFE, "", "")
_rule(lambda sc, a: sc == "remote" and (not a or a[0] in ("-v", "--verbose", "get-url", "get")),
      RiskLevel.SAFE, "", "")
_rule(lambda sc, a: sc == "branch",
      RiskLevel.CAUTION, "warning_branch_generic", "")
_rule(lambda sc, a: sc == "tag",
      RiskLevel.CAUTION, "warning_tag_generic", "")
_rule(lambda sc, a: sc == "stash",
      RiskLevel.CAUTION, "warning_stash_generic", "")
_rule(lambda sc, a: sc == "remote",
      RiskLevel.CAUTION, "warning_remote_generic", "")
_rule(lambda sc, a: sc == "switch",
      RiskLevel.CAUTION, "warning_checkout_branch", "")

# ---- Explicitly SAFE (read-only only) ----
SAFE_SUBCOMMANDS = {
    # Read-only commands. Commands that mutate repository state are classified
    # explicitly below so new destructive behavior cannot accidentally become SAFE.
    "status", "log", "diff", "show", "blame", "shortlog", "describe",
    "ls-files", "rev-parse", "rev-list",
}


def classify(parsed) -> "tuple[RiskLevel, str, str]":
    """
    Classify a gitassist.security.parser.ParsedGitCommand.
    Returns (RiskLevel, warning_key, alternative_key). Keys are "" when
    not applicable (e.g. for SAFE).
    """
    if parsed.blocked:
        return RiskLevel.BLOCKED, parsed.block_reason_key or "blocked_generic", ""

    if not parsed.ok:
        # A parse error (malformed input) is refused, not guessed at.
        return RiskLevel.BLOCKED, parsed.parse_error_key or "blocked_generic", ""

    sc = parsed.subcommand
    args = parsed.sub_args

    for predicate, level, warning_key, alternative_key in RULES:
        try:
            if predicate(sc, args):
                return level, warning_key, alternative_key
        except Exception:
            # A malformed/unexpected argument shape must never be
            # silently treated as safe.
            return RiskLevel.CAUTION, "warning_unrecognized_shape", ""

    if sc in SAFE_SUBCOMMANDS:
        return RiskLevel.SAFE, "", ""

    # Unknown subcommands are BLOCKED, not merely cautioned. Git resolves
    # unknown names through aliases and git-* executables on PATH; either can
    # become an arbitrary external-command execution primitive. GitAssist
    # therefore requires an explicit policy rule for every executable
    # subcommand it permits.
    return RiskLevel.BLOCKED, "blocked_unknown_subcommand", ""
