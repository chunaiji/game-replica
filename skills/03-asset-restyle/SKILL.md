---
name: asset-restyle
description: Restyle or validate game visual assets while preserving dimensions, aspect ratios, formats, alpha, Sprite Sheet structure, animation frames, and references.
metadata:
  short-description: Restyle assets without breaking specs
---

# Asset Restyle

Use this phase after code replication, or earlier only for asset analysis support requested by `source-analyzer`.

The visual style may change when the user requests it. Asset specifications and references must not be broken.

## Required Inputs

Read:

```text
replication/ASSET_MANIFEST.json
replication/SOURCE_SPEC.md
user visual style requirements
```

If the user did not ask for visual restyling, validate and report existing asset compatibility instead of generating replacement art.

## Core Rules

Read [../../references/asset-rules.md](../../references/asset-rules.md) before replacing, resizing, cropping, padding, converting, or validating assets.

Preserve:

* Asset count, purpose, path semantics, keys, and references.
* Width, height, aspect ratio, format, alpha requirement, and filename strategy.
* Sprite Sheet layout, frame dimensions, frame count, frame order, animation speed, loop settings, pivot/origin/anchor, and hitbox references.

Default target size:

```text
original asset dimensions = new asset dimensions
```

Never directly replace an asset with an AI-generated image of a different size or alpha mode. Normalize and validate first.

## Style Specification

When restyling is requested, write:

```text
replication/STYLE_SPEC.md
```

Define art style, palette, lighting, outlines, texture, perspective, materials, shadows, saturation, contrast, character proportions, environment style, UI style, and effects style. Use this shared style spec for all generated assets.

## Report

Write:

```text
replication/ASSET_RESTYLE_REPORT.md
```

Include processed assets, unchanged assets, resized/cropped/padded assets, alpha validation, Sprite Sheet validation, reference validation, known differences, and remaining issues. Update `replication/ASSET_MANIFEST.json` when replacement assets are created or classifications are improved.

## Completion Gate

Continue to `replica-validator` only when all assets have been checked against the manifest, dimensions and alpha requirements are validated, Sprite Sheet and animation structures are validated, references are intact, and the report exists.
