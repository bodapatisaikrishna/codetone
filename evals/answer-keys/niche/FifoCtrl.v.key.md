V1 file extension `.v` / file name `FifoCtrl` doesn't match module `fifo_ctrl` (should be fifo_ctrl.sv)
V2 no file header comment
V3 `define macro name not ALL_CAPS (`width`) / global define outside a global macro file
V4 4-space indentation (should be 2)
V5 non-ANSI (Verilog-1995) port declarations
V6 parameter `depth` should be UpperCamelCase (`Depth`)
V7 `reg` instead of `logic`
V8 reset named `reset_l` — should be `rst_n` (active-low `_n` suffix)
V9 enum values not kUpperCamelCase (IDLE/BUSY/DONE)
V10 `always @(posedge…)` instead of `always_ff`
V11 blocking assignments `=` in sequential logic
V12 missing begin/end on multi-line if/else chain
V13 combinational block with sensitivity list / `always @(...)` instead of `always_comb`, and non-blocking `<=` in combinational logic
V14 `#1` delay in synthesizable code
V15 implicit nets / undeclared signals (`busy_flag`, `q`)
V16 generate block not named with `gen_` prefix
V17 positional port connections in instance (use named ports)
V18 case statement without `default` / not `unique case`
(18)
