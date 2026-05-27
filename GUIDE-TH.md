# 9arm-skills — คู่มือการใช้งาน (ภาษาไทย-อังกฤษ)
> อ่านครั้งเดียวตอนเริ่มต้น แล้วเปิดดูตามหัวข้อเวลาลืม | อัปเดต: 2026-05-27

---

## 1. ภาพรวม — คิดแบบนี้ทุกครั้ง

```
ทุก session มี 3 ช่วงที่ต้องใช้ skill:

  PLAN (วางแผน)  →  BUILD (เขียนโค้ด)  →  SHIP (ส่งงาน)

  PLAN:  grill-with-docs (มี code อยู่แล้ว) | grill-me (โปรเจกต์ใหม่)
  BUILD: writing-plans → tdd → verification-before-completion
  SHIP:  code-review → git-workflow
```

> 💡 **จำไว้:** ไม่ต้องโหลด skill ทุกตัว — เลือกแค่ tier ที่เหมาะกับงาน
> ยิ่งโหลดน้อย = Claude ตอบเร็วขึ้น + ประหยัด token

---

## 2. เริ่มโปรเจกต์ใหม่

```bash
# ขั้นตอนที่ 1 — สร้างไฟล์ config ให้โปรเจกต์
bash ~/9arm-skills/scripts/init-project.sh ~/myproject engineering

# ขั้นตอนที่ 2 — เปิด Claude Code (skills โหลดอัตโนมัติจาก CLAUDE.md)
cd ~/myproject && claude
```

แค่นี้พอ — Claude Code อ่าน `CLAUDE.md` แล้วโหลด skill ที่ระบุไว้เท่านั้น

**เลือก type ไหน?**

| Type | ใช้ตอนไหน |
|------|-----------|
| `engineering` | เขียน TypeScript, Python, Next.js, แอปทั่วไป |
| `ai-agent` | สร้าง AI features, prompts, เชื่อมต่อ LLM, evals |
| `hermes` | แก้ตัว Hermes เอง, MCP tools, agent orchestration |
| `planning` | วางแผน product/feature ก่อนเขียน code แม้แต่บรรทัดเดียว |
| `full` | ใช้น้อยมาก — เฉพาะตอนต้องการทุกอย่าง (~20,000t) |

> ⚠️ `full` ใช้ token เยอะมาก เปิดแค่ตอนจำเป็นจริงๆ

---

## 3. Tier 0 — โหลดทุก Session อัตโนมัติ

4 skill นี้โหลดเสมอผ่าน `~/CLAUDE.md` — ไม่ต้องพิมพ์อะไร

---

### 🔍 `systematic-debugging` — ใช้ทุกครั้งที่มี bug

**4 ขั้นตอน ห้ามข้าม:**

```
1. REPRODUCE — จำลอง bug ให้เกิดซ้ำได้ด้วย case เล็กที่สุด
               บันทึก environment (OS, version, config)

2. TRACE     — ตามรอยจาก symptom (อาการ) ไปหา root cause (ต้นเหตุจริงๆ)
               log state ทุกขั้น อย่าเดา

3. FALSIFY   — ตั้ง hypothesis แล้วทดสอบ — เปลี่ยนทีละตัวแปร
               ถ้า hypothesis ผิด → ตั้งใหม่ อย่าแก้แบบสุ่ม

4. VERIFY    — ยืนยันว่า bug หายจริง + test เก่าไม่พัง (regression)
```

❌ **ห้ามเด็ดขาด:** แก้แบบสุ่มหวังโชค | แก้แค่ symptom | ข้ามขั้นตอน | ไม่จด

---

### 🎯 `grill-me` / `grill-with-docs` — เลือกอัตโนมัติ

| สถานการณ์ | Skill ที่ใช้ |
|-----------|-------------|
| โปรเจกต์ใหม่ ยังไม่มี code | `grill-me` — ถามทีละคำถาม เพื่อให้ requirement ชัด |
| มี code อยู่แล้ว หรือมี `CONTEXT.md` | `grill-with-docs` — วิเคราะห์ codebase อัปเดต docs |

