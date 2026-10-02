# Prompt template (fill the {braces}, delete unused lines)

Ready-to-paste skeleton for the ChatGPT / DALL-E / Midjourney / Canva prompt. Style block and text rules stay fixed; the 8 section blocks carry the user's exact words.

```
Create a premium vertical (4:5) educational infographic in {Thai|English} for {AUDIENCE}.
Topic: "{TITLE}" ({one line: what it explains and why people need it}).

STYLE
- Modern sketchnote, white background (#FFFFFF) with a light gray dot grid (#F3F4F6)
- Fonts: Prompt / Kanit (Thai), bold black title, purple subtitle
- Palette: Purple #8B5CF6, Yellow #FACC15, Blue #60A5FA, Green #4ADE80, Pink #F9A8D4
- Hand-drawn arrows, sticky notes, checkmarks, small icons. Clean and printable. Not cartoon-heavy.
- Color meaning: {e.g. red = loss, yellow = source, green = restore, blue = normal path}

STRICT TEXT RULES
- Render every text EXACTLY as written below, character by character.
- Do NOT invent, translate, shorten or add any path, command, number or name.
- Keep text blocks short. Commands go in monospace boxes.
- No passwords, keys or personal data anywhere.

LAYOUT: 8 sections stacked top to bottom

1) HOOK (largest)  Title: "{3-8 words}"  Purple subtitle: "{...}"  Tagline: "{...}"
2) BIG IDEA (one sticky note)  "{one sentence}"
3) VISUAL FLOW (arrows, no crossing)  "{step 1}" -> "{step 2}" -> ...  Red note: "{what goes wrong}"  Green arrow: "{the fix}"
4) COMPONENT CARDS ({3-5} cards, one idea each, max 3 bullets)  Card "{name}": "{b1}" / "{b2}" / "{b3}"
5) ARCHITECTURE (simple boxes + arrows)  Box: "{...}"
6) COMPARISON (max 4 columns, one takeaway)  Columns: {c1} | {c2} | {c3} | {c4}  rows...
7) DECISION FRAMEWORK (always)  Column "Choose X if...": "{...}" / "{...}" / "{...}"  Column "Choose Y if...": ...
8) SUMMARY  4-5 checkmark lines + "Best for" lines + small disclaimer "{...}"
   {optional monospace strip, verbatim: the 1-2 commands people must not get wrong}

Audience: {AUDIENCE}. Short sentences and bullets only.
```

After generating, if text is wrong, send: "Fix only the wrong text so it matches what I gave exactly, character by character. Do not change the layout."
