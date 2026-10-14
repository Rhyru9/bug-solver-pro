# Flask: debugging playbook

Deeper case: [Two successful requests lose one session update](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Worker raises Working outside of request context

**Mechanism:** request and related proxies resolve within the current context; passing the proxy does not snapshot its data.

**Probe and falsifier:** Compare copied primitive inputs with a captured request proxy in an isolated job. If both fail before access, inspect the worker setup instead.

**Repair and verify:** Extract required validated values before scheduling; give the job its own application/resource scope. Do not keep a request context alive indefinitely. Verify request completion before job execution. [Official contract](https://flask.palletsprojects.com/en/stable/reqcontext/).

## 2. Tests contaminate each other across app factories

**Mechanism:** An extension bound at import time or app-specific state stored globally can keep the first application's configuration.

**Probe and falsifier:** Create two apps with distinct nonsecret sentinel settings in one process; observe the extension and operation configuration. Correct isolation rejects this cause.

**Repair and verify:** Keep extension setup unbound until init_app(app), and obtain app-specific configuration through the active app. Verify both app creation orders. [Official contract](https://flask.palletsprojects.com/en/stable/patterns/appfactories/).

## 3. Teardown crashes before the intended error is reported

**Mechanism:** Teardown can run even when request setup failed; cleanup that assumes successful initialization raises a second exception.

**Probe and falsifier:** Fail before acquisition, after acquisition, and during the view. Observe which exception survives. Correct cleanup in all cases rejects this mechanism.

**Repair and verify:** Make teardown conditional on resources actually acquired and safe on partial setup. Preserve the original exception; verify closure exactly once. [Official contract](https://flask.palletsprojects.com/en/stable/reqcontext/).
