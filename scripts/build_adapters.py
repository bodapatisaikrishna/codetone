#!/usr/bin/env python3
"""Generates tool-specific adapters from the skill's reference files.

The rule sheets in skills/codetone/references/ are the single source
of truth. This script turns them into the rule/instruction formats that other
AI tools read, so the skill works with any LLM:

  adapters/cursor/.cursor/rules/*.mdc                    Cursor
  adapters/copilot/.github/instructions/*.instructions.md GitHub Copilot
  adapters/windsurf/.windsurf/rules/*.md                 Windsurf
  adapters/agents-md/AGENTS.md                           Codex, Gemini CLI,
                                                         Aider, Cline, Zed...
  adapters/prompts/*.md                                  ChatGPT, Gemini,
                                                         local models (paste)

Usage:
  python3 scripts/build_adapters.py
"""

import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
REFS = ROOT / 'skills' / 'codetone' / 'references'
OUT = ROOT / 'adapters'

# slug -> (display name, file globs)
LANGUAGES = {
    'python': ('Python', ['**/*.py', '**/*.pyi']),
    'cpp': ('C++', ['**/*.cc', '**/*.cpp', '**/*.cxx', '**/*.h', '**/*.hpp']),
    'java': ('Java', ['**/*.java']),
    'javascript': ('JavaScript', ['**/*.js', '**/*.mjs', '**/*.cjs']),
    'typescript': ('TypeScript', ['**/*.ts', '**/*.tsx']),
    'angular': (
        'Angular',
        [
            '**/*.component.ts',
            '**/*.component.html',
            '**/*.service.ts',
            '**/*.directive.ts',
        ],
    ),
    'go': ('Go', ['**/*.go']),
    'rust': ('Rust', ['**/*.rs']),
    'shell': ('Shell (Bash)', ['**/*.sh', '**/*.bash']),
    'csharp': ('C#', ['**/*.cs']),
    'objective-c': ('Objective-C', ['**/*.m', '**/*.mm']),
    'swift': ('Swift', ['**/*.swift']),
    'kotlin': ('Kotlin', ['**/*.kt', '**/*.kts']),
    'dart': ('Dart', ['**/*.dart']),
    'html-css': ('HTML/CSS', ['**/*.html', '**/*.css', '**/*.scss']),
    'json': ('JSON', ['**/*.json']),
    'xml': ('XML', ['**/*.xml']),
    'markdown': ('Markdown', ['**/*.md']),
    'r': ('R', ['**/*.R', '**/*.r', '**/*.Rmd']),
    'haskell': ('Haskell', ['**/*.hs']),
    'common-lisp': ('Common Lisp', ['**/*.lisp', '**/*.asd', '**/*.cl']),
    'verilog': ('SystemVerilog/Verilog', ['**/*.sv', '**/*.svh', '**/*.v']),
    'vimscript': ('Vim script', ['**/*.vim']),
    'tcl': ('Tcl/Tk', ['**/*.tcl']),
}

PRECEDENCE = (
    'Precedence: the project\'s own formatter/linter config and the existing '
    'style of the file win over these rules; otherwise apply them.'
)

ATTRIBUTION = (
    'Condensed from the Google Style Guides '
    '(https://github.com/google/styleguide), CC BY 3.0. '
    'Not affiliated with or endorsed by Google.'
)


def _globs(globs):
    return ','.join(globs)


def _short_globs(globs):
    return ', '.join(g.replace('**/', '') for g in globs)


def read_ref(slug):
    return (REFS / f'{slug}.md').read_text(encoding='utf-8').strip()


