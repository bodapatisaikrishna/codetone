"""Mechanical tests for the skill and its generated adapters.

Run with:
    python3 -m pytest tests/
"""

import fnmatch
import pathlib
import re
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / 'skills' / 'codetone'
REFS = SKILL_DIR / 'references'
ADAPTERS = ROOT / 'adapters'

sys.path.insert(0, str(ROOT / 'scripts'))
import build_adapters  # pylint: disable=wrong-import-position

# A sample file name for each language, and the rule sheet it must map to.
SAMPLES = {
    'app/main.py': 'python',
    'src/table.cc': 'cpp',
    'src/Foo.java': 'java',
    'web/app.mjs': 'javascript',
    'web/store.ts': 'typescript',
    'web/user-card.component.ts': 'angular',
    'cmd/server.go': 'go',
    'src/lib.rs': 'rust',
    'scripts/deploy.sh': 'shell',
    'App/Program.cs': 'csharp',
    'ios/ViewController.m': 'objective-c',
    'ios/Model.swift': 'swift',
    'android/Repo.kt': 'kotlin',
    'lib/widget.dart': 'dart',
    'site/index.html': 'html-css',
    'api/user.json': 'json',
    'config/layout.xml': 'xml',
    'docs/README.md': 'markdown',
    'analysis/model.R': 'r',
    'src/Parser.hs': 'haskell',
    'src/utils.lisp': 'common-lisp',
    'rtl/fifo.sv': 'verilog',
    'plugin/foo.vim': 'vimscript',
    'tools/build.tcl': 'tcl',
}


def _frontmatter(text):
    match = re.match(r'---\n(.*?)\n---\n', text, re.S)
    assert match, 'missing frontmatter'
    fields = {}
    for line in match.group(1).splitlines():
        if ':' in line and not line.startswith(' '):
            key, value = line.split(':', 1)
            fields[key.strip()] = value.strip()
    return fields


def test_skill_frontmatter_follows_spec():
    fields = _frontmatter((SKILL_DIR / 'SKILL.md').read_text(encoding='utf-8'))
    assert fields['name'] == SKILL_DIR.name
    assert re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', fields['name'])
    assert 0 < len(fields['description']) <= 1024
    assert '<' not in fields['description']


def test_skill_md_is_short():
    lines = (SKILL_DIR / 'SKILL.md').read_text(encoding='utf-8').splitlines()
    assert len(lines) < 500


def test_every_linked_reference_exists_and_every_reference_is_linked():
    skill = (SKILL_DIR / 'SKILL.md').read_text(encoding='utf-8')
    linked = set(re.findall(r'references/([\w-]+\.md)', skill))
    on_disk = {p.name for p in REFS.glob('*.md')}
    assert linked == on_disk


@pytest.mark.parametrize('ref', sorted(REFS.glob('*.md')), ids=lambda p: p.stem)
def test_reference_has_source_and_checklist(ref):
    text = ref.read_text(encoding='utf-8')
    assert re.search(r'^Source.*https?://', text, re.M), 'no Source: link'
    assert '## Review checklist' in text
    assert text.count('- [ ]') >= 3


def test_generator_covers_every_reference():
    assert set(build_adapters.LANGUAGES) == {p.stem for p in REFS.glob('*.md')}


@pytest.mark.parametrize('path,slug', sorted(SAMPLES.items()))
def test_globs_route_sample_file_to_right_language(path, slug):
    matches = [
        s
        for s, (_, globs) in build_adapters.LANGUAGES.items()
        if any(
            fnmatch.fnmatch(path, g) or fnmatch.fnmatch(path, g[3:])
            for g in globs
        )
    ]
    assert slug in matches, f'{path} not matched by {slug} globs'
    # Angular component files are TypeScript too; nothing else may overlap.
    allowed = {slug, 'typescript'} if slug == 'angular' else {slug}
    assert set(matches) <= allowed, f'{path} also matched {matches}'


def test_adapters_are_up_to_date():
    before = {
        p.relative_to(ADAPTERS): p.read_bytes()
        for p in ADAPTERS.rglob('*')
        if p.is_file()
    }
    subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'build_adapters.py')],
        check=True,
        capture_output=True,
    )
    after = {
        p.relative_to(ADAPTERS): p.read_bytes()
        for p in ADAPTERS.rglob('*')
        if p.is_file()
    }
    assert before == after, 'run scripts/build_adapters.py and commit'


@pytest.mark.parametrize(
    'folder,suffix',
    [
        ('cursor/.cursor/rules', '.mdc'),
        ('copilot/.github/instructions', '.instructions.md'),
        ('windsurf/.windsurf/rules', '.md'),
    ],
)
def test_rule_adapters_have_one_file_per_language(folder, suffix):
    files = [
        p for p in (ADAPTERS / folder).iterdir() if p.name.endswith(suffix)
    ]
    assert len(files) == len(build_adapters.LANGUAGES)
    for f in files:
        fields = _frontmatter(f.read_text(encoding='utf-8'))
        assert fields.get('globs') or fields.get('applyTo')


def test_agents_md_paths_exist():
    agents_dir = ADAPTERS / 'agents-md'
    text = (agents_dir / 'AGENTS.md').read_text(encoding='utf-8')
    pattern = r'`(codetone/references/[\w-]+\.md)`'
    for rel in re.findall(pattern, text):
        assert (agents_dir / rel).is_file(), rel


def test_prompts_exist_for_every_language():
    names = {p.stem for p in (ADAPTERS / 'prompts').glob('*.md')}
    assert names == set(build_adapters.LANGUAGES) | {'all-languages'}
