# 20. Diagnose failures that cross mechanisms

Use when each component passes alone, one fix exposes another symptom, or a retry/cache/transaction boundary joins otherwise reasonable behavior. Start with [causal decision gates](19-causal-decision-procedure.md). The examples below are synthetic reasoning cases, not framework runtime reproductions.

## Find the guarantee that fails in composition

Draw only the implicated flow: producer → transformation/validation → state transition → commit → publication → acknowledgement → consumer/read model. Mark owners, IDs, versions, retry/cancel boundaries and resources held. A component promise applies only within its stated scope: per render is not per user action; per process is not per cluster; after commit is not durable publication.

## Use a controlled interaction matrix

For two suspected factors A and B, reset equivalent initial state and compare neither, A alone, B alone, and A+B where safe. Record actual activation and the same failure signature. If only A+B fails, investigate their shared boundary; neither component is thereby proven defective. If both single-factor cases fail, the model may contain separate causes. If the trigger vanishes, check that reduction did not remove the relevant path.

### Case 1: retry plus ambiguous commit

Synthetic trace: attempt 1 commits operation O, its reply is lost, attempt 2 commits O again. Two user-visible effects follow one action. Candidate explanations include duplicate UI submission and downstream retry.

Count submissions, attempts, commits and effect IDs. One submission, two attempts and two commits supports downstream multiplicity; two submissions require tracing one boundary earlier. Force “commit then lost reply” in a local test instead of merely timing out before the operation starts.

A durable operation key enforced atomically with the protected transition can close the demonstrated duplicate path. A dedupe flag written after the effect leaves a crash window. Cancellation does not establish failure, and a client abort does not undo an already committed write. Verify concurrent retries and distinct legitimate operations. See [concurrency](06-concurrency-transactions.md).

### Case 2: repaired proxy call plus pool exhaustion

An internal Spring call bypasses REQUIRES_NEW advice. Moving it to an injected bean restores the intended independent boundary; under load, outer transactions now hold connections while inner transactions wait for additional ones.

The original repair and new stall can both be real. Compare transaction identities, connection holders and waiters before assuming the proxy repair was wrong. Do not “fix” the stall by silently restoring the bypass. Check the independent-commit requirement, admission and database budget together. Use the [Spring boundary case](languages/java/frameworks/spring/boundary-case.md) and [playbook](languages/java/frameworks/spring/playbook.md); their official sources support the framework mechanics.

### Case 3: request authentication plus shared cached output

Synthetic trace: actor A passes authorization and fills a cache keyed only by document ID. Actor B requests the same ID and receives that cached personalized projection before the intended resource decision.

Swap actors while keeping the document fixed, then swap documents while keeping the actor fixed. Observe effective decision, cache key and response owner at the same boundary. A correct endpoint guard does not prove an earlier cache hit is scoped correctly; a shared public representation may be legitimate, so establish the contract first.

Place access decisions and cache identity according to representation ownership. Validate actor/resource variants, cache hit/miss, invalidation and signed-out requests in isolated fixtures. Disabling the whole cache can localize the interaction while changing timing; it is not a complete diagnosis or automatically the right repair.

### Case 4: correct SQL plus a reused ORM context

Synthetic trace: a previous query tracks entity E. A later filtered query emits correct SQL but its navigation graph still contains E. Rewriting the SQL filter does not address tracking/fixup and can change valid results.

Keep rows fixed; compare raw result membership, managed graph and a fresh/no-tracking read. If divergence first appears after materialization, investigate tracking. If wrong rows are already in SQL, fix the predicate first. See [EF Core boundary case](languages/csharp/frameworks/aspnet-core/boundary-case.md). Do not clear a context containing pending edits just to get a clean read.

### Case 5: resource cleanup plus response completion

A request finishes and disposes its session while a stream or background job still borrows it. Moving cleanup later can conceal leaks; copying a request object does not transfer ownership of its session, body stream or writer.

Record acquire → last legitimate use → response/worker completion → release with resource IDs. Force completion order with local barriers. Choose an owner whose lifetime covers actual work and test error/disconnect exits. Background work may need its own resource scope and immutable identifiers rather than a borrowed request resource.

## Make the repair close the boundary

State what remains atomic, scoped, ordered or bounded after the fix. Separate code repair from recovery of old corrupted rows/effects. Verify both component behavior and the demonstrated interaction; a four-cell synthetic matrix does not prove every deployment, adapter or schedule safe. For unmodeled mechanisms, return to the first violated invariant rather than adding speculative patches.
