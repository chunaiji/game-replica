#!/usr/bin/env python3
"""Compare two PARAMETER_LOCK JSON files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def value_of(entry):
    if isinstance(entry, dict) and "value" in entry:
        return entry["value"]
    return entry


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
            status = "EXTRA"
            failed = True
        elif key not in replica:
            status = "MISSING"
            failed = True
        elif value_of(original[key]) == value_of(replica[key]):
            status = "PASS"
        else:
            status = "FAIL"
            failed = True
        rows.append(
            {
                "parameter": key,
                "original": value_of(original.get(key)),
                "replica": value_of(replica.get(key)),
                "status": status,
            }
        )

    result = {
        "status": "FAIL" if failed else "PASS",
        "differences": [row for row in rows if row["status"] != "PASS"],
        "results": rows,
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
