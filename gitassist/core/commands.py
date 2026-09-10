"""Basic Git command handlers for GitAssist."""

import os
import re

from gitassist.cli import output
from gitassist.cli.input_handler import ask_input, ask_yes_no
from gitassist.git import repository
from gitassist.git import branches as branch_ops
from gitassist.git import stash as stash_ops
from gitassist.git import sync as sync_ops
from gitassist.git.executor import run_git_command
from gitassist.core.manual_command import manual_command_mode
from gitassist.core import files as file_ops
from gitassist.github import manager as github_manager
from gitassist.localization.texts import get_text


def create_new_project():
    name = ask_input(get_text("project_name_prompt"))
    if not name:
        output.print_warning(get_text("input_empty"))
        return

    base_path = ask_input(get_text("location_prompt"), allow_empty=True)
    project_path = os.path.join(base_path, name) if base_path else name

    if os.path.exists(project_path):
        output.print_error(get_text("path_exists_error", path=project_path))
        return

    os.makedirs(project_path)
    os.chdir(project_path)

    success = run_git_command(["git", "init"], get_text("initialize_repo"))
    if success:
        output.print_success(get_text("repo_initialized"))

        if ask_yes_no(get_text("create_readme_prompt")):
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(f"# {name}\n")
            run_git_command(["git", "add", "README.md"], get_text("staging_readme"))
            run_git_command(["git", "commit", "-m", "Initial commit"], get_text("creating_commit"))
            output.print_success(get_text("initial_commit_created"))

        if ask_yes_no(get_text("add_remote_prompt")):
            url = ask_input(get_text("remote_url_prompt"))
            run_git_command(["git", "remote", "add", "origin", url], get_text("adding_remote"))


def open_existing_project():
    path = ask_input(get_text("project_path_prompt"))
    if not repository.is_git_repo(path):
        output.print_error(get_text("not_git_repo_error"))
        return

    os.chdir(path)
    output.print_success(get_text("opened_project", path=path))


def clone_repository():
    url = ask_input(get_text("clone_url_prompt"))
    if not url:
        output.print_warning(get_text("input_empty"))
        return

    dest = ask_input(get_text("clone_dest_prompt"), allow_empty=True)
    cmd = ["git", "clone", url]
    if dest:
        cmd.append(dest)

    success = run_git_command(cmd, get_text("cloning_repo"))
    if success:
        output.print_success(get_text("clone_completed"))
        if not dest:
            match = re.search(r"/([^/]+?)(\.git)?$", url)
            if match:
                dest = match.group(1)
        if dest and ask_yes_no(get_text("open_cloned_prompt")):
            if os.path.exists(dest):
                os.chdir(dest)
                output.print_info(get_text("changed_to", path=dest))


def show_status():
    run_git_command(["git", "status"], get_text("fetching_status"))


def save_changes():
    if not repository.has_uncommitted_changes():
        output.print_info(get_text("uncommitted_changes_no"))
        return

    add_all = ask_yes_no(get_text("save_changes_prompt"))
    if add_all:
        run_git_command(["git", "add", "."], get_text("staging_all"))
    else:
        file = ask_input(get_text("file_to_stage"))
        run_git_command(["git", "add", file], get_text("staging_file", file=file))

    message = ask_input(get_text("commit_message_prompt"))
    if not message:
        output.print_warning(get_text("input_empty"))
        return
    run_git_command(["git", "commit", "-m", message], get_text("committing_changes"))


def show_log():
    run_git_command(["git", "log", "--oneline", "--graph", "--decorate", "--all"], get_text("fetching_history"))


def manage_branches():
    while True:
        output.print_title(get_text("branch_management"))
        print("1. " + get_text("list_branches"))
        print("2. " + get_text("create_branch"))
        print("3. " + get_text("switch_branch"))
        print("4. " + get_text("delete_branch"))
        print("5. " + get_text("merge_branch"))
        print("0. " + get_text("back_to_main"))

        choice = ask_input(get_text("menu_prompt"), allow_empty=False)

        if choice == "1":
            branch_ops.list_branches()
        elif choice == "2":
            name = ask_input(get_text("new_branch_name"))
            if name:
                if branch_ops.create_branch(name):
                    output.print_success(get_text("branch_created", name=name))
        elif choice == "3":
            name = ask_input(get_text("branch_to_switch"))
            if name:
                if branch_ops.switch_branch(name):
                    output.print_success(get_text("branch_switched", name=name))
        elif choice == "4":
            name = ask_input(get_text("branch_to_delete"))
            if name:
                if branch_ops.is_current_branch(name):
                    output.print_error(get_text("cannot_delete_current_branch"))
                    output.print_info(get_text("switch_first_hint"))
                elif branch_ops.is_branch_in_use(name):
                    output.print_error(get_text("branch_in_use_error", name=name))
                    output.print_info(get_text("prune_worktree_hint"))
                else:
                    force = ask_yes_no(get_text("confirm_force_delete"), default=False)
                    if branch_ops.delete_branch(name, force):
                        output.print_success(get_text("branch_deleted", name=name))
        elif choice == "5":
            name = ask_input(get_text("branch_to_merge"))
            if name:
                if ask_yes_no(get_text("confirm_merge", name=name)):
                    if branch_ops.merge_branch(name):
                        output.print_success(get_text("merge_success"))
        elif choice == "0":
            break
        else:
            output.print_error(get_text("invalid_choice"))
        output.print_line()