> **กฎ:** ถ้ามีโฟลเดอร์ `src/` หรือไฟล์ `CONTEXT.md` → `grill-with-docs` รันก่อนเสมอ

**grill-with-docs ทำอะไร?**
- อ่าน `CONTEXT.md` + `docs/adr/` ที่มีอยู่
- ตรวจสอบว่าแผนใหม่ขัดกับ decision เก่าไหม
- อัปเดต `CONTEXT.md` เมื่อตกลงอะไรได้
- สร้าง ADR (Architecture Decision Record) เฉพาะตอนตัดสินใจสำคัญ

---

### 📝 `git-workflow` — ทุกครั้งที่ commit

**รูปแบบ commit message:**
```
feat(scope): สิ่งที่เพิ่ม
fix(scope): สิ่งที่แก้
chore: งาน housekeeping ทั่วไป
docs: แก้เฉพาะ documentation
refactor: refactor โค้ด ไม่เปลี่ยน behavior
test: เพิ่ม/แก้ test
perf: ปรับ performance
```

**ตัวอย่างจริง:**
```
feat(delivery-notes): add PDF export button
fix(auth): redirect to login on token expiry
chore: upgrade Next.js to 15.2
```

**PR description ต้องมีเสมอ:**
- **What changed** — เปลี่ยนอะไร
- **Why** — ทำไมต้องเปลี่ยน
- **How to test** — ทดสอบยังไง

---

## 4. Engineering Work — Tier 1

โหลดเหล่านี้ตอนพัฒนา feature:

---

### 📋 `writing-plans` — ก่อนเขียน code แม้แต่บรรทัดเดียว

แบ่งงานเป็นชิ้น **2-5 นาที** แต่ละชิ้นต้องมี:
- ระบุ file path ที่จะแก้ให้ชัดเจน
- ผลลัพธ์ที่ต้องการ 1 อย่างเท่านั้น
- scope ชัดเจน ไม่คลุมเครือ

**ตัวอย่างแผนที่ดี:**
```
Task 1 (3 min): แก้ src/app/api/delivery-notes/route.ts
  → เพิ่ม validation สำหรับ field "customerName" ต้องไม่ว่าง
  → return 400 พร้อม error message ถ้า validate ไม่ผ่าน

Task 2 (4 min): แก้ src/components/DeliveryForm.tsx
  → แสดง error message ใต้ field customerName
  → clear error เมื่อ user พิมพ์ใหม่
```

> 💡 แผนแย่เสียเวลา 10 นาที — ไม่มีแผนเสียเวลา 2 ชั่วโมง

---

### 🔴 `tdd` — RED → GREEN → REFACTOR

```
1. 🔴 RED     — เขียน test ที่ยังพังก่อน — หยุด ยังเขียน code ไม่ได้
2. 🟢 GREEN   — เขียน code น้อยที่สุดที่ทำให้ test ผ่าน
3. 🔵 REFACTOR — ทำความสะอาด code โดยไม่ให้ test พัง
```

**กฎเหล็ก:** ถ้าเขียน code ก่อน test → ลบทิ้ง แล้วเริ่มใหม่ตามลำดับ

**ตัวอย่างในชีวิตจริง:**
```typescript
// 🔴 RED — เขียน test ก่อน (ยัง fail)
it('should return 400 if customerName is empty', async () => {
  const res = await POST({ customerName: '' })
  expect(res.status).toBe(400)
})

// 🟢 GREEN — เขียน code ให้ผ่าน
if (!customerName) return NextResponse.json({ error: '...' }, { status: 400 })

// 🔵 REFACTOR — เก็บให้สะอาด
const validateCustomer = (name: string) => name.trim().length > 0
```

---

### ✅ `verification-before-completion` — ก่อนบอกว่า "เสร็จแล้ว"

checklist ก่อน mark task ว่าเสร็จ:
- [ ] จำลอง bug เดิม — ยืนยันว่าหายแล้ว
- [ ] รัน test ทั้งหมด — ไม่มี regression
- [ ] เช็ค edge cases ที่ระบุใน task
- [ ] ไม่มี console error หรือ warning ใหม่

