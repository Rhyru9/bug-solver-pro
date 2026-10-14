# Next.js: A hidden button still allows a server-side mutation

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** A Server Action/server function is an independently reachable server entrypoint. Hiding UI or checking access only in a layout does not enforce authorization at the mutation's owner.

**Discriminating probe:** Using isolated fixtures, invoke the actual action as allowed, denied, and allowed-for-a-different-resource actors. Observe effective actor/resource immediately before persistence and assert no denied effect. A validated server-side resource decision on every path rejects this bypass; a browser-only test cannot.

**Repair, verification, and trap:** Validate untrusted action arguments and perform authentication plus resource authorization at the server operation boundary. Revalidate relevant data only after a permitted mutation. Verify direct action invocation, session changes, and resource substitution; do not trust captured client values as authority. [Official contract](https://nextjs.org/docs/app/guides/data-security).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
