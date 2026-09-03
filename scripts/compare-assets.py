#!/usr/bin/env python3
"""Compare two ASSET_MANIFEST JSON files for spec compatibility."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FIELDS = ("width", "height", "format", "alpha", "sprite_sheet", "frame_count")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("replica", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    original = load(args.original)
    replica = load(args.replica)
    rows = []
    failed = False

    for key in sorted(set(original) | set(replica)):
        if key not in original:
            rows.append({"asset": key, "status": "EXTRA", "field": None, "original": None, "replica": replica[key]})
            failed = True
            continue
        if key not in replica:
            rows.append({"asset": key, "status": "MISSING", "field": None, "original": original[key], "replica": None})
            failed = True
            continue
        for field in FIELDS:
            expected = original[key].get(field)
            actual = replica[key].get(field)
            if expected != actual:
                rows.append({"asset": key, "status": "FAIL", "field": field, "original": expected, "replica": actual})
                failed = True

    result = {
        "status": "FAIL" if failed else "PASS",
        "differences": rows,
    }

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(text)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
