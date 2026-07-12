#!/usr/bin/env bash
# Dev-install the theme pack into VS Code and/or Cursor by symlinking this repo
# into each editor's extensions directory. A symlink (not a copy) means edits +
# `python3 build/generate.py` go live on the next window reload — no reinstall.
#
#   ./install.sh            # install into every editor found
#   ./install.sh --copy     # copy instead of symlink (for a frozen snapshot)
#   ./install.sh --uninstall
#
# To publish properly instead, package a .vsix (see README): `npx @vscode/vsce
# package`, then `code --install-extension harlan-vscode-themes-<v>.vsix`.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$repo"

# id = <publisher>.<name>-<version>, read straight from package.json
read -r publisher name version < <(python3 - <<'PY'
import json
p = json.load(open("package.json"))
print(p["publisher"], p["name"], p["version"])
PY
)
id="${publisher}.${name}-${version}"

mode="link"
[[ "${1:-}" == "--copy" ]] && mode="copy"
[[ "${1:-}" == "--uninstall" ]] && mode="uninstall"

found=0
for dir in "$HOME/.vscode/extensions" "$HOME/.cursor/extensions"; do
  [[ -d "$dir" ]] || continue
  found=1
  editor="$(basename "$(dirname "$dir")")"   # .vscode / .cursor
  # Remove any prior install of this pack (old copies, links, or renamed ids).
  rm -rf "$dir/$id" "$dir/${publisher}.harlan-light-theme-"* 2>/dev/null || true
  if [[ "$mode" == "uninstall" ]]; then
    echo "removed  $editor/$id"
    continue
  fi
  if [[ "$mode" == "copy" ]]; then
    mkdir -p "$dir/$id"
    cp -R package.json README.md themes "$dir/$id/"
    echo "copied   $editor/$id"
  else
    ln -s "$repo" "$dir/$id"
    echo "linked   $editor/$id -> $repo"
  fi
done

if [[ "$found" == "0" ]]; then
  echo "No VS Code or Cursor extensions directory found (~/.vscode, ~/.cursor)." >&2
  exit 1
fi

[[ "$mode" == "uninstall" ]] && exit 0
echo
echo "Reload the window (Cmd-Shift-P → Reload Window), then:"
echo "  Cmd-K Cmd-T → Harlan Paper / Slate / Terracotta (Light|Dark) / Terminal (Green|Amber)"
