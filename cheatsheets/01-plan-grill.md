# 01 · คิดให้ชัดก่อนลงมือ (Grill + Planning)

> ไฟล์นี้ไม่มีรหัสผ่าน, token หรือข้อมูลส่วนตัว

## จำเร็ว

| Skill | ใช้เมื่อ | เรียกยังไง | ได้อะไรออกมา |
|---|---|---|---|
| `grill-me` ★ Tier 0 | มีไอเดียหรือแผน แต่ยังไม่มีโค้ด | `/grill-me <แผน>` หรือพิมพ์ "grill me" | ถามทีละข้อ อย่างน้อย 10 ข้อ จนเข้าใจตรงกัน แล้วสรุปแผนให้ยืนยัน |
| `grill-with-docs` ★ Tier 0 | โปรเจกต์มี `src/` หรือ `CONTEXT.md` แล้ว | `/grill-with-docs` | grill แผนเทียบกับคำศัพท์และเอกสารเดิม แล้วอัปเดต `CONTEXT.md` และ ADR ไปพร้อมกัน |
| `grilling` | อยาก stress-test ความคิดหรือการตัดสินใจ (ไม่ต้องเป็นโค้ด) | "grill this decision" | ถามแบบไม่ปล่อยผ่าน ใช้ได้กับทุกเรื่อง |
| `domain-modeling` | คำศัพท์ในทีมหรือในโค้ดเริ่มสับสน | "sharpen the domain model" | `CONTEXT.md` (glossary) + ADR |
| `scrutinize` | อยากให้มองแบบคนนอก ก่อนอนุมัติแผนหรือ PR | `/scrutinize` | ถามว่าทำไปเพื่ออะไร, มีทางที่ง่ายกว่าไหม, แล้วไล่โค้ดจริงว่าทำได้ตามที่บอกหรือเปล่า |
| `write-a-prd` | grill จบแล้ว อยากได้เอกสารความต้องการ | `/write-a-prd` | PRD ที่มีเป้าหมาย, ข้อจำกัด, เกณฑ์ความสำเร็จ และงานย่อยที่บอกว่าอะไรต้องรออะไร |
| `prototype` | ยังไม่แน่ใจว่า logic หรือ UI แบบไหนดี | "prototype this" | ของทดลองที่ตั้งใจทิ้ง ใช้ตอบคำถามเรื่องดีไซน์ |

**กฎเลือกอัตโนมัติ** (จาก `~/CLAUDE.md`): ถ้ามี `src/` หรือ `CONTEXT.md` → `grill-with-docs` · ถ้าไม่มี → `grill-me`

**จบเมื่อไร:** Claude อธิบายแผนกลับมาได้ และคุณตอบว่า "ใช่ ตามนี้เลย", ระบุครบแล้วว่างานไหนต้องรองานไหน, คุยเรื่อง edge case แล้ว และตกลงกันแล้วว่าอะไรอยู่ในขอบเขต

---

## Prompt สำหรับทำภาพ

---เริ่ม---

Create a premium vertical (4:5) educational infographic in Thai for a developer who uses Claude Code every day.
Topic: "Grill ก่อน Build" (which planning skill to use before writing any code).

STYLE
- Modern sketchnote, white background (#FFFFFF) with a light gray dot grid (#F3F4F6)
- Fonts: Prompt / Kanit (Thai), bold black title, purple subtitle
- Palette: Purple #8B5CF6, Yellow #FACC15, Blue #60A5FA, Green #4ADE80, Pink #F9A8D4
- Hand-drawn arrows, sticky notes, checkmarks, small icons. Clean and printable. Not cartoon-heavy.
- Skill names always in a small monospace pill.
- Color meaning: purple = questions/planning · yellow = key takeaway · green = agreed plan · pink = warning

STRICT TEXT RULES
- Render every Thai and English text EXACTLY as written below, character by character.
- Do NOT invent, translate, shorten or add any skill name, command, path or number.
- Keep text blocks short. Commands go in monospace boxes.
- No passwords, keys or personal data anywhere.

LAYOUT: 8 sections stacked top to bottom

1) HOOK (largest)
   Title: "Grill ก่อน Build"
   Purple subtitle: "ถามให้สุด ก่อนเขียนบรรทัดแรก"
   Tagline: "ไม่มีโค้ด → grill-me · มีโค้ด → grill-with-docs"

