# JSON — Google Style (condensed)

Source: https://google.github.io/styleguide/jsoncguide.html

Applies to JSON API requests and responses (RPC and REST).

Tools: a JSON schema validator; `jq`/Prettier for pretty-printing (2-space
indent is conventional).

## General

- **No comments** in JSON.
- **Double quotes** for all property names and string values.
- Don't group data arbitrarily for convenience — nest only when the hierarchy is
  meaningful (e.g. `address: {…}`), otherwise keep it flat.

## Property names

- Meaningful names with defined semantics.
- **`camelCase`**, ASCII only; first character a letter, `_`, or `$`; following
  characters letters, digits, `_`, `$`.
- Avoid JavaScript reserved words as names.
- Map/dictionary keys (data, not schema) may use any Unicode.
- **Arrays → plural names** (`items`, `users`); everything else singular
  (`totalItems`, not `totalItem`s).
- Don't reuse a reserved name with a different meaning; when a new name clashes,
  pick a different name or version the API.

## Property values

- Values: booleans, numbers, strings, objects, arrays, or `null` — never
  functions or `undefined`.
- Consider **omitting** empty or `null` properties unless their presence carries
  meaning.
- **Enums as strings** (`"color": "WHITE"`), not numbers — keeps them stable if
  order changes.
- Dates: **RFC 3339** strings (`"2026-11-16T18:30:00.000Z"`).
- Durations: **ISO 8601** (`"P3Y6M4DT12H30M5S"`).
- Lat/long: **ISO 6709**, favoring `±DD.DDDD±DDD.DDDD` (`"+40.6894-074.0447"`).

## Reserved top-level structure (Google JSON API convention)

All reserved names are optional (0 or 1 times each); `apiVersion` should always
be present. A response contains `data` or `error` — if both appear, `error`
wins:

- `apiVersion` — version of the API.
- `context` — client-supplied value echoed back.
- `id` — server-assigned identifier for the response (for correlating with
  server logs).
- `method` — operation performed (`"people.get"`).
- `params` — input parameters for RPC-style requests.
- `data` — the result, may include: `kind`, `fields`, `etag`, `id`, `lang`,
  `updated` (RFC 3339), `deleted`, `items`.
  - Paging: `currentItemCount`, `itemsPerPage`, `startIndex`, `totalItems`,
    `pagingLinkTemplate`, `pageIndex`, `totalPages`.
  - Links: `self`/`selfLink`, `edit`/`editLink`, `next`/`nextLink`,
    `previous`/`previousLink`.
- `error` — `code` (HTTP status), `message`, `errors[]` each with `domain`,
  `reason`, `message`, `location`, `locationType`, `extendedHelp`, `sendReport`.

## Property ordering

- `kind` should be the **first** property in an object (helps parsers pick the
  right type).
- `items` should be the **last** property in `data` (so metadata is read before
  the list).

## Review checklist

- [ ] no comments; double quotes; camelCase ASCII names
- [ ] plural names only for arrays; enums as strings
- [ ] RFC 3339 dates, ISO 8601 durations
- [ ] `data` xor `error`; `kind` first, `items` last
