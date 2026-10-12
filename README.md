# bug-solver-pro

An installable agent skill for diagnosing and fixing backend and application logic bugs across languages and frameworks. The skill and repository are both named **`bug-solver-pro`**.

Canonical repository: [Rhyru9/bug-solver-pro](https://github.com/Rhyru9/bug-solver-pro). [Report an issue](https://github.com/Rhyru9/bug-solver-pro/issues) or browse [releases](https://github.com/Rhyru9/bug-solver-pro/releases).

Install with [Skills CLI](https://github.com/vercel-labs/skills). Node.js and npm (which includes `npx`) are required. The first run downloads the CLI. There is no separate npm package named `bug-solver-pro`. Command examples match Skills CLI 1.7.2; pin with `npx skills@1.7.2` when a newer CLI changes flags.

## Install from GitHub

Run these commands from the project where the skill should be used:

```bash
# Install in the current project; select agents interactively
npx skills@1.7.2 add Rhyru9/bug-solver-pro --skill bug-solver-pro

# Install globally for the current user
npx skills@1.7.2 add Rhyru9/bug-solver-pro --skill bug-solver-pro --global

# The full repository URL also works
npx skills@1.7.2 add https://github.com/Rhyru9/bug-solver-pro --skill bug-solver-pro
```

GitHub installation fetches the complete skill directory, including data, scripts, references, and the MIT license. For a private fork, configure GitHub access in the environment before installing.

## Install from a local clone

Run these commands from the **destination project** (the app being debugged). Replace `/path/to/bug-solver-pro` with the absolute path of the cloned skill repository.

```bash
# Install for the current project
npx skills@1.7.2 add /path/to/bug-solver-pro --skill bug-solver-pro

# Install globally for the current user, across projects
npx skills@1.7.2 add /path/to/bug-solver-pro --skill bug-solver-pro --global
```

The CLI prompts for target agents. To choose them explicitly and skip prompts:

```bash
# Current project: Codex and Claude Code
npx skills@1.7.2 add /path/to/bug-solver-pro --skill bug-solver-pro --agent codex claude-code --yes

# Global: Codex and Claude Code
npx skills@1.7.2 add /path/to/bug-solver-pro --skill bug-solver-pro --agent codex claude-code --global --yes
```

Use `--copy` for copied files instead of agent-directory symlinks. All references, templates, and helper scripts ship with the skill.

## Verify and use

```bash
# List skills in the published repository without installing
npx skills@1.7.2 add Rhyru9/bug-solver-pro --list

# List installed skills in the current project
npx skills@1.7.2 list

# List globally installed skills
npx skills@1.7.2 list --global
```

In Codex, invoke `$bug-solver-pro`; in Claude Code, invoke `/bug-solver-pro`. Agents can also select it when the request matches its description. Invocation and discovery differ between products; see [agent compatibility](COMPATIBILITY.md).

Project installation applies to the project where the install command runs. Global installation applies to the current user. Destination directories depend on the selected agent; see the CLI's [supported agents](https://github.com/vercel-labs/skills#supported-agents).

## After install

Ask the agent to use the skill on a real failure:

> Investigate why replayed webhook retries send duplicate notifications. Use bug-solver-pro.

A useful answer names expected versus actual behavior, the suspected invariant, a discriminating experiment, and the evidence limits. Catalog hits are leads.

If Python 3.9+ is available, run the installed search from the destination project. Replace `<skill-root>` with the installed `bug-solver-pro` folder (typical paths are in [COMPATIBILITY.md](COMPATIBILITY.md)):

```bash
python3 "<skill-root>/scripts/search.py" "replayed webhook retry duplicate notification" --plan
```

If `python3` is missing, use `python` or `py -3`.

## Upgrade and remove

```bash
npx skills@1.7.2 update
npx skills@1.7.2 remove bug-solver-pro
npx skills@1.7.2 remove bug-solver-pro --global
```

Claude Code marketplace installs are separate from `npx skills add`. Remove the plugin in Claude Code if that route was used, so two copies of the workflow are not left behind.

## Claude Code plugin and marketplace

This repository also packages the skill as the `bug-solver-pro` Claude Code plugin, owned by Rhyru9, in the `rhyru9-skills` marketplace. Metadata lives in [.claude-plugin/plugin.json](.claude-plugin/plugin.json) and [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json). The plugin loads the existing root `skills/` directory using Claude Code's standard layout.

```bash
# Register the GitHub repository as a marketplace
claude plugin marketplace add Rhyru9/bug-solver-pro

# Install for the current user (default scope)
claude plugin install bug-solver-pro@rhyru9-skills

# Install for the current destination project
claude plugin install bug-solver-pro@rhyru9-skills --scope project
```

Invoke the plugin skill as `/bug-solver-pro:bug-solver-pro`. Direct installation through `npx skills add` uses `/bug-solver-pro`. Pick one route in Claude Code so the same workflow is not loaded twice.

To register a local clone as a marketplace:

```bash
claude plugin marketplace add /path/to/bug-solver-pro
```

See the official [marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces) and [plugin manifest reference](https://code.claude.com/docs/en/plugins-reference).

## Install for multiple agents

The same skill package can target many agents through Skills CLI, including Claude Code, Codex, Cursor, Gemini CLI, OpenCode, GitHub Copilot CLI, OpenClaw, and Hermes Agent. These are examples, not a fixed allowlist:

```bash
# From the destination project
npx skills@1.7.2 add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent claude-code codex cursor gemini-cli opencode github-copilot --yes

# Same agents, globally
npx skills@1.7.2 add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent claude-code codex cursor gemini-cli opencode github-copilot --global --yes

# OpenClaw and Hermes Agent, from the destination project/workspace
npx skills@1.7.2 add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent openclaw hermes-agent --yes

# OpenClaw and Hermes Agent, globally
npx skills@1.7.2 add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent openclaw hermes-agent --global --yes

# GitHub Copilot CLI uses the github-copilot installer target
npx skills@1.7.2 add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent github-copilot --yes

# Every agent supported by the installed CLI
npx skills@1.7.2 add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent '*' --yes
```

The wildcard includes agents the reader may not use; an explicit list is safer. Add `--global` to the wildcard command for user-level installation. Other targets include Goose, Pi, Kimi Code CLI, Qwen Code, Roo Code, Windsurf, and more; the complete list is in the [Skills CLI README](https://github.com/vercel-labs/skills#supported-agents). See [COMPATIBILITY.md](COMPATIBILITY.md) for directories, invocation, OpenClaw workspace selection, Hermes project trust, helper requirements, and known limits.

For Copilot CLI, run `/skills reload` and `/skills info bug-solver-pro` inside an existing session after installation. Invoke `/bug-solver-pro` in the prompt. See the [official Copilot CLI skill guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills).

## Skill contents

The discoverable entrypoint lives at [skills/bug-solver-pro/SKILL.md](skills/bug-solver-pro/SKILL.md). Supporting files stay alongside it so relative links work after installation.

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

See the [skill overview](skills/bug-solver-pro/README.md) for the workflow.

## Structured diagnostic tooling

The package includes 48 structured heuristic patterns across eleven domains, covering representation, lifecycle, control flow, concurrency, persistence, contracts, integration, access decisions, performance, testing, and diagnosis. Local lexical search returns candidate mechanisms with experiments, falsifying observations, verification checks, and references. Fourteen observation angles support investigation beyond the recorded catalog.

Requires Python 3.9+; no pip dependencies or network calls. Replace `<skill-root>` with the installed folder that contains `SKILL.md`. If `python3` is missing, use `python` or `py -3`:

```bash
python3 "<skill-root>/scripts/search.py" "duplicate webhook retry" --domain concurrency
python3 "<skill-root>/scripts/search.py" "memory retained listeners" --plan --json
python3 "<skill-root>/scripts/search.py" "unexplained boundary failure" --explore --json
```

Search scores describe lexical relevance, not causal confidence. Missing or weak matches route to open-world exploration. Use sanitized English keywords. Catalog seeds are curated from bundled references; they are not verified incident cases. [Structured tooling](skills/bug-solver-pro/references/17-structured-tooling.md) describes the schema; [coverage and unknowns](skills/bug-solver-pro/references/18-coverage-and-unknowns.md) covers unrecorded bugs and interacting mechanisms.

Issue reports, diagnostic coverage gaps, and contributor checks are in the [.github contributor guide](.github/CONTRIBUTING.md). User-visible changes are listed in [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE), copyright (c) 2026 Rhyru9. A copy is bundled in the [skill directory](skills/bug-solver-pro/LICENSE) so standalone skill installation carries its license notice.
