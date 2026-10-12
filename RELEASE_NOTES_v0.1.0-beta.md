# PM One-Pager v0.1.0-beta

Prepared from tested main commit `8e845afa0e37adea9d6eb87a0ccf7005cafa71f2`. This is a draft release note; the release has not been published.

## What is included

- Designed 16:9 product brief output by default; portrait 9:16 on request.
- Editable HTML/CSS fallback with print styling and static PNG/PDF exports where the host can create and verify them.
- All eleven decision sections, evidence labels, compact citations, supporting notes, and a prominent recommendation area.
- Bundled fallback design reference with attribution, plus the installable skill's `NOTICE.md`.

## Tested installation routes

- Claude Code plugin: hosted installation from `main` tested with isolated configuration and cache directories. Claude model invocation is untested.
- Skills CLI: hosted/default-branch installation tested into an isolated Codex project.
- ZIP/manual route: package creation and exact-content verification passed.

## Live Codex scenario

One fresh fictional BerthWise / Turnaround Readiness scenario was run through the installed skill using an authenticated Codex session. It reused supplied product context, included all eleven sections, labeled unsupported assumptions, and gave the justified recommendation **Proceed with Validation**. The final brief was one readable 16:9 HTML visual with editable text, plus a PNG preview and one-page PDF export. The bundled RelayDesk example was not used.

The run first attempted a Canva native design. Canva returned six slides, which failed the one-page requirement. The model rejected that result, explicitly switched to the HTML fallback, rendered the brief, and inspected the final output. This Canva failure/recovery is recorded as a host-capability limitation, not as a successful native one-page export.

## Limitations

Research, native canvases, rendering, file generation, exports, and model behavior depend on host capabilities and credentials. Claude model invocation remains untested. Structural validation and artifact checks do not prove behavior on every agent. No distribution license has been selected; attribution and notices grant no rights to third-party material.
