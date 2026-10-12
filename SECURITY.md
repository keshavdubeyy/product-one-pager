# Security Policy

## Scope

Security reports may cover the skill instructions, packaging and validation scripts, or GitHub Actions workflow in this repository. Examples include unsafe archive handling, command execution that exceeds documented behavior, or instructions that could cause unintended disclosure of user data.

## Reporting

This project does not currently publish a dedicated security email address or response SLA.

If GitHub offers a private vulnerability-reporting option in this repository's **Security** tab, use it. If no private option is available, do not post secrets, personal data, exploit details, or working payloads in a public issue. Instead, open a minimal public issue asking the maintainer to establish a private reporting channel.

Include the affected commit or file, impact, reproduction conditions, and a suggested mitigation when available. Remove credentials and sensitive data from all reports.

## Supported versions

The current supported version is **v0.1.0-beta** (tag `v0.1.0-beta`). This is a pre-release. Security fixes, when accepted, will target the current default branch on a best-effort basis.

## Operational note

Skills are instructions consumed by an AI host. Review this skill before installing it, limit the host's permissions, and require explicit approval for sensitive or high-impact actions. The repository's structural checks do not establish that every model or host will behave safely.
