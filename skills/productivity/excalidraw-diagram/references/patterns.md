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

## Icon nodes ("explain it like a talk slide")

Makes a flow readable in two seconds: the icon says *what kind of thing*, the label says *which one*.

- **Node = circle + icon + label below + 1–3 detail lines.** Hero circles 90×90, inner-loop circles 64×64.
  The circle carries `"customData": {"icon": "<name>"}`; `scripts/icons.py` draws the Lucide icon inside in the
  circle's stroke color. Names: `uv run python icons.py --list` (user, users, bot, brain, split, target, zap,
  monitor, search, git-merge, git-pull-request, flask-conical, rocket, eye, database, server, cloud, mail, …).
- **Pick the icon from the role, not decoration**: person → `user`, split work → `split`, pick/goal → `target`,
  build/ship → `zap`, check UI → `monitor`, review → `search`, merge → `git-merge`, test → `flask-conical`,
  release → `rocket`, watcher/manager agent → `eye` or `bot`. Same icon = same meaning across the picture.
- Labels and details are **free text under the circle** (not bound to it), centred on the circle's x.
- **One container** for the core loop/system, its name top-left inside ("The loop"), a side note top-right with a
  small icon circle (e.g. the agent that watches it), a one-line caption at the bottom inside.
- **Feedback arrow** leaves from under a node and returns into the container with an elbow route; label it with
  what is fed back.
- **Part brackets** at the bottom: a thin `line` whose end-ticks point **up** toward the nodes it groups, like `└──┘`
  (`[[0,0],[0,10],[w,10],[w,0]]`), under each phase, label centred below ("Part 1 · Plan and split").
- Last node of the success path in green (input/success role `#047857`); arrows into it green too.
- **Lines never cross text.** Route a feedback arrow over the top of the row (labels sit under the circles), keep
  arrow labels ≥ 8 px off the line, and render with `--strict`: it lists every line that crosses a text box.
- Budget: ≤ 9 icon nodes. More → split into overview + zoom.
