# Answer key — inventory.py (12 seeded violations)
P1 `from os.path import join` — imports a function, not a module
P2 `import sys, json` — multiple imports on one line
P3 `GetItems` — function name should be lower_with_under
P4 2-space indentation in GetItems (must be 4)
P5 `open(...)` without `with` — resource not closed
P6 mutable default argument `items=[]`
P7 docstring not Google style / summary not capitalized+period; missing docstrings with Args/Returns on functions
P8 string concatenation with `+` in a loop (use join)
P9 `len(items) == 0` — use implicit false `if not items`
P10 bare `except:`
P11 logging with f-string instead of %-pattern args
P12 line longer than 80 chars in find_price
P13 `!= None` (should be `is not None`) and `== True` comparison
P14 top-level executable code with no `main()` / `if __name__ == '__main__':` guard
P15 no module docstring
(15 items; score = found / 15)
