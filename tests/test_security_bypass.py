"""
Security regression tests: bypass attempts against the risk/policy engine.

These are the exact bypass attempts enumerated in the project's own
security specification. None of them may ever be classified as SAFE by
gitassist.security.analyzer.analyze_command - most must be BLOCKED
outright (config/alias/transport-based code execution vectors), the rest
must be DANGEROUS/CAUTION (destructive Git operations reached through a
different argument shape than the original regex expected).
"""

import unittest

from gitassist.security.analyzer import analyze_command, analyze_command_full
from gitassist.security.risk import RiskLevel


class TestGlobalOptionBypass(unittest.TestCase):
    """git -C/--git-dir/--work-tree must not let a destructive command
    hide behind a redirected repository context."""

    def test_dash_C_reset_hard(self):
        level, _, _ = analyze_command(["git", "-C", "/tmp", "reset", "--hard"])
        self.assertEqual(level, RiskLevel.DANGEROUS)

    def test_git_dir_reset_hard(self):
        level, _, _ = analyze_command(["git", "--git-dir=/tmp/.git", "reset", "--hard"])
        self.assertEqual(level, RiskLevel.DANGEROUS)

    def test_work_tree_reset_hard(self):
        level, _, _ = analyze_command(["git", "--work-tree=/tmp", "reset", "--hard"])
        self.assertEqual(level, RiskLevel.DANGEROUS)

    def test_context_resolves_to_the_dash_C_path(self):
        _, _, _, parsed = analyze_command_full(["git", "-C", "/tmp/other-repo", "status"])
        self.assertEqual(parsed.resolved_path(), "/tmp/other-repo")


class TestConfigInjectionBypass(unittest.TestCase):
    """`-c alias.x='!cmd'` and similar exec-capable config must never be
    SAFE, regardless of how harmless the alias name looks."""

    def test_alias_pwn_shell_escape_is_blocked(self):
        level, _, _ = analyze_command(["git", "-c", "alias.pwn=!command", "pwn"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_alias_printf_shell_escape_is_blocked(self):
        level, _, _ = analyze_command(["git", "-c", "alias.foo=!printf PWNED", "foo"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_glued_short_form_alias_escape_is_blocked(self):
        level, _, _ = analyze_command(["git", "-calias.pwn=!id", "pwn"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_persistent_config_alias_escape_is_blocked(self):
        level, _, _ = analyze_command(["git", "config", "alias.pwn", "!id"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_core_pager_override_is_blocked(self):
        level, _, _ = analyze_command(["git", "-c", "core.pager=curl evil.example", "log"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_credential_helper_override_is_blocked(self):
        level, _, _ = analyze_command(["git", "-c", "credential.helper=!steal", "status"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_harmless_config_override_is_not_blocked(self):
        # Sanity check: a config key with no execution capability must
        # NOT be over-blocked. user.name is a plain data field.
        level, _, _ = analyze_command(["git", "-c", "user.name=Someone", "status"])
        self.assertEqual(level, RiskLevel.SAFE)


class TestExecPathAndTransportBypass(unittest.TestCase):
    def test_exec_path_is_blocked(self):
        level, _, _ = analyze_command(["git", "--exec-path=/tmp/evil-bin", "status"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_ext_transport_clone_is_blocked(self):
        level, _, _ = analyze_command(["git", "clone", "ext::sh -c touch /tmp/pwned", "dest"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_upload_pack_is_blocked(self):
        level, _, _ = analyze_command(
            ["git", "clone", "--upload-pack=touch /tmp/pwned", "/tmp/some-repo", "dest"]
        )
        self.assertEqual(level, RiskLevel.BLOCKED)


class TestKnownDestructiveCommands(unittest.TestCase):
    """The exact destructive-command list from the security spec - none
    of these may be SAFE."""

    DESTRUCTIVE_COMMANDS = [
        ["git", "push", "-f"],
        ["git", "push", "--force"],
        ["git", "clean", "-fd"],
        ["git", "clean", "-fdx"],
        ["git", "restore", "."],
        ["git", "checkout", "--", "."],
        ["git", "reset", "--hard"],
        ["git", "rebase", "-i"],
        ["git", "branch", "-D", "feature"],
    ]

    def test_none_are_safe(self):
        for cmd in self.DESTRUCTIVE_COMMANDS:
            with self.subTest(cmd=cmd):
                level, warning, _ = analyze_command(cmd)
                self.assertNotEqual(level, RiskLevel.SAFE, f"{cmd} was classified SAFE")
                self.assertIn(level, (RiskLevel.CAUTION, RiskLevel.DANGEROUS, RiskLevel.BLOCKED))
                self.assertTrue(warning, f"{cmd} produced no warning text")

    def test_force_with_lease_is_still_flagged(self):
        # A safer flag than --force, but still a push and still requires
        # confirmation - must not silently become SAFE.
        level, _, _ = analyze_command(["git", "push", "--force-with-lease"])
        self.assertNotEqual(level, RiskLevel.SAFE)


class TestUnknownCommandsNeverAutoSafe(unittest.TestCase):
    def test_unknown_subcommand_is_blocked(self):
        level, _, _ = analyze_command(["git", "totally-made-up-subcommand", "--whatever"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_unrecognized_global_option_is_blocked_not_safe(self):
        level, _, _ = analyze_command(["git", "--some-unknown-global-flag", "status"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_non_git_invocation_is_blocked(self):
        level, _, _ = analyze_command(["bash", "-c", "echo hi"])
        self.assertEqual(level, RiskLevel.BLOCKED)


class TestCommandParsingEdgeCases(unittest.TestCase):
    """Argument-shape edge cases the parser must handle without crashing
    or silently doing the wrong thing."""

    def test_empty_command_list(self):
        level, _, _ = analyze_command([])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_git_with_no_subcommand(self):
        level, _, _ = analyze_command(["git"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_dash_C_missing_value(self):
        level, _, _ = analyze_command(["git", "-C"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_malformed_dash_c_missing_equals(self):
        level, _, _ = analyze_command(["git", "-c", "not-a-kv-pair", "status"])
        self.assertEqual(level, RiskLevel.BLOCKED)

    def test_arabic_and_unicode_paths_do_not_crash(self):
        level, _, _ = analyze_command(["git", "add", "ملف_عربي.txt", "café.txt"])
        self.assertEqual(level, RiskLevel.SAFE)

    def test_path_with_spaces_as_single_argv_token(self):
        # Since we always operate on an already-split argv list (never a
        # shell string), a path with spaces is just one list element and
        # must not confuse the parser into treating it as two arguments.
        level, _, _ = analyze_command(["git", "add", "my file with spaces.txt"])
        self.assertEqual(level, RiskLevel.SAFE)


if __name__ == "__main__":
    unittest.main()
