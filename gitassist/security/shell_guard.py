"""Guard raw command strings against shell command injection syntax.

GitAssist executes Git through ``subprocess.run(..., shell=False)``. This
module additionally rejects shell operators in the *unquoted* portions of
user/voice/AI text so a raw input represents one Git invocation rather than a
shell command line. Quoted arguments may legitimately contain characters
such as ``;`` or ``>``.
"""

from __future__ import annotations

import shlex

SHELL_METACHARACTERS = (";", "&&", "||", "|", "`", "$(", ">", "<", "\n")


def has_shell_metacharacters(text: str) -> bool:
    """Return True for shell operators outside single/double quotes."""
    if not text:
        return False
    quote = None
    escaped = False
    i = 0
    while i < len(text):
        ch = text[i]
        if escaped:
            escaped = False
            i += 1
            continue
        if quote == "'":
            if ch == "'":
                quote = None
            i += 1
            continue
        if quote == '"':
            if ch == "\\":
                escaped = True
            elif ch == '"':
                quote = None
            i += 1
            continue
        if ch == "'" or ch == '"':
            quote = ch
            i += 1
            continue
        if ch == "\\":
            escaped = True
            i += 1
            continue
        if ch == "\n" or ch in ";|><`&":
            return True
        if ch == "$" and i + 1 < len(text) and text[i + 1] == "(":
            return True
        i += 1
    return False


def safe_split(text: str):
    """Split a raw Git command without invoking a shell."""
    if has_shell_metacharacters(text):
        return [], "invalid_shell_syntax"
    try:
        tokens = shlex.split(text, posix=True)
    except ValueError:
        return [], "invalid_quoting"
    if not tokens:
        return [], "invalid_command"
    return tokens, ""
