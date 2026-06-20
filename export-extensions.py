#!/usr/bin/env python3
"""Refresh extensions.txt from the extensions currently installed here.

Run this after adding/removing extensions, then commit the change.
"""
import shutil
import subprocess
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent


def main() -> None:
    code = shutil.which("code")
    if not code:
        sys.exit("'code' CLI not found on PATH.")
    out = subprocess.run([code, "--list-extensions"],
                         capture_output=True, text=True, check=True).stdout
    exts = sorted(filter(None, (line.strip() for line in out.splitlines())))
    target = REPO_DIR / "extensions.txt"
    target.write_text("\n".join(exts) + "\n")
    print(f"Wrote {len(exts)} extensions to extensions.txt")


if __name__ == "__main__":
    main()
