"""
Integration tests for gitassist.core.commands.open_existing_project and
gitassist.cli.dashboard, exercising all three real workflow branches:
a nonexistent path, an existing non-repo directory (offering init/clone),
and a valid repository (showing the dashboard and remote-appropriate menu).
"""

import os
import shutil
import subprocess
import tempfile
import unittest

from gitassist.core import commands
from gitassist.cli import dashboard


def _run(args, cwd):
    subprocess.run(["git"] + args, cwd=cwd, check=True, capture_output=True, text=True)


class TestOpenExistingProject(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gitassist-openflow-test-")
        self._prev_cwd = os.getcwd()

    def tearDown(self):
        os.chdir(self._prev_cwd)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _feed_inputs(self, values):
        it = iter(values)
        import builtins
        self._orig_input = builtins.input
        builtins.input = lambda *a: next(it)

    def _restore_input(self):
        import builtins
        builtins.input = self._orig_input

    def test_nonexistent_path_reports_clear_error(self):
        missing = os.path.join(self.tmp, "does-not-exist")
        self._feed_inputs([missing])
        try:
            commands.open_existing_project()  # must not raise
        finally:
            self._restore_input()
        self.assertFalse(os.path.exists(missing))

    def test_existing_non_repo_dir_offers_init_and_initializes_on_choice(self):
        plain = os.path.join(self.tmp, "plain")
        os.makedirs(plain)
        self._feed_inputs([plain, "1"])
        try:
            commands.open_existing_project()
        finally:
            self._restore_input()
        self.assertTrue(os.path.isdir(os.path.join(plain, ".git")))

    def test_existing_non_repo_dir_cancel_does_not_initialize(self):
        plain = os.path.join(self.tmp, "plain2")
        os.makedirs(plain)
        self._feed_inputs([plain, "0"])
        try:
            commands.open_existing_project()
        finally:
            self._restore_input()
        self.assertFalse(os.path.isdir(os.path.join(plain, ".git")))

    def test_valid_repo_with_no_remote_shows_dashboard_and_menu(self):
        repo = os.path.join(self.tmp, "repo")
        os.makedirs(repo)
        _run(["init", "-q"], repo)
        _run(["config", "user.email", "t@t.com"], repo)
        _run(["config", "user.name", "T"], repo)

        self._feed_inputs([repo, "0"])
        try:
            commands.open_existing_project()  # must not raise
        finally:
            self._restore_input()
        # os.chdir happens as a side effect of opening a valid repo
        self.assertEqual(os.path.realpath(os.getcwd()), os.path.realpath(repo))


class TestDashboardRendering(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gitassist-dashboard-test-")
        _run(["init", "-q"], self.tmp)
        _run(["config", "user.email", "t@t.com"], self.tmp)
        _run(["config", "user.name", "T"], self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_clean_repo_shows_clean_working_tree(self):
        with open(os.path.join(self.tmp, "f.txt"), "w") as f:
            f.write("x\n")
        _run(["add", "f.txt"], self.tmp)
        _run(["commit", "-q", "-m", "init"], self.tmp)
        box = dashboard.render_dashboard_box(self.tmp, check_remote=False)
        self.assertIn("CLEAN", box)

    def test_staged_and_untracked_are_both_reflected(self):
        with open(os.path.join(self.tmp, "staged.txt"), "w") as f:
            f.write("x\n")
        _run(["add", "staged.txt"], self.tmp)
        with open(os.path.join(self.tmp, "untracked.txt"), "w") as f:
            f.write("y\n")
        box = dashboard.render_dashboard_box(self.tmp, check_remote=False)
        self.assertIn("staged", box)
        self.assertIn("untracked", box)

    def test_no_remote_shown_when_none_configured(self):
        box = dashboard.render_dashboard_box(self.tmp, check_remote=False)
        self.assertTrue("none configured" in box or "غير مُعرَّف" in box)


if __name__ == "__main__":
    unittest.main()
