# Example commands

```sh
# Make a demo folder to try the tool on
mkdir -p demo
cp examples/sample.txt demo/report.txt
cp examples/sample.txt demo/report-copy.txt
echo "photo" > demo/photo1.jpg
echo "song" > demo/song1.mp3

# Find duplicate files by SHA-256 hash
python tools/filetool.py duplicates demo
python tools/filetool.py duplicates demo --recursive

# Organize by extension (dry run first)
python tools/filetool.py organize demo
python tools/filetool.py organize demo --apply

# Batch-rename (dry run first)
python tools/filetool.py rename demo "doc_{n:02d}.{ext}"
python tools/filetool.py rename demo "doc_{n:02d}.{ext}" --apply
```

Organize and rename are dry-run by default. Add `--apply` only when you are happy with the preview.
