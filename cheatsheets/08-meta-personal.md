# 08 · Skill ของ Skill และเรื่องส่วนตัว (Meta + Personal)

> ไฟล์นี้ไม่มีรหัสผ่าน, token หรือข้อมูลส่วนตัว

## จำเร็ว

| Skill | ใช้เมื่อ | เรียกยังไง | ได้อะไรออกมา |
|---|---|---|---|
| `writing-skills` | สร้างหรือแก้ skill ใน 9arm-skills (งานหลักของ repo นี้) | "create a new skill" | `SKILL.md` ที่เขียนถูกแบบ และตรวจว่าทำงานจริงก่อนใช้ |
| `writing-great-skills` | อยากรู้หลักการเขียน skill ให้ Claude เรียกใช้ได้แม่น | `/writing-great-skills` (ต้องพิมพ์เอง) | คำศัพท์และหลักการ เช่น skill ที่ model เรียกเอง กับ skill ที่คนต้องเรียก |
| `skill-creator` | อยากวัดผลหรือ benchmark skill หรือปรับ description ให้ Claude เรียกแม่นขึ้น | "optimize this skill's description" | ชุด eval และตัวเลขผล |
| `document-skill` | ทำเอกสาร skill เป็นภาษาไทยและอังกฤษ | "document this skill" | เอกสาร 2 ภาษา พร้อม frontmatter |
| `continuous-learning` ★ Tier 2 | จบ session ใหญ่ หรือเจอปัญหาเดิมซ้ำ | "learn from this" | pattern และวิธีแก้ที่เก็บไว้ใช้ครั้งหน้า |
| `teach` | อยากเรียนเรื่องใหม่ภายใน workspace | `/teach <เรื่อง>` (ต้องพิมพ์เอง) | Claude สอนทีละขั้น |
| `find` | หาราคาที่ถูกหรือคุ้มที่สุด เช่น ของ, ตั๋วเครื่องบิน, โรงแรม หรือ subscription | `/find <ของ>` | ราคาสุทธิ (รวมค่าธรรมเนียม FX, DCC และ cashback) แต่ไม่จองและไม่จ่ายแทน |
| `andaman-context` | ทำงานเกี่ยวกับร้าน Andaman Print Form, AWOMS หรือใบส่งของ | อัตโนมัติในโปรเจกต์ที่เกี่ยวข้อง | ความรู้เรื่องธุรกิจงานพิมพ์ |

**หลังเพิ่ม skill ใหม่ทุกครั้ง** (จาก `CLAUDE.md` ของ repo):
1. ใส่ไว้ใน bucket ที่ถูก (`engineering/`, `productivity/`, `ai-agent/`, `meta/` หรือ `personal/`)
2. ลงทะเบียนใน `README.md`, `plugin.json`, `catalog.json` และ `tier-manifest.yaml`
3. รัน `validate.sh` → `link-skills.sh` → commit แบบ conventional

---

## Prompt สำหรับทำภาพ

---เริ่ม---

Create a premium vertical (4:5) educational infographic in Thai for a developer who maintains their own Claude Code skill library.
Topic: "สร้าง Skill ของตัวเอง" (how to write, register and improve a skill in 9arm-skills, plus personal helper skills).

STYLE
- Modern sketchnote, white background (#FFFFFF) with a light gray dot grid (#F3F4F6)
- Fonts: Prompt / Kanit (Thai), bold black title, purple subtitle
- Palette: Purple #8B5CF6, Yellow #FACC15, Blue #60A5FA, Green #4ADE80, Pink #F9A8D4
- Hand-drawn arrows, sticky notes, checkmarks, small icons (toolbox, book). Clean and printable. Not cartoon-heavy.
- Skill names always in a small monospace pill.
- Color meaning: purple = write · blue = register · green = validated · pink = personal · yellow = takeaway

STRICT TEXT RULES
- Render every Thai and English text EXACTLY as written below, character by character.
- Do NOT invent, translate, shorten or add any skill name, command, path or number.
- Keep text blocks short. Commands go in monospace boxes.
- No passwords, keys or personal data anywhere.

LAYOUT: 8 sections stacked top to bottom

1) HOOK (largest)
   Title: "สร้าง Skill ของตัวเอง"
   Purple subtitle: "เขียน → ลงทะเบียน → ตรวจ → link"
   Tagline: "description ดี = Claude เรียกถูกจังหวะ"

