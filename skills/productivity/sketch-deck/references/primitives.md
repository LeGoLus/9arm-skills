# Sketch-deck primitives and layout reference

Contents: 1. slides.js shape · 2. Canvas and zones · 3. Drawing functions · 4. Visual pattern library · 5. Gotchas

## 1. slides.js shape

```js
const CONFIG = { stepLabel: 'tip', boardLabel: 'board', revealedLabel: 'revealed', board: true };

const SLIDES = [
  { steps: 1, draw(E){ /* title slide: no n/t/c, draw your own big title */ } },
  { n: 1, t: 'Give it a way to check its own work', c: C.green, steps: 4, draw(E){
      E(0, box(110, 420, 200, 90, 'Task'));          // visible from step 0 onward
      E(0, txt(120, 745, 'old caption', {color: RED}), 1); // visible at step 0 only (hidden from step 1)
      E(1, txt(120, 745, 'new caption', {color: GREEN}));  // replaces it at step 1
  }},
];
```

- `n` = number shown in the round badge, `t` = heading text, `c` = palette entry. Omit all three for a title or section slide.
- `steps` = number of build steps. Every `E(s, ...)` must use `s < steps`.
- `E(start, svgString, end?)`: element is visible when `start <= step < end`. Use `end` to swap captions, replace a low bar with a full one, turn ✗ into ✓, etc.
- Code order = z-order. Add fills before outlines, and things that should sit on top last.
- `CONFIG.board: false` turns off the reveal board between slides (use for short or formal decks).

## 2. Canvas and zones (1600 × 900)

```
y  60-160   heading zone   (badge + title + coloured underline, drawn automatically)
y 200-780   content zone   (diagram, 2-3 columns max)
y 790-880   takeaway zone  (one bold sentence, usually the last build step)
x 100-1500  safe width; keep the bottom-right corner (x>1350, y>860) clear for the step label
```

Type sizes: title 58 (auto), body 28-34, labels 22-26, takeaway 36-40. Never below 21.
Text width estimate: Latin ≈ `chars × size × 0.5`; Thai ≈ `chars × size × 0.42` (vowel marks stack), so measure long Thai lines with care and break with `\n`.
Keep on-slide words tight: roughly ≤ 25 words per slide excluding labels.

## 3. Drawing functions

All return SVG strings. Colours: `INK`, `GRAY`, `RED`, `GREEN`, and palette `C.orange|green|teal|purple|blue|red|yellow|pink`, each `{fill, line}`.

| Function | Use |
|---|---|
| `txt(x, y, s, {size, color, anchor:'start'|'middle'|'end', base:'central', w:700, mono:true})` | Text. `\n` makes lines. With `base:'central'` the block is vertically centred on y. |
| `box(x, y, w, h, label, fill, {fs, w, mono})` | Sketchy rounded box with centred label. |
| `chip(x, y, w, h, label)` | White box, 28px label. For option pills. |
| `srect(x, y, w, h, fill, r, stroke)` | Sketchy outline rect (panels, bars, windows). `fill:'none'` for outlines. |
| `rect(x, y, w, h, fill, r)` | Plain filled rect (bar fills, segments, highlights). |
| `sline(x1, y1, x2, y2, color, width)` | Hand-drawn line (underlines, strike-through). |
| `dashed(x1, y1, x2, y2, color)` | Straight dashed connector. |
| `arrow(x1, y1, x2, y2, {bend, color, dash, w})` | Curved arrow. `bend` offsets the control point along the left-hand normal of the direction of travel: for a left-to-right arrow, **negative bend bulges up**, positive bends down. For a loop drawn clockwise, use negative bends throughout so every arc bulges outward. |
| `check(x, y, size, color)` / `cross(x, y, size, color)` | Green tick / red X. |
| `doc(x, y, w, h, fill, {lines, lc:[colors]})` | Document icon with folded corner and optional scribble lines. |
| `win(x, y, w, h, label)` | Window/panel with header strip ("new session", "session 2"). |
| `bubble(x, y, w, h, text, fill, {fs, mono})` | Speech bubble with tail at bottom right. |
| `terminal(x, y, w, h, text)` | Dark command box with green mono text. |
| `stamp(x, y, label)` | Rotated green stamp ("SAVED", "APPROVED"). 150×50. |
| `meter(x, y, w, pct, fill, label)` | Progress/capacity bar with label above. |
| `badge(cx, cy, n, fill, r)` | Numbered circle. |
| `robot(cx, cy, scale)` | AI agent icon (~74×90 at scale 1). |
| `stick(x, y)` | Stick person (head at y-62, feet at y+84). |
| `sparkle(cx, cy, r, color)` | 4-point star (AI / magic / highlight). |
| `magnifier(cx, cy)` | Search / inspect icon. |
| `zigzag(x, y, w, h)` | Red scribble to cross something out. |
| `sline` + `rect` | Combine for charts: a bar = `rect` fill + `srect` outline. |

Emoji inside `txt` work (🧪 📷 📄 ⚠ 🎲) and are a cheap way to add icons.

## 4. Visual pattern library

Map the brief's "visual concept" to one of these. Each has a proven layout in `example-slides.js` (tip number in brackets).

| Message type | Pattern | Build steps |
|---|---|---|
| "One try isn't enough / consistency" | Row of repeated outputs with ✓/✗ marks + loop-back arrow [1] | single → many → loop → all pass → takeaway |
| "Add a feedback loop" | Task → Attempt → Check/Fix cycle + quality gauge [2] | naive path → loop → gauge fills → methods → takeaway |
| "Old way vs new way" | Left panel red, right panel green [6] | left → right → ticks → takeaway |
| "Don't do X, do Y" | Top row bad path with ✗, bottom row good path with ✓ [7] | bad → good → example prompt |
| "Replace A with B" | Big A on left, arrow with condition label, small B on right [8] | A → condition → B → takeaway |
| "Split and merge" | One box → N parallel lanes → merge box [9] | task → lanes → merge → takeaway |
| "Handover / continuity" | Window → note → window, with meters [10] | full → note → fresh → takeaway |
| "Capacity / budget" | Segmented horizontal bar + action chips [5] | bar → overflow → fixes → takeaway |
| "Funnel / many to one" | Grid of items → many small workers → one big box → answer [12] | items → fan out → fan in → cost bars |
| "Continuous improvement" | 4-box cycle with outward-bulging arrows, example in centre [15] | box by box, close the loop last |
| "Truth drifts / one source" | Main doc vs satellite docs with ≠, then zig-zag them out [3] | problem → fix → consequence → exception |
| "Numbers / KPI" | 2-4 big `txt` numbers (size 80-110) with small labels, or bars with `rect` | one number per step |
| "Timeline / roadmap" | Horizontal `sline` with `badge` milestones and labels above/below | milestone per step |

When nothing fits, sketch it on paper first: 1 focal object, ≤ 3 supporting objects, 1 takeaway.

## 5. Gotchas

- Each slide is seeded, so the jitter is identical in the board thumbnails and the live slide. Don't call `Math.random()`; use `rnd()` or `j()`.
- Strings containing apostrophes: use double quotes or escape (`'don\'t'`).
- `heading()` estimates title width; keep titles ≤ 38 Latin chars (≈ 30 Thai chars) or they crowd the badge.
- Build validation: `python scripts/build_deck.py slides.js out.html --title "..."` must print "All slides rendered cleanly." before you present the file.
