"""File management operations for GitAssist."""

import os
from gitassist.cli.output import print_error, print_success, print_warning
from gitassist.cli.input_handler import ask_input, ask_yes_no
from gitassist.localization.texts import get_text


def _is_outside_cwd(path: str) -> bool:
    """True if the resolved path escapes the current working directory
    tree - e.g. via '../..' or an absolute path elsewhere. Used only to
    surface a confirmation before a *destructive* operation; creating or
    editing files outside cwd is a legitimate thing to want and is not
    blocked, only flagged for delete."""
    try:
        resolved = os.path.realpath(path)
        cwd = os.path.realpath(os.getcwd())
        return os.path.commonpath([resolved, cwd]) != cwd
    except ValueError:
        # Different drives on Windows, or other incomparable paths.
        return True


def create_file():
    filename = ask_input(get_text("filename_prompt"), allow_empty=False)
    if os.path.exists(filename):
        print_error(get_text("file_exists_error", name=filename))
        return
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("")
        print_success(get_text("file_created", name=filename))
    except PermissionError as e:
        print_error(get_text("permission_denied_error", path=filename))
    except OSError as e:
        print_error(get_text("create_file_failed", name=filename, error=str(e)))


def edit_file():
    filename = ask_input(get_text("file_to_edit"), allow_empty=False)
    if not os.path.isfile(filename):
        print_error(get_text("file_not_found", name=filename))
        return
    line = ask_input(get_text("line_to_append"), allow_empty=False)
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        print_success(get_text("line_appended", name=filename))
    except PermissionError:
        print_error(get_text("permission_denied_error", path=filename))
    except OSError as e:
        print_error(get_text("edit_file_failed", name=filename, error=str(e)))


def delete_file():
    filename = ask_input(get_text("file_to_delete"), allow_empty=False)
    if not os.path.isfile(filename):
        print_error(get_text("file_not_found", name=filename))
        return

    if _is_outside_cwd(filename):
        print_warning(get_text("path_outside_cwd_warning", path=os.path.realpath(filename)))

    if ask_yes_no(get_text("delete_confirm", name=filename)):
        try:
            os.remove(filename)
            print_success(get_text("file_deleted", name=filename))
        except PermissionError:
            print_error(get_text("permission_denied_error", path=filename))
        except OSError as e:
            print_error(get_text("delete_file_failed", name=filename, error=str(e)))


def create_directory():
    dirname = ask_input(get_text("dirname_prompt"), allow_empty=False)
    if os.path.exists(dirname):
        print_error(get_text("file_exists_error", name=dirname))
        return
    try:
        os.makedirs(dirname)
        print_success(get_text("file_created", name=dirname))
    except PermissionError:
        print_error(get_text("permission_denied_error", path=dirname))
    except OSError as e:
        print_error(get_text("create_dir_failed", name=dirname, error=str(e)))
