"""Intent analysis using AI or rule-based fallback."""

from gitassist.ai.assistant import suggest_git_command, is_available
from gitassist.ai.fallback import rule_based_intent


def interpret_user_input(text: str, repo_state: str = ""):
    """
    First try rule-based, then AI if enabled and available.
    Returns command string or None.
    """
    command = rule_based_intent(text, repo_state)
    if command:
        return command

    if is_available():
        return suggest_git_command(text, repo_state)

    return None