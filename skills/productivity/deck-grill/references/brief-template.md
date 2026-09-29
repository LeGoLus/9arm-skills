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
| Style | talk (takeaway line + ≤25 words) \| pitch-minimal (title + short labels, no takeaway line, detail in notes) |
| Success looks like | |

## 2. Storyline
Pattern: <chosen pattern>
1. <Action title slide 1>
2. <Action title slide 2>
...
Time budget: <N> slides × ~<M> min = <total> (slot: <minutes>)

## 2b. Format preview (show BEFORE the slide details; user approves the look here)
One row per slide, so the user knows the output shape in advance:
```
#  Title                          Pattern            Theme   Steps  Images
1  TOR เดิมมีแค่ 2 เฟส            old-vs-new         red     4      –
2  เฟสหลัก ก่อนถึง CAAT           milestone timeline blue    5      –
6  การวางกล้อง Best/Base          image slot         teal    5      4 (1240×640)
```
Plus one ASCII sketch per distinct pattern (boxes/arrows as they will look). State the fixed rules: 1600×900 canvas, editor-native shapes only, images = dashed slots filled later, notes hold the detail.

## 3. Slide-by-slide layout information

### Slide <N>: <Action title — full sentence>
- **Role in story:** hook | problem | stakes | insight | solution | proof | how | objection | ask | recap
- **Objective link:** <which supporting point / the objective itself>
- **Takeaway:** <one sentence the audience remembers>
- **Visual concept:** <pattern name from the sketch-deck library, or chart/table/photo> — <one-line description>
- **Pattern / Theme:** <pattern name from the sketch-deck library, e.g. old-vs-new> / <red|orange|yellow|green|teal|blue|purple|pink>
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
  (3-5 steps; talk style: last step reveals the takeaway; pitch-minimal: last step is the last idea, no takeaway line)
- **Image slots:** none | per step: `step <k>: <what it shows> · 1240×640 · source: screenshot | ChatGPT prompt: "<prompt>" | photo` (the user supplies these; the slot is a dashed frame until filled)
- **On-slide text (exact):** <≤ ~25 words, excluding labels>
- **Speaker notes:** <2-4 sentences; in pitch-minimal ALL the detail cut from the slide goes here>
- **Evidence / source:** <data, citation, example — or MISSING>
- **Audience lens:** <which concern or objection this slide answers>

(repeat per slide)

## 4. Objective traceability
| Slide | Supports | If cut, what's lost? |
|---|---|---|

## 4b. Image list
| Slide/step | Shows | Size | Source / ChatGPT prompt | Status |
|---|---|---|---|---|

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
repeat-and-check row · feedback loop + gauge · old vs new panels · bad path / good path rows · A → B replacement · split & merge lanes · handoff (window → note → window) · capacity bar + fixes · fan-out / fan-in funnel · improvement cycle · one source vs drifting copies · big numbers · timeline · milestone timeline (badges + gate stamp) · milestone hub (→ MVP → optional) · hub-and-spoke · image slot · two-box ask. For PPTX, also: chart (bar/line), table, photo + caption, quote.
