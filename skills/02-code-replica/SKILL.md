---
name: code-replica
description: Rewrite game code from source-analysis artifacts while preserving framework, mechanics, parameters, state transitions, inputs, events, and runtime behavior.
metadata:
  short-description: Rewrite code with behavior preserved
---

# Code Replica

Use this phase after `source-analyzer` has produced the required `replication/` artifacts.

The goal is functional equivalence, not textual copying. Names and internal organization may change, but behavior, parameters, dependencies, and runtime semantics must remain aligned with the source specification.

## Required Inputs

Read:

```text
replication/SOURCE_SPEC.md
replication/ARCHITECTURE.md
replication/PARAMETER_LOCK.json
replication/SYMBOL_MAP.json
replication/REPLICATION_PLAN.md
```

If any input is missing or too incomplete to guide implementation, stop and route back to `source-analyzer`.

## Output Location

Do not modify the original project source. Create or use a sibling replica workspace named:

```text
<original-folder-name>_replace
```

Example:

```text
D:\games\bird-runner
D:\games\bird-runner_replace
```

All code changes, asset replacements, build fixes, and generated `replication/` reports for the replica should happen inside the `_replace` workspace. Keep the original project available as read-only comparison input.

The replica workspace should preserve the original file layout wherever practical:

```text
Original: src/main.ts
Replica:  src/main.ts

Original: assets/ui/start.png
Replica:  assets/ui/start.png
```

If a path or layout must change, document the reason in `replication/CODE_REPLICA_REPORT.md` and ensure `replica-validator` checks the difference.

## Core Rules

* Preserve the original framework, language, build system, runtime platform, and dependency semantics. Read [../../references/framework-rules.md](../../references/framework-rules.md) when framework or build choices are unclear.
* Preserve all locked parameters. Read [../../references/parameter-rules.md](../../references/parameter-rules.md) before changing constants or config values.
* Preserve input mappings, event order, state transitions, calculations, timing, collision behavior, animation behavior, scoring, damage, health, spawn/despawn logic, win conditions, and lose conditions.
* Do not add mechanics, remove features, rebalance numbers, or migrate frameworks unless the user explicitly requests that difference.
* If symbols are renamed, update `replication/SYMBOL_MAP.json`.

## Implementation Strategy

Implement module by module in the order suggested by `REPLICATION_PLAN.md`, typically:

```text
Entry → Configuration → Runtime → State → Player → Enemy → Level
→ Physics → UI → Audio → Input → Assets → Save/Data
```

After each significant module, run the closest available build, type check, or smoke test. Do not wait until the end for the first build.

When creating the initial replica workspace, use this helper when appropriate:

```text
python scripts/create-replica-workspace.py <original-project-root>
```

## Report

Write:

```text
replication/CODE_REPLICA_REPORT.md
```

Include implemented modules, renamed symbols, preserved parameters, preserved functions, known differences, build result, and remaining issues.

## Completion Gate

Continue to `asset-restyle` only when the `_replace` workspace exists, original source files remain unmodified, necessary modules are implemented, locked parameters are preserved, symbol mappings are updated, a build or type check has run, known differences are recorded, and `CODE_REPLICA_REPORT.md` exists.
