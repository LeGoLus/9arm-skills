# Deck brief template

Use this exact structure for `deck-brief.md`. The sketch-deck and pptx skills read it as their input, so keep the headings stable.

````markdown
# Deck Brief: <working title>
Version: v<N> · Status: DRAFT | APPROVED · Format: sketch-deck HTML | PPTX | both

## 1. Brief summary
| Field | Answer |
|---|---|
| Objective (observable outcome) | |
| Primary audience (persona) | |
| What they care about most | |
| Main objection to address | |
| Core message (one sentence) | |
| Supporting points (2-4) | |
| Call to action | |
| Context (live/read, minutes, setting) | |
| Language and tone | |
| Must include / must avoid | |
| Constraints (slide count, brand, deadline) | |
| Success looks like | |

## 2. Storyline
Pattern: <chosen pattern>
1. <Action title slide 1>
2. <Action title slide 2>
...
Time budget: <N> slides × ~<M> min = <total> (slot: <minutes>)

## 3. Slide-by-slide layout information

### Slide <N>: <Action title — full sentence>
- **Role in story:** hook | problem | stakes | insight | solution | proof | how | objection | ask | recap
- **Objective link:** <which supporting point / the objective itself>
- **Takeaway:** <one sentence the audience remembers>
- **Visual concept:** <pattern name from the sketch-deck library, or chart/table/photo> — <one-line description>
- **Layout:**
  ```
  [Title zone]   badge <N> + "<title>"
  [Left]         ...
  [Centre]       ...
  [Right]        ...
  [Bottom]       takeaway line
  ```
- **Build steps:**
  1. <what appears first + what the presenter says>
  2. ...
  (3-5 steps; last step usually reveals the takeaway)
- **On-slide text (exact):** <≤ ~25 words, excluding labels>
- **Speaker notes:** <2-4 sentences>
- **Evidence / source:** <data, citation, example — or MISSING>
- **Audience lens:** <which concern or objection this slide answers>

(repeat per slide)

## 4. Objective traceability
| Slide | Supports | If cut, what's lost? |
|---|---|---|

## 5. Open questions and risks
- <anything unresolved, missing evidence, assumptions made>

## 6. Change log
- v1: first draft
````

## Storyline patterns

Pick by objective; say why in one line.

| Objective | Pattern | Arc |
|---|---|---|
| Get a decision / approval | **SCR / SCQA** | Situation → Complication → (Question) → Resolution → Ask |
| Persuade to change behaviour | **Problem → Stakes → Solution → Proof → Ask** | pain first, then relief |
| Teach a skill | **Lessons list** (like "15 things I learned") | hook → lesson × N (each: problem → rule → example) → recap |
| Pitch a product/idea | **Before → After → Bridge** | world today → world with it → how we get there → ask |
| Status / progress update | **Answer first (pyramid)** | headline result → 3 drivers → risks → next steps |
| Explain a system / architecture | **Zoom in** | big picture → components → one flow end-to-end → edge cases |
| Inspire / keynote | **What is → What could be** (contrast) | alternate reality/ideal, end on the new bliss |

## Action title rules
- Full sentence with a verb and a point of view: "Checking its own work doubles Claude's first-pass quality", not "Verification".
- Read all titles in order: they alone should tell the story.
- One idea per slide. If a title needs "and", consider two slides.

## Visual concept vocabulary (for the sketch-deck skill)
repeat-and-check row · feedback loop + gauge · old vs new panels · bad path / good path rows · A → B replacement · split & merge lanes · handoff (window → note → window) · capacity bar + fixes · fan-out / fan-in funnel · improvement cycle · one source vs drifting copies · big numbers · timeline. For PPTX, also: chart (bar/line), table, photo + caption, quote.
