"""Offline tests for scripts/check_upstream.py and its data files.

Run with:
    python3 -m pytest tests/
"""

import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import check_upstream  # pylint: disable=wrong-import-position

SOURCES = check_upstream.load_json(check_upstream.SOURCES)
LOCK = check_upstream.load_json(check_upstream.LOCK)
SHEETS = sorted(p.stem for p in check_upstream.REFS.glob('*.md'))
TODAY = datetime.date(2026, 11, 16)


def fake_fetch(table):
    """Returns a fetch function that answers from table[(repo, path)]."""
    def fetch(repo, branch, path):
        del branch  # unused
        return table[(repo, path)], '2026-11-20T00:00:00Z'
    return fetch


def test_every_sheet_has_an_upstream_source():
    assert sorted(SOURCES) == SHEETS


def test_every_source_is_git_or_manual():
    for sheet, source in SOURCES.items():
        if 'manual' in source:
            assert source['manual'].startswith('https://'), sheet
        else:
            assert source['repo'].count('/') == 1, sheet
            assert source['branch'], sheet
            assert source['paths'], sheet


def test_lock_records_every_watched_file():
    assert sorted(LOCK) == SHEETS
    for sheet, source in SOURCES.items():
        if 'manual' in source:
            datetime.date.fromisoformat(LOCK[sheet]['checked_on'])
        else:
            assert sorted(LOCK[sheet]['paths']) == sorted(source['paths'])
            for sha in LOCK[sheet]['paths'].values():
                assert len(sha) == 40, sheet


def test_no_drift_when_upstream_matches_lock():
    sources = {'go': {'repo': 'g/s', 'branch': 'b', 'paths': ['a.md']}}
    lock = {'go': {'paths': {'a.md': 'x' * 40}}}
    fetch = fake_fetch({('g/s', 'a.md'): 'x' * 40})
    assert check_upstream.find_drift(sources, lock, fetch, TODAY) == (
        [], [], [])


def test_changed_upstream_file_is_reported_with_compare_link():
    sources = {'go': {'repo': 'g/s', 'branch': 'b', 'paths': ['a.md']}}
    lock = {'go': {'paths': {'a.md': 'a' * 40}}}
    fetch = fake_fetch({('g/s', 'a.md'): 'b' * 40})
    drifted, stale, errors = check_upstream.find_drift(
        sources, lock, fetch, TODAY)
    assert [d['path'] for d in drifted] == ['a.md']
    assert not stale and not errors
    report = check_upstream.render_report(drifted, stale, errors)
    assert 'compare/' + 'a' * 12 + '...' + 'b' * 12 in report


def test_manual_source_reported_only_when_stale():
    sources = {'tcl': {'manual': 'https://example.com'}}
    fresh = {'tcl': {'checked_on': '2026-10-01'}}
    stale = {'tcl': {'checked_on': '2026-01-01'}}
    assert not check_upstream.find_drift(sources, fresh, today=TODAY)[1]
    assert len(check_upstream.find_drift(sources, stale, today=TODAY)[1]) == 1


def test_fetch_errors_are_collected_not_raised():
    sources = {'go': {'repo': 'g/s', 'branch': 'b', 'paths': ['gone.md']}}

    def broken(repo, branch, path):
        raise LookupError(f'{repo}:{path} on {branch}')

    errors = check_upstream.find_drift(sources, {}, broken, TODAY)[2]
    assert errors[0]['path'] == 'gone.md'


def test_update_lock_records_new_state():
    sources = {
        'go': {'repo': 'g/s', 'branch': 'b', 'paths': ['a.md']},
        'tcl': {'manual': 'https://example.com'},
    }
    lock = {}
    fetch = fake_fetch({('g/s', 'a.md'): 'c' * 40})
    check_upstream.update_lock(sources, lock, ['go', 'tcl'], fetch, TODAY)
    assert lock == {
        'go': {'paths': {'a.md': 'c' * 40}},
        'tcl': {'checked_on': '2026-11-16'},
    }
