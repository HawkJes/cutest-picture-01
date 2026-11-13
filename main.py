# cutest-picture-01 v4 — "baby fawn with a butterfly on its nose".
#
# The picture is vendored in this repo as entry.png. This program copies
# that file to the output directory, byte for byte, and then proves the
# copy is intact by comparing the sha256 of the copy against the sha256
# of the vendored file. A truncated or altered write fails loudly here
# instead of reaching the judge.
#
# Standard library only. No network, no clock, no randomness: two runs
# produce byte-identical output.
#
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDORED = HERE / "entry.png"


def digest(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            block = stream.read(65536)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def main():
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    if not VENDORED.is_file():
        raise FileNotFoundError(f"vendored picture not found: {VENDORED}")
    written = output_dir / "entry.png"
    shutil.copyfile(VENDORED, written)
    if digest(written) != digest(VENDORED):
        raise ValueError("output failed the sha256 self-check")


if __name__ == "__main__":
    main()
