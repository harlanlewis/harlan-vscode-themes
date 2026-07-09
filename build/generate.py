#!/usr/bin/env python3
"""Generate the Harlan theme JSONs from one shared structure + per-theme role
palettes. Every theme is the *same* mapping of the site's intent accents onto
editor roles; only the palette swaps. Run from anywhere:

    python3 build/generate.py

Writes themes/harlan-<variant>-color-theme.json for each palette below. The
palettes are the site's tokens (harlanlewis.com assets/css/style.css), converted
OKLCH -> sRGB with the site's own oklch skill (round-trip verified). Stdlib only,
never a runtime/build dependency for the extension — just a dev tool, like vips
for the site's photos.
"""
import json, os

# --- roles -----------------------------------------------------------------
# Each palette is a dict of named roles. The theme() builder below references
# only these names, so a new variant is just a new palette.
#
# neutrals: bg chrome surface surfaceDeep rule indent indentActive lineNr
#           inactiveFg inputBg fg muted quote faint
# accents:  accentFill accent accentDeep accentFg  (violet family / the door)
#           brand brandDeep                        (fuchsia / the mark)
# syntax:   type string number func builtin regexp
# intents:  error errorDeep warning info added modified deleted modSoft selection
# ansi:     list of 16 (black red green yellow blue magenta cyan white + bright*)

LIGHT = {
    "bg": "#fdfaf3", "chrome": "#f7f3ed", "surface": "#efece7",
    "surfaceDeep": "#e2dfda", "rule": "#e2e1dd", "indent": "#efebe5",
    "indentActive": "#d8d5cf", "lineNr": "#c5c2bc", "inactiveFg": "#aaa7a2",
    "inputBg": "#ffffff", "fg": "#18181a", "muted": "#71716e",
    "quote": "#4b4b47", "faint": "#9c9994",
    "accentFill": "#7c3aed", "accent": "#7c3aed", "accentDeep": "#5b21b6",
    "accentFg": "#ffffff", "brand": "#db2777", "brandDeep": "#be185d",
    "linkActive": "#5b21b6",
    "type": "#38759d", "string": "#166534", "number": "#9a3412",
    "func": "#be185d", "builtin": "#0f36bd", "regexp": "#a16207",
    "error": "#dc2626", "errorDeep": "#991b1b", "warning": "#a16207",
    "info": "#38759d", "added": "#16a34a", "modified": "#ea580c",
    "deleted": "#dc2626", "modSoft": "#f4a15c", "selection": "#eab308",
    "ansi": ["#18181a", "#dc2626", "#166534", "#a16207", "#264c69", "#be185d",
             "#38759d", "#71716e", "#9d9991", "#ef4444", "#16a34a", "#ea580c",
             "#38759d", "#db2777", "#629bc6", "#4b4b47"],
    "meta": {"variant": "light", "label": "Harlan Light",
             "type": "light", "uiTheme": "vs"},
}

# Dark: cool teal bg, warm ink (the site's dark theme). Resting text steps up to
# the palette's -light rungs (base violet/steel/etc sink into the dark bg), but
# UI *fills* keep the saturated base step with white knockout, exactly as light.
DARK = {
    "bg": "#182529", "chrome": "#111e22", "surface": "#253337",
    "surfaceDeep": "#314045", "rule": "#293539", "indent": "#243034",
    "indentActive": "#3f4a4d", "lineNr": "#4b5457", "inactiveFg": "#626b6d",
    "inputBg": "#111e22", "fg": "#e7e5e0", "muted": "#8c8b86",
    "quote": "#afaea9", "faint": "#626b6d",
    "accentFill": "#7c3aed", "accent": "#a78bfa", "accentDeep": "#8b5cf6",
    "accentFg": "#ffffff", "brand": "#f472b6", "brandDeep": "#f472b6",
    "linkActive": "#a78bfa",
    "type": "#629bc6", "string": "#4ade80", "number": "#fb923c",
    "func": "#f472b6", "builtin": "#7e99fc", "regexp": "#eab308",
    "error": "#f87171", "errorDeep": "#f87171", "warning": "#eab308",
    "info": "#629bc6", "added": "#4ade80", "modified": "#fb923c",
    "deleted": "#f87171", "modSoft": "#9a5a2e", "selection": "#eab308",
    "ansi": ["#253337", "#f87171", "#4ade80", "#fde047", "#7e99fc", "#f472b6",
             "#629bc6", "#afaea9", "#626b6d", "#f87171", "#4ade80", "#fde047",
             "#7e99fc", "#f9a8d4", "#629bc6", "#e7e5e0"],
    "meta": {"variant": "dark", "label": "Harlan Dark",
             "type": "dark", "uiTheme": "vs-dark"},
}

