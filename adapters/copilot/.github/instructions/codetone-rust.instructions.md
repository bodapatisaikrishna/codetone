---
applyTo: "**/*.rs"
---

Precedence: the project's own formatter/linter config and the existing style of the file win over these rules; otherwise apply them.

# Rust — Google Style (condensed)

Source: https://google.github.io/styleguide/rustguide.html

Tools: `rustfmt` via your codebase's formatter (config: `max_width = 100`,
`imports_granularity = "Module"`, `hex_literal_case = "Lower"`,
`format_macro_matchers = true`). Several rules map to Clippy lints.

> This guide builds on the official Rust Style Guide and API Guidelines. Rules
> tagged *[Chrome]* or *[Fuchsia]* apply only to those codebases — skip them
> elsewhere.

## Code organization

- Prefer small crates *[Chrome]*; flat file layout for library sources
  *[Chrome]*.
- Name source files / leaf modules after their primary item (`foo_bar.rs` for
  `FooBar`).
- Non-leaf modules (`mod.rs`, `lib.rs`) contain only `mod` declarations and
  re-exports — no API implementations.
- **No glob imports** (`use foo::*`), except: `use super::*` in inline modules
  (e.g. tests), `use Enum::*` in code mainly about that enum,
  `pub use submodule::*` in non-leaf modules, and private C++-namespace merging.
  Third-party preludes only if the reviewer allows; don't define preludes.
- One module per `use` statement (rustfmt `imports_granularity = Module`).
- Import traits locally (inside the function) unless used throughout the file.
- Call top-level functions qualified by their module (`fs::read_to_string(…)`);
  import and use **types and traits unqualified**.

## Formatting

- Always run the formatter. `#[rustfmt::skip]` only for deliberate manual
  alignment (e.g. matrices) or generated code — never for personal preference.

## Ownership and borrowing

- Prefer unique ownership and borrows over `Rc`/`Arc`.
- `.clone()` only when a deep copy is genuinely needed — don't clone to silence
  the borrow checker.

## Function inputs and outputs

- Accept flexible borrowed types: `&str` not `&String`, `&[T]` not `&Vec<T>`,
  `&Path` not `&PathBuf`.
- Prefer returning iterators (`impl Iterator<Item = T>`) when callers may not
  need a collection; reusable libraries may accept `impl IntoIterator`.
- Accept `impl Into<T>` only where it materially improves ergonomics.
- **Use enums instead of `bool` parameters** when the meaning isn't obvious at
  the call site.
- Errors: choose `Option`, `Result`, or panic based on the API contract;
  recoverable failures return `Result`.

## Types

- Newtypes (`struct UserId(u64)`) for distinct semantics; type aliases only for
  brevity.
- Prefer named fields over tuples and tuple structs (except newtypes).

## Traits

- Standard traits (`Debug`, `Clone`, `Default`, `PartialEq`, `Display`, `From`):
  libraries implement them proactively; application code adds them as needed.
  Prefer them over custom methods with the same meaning.
- Use `#[derive(...)]` whenever possible instead of manual impls.
- Libraries: prefer generics (`impl Trait`, `T: Trait`) in arguments;
  `dyn Trait` when code size, heterogeneous collections, or object safety
  matter.
- Define a trait only for generic bounds (`T: Trait`), `impl Trait`/`dyn Trait`
  parameters or returns, or extension traits — otherwise use an inherent `impl`;
  never just to organize code.
- Extension traits are named with an `Ext` suffix.
- Pair important `From` impls with an explicit constructor (`Foo::from_bar`).
- "Options" structs with all-public fields implement `Default`.

## Concurrency

- Never reach inside a poisoned mutex to get at its contents.
- *[Chrome]* no `async`/`.await`, no `std::thread` (use sequences). *[Fuchsia]*
  use `fuchsia_sync::Mutex`.

## Macros

- Prefer, in order: functions → generics/traits → `macro_rules!` → procedural
  macros. Use macros only when nothing simpler works.

## Naming

- Follow Rust std conventions: `snake_case` functions/modules/variables,
  `UpperCamelCase` types/traits/enum variants, `SCREAMING_SNAKE_CASE`
  consts/statics.
- Method names follow std patterns: `as_`/`to_`/`into_` conversions,
  `iter`/`iter_mut`/`into_iter`, `with_` builders, `try_` fallible variants.
- Lifetimes descriptive where they carry meaning (`'conn`, not just `'a`) for
  type lifetimes.
- Generic parameters short (`T`, `K`, `V`, or short words).
- Constructors: `new()`, `new_with_foo()` when there are several, `try_new()` if
  it returns `Result`; conversions: `from_foo()` with a matching `From` impl.
  (`with_foo()` is for closure-taking accessors.)
- Avoid abbreviations readers might not know.

## Documentation

- Doc comments (`///`) on all public items (consider `#![deny(missing_docs)]`).
  Start with a one-line summary; document panics, errors, and safety
  (`# Panics`, `# Errors`, `# Safety`).

## Other features

- No `unsafe` unless there is no safe way; every `unsafe` block needs a
  `// SAFETY:` comment justifying it.
- No unstable/nightly features.
- Getters: no `get_` prefix (`fn name(&self)`), setters `set_name`; `*_mut` for
  mutable access.
- Implement related APIs together (`len` with `is_empty`, `iter` with
  `IntoIterator`).
- Don't use `#[doc(hidden)]` items you don't own.
- Mark public functions `const` only if they'll stay `const`.
- Operator overloading only for mathematical/logical meaning.
- `#[non_exhaustive]` on public enums and public structs with public fields used
  by other teams.
- `#[must_use]` on pure functions and functions returning errors or critical
  info (unless the type is already `#[must_use]`, like `Result`); on types for
  error types and lazily evaluated computations.
- No code running before `main()` (no life-before-main ctors).

## Implementation

- Add explicit type annotations where inference makes code hard to follow.
- Prefer pattern matching (`if let`, `match`, `let … else`) over
  check-then-`unwrap`.
- Prefer `expect("why this can't fail")` over `unwrap()`.
- When matching a `non_exhaustive` enum, list every known variant (unneeded ones
  go with the `_` arm, e.g. `A | _ => {}`); if you only care about some, use
  `if let`/`let … else`.
- Add context messages to assertions (`assert!(x > 0, "x was {x}")`).
- Use a plain `for` loop when an iterator chain becomes hard to read.
- Don't call `std::panic::catch_unwind` in first-party code (only as
  never-relied-upon defense in depth on `panic=unwind` builds).
- Prefer `format!`/`write!` over manual concatenation.
- Use the codebase's own test framework where one exists.

## Review checklist

- [ ] rustfmt clean; no glob imports; types imported unqualified, functions
  module-qualified
- [ ] `&str`/`&[T]` params, enums not bool flags
- [ ] derive std traits; `Default` for option structs
- [ ] `expect` over `unwrap`; `// SAFETY:` on unsafe
- [ ] docs on public items; `#[non_exhaustive]`/`#[must_use]` where relevant

<!-- Condensed from the Google Style Guides (https://github.com/google/styleguide), CC BY 3.0. Not affiliated with or endorsed by Google. -->
