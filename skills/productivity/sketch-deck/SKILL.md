---
name: sketch-deck
description: Build hand-drawn, whiteboard-style interactive presentations (Excalidraw look, sketchy boxes and arrows, diagrams that build up step by step, and a "reveal board" overview between slides) as a single HTML file that works on phone and desktop. Use this whenever the user wants slides "like that YouTube video", a sketch / whiteboard / doodle / Excalidraw-style deck, animated step-by-step diagrams, a teaching or explainer presentation, or when a deck-grill slide brief has been approved and it is time to build. Also use when the user shares screenshots of hand-drawn slides and asks to make the same kind of presentation. If the user needs an editable .pptx instead, still use this skill's brief-to-layout rules, then hand the layout to the pptx skill.
---

# Sketch Deck

Turns an approved slide brief into a hand-drawn, step-building HTML presentation. The engine (drawing kit, step builds, reveal board, tap/keyboard/swipe navigation, fullscreen) is already written in `assets/engine.html`; your job is to write `slides.js` — the content and coordinates — and build.

## Workflow

### 1. Get the brief first
Look for an approved brief from the **deck-grill** skill (usually `deck-brief.md` in outputs or earlier in the chat). The brief gives, per slide: action title, takeaway, visual concept, layout zones, build steps and on-slide text. Follow it; don't invent a different storyline.

If there is no brief:
- For anything client-facing, high-stakes, or longer than ~5 slides, say so and run the deck-grill interview first. A pretty deck with the wrong message is the most expensive failure.
- If the user explicitly wants to skip it, ask just the three essentials (objective, audience, core message) and write a compact brief yourself before drawing.

### 2. Plan each slide on paper before coding
Read `references/primitives.md` (API, canvas zones, pattern library). For each slide decide:
- the pattern from the library that best carries the takeaway,
- 3-5 build steps, where each step adds one idea the presenter will say out loud,
- the final step: usually the one-sentence takeaway in the bottom zone.

Look at `references/example-slides.js` for working coordinates of every pattern; adapting a proven layout is faster and cleaner than starting from blank.

### 3. Write slides.js
- Slide 0 is a title slide (no `n/t/c`). Add section slides the same way if the deck has chapters.
- Use the palette consistently: give each section or idea family its own colour, and keep RED for problems and GREEN for solutions throughout.
- Keep on-slide text short; the detail lives in speaker notes (give those to the user in the brief or a separate notes file, not on the slide).
- Match the audience's language. Thai text renders in the Itim hand-drawn font automatically; break long Thai lines with `\n`.
- Set `CONFIG.stepLabel` to fit the deck ("tip", "step", "ข้อ", "slide"), and `board:false` for decks where a reveal board would feel gimmicky (e.g. executive updates).

### 4. Build and validate
```bash
python scripts/build_deck.py /home/claude/slides.js /mnt/user-data/outputs/<name>.html --title "<Deck title>"
```
Fix every ERROR and any WARN that is real. Then re-read two or three slides' coordinates against the zone map for overlaps (text crossing arrows, labels running into the gauge, captions under the step label). The validator can't see overlaps; you can.

### 5. Deliver
Present the HTML file. In the reply, keep it short: how to navigate (tap right/left or → ←, B board, F fullscreen), any slide where you deviated from the brief and why, and the offer of a .pptx export (static: one slide per build step) via the pptx skill.

## Quality bar
- Every slide has exactly one takeaway, and the final build step makes it explicit.
- A stranger scrolling the board view can follow the story from thumbnails alone.
- No text below 21px, nothing outside the safe area, no overlapping labels.
- The deck serves the brief's objective: if a slide doesn't move the audience toward the desired action, cut or merge it and tell the user.
