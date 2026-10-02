# TASK_BRAIN.md — Project Execution Context
> **AI Agent**: อ่านไฟล์นี้ทั้งหมดก่อนทำงาน
> อัพเดท section ของตัวเองทันทีหลังเสร็จแต่ละ task
> ห้ามลบ LOG entries เก่า — append เท่านั้น

---

## 📋 PROJECT OVERVIEW

**Project**  : 9arm-skills — LeGoLus skill library for Claude Code
**Goal**     : Maintain the single source-of-truth repo of Claude Code skills (SKILL.md files, organized by bucket: engineering/productivity/ai-agent/meta/personal/in-progress/deprecated), with catalog.json + tier-manifest.yaml describing tiers/budgets, and scripts (init-project.sh, link-skills.sh, validate.sh, token-audit.sh) that scaffold per-project CLAUDE.md files and keep ~/.claude/skills/ symlinked to this repo. This repo is the skill ecosystem itself — every other project (hermes, andaman/awoms, etc.) consumes skills from here.
**Deadline** : — (ongoing maintenance repo, no fixed deadline)
**Output**   : Markdown skill files + JSON/YAML manifests + shell scripts, committed to github.com/LeGoLus/9arm-skills
**Out path** : ~/9arm-skills/ (this repo root)

---

## 🎯 SUCCESS CRITERIA
<!-- วัดได้จริง — ไม่ใช่แค่ "ดูดี" -->

- [ ] Every skill in `engineering/`, `productivity/`, `ai-agent/`, `meta/` has a README.md reference + catalog.json entry
- [ ] `tier-manifest.yaml` lists every shippable skill under the correct tier
- [ ] `scripts/validate.sh` passes with 0 failures against the real filesystem paths it checks
- [ ] `scripts/init-project.sh` produces a correct, non-literal `$PROJECT_NAME` and correct Knowledge/Sources lines regardless of whether it's invoked with `.` or an absolute path
- [ ] No uncommitted changes left silently unpushed — human has reviewed and decided

---

## 📁 TASK LIST

