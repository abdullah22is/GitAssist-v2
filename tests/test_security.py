"""Tests for security analyzer."""

import unittest
from gitassist.security.analyzer import analyze_command
from gitassist.security.risk import RiskLevel


class TestSecurityAnalyzer(unittest.TestCase):
    def test_safe_command(self):
        level, _, _ = analyze_command(["git", "status"])
        self.assertEqual(level, RiskLevel.SAFE)

    def test_dangerous_reset_hard(self):
        level, warning, alternative = analyze_command(["git", "reset", "--hard"])
        self.assertEqual(level, RiskLevel.DANGEROUS)
        self.assertTrue(warning)
        self.assertTrue(alternative)

    def test_caution_merge(self):
        level, _, _ = analyze_command(["git", "merge", "feature"])
        self.assertEqual(level, RiskLevel.CAUTION)

    def test_force_push_dangerous(self):
        level, _, _ = analyze_command(["git", "push", "--force", "origin", "main"])
        self.assertEqual(level, RiskLevel.DANGEROUS)


if __name__ == "__main__":
    unittest.main()