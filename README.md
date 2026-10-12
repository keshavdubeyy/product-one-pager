# PM One-Pager

PM One-Pager is an Agent Skill for product managers who need a concise, evidence-aware investment brief for a product, feature, or capability. It separates the user problem from the proposed feature, challenges weak premises, defines a focused MVP and outcome metrics, and recommends whether to proceed, validate, rework, or stop.

The skill is intended for early product decisions. It is not a replacement for customer discovery, a full PRD, or marketing copy.

## Example invocation

```text
Use $product-one-pager to assess an AI-assisted handoff summary for our customer-support product.
```

The skill reuses information already in context and asks for only the missing product or feature input. See the [fictional example](examples/illustrative-one-pager.md) for a clearly labeled sample input and illustrative output.

## Output and host requirements

The default output is a structured text brief of approximately 650–900 words with eleven decision-oriented sections. A PDF or document can be requested when the host provides suitable file-generation tools. Research, source access, and file generation all depend on the host AI assistant's capabilities.

Designed or graphically composed output is not implemented.

## Installation

Review `skills/product-one-pager/SKILL.md` before installing it. Skills are instructions that can influence model behavior and tool use.

### Codex repository-local skill

OpenAI's documentation shows repository-scoped Codex skills under `.codex/skills/`. Copy the installable folder into the repository where you want Codex to discover it:

```bash
mkdir -p .codex/skills
cp -R /path/to/PM-One-Pager/skills/product-one-pager .codex/skills/product-one-pager
```

Then invoke `$product-one-pager` in that repository. See OpenAI's [systematic skill evaluation guide](https://developers.openai.com/blog/eval-skills) for the repo-local layout.

### OpenAI API skill upload

OpenAI's Skills guide accepts either a skill directory or a ZIP containing one top-level skill folder. Build and verify that ZIP locally:

```bash
python3 scripts/package_skill.py
python3 scripts/verify_package.py dist/product-one-pager.zip
```

Upload the resulting archive using the workflow in the official [OpenAI API Skills guide](https://developers.openai.com/api/docs/guides/tools-skills). API access, credentials, and charges are outside this repository.

### Universal fallback

If the host has no skill installation mechanism, paste the contents of `skills/product-one-pager/SKILL.md` into the AI assistant as instructions, then provide the product and feature idea. Tool-dependent research and file output may be unavailable.

## Compatibility status

| Surface | Status | What has been checked |
| --- | --- | --- |
| Installable skill folder and ZIP | Tested in this repository | Local scripts validate metadata and structure, build the ZIP, and compare its contents with the source folder. |
| Codex repository-local skills | Documentation-supported; not end-to-end tested here | The documented `.codex/skills/` layout is used in the installation instructions. |
| OpenAI API hosted skills | Documentation-supported; not end-to-end tested here | The ZIP follows the documented single-top-level-folder shape. No authenticated upload or model run is performed. |
| Other AI assistants | Untested fallback only | Pasting `SKILL.md` may work, but discovery, research, citations, and file tools vary by host. |

Structural checks do not prove model behavior. The scenarios in [tests/behavioral-cases.md](tests/behavioral-cases.md) are review cases for manual runs or a future model-evaluation harness.

## Repository layout

```text
skills/product-one-pager/   Installable skill and Codex UI metadata
examples/                   Fictional input and illustrative output
tests/                      Behavioral review cases
scripts/                    Dependency-free validation and packaging tools
.github/workflows/          Push and pull-request validation
```

## Validate and package

Python 3.9 or later is sufficient; the scripts use only the standard library.

```bash
python3 scripts/validate_skill.py
python3 scripts/package_skill.py
python3 scripts/verify_package.py dist/product-one-pager.zip
```

## Security, attribution, and licensing

Read [SECURITY.md](SECURITY.md) before reporting a vulnerability. Source attribution and third-party status are recorded in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

No distribution license has been selected for this repository. No license or rights to third-party material are granted by this repository.
