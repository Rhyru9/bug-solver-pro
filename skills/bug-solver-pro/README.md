# bug-solver-pro

Use this skill to investigate backend and application logic failures, explain their mechanism, and verify a targeted repair. Start at [SKILL.md](SKILL.md). Installation and host compatibility are documented in the [repository README](https://github.com/Rhyru9/bug-solver-pro) and [compatibility guide](https://github.com/Rhyru9/bug-solver-pro/blob/main/COMPATIBILITY.md).

A useful investigation follows the reported operation through its real entrypoint and state changes, finds the first broken invariant, and runs a probe that distinguishes the suspected cause from alternatives. A non-failing probe is inconclusive if it never activated the mechanism or could not observe the failure. Read the [causal decision procedure](references/19-causal-decision-procedure.md) when that distinction affects the fix.

For a known stack, open the [framework index](references/frameworks/index.md). Its 22 modules contain 66 base recipes and 22 deeper boundary cases, with mechanisms, local probes, repair tradeoffs, and supporting official contracts. Use [composed failures](references/20-composed-failures.md) when retry, cache, transaction, lifecycle, or resource guarantees interact. For unfamiliar stacks, inspect the actual version and execution path using [stack semantics](references/14-stack-semantics.md).

The optional `scripts/search.py` requires Python 3.9+ with no external packages. It searches 54 shared heuristic patterns and 88 indexed framework techniques. `--framework <name>` scopes recipe leads and includes local working knowledge; `--plan` adds candidate experiments; `--explore` provides 20 observation angles. Run it through its installed absolute path. [Structured tooling](references/17-structured-tooling.md) documents the output and data contracts.

The [coverage audit](references/coverage/gap-audit.md) and [data audit](references/coverage/data-audit.md) distinguish implemented guidance, tested tooling, bounded runtime fixtures, and remaining limits. The local FastAPI and SQLite probes are synthetic checks. Catalog matches and recipe counts do not establish a production diagnosis or general agent effectiveness.

To extend coverage, use the [module template](templates/stack-module.md), preserve a single Markdown source for each technique, and update its retrieval index. Update learned cases only when skill maintenance is authorized. Report issues in the [repository tracker](https://github.com/Rhyru9/bug-solver-pro/issues).
