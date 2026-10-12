# Agent compatibility

Researched on 2026-10-13. This is documentation and package inspection, not an execution test in each agent.

Canonical source: [Rhyru9/bug-solver-pro](https://github.com/Rhyru9/bug-solver-pro). Installation examples below use that repository once it is available; a local checkout path can be substituted before publication.

## Shared package

`bug-solver-pro` uses the portable [Agent Skills format](https://agentskills.io/specification): a skill folder with `SKILL.md`, YAML `name` and `description`, and relative references to bundled resources. The folder matches the skill name. Inspection found no required proprietary tools, MCP servers, or agent-specific frontmatter. This supports using one package across compatible hosts; it does not establish equal debugging effectiveness.

## Installer targets

The skill is not restricted to a fixed list of agents. The following are representative destination roots documented by [Skills CLI](https://github.com/vercel-labs/skills#supported-agents), not an exhaustive support matrix. The skill folder `bug-solver-pro/` belongs under each root; default installs may use symlinks. The installed CLI version determines which `--agent` identifiers it accepts.

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
# Install from the canonical repository after publication
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent openclaw hermes-agent goose pi --yes

# User-level installation for the same agents
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent openclaw hermes-agent goose pi --global --yes

# Every target recognized by the installed CLI
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro --agent '*' --global --yes
```

For a host not yet registered in Skills CLI, check its native Agent Skills support. If supported, place the complete `skills/bug-solver-pro/` folder in a documented discovery root or configure an external skill directory. Preserve the bundled data, scripts and references; installing only `SKILL.md` breaks relative resources. A product name alone does not establish native skill support.

## Activation differs by host

- **Claude Code:** direct skill installation uses `/bug-solver-pro`. Installation through this repository's `rhyru9-skills` marketplace uses the plugin namespace `/bug-solver-pro:bug-solver-pro`. Both use the same skill resources; choose one installation route. Its native project and personal skill directories match the installer destinations. [Claude Code documentation](https://code.claude.com/docs/en/skills), [plugin marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces).
- **Codex CLI / IDE:** invoke `$bug-solver-pro`, use `/skills`, or let Codex match the description. Repository and user skills load from `.agents/skills/`; symlinked folders are supported. [Official OpenAI documentation](https://learn.chatgpt.com/docs/build-skills).
- **Cursor:** supports project and user skill directories, including `.agents/skills/`. Local global installation does not automatically make the skill available to remote or cloud environments. [Cursor documentation](https://cursor.com/docs/skills).
- **Gemini CLI:** discovers `.agents/skills/` as an alias of its native skill locations. Use `/skills list` to check discovery and `/skills reload` to refresh it. Matching tasks activate the skill through its tool and host consent flow. [Gemini CLI documentation](https://geminicli.com/docs/cli/skills/).
- **OpenCode:** discovers agent-compatible directories and loads skills on demand through its skill tool. A slash command is an optional host feature; this package does not enable OpenCode-specific metadata. [OpenCode documentation](https://opencode.ai/docs/skills).
- **OpenClaw:** reads `<workspace>/skills/` and `<workspace>/.agents/skills/`; managed skills default to `~/.openclaw/skills/`. For a project install, run the installer from the configured agent workspace. If this source repository itself is that workspace, its existing `skills/bug-solver-pro/` is already in a native discovery root; there is no need to install over the source folder. Custom state directories and allowlists affect visibility. [OpenClaw documentation](https://docs.openclaw.ai/tools/skills).
- **Hermes Agent:** supports the Agent Skills format and uses `~/.hermes/skills/` for its default user library. Repo discovery accepts `.hermes/skills/` and `.agents/skills/` at the Git project root, but project skills load only after the user trusts the repository (`hermes skills trust`). Skills are available as `/skill-name` commands; external directories and profiles can change discovery. [Official Hermes documentation](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md).
- **GitHub Copilot CLI:** use the installer target `github-copilot`, not `copilot-cli`. Native project discovery accepts `.github/skills/`, `.claude/skills/` and `.agents/skills/`; personal discovery accepts `~/.copilot/skills/` and `~/.agents/skills/`. In an active session run `/skills reload`, then `/skills info bug-solver-pro` to check discovery. Invoke with `/bug-solver-pro` in your prompt or let Copilot match the description. CLI support does not imply identical behavior in every editor or cloud surface. [Copilot CLI documentation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills).
- **Cline:** its installer target is documented above. Check native discovery and the installed product version. [Skills CLI](https://github.com/vercel-labs/skills#supported-agents).

Do not assume Codex's `$name` invocation works in every agent. Where explicit invocation is unavailable, ask the agent to use `bug-solver-pro` and verify that it reads the installed entrypoint.

## Optional helpers and operating systems

The reasoning workflow is Markdown and can be used without the shell helpers. The four `.sh` helpers require Bash and common shell utilities; history helpers also require Git. Search helpers prefer `rg` and fall back to `grep`.

The searchable catalog CLI requires Python 3.9+ and uses only its standard library. It resolves bundled data relative to the installed script, independent of the project working directory. Invoke it through the installed skill's absolute path; no Claude plugin environment variable is needed.

Catalog data, script output and instructions are in English. Use sanitized English query terms. `--explore` provides observation angles for bugs that have no recorded pattern; weak matches remain lexical leads rather than automatically becoming hypotheses.

`scan-risky-patterns.sh` additionally requires `timeout` or `gtimeout`. It now fails explicitly if that dependency is missing or a search fails, instead of treating failure as an empty match set. Native Windows requires a Bash environment such as WSL or Git Bash plus the required utilities. Where these are unavailable, use the agent's IDE search, language server, or debugger as the skill already instructs.

`find-usages.sh` treats symbols literally and distinguishes tool failure from no matches. `co-change.sh` handles terminated commit records and valid empty results; paths requiring Git quoting or historical names across renames still need manual review. The current suite checks these helpers on local fixtures, not every OS or Git/search-tool variant.

## Validation limits

Package metadata and local links were checked. Live installation remains untested because this environment could not resolve the npm registry during the earlier CLI attempt. No agent sessions or global installs were launched for this research. Future runtime checks should verify discovery, reading relative references, and a representative debugging task in each target host.
