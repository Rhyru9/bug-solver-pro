# NestJS: ValidationPipe is installed but malformed DTOs still pass

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** TypeScript interfaces, generics, and type-only imports do not necessarily provide concrete runtime DTO metadata for class-based validation. A direct service test also bypasses controller pipes.

**Discriminating probe:** Send a field violating a real class-validator constraint through the actual transport; inspect the metatype and whether the pipe runs. A runtime class plus the expected rejection refutes missing metadata for that route. Testing only a valid DTO cannot distinguish anything.

**Repair, verification, and trap:** Use the concrete decorated DTO class as a runtime import and register the intended pipe at the real boundary. Choose transform/whitelist behavior deliberately; neither replaces domain authorization. Verify malformed, extra, and valid fields through HTTP or the actual non-HTTP transport. [Official contract](https://docs.nestjs.com/techniques/validation).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
