# Symfony debugging

For a deeper boundary case, read [Repository read appears to prove a write that never reached the database](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

## Establish configuration and entrypoints

Inspect Symfony/PHP versions, kernel/environment, compiled container, event subscribers, and Messenger transports. Match the executing artifact and entrypoint with the reproduction/test environment.

## Boundary and lifecycle questions

- Which controller, argument resolver, validator, security rule, and event subscriber run on this path? Does a command or worker bypass them?
- Does a shared service retain operation-specific state? Which transaction boundary surrounds a message, and can retries repeat external effects?

## Distinguishing experiment

Compare the failing HTTP/console/message entrypoint with a healthy path; record service identity, event order, database commit, message acknowledgement, and retry effects.

Before the experiment, state the predicted observation and a result that rejects the candidate mechanism. Keep effects isolated from production systems.

## Verification and limits

Verify the original trigger, healthy neighboring behavior, and implicated error/cleanup paths through the real framework boundary. Use matching providers, features, and worker/build modes where they affect the mechanism. Passing a direct function test does not verify framework wiring. Record evidence and untested boundaries; these questions do not establish a diagnosis.
