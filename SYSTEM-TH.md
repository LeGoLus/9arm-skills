# ภาพรวมระบบทั้งหมด — LeGoLus AI Workflow
> อ่านหน้านี้ก่อนทุกอย่าง | ดู GUIDE-TH.md สำหรับวิธีใช้งานละเอียด
> Updated: 2026-05-28

---

## 🗺️ แผนผังระบบ (Big Picture)

```
                    ┌─────────────────────────────────────────┐
                    │     github.com/LeGoLus/9arm-skills       │
                    │        📚 ห้องสมุด skill ทั้งหมด          │
                    │     28 skills | GUIDE-TH | SYSTEM-TH     │
                    └──────────┬──────────────────────────────┘
                               │ โหลด skill ตาม tier
          ┌────────────────────┼────────────────────────┐
          │                    │                        │
          ▼                    ▼                        ▼
  ┌───────────────┐   ┌────────────────┐    ┌──────────────────┐
  │ Claude Mobile │   │ Claude Desktop │    │   Claude Code    │
  │  ~450t always │   │  ~600t always  │    │  per-project     │
  │  Tier 0 only  │   │  Tier 0 full   │    │  from CLAUDE.md  │
  └───────────────┘   └────────────────┘    └────────┬─────────┘
                                                     │
                                          ┌──────────┴──────────┐
                                          │                     │
                                          ▼                     ▼
                                  ┌──────────────┐   ┌──────────────────┐
                                  │  ~/.hermes/  │   │  awoms-app/      │
                                  │  (Hermes AI) │   │  (Andaman/AWOMS) │
                                  │  hermes type │   │  engineering type│
                                  └──────┬───────┘   └──────────────────┘
                                         │
                                         ▼
                                  ┌──────────────┐
                                  │ Hermes M2.7  │◄── MCP Tool:
                                  │  MiniMax via │    claude_code_with_skills
                                  │  minimax.io  │    (delegate → Claude Code)
                                  └──────────────┘
```

---

## 📁 3 Repo หลัก

```
~/
├── 9arm-skills/          ← 🧠 ศูนย์กลาง skill library
│   ├── skills/           ← SKILL.md ทุกตัว (28+ skills)
│   ├── scripts/          ← เครื่องมือ: init, validate, audit
│   ├── tier-manifest.yaml← จัด skill เป็น tier 0-3
│   ├── catalog.json      ← สำหรับ SkillManager app
│   ├── GUIDE-TH.md       ← วิธีใช้ skill (อ่านครั้งเดียว)
│   ├── SYSTEM-TH.md      ← ไฟล์นี้ (ภาพรวมระบบ)
│   └── upstream/         ← git subtree: obra/superpowers
│
├── LifeVault/            ← 📔 Obsidian knowledge base
│   ├── 10-Projects/      ← project notes ต่างๆ
│   ├── 20-Areas/AI-Workflow/ ← skill-system.md quick ref
│   ├── 30-Resources/     ← บทความ, links อ้างอิง
│   └── 40-Archive/       ← งานเก่า
│
└── NotebooksLM/          ← 📄 raw source files สำหรับ AI
    ├── hermes-ai-agent/sources/
    ├── andaman-print/sources/
    └── skill-ecosystem/sources/
```

**GitHub status:**
| Repo | URL | Visibility | สถานะ |
|------|-----|-----------|-------|
| 9arm-skills | github.com/LeGoLus/9arm-skills | 🌐 Public | ✅ Live |
| LifeVault | github.com/LeGoLus/LifeVault | 🔒 Private | ✅ Live |

---

## 🗂️ Projects ที่กำลังทำงาน

```
┌────────────────────────────────────────────────────────────┐
│  Project 1: Hermes AI Agent                                │
│  Path:   ~/.hermes/                                        │
│  Type:   hermes (init-project type)                        │
│  Model:  MiniMax M2.7 via minimax.io                       │
│  Skills: systematic-debugging, grill-with-docs,            │
│          subagent-driven-dev, dispatching-parallel-agents  │
│  MCP:    ~/.hermes/mcp_tools/claude_code_skill.py          │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  Project 2: Andaman / AWOMS                                │
│  Path:   ~/Documents/Andaman/AWOMS/awoms-app/              │
│  Type:   engineering (init-project type)                   │
│  Stack:  Next.js, TypeScript, Tailwind                     │
│  Skills: tdd, code-review, error-handling,                 │
│          verification-before-completion, writing-plans     │
│  API:    src/app/api/delivery-notes/                       │
└────────────────────────────────────────────────────────────┘
```

