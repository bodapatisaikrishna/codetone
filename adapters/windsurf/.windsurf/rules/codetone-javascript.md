---
trigger: glob
globs: **/*.js,**/*.mjs,**/*.cjs
---

Precedence: the project's own formatter/linter config and the existing style of the file win over these rules; otherwise apply them.

# JavaScript — Google Style (condensed)

Source: https://google.github.io/styleguide/jsguide.html

Tools: `clang-format` and the Closure Compiler (named by the guide). Third-party
options not named by the guide: ESLint with `eslint-config-google`, Prettier
configured to match.

## Source files

- File names: all lowercase, may contain `_` or `-`, extension `.js`. UTF-8.
- Use special escape sequences (`\n`, `\'`) not numeric escapes; for other
  non-ASCII characters use the literal character or a `\u` escape, whichever
  reads more clearly; non-printable characters use escapes with a comment.
- Order (one blank line between): license → `@fileoverview` → `goog.module`/ES
  `import`s → `goog.require`s → implementation.
- ES modules: named exports only (**no default exports**); import paths include
  `.js`; don't line-wrap imports/exports.

## Formatting

- Braces required for all control structures (a single-line `if` with no else
  may omit them).
- K&R braces; `} else {` on one line; empty blocks `{}`.
- **+2 spaces** indent. One statement per line. **Semicolons required** (no ASI
  reliance).
- Column limit **80** (exceptions: long URLs, `goog.module`/`require`/import
  lines, shell commands in comments).
- Wrap at higher syntactic levels; break **after** operators (but **before**
  `.`); a comma stays with the preceding token. Continuation lines indent
  **+4**.
- Spaces after keywords (`if (`), before `{`, around binary/ternary ops, after
  `,` and `;` in `for`, after `//`. None inside `()` `[]`.
- Array/object literals may be "block-like" (trailing comma when the closing
  bracket is on its own line).
- No horizontal alignment required (discouraged).

## Language features

- Use `const` by default, `let` when reassigned; **never `var`**. One variable
  per declaration; declare near first use.
- Arrays: trailing commas in multi-line literals; never `new Array()`; no
  non-numeric properties on arrays; destructuring and spread OK.
- Objects: trailing commas; never `new Object()`; don't mix quoted and unquoted
  keys (computed keys count as quoted, symbols excepted); method shorthand is
  fine. Enums: `@enum` object literal, constant, values only string/number
  literals, nothing added later.
- Classes: use `class` syntax; constructors optional; set all fields in the
  constructor; don't manipulate `prototype` directly; **no JS getter/setter
  properties** (use ordinary methods) unless a framework or external API forces
  it — then getters must not change observable state; `toString` must not have
  side effects.
- Functions: arrow functions for nested functions and callbacks (avoid
  `const self = this`); default params must be side-effect-free; use rest
  params, not `arguments`.
- Strings: **single quotes**; template literals for complex concatenation; no
  line continuations with `\`.
- Numbers: decimal, `0x`, `0o`, `0b` — never leading-zero octal.
- Control: `for…of` preferred; `for…in` only on dict-style objects with
  `hasOwnProperty`; `switch` must have a `default` (last) and comment
  intentional fall-through; throw only `Error` objects.
- Equality: `===`/`!==` — except `== null` to check both `null` and `undefined`.
- `this` only in class constructors/methods, arrow functions inside them, or
  functions with explicit `@this`.
- **Disallowed:** `with`, `eval`, `Function(...string)`, `debugger` in commits,
  modifying built-in prototypes, wrapper objects (`new String`), relying on ASI,
  non-standard features.

## Naming

| Kind                                                | Style                                        |
| --------------------------------------------------- | -------------------------------------------- |
| packages / namespaces                               | `lowerCamelCase`                             |
| classes, interfaces, records, typedefs              | `UpperCamelCase`                             |
| methods, functions                                  | `lowerCamelCase` (private may end with `_`)  |
| enums                                               | `UpperCamelCase` name, `CONSTANT_CASE` items |
| constants (deeply immutable, module-level / static) | `CONSTANT_CASE`                              |
| non-constant fields, params, locals                 | `lowerCamelCase`                             |

- Names descriptive; avoid unclear abbreviations. Treat acronyms as words
  (`loadHttpUrl`).
- No `$` prefix except to follow a framework convention.

## JSDoc

- Use `/** … */` on classes, fields, methods, functions; `//` for implementation
  comments.
- Parameter and return **types are required** in JSDoc
  (`@param {string} name Description.`), even on same-signature `@override`s;
  `@return` may be omitted only if the function has no non-empty `return`.
  Descriptions (not types) may be omitted when obvious.
- Use Markdown in JSDoc; wrap at 80 with +4 continuation indent.
- Class comments describe the class; `@enum` and `@typedef` need descriptions.
- Visibility: `@private`, `@protected`, `@package`; mark overrides with
  `@override`.
- `@fileoverview` for files with multiple top-level items.

## Policies

- When the guide is silent, match the surrounding file.
- Fix or justify all compiler warnings (`@suppress` with a comment).
- Mark deprecated APIs with `@deprecated` and a migration note.

## Review checklist

- [ ] `const`/`let`, never `var`; semicolons everywhere
- [ ] single quotes; `===`; no default exports
- [ ] 80 cols, 2-space indent, +4 continuation
- [ ] JSDoc with types on public functions
- [ ] no `eval`/`with`/prototype hacks

<!-- Condensed from the Google Style Guides (https://github.com/google/styleguide), CC BY 3.0. Not affiliated with or endorsed by Google. -->
