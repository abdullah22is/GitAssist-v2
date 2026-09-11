"""Interactive CLI menu for GitAssist."""

import os

from gitassist.cli import output
from gitassist.cli.input_handler import ask_input
from gitassist.git import repository
from gitassist.git.repository import get_repo_root, get_current_branch
from gitassist.localization.texts import get_text


def show_main_menu():
    """Show the main dynamic menu based on repository state."""

    output.print_title(get_text("main_menu_title"))

    in_repo = repository.is_git_repo()
    has_changes = repository.has_uncommitted_changes() if in_repo else False

    if in_repo:
        root = get_repo_root()

        if root:
            output.print_info(get_text("repo_detected"))
            output.print_info(
                get_text(
                    "current_branch",
                    branch=get_current_branch() or get_text("no_branch"),
                )
            )
        else:
            output.print_info(get_text("repo_detected"))

        if has_changes:
            output.print_info(get_text("uncommitted_changes_yes"))
        else:
            output.print_info(get_text("uncommitted_changes_no"))

        if repository.has_remote():
            output.print_info(
                get_text("remote_configured", remote=repository.get_remote_info())
            )
        else:
            output.print_info(get_text("remote_not_configured"))

    else:
        output.print_info(get_text("repo_not_detected"))

    # Each item: (display label, internal action, actual Git command)
    if not in_repo:
        menu_items = [
            (get_text("create_new_project"), "new", "git init"),
            (get_text("open_existing_project"), "open", "open local repo"),
            (get_text("clone_repository"), "clone", "git clone <url>"),
        ]
    else:
        menu_items = [
            (get_text("show_status"), "status", "git status"),
            (get_text("stage_changes"), "stage", "git add"),
            (get_text("commit_changes"), "commit", "git commit"),
            (get_text("view_history"), "log", "git log"),
            (get_text("manage_branches"), "branches", "git branch / switch / merge"),
            (get_text("stash_changes"), "stash", "git stash"),
            (get_text("manage_files"), "files", "filesystem"),
        ]

        if repository.has_remote():
            menu_items.append(
                (get_text("synchronize"), "sync", "git fetch / pull / push")
            )
            menu_items.append(
                (get_text("github_info"), "github", "GitHub API / remote")
            )

        if has_changes:
            menu_items.insert(
                0,
                (get_text("review_changes"), "review", "git status"),
            )

    menu_items.append((get_text("exit"), "exit", "exit"))

    while True:
        print()

        for index, (text, _action, git_command) in enumerate(menu_items, start=1):
            print(f"{index}. {text} ({git_command})")

        print("m. " + get_text("manual_command") + " (manual git command)")
        print("v. " + get_text("voice_command") + " (voice command)")

        choice = ask_input(get_text("menu_prompt"), allow_empty=False)

        if choice.lower() == "m":
            return "manual"
        if choice.lower() == "v":
            return "voice"

        try:
            index = int(choice) - 1
            if 0 <= index < len(menu_items):
                return menu_items[index][1]
            output.print_error(get_text("invalid_choice"))
        except ValueError:
            output.print_error(get_text("please_enter_number"))