"""AI-powered suggestions and command interpretation."""

import json
import os
import urllib.request
import urllib.error
from gitassist.cli import output
from gitassist.config import settings


def is_available():
    """Return True if AI provider is available."""
    provider = getattr(settings, "AI_PROVIDER", "rule_based")
    if provider == "rule_based":
        return False
    if provider == "ollama":
        return _check_ollama()
    if provider == "openai":
        try:
            import openai
            return True
        except ImportError:
            return False
    return False


def _check_ollama():
    """Check if Ollama server is running."""
    try:
        url = f"{settings.OLLAMA_BASE_URL}/api/tags"
        with urllib.request.urlopen(url, timeout=2) as response:
            return response.status == 200
    except Exception:
        return False


def suggest_git_command(user_intent: str, repo_state: str = ""):
    """Convert natural language to Git command using available provider."""
    provider = getattr(settings, "AI_PROVIDER", "rule_based")
    if provider == "ollama":
        return _ollama_suggest(user_intent, repo_state)
    elif provider == "openai":
        return _openai_suggest(user_intent, repo_state)
    return None


def _ollama_suggest(user_intent: str, repo_state: str = ""):
    """Get suggestion from Ollama."""
    prompt = (
        "You are GitAssist. Convert the following user request into a single Git command.\n"
        f"Repository state: {repo_state}\n"
        f"User request: {user_intent}\n"
        "Reply with only the Git command, no explanation."
    )
    payload = json.dumps({
        "model": settings.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{settings.OLLAMA_BASE_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            command = result.get("response", "").strip()
            if command.startswith("git "):
                return command
            return None
    except Exception as e:
        output.print_debug(f"Ollama error: {e}", debug=settings.DEBUG)
        return None


def _openai_suggest(user_intent: str, repo_state: str = ""):
    """Get suggestion from OpenAI."""
    try:
        import openai
        api_key = os.environ.get("GITASSIST_AI_API_KEY") or getattr(settings, "AI_API_KEY", "")
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=getattr(settings, "AI_MODEL", "gpt-3.5-turbo"),
            messages=[{"role": "user", "content": (
                "Convert this request to a Git command only:\n"
                f"Repo: {repo_state}\nRequest: {user_intent}"
            )}],
            max_tokens=50,
            temperature=0,
        )
        command = response.choices[0].message.content.strip()
        if command.startswith("git "):
            return command
    except Exception as e:
        output.print_debug(f"OpenAI error: {e}", debug=settings.DEBUG)
    return None


def explain_error(error_text: str):
    """Explain Git error using available provider."""
    provider = getattr(settings, "AI_PROVIDER", "rule_based")
    if provider == "ollama":
        prompt = f"Explain this Git error in simple terms and suggest a solution:\n{error_text}"
        payload = json.dumps({
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response", "").strip()
        except Exception:
            return None
    elif provider == "openai":
        try:
            import openai
            api_key = os.environ.get("GITASSIST_AI_API_KEY") or getattr(settings, "AI_API_KEY", "")
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=getattr(settings, "AI_MODEL", "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": f"Explain this Git error: {error_text}"}],
                max_tokens=150,
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return None
    return None