> อย่ารีบบอกว่าเสร็จ — ใช้เวลา 2 นาทีเช็ค checklist นี้ก่อน

---

### 👁️ `code-review` — ก่อน merge ทุกครั้ง

review checklist:
- [ ] **Security:** ไม่มี secret ใน code, validate input ครบ
- [ ] **Performance:** ไม่มี N+1 query, ไม่ re-render โดยไม่จำเป็น
- [ ] **Naming:** ชื่อตัวแปร/function บอกความหมายชัดเจน
- [ ] **Dead code:** ไม่มี code ที่ไม่ได้ใช้เหลืออยู่
- [ ] **Tests:** มี test cover การเปลี่ยนแปลงที่ทำ
- [ ] **Accessibility (UI):** มี ARIA labels, ใช้ keyboard ได้

---

## 5. AI/Agent Work — Tier 2

โหลดเหล่านี้ตอนสร้าง AI features หรือรัน subagents:

---

### 🤖 `subagent-driven-development` — กระจายงานให้ subagent

ส่งงานให้ subagent ใหม่ทีละ task:
1. **Stage 1:** ตรวจว่าตรง spec ไหม (requirements ครบหรือเปล่า)
2. **Stage 2:** ตรวจ code quality (สะอาด อ่านง่าย ไหม)

> อย่าให้ agent เดียวทำทุกอย่างในรอบเดียว — แยกเป็น task ย่อย

---

### ⚡ `dispatching-parallel-agents` — รัน task พร้อมกันหลายตัว

ใช้ตอน task เหล่านั้นทำงานคู่ขนานกันได้:

```
✅ ทำพร้อมกันได้:  เขียน test | อัปเดต docs | เพิ่ม TypeScript types
❌ ทำพร้อมกันไม่ได้: task B ต้องรอผลจาก task A ก่อน
```

---

### ✍️ `prompt-engineer` — ตอนเขียน prompt ให้ AI

- ระบุ format, ความยาว, โทนให้ชัดเจน
- ใส่ตัวอย่าง (few-shot) สำหรับ output ที่ซับซ้อน
- ทดสอบกับ edge cases: input ว่าง, input ยาวมาก, input แปลกๆ
- วัดผล: output ดีขึ้นจริงไหม?

---

## 6. ลำดับการทำงานแบบเต็ม

```
1. วางแผน (PLAN)
   ├── มี code อยู่แล้ว → grill-with-docs → อัปเดต CONTEXT.md
   └── โปรเจกต์ใหม่    → grill-me → ยืนยัน requirements

2. แบ่งงาน (BREAK DOWN)
   └── writing-plans → แบ่งเป็น task 2-5 นาที พร้อม file path

3. เขียนโค้ด (BUILD) — ทำทีละ task
   ├── tdd: เขียน test fail → เขียน code → refactor
   └── ถ้ามี bug → systematic-debugging (4 phases ห้ามข้าม)

4. ตรวจสอบ (VERIFY)
   └── verification-before-completion → bug หาย + test ผ่านทั้งหมด

5. Review (REVIEW)
   └── code-review → security + perf + naming + dead code + tests

6. ส่งงาน (SHIP)
   └── git-workflow → conventional commit → PR พร้อม What/Why/How
```

---

## 7. จัดการ Token

**กฎ:** โหลดแค่ tier ที่ต้องการ ไม่โหลดเกิน

```
วางแผนอย่างเดียว?         → planning    (~4,500t)
เขียน app code ทั่วไป?     → engineering  (~9,500t)
สร้าง AI features?         → ai-agent    (~13,000t)
แก้ Hermes?                → hermes      (~9,000t)
ต้องการทุกอย่าง?           → full        (~20,000t) ← หลีกเลี่ยง
```

**โหลด skill เพิ่มตอน on-demand** — สำหรับ skill ที่ไม่ได้อยู่ใน CLAUDE.md:
```
"load skill: ~/9arm-skills/skills/engineering/search-first/SKILL.md"
```

**Personal skills ห้ามโหลดอัตโนมัติ** — `andaman-context`, `document-skill` ต้องพิมพ์ขอเองเท่านั้น

---

