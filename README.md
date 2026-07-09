# Harlan Light

A VS Code / Cursor color theme derived from the **light** theme of
[harlanlewis.com](https://harlanlewis.com) — "a well-kept terminal": calm,
warm, monospace-minded, hierarchy from weight and space over color.

## The palette

Straight from the site's `:root` tokens (OKLCH → sRGB):

| Role | Token | Hex |
|---|---|---|
| Background | `--pole-bg-light` | `#fbfbf8` |
| Foreground | `--pole-fg-light` | `#18181a` |
| Muted (comments) | `--muted` | `#71716e` |
| Rule / borders | `--rule` | `#e2e1dd` |
| Violet — keywords, primary UI accent | `--violet` | `#7c3aed` |
| Fuchsia — the "name", functions, **cursor** | `--fuchsia` | `#db2777` |
| Steel — types, tags | `--steel` | `#38759d` |
| Green — strings | `--green-deep` | `#166534` |
| Orange — numbers, constants | `--orange-deep` | `#9a3412` |
| Yellow — selection highlighter | `--yellow` | `#eab308` |
| Red — errors, invalid | `--red` | `#dc2626` |

The site refuses syntax color on its own code blocks (all one monospace,
weight-and-space hierarchy), so this theme carries its intent-accent semantics
onto code instead of inventing a new palette: **violet** keywords, **fuchsia**
names/functions (the site's `--mark`), **steel** types/tags, **green** strings,
**orange** numbers. The blinking `/` cursor of the site's command palette is
fuchsia — so is the editor caret here.

## Install

It's already installed if you ran the setup from this repo. Otherwise, copy or
symlink this folder into your editor's extensions directory and reload:

```sh
# Cursor
ln -s "$PWD" ~/.cursor/extensions/harlanlewis.harlan-light-theme-1.0.0
# VS Code
ln -s "$PWD" ~/.vscode/extensions/harlanlewis.harlan-light-theme-1.0.0
```

Then: **Cmd-K Cmd-T** → **Harlan Light**.
