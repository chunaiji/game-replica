#!/usr/bin/env python3
"""Scan a game project and write a lightweight source inventory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "Library",
    "Temp",
    "Logs",
    "obj",
    "bin",
    ".gradle",
    ".idea",
    ".vscode",
}

SOURCE_EXTS = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".cs",
    ".cpp",
    ".cc",
    ".c",
    ".h",
    ".hpp",
    ".py",
    ".java",
    ".gd",
    ".lua",
}

ASSET_EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".svg",
    ".mp3",
    ".wav",
    ".ogg",
    ".ttf",
    ".otf",
    ".atlas",
    ".sprite",
}

CONFIG_EXTS = {".json", ".yaml", ".yml", ".xml", ".toml", ".ini", ".cfg"}


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def detect_framework(root: Path, files: list[Path]) -> dict:
    names = {rel(path, root).lower(): path for path in files}
    signals: list[str] = []
    framework = "unknown"
    language = "unknown"
    build_tool = "unknown"
    package_manager = "unknown"

    if "package.json" in names:
        package_manager = "npm-compatible"
        language = "JavaScript/TypeScript"
        build_tool = "package.json scripts"
        try:
            package = json.loads(names["package.json"].read_text(encoding="utf-8"))
            deps = {**package.get("dependencies", {}), **package.get("devDependencies", {})}
            for candidate in ("phaser", "pixi.js", "three", "vite", "webpack"):
                if candidate in deps:
                    signals.append(f"{candidate}: {deps[candidate]}")
            if "phaser" in deps:
                framework = "Phaser"
            elif "pixi.js" in deps:
                framework = "PixiJS"
        except Exception as exc:  # pragma: no cover - diagnostic path
            signals.append(f"package.json unreadable: {exc}")

    if "project.godot" in names:
        framework = "Godot"
        language = "GDScript/C#"
        signals.append("project.godot")

    if any(path.name.endswith(".uproject") for path in files):
        framework = "Unreal"
        language = "C++/Blueprint"
        signals.append("*.uproject")

    if any("ProjectSettings" in path.parts for path in files) and any("Assets" in path.parts for path in files):
        framework = "Unity"
        language = "C#"
        signals.append("Assets/ + ProjectSettings/")

    if "cocoscreator" in " ".join(names.keys()) or any(path.suffix == ".fire" for path in files):
        framework = "Cocos Creator"
        signals.append("Cocos project signals")

    return {
        "framework": framework,
        "language": language,
        "build_tool": build_tool,
        "package_manager": package_manager,
        "signals": signals,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--out", type=Path, default=Path("replication/SOURCE_SCAN.json"))
    args = parser.parse_args()

    root = args.project_root.resolve()
    files = list(iter_files(root))

    inventory = {
        "root": str(root),
        "framework_detection": detect_framework(root, files),
        "counts": {
            "files": len(files),
            "source": sum(1 for path in files if path.suffix.lower() in SOURCE_EXTS),
            "assets": sum(1 for path in files if path.suffix.lower() in ASSET_EXTS),
            "config": sum(1 for path in files if path.suffix.lower() in CONFIG_EXTS),
        },
        "source_files": [rel(path, root) for path in files if path.suffix.lower() in SOURCE_EXTS],
        "asset_files": [rel(path, root) for path in files if path.suffix.lower() in ASSET_EXTS],
        "config_files": [rel(path, root) for path in files if path.suffix.lower() in CONFIG_EXTS],
    }

    out = args.out
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
