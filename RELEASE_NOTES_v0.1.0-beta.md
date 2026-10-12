# PM One-Pager v0.1.0-beta

Initial public beta. The successful live Codex test used commit `8e845afa0e37adea9d6eb87a0ccf7005cafa71f2`. The release-preparation commit is `83b0ad2` (`83b0ad2 Prepare v0.1.0-beta release notes`), which adds the native page-count safeguard and bundled notices.

## What is included

- Designed 16:9 product brief output by default; portrait 9:16 on request.
- Editable HTML/CSS fallback with print styling and static PNG/PDF exports where the host can create and verify them.
- All eleven decision sections, evidence labels, compact citations, supporting notes, and a prominent recommendation area.
- Bundled fallback design reference with attribution, plus the installable skill's `NOTICE.md`.

## Tested installation routes

- Claude Code plugin: hosted installation from `main` tested with isolated configuration and cache directories. Claude model invocation is untested.
- Skills CLI: hosted/default-branch installation tested into an isolated Codex project.
- ZIP/manual route: package creation and exact-content verification passed.

Installable ZIP checksum (built from final intended release commit `7d28690`; the packaged skill content was introduced in `83b0ad2`):

`SHA-256  f311a76fd03e7ea389e9c1c2b02800a1d3f6bfad43b8884ca15678836f969ac1  dist/product-one-pager.zip`

## Live Codex scenario

One fresh fictional BerthWise / Turnaround Readiness scenario was run through the installed skill using an authenticated Codex session. It reused supplied product context, included all eleven sections, labeled unsupported assumptions, and gave the justified recommendation **Proceed with Validation**. The final brief was one readable 16:9 HTML visual with editable text, plus a PNG preview and one-page PDF export. The bundled RelayDesk example was not used.

The run first attempted a Canva native design. Canva returned six slides, which failed the one-page requirement. The model rejected that result, explicitly switched to the HTML fallback, rendered the brief, and inspected the final output. This Canva failure/recovery is recorded as a host-capability limitation, not as a successful native one-page export.

## Limitations

Research, native canvases, rendering, file generation, exports, and model behavior depend on host capabilities and credentials. Claude model invocation remains untested. Structural validation and artifact checks do not prove behavior on every agent.

This repository is released under the MIT License for original contributions. The skill content adapted from the MISFIT collection and the design reference adapted from Refero Styles are included under attribution only; redistribution rights for that material have not been independently confirmed. See THIRD_PARTY_NOTICES.md.
