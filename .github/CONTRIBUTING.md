# Contributing to bug-solver-pro

Project repository: [Rhyru9/bug-solver-pro](https://github.com/Rhyru9/bug-solver-pro). Use its [issue tracker](https://github.com/Rhyru9/bug-solver-pro/issues) and [pull requests](https://github.com/Rhyru9/bug-solver-pro/pulls). Public installation is documented in the [README](https://github.com/Rhyru9/bug-solver-pro#install-from-github).

For source development after publication:

```bash
git clone https://github.com/Rhyru9/bug-solver-pro.git
cd bug-solver-pro
```

Canonical skill resources live in `skills/bug-solver-pro/`. Claude plugin metadata lives in `.claude-plugin/`. Tests and repository tooling live in `tests/` and `scripts/`; neither requires third-party Python packages.

Report broken behavior with the bug template. Use the diagnostic-gap template for unrecorded mechanisms, misleading search results or missing observation angles. Include sanitized inputs, versions, expected/actual behavior and traceable evidence. Keep unrelated production actions outside reproduction work.

Catalog seeds remain heuristics. Each added pattern needs a candidate mechanism, discriminator, falsifying result, verification, limits and local source references. Add positive paraphrases and confusing or unrelated queries to retrieval tests. Keep genuinely reproduced lessons separate from hypothetical mechanisms. Do not make the catalog a required ceiling on investigation.

Before submitting a change, run:

```bash
python -B scripts/check_package.py
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
