# PM One-Pager

## Your next product idea. A clearer decision.

An AI skill that turns your product or feature idea into a concise investment brief—covering the problem, alternatives, MVP, metrics, risks, and a recommended next step.

## What it helps you do

- Research relevant alternatives.
- Challenge assumptions and weak premises.
- Recommend whether to proceed, validate, rework, or stop.

## Quick installation

Review [`SKILL.md`](skills/product-one-pager/SKILL.md) before installing it. Skills are instructions that can influence model behavior and tool use.

### Claude Code plugin

```bash
claude plugin marketplace add keshavdubeyy/product-one-pager
claude plugin install pm-one-pager@keshav-pm-skills
```

These commands were tested against the default branch with Claude Code 2.1.89. They install into Claude Code, not the Claude website. See the official [Claude Code marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces).

### Supported agents through the Skills CLI

```bash
npx skills add keshavdubeyy/product-one-pager --skill product-one-pager
```

The default branch was tested with the Skills CLI using an isolated Codex target. The CLI prompts for an installed target agent unless one is selected with `--agent`; consult its current [supported-agent list](https://github.com/vercel-labs/skills#supported-agents).

## Try it

After the Claude Code plugin installation:

```text
/pm-one-pager:product-one-pager Assess an AI-assisted handoff summary for our customer-support product.
```

After installing through the Skills CLI for Codex:

```text
Use $product-one-pager to assess an AI-assisted handoff summary for our customer-support product.
```

The skill reuses product and feature details already supplied in the conversation and asks only for any missing product or feature details.

## Example output

See the [fictional example input and illustrative output](examples/illustrative-one-pager.md). It demonstrates the structured text format; it is not a designed PDF preview.

> **Limitations:** Outputs need review. Research and file generation depend on your AI tool. The current default output is structured text.

<details>
<summary><strong>Compatibility and testing status</strong></summary>

| Surface                          | Status                                                                  | What has been checked                                                                                                                                                                                                                                                                                                 |
| -------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Code plugin               | Default-branch installation tested; model invocation unavailable        | Claude Code 2.1.89 added the GitHub marketplace, installed the plugin from `main`, and listed it as enabled using isolated temporary configuration and cache directories. The installed skill matched the repository source. No authenticated Claude session or environment credential was available for a model run. |
| Skills CLI                       | Default-branch installation tested for Codex; model invocation untested | The CLI discovered one skill from the GitHub repository and installed it into an isolated Codex project. Other target agents were not tested.                                                                                                                                                                         |
| Installable skill folder and ZIP | Structurally tested                                                     | Local scripts validate metadata, eleven required sections, references, and package contents.                                                                                                                                                                                                                          |
| OpenAI API hosted skills         | Documentation-supported; not end-to-end tested                          | The ZIP follows the documented single-top-level-folder shape. No authenticated upload or model run has been performed.                                                                                                                                                                                                |
| Other AI assistants              | Untested fallback                                                       | Pasting `SKILL.md` may work, but skill discovery, research, citations, and file tools vary by host.                                                                                                                                                                                                                   |

Structural validation does not prove model behavior. The scenarios in [tests/behavioral-cases.md](tests/behavioral-cases.md) are review cases for manual runs or a future model-evaluation harness.

The default result is an approximately 650–900-word brief with eleven decision-oriented sections. A PDF or document can be requested when the host has suitable file-generation tools. Designed or graphically composed output is not implemented.

</details>

<details>
<summary><strong>ZIP/manual installation</strong></summary>

Build and verify a ZIP containing the single installable skill folder:

```bash
python3 scripts/package_skill.py
python3 scripts/verify_package.py dist/product-one-pager.zip
```

The archive can be used with the official [OpenAI API Skills guide](https://developers.openai.com/api/docs/guides/tools-skills). API access, credentials, and charges are outside this repository.

For a host that discovers skills from the filesystem, copy only `skills/product-one-pager/` into that host's documented skill location. A universal fallback is to paste the contents of [`SKILL.md`](skills/product-one-pager/SKILL.md) into an AI assistant as instructions, then provide the product and feature idea. Research and file output remain dependent on that host's tools.

</details>

<details>
<summary><strong>Development and validation commands</strong></summary>

Python 3.9 or later is sufficient; the scripts use only the standard library.

```bash
python3 scripts/validate_skill.py
python3 scripts/package_skill.py
python3 scripts/verify_package.py dist/product-one-pager.zip
claude plugin validate .
```

Claude Code 2.1.89 reports an optional warning because the marketplace omits its optional description for compatibility with this CLI version. Current release: **v0.1.0-beta**.

Repository layout:

```text
.claude-plugin/             Claude Code plugin and marketplace manifests
skills/product-one-pager/   Installable skill and Codex UI metadata
examples/                   Fictional input and illustrative output
tests/                      Behavioral review cases
scripts/                    Dependency-free validation and packaging tools
.github/workflows/          Push and pull-request validation
```

</details>

---

[Security reporting](SECURITY.md) · [Source attribution and third-party notices](THIRD_PARTY_NOTICES.md) · Released under the MIT License for original contributions. Third-party material (MISFIT collection, Refero Styles design reference) is included under attribution only; redistribution rights for that material have not been independently confirmed.