### Phase 1 — dynamic-skill-init Rollout (2026-06-22)
| # | Task | Owner | State | Output path |
|---|------|-------|-------|-------------|
| 1.1 | Add `dynamic-skill-init` skill (tailors a project's CLAUDE.md skill list by reading its own IMPLEMENTATION.md/PRD.md/CONTEXT.md/TASK_BRAIN.md instead of a fixed profile) | `code` | `[x]` | skills/productivity/dynamic-skill-init/SKILL.md |
| 1.2 | Register `dynamic-skill-init` in catalog.json (productivity, tier 3) | `code` | `[x]` | catalog.json |
| 1.3 | Register `dynamic-skill-init` in tier-manifest.yaml (tier_3_optional) | `code` | `[x]` | tier-manifest.yaml |
| 1.4 | Fix `init-project.sh` bug: `$PROJECT_NAME` became literal `.` when script invoked with `.` as the path arg — now resolves via `basename "$(cd "$PROJECT_PATH" && pwd)")` | `code` | `[x]` | scripts/init-project.sh |
| 1.5 | Fix `init-project.sh` stale template lines pointing at wrong LifeVault/NotebooksLM path patterns (Knowledge line now points at the one-file-per-project `.md` convention, not a folder; Sources line now points at TASK_BRAIN.md instead of a NotebooksLM path) | `code` | `[x]` | scripts/init-project.sh |
| 1.6 | Fix `validate.sh` stale hardcoded AWOMS path — was checking `~/Documents/Andaman/AWOMS/awoms-app/CLAUDE.md` (does not exist on disk), now checks `~/projects/awoms-app/awoms-app/CLAUDE.md` (confirmed exists) | `code` | `[x]` | scripts/validate.sh |
| 1.7 | Commit and push today's dynamic-skill-init + bug fix changes (catalog.json, tier-manifest.yaml, scripts/init-project.sh, scripts/validate.sh, new skills/productivity/dynamic-skill-init/, new skills/engineering/ui-ux-pro-max/) | `human` | `[ ]` | git commit + git push |

### Phase 2 — LifeVault GitHub Sync (from MASTER_IMPLEMENTATION.md TODO 1)
| # | Task | Owner | State | Output path |
|---|------|-------|-------|-------------|
| 2.1 | Fix LifeVault empty folders not tracked on GitHub (10-Projects, 30-Resources, 40-Archive, 90-Templates missing — add `.gitkeep` or check `.gitignore` for accidental excludes) | `human` | `[?]` | ~/LifeVault/ |

### Phase 3 — SkillManager App Integration (from MASTER_IMPLEMENTATION.md TODO 2)
| # | Task | Owner | State | Output path |
|---|------|-------|-------|-------------|
| 3.1 | Evaluate/install tddworks/SkillsManager (macOS app) as a GUI browse/install layer over this repo's catalog.json | `human` | `[ ]` | — |
| 3.2 | `catalog.json` SkillManager-compatible format | `code` | `[x]` | catalog.json (already exists and is actively maintained — see Phase 1) |

### Phase 4 — Hermes MCP Tool (from MASTER_IMPLEMENTATION.md TODO 3)
| # | Task | Owner | State | Output path |
|---|------|-------|-------|-------------|
| 4.1 | Create `~/hermes/tools/claude_code_tool.py` — profile-based skill loader for Hermes-delegated Claude Code tasks | `code` | `[?]` | ~/hermes/tools/claude_code_tool.py |
| 4.2 | Create `~/hermes/mcp_tools/claude_code_skill.py` — MCP tool wrapper exposing `claude_code_with_skills` to Hermes (MiniMax M2.7) | `code` | `[?]` | ~/hermes/mcp_tools/claude_code_skill.py |
| 4.3 | Add coding-task delegation rule to Hermes Control Room system prompt | `human` | `[?]` | Hermes system prompt |
| 4.4 | Test: Hermes → claude_code_with_skills → real project task | `human` | `[ ]` | — |

> Note on Phase 4: MASTER_IMPLEMENTATION.md refers to `~/hermes/` (no dot) throughout, but the actual project on this machine is `~/.hermes/` (per current global CLAUDE.md repo map and per the live `~/.hermes/CLAUDE.md`). It's unclear whether the `~/hermes/tools/` and `~/hermes/mcp_tools/` paths in the original plan were ever created, and under which actual path. Marked `[?]` — needs human review to confirm current state before treating as open work.

### Phase 5 — Other Implementation Checklist Items (from MASTER_IMPLEMENTATION.md, end of file)
| # | Task | Owner | State | Output path |
|---|------|-------|-------|-------------|
| 5.1 | Paste Custom Instructions (Claude Mobile + Desktop surfaces) from MASTER_IMPLEMENTATION.md Phase 3 | `human` | `[?]` | Claude Mobile/Desktop settings (external to this repo) |
| 5.2 | `chmod +x ~/9arm-skills/scripts/*.sh` | `code` | `[?]` | scripts/ (likely already executable — verify) |
| 5.3 | NotebooksLM folder structure scaffold (`_template`, `hermes/sources`, etc.) | `human` | `[?]` | ~/NotebooksLM/ |
| 5.4 | LifeVault `.gitkeep` fix + push (duplicate of 2.1, listed again in original checklist) | `human` | `[?]` | ~/LifeVault/ |

---

## 🔄 LAST HANDOFF
<!-- อัพเดททุกครั้งที่มีการส่งงาน — เขียนทับของเก่า -->

```
From      : code
To        : human
Date      : 2026-06-22 13:43
Reason    : task split — TASK_BRAIN.md/HTML initialized for this repo, but committing/pushing and reviewing several [?] items requires human decision

Completed :
  - #1.1–1.6 [dynamic-skill-init rollout: skill, catalog/manifest entries, init-project.sh + validate.sh fixes] → already present in working tree (done earlier today, before this TASK_BRAIN.md existed)
  - TASK_BRAIN.md + TASK_BRAIN.html initialized for this repo → ~/9arm-skills/TASK_BRAIN.md, ~/9arm-skills/TASK_BRAIN.html

Next      :
  - #1.7 commit + push today's changes — รอ human
  - #2.1, #5.1–5.4 review whether still relevant/open — รอ human (many reference paths/tools that may have moved since 2026-05-28)
  - #4.1–4.4 confirm actual current path/state of Hermes MCP work (~/.hermes/ vs ~/hermes/) — รอ human

Gaps      :
  - MASTER_IMPLEMENTATION.md is dated 2026-05-28 and consistently refers to ~/hermes/ (no dot), while the live system uses ~/.hermes/ — every Phase 4 task path needs re-verification against current reality, not assumed from the old doc
  - Did not verify whether skills/engineering/ui-ux-pro-max/ (new untracked directory) is part of today's dynamic-skill-init work or a separate unrelated addition — it appears in tier-manifest.yaml tier_1_engineering already but git status shows it untracked, so it predates today's commit boundary or was added alongside it; flagged for human awareness, not marked done/not-done since scope was specifically dynamic-skill-init + the two script fixes + validate.sh fix

Files     :
  - TASK_BRAIN.md [added]
  - TASK_BRAIN.html [added]
  - CLAUDE.md [modified — skill selection reviewed/refined, see repo CLAUDE.md itself for diff]
```

---

## 📝 SUMMARY SO FAR
<!-- เขียนทับได้ทุก session — ดู LOG สำหรับ history -->

**ทำไปแล้ว** :
- 2026-06-22: Added `dynamic-skill-init` skill (skills/productivity/dynamic-skill-init/SKILL.md) — tailors a project's CLAUDE.md skill list by reading the project's own IMPLEMENTATION.md/PRD.md/CONTEXT.md/TASK_BRAIN.md rather than picking from a fixed profile (engineering/ai-agent/hermes/planning/full)
- 2026-06-22: Registered the new skill in both catalog.json (productivity, tier 3) and tier-manifest.yaml (tier_3_optional)
- 2026-06-22: Fixed two bugs in scripts/init-project.sh: (1) `$PROJECT_NAME` resolved to literal `.` when the script was invoked with `.` as the path argument — fixed by resolving the absolute path first via `cd "$PROJECT_PATH" && pwd`; (2) the generated CLAUDE.md's "Repo Context" section had stale template lines pointing at incorrect LifeVault/NotebooksLM path conventions — corrected to match the actual one-file-per-project LifeVault convention and TASK_BRAIN.md-based session handoff instead of a NotebooksLM folder
- 2026-06-22: Fixed scripts/validate.sh's hardcoded AWOMS path check — was pointing at `~/Documents/Andaman/AWOMS/awoms-app/CLAUDE.md` (verified: does NOT exist on this machine), now correctly points at `~/projects/awoms-app/awoms-app/CLAUDE.md` (verified: exists, 2854 bytes, dated May 28)

**Decisions (และทำไม)** :
- Kept catalog.json/tier-manifest.yaml entries for dynamic-skill-init at tier 3 (on-demand) rather than tier 0/1, since it's a meta-tool for project setup, not something every session needs loaded
- Did NOT commit or push any of today's changes — per explicit instruction, this is a human decision (review diff, confirm correctness, decide commit message/timing)

**ยังค้างอยู่** :
- All of today's repo changes are uncommitted (see git status below) — nothing has been pushed to github.com/LeGoLus/9arm-skills
- skills/engineering/ui-ux-pro-max/ is untracked in git but already referenced in tier-manifest.yaml tier_1_engineering — relationship to today's work is unclear, flagged for human review
- Older TODOs from MASTER_IMPLEMENTATION.md (LifeVault folder fix, SkillManager app, Hermes MCP tool wiring, NotebooksLM scaffold) — genuinely unclear which of these are still relevant a month later (2026-05-28 → 2026-06-22); the doc's repo paths (`~/hermes/` vs actual `~/.hermes/`) are already stale in at least one place, so all Phase 4/5 items here are marked `[?]` pending human review rather than assumed still-open or already-done

**Context สำคัญ** :
- This repo (~/9arm-skills/) is the skill SOURCE — changes here propagate to every other project via `scripts/link-skills.sh` (symlinks into ~/.claude/skills/). Treat edits with the same care as a shared library: breaking a SKILL.md here affects hermes, andaman/awoms, and all other consuming projects simultaneously
- git status as of this session: `M catalog.json`, `M scripts/init-project.sh`, `M scripts/validate.sh`, `M tier-manifest.yaml`, `?? skills/engineering/ui-ux-pro-max/`, `?? skills/productivity/dynamic-skill-init/` — 10 most recent commits show prior work (find skill, teach skill, GitHub-first architecture, SYSTEM-TH.md, catalog.json+validate.sh, GUIDE docs) but none of today's changes are committed yet

---

## ✅ QUALITY GATE
<!-- cowork/code เขียนตอนเริ่ม — ห้ามแก้ระหว่างทำงาน -->
<!-- ใช้ตรวจทุกครั้งที่รับงานกลับมา -->

- [x] ไฟล์ output อยู่ใน path ที่กำหนด (TASK_BRAIN.md, TASK_BRAIN.html in ~/9arm-skills/ root)
- [x] Format ตรงกับ PROJECT OVERVIEW
- [x] ไม่มี placeholder เช่น `[TODO]`, `...` (all sections filled)
- [x] ข้อมูลครบ ไม่มี section ว่าง
- [ ] No outstanding `[?]` items left unreviewed by a human (currently 7 items across Phases 2, 4, 5 await review)
- [ ] Today's git changes committed/pushed (explicitly deferred to human — task 1.7)

---

## 📋 SESSION LOG
<!-- Append เท่านั้น — ห้ามลบ -->
<!-- ทุก agent เขียนที่นี่เมื่อเสร็จ task หรือเจอปัญหา -->

```
[2026-06-22 13:43] [code] Task #1.1-1.6 — DONE (pre-existing, captured retroactively)
  Input  : git -C ~/9arm-skills log/status/diff, catalog.json, tier-manifest.yaml
  Output : skills/productivity/dynamic-skill-init/SKILL.md, catalog.json, tier-manifest.yaml, scripts/init-project.sh, scripts/validate.sh
  Notes  : These changes existed in the working tree before this TASK_BRAIN.md was created today; verified via git diff that all 4 described fixes/additions are present and correct. Did not re-do the work, only documented it.
```

```
[2026-06-22 13:43] [code] Task — TASK_BRAIN.md + TASK_BRAIN.html initialization — DONE
  Input  : ~/.claude/skills/task-brain/assets/TASK_BRAIN_TEMPLATE.md, TASK_BRAIN_TEMPLATE.html, ~/.hermes/MASTER_IMPLEMENTATION.md TODO sections
  Output : ~/9arm-skills/TASK_BRAIN.md, ~/9arm-skills/TASK_BRAIN.html
  Notes  : Captured today's dynamic-skill-init rollout as done; surfaced 3 MASTER_IMPLEMENTATION.md TODO sections (LifeVault, SkillManager, Hermes MCP) plus the end-of-doc Implementation Checklist as open/uncertain items. Did not commit/push repo changes per explicit instruction — added as human-owned task #1.7.
```

```
[2026-06-22 13:43] [code] Repo CLAUDE.md review — DONE
  Input  : existing ~/9arm-skills/CLAUDE.md
  Output : ~/9arm-skills/CLAUDE.md (refined in place)
  Notes  : See CONSTRAINTS section below + the file itself for what changed and why.
```

---

## 🗂️ FILE REGISTRY
<!-- อัพเดทเมื่อมีไฟล์ใหม่ -->

| File | By | Status | Description |
|------|----|--------|-------------|
| TASK_BRAIN.md | code | added | This file — shared state for the 9arm-skills repo itself |
| TASK_BRAIN.html | code | added | Human-facing companion view of TASK_BRAIN.md |
| skills/productivity/dynamic-skill-init/SKILL.md | code | added (earlier today, pre-existing) | Reads a project's own plan doc to pick skills instead of a fixed profile |
| catalog.json | code | modified (earlier today, pre-existing) | Added dynamic-skill-init entry |
| tier-manifest.yaml | code | modified (earlier today, pre-existing) | Added dynamic-skill-init to tier_3_optional |
| scripts/init-project.sh | code | modified (earlier today, pre-existing) | Fixed PROJECT_NAME literal-dot bug + stale LifeVault/NotebooksLM template lines |
| scripts/validate.sh | code | modified (earlier today, pre-existing) | Fixed stale hardcoded AWOMS path |
| CLAUDE.md (this repo's) | code | modified | Refined skill selection reasoning, added dynamic-skill-init source comment |
| skills/engineering/ui-ux-pro-max/ | unknown | untracked (pre-existing, unattributed) | Present in tier-manifest.yaml already; relationship to today's session unclear — flagged for human review, not modified by this session |

---

## ⚙️ AGENT CONFIG
<!-- เขียนครั้งเดียวตอนเริ่ม -->

```yaml
cowork:
  model : claude-sonnet-4 / claude-opus-4
  owns  : complex reasoning, connectors, quality review, scheduled tasks
  scope : not used for this repo's maintenance — file-system/script work only

code:
  model : claude-sonnet-4 / claude-opus-4 (CLI)
  owns  : bash, file ops, SKILL.md authoring, catalog/manifest edits, script fixes
  scope : all maintenance of this repo — skill content, scripts, manifests

handoff_trigger:
  cowork→code : not applicable to this repo
  code→human  : any git commit/push decision, any [?] item requiring judgment about whether old plan items are still relevant
```

---

## 📚 CONSTRAINTS & REFERENCE
<!-- ข้อมูลที่ทั้งสอง agent ต้องรู้ตลอด project -->

**Style / Format** :
- Conventional commits for all changes (feat/fix/chore/docs/refactor/test scope: description)
- Every skill in engineering/, productivity/, ai-agent/, meta/ needs a README.md reference + catalog.json entry; personal/, in-progress/, deprecated/ must NOT appear in either
- Update tier-manifest.yaml whenever adding a new skill
- Run scripts/validate.sh after any change

**ข้อมูลสำคัญ** :
- This repo is the canonical source; ~/.claude/skills/ is a symlinked mirror via scripts/link-skills.sh — never edit the symlinked copy directly
- MASTER_IMPLEMENTATION.md (the original planning doc this repo was built from) lives OUTSIDE this repo, at ~/.hermes/MASTER_IMPLEMENTATION.md — it is dated 2026-05-28 and already contains at least one stale path (`~/hermes/` vs actual `~/.hermes/`); treat its TODO items as candidates for review, not as ground truth

**Tools ที่ใช้** :
- bash scripts under scripts/ (init-project.sh, link-skills.sh, validate.sh, token-audit.sh, list-skills.sh)
- catalog.json (SkillManager-app-compatible format)
- tier-manifest.yaml (token-budget tiering)

**ข้อจำกัด** :
- Per explicit instruction: do NOT git commit or git push in this repo without the user doing so themselves — always leave that as a human-owned task
- Do not modify skill files beyond what's explicitly described in a given task

---
*task-brain skill v1.0*
