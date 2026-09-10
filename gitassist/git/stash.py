"""Git stash operations."""

from gitassist.git.executor import run_git_command
from gitassist.config import settings
from gitassist.localization.texts import get_text


def save_stash(message="", lang=None, include_untracked=True):
    """
    Save current changes to stash.
    By default includes untracked files (-u), so beginners don't lose
    newly created files that they haven't 'git add'-ed yet.
    """
    lang = lang or settings.LANGUAGE
    cmd = ["git", "stash", "push"]
    if include_untracked:
        cmd.append("-u")
    if message:
        cmd.extend(["-m", message])
    return run_git_command(cmd, get_text("stash_saving", lang), lang=lang)


def list_stashes(lang=None):
    """List all stashes."""
    lang = lang or settings.LANGUAGE
    return run_git_command(
        ["git", "stash", "list"],
        get_text("stash_listing", lang),
        lang=lang,
    )


def pop_stash(lang=None):
    """Apply and remove the most recent stash."""
    lang = lang or settings.LANGUAGE
    return run_git_command(
        ["git", "stash", "pop"],
        get_text("stash_popping", lang),
        lang=lang,
    )


def apply_stash(lang=None):
    """Apply the most recent stash without removing it."""
    lang = lang or settings.LANGUAGE
    return run_git_command(
        ["git", "stash", "apply"],
        get_text("stash_applying", lang),
        lang=lang,
    )


def drop_stash(lang=None):
    """Drop the most recent stash."""
    lang = lang or settings.LANGUAGE
    return run_git_command(
        ["git", "stash", "drop"],
        get_text("stash_dropping", lang),
        lang=lang,
    )


def has_stashes():
    """Return True if there is at least one stash."""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "stash", "list"],
            capture_output=True, text=True, check=False,
            encoding="utf-8", errors="replace",
        )
        return bool(result.stdout.strip())
    except Exception:
        return False