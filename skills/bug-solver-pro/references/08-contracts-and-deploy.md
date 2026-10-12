# 08. Contracts, Integrations, and Staged Deployment

A contract is any promise to another party: API, event, webhook, DB schema, file format, error code, or side-effect ordering.

## Compatibility principles
- Choose compatible transitions based on actual consumers. Optional fields can still break strict parsers/schemas or signatures. Test required version combinations.
- Validate according to contracts and trust boundaries. Ignore unknown fields only when permitted; compatibility tolerance does not justify ambiguous/dangerous input.
- **Do not change a field's meaning**, such as changing `amount` from rupiah to cents. Introduce a new field.
- **Error codes and HTTP statuses** are contracts; changing them breaks clients that handle them.
- Array/result **ordering** is an implicit contract; do not change it accidentally.
- **Defaults** are contracts: changing a default changes behavior for every consumer that omits it.

## Before changing APIs/events
- [ ] Who consumes them (frontend, old mobile versions, other services, partners, BI)? Inspect access logs/metrics, not only text searches.
- [ ] Do old clients work with new responses?
- [ ] Do new servers still accept old clients' requests?
- [ ] Are OpenAPI/docs/schemas/SDKs updated?
- [ ] Are contract/consumer-driven tests available? If not, add at least one for the changed shape.
- [ ] Is a new API version or flag needed?

## Rolling deployment and coexisting versions

Old/new code may run together against the same DB. Ensure:
- New code reads old code's writes, and **old code reads new code's writes**.
- Old queued messages remain processable; old workers do not crash on new messages.
- Schema migrations support code **before and after** deployment.
- Sequence: expand schema → deploy compatible code → backfill → switch → contract.

## Feature flags and rollout
- Use flags/staged rollout when they reduce risk; choose defaults based on invariants and mitigation needs, not always off.
- Roll out by percentage/tenant while monitoring metrics.
- Prepare rollback paths that do not require reverse migrations.
- Remove flags after stabilization to avoid confusing dead branches.

## External integrations
- Assume calls can be slow, fail, or return unexpected data.
- Use explicit timeouts; backoff retries for transient failures; **idempotency keys** for operations with effects.
- Validate response types/required fields before using them.
- Incoming webhooks: verify according to protocol, handle replay/redelivery/ordering; acknowledge only after reaching the promised receipt/processing durability point.
- Outgoing webhooks/events: payload versions, retries, audit trails.
- Log and alert on failures; investigate silent failures hidden by success metrics.

## Cross-service consistency
- Do not assume local transactions protect other services. Specify coordination protocols and guarantees: outbox, idempotency, compensation, genuinely supported distributed transactions, or reconciliation as appropriate.
- Establish authoritative sources for each value; other services maintain copies under explicit synchronization rules.
- Reconciliation: jobs comparing both sides and reporting/repairing differences.

## Documentation and communication
- Update API documentation/changelogs alongside code.
- Prepare consumer impact notes and migration paths; sending messages follows session authorization.