# Phosphor tubes — monochrome takeovers (the site's secret terminal themes). One
# hue, hierarchy from lightness. Diagnostics (error/warning) stay off-hue so a
# real error still reads — the site's "legibility over fidelity" rule (it keeps
# error red even on the tube). Everything else is the phosphor family.
PHOSPHOR_GREEN = {
    "bg": "#020a02", "chrome": "#071307", "surface": "#0a200e",
    "surfaceDeep": "#0f2e17", "rule": "#143f20", "indent": "#0f2e17",
    "indentActive": "#195c2e", "lineNr": "#195c2e", "inactiveFg": "#22864a",
    "inputBg": "#071307", "fg": "#54ff8c", "muted": "#22864a",
    "quote": "#2e9e52", "faint": "#195c2e",
    "accentFill": "#2bcf70", "accent": "#2bcf70", "accentDeep": "#5cf59b",
    "accentFg": "#03130a", "brand": "#5cf59b", "brandDeep": "#5cf59b",
    "linkActive": "#5cf59b",
    "type": "#3dd474", "string": "#38b463", "number": "#39c266",
    "func": "#5cf59b", "builtin": "#3dd474", "regexp": "#38b463",
    "error": "#f87171", "errorDeep": "#f87171", "warning": "#eab308",
    "info": "#2bcf70", "added": "#5cf59b", "modified": "#eab308",
    "deleted": "#f87171", "modSoft": "#195c2e", "selection": "#2bcf70",
    "ansi": ["#03130a", "#38b463", "#2bcf70", "#5cf59b", "#22864a", "#38b463",
             "#2bcf70", "#54ff8c", "#195c2e", "#5cf59b", "#54ff8c", "#5cf59b",
             "#38b463", "#5cf59b", "#54ff8c", "#5cf59b"],
    "meta": {"variant": "terminal-green", "label": "Harlan Terminal (Green)",
             "type": "dark", "uiTheme": "vs-dark"},
}

PHOSPHOR_AMBER = {
    "bg": "#0a0600", "chrome": "#140f03", "surface": "#231906",
    "surfaceDeep": "#32230a", "rule": "#3a2606", "indent": "#32230a",
    "indentActive": "#704a07", "lineNr": "#704a07", "inactiveFg": "#b07a32",
    "inputBg": "#140f03", "fg": "#ffcf8a", "muted": "#b07a32",
    "quote": "#c28d42", "faint": "#704a07",
    "accentFill": "#ffb454", "accent": "#ffb454", "accentDeep": "#ffd9a0",
    "accentFg": "#160a00", "brand": "#ffd9a0", "brandDeep": "#ffd9a0",
    "linkActive": "#ffd9a0",
    "type": "#f3ae54", "string": "#cf9b56", "number": "#e6a64f",
    "func": "#ffd9a0", "builtin": "#f3ae54", "regexp": "#cf9b56",
    "error": "#f87171", "errorDeep": "#f87171", "warning": "#eab308",
    "info": "#ffb454", "added": "#ffd9a0", "modified": "#ffb454",
    "deleted": "#f87171", "modSoft": "#704a07", "selection": "#ffb454",
    "ansi": ["#160a00", "#cf9b56", "#ffb454", "#ffd9a0", "#b07a32", "#cf9b56",
             "#ffb454", "#ffcf8a", "#704a07", "#ffd9a0", "#ffcf8a", "#ffd9a0",
             "#cf9b56", "#ffd9a0", "#ffcf8a", "#ffd9a0"],
    "meta": {"variant": "terminal-amber", "label": "Harlan Terminal (Amber)",
             "type": "dark", "uiTheme": "vs-dark"},
}

PALETTES = [LIGHT, DARK, PHOSPHOR_GREEN, PHOSPHOR_AMBER]


def a(hex6, alpha):
    """hex6 + two-digit alpha -> #rrggbbaa"""
    return hex6 + alpha


