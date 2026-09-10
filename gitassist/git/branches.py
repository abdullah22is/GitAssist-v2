"""Git branch operations."""
from gitassist.git.executor import run_git_command
from gitassist.git.repository import get_current_branch


def list_branches(show_all=False):
    """List local (or all) branches."""
    cmd = ["git", "branch", "-a"] if show_all else ["git", "branch"]
    return run_git_command(cmd, "Listing branches...")


def create_branch(name):
    """Create a new branch from current HEAD."""
    cmd = ["git", "branch", name]
    return run_git_command(cmd, f"Creating branch '{name}'")


def switch_branch(name):
    """Switch to an existing branch."""
    cmd = ["git", "switch", name]
    return run_git_command(cmd, f"Switching to branch '{name}'")


def delete_branch(name, force=False):
    """
    Delete a branch.
    force=True uses -D, otherwise -d (safe delete).
    """
    flag = "-D" if force else "-d"
    cmd = ["git", "branch", flag, name]
    return run_git_command(cmd, f"Deleting branch '{name}'")


def merge_branch(name):
    """Merge a branch into current branch."""
    cmd = ["git", "merge", name]
    return run_git_command(cmd, f"Merging branch '{name}' into current branch")


def is_current_branch(name):
    """Return True if the given name is the current branch."""
    current = get_current_branch()
    return current is not None and current == name