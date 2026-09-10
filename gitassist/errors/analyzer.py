"""Analyze Git command failures and provide useful explanations."""

import re
from gitassist.localization.texts import get_text


ERROR_PATTERNS = [
    {
        "pattern": r"fatal: not a git repository",
        "explanation_key": "error_not_git_repo",
        "suggestion_key": "suggestion_init_or_clone",
    },
    {
        "pattern": r"fatal: remote origin already exists",
        "explanation_key": "error_remote_exists",
        "suggestion_key": "suggestion_remote_set_url",
    },
    {
        "pattern": r"error: failed to push some refs",
        "explanation_key": "error_push_rejected",
        "suggestion_key": "suggestion_pull_first",
    },
    {
        "pattern": r"CONFLICT \(content\):",
        "explanation_key": "error_merge_conflict",
        "suggestion_key": "suggestion_resolve_conflicts",
    },
    {
        "pattern": r"error: Your local changes to the following files would be overwritten by merge",
        "explanation_key": "error_local_changes_overwritten",
        "suggestion_key": "suggestion_commit_or_stash",
    },
    {
        "pattern": r"fatal: unable to access .* 403",
        "explanation_key": "error_auth_failed",
        "suggestion_key": "suggestion_check_credentials",
    },
    {
        "pattern": r"fatal: unable to access .* 404",
        "explanation_key": "error_not_found",
        "suggestion_key": "suggestion_verify_url",
    },
    {
        "pattern": r"fatal: refusing to merge unrelated histories",
        "explanation_key": "error_unrelated_histories",
        "suggestion_key": "suggestion_allow_unrelated",
    },
    {
        "pattern": r"error: pathspec .* did not match any file",
        "explanation_key": "error_pathspec",
        "suggestion_key": "suggestion_check_path",
    },
    {
        "pattern": r"fatal: could not read Username",
        "explanation_key": "error_username",
        "suggestion_key": "suggestion_credential_manager",
    },
    {
        "pattern": r"fatal: The current branch .* has no upstream branch",
        "explanation_key": "error_no_upstream",
        "suggestion_key": "suggestion_set_upstream",
    },
    {
        "pattern": r"(Pulling is not possible because|Cannot pull with rebase:) you have unmerged (paths|files)",
        "explanation_key": "error_unmerged_files",
        "suggestion_key": "suggestion_resolve_conflicts",
    },
]


def analyze_error(stderr: str) -> str:
    """Return a friendly explanation for known Git errors, or empty string."""
    if not stderr:
        return ""

    for entry in ERROR_PATTERNS:
        if re.search(entry["pattern"], stderr, re.IGNORECASE):
            explanation = get_text(entry["explanation_key"])
            suggestion = get_text(entry["suggestion_key"])
            return f"{explanation}\n{suggestion}"

    return ""