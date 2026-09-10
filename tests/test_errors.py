"""Tests for error analyzer."""

import unittest
from gitassist.errors.analyzer import analyze_error


class TestErrorAnalyzer(unittest.TestCase):
    def test_not_git_repo(self):
        explanation = analyze_error("fatal: not a git repository")
        self.assertIn("Git repository", explanation)

    def test_push_rejected(self):
        explanation = analyze_error("error: failed to push some refs")
        self.assertIn("remote contains commits", explanation)

    def test_unknown_error(self):
        explanation = analyze_error("some unknown error")
        self.assertEqual(explanation, "")

    def test_no_upstream_branch(self):
        explanation = analyze_error(
            "fatal: The current branch feature has no upstream branch.\n"
            "To push the current branch and set the remote as upstream, use\n"
            "    git push --set-upstream origin feature"
        )
        self.assertIn("upstream", explanation.lower())

    def test_unmerged_files_block_pull(self):
        explanation = analyze_error("error: Pulling is not possible because you have unmerged files.")
        self.assertIn("conflict", explanation.lower())


if __name__ == "__main__":
    unittest.main()