---
name: codetone
description: Write or review code and docs in Google's style for 24 languages (Python, C++, Java, JS/TS, Go, Rust, Shell, Kotlin, Swift, HTML/CSS, Markdown and more). Use when asked to follow, apply or check Google style.
license: CC-BY-3.0
metadata:
  author: Bodapati Sai Krishna
  version: "1.3.1"
  source: https://github.com/google/styleguide
---

# CodeTone — Google Style Guides

Condensed, language-by-language versions of Google's public style guides
(https://github.com/google/styleguide), so code and docs come out consistent
every time.

## When to use

- The user asks for code "in Google style", "following Google's style guide", or
  names a specific guide (e.g. "Google Python style", "Google Java format").
- The user asks to **review / lint / check** code against Google style.
- The repo already follows Google style (e.g. has `pylintrc` from Google,
  `google-java-format`, `.clang-format` with `BasedOnStyle: Google`, `gts`).

Do **not** force Google style on a project with its own established style or
formatter config — see "Precedence" below.

## Step 1 — Pick the language file

Read **only** the reference file(s) for the languages involved. Each file is
self-contained: formatting, naming, language rules, docs, tools, and a review
checklist.

| Language                | Extensions / signals                | File                                        |
| ----------------------- | ----------------------------------- | ------------------------------------------- |
| Python                  | `.py`, `.pyi`                       | `references/python.md`                      |
| C++                     | `.cc`, `.cpp`, `.h`, `.hpp`         | `references/cpp.md`                         |
| Java                    | `.java`                             | `references/java.md`                        |
| JavaScript              | `.js`, `.mjs`, `.cjs`               | `references/javascript.md`                  |
| TypeScript              | `.ts`, `.tsx`                       | `references/typescript.md`                  |
| Angular                 | `@Component`, `angular.json`        | `references/angular.md` (+ `typescript.md`) |
| Go                      | `.go`                               | `references/go.md`                          |
| Rust                    | `.rs`                               | `references/rust.md`                        |
| Shell (Bash)            | `.sh`, `#!/bin/bash`                | `references/shell.md`                       |
| C#                      | `.cs`                               | `references/csharp.md`                      |
| Objective-C / ObjC++    | `.m`, `.mm`, `.h` with `@interface` | `references/objective-c.md`                 |
| Swift                   | `.swift`                            | `references/swift.md`                       |
| Kotlin                  | `.kt`, `.kts`                       | `references/kotlin.md`                      |
| Dart                    | `.dart`                             | `references/dart.md`                        |
| HTML / CSS              | `.html`, `.css`, `.scss`            | `references/html-css.md`                    |
| JSON (APIs, data)       | `.json`, JSON API design            | `references/json.md`                        |
| XML (document formats)  | `.xml`, schema design               | `references/xml.md`                         |
| Markdown / docs         | `.md`, READMEs                      | `references/markdown.md`                    |
| R                       | `.R`, `.Rmd`                        | `references/r.md`                           |
| Haskell                 | `.hs`                               | `references/haskell.md`                     |
| Common Lisp             | `.lisp`, `.asd`                     | `references/common-lisp.md`                 |
| SystemVerilog / Verilog | `.sv`, `.svh`, `.v`                 | `references/verilog.md`                     |
| Vim script              | `.vim`, `vimrc`                     | `references/vimscript.md`                   |
| Tcl/Tk                  | `.tcl`                              | `references/tcl.md`                         |

For a header file (`.h`), decide between C++ and Objective-C by its contents. If
a rule you need is not covered in the condensed file, follow the source link at
the top of that file.

## Step 2 — Choose the mode

### Mode A: Write code in Google style

1. Read the language file.
2. Write the code following its Formatting, Naming, Language and Comments rules.
3. Add the documentation format the guide requires (e.g. Python
   `Args/Returns/Raises` docstrings, Javadoc summary fragments, Go doc comments
   starting with the name).
4. Before finishing, walk the file's **Review checklist** against your own
   output.
5. Mention the formatter/linter from the file's **Tools** line so the user can
   enforce it automatically (formatters beat manual style every time).

### Mode B: Review code against Google style

1. Read the language file.
2. Go through the code and collect violations. For each one report:
   - location (file:line or the snippet),
   - the rule (section name from the reference file),
   - the fix (show corrected code).
3. Group findings by severity:
   - **Must fix** — correctness/safety-related rules (mutable defaults, ignored
     errors, exceptions in Google C++, `unsafe` without justification, missing
     `@Override`, `var`, etc.).
   - **Should fix** — naming, imports, documentation.
   - **Nit** — pure formatting a formatter would fix automatically (suggest
     running the formatter instead of listing each one).
4. If asked, produce the fully corrected file.
5. Be honest: if the code is already compliant, say so; don't invent issues.

## Precedence

1. The project's own config and conventions (`.editorconfig`, `pyproject.toml`,
   `.clang-format`, `.eslintrc`, `rustfmt.toml`, existing file style) win.
2. Within a file, consistency with surrounding code wins over a rule change —
   every Google guide says "be consistent".
3. Otherwise apply the Google guide as condensed here.
4. Rules marked as specific to one codebase (e.g. *[Chrome]* / *[Fuchsia]* in
   Rust) only apply to that codebase.

## Shared principles across all guides

- Optimize for the **reader**, not the writer.
- **Be consistent** with the surrounding code.
- Let **tools** (formatters, linters) enforce mechanical style.
- Prefer clear names over comments; comments explain **why**.
- Commit messages: short imperative summary line (~50 chars), blank line, then
  wrapped body explaining what and why.

## Attribution

Condensed from Google's style guides, licensed CC BY 3.0
(https://creativecommons.org/licenses/by/3.0/). Not affiliated with or endorsed
by Google. Angular, Dart, Kotlin, Swift and Tcl summaries are condensed from the
external guides that google/styleguide links to (see each file's Source line).
