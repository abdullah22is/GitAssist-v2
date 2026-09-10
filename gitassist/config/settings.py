"""Global configuration settings for GitAssist."""

import os
import sys

APP_NAME = "GitAssist"
APP_VERSION = "0.2.0"
DEBUG = False
LOG_FILE = os.path.join(os.path.expanduser("~"), ".gitassist.log")
DEFAULT_LANGUAGE = "en"
LANGUAGE = "en"
DRY_RUN = "--dry-run" in sys.argv

# AI Provider settings
AI_PROVIDER = "rule_based"  # options: rule_based, ollama, openai
AI_ENABLED = False           # kept for backward compatibility, use AI_PROVIDER now
AI_API_KEY = ""              # for OpenAI
AI_MODEL = "gpt-3.5-turbo"   # for OpenAI

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2"

# Remote update monitor (see gitassist.git.remote_monitor). Throttled by
# design - never fetch on every command, never retry aggressively, and
# never act on what it finds (report only; pull/merge/rebase always
# require an explicit user action).
REMOTE_CHECK_ENABLED = True
REMOTE_CHECK_INTERVAL_SECONDS = 300      # don't re-check more often than this
REMOTE_CHECK_TIMEOUT_SECONDS = 8         # abort a stuck fetch instead of hanging
REMOTE_CHECK_CACHE_FILE = os.path.join(os.path.expanduser("~"), ".gitassist_remote_cache.json")