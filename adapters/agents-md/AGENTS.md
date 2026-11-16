# Code style: Google Style Guides (via CodeTone)

When you write, edit or review code in this repository, follow Google's style
for that language. The rules live in `codetone/references/`
(copy that folder into the repo root, or change the paths below).

Before working on a file, open **only** the rule sheet for its language:

| Language | Files | Rule sheet |
|---|---|---|
| Python | `*.py, *.pyi` | `codetone/references/python.md` |
| C++ | `*.cc, *.cpp, *.cxx, *.h, *.hpp` | `codetone/references/cpp.md` |
| Java | `*.java` | `codetone/references/java.md` |
| JavaScript | `*.js, *.mjs, *.cjs` | `codetone/references/javascript.md` |
| TypeScript | `*.ts, *.tsx` | `codetone/references/typescript.md` |
| Angular | `*.component.ts, *.component.html, *.service.ts, *.directive.ts` | `codetone/references/angular.md` |
| Go | `*.go` | `codetone/references/go.md` |
| Rust | `*.rs` | `codetone/references/rust.md` |
| Shell (Bash) | `*.sh, *.bash` | `codetone/references/shell.md` |
| C# | `*.cs` | `codetone/references/csharp.md` |
| Objective-C | `*.m, *.mm` | `codetone/references/objective-c.md` |
| Swift | `*.swift` | `codetone/references/swift.md` |
| Kotlin | `*.kt, *.kts` | `codetone/references/kotlin.md` |
| Dart | `*.dart` | `codetone/references/dart.md` |
| HTML/CSS | `*.html, *.css, *.scss` | `codetone/references/html-css.md` |
| JSON | `*.json` | `codetone/references/json.md` |
| XML | `*.xml` | `codetone/references/xml.md` |
| Markdown | `*.md` | `codetone/references/markdown.md` |
| R | `*.R, *.r, *.Rmd` | `codetone/references/r.md` |
| Haskell | `*.hs` | `codetone/references/haskell.md` |
| Common Lisp | `*.lisp, *.asd, *.cl` | `codetone/references/common-lisp.md` |
| SystemVerilog/Verilog | `*.sv, *.svh, *.v` | `codetone/references/verilog.md` |
| Vim script | `*.vim` | `codetone/references/vimscript.md` |
| Tcl/Tk | `*.tcl` | `codetone/references/tcl.md` |

- Writing code: follow the sheet, then check your output against its
  "Review checklist".
- Reviewing code: list each violation with location, rule and fix, grouped as
  Must fix / Should fix / Nit.
- Precedence: the project's own formatter/linter config and the existing style of the file win over these rules; otherwise apply them.

<!-- Condensed from the Google Style Guides (https://github.com/google/styleguide), CC BY 3.0. Not affiliated with or endorsed by Google. -->
