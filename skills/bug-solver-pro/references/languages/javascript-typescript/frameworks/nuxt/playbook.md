# Nuxt: debugging playbook

Deeper case: [Authenticated API works in the browser but fails during SSR](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. SSR page fetches the same data again during hydration

**Mechanism:** A direct $fetch in component setup does not itself transfer the result as Nuxt async-data payload for hydration reuse.

**Probe and falsifier:** Count server and browser calls for a cold direct load; compare useFetch/useAsyncData. Identical duplicate calls after payload reuse reject this explanation.

**Repair and verify:** Use the appropriate payload-aware composable for page data and return defined data from its handler. Verify SSR, hydration, and navigation; duplicate reads do not justify making mutations run on mount. [Official contract](https://raw.githubusercontent.com/nuxt/nuxt/main/docs/1.getting-started/10.data-fetching.md).

## 2. Two components display each other's async data

**Mechanism:** Calls sharing an async-data key share the associated state; a constant key can accidentally join distinct resources.

**Probe and falsifier:** Inspect keys and result identities while loading two resource IDs. Distinct keys with independent state reject this cause.

**Repair and verify:** Choose keys that encode the intended resource identity and keep shared-key options consistent. Verify navigation between IDs and legitimate sharing; do not insert secrets into keys. [Official contract](https://raw.githubusercontent.com/nuxt/nuxt/main/docs/1.getting-started/10.data-fetching.md).

## 3. One SSR visitor observes another visitor's state

**Mechanism:** A module-level ref on the server can live across requests instead of belonging to one render/request.

**Probe and falsifier:** Interleave two synthetic visitors in the same server process and trace state initialization. No shared mutation rejects this candidate.

**Repair and verify:** Move request state into useState with an appropriate key or request-owned state. Keep its payload serializable. Verify isolation through SSR and hydration; process-local state is not durable shared storage. [Official contract](https://raw.githubusercontent.com/nuxt/nuxt/main/docs/1.getting-started/11.state-management.md).
