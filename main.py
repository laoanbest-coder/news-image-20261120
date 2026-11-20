#!/usr/bin/env python3
"""News-image entry (Python 3.13, standard library only).

Writes the entry image to /output/entry.png (or $MAKEFUN_OUTPUT_DIR when
set, for local testing). The image bytes live in entry.png.b64 beside this
file (base64 of the PNG): the entry is assembled from text files, so the
image is carried as base64 and decoded here. Decoding is deterministic and
uses no network, so two runs produce identical bytes.

Local test:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import base64
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    data = base64.b64decode((HERE / "entry.png.b64").read_text())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "entry.png").write_bytes(data)


if __name__ == "__main__":
    main()
