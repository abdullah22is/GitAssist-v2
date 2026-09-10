"""Repository detection and state inspection."""

from __future__ import annotations

import subprocess

# Local, read-only plumbing queries (branch name, status, etc.) should
# never be able to hang the app - bound them defensively even though a
# real hang here would be unusual (e.g. a broken network-mounted repo).
_LOCAL_QUERY_TIMEOUT = 5


def _run(args, path=".", timeout=_LOCAL_QUERY_TIMEOUT):
    """Run a read-only git plumbing command, never raising on failure -
    returns a subprocess.CompletedProcess-like result with returncode=1
    and empty output on any error (timeout, missing git, permission,
    OS-level issue), so callers can use a single truthy/returncode check
    without each needing its own try/except."""
    try:
        return subprocess.run(
            ["git", "-C", path] + args,
            capture_output=True, text=True, check=False, timeout=timeout,
        )
    except (subprocess.TimeoutExpired, OSError, ValueError):
        class _Empty:
            returncode = 1
            stdout = ""
            stderr = ""
        return _Empty()


def is_git_installed() -> bool:
    """Return True if Git is installed and accessible."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True, timeout=_LOCAL_QUERY_TIMEOUT)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def is_git_repo(path: str = ".") -> bool:
    """Return True if the given path is inside a Git repository."""
    result = _run(["rev-parse", "--is-inside-work-tree"], path)
    return result.returncode == 0 and result.stdout.strip() == "true"


def get_repo_root(path: str = ".") -> str | None:
    """Return the absolute path of the repository root, or None if not a repo."""
    if not is_git_repo(path):
        return None
    result = _run(["rev-parse", "--show-toplevel"], path)
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def get_current_branch(path: str = ".") -> str | None:
    """Return the current branch name, or None if not available."""
    if not is_git_repo(path):
        return None
    result = _run(["branch", "--show-current"], path)
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def has_uncommitted_changes(path: str = ".") -> bool:
    """Return True if there are uncommitted changes in the working tree."""
    if not is_git_repo(path):
        return False
    result = _run(["status", "--porcelain"], path)
    return bool(result.stdout.strip())


def get_remote_info(path: str = ".") -> str | None:
    """Return the first remote URL if configured, else None."""
    if not is_git_repo(path):
        return None
    result = _run(["remote", "-v"], path)
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


def get_remote_url(remote="origin", path: str = ".") -> str | None:
    """Return the configured URL for a named remote without invoking a shell."""
    if not is_git_repo(path):
        return None
    result = _run(["config", "--get", f"remote.{remote}.url"], path)
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip().splitlines()[0]
    return None


def get_remote_uploadpack(remote="origin", path: str = ".") -> str | None:
    """Return a custom remote upload-pack helper, if configured."""
    if not is_git_repo(path):
        return None
    result = _run(["config", "--get", f"remote.{remote}.uploadpack"], path)
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip().splitlines()[0]
    return None


def get_upstream_branch(path: str = ".") -> str | None:
    """Return the configured upstream (e.g. 'origin/main') for the
    current branch, or None if the branch has no upstream set."""
    if not is_git_repo(path):
        return None
    result = _run(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], path)
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return None


def get_conflicted_files(path: str = "."):
    """Return a list of files with merge conflicts."""
    if not is_git_repo(path):
        return []
    result = _run(["diff", "--name-only", "--diff-filter=U"], path)
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

    ahead_res = _run(["rev-list", "--count", f"{remote}/{branch}..HEAD"], path)
    behind_res = _run(["rev-list", "--count", f"HEAD..{remote}/{branch}"], path)
    ahead = int(ahead_res.stdout.strip()) if ahead_res.returncode == 0 and ahead_res.stdout.strip().isdigit() else 0
    behind = int(behind_res.stdout.strip()) if behind_res.returncode == 0 and behind_res.stdout.strip().isdigit() else 0
    return ahead, behind


def get_head_description(path: str = ".") -> str | None:
    """Return the current branch name, or 'detached at <short-sha>' if
    HEAD is not on a branch. None if not a repository or HEAD is unborn."""
    if not is_git_repo(path):
        return None
    branch = get_current_branch(path)
    if branch:
        return branch
    result = _run(["rev-parse", "--short", "HEAD"], path)
    if result.returncode == 0 and result.stdout.strip():
        return f"detached at {result.stdout.strip()}"
    return None  # unborn HEAD (no commits yet)


def get_working_tree_summary(path: str = ".") -> dict:
    """
    Return {"staged": int, "unstaged": int, "untracked": int, "clean": bool}
    parsed from `git status --porcelain`, which uses an XY status pair per
    line: X is the index (staged) status, Y is the worktree status, and
    "??" marks an untracked file.
    """
    summary = {"staged": 0, "unstaged": 0, "untracked": 0, "clean": True}
    if not is_git_repo(path):
        return summary
    result = _run(["status", "--porcelain"], path)
    if result.returncode != 0:
        return summary
    for line in result.stdout.splitlines():
        if not line:
            continue
        code = line[:2]
        if code == "??":
            summary["untracked"] += 1
        else:
            if code[0] not in (" ", "?"):
                summary["staged"] += 1
            if code[1] not in (" ", "?"):
                summary["unstaged"] += 1
    summary["clean"] = summary["staged"] == 0 and summary["unstaged"] == 0 and summary["untracked"] == 0
    return summary


def get_repo_state_summary(path="."):
    """Return a short text summary of repository state for AI context."""
    if not is_git_repo(path):
        return "Not inside a Git repository."
    branch = get_current_branch(path) or "unknown branch"
    changes = "uncommitted changes present" if has_uncommitted_changes(path) else "clean working tree"
    remote = get_remote_info(path) or "no remote"
    return f"Repo: {get_repo_root(path)} Branch: {branch}; {changes}; remote: {remote}"