def colors(P):
    """Workbench colors, keyed by role. One structure, every theme."""
    p = P
    return {
        "foreground": p["quote"],
        "descriptionForeground": p["muted"],
        "errorForeground": p["error"],
        "focusBorder": a(p["accent"], "80"),
        "selection.background": a(p["selection"], "40"),
        "widget.border": p["rule"],
        "widget.shadow": a(p["fg"], "0f"),
        "icon.foreground": p["muted"],
        "sash.hoverBorder": a(p["accent"], "80"),

        # editor
        "editor.background": p["bg"],
        "editor.foreground": p["fg"],
        "editorLineNumber.foreground": p["lineNr"],
        "editorLineNumber.activeForeground": p["muted"],
        "editorCursor.foreground": p["brand"],
        "editorCursor.background": p["bg"],
        "editor.selectionBackground": a(p["selection"], "45"),
        "editor.selectionHighlightBackground": a(p["selection"], "26"),
        "editor.inactiveSelectionBackground": a(p["selection"], "1f"),
        "editor.wordHighlightBackground": a(p["accent"], "1a"),
        "editor.wordHighlightStrongBackground": a(p["accent"], "26"),
        "editor.findMatchBackground": a(p["selection"], "66"),
        "editor.findMatchHighlightBackground": a(p["selection"], "38"),
        "editor.findRangeHighlightBackground": a(p["accent"], "14"),
        "editor.hoverHighlightBackground": a(p["accent"], "14"),
        "editor.lineHighlightBackground": a(p["fg"], "08"),
        "editor.lineHighlightBorder": "#00000000",
        "editorLink.activeForeground": p["accent"],
        "editor.rangeHighlightBackground": a(p["accent"], "10"),
        "editorWhitespace.foreground": p["rule"],
        "editorIndentGuide.background1": p["indent"],
        "editorIndentGuide.activeBackground1": p["indentActive"],
        "editorRuler.foreground": p["indent"],
        "editorBracketMatch.background": a(p["accent"], "1f"),
        "editorBracketMatch.border": a(p["accent"], "66"),
        "editorCodeLens.foreground": p["faint"],
        "editorInlayHint.foreground": p["faint"],
        "editorInlayHint.background": p["surface"],

        "editorBracketHighlight.foreground1": p["accent"],
        "editorBracketHighlight.foreground2": p["type"],
        "editorBracketHighlight.foreground3": p["modified"],
        "editorBracketHighlight.foreground4": p["added"],
        "editorBracketHighlight.foreground5": p["brand"],
        "editorBracketHighlight.foreground6": p["builtin"],
        "editorBracketHighlight.unexpectedBracket.foreground": p["error"],

        # diff / gutter
        "editorGutter.modifiedBackground": p["modified"],
        "editorGutter.addedBackground": p["added"],
        "editorGutter.deletedBackground": p["deleted"],
        "editorGutter.foldingControlForeground": p["faint"],
        "diffEditor.insertedTextBackground": a(p["added"], "1f"),
        "diffEditor.removedTextBackground": a(p["deleted"], "1a"),
        "diffEditor.insertedLineBackground": a(p["added"], "14"),
        "diffEditor.removedLineBackground": a(p["deleted"], "14"),
        "diffEditor.diagonalFill": p["rule"],

        # diagnostics
        "editorError.foreground": p["error"],
        "editorWarning.foreground": p["warning"],
        "editorInfo.foreground": p["info"],
        "editorHint.foreground": p["accent"],
        "problemsErrorIcon.foreground": p["error"],
        "problemsWarningIcon.foreground": p["warning"],
        "problemsInfoIcon.foreground": p["info"],
        "editorOverviewRuler.border": "#00000000",
        "editorOverviewRuler.errorForeground": p["error"],
        "editorOverviewRuler.warningForeground": p["warning"],
        "editorOverviewRuler.infoForeground": p["info"],
        "editorOverviewRuler.findMatchForeground": a(p["selection"], "66"),
        "editorOverviewRuler.modifiedForeground": p["modified"],
        "editorOverviewRuler.addedForeground": p["added"],
        "editorOverviewRuler.deletedForeground": p["deleted"],

        # chrome / widgets
        "editorWidget.background": p["chrome"],
        "editorWidget.border": p["rule"],
        "editorSuggestWidget.background": p["chrome"],
        "editorSuggestWidget.border": p["rule"],
        "editorSuggestWidget.foreground": p["fg"],
        "editorSuggestWidget.selectedBackground": a(p["accent"], "14"),
        "editorSuggestWidget.selectedForeground": p["fg"],
        "editorSuggestWidget.highlightForeground": p["accent"],
        "editorSuggestWidget.focusHighlightForeground": p["accent"],
        "editorHoverWidget.background": p["chrome"],
        "editorHoverWidget.border": p["rule"],
        "editorHoverWidget.foreground": p["fg"],

        "editorGroup.border": p["rule"],
        "editorGroupHeader.tabsBackground": p["chrome"],
        "editorGroupHeader.tabsBorder": p["rule"],
        "editorGroupHeader.noTabsBackground": p["chrome"],
        "editorGroupHeader.border": p["rule"],

        "tab.activeBackground": p["bg"],
        "tab.activeForeground": p["fg"],
        "tab.inactiveBackground": p["chrome"],
        "tab.inactiveForeground": p["muted"],
        "tab.hoverBackground": p["surface"],
        "tab.hoverForeground": p["fg"],
        "tab.border": p["rule"],
        "tab.activeBorder": "#00000000",
        "tab.activeBorderTop": p["brand"],
        "tab.unfocusedActiveBorderTop": p["lineNr"],
        "tab.lastPinnedBorder": p["rule"],
        "tab.activeModifiedBorder": p["modified"],
        "tab.inactiveModifiedBorder": p["modSoft"],

        # side bar
        "sideBar.background": p["chrome"],
        "sideBar.foreground": p["quote"],
        "sideBar.border": p["rule"],
        "sideBarTitle.foreground": p["muted"],
        "sideBarSectionHeader.background": p["chrome"],
        "sideBarSectionHeader.foreground": p["muted"],
        "sideBarSectionHeader.border": p["rule"],

        "list.activeSelectionBackground": a(p["accent"], "1f"),
        "list.activeSelectionForeground": p["fg"],
        "list.activeSelectionIconForeground": p["accent"],
        "list.inactiveSelectionBackground": p["surfaceDeep"],
        "list.inactiveSelectionForeground": p["fg"],
        "list.hoverBackground": p["surface"],
        "list.hoverForeground": p["fg"],
        "list.focusBackground": a(p["accent"], "1f"),
        "list.focusForeground": p["fg"],
        "list.focusOutline": a(p["accent"], "66"),
        "list.highlightForeground": p["accent"],
        "list.errorForeground": p["errorDeep"],
        "list.warningForeground": p["warning"],
        "list.dropBackground": a(p["accent"], "14"),
        "listFilterWidget.background": p["chrome"],
        "listFilterWidget.outline": a(p["accent"], "66"),
        "listFilterWidget.noMatchesOutline": p["error"],
        "tree.indentGuidesStroke": p["indentActive"],
        "tree.inactiveIndentGuidesStroke": p["rule"],

        # activity bar
        "activityBar.background": p["chrome"],
        "activityBar.foreground": p["quote"],
        "activityBar.inactiveForeground": p["inactiveFg"],
        "activityBar.border": p["rule"],
        "activityBar.activeBorder": p["brand"],
        "activityBar.activeBackground": p["surface"],
        "activityBarBadge.background": p["accentFill"],
        "activityBarBadge.foreground": p["accentFg"],

        # status bar
        "statusBar.background": p["chrome"],
        "statusBar.foreground": p["muted"],
        "statusBar.border": p["rule"],
        "statusBar.debuggingBackground": p["modified"],
        "statusBar.debuggingForeground": p["accentFg"],
        "statusBar.noFolderBackground": p["chrome"],
        "statusBar.noFolderForeground": p["muted"],
        "statusBarItem.hoverBackground": p["surface"],
        "statusBarItem.activeBackground": p["surfaceDeep"],
        "statusBarItem.prominentBackground": p["accentFill"],
        "statusBarItem.prominentForeground": p["accentFg"],
        "statusBarItem.prominentHoverBackground": p["accentDeep"],
        "statusBarItem.remoteBackground": p["accentFill"],
        "statusBarItem.remoteForeground": p["accentFg"],
        "statusBarItem.errorBackground": p["error"],
        "statusBarItem.errorForeground": "#ffffff",
        "statusBarItem.warningBackground": p["warning"],
        "statusBarItem.warningForeground": "#ffffff",

        # title bar
        "titleBar.activeBackground": p["chrome"],
        "titleBar.activeForeground": p["quote"],
        "titleBar.inactiveBackground": p["chrome"],
        "titleBar.inactiveForeground": p["inactiveFg"],
        "titleBar.border": p["rule"],

        # menus
        "menu.background": p["chrome"],
        "menu.foreground": p["fg"],
        "menu.border": p["rule"],
        "menu.selectionBackground": a(p["accent"], "1f"),
        "menu.selectionForeground": p["fg"],
        "menu.separatorBackground": p["rule"],
        "menubar.selectionBackground": p["surface"],
        "menubar.selectionForeground": p["fg"],

        # inputs / buttons
        "input.background": p["inputBg"],
        "input.foreground": p["fg"],
        "input.border": p["rule"],
        "input.placeholderForeground": p["faint"],
        "inputOption.activeBackground": a(p["accent"], "26"),
        "inputOption.activeBorder": a(p["accent"], "66"),
        "inputOption.activeForeground": p["linkActive"],
        "inputValidation.errorBackground": a(p["error"], "20"),
        "inputValidation.errorBorder": p["error"],
        "inputValidation.errorForeground": p["fg"],
        "inputValidation.warningBackground": a(p["warning"], "20"),
        "inputValidation.warningBorder": p["warning"],
        "inputValidation.infoBackground": a(p["info"], "20"),
        "inputValidation.infoBorder": p["info"],
        "dropdown.background": p["inputBg"],
        "dropdown.foreground": p["fg"],
        "dropdown.border": p["rule"],
        "dropdown.listBackground": p["chrome"],

        "button.background": p["accentFill"],
        "button.foreground": p["accentFg"],
        "button.hoverBackground": p["accentDeep"],
        "button.secondaryBackground": p["surface"],
        "button.secondaryForeground": p["fg"],
        "button.secondaryHoverBackground": p["surfaceDeep"],
        "checkbox.background": p["inputBg"],
        "checkbox.foreground": p["fg"],
        "checkbox.border": p["lineNr"],

        "badge.background": p["surfaceDeep"],
        "badge.foreground": p["fg"],
        "progressBar.background": p["accentFill"],

        # scrollbar
        "scrollbar.shadow": a(p["fg"], "10"),
        "scrollbarSlider.background": a(p["muted"], "3d"),
        "scrollbarSlider.hoverBackground": a(p["muted"], "59"),
        "scrollbarSlider.activeBackground": a(p["muted"], "73"),
        "minimap.selectionHighlight": a(p["selection"], "66"),
        "minimap.findMatchHighlight": a(p["selection"], "66"),
        "minimap.errorHighlight": p["error"],
        "minimapSlider.background": a(p["muted"], "24"),
        "minimapSlider.hoverBackground": a(p["muted"], "38"),
        "minimapSlider.activeBackground": a(p["muted"], "4d"),

        # text links & keybindings
        "textLink.foreground": p["accent"],
        "textLink.activeForeground": p["linkActive"],
        "textPreformat.foreground": p["brandDeep"],
        "textBlockQuote.background": p["chrome"],
        "textBlockQuote.border": p["rule"],
        "textCodeBlock.background": p["surface"],
        "textSeparator.foreground": p["rule"],
        "keybindingLabel.background": p["surface"],
        "keybindingLabel.foreground": p["quote"],
        "keybindingLabel.border": p["rule"],
        "keybindingLabel.bottomBorder": p["indentActive"],

        # panel & terminal
        "panel.background": p["bg"],
        "panel.border": p["rule"],
        "panelTitle.activeForeground": p["fg"],
        "panelTitle.activeBorder": p["brand"],
        "panelTitle.inactiveForeground": p["muted"],
        "panelInput.border": p["rule"],

        "terminal.background": p["bg"],
        "terminal.foreground": p["fg"],
        "terminalCursor.foreground": p["brand"],
        "terminalCursor.background": p["bg"],
        "terminal.selectionBackground": a(p["selection"], "45"),
        "terminal.border": p["rule"],
        "terminal.ansiBlack": p["ansi"][0],
        "terminal.ansiRed": p["ansi"][1],
        "terminal.ansiGreen": p["ansi"][2],
        "terminal.ansiYellow": p["ansi"][3],
        "terminal.ansiBlue": p["ansi"][4],
        "terminal.ansiMagenta": p["ansi"][5],
        "terminal.ansiCyan": p["ansi"][6],
        "terminal.ansiWhite": p["ansi"][7],
        "terminal.ansiBrightBlack": p["ansi"][8],
        "terminal.ansiBrightRed": p["ansi"][9],
        "terminal.ansiBrightGreen": p["ansi"][10],
        "terminal.ansiBrightYellow": p["ansi"][11],
        "terminal.ansiBrightBlue": p["ansi"][12],
        "terminal.ansiBrightMagenta": p["ansi"][13],
        "terminal.ansiBrightCyan": p["ansi"][14],
        "terminal.ansiBrightWhite": p["ansi"][15],

        # git decorations
        "gitDecoration.modifiedResourceForeground": p["number"],
        "gitDecoration.deletedResourceForeground": p["errorDeep"],
        "gitDecoration.untrackedResourceForeground": p["string"],
        "gitDecoration.ignoredResourceForeground": p["inactiveFg"],
        "gitDecoration.conflictingResourceForeground": p["accent"],
        "gitDecoration.stageModifiedResourceForeground": p["number"],
        "gitDecoration.stageDeletedResourceForeground": p["errorDeep"],
        "gitDecoration.addedResourceForeground": p["string"],
        "gitDecoration.renamedResourceForeground": p["type"],
        "gitDecoration.submoduleResourceForeground": p["muted"],

        # peek
        "peekView.border": a(p["accent"], "66"),
        "peekViewEditor.background": p["bg"],
        "peekViewEditor.matchHighlightBackground": a(p["selection"], "45"),
        "peekViewResult.background": p["chrome"],
        "peekViewResult.selectionBackground": a(p["accent"], "1f"),
        "peekViewResult.matchHighlightBackground": a(p["selection"], "45"),
        "peekViewTitle.background": p["chrome"],
        "peekViewTitleLabel.foreground": p["fg"],
        "peekViewTitleDescription.foreground": p["muted"],

        # notifications & misc
        "notifications.background": p["chrome"],
        "notifications.foreground": p["fg"],
        "notifications.border": p["rule"],
        "notificationCenterHeader.background": p["surface"],
        "notificationCenterHeader.foreground": p["muted"],
        "notificationLink.foreground": p["accent"],
        "notificationsErrorIcon.foreground": p["error"],
        "notificationsWarningIcon.foreground": p["warning"],
        "notificationsInfoIcon.foreground": p["info"],

        "breadcrumb.foreground": p["muted"],
        "breadcrumb.focusForeground": p["fg"],
        "breadcrumb.activeSelectionForeground": p["accent"],
        "breadcrumbPicker.background": p["chrome"],

        "quickInput.background": p["chrome"],
        "quickInput.foreground": p["fg"],
        "quickInputList.focusBackground": a(p["accent"], "1f"),
        "quickInputList.focusForeground": p["fg"],
        "pickerGroup.foreground": p["muted"],
        "pickerGroup.border": p["rule"],

        "charts.foreground": p["quote"],
        "charts.lines": p["rule"],
        "charts.red": p["error"],
        "charts.blue": p["type"],
        "charts.yellow": p["warning"],
        "charts.orange": p["modified"],
        "charts.green": p["added"],
        "charts.purple": p["accent"],

        # debug & testing
        "debugToolBar.background": p["chrome"],
        "debugToolBar.border": p["rule"],
        "debugIcon.breakpointForeground": p["error"],
        "debugIcon.breakpointDisabledForeground": p["lineNr"],
        "testing.iconPassed": p["added"],
        "testing.iconFailed": p["error"],
        "testing.iconSkipped": p["warning"],

        # misc surfaces
        "welcomePage.tileBackground": p["chrome"],
        "welcomePage.tileHoverBackground": p["surface"],
        "welcomePage.background": p["bg"],
        "walkThrough.embeddedEditorBackground": p["chrome"],
        "settings.headerForeground": p["fg"],
        "settings.modifiedItemIndicator": p["accent"],
        "settings.dropdownBackground": p["inputBg"],
        "settings.dropdownBorder": p["rule"],
        "settings.checkboxBackground": p["inputBg"],
        "settings.textInputBackground": p["inputBg"],
        "settings.numberInputBackground": p["inputBg"],

        "extensionButton.prominentBackground": p["accentFill"],
        "extensionButton.prominentForeground": p["accentFg"],
        "extensionButton.prominentHoverBackground": p["accentDeep"],
        "extensionBadge.remoteBackground": p["accentFill"],
        "extensionBadge.remoteForeground": p["accentFg"],
    }