## 8. คำสั่งที่ใช้บ่อย

```bash
# สร้าง config สำหรับโปรเจกต์ใหม่
bash ~/9arm-skills/scripts/init-project.sh <path> <type>

# ตรวจสอบว่า setup ถูกต้องทั้งหมด (รันหลังแก้ไขอะไรก็ตาม)
bash ~/9arm-skills/scripts/validate.sh

# ดูค่า token ของแต่ละ skill
bash ~/9arm-skills/scripts/token-audit.sh

# แสดงรายชื่อ skill ทั้งหมดพร้อม tier และ description
bash ~/9arm-skills/scripts/list-skills.sh

# เชื่อม skill เข้า ~/.claude/skills/ (ให้ Claude Code หาเจอ)
bash ~/9arm-skills/scripts/link-skills.sh

# อัปเดต superpowers เป็น version ล่าสุด
git -C ~/9arm-skills subtree pull --prefix=upstream/superpowers superpowers main --squash
```

---

## 9. แก้ปัญหาเมื่อมีอะไรผิดพลาด

| ปัญหา | วิธีแก้ |
|-------|---------|
| Claude หา skill ไม่เจอ | รัน `link-skills.sh` แล้วเช็ค path ใน `CLAUDE.md` |
| ใช้ token เยอะเกินไป | เปลี่ยนเป็น profile ที่เล็กกว่า ย้าย skill ไป on-demand |
| `validate.sh` ขึ้น ❌ | อ่าน error message แล้วเช็ค path ใน `tier-manifest.yaml` |
| เนื้อหา skill เก่าแล้ว | `git -C ~/9arm-skills pull origin main` |
| Superpowers ล้าสมัย | `git subtree pull --prefix=upstream/superpowers superpowers main --squash` |
| `CONTEXT.md` ผิดพลาด | ลบทิ้ง แล้วรัน `grill-with-docs` ใหม่ |

---

## 10. เพิ่ม Skill ใหม่

1. สร้าง directory: `~/9arm-skills/skills/<category>/<skill-name>/`
2. เขียน `SKILL.md` พร้อม frontmatter:
   ```yaml
   ---
   name: skill-name
   description: หนึ่งบรรทัด — ใช้ skill นี้ตอนไหน
   tags: [tag1, tag2]
   tier: 0|1|2|3|personal
   estimated_tokens: <จำนวนตัวอักษร/4>
   ---
   ```
3. รัน `token-audit.sh` — ตรวจว่าไม่ 🔴 HEAVY โดยไม่จำเป็น
4. เพิ่มใน `tier-manifest.yaml` ที่ tier ที่เหมาะสม
5. เพิ่ม reference ใน `README.md`
6. รัน `validate.sh`
7. Commit: `docs(skills): add <skill-name>`

> ใช้ skill `document-skill` เป็นแนวทางตอนเขียน skill ใหม่

---

## 11. แต่ละ Surface ทำงานยังไง

| Surface | วิธีโหลด skill | ไฟล์ config |
|---------|--------------|------------|
| Claude Mobile | Custom Instructions (สรุป Tier 0) | Settings → Custom Instructions |
| Claude Desktop | Custom Instructions (Tier 0 เต็ม) | Settings → Custom Instructions |
| Claude Code | โหลดอัตโนมัติจาก `CLAUDE.md` | `~/CLAUDE.md` + per-project |
| Hermes (MiniMax) | ผ่าน MCP tool `claude_code_with_skills` | `~/.hermes/mcp_tools/` |

---

## สรุปเร็ว — กฎ 5 ข้อที่จำไว้เสมอ

```
1. มี bug?          → systematic-debugging 4 phases ห้ามข้าม
2. โค้ดใหม่?        → เขียน test ก่อน แล้วค่อยเขียน code (TDD)
3. Task เสร็จ?       → verification-before-completion ก่อน mark done
4. จะ commit?       → conventional commits เสมอ
5. Session ยาว?     → strategic-compact เพื่อสรุป context
```

---

*ไฟล์นี้อยู่ที่ `~/9arm-skills/GUIDE-TH.md` — แก้ไขเมื่อ convention เปลี่ยน*
