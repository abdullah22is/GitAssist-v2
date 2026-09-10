"""
Repository dashboard rendering.

Builds the small text-box overview of repository state used when opening
a project and (optionally) at other points in the app. Read-only: this
module never modifies anything, and its one network-capable call (the
remote status) goes through the throttled monitor so opening a project
repeatedly does not repeatedly hit the network.
"""

from __future__ import annotations

from gitassist.git import repository
from gitassist.git import remote_monitor
from gitassist.localization.texts import get_text
from gitassist.config import settings


def _working_tree_label(summary: dict, lang: str) -> str:
    if summary["clean"]:
        return get_text("dashboard_working_clean", lang)
    parts = []
    if summary["staged"]:
        parts.append(get_text("dashboard_staged_count", lang, count=summary["staged"]))
    if summary["unstaged"]:
        parts.append(get_text("dashboard_unstaged_count", lang, count=summary["unstaged"]))
    if summary["untracked"]:
        parts.append(get_text("dashboard_untracked_count", lang, count=summary["untracked"]))
    return ", ".join(parts) if parts else get_text("dashboard_working_clean", lang)


def build_dashboard_lines(path: str = ".", lang: str = None, check_remote: bool = True) -> list:
    """Return the dashboard as a list of "label: value" lines (no box
    drawing), so callers can either print them plainly or wrap them in a
    box via render_dashboard_box()."""
    if lang is None:
        lang = settings.LANGUAGE

    lines = []
    root = repository.get_repo_root(path)
    lines.append(f"{get_text('dashboard_repository', lang)}: {root.rsplit('/', 1)[-1] if root else '-'}")
    lines.append(f"{get_text('dashboard_branch', lang)}: {repository.get_head_description(path) or '-'}")

    summary = repository.get_working_tree_summary(path)
    lines.append(f"{get_text('dashboard_working', lang)}: {_working_tree_label(summary, lang)}")

    if repository.has_remote(path):
        remote_url = repository.get_remote_info(path)
        upstream = repository.get_upstream_branch(path)
        lines.append(f"{get_text('dashboard_remote', lang)}: {remote_url}")
        lines.append(f"{get_text('dashboard_upstream', lang)}: {upstream or '-'}")
        if check_remote:
            status = remote_monitor.get_remote_status(path, force=False)
            status_key = "dashboard_status_" + status["status"]
            lines.append(f"{get_text('dashboard_status', lang)}: {get_text(status_key, lang)}")
    else:
        lines.append(f"{get_text('dashboard_remote', lang)}: {get_text('dashboard_no_remote', lang)}")

    return lines


def render_dashboard_box(path: str = ".", lang: str = None, check_remote: bool = True) -> str:
    if lang is None:
        lang = settings.LANGUAGE
    title = get_text("dashboard_title", lang)
    lines = build_dashboard_lines(path, lang, check_remote)
    width = max(len(title), max((len(l) for l in lines), default=0)) + 2
    box = [title]
    box.append("─" * width)
    box.extend(lines)
    box.append("─" * width)
    return "\n".join(box)
