#!/usr/bin/env python3
"""Entry for make.fun news-image-20261119.

Copies the front-page image held in this repository to the output path
the competition requires: /output/entry.png (or $MAKEFUN_OUTPUT_DIR
when set, the kit starter's local-run convention). Pure standard
library, no network, deterministic: both runs write identical bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
