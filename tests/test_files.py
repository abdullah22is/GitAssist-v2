"""Tests for gitassist.core.files (section 21: file operations audit)."""

import builtins
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from gitassist.core import files


class TestFileOperations(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gitassist-files-test-")
        self._prev_cwd = os.getcwd()
        os.chdir(self.tmp)

    def tearDown(self):
        os.chdir(self._prev_cwd)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _feed(self, values):
        it = iter(values)
        return patch("builtins.input", lambda *a: next(it))

    def test_create_file_creates_and_reports_success(self):
        with self._feed(["newfile.txt"]):
            files.create_file()
        self.assertTrue(os.path.isfile("newfile.txt"))

    def test_create_file_existing_reports_localized_error_not_english_fstring(self):
        open("exists.txt", "w").close()
        with self._feed(["exists.txt"]):
            with patch("gitassist.core.files.print_error") as mock_err:
                files.create_file()
        # The error call must use a localization key + kwargs, not a
        # pre-formatted raw f-string like "Failed to create file: ...".
        args, kwargs = mock_err.call_args
        self.assertNotIn("Failed to create file:", args[0])

    def test_permission_denied_uses_dedicated_message(self):
        open("locked.txt", "w").close()
        with self._feed(["locked.txt", "some text"]):
            with patch("builtins.open", side_effect=PermissionError("denied")):
                with patch("gitassist.core.files.print_error") as mock_err:
                    files.edit_file()
        mock_err.assert_called_once()
        args, kwargs = mock_err.call_args
        self.assertIn("locked.txt", args[0])
        self.assertIn("ermission", args[0])  # "Permission denied" (en) - case-insensitive-ish check

    def test_delete_nonexistent_file_reports_not_found(self):
        with self._feed(["ghost.txt"]):
            with patch("gitassist.core.files.print_error") as mock_err:
                files.delete_file()
        args, kwargs = mock_err.call_args
        self.assertIn("ghost.txt", args[0])

    def test_delete_file_inside_cwd_does_not_warn(self):
        open("inside.txt", "w").close()
        with self._feed(["inside.txt", "y"]):
            with patch("gitassist.core.files.print_warning") as mock_warn:
                files.delete_file()
        mock_warn.assert_not_called()
        self.assertFalse(os.path.exists("inside.txt"))

    def test_delete_file_outside_cwd_warns_before_confirming(self):
        outside_dir = tempfile.mkdtemp(prefix="gitassist-outside-")
        outside_file = os.path.join(outside_dir, "outside.txt")
        open(outside_file, "w").close()
        try:
            with self._feed([outside_file, "n"]):  # decline the delete
                with patch("gitassist.core.files.print_warning") as mock_warn:
                    files.delete_file()
            mock_warn.assert_called_once()
            args, kwargs = mock_warn.call_args
            self.assertIn("outside", args[0].lower())
            self.assertTrue(os.path.exists(outside_file), "file should not be deleted when user declines")
        finally:
            shutil.rmtree(outside_dir, ignore_errors=True)

    def test_create_directory_success(self):
        with self._feed(["newdir"]):
            files.create_directory()
        self.assertTrue(os.path.isdir("newdir"))


if __name__ == "__main__":
    unittest.main()
