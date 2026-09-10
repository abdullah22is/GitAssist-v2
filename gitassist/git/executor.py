"""Controlled execution of Git commands."""

from __future__ import annotations

import subprocess
from gitassist.cli.output import print_info, print_warning, print_error
from gitassist.cli.input_handler import ask_yes_no
from gitassist.security.analyzer import analyze_command_full
from gitassist.security.risk import risk_to_string, RiskLevel
from gitassist.errors.analyzer import analyze_error
from gitassist.security.context import check_context
from gitassist.security.redaction import redact, redact_command
from gitassist.config import settings
from gitassist.gitlog.logger import logger, log_security_event
from gitassist.localization.texts import get_text


def run_git_command(
    command: list[str],
    description: str = "",
    show_output: bool = True,
    interactive: bool = True,
    lang: str = None,
    capture_text: bool = False,
    timeout: float = None,
):
    """
    Execute a Git command safely using a list of arguments.

    Every command - whether typed manually, produced by the AI assistant,
    or triggered from a menu - passes through the same pipeline here:
    parse -> classify risk -> (refuse if BLOCKED) -> repository-context
    check -> user confirmation for anything not SAFE -> execute -> report.
    No caller can skip this by passing interactive=False for a BLOCKED
    command; only the confirmation step is skippable, never the block.

    interactive=False means "don't prompt", not "skip the safety check":
    if the command is anything other than SAFE (or the repository context
    is flagged as inappropriate) and interactive=False, the command is
    refused rather than silently executed, since there is no way to get
    the required confirmation. Only genuinely SAFE commands run without
    a prompt in non-interactive mode.

    `timeout` (seconds) bounds network-capable commands (fetch/pull/push/
    clone) so a dead connection can't hang the whole app - it surfaces as
    a normal failure, not a crash. Left as None (no timeout) for local
    commands, which have no reason to hang.

    Returns True/False as before, unless capture_text=True, in which case
    it returns the command's stdout (str) on success or None on failure/
    cancellation - kept opt-in and off by default so every existing caller
    keeps getting a bool exactly as before.
    """
    if lang is None:
        lang = settings.LANGUAGE

    safe_display = redact_command(command)

    risk_level, warning, alternative, parsed = analyze_command_full(command, lang)

    if risk_level == RiskLevel.BLOCKED:
        # No confirmation, no dry-run bypass, no interactive=False bypass.
        # A blocked command is never executed, full stop.
        print_error(get_text("blocked_command", lang, reason=warning or get_text("blocked_generic", lang)))
        log_security_event(f"BLOCKED command refused: {safe_display} - reason: {warning}")
        return None if capture_text else False

    target_path = parsed.resolved_path(".")
    is_appropriate, context_warning, context_alternative = check_context(command, target_path)

    if settings.DRY_RUN:
        print_info(get_text("dry_run_message", lang, command=safe_display))
        print_info(get_text("risk_level", lang, level=risk_to_string(risk_level)))
        if warning:
            print_warning(warning)
        if not is_appropriate:
            print_warning(context_warning)
            if context_alternative:
                print_info(context_alternative)
        logger.info(f"Dry-run: would execute: {safe_display} (risk={risk_to_string(risk_level)})")
        return True

    if description:
        print_info(description)

    if not is_appropriate:
        print_warning(context_warning)
        if context_alternative:
            print_info(context_alternative)
        if interactive:
            if not ask_yes_no(get_text("confirm_continue", lang)):
                print_info(get_text("command_cancelled", lang))
                logger.info(f"Command cancelled by user: {safe_display}")
                return None if capture_text else False
        else:
            # No way to obtain confirmation - fail closed rather than
            # silently proceeding with a context the analyzer flagged.
            log_security_event(f"Refused (no confirmation available, context issue): {safe_display}")
            return None if capture_text else False

    if risk_level != RiskLevel.SAFE:
        print_warning(get_text("risk_level", lang, level=risk_to_string(risk_level)))
        if warning:
            print_warning(warning)
        if alternative:
            print_info(get_text("safer_alternative", lang, alternative=alternative))

        if interactive:
            if not ask_yes_no(get_text("confirm_continue", lang)):
                print_info(get_text("command_cancelled", lang))
                logger.info(f"Command cancelled by user: {safe_display}")
                return None if capture_text else False
        else:
            # Same fail-closed rule: a CAUTION/DANGEROUS command with no
            # interactive confirmation available must not run silently.
            log_security_event(f"Refused (no confirmation available, risk={risk_to_string(risk_level)}): {safe_display}")
            return None if capture_text else False
        if risk_level == RiskLevel.DANGEROUS:
            log_security_event(f"DANGEROUS command confirmed and executed: {safe_display}")

    logger.info(f"Executing command: {safe_display}")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
        if result.returncode == 0:
            if show_output and result.stdout:
                print(result.stdout)
            logger.info(f"Command succeeded: {safe_display}")
            return result.stdout if capture_text else True
        else:
            print_error(get_text("command_failed", lang, command=safe_display))
            safe_stderr = redact(result.stderr)
            if safe_stderr:
                print(safe_stderr)
            explanation = analyze_error(result.stderr)
            if explanation:
                print_info(explanation)
            logger.error(f"Command failed: {safe_display} - {safe_stderr}")
            return None if capture_text else False
    except subprocess.TimeoutExpired:
        print_error(get_text("command_timed_out", lang, command=safe_display))
        logger.error(f"Command timed out after {timeout}s: {safe_display}")
        return None if capture_text else False
    except Exception as exc:
        print_error(get_text("unexpected_error", lang, error=redact(str(exc))))
        logger.error(f"Exception while executing {safe_display}: {redact(str(exc))}")
        return None if capture_text else False
