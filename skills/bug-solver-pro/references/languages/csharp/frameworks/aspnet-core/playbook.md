# ASP.NET Core: debugging playbook

Deeper case: [Filtered Include returns entities outside the filter](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Background work fails after the response

**Mechanism:** Fire-and-forget work captured a request-scoped service/HttpContext that has been disposed or reused.

**Probe and falsifier:** Delay the work until after response completion; record scope disposal and service identity. A separately owned live scope rejects this cause.

**Repair and verify:** Pass immutable inputs to an owned background queue/service and create its own scope. Avoid async void and capturing HttpContext. Verify errors remain observed after the request ends. [Official contract](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices).

## 2. Parallel queries report a second operation on DbContext

**Mechanism:** EF Core DbContext is not safe for parallel operations; Task.WhenAll can overlap work on one instance.

**Probe and falsifier:** Record context identity and overlapping operation intervals. Distinct contexts with no overlap reject this explanation.

**Repair and verify:** Await operations serially or create independently owned contexts for truly independent work. Preserve transaction semantics; splitting contexts can change atomicity. Verify concurrency and cleanup with the real provider. [Official contract](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/).

## 3. Error middleware cannot change status or headers

**Mechanism:** The response may already have started, often through a stream or earlier write.

**Probe and falsifier:** Record Response.HasStarted before error formatting and identify the first write. A false value at the failure boundary rejects early commitment.

**Repair and verify:** Choose one response owner and handle errors before starting output where possible. After start, use the appropriate abort/stream protocol; verify pre-write and mid-stream failures. [Official contract](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices).
