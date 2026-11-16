# CodeTone — Google style for every AI coding tool

Teach **any LLM or AI coding agent** to write and review code in Google's style
for **24 languages**, using condensed versions of the
[Google Style Guides](https://github.com/google/styleguide).

It ships as an open-standard [Agent Skill](https://agentskills.io) (`SKILL.md`)
plus ready-made rule files for tools that use their own formats, and copy-paste
prompts for chat apps.

Instead of loading thousands of lines of guides, the model reads one short rule
sheet for the language it is working in — formatting, naming, language rules,
docs format, recommended tools, and a review checklist.

Created and maintained by **Bodapati Sai Krishna**.

> Not affiliated with or endorsed by Google. See [NOTICE.md](NOTICE.md).

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

## What it does

- **Write mode** — "Write a Python CLI to rename files, Google style." The model
  follows the Python rules (80 cols, module-only imports, `Args/Returns/Raises`
  docstrings, `main()` guard) and self-checks the output.
- **Review mode** — "Review `server.go` against Google's Go style guide."
  Violations come back grouped as **Must fix / Should fix / Nit**, each with the
  rule and a corrected snippet.
- **Respects your project** — your formatter config and existing file style take
  precedence over the guide.

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
├── evals/                        # test fixtures, answer keys, results
├── .claude-plugin/               # Claude Code plugin + marketplace manifest
├── LICENSE                       # CC BY 3.0
├── NOTICE.md                     # attribution and changes
└── CHANGELOG.md                  # release notes
```

## Contributing

1. Edit only `skills/codetone/references/<language>.md`.
2. Run `python3 scripts/build_adapters.py` to regenerate `adapters/`.
3. Keep each rule sheet short — rules, not essays — written in your own words,
   with a `Source:` link and a `Review checklist`.
4. If you change a rule, re-run the relevant test in `evals/`.

## Author

**Bodapati Sai Krishna** — designed and built this project: the skill, the
condensed rule sheets, the multi-tool adapters, the build script, the tests and
the evals.

## License

Content is adapted from the Google Style Guides and licensed under
[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). See
[LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
