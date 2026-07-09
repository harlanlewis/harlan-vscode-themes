# Harlan Themes

Calm, warm, monospace-minded themes for VS Code & Cursor, derived from
[harlanlewis.com](https://harlanlewis.com) — "a well-kept terminal": hierarchy
from weight and space over color, one restrained palette of intent accents.

A theme pack: one extension contributing several themes, each generated from a
shared structure so they stay consistent.

## Themes

| Theme | Base | Notes |
|---|---|---|
| **Harlan Light** | light | warm paper-cream bg, near-black ink |
| **Harlan Dark** | dark | cool teal bg, warm ink; accents step to their lighter rungs |
| **Harlan Terminal (Green)** | dark | monochrome P1 phosphor tube — one green, hierarchy from lightness |
| **Harlan Terminal (Amber)** | dark | monochrome P3 phosphor tube — amber |

Each maps the site's **intent accents** onto code the same way: **violet**
keywords, **fuchsia** inline code + named references (the site's `--mark` hue),
**steel** types/tags, **green** strings, **orange** numbers, **muted** comments.
The blinking `/` cursor of the site's command palette is fuchsia — so is the
editor caret. Fenced code *blocks* stay flat, uncolored slabs, as on the site.
The phosphor tubes go monochrome but keep diagnostics off-hue so a real error
still reads (the site's "legibility over fidelity" rule).

## Install

**Dev install** (symlinks this repo into every editor found; edits go live on
reload):

```sh
./install.sh              # or --copy for a frozen snapshot, --uninstall to remove
```

Then reload the window and pick a theme: **Cmd-K Cmd-T → Harlan …**

**Package a `.vsix`** (the standard, shareable install — needs Node):

```sh
npx @vscode/vsce package
code --install-extension harlan-vscode-themes-*.vsix     # VS Code
cursor --install-extension harlan-vscode-themes-*.vsix   # Cursor
```

## Editing

The theme JSONs in `themes/` are **generated** — don't hand-edit them. Change a
color in a palette (or the shared structure) in `build/generate.py`, then:

```sh
python3 build/generate.py     # rewrites themes/ + syncs package.json
```

Palettes are the site's `:root` tokens, converted OKLCH → sRGB with the site's
`oklch` skill (round-trip verified). `generate.py` is stdlib-only and never a
runtime dependency — a dev tool, like `vips` is for the site's photos.
