# Parameter Rules

Use these rules when extracting, preserving, or comparing gameplay parameters.

## What to Lock

Lock values that can affect gameplay, timing, layout, physics, animation, input feel, scoring, economy, or level behavior.

Common locked categories:

```text
movement
physics
collision
combat
health
damage
cooldown
animation
spawn
despawn
timer
score
level
AI
camera
input
UI behavior
randomness/probability
```

## Sources to Scan

Scan:

```text
const / let / var / enum
config files
JSON / YAML / XML
ScriptableObject
prefabs / scenes / level files
environment defaults
animation settings
physics settings
package or engine config
```

## Lock Format

Prefer this shape in `replication/PARAMETER_LOCK.json`:

```json
{
  "player_speed": {
    "value": 320,
    "source": "src/config/player.ts",
    "category": "movement",
    "used_by": ["PlayerController.update"],
    "locked": true
  }
}
```

Use stable IDs for parameter keys. Include source paths and usage when known.

## Comparison Rule

For locked values:

```text
Original Value == Replica Value
```

Any mismatch is a validation failure. Fix the replica, not the original lock file.

## Unknown Values

If a value appears derived or computed, record:

* The expression or derivation source.
* The resolved runtime value when available.
* Any uncertainty that affects validation.
