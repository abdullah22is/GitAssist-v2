import os
import tempfile
import unittest
from unittest import mock

from gitassist.security.analyzer import analyze_command, analyze_command_full
from gitassist.security.risk import RiskLevel
from gitassist.security.shell_guard import safe_split
from gitassist.security.context import check_context


class TestSecurityHardeningExtra(unittest.TestCase):
    def test_force_with_lease_is_dangerous(self):
        level, _, _ = analyze_command(["git", "push", "--force-with-lease"])
        self.assertEqual(level, RiskLevel.DANGEROUS)

    def test_push_short_u_is_not_upload_pack(self):
        level, _, _ = analyze_command(["git", "push", "-u", "origin", "main"])
        self.assertEqual(level, RiskLevel.CAUTION)

    def test_clone_upload_pack_is_blocked(self):
        level, _, _ = analyze_command(["git", "clone", "-u", "/tmp/helper", "repo"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_fetch_upload_pack_is_blocked(self):
        level, _, _ = analyze_command(["git", "fetch", "--upload-pack=/tmp/helper", "origin"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_push_receive_pack_is_blocked(self):
        level, _, _ = analyze_command(["git", "push", "--receive-pack=/tmp/helper", "origin", "main"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_config_env_is_blocked(self):
        self.assertEqual(
            analyze_command(["git", "--config-env=core.pager=EVIL", "log"])[0],
            RiskLevel.BLOCKED,
        )

    def test_hooks_path_config_is_blocked(self):
        self.assertEqual(
            analyze_command(["git", "-c", "core.hooksPath=/tmp/hooks", "commit", "-m", "x"])[0],
            RiskLevel.BLOCKED,
        )

    def test_persistent_hooks_path_is_blocked(self):
        self.assertEqual(
            analyze_command(["git", "config", "core.hooksPath", "/tmp/hooks"])[0],
            RiskLevel.BLOCKED,
        )

    def test_commit_is_caution(self):
        self.assertEqual(analyze_command(["git", "commit", "-m", "x"])[0], RiskLevel.CAUTION)

    def test_quoted_shell_characters_are_allowed(self):
        parts, error = safe_split('git commit -m "fix; parser > safety"')
        self.assertEqual(error, "")
        self.assertEqual(parts[-1], "fix; parser > safety")

    def test_unquoted_shell_chain_is_rejected(self):
        parts, error = safe_split("git status; echo PWNED")
        self.assertEqual(parts, [])
        self.assertEqual(error, "invalid_shell_syntax")

    def test_context_uses_parsed_subcommand_for_dash_c(self):
        with tempfile.TemporaryDirectory() as td:
            import subprocess
            subprocess.run(["git", "init", "-q", td], check=True, capture_output=True)
            ok, warning, _ = check_context(["git", "-C", td, "push"], td)
            self.assertFalse(ok)
            self.assertIn("remote", warning.lower())


if __name__ == "__main__":
    unittest.main()


class TestUnknownExecutionVectors(unittest.TestCase):
    def test_unknown_subcommand_is_blocked_even_if_a_git_alias_exists(self):
        self.assertEqual(
            analyze_command(["git", "pwn"])[0], RiskLevel.BLOCKED
        )

    def test_unknown_subcommand_is_blocked_even_if_git_extension_exists(self):
        self.assertEqual(
            analyze_command(["git", "custom-helper"])[0], RiskLevel.BLOCKED
        )


class TestLoggerBoundaryRedaction(unittest.TestCase):
    def test_logger_formatter_redacts_secrets_at_sink(self):
        from gitassist.gitlog.logger import RedactingFormatter
        import logging
        formatter = RedactingFormatter("%(message)s")
        record = logging.LogRecord("test", logging.INFO, "", 0,
                                   "token=ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ12345", (), None)
        rendered = formatter.format(record)
        self.assertNotIn("ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ12345", rendered)
        self.assertIn("token=***", rendered)
