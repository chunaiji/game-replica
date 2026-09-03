# Validation Rules

Use these rules in the final validator and when deciding whether to return to an earlier phase.

## Required Checks

Validate:

```text
Framework
Build
Structure
Parameters
Functions
Game Logic
Input
Events
Assets
Animation
Runtime
Critical Behavior
```

## Severity

Classify every difference.

### CRITICAL

```text
Game cannot start
Game cannot build
Core mechanic changed
Locked parameter changed
State machine broken
Required asset missing
```

### HIGH

```text
Major UI broken
Animation broken
Input broken
Enemy behavior changed
Important event order changed
Collision behavior changed
```

### MEDIUM

```text
Minor layout difference
Non-critical visual difference
Non-blocking audio difference
Small presentation mismatch
```

### LOW

```text
Naming difference
Comment difference
Internal implementation difference
Non-behavioral file organization difference
```

## Repair Routing

Route failures by source:

```text
Parameter    → code-replica
Architecture → source-analyzer
Code         → code-replica
Asset        → asset-restyle
Animation    → asset-restyle or code-replica, depending on source
Input/Event  → code-replica
Unknown      → source-analyzer
```

Run validation again after repairs.

## Final Status

Only output:

```text
REPLICATION COMPLETE
```

when all are true:

* `CRITICAL = 0`
* `HIGH = 0`
* `Build = PASS`
* `Parameters = PASS`
* `Runtime = PASS`
* Critical behavior validation passes.

Otherwise output:

```text
REPLICATION INCOMPLETE
```

Do not weaken checks or edit locked source-analysis artifacts just to pass validation.
