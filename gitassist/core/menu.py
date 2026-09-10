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
            repo_name = os.path.basename(root)
            output.print_info(get_text("repo_detected"))
            output.print_info(get_text("current_branch", branch=get_current_branch() or get_text("no_branch")))
        else:
            output.print_info(get_text("repo_detected"))
        if has_changes:
            output.print_info(get_text("uncommitted_changes_yes"))
        else:
            output.print_info(get_text("uncommitted_changes_no"))
        if repository.has_remote():
            output.print_info(get_text("remote_configured", remote=repository.get_remote_info()))
        else:
            output.print_info(get_text("remote_not_configured"))
    else:
        output.print_info(get_text("repo_not_detected"))

    menu_items = []
    if not in_repo:
        menu_items = [
            (get_text("create_new_project"), "new"),
            (get_text("open_existing_project"), "open"),
            (get_text("clone_repository"), "clone"),
        ]
    else:
        menu_items = [
            (get_text("show_status"), "status"),
            (get_text("save_changes"), "save"),
            (get_text("view_history"), "log"),
            (get_text("manage_branches"), "branches"),
            (get_text("stash_changes"), "stash"),
            (get_text("manage_files"), "files"),
        ]
        if repository.has_remote():
            menu_items.append((get_text("synchronize"), "sync"))
            menu_items.append((get_text("github_info"), "github"))
        if has_changes:
            menu_items.insert(0, (get_text("uncommitted_changes_yes"), "review"))

    menu_items.append((get_text("exit"), "exit"))

    while True:
        for i, (text, _) in enumerate(menu_items, start=1):
            print(f"{i}. {text}")
        print("m. " + get_text("manual_command"))
        print("v. " + get_text("voice_command"))

        choice = ask_input(get_text("menu_prompt"), allow_empty=False)
        if choice.lower() == "m":
            return "manual"
        if choice.lower() == "v":
            return "voice"
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(menu_items):
                return menu_items[idx][1]
            else:
                output.print_error(get_text("invalid_choice"))
        except ValueError:
            output.print_error(get_text("please_enter_number"))