---
name: replica-validator
description: Compare an original game project with its replica and decide whether build, parameters, mechanics, inputs, events, assets, animations, and runtime behavior pass.
metadata:
  short-description: Validate replica completion
---

# Replica Validator

Use this as the final gate in the `game-replica` workflow. It decides whether the replica is complete.

Do not lower validation standards, skip failed checks, or modify locked files to make the result pass.

## Required Inputs

Read:

```text
Original Project
Replica Project
replication/SOURCE_SPEC.md
replication/ARCHITECTURE.md
replication/PARAMETER_LOCK.json
replication/SYMBOL_MAP.json
replication/ASSET_MANIFEST.json
replication/CODE_REPLICA_REPORT.md
replication/ASSET_RESTYLE_REPORT.md
```

If a core input is missing, report `REPLICATION INCOMPLETE` and route back to the appropriate phase.

## Validation Pipeline

1. Framework validation.
2. Build validation.
3. Structure validation.
4. Parameter validation; read [../../references/parameter-rules.md](../../references/parameter-rules.md).
5. Function validation using `SYMBOL_MAP.json`.
6. Event validation.
7. Input validation.
8. Asset validation; read [../../references/asset-rules.md](../../references/asset-rules.md).
9. Animation validation.
10. Runtime validation.
11. Critical behavior validation.
12. Final report.

Read [../../references/validation-rules.md](../../references/validation-rules.md) before assigning severity or final status.

## Helpful Scripts

Use these when appropriate:

```text
python scripts/compare-parameters.py <original-lock.json> <replica-lock.json>
python scripts/compare-assets.py <original-assets.json> <replica-assets.json>
python scripts/validate-build.py <project-root>
```

## Report

Write:

```text
replication/REPLICATION_REPORT.md
```

The final status must be exactly one of:

```text
REPLICATION COMPLETE
REPLICATION INCOMPLETE
```

Only use `REPLICATION COMPLETE` when build, runtime, locked parameters, critical behavior, and asset validation pass with no unresolved `CRITICAL` or `HIGH` differences.
