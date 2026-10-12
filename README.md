# Product One-Pager Skill

An AI skill that helps product managers create or revise an **evidence-based product one-pager** — a concise executive brief that lets a VP of Product, CPO, or engineering leader understand a proposal and decide its next investment step in 2–3 minutes.

The skill challenges the idea, researches alternatives, defines a focused MVP and outcome metrics, and recommends whether to invest further. It is **not** a PRD generator, concept-note writer, or marketing copy tool.

---

## What It Produces

By default, the skill returns a structured text brief (~650–900 words) with eleven sections:

1. Executive Summary
2. Problem
3. Opportunity
4. Proposed Solution
5. Target User
6. Why This Will Win
7. Business Impact
8. Success Metrics
9. MVP & Scope
10. Key Risks & Assumptions
11. Recommendation *(Proceed / Proceed with Validation / Rework / Do Not Proceed)*

Ask for a PDF or document when you need a file. File generation depends on the tools available in the host AI assistant. Designed output is not currently implemented.

---

## Use

In a host that supports skills, add this repository using that host's documented skill workflow, then invoke it with:

```
Use $product-one-pager to assess my product idea and create an executive-ready one-pager.
```

Universal fallback: paste the contents of `SKILL.md` into an AI assistant as instructions, then provide the product and feature idea you want assessed.

The skill will ask for at most two inputs if they are not already in context:

1. **Product** — name and brief description
2. **Feature / idea** — what you want to evaluate

It then fills remaining gaps with explicit working assumptions and produces the brief. You can also ask it to revise an existing draft, challenge the premise, or adjust the recommendation. Research quality, source access, and file generation depend on the tools provided by the host AI assistant.

---

## File Structure

```
product-one-pager/
├── SKILL.md            # Skill instructions (workflow, evidence rules, output format)
├── agents/
│   └── openai.yaml     # Codex UI metadata and invocation policy
├── README.md           # This file
└── .gitignore
```

---

## Adaptation Note

Adapted from Prompt 01, *"Product One Pager Creation"*, in the AI Prompt Library for Product Managers (MISFIT collection). The eleven-section decision structure is preserved; evidence handling, context reuse, and validation discipline have been strengthened.
