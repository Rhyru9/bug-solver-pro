# bug-solver-pro

An installable agent skill for diagnosing and fixing backend and application logic bugs across languages and frameworks. The skill and repository are both named **`bug-solver-pro`**.

Canonical repository: [Rhyru9/bug-solver-pro](https://github.com/Rhyru9/bug-solver-pro). [Report an issue](https://github.com/Rhyru9/bug-solver-pro/issues) or browse [releases](https://github.com/Rhyru9/bug-solver-pro/releases).

Install with [Skills CLI](https://github.com/vercel-labs/skills). No custom npm package or installer is required. Node.js and npm (which includes `npx`) are needed to run the installer. The first run downloads the CLI.

## Install from GitHub

Once the repository is available on GitHub, run from the project where you want to use the skill:

```bash
# Install in the current project; select agents interactively
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro

# Install globally for your user
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro --global

# The full repository URL also works
npx skills add https://github.com/Rhyru9/bug-solver-pro --skill bug-solver-pro
```

GitHub installation fetches the complete skill directory, including its data, scripts, references and MIT license. Repository publication is sufficient; no separate `bug-solver-pro` npm package is required. For a private repository, configure access to GitHub in your environment before installing.

## Install from a local checkout

Run these commands **from the project where you want to use the skill**. Replace `/path/to/bug-solver-pro` with the absolute path to this checkout.

```bash
# Install for the current project
npx skills add /path/to/bug-solver-pro --skill bug-solver-pro

# Install globally for your user, across projects
npx skills add /path/to/bug-solver-pro --skill bug-solver-pro --global
```

The CLI prompts for the target agents. To choose them explicitly and skip prompts:

```bash
# Current project: Codex and Claude Code
npx skills add /path/to/bug-solver-pro --skill bug-solver-pro --agent codex claude-code --yes

# Global: Codex and Claude Code
npx skills add /path/to/bug-solver-pro --skill bug-solver-pro --agent codex claude-code --global --yes
```

Use `--copy` if you prefer copied files instead of agent-directory symlinks. All references, templates, and helper scripts are included with the skill.

To install into this repository itself, run from its root:

```bash
npx skills add . --skill bug-solver-pro --agent codex --yes
```

## Verify and use

```bash
# Discover the published repository's skill without installing it
npx skills add Rhyru9/bug-solver-pro --list

# List installed skills in the current project
npx skills list

# List globally installed skills
npx skills list --global
```

In Codex, invoke `$bug-solver-pro`; in Claude Code, invoke `/bug-solver-pro`. Agents can also select it when the request matches its description. Invocation and discovery differ between products; see [agent compatibility](COMPATIBILITY.md).

Project installation applies to the project where the install command runs. Global installation applies to the current user. Destination directories depend on the selected agent; see the CLI's [supported agents](https://github.com/vercel-labs/skills#supported-agents).

## Claude Code plugin and marketplace

This repository also packages the skill as the `bug-solver-pro` Claude Code plugin, owned by Rhyru9, in the `rhyru9-skills` marketplace. Metadata lives in [.claude-plugin/plugin.json](.claude-plugin/plugin.json) and [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json). The plugin loads the existing root `skills/` directory using Claude Code's standard layout.

```bash
# Register the published GitHub repository as a marketplace
claude plugin marketplace add Rhyru9/bug-solver-pro

# Install for your user (default scope)
claude plugin install bug-solver-pro@rhyru9-skills

# Alternatively, install for the current destination project
claude plugin install bug-solver-pro@rhyru9-skills --scope project
```

Invoke the plugin skill as `/bug-solver-pro:bug-solver-pro`. Direct installation through `npx skills add` uses `/bug-solver-pro` instead. Choose either route for Claude Code to avoid loading two copies of the same workflow.

For local development, run from this repository root:

```bash
claude plugin validate .
claude --plugin-dir .
```

For a checkout that has not been published, register it with `claude plugin marketplace add /path/to/bug-solver-pro`. See the official [marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces) and [plugin manifest reference](https://code.claude.com/docs/en/plugins-reference).

## Install for multiple agents

The same skill package can target many agents through Skills CLI, including Claude Code, Codex, Cursor, Gemini CLI, OpenCode, GitHub Copilot CLI, OpenClaw and Hermes Agent. These are examples, not a fixed allowlist:

```bash
# Run from the destination project after repository publication
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent claude-code codex cursor gemini-cli opencode github-copilot --yes

# Install for the same agents globally
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent claude-code codex cursor gemini-cli opencode github-copilot --global --yes

# OpenClaw and Hermes Agent, from the destination project/workspace
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent openclaw hermes-agent --yes

# OpenClaw and Hermes Agent, globally
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent openclaw hermes-agent --global --yes

# GitHub Copilot CLI uses the github-copilot installer target
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent github-copilot --yes

# Target every agent supported by the installed CLI
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent '*' --yes
```

The wildcard includes agents you may not use; prefer an explicit list. Add `--global` to the wildcard command for user-level installation. Other targets include Goose, Pi, Kimi Code CLI, Qwen Code, Roo Code, Windsurf and more; the complete list is maintained in the [Skills CLI README](https://github.com/vercel-labs/skills#supported-agents). See [COMPATIBILITY.md](COMPATIBILITY.md) for directories, invocation, OpenClaw workspace selection, Hermes project trust, helper requirements and research limits.

For Copilot CLI, run `/skills reload` and `/skills info bug-solver-pro` inside an existing session after installation. Invoke `/bug-solver-pro` in your prompt. See the [official Copilot CLI skill guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills).

## Skill contents

The discoverable entrypoint lives at [skills/bug-solver-pro/SKILL.md](skills/bug-solver-pro/SKILL.md). Keep supporting files alongside it so relative links work after installation.

```text
skills/bug-solver-pro/
├── SKILL.md
├── README.md
├── data/
│   ├── patterns.json
│   └── angles.json
├── references/
├── templates/
└── scripts/
```

See the [skill overview](skills/bug-solver-pro/README.md) for its workflow.

## Structured diagnostic tooling

The package includes 48 structured heuristic patterns across eleven domains, covering representation, lifecycle, control flow, concurrency, persistence, contracts, integration, access decisions, performance, testing and diagnosis. Local lexical search returns candidate mechanisms with experiments, falsifying observations, verification checks and references. Fourteen observation angles support investigation beyond the recorded catalog.

Requires Python 3.9+; no pip dependencies or network calls. Replace `<skill-root>` with the installed folder containing `SKILL.md`, regardless of your agent:

```bash
python3 "<skill-root>/scripts/search.py" "duplicate webhook retry" --domain concurrency
python3 "<skill-root>/scripts/search.py" "memory retained listeners" --plan --json
python3 "<skill-root>/scripts/search.py" "unexplained boundary failure" --explore --json
```

Search scores describe lexical relevance, not causal confidence. Missing or weak matches route to open-world exploration rather than automatically becoming hypotheses. Use sanitized English keywords. The catalog is curated from bundled references, and its seeds are not verified incident cases. [Structured tooling](skills/bug-solver-pro/references/17-structured-tooling.md) describes the schema; [coverage and unknowns](skills/bug-solver-pro/references/18-coverage-and-unknowns.md) explains investigation of unrecorded bugs and interacting mechanisms.

For development checks, run from this repository root:

```bash
python3 -B scripts/check_package.py
python3 -B skills/bug-solver-pro/scripts/validate_data.py
python3 -B -m unittest discover -s tests -v
```

## GitHub contribution and automation

The [.github contributor guide](.github/CONTRIBUTING.md) explains issue reports, diagnostic coverage gaps and PR checks. CI runs the regression suite across Linux, macOS and Windows, validates package resources and checks extracted ZIP behavior. These checks cover local tooling and distribution; they do not establish bug-solving effectiveness in every agent.

Pushing a tag matching `.claude-plugin/plugin.json`, such as `v1.0.0`, triggers tests and prepares a draft GitHub release with standalone-skill and Claude-plugin ZIPs. Review the draft before publishing. Build those ZIPs locally with:

```bash
python3 -B scripts/build_release.py --output-dir dist
```

## License

[MIT](LICENSE), copyright (c) 2026 Rhyru9. A copy is bundled in the [skill directory](skills/bug-solver-pro/LICENSE) so standalone skill installation carries its license notice.
