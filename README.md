# bug-solver-pro

`bug-solver-pro` gives a coding agent a way to investigate backend and application logic bugs: trace the failing path, test an explanation, then verify the repair. It combines a debugging workflow with local framework playbooks and searchable diagnostic knowledge.

Consider a webhook that sends the same notification twice. The first request may have committed successfully before its response was lost. A retry then repeats the effect. To choose a repair, the agent needs to distinguish two submissions from two attempts at the same operation, find where the duplicate becomes possible, and check what happens after a crash.

This skill guides that investigation. Use it for incorrect results, inconsistent state, races, failed integrations, resource problems, and bugs that return after an apparently successful patch. Its scope is debugging existing behavior; new feature planning belongs elsewhere.

## How an investigation works

Start by giving the agent the failure you observed and the behavior you expected. For the webhook example, that might be:

> Replaying the same webhook sends another notification. Each event should notify once. Use bug-solver-pro to investigate, fix it, and verify retry behavior.

The workflow asks the agent to follow the operation through its real entrypoint, database changes, queue, and external effects. It separates the logical event from individual delivery attempts, then looks for the first boundary where the promised behavior breaks.

A candidate explanation needs a useful test. The agent might replay one event with a lost acknowledgement after the first effect, then inspect durable state and notification counts. A passing test only rules out that explanation when the relevant retry occurred and the test could detect a duplicate.

Once the evidence supports a cause, the agent repairs the boundary that owns the invariant and checks the original trigger, nearby valid behavior, and relevant failure paths. For this example, recording an operation key after sending the notification would still leave a crash window. The repair has to account for the actual transaction and delivery guarantees.

The result should explain the cause, the change, what was tested, and what remains uncertain. When reproduction is unavailable, the agent can work from incident evidence and report a candidate fix with its limits.

## Knowledge for your stack

Framework playbooks make that workflow concrete. They cover traps such as Spring calls bypassing transaction advice, React drafts following the wrong list keys, Django bulk writes skipping model hooks, and an Express parser consuming bytes needed for webhook verification.

Each framework has local recipes with a mechanism, a probe, observations that would contradict it, repair options, and regression checks. A deeper boundary case examines an additional trap and the tempting fixes that can make it worse. Official documentation supports unresolved contracts and version differences.

| Language | Frameworks and libraries with local guidance |
|---|---|
| JavaScript / TypeScript | Express, NestJS, React, Next.js, Vue, Nuxt, Svelte, SvelteKit, Angular, Hono |
| Python | Django, FastAPI, Flask |
| PHP | Laravel, Symfony |
| Java | Spring |
| C# / .NET | ASP.NET Core, including EF Core boundary cases |
| Go | Gin, Echo |
| Rust | Axum, Actix Web |
| Ruby | Rails |

The [framework index](skills/bug-solver-pro/references/frameworks/index.md) leads to 88 techniques across these 22 modules. A shared catalog adds 54 diagnostic patterns, while 20 observation angles help investigate bugs outside the recorded examples. For an unfamiliar stack, the workflow starts from its actual execution and dependency semantics.

These are authored techniques supported by contracts and specific probes. The [coverage audit](skills/bug-solver-pro/references/coverage/gap-audit.md) and [data audit](skills/bug-solver-pro/references/coverage/data-audit.md) record their evidence and remaining gaps. Executed FastAPI and SQLite fixtures check a few bounded cases; they do not establish debugging quality for every framework, version, or agent.

## Install from GitHub

