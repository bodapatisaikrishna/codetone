# Write tasks (one per language)

## python
Write `top_students.py`: a module + CLI that reads a CSV file of students (columns: name, marks),
and prints the top N students by marks (N from a `--top` flag, default 3). Handle a missing file
and bad rows (skip them with a warning). Include a function `top_students(rows, n)` that is
importable and testable.

## typescript
Write `rateLimiter.ts`: a token-bucket rate limiter class with a configurable capacity and refill
rate per second, a method that returns whether a request identified by a client key is allowed,
and a method to reset a client. Export it for use by other modules.

## go
Write `fetcher.go` in package `fetch`: a function that GETs a URL with a `context.Context`,
retries up to a configurable number of times with exponential backoff on 5xx or network errors,
and returns the body bytes or a wrapped error. Include a table-driven test file `fetcher_test.go`
using `net/http/httptest`.

## shell
Write `rotate_logs.sh`: a Bash script that takes a log directory and a number of days, gzips
`.log` files older than that many days, deletes `.gz` files older than 30 days, prints a summary,
and exits non-zero on bad arguments.
