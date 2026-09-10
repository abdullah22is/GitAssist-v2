"""Tests for GitHub manager URL parsing."""

import unittest
from gitassist.github.manager import parse_remote_url


class TestRemoteParsing(unittest.TestCase):
    def test_https_github(self):
        provider, owner, repo = parse_remote_url("https://github.com/user/repo.git")
        self.assertEqual(provider, "github")
        self.assertEqual(owner, "user")
        self.assertEqual(repo, "repo")

    def test_ssh_github(self):
        provider, owner, repo = parse_remote_url("git@github.com:user/repo.git")
        self.assertEqual(provider, "github")
        self.assertEqual(owner, "user")
        self.assertEqual(repo, "repo")

    def test_invalid_url(self):
        result = parse_remote_url("not-a-url")
        self.assertEqual(result, (None, None, None))


if __name__ == "__main__":
    unittest.main()