#!/usr/bin/env python3
"""Reports rule sheets whose upstream style guide changed since last check.

Each rule sheet in skills/codetone/references/ is a condensed copy of an
upstream guide. scripts/upstream.json maps every sheet to the files it was
written from. scripts/upstream.lock.json records, for each of those files,
the upstream commit the sheet was last checked against.

This script asks the GitHub API for the newest commit that touched each file
and reports every file that moved on. Guides without a Git source (marked
"manual") are reported when their last manual check is older than
MANUAL_MAX_AGE_DAYS.

Usage:
  python3 scripts/check_upstream.py                  # report drift
  python3 scripts/check_upstream.py --report out.md  # also write Markdown
  python3 scripts/check_upstream.py --update python  # mark sheets re-checked
  python3 scripts/check_upstream.py --update --all

Exit status: 0 if nothing drifted, 1 if something drifted, 2 on errors.
Set GITHUB_TOKEN to avoid the low unauthenticated API rate limit.
"""

import argparse
import datetime
import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
REFS = ROOT / 'skills' / 'codetone' / 'references'
SOURCES = ROOT / 'scripts' / 'upstream.json'
LOCK = ROOT / 'scripts' / 'upstream.lock.json'

MANUAL_MAX_AGE_DAYS = 180
API = 'https://api.github.com'


def load_json(path):
    """Returns the parsed JSON file at path."""
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    """Writes data to path as sorted, indented JSON."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write('\n')


def latest_commit(repo, branch, path):
    """Returns (sha, iso_date) of the newest commit on branch touching path.

    Args:
        repo: GitHub repository as "owner/name".
        branch: Branch to look at.
        path: File path inside the repository.

    Returns:
        A (sha, iso_date) tuple.

    Raises:
        LookupError: If no commit touches the path (it was moved or deleted).
        urllib.error.URLError: On network or API errors.
    """
    query = urllib.parse.urlencode({'sha': branch, 'path': path, 'per_page': 1})
    request = urllib.request.Request(f'{API}/repos/{repo}/commits?{query}')
    request.add_header('Accept', 'application/vnd.github+json')
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        request.add_header('Authorization', f'Bearer {token}')
    with urllib.request.urlopen(request, timeout=30) as response:
        commits = json.load(response)
    if not commits:
        raise LookupError(f'{repo}:{path} has no commits on {branch}')
    commit = commits[0]
    return commit['sha'], commit['commit']['committer']['date']


def find_drift(sources, lock, fetch=latest_commit, today=None):
    """Compares the lock file with upstream.

    Args:
        sources: Parsed upstream.json.
        lock: Parsed upstream.lock.json.
        fetch: Function (repo, branch, path) -> (sha, date). Injected in tests.
        today: datetime.date to measure manual-check age from.

    Returns:
        A (drifted, stale_manual, errors) tuple of lists of dicts.
    """
    today = today or datetime.date.today()
    drifted, stale_manual, errors = [], [], []
    for sheet, source in sorted(sources.items()):
        checked = lock.get(sheet, {})
        if 'manual' in source:
            if _manual_is_stale(checked.get('checked_on'), today):
                stale_manual.append({
                    'sheet': sheet,
                    'url': source['manual'],
                    'checked_on': checked.get('checked_on') or 'never',
                })
            continue
        for path in source['paths']:
            try:
                sha, date = fetch(source['repo'], source['branch'], path)
            except Exception as e:  # pylint: disable=broad-except
                errors.append({'sheet': sheet, 'path': path, 'error': str(e)})
                continue
            old = checked.get('paths', {}).get(path)
            if sha != old:
                drifted.append({
                    'sheet': sheet,
                    'repo': source['repo'],
                    'branch': source['branch'],
                    'path': path,
                    'old': old,
                    'new': sha,
                    'date': date,
                })
    return drifted, stale_manual, errors


def _manual_is_stale(checked_on, today):
    """Returns True if a manual source was never checked or is overdue."""
    if not checked_on:
        return True
    age = (today - datetime.date.fromisoformat(checked_on)).days
    return age > MANUAL_MAX_AGE_DAYS


def render_report(drifted, stale_manual, errors):
    """Returns a Markdown report of the findings."""
    lines = ['Upstream style guides changed since these rule sheets were last',
             'checked. Re-read each change, update the sheet in',
             '`skills/codetone/references/` if a rule changed, then run',
             '`python3 scripts/check_upstream.py --update <sheet>`.', '']
    if drifted:
        lines += ['## Changed upstream', '',
                  '| Sheet | Upstream file | Last change | Diff |',
                  '| --- | --- | --- | --- |']
        for d in drifted:
            if d['old']:
                diff = (f"[compare](https://github.com/{d['repo']}/compare/"
                        f"{d['old'][:12]}...{d['new'][:12]})")
            else:
                diff = (f"[history](https://github.com/{d['repo']}/commits/"
                        f"{d['branch']}/{d['path']})")
            lines.append(f"| `{d['sheet']}.md` | `{d['repo']}:{d['path']}` | "
                         f"{d['date'][:10]} | {diff} |")
        lines.append('')
    if stale_manual:
        lines += ['## Due for a manual check', '',
                  f'These sources have no Git history to watch. Re-read them '
                  f'at least every {MANUAL_MAX_AGE_DAYS} days.', '']
        for m in stale_manual:
            lines.append(f"- `{m['sheet']}.md`: {m['url']} "
                         f"(last checked {m['checked_on']})")
        lines.append('')
    if errors:
        lines += ['## Errors', '']
        for e in errors:
            lines.append(f"- `{e['sheet']}.md` `{e['path']}`: {e['error']}")
        lines.append('')
    return '\n'.join(lines)


def update_lock(sources, lock, sheets, fetch=latest_commit, today=None):
    """Records the current upstream state of sheets as checked.

    Args:
        sources: Parsed upstream.json.
        lock: Parsed upstream.lock.json; modified in place.
        sheets: Names of the sheets to mark as checked.
        fetch: Function (repo, branch, path) -> (sha, date).
        today: datetime.date recorded for manual sources.
    """
    today = today or datetime.date.today()
    for sheet in sheets:
        source = sources[sheet]
        if 'manual' in source:
            lock[sheet] = {'checked_on': today.isoformat()}
            continue
        lock[sheet] = {'paths': {
            path: fetch(source['repo'], source['branch'], path)[0]
            for path in source['paths']
        }}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--report', help='write a Markdown report here')
    parser.add_argument('--update', nargs='*', metavar='SHEET',
                        help='mark these sheets as re-checked')
    parser.add_argument('--all', action='store_true',
                        help='with --update, mark every sheet')
    args = parser.parse_args(argv)

    sources = load_json(SOURCES)
    lock = load_json(LOCK) if LOCK.exists() else {}

    if args.update is not None:
        sheets = sorted(sources) if args.all else args.update
        unknown = [s for s in sheets if s not in sources]
        if unknown or not sheets:
            parser.error(f'unknown or missing sheet names: {unknown}')
        update_lock(sources, lock, sheets)
        save_json(LOCK, lock)
        print(f'Marked as checked: {", ".join(sheets)}')
        return 0

    drifted, stale_manual, errors = find_drift(sources, lock)
    report = render_report(drifted, stale_manual, errors)
    if args.report:
        pathlib.Path(args.report).write_text(report, encoding='utf-8')
    if not (drifted or stale_manual or errors):
        print('All rule sheets match their upstream guides.')
        return 0
    print(report)
    return 2 if errors and not (drifted or stale_manual) else 1


if __name__ == '__main__':
    sys.exit(main())