---

## 🎯 4 Surfaces — ใช้อะไรตอนไหน?

```
┌──────────────────┬────────────────────────────┬────────────┐
│ Surface          │ เปิดตอนไหน                  │ Token ~    │
├──────────────────┼────────────────────────────┼────────────┤
│ Claude Mobile    │ คิดเร็ว, ถามทั่วไป           │ ~450t      │
│                  │ Tier 0 อยู่ใน Custom Instr.  │            │
├──────────────────┼────────────────────────────┼────────────┤
│ Claude Desktop   │ งานที่ไม่ต้องการ file access │ ~600t      │
│                  │ Tier 0 full ใน Custom Instr. │            │
├──────────────────┼────────────────────────────┼────────────┤
│ Claude Code      │ เขียน/แก้โค้ด, อ่านไฟล์จริง │ ~9,500t    │
│ (CLI: claude)    │ โหลด skill จาก CLAUDE.md    │            │
├──────────────────┼────────────────────────────┼────────────┤
│ Hermes (M2.7)    │ งาน orchestration, MCP      │ ~9,000t    │
│                  │ delegate → Claude Code      │            │
└──────────────────┴────────────────────────────┴────────────┘
```

---

## 📊 Tier System — โหลด skill แค่ไหน?

```
TIER 0 — โหลดทุก session อัตโนมัติ (~4,923t)
┌─────────────────────────────────────────────┐
│ systematic-debugging  git-workflow           │
│ grill-me              grill-with-docs        │
└─────────────────────────────────────────────┘
         ▼ เพิ่มสำหรับงาน Engineering
TIER 1 (~+9,500t)
┌─────────────────────────────────────────────┐
│ tdd  code-review  error-handling            │
│ verification-before-completion              │
│ writing-plans  executing-plans              │
│ strategic-compact  verification-loop        │
└─────────────────────────────────────────────┘
         ▼ เพิ่มสำหรับงาน AI/Agent
TIER 2 (~+7,000t)
┌─────────────────────────────────────────────┐
│ subagent-driven-development                 │
│ dispatching-parallel-agents                 │
│ prompt-engineer  agentic-eval               │
│ continuous-learning  security-review        │
└─────────────────────────────────────────────┘
         ▼ โหลดเฉพาะตอนต้องการ (on-demand)
TIER 3 (say: "load skill: <path>")
┌─────────────────────────────────────────────┐
│ post-mortem  scrutinize  debug-mantra       │
│ management-talk  search-first               │
│ using-git-worktrees  write-a-prd            │
│ finishing-dev-branch  improve-arch          │
│ receiving-code-review                       │
└─────────────────────────────────────────────┘
         ▼ ต้องพิมพ์ขอเองเท่านั้น
PERSONAL (explicit only)
┌─────────────────────────────────────────────┐
│ andaman-context  document-skill             │
└─────────────────────────────────────────────┘
```

---

## 🔄 Data Flow — ข้อมูลไหลยังไง?

```
คุณ (LeGoLus)
    │
    ├── คิด/วางแผน ──────────────► Claude Mobile / Desktop
    │                               (Tier 0 เท่านั้น)
    │
    ├── เขียนโค้ด ────────────────► Claude Code (claude CLI)
    │   cd <project> && claude       อ่าน CLAUDE.md → โหลด skill
    │                               เขียน/แก้ไฟล์ใน project จริง
    │
    ├── งาน AI/Orchestration ────► Hermes (MiniMax M2.7)
    │                               Hermes → claude_code_with_skills
    │                               → Claude Code → แก้โค้ด → return
    │
    ├── บันทึกความรู้ ────────────► LifeVault (Obsidian)
    │                               CONTEXT.md, ADRs, notes
    │
    └── เก็บ raw sources ─────────► NotebooksLM
                                    PDFs, specs, reference docs
```

---

