# agent-file-skills

> **Agent Skills for files — organize folders, find duplicate files, and batch-rename. Offline, stdlib-only Python.**

**1 skill · 1 CLI · 0 dependencies · 100% offline**

[![GitHub stars](https://img.shields.io/github/stars/megaartaiking-cmd/agent-file-skills?style=social)](https://github.com/megaartaiking-cmd/agent-file-skills/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](tools/filetool.py)

AI agents are great at code, but a messy folder still means dragging files one by one, or writing a one-off script to find duplicates. This repo fixes that gap: a small Agent Skill (SKILL.md) plus a tiny Python CLI that organizes folders by file type, finds true duplicates by hash, and batch-renames files — in the terminal, on the user's own PC.

Works with Claude Code, Cursor, GitHub Copilot, Codex, Gemini CLI, and any agent that reads SKILL.md files.

## Why this exists

Agent Skills are the fastest-growing category on GitHub — small, composable skill bundles, one job per skill, install in one step. Files are what agents touch most, and there is no small, offline, agent-native way to tidy a folder or find wasted space without a heavy file manager.

This one is:

- **Agent-native** — a skill in the open SKILL.md format, one job, clear rules
- **Offline** — no upload, no cloud, files never leave the PC
- **Lightweight** — stdlib-only Python, no pip install, no heavy app
- **Safe** — organize and rename are dry-run by default. Duplicates are never deleted — the skill only shows the list

## Skills

| Skill | What it does | Command |
|---|---|---|
| `file-organize` | Organize, find duplicates, batch-rename | `filetool.py` |

The skill lives in `skills/file-organize/SKILL.md` — copy that folder into your agent's skills folder, or point your agent at this repo.

## Quick start

```sh
git clone https://github.com/megaartaiking-cmd/agent-file-skills.git
cd agent-file-skills

# 1. Make a demo folder to try the tool on
mkdir -p demo
cp examples/sample.txt demo/report.txt
cp examples/sample.txt demo/report-copy.txt

# 2. Find duplicates (dry run, nothing is changed)
python tools/filetool.py duplicates demo

# 3. Organize by extension (dry run first)
python tools/filetool.py organize demo
python tools/filetool.py organize demo --apply
```

No installation needed — Python 3.9+ is the only requirement.

## Usage

```sh
# Move files into folders by extension (dry run by default)
python tools/filetool.py organize ~/Downloads
python tools/filetool.py organize ~/Downloads --apply

# Find duplicate files by SHA-256 hash
python tools/filetool.py duplicates ~/Pictures
python tools/filetool.py duplicates ~/Pictures --recursive

# Batch-rename with a pattern (dry run by default)
python tools/filetool.py rename photos "IMG_{n:03d}.{ext}"
python tools/filetool.py rename photos "IMG_{n:03d}.{ext}" --apply
```

`{n}` is the number, `{name}` is the original name, `{ext}` is the extension. See [examples/commands.md](examples/commands.md) for all commands.

## How it works

1. You (or your agent) describe the job in plain words: "organize my Downloads folder".
2. The skill in `skills/file-organize/` tells the agent the exact workflow, the command to run, and the rules — dry run first, never delete duplicates, never touch system folders.
3. `tools/filetool.py` (stdlib-only Python) does the work locally and reports what moved, what would move, and what was skipped.
4. Nothing is uploaded. The work happens on your PC.

## Works with

- Claude Code
- Cursor
- GitHub Copilot
- Codex
- Gemini CLI
- Any agent that reads Agent Skills (SKILL.md)

Copy `skills/file-organize/` into your agent's skills directory, or ask your agent to read the SKILL.md file in this repo directly.

## FAQ

**Does it need the internet?**
No. After `git clone`, everything runs offline.

**Does it delete duplicate files?**
No — deliberately. It lists each duplicate set and the wasted space. You choose what to remove.

**What does organize do exactly?**
It moves files into folders by extension: images, videos, audio, documents, data, archives, and other.

**What if a rename target already exists?**
That file is skipped, and the tool says so.

**Will it organize my home folder?**
No — the skill says never to organize a home folder, system folder, or code folder without asking first.

**Will it run on an old PC?**
Yes — that is the point. It is a small Python script with no dependencies.

**Can I add a skill?**
Yes — copy `skills/file-organize/` as a template, write a SKILL.md with a clear name, description, workflow, and rules, and open a pull request.

## Contributing

Issues and pull requests are welcome. Keep skills small, one job per skill, with a tested command in `tools/filetool.py`. Please do not add dependencies — stdlib only.

## License

MIT — see [LICENSE](LICENSE).

---

**Keywords:** agent skills, AI agent files, organize files, find duplicates, batch rename, Claude Code skills, Cursor skills, offline file organizer, Python file CLI, duplicate finder
