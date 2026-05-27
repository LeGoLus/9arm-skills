# 9arm-skills — Practical Guide
> Read this once. Refer back when unsure. Last updated: 2026-05-27

---

## 1. Quick Mental Model

```
Every session has 3 moments that need a skill:

  PLAN  →  BUILD  →  SHIP

  PLAN:  grill-with-docs (existing) | grill-me (new)
  BUILD: writing-plans → tdd → verification-before-completion
  SHIP:  code-review → git-workflow
```

You never load all skills. You pick the right tier for the job.

---

## 2. Starting a New Project

```bash
# Step 1 — scaffold the project config
bash ~/9arm-skills/scripts/init-project.sh ~/myproject engineering
# Types: engineering | ai-agent | hermes | planning | full

# Step 2 — open Claude Code (skills auto-load from CLAUDE.md)
cd ~/myproject && claude
```

That's it. Claude Code reads `CLAUDE.md` and loads only the listed skills.

**Choosing the type:**

| Type | Use when |
|------|----------|
| `engineering` | TypeScript, Python, Next.js, general app code |
| `ai-agent` | Building AI features, prompts, LLM integrations, evals |
| `hermes` | Working on Hermes itself, MCP tools, agent orchestration |
| `planning` | Planning a new product/feature before writing any code |
| `full` | Rare — only when you need everything (~20,000t) |

---

## 3. Every Session — Tier 0 (Always Active)

These 4 skills are always loaded via `~/CLAUDE.md`. You never need to ask for them.

### `systematic-debugging` — use for every bug

4 phases, no skipping:
1. **Reproduce** — create a minimal failing case, document env
2. **Trace** — follow symptom → root cause, log state transitions
3. **Falsify** — test one hypothesis at a time, change one variable
4. **Verify** — original bug gone + regression tests pass

❌ Never: random changes, fix symptom only, skip steps, no docs

### `grill-me` / `grill-with-docs` — auto-selected

| Situation | Skill |
|-----------|-------|
| New project, blank slate | `grill-me` — clarifying questions, one at a time |
| Existing code / `CONTEXT.md` exists | `grill-with-docs` — challenge plan against codebase, update docs |

> **Rule:** If `src/` or `CONTEXT.md` exists → `grill-with-docs` runs first.

### `git-workflow` — every commit

```
feat(scope): what changed
fix(scope): what was broken
chore: housekeeping
docs: documentation only
refactor: no behavior change
test: tests only
perf: performance improvement
```

PR description always: **What changed / Why / How to test**

---

## 4. Engineering Work — Tier 1

Load these for feature development:

### `writing-plans` — before coding anything

Break the task into **2-5 minute chunks**. Each chunk must have:
- Exact file path(s) to touch
- One clear outcome
- No ambiguous scope

> Do this before opening any file. A bad plan costs 10 minutes. No plan costs 2 hours.

### `tdd` — RED → GREEN → REFACTOR

```
1. Write a failing test (RED) — STOP, do not write code yet
2. Write minimal code to pass (GREEN)
3. Clean up without breaking (REFACTOR)
```

**Hard rule:** If code was written before a test → delete it and start over.

### `verification-before-completion` — before saying "done"

Checklist before marking any task complete:
- [ ] Reproduce the original issue — confirm it's gone
- [ ] Run the full test suite — no regressions
- [ ] Check edge cases mentioned in the task
- [ ] No new console errors or warnings

### `code-review` — before every PR

Review checklist:
- [ ] Security: no hardcoded secrets, inputs validated
- [ ] Performance: no obvious N+1, no unnecessary re-renders
- [ ] Naming: variables/functions say what they do
- [ ] Dead code: nothing unused
- [ ] Tests: coverage for the change
- [ ] Accessibility (UI): ARIA labels, keyboard nav

---

## 5. AI/Agent Work — Tier 2

Load these when building AI features or running subagents:

### `subagent-driven-development`

Dispatch a fresh subagent per task. Each subagent:
1. Stage 1: verify spec compliance (does it match requirements?)
2. Stage 2: code quality review (is it clean?)

> Never let one agent do everything in one shot. Fresh eyes per task.

### `dispatching-parallel-agents`

When tasks are independent — run them concurrently.

