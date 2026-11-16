"""Mechanical and structural tests for the CodeTone skill, adapters, and evals.

Run with:
    python3 -m pytest tests/
"""

import fnmatch
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.request
import yaml

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / 'skills' / 'codetone'
REFS = SKILL_DIR / 'references'
ADAPTERS = ROOT / 'adapters'
EVALS = ROOT / 'evals'

sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'evals'))
import build_adapters  # pylint: disable=wrong-import-position
import run_all_evals  # pylint: disable=wrong-import-position

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

# References with explicit Tools lines (angular references typescript, xml is schema, markdown is text)
LANGUAGES_WITH_TOOLS = [
    s for s in build_adapters.LANGUAGES if s not in {'angular', 'xml', 'markdown'}
]


def _frontmatter(text):
    """Simple parser for adapter frontmatter that may contain unquoted wildcards."""
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    assert match, 'missing frontmatter'
    fields = {}
    for line in match.group(1).splitlines():
        if ':' in line and not line.startswith(' '):
            key, value = line.split(':', 1)
            fields[key.strip()] = value.strip().strip('"\'')
    return fields


def _skill_frontmatter(text):
    """Strict YAML parser for SKILL.md which follows agentskills.io spec."""
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    assert match, 'missing frontmatter'
    return yaml.safe_load(match.group(1)) or {}


def test_skill_frontmatter_follows_spec():
    fields = _skill_frontmatter((SKILL_DIR / 'SKILL.md').read_text(encoding='utf-8'))
    assert fields['name'] == SKILL_DIR.name
    assert re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', fields['name'])
    assert 0 < len(fields['description']) <= 1024
    assert '<' not in fields['description']
    assert fields.get('license') == 'CC-BY-3.0'
    metadata = fields.get('metadata', {})
    assert metadata.get('author') == 'Bodapati Sai Krishna'
    assert metadata.get('version') == '1.3.1'


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
    assert re.search(r'^Source:\s*https?://', text, re.M), f'{ref.name}: missing standard Source: link'
    assert '## Review checklist' in text, f'{ref.name}: missing Review checklist'
    assert text.count('- [ ]') >= 3, f'{ref.name}: checklist has fewer than 3 items'
    headings = [line for line in text.splitlines() if line.startswith('## ')]
    assert len(headings) >= 3, f'{ref.name}: has fewer than 3 section headings'


@pytest.mark.parametrize('slug', sorted(LANGUAGES_WITH_TOOLS))
def test_reference_has_tools_line(slug):
    text = (REFS / f'{slug}.md').read_text(encoding='utf-8')
    assert 'Tools:' in text, f'{slug}.md missing Tools: line'


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
        assert f.name.startswith('codetone-'), f'{f.name} missing codetone- prefix'
        fields = _frontmatter(f.read_text(encoding='utf-8'))
        assert fields.get('globs') or fields.get('applyTo')


def test_agents_md_paths_exist():
    agents_dir = ADAPTERS / 'agents-md'
    text = (agents_dir / 'AGENTS.md').read_text(encoding='utf-8')
    pattern = r'`(codetone/references/[\w-]+\.md)`'
    matches = re.findall(pattern, text)
    assert len(matches) == len(build_adapters.LANGUAGES)
    for rel in matches:
        assert (agents_dir / rel).is_file(), rel


def test_prompts_exist_for_every_language():
    names = {p.stem for p in (ADAPTERS / 'prompts').glob('*.md')}
    assert names == set(build_adapters.LANGUAGES) | {'all-languages'}


def test_eval_fixtures_and_keys_parity():
    routing_key = EVALS / 'answer-keys' / 'routing.key'
    assert routing_key.is_file(), 'missing routing.key'
    lines = [line.strip().split() for line in routing_key.read_text().splitlines() if line.strip()]
    assert len(lines) == 24, f'routing.key has {len(lines)} entries, expected 24'
    for sample, lang in lines:
        assert (EVALS / 'fixtures' / 'routing' / sample).exists(), f'missing fixture {sample}'
        assert lang in build_adapters.LANGUAGES, f'unknown language {lang} in routing.key'


def test_version_consistency():
    skill_fields = _skill_frontmatter((SKILL_DIR / 'SKILL.md').read_text(encoding='utf-8'))
    skill_version = skill_fields['metadata']['version']
    assert skill_version == '1.3.1'

    plugin_json = json.loads((ROOT / '.claude-plugin' / 'plugin.json').read_text(encoding='utf-8'))
    assert plugin_json['version'] == skill_version

    mkt_json = json.loads((ROOT / '.claude-plugin' / 'marketplace.json').read_text(encoding='utf-8'))
    assert mkt_json['plugins'][0]['version'] == skill_version

    changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
    assert f'## {skill_version}' in changelog


@pytest.mark.parametrize('slug', sorted(run_all_evals.TEST_CASES.keys()))
def test_skill_behavioral_and_tool_execution(slug):
    """Verifies that each of the 24 skills actually catches violations and produces valid code."""
    collector = []
    run_all_evals.run_single_eval(slug, run_all_evals.TEST_CASES[slug], collector)
    assert len(collector) == 1
    res = collector[0]
    assert res['verdict'] == 'PASSED', f"Behavioral test failed for {res['name']}"


@pytest.mark.network
def test_all_external_urls_healthy():
    if os.environ.get('SKIP_NETWORK_TESTS') == '1':
        pytest.skip('Skipping network tests via SKIP_NETWORK_TESTS=1')

    all_urls = set()
    for p in REFS.glob('*.md'):
        text = p.read_text(encoding='utf-8')
        all_urls.update(re.findall(r'https?://[^\s\)\]]+', text))

    req_headers = {'User-Agent': 'Mozilla/5.0 (compatible; CodeTone-Validator/1.3.1)'}
    for url in sorted(all_urls):
        req = urllib.request.Request(url, headers=req_headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                assert resp.status in (200, 301, 302), f'{url} returned HTTP {resp.status}'
        except Exception as exc:
            pytest.fail(f'Failed to fetch {url}: {exc}')
