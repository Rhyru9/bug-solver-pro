# Nuxt: Authenticated API works in the browser but fails during SSR

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** A server-side $fetch does not automatically inherit the browser's request credentials. The first server render and subsequent browser request can reach the same API with different identities.

**Discriminating probe:** Using synthetic actors, compare credential-presence markers and effective actor IDs at the internal API for SSR and client navigation. Missing SSR context supports forwarding failure. Identical validated identities with divergent data refute this explanation; logging raw cookies is unnecessary.

**Repair, verification, and trap:** For intended internal relative requests, use the request-aware fetch/composable supported by the installed Nuxt version, or explicitly forward only the needed headers to a trusted target. Verify SSR, navigation, signed-out state, and two users. Never forward the entire inbound header set to an arbitrary external URL. [Official contract](https://raw.githubusercontent.com/nuxt/nuxt/main/docs/1.getting-started/10.data-fetching.md).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
