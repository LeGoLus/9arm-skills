# 04 · เจอบั๊ก / ต้องสืบค้น (Debug + Investigate)

> ไฟล์นี้ไม่มีรหัสผ่าน, token หรือข้อมูลส่วนตัว

## จำเร็ว

| Skill | ใช้เมื่อ | เรียกยังไง | ได้อะไรออกมา |
|---|---|---|---|
| `systematic-debugging` ★ Tier 0 | เจอบั๊ก เทส fail หรือพฤติกรรมแปลก **ก่อนเสนอวิธีแก้** | อัตโนมัติ หรือ `/systematic-debugging` | 4 เฟส ห้ามข้าม: หาสาเหตุ → ดูรูปแบบ → ตั้งสมมติฐานแล้วทดสอบ → แก้แล้วยืนยัน |
| `debug-mantra` | อยากได้ฉบับย่อของวินัย debug | "debug mantra" | ท่องคาถา 4 ข้อ: reproduce, trace เส้นทางที่ fail, พิสูจน์ว่าสมมติฐานผิด, เทียบทุกร่องรอย |
| `post-mortem` | แก้บั๊กเสร็จแล้ว ก่อนปิดตั๋ว | `/post-mortem` | บันทึกสาเหตุ, กลไก, วิธีแก้, การยืนยัน และสาเหตุที่หลุดมาได้ |
| `research` | ต้องหาข้อเท็จจริงจากเอกสารหรือ API ทางการ | "research this" | ไฟล์ Markdown ในโปรเจกต์ ที่อ้างแหล่งข้อมูลหลัก |
| `reverse-engineer` | ต้องเข้าใจไบนารี แอป Electron/JS, APK หรือ firmware ที่ไม่มี source | "reverse engineer…" | ใช้ REA MCP ถอดโค้ด เทียบเวอร์ชัน และอธิบายฟีเจอร์ โดยอิงหลักฐาน |
| `playwright-trace` | เทส Playwright fail และมีไฟล์ trace | "inspect this trace" | ดู action, request, console, error และ screenshot จาก command line |

**กฎเหล็กของ `~/CLAUDE.md`:** debug ต้องครบ 4 เฟสเสมอ และก่อนบอกว่าแก้แล้วต้องผ่าน `verification-before-completion`

---

## Prompt สำหรับทำภาพ

---เริ่ม---

Create a premium vertical (4:5) educational infographic in Thai for a developer who uses Claude Code every day.
Topic: "หาสาเหตุ ก่อนแก้" (the debugging and investigation skills).

STYLE
- Modern sketchnote, white background (#FFFFFF) with a light gray dot grid (#F3F4F6)
- Fonts: Prompt / Kanit (Thai), bold black title, purple subtitle
- Palette: Purple #8B5CF6, Yellow #FACC15, Blue #60A5FA, Green #4ADE80, Pink #F9A8D4
- Hand-drawn arrows, sticky notes, checkmarks, small icons, a magnifying glass. Clean and printable. Not cartoon-heavy.
- Skill names always in a small monospace pill.
- Color meaning: pink/red = bug/guess · blue = investigation step · green = verified fix · yellow = takeaway

STRICT TEXT RULES
- Render every Thai and English text EXACTLY as written below, character by character.
- Do NOT invent, translate, shorten or add any skill name, command, path or number.
- Keep text blocks short. Commands go in monospace boxes.
- No passwords, keys or personal data anywhere.

LAYOUT: 8 sections stacked top to bottom

1) HOOK (largest)
   Title: "หาสาเหตุ ก่อนแก้"
   Purple subtitle: "4 เฟส ห้ามข้าม"
   Tagline: "เดาแล้วแก้ = บั๊กใหม่"

2) BIG IDEA (one yellow sticky note)
   "ยังไม่รู้สาเหตุ ห้ามเสนอวิธีแก้"

3) VISUAL FLOW (top to bottom, 4 numbered steps)
   "① Reproduce: ทำให้พังซ้ำได้" -> "② Trace: ไล่เส้นทางที่ fail" -> "③ Falsify: พิสูจน์สมมติฐาน" -> "④ Fix + Verify: แก้แล้วยืนยัน"
   Red note: "แก้ 3 ครั้งยังไม่หาย = กลับไปเฟส ①"
   Green arrow: "แก้แล้ว → post-mortem"

4) COMPONENT CARDS (4 cards, max 3 bullets)
   Pink card "systematic-debugging": "Tier 0 ทุกโปรเจกต์" / "บั๊ก · เทส fail · แปลก" / "4 เฟส ไม่มีข้อยกเว้น"
   Blue card "debug-mantra": "ฉบับย่อ 4 ข้อ" / "ท่องก่อนเริ่ม debug" / "เทียบทุกร่องรอย"
   Green card "post-mortem": "หลังแก้เสร็จ" / "สาเหตุ · กลไก · วิธีแก้" / "ทำไมถึงหลุดมาได้"
   Purple card "research / reverse-engineer": "หาข้อมูลจากแหล่งหลัก" / "ไม่มี source → REA" / "อ้างหลักฐานเสมอ"

5) ARCHITECTURE (simple boxes + arrows)
   "บั๊ก" -> "systematic-debugging" -> "tdd: เทสจำลองบั๊ก" -> "แก้" -> "verification-before-completion" -> "post-mortem"

6) COMPARISON (table, 4 columns)
   Columns: ปัญหา | ใช้ | ได้อะไร | ต่อด้วย
   "บั๊กในโค้ดเรา" | "systematic-debugging" | "สาเหตุจริง" | "tdd"
   "ไม่รู้ว่า API ทำงานยังไง" | "research" | "ไฟล์สรุป + แหล่งอ้างอิง" | "search-first"
   "ไม่มี source" | "reverse-engineer" | "โค้ดที่ถอดได้ + หลักฐาน" | "research"
   "เทส Playwright fail" | "playwright-trace" | "action + error" | "systematic-debugging"
   Small orange box "พลาดบ่อย": "แก้อาการ ไม่แก้สาเหตุ" / "เปลี่ยนหลายอย่างพร้อมกัน"

7) DECISION FRAMEWORK (two columns)
   Pink column "debug เอง ถ้า…": "✅ ทำให้พังซ้ำได้" / "✅ อยู่ในโค้ดของเรา" / "✅ มี log หรือ error"
   Blue column "research ก่อน ถ้า…": "✅ เป็นพฤติกรรมของ library" / "✅ เอกสารขัดกัน" / "✅ ไม่แน่ใจว่าเป็นบั๊กจริง"

8) SUMMARY
   "✅ reproduce ให้ได้ก่อน"
   "✅ เปลี่ยนทีละอย่าง"
   "✅ เทสจำลองบั๊กก่อนแก้"
   "✅ ยืนยันด้วยผลจริง"
   "✅ ปิดงานด้วย post-mortem"
   "Best for: บั๊ก · เทส fail · ระบบทำงานแปลก"
   Monospace strip (verbatim, 1 line):
   Reproduce → Trace → Falsify → Verify
   Footer (small): "หน้า 04 จาก 09"

Audience: Thai developer who uses Claude Code every day. Short sentences and bullets only.

---จบ---