Run the installer from the application project where you want to use the skill. It requires Node.js and npm; `npx` fetches the [Skills CLI](https://github.com/vercel-labs/skills), which installs the skill from this repository.

```bash
# Install for the current project and select your agents
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro

# Or install for the current user across projects
npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro --global
```

<a id="install-for-multiple-agents"></a>

To select agents without prompts, append `--agent codex claude-code --yes`. The installer supports other hosts too; [COMPATIBILITY.md](COMPATIBILITY.md) explains their target names, locations, and activation. Add `--copy` if you want copied files rather than symlinks.

<a id="install-from-a-local-clone"></a>

If you are developing this repository, run `npx skills add /path/to/bug-solver-pro --skill bug-solver-pro` from the destination application project. Install the complete skill folder so its data, scripts, and relative references travel together.

## After install

<a id="verify-and-use"></a>

Ask your agent to use `bug-solver-pro` with a concrete failure, as in the webhook example above. Direct skill installations use `$bug-solver-pro` in Codex and `/bug-solver-pro` in Claude Code. Other hosts have their own discovery and invocation rules.

You can check project installations with `npx skills list`, or user installations with `npx skills list --global`. If the skill is missing from the agent's session, follow its reload/discovery steps in [COMPATIBILITY.md](COMPATIBILITY.md).

Python is optional for the written workflow. The agent can inspect the local guides and use the application's existing tools without running the bundled search.

## Claude Code plugin and marketplace

Claude Code users can also install the same skill through this repository's marketplace:

```bash
claude plugin marketplace add Rhyru9/bug-solver-pro
claude plugin install bug-solver-pro@rhyru9-skills
```

This route uses `/bug-solver-pro:bug-solver-pro`. Add `--scope project` to the install command for project scope. Choose either the direct skill or the marketplace plugin so the workflow has one installation source. See [Claude's marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces) for host-specific behavior.

## Structured diagnostic tooling

The optional search runs locally with Python 3.9+ and its standard library. Replace `<skill-root>` with the installed directory containing `SKILL.md`; run the script through that path from the application you are debugging.

```bash
python3 "<skill-root>/scripts/search.py" "duplicate webhook retry" --plan
python3 "<skill-root>/scripts/search.py" "body signature whitespace" --framework Express --json
python3 "<skill-root>/scripts/search.py" "unexplained boundary failure" --explore
```

Use a few sanitized English symptom terms. Search returns shared mechanisms and matching local framework sections. `--framework` restricts recipe leads to the named stack and includes its full local playbook. `--plan` adds candidate experiments; `--explore` supplies observation angles without generating hypotheses. If your interpreter is named `python` or `py -3`, use that instead.

A search result is a lead to inspect. Scores measure word overlap, and a strong match still needs code and evidence. JSON keeps shared-catalog status separate from `framework_matches`, so a missing shared pattern can coexist with a useful framework recipe. The [tooling reference](skills/bug-solver-pro/references/17-structured-tooling.md) describes the output, filters, validation, and limits.

## Upgrade and remove

For a Skills CLI installation, update from the destination project or the appropriate user scope:

```bash
npx skills update
npx skills remove bug-solver-pro
```

Use `--global` when removing a user-level installation. Installer commands follow the current Skills CLI; the older `skills@1.7.2` examples in the compatibility guide provide a pinned reference.

For a marketplace installation, refresh its catalog, update the plugin, then restart Claude Code:

```bash
claude plugin marketplace update rhyru9-skills
claude plugin update bug-solver-pro@rhyru9-skills
```

Package version 1.1.0 keeps the skill name, installation layout, existing search flags, shared data schema, and shared result fields. It adds framework recipe results and `--framework`; JSON consumers should tolerate the additional fields. Reinstall or update the whole skill rather than copying individual new scripts into an older installation.

## Extend the skill

<a id="skill-contents"></a>

The entrypoint is [SKILL.md](skills/bug-solver-pro/SKILL.md). Shared reasoning lives in `references/`; language and framework guides live beneath `references/languages/`. Framework retrieval metadata lives in `data/frameworks/<language>/<framework>/recipes.json` and points to the local Markdown that owns the technique.

To add coverage, start with a concrete debugging gap and the [module template](skills/bug-solver-pro/templates/stack-module.md). Include a discriminator, repair tradeoffs, verification, and evidence limits. Update the index when changing a recipe's heading. The [.github contributor guide](.github/CONTRIBUTING.md) covers data contracts, validation, and building installable ZIPs.

Report a bug or missing diagnostic angle in [GitHub issues](https://github.com/Rhyru9/bug-solver-pro/issues). Changes are recorded in [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE), copyright (c) 2026 Rhyru9. The license is also bundled in the standalone [skill folder](skills/bug-solver-pro/LICENSE).
