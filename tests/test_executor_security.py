"""
Executor-level security regression tests.

Unlike test_security_bypass.py (which tests the analyzer/parser/policy in
isolation), these tests exercise gitassist.git.executor.run_git_command
end-to-end against a real temporary Git repository, to catch bugs that
only show up in the full pipeline - e.g. the real bug this suite was
written to catch: `interactive=False` originally let DANGEROUS commands
execute with no confirmation of any kind, because the code only asked
for confirmation when interactive=True and otherwise fell straight
through to subprocess.run().
"""

import os
import shutil
import subprocess
import tempfile
import unittest

from gitassist.git.executor import run_git_command


def _fail_if_called(*args, **kwargs):
    raise AssertionError("ask_yes_no()/input() must not be called when interactive=False")


class TestExecutorFailsClosed(unittest.TestCase):
    def setUp(self):
        self.repo_dir = tempfile.mkdtemp(prefix="gitassist-exec-test-")
        subprocess.run(["git", "init", "-q"], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "config", "user.email", "t@t.com"], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "config", "user.name", "T"], cwd=self.repo_dir, check=True)
        with open(os.path.join(self.repo_dir, "f.txt"), "w") as f:
            f.write("hello\n")
        subprocess.run(["git", "add", "f.txt"], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=self.repo_dir, check=True)
        self._prev_cwd = os.getcwd()
        os.chdir(self.repo_dir)

    def tearDown(self):
        os.chdir(self._prev_cwd)
        shutil.rmtree(self.repo_dir, ignore_errors=True)

    def test_dangerous_command_with_interactive_false_is_refused_not_executed(self):
        with open("f.txt", "a") as f:
            f.write("uncommitted change\n")

        result = run_git_command(["git", "reset", "--hard"], interactive=False)

        self.assertIn(result, (False, None))
        with open("f.txt") as f:
            self.assertIn("uncommitted change", f.read(), "reset --hard ran despite interactive=False")

    def test_blocked_command_with_interactive_true_never_prompts_and_never_runs(self):
        import gitassist.git.executor as executor_module
        original_ask = executor_module.ask_yes_no
        executor_module.ask_yes_no = _fail_if_called
        try:
            marker = os.path.join(self.repo_dir, "PWNED")
            result = run_git_command(
                ["git", "-c", f"alias.pwn=!touch {marker}", "pwn"],
                interactive=True,
            )
            self.assertIn(result, (False, None))
            self.assertFalse(os.path.exists(marker), "blocked alias command actually ran")
        finally:
            executor_module.ask_yes_no = original_ask

    def test_safe_command_with_interactive_false_runs_without_prompting(self):
        import gitassist.git.executor as executor_module
        original_ask = executor_module.ask_yes_no
        executor_module.ask_yes_no = _fail_if_called
        try:
            result = run_git_command(["git", "status"], interactive=False, show_output=False)
            self.assertTrue(result)
        finally:
            executor_module.ask_yes_no = original_ask

    def test_dry_run_never_executes(self):
        from gitassist.config import settings
        original_dry_run = settings.DRY_RUN
        settings.DRY_RUN = True
        try:
            with open("f.txt", "a") as f:
                f.write("more uncommitted\n")
            run_git_command(["git", "reset", "--hard"], interactive=False)
            with open("f.txt") as f:
                self.assertIn("more uncommitted", f.read(), "dry-run actually executed reset --hard")
        finally:
            settings.DRY_RUN = original_dry_run


if __name__ == "__main__":
    unittest.main()
