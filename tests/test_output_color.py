"""Tests for gitassist.cli.output color handling (section 17: must remain
usable in non-color terminals, CI, and redirected/piped output)."""

import io
import os
import unittest
from unittest.mock import patch

from gitassist.cli import output


class TestColorSuppression(unittest.TestCase):
    def setUp(self):
        self._env_backup = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._env_backup)

    def test_no_color_env_disables_color_even_if_tty(self):
        os.environ["NO_COLOR"] = "1"
        os.environ.pop("GITASSIST_FORCE_COLOR", None)
        with patch("sys.stdout.isatty", return_value=True):
            self.assertFalse(output._color_enabled())

    def test_non_tty_disables_color_by_default(self):
        os.environ.pop("NO_COLOR", None)
        os.environ.pop("GITASSIST_FORCE_COLOR", None)
        with patch("sys.stdout.isatty", return_value=False):
            self.assertFalse(output._color_enabled())

    def test_tty_enables_color_by_default(self):
        os.environ.pop("NO_COLOR", None)
        os.environ.pop("GITASSIST_FORCE_COLOR", None)
        with patch("sys.stdout.isatty", return_value=True):
            self.assertTrue(output._color_enabled())

    def test_force_color_overrides_non_tty(self):
        os.environ.pop("NO_COLOR", None)
        os.environ["GITASSIST_FORCE_COLOR"] = "1"
        with patch("sys.stdout.isatty", return_value=False):
            self.assertTrue(output._color_enabled())

    def test_messages_always_carry_a_plain_text_label(self):
        # Meaning must never depend on color alone - the bracketed label
        # must be present in the output regardless of color state.
        os.environ["NO_COLOR"] = "1"
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            output.print_success("welcome")
        self.assertIn("[SUCCESS]", buf.getvalue())

    def test_no_raw_escape_codes_when_color_disabled(self):
        os.environ["NO_COLOR"] = "1"
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            output.print_error("welcome")
        self.assertNotIn("\033[", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
