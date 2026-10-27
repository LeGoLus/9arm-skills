# 00 · แผนที่ Skills ทั้งหมด (เปิดหน้านี้ก่อน)

> ไฟล์นี้ไม่มีรหัสผ่าน, token หรือข้อมูลส่วนตัว นำไปวางใน ChatGPT, Canva หรือ Gamma ได้
> ที่มาของข้อมูล: `catalog.json`, `SKILL.md` ทุกตัว และประวัติ Claude Code ในเครื่องนี้ (นับเมื่อ 2026-10-23)

## จำเร็ว: เจอสถานการณ์ไหน เปิดหน้าไหน

| สถานการณ์ | เปิดหน้า | Skill ตัวแรกที่ควรเรียก |
|---|---|---|
| มีไอเดีย/แผน แต่ยังไม่ชัด | [01 Grill](01-plan-grill.md) | `grill-me` (โปรเจกต์ใหม่) · `grill-with-docs` (มี `src/` หรือ `CONTEXT.md`) |
| แผนชัดแล้ว ต้องแตกเป็นงาน | [02 แผน → ลงมือ](02-plan-execute.md) | `writing-plans` → `executing-plans` |
| กำลังเขียนโค้ด | [03 สร้างให้มีคุณภาพ](03-build-quality.md) | `tdd` |
| เจอบั๊ก หรือของพัง | [04 Debug](04-debug-investigate.md) | `systematic-debugging` |
| จะ commit, เปิด PR หรือ merge | [05 Git](05-git-ship.md) | `git-workflow` |
| ต้องทำรูป, เอกสาร หรือสไลด์ | [06 ภาพ + เอกสาร](06-visual-docs.md) | `excalidraw-diagram` |
| ให้ AI ทำงานแทน หรือคุมหน้าจอ | [07 Agent + Automation](07-agents-automation.md) | `drive-screen` · `subagent-driven-development` |
| สร้างหรือแก้ skill เอง / เรื่องส่วนตัว | [08 Meta + Personal](08-meta-personal.md) | `writing-skills` |
| ลืมคำสั่ง `/` | [09 Commands](09-commands.md) | `/model` · `/compact` · `/plan` |

**Tier คืออะไร** (จาก `tier-manifest.yaml`)
- **Tier 0** โหลดทุกโปรเจกต์ผ่าน `~/CLAUDE.md`: `systematic-debugging`, `git-workflow`, `grill-me`, `grill-with-docs`
- **Tier 1** แกนหลักของงานโค้ด: `tdd`, `code-review`, `error-handling`, `verification-before-completion`, `writing-plans`, `executing-plans`, `strategic-compact`, `verification-loop`
- **Tier 2** งาน AI หรือ agent: `subagent-driven-development`, `dispatching-parallel-agents`, `prompt-engineer`, `agentic-eval`, `continuous-learning`, `security-review`
- **Tier 3** เรียกเมื่อใช้ ไม่ได้โหลดไว้ล่วงหน้า: ตัวอื่นทั้งหมด

**ใช้บ่อยที่สุดจากประวัติ** (นับ session ที่เรียกใช้): `excalidraw-diagram` 6 · `grill-with-docs` 4 · `docx` 3 · `grill-me` · `infographic-one-page` 2
ส่วน `drive-screen` และ `tdd` เป็นตัวที่คุณบอกว่าใช้แล้วดี

**ตัวที่ต้องพิมพ์เรียกเอง** (Claude ไม่เรียกให้อัตโนมัติ): `/teach`, `/wayfinder`, `/to-tickets`, `/writing-great-skills`

---

## Prompt สำหรับทำภาพ (คัดลอกตั้งแต่ ---เริ่ม--- ถึง ---จบ---)

---เริ่ม---

Create a premium vertical (4:5) educational infographic in Thai for a developer who uses Claude Code every day.
Topic: "54 Skills จำยังไง?" (a map of the 9arm-skills library: which page to open for which situation).

