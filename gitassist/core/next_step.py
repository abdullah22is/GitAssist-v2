"""
Next-step suggestion engine.

After a command completes, suggest what a user would naturally do next -
purely informational, never executed automatically. Kept as a small,
explicit mapping rather than a clever inference system, since guessing
wrong is worse than saying nothing.
"""

from __future__ import annotations

from gitassist.localization.texts import get_text
from gitassist.git import repository


def suggest_after(action: str, path: str = ".", lang: str = None) -> str:
    """
    Return a localized next-step suggestion for the action just performed,
    or "" if there's nothing useful to suggest. `action` is one of:
    "init", "clone", "add", "commit", "fetch", "merge_or_pull_clean",
    "resolved_conflicts".
    """
    if action == "init":
        return get_text("next_step_after_init", lang)

    if action == "clone":
        return get_text("next_step_after_clone", lang)

    if action == "add":
        return get_text("next_step_after_add", lang)

    if action == "commit":
        if repository.has_remote(path):
            return get_text("next_step_after_commit_with_remote", lang)
        return get_text("next_step_after_commit_no_remote", lang)

    if action == "fetch":
        return get_text("next_step_after_fetch", lang)

    if action == "conflicts_detected":
        return get_text("next_step_conflicts", lang)

    return ""
