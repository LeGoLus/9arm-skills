---
name: excalidraw-diagram
description: Draw diagrams as Excalidraw files, render them to PNG, review them, and embed them in documents. Use when the user asks for a diagram, flowchart or picture of how something works, AND whenever you write a report, PRD, guide, proposal or explainer where a flow, architecture, relationship, timeline or before/after is hard to grasp from text alone.
---

# Excalidraw Diagram

Turn a hard-to-read explanation into one clear picture, and keep the source so it can be edited later.
Inspired by coleam00/excalidraw-diagram-skill (see `CREDITS.md`); this is an independent rewrite.

## When to use / skip

- **Use** when the reader must see structure: steps, branches, loops, who-talks-to-whom, layers, before/after, timeline.
- **Skip** for simple docs, lists, or anything a sentence explains. A decorative diagram is worse than none.
- In documents the diagram **supplements** the written explanation; it never replaces it.

## Process

1. **One message.** Write the takeaway in one sentence ("Requests are validated, then routed to one of three queues").
   That sentence is the diagram's title or caption.
2. **Ground it.** For a real system, look up actual names, fields, commands and numbers first. Do not invent them.
3. **Choose the form** from `references/patterns.md` (what the content *does* → what it looks like). Budget ~12 nodes;
   more than that → split into an overview + a zoom.
4. **Colors** come from `references/palette.md` by role. Do not invent colors.
5. **Write the JSON in sections**, not in one giant response (one zone or one row per edit), with readable ids.
   Format cheat-sheet: `references/format-notes.md`. Hand-write the JSON; no generator scripts.
6. **Render and look at it** (mandatory, see below). JSON alone cannot tell you it looks right.
7. **Fix and re-render** until the checklist passes (usually 2–3 rounds).
8. **Save and embed** (see "In documents").

## Render

```bash
cd ~/.claude/skills/excalidraw-diagram/scripts && uv run python render.py <file.excalidraw> [--out x.png] [--scale 2]
```

Then open the PNG with the Read tool and inspect it. First time on a machine:
`cd ~/.claude/skills/excalidraw-diagram/scripts && uv sync && uv run playwright install chromium`.
The renderer needs internet (Excalidraw is loaded from esm.sh, version pinned in `render.py`). It validates references
first and exits with a clear message on dangling ids, timeouts or renderer errors.

## Review checklist (after every render)

- Does the picture match the one-sentence message? Would the structure still read with the words removed?
- Text clipped, overflowing, overlapping, or too small to read at document size? (Thai text is wide: size boxes generously.)
- Arrows land on the intended element, don't cut through other shapes, and every relationship has one.
- Spacing even; no crowded corner next to an empty one; the most important element is the biggest and most isolated.
- Colors follow the palette roles; contrast is readable; `opacity` 100 everywhere.
- Labels are anchored to what they describe; the same term is used for the same thing throughout.

## In documents (house rule)

1. **Store as data next to the document:** `<doc-dir>/diagrams/<doc-slug>-<nn>-<topic>.excalidraw` and the `.png`
   beside it. Never delete them; later edits start from the `.excalidraw`.
2. **Embed the PNG:** Markdown/HTML `![alt](diagrams/<file>.png)` with a one-line caption (relative path keeps the doc
   portable); `.docx`/`.pptx` insert the PNG via the docx/pptx skill; Gamma/Canva upload the PNG.
3. **Refer to it in the text** ("see the diagram below") and check that picture and prose say the same thing.
4. Labels use the document's language.

## Rules

- No screenshots of code as "diagrams"; use real diagram elements.
- Don't fake precision: if a value is unknown, leave it out instead of guessing.
- Don't restyle per diagram. To change the look, edit `references/palette.md` once.

## Files

| Path | What |
|---|---|
| `references/patterns.md` | content → visual pattern, depth, composition |
| `references/palette.md` | roles, colors, text sizes (single source of truth) |
| `references/format-notes.md` | minimal `.excalidraw` JSON for shapes, labels, arrows |
| `scripts/render.py` | `.excalidraw` → PNG (headless Chromium) |
| `examples/` | one worked diagram (source + PNG) |
