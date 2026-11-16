# Answer key — backup.sh (15 seeded violations)
S1 `#!/bin/sh` — must be `#!/bin/bash`
S2 no file header comment
S3 alias used in a script
S4 unquoted / unbraced variables (`$1`, `$src`, `$dest`, `$name`) — should be "${var}"
S5 `function DoBackup` — function names lower_with_under
S6 4-space indentation (should be 2)
S7 backticks instead of `$( )`
S8 `[ … ]` instead of `[[ … ]]`, and testing empty string with `== ""` instead of `-z`
S9 error message to STDOUT instead of STDERR
S10 `cd $dest` return value not checked
S11 `expr` used for arithmetic
S12 `let` used for arithmetic
S13 `eval` used
S14 `$*` instead of `"$@"`
S15 no `local` for function variables
S16 no `main` function / code between functions
S17 wildcard without explicit path / rm -rf unquoted path risk
S18 no function header comments
(18 items; score = found / 18)
