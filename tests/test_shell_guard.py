"""Tests for gitassist.security.shell_guard and its use in manual_command."""

import unittest

from gitassist.security.shell_guard import safe_split, has_shell_metacharacters


class TestShellGuard(unittest.TestCase):
    def test_quoted_commit_message_with_spaces(self):
        tokens, err = safe_split('git commit -m "fix: handle spaces correctly"')
        self.assertEqual(err, "")
        self.assertEqual(tokens, ["git", "commit", "-m", "fix: handle spaces correctly"])

    def test_arabic_path_with_spaces(self):
        tokens, err = safe_split('git add "ملف مهم.txt"')
        self.assertEqual(err, "")
        self.assertEqual(tokens, ["git", "add", "ملف مهم.txt"])

    def test_plain_command_still_splits_normally(self):
        tokens, err = safe_split("git status")
        self.assertEqual(err, "")
        self.assertEqual(tokens, ["git", "status"])

    def test_semicolon_chain_rejected(self):
        tokens, err = safe_split("git status; rm -rf /")
        self.assertEqual(tokens, [])
        self.assertEqual(err, "invalid_shell_syntax")

    def test_double_ampersand_chain_rejected(self):
        tokens, err = safe_split("git add . && git commit -m done")
        self.assertEqual(tokens, [])
        self.assertEqual(err, "invalid_shell_syntax")

    def test_pipe_rejected(self):
        tokens, err = safe_split("git log | less")
        self.assertEqual(tokens, [])
        self.assertEqual(err, "invalid_shell_syntax")

    def test_command_substitution_rejected(self):
        tokens, err = safe_split("git commit -m $(whoami)")
        self.assertEqual(tokens, [])
        self.assertEqual(err, "invalid_shell_syntax")

    def test_unmatched_quote_rejected(self):
        tokens, err = safe_split('git commit -m "unterminated')
        self.assertEqual(tokens, [])
        self.assertEqual(err, "invalid_quoting")

    def test_whitespace_only_input_does_not_crash(self):
        tokens, err = safe_split("   ")
        self.assertEqual(tokens, [])
        self.assertEqual(err, "invalid_command")

    def test_has_shell_metacharacters_detection(self):
        self.assertTrue(has_shell_metacharacters("a && b"))
        self.assertFalse(has_shell_metacharacters("git status"))


if __name__ == "__main__":
    unittest.main()
