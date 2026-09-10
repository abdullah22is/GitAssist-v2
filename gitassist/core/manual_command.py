"""Manual command entry mode with safe parsing, typo detection and AI support."""

import difflib
from gitassist.cli.output import print_info, print_warning, print_error, print_title
from gitassist.cli.input_handler import ask_input, ask_yes_no
from gitassist.git.executor import run_git_command
from gitassist.localization.texts import get_text
from gitassist.ai.intent import interpret_user_input
from gitassist.git.repository import get_repo_state_summary
from gitassist.security.shell_guard import safe_split

COMMON_COMMANDS = [
    "status", "init", "add", "commit", "log", "branch", "checkout",
    "switch", "merge", "stash", "pull", "push", "fetch", "clone", "remote"
]


def suggest_correction(user_cmd):
    """Suggest a correction for a mistyped Git subcommand using parsed argv."""
    parts, error_key = safe_split(user_cmd)
    if error_key or not parts or parts[0] != "git" or len(parts) < 2:
        return None
    subcmd = parts[1]
    closest = difflib.get_close_matches(subcmd, COMMON_COMMANDS, n=1, cutoff=0.7)
    if closest and closest[0] != subcmd:
        parts[1] = closest[0]
        # Rebuild only for display; execution reparses the final string.
        import shlex
        return " ".join(shlex.quote(p) if any(c.isspace() for c in p) else p for p in parts)
    return None


def execute_text_command(command_str):
    """Process a text command from manual entry, voice, or another input source."""
    initial_parts, initial_error = safe_split(command_str)
    is_git_command = not initial_error and initial_parts and initial_parts[0] == "git"

    if not is_git_command:
        print_info(get_text("interpreting"))
        suggestion = interpret_user_input(command_str, get_repo_state_summary())
        if suggestion:
            print_info(get_text("ai_suggestion", command=suggestion))
            if ask_yes_no(get_text("execute_suggested")):
                command_str = suggestion
            else:
                return
        else:
            if initial_error:
                print_error(get_text(initial_error))
            else:
                print_error(get_text("invalid_command"))
            return

    suggested = suggest_correction(command_str)
    if suggested:
        print_warning(get_text("typo_detected"))
        print_info(get_text("you_entered", command=command_str))
        print_info(get_text("did_you_mean", suggestion=suggested))
        if ask_yes_no(get_text("execute_corrected")):
            command_str = suggested

    parts, error_key = safe_split(command_str)
    if error_key:
        print_error(get_text(error_key))
        return
    command_list = parts if parts[0] == "git" else ["git"] + parts
    # The executor is the final security authority. AI/manual input cannot
    # bypass parsing, policy, context checks, confirmation, or redaction.
    return run_git_command(command_list, get_text("executing_manual"))


def manual_command_mode():
    """Handle manual Git command entry."""
    print_title(get_text("manual_mode_title"))
    command_str = ask_input(get_text("enter_git_command"), allow_empty=False)
    return execute_text_command(command_str)
