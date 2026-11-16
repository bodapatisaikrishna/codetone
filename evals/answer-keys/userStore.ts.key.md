# Answer key — userStore.ts (15 seeded violations)
T1 `// @ts-ignore` used
T2 double-quoted strings (should be single quotes)
T3 `namespace Utils {}` — namespaces not allowed
T4 `const enum` — must use plain `enum`
T5 `IUser` — no `I` prefix on interfaces
T6 NOT SCORED — `email: string | undefined` vs `email?:` is not a rule in the current guide (removed after source audit)
T7 `type Settings = {...}` — prefer interface for object shapes
T8 `export default` — no default exports
T9 `#secret` — no #private fields
T10 `_cache` — no underscore prefix for private members
T11 `any` type used
T12 explicit `public` modifier (should be omitted)
T13 `var` used
T14 `==` comparison (should be `===`, or `== null` only for null/undefined check — `== undefined` is not the allowed form)
T15 `<IUser>entry.user` — angle-bracket type assertion, use `as`
T16 if without braces on multi-statement path / single-line if is OK only w/o else — `if (...) return undefined;` acceptable; NOT scored
T17 function expression `count = function ()` — use method/arrow; also `this` misuse
T18 non-null assertion `first!` without justification
T19 `settings` could be readonly / parameter property instead of boilerplate assignment
(scored items: T1–T5, T7–T15, T17, T18, T19 = 17; score = found / 17)