def reset_dir(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def build_cursor():
    out = OUT / 'cursor' / '.cursor' / 'rules'
    reset_dir(out)
    for slug, (name, globs) in LANGUAGES.items():
        text = (
            '---\n'
            f'description: Google {name} style rules. Apply when writing or '
            f'reviewing {name} code.\n'
            f'globs: {_globs(globs)}\n'
            'alwaysApply: false\n'
            '---\n\n'
            f'{PRECEDENCE}\n\n{read_ref(slug)}\n\n<!-- {ATTRIBUTION} -->\n'
        )
        (out / f'codetone-{slug}.mdc').write_text(text, encoding='utf-8')


def build_copilot():
    out = OUT / 'copilot' / '.github' / 'instructions'
    reset_dir(out)
    for slug, (_, globs) in LANGUAGES.items():
        text = (
            '---\n'
            f'applyTo: "{_globs(globs)}"\n'
            '---\n\n'
            f'{PRECEDENCE}\n\n{read_ref(slug)}\n\n<!-- {ATTRIBUTION} -->\n'
        )
        (out / f'codetone-{slug}.instructions.md').write_text(
            text, encoding='utf-8'
        )


def build_windsurf():
    out = OUT / 'windsurf' / '.windsurf' / 'rules'
    reset_dir(out)
    for slug, (_, globs) in LANGUAGES.items():
        text = (
            '---\n'
            'trigger: glob\n'
            f'globs: {_globs(globs)}\n'
            '---\n\n'
            f'{PRECEDENCE}\n\n{read_ref(slug)}\n\n<!-- {ATTRIBUTION} -->\n'
        )
        (out / f'codetone-{slug}.md').write_text(text, encoding='utf-8')


def build_agents_md():
    """One small router file; the agent opens only the rule sheet it needs."""
    out = OUT / 'agents-md'
    reset_dir(out)
    rows = '\n'.join(
        f'| {name} | `{_short_globs(globs)}` | '
        f'`codetone/references/{slug}.md` |'
        for slug, (name, globs) in LANGUAGES.items()
    )
    text = f"""# Code style: Google Style Guides (via CodeTone)

When you write, edit or review code in this repository, follow Google's style
for that language. The rules live in `codetone/references/`
(copy that folder into the repo root, or change the paths below).

Before working on a file, open **only** the rule sheet for its language:

| Language | Files | Rule sheet |
|---|---|---|
{rows}

- Writing code: follow the sheet, then check your output against its
  "Review checklist".
- Reviewing code: list each violation with location, rule and fix, grouped as
  Must fix / Should fix / Nit.
- {PRECEDENCE}

<!-- {ATTRIBUTION} -->
"""
    (out / 'AGENTS.md').write_text(text, encoding='utf-8')
    refs_out = out / 'codetone' / 'references'
    shutil.copytree(REFS, refs_out)


def build_prompts():
    """Copy-paste system prompts for chat LLMs without file access."""
    out = OUT / 'prompts'
    reset_dir(out)
    header = (
        'You are a code assistant that writes and reviews code in Google\'s '
        'style.\n'
        '- When writing code: follow the rules below exactly, then check your '
        'output against the Review checklist before answering.\n'
        '- When reviewing code: list every violation with its line, the rule, '
        'and the corrected code, grouped as Must fix / Should fix / Nit. If '
        'the code is already compliant, say so.\n'
        f'- {PRECEDENCE}\n'
    )
    sheets = []
    for slug in LANGUAGES:
        sheet = read_ref(slug)
        sheets.append(sheet)
        (out / f'{slug}.md').write_text(
            f'{header}\n{sheet}\n\n{ATTRIBUTION}\n', encoding='utf-8'
        )
    (out / 'all-languages.md').write_text(
        f'{header}- First identify the language, then use only its section.\n\n'
        + '\n\n---\n\n'.join(sheets)
        + f'\n\n{ATTRIBUTION}\n',
        encoding='utf-8',
    )


def main():
    missing = [s for s in LANGUAGES if not (REFS / f'{s}.md').exists()]
    extra = sorted(p.stem for p in REFS.glob('*.md') if p.stem not in LANGUAGES)
    if missing or extra:
        raise SystemExit(
            f'Reference mismatch. Missing: {missing} Extra: {extra}'
        )
    build_cursor()
    build_copilot()
    build_windsurf()
    build_agents_md()
    build_prompts()
    print(f'Built adapters for {len(LANGUAGES)} languages in {OUT}')


if __name__ == '__main__':
    main()
