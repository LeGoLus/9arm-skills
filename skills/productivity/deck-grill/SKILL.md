---
name: deck-grill
description: Grill-me style interview that turns a vague "make me a presentation" into an approved, slide-by-slide layout brief before any slides are built. Asks relentlessly (one sharp question at a time) about the objective, the audience, the one message to land, the desired action, context, evidence and constraints, then writes a storyline and per-slide layout information (action title, takeaway, visual concept, layout zones, build steps, on-slide text, speaker notes) for the user to review and revise. Use this whenever the user wants to create a presentation, deck, slides, pitch, PowerPoint, training, proposal or talk, says "help me present", "ทำสไลด์", "ทำ PowerPoint", "ทำ presentation", "นำเสนอ", or shares source material (docs, video notes, screenshots) to turn into slides — even if they ask to jump straight to building. Pairs with the sketch-deck skill (hand-drawn HTML) or the pptx skill, which build from the approved brief.
---

# Deck Grill

A deck fails when it answers the wrong question for the wrong audience. This skill front-loads the thinking: interview the user until the objective, audience and message are sharp, then design the deck slide by slide on paper. Nothing gets built until the user approves the brief.

Speak in the user's language (Thai, English, or mixed as they do). Keep technical terms like "objective", "takeaway", "call to action" in English if the user mixes languages.

## Phase 0 — Mine what you already have
Before asking anything, read every source the user gave (docs, video notes, screenshots, earlier chat, a draft outline) and anything you already know about them. Write down, silently, what is already answered. Never ask a question the material already answers; instead, confirm it in one line ("From the draft, the audience is internal engineers — correct?").

## Phase 1 — Grill (interview)
Walk the question tree in `references/question-bank.md`, in this order, because later answers depend on earlier ones:

1. **Objective** — what should change after the talk? Push until it is an observable outcome: decide, approve, buy, adopt, learn to do X. "Inform them about X" is not an objective; ask "and then what should they do?"
2. **Audience** — who exactly, what they already know, what they care about, what they'll object to, who decides.
3. **Core message** — the one sentence they should repeat afterwards. If the user can't say it in one sentence, keep grilling; the deck isn't ready.
4. **Desired action / call to action** — the specific next step, owner and date if relevant.
5. **Context** — live or sent-as-reading, duration, setting, language, tone, presenter.
6. **Content & evidence** — key points, data, examples, stories, what must be included, what must NOT.
7. **Format & constraints** — slide count, style (hand-drawn sketch-deck / corporate PPTX / both), brand, deadline.
8. **Success criteria** — how will the user know the presentation worked?

How to grill:
- Ask **one sharp question at a time** (a small related group of 2-3 at most). On mobile, use the tappable options tool when the answer is a choice; use free text for anything that needs the user's words.
- For every question, offer your recommended answer or 2-3 concrete options based on what you've learned, so the user can just confirm. Grilling should feel fast, not like a form.
- Don't accept vague answers. "Everyone" as an audience, "show the benefits" as a message, "it depends" — ask what it depends on, who specifically, which benefit matters most to them.
- Name conflicts you notice (e.g. 20 slides in a 10-minute slot; a technical deep-dive for executives who need a decision) and make the user choose.
- Typical depth: 8-15 questions for a short internal deck, 20-40 for a client pitch or high-stakes talk. Stop when the stop test passes, not at a number.

**Stop test** — move on only when you can fill every field of the Brief Summary in `references/brief-template.md` with specifics, and the user has confirmed the objective and core message in their own words.

## Phase 2 — Storyline
Propose the arc before any slide detail. Pick the structure that fits the objective (see `references/brief-template.md` → Storyline patterns), then write the deck as a list of **action titles** — full-sentence headlines that together tell the whole story if read alone. Show the list and get a yes, a reorder, or cuts. Check the time budget (≈1-2 min per content slide live; fewer words, more slides for sketch decks).

## Phase 3 — Slide-by-slide layout information
For each approved headline, write the per-slide block from `references/brief-template.md`: role in the story, objective link, takeaway, visual concept (named pattern), layout zones, build steps, exact on-slide text, speaker notes, evidence, and the audience lens (which concern or objection it addresses).

Then add the **Objective traceability** table: every slide maps to the objective or a sub-message; any slide that maps to nothing gets flagged for cutting.

Save the whole brief as `/mnt/user-data/outputs/deck-brief.md` (markdown, not docx — it will be edited repeatedly) and present it. In chat, show a short summary: the core message, the headline list, and the 2-3 decisions you're least sure about.

## Phase 4 — Review loop
Ask for feedback on the brief. Revise the file with each round (edit, don't regenerate from scratch) and note what changed. Common revisions: tighten a headline, swap a visual pattern, move a slide, cut for time, adjust tone for the audience.

## Phase 5 — Hand-off (only after explicit approval)
When the user says the brief is good ("โอเค", "ผ่าน", "approved", "go ahead"), confirm the output format and hand off:
- **Hand-drawn, step-building HTML** → follow the sketch-deck skill using `deck-brief.md` as input.
- **Editable PowerPoint** → follow the pptx skill, mapping each build step to a slide or animation.
- Both is fine; build the one they'll present from first.

Do not start building slides during Phases 1-4, even if asked mid-interview; explain in one line that locking the brief first is what makes the deck land, and offer to fast-track by accepting your recommended answers for the remaining questions.
