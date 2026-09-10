"""Next-step suggestion engine."""

from gitassist.git import repository
from gitassist.cli import output
from gitassist.localization.texts import get_text


def suggest_next_step():
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