STYLE
- Modern sketchnote, white background (#FFFFFF) with a light gray dot grid (#F3F4F6)
- Fonts: Prompt / Kanit (Thai), bold black title, purple subtitle
- Palette: Purple #8B5CF6, Yellow #FACC15, Blue #60A5FA, Green #4ADE80, Pink #F9A8D4
- Hand-drawn arrows, sticky notes, checkmarks, small icons. Clean and printable. Not cartoon-heavy.
- Skill names always in a small monospace pill.
- Color meaning: purple = think/plan · blue = build · pink = debug · green = verify/ship · yellow = key takeaway

STRICT TEXT RULES
- Render every Thai and English text EXACTLY as written below, character by character.
- Do NOT invent, translate, shorten or add any skill name, command, path or number.
- Keep text blocks short. Commands go in monospace boxes.
- No passwords, keys or personal data anywhere.

LAYOUT: 8 sections stacked top to bottom

1) HOOK (largest)
   Title: "54 Skills จำยังไง?"
   Purple subtitle: "เลือกจากสถานการณ์ ไม่ใช่จากชื่อ"
   Tagline: "คิด → ทำ → ตรวจ → ส่ง"

2) BIG IDEA (one yellow sticky note)
   "ถามก่อนสร้าง · เทสก่อนเขียน · ตรวจก่อนบอกว่าเสร็จ"

3) VISUAL FLOW (left to right, 5 numbered steps, no crossing arrows)
   "① คิด: grill-me" -> "② แตกงาน: writing-plans" -> "③ เขียน: tdd" -> "④ พัง: systematic-debugging" -> "⑤ ส่ง: git-workflow"
   Red note: "ข้าม ① = สร้างของผิดตั้งแต่แรก"
   Green arrow (from ⑤ back to ①): "ไม่แน่ใจ → grill ก่อนเสมอ"

4) COMPONENT CARDS (4 cards, max 3 bullets)
   Purple card "Tier 0 · โหลดทุกโปรเจกต์": "grill-me" / "grill-with-docs" / "systematic-debugging · git-workflow"
   Blue card "Tier 1 · แกนงานโค้ด": "tdd · code-review" / "writing-plans · executing-plans" / "verification-loop"
   Pink card "Tier 2 · งาน AI/agent": "subagent-driven-development" / "prompt-engineer · agentic-eval" / "security-review"
   Green card "Tier 3 · เรียกเมื่อใช้": "excalidraw-diagram · drive-screen" / "deck-grill · sketch-deck" / "อีก 30+ ตัว"

5) ARCHITECTURE (simple boxes + arrows)
   Box "GitHub: 9arm-skills" -> Box "link-skills.sh" -> Box "~/.claude/skills/" -> Box "Claude Code อ่าน SKILL.md"

6) COMPARISON (table, 3 columns, 6 rows) — title "เปิดหน้าไหน"
   Columns: สถานการณ์ | หน้า | ตัวแรก
   "แผนยังไม่ชัด" | "01" | "grill-me"
   "แตกงาน" | "02" | "writing-plans"
   "เขียนโค้ด" | "03" | "tdd"
   "เจอบั๊ก" | "04" | "systematic-debugging"
   "ทำรูป/เอกสาร" | "06" | "excalidraw-diagram"
   "คุมจอ/agent" | "07" | "drive-screen"

7) DECISION FRAMEWORK (two columns)
   Green column "เรียก skill ถ้า…": "✅ งานมีหลายขั้น" / "✅ พลาดแล้วแก้ยาก" / "✅ ทำซ้ำบ่อย"
   Blue column "ไม่ต้องเรียก ถ้า…": "✅ ถามข้อเท็จจริงสั้นๆ" / "✅ แก้บรรทัดเดียว" / "✅ งานทำครั้งเดียวจบ"

8) SUMMARY
   "✅ ไม่แน่ใจ → grill-me"
   "✅ มีโค้ดแล้ว → grill-with-docs"
   "✅ ก่อนเขียนโค้ด → tdd"
   "✅ ก่อนบอกว่าเสร็จ → verification-before-completion"
   "✅ ทุกเอกสาร → excalidraw-diagram"
   "Best for: ใช้ Claude Code ทุกวัน"
   Monospace strip (render verbatim, 1 line):
   bash ~/9arm-skills/scripts/link-skills.sh
   Footer (small): "หน้า 00 จาก 09 · ดูรายละเอียดแต่ละกลุ่มในหน้า 01-09"

Audience: Thai developer who uses Claude Code every day. Short sentences and bullets only.

---จบ---
