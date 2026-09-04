# Asset Rules

Use these rules for game images, atlases, Sprite Sheets, animation frames, icons, UI art, backgrounds, particles, and visual effects.

## Manifest Requirements

Every relevant asset should have an entry in `replication/ASSET_MANIFEST.json` with:

```text
filename
path
width
height
format
alpha
file_size
category
usage
reference_count
sprite_sheet
frame_count
locked
```

For Sprite Sheets, also record:

```text
sheet_width
sheet_height
rows
columns
frame_width
frame_height
frame_order
animation_keys
```

## Dimension and Ratio Preservation

Default:

```text
original width  = replica width
original height = replica height
```

Do not replace an asset with a generated image of a different size, aspect ratio, alpha mode, or format. Normalize it first with resize, crop, padding, alpha handling, and format conversion.

## Transparency

If the original asset has alpha, the replacement must preserve alpha.

Usually alpha-sensitive categories:

```text
Character
NPC
Item
Icon
Effect
Particle
UI element
```

Do not add a background to transparent sprites unless the original has one or the user explicitly requests it.

## Sprite Sheet and Animation

Preserve:

* Frame count.
* Frame order.
* Frame width and height.
* Rows and columns.
* Animation speed.
* Loop settings.
* Pivot, origin, anchor, and hitbox references.

Frame changes can alter gameplay timing and collision, so treat unexpected differences as high priority.

## Replacement Strategy

Prefer preserving original resource paths and keys:

```text
assets/player_idle.png → assets/player_idle.png
```

Avoid code changes for asset paths unless a manifest-backed reason requires it. If paths or keys change, update the manifest and symbol/reference reports.

## Generation and Slicing Order

When AI-generated art is used, keep the replacement flow in this order:

1. Generate the image.
2. Back up the raw generated file before any edits.
3. Slice, crop, or cut the asset into the required final shape or Sprite Sheet frames.
4. Normalize dimensions, alpha, and format.
5. Write the final asset into the replica workspace under the matching path.

Never replace the original project file directly with a generated draft. Always stage the replacement in the `_replace` workspace and keep the original source project untouched.
