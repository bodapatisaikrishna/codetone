---
trigger: glob
globs: **/*.cc,**/*.cpp,**/*.cxx,**/*.h,**/*.hpp
---

Precedence: the project's own formatter/linter config and the existing style of the file win over these rules; otherwise apply them.

# C++ — Google Style (condensed)

Source: https://google.github.io/styleguide/cppguide.html

Tools: `clang-format --style=Google`, `cpplint` (community fork:
https://github.com/cpplint/cpplint), `clang-tidy` with `google-*` checks.

## Language version

- Target **C++20**; don't use C++23 features yet. Avoid non-standard compiler
  extensions.

## Header files

- Every `.cc` normally has a matching `.h`. Headers must be self-contained
  (compile on their own) and end in `.h`.
- Use `#define` guards named `<PROJECT>_<PATH>_<FILE>_H_` (not `#pragma once`).
- Include what you use; don't rely on transitive includes.
- Never forward-declare entities your project doesn't own; avoid forward
  declarations in general — include the header.
- Only define functions in headers if they are short (~10 lines) or templates.
- Include order (blank line between groups): related header → C system headers →
  C++ standard library → other libraries → your project. Alphabetical within
  groups. Use full project paths, no `.`/`..`.

## Scoping

- Put code in namespaces named after the project/path. Never
  `using namespace foo;`. No inline namespaces; don't declare things in `std`.
- Comment closing braces of namespaces: `}  // namespace foo`.
- File-local items: unnamed namespace or `static` in `.cc` files — never in
  headers.
- Prefer namespace-scoped non-member functions over static-member utility
  classes.
- Declare locals in the narrowest scope, initialize at declaration.
- Objects with static storage duration must be **trivially destructible**
  (`constexpr`, plain data, or function-local static pointer). No static
  `std::string`, `std::map`, smart pointers, etc.
- `thread_local` at namespace scope must be `constinit`.

## Classes

- Constructors shouldn't call virtual functions or do work that can fail — use a
  factory or `Init()`.
- Mark single-argument constructors and conversion operators **`explicit`**
  (except copy/move).
- Make copy/move semantics explicit: declare or `= delete` them in the public
  section.
- `struct` only for passive data with all-public fields and no invariants;
  otherwise `class`.
- Prefer a `struct` with named fields over `std::pair`/`std::tuple`.
- Prefer composition; inheritance must be `public`. Mark overrides with exactly
  one of `override` or `final` (not `virtual`). Multiple implementation
  inheritance is discouraged.
- Overload operators only where meaning is obvious and consistent with
  built-ins. Never overload `&&`, `||`, `,`, unary `&`, or `""` literals.
- All data members `private` (except constants and structs).
- Declaration order: `public:` → `protected:` → `private:`; within each:
  types/aliases, static constants, factory functions, constructors/assignment,
  destructor, methods, data members.

## Functions

- Prefer return values over output parameters. Inputs: values or `const&`;
  optional inputs: `std::optional` or `const T*`. Outputs: references (non-null)
  or pointers (nullable). Put inputs before outputs.
- Keep functions short (~40 lines is a signal to split).
- Overload only when callers can't be surprised; default arguments allowed on
  non-virtual functions only.
- Trailing return type only when required (e.g. lambdas) or clearly more
  readable.

## Other features

- Ownership: single ownership with `std::unique_ptr`; `std::shared_ptr` only
  with a real reason. Never `std::auto_ptr`.
- **No C++ exceptions.**
- Avoid RTTI (`typeid`, `dynamic_cast`) outside tests; `dynamic_cast` is OK when
  program logic guarantees the derived type (otherwise prefer virtual methods or
  Visitor).
- Use C++ casts (`static_cast`, etc.) or brace init for arithmetic conversions
  (`int64_t{x}`); no `(int)x` casts except to `void`; `T(x)` only for class
  types.
- Streams only for ad-hoc, developer-facing I/O; prefer logging libraries over
  `std::cerr` and `absl/strings` over `std::stringstream`; never for user-facing
  or untrusted I/O.
- Prefer `++i` over `i++` when the value is unused.
- Use `const` wherever meaningful; `constexpr`/`constinit` for true constants.
- Integers: `int` for ordinary values; `<cstdint>` sized types (`int64_t`) when
  size matters. Avoid unsigned types except bit patterns. Don't use
  `long`/`short` etc.
- Macros: avoid; don't define them in `.h` files. If you must, `#define` right
  before use and `#undef` right after. A macro exported from a header needs a
  globally unique `PROJECT_` prefix.
- Use `nullptr` (not `NULL`/`0`), `sizeof(var)` over `sizeof(type)`.
- `auto` only when it makes code clearer (iterators, obvious types,
  `make_unique`). Avoid on public APIs.
- Lambdas: prefer explicit captures when the lambda may escape the current
  scope; use default `[=]` only for short lambdas binding a few obvious
  variables; write `this` explicitly when capturing it.
- Avoid complex template metaprogramming; prefer concepts (`requires`) over
  SFINAE. No C++20 modules; avoid coroutines unless approved libraries.
- Don't use `<ratio>`, `<cfenv>`, `<filesystem>` (and other disallowed std
  features listed in the guide).
- `switch` statements not on an enum must always have a `default` (enum switches
  rely on the compiler's unhandled-value warning); mark fallthrough with
  `[[fallthrough]];`.

## Naming

| Kind                                                        | Style                                            | Example            |
| ----------------------------------------------------------- | ------------------------------------------------ | ------------------ |
| files                                                       | `lower_with_under.cc/.h` (or dashes per project) | `url_table.cc`     |
| types (class, struct, alias, enum, concept, template param) | `PascalCase`                                     | `UrlTable`         |
| variables, params                                           | `snake_case`                                     | `table_name`       |
| class data members                                          | `snake_case_` (trailing underscore)              | `table_name_`      |
| struct data members                                         | `snake_case` (no underscore)                     | `num_entries`      |
| constants (`constexpr`/`const` static storage)              | `kPascalCase`                                    | `kDaysInAWeek`     |
| functions                                                   | `PascalCase` (accessors may be `snake_case`)     | `AddTableEntry()`  |
| namespaces                                                  | `snake_case`                                     | `websearch::index` |
| enumerators                                                 | `kPascalCase`                                    | `kOk`              |
| macros                                                      | `UPPER_SNAKE` with project prefix                | `MYPROJ_ROUND`     |

## Comments

- `//` or `/* */` — be consistent (`//` is far more common).
- File comment: license boilerplate; describe contents if the file isn't a
  single obvious class.
