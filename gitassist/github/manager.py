"""GitHub/Git remote URL parsing and information extraction."""

import re
import json
import socket
import urllib.request
import urllib.error
import webbrowser
from gitassist.git import repository
from gitassist.cli import output
from gitassist.localization.texts import get_text
from gitassist.security.redaction import redact
from gitassist.gitlog.logger import logger, log_security_event

API_TIMEOUT_SECONDS = 10


def _redact_url_credentials(url: str) -> str:
    """Never display or log credentials embedded in a remote URL
    (https://user:token@host/... or https://token@host/...)."""
    return redact(url)


def parse_remote_url(url: str):
    if not url:
        return None, None, None

    https_match = re.match(r"https?://([^/]+)/([^/]+)/([^/]+?)(?:\.git)?/?$", url)
    if https_match:
        host = https_match.group(1)
        # A URL can carry credentials as user:pass@host - strip them
        # before treating the remainder as the hostname.
        host = host.split("@")[-1]
        owner = https_match.group(2)
        repo = https_match.group(3)
        provider = "github" if "github" in host else ("gitlab" if "gitlab" in host else ("bitbucket" if "bitbucket" in host else host))
        return provider, owner, repo

    ssh_match = re.match(r"git@([^:]+):([^/]+)/([^/]+?)(?:\.git)?$", url)
    if ssh_match:
        host = ssh_match.group(1)
        owner = ssh_match.group(2)
        repo = ssh_match.group(3)
        provider = "github" if "github" in host else ("gitlab" if "gitlab" in host else ("bitbucket" if "bitbucket" in host else host))
        return provider, owner, repo

    return None, None, None


def show_remote_details():
    url = repository.get_remote_info()
    if not url:
        output.print_warning(get_text("remote_not_configured"))
        return

    provider, owner, repo = parse_remote_url(url)
    safe_url = _redact_url_credentials(url)
    output.print_info(get_text("remote_url", url=safe_url))
    if provider:
        output.print_info(get_text("provider", provider=provider))
    if owner:
        output.print_info(get_text("owner", owner=owner))
    if repo:
        output.print_info(get_text("repo_name", repo=repo))


def open_repo_in_browser():
    url = repository.get_remote_info()
    if not url:
        output.print_warning(get_text("remote_not_configured"))
        return

    if url.startswith("git@"):
        url = re.sub(r"git@([^:]+):", r"https://\1/", url)
    if url.endswith(".git"):
        url = url[:-4]

    output.print_info(get_text("opening_url", url=_redact_url_credentials(url)))
    try:
        webbrowser.open(url)
        output.print_success(get_text("browser_opened"))
    except Exception as e:
        output.print_error(get_text("browser_open_failed", error=redact(str(e))))


def create_github_repo(token, repo_name, private=False, description=""):
    """
    Create a new GitHub repository via the API.

    Returns (clone_url, error_key) - on success error_key is "" and
    clone_url is set; on failure clone_url is None and error_key names
    what went wrong (localization key) so the caller can show a specific,
    actionable message instead of one generic failure string.
    """
    if not token:
        return None, "github_error_no_token"
    if not repo_name or not re.match(r"^[A-Za-z0-9._-]+$", repo_name):
        return None, "github_error_invalid_repo_name"

    url = "https://api.github.com/user/repos"
    data = json.dumps({
        "name": repo_name,
        "private": private,
        "description": description,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"token {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "GitAssist")
    req.add_header("Accept", "application/vnd.github+json")

    try:
        with urllib.request.urlopen(req, timeout=API_TIMEOUT_SECONDS) as response:
            if response.status == 201:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("clone_url"), ""
            logger.error(f"GitHub repo creation returned unexpected status {response.status}")
            return None, "github_error_unexpected"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            log_security_event("GitHub API rejected token as invalid/expired (401)")
            return None, "github_error_invalid_token"
        if e.code == 403:
            # Could be rate limiting or an insufficiently-scoped token;
            # both surface as 403 from this endpoint.
            return None, "github_error_rate_limited_or_forbidden"
        if e.code == 422:
            return None, "github_error_repo_exists_or_invalid"
        logger.error(f"GitHub API HTTP error {e.code}: {redact(str(e))}")
        return None, "github_error_api_generic"
    except socket.timeout:
        return None, "github_error_timeout"
    except urllib.error.URLError as e:
        # Covers DNS failure, connection refused, offline, etc.
        logger.error(f"GitHub API network error: {redact(str(e))}")
        return None, "github_error_network"
    except Exception as e:
        logger.error(f"Unexpected error creating GitHub repo: {redact(str(e))}")
        return None, "github_error_unexpected"
