#!/usr/bin/env python3
"""Create a sibling <project>_replace workspace without modifying the source project."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


DEFAULT_EXCLUDES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "dist",
    "build",
    "Library",
    "Temp",
    "Logs",
    "obj",
    "bin",
}


def should_exclude(path: Path, source: Path, excludes: set[str]) -> bool:
    try:
        relative = path.relative_to(source)
    except ValueError:
        return False
    return any(part in excludes for part in relative.parts)


def copy_tree(source: Path, target: Path, excludes: set[str]) -> None:
    target.mkdir(parents=True, exist_ok=False)
    for item in source.rglob("*"):
        if should_exclude(item, source, excludes):
            continue
        relative = item.relative_to(source)
        destination = target / relative
        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--target", type=Path, help="Optional explicit replica workspace path.")
    parser.add_argument("--force", action="store_true", help="Replace an existing target directory.")
    parser.add_argument(
        "--include-heavy",
        action="store_true",
        help="Also copy generated/dependency directories such as node_modules, dist, build, Library, and Temp.",
    )
    args = parser.parse_args()

    source = args.project_root.resolve()
    if not source.exists() or not source.is_dir():
        raise SystemExit(f"Source project does not exist or is not a directory: {source}")

    target = args.target.resolve() if args.target else source.parent / f"{source.name}_replace"
    if source == target or source in target.parents:
        raise SystemExit(f"Refusing to create replica inside the source project: {target}")

    if target.exists():
        if not args.force:
            raise SystemExit(f"Target already exists. Use --force to replace it: {target}")
        shutil.rmtree(target)

    excludes = set()
    if not args.include_heavy:
        excludes = DEFAULT_EXCLUDES
    else:
        excludes = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}

    copy_tree(source, target, excludes)
    print(f"Created replica workspace: {target}")
    print(f"Source left unchanged: {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
