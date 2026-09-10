"""
Command safety analyzer - public entry point used by the executor.

This module is now a thin, backward-compatible wrapper around the real
structured parser (gitassist.security.parser) and the policy engine
(gitassist.security.policy). It replaces the previous implementation,
which matched regex patterns against a naively-joined command string and
could not see through Git global options like `-C`, `--git-dir`, or
`-c alias.foo='!cmd'`.
"""

from gitassist.security.parser import parse_git_command
from gitassist.security.policy import classify
from gitassist.security.risk import RiskLevel
from gitassist.localization.texts import get_text


def analyze_command_full(command_list, lang=None):
    """
    Parse + classify a full argv-style Git command.
    Returns (risk_level, warning_text, alternative_text, parsed).
    `parsed` is the ParsedGitCommand, useful for repository-context
    resolution (e.g. reading parsed.chdir for a `-C` override).
    """
    parsed = parse_git_command(command_list)
    level, warning_key, alternative_key = classify(parsed)
    warning = get_text(warning_key, lang) if warning_key else ""
    alternative = get_text(alternative_key, lang) if alternative_key else ""
    return level, warning, alternative, parsed


def analyze_command(command_list, lang=None):
    """Return (risk_level, warning_text, alternative_text).

    Kept for backward compatibility with existing callers/tests that only
    need the risk classification, not the parsed structure.
    """
    level, warning, alternative, _parsed = analyze_command_full(command_list, lang)
    return level, warning, alternative