- Every non-obvious class/struct: what it is for and how to use it,
  thread-safety notes.
- Function declarations: what it does, inputs/outputs, ownership, null handling,
  performance; written descriptively ("Opens the file") not imperatively.
- Implementation comments explain tricky parts. Write complete sentences with
  punctuation.
- TODO: `// TODO(bug 12345): explanation.` — bug ID, name, or e-mail in
  parentheses.

## Formatting

- **80** column limit. Spaces only, **2-space** indent.
- Return type on the same line as the function name; wrapped params aligned with
  the first or indented 4.
- Braces: opening `{` on the same line; `} else {` on one line.
- `if (cond) {` — space after keyword, none inside parens. Always use braces for
  multi-line bodies.
- Pointers/references: `char* c` or `char *c` — consistent within a file; never
  declare multiple pointers in one line.
- Wrap long boolean expressions with operators at line end consistently.
- Don't wrap `return` value in parentheses.
- `public:`/`private:` indented **1 space**; members indented 2.
- Constructor initializer lists: on one line, or break after `:` indented 4.
- Namespace contents are **not** indented.
- Preprocessor directives start at column 0.
- Minimal vertical whitespace; no blank lines at start/end of blocks.

## Review checklist

- [ ] `#define` guards, include order, IWYU
- [ ] no exceptions, no `using namespace`, no non-trivial static objects
- [ ] `explicit` single-arg ctors; `override` on overrides
- [ ] names: `PascalCase` funcs/types, `snake_case_` members, `kConstant`
- [ ] 80 cols, 2-space indent, 1-space access specifiers

<!-- Condensed from the Google Style Guides (https://github.com/google/styleguide), CC BY 3.0. Not affiliated with or endorsed by Google. -->
