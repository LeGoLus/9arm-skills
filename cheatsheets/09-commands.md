# 09 · คำสั่ง Claude Code ที่ใช้บ่อย (Slash commands)

> ไฟล์นี้ไม่มีรหัสผ่าน, token หรือข้อมูลส่วนตัว
> ตัวเลขคือจำนวนครั้งที่คุณพิมพ์จริง นับจาก `~/.claude/history.jsonl` และ transcript (215 prompt, ณ 2026-10-23)

## จำเร็ว: ที่คุณใช้จริง

| คำสั่ง | ใช้ไป | ทำอะไร |
|---|---|---|
| `/model` | 17 | เปลี่ยน model เช่น Opus, Sonnet หรือ Haiku |
| `/remote-control` | 16 | ต่อ session นี้ไปคุมจากเครื่องหรือมือถืออื่น |
| `/exit` | 7 | ออกจาก Claude Code |
| `/anatomy` | 5 | เรียก skill anatomy (ทุก skill เรียกได้ด้วย `/ชื่อ-skill`) |
| `/plan` | 3 | เข้า plan mode: วางแผนก่อน ยังไม่แก้ไฟล์ |
| `/login` · `/logout` | 3 · 1 | เข้าและออกจากบัญชี |
| `/init` | 2 | สร้าง `CLAUDE.md` ของโปรเจกต์ |
| `/clear` | 2 | ล้าง context เริ่มเรื่องใหม่ |
| `/permissions` | 2 | ดูและแก้สิทธิ์ของ tool |
| `/compact` | 1 | สรุป context ให้สั้นลง แต่ยังคุยเรื่องเดิมต่อได้ |
| `/mcp` · `/plugin` | 1 · 1 | จัดการ MCP server และ plugin |

## ควรรู้เพิ่ม (ยังไม่ค่อยได้ใช้)

| คำสั่ง / ปุ่ม | ทำอะไร |
|---|---|
| `/resume` | กลับไปทำ session เก่าต่อ |
| `/context` | ดูว่า context ใช้ไปเท่าไรแล้ว ควร compact หรือยัง |
| `/fast` | เปิดหรือปิด fast mode (ยังเป็น Opus แต่ตอบเร็วขึ้น) |
| `/code-review ultra` | ให้ agent หลายตัวรีวิว branch บน cloud (คิดค่าใช้จ่าย และต้องสั่งเอง) |
| `/artifacts` | ดู artifact ที่เคย publish |
| `/help` | ดูคำสั่งทั้งหมด |
| `! <คำสั่ง>` | รันคำสั่ง shell ใน session นี้ ผลลัพธ์จะเข้ามาในแชทด้วย |
| `Shift+Tab` | สลับโหมดสิทธิ์ เช่น plan หรือ auto |
| `Esc` | หยุด Claude กลางทาง |

## คำสั่งของ 9arm-skills

| คำสั่ง | ทำอะไร |
|---|---|
| `bash ~/9arm-skills/scripts/link-skills.sh` | ดึง skill จาก repo มา link ไว้ใน `~/.claude/skills/` |
| `bash ~/9arm-skills/scripts/validate.sh` | ตรวจว่าลงทะเบียน skill ครบทุกไฟล์ |
| `bash ~/9arm-skills/scripts/list-skills.sh` | แสดง skill ทั้งหมดพร้อมคำอธิบาย |
| `bash ~/9arm-skills/scripts/token-audit.sh` | ตรวจว่าแต่ละ skill ใช้ token เท่าไร |

**จังหวะ compact (`strategic-compact`):** ใช้ `/compact` ตอนจบงานย่อย ไม่ใช่กลางงาน · ใช้ `/clear` ตอนเปลี่ยนไปทำเรื่องใหม่ทั้งหมด

---

## Prompt สำหรับทำภาพ

---เริ่ม---

Create a premium vertical (4:5) educational infographic in Thai for a developer who uses Claude Code every day.
Topic: "คำสั่ง / ที่ใช้จริง" (the slash commands this user types most, plus the few worth learning).

