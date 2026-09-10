"""Tests for gitassist.core.next_step."""

import os
import shutil
import subprocess
import tempfile
import unittest

from gitassist.core import next_step


def _run(args, cwd):
    subprocess.run(["git"] + args, cwd=cwd, check=True, capture_output=True, text=True)


class TestNextStepStatic(unittest.TestCase):
    def test_init_suggests_creating_files(self):
        self.assertTrue(next_step.suggest_after("init"))

    def test_clone_suggests_something(self):
        self.assertTrue(next_step.suggest_after("clone"))

    def test_add_suggests_commit(self):
        self.assertIn("commit", next_step.suggest_after("add").lower())

    def test_fetch_suggests_checking_status(self):
        self.assertTrue(next_step.suggest_after("fetch"))

    def test_conflicts_detected_suggests_resolution(self):
        self.assertTrue(next_step.suggest_after("conflicts_detected"))

    def test_unknown_action_returns_empty(self):
        self.assertEqual(next_step.suggest_after("something_made_up"), "")


class TestNextStepRemoteAwareness(unittest.TestCase):
    """The post-commit suggestion should differ depending on whether a
    remote is configured - push when there is one, add-a-remote when
    there isn't."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gitassist-nextstep-test-")
        _run(["init", "-q"], self.tmp)
        _run(["config", "user.email", "t@t.com"], self.tmp)
        _run(["config", "user.name", "T"], self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_commit_with_no_remote_suggests_adding_one(self):
        suggestion = next_step.suggest_after("commit", path=self.tmp)
        self.assertIn("remote", suggestion.lower())

    def test_commit_with_remote_suggests_push(self):
        _run(["remote", "add", "origin", "https://example.invalid/x/y.git"], self.tmp)
        suggestion = next_step.suggest_after("commit", path=self.tmp)
        self.assertIn("push", suggestion.lower())


if __name__ == "__main__":
    unittest.main()
