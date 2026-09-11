"""Entry point for GitAssist."""

import sys
import os

# Fix Windows console encoding for Arabic paths and text
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from gitassist.cli import output
from gitassist.cli.input_handler import ask_input
from gitassist.git import repository
from gitassist.core.menu import show_main_menu
from gitassist.core import commands
from gitassist.core.suggestions import suggest_next_step
from gitassist.cli.language import choose_language
from gitassist.localization.texts import get_text


def choose_project() -> bool:
    """
    Present an initial project selection menu.
    Returns True if the user wants to continue with the current directory,
    False if they want to exit.
    """
    in_repo = repository.is_git_repo()

    output.print_title(get_text("project_selection_title"))

    options = []
    keys = []

    if in_repo:
        options.append(get_text("use_current_project"))
        keys.append("current")
    options.append(get_text("create_new_project"))
    keys.append("new")
    options.append(get_text("open_existing_project"))
    keys.append("open")
    options.append(get_text("clone_repository"))
    keys.append("clone")
    options.append(get_text("exit"))
    keys.append("exit")

    for i, opt in enumerate(options, start=1):
        print(f"{i}. {opt}")

    choice = ask_input(get_text("menu_prompt"), allow_empty=False)

    try:
        idx = int(choice) - 1
    except ValueError:
        output.print_error(get_text("please_enter_number"))
        return choose_project()

    if idx < 0 or idx >= len(options):
        output.print_error(get_text("invalid_choice"))
        return choose_project()

    selected_key = keys[idx]

    if selected_key == "exit":
        output.print_info(get_text("exit_message"))
        return False
    elif selected_key == "new":
        commands.create_new_project()
        return True
    elif selected_key == "open":
        commands.open_existing_project()
        return True
    elif selected_key == "clone":
        commands.clone_repository()
        return True

    # "current" — continue with the current directory
    return True


def main() -> int:
    output.print_banner()

    choose_language()

    if not repository.is_git_installed():
        output.print_error("git_not_installed")
        return 1

    output.print_success("git_installed")

    # Initial project selection — runs once at startup
    if not choose_project():
        return 0

    while True:
        action = show_main_menu()
        if action == "exit":
            output.print_info("exit_message")
            break
        elif action == "new":
            commands.create_new_project()
        elif action == "open":
            commands.open_existing_project()
        elif action == "clone":
            commands.clone_repository()
        elif action == "status":
            commands.show_status()
        elif action == "save":
            commands.save_changes()
        elif action == "log":
            commands.show_log()
        elif action == "branches":
            commands.manage_branches()
        elif action == "stash":
            commands.manage_stash()
        elif action == "files":
            commands.manage_files()
        elif action == "sync":
            commands.manage_sync()
        elif action == "github":
            commands.manage_github()
        elif action == "manual":
            commands.manual_command()
        elif action == "voice":
            try:
                from gitassist.cli.voice import start_voice_command
                start_voice_command()
            except Exception:
                output.print_error(get_text("voice_unavailable"))
                output.print_info(get_text("voice_install_hint"))
        elif action == "review":
            commands.show_status()
        else:
            output.print_error("invalid_choice")

        suggest_next_step()
        output.print_line()

    return 0


if __name__ == "__main__":
    sys.exit(main())