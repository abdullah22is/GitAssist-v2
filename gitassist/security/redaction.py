"""
Secret redaction.

Applied to anything that reaches a log file or the terminal that might
contain credentials: command argv, subprocess stdout/stderr, and remote
URLs. This is best-effort defense-in-depth, not a guarantee - it cannot
redact a secret it doesn't recognize the shape of.
"""

from __future__ import annotations

import re

_PATTERNS = [
    # https://user:TOKEN@host/... or https://TOKEN@host/...
    (re.compile(r"(https?://)([^/@\s:]+):([^/@\s]+)@"), r"\1***:***@"),
    (re.compile(r"(https?://)([^/@\s:]{8,})@"), r"\1***@"),
    # Authorization / Bearer headers
    (re.compile(r"(?i)(authorization\s*[:=]\s*)(bearer|token)\s+\S+"), r"\1\2 ***"),
    (re.compile(r"(?i)(bearer\s+)[a-z0-9._\-]+", re.IGNORECASE), r"\1***"),
    # GitHub / common vendor token prefixes
    (re.compile(r"\b(ghp|gho|ghu|ghs|ghr|github_pat)_[A-Za-z0-9_]{10,}\b"), r"\1_***"),
    # key=value style secrets in args/env/config
    (re.compile(r"(?i)\b((?:api[_-]?key|token|password|passwd|secret)\s*[:=]\s*)\S+"), r"\1***"),
]


def redact(text: str) -> str:
    """Return `text` with recognizable secrets masked. Safe on None/empty."""
    if not text:
        return text
    out = text
    for pattern, repl in _PATTERNS:
        out = pattern.sub(repl, out)
    return out


def redact_command(command_list) -> str:
    """Join and redact an argv-style command for safe display/logging."""
    return redact(" ".join(command_list))
