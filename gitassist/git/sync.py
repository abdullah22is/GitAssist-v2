"""Git synchronization operations (fetch, pull, push)."""

from gitassist.git.executor import run_git_command
from gitassist.git import repository
from gitassist.config import settings
from gitassist.localization.texts import get_text


def fetch(remote="origin", lang=None):
    """Fetch changes from remote without merging."""
    lang = lang or settings.LANGUAGE
    return run_git_command(
        ["git", "fetch", remote],
        get_text("fetching_remote", lang, remote=remote),
        lang=lang,
    )


def pull(remote="origin", branch=None, lang=None, allow_unrelated=False):
    """Pull changes from remote and merge into current branch."""
    lang = lang or settings.LANGUAGE
    if not branch:
        branch = repository.get_current_branch()
    cmd = ["git", "pull"]
    if remote:
        cmd.append(remote)
    if branch:
        cmd.append(branch)
    if allow_unrelated:
        cmd.append("--allow-unrelated-histories")
    return run_git_command(cmd, get_text("pulling_remote", lang), lang=lang)


def push(remote="origin", branch=None, lang=None):
    """Push local commits to remote."""
    lang = lang or settings.LANGUAGE
    if not branch:
        branch = repository.get_current_branch()
    cmd = ["git", "push"]
    if remote:
        cmd.append(remote)
    if branch:
        cmd.append(branch)
    return run_git_command(cmd, get_text("pushing_remote", lang), lang=lang)


def has_remote_updates(remote="origin", lang=None):
    """
    Check if there are remote updates available.
    Returns True if local branch is behind remote, False otherwise.
    """
    lang = lang or settings.LANGUAGE
    if not repository.has_remote():
        return False

    if not fetch(remote, lang=lang):
        return False

    branch = repository.get_current_branch()
    if not branch:
        return False

    output_text = run_git_command(
        ["git", "rev-list", "--count", f"HEAD..{remote}/{branch}"],
        "",
        show_output=False,
        interactive=False,
        lang=lang,
        capture_text=True,
    )
    if output_text is None:
        return False

    stripped = output_text.strip()
    return stripped.isdigit() and int(stripped) > 0