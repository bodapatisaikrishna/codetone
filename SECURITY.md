# Security policy

## What this project is

CodeTone is Markdown rule sheets plus a small build script
(`scripts/build_adapters.py`). It does not run a service or handle user data.

## What counts as a security issue

- The build script can be made to write outside the repository, run
  attacker-controlled code, or leak secrets.
- A rule sheet or generated file contains text that would make an AI agent take
  a harmful action (for example hidden instructions to exfiltrate data or run
  commands).
- A dependency or GitHub Actions version used by the project has a known
  vulnerability that affects it.

A rule that is merely wrong or outdated is not a security issue. Open a normal
issue for it.

## Reporting

Please report privately and do not open a public issue.

Use GitHub's private reporting: go to the repository's **Security** tab and
choose **Report a vulnerability**.

Include what you found, how to reproduce it, and the version or commit. You
should get a reply within 7 days. This is a one-person volunteer project, so fix
times are best effort.

## Supported versions

Only the latest release and the `main` branch are supported.
