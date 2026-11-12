# cutest-picture-01: the entry is a picture vendored in this repository.
# The program copies it to the output path, byte for byte, every run.
# Standard library only, no network. Run it with:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    if not SRC.is_file():
        raise FileNotFoundError(f"vendored picture missing: {SRC}")
    shutil.copyfile(SRC, out_dir / "entry.png")


if __name__ == "__main__":
    main()
