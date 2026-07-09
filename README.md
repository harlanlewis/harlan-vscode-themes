# Harlan Themes

Calm, warm, monospace-minded themes for VS Code & Cursor, derived from
[harlanlewis.com](https://harlanlewis.com) — "a well-kept terminal": hierarchy
from weight and space over color, one restrained palette of intent accents.

A theme pack: one extension, one theme per file in `themes/`, each registered in
`package.json` under `contributes.themes`.

## Themes

- **Harlan Light** — from the site's light theme. A warm paper-cream background,
  near-black ink, and the site's intent accents mapped onto code.

_(More to come — dark, and the phosphor terminal tubes.)_

## The palette (Harlan Light)

Straight from the site's `:root` tokens (OKLCH → sRGB):

| Role | Token | Hex |
|---|---|---|
| Background (warm cream) | `--pole-bg-light` | `#fffaef` |
| Foreground | `--pole-fg-light` | `#18181a` |
| Muted (comments) | `--muted` | `#71716e` |
| Rule / borders | `--rule` | `#e2e1dd` |
| Violet — keywords, primary UI accent | `--violet` | `#7c3aed` |
| Fuchsia — inline code, function/named refs, **cursor** | `--fuchsia` | `#db2777` |
| Steel — types, tags | `--steel` | `#38759d` |
| Green — strings | `--green-deep` | `#166534` |
| Orange — numbers, constants | `--orange-deep` | `#9a3412` |
| Yellow — selection highlighter | `--yellow` | `#eab308` |
| Red — errors, invalid | `--red` | `#dc2626` |

The site refuses syntax color on its own code blocks (all one monospace,
weight-and-space hierarchy), so the theme carries its intent-accent semantics
onto code instead of inventing a new palette: **violet** keywords, **fuchsia**
inline code + named references (the site's `--mark` hue), **steel** types/tags,
**green** strings, **orange** numbers. The blinking `/` cursor of the site's
command palette is fuchsia — so is the editor caret here. Fenced code *blocks*
stay flat, uncolored slabs, as they are on the site.

## Install

Copy or symlink this folder into your editor's extensions directory and reload:

```sh
# Cursor
ln -s "$PWD" ~/.cursor/extensions/harlanlewis.harlan-vscode-themes-1.0.0
# VS Code
ln -s "$PWD" ~/.vscode/extensions/harlanlewis.harlan-vscode-themes-1.0.0
```

Then: **Cmd-K Cmd-T** → **Harlan Light**.