2) BIG IDEA (one yellow sticky note)
   "skill ที่ไม่ได้ลงทะเบียนและไม่ได้ตรวจ = skill ที่ไม่มีใครเรียกใช้"

3) VISUAL FLOW (left to right, 4 numbered steps)
   "① writing-skills: เขียน SKILL.md" -> "② ลงทะเบียน 4 ไฟล์" -> "③ validate.sh" -> "④ link-skills.sh + commit"
   Red note: "ลืมลงทะเบียน = validate ไม่ผ่าน"
   Green arrow: "เรียกไม่ค่อยติด → skill-creator ปรับ description"

4) COMPONENT CARDS (4 cards, max 3 bullets)
   Purple card "writing-skills": "งานหลักของ repo นี้" / "สร้าง / แก้ skill" / "ตรวจก่อนใช้จริง"
   Blue card "writing-great-skills": "หลักการเขียน skill" / "model เรียกเอง vs คนเรียก" / "ต้องพิมพ์ /ชื่อ เอง"
   Green card "skill-creator": "วัดผล skill" / "benchmark" / "ปรับ description"
   Pink card "continuous-learning": "จบ session ใหญ่" / "เจอปัญหาซ้ำ" / "เก็บ pattern ไว้ใช้ต่อ"

5) ARCHITECTURE (simple boxes + arrows)
   "skills/<bucket>/<name>/SKILL.md" -> "README.md · plugin.json · catalog.json · tier-manifest.yaml" -> "validate.sh" -> "~/.claude/skills/"

6) COMPARISON (table, 3 columns) — title "Personal helpers"
   Columns: Skill | ใช้เมื่อ | หมายเหตุ
   "teach" | "อยากเรียนเรื่องใหม่" | "พิมพ์ /teach เอง"
   "find" | "หาราคาคุ้มสุด" | "ไม่จอง ไม่จ่ายแทน"
   "document-skill" | "เอกสาร skill ไทย + อังกฤษ" | "มี frontmatter"
   "andaman-context" | "งาน Andaman / AWOMS" | "ความรู้ธุรกิจงานพิมพ์"
   Small orange box "พลาดบ่อย": "description กว้างเกิน → เรียกผิดเวลา" / "ใส่ personal skill ใน plugin.json"

7) DECISION FRAMEWORK (two columns)
   Purple column "สร้าง skill ใหม่ ถ้า…": "✅ ทำแบบเดิมเกิน 3 ครั้ง" / "✅ มีกฎที่ Claude ลืมบ่อย" / "✅ มีขั้นตอนที่ต้องเป๊ะ"
   Pink column "แค่จดใน memory ถ้า…": "✅ เป็นข้อเท็จจริงข้อเดียว" / "✅ ใช้กับโปรเจกต์เดียว" / "✅ ไม่มีขั้นตอน"

8) SUMMARY
   "✅ เขียนด้วย writing-skills"
   "✅ ลงทะเบียนให้ครบ 4 ไฟล์"
   "✅ validate.sh ต้องผ่าน"
   "✅ personal/ ไม่ใส่ใน plugin.json"
   "Best for: ดูแลคลัง 9arm-skills"
   Monospace strip (verbatim, 1 line):
   bash scripts/validate.sh && bash scripts/link-skills.sh
   Footer (small): "หน้า 08 จาก 09"

Audience: Thai developer who maintains a personal skill library. Short sentences and bullets only.

---จบ---