## 🚦 Decision Tree — "ฉันจะทำอะไร?"

```
ฉันจะ...
│
├── ถามคำถามทั่วไป / คิดเร็ว
│   └── ► Claude Mobile
│
├── วางแผน feature ใหม่ (ยังไม่มีโค้ด)
│   └── ► Claude Code: /grill-me
│
├── เขียน/แก้โค้ด
│   ├── มี CONTEXT.md หรือ src/ อยู่แล้ว
│   │   └── ► Claude Code: /grill-with-docs ก่อน → writing-plans → tdd
│   └── โปรเจกต์ใหม่
│       └── ► Claude Code: /grill-me ก่อน → writing-plans → tdd
│
├── Debug / มี bug
│   └── ► Claude Code: systematic-debugging 4 phases
│
├── Review code ก่อน merge
│   └── ► Claude Code: /code-review
│
├── งาน AI/LLM features
│   └── ► Claude Code (ai-agent type): prompt-engineer + agentic-eval
│
├── orchestrate หลาย agent
│   └── ► Hermes → claude_code_with_skills (dispatching-parallel-agents)
│
├── เกิด production incident
│   └── ► Claude Code: systematic-debugging → post-mortem
│
├── ต้องสื่อสารกับ stakeholder/ผู้บริหาร
│   └── ► Claude Code: "load skill: management-talk"
│
└── บันทึก decision / สิ่งที่เรียนรู้
    └── ► LifeVault (Obsidian) หรือ CONTEXT.md ใน project
```

---

## ⚡ Quick Commands

```bash
# เปิดโปรเจกต์ใหม่ (สร้าง CLAUDE.md)
bash ~/9arm-skills/scripts/init-project.sh <path> engineering

# เปิด Claude Code
cd <project> && claude

# ตรวจสอบระบบทั้งหมด (ต้องผ่าน 34/34)
bash ~/9arm-skills/scripts/validate.sh

# ดู skill ทั้งหมดพร้อม tier
bash ~/9arm-skills/scripts/list-skills.sh

# ดูค่า token แต่ละ skill
bash ~/9arm-skills/scripts/token-audit.sh

# อัปเดต superpowers
git -C ~/9arm-skills subtree pull --prefix=upstream/superpowers superpowers main --squash
```

---

## 📍 ไฟล์สำคัญ — อยู่ที่ไหน?

```
~/CLAUDE.md                              ← global config (Tier 0 always load)
~/9arm-skills/tier-manifest.yaml         ← tier ของแต่ละ skill
~/9arm-skills/catalog.json              ← สำหรับ SkillManager app
~/9arm-skills/GUIDE-TH.md               ← วิธีใช้งานละเอียด (อ่านครั้งเดียว)
~/9arm-skills/SYSTEM-TH.md              ← ไฟล์นี้ (ภาพรวม)
~/.hermes/CLAUDE.md                     ← config สำหรับ Hermes project
~/.hermes/tools/claude_code_tool.py     ← Hermes → Claude Code bridge
~/.hermes/mcp_tools/claude_code_skill.py← MCP server
~/Documents/Andaman/AWOMS/awoms-app/CLAUDE.md ← config สำหรับ AWOMS
~/LifeVault/20-Areas/AI-Workflow/skill-system.md ← quick ref ใน vault
```

---

## 🗓️ Maintenance Schedule

```
ทุกครั้งที่เพิ่ม skill ใหม่:
  □ สร้าง SKILL.md พร้อม frontmatter
  □ อัปเดต tier-manifest.yaml
  □ อัปเดต catalog.json
  □ เพิ่มใน README.md
  □ รัน validate.sh → ผ่านทุกข้อ
  □ commit + push

ทุก 2-4 สัปดาห์:
  □ git subtree pull superpowers (อัปเดต upstream)
  □ รัน token-audit.sh (ตรวจ skill ที่ HEAVY เกินไป)
  □ รัน validate.sh (ยืนยันระบบยัง 34/34)
```

---

*ดูรายละเอียดการใช้งาน: [GUIDE-TH.md](./GUIDE-TH.md)*
*ดู skill ทั้งหมด: [README.md](./README.md)*
*Source: github.com/LeGoLus/9arm-skills*
