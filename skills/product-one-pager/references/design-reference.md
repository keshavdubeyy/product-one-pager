# Product Brief Design Reference

Use this reference only when the user has not supplied design instructions and the accessible project has no usable design system. Project tokens and templates take priority. Adapt these web-derived cues to presentation-scale viewing; do not copy small UI typography directly onto a slide.

## Source and status

This fallback is adapted from the [Refero Styles “Ui” reference](https://styles.refero.design/style/0fd67ec5-7e9c-4ca9-b368-5d9c7388477a), which reconstructs visual patterns associated with `ui.shadcn.com`. It is an independent reference, not an official shadcn design-system specification. Do not imply endorsement or official status.

## Typography

- Prefer Geist. Fall back to Inter, Arial, or a clean installed sans-serif.
- Landscape title: 34–44 pt equivalent. Portrait title: 38–48 pt equivalent.
- Summary: 18–22 pt equivalent. Section labels: 13–16 pt equivalent, semibold. Body: 15–18 pt equivalent.
- Use tight display tracking and normal body tracking. Keep line height near 1.15 for titles and 1.3–1.45 for body copy.
- Shorten copy before reducing type. Never use web UI sizes such as 12–14 px for slide body text.

## Color

- Canvas: `#F5F5F5`
- Paper: `#FFFFFF`
- Primary text: `#0A0A0A`
- Secondary text: `#525252`
- Muted text: `#737373`
- Hairline border: `#E5E5E5`
- Subtle surface: `#FAFAFA`
- Strong neutral emphasis: `#171717`
- Destructive/error only: `#E7000B`

Keep the brief achromatic by default. Do not use decorative red. Meet WCAG AA contrast for normal text whenever the output format supports color control.

## Spacing and surfaces

- Base spacing unit: 8 px equivalent. Prefer increments of 8, with 4 only for fine alignment.
- Outer safe area: about 5–6% of the shorter slide dimension.
- Use 24–40 px equivalent between major groups and 8–16 px within a group.
- Use fine 1 px gray rules to establish grouping. Use restrained 16–24 px corner radii only for major containers.
- Keep shadows minimal or omit them. Hierarchy should come from type, spacing, tonal surfaces, and rules.

## Hierarchy and layout

- Use one title and executive summary band at the top.
- Group related sections rather than drawing eleven identical cards:
  - **Problem framing:** Problem, Opportunity, Proposed Solution.
  - **Audience and advantage:** Target User, Why This Will Win, Business Impact.
  - **Test and decide:** Success Metrics, MVP & Scope, Key Risks & Assumptions.
  - **Decision:** Recommendation in the most prominent closing area.
- Keep every numbered section label visible, including `1. Executive Summary` in the top band.
- Use a balanced three-column or asymmetric grid in landscape. In portrait, reflow into a vertical sequence or two-column middle region; do not merely rotate or uniformly scale the landscape layout.
- Aim for 300–400 visible words, reducing further when needed for legibility. Preserve material uncertainty, evidence labels, and the decision-changing condition.

## Citations and supporting detail

- Use compact linked citation markers such as `[1]` next to consequential external claims.
- Put full source titles, URLs, access dates, calculations, and supporting analysis in editable notes or a companion Markdown file when they do not fit legibly.
- Never manufacture evidence to fill the visual design.

## Output integrity

- Keep text, shapes, tables, and links editable when the chosen host format supports them.
- A raster preview is static even when it depicts an editable source.
- Confirm the exported files actually exist before naming or linking them.
- Check clipping, overlap, contrast, font substitution, link targets, and orientation before delivery.
