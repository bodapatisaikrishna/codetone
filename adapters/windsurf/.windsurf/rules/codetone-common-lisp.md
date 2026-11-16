---
trigger: glob
globs: **/*.lisp,**/*.asd,**/*.cl
---

Precedence: the project's own formatter/linter config and the existing style of the file win over these rules; otherwise apply them.

# Common Lisp — Google Style (condensed)

Source: https://google.github.io/styleguide/lispguide.html

Tools: SLIME's `cl-indent` (the reference indenter). `lisp-critic` is a common
extra, not named by the guide.

## Existing code

- Fix old code as you go; don't churn unrelated code just for style.

## Formatting

- Correct spelling and grammar in comments and code.
- **100-column** limit. Prefer small, focused top-level forms.
- Spaces, not tabs; indent as Emacs/SLIME does (body forms indented 2 relative
  to the operator).
- File begins with a brief description of its contents, then `(in-package …)`.
  No author line; no copyright notice unless the file is distributed standalone.
- One blank line between top-level forms; no blank lines inside a form except to
  separate clear groups.
- No space after `(` or before `)`; no closing parens on their own line — stack
  them (exception: a closing top-level `eval-when`). Don't pad with spaces to
  align forms vertically.

## Documentation

- Docstrings everywhere the language allows (functions, classes, variables,
  packages).
- Explain non-obvious bug fixes and tricky code in comments.
- Comment semicolons: `;;;` for top-level/file sections, `;;` inside forms
  between lines, `;` at end of a line; always a space after the semicolons.

## Naming

- **All lowercase, words separated by hyphens** (`compute-total`); no
  underscores, no CamelCase.
- Global special variables in earmuffs: `*default-timeout*`. Constants in plus
  signs: `+max-size+`.
- Predicates: trailing `p` for single-word names (`emptyp`), `-p` for multi-word
  (`small-prime-p`).
- Don't prefix symbols with the library name — that's what packages are for.
- Package names designed to read well as prefixes; file names use hyphens.

## Code structure

- One package per file (`defpackage` + `in-package`), with explicit `:export`s.
  No package nicknames; no `::` access to internal symbols outside tests; prefer
  `:import-from` over `:use`; don't shadow `common-lisp` symbols; no dotted
  package names.
- **No new uses of CLOS** in new code (new `print-object` methods are fine).

## Language usage

- Mostly functional style; use side effects only when clearer or necessary.
- Use special variables sparingly; bind them with `let` rather than `setf` where
  possible.
- Be consistent with assignment forms within a package (e.g. one `setf` per
  assignment vs. grouped).
- `assert`, `check-type`, `etypecase` detect **internal bugs**; signal
  conditions (`error`) for user/external errors.
- Use type declarations judiciously; never in place of runtime checks for
  external input.

## Meta-language

- Macros only to express a clear repeated pattern that functions can't; keep
  them simple and hygienic (`gensym`/`with-gensyms`).
- Avoid `#.` read-time evaluation. **Never `eval` at runtime** in production.
  Never `intern`/`unintern` at runtime.

## Data representation

- `nil` for false and for the empty list (test with `endp`/`null`); when "no
  value" could be ambiguous, use an explicit descriptive symbol.
- Lists for homogeneous sequential containers; arrays for random access;
  structs/classes for heterogeneous records; pairs only for exactly two values.

## Proper forms

- Avoid `&aux` and `&allow-other-keys`; don't mix `&optional` with `&key`.
- Refer to functions as `#'fun`, not `'fun` (except for symbols meant to be
  redefined/late-bound).
- `when`/`unless` for one branch, `if` for two, `cond` for more.
- Prefer `eql` (or `equal`/`string=`/`=` as appropriate) over `eq`, except in
  performance-critical low-level code — treat `eq` as an unsafe optimization.
- `dolist`/`dotimes` for simple iteration; `loop` for complex ones.
- Use logging facilities instead of writing directly to `*standard-output*`.

## Review checklist

- [ ] `lower-hyphen-case`, `*specials*`, `+constants+`, `p` predicates
- [ ] docstrings; `;;;`/`;;`/`;` comment levels
- [ ] 100 cols; stacked closing parens
- [ ] no runtime `eval`/`intern`; no new CLOS

<!-- Condensed from the Google Style Guides (https://github.com/google/styleguide), CC BY 3.0. Not affiliated with or endorsed by Google. -->