def manage_stash():
    while True:
        output.print_title(get_text("stash_management"))
        print("1. " + get_text("stash_save"))
        print("2. " + get_text("stash_list"))
        print("3. " + get_text("stash_apply"))
        print("4. " + get_text("stash_pop"))
        print("5. " + get_text("stash_drop"))
        print("0. " + get_text("back_to_main"))

        choice = ask_input(get_text("menu_prompt"), allow_empty=False)

        if choice == "1":
            message = ask_input(get_text("stash_message_prompt"), allow_empty=True)
            if stash_ops.save_stash(message):
                output.print_success(get_text("changes_stashed"))
        elif choice == "2":
            if stash_ops.has_stashes():
                stash_ops.list_stashes()
            else:
                output.print_info(get_text("no_stashes"))
        elif choice == "3":
            if not stash_ops.has_stashes():
                output.print_info(get_text("no_stashes"))
            else:
                if stash_ops.apply_stash():
                    output.print_success(get_text("stash_applied"))
        elif choice == "4":
            if not stash_ops.has_stashes():
                output.print_info(get_text("no_stashes"))
            else:
                if stash_ops.pop_stash():
                    output.print_success(get_text("stash_popped"))
        elif choice == "5":
            if not stash_ops.has_stashes():
                output.print_info(get_text("no_stashes"))
            else:
                if ask_yes_no(get_text("confirm_drop_stash")):
                    if stash_ops.drop_stash():
                        output.print_success(get_text("stash_dropped"))
        elif choice == "0":
            break
        else:
            output.print_error(get_text("invalid_choice"))
        output.print_line()


def manage_files():
    while True:
        output.print_title(get_text("file_management"))
        print("1. " + get_text("create_file"))
        print("2. " + get_text("edit_file"))
        print("3. " + get_text("delete_file"))
        print("4. " + get_text("create_directory"))
        print("0. " + get_text("back_to_main"))

        choice = ask_input(get_text("menu_prompt"), allow_empty=False)

        if choice == "1":
            file_ops.create_file()
        elif choice == "2":
            file_ops.edit_file()
        elif choice == "3":
            file_ops.delete_file()
        elif choice == "4":
            file_ops.create_directory()
        elif choice == "0":
            break
        else:
            output.print_error(get_text("invalid_choice"))
        output.print_line()


def manage_sync():
    while True:
        output.print_title(get_text("synchronize"))
        print("1. " + get_text("sync_fetch"))
        print("2. " + get_text("sync_pull"))
        print("3. " + get_text("sync_push"))
        print("4. " + get_text("check_updates"))
        print("0. " + get_text("back_to_main"))

        choice = ask_input(get_text("menu_prompt"), allow_empty=False)

        if choice == "1":
            if sync_ops.fetch():
                output.print_success(get_text("fetch_completed"))
        elif choice == "2":
            if sync_ops.pull():
                output.print_success(get_text("pull_completed"))
                conflicts = repository.get_conflicted_files()
                if conflicts:
                    output.print_warning(get_text("conflicts_detected"))
                    for f in conflicts:
                        print(f"  - {f}")
                    output.print_info(get_text("resolve_conflicts"))
            else:
                # Pull failed - possibly due to unrelated histories
                if ask_yes_no(get_text("allow_unrelated_prompt"), default=False):
                    if sync_ops.pull(allow_unrelated=True):
                        output.print_success(get_text("pull_completed"))
                        conflicts = repository.get_conflicted_files()
                        if conflicts:
                            output.print_warning(get_text("conflicts_detected"))
                            for f in conflicts:
                                print(f"  - {f}")
                            output.print_info(get_text("resolve_conflicts"))
        elif choice == "3":
            if sync_ops.push():
                output.print_success(get_text("push_completed"))
        elif choice == "4":
            if sync_ops.has_remote_updates():
                output.print_warning(get_text("behind_remote"))
            else:
                output.print_success(get_text("up_to_date"))
        elif choice == "0":
            break
        else:
            output.print_error(get_text("invalid_choice"))
        output.print_line()
def manage_github():
    while True:
        output.print_title(get_text("github_management"))
        print("1. " + get_text("show_remote_details"))
        print("2. " + get_text("open_browser"))
        print("3. " + get_text("create_github_repo"))
        print("0. " + get_text("back_to_main"))

        choice = ask_input(get_text("menu_prompt"), allow_empty=False)

        if choice == "1":
            github_manager.show_remote_details()
        elif choice == "2":
            github_manager.open_repo_in_browser()
        elif choice == "3":
            token = ask_input(get_text("github_token_prompt"))
            repo_name = ask_input(get_text("github_repo_name_prompt"))
            private = ask_yes_no(get_text("github_private_prompt"))
            clone_url = github_manager.create_github_repo(token, repo_name, private)
            if clone_url:
                output.print_success(get_text("github_repo_created", url=clone_url))
                if ask_yes_no(get_text("add_remote_prompt")):
                    run_git_command(["git", "remote", "add", "origin", clone_url], get_text("adding_remote"))
            else:
                output.print_error(get_text("github_failed"))
        elif choice == "0":
            break
        else:
            output.print_error(get_text("invalid_choice"))
        output.print_line()


def manual_command():
    manual_command_mode()