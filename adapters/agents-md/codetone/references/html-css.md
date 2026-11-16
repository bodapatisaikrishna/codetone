# HTML / CSS — Google Style (condensed)

Source: https://google.github.io/styleguide/htmlcssguide.html

Tools: W3C HTML validator, W3C CSS validator (named by the guide). Optional
third-party: Stylelint, Prettier (2-space indent).

## General (both)

- Use `https:` for embedded resources (images, scripts, styles) whenever
  available.
- Indent **2 spaces**, no tabs; don't mix.
- **Lowercase only**: element names, attributes, attribute values (except
  text/`CDATA`), CSS selectors, properties, values (except strings), hex colors.
- No trailing whitespace.
- UTF-8 without BOM; declare `<meta charset="utf-8">` in HTML; don't specify
  encoding in CSS.
- Comment as needed to explain what code covers and why; TODOs:
  `TODO(bug-or-link): explanation`.

## HTML style

- Use `<!doctype html>` (no-quirks mode).
- Use valid HTML unless file-size performance goals make it impossible (check
  with the W3C validator).
- **Semantics**: use elements for what they mean — `<a>` for links, `<button>`
  for actions, headings for headings — never a `<div>` with a click handler for
  navigation.
- Multimedia fallbacks: meaningful `alt` text for images; `alt=""` for purely
  decorative ones; captions/transcripts for audio/video.
- **Separation of concerns**: structure in HTML, presentation in CSS, behavior
  in JS. No inline `style` attributes, minimal inline scripts, link as few
  stylesheets/scripts as possible.
- Don't use entity references (`&eacute;`) except for characters with special
  meaning in HTML (`<`, `&`) and invisible characters (`&nbsp;`).
- Consider omitting optional tags (`<html>`, `<head>`, `<body>`, closing `</p>`,
  `</li>`) — optional rule; if you do, omit all of them, not a selection.
- Omit `type` on `<link rel="stylesheet">` and `<script>` (except non-JS script
  types like modules/JSON).
- Avoid unnecessary `id`s; prefer `class` for styling and `data-*` for script
  hooks. When needed, `id`s must contain a hyphen (so they don't clash with JS
  globals).

## HTML formatting

- Put every block, list, or table element on a new line and indent its children.
- Long lines may be wrapped; indent continuation lines consistently (e.g. 4
  spaces or aligned attributes).
- Use **double quotes** for attribute values.

## CSS style

- Write valid CSS; avoid hacks — try other approaches first; user-agent
  detection is a last resort.
- **Class names**: meaningful/generic (`.video`, `.login`), not presentational
  (`.yee-1901`, `.button-green`); as short as possible but not cryptic.
- Lowercase, words separated by **hyphens** (`.video-id`, not `.videoId` /
  `.video_id`).
- Prefix classes with a short namespace in large projects (`.adw-help`).
- Avoid qualifying class names with type selectors (`.error`, not `ul.error`)
  unless needed.
- Avoid **ID selectors** for styling (high specificity; hurts reuse).
- Use shorthand properties where possible (`padding: 0 1em 2em;`).
- Omit units after `0` (`margin: 0;`) unless required (e.g. `flex: 0px`).
- Always include leading `0` in decimals (`0.8em`, not `.8em`).
- 3-character hex where possible (`#ebc` not `#eebbcc`).
- Avoid `!important`.

## CSS formatting

- Sort declarations consistently within a project (optional; alphabetical if no
  tooling enforces an order; ignore vendor prefixes when sorting, keep prefixed
  variants sorted).
- Indent all block contents (rules inside `@media`, declarations inside rules).
- Every declaration ends with `;` (including the last).
- One space after the property colon (`font-weight: bold;`), none before.
- One space between the last selector and `{`; `{` on the same line.
- Each selector and each declaration on its own line.
- Blank line between rules.
- **Single quotes** for attribute selectors and property values (`url()` without
  quotes); `@charset` is the exception (double quotes).
- Group sections with section comments (`/* Header */`) followed by a blank
  line.

## Review checklist

- [ ] `<!doctype html>`, `<meta charset="utf-8">`, valid markup
- [ ] semantic elements, `alt` text, no inline styles
- [ ] hyphenated meaningful class names; no ID selectors; no `!important`
- [ ] consistent declaration order; `0` without units; `0.5` leading zero
- [ ] 2-space indent, lowercase everything
