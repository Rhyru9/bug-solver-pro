# Contributing to bug-solver-pro

Project repository: [Rhyru9/bug-solver-pro](https://github.com/Rhyru9/bug-solver-pro). Use its [issue tracker](https://github.com/Rhyru9/bug-solver-pro/issues) and [pull requests](https://github.com/Rhyru9/bug-solver-pro/pulls). Public installation is documented in the [README](https://github.com/Rhyru9/bug-solver-pro#install-from-github).

Clone the source:

```bash
git clone https://github.com/Rhyru9/bug-solver-pro.git
cd bug-solver-pro
```

Canonical skill resources live in `skills/bug-solver-pro/`. Claude plugin metadata lives in `.claude-plugin/`. Tests and repository tooling live in `tests/` and `scripts/`; neither requires third-party Python packages.

Language-specific guidance belongs in `references/languages/<language>/guide.md` within the canonical skill. Framework-specific guidance belongs in `references/languages/<language>/frameworks/<framework>/guide.md`. Use the [module index](../skills/bug-solver-pro/references/languages/index.md) and [authoring template](../skills/bug-solver-pro/templates/stack-module.md). Link each new module from the index and each framework from its language guide. Keep shared causal mechanisms in the numbered references and add only populated modules with concrete discovery questions, experiments, and verification limits. Package checks validate nested Markdown links and release builds include these directories recursively.

To load this checkout into Codex while developing the skill:

```bash
npx skills@1.7.2 add . --skill bug-solver-pro --agent codex --yes
```

To run Claude Code against this checkout as a plugin:

```bash
claude --plugin-dir .
```

Report broken behavior with the bug template. Use the diagnostic-gap template for unrecorded mechanisms, misleading search results or missing observation angles. Include sanitized inputs, versions, expected/actual behavior and traceable evidence. Keep unrelated production actions outside reproduction work.

Catalog seeds remain heuristics. Each added pattern needs a candidate mechanism, discriminator, falsifying result, verification, limits and local source references. Add positive paraphrases and confusing or unrelated queries to retrieval tests. Keep genuinely reproduced lessons separate from hypothetical mechanisms. Do not make the catalog a required ceiling on investigation. Installed-skill search contracts live in `skills/bug-solver-pro/references/17-structured-tooling.md`; repository tests stay in `tests/`.

Framework techniques also need retrieval metadata in `data/frameworks/<language>/<framework>/recipes.json`. Follow the structured-tooling schema: stable IDs, diagnostic domain, curated keyword aliases, one owning reference, exact heading and heuristic evidence label. Markdown remains the content owner. Every numbered playbook recipe and optional boundary case must be indexed exactly once, and metadata owner must match file/reference paths. Validators reject duplicate JSON keys/references/domains, cross-owner routes, omitted recipes and ambiguous/empty sections. Add meaningful retrieval regressions and negative controls; counts alone do not assess semantic quality. The [data audit](../skills/bug-solver-pro/references/coverage/data-audit.md) tracks demonstrated gaps and evidence.

Framework modules require `playbook.md` with usable stack-specific recipes: concrete failure signatures, causal mechanisms/prerequisites, probes with falsifying outcomes, repair options/tradeoffs, and regression verification. A generic question list or URL list alone is insufficient. Link supporting official contracts at the recipe and keep authored techniques distinct from reproduced incidents. Each module also requires `docs.md` with verified direct official links and version-selection guidance. Lead the dedicated [framework index](../skills/bug-solver-pro/references/frameworks/index.md) and guide with the playbook. Follow the [documentation access workflow](../skills/bug-solver-pro/references/framework-documentation.md) for unresolved contracts/version changes. Package checks cover local links; remote availability requires a separate check when changing URLs.

Track consequential skill gaps in the [coverage audit](../skills/bug-solver-pro/references/coverage/gap-audit.md), naming observed weakness, implemented correction, evidence level and remaining limits. A non-failing probe is inconclusive unless applicability, activation, sensitivity and comparable state are established. Keep optional deep cases in `boundary-case.md` and link them from the playbook and guide; `--framework` loads that file when present. Package checks require each discovered framework to have playbook/guide/docs and resolve its local resources. Runtime effectiveness is a separate claim from Python tooling tests.

The optional FastAPI runtime probe executes isolated ASGI fixtures only when FastAPI is already installed; it does not add a dependency requirement to ordinary tooling checks. Record its actual versions and bounded results separately from production incidents or general agent effectiveness. New runtime probes need independent correctness expectations and a discriminator/repair comparison, not assertions that merely echo documentation headings.

Before submitting a change, run:

```bash
python -B scripts/check_package.py
python -B skills/bug-solver-pro/scripts/validate_data.py
python -B -m unittest discover -s tests -v
```

Where Bash is available, check changed shell helpers with `bash -n`. If Claude Code is installed, validate the marketplace and plugin with `claude plugin validate .` and `claude plugin validate .claude-plugin/plugin.json`. The Python package check validates repository invariants; it does not replace Claude's authoritative manifest validator.

## CI and release packaging

The tests workflow covers Python 3.9 and 3.14 on Linux, plus Python 3.14 on macOS and Windows. It checks data, references, manifests, matching licenses and extracted ZIP behavior in the same suite. Optional Bash/Git tests skip where those tools are unavailable. Text resources use LF line endings across checkout platforms.

Plugin version in `.claude-plugin/plugin.json` is the release version source of truth. Update it deliberately, merge the validated change, then push a matching tag such as `v1.0.0`. A tag triggers checks and creates a **draft** GitHub release with standalone-skill and Claude-plugin ZIP files. A maintainer reviews the draft before publishing. No npm publication or automatic source-version commit is required.

Release drafts and published assets belong to [Rhyru9/bug-solver-pro releases](https://github.com/Rhyru9/bug-solver-pro/releases). The workflow derives its repository from the GitHub event so it does not hardcode credentials or a separate publication destination.

Build the same artifacts locally without publishing:

```bash
python -B scripts/build_release.py --output-dir dist
```

The release workflow requires an existing tag matching the plugin version and uses the repository's GitHub token to create the draft. Test workflows use read-only repository permissions. Hosted CI and release behavior can only be confirmed after the repository is pushed and the corresponding events run.
