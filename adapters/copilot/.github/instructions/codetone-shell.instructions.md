---
applyTo: "**/*.sh,**/*.bash"
---

Precedence: the project's own formatter/linter config and the existing style of the file win over these rules; otherwise apply them.

# Shell (Bash) — Google Style (condensed)

Source: https://google.github.io/styleguide/shellguide.html

Tools: ShellCheck (recommended for all scripts). Not named by the guide but
compatible: `shfmt -i 2 -ci`.

## When to use shell

- **Bash only** for executables: start with `#!/bin/bash` and minimal flags; use
  `set` for options so `bash script.sh` still works.
- Shell is for small utilities and wrappers. If a script exceeds ~100 lines or
  has non-trivial control flow, rewrite it in a structured language.

## Files

- Executables: `.sh` or no extension — prefer `.sh` when a build rule renames
  the file, no extension when it goes directly on `PATH`. Libraries: `.sh` and
  not executable.
- SUID/SGID are forbidden — use `sudo`.
- Errors go to **STDERR** (write an `err()` helper that prints timestamp +
  message to `>&2`).

## Comments

- Every file starts with a top-level comment describing its contents (after the
  shebang and license).
- Every non-obvious function, and all library functions, need a header comment:
  description, `Globals:`, `Arguments:`, `Outputs:`, `Returns:`.
- Comment tricky code; `TODO(name|bug):` for TODOs.

## Formatting

- **2-space** indent, no tabs (except heredoc bodies with `<<-`).
- Max line **80**. For long strings use heredocs or embedded newlines.
- Pipelines: one line if they fit; otherwise one segment per line with `|` at
  the start of the continuation line, indented 2.
- `; then` and `; do` on the same line as `if`/`for`/`while`; `else`, `fi`,
  `done` on their own lines.
- `case`: alternatives indented 2; one-liners `pattern) cmd ;;`; multi-line with
  `;;` on its own line.
- Variables: prefer `"${var}"` (braced, quoted) over `$var`; don't brace
  single-char specials (`$1`, `$?`) unless needed.

## Quoting

- Always quote strings containing variables, command substitutions, spaces, or
  shell metacharacters.
- Use arrays for lists of elements, especially command-line flags:
  `"${flags[@]}"`.
- `"$@"` almost always (not `$*`).

## Features

- Use `$(command)` — never backticks.
- Use `[[ … ]]` over `[ … ]` / `test`.
- Test strings with `-z` / `-n` and `==` (not `=`); never filler chars like
  `"x${var}"`.
- Use explicit paths for wildcards: `rm -v ./*` not `rm -v *`.
- Avoid `eval`.
- Use arrays for lists; don't stuff lists into strings.
- Avoid piping into `while` (subshell loses variables); use process substitution
  `< <(cmd)` or `readarray`.
- Arithmetic: `(( … ))` or `$(( … ))`; never `let`, `$[ ]`, or `expr`. Beware
  `(( i++ ))` returning non-zero under `set -e`.
- No aliases in scripts — use functions.

## Naming

- Functions: `lower_with_under`; packages separated by `::`
  (`mypackage::my_func`); `()` required, `function` keyword optional but
  consistent; brace on the same line.
- Variables: `lower_with_under`; loop variables named after what they iterate.
- Constants and exported env vars: `UPPER_WITH_UNDER`, declared at top; use
  `readonly` / `declare -r` / `export`.
- Source files: lowercase with underscores.
- Use `local` for function variables; separate declaration from assignment when
  assigning command substitution (`local x; x="$(cmd)"`) so the exit code isn't
  masked.

## Structure

- Put all functions together right after constants. No executable code between
  functions.
- Scripts with at least one function need a `main` function, called last:
  `main "$@"`.

## Commands

- Always check return values: `if ! mv …; then …` or check `$?`; for pipes use
  `PIPESTATUS`.
- Prefer builtins (parameter expansion `${var//a/b}`, `(( ))`) over external
  commands like `sed`/`expr` when equivalent.

## Review checklist

- [ ] `#!/bin/bash`, passes shellcheck
- [ ] `"${var}"` quoted; arrays for flag lists; `"$@"`
- [ ] `$( )`, `[[ ]]`, `(( ))` — no backticks/`expr`/`let`
- [ ] `local` vars; `main "$@"` at the bottom
- [ ] errors to STDERR, return codes checked

<!-- Condensed from the Google Style Guides (https://github.com/google/styleguide), CC BY 3.0. Not affiliated with or endorsed by Google. -->
