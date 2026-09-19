# Pick the picture from the content

Ask "what does this thing *do*?" then draw that motion. If deleting every word still leaves the structure
recognisable (a loop still looks like a loop), the pattern is right.

| The content is… | Draw it as | Notes |
|---|---|---|
| a sequence of steps | left→right (or top→bottom) chain of boxes | ≤ 6 steps per row; wrap into rows |
| a branch / rule | diamond with labelled exits (yes/no, A/B) | every exit must lead somewhere |
| one thing producing many | fan-out: one source, arrows to targets | |
| many things merging | fan-in / funnel to one target | |
| a loop / feedback | boxes in a ring, arrow returning to start | label what is fed back |
| who talks to whom over time | swim-lanes: one column per actor, arrows down the time axis | |
| levels / stack | horizontal layers, biggest ground at the bottom | |
| containment / scope | nested zones (dashed rounded rectangles) | |
| before vs after / A vs B | two columns, same row order, contrasting colors | |
| dates / phases | horizontal line with dots, labels above/below | text needs no box |
| hierarchy | tree from lines + free text | boxes only for the root |
| what data looks like | dark code card next to the box that produces it | use real field/event names |

## Depth: how much to draw

- **Concept** (mental model, explaining to a non-technical reader): abstract shapes, ≤ 8 nodes, generic labels are OK.
- **Technical** (real system, protocol, workflow someone will follow): real names, real values, at least one concrete
  example card (payload, command, sample row). Look the facts up first — never invent endpoints, fields or numbers.
- A diagram in a document should carry **one** message. If it needs more than ~12 nodes, split it into two pictures
  (overview + zoom) instead of shrinking the text.

## Composition

- Overview strip on top or bottom (one line: A → B → C), detail sections below it, grouped by zone.
- Leave the most whitespace around the most important element; make it the largest.
- Sizes: hero 280×140, primary 180×80, secondary 120×60, marker 12. Grid of 20; gaps ≥ 60 between boxes.
- Containers only when they mean something (a step, a system, a decision). Titles, captions and notes are plain text.
- Every relationship is an arrow or a line; proximity alone is not a relationship.
- Vary the pattern between sections; a wall of identical cards reads as a list, not a picture.