```
✅ Good for parallel: write tests | update docs | add types
❌ Bad for parallel: task B depends on output of task A
```

### `prompt-engineer` — when writing prompts for AI features

- Be explicit about format, length, tone
- Include examples (few-shot) for complex outputs
- Test with edge cases: empty input, long input, adversarial input
- Measure: does output quality improve?

---

## 6. The Full Development Flow

```
1. PLAN
   ├── existing code → /grill-with-docs → CONTEXT.md updated
   └── new project  → /grill-me → requirements confirmed

2. BREAK DOWN
   └── writing-plans → list of 2-5 min tasks, exact file paths

3. BUILD (per task)
   ├── tdd: write failing test → minimal code → refactor
   └── systematic-debugging if anything breaks (4 phases)

4. VERIFY
   └── verification-before-completion → original issue gone + tests pass

5. REVIEW
   └── code-review → security + perf + naming + dead code + tests

6. SHIP
   └── git-workflow → conventional commit → PR with What/Why/How
```

---

## 7. Token Management

**The rule:** load the minimum tier that covers the work.

```
planning only?           → planning type  (~4,500t)
writing app code?        → engineering    (~9,500t)
building AI features?    → ai-agent       (~13,000t)
working on Hermes?       → hermes         (~9,000t)
everything at once?      → full           (~20,000t) ← avoid
```

**On-demand loading** — for any skill NOT in your active CLAUDE.md:
```
"load skill: ~/9arm-skills/skills/engineering/search-first/SKILL.md"
```

**Never load personal skills by default** — `andaman-context`, `document-skill` are explicit-only.

---

## 8. Common Commands

```bash
# New project
bash ~/9arm-skills/scripts/init-project.sh <path> <type>

# Validate the full setup (run after any changes)
bash ~/9arm-skills/scripts/validate.sh

# Token cost of every skill
bash ~/9arm-skills/scripts/token-audit.sh

# List all skills with tier + description
bash ~/9arm-skills/scripts/list-skills.sh

# Link skills to ~/.claude/skills/ (for Claude Code discovery)
bash ~/9arm-skills/scripts/link-skills.sh

# Update superpowers to latest
git -C ~/9arm-skills subtree pull --prefix=upstream/superpowers superpowers main --squash
```

---

## 9. When Something Goes Wrong

| Problem | Fix |
|---------|-----|
| Claude not finding skills | Run `link-skills.sh`, check `CLAUDE.md` paths |
| Token budget too high | Drop to a lower profile type, move skills to on-demand |
| validate.sh failures | Read the ❌ lines, check file paths in `tier-manifest.yaml` |
| Skill content outdated | `git -C ~/9arm-skills pull origin main` |
| Superpowers outdated | `git subtree pull --prefix=upstream/superpowers superpowers main --squash` |
| Wrong CONTEXT.md | Delete it, re-run `grill-with-docs` |

---

## 10. Adding a New Skill

1. Create directory: `~/9arm-skills/skills/<category>/<skill-name>/`
2. Write `SKILL.md` with required frontmatter:
   ```yaml
   ---
   name: skill-name
   description: One line — WHEN to use this skill
   tags: [tag1, tag2]
   tier: 0|1|2|3|personal
   estimated_tokens: <chars/4>
   ---
   ```
3. Run `token-audit.sh` — check it's not 🔴 HEAVY unless justified
4. Add to `tier-manifest.yaml` in the right tier
5. Add reference to `README.md`
6. Run `validate.sh`
7. Commit: `docs(skills): add <skill-name>`

> Use `document-skill` as your guide when writing new skills.

---

## 11. Surface Reference

| Surface | How skills load | Config location |
|---------|----------------|-----------------|
| Claude Mobile | Custom Instructions (Tier 0 summaries) | Settings → Custom Instructions |
| Claude Desktop | Custom Instructions (Tier 0 full) | Settings → Custom Instructions |
| Claude Code | Auto from `CLAUDE.md` | `~/CLAUDE.md` + per-project |
| Hermes (MiniMax) | `claude_code_with_skills` MCP tool | `~/.hermes/mcp_tools/` |

---

*This guide lives at `~/9arm-skills/GUIDE.md`. Edit it when conventions change.*
