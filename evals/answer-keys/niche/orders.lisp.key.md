L1 file header comment uses single `;` (should be `;;;`) / weak file description
L2 global special variable without earmuffs (`counter` → `*counter*`)
L3 constant without plus signs (`max-size` → `+max-size+`)
L4 new CLOS use (`defclass`) — disallowed in new code
L5 `computeTotal` — camelCase; should be `compute-total`
L6 `&optional` mixed with `&key`
L7 `&aux` used
L8 closing parens on their own lines
L9 missing docstrings
L10 predicate `is-valid-order` should be `valid-order-p`
L11 `if` with one branch + `progn` → use `when`
L12 side effect (incf global) in a predicate / mostly-functional style
L13 runtime `eval`
L14 runtime `intern`
L15 `'computeTotal` should be `#'compute-total`
L16 `eq` for numbers (use `eql` / `=`)
(16)
