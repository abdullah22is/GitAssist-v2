"""Input handling utilities for GitAssist CLI."""

import getpass
from gitassist.localization.texts import get_text
from gitassist.cli.output import print_error
from gitassist.config import settings


def ask_yes_no(prompt: str, default: bool = False, lang: str = None) -> bool:
    if lang is None:
        lang = settings.LANGUAGE
    suffix = " [Y/n] " if default else " [y/N] "
    while True:
        answer = input(prompt + suffix).strip().lower()
        if not answer:
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print_error(get_text("invalid_choice", lang))


def ask_input(prompt: str, allow_empty: bool = False, lang: str = None) -> str:
    if lang is None:
        lang = settings.LANGUAGE
    while True:
        value = input(prompt + " ").strip()
        if value or allow_empty:
            return value
        print_error(get_text("input_empty", lang))


def ask_secret(prompt: str, allow_empty: bool = False, lang: str = None) -> str:
    """
    Like ask_input, but for tokens/passwords: uses getpass so the value
    is never echoed to the terminal (and therefore never ends up in a
    terminal scrollback buffer or session recording).

    Falls back to a plain (visible) prompt only if getpass can't attach
    to a real terminal (e.g. input is piped/redirected in a test or CI
    context) - getpass itself raises in that case rather than silently
    echoing, so this is a deliberate, narrow fallback, not a silent
    downgrade of security in normal interactive use.
    """
    if lang is None:
        lang = settings.LANGUAGE
    while True:
        try:
            value = getpass.getpass(prompt + " ").strip()
        except EOFError:
            value = input(prompt + " ").strip()
        if value or allow_empty:
            return value
        print_error(get_text("input_empty", lang))