# SystemVerilog / Verilog — Google Style (condensed)

Source: https://google.github.io/styleguide/verilogguide.html

Tools: the Verible style linter (`verible-verilog-lint`, named by the guide);
`verible-verilog-format` and simulator/synthesis lint are common extras.

## Basics

- Target **SystemVerilog-2017** for both RTL and testbench code. Justify every
  style exception with a comment.

## Files

- Extensions `.sv` (and `.svh` for include files).
- One design element per file; the file name starts with the element name
  (`my_fifo.sv` contains `module my_fifo`; variants like `my_fifo.gate.sv` are
  OK). Special names: `[design]_top.sv`, `[design]_pkg.sv`.
- Each file: header comment → declaration → implementation.
- Generated code must ship with the inputs/scripts that regenerate it.

## Formatting

- ASCII only, UNIX line endings, newline at end of file.
- **100-column** limit. **2-space** indent. **No tabs.** No trailing whitespace;
  delete redundant semicolons.
- `begin`/`end` required unless the whole statement fits on one line.
- Preprocessor directives left-aligned, not indented.
- Spaces around keywords and all binary operators; one space after commas.
- Code block labels: space on both sides of `:` (`end : gen_loop`); statement
  labels: no space before `:`.
- Spaces after module name and between parameter/port lists in headers and
  instances; **no** space between a function/task/macro name and `(`.
- Align related items for readability (recommended); right-align line
  continuations.
- Parentheses: whenever precedence could be unclear; required around reductions
  preceded by another operator and around nested ternaries.
- Comments: `//` style strongly recommended; `/** … **/` is reserved for code
  generators.

## Naming

| Kind                                                               | Style                                     |
| ------------------------------------------------------------------ | ----------------------------------------- |
| default (signals, ports, modules, instances, functions, variables) | `lower_snake_case`                        |
| `` `define `` macros                                               | `ALL_CAPS` (local macros start with `_`)  |
| tunable parameters, constants                                      | `UpperCamelCase`                          |
| type parameters, struct/union/enum types                           | `lower_snake_case_t` (enums may use `_e`) |
| enum values                                                        | `kUpperCamelCase`                         |
| constraints                                                        | `lower_snake_case_c`                      |
| interfaces                                                         | `lower_snake_case_if`                     |

- Name signals **positively** (`enable`, not `disable_n` logic inversions).
- Same signal keeps the same name throughout the hierarchy.
- Clocks/resets: `clk`, `rst`, `arst`; with multiple clocks, prefix signals by
  clock domain.
- Suffixes: `_n` active-low; `_p`/`_n` differential pair; `_d` delayed one cycle
  (`_d2`, …); `_next` register next-state; `_le` load enable; `foo_valid`
  qualifies `foo_*`. Order suffixes inner-semantic → outer-temporal (`rst_n_d`).
- Avoid names ending in `_<number>` and SystemVerilog/VHDL keywords.

## Preprocessor

- Global `` `define ``s only in dedicated global macro files; avoid `` `ifdef ``
  except as prescribed; no include guards; `` `include `` only into packages or
  for snippets; fail compilation with `` `DIE() ``.
- No synthesis pragmas that cause sim/synth mismatches.

## Modules and packages

- Verilog-2001 ANSI port declarations. Top module `[design]_top`; unit tests end
  in `_test`.
- Instance names start with the module name (`my_fifo_nibble`).
- **Named port and named parameter connections** for all instances. No recursive
  instantiation.
- Name every generate block with a `gen_` prefix.
- No cyclic package dependencies.

## Signals, types, constants

- Declare all signals before use, with a data type — no implicit nets (tip, not
  from the guide: `` `default_nettype none `` enforces this).
- Use `logic` for synthesis (`wire` only when needed). No default port values.
- Design-wide constants as package parameters; local ones as `localparam`; avoid
  magic numbers.
- Packed vectors little-endian (`[7:0]`); unpacked arrays big-endian
  (`[0:N-1]`).
- Typedef all structs/unions; union members prefixed `as_`.

## Logic

- Synthesizable RTL: encapsulate with modules; no tasks; functions only for
  short combinational logic, and always `automatic`.
- Sequential: `always_ff` with **non-blocking** (`<=`) assignments; avoid
  latches; standard reset format; no `#delay` in synthesizable code.
- Combinational: `always_comb` or `assign` with **blocking** (`=`) assignments;
  no sensitivity lists.
- FSMs: enum state type; two processes (combinational next-state + clocked state
  register).
- Don't silently squash `X` — propagate or assert. No don't-care assignments in
  synthesizable code.
- Use `unique case` with a `default`; no case-modifying pragmas.
- Use signed constructs explicitly; mind expression widths; logical ops (`&&`)
  for single-bit logic.
- Don't use `alias`.

## Design conventions

- Consistent `timescale` per project. Ready/Valid flow control (Req/Ack as
  alternative); don't mix flow-control and data in one struct.
- Use proven CDC synchronizer libraries; isolate each clock domain in its own
  submodule. Prefer registered module outputs.

## Verification

- Express assumptions and invariants as runtime assertions in the RTL (covering
  every port), using the standard assertion macros; no side effects (e.g.
  `randomize`) inside assertions.
- No `program` blocks; wrap simulator-specific code in preprocessor guards;
  isolate `wait fork`/`disable fork` inside a `fork … join`; no `[*]` wildcard
  associative arrays; `bind` is the preferred way to attach assertion monitors.

## Review checklist

- [ ] `.sv`, file = module name, header comment
- [ ] 2-space, 100 col, `begin/end`, no tabs
- [ ] `lower_snake_case`, `kEnumValue`, `_t` types, `_n`/`_d` suffixes
- [ ] named port/param connections; `gen_` generate labels
- [ ] `always_ff` + `<=`, `always_comb` + `=`, `unique case` with `default`
