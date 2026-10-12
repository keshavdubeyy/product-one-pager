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

### Option 1: Claude Code plugin

Register this repository as a Claude Code marketplace, then install the plugin:

```bash
claude plugin marketplace add keshavdubeyy/product-one-pager
claude plugin install pm-one-pager@keshav-pm-skills
```

Invoke the namespaced plugin skill inside Claude Code:

```text
/pm-one-pager:product-one-pager Assess an AI-assisted handoff summary for our support product.
```

These are [Claude Code marketplace](https://code.claude.com/docs/en/plugin-marketplaces) commands. They are not installation instructions for the Claude website. The plugin manifest follows Claude Code's [manifest](https://code.claude.com/docs/en/plugins/manifest-reference) and [skills](https://code.claude.com/docs/en/skills) documentation and points to the repository's existing `skills/` directory.

### Option 2: Supported agents through the Skills CLI

The [Vercel Skills CLI](https://github.com/vercel-labs/skills) discovers the repository's `skills/product-one-pager/` folder:

```bash
npx skills add keshavdubeyy/product-one-pager --skill product-one-pager
```

The CLI prompts for an installed target agent unless one is selected with `--agent`. Its published [supported-agent list](https://github.com/vercel-labs/skills#supported-agents) is the source of truth for installation targets; this repository has not tested every listed host.

Invocation depends on the selected host:

- **Claude Code direct skill:** `/product-one-pager Assess my feature idea.`
- **Codex:** `Use $product-one-pager to assess my feature idea.`

Installing through the Skills CLI gives Claude Code a direct skill, not the namespaced plugin command from Option 1.

### Option 3: ZIP or manual installation

OpenAI's Skills guide accepts either a skill directory or a ZIP containing one top-level skill folder. Build and verify that ZIP locally:

```bash
python3 scripts/package_skill.py
python3 scripts/verify_package.py dist/product-one-pager.zip
```

Upload the resulting archive using the workflow in the official [OpenAI API Skills guide](https://developers.openai.com/api/docs/guides/tools-skills). API access, credentials, and charges are outside this repository.

For a host that discovers skills from a filesystem directory, copy only `skills/product-one-pager/` into that host's documented skill location. In an OpenAI API prompt, invoke it explicitly with wording such as `Use the product-one-pager skill to assess this feature idea.`

Universal fallback: paste the contents of `skills/product-one-pager/SKILL.md` into an AI assistant as instructions, then say `Using these instructions, assess this product and feature idea:` and provide the inputs. Tool-dependent research and file output may be unavailable.

## Compatibility status

| Surface | Status | What has been checked |
| --- | --- | --- |
| Claude Code plugin | Installation tested; model invocation untested | Claude Code 2.1.89 validated the manifests with optional-field warnings, then added the marketplace, installed the plugin, and listed it as enabled using isolated temporary config and cache directories. |
| Skills CLI | Installation tested for Codex target; model invocation untested | The exact GitHub source command and the current local layout each discovered one skill and installed it into isolated project directories. Other target agents were not tested. |
| Installable skill folder and ZIP | Tested in this repository | Local scripts validate metadata and structure, build the ZIP, and compare its contents with the source folder. |
| OpenAI API hosted skills | Documentation-supported; not end-to-end tested here | The ZIP follows the documented single-top-level-folder shape. No authenticated upload or model run is performed. |
| Other AI assistants | Untested fallback only | Pasting `SKILL.md` may work, but discovery, research, citations, and file tools vary by host. |

Structural checks do not prove model behavior. The scenarios in [tests/behavioral-cases.md](tests/behavioral-cases.md) are review cases for manual runs or a future model-evaluation harness.

## Repository layout

```text
.claude-plugin/            Claude Code plugin and marketplace manifests
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
claude plugin validate .
```

Claude Code 2.1.89 reports optional warnings because the plugin has no release version and the marketplace omits its optional description for compatibility with this CLI version. No release version has been selected.

## Security, attribution, and licensing

Read [SECURITY.md](SECURITY.md) before reporting a vulnerability. Source attribution and third-party status are recorded in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

No distribution license has been selected for this repository. No license or rights to third-party material are granted by this repository.
