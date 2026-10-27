# 03 · เขียนโค้ดให้มีคุณภาพ (Build + Review)

> ไฟล์นี้ไม่มีรหัสผ่าน, token หรือข้อมูลส่วนตัว

## จำเร็ว

| Skill | ใช้เมื่อ | เรียกยังไง | ได้อะไรออกมา |
|---|---|---|---|
| `tdd` ★ Tier 1 | ทุกครั้งที่จะเขียนหรือแก้โค้ด | `/tdd` หรือพิมพ์ "implement…" | RED (เทสที่ fail) → GREEN (โค้ดน้อยที่สุดที่ผ่าน) ส่วน refactor เป็นงานของ `code-review` |
| `search-first` | ก่อนเขียนของใหม่ หรือใช้ library ที่ไม่คุ้น | "how do I…" | ค้นเอกสารและโค้ดเดิมก่อน ไม่เดา API |
| `error-handling` ★ Tier 1 | ใช้ควบคู่กับทุกงานที่เขียนโค้ด | "make it reliable" | error boundary, structured log, retry และ graceful degradation |
| `verification-loop` ★ Tier 1 | เขียนเสร็จแล้ว ก่อน commit หรือเปิด PR | "run all checks" | วน build → test → lint → typecheck → security จนผ่านหมด |
| `verification-before-completion` ★ Tier 1 | ก่อนบอกว่า "เสร็จ", "แก้แล้ว" หรือ "ผ่าน" | อัตโนมัติ | รันคำสั่งตรวจจริงและดูผลก่อน ต้องมีหลักฐานก่อนพูด |
| `code-review` ★ Tier 1 | รีวิวตัวเองก่อน commit | "review this" | เช็ก security, performance, ชื่อ, dead code และ test |
| `receiving-code-review` | ได้รับ comment รีวิวมา | "got review feedback" | ตรวจว่าข้อเสนอถูกจริงไหมก่อนแก้ ไม่รับแบบไม่คิด |
| `security-review` ★ Tier 2 | ก่อนขึ้น production หรือจับข้อมูลสำคัญ | "is this secure" | ตรวจตาม OWASP Top 10, injection, auth, ข้อมูลรั่ว และ dependency |
| `improve-codebase-architecture` | ทุกสัปดาห์ หรือหลังเร่งงานหนัก | "refactor", "clean up" | หา module ที่บางเกินไปและ dependency ที่พันกัน |
| `ui-ux-pro-max` | ออกแบบหน้าจอเว็บหรือแอป | "design this UI" | 50+ สไตล์, 161 palette และ 99 UX guideline |

**ลำดับที่ใช้จริง:** `search-first` → `tdd` (+ `error-handling`) → `verification-loop` → `code-review` → `verification-before-completion` → commit (หน้า 05)

---

## Prompt สำหรับทำภาพ

---เริ่ม---

Create a premium vertical (4:5) educational infographic in Thai for a developer who uses Claude Code every day.
Topic: "Test ก่อน Code" (the build-and-review loop: tdd, verification and review skills).

STYLE
- Modern sketchnote, white background (#FFFFFF) with a light gray dot grid (#F3F4F6)
- Fonts: Prompt / Kanit (Thai), bold black title, purple subtitle
- Palette: Purple #8B5CF6, Yellow #FACC15, Blue #60A5FA, Green #4ADE80, Pink #F9A8D4
- Hand-drawn arrows, sticky notes, checkmarks, small icons. Clean and printable. Not cartoon-heavy.
- Skill names always in a small monospace pill.
- Color meaning: pink/red = failing test (RED) · green = passing (GREEN) · blue = build step · yellow = takeaway

STRICT TEXT RULES
- Render every Thai and English text EXACTLY as written below, character by character.
- Do NOT invent, translate, shorten or add any skill name, command, path or number.
- Keep text blocks short. Commands go in monospace boxes.
- No passwords, keys or personal data anywhere.

LAYOUT: 8 sections stacked top to bottom

1) HOOK (largest)
   Title: "Test ก่อน Code"
   Purple subtitle: "RED → GREEN → ตรวจ → ส่ง"
   Tagline: "ไม่มีหลักฐาน = ยังไม่เสร็จ"

