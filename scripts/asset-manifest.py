#!/usr/bin/env python3
"""Create an asset manifest with basic file metadata and image dimensions."""

from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path


IGNORE_DIRS = {".git", "node_modules", "dist", "build", "Library", "Temp", "obj", "bin"}
ASSET_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".atlas", ".json", ".sprite", ".mp3", ".wav", ".ogg", ".ttf", ".otf"}


def read_png(data: bytes):
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 33:
        width, height = struct.unpack(">II", data[16:24])
        color_type = data[25]
        return width, height, color_type in (4, 6)
    return None


def read_gif(data: bytes):
    if data.startswith((b"GIF87a", b"GIF89a")) and len(data) >= 10:
        width, height = struct.unpack("<HH", data[6:10])
        return width, height, None
    return None


def read_jpeg(data: bytes):
    if not data.startswith(b"\xff\xd8"):
        return None
    index = 2
    while index + 9 < len(data):
        if data[index] != 0xFF:
            index += 1
            continue
        marker = data[index + 1]
        index += 2
        if marker in (0xD8, 0xD9):
            continue
        if index + 2 > len(data):
            break
        length = struct.unpack(">H", data[index:index + 2])[0]
        if marker in range(0xC0, 0xC4) and index + 7 < len(data):
            height, width = struct.unpack(">HH", data[index + 3:index + 7])
            return width, height, False
        index += length
    return None


def image_info(path: Path):
    try:
        data = path.read_bytes()
    except OSError:
        return None
    suffix = path.suffix.lower()
    if suffix == ".png":
        return read_png(data)
    if suffix in {".jpg", ".jpeg"}:
        return read_jpeg(data)
    if suffix == ".gif":
        return read_gif(data)
    return None


def category_for(path: Path) -> str:
    lowered = path.as_posix().lower()
    for name in ("character", "enemy", "npc", "item", "weapon", "background", "ui", "icon", "effect", "particle", "tile", "audio", "font"):
        if name in lowered:
            return name
    if path.suffix.lower() in {".mp3", ".wav", ".ogg"}:
        return "audio"
    if path.suffix.lower() in {".ttf", ".otf"}:
        return "font"
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--out", type=Path, default=Path("replication/ASSET_MANIFEST.json"))
    args = parser.parse_args()

    root = args.project_root.resolve()
    manifest: dict[str, dict] = {}

    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if not path.is_file() or path.suffix.lower() not in ASSET_EXTS:
            continue
        relative = path.relative_to(root).as_posix()
        info = image_info(path)
        width, height, alpha = (info if info else (None, None, None))
        key = relative
        manifest[key] = {
            "source": relative,
            "replica": relative,
            "width": width,
            "height": height,
            "format": path.suffix.lower().lstrip("."),
            "alpha": alpha,
            "file_size": path.stat().st_size,
            "category": category_for(path),
            "usage": "unknown",
            "reference_count": None,
            "sprite_sheet": False,
            "frame_count": 1 if width and height else None,
            "locked": True,
        }

    out = args.out
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(manifest)} assets to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
