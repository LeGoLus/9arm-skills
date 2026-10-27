# 06 · ภาพ เอกสาร และสไลด์ (Visual + Docs)

> ไฟล์นี้ไม่มีรหัสผ่าน, token หรือข้อมูลส่วนตัว

## จำเร็ว

| Skill | ใช้เมื่อ | เรียกยังไง | ได้อะไรออกมา |
|---|---|---|---|
| `excalidraw-diagram` ★ ใช้บ่อยสุด | ทุกเอกสารที่มี flow, สถาปัตยกรรม หรือ timeline (กฎใน `~/CLAUDE.md`) | "draw a diagram" | ไฟล์ `.excalidraw` + `.png` ใน `<doc>/diagrams/` ที่ render แล้วตรวจเอง |
| `anatomy` | อยากได้ภาพ isometric อธิบายแนวคิดเทคนิคเป็นเครื่องจักรจริง | `/anatomy` | SVG แบบ interactive, เพิ่มเอฟเฟกต์ WebGL ได้, พิมพ์ A4 ได้ |
| `infographic-one-page` | ย่อเรื่องให้เหลือภาพเดียว 4:5 (ไฟล์ชุดนี้ทำด้วยตัวนี้) | `/infographic-one-page` | prompt 8 ส่วนสำหรับ ChatGPT หรือ Canva หรือ render เป็น HTML เองในเครื่อง |
| `deck-grill` | "ทำสไลด์ให้หน่อย" แต่ยังไม่รู้ว่าจะพูดอะไร | `/deck-grill` | brief ที่อนุมัติแล้ว ระบุทีละสไลด์ |
| `sketch-deck` | ได้ brief จาก `deck-grill` แล้ว | `/sketch-deck` | สไลด์ HTML ไฟล์เดียว สไตล์ไวท์บอร์ด ทยอยแสดงทีละขั้น ดูได้ทั้งมือถือและคอม |
| `design-phase` | งานออกแบบทุกชนิด เช่น company profile หรือโบรชัวร์ | "show me the concept first" | แบ่งเป็นข้อมูล → concept → preview → งานจริง หยุดให้ลูกค้าดูทุกขั้น |
| `ui-ux-pro-max` | ออกแบบหน้าเว็บหรือแอป | "design this UI" | สไตล์, palette, คู่ font และ UX guideline |
| `docx` · `pptx` · `xlsx` · `pdf` | ต้องได้ไฟล์ Word, PowerPoint, Excel หรือ PDF | พูดชื่อไฟล์หรือนามสกุลมาเลย | ไฟล์จริงตามรูปแบบที่ขอ |
| `management-talk` | ต้องเล่าเรื่องเทคนิคให้หัวหน้าหรือผู้บริหารฟัง | "rewrite for leadership" | ข้อความที่เหมาะกับช่องทาง เช่น Slack, email, JIRA หรือห้องประชุม |

**เส้นทางสไลด์:** `deck-grill` → `sketch-deck` (HTML) · ถ้าต้องเป็นไฟล์ `.pptx` → `pptx`

---

## Prompt สำหรับทำภาพ

---เริ่ม---

Create a premium vertical (4:5) educational infographic in Thai for a developer who uses Claude Code every day.
Topic: "ภาพเดียว ชนะ 1,000 คำ" (which skill makes which kind of picture, document or slide deck).

STYLE
- Modern sketchnote, white background (#FFFFFF) with a light gray dot grid (#F3F4F6)
- Fonts: Prompt / Kanit (Thai), bold black title, purple subtitle
- Palette: Purple #8B5CF6, Yellow #FACC15, Blue #60A5FA, Green #4ADE80, Pink #F9A8D4
- Hand-drawn arrows, sticky notes, checkmarks, small icons (pencil, slide, page). Clean and printable. Not cartoon-heavy.
- Skill names always in a small monospace pill.
- Color meaning: purple = diagram · blue = slides · green = office files · pink = design · yellow = takeaway

STRICT TEXT RULES
- Render every Thai and English text EXACTLY as written below, character by character.
- Do NOT invent, translate, shorten or add any skill name, command, path or number.
- Keep text blocks short. Commands go in monospace boxes.
- No passwords, keys or personal data anywhere.

LAYOUT: 8 sections stacked top to bottom

1) HOOK (largest)
   Title: "ภาพเดียว ชนะ 1,000 คำ"
   Purple subtitle: "เลือก skill ตามสิ่งที่ต้องส่ง"
   Tagline: "ทุกเอกสาร + 1 diagram"

