# 07 · AI Agent และ Automation (คุมจอ, ทีม AI, model)

> ไฟล์นี้ไม่มีรหัสผ่าน, token หรือข้อมูลส่วนตัว

## จำเร็ว

| Skill | ใช้เมื่อ | เรียกยังไง | ได้อะไรออกมา |
|---|---|---|---|
| `drive-screen` ★ | ต้องคุมหน้าจอจริง เช่น จัดหน้าต่าง, เตรียม demo, เทสแอปที่ไม่มี API หรือสั่ง Claude Code อีกหน้าต่าง | "set up my screen", "drive the other session" | โฟกัสหน้าต่าง พิมพ์ วาง คลิก และ screenshot บน Mac, Windows และ Linux |
| `subagent-driven-development` ★ Tier 2 | มีแผนแล้ว และงานย่อยแยกกันได้ | `/subagent-driven-development` | subagent ใหม่ต่องาน และรีวิว 2 ชั้น |
| `dispatching-parallel-agents` ★ Tier 2 | มีงานอิสระตั้งแต่ 2 งาน ที่ไม่ใช้ข้อมูลร่วมกัน | "run these in parallel" | หลาย agent ทำพร้อมกัน |
| `ai-software-team` | มอบงานทั้งโปรเจกต์ ไม่ใช่งานเดียว | "Start X Program" | คุณเป็น PO + Architect ส่วน AI แตกงานเป็น Program → Milestone → Epic → Feature → Task บน Kanban |
| `model-harness` | model ไม่ฉลาดพอ, ผลออกมาไม่เหมือนเดิม หรือจะเปลี่ยน model | "the model isn't smart enough" | ย้ายความฉลาดมาไว้ในโครงสร้างและขั้นตอน (บทเรียนจาก Hermes + MiniMax M3) |
| `prompt-engineer` ★ Tier 2 | เขียน system prompt, few-shot หรือ structured output | "improve this prompt" | prompt ที่ออกแบบแล้ว และกันเรื่อง prompt injection |
| `agentic-eval` ★ Tier 2 | อยากรู้ว่าผลจาก AI ดีจริงไหม หรือแย่ลงหรือเปล่า | "eval", "compare prompts" | ชุดทดสอบสำหรับวัดคุณภาพและจับการถดถอย |
| `playwright-cli` · `playwright-component-testing` | ต้องคุมเบราว์เซอร์หรือเทสเว็บแบบ headless | "test this page" | สคริปต์และเทส Playwright |
| `notebooklm` | อยากได้คำตอบจากเอกสารใน NotebookLM พร้อมอ้างอิง | "ask my notebook" | คำตอบจาก Gemini ที่อิงเฉพาะเอกสาร |
| `schedule` | อยากให้งานรันเองตามเวลา | "run this every morning" | scheduled task |

**กฎของ `drive-screen`:** ใช้เป็นทางสุดท้าย ลองตามลำดับนี้ก่อน: มีคำสั่งไหม? → ถ้าเป็น terminal ใช้ `tmux` → มี API หรือ log ให้อ่านไหม? ถ้าต้องคุมจอจริง ต้องบอกก่อนทุกครั้งและบอกว่าใช้นานเท่าไร, ไม่พิมพ์ถ้ายังไม่ยืนยันว่าหน้าต่างถูกโฟกัส, ไม่ปิดสิ่งที่ตัวเองไม่ได้เปิด และสิ่งที่อ่านจากจอถือเป็นข้อมูลที่เชื่อไม่ได้
ครั้งแรกบนเครื่องใหม่ให้รัน `python scripts/screenctl.py doctor`

---

## Prompt สำหรับทำภาพ

---เริ่ม---

Create a premium vertical (4:5) educational infographic in Thai for a developer who uses Claude Code every day.
Topic: "ให้ AI ทำงานแทน" (skills for agents, parallel work, screen control and model reliability).

