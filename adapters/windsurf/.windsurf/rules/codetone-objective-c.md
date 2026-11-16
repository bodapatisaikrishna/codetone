---
trigger: glob
globs: **/*.m,**/*.mm
---

Precedence: the project's own formatter/linter config and the existing style of the file win over these rules; otherwise apply them.

# Objective-C — Google Style (condensed)

Source: https://google.github.io/styleguide/objcguide.html

Tools: `clang-format --style=Google` (with ObjC settings), Xcode warnings as
errors.

## Principles

- Optimize for the reader; be consistent; be consistent with **Apple SDK**
  conventions; a rule must pull its weight.

## Naming

- Long, descriptive names in the Apple style: `insertObject:atIndex:` reads like
  a sentence.
- **Prefixes** (3+ characters is best practice; Apple reserves 2-letter):
  required for classes/protocols in code shared across applications and for
  non-static functions and external constants; recommended otherwise.
- Files: named after the class; `.h`, `.m`, `.mm` (ObjC++); categories
  `ClassName+CategoryName.h`.
- Classes and protocols: `UpperCamelCase` (with prefix where required).
- Category names and category methods on system classes: prefixed
  (`gtm_myMethod`) to avoid collisions.
- Methods: `lowerCamelCase`; read as a sentence; don't prefix getters with `get`
  (`- (id)name`), booleans may use `is` (`isEnabled`); don't use `and` to join
  params (except for distinct actions).
- Functions: `UpperCamelCase` with prefix (`GTMSomeFunction`).
- Variables: locals/params `lowerCamelCase`; ivars `_lowerCamelCase`;
  file-scope/global variables `gName`; external constants with the project/class
  prefix (`ABCErrorDomain`); `kName` only for static constants inside `.m`
  files.
- Avoid abbreviations except widely known ones; acronyms all-caps in names
  (`URLString`, `HTTPRequest`).
- Use inclusive language.

## Types and declarations

- Avoid forward declarations of classes/protocols where an `#import` works
  (except to break cycles).
- Method declarations in headers only for public API; don't redeclare overrides.
- Declare locals close to first use; initialize at declaration (ARC zeroes
  object pointers, but initialize scalars).
- Avoid unsigned integers except to match system interfaces (`NSUInteger`) or
  for flags/bitmasks (often `NS_OPTIONS`/`NS_ENUM` is better); use `int64_t`
  etc. where exact size matters (protos, file sizes).

## Comments

- File comment with license; describe file contents if needed.
- Every interface, category, protocol: comment describing purpose. Public
  methods/properties: doc comments (`///` or `/** */`) describing what, params,
  return value.
- Use backticks or `|var|` to refer to symbols in comments.
- Document ownership and nullability assumptions.

## C / Cocoa features

- Avoid macros, especially ones that define methods or obscure control flow;
  prefer `static const` / `inline` functions. If used, `ALL_CAPS` and prefixed.
- `nil` for ObjC object/class pointers; `nullptr` for all other pointers (use
  `NULL` only where C23 isn't supported); `nullptr` in ObjC++.
- Identify designated initializers with `NS_DESIGNATED_INITIALIZER`; override
  the superclass designated initializer.
- Don't call accessors/send messages to `self` in `init`/`dealloc` — access
  ivars directly.
- Instance variables in headers must be `@protected` or `@private`; prefer class
  extensions or properties.
- **Don't use `+new`** — use `alloc]init]`.
- Keep the public API minimal; private methods in a class extension in the `.m`.
- `#import` for ObjC/ObjC++ headers, `#include` for C/C++ headers. Include
  order: related header → OS headers → language library → other dependencies →
  project headers. Use umbrella headers for system frameworks
  (`@import Foundation;` or `#import <Foundation/Foundation.h>`).
- `copy` properties for types with mutable subclasses (`NSString`, `NSArray`,
  blocks).
- Use lightweight generics: `NSArray<NSString *> *`.
- **Avoid throwing exceptions**; use `NSError **` for recoverable errors.
- `nil` messaging is safe — only check for `nil` where the logic needs it.
- Annotate nullability (`nullable`/`nonnull`, `NS_ASSUME_NONNULL_BEGIN/END`).
- `BOOL` pitfalls: don't cast large integers to `BOOL`; compare with `YES`/`NO`
  only via truthiness, never `== YES`.
- Delegates: `weak` references; protocol methods prefixed by the sender
  (`- (void)tableView:(…)didSelect…`).

## Objective-C++

- Use the style of the language being written: ObjC style inside
  `@interface/@implementation`, C++ style for C++ classes.

## Formatting

- **2-space** indent, no tabs. Column limit **100**.

- Method declarations: one space after `-`/`+`; colons aligned when wrapped
  (`clang-format` does this).

- Space after `if`/`for`/`while`; braces may be omitted only when the whole
  statement fits on one line; if there's an `else`, both clauses use braces;
  `} else {` on one line.

- Invocations with multiple inline blocks may left-align parameter names at a
  4-space indent.

- `NSString *name` is typical, but the space before `*` is optional — be
  consistent with the file.

- Keep functions short; use vertical whitespace sparingly.

- Mark intentional style deviations with `// NOLINT` (end of line) or
  `// NOLINTNEXTLINE` (previous line).

## Review checklist

- [ ] 3+ letter prefixes on public symbols and categories
- [ ] `_ivar`, `kConstant`, no `get` prefix
- [ ] designated initializers marked; no `+new`; no exceptions for errors
- [ ] nullability + lightweight generics annotated
- [ ] 2-space indent, 100 cols

<!-- Condensed from the Google Style Guides (https://github.com/google/styleguide), CC BY 3.0. Not affiliated with or endorsed by Google. -->
