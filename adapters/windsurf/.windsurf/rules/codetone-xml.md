---
trigger: glob
globs: **/*.xml
---

Precedence: the project's own formatter/linter config and the existing style of the file win over these rules; otherwise apply them.

# XML Document Format — Google Style (condensed)

Source: https://google.github.io/styleguide/xmlguide.html

Scope: designing new XML **document formats** (vocabularies), not styling
arbitrary files.

Tools (not named by the guide): RELAX NG validators (`jing`),
`xmllint --format`.

## Design first

- Reuse an existing XML format whenever possible (Atom, XHTML, DocBook, SVG…);
  extend sensibly using the existing format's own style rather than inventing
  your own.

## Schemas

- Express formats with a schema — **RELAX NG compact syntax** preferred; may add
  Schematron/regex constraints for complex values; DTD / W3C XML Schema only for
  compatibility.

## Namespaces

- Element names **must** be in a namespace (except when extending an
  un-namespaced format); attributes usually not namespaced.
- Namespace names are HTTP URIs; don't change a namespace unless semantics
  change.
- Short prefixes of lowercase ASCII letters — never single-letter; declare
  namespaces on the root element; keep prefix mappings constant; use well-known
  prefixes (`html:`, `dc:`, `xs:`).

## Names

- **lowerCamelCase** for all element/attribute names and enumerated values;
  ASCII letters and digits only. Acronyms are camel-cased as words
  (`informationUri`, not `informationURI`); no ad hoc abbreviations.
- Names should be ≤ 25 characters (ignore the limit if staying under it makes a
  name obscure); well-known standard abbreviations are allowed.

## Elements and attributes

- An element contains nothing, text only, or child elements only — **no mixed
  content** in data formats.
- Don't add wrapper elements that only hold repeating children.
- Don't depend on attribute order; ≤ ~10 attributes per element.
- Attributes must not hold values with significant line breaks.
- Use **elements** when data repeats, has substructure, needs order, is
  user-visible text, or might grow; use **attributes** for small, simple,
  unordered metadata (IDs, units, types).

## Values

- Numbers: 32/64-bit signed integers or 64-bit IEEE doubles.
- Avoid booleans — prefer enumerations (if used: `true`/`false`).
- Dates: RFC 3339 (a subset of ISO 8601), preferably UTC.
- Don't embed other syntaxes in values (dates, URIs, XPath, and
  whitespace-separated token lists are OK); define whitespace-stripping rules.
- Key-value pairs: an empty element **named after the key** with a `value`
  attribute (optional SI `unit`): `<timeout value="30" unit="s"/>`. Only for
  very large/unbounded key sets use a generic element with `key`/`value`
  attributes.
- Binary data: Base64 (line breaks optional), never raw.
- Don't create new processing instructions (except purely local conventions);
  existing standard ones (e.g. `xml-stylesheet`) may be used.

## Document instances

- Encoding **UTF-8**.
- No redundant whitespace inside tags; one space before each attribute.
- Empty elements as `<x/>` or `<x></x>`.
- If pretty-printing, use **2-space** indentation; never wrap elements that
  contain character content.
- Either quote style allowed (formats must accept both).
- Comments never carry real data (TODOs in hand-written XML are OK; none in
  publicly transmitted documents); put them only in the prolog or in elements
  with child elements, never in character content; whitespace after `<!--` and
  before `-->`.
- CDATA allowed; avoid entity references beyond the five XML standard ones.

## Review checklist

- [ ] reused an existing format if possible; RELAX NG schema
- [ ] namespaced lowerCamelCase element names ≤ 25 chars
- [ ] no mixed content; elements vs attributes chosen by the rules above
- [ ] UTF-8, 2-space indent, RFC 3339 dates, Base64 binaries

<!-- Condensed from the Google Style Guides (https://github.com/google/styleguide), CC BY 3.0. Not affiliated with or endorsed by Google. -->
