#!/usr/bin/env python3
"""
Generate a manifest.json for PNG files in a directory.

Usage:
- Drop this script into any target folder and run it (double-click or `python generate_manifest.py`).
  It will write `manifest.json` for the folder the script resides in.
- OR run it from anywhere and pass one or more folders:
    python generate_manifest.py D:\path\to\folder1 D:\path\to\folder2

Behavior:
- Only includes files ending with .png (case-insensitive)
- Non-recursive (only the given directory, not subfolders)
- Writes a JSON array of filenames (strings), sorted alphabetically
- Overwrites an existing manifest.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def build_manifest_for_dir(dir_path: Path) -> Path:
    if not dir_path.exists() or not dir_path.is_dir():
        raise FileNotFoundError(f"Not a directory: {dir_path}")

    # Collect only .png files in this directory (non-recursive)
    files = [p.name for p in dir_path.iterdir() if p.is_file() and p.suffix.lower() == ".png"]
    files.sort(key=lambda s: s.casefold())

    manifest_path = dir_path / "manifest.json"
    manifest_path.write_text(json.dumps(files, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def main(argv: list[str]) -> int:
    # If no args: use the directory where this script is located
    if len(argv) <= 1:
        target_dir = Path(__file__).resolve().parent
        out = build_manifest_for_dir(target_dir)
        print(f"Written {out} ({out.stat().st_size} bytes)")
        return 0

    # If args are given: treat each as a directory
    status = 0
    for arg in argv[1:]:
        try:
            out = build_manifest_for_dir(Path(arg).expanduser().resolve())
            print(f"Written {out} ({out.stat().st_size} bytes)")
        except Exception as e:
            print(f"Error for '{arg}': {e}")
            status = 1
    return status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
