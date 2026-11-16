# Evals

A small test suite for the skill: seeded-violation files to review, plus write
tasks. Each file in `fixtures/` has a matching answer key in `answer-keys/`.
Keep the keys away from the agent under test.

## How to run

For each fixture, run two agents on the same model:

1. **With skill** — told to read `skills/codetone/SKILL.md` and follow it.
2. **Baseline** — told to use only its own knowledge of Google style.

Each agent:

1. Reviews the fixture and lists every violation.
2. Does the matching task in `write-tasks.md`.

Then score:

- **Review recall**: seeded violations found ÷ total in the answer key.
- **False positives**: flagged "violations" the guide doesn't actually forbid.
- **Write quality**: run the real tools — `pylint --rcfile=pylintrc`,
  `shellcheck`, `gofmt -l` + `go vet` + `go test`, `tsc --strict`.

## Results — Claude Fable 5.2 (2026-11-16)

| Language   | Review recall (skill) | Review recall (baseline) | Write: tools (skill)  | Write: tools (baseline) |
| ---------- | --------------------- | ------------------------ | --------------------- | ----------------------- |
| Python     | 15/15                 | 15/15                    | pylint clean          | 1 pylint warning        |
| TypeScript | 17/17                 | 17/17                    | `tsc --strict` passes | `tsc --strict` passes   |
| Go         | 18/18                 | 18/18                    | gofmt/vet/test pass   | gofmt/vet/test pass     |
| Shell      | 18/18                 | 18/18                    | shellcheck clean      | shellcheck clean        |

Findings:

- Fable already knows these four guides well; the skill made reviews more
  consistent (same severity groups, rule names, tool advice) rather than finding
  more issues.
- One false positive came from the skill: it said single-line `if` without
  braces is forbidden in TypeScript. The reference file was fixed.

## Results — Claude Haiku 5.5 (2026-11-16): "does it work?" check

| Test                                                                                            | Result     |
| ----------------------------------------------------------------------------------------------- | ---------- |
| Mechanical tests (`tests/test_skill.py`)                                                        | 58/58 pass |
| Spec validator (`agentskills validate`)                                                         | valid      |
| Routing: picks the right rule sheet (`fixtures/routing/`, 24 files incl. ambiguous `.h`)        | 24/24      |
| Triggering: activates only for style requests (8 requests, 5 skills)                            | 8/8        |
| `AGENTS.md` adapter: reads only `AGENTS.md` + the Python sheet; output passes Google `pylintrc` | pass       |
| Prompt adapter (`prompts/go.md` as system prompt): `gofmt`, `go vet`, `go test`                 | pass       |

Review of less common languages (`fixtures/niche/`), seeded violations found:

| Language            | With skill      | Without skill   |
| ------------------- | --------------- | --------------- |
| Rust (Google rules) | 15/15           | 12/15           |
| SystemVerilog       | 18/18           | 10/18           |
| Kotlin              | 15/16           | 12/16           |
| Common Lisp         | 16/16           | 15/16           |
| **Total**           | **64/65 (98%)** | **49/65 (75%)** |

Both missed the Kotlin rule against `\u` escapes for printable characters. The
skill matters most for smaller models and less common guides.
