# 02 · จากแผนสู่การลงมือ (Plan → Execute)

> ไฟล์นี้ไม่มีรหัสผ่าน, token หรือข้อมูลส่วนตัว

## จำเร็ว

| Skill | ใช้เมื่อ | เรียกยังไง | ได้อะไรออกมา |
|---|---|---|---|
| `writing-plans` | มี spec หรือแผนแล้ว ก่อนแตะโค้ด | `/writing-plans` | แผนที่แตกเป็นงานละ 2-5 นาที ระบุ path ไฟล์ชัด |
| `executing-plans` | มีแผนเป็นลายลักษณ์อักษรแล้ว จะลงมือ | `/executing-plans` | ทำทีละชุด หยุดให้คนตรวจเป็นระยะ |
| `to-tickets` | อยากแตกแผนหรือบทสนทนาเป็นตั๋วงาน | `/to-tickets` (ต้องพิมพ์เอง) | `tickets.md` หรือ `TASK_BRAIN.md` ที่มีงานแบบ tracer-bullet และบอกว่าตั๋วไหนรอตั๋วไหน |
| `wayfinder` | งานใหญ่เกินกว่าที่ session เดียวจะรับได้ | `/wayfinder` (ต้องพิมพ์เอง) | แผนที่ของตั๋วสืบค้น แล้วไล่ปิดทีละใบจนเห็นทางชัด |
| `task-brain` | งานหลาย session หรือส่งต่องานระหว่าง Claude Code กับ Cowork | "start a new project", "continue" | `TASK_BRAIN.md` เก็บสถานะ, การตัดสินใจ และจุดส่งต่องาน |
| `dynamic-skill-init` | grill จบและได้ `IMPLEMENTATION.md` แล้ว | "set up skills for this project" | รายชื่อ skill ใน `CLAUDE.md` ของโปรเจกต์ ที่เลือกจากแผนจริง |
| `strategic-compact` ★ Tier 1 | session ยาว เริ่มลืม เริ่มมั่ว | "session is getting long" | บอกจังหวะที่ควร `/compact` หรือ `/clear` และสรุปสิ่งที่ต้องเก็บไว้ |

**เลือกขนาดงาน:** งานเล็ก → `writing-plans` · หลายวันหรือหลาย session → `to-tickets` + `task-brain` · ใหญ่จนยังไม่รู้ทาง → `wayfinder`

---

## Prompt สำหรับทำภาพ

---เริ่ม---

Create a premium vertical (4:5) educational infographic in Thai for a developer who uses Claude Code every day.
Topic: "แผนดี = งานเดินเอง" (how to turn an agreed plan into executed work, by size of the job).

STYLE
- Modern sketchnote, white background (#FFFFFF) with a light gray dot grid (#F3F4F6)
- Fonts: Prompt / Kanit (Thai), bold black title, purple subtitle
- Palette: Purple #8B5CF6, Yellow #FACC15, Blue #60A5FA, Green #4ADE80, Pink #F9A8D4
- Hand-drawn arrows, sticky notes, checkmarks, small icons. Clean and printable. Not cartoon-heavy.
- Skill names always in a small monospace pill.
- Color meaning: purple = plan · blue = execute · green = checkpoint passed · yellow = takeaway · pink = warning

STRICT TEXT RULES
- Render every Thai and English text EXACTLY as written below, character by character.
- Do NOT invent, translate, shorten or add any skill name, command, path or number.
- Keep text blocks short. Commands go in monospace boxes.
- No passwords, keys or personal data anywhere.

LAYOUT: 8 sections stacked top to bottom

1) HOOK (largest)
   Title: "แผนดี = งานเดินเอง"
   Purple subtitle: "แตกงานก่อน แล้วค่อยลงมือ"
   Tagline: "งานละ 2-5 นาที · มีจุดตรวจ"

2) BIG IDEA (one yellow sticky note)
   "งานที่ใหญ่เกินจะเขียนเป็นข้อๆ ได้ คืองานที่ยังไม่ได้วางแผน"

3) VISUAL FLOW (left to right, 4 numbered steps)
   "① แผนจาก grill" -> "② writing-plans: แตกงาน" -> "③ executing-plans: ทำทีละชุด" -> "④ จุดตรวจ: คนรีวิว"
   Red note: "ทำรวดเดียวไม่หยุด = พลาดแล้วย้อนยาก"
   Green arrow (④ back to ③): "ผ่าน → ชุดถัดไป"

4) COMPONENT CARDS (4 cards, max 3 bullets)
   Purple card "writing-plans": "งานละ 2-5 นาที" / "ระบุ path ไฟล์ชัด" / "ก่อนแตะโค้ด"
   Blue card "executing-plans": "ทำทีละชุด" / "หยุดให้คนตรวจ" / "ทำตามแผน ไม่เพิ่มเอง"
   Green card "to-tickets / wayfinder": "งานใหญ่ → ตั๋ว" / "แต่ละตั๋วบอกว่ารอใคร" / "ต้องพิมพ์ /ชื่อ เอง"
   Pink card "strategic-compact": "session ยาว = เริ่มลืม" / "compact ตอนจบงานย่อย" / "เก็บสิ่งที่ต้องจำไว้ก่อน"

5) ARCHITECTURE (simple boxes + arrows)
   "IMPLEMENTATION.md" -> "dynamic-skill-init" -> "CLAUDE.md ของโปรเจกต์"
   "tickets.md / TASK_BRAIN.md" <-> "หลาย session (task-brain)"

6) COMPARISON (table, 4 columns) — title "เลือกตามขนาดงาน"
   Columns: ขนาดงาน | ใช้ | ไฟล์ที่ได้ | จุดเด่น
   "ไม่กี่ชั่วโมง" | "writing-plans" | "แผนในแชท/ไฟล์" | "เร็ว"
   "หลายวัน" | "to-tickets + task-brain" | "tickets.md, TASK_BRAIN.md" | "ส่งต่อ session ได้"
   "ยังไม่รู้ทาง" | "wayfinder" | "แผนที่ตั๋วสืบค้น" | "ไล่ทีละใบจนชัด"
   Small orange box "พลาดบ่อย": "ไม่ compact จน Claude ลืมกฎ" / "แผนไม่ระบุไฟล์ → เดาเอง"

7) DECISION FRAMEWORK (two columns)
   Blue column "ใช้ executing-plans ถ้า…": "✅ มีแผนเป็นไฟล์แล้ว" / "✅ งานแยกเป็นชุดได้" / "✅ อยากตรวจเป็นระยะ"
   Purple column "ใช้ wayfinder ถ้า…": "✅ งานเกิน 1 session" / "✅ ยังมีเรื่องต้องสืบค้น" / "✅ ไม่รู้ว่าเริ่มตรงไหน"

8) SUMMARY
   "✅ แตกงานละ 2-5 นาที พร้อม path"
   "✅ ทำทีละชุด หยุดให้ตรวจ"
   "✅ งานหลาย session → TASK_BRAIN.md"
   "✅ ยาวแล้ว → compact ตอนจบงานย่อย"
   "Best for: ฟีเจอร์หลายไฟล์ · โปรเจกต์หลายวัน"
   Monospace strip (verbatim, 1 line):
   /writing-plans → /executing-plans
   Footer (small): "หน้า 02 จาก 09 · ต่อไป: หน้า 03 สร้างให้มีคุณภาพ"

Audience: Thai developer who uses Claude Code every day. Short sentences and bullets only.

---จบ---
