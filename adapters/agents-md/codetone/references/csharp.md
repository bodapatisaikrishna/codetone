# C# — Google Style (condensed)

Source: https://google.github.io/styleguide/csharpguide.html

Tools: `dotnet format` with an `.editorconfig` matching the rules below (2-space
indent, 100 cols).

## Naming (follows Microsoft guidelines + CoreFX for privates)

| Kind                                                          | Style                                                        |
| ------------------------------------------------------------- | ------------------------------------------------------------ |
| classes, methods, enums, public fields/properties, namespaces | `PascalCase`                                                 |
| locals, parameters                                            | `camelCase`                                                  |
| private / protected / internal fields and properties          | `_camelCase`                                                 |
| interfaces                                                    | `IPascalCase`                                                |
| files and directories                                         | `PascalCase`, file named after its main class (`MyClass.cs`) |

- Casing ignores modifiers (`const`, `static`, `readonly` don't change the
  case).
- Acronyms are words: `MyRpc`, not `MyRPC`.
- One core class per file where possible. Namespaces ≤ 2 levels deep.

## Organization

- Modifier order:
  `public protected internal private new abstract virtual override sealed static readonly extern unsafe volatile async`.
- `using` directives at the top, outside namespaces; `System.*` first, then
  alphabetical.
- Member order by group: nested types/enums/delegates/events → static, const,
  readonly fields → fields & properties → constructors & finalizers → methods.
- Within each group: public → internal → protected internal → protected →
  private. Keep interface implementations together.

## Whitespace / formatting (derived from Google Java style)

- One statement per line; one assignment per statement.
- **2-space** indent, no tabs. Column limit **100**.
- No line break before `{`; `} else` on the same line; braces even when
  optional.
- Space after `if`/`for`/`while` and after commas; none inside parentheses.
- No space between unary operator and operand; spaces around other operators.
- Continuation lines indented **4**; braces for initializers/lambdas don't count
  as continuations.
- Wrapped arguments: align with the first argument, or if no room, put them on
  following lines indented 4.

## Coding guidelines

- Make everything that can be `const` `const`; otherwise prefer `readonly`.
  Prefer named constants over magic numbers.
- Parameters: least-capable type (e.g. `IReadOnlyCollection`; `IEnumerable` only
  if iterated at most once). Returns: when transferring ownership, the most
  capable interface (`IList`, not `List`); otherwise the most restrictive.
- Be careful returning lazy generators (`yield`) — callers may enumerate
  multiple times.
- Properties: expression-bodied for simple read-only ones
  (`public int Foo => _foo;`); use `{ get; set; }` auto-properties otherwise.
- Expression bodies: use sparingly, mostly for simple properties and lambdas.
- Almost always use a class; use a struct only for small value-like types (e.g.
  `Vector3`) that are short-lived or embedded in other objects.
- Lambdas: use a named method if the lambda is non-trivial (more than a couple
  of statements) or reused in several places.
- Field initializers encouraged.
- Extension methods only when you can't change the original source **and** the
  feature is a core, general one; put them only in core libraries available
  everywhere; when in doubt, don't add one.
- `out` for extra returns (placed after all other parameters); `ref` only when
  mutating an input is necessary — never as a performance optimisation for
  structs.
- LINQ: prefer simple single-line calls or plain loops over long chains; prefer
  method syntax over query syntax.
- Prefer `List<>` to arrays in public APIs (arrays OK for fixed-size or
  performance).
- Prefer a named class over `Tuple<>`, especially for complex return types.
- String building: use what reads best (usually interpolation); `StringBuilder`
  in loops.
- Don't alias long type names with `using` (sign of over-generic code).
- Object initializers are fine for plain-old-data types; avoid them for
  classes/structs that have constructors.
- For struct lookups, return a `bool` success flag + `out` value instead of
  null/default.
- Don't remove from a collection while iterating — use `RemoveAll` or iterate a
  copy.
- Invoke delegates via `Foo?.Invoke()`.
- `var` encouraged when the type is obvious or long; avoid for basic types or
  when it hides meaning.
- Attributes on the line above what they decorate, one per line.
- Name arguments when meaning isn't clear from the call (`Foo(useCache: true)`),
  or use an enum.

## Comments (derived from Google C++)

- Every non-obvious class: comment describing purpose and usage.
- Almost every method: comment describing what it does and how to use it (not
  how it's implemented).
- Data members: purpose and invariants clear.
- Tricky code blocks: explanatory comments before them.

## Review checklist

- [ ] `PascalCase` public, `camelCase` locals, `_camelCase` private fields, `I`
  interfaces
- [ ] modifier and member ordering
- [ ] 2-space indent, 100 cols, braces always
- [ ] `const`/`readonly`, least-capable parameter types
