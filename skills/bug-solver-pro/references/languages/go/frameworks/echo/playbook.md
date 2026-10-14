# Echo: debugging playbook

Deeper case: [Client disconnects but downstream calls keep consuming resources](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. A goroutine reads the wrong request or races

**Mechanism:** Echo request contexts have a request-owned lifetime and must not be concurrently accessed as arbitrary shared state.

**Probe and falsifier:** Delay worker execution past handler completion and run overlapping requests under the race detector. If only copied values are used, inspect another shared object.

**Repair and verify:** Extract immutable inputs before spawning; keep response writes in the handler and give work a deliberate cancellation/lifetime policy. Verify cancellation and repeated requests. Respect Echo v4/v5 API differences. [Official contract](https://echo.labstack.com/guide/context/).

## 2. Body input replaces an authoritative route ID

**Mechanism:** Multi-source binding can overwrite earlier path/query values with body fields.

**Probe and falsifier:** Send a request whose path ID differs from its JSON ID; inspect the bound DTO before authorization and persistence. A preserved path identity rejects this binding cause.

**Repair and verify:** Separate path identity from body DTO and explicitly map allowed fields. Verify conflicting inputs, authorization, and valid updates; do not let binding select the operation's authority. [Official contract](https://echo.labstack.com/guide/binding/).

## 3. Client can set an internal field despite validation passing

**Mechanism:** Binding a persistence/domain struct can expose writable fields not intended in the public input contract.

**Probe and falsifier:** In an isolated handler test, submit an extra internal flag and inspect bound versus persisted state. If it is never writable, inspect another path.

**Repair and verify:** Use a dedicated request DTO and explicit mapping to server-owned fields; validation alone is not an allowlist. Verify unexpected fields cannot change internal state. [Official contract](https://echo.labstack.com/guide/binding/).