def rule(name, scope, fg=None, style=None):
    s = {}
    if fg:
        s["foreground"] = fg
    if style:
        s["fontStyle"] = style
    return {"name": name, "scope": scope, "settings": s}


def token_colors(P):
    p = P
    return [
        rule("Comments", ["comment", "punctuation.definition.comment",
                          "string.comment"], p["muted"], "italic"),
        rule("Plain text / variables — weight and space, not color",
             ["variable", "variable.other", "variable.other.readwrite",
              "meta.definition.variable variable"], p["fg"]),
        rule("Parameters", ["variable.parameter",
                            "meta.function.parameters variable"], p["quote"]),
        rule("Language variables (this, self, super)",
             ["variable.language", "variable.language.this"],
             p["brandDeep"], "italic"),
        rule("Keywords, storage, control, modifiers",
             ["keyword", "keyword.control", "keyword.other", "storage",
              "storage.type", "storage.modifier", "keyword.operator.new",
              "keyword.operator.expression", "keyword.operator.logical",
              "keyword.control.flow"], p["accent"]),
        rule("Operators & punctuation",
             ["keyword.operator", "punctuation", "punctuation.separator",
              "punctuation.terminator", "meta.brace", "punctuation.section"],
             p["quote"]),
        rule("Strings", ["string", "string.quoted", "string.template",
                        "punctuation.definition.string"], p["string"]),
        rule("String escapes & template expressions",
             ["constant.character.escape",
              "punctuation.definition.template-expression",
              "meta.template.expression"], p["number"]),
        rule("Regular expressions",
             ["string.regexp", "constant.other.character-class.regexp"],
             p["regexp"]),
        rule("Numbers, constants, booleans, language constants",
             ["constant.numeric", "constant.language",
              "constant.language.boolean", "constant.language.null",
              "constant.language.undefined", "keyword.other.unit"], p["number"]),
        rule("Other constants (enums, symbols)",
             ["constant.other", "constant.character",
              "variable.other.constant"], p["number"]),
        rule("Functions & methods — the name's hue",
             ["entity.name.function", "meta.function-call", "support.function",
              "meta.function-call entity.name.function", "variable.function"],
             p["func"]),
        rule("Decorators & annotations",
             ["meta.decorator", "punctuation.decorator",
              "entity.name.function.decorator", "meta.annotation",
              "storage.type.annotation"], p["func"]),
        rule("Types, classes, interfaces, namespaces — tag intent",
             ["entity.name.type", "entity.name.class", "entity.name.namespace",
              "entity.other.inherited-class", "support.type", "support.class",
              "entity.name.type.class", "storage.type.class"], p["type"]),
        rule("Built-in / support types & constants",
             ["support.type.primitive", "support.constant",
              "support.type.builtin"], p["builtin"]),
        rule("Object properties",
             ["variable.other.property", "variable.other.object.property",
              "meta.object-literal.key", "support.variable.property"], p["fg"]),
        rule("Enum members", ["variable.other.enummember"], p["number"]),
        rule("HTML/XML tags — tag intent (steel)",
             ["entity.name.tag", "punctuation.definition.tag"], p["type"]),
        rule("HTML/JSX attribute names — the mark hue (tag / attr / value)",
             ["entity.other.attribute-name",
              "entity.other.attribute-name.html"], p["func"]),
        rule("JSX component names",
             ["support.class.component", "entity.name.tag.jsx"], p["type"]),
        rule("CSS selectors — classes & ids",
             ["entity.other.attribute-name.class.css",
              "entity.other.attribute-name.id.css"], p["type"]),
        rule("CSS property names",
             ["support.type.property-name.css", "meta.property-name.css"],
             p["fg"]),
        rule("CSS property values & keywords",
             ["support.constant.property-value.css", "keyword.other.unit.css"],
             p["number"]),
        rule("Tag / element (Markdown, misc)",
             ["meta.tag", "support.other.namespace"], p["fg"]),
        rule("Invalid", ["invalid", "invalid.illegal"], p["error"]),
        rule("Deprecated", ["invalid.deprecated"], p["warning"], "strikethrough"),
        rule("JSON keys",
             ["support.type.property-name.json",
              "meta.structure.dictionary.json support.type.property-name.json"],
             p["type"]),
        rule("YAML keys",
             ["entity.name.tag.yaml",
              "punctuation.definition.block.sequence.item.yaml"], p["type"]),
        rule("Markdown headings — fg bold (in-article heads rest fg-bold)",
             ["markup.heading", "entity.name.section.markdown",
              "markup.heading.markdown punctuation.definition.heading.markdown"],
             p["fg"], "bold"),
        rule("Markdown bold", ["markup.bold"], p["fg"], "bold"),
        rule("Markdown italic", ["markup.italic"], p["fg"], "italic"),
        rule("Markdown inline code — the mark hue (fenced BLOCKS stay default fg)",
             ["markup.inline.raw"], p["brandDeep"]),
        rule("Markdown links",
             ["markup.underline.link", "string.other.link.title.markdown",
              "constant.other.reference.link.markdown"], p["type"], "underline"),
        rule("Markdown link text / labels",
             ["string.other.link.description.markdown"], p["accent"]),
        rule("Markdown blockquote — muted, like a #spark quote",
             ["markup.quote"], p["muted"], "italic"),
        rule("Markdown list markers — muted (bullets are neutral)",
             ["markup.list punctuation.definition.list.begin",
              "beginning.punctuation.definition.list.markdown"], p["muted"]),
        rule("Markdown inserted (diff-in-md)", ["markup.inserted"], p["string"]),
        rule("Markdown deleted", ["markup.deleted"], p["errorDeep"]),
        rule("Diff header", ["meta.diff.header", "meta.diff.range"], p["accent"]),
    ]