2) BIG IDEA (one yellow sticky note)
   "คำถามที่ไม่ได้ถามวันนี้ = บั๊กที่ต้องแก้พรุ่งนี้"

3) VISUAL FLOW (top to bottom, 4 numbered steps)
   "① เล่าแผนคร่าวๆ" -> "② Claude ถามทีละข้อ (10+ ข้อ)" -> "③ ตอบให้ชัด ไม่ตอบ 'แล้วแต่'" -> "④ สรุปแผน → ยืนยัน"
   Red note: "ตอบ 'แล้วแต่' = ยังไม่ได้ตัดสินใจ"
   Green arrow: "ถามกลับ: แล้วแต่อะไร?"

4) COMPONENT CARDS (4 cards, max 3 bullets)
   Purple card "grill-me": "ไอเดียใหม่ ยังไม่มีโค้ด" / "ถามทีละข้อ 10+ ข้อ" / "ได้: แผนที่ยืนยันแล้ว"
   Blue card "grill-with-docs": "มี src/ หรือ CONTEXT.md" / "เทียบกับศัพท์ของโปรเจกต์" / "ได้: CONTEXT.md + ADR"
   Pink card "scrutinize": "มุมคนนอก ก่อนอนุมัติ" / "มีทางที่ง่ายกว่าไหม?" / "ไล่โค้ดจริง ไม่ใช่แค่ diff"
   Green card "write-a-prd": "หลัง grill จบ" / "เป้าหมาย + เกณฑ์สำเร็จ" / "งานย่อย + ลำดับที่ต้องรอ"

5) ARCHITECTURE (simple boxes + arrows, left to right)
   "ไอเดีย" -> "grill-me / grill-with-docs" -> "write-a-prd" -> "writing-plans (หน้า 02)"
   Side box under grill-with-docs: "domain-modeling → CONTEXT.md"

6) COMPARISON (table, 4 columns)
   Columns: Skill | ใช้เมื่อ | เขียนไฟล์ไหม | ผลลัพธ์
   "grill-me" | "ยังไม่มีโค้ด" | "ไม่" | "แผนที่ตกลงกัน"
   "grill-with-docs" | "มีโค้ด/เอกสาร" | "CONTEXT.md, ADR" | "แผน + ศัพท์ตรงกัน"
   "grilling" | "เรื่องอะไรก็ได้" | "ไม่" | "ความคิดที่ผ่านการทดสอบ"
   "prototype" | "ดีไซน์ยังไม่ลงตัว" | "โค้ดทิ้งได้" | "คำตอบเรื่องดีไซน์"
   Small orange box "พลาดบ่อย": "ข้าม grill เพราะคิดว่างานเล็ก" / "ตอบกว้างๆ ไม่ระบุตัวเลข"

7) DECISION FRAMEWORK (two columns)
   Purple column "ใช้ grill-me ถ้า…": "✅ เริ่มโปรเจกต์ใหม่" / "✅ ยังไม่มี src/" / "✅ ขอบเขตยังไม่ชัด"
   Blue column "ใช้ grill-with-docs ถ้า…": "✅ มี src/ หรือ CONTEXT.md" / "✅ คำศัพท์ในทีมเริ่มสับสน" / "✅ อยากได้ ADR ไว้อ้างอิง"

8) SUMMARY
   "✅ grill จบเมื่อพูดได้ว่า 'ใช่ ตามนี้เลย'"
   "✅ ระบุว่างานไหนต้องรองานไหนให้ครบ"
   "✅ คุยเรื่อง edge case ก่อนเขียนโค้ด"
   "✅ ตกลงกันว่าอะไรไม่ทำ"
   "Best for: ฟีเจอร์ใหม่ · ระบบใหม่ · เปลี่ยนแผนใหญ่"
   Monospace strip (verbatim, 1 line):
   /grill-me <เล่าแผน>
   Footer (small): "หน้า 01 จาก 09 · ต่อไป: หน้า 02 แผน → ลงมือ"

Audience: Thai developer who uses Claude Code every day. Short sentences and bullets only.

---จบ---
