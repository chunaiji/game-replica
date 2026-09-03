#!/usr/bin/env python3
"""Extract likely gameplay constants into a PARAMETER_LOCK-style JSON file."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


IGNORE_DIRS = {".git", "node_modules", "dist", "build", "Library", "Temp", "obj", "bin"}
SCAN_EXTS = {".js", ".jsx", ".ts", ".tsx", ".cs", ".cpp", ".c", ".h", ".hpp", ".py", ".gd", ".lua", ".json"}
KEYWORDS = re.compile(
    r"speed|velocity|accel|gravity|jump|health|hp|damage|attack|defen[cs]e|cooldown|"
    r"collision|hitbox|duration|timer|time|score|spawn|despawn|chance|prob|rate|"
    r"scale|size|width|height|radius|range|force|friction|drag|level|enemy|player",
    re.IGNORECASE,
)
ASSIGNMENT = re.compile(
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*(?::\s*[\w<>\[\]\|]+)?\s*[=:]\s*(?P<value>-?\d+(?:\.\d+)?)"
)


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in SCAN_EXTS:
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--out", type=Path, default=Path("replication/PARAMETER_LOCK.json"))
    args = parser.parse_args()

    root = args.project_root.resolve()
    params: dict[str, dict] = {}

    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            match = ASSIGNMENT.search(line)
            if not match:
                continue
            name = match.group("name")
            if not KEYWORDS.search(name):
                continue
            raw_value = match.group("value")
            value = float(raw_value) if "." in raw_value else int(raw_value)
            key = name
            if key in params:
                key = f"{name}@{path.relative_to(root).as_posix()}:{line_no}"
            params[key] = {
                "value": value,
                "source": f"{path.relative_to(root).as_posix()}:{line_no}",
                "category": "unknown",
                "used_by": [],
                "locked": True,
                "confidence": "candidate",
            }

    out = args.out
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(params, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(params)} candidate parameters to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