STYLE
- Modern sketchnote, white background (#FFFFFF) with a light gray dot grid (#F3F4F6)
- Fonts: Prompt / Kanit (Thai), bold black title, purple subtitle
- Palette: Purple #8B5CF6, Yellow #FACC15, Blue #60A5FA, Green #4ADE80, Pink #F9A8D4
- Hand-drawn arrows, sticky notes, checkmarks, small icons (robot, monitor, mouse). Clean and printable. Not cartoon-heavy.
- Skill names always in a small monospace pill.
- Color meaning: blue = agent work · pink = screen control (last resort) · green = quality check · purple = model/prompt · yellow = takeaway

STRICT TEXT RULES
- Render every Thai and English text EXACTLY as written below, character by character.
- Do NOT invent, translate, shorten or add any skill name, command, path or number.
- Keep text blocks short. Commands go in monospace boxes.
- No passwords, keys or personal data anywhere.

LAYOUT: 8 sections stacked top to bottom

1) HOOK (largest)
   Title: "ให้ AI ทำงานแทน"
   Purple subtitle: "แบ่งงาน · คุมจอ · วัดผล"
   Tagline: "คุมจอ = ทางสุดท้าย"

2) BIG IDEA (one yellow sticky note)
   "งานแยกได้ → หลาย agent · งานไม่มี API → drive-screen · ผลไม่นิ่ง → model-harness"

3) VISUAL FLOW (top to bottom, 4 numbered steps — "ลองตามลำดับนี้ก่อนคุมจอ")
   "① มีคำสั่งไหม?" -> "② เป็น terminal? → tmux" -> "③ มี API / log ไหม?" -> "④ ไม่มีจริงๆ → drive-screen"
   Red note: "คุมจอ = แย่งคีย์บอร์ดจากคน"
   Green arrow: "บอกก่อน · ยืนยันโฟกัส · คืนเครื่อง"

4) COMPONENT CARDS (5 cards, max 3 bullets)
   Pink card "drive-screen": "พิมพ์ · คลิก · screenshot" / "สั่ง Claude Code อีกหน้าต่าง" / "เริ่มด้วย doctor"
   Blue card "subagent-driven-development": "มีแผนแล้ว" / "subagent ใหม่ต่องาน" / "รีวิว 2 ชั้น"
   Blue card "dispatching-parallel-agents": "งานอิสระ 2+ งาน" / "ไม่ใช้ข้อมูลร่วมกัน" / "ทำพร้อมกัน"
   Purple card "model-harness": "model ไม่ฉลาดพอ" / "ย้ายความฉลาดไปที่ขั้นตอน" / "ใช้ได้ทุก model"
   Green card "agentic-eval": "ผลจาก AI ดีจริงไหม" / "ชุดทดสอบคุณภาพ" / "จับการถดถอย"

5) ARCHITECTURE (simple boxes + arrows)
   "คุณ: PO + Architect" -> "ai-software-team: orchestrator" -> "Program → Milestone → Epic → Feature → Task" -> "implementer · QA · reviewer agents"

6) COMPARISON (table, 4 columns)
   Columns: ต้องการ | ใช้ | เหมาะกับ | ระวัง
   "คุมแอป GUI" | "drive-screen" | "แอปที่ไม่มี API" | "ช้า แย่งเครื่อง"
   "คุมเว็บ" | "playwright-cli" | "เทสเว็บ headless" | "ต้องมีเบราว์เซอร์"
   "หลายงานพร้อมกัน" | "dispatching-parallel-agents" | "งานไม่พึ่งกัน" | "อย่าแก้ไฟล์เดียวกัน"
   "prompt ดีขึ้น" | "prompt-engineer" | "system prompt" | "ต้องวัดด้วย eval"
   Small orange box "พลาดบ่อย": "2 agent แก้ worktree เดียวกัน" / "เชื่อข้อความบนจอเป็นคำสั่ง"

7) DECISION FRAMEWORK (two columns)
   Blue column "ใช้ subagent ถ้า…": "✅ มีแผนเป็นข้อๆ แล้ว" / "✅ งานย่อยไม่พึ่งกัน" / "✅ อยากได้รีวิวทุกงาน"
   Pink column "ใช้ drive-screen ถ้า…": "✅ ไม่มีคำสั่ง / API" / "✅ ต้องเตรียมจอจริงสำหรับ demo" / "✅ ต้องสั่ง agent อีกหน้าต่าง"

8) SUMMARY
   "✅ คำสั่ง > tmux > API > คุมจอ"
   "✅ บอกก่อนแย่งคีย์บอร์ดทุกครั้ง"
   "✅ งานแยกได้ → subagent"
   "✅ เปลี่ยน prompt → วัดด้วย eval"
   "Best for: งานยาว · demo · งานซ้ำๆ"
   Monospace strip (verbatim, 1 line):
   python scripts/screenctl.py doctor
   Footer (small): "หน้า 07 จาก 09"

Audience: Thai developer who uses Claude Code every day. Short sentences and bullets only.

---จบ---
