"""
Throttled remote update monitor.

Design constraints (see project security spec, section 13):
- Never fetch on every command; only when the configured interval has
  elapsed since the last check (persisted across runs in a small cache
  file), or when the caller explicitly forces a check.
- A fetch has a hard timeout; a stuck/offline connection degrades to a
  clear "couldn't reach remote" status, never a hang or a crash.
- This module only *reports* ahead/behind/diverged - it never pulls,
  merges, rebases, resets, or otherwise touches the working tree.
"""

from __future__ import annotations

import json
import os
import time

from gitassist.config import settings
from gitassist.git import repository
from gitassist.git.executor import run_git_command


def _load_cache() -> dict:
    try:
        with open(settings.REMOTE_CHECK_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _save_cache(cache: dict) -> None:
    try:
        with open(settings.REMOTE_CHECK_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    except OSError:
        pass  # Best-effort - a monitor that can't cache should not crash.


def _repo_key(path: str) -> str:
    root = repository.get_repo_root(path) or os.path.abspath(path)
    return root


def get_remote_status(path: str = ".", remote: str = "origin", force: bool = False) -> dict:
    """
    Return a status dict describing the remote update situation:

        {
            "checked": bool,       # did we actually talk to the network this call?
            "status": str,         # "up_to_date" | "behind" | "ahead" | "diverged" |
                                    # "no_remote" | "not_a_repo" | "offline" | "disabled" |
                                    # "cached" | "unsafe_remote"
            "ahead": int, "behind": int,
            "remote": str, "branch": str or None,
            "last_checked": float or None,   # unix timestamp
        }

    Never raises. Never modifies the working tree or any ref.
    """
    if not repository.is_git_repo(path):
        return {"checked": False, "status": "not_a_repo", "ahead": 0, "behind": 0,
                "remote": remote, "branch": None, "last_checked": None}

    remote_url = repository.get_remote_url(remote, path)
    if not remote_url:
        return {"checked": False, "status": "no_remote", "ahead": 0, "behind": 0,
                "remote": remote, "branch": repository.get_current_branch(path), "last_checked": None}

    # The monitor is automatic, so refuse transports/configuration that can
    # turn a fetch into execution of a local helper. The interactive command
    # parser separately blocks explicit ext::/fd:: and upload-pack options.
    if remote_url.lower().startswith(("ext::", "fd::")):
        return {"checked": False, "status": "unsafe_remote", "ahead": 0, "behind": 0,
                "remote": remote, "branch": repository.get_current_branch(path), "last_checked": None}
    if repository.get_remote_uploadpack(remote, path):
        return {"checked": False, "status": "unsafe_remote", "ahead": 0, "behind": 0,
                "remote": remote, "branch": repository.get_current_branch(path), "last_checked": None}

    branch = repository.get_current_branch(path)
    key = _repo_key(path)
    cache = _load_cache()
    entry = cache.get(key, {})
    now = time.time()
    last_checked = entry.get("last_checked")

    if not settings.REMOTE_CHECK_ENABLED:
        return {"checked": False, "status": "disabled", "ahead": 0, "behind": 0,
                "remote": remote, "branch": branch, "last_checked": last_checked}

    due = force or last_checked is None or (now - last_checked) >= settings.REMOTE_CHECK_INTERVAL_SECONDS

    if not due:
        ahead, behind = entry.get("ahead", 0), entry.get("behind", 0)
        return {"checked": False, "status": _classify(ahead, behind, cached=True),
                "ahead": ahead, "behind": behind, "remote": remote, "branch": branch,
                "last_checked": last_checked}

    # A fetch is a network operation, so it must be strictly read-only
    # (no merge/pull) and bounded by a timeout. Target `path` explicitly
    # via -C rather than relying on cwd, since callers may query the
    # status of a repository other than the current directory.
    fetch_ok = run_git_command(
        ["git", "-C", path, "fetch", remote],
        show_output=False,
        interactive=False,
        timeout=settings.REMOTE_CHECK_TIMEOUT_SECONDS,
    )

    if not fetch_ok:
        # Offline, timed out, or auth failure - report what we knew
        # before, clearly labeled as possibly stale, rather than
        # crashing or retrying aggressively.
        ahead, behind = entry.get("ahead", 0), entry.get("behind", 0)
        return {"checked": False, "status": "offline", "ahead": ahead, "behind": behind,
                "remote": remote, "branch": branch, "last_checked": last_checked}

    ahead, behind = repository.get_ahead_behind(remote, branch, path)
    cache[key] = {"last_checked": now, "ahead": ahead, "behind": behind}
    _save_cache(cache)

    return {"checked": True, "status": _classify(ahead, behind, cached=False),
            "ahead": ahead, "behind": behind, "remote": remote, "branch": branch,
            "last_checked": now}


def _classify(ahead: int, behind: int, cached: bool) -> str:
    if ahead > 0 and behind > 0:
        return "diverged"
    if behind > 0:
        return "behind"
    if ahead > 0:
        return "ahead"
    return "up_to_date"


def render_status_box(status: dict, lang: str = None) -> str:
    """Render a small text dashboard box for a get_remote_status() result."""
    from gitassist.localization.texts import get_text
    from gitassist.config import settings as _settings
    if lang is None:
        lang = _settings.LANGUAGE

    title = get_text("remote_status_title", lang)
    lines = []
    kind = status["status"]

    if kind == "not_a_repo":
        lines.append(get_text("remote_status_not_a_repo", lang))
    elif kind == "no_remote":
        lines.append(get_text("remote_status_no_remote", lang))
    elif kind == "disabled":
        lines.append(get_text("remote_status_disabled", lang))
    elif kind == "unsafe_remote":
        lines.append(get_text("remote_status_unsafe_remote", lang))
    else:
        lines.append(f"{get_text('remote_status_remote', lang)}: {status['remote']}")
        lines.append(f"{get_text('remote_status_branch', lang)}: {status['branch'] or '-'}")
        if kind == "up_to_date":
            lines.append(get_text("remote_status_up_to_date", lang, remote=status["remote"], branch=status["branch"]))
        elif kind == "behind":
            lines.append(get_text("remote_status_behind", lang, remote=status["remote"], branch=status["branch"], behind=status["behind"]))
        elif kind == "ahead":
            lines.append(get_text("remote_status_ahead", lang, remote=status["remote"], branch=status["branch"], ahead=status["ahead"]))
        elif kind == "diverged":
            lines.append(get_text("remote_status_diverged", lang, remote=status["remote"], branch=status["branch"], ahead=status["ahead"], behind=status["behind"]))
        elif kind == "offline":
            lines.append(get_text("remote_status_offline", lang))
        if not status.get("checked", False) and kind not in ("offline", "disabled", "no_remote", "not_a_repo"):
            lines.append(get_text("remote_status_cached_note", lang))

    width = max(len(title), max((len(l) for l in lines), default=0)) + 2
    box = ["┌─ " + title + " " + "─" * max(0, width - len(title) - 3) + "┐"]
    for l in lines:
        box.append("│ " + l.ljust(width - 2) + " │")
    box.append("└" + "─" * width + "┘")
    return "\n".join(box)
