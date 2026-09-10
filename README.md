# GitAssist

A smart and security-aware Git assistant that analyzes repository state, presents relevant actions, validates commands, and helps users work with Git safely.

![Version](https://img.shields.io/badge/version-0.2.0-blue)

## Features

- **Context-aware dynamic menu**: Only shows relevant actions based on repository state.
- **Repository dashboard**: Shows branch, working-tree status, remote, upstream, and sync status at a glance.
- **Safe execution pipeline**: Every Git command — from menus, manual entry, or AI suggestions — passes through the same pipeline: parsing, risk classification, context check, and confirmation before it ever runs.
- **Structured command parser**: Understands Git's real argument grammar (`-C`, `--git-dir`, `--work-tree`, `-c key=value`, quoting, Arabic/Unicode paths) instead of naive string matching.
- **Risk levels**: `SAFE`, `CAUTION`, `DANGEROUS`, and `BLOCKED`, with warnings and safer alternatives shown before you confirm.
- **Hard security blocks**: Refuses constructs known to enable arbitrary command execution — shell-escaping Git aliases (`alias.x=!cmd`), exec-capable config keys (`core.pager`, `credential.helper`, etc.), `--exec-path`, `ext::`/`fd::` transport URLs, and `--upload-pack`/`--receive-pack` — regardless of how they're entered.
- **Fail-closed by design**: If a command needs confirmation and no interactive prompt is available, it is refused rather than run silently.
- **Local project workflow**: Point GitAssist at any folder — it validates the path, offers to initialize or clone if it isn't a repository yet, and shows the dashboard plus remote-appropriate next steps if it is.
- **Throttled remote update monitor**: Checks ahead/behind/diverged status against the remote without fetching on every command — checks are cached and rate-limited, with a hard timeout so a dead connection can't hang the app.
- **Manual command mode**: Enter any Git command (quoting-aware); shell syntax like `;`, `&&`, or `|` is rejected up front since it isn't a single Git command.
- **Typo detection**: Suggests corrections for common Git command typos.
- **Error intelligence**: Explains common Git error messages (push rejected, merge conflicts, no upstream branch, auth failures, etc.) with actionable suggestions.
- **Next-step suggestions**: After init, add, commit, or fetch, suggests the natural next action — purely informational, never automatic.
- **Conflict detection**: After pull/merge, lists conflicted files and guides resolution.
- **File management**: Create, edit, delete files, and create directories, with permission-error handling and a warning before deleting a file outside the current project.
- **Branch management**: List, create, switch, delete, merge branches.
- **Stash management**: Save, list, apply, pop, drop stashes.
- **Synchronization**: Fetch, pull, push, each bounded by a timeout so a stalled network operation can't hang the app.
- **GitHub integration**: View remote details (with any embedded credentials masked), open the repo in a browser, and create a repository via the API with specific, actionable error messages (invalid token, rate limited, name conflict, timeout, offline).
- **Secret handling**: GitHub tokens are entered with hidden input (no terminal echo) and are never written to logs; credentials embedded in remote URLs are masked wherever they'd otherwise be displayed or logged.
- **Bilingual support**: English and Arabic, covered by an automated test that every user-facing message exists and is translated in both languages.
- **Voice commands**: Optional voice input using speech recognition; missing dependencies degrade gracefully instead of crashing.
- **AI assistance**: Optional AI provider (Ollama local or OpenAI) for natural language understanding — AI-suggested commands go through the exact same safety pipeline as anything else, never executed directly.
- **Dry-run mode**: `--dry-run` performs full parsing, risk classification, and context analysis, then reports what it would do without executing it.
- **Terminal-friendly output**: Color is automatically disabled when output isn't a real terminal (piped, redirected, or CI) or when `NO_COLOR` is set; every message also carries a plain-text label so meaning never depends on color alone.
- **Logging**: Records operations to `~/.gitassist.log`, with secrets (tokens, credentials in URLs) redacted before anything is written.

## Installation

### Prerequisites
- Python 3.9+ (3.12+ recommended for the current optional voice/AI stack)
- Git installed and in PATH

### Steps

```bash
git clone <repository-url>
cd GitAssist
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
```

Core functionality uses only the Python standard library — the command above has nothing to install. Optional voice/AI features require additional packages:

```bash
pip install -r requirements-optional.txt
```

## Usage

Run the interactive CLI:

```bash
python -m gitassist
```

At startup, choose a language: **English** or **العربية**.

Dry-run mode (analyze and report without executing anything):

```bash
python -m gitassist --dry-run
```

## Voice Commands (Optional)

To enable voice commands, install the optional dependencies:

```bash
pip install SpeechRecognition sounddevice numpy
```

Then choose the voice option from the main menu and speak a Git command, e.g. "git status" or "git log".

> Voice recognition uses Google Speech Recognition, which requires an internet connection. If the optional packages aren't installed, or the platform's audio backend isn't available, voice mode reports that clearly instead of crashing — it never partially starts.

## AI Assistance (Optional)

GitAssist has a built-in rule-based engine that understands common Arabic/English phrases without any API key. Examples:

- "انشاء مستودع جديد" → `git init`
- "عرض الحالة" → `git status`
- "حفظ التغييرات" → `git add .` (you're still asked for a real commit message afterward — a meaningful message can't be guessed)

To enable advanced AI:

**Ollama (local, free, no internet after setup)**
1. Install Ollama from https://ollama.com
2. Pull a model: `ollama pull llama3.2`
3. In `config/settings.py`:
   ```python
   AI_PROVIDER = "ollama"
   OLLAMA_MODEL = "llama3.2"
   ```

**OpenAI (requires an API key)**
1. Install: `pip install openai`
2. Set the key via an environment variable rather than committing it to `settings.py`.
3. In `config/settings.py`:
   ```python
   AI_PROVIDER = "openai"
   AI_MODEL = "gpt-3.5-turbo"
   ```

**Important:** AI-suggested commands are never executed directly. They pass through the exact same structured parser, risk classification, and confirmation pipeline as manually typed commands — including the hard security blocks.

## Configuration

| Setting | Description |
|---|---|
| `settings.LANGUAGE` | Selected at startup (`en` / `ar`). |
| `--dry-run` (CLI flag) | Analyzes and reports commands without executing them. |
| `settings.LOG_FILE` | Defaults to `~/.gitassist.log`. |
| `settings.AI_PROVIDER` | `rule_based`, `ollama`, or `openai`. |
| `settings.REMOTE_CHECK_ENABLED` | Turns the throttled remote update monitor on/off. |
| `settings.REMOTE_CHECK_INTERVAL_SECONDS` | Minimum time between automatic remote checks (default 300). |
| `settings.REMOTE_CHECK_TIMEOUT_SECONDS` | Timeout for a remote status check's fetch (default 8). |
| `NO_COLOR` (env var) | Disables ANSI colors regardless of terminal. |

## Testing

Run the full test suite:

```bash
python -m unittest discover -s tests
```

The suite includes unit tests for the parser, policy engine, localization completeness, and error analyzer, plus integration tests that exercise real temporary Git repositories and local bare repositories standing in for a remote (no real network access, no user repositories touched).

## Project Structure

```
GitAssist/
├── gitassist/
│   ├── __main__.py
│   ├── cli/            # output formatting, input handling, dashboard rendering
│   ├── core/            # menu workflows, manual command mode, file ops, next-step engine
│   ├── git/             # executor, repository inspection, sync, stash, branches, remote monitor
│   ├── security/        # parser, policy engine, context checks, redaction, shell guard
│   ├── errors/          # error pattern matching and explanations
│   ├── github/          # remote URL parsing and GitHub API integration
│   ├── ai/               # rule-based and AI-assisted command suggestion
│   ├── gitlog/          # log setup and security-event logging
│   ├── config/           # central settings
│   └── localization/     # English/Arabic text catalog
├── tests/
├── docs/
├── README.md
└── LICENSE
```

## Notes on Voice and AI

- Voice commands require microphone access and an internet connection for Google Speech Recognition.
- The built-in rule-based engine works fully offline and supports common Arabic/English phrases.
- Ollama-based AI works completely offline after the model is downloaded.
- OpenAI-based AI requires an API key and an internet connection.
- AI and voice are both optional — every core Git feature works without either dependency installed.
- AI suggestions are suggestions only: they pass through the same parser and risk engine as any other command and require confirmation like anything else.
- Tokens and credentials are never written to logs; a GitHub token is entered with terminal echo disabled.

## Troubleshooting

**PyAudio errors**
GitAssist uses `sounddevice`, not PyAudio, specifically to avoid needing C++ build tools. If you see PyAudio-related errors, make sure you installed `sounddevice` and `numpy`, not `PyAudio`.

**numpy not available on a very new Python version**
If you're on a Python release too new for prebuilt `numpy` wheels, switch to Python 3.12 or 3.13 for voice support — core Git features work on any supported Python version regardless.

**AI not generating commands**
- Rule-based: check that your phrase matches a pattern in `gitassist/ai/fallback.py`.
- Ollama: make sure Ollama is running (`ollama serve`) and the model has been pulled.
- OpenAI: check your API key and internet connection.

**"This command was blocked for security reasons"**
This means the command matched a known code-execution vector (a shell-escaping Git alias, an exec-capable config key, `--exec-path`, an `ext::`/`fd::` transport, or `--upload-pack`/`--receive-pack`). This is intentional and cannot be bypassed with `--dry-run` or by declining a confirmation prompt — see `docs/security.md` for the full list.

## Contributing

Contributions are welcome! Please open an issue first to discuss your ideas.

## License

MIT License. See `LICENSE`.
