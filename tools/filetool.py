#!/usr/bin/env python3
"""filetool.py — tiny offline file CLI for agent-file-skills.

Stdlib only. No dependencies, no network, no cloud.
Organizes folders by extension, finds duplicate files
by SHA-256 hash, and batch-renames files.

Safety: organize and rename are DRY-RUN by default.
Add --apply to actually move or rename files.

Usage:
  python tools/filetool.py organize ~/Downloads
  python tools/filetool.py organize ~/Downloads --apply
  python tools/filetool.py duplicates ~/Pictures
  python tools/filetool.py rename photos "IMG_{n:03d}.{ext}" --apply
"""
import argparse
import hashlib
import os
import re
import sys
from collections import defaultdict

EXT_FOLDERS = {
    ".jpg": "images", ".jpeg": "images", ".png": "images", ".gif": "images",
    ".mp4": "videos", ".mov": "videos", ".mkv": "videos",
    ".mp3": "audio", ".wav": "audio",
    ".pdf": "documents", ".doc": "documents", ".docx": "documents",
    ".txt": "documents", ".md": "documents",
    ".csv": "data", ".json": "data", ".xlsx": "data",
    ".zip": "archives", ".tar": "archives", ".gz": "archives",
}


def fail(msg):
    print(f"filetool: error: {msg}", file=sys.stderr)
    return 2


def list_files(directory, recursive=False):
    found = []
    if recursive:
        for root, _, names in os.walk(directory):
            for name in names:
                found.append(os.path.join(root, name))
    else:
        for name in sorted(os.listdir(directory)):
            path = os.path.join(directory, name)
            if os.path.isfile(path):
                found.append(path)
    return found


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_organize(a):
    if not os.path.isdir(a.directory):
        return fail(f"not a directory: {a.directory}")
    files = list_files(a.directory, recursive=False)
    if not files:
        print(f"No files to organize in {a.directory}.")
        return 0
    moved = 0
    for path in files:
        ext = os.path.splitext(path)[1].lower()
        folder = EXT_FOLDERS.get(ext, "other")
        target_dir = os.path.join(a.directory, folder)
        target = os.path.join(target_dir, os.path.basename(path))
        if os.path.abspath(path) == os.path.abspath(target):
            continue
        if a.apply:
            os.makedirs(target_dir, exist_ok=True)
            os.rename(path, target)
            print(f"Moved: {os.path.basename(path)} -> {folder}/")
        else:
            print(f"Would move: {os.path.basename(path)} -> {folder}/")
        moved += 1
    if a.apply:
        print(f"Organized {moved} file(s) in {a.directory}.")
    else:
        print(f"\nDry run: {moved} file(s) would move. Add --apply to actually move them.")
    return 0


def cmd_duplicates(a):
    if not os.path.isdir(a.directory):
        return fail(f"not a directory: {a.directory}")
    files = list_files(a.directory, recursive=a.recursive)
    groups = defaultdict(list)
    for path in files:
        try:
            groups[sha256(path)].append(path)
        except OSError as e:
            print(f"Skipping {path}: {e}", file=sys.stderr)
    dupes = {h: ps for h, ps in groups.items() if len(ps) > 1}
    if not dupes:
        print(f"No duplicates found in {a.directory} ({len(files)} files checked).")
        return 0
    total_extra = 0
    for h, paths in sorted(dupes.items(), key=lambda kv: -len(kv[1])):
        size = os.path.getsize(paths[0])
        print(f"\nDuplicate set ({len(paths)} files, {size} bytes each, sha256 {h[:12]}...):")
        for p in paths:
            print(f"  {p}")
        total_extra += size * (len(paths) - 1)
    print(f"\n{len(dupes)} duplicate set(s). Wasted space: about {total_extra} bytes.")
    print("Nothing was deleted. Review the list before removing anything.")
    return 0


def cmd_rename(a):
    if not os.path.isdir(a.directory):
        return fail(f"not a directory: {a.directory}")
    files = sorted(f for f in list_files(a.directory) if os.path.isfile(f))
    if not files:
        print(f"No files to rename in {a.directory}.")
        return 0
    pattern = a.pattern
    if not re.search(r"\{n(?::[^}]*)?\}", pattern) and "{name}" not in pattern:
        return fail("pattern must contain {n} (number) or {name} (original name)")
    for i, path in enumerate(files, 1):
        base, ext = os.path.splitext(os.path.basename(path))
        name = pattern.replace("{name}", base).replace("{ext}", ext.lstrip("."))
        # Support {n:03d} style padding.
        name = re.sub(r"\{n(?::0?(\d+)d)?\}",
                      lambda m: str(i).zfill(int(m.group(1))) if m.group(1) else str(i),
                      name)
        if "{ext}" not in pattern and not name.endswith(ext):
            name += ext
        target = os.path.join(a.directory, name)
        if os.path.abspath(path) == os.path.abspath(target):
            continue
        if os.path.exists(target):
            print(f"Skipping (target exists): {os.path.basename(path)} -> {name}")
            continue
        if a.apply:
            os.rename(path, target)
            print(f"Renamed: {os.path.basename(path)} -> {name}")
        else:
            print(f"Would rename: {os.path.basename(path)} -> {name}")
    if not a.apply:
        print("\nDry run: nothing was renamed. Add --apply to actually rename.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="filetool", description="Tiny offline file CLI (stdlib only).")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("organize", help="Move files into folders by extension")
    s.add_argument("directory")
    s.add_argument("--apply", action="store_true", help="Actually move files (default: dry run)")
    s.set_defaults(fn=cmd_organize)

    s = sub.add_parser("duplicates", help="Find duplicate files by SHA-256 hash")
    s.add_argument("directory")
    s.add_argument("--recursive", action="store_true")
    s.set_defaults(fn=cmd_duplicates)

    s = sub.add_parser("rename", help="Batch-rename files with a pattern")
    s.add_argument("directory")
    s.add_argument("pattern", help='e.g. "IMG_{n:03d}.{ext}" or "trip_{name}.{ext}"')
    s.add_argument("--apply", action="store_true", help="Actually rename (default: dry run)")
    s.set_defaults(fn=cmd_rename)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
