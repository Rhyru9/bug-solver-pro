# NestJS: debugging playbook

Deeper case: [ValidationPipe is installed but malformed DTOs still pass](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. One provider unexpectedly has multiple instances

**Mechanism:** Declaring the same provider in several modules can create separate instances instead of reusing an exported provider.

**Probe and falsifier:** Add a temporary constructor instance ID; resolve the service through both consumers. Equal IDs reject this explanation.

**Repair and verify:** Register in its owning module, export it, and import that module in consumers. Avoid adding forwardRef to conceal duplicate registrations. Verify both paths share state only where intended. [Official contract](https://docs.nestjs.com/faq/common-errors).

## 2. Request state leaks or construction count explodes

**Mechanism:** Default singleton providers retain fields; request-scoped dependencies can cause dependent providers to become request-scoped.

**Probe and falsifier:** Trace constructor IDs and a synthetic request marker across overlapping requests. Stable isolation and expected construction counts reject this cause.

**Repair and verify:** Keep operation state in parameters or intentionally scoped context. Choose request scope only for dependencies needing it; verify concurrent isolation and construction cost. [Official contract](https://docs.nestjs.com/fundamentals/injection-scopes).

## 3. Dependency is undefined despite a visible import

**Mechanism:** A circular file/barrel import can make a runtime token unavailable; type-only imports also cannot supply a runtime provider token.

**Probe and falsifier:** Inspect the failing dependency index/token and replace the implicated barrel import with a direct import in a local reproduction. If the token is unchanged, inspect module exports.

**Repair and verify:** Separate shared tokens/constants from cyclic imports; use explicit injection tokens for interfaces. Use forwardRef only for a demonstrated provider cycle. Verify boot and actual resolution. [Official contract](https://docs.nestjs.com/faq/common-errors).
