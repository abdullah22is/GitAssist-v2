"""Tests for localization."""

import unittest
from gitassist.localization.texts import get_text
from gitassist.config import settings


class TestLocalization(unittest.TestCase):
    def setUp(self):
        self.original_lang = settings.LANGUAGE

    def tearDown(self):
        settings.LANGUAGE = self.original_lang

    def test_english_text(self):
        settings.LANGUAGE = "en"
        self.assertEqual(get_text("welcome"), "Welcome to GitAssist!")

    def test_arabic_text(self):
        settings.LANGUAGE = "ar"
        self.assertEqual(get_text("welcome"), "مرحبًا بك في GitAssist!")

    def test_missing_key_fallback(self):
        settings.LANGUAGE = "en"
        self.assertEqual(get_text("non_existent_key"), "non_existent_key")

    def test_formatting(self):
        settings.LANGUAGE = "en"
        self.assertEqual(get_text("current_branch", branch="main"), "Current branch: main")

    def test_all_used_keys_exist_in_both_languages(self):
        """
        Regression test for a real bug found in a security audit: 53 keys
        referenced across the codebase (including every dangerous-command
        warning in security/analyzer.py) were missing from TEXTS, silently
        falling back to raw key names being shown to the user.

        A prior test only checked that a warning/alternative string was
        truthy, which a raw fallback key name ("warning_reset_hard") also
        satisfies - so it never caught this. This test instead statically
        collects every key the code can possibly ask for and verifies each
        one is actually translated in both languages.
        """
        import ast
        import pathlib
        from gitassist.localization.texts import TEXTS
        from gitassist.security.policy import RULES
        from gitassist.errors.analyzer import ERROR_PATTERNS

        used_keys = set()

        # 1. Every literal key passed to get_text(...) or a print_* helper
        #    anywhere in the gitassist package.
        pkg_root = pathlib.Path(__file__).resolve().parent.parent / "gitassist"
        target_funcs = {"get_text", "print_info", "print_success", "print_warning", "print_error"}
        for path in pkg_root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id in target_funcs
                    and node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                ):
                    used_keys.add(node.args[0].value)

        # 2. Keys referenced dynamically rather than as a literal get_text(...)
        #    argument at the use site, which (1) cannot catch:
        #    - every (warning_key, alternative_key) pair in the security
        #      policy engine's rule table
        #    - every block_reason_key / parse_error_key the structured
        #      parser can produce
        #    - every explanation/suggestion key in the error analyzer
        for _predicate, _level, warning_key, alternative_key in RULES:
            if warning_key:
                used_keys.add(warning_key)
            if alternative_key:
                used_keys.add(alternative_key)
        # The parser's own blocked/parse-error keys (kept as a plain list
        # here rather than importing private constants, since these are
        # string literals baked into control flow, not a data table).
        used_keys.update({
            "blocked_not_git_invocation",
            "blocked_unrecognized_global_option",
            "blocked_exec_path",
            "blocked_alias_shell_escape",
            "blocked_exec_capable_config",
            "blocked_unsafe_transport",
            "blocked_upload_receive_pack",
            "blocked_generic",
            "parse_error_malformed_config",
            "parse_error_missing_value",
            "parse_error_no_subcommand",
        })
        for entry in ERROR_PATTERNS:
            used_keys.add(entry["explanation_key"])
            used_keys.add(entry["suggestion_key"])

        # shell_guard.safe_split() returns an error_key that callers pass
        # to get_text(error_key) as a variable, not a literal - invisible
        # to the AST scan above.
        used_keys.update({"invalid_shell_syntax", "invalid_quoting", "invalid_command"})

        # dashboard.py builds "dashboard_status_" + status["status"] where
        # status["status"] comes from remote_monitor's fixed set of
        # possible values - not a literal at the get_text() call site.
        used_keys.update({
            "dashboard_status_up_to_date", "dashboard_status_behind",
            "dashboard_status_ahead", "dashboard_status_diverged",
            "dashboard_status_offline", "dashboard_status_disabled",
            "dashboard_status_no_remote", "dashboard_status_not_a_repo",
        })

        # "non_existent_key" is intentionally used by test_missing_key_fallback
        # above to verify fallback behavior - it is supposed to be absent.
        used_keys.discard("non_existent_key")

        missing = sorted(k for k in used_keys if k not in TEXTS)
        self.assertEqual(missing, [], f"Missing localization keys: {missing}")

        incomplete = sorted(
            k for k in used_keys
            if k in TEXTS and not ({"en", "ar"} <= TEXTS[k].keys())
        )
        self.assertEqual(incomplete, [], f"Keys missing 'en' or 'ar' entry: {incomplete}")


if __name__ == "__main__":
    unittest.main()