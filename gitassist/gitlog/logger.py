"""Secure logging setup for GitAssist.

All application log messages pass through a redacting formatter as a final
line of defense. Callers should still redact values before logging, but the
logger itself must not become a secret-exfiltration sink.
"""

from __future__ import annotations

import logging
import os
import stat
from gitassist.config import settings
from gitassist.security.redaction import redact


class RedactingFormatter(logging.Formatter):
    """Formatter that masks recognized secrets from every log record."""

    def format(self, record):
        return redact(super().format(record))


logger = logging.getLogger("gitassist")
logger.propagate = False
if not logger.handlers:
    logger.setLevel(logging.INFO)
    log_dir = os.path.dirname(settings.LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler(settings.LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        RedactingFormatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)

try:
    # Best-effort owner-only permissions on POSIX platforms.
    if os.path.exists(settings.LOG_FILE):
        os.chmod(settings.LOG_FILE, stat.S_IRUSR | stat.S_IWUSR)
except OSError:
    pass


def log_security_event(message: str) -> None:
    """Write a distinct security event; formatter performs final redaction."""
    logger.warning(f"[SECURITY] {redact(message)}")
