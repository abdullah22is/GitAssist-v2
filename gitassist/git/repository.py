"""Repository detection and state inspection."""

from __future__ import annotations

import subprocess


def is_git_installed() -> bool:
    """Return True if Git is installed and accessible."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def is_git_repo(path: str = ".") -> bool:
    """Return True if the given path is inside a Git repository."""
    try:
        result = subprocess.run(
            ["git", "-C", path, "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, check=False,
            encoding="utf-8", errors="replace",
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except Exception:
        return False


def get_repo_root(path: str = ".") -> str | None:
    """Return the absolute path of the repository root, or None if not a repo."""
    if not is_git_repo(path):
        return None
    result = subprocess.run(
        ["git", "-C", path, "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=False,
        encoding="utf-8", errors="replace",
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def get_current_branch(path: str = ".") -> str | None:
    """Return the current branch name, or None if not available."""
    if not is_git_repo(path):
        return None
    result = subprocess.run(
        ["git", "-C", path, "branch", "--show-current"],
        capture_output=True, text=True, check=False,
        encoding="utf-8", errors="replace",
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def has_uncommitted_changes(path: str = ".") -> bool:
    """Return True if there are uncommitted changes in the working tree."""
    if not is_git_repo(path):
        return False
    result = subprocess.run(
        ["git", "-C", path, "status", "--porcelain"],
        capture_output=True, text=True, check=False,
        encoding="utf-8", errors="replace",
    )
    return bool(result.stdout.strip())


def get_remote_info(path: str = ".") -> str | None:
    """Return the first remote URL if configured, else None."""
    if not is_git_repo(path):
        return None
    result = subprocess.run(
        ["git", "-C", path, "remote", "-v"],
        capture_output=True, text=True, check=False,
        encoding="utf-8", errors="replace",
    )
    if result.returncode == 0 and result.stdout.strip():
        lines = result.stdout.strip().splitlines()
        if lines:
            parts = lines[0].split()
            if len(parts) >= 2:
                return parts[1]
    return None


def has_remote(path: str = ".") -> bool:
    """Return True if a remote is configured."""
    return get_remote_info(path) is not None


def get_conflicted_files(path: str = "."):
    """Return a list of files with merge conflicts."""
    if not is_git_repo(path):
        return []
    result = subprocess.run(
        ["git", "-C", path, "diff", "--name-only", "--diff-filter=U"],
        capture_output=True, text=True, check=False,
        encoding="utf-8", errors="replace",
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip().splitlines()
    return []


def get_ahead_behind(remote="origin", branch=None, path="."):
    """Return (ahead_count, behind_count) relative to remote tracking branch."""
    if not is_git_repo(path) or not has_remote(path):
        return 0, 0

    if not branch:
        branch = get_current_branch(path)
    if not branch:
        return 0, 0

    try:
        ahead_res = subprocess.run(
            ["git", "-C", path, "rev-list", "--count", f"{remote}/{branch}..HEAD"],
            capture_output=True, text=True, check=False,
            encoding="utf-8", errors="replace",
        )
        behind_res = subprocess.run(
            ["git", "-C", path, "rev-list", "--count", f"HEAD..{remote}/{branch}"],
            capture_output=True, text=True, check=False,
            encoding="utf-8", errors="replace",
        )
        ahead = int(ahead_res.stdout.strip()) if ahead_res.returncode == 0 and ahead_res.stdout.strip().isdigit() else 0
        behind = int(behind_res.stdout.strip()) if behind_res.returncode == 0 and behind_res.stdout.strip().isdigit() else 0
        return ahead, behind
    except Exception:
        return 0, 0


def get_repo_state_summary(path="."):
    """Return a short text summary of repository state for AI context."""
    if not is_git_repo(path):
        return "Not inside a Git repository."
    branch = get_current_branch(path) or "unknown branch"
    changes = "uncommitted changes present" if has_uncommitted_changes(path) else "clean working tree"
    remote = get_remote_info(path) or "no remote"
    return f"Repo: {get_repo_root(path)} Branch: {branch}; {changes}; remote: {remote}"


def get_working_tree_summary(path="."):
    """
    Return a dict with counts of staged, modified, and untracked files.
    Used to determine whether there's anything to commit.
    """
    result = {
        "staged": 0,
        "modified": 0,
        "untracked": 0,
    }

    if not is_git_repo(path):
        return result

    proc = subprocess.run(
        ["git", "-C", path, "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        return result

    for line in proc.stdout.splitlines():
        if not line or len(line) < 2:
            continue
        index_status = line[0]
        worktree_status = line[1]

        if index_status not in (" ", "?"):
            result["staged"] += 1
        if worktree_status == "M":
            result["modified"] += 1
        if line.startswith("??"):
            result["untracked"] += 1

    return result