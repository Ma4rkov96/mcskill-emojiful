#!/usr/bin/env python3
"""Writes manifest.json: every emoji image in the repository with its SHA-1.

The Emojiful fork downloads this one file per game session. When a player's cached image has the
same SHA-1, it is used without any further request; a different SHA-1 means the image was replaced,
and it is downloaded again. Run by .github/workflows/manifest.yml on every push.
"""
import hashlib
import json
import os
import sys

BASE = "https://raw.githubusercontent.com/Ma4rkov96/mcskill-emojiful/main/"
IMAGE_EXTENSIONS = {".png", ".gif", ".webp", ".jpg", ".jpeg", ".bmp"}
SKIP_DIRS = {".git", ".github", "tools"}


def main(root: str) -> int:
    files = {}
    for directory, subdirs, names in os.walk(root):
        subdirs[:] = sorted(d for d in subdirs if d not in SKIP_DIRS)
        for name in sorted(names):
            if os.path.splitext(name)[1].lower() not in IMAGE_EXTENSIONS:
                continue
            path = os.path.join(directory, name)
            relative = os.path.relpath(path, root).replace(os.sep, "/")
            with open(path, "rb") as handle:
                files[relative] = hashlib.sha1(handle.read()).hexdigest()
    manifest = {"base": BASE, "files": dict(sorted(files.items()))}
    with open(os.path.join(root, "manifest.json"), "w", encoding="utf-8", newline="\n") as out:
        json.dump(manifest, out, ensure_ascii=False, indent=1)
        out.write("\n")
    print(f"manifest.json: {len(files)} images")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