STYLE
- Modern sketchnote, white background (#FFFFFF) with a light gray dot grid (#F3F4F6)
- Fonts: Prompt / Kanit (Thai), bold black title, purple subtitle; commands in a monospace font
- Palette: Purple #8B5CF6, Yellow #FACC15, Blue #60A5FA, Green #4ADE80, Pink #F9A8D4
- Hand-drawn arrows, sticky notes, checkmarks, small keyboard icons. Clean and printable. Not cartoon-heavy.
- Color meaning: blue = everyday command · green = context/session care · purple = worth learning · yellow = takeaway

STRICT TEXT RULES
- Render every Thai and English text EXACTLY as written below, character by character.
- Every command must keep its leading "/" and exact spelling.
- Do NOT invent, translate, shorten or add any command, path or number.
- Keep text blocks short. Commands go in monospace boxes.
- No passwords, keys or personal data anywhere.

LAYOUT: 8 sections stacked top to bottom

1) HOOK (largest)
   Title: "คำสั่ง / ที่ใช้จริง"
   Purple subtitle: "10 คำสั่งที่พิมพ์บ่อยที่สุด"
   Tagline: "ทุก skill เรียกได้ด้วย /ชื่อ-skill"

2) BIG IDEA (one yellow sticky note)
   "compact ตอนจบงานย่อย · clear ตอนเปลี่ยนเรื่อง"

3) VISUAL FLOW (left to right, 4 numbered steps — "หนึ่ง session")
   "① /model เลือก model" -> "② /plan วางแผน" -> "③ ทำงาน + /compact" -> "④ /clear เรื่องใหม่"
   Red note: "session ยาวไม่ compact = Claude ลืมกฎ"
   Green arrow: "/context ดูก่อนว่าเหลือเท่าไร"

4) COMPONENT CARDS (4 cards, max 3 bullets)
   Blue card "ใช้ทุกวัน": "/model (17)" / "/remote-control (16)" / "/exit (7)"
   Green card "ดูแล context": "/compact" / "/clear" / "/context"
   Purple card "ตั้งค่า": "/permissions" / "/mcp · /plugin" / "/init → CLAUDE.md"
   Pink card "ควรลองใช้": "/resume" / "/fast" / "! <คำสั่ง shell>"

5) ARCHITECTURE (simple boxes + arrows)
   "พิมพ์ /grill-me" -> "Claude Code หา skill" -> "~/.claude/skills/grill-me/SKILL.md" -> "ทำตามขั้นตอนใน skill"

6) COMPARISON (table, 3 columns)
   Columns: คำสั่ง | ทำอะไร | ใช้ตอนไหน
   "/compact" | "สรุป context ให้สั้น" | "จบงานย่อย คุยต่อเรื่องเดิม"
   "/clear" | "ล้าง context" | "เริ่มเรื่องใหม่"
   "/resume" | "กลับไป session เก่า" | "ทำงานค้างต่อ"
   "/plan" | "วางแผน ไม่แก้ไฟล์" | "ก่อนงานใหญ่"
   Small orange box "พลาดบ่อย": "/clear กลางงาน = ลืมทุกอย่าง" / "ลืม link-skills.sh หลังดึง repo"

7) DECISION FRAMEWORK (two columns)
   Green column "/compact ถ้า…": "✅ จบงานย่อยแล้ว" / "✅ ยังทำเรื่องเดิมต่อ" / "✅ Claude เริ่มลืมรายละเอียด"
   Blue column "/clear ถ้า…": "✅ เปลี่ยนไปเรื่องใหม่ทั้งหมด" / "✅ ไม่ต้องใช้ข้อมูลเดิม" / "✅ context เต็มไปด้วยของเก่า"

8) SUMMARY
   "✅ /model ก่อนเริ่มงานหนัก"
   "✅ /plan ก่อนงานใหญ่"
   "✅ /compact ตอนจบงานย่อย"
   "✅ /clear ตอนเปลี่ยนเรื่อง"
   "✅ /ชื่อ-skill เรียก skill ได้ทันที"
   "Best for: ทุก session"
   Monospace strip (verbatim, 1 line):
   bash ~/9arm-skills/scripts/link-skills.sh
   Footer (small): "หน้า 09 จาก 09"

Audience: Thai developer who uses Claude Code every day. Short sentences and bullets only.

---จบ---
