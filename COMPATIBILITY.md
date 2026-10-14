# Agent compatibility

Canonical source: [Rhyru9/bug-solver-pro](https://github.com/Rhyru9/bug-solver-pro). Installation examples use that repository. A local clone path can be substituted.

This document describes installer destinations, invocation differences, and helper requirements. It does not claim equal debugging quality in every host.

## Shared package

`bug-solver-pro` uses the portable [Agent Skills format](https://agentskills.io/specification): a skill folder with `SKILL.md`, YAML `name` and `description`, and relative references to bundled resources. The folder matches the skill name. The package does not require proprietary tools, MCP servers, or agent-specific frontmatter. One package can be copied into compatible hosts.

## Installer targets

The skill is not restricted to a fixed list of agents. The following are representative destination roots documented by [Skills CLI](https://github.com/vercel-labs/skills#supported-agents), not an exhaustive support matrix. The skill folder `bug-solver-pro/` belongs under each root; default installs may use symlinks. The installed CLI version determines which `--agent` identifiers it accepts. Examples in this repository match Skills CLI 1.7.2.

| Agent | `--agent` value | Project root | Global root |
|---|---|---|---|
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `codex` | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `cursor` | `.agents/skills/` | `~/.cursor/skills/` |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | `~/.gemini/skills/` |
| OpenCode | `opencode` | `.agents/skills/` | `~/.config/opencode/skills/` |
| GitHub Copilot CLI | `github-copilot` | `.agents/skills/` | `~/.copilot/skills/` |
| Cline | `cline` | `.agents/skills/` | `~/.agents/skills/` |
| OpenClaw | `openclaw` | `skills/` | `~/.openclaw/skills/` |
| Hermes Agent | `hermes-agent` | `.hermes/skills/` | `~/.hermes/skills/` |
| Goose | `goose` | `.goose/skills/` | `~/.config/goose/skills/` |
| Pi | `pi` | `.agents/skills/` | `~/.agents/skills/` |
| Kimi Code CLI | `kimi-code-cli` | `.agents/skills/` | `~/.agents/skills/` |
| Qwen Code | `qwen-code` | `.qwen/skills/` | `~/.qwen/skills/` |
| Roo Code | `roo` | `.roo/skills/` | `~/.roo/skills/` |
| Windsurf | `windsurf` | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| Droid | `droid` | `.agents/skills/` | `~/.factory/skills/` |
| Amp | `amp` | `.agents/skills/` | `~/.config/agents/skills/` |
| Antigravity | `antigravity` | `.agents/skills/` | `~/.gemini/antigravity/skills/` |
| Deep Agents | `deepagents` | `.agents/skills/` | `~/.deepagents/agent/skills/` |

The complete, maintained target list is upstream. Native discovery paths may include additional aliases beyond these installer destinations. Standard-format support and successful installation do not establish identical tool access or diagnosis quality in every host.

To target additional agents from the destination project or workspace:

```bash
# Install from the canonical repository
npx skills@1.7.2 add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent openclaw hermes-agent goose pi --yes

# User-level installation for the same agents
npx skills@1.7.2 add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent openclaw hermes-agent goose pi --global --yes

# Every target recognized by the installed CLI
npx skills@1.7.2 add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent '*' --global --yes
```

For a host not yet registered in Skills CLI, check its native Agent Skills support. If supported, place the complete `skills/bug-solver-pro/` folder in a documented discovery root or configure an external skill directory. Preserve the bundled data, scripts and references; installing only `SKILL.md` breaks relative resources. A product name alone does not establish native skill support.

## Activation differs by host

- **Claude Code:** direct skill installation uses `/bug-solver-pro`. Installation through this repository's `rhyru9-skills` marketplace uses the plugin namespace `/bug-solver-pro:bug-solver-pro`. Both use the same skill resources; choose one installation route. Its native project and personal skill directories match the installer destinations. [Claude Code documentation](https://code.claude.com/docs/en/skills), [plugin marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces).
- **Codex CLI / IDE:** invoke `$bug-solver-pro`, use `/skills`, or let Codex match the description. Repository and user skills load from `.agents/skills/`; symlinked folders are supported. [Official OpenAI documentation](https://learn.chatgpt.com/docs/build-skills).
- **Cursor:** supports project and user skill directories, including `.agents/skills/`. Local global installation does not automatically make the skill available to remote or cloud environments. [Cursor documentation](https://cursor.com/docs/skills).
- **Gemini CLI:** discovers `.agents/skills/` as an alias of its native skill locations. Use `/skills list` to check discovery and `/skills reload` to refresh it. Matching tasks activate the skill through its tool and host consent flow. [Gemini CLI documentation](https://geminicli.com/docs/cli/skills/).
- **OpenCode:** discovers agent-compatible directories and loads skills on demand through its skill tool. A slash command is an optional host feature; this package does not enable OpenCode-specific metadata. [OpenCode documentation](https://opencode.ai/docs/skills).
- **OpenClaw:** reads `<workspace>/skills/` and `<workspace>/.agents/skills/`; managed skills default to `~/.openclaw/skills/`. For a project install, run the installer from the configured agent workspace. If that workspace already contains `skills/bug-solver-pro/`, OpenClaw can discover it without a second copy. Custom state directories and allowlists affect visibility. [OpenClaw documentation](https://docs.openclaw.ai/tools/skills).
- **Hermes Agent:** supports the Agent Skills format and uses `~/.hermes/skills/` for its default user library. Repo discovery accepts `.hermes/skills/` and `.agents/skills/` at the Git project root, but project skills load only after the user trusts the repository (`hermes skills trust`). Skills are available as `/skill-name` commands; external directories and profiles can change discovery. [Official Hermes documentation](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md).
- **GitHub Copilot CLI:** use the installer target `github-copilot`, not `copilot-cli`. Native project discovery accepts `.github/skills/`, `.claude/skills/` and `.agents/skills/`; personal discovery accepts `~/.copilot/skills/` and `~/.agents/skills/`. In an active session run `/skills reload`, then `/skills info bug-solver-pro` to check discovery. Invoke with `/bug-solver-pro` in the prompt or let Copilot match the description. CLI support does not imply identical behavior in every editor or cloud surface. [Copilot CLI documentation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills).
- **Cline:** its installer target is documented above. Check native discovery and the installed product version. [Skills CLI](https://github.com/vercel-labs/skills#supported-agents).

Do not assume Codex's `$name` invocation works in every agent. Where explicit invocation is unavailable, ask the agent to use `bug-solver-pro` and verify that it reads the installed entrypoint.

## Optional helpers and operating systems

The reasoning workflow is Markdown and can be used without the shell helpers. The four `.sh` helpers require Bash and common shell utilities; history helpers also require Git. Search helpers prefer `rg` and fall back to `grep`.

The searchable catalog CLI requires Python 3.9+ and uses only its standard library. It resolves bundled data relative to the installed script, independent of the project working directory. Invoke it through the installed skill's absolute path; no Claude plugin environment variable is needed. If `python3` is missing, use `python` or `py -3` with the same arguments.

Catalog data, script output and instructions are in English. Use sanitized English query terms. `--explore` provides observation angles for bugs that have no recorded pattern; weak matches remain lexical leads rather than automatically becoming hypotheses.

`scan-risky-patterns.sh` additionally requires `timeout` or `gtimeout`. It fails explicitly if that dependency is missing or a search fails. The scan skips credential-like names such as `.env`, `*.pem`, and paths containing `secret` or `credential`. Native Windows requires a Bash environment such as WSL or Git Bash plus the required utilities. Where these are unavailable, use the agent's IDE search, language server, or debugger as the skill already instructs.

`find-usages.sh` treats symbols literally, skips the same credential-like names, and distinguishes tool failure from no matches. `co-change.sh` handles terminated commit records and valid empty results; paths requiring Git quoting or historical names across renames still need manual review. The current suite checks these helpers on local fixtures, not every OS or Git/search-tool variant.

## Updating from 1.0.x

Version 1.1.0 preserves the skill name, standard installation layout, existing search flags, shared catalog/angle schema version 1, and shared JSON result fields. The CLI additionally returns `framework_matches`; `--framework` scopes those recipe leads and loads local module context. Lexical rankings can change as the catalog grows. JSON consumers should accept additional fields and distinguish shared status from recipe status.

Update the complete skill directory so scripts, indexes, and Markdown sections remain aligned. Existing Skills CLI installations can use `npx skills update` in the intended scope. For the Claude marketplace route, run `claude plugin marketplace update rhyru9-skills`, then `claude plugin update bug-solver-pro@rhyru9-skills` and restart the host. The plugin manifest version advances to 1.1.0 for this package update.

## Known limits

- CI checks package metadata, Markdown links, catalog schema, retrieval ranking, and extracted ZIP behavior.
- Live `npx skills add` into each agent, and a representative debugging session in each host, are outside that suite.
- Catalog scores are lexical relevance. They are not causal confidence or a guarantee against regressions.
- Helper scripts need the tools listed above; the Markdown workflow does not.
