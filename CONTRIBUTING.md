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
pip install skills-ref mdformat mdformat-gfm

# 1. Edit skills/codetone/references/<language>.md
# 2. Regenerate the adapters
python3 scripts/build_adapters.py

# 3. Validate the skill against the Agent Skills spec
agentskills validate ./skills/codetone

# 4. Format Markdown (80 columns, numbered lists)
mdformat --wrap 80 --number <changed files>
```

Commit the regenerated `adapters/` together with your change.

Python code follows the Google Python style: 4-space indent, 80 columns.

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
