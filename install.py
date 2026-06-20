#!/usr/bin/env python3
"""Install this VS Code configuration onto the current machine.

Symlinks settings/keybindings/snippets into the VS Code User directory
(backing up anything already there) and installs the extension set.

Usage:
    ./install.py            # link configs + install extensions
    ./install.py --copy     # copy files instead of symlinking
    ./install.py --no-ext   # skip installing extensions
"""
import argparse
import datetime as dt
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent


def user_dir() -> Path:
    """Locate the VS Code 'User' directory for this platform."""
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Code" / "User"
    if system == "Linux":
        base = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
        return Path(base) / "Code" / "User"
    if system == "Windows":
        return Path(os.environ["APPDATA"]) / "Code" / "User"
    sys.exit(f"Unsupported OS: {system}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--copy", action="store_true",
                        help="copy files instead of symlinking")
    parser.add_argument("--no-ext", dest="install_ext", action="store_false",
                        help="skip installing extensions")
    args = parser.parse_args()

    dest_dir = user_dir()
    print(f"VS Code User directory: {dest_dir}")
    (dest_dir / "snippets").mkdir(parents=True, exist_ok=True)

    backup_dir = dest_dir / f"backup-{dt.datetime.now():%Y%m%d-%H%M%S}"

    def place(src: Path, dest: Path) -> None:
        if not src.exists():
            return
        if dest.is_symlink() or dest.exists():
            if dest.is_symlink():
                dest.unlink()
            else:
                backup_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(dest), str(backup_dir / dest.name))
                print(f"  backed up existing {dest.name} -> {backup_dir}/")
        if args.copy:
            shutil.copy2(src, dest)
            print(f"  copied  {dest.name}")
        else:
            dest.symlink_to(src)
            print(f"  linked  {dest.name}")

    print("Installing config files...")
    place(REPO_DIR / "settings.json", dest_dir / "settings.json")
    place(REPO_DIR / "keybindings.json", dest_dir / "keybindings.json")
    snippets = REPO_DIR / "snippets"
    if snippets.is_dir():
        for f in sorted(snippets.iterdir()):
            place(f, dest_dir / "snippets" / f.name)

    if args.install_ext:
        code = shutil.which("code")
        if code:
            print("Installing extensions...")
            exts = (REPO_DIR / "extensions.txt").read_text().splitlines()
            for ext in filter(None, (e.strip() for e in exts)):
                subprocess.run([code, "--install-extension", ext, "--force"],
                               check=False)
        else:
            print("WARNING: 'code' CLI not found on PATH; skipping extensions.",
                  file=sys.stderr)
            print("  In VS Code run: Shell Command: Install 'code' command in PATH",
                  file=sys.stderr)

    print("Done.")


if __name__ == "__main__":
    main()
