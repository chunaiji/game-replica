---
name: source-analyzer
description: Analyze an original game source project and produce the technical, behavioral, parameter, symbol, asset, and replication-plan artifacts required before rewriting.
metadata:
  short-description: Analyze source before replication
---

# Source Analyzer

Use this phase first in the `game-replica` workflow. It builds the specification that later phases must preserve.

Do not modify the original project in this phase. Do not begin substantial rewriting until all required analysis artifacts exist.

## Inputs

Read the original game source, including code, configs, build files, assets, scene files, level data, and dependency manifests.

## Required Outputs

Write these files under `replication/`:

```text
SOURCE_SPEC.md
ARCHITECTURE.md
PARAMETER_LOCK.json
SYMBOL_MAP.json
ASSET_MANIFEST.json
REPLICATION_PLAN.md
```

## Analysis Order

1. Detect framework, language, version, build tool, package manager, entry point, runtime, and target platform.
2. Scan the directory structure and identify generated, vendor, source, config, and asset areas.
3. Analyze modules, classes, functions, lifecycle hooks, and update order.
4. Analyze game loop, state machines, inputs, events, UI, audio, physics, AI, animations, scenes, and levels.
5. Extract gameplay parameters into `PARAMETER_LOCK.json`; read [../../references/parameter-rules.md](../../references/parameter-rules.md) when deciding what to lock.
6. Build `SYMBOL_MAP.json` for original symbols and semantic roles.
7. Build `ASSET_MANIFEST.json`; read [../../references/asset-rules.md](../../references/asset-rules.md) when scanning visual assets, atlases, Sprite Sheets, and alpha requirements.
8. Write `REPLICATION_PLAN.md` with module-by-module rewrite and validation guidance.

## Helpful Scripts

Use these when appropriate:

```text
python scripts/scan-project.py <project-root> --out replication/SOURCE_SCAN.json
python scripts/extract-parameters.py <project-root> --out replication/PARAMETER_LOCK.json
python scripts/asset-manifest.py <project-root> --out replication/ASSET_MANIFEST.json
```

Script output must be reviewed and completed by source reading.

## Completion Gate

This phase is complete only when all required output files exist, the framework and entry point are identified, core parameters are locked, core resources are listed, and critical behavior is described well enough for another phase to implement and validate it.
