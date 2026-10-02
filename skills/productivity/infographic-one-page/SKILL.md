---
name: infographic-one-page
description: Turn any topic, procedure, comparison or set of notes into a one-page (4:5) sketchnote infographic, delivered as a copy-paste image-generation prompt (ChatGPT / DALL-E / Midjourney / Canva) built on the 8-section Tech-Infographic-Design-System (Hook, Big Idea, Visual Flow, Component Cards, Architecture, Comparison, Decision Framework, Summary). Use this whenever the user says "ทำ infographic", "infographic 1 หน้า", "one page", "สร้างรูปภาพสรุป", "prompt ให้ ChatGPT generate", "ทำเป็นภาพให้จำง่าย", or wants a manual, cheat sheet or explainer condensed into a single memorable picture — even if they don't name the template. Also use when they want it as a local HTML/PNG instead of an AI-generated image.
---

# Infographic One Page

Condenses a topic into one picture people can remember and find fast. Output is a ready-to-paste prompt (and optionally a local HTML/PNG), never a wall of prose. Speak the user's language (Thai/English mixed is normal).

Design source of truth: `~/LifeVault/20-Areas/AI-Workflow/Tech-Infographic-Design-System.md` (palette, typography, 8 sections). Prompt skeleton: `references/prompt-template.md`. Worked example (real, used): `references/example-exercise-lde.md`.

## Workflow

1. **Mine the source first.** Read whatever the user gave (files, PDFs, chat, notes). Don't ask what the material already answers.
2. **Find the one idea.** Write the single sentence the reader must remember (becomes ② BIG IDEA) and a 3-8 word hook (①). If you can't, ask one sharp question: "ถ้าคนจำได้ประโยคเดียว ควรเป็นอะไร?" Offer your best guess to confirm.
3. **Map content to the 8 sections** (below). Be strict: short lines, max 3 bullets per card, 3-5 cards, max 4 comparison columns. Cut anything that is not needed to act.
4. **Write the prompt file** from `references/prompt-template.md`, saved next to the source material as `chatgpt_infographic_prompt.md` (or under the project's docs folder). Put exact on-image text inside quotes. Add a `{name}.md` template version only if the user wants the human-readable layout too.
5. **Deliver.** Send the prompt file, state plainly that you cannot generate the image yourself unless an image tool is connected, and offer a local HTML/PNG render (correct Thai and commands) as the no-garble option.

## The 8 sections

| # | Section | Rule |
|---|---------|------|
| 1 | HOOK | 3-8 words, largest type, plus a purple subtitle and a tagline carrying the rule to remember |
| 2 | BIG IDEA | one sentence, one sticky note |
| 3 | VISUAL FLOW | 3-5 numbered steps, one direction, no crossing arrows; red note = what goes wrong, green arrow = the fix |
| 4 | COMPONENT CARDS | one idea per card, max 3 bullets, pastel fill, small icon |
| 5 | ARCHITECTURE | simple boxes and arrows, minimal text, system relationships only |
| 6 | COMPARISON | table, max 4 columns, one takeaway; a small orange box for common failures if relevant |
| 7 | DECISION FRAMEWORK | always include: "Choose X if..." / "Do A if..." columns, 3 checkmarks each. This is the differentiator; never drop it |
| 8 | SUMMARY | 4-5 checkmark lines, "Best for", small disclaimer, optional monospace command strip |

Color meaning must be stated in the prompt (e.g. red = loss, yellow = source, green = fix/safe, blue = normal). Default palette: Purple `#8B5CF6`, Yellow `#FACC15`, Blue `#60A5FA`, Green `#4ADE80`, Pink `#F9A8D4`; white background with `#F3F4F6` dot grid; Prompt / Kanit fonts; hand-drawn arrows, sticky notes, checkmarks, not cartoon-heavy.

## Hard rules

- **Never put secrets in the prompt** — passwords, tokens, keys, personal data. The prompt leaves your machine. Say in the file header that none are included.
- **Internal systems**: hostnames and paths are fine only if the user is already taking the prompt to an external tool themselves; otherwise confirm before sending content to any third-party generator (Canva, Gamma, etc.).
- **Image models garble Thai and long paths/commands.** Keep on-image text short. If a command must appear, put at most 1-2 lines in a monospace strip, tell the model to render it verbatim, and tell the user to check it character by character. Long commands belong in a separate text page that travels with the picture.
- **Exact text, no invention**: the prompt must forbid the model from adding or rewording paths, commands or numbers.
- **Unverified facts stay flagged.** If the source was ambiguous (handwriting, mixed manuals), list the open questions in the final message and in the footer disclaimer ("ตรวจกับเครื่องจริงก่อนใช้"); don't present guesses as fact.
- One idea per card; one picture per topic. If the topic needs more than a page, split into two prompts rather than shrinking the type.

## Local render option (no garbled text)

When the user wants correct text, build a single self-contained HTML (Sarabun/Prompt via Google Fonts link with a fallback stack, inline CSS, same palette and 8 sections, `@page` set for print) and export PNG/PDF from the browser. Keep the 4:5 ratio (e.g. 1080x1350) for social, or A4 portrait for printing at a workstation.

## Related

- `deck-grill`, `sketch-deck`: when the output should be slides, not one picture.
- `grill-with-docs`: build a shared glossary first when the source uses inconsistent terms (do this before step 3).
