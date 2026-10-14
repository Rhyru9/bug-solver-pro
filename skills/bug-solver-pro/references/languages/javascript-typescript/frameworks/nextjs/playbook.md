# Next.js: debugging playbook

Deeper case: [A hidden button still allows a server-side mutation](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. router.refresh still shows old data

**Mechanism:** In the App Router caching model, refreshing the router does not itself invalidate every server-side data cache.

**Probe and falsifier:** In an isolated reproduction, compare database value, server fetch result, and RSC output before/after refresh and targeted invalidation. A fresh server value rejects server-data-cache staleness.

**Repair and verify:** Invalidate the owning path/tag or select the intended fetch policy using the installed Next version and cacheComponents mode. Verify mutation, refresh, and client navigation; avoid globally disabling caching. [Official contract](https://nextjs.org/docs/app/deep-dive/caching).

## 2. Successful mutation ends as an error instead of redirecting

**Mechanism:** redirect() uses framework control flow by throwing; a surrounding catch can intercept it.

**Probe and falsifier:** Move only redirect outside the local mutation catch in a reproduction. If the same error persists, inspect the actual mutation failure.

**Repair and verify:** Catch mutation failures narrowly and redirect after the catch. Verify failed mutations remain errors and successful ones navigate once; do not swallow all thrown values. [Official contract](https://nextjs.org/docs/app/api-reference/functions/redirect).

## 3. Hydration mismatch appears only on direct load

**Mechanism:** Server and first client render may disagree on time, locale, browser-only state, or HTML nesting.

**Probe and falsifier:** Compare serialized server inputs with the first client render before effects. A matching initial tree rejects this mechanism.

**Repair and verify:** Render deterministic initial content, then read browser-only values after hydration where appropriate. Fix invalid nesting. Verify direct load and navigation; suppressHydrationWarning only hides a narrow warning. [Official contract](https://nextjs.org/docs/messages/react-hydration-error).
