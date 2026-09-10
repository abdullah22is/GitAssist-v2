"""Context-aware command checking."""

from gitassist.git import repository
from gitassist.security.parser import parse_git_command
from gitassist.localization.texts import get_text


def check_context(command_list, path="."):
    """
    Return (is_appropriate, warning_text, alternative_text).

    `path` is the actual repository location the command targets - the
    caller is responsible for resolving this from any -C/--git-dir/
    --work-tree global options (see gitassist.security.parser), so that
    redirecting the command at a different repository can't skip these
    checks.
    """
    parsed = parse_git_command(command_list)
    if parsed.blocked or not parsed.ok:
        return False, get_text("blocked_generic"), ""

    subcommand = parsed.subcommand

    if not repository.is_git_repo(path):
        # init/clone are specifically designed to work outside an existing
        # work tree. Everything else needs a valid repository context.
        if subcommand in ("init", "clone"):
            return True, "", ""
        return False, get_text("warning_not_git_repo"), get_text("suggestion_init_or_clone")

    # Context checks use the parsed subcommand, never raw string prefixes.
    # This means `git -C /repo merge feature` receives the same checks as
    # `git merge feature`.
    if subcommand in ("merge", "pull") and repository.has_uncommitted_changes(path):
        return False, get_text("warning_uncommitted_changes"), get_text("suggestion_commit_or_stash")

    if subcommand == "push" and not repository.get_remote_info(path):
        return False, get_text("warning_no_remote"), get_text("suggestion_add_remote")

    if subcommand == "pull" and not repository.get_remote_info(path):
        return False, get_text("warning_no_remote"), get_text("suggestion_add_remote")

    return True, "", ""