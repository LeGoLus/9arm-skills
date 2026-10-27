# 05 · Git และการส่งงาน (Git + Ship)

> ไฟล์นี้ไม่มีรหัสผ่าน, token หรือข้อมูลส่วนตัว

## จำเร็ว

| Skill | ใช้เมื่อ | เรียกยังไง | ได้อะไรออกมา |
|---|---|---|---|
| `git-workflow` ★ Tier 0 | ทุกครั้งที่ commit, สร้าง branch หรือเปิด PR | อัตโนมัติหลังทำงานเสร็จ | conventional commit (`feat:`, `fix:`, `docs:`…), commit ละเรื่อง และคำอธิบาย PR ที่รีวิวง่าย |
| `using-git-worktrees` | ทำหลาย branch พร้อมกันโดยไม่ต้อง stash | "use a worktree" | โฟลเดอร์แยกต่อ branch |
| `finishing-a-development-branch` | ทำเสร็จและเทสผ่านแล้ว แต่ยังไม่รู้ว่าจะรวมแบบไหน | "finish this branch" | ตัวเลือก merge, PR หรือ cleanup พร้อมเช็กลิสต์ |
| `resolving-merge-conflicts` | merge หรือ rebase ค้างเพราะ conflict | "resolve the conflict" | แก้ conflict ทีละไฟล์ โดยเข้าใจว่าแต่ละฝั่งตั้งใจทำอะไร |
| `git-guardrails` | อยากกัน `reset --hard` และ `push --force` ไม่ให้เกิดโดยไม่ตั้งใจ | "add git safety hooks" | hook ของ Claude Code ที่บล็อกคำสั่ง git อันตราย |
| `setup-pre-commit` | โปรเจกต์ JS/TS ต้องการ pre-commit hook | "set up husky" | Husky + lint-staged (Prettier) + typecheck + test (ใช้กับ Python ไม่ได้) |

**เส้นทางปกติ:** branch → commit ทีละเรื่อง (`git-workflow`) → `verification-loop` → `finishing-a-development-branch` → PR หรือ merge

---

## Prompt สำหรับทำภาพ

---เริ่ม---

Create a premium vertical (4:5) educational infographic in Thai for a developer who uses Claude Code every day.
Topic: "Commit สวย ส่งงานปลอดภัย" (the git and shipping skills).

STYLE
- Modern sketchnote, white background (#FFFFFF) with a light gray dot grid (#F3F4F6)
- Fonts: Prompt / Kanit (Thai), bold black title, purple subtitle
- Palette: Purple #8B5CF6, Yellow #FACC15, Blue #60A5FA, Green #4ADE80, Pink #F9A8D4
- Hand-drawn arrows, sticky notes, checkmarks, small icons, git branch lines. Clean and printable. Not cartoon-heavy.
- Skill names always in a small monospace pill.
- Color meaning: blue = branch/commit · green = merged/safe · pink/red = dangerous command · yellow = takeaway

STRICT TEXT RULES
- Render every Thai and English text EXACTLY as written below, character by character.
- Do NOT invent, translate, shorten or add any skill name, command, path or number.
- Keep text blocks short. Commands go in monospace boxes.
- No passwords, keys or personal data anywhere.

LAYOUT: 8 sections stacked top to bottom

1) HOOK (largest)
   Title: "Commit สวย ส่งงานปลอดภัย"
   Purple subtitle: "หนึ่ง commit = หนึ่งเรื่อง"
   Tagline: "feat: · fix: · docs: · refactor:"

2) BIG IDEA (one yellow sticky note)
   "ประวัติ git ที่อ่านรู้เรื่อง คือเอกสารที่ดีที่สุดของโปรเจกต์"

3) VISUAL FLOW (git branch drawing, left to right, 4 steps)
   "① สร้าง branch" -> "② commit ทีละเรื่อง" -> "③ verification-loop ผ่าน" -> "④ finishing-a-development-branch → PR / merge"
   Red note: "push --force / reset --hard = งานหาย"
   Green arrow: "git-guardrails บล็อกให้ก่อน"

4) COMPONENT CARDS (4 cards, max 3 bullets)
   Blue card "git-workflow": "Tier 0 ทุกโปรเจกต์" / "conventional commits" / "PR ที่รีวิวง่าย"
   Purple card "using-git-worktrees": "หลาย branch พร้อมกัน" / "ไม่ต้อง stash" / "โฟลเดอร์แยกต่อ branch"
   Green card "finishing-a-development-branch": "เทสผ่านแล้ว" / "เลือก merge / PR / cleanup" / "มีเช็กลิสต์"
   Pink card "git-guardrails": "hook บล็อกคำสั่งอันตราย" / "reset --hard" / "push --force"

5) ARCHITECTURE (simple boxes + arrows)
   "git commit" -> "setup-pre-commit: Husky + lint-staged" -> "typecheck + test" -> "commit ผ่าน"
   Small note: "JS/TS เท่านั้น"

6) COMPARISON (table, 3 columns)
   Columns: สถานการณ์ | ใช้ | ผล
   "จะ commit / PR" | "git-workflow" | "ข้อความ commit มาตรฐาน"
   "merge ติด conflict" | "resolving-merge-conflicts" | "แก้ทีละไฟล์ เข้าใจทั้งสองฝั่ง"
   "งานเสร็จ จะรวม" | "finishing-a-development-branch" | "เลือกวิธีรวมพร้อมเช็กลิสต์"
   "กลัวพลาดคำสั่ง" | "git-guardrails" | "บล็อกก่อนรัน"
   Small orange box "พลาดบ่อย": "commit รวมหลายเรื่อง" / "ข้อความว่า 'update'"

7) DECISION FRAMEWORK (two columns)
   Blue column "ใช้ worktree ถ้า…": "✅ แก้ hotfix ระหว่างทำฟีเจอร์" / "✅ ให้ agent ทำคนละ branch" / "✅ ไม่อยาก stash"
   Green column "branch ธรรมดาพอ ถ้า…": "✅ ทำทีละเรื่อง" / "✅ งานสั้น" / "✅ ไม่มีใครทำคู่ขนาน"

8) SUMMARY
   "✅ หนึ่ง commit = หนึ่งเรื่อง"
   "✅ ขึ้นต้นด้วย feat: / fix: / docs:"
   "✅ ตรวจผ่านก่อน push"
   "✅ ห้าม force push ไป main"
   "Best for: ทุก repo"
   Monospace strip (verbatim, 1 line):
   git commit -m "feat(skills): add anatomy skill"
   Footer (small): "หน้า 05 จาก 09"

Audience: Thai developer who uses Claude Code every day. Short sentences and bullets only.

---จบ---
