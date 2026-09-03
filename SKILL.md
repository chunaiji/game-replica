---
name: game-replica
description: Analyze, rewrite, restyle, and validate an existing game project as a behavior-preserving replica when the user has rights to the source.
metadata:
  short-description: Behavior-preserving game replica workflow
---

# Game Replica

Use this skill when the user wants to replicate, refactor, restyle, or rebuild an existing game while preserving its framework, mechanics, parameters, resources, and runtime behavior.

Only use it when the user provides source code or clearly has permission to modify or reproduce the project. Do not use it to copy a game from screenshots, storefront pages, videos, or inaccessible proprietary code.

## Workflow

Run the phases in order:

```text
01 source-analyzer
    ↓
02 code-replica
    ↓
03 asset-restyle
    ↓
04 replica-validator
```

Do not skip gates:

* Do not rewrite code before the source analysis outputs exist.
* Do not change gameplay parameters before `replication/PARAMETER_LOCK.json` exists.
* Do not replace assets before `replication/ASSET_MANIFEST.json` exists.
* Do not modify original source files. Create the replica in a sibling directory named `<original-folder-name>_replace` unless the user explicitly chooses another output path.
* Preserve the original project's file and directory layout inside the replica workspace, including source, config, asset, scene, and build-entry paths.
* Do not change asset dimensions, aspect ratios, formats, alpha requirements, or Sprite Sheet layouts unless the user explicitly requests that difference.
* Do not claim completion until validation produces `REPLICATION COMPLETE`.

## Replica Workspace

Before Phase 02 changes code or assets, create a separate replica workspace next to the original project:

```text
<parent>/
├── <original-folder-name>/
└── <original-folder-name>_replace/
```

All implementation, asset replacement, build, and validation work should happen in `<original-folder-name>_replace/`. Treat the original project as read-only analysis input after the workspace is created.

The replica workspace must keep the same project layout as the original wherever practical:

```text
Original: <original>/src/player/PlayerController.ts
Replica:  <original>_replace/src/player/PlayerController.ts

Original: <original>/assets/player_idle.png
Replica:  <original>_replace/assets/player_idle.png
```

Only change paths or layout when the user explicitly requests it or when the original project cannot build without a documented adjustment. Record any such difference in `replication/REPLICATION_REPORT.md`.

## Phase Routing

For source discovery and specification, follow [skills/01-source-analyzer/SKILL.md](skills/01-source-analyzer/SKILL.md).

For code rewriting, follow [skills/02-code-replica/SKILL.md](skills/02-code-replica/SKILL.md).

For visual resource replacement or style unification, follow [skills/03-asset-restyle/SKILL.md](skills/03-asset-restyle/SKILL.md).

For final comparison and completion judgment, follow [skills/04-replica-validator/SKILL.md](skills/04-replica-validator/SKILL.md).

Load supporting references only when the current phase needs them:

* [references/framework-rules.md](references/framework-rules.md) for framework and build preservation.
* [references/parameter-rules.md](references/parameter-rules.md) for parameter locking and comparison.
* [references/asset-rules.md](references/asset-rules.md) for image, atlas, Sprite Sheet, and alpha handling.
* [references/validation-rules.md](references/validation-rules.md) for severity, final reports, and repair routing.

## Required Artifacts

The workflow writes analysis and reports under `replication/`:

```text
replication/
├── SOURCE_SPEC.md
├── ARCHITECTURE.md
├── PARAMETER_LOCK.json
├── SYMBOL_MAP.json
├── ASSET_MANIFEST.json
├── REPLICATION_PLAN.md
├── CODE_REPLICA_REPORT.md
├── STYLE_SPEC.md
├── ASSET_RESTYLE_REPORT.md
└── REPLICATION_REPORT.md
```

When the user does not request asset restyling, still validate existing asset specifications and note that no visual replacement was performed.

## Useful Scripts

The `scripts/` directory contains helpers for repeatable checks:

```text
python scripts/scan-project.py <project-root> --out replication/SOURCE_SCAN.json
python scripts/extract-parameters.py <project-root> --out replication/PARAMETER_LOCK.json
python scripts/asset-manifest.py <project-root> --out replication/ASSET_MANIFEST.json
python scripts/create-replica-workspace.py <original-project-root>
python scripts/compare-parameters.py <original-lock.json> <replica-lock.json>
python scripts/compare-assets.py <original-assets.json> <replica-assets.json>
python scripts/validate-build.py <project-root>
```

Use these scripts when they fit the project, but do not treat their output as a substitute for reading the source. They are scaffolding for repeatable validation.

## Source Priority

When sources conflict, use this order:

```text
source code > build/runtime results > screenshots/videos > user description > inference
```

Record uncertainty in `replication/REPLICATION_REPORT.md`.

## Completion Rule

Only report `REPLICATION COMPLETE` when all of these are true:

* The framework, language, build system, and runtime platform are preserved.
* The project builds successfully.
* Locked parameters match.
* Core mechanics, state transitions, inputs, events, and critical behaviors are preserved.
* Assets are present and match required dimensions, formats, alpha requirements, and Sprite Sheet structures.
* There are no unresolved `CRITICAL` or `HIGH` differences.

Otherwise report `REPLICATION INCOMPLETE` and route the remaining work back to the correct phase.
