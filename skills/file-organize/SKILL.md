---
name: file-organize
description: Organize folders by file type, find duplicate files by hash, and batch-rename files, offline, with Python. Use when the user or agent wants to tidy a messy folder, find wasted space, or rename many files at once.
---

# File Organize

Tidy up folders without dragging files one by one. Sort files into
folders by type, find true duplicates by SHA-256 hash, or batch-rename
with a pattern. No cloud, no upload. Files stay local.

## When to use

- "Organize my Downloads folder"
- "Find the duplicate files in this folder"
- "Rename all the photos in this folder"

## Workflow

1. Ask which folder, or use the one the user named. If it does not exist, say so and stop.
2. Organize — dry run first, always:
   ```sh
   python tools/filetool.py organize ~/Downloads
   python tools/filetool.py organize ~/Downloads --apply
   ```
   The dry run shows what would move. Only add `--apply` when the user agrees.
3. Find duplicates — by content hash, not by name:
   ```sh
   python tools/filetool.py duplicates ~/Pictures
   python tools/filetool.py duplicates ~/Pictures --recursive
   ```
   Report each duplicate set and the wasted space. Nothing is deleted.
4. Batch-rename — dry run first, always:
   ```sh
   python tools/filetool.py rename photos "IMG_{n:03d}.{ext}"
   python tools/filetool.py rename photos "IMG_{n:03d}.{ext}" --apply
   ```
   `{n}` is the number, `{name}` is the original name, `{ext}` is the extension.
5. Confirm what actually moved or renamed, and report any skipped files.

## Examples

**Tidy the Downloads folder — preview first**
```sh
python tools/filetool.py organize ~/Downloads
# Would move: report.pdf -> documents/
# Dry run: 42 file(s) would move. Add --apply to actually move them.
```

**How much space are duplicates wasting?**
```sh
python tools/filetool.py duplicates ~/Pictures --recursive
# 3 duplicate set(s). Wasted space: about 1843200 bytes.
```

**Rename holiday photos in order**
```sh
python tools/filetool.py rename photos "holiday_{n:03d}.{ext}" --apply
# Renamed: IMG_001.jpg -> holiday_001.jpg
```

## Rules

- Organize and rename are DRY-RUN by default. Never add `--apply` without the user agreeing first.
- Duplicates are never deleted by this skill. Show the list and let the user choose.
- Never organize the user's home folder, system folders, or a folder with code in it — ask first if the folder is not an obvious downloads or media folder.
- If a rename target already exists, skip that file and say so.
- Report the folder path in every answer so the user knows exactly what was touched.
