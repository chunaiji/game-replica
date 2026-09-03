#!/usr/bin/env python3
"""Run the closest available build validation command for a project."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def command_for(root: Path) -> list[str] | None:
    package_json = root / "package.json"
    if package_json.exists():
        package = json.loads(package_json.read_text(encoding="utf-8"))
        scripts = package.get("scripts", {})
        package_manager = "npm"
        if (root / "pnpm-lock.yaml").exists() and shutil.which("pnpm"):
            package_manager = "pnpm"
        elif (root / "yarn.lock").exists() and shutil.which("yarn"):
            package_manager = "yarn"
        if "build" in scripts:
            return [package_manager, "run", "build"]
        if "typecheck" in scripts:
            return [package_manager, "run", "typecheck"]
        if "test" in scripts:
            return [package_manager, "test"]
    if (root / "Cargo.toml").exists() and shutil.which("cargo"):
        return ["cargo", "test"]
    if (root / "pom.xml").exists() and shutil.which("mvn"):
        return ["mvn", "test"]
    if (root / "build.gradle").exists() and shutil.which("gradle"):
        return ["gradle", "test"]
    if (root / "pyproject.toml").exists() and shutil.which("python"):
        return ["python", "-m", "compileall", "."]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    root = args.project_root.resolve()
    cmd = command_for(root)
    if not cmd:
        result = {
            "status": "NOT RUN",
            "reason": "No supported build, typecheck, or test command detected.",
            "command": None,
        }
        text = json.dumps(result, ensure_ascii=False, indent=2)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(text, encoding="utf-8")
        print(text)
        return 2

    completed = subprocess.run(
        cmd,
        cwd=root,
        text=True,
        capture_output=True,
        timeout=args.timeout,
        check=False,
    )
    result = {
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "command": cmd,
        "returncode": completed.returncode,
        "stdout": completed.stdout[-8000:],
        "stderr": completed.stderr[-8000:],
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(text)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
