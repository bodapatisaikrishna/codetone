# Contributing to CodeTone

Thanks for helping. CodeTone is a set of short rule sheets, so the most useful
contributions are **accuracy fixes**: a rule that is wrong, overstated, or
missing compared with the original Google guide.

By contributing you agree that your contribution is released under the same
license as the project (see [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md)).

## Before you start

- Search [open and closed issues and pull requests](../../issues) first.
- For anything bigger than a fix to one sheet (a new language, a new adapter, a
  change to `SKILL.md`), open an issue and wait for a maintainer's reply before
  writing the change.
- Small fixes (a wrong rule, a typo, a broken link) can go straight to a pull
  request.

## Where to edit

`skills/codetone/references/*.md` and `skills/codetone/SKILL.md` are the source
of truth.

**Never edit `adapters/` by hand.** It is generated from the rule sheets.

## Rule sheet guidelines

- Rules, not essays. Keep each sheet short.
- Write in your own words. Do not paste text from the original guide.
- Every sheet keeps its `Source:` link, a `Tools:` line, and a
  `## Review checklist`.
- Every rule must match the original guide. In the pull request, link the
  section of the guide that supports a changed rule.
- Do not state a preference as if it were Google's rule. Tools the guide does
  not name go under "common extras".

## Workflow

```sh
pip install -r requirements-dev.txt

# 1. Edit skills/codetone/references/<language>.md
# 2. Regenerate the adapters
python3 scripts/build_adapters.py

# 3. Check everything
SKIP_NETWORK_TESTS=1 python3 -m pytest tests/ -v
agentskills validate ./skills/codetone

# 4. Format Markdown (80 columns, numbered lists)
mdformat --wrap 80 --number <changed files>
```

CI runs the test suite and checks that `adapters/` is up to date on every push
and pull request. Commit the regenerated `adapters/` together with your change.

Python code follows the Google Python style: 4-space indent, 80 columns.

## Keeping sheets in sync with upstream

Google's guides change. Every Monday the `upstream drift` workflow compares each
rule sheet with the upstream files it was written from (`scripts/upstream.json`)
and opens or updates an issue labeled `upstream-drift` when one changed. Guides
with no Git source (Kotlin, Tcl) are flagged for a manual re-read every 180
days.

To work through the issue:

1. Open the compare link for each changed file and read the diff.
2. If a rule changed, update the sheet and regenerate the adapters.
3. Mark the sheet as checked, which records the new upstream commit in
   `scripts/upstream.lock.json`:

```sh
python3 scripts/check_upstream.py              # see what changed
python3 scripts/check_upstream.py --update go  # after re-checking go.md
```

Mark a sheet as checked only after you have read the upstream change, even if
the sheet needed no edit.

## Pull requests

- One purpose per pull request, small enough to review in one sitting.
- Imperative commit subject under 72 characters, for example
  `Fix Python TODO format`. Explain why in the body.
- Say what you ran. If you could not test something, say so.
- Version bumps and changelog entries are done by the maintainer at release
  time. Do not include them.

## Reporting problems

Use the [issue templates](../../issues/new/choose). For security problems, see
[SECURITY.md](SECURITY.md). Everyone taking part follows the
[Code of Conduct](CODE_OF_CONDUCT.md).
