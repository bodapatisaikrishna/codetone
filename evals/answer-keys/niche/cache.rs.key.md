R1 glob import `use std::collections::*`
R2 Rc/RefCell shared ownership (avoid Rc/Arc)
R3 tuple struct with multiple fields `Entry(String, u64, bool)` — prefer named fields
R4 public enum without #[non_exhaustive]
R5 manual `impl Clone` that should be #[derive(Clone)] (and Debug etc.)
R6 `get_items` getter with `get_` prefix
R7 `len()` without `is_empty()`
R8 `&String` parameter (use &str)
R9 `&Vec<String>` parameter (use &[String])
R10 `bool` parameter `persist` — use an enum
R11 string concatenation with `+` instead of format!
R12 check-then-unwrap (`is_some()` then `unwrap()`) — use pattern matching / and `unwrap` without expect
R13 `unsafe` without `// SAFETY:` comment (and avoidable)
R14 `catch_unwind` used
R15 missing doc comments on public items
(15)
