# CodeTone — Google style for every AI coding tool

[![CI](https://github.com/bodapatisaikrishna/codetone/actions/workflows/check.yml/badge.svg)](https://github.com/bodapatisaikrishna/codetone/actions/workflows/check.yml)
[![License: CC BY 3.0](https://img.shields.io/badge/License-CC_BY_3.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.3.1-green.svg)](CHANGELOG.md)

**AI coding assistants write code in whatever style they happen to guess.**
CodeTone teaches them to write and review code the way Google's engineers do, in
**24 languages**, without pasting thousands of lines of style guide into every
chat.

[Quick start](#quick-start) · [Install](#install--pick-your-tool) ·
[Languages](#languages) · [Releases](../../releases)

> Not affiliated with or endorsed by Google. See [NOTICE.md](NOTICE.md).

## Why CodeTone

- **Consistent code from any AI.** Naming, formatting, docs and idioms follow
  one published standard instead of the model's mood.
- **Small and cheap.** Google's guides run to thousands of lines. CodeTone
  condenses each into one short rule sheet, and the model reads only the sheet
  for the language it is editing (about 1–2k tokens).
- **Write and review.** The same rules generate new code and audit existing
  code.
- **Works across tools.** One open-standard
  [Agent Skill](https://agentskills.io) plus ready-made rule files for Cursor,
  Copilot, Windsurf and `AGENTS.md` tools, and paste-in prompts for chat apps
  and local models.
- **Free and open.** Every rule links back to its original guide.

## How it works

1. You ask for code or a review ("Write a Python CLI, Google style", "Review
   `server.go`").
2. The skill picks the language from your request or file type.
3. The model loads only that language's rule sheet: formatting, naming, language
   rules, docs format, recommended tools and a review checklist.
4. It writes code that follows the rules and checks its own output, or reviews
   your code against the checklist.

Your project comes first: if you have a formatter config or an established file
style, that takes precedence over the guide.

## Example

A review request returns findings grouped by priority, each with the rule and a
fix. Illustrative output for Python:

```text
Must fix
- Mutable default argument: def add(item, items=[])
  Fix: def add(item, items=None): items = [] if items is None else items
- Bare `except:` hides real errors.
  Fix: catch the specific exception.

Should fix
- `from utils import *`: import the module, not its contents.
- Missing `Args/Returns/Raises` sections in the docstring.

Nit
- Line is 96 columns, the limit is 80 (a formatter can fix this).
```

## Who it is for

- **Teams** that want AI-written code to look the same as the rest of the
  codebase.
- **Developers** who want a style review without setting up a linter for every
  language.
- **Learners** who want to see Google's conventions applied to their own code.
- **Anyone using Claude, Codex, Gemini, Copilot, Cursor, Windsurf, ChatGPT or a
  local model** and tired of re-explaining style preferences.

## What it is not

CodeTone does not replace formatters and linters such as `gofmt`, `black` or
`clang-format`. It guides the AI's judgment, and each rule sheet names the right
tool to run. It is a condensed, unofficial summary, so check the original guide
when something matters.

## Quick start

```sh
npx skills add bodapatisaikrishna/codetone
```

Then ask your agent: *"Write a Go HTTP handler, Google style"* or *"Review this
file against Google's Python style guide."* Other tools: see
[Install](#install--pick-your-tool).

## Languages

|              |               |             |            |
| ------------ | ------------- | ----------- | ---------- |
| Python       | C++           | Java        | JavaScript |
| TypeScript   | Angular       | Go          | Rust       |
| Shell (Bash) | C#            | Objective-C | Swift      |
| Kotlin       | Dart          | HTML/CSS    | JSON       |
| XML          | Markdown      | R           | Haskell    |
| Common Lisp  | SystemVerilog | Vim script  | Tcl/Tk     |

## Install — pick your tool

### Tools that support Agent Skills (`SKILL.md`)

Claude, OpenAI Codex, Gemini CLI, GitHub Copilot, Cursor, VS Code, Goose, Roo
Code, OpenCode, Amp, JetBrains Junie and other tools that follow the
[Agent Skills spec](https://agentskills.io) can use the skill as-is.

```sh
# Option 1: the skills CLI (installs into the right folder for your tool)
npx skills add bodapatisaikrishna/codetone

# Option 2: copy the folder yourself
git clone https://github.com/bodapatisaikrishna/codetone.git
cp -r codetone/skills/codetone <your tool's skills folder>
```

Common skills folders (project level): `.claude/skills/`, `.agents/skills/`
(Codex and others), `.github/skills/` (Copilot), `.gemini/skills/`,
`.cursor/skills/`. Check your tool's docs for its user-level folder.

**Claude Code plugin:**

```sh
/plugin marketplace add bodapatisaikrishna/codetone
/plugin install codetone@codetone
```

**Claude apps (web/desktop):** download `codetone.zip` from
[Releases](../../releases) and upload it in Claude's Skills settings.

### Tools that use rule files

Copy the matching folder from `adapters/` into your project root. Each language
gets its own file that only activates for that language's files.

| Tool           | Copy this                      | Activates on              |
| -------------- | ------------------------------ | ------------------------- |
| Cursor         | `adapters/cursor/.cursor/`     | file globs (`.mdc` rules) |
| GitHub Copilot | `adapters/copilot/.github/`    | `applyTo` globs           |
| Windsurf       | `adapters/windsurf/.windsurf/` | `trigger: glob`           |

You can delete the files for languages you don't use.

### Tools that read `AGENTS.md` (or similar)

Codex, Gemini CLI, Aider, Cline, Zed, Devin, Jules, Warp and many others read an
instructions file at the repo root.

1. Copy `adapters/agents-md/codetone/` into your repo root.
2. Copy `adapters/agents-md/AGENTS.md` to the root (or append it to your
   existing one). It tells the agent to open only the rule sheet for the
   language it is editing.
3. If your tool uses a different file name, use the same content:

| Tool                                                 | File name                                                   |
| ---------------------------------------------------- | ----------------------------------------------------------- |
| Codex, Cursor, Copilot, Zed, Warp, Amp, Devin, Jules | `AGENTS.md`                                                 |
| Gemini CLI                                           | `GEMINI.md` (or set `context.fileName` to `AGENTS.md`)      |
| Claude Code                                          | `CLAUDE.md` (or use the skill above)                        |
| Aider                                                | `CONVENTIONS.md`, loaded with `aider --read CONVENTIONS.md` |
| Cline / Roo Code                                     | `.clinerules/codetone.md`                                   |

### Chat apps and local models (ChatGPT, Gemini, DeepSeek, Ollama, LM Studio…)

Models without file access get a ready-made system prompt:

- One language: paste `adapters/prompts/<language>.md` (≈1–2k tokens) into the
  system prompt, custom instructions, a custom GPT / Gem, or your API `system`
  message.
- Every language: use `adapters/prompts/all-languages.md` (≈25k tokens) for
  models with large context windows.

```python
# Example: any OpenAI-compatible API (OpenAI, Gemini, Groq, Ollama, vLLM...)
system = open('adapters/prompts/python.md', encoding='utf-8').read()
messages = [
    {'role': 'system', 'content': system},
    {'role': 'user', 'content': 'Review this file:\n' + code},
]
```

## Repository layout

```text
codetone/
├── skills/codetone/   # the Agent Skill (source of truth)
│   ├── SKILL.md                  # router: picks the language, write/review modes
│   └── references/               # one condensed rule sheet per language (24)
├── adapters/                     # GENERATED — don't edit by hand
│   ├── cursor/  copilot/  windsurf/
│   ├── agents-md/                # AGENTS.md router + rule sheets
│   └── prompts/                  # system prompts for chat apps / APIs
├── scripts/build_adapters.py     # regenerates adapters/ from references/
├── tests/                        # 80+ mechanical & contract tests (pytest)
├── evals/                        # routing & review eval fixtures and answer keys
├── .claude-plugin/               # Claude Code plugin + marketplace manifest
├── .github/                      # CI workflow, issue and PR templates
├── LICENSE                       # CC BY 3.0
├── NOTICE.md                     # attribution and changes
├── CONTRIBUTING.md               # how to contribute
├── CODE_OF_CONDUCT.md            # community rules
├── SECURITY.md                   # how to report a vulnerability
└── CHANGELOG.md                  # release notes
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. In short:

1. Edit only `skills/codetone/references/<language>.md`.
2. Run `python3 scripts/build_adapters.py` to regenerate `adapters/`.
3. Keep each rule sheet short — rules, not essays — written in your own words,
   with a `Source:` link and a `Review checklist`.

## Support the project

If CodeTone saves you time, **star the repo** so others can find it, share it
with your team, and open an issue when a rule is wrong. Accuracy fixes are the
most useful contribution.

## Author

**Bodapati Sai Krishna** — designed and built this project: the skill, the
condensed rule sheets, the multi-tool adapters, the build script, the test suite
and evals.

## License

Content is adapted from the Google Style Guides and licensed under
[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). See
[LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