2) BIG IDEA (one yellow sticky note)
   "เขียนเทสที่ fail ก่อนเสมอ แล้วรันตรวจจริงก่อนพูดว่าเสร็จ"

3) VISUAL FLOW (circular loop, 5 numbered steps, clockwise, no crossing)
   "① search-first: ค้นก่อน" -> "② RED: เทส fail" -> "③ GREEN: โค้ดน้อยสุดที่ผ่าน" -> "④ verification-loop" -> "⑤ code-review"
   Red note: "เขียนโค้ดก่อนเทส = เทสแค่ยืนยันสิ่งที่เขียนไปแล้ว"
   Green arrow: "เทส fail ก่อน → รู้ว่าเทสจับบั๊กได้จริง"

4) COMPONENT CARDS (5 cards, max 3 bullets)
   Pink card "tdd": "RED → GREEN" / "ทุกงานเขียนโค้ด" / "refactor = งาน code-review"
   Blue card "verification-loop": "build → test → lint" / "→ typecheck → security" / "วนจนผ่านหมด"
   Green card "verification-before-completion": "ก่อนพูดว่า 'เสร็จ'" / "รันคำสั่งจริง ดูผลจริง" / "หลักฐานก่อนคำพูด"
   Purple card "code-review": "รีวิวตัวเองก่อน commit" / "security · perf · ชื่อ" / "dead code · test"
   Yellow card "error-handling": "ใช้คู่กับทุกงาน" / "log มีโครงสร้าง" / "retry + ล้มอย่างนุ่มนวล"

5) ARCHITECTURE (simple boxes + arrows)
   "โค้ด" -> "verification-loop" -> "code-review" -> "security-review (ก่อน production)" -> "commit"
   Side box: "receiving-code-review: ได้ comment → ตรวจก่อนแก้"

6) COMPARISON (table, 4 columns)
   Columns: Skill | ตอนไหน | ตรวจอะไร | ใครเรียก
   "verification-loop" | "หลังเขียนเสร็จ" | "build/test/lint/type" | "พิมพ์เรียก"
   "verification-before-completion" | "ก่อนบอกว่าเสร็จ" | "ผลจริงของคำสั่ง" | "อัตโนมัติ"
   "code-review" | "ก่อน commit" | "คุณภาพโค้ด" | "พิมพ์เรียก"
   "security-review" | "ก่อน production" | "OWASP Top 10" | "พิมพ์เรียก"
   Small orange box "พลาดบ่อย": "บอกว่าเสร็จโดยไม่ได้รันเทส" / "แก้ตาม review ทันทีโดยไม่ตรวจ"

7) DECISION FRAMEWORK (two columns)
   Green column "ใช้ tdd ถ้า…": "✅ เพิ่มฟีเจอร์" / "✅ แก้บั๊ก (เทสจำลองบั๊กก่อน)" / "✅ มีโค้ดที่เทสได้"
   Blue column "ใช้ prototype แทน ถ้า…": "✅ แค่ลองว่าดีไซน์ใช้ได้ไหม" / "✅ จะทิ้งโค้ดหลังได้คำตอบ" / "✅ ยังไม่รู้ว่าจะสร้างอะไร"

8) SUMMARY
   "✅ ค้นก่อน ไม่เดา API"
   "✅ เทส fail ก่อนเขียนโค้ดเสมอ"
   "✅ วนตรวจจนผ่านทุกอย่าง"
   "✅ ไม่มีหลักฐาน ไม่พูดว่าเสร็จ"
   "✅ ก่อน production → security-review"
   "Best for: ทุกงานที่แตะโค้ด"
   Monospace strip (verbatim, 1 line):
   RED → GREEN → verify → review → commit
   Footer (small): "หน้า 03 จาก 09 · บั๊กโผล่? ไปหน้า 04"

Audience: Thai developer who uses Claude Code every day. Short sentences and bullets only.

---จบ---
