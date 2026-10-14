# Hono: debugging playbook

Deeper case: [Validator works but a later raw Request read fails](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. After-middleware sees an unfinished response

**Mechanism:** Calling next() without await lets post-processing run before downstream completion.

**Probe and falsifier:** Use a delayed handler and record middleware entry/exit plus response status. Correct nested order rejects missing await.

**Repair and verify:** Await next() before response-dependent work and return explicit responses for short-circuits. Verify both successful and failed downstream execution. [Official contract](https://hono.dev/docs/guides/middleware).

## 2. Headers disappear after middleware rewrites the body

**Mechanism:** Replacing c.res with a fresh Response can discard headers/status from downstream or previous middleware.

**Probe and falsifier:** Record response headers immediately after downstream work and after each replacement. If they never existed, inspect earlier middleware.

**Repair and verify:** Preserve the intended status and headers when replacing the response or use supported response mutation helpers. Verify cookies, CORS, and error headers after the complete chain. [Official contract](https://hono.dev/docs/guides/middleware).

## 3. Typed context variable is undefined at runtime

**Mechanism:** Declaring Variables in Hono's type parameter does not execute the c.set middleware that supplies a value.

**Probe and falsifier:** Invoke both the intended route group and the failing route; record whether the setter ran. A populated value before use rejects missing registration.

**Repair and verify:** Attach the supplying middleware to every intended route with correct order/scope and use request-local c.set/c.get. Verify missing-auth rejection and concurrent requests; a type assertion cannot repair runtime wiring. [Official contract](https://hono.dev/docs/api/context).

## Small implementation pattern

Adapt identifiers and imports to the existing project. This illustrates the relevant boundary; it is not a standalone application or an incident reproduction.

```ts
app.use('*', async (c, next) => {
  await next(); // post-processing must wait for downstream completion
  c.header('X-Trace-Stage', 'complete');
});
```
