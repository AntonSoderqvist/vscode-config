# vscode-config

My portable VS Code configuration: settings, keybindings, snippets, and the
list of extensions I use. Clone this on any machine to reproduce my setup.

## Contents

| File                  | What it is                                  |
|-----------------------|---------------------------------------------|
| `settings.json`       | User settings                               |
| `keybindings.json`    | Custom keybindings                          |
| `snippets/`           | User snippets (e.g. `python.json`)          |
| `extensions.txt`      | Extension IDs, one per line                 |
| `install.py`          | Symlinks the configs in place + installs extensions |
| `export-extensions.py`| Regenerates `extensions.txt` from this machine |

## Install on a new machine

Requires Python 3 (standard library only).

```bash
git clone <this-repo-url> vscode-config
cd vscode-config
./install.py
```

By default this **symlinks** the config files into VS Code's User directory, so
future edits and `git pull`s stay in sync automatically. Existing non-symlink
files are moved into a timestamped `backup-*` folder first.

Options:

- `./install.py --copy` — copy the files instead of symlinking (no live sync).
- `./install.py --no-ext` — skip installing extensions.

The script finds the right User directory per platform:

- Linux: `~/.config/Code/User`
- macOS: `~/Library/Application Support/Code/User`
- Windows (Git Bash): `%APPDATA%/Code/User`

It needs the `code` CLI on your `PATH` to install extensions. If it's missing,
open VS Code and run **Shell Command: Install 'code' command in PATH** from the
command palette.

## Keeping it up to date

After changing settings, just edit the files here (or, if symlinked, edit in
VS Code and the repo updates itself) and commit.

After adding or removing extensions:

```bash
./export-extensions.py
git commit -am "Update extensions"
```
