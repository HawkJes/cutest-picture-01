# cutest-picture-01 v3: baby harp seal pup holding a tiny pink fish.
# The picture lives vendored next to this file. On every run the program
# copies it byte for byte into the harness output directory, then proves
# the copy by comparing sha256 hashes of source and destination. If the
# hashes ever disagree the run fails loudly instead of shipping a
# truncated file. Pure standard library, no network access at all.
# Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            block = f.read(65536)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def main():
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out.mkdir(parents=True, exist_ok=True)
    if not PICTURE.is_file():
        raise FileNotFoundError(f"vendored picture not found: {PICTURE}")
    target = out / "entry.png"
    shutil.copyfile(PICTURE, target)
    if digest(target) != digest(PICTURE):
        raise ValueError("output picture failed its byte self-check")


if __name__ == "__main__":
    main()
