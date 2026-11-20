#!/usr/bin/env python3
"""News-image entry v2 (Python 3.13, standard library only).

Writes the entry image to /output/entry.png (or $MAKEFUN_OUTPUT_DIR
when set, for local testing). The image bytes live in entry.png.b64
beside this file (base64 of the PNG): the entry is assembled from text
files, so the image is carried as base64 and decoded here. Decoding is
deterministic and uses no network, so two runs produce identical bytes.

The write is atomic (temp file + rename) and the decoded bytes are
checked for the PNG magic before anything is written, so a truncated
or corrupt entry.png.b64 fails loudly instead of producing a bad
entry image. The sha256 of the written file is printed for checking.

Local test:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import base64
import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    data = base64.b64decode((HERE / "entry.png.b64").read_text())
    if not data.startswith(PNG_MAGIC):
        raise ValueError("entry.png.b64 did not decode to a PNG image")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUT_DIR / "entry.png"
    tmp = target.with_suffix(".png.tmp")
    tmp.write_bytes(data)
    os.replace(tmp, target)
    print("wrote %s (%d bytes, sha256 %s)"
          % (target, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