def semantic(P):
    p = P
    return {
        "comment": {"foreground": p["muted"], "fontStyle": "italic"},
        "keyword": p["accent"],
        "type": p["type"], "class": p["type"], "interface": p["type"],
        "enum": p["type"], "typeParameter": p["type"], "namespace": p["type"],
        "struct": p["type"],
        "function": p["func"], "method": p["func"], "macro": p["func"],
        "decorator": p["func"],
        "string": p["string"], "number": p["number"], "regexp": p["regexp"],
        "variable": p["fg"], "variable.readonly": p["number"],
        "parameter": p["quote"], "property": p["fg"],
        "property.readonly": p["number"], "enumMember": p["number"],
        "event": p["func"], "operator": p["quote"],
        "*.defaultLibrary": p["builtin"],
        "selfKeyword": {"foreground": p["func"], "fontStyle": "italic"},
    }


def theme(P):
    m = P["meta"]
    return {
        "$schema": "vscode://schemas/color-theme",
        "name": m["label"],
        "type": m["type"],
        "semanticHighlighting": True,
        "colors": colors(P),
        "tokenColors": token_colors(P),
        "semanticTokenColors": semantic(P),
    }


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    themes_dir = os.path.join(root, "themes")
    os.makedirs(themes_dir, exist_ok=True)
    contributes = []
    for P in PALETTES:
        m = P["meta"]
        fname = "harlan-%s-color-theme.json" % m["variant"]
        path = os.path.join(themes_dir, fname)
        with open(path, "w") as f:
            json.dump(theme(P), f, indent=2, ensure_ascii=False)
            f.write("\n")
        contributes.append({"label": m["label"], "uiTheme": m["uiTheme"],
                            "path": "./themes/%s" % fname})
        print("wrote themes/%s  (%s)" % (fname, m["label"]))
    # keep package.json's contributes.themes in sync
    pkg_path = os.path.join(root, "package.json")
    with open(pkg_path) as f:
        pkg = json.load(f)
    pkg["contributes"]["themes"] = contributes
    with open(pkg_path, "w") as f:
        json.dump(pkg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("synced package.json contributes.themes (%d themes)" % len(contributes))


if __name__ == "__main__":
    main()
