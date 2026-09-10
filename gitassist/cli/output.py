"""Output formatting utilities for the CLI."""

import os
import sys
from gitassist.localization.texts import get_text
from gitassist.config import settings


def _color_enabled() -> bool:
    """
    Decide whether ANSI color codes should be emitted.

    Colors are disabled when output isn't a real terminal (redirected to
    a file, piped, or running in CI) or when the NO_COLOR convention
    (https://no-color.org/) is set - either way, raw escape codes in a
    log file or a non-ANSI terminal are noise, not decoration. Every
    message still carries a plain-text label ([INFO]/[ERROR]/etc.), so
    meaning is never conveyed by color alone.
    """
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("GITASSIST_FORCE_COLOR") is not None:
        return True
    try:
        return sys.stdout.isatty()
    except (AttributeError, ValueError):
        return False


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"


def _wrap(code: str, text: str) -> str:
    if not _color_enabled():
        return text
    return f"{code}{text}{Colors.RESET}"


def print_banner():
    line1 = "================================"
    line2 = f"        GitAssist v{settings.APP_VERSION}        "
    line3 = "   Smart & Safe Git Assistant   "
    print(_wrap(Colors.CYAN + Colors.BOLD, line1))
    print(_wrap(Colors.CYAN + Colors.BOLD, line2))
    print(_wrap(Colors.CYAN + Colors.BOLD, line3))
    print(_wrap(Colors.CYAN + Colors.BOLD, line1))


def print_info(message, lang=None, **kwargs):
    if lang is None:
        lang = settings.LANGUAGE
    text = get_text(message, lang, **kwargs)
    print(f"{_wrap(Colors.CYAN, '[INFO]')} {text}")


def print_success(message, lang=None, **kwargs):
    if lang is None:
        lang = settings.LANGUAGE
    text = get_text(message, lang, **kwargs)
    print(f"{_wrap(Colors.GREEN, '[SUCCESS]')} {text}")


def print_warning(message, lang=None, **kwargs):
    if lang is None:
        lang = settings.LANGUAGE
    text = get_text(message, lang, **kwargs)
    print(f"{_wrap(Colors.YELLOW, '[WARNING]')} {text}")


def print_error(message, lang=None, **kwargs):
    if lang is None:
        lang = settings.LANGUAGE
    text = get_text(message, lang, **kwargs)
    print(f"{_wrap(Colors.RED, '[ERROR]')} {text}")


def print_debug(message, debug=False):
    if debug:
        print(f"{_wrap(Colors.MAGENTA, '[DEBUG]')} {message}")


def print_title(title):
    print(_wrap(Colors.CYAN + Colors.BOLD, f"--- {title} ---"))


def print_line():
    print(_wrap(Colors.CYAN, "--------------------------------"))
