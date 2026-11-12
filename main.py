# cutest-picture-01: the entry is a picture vendored in this repository.
# The program copies it to the output path, byte for byte, every run,
# then checks the copy's sha256 against the vendored file so a
# truncated or corrupted write can never pass silently.
# Standard library only, no network. Run it with:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    if not SRC.is_file():
        raise FileNotFoundError(f"vendored picture missing: {SRC}")
    dest = out_dir / "entry.png"
    shutil.copyfile(SRC, dest)
    if sha256_of(dest) != sha256_of(SRC):
        raise ValueError("copied picture failed the byte self-check")


if __name__ == "__main__":
    main()
