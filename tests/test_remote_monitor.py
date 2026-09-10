"""
Integration tests for gitassist.git.remote_monitor.

Uses a real local bare repository as the "remote" (never touches any
real network or the user's actual repositories), matching the project's
testing requirement to simulate remotes with local bare repos.
"""

import os
import shutil
import subprocess
import tempfile
import unittest

from gitassist.git import remote_monitor
from gitassist.config import settings


def _run(args, cwd):
    subprocess.run(["git"] + args, cwd=cwd, check=True, capture_output=True, text=True)


class TestRemoteMonitor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gitassist-remote-test-")
        self.bare_dir = os.path.join(self.tmp, "remote.git")
        self.work_dir = os.path.join(self.tmp, "work")
        self.clone_dir = os.path.join(self.tmp, "clone")

        os.makedirs(self.work_dir)
        _run(["init", "-q"], self.work_dir)
        _run(["config", "user.email", "t@t.com"], self.work_dir)
        _run(["config", "user.name", "T"], self.work_dir)
        with open(os.path.join(self.work_dir, "f.txt"), "w") as f:
            f.write("one\n")
        _run(["add", "f.txt"], self.work_dir)
        _run(["commit", "-q", "-m", "first"], self.work_dir)

        _run(["init", "-q", "--bare", self.bare_dir], self.tmp)
        _run(["remote", "add", "origin", self.bare_dir], self.work_dir)
        # Push and set upstream in one step so ahead/behind tracking works.
        _run(["push", "-u", "origin", "HEAD:refs/heads/main"], self.work_dir)
        _run(["checkout", "-q", "-B", "main"], self.work_dir)
        # The bare repo's HEAD symref still defaults to refs/heads/master,
        # which doesn't exist (only "main" was ever pushed) - fix it up
        # so `git clone` checks out "main" instead of warning and leaving
        # an unborn, disconnected "master" branch.
        _run(["symbolic-ref", "HEAD", "refs/heads/main"], self.bare_dir)

        _run(["clone", "-q", self.bare_dir, self.clone_dir], self.tmp)
        _run(["config", "user.email", "t@t.com"], self.clone_dir)
        _run(["config", "user.name", "T"], self.clone_dir)

        self._prev_cache_file = settings.REMOTE_CHECK_CACHE_FILE
        settings.REMOTE_CHECK_CACHE_FILE = os.path.join(self.tmp, "cache.json")
        self._prev_interval = settings.REMOTE_CHECK_INTERVAL_SECONDS
        self._prev_cwd = os.getcwd()

    def tearDown(self):
        os.chdir(self._prev_cwd)
        settings.REMOTE_CHECK_CACHE_FILE = self._prev_cache_file
        settings.REMOTE_CHECK_INTERVAL_SECONDS = self._prev_interval
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_up_to_date_immediately_after_clone(self):
        status = remote_monitor.get_remote_status(self.clone_dir, force=True)
        self.assertEqual(status["status"], "up_to_date")
        self.assertEqual(status["behind"], 0)
        self.assertEqual(status["ahead"], 0)

    def test_detects_behind_after_new_commit_pushed_upstream(self):
        with open(os.path.join(self.work_dir, "f.txt"), "a") as f:
            f.write("two\n")
        _run(["add", "f.txt"], self.work_dir)
        _run(["commit", "-q", "-m", "second"], self.work_dir)
        _run(["push", "origin", "main"], self.work_dir)

        status = remote_monitor.get_remote_status(self.clone_dir, force=True)
        self.assertEqual(status["status"], "behind")
        self.assertEqual(status["behind"], 1)

    def test_detects_ahead_when_local_has_unpushed_commit(self):
        with open(os.path.join(self.clone_dir, "g.txt"), "w") as f:
            f.write("local only\n")
        _run(["add", "g.txt"], self.clone_dir)
        _run(["commit", "-q", "-m", "local commit"], self.clone_dir)

        status = remote_monitor.get_remote_status(self.clone_dir, force=True)
        self.assertEqual(status["status"], "ahead")
        self.assertEqual(status["ahead"], 1)


    def test_unsafe_transport_is_never_auto_fetched(self):
        unsafe_dir = os.path.join(self.tmp, "unsafe")
        os.makedirs(unsafe_dir)
        _run(["init", "-q"], unsafe_dir)
        _run(["config", "remote.origin.url", "ext::printf PWNED"], unsafe_dir)
        status = remote_monitor.get_remote_status(unsafe_dir, force=True)
        self.assertEqual(status["status"], "unsafe_remote")
        self.assertFalse(status["checked"])

    def test_no_remote_reports_cleanly(self):
        no_remote_dir = os.path.join(self.tmp, "lonely")
        os.makedirs(no_remote_dir)
        _run(["init", "-q"], no_remote_dir)
        status = remote_monitor.get_remote_status(no_remote_dir, force=True)
        self.assertEqual(status["status"], "no_remote")

    def test_not_a_repo_reports_cleanly(self):
        not_a_repo = os.path.join(self.tmp, "plain_dir")
        os.makedirs(not_a_repo)
        status = remote_monitor.get_remote_status(not_a_repo, force=True)
        self.assertEqual(status["status"], "not_a_repo")

    def test_disabled_setting_skips_network_entirely(self):
        original = settings.REMOTE_CHECK_ENABLED
        settings.REMOTE_CHECK_ENABLED = False
        try:
            status = remote_monitor.get_remote_status(self.clone_dir, force=True)
            self.assertEqual(status["status"], "disabled")
            self.assertFalse(status["checked"])
        finally:
            settings.REMOTE_CHECK_ENABLED = original

    def test_throttling_skips_network_on_second_call(self):
        settings.REMOTE_CHECK_INTERVAL_SECONDS = 300
        first = remote_monitor.get_remote_status(self.clone_dir, force=True)
        self.assertTrue(first["checked"])

        # A new commit appears upstream, but the interval hasn't elapsed
        # and force=False - the throttle should serve the cached result
        # (still "up_to_date") instead of fetching again.
        with open(os.path.join(self.work_dir, "f.txt"), "a") as f:
            f.write("three\n")
        _run(["add", "f.txt"], self.work_dir)
        _run(["commit", "-q", "-m", "third"], self.work_dir)
        _run(["push", "origin", "main"], self.work_dir)

        second = remote_monitor.get_remote_status(self.clone_dir, force=False)
        self.assertFalse(second["checked"])
        self.assertEqual(second["status"], "up_to_date")

    def test_force_bypasses_throttle(self):
        settings.REMOTE_CHECK_INTERVAL_SECONDS = 300
        remote_monitor.get_remote_status(self.clone_dir, force=True)

        with open(os.path.join(self.work_dir, "f.txt"), "a") as f:
            f.write("four\n")
        _run(["add", "f.txt"], self.work_dir)
        _run(["commit", "-q", "-m", "fourth"], self.work_dir)
        _run(["push", "origin", "main"], self.work_dir)

        forced = remote_monitor.get_remote_status(self.clone_dir, force=True)
        self.assertTrue(forced["checked"])
        self.assertEqual(forced["status"], "behind")

    def test_render_status_box_does_not_crash_for_every_status_kind(self):
        for status in ("not_a_repo", "no_remote", "disabled", "up_to_date", "behind", "ahead", "diverged", "offline"):
            box = remote_monitor.render_status_box({
                "checked": False, "status": status, "ahead": 1, "behind": 2,
                "remote": "origin", "branch": "main", "last_checked": None,
            })
            self.assertIsInstance(box, str)
            self.assertGreater(len(box), 0)


if __name__ == "__main__":
    unittest.main()