2) BIG IDEA (one yellow sticky note)
   "อะไรที่อธิบายด้วยข้อความยาก ให้วาดเพิ่ม แต่ไม่วาดเพื่อตกแต่ง"

3) VISUAL FLOW (left to right, 4 numbered steps)
   "① เขียนเนื้อหา" -> "② ส่วนที่เข้าใจยาก → excalidraw-diagram" -> "③ render → ตรวจภาพ" -> "④ ฝัง PNG ในเอกสาร"
   Red note: "ลบไฟล์ .excalidraw = แก้ภาพไม่ได้อีก"
   Green arrow: "เก็บ .excalidraw + .png ใน diagrams/"

4) COMPONENT CARDS (5 cards, max 3 bullets)
   Purple card "excalidraw-diagram": "ใช้บ่อยสุด" / "flow · สถาปัตยกรรม · timeline" / "render แล้วตรวจเองทุกครั้ง"
   Pink card "anatomy": "ภาพ isometric" / "แนวคิด = เครื่องจักรจริง" / "พิมพ์ A4 ได้"
   Yellow card "infographic-one-page": "ย่อเหลือภาพเดียว 4:5" / "8 ส่วน" / "prompt หรือ HTML"
   Blue card "deck-grill → sketch-deck": "ถามก่อนทำสไลด์" / "brief ทีละสไลด์" / "HTML สไตล์ไวท์บอร์ด"
   Green card "docx · pptx · xlsx · pdf": "ต้องได้ไฟล์ office" / "พูดนามสกุลไฟล์ได้เลย" / "ไฟล์จริง"

5) ARCHITECTURE (simple boxes + arrows)
   "deck-grill (brief)" -> "sketch-deck (HTML)"
   "deck-grill (brief)" -> "pptx (.pptx)"
   "design-phase: ข้อมูล → concept → preview → งานจริง"

6) COMPARISON (table, 3 columns)
   Columns: ต้องการ | ใช้ | ผลลัพธ์
   "flow / สถาปัตยกรรม" | "excalidraw-diagram" | ".excalidraw + .png"
   "ภาพอธิบายสวยๆ" | "anatomy" | "SVG interactive"
   "สรุปหน้าเดียว" | "infographic-one-page" | "prompt 4:5"
   "สไลด์" | "deck-grill → sketch-deck" | "HTML deck"
   "เล่าให้ผู้บริหาร" | "management-talk" | "ข้อความตามช่องทาง"
   Small orange box "พลาดบ่อย": "ภาพ AI สะกดไทยผิด → ตรวจทุกตัวอักษร" / "ไม่ตรวจภาพหลัง render"

7) DECISION FRAMEWORK (two columns)
   Purple column "ใช้ excalidraw-diagram ถ้า…": "✅ ต้องแก้ภาพภายหลังได้" / "✅ ฝังในเอกสาร" / "✅ เป็น flow หรือความสัมพันธ์"
   Pink column "ใช้ anatomy ถ้า…": "✅ อยากได้ภาพที่สะดุดตา" / "✅ อธิบายกลไกด้วยของจริง" / "✅ ใช้ในบทความหรือเว็บ"

8) SUMMARY
   "✅ ทุกเอกสารที่เข้าใจยาก → diagram"
   "✅ เก็บไฟล์ต้นฉบับไว้ ห้ามลบ"
   "✅ สไลด์: grill ก่อน แล้วค่อยทำ"
   "✅ ภาพจาก AI: ตรวจข้อความทุกตัว"
   "Best for: รายงาน · คู่มือ · PRD · พรีเซนต์"
   Monospace strip (verbatim, 1 line):
   <doc>/diagrams/<doc>-01-<topic>.excalidraw
   Footer (small): "หน้า 06 จาก 09"

Audience: Thai developer who uses Claude Code every day. Short sentences and bullets only.

---จบ---
