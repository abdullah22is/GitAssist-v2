"""
Tests for gitassist.security.redaction and the GitHub manager's handling
of credentials-in-URLs and specific API error outcomes.

No real network calls are made - urllib.request.urlopen is mocked for
every HTTP-error scenario.
"""

import io
import socket
import unittest
import urllib.error
from unittest.mock import patch

from gitassist.security.redaction import redact, redact_command
from gitassist.github.manager import (
    create_github_repo,
    parse_remote_url,
    _redact_url_credentials,
)


class TestRedaction(unittest.TestCase):
    def test_https_url_with_user_and_token(self):
        out = redact("https://myuser:ghp_abcdEFGH12345678@github.com/x/y.git")
        self.assertNotIn("ghp_abcdEFGH12345678", out)
        self.assertNotIn("myuser", out)

    def test_https_url_with_bare_token(self):
        out = redact("https://ghp_abcdEFGH12345678@github.com/x/y.git")
        self.assertNotIn("ghp_abcdEFGH12345678", out)

    def test_authorization_bearer_header(self):
        out = redact("Authorization: Bearer sometoken.value.here")
        self.assertNotIn("sometoken.value.here", out)

    def test_github_token_prefix_anywhere_in_text(self):
        out = redact("failed while using ghp_1234567890abcdef for auth")
        self.assertNotIn("ghp_1234567890abcdef", out)

    def test_key_value_secret_pattern(self):
        out = redact("api_key=SUPERSECRETVALUE123 and other stuff")
        self.assertNotIn("SUPERSECRETVALUE123", out)

    def test_plain_text_untouched(self):
        self.assertEqual(redact("git status completed successfully"), "git status completed successfully")

    def test_none_and_empty_safe(self):
        self.assertEqual(redact(None), None)
        self.assertEqual(redact(""), "")

    def test_redact_command_joins_and_redacts(self):
        out = redact_command(["git", "clone", "https://user:pw12345678@host/repo.git"])
        self.assertNotIn("pw12345678", out)
        self.assertTrue(out.startswith("git clone"))


class TestGithubUrlCredentialRedaction(unittest.TestCase):
    def test_redact_url_credentials_helper(self):
        out = _redact_url_credentials("https://user:token123456@github.com/o/r.git")
        self.assertNotIn("token123456", out)

    def test_parse_remote_url_strips_credentials_before_matching_host(self):
        # Credentials embedded in the URL must not break provider
        # detection, and must never appear in the parsed output.
        provider, owner, repo = parse_remote_url("https://user:token@github.com/owner/repo.git")
        self.assertEqual(provider, "github")
        self.assertEqual(owner, "owner")
        self.assertEqual(repo, "repo")


class _FakeHTTPResponse:
    def __init__(self, status, body):
        self.status = status
        self._body = body

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class TestGithubApiErrorMapping(unittest.TestCase):
    def test_missing_token_rejected_before_any_network_call(self):
        clone_url, error_key = create_github_repo("", "my-repo")
        self.assertIsNone(clone_url)
        self.assertEqual(error_key, "github_error_no_token")

    def test_invalid_repo_name_rejected_before_any_network_call(self):
        clone_url, error_key = create_github_repo("tok", "not a valid name!")
        self.assertIsNone(clone_url)
        self.assertEqual(error_key, "github_error_invalid_repo_name")

    @patch("urllib.request.urlopen")
    def test_success(self, mock_urlopen):
        mock_urlopen.return_value = _FakeHTTPResponse(201, b'{"clone_url": "https://github.com/o/r.git"}')
        clone_url, error_key = create_github_repo("validtoken", "my-repo")
        self.assertEqual(clone_url, "https://github.com/o/r.git")
        self.assertEqual(error_key, "")

    @patch("urllib.request.urlopen")
    def test_invalid_token_maps_to_specific_key(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError("url", 401, "Unauthorized", {}, io.BytesIO(b""))
        clone_url, error_key = create_github_repo("badtoken", "my-repo")
        self.assertIsNone(clone_url)
        self.assertEqual(error_key, "github_error_invalid_token")

    @patch("urllib.request.urlopen")
    def test_rate_limit_or_forbidden_maps_to_specific_key(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError("url", 403, "Forbidden", {}, io.BytesIO(b""))
        clone_url, error_key = create_github_repo("tok", "my-repo")
        self.assertEqual(error_key, "github_error_rate_limited_or_forbidden")

    @patch("urllib.request.urlopen")
    def test_repo_conflict_maps_to_specific_key(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError("url", 422, "Unprocessable", {}, io.BytesIO(b""))
        clone_url, error_key = create_github_repo("tok", "my-repo")
        self.assertEqual(error_key, "github_error_repo_exists_or_invalid")

    @patch("urllib.request.urlopen")
    def test_timeout_maps_to_specific_key(self, mock_urlopen):
        mock_urlopen.side_effect = socket.timeout()
        clone_url, error_key = create_github_repo("tok", "my-repo")
        self.assertEqual(error_key, "github_error_timeout")

    @patch("urllib.request.urlopen")
    def test_network_error_maps_to_specific_key(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("DNS failure")
        clone_url, error_key = create_github_repo("tok", "my-repo")
        self.assertEqual(error_key, "github_error_network")


if __name__ == "__main__":
    unittest.main()
