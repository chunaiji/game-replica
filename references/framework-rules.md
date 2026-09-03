# Framework Rules

Use these rules when detecting, preserving, or validating a game project's technical framework.

## Preserve the Stack

Keep the original:

* Engine or rendering framework.
* Programming language.
* Major framework version when known.
* Build tool and package manager.
* Entry point and runtime platform.
* Dependency semantics and lifecycle.

Examples:

```text
Phaser + TypeScript + Vite → Phaser + TypeScript + Vite
Unity + C#                → Unity + C#
Cocos Creator             → Cocos Creator
```

Do not migrate frameworks unless the user explicitly requests migration.

## Workspace and Layout Preservation

Create the replica in a sibling directory named `<original-folder-name>_replace` unless the user explicitly requests another destination.

Example:

```text
Original: C:\work\space-game
Replica:  C:\work\space-game_replace
```

After the replica workspace is created, treat the original project as read-only. Do not edit source, config, assets, dependency manifests, scenes, or build files in the original directory.

Preserve the project layout inside the replica workspace:

* Source files should stay under corresponding source paths.
* Asset files should stay under corresponding asset paths.
* Config, scene, level, package, and build files should keep their relative paths.
* Resource keys and path assumptions should remain valid.

If a layout change is unavoidable, record the original path, replica path, reason, and validation impact in `replication/REPLICATION_REPORT.md`.

## Detection Signals

Use source files and manifests before inference:

```text
package.json
vite.config.*
webpack.config.*
tsconfig.json
project.godot
*.unity
*.uproject
ProjectSettings/
Assets/
Packages/manifest.json
composer / gradle / maven / cmake files
```

Record uncertain versions with evidence, for example:

```text
Framework: Phaser 3 inferred from package.json dependency "phaser": "^3.80.0"
```

## Build Preservation

Replica build behavior should match the original project unless the user asks otherwise:

* Same package manager when practical.
* Same script names when practical.
* Same platform target.
* Same static asset serving assumptions.
* Same environment variable semantics.

If environment limitations prevent verification, record the skipped command, failure reason, and residual risk in `replication/REPLICATION_REPORT.md`.
