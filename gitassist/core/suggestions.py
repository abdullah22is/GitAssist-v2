"""Next-step suggestion engine."""

from gitassist.git import repository
from gitassist.cli import output
from gitassist.localization.texts import get_text


def suggest_after(action: str):
    """Return a suggestion string based on the last completed action."""
    if action == "commit":
        if repository.has_remote():
            return get_text("suggest_push_after_commit")
        return get_text("suggest_add_remote_after_commit")
    if action == "stage":
        return get_text("suggest_commit_after_stage")
    if action == "init":
        return get_text("suggest_stage_after_init")
    return None


def suggest_next_step():
    """Print a relevant suggestion based on current repository state."""
    if not repository.is_git_repo():
        output.print_info(get_text("repo_not_detected"))
        return

    if repository.has_uncommitted_changes():
        output.print_info(get_text("uncommitted_changes_yes"))
        return

    if repository.has_remote():
        ahead, behind = repository.get_ahead_behind()
        if behind > 0:
            output.print_warning(get_text("behind_remote"))
        elif ahead > 0:
            output.print_info(get_text("ahead_commits", count=ahead))
        else:
            output.print_info(get_text("up_to_date"))
        return

    output.print_info(get_text("remote_not_configured"))