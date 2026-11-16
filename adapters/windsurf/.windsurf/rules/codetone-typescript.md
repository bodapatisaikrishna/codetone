---
trigger: glob
globs: **/*.ts,**/*.tsx
---

Precedence: the project's own formatter/linter config and the existing style of the file win over these rules; otherwise apply them.

# TypeScript — Google Style (condensed)

Source: https://google.github.io/styleguide/tsguide.html

Tools: all files must pass type checking with the standard toolchain; formatting
is delegated to an automatic formatter. Third-party options not named by the
guide: `gts`, Prettier, ESLint, `tsc --strict`.

## Source files

- UTF-8. Order: copyright → `@fileoverview` → imports → implementation,
  separated by one blank line.

## Imports / exports

- Use ES6 `import`; module imports (`import * as foo`) for big APIs, named
  imports for frequently used symbols. Relative paths (`./foo`) within the same
  project.
- **No default exports** — always named exports.
- **No `namespace Foo {}`**, no `require` (`import x = require(...)`), no
  `/// <reference>` for modules.
- `import type` is allowed for type-only imports; use `export type` when
  re-exporting types.
- Don't export mutable bindings (`export let`).
- Don't create container classes with only static members for namespacing —
  export functions/consts.

## Language features

- `const`/`let`, **never `var`**. One variable per declaration.
- Arrays: don't use `Array()` constructor; use literals or `Array.from`.
- Objects: no `Object()` constructor; iterate with `Object.keys/entries` +
  `for…of`, not raw `for…in`.
- Classes: no semicolons after class bodies; method declarations separated by a
  blank line.
  - Use TS visibility (`private`, `protected`); **no `#private` fields**.
  - Don't write `public` (default) except on non-readonly parameter properties.
  - Mark never-reassigned properties `readonly`. Use parameter properties
    instead of boilerplate assignments.
  - Initialize fields where declared when possible.
  - Getters must be pure; don't create pointless pass-through accessors.
- Functions: prefer function declarations for named top-level functions; arrow
  functions for callbacks/nested; no `function` expressions. Arrow bodies: block
  body when the return value is unused.
- `this` only in class methods/arrow functions; don't rebind with `bind`
  unnecessarily.
- Strings: **single quotes**; template literals for interpolation; no `\` line
  continuations.
- Numbers: decimal, `0x`, `0o`, `0b`. Parse with `Number()` and check for `NaN`;
  never unary `+`; `parseInt`/`parseFloat` only for non-decimal radixes.
- Control flow: braces on all blocks (exception: an `if` that fits entirely on
  one line may omit them); `for…of` for arrays; `switch` needs `default`; no
  fall-through for non-empty cases.
- Equality: `===`/`!==` except `== null`.
- Exceptions: throw only `Error` (or subclasses) with `new`; catch as `unknown`
  and narrow.
- Type assertions: `x as Foo`, never `<Foo>x`; avoid non-null `!` unless
  justified with a comment.
- Decorators: no custom ones unless from frameworks (Angular etc.); place
  immediately before the target.
- **Disallowed:** `const enum` (use `enum`), wrapper objects (`new String`),
  modifying builtins, `eval`, `Function(...)`, `debugger`, `with`, ASI reliance,
  `@ts-ignore`/`@ts-expect-error` (except in tests), `@ts-nocheck`.

## Naming

| Kind                                                              | Style            |
| ----------------------------------------------------------------- | ---------------- |
| classes, interfaces, types, enums, decorators, type params        | `UpperCamelCase` |
| variables, params, functions, methods, properties, module aliases | `lowerCamelCase` |
| global/static constants, enum values                              | `CONSTANT_CASE`  |

- **No `_` prefix/suffix** for privacy; no `I` prefix for interfaces; no
  Hungarian; treat acronyms as words (`loadHttpUrl`).
- `$` suffix allowed for Observables if the project already does it.
- Type parameters: `T` or `UpperCamelCase`.

## Type system

- Rely on inference for trivially inferred types (`const x = 5`); annotate
  complex return types and public APIs.
- Don't include `null`/`undefined` in type aliases — add them at use sites. (No
  general preference between `undefined` and `null`.)
- Prefer **interfaces over type-literal aliases** for object shapes.
- Arrays: `T[]` for simple element types, `Array<T>` for complex ones (unions,
  objects).
- Index signatures need meaningful key names; prefer `Map`/`Set` or `Record`
  when appropriate.
- Avoid `any` — use `unknown`, a specific type, or a generic; if you must,
  comment why.
- Avoid `{}` type; use `unknown`, `Record<string, T>`, or `object`.
- Use lowercase primitives (`string`), never
  `String`/`Boolean`/`Number`/`Object`.
- Avoid return-type-only generics.
- Keep mapped/conditional types simple; prefer explicit interfaces.

## Comments

- `/** JSDoc */` for documentation, `//` for implementation notes.
- Don't repeat types in JSDoc (`@param {string}`) — TypeScript already has them.
- Document all top-level exports, classes, non-obvious methods/params. JSDoc
  goes **before** decorators.
- Comments must add information beyond the name/type.

## Review checklist

- [ ] named exports only; no namespaces
- [ ] no `var`, `any`, `#private`, `const enum`, `@ts-ignore`
- [ ] interfaces for object shapes; no `null`/`undefined` in type aliases
- [ ] single quotes, `===`, braces on all control blocks (only a one-line `if`
  may omit them)
- [ ] no `_` private naming, no `I`-prefixed interfaces

<!-- Condensed from the Google Style Guides (https://github.com/google/styleguide), CC BY 3.0. Not affiliated with or endorsed by Google. -->
