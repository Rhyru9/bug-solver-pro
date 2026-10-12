# bug-solver-pro

Source and installation guide: [Rhyru9/bug-solver-pro](https://github.com/Rhyru9/bug-solver-pro). Once published, install from your destination project with `npx skills add Rhyru9/bug-solver-pro --skill bug-solver-pro`; add `--global` for user-level installation. Report skill or tooling problems in the [issue tracker](https://github.com/Rhyru9/bug-solver-pro/issues).

A debugging framework across languages, frameworks, and libraries. Start with [SKILL.md](SKILL.md); open references according to the question under investigation.

The skill guides invariant/flow mapping, discovery of actual stack semantics, causal experiments, impact analysis, and risk-proportional verification. Small bugs need brief notes; state, concurrency, and cross-service problems require evidence at relevant boundaries.

[14-stack-semantics](references/14-stack-semantics.md) supports unfamiliar stacks. [15-evidence-and-experiments](references/15-evidence-and-experiments.md) covers experiment selection, intermittent failures, crashes, performance, and incidents without reproduction.

Templates and shell helpers are optional; the skill can be used without Git, a shell, or internet access when evidence limits are stated. Update learned cases only when skill maintenance is authorized.

The optional Python tooling searches 48 structured heuristic patterns across eleven diagnostic domains, with experiments and falsifying observations. Run `scripts/search.py` through the installed skill's absolute path; use `--plan` for investigation guidance, `--explore` for fourteen open-world observation angles, or `--json` for machine-readable output. Requires Python 3.9+ with no external packages. See [structured tooling](references/17-structured-tooling.md) for query interpretation and [coverage and unknowns](references/18-coverage-and-unknowns.md) for unrecorded bugs. Search matches are leads, never verified causes.
