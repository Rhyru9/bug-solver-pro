# FastAPI: debugging playbook

Deeper case: [A supposedly filtered response exposes extra fields on one route](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. One async endpoint stalls unrelated requests

**Mechanism:** A blocking helper called inside async def runs directly; FastAPI does not automatically offload ordinary helper calls.

**Probe and falsifier:** Run a slow request alongside a lightweight endpoint in an isolated worker. Compare with a nonblocking/offloaded implementation. No scheduling delay weakens this explanation.

**Repair and verify:** Use the async client or explicitly offload blocking I/O; a sync endpoint can fit sync I/O. CPU work may need process/task isolation. Verify concurrent latency, not just single-request speed. [Official contract](https://fastapi.tiangolo.com/async/).

## 2. Errors disappear in a yield dependency

**Mechanism:** A dependency that catches an exception after yield and does not re-raise can hide the error from the framework.

**Probe and falsifier:** Inject a sentinel failure into the endpoint; compare propagation with and without the dependency catch. Preserved propagation rejects swallowing here.

**Repair and verify:** Do cleanup in finally and re-raise unless deliberately translating to a defined exception. Verify status, logs, and resource closure on failure. [Official contract](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/).

## 3. Stream or background job uses a closed session

**Mechanism:** yield-dependency cleanup timing is version/scope-sensitive; response work may outlive the resource it borrows.

**Probe and falsifier:** Trace session open/close, stream consumption, and background execution under the installed version and dependency scope. If lifetime covers use, investigate sharing/concurrency.

**Repair and verify:** Give background work its own resource lifetime and pass identifiers rather than request sessions. Ensure streaming resources survive consumption. Verify client disconnect and cleanup without changing scopes blindly. [Official contract](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/).
