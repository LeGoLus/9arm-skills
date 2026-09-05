# 9arm-skills

> LeGoLus skill library for Claude Code — Mac Mini M4 Pro
> 24+ skills across 4 tiers, 4 surfaces

## Layout

Skills live under `skills/`, grouped into buckets:

- `engineering/` — daily code work
- `productivity/` — daily non-code workflow tools
- `ai-agent/` — AI/LLM/agent skills
- `meta/` — writing and documentation skills
- `personal/` — tied to my own setup, not promoted
- `in-progress/` — drafts not yet ready to ship
- `deprecated/` — no longer used

Each skill is its own directory with a `SKILL.md` (YAML frontmatter: `name`, `description`, `tier`, `estimated_tokens`) and any bundled scripts or reference files.

## Structure

```
9arm-skills/
├── upstream/superpowers/          ← git subtree: obra/superpowers
├── upstream/mattpocock-skills/    ← git subtree: mattpocock/skills (reference; wayfinder itself is hand-adapted, not symlinked from here)
├── skills/
│   ├── engineering/               ← tdd, code-review, debugging, security
│   ├── productivity/              ← planning, git, writing, execution
│   ├── ai-agent/                  ← subagents, dispatching, evals
│   ├── meta/                      ← writing-skills
│   └── personal/                  ← andaman-context, document-skill
├── scripts/
│   ├── init-project.sh            ← scaffold CLAUDE.md per project
│   ├── migrate-existing.sh        ← copy from ~/.claude/skills/
│   ├── install-superpowers.sh     ← git subtree + symlinks
│   ├── link-skills.sh             ← symlink to ~/.claude/skills/
│   ├── list-skills.sh             ← list all skills
│   ├── token-audit.sh             ← token cost per skill
│   └── validate.sh                ← post-setup verification
├── tier-manifest.yaml
└── README.md
```

## Install

Symlink every shippable skill into `~/.claude/skills/`:

```bash
bash ./scripts/link-skills.sh
```

New project scaffold:

```bash
bash ~/9arm-skills/scripts/init-project.sh ~/myproject engineering
```

## Tier System

| Tier | When | Token budget |
|------|------|-------------|
| 0 | Always | ~4,923t |
| 1 Engineering | Most projects | +~9,500t |
| 2 AI/Agent | AI features | +~7,000t |
| 3 Optional | On demand | varies |

## Profiles

| Profile | Tokens |
|---------|--------|
| planning | ~4,500t |
| engineering | ~9,500t |
| ai-agent | ~13,000t |
| hermes | ~9,000t |
| full | ~20,000t |

## Update Superpowers

```bash
git -C ~/9arm-skills subtree pull --prefix=upstream/superpowers superpowers main --squash
```

---

## Reference

### Engineering

- **[systematic-debugging](./skills/engineering/systematic-debugging/SKILL.md)** — 4-phase debugging: reproduce → trace → falsify → verify. Always applied before any fix.
- **[debug-mantra](./skills/engineering/debug-mantra/SKILL.md)** — Four-mantra debugging discipline (legacy; superseded by systematic-debugging from superpowers).
- **[post-mortem](./skills/engineering/post-mortem/SKILL.md)** — Write the canonical engineering record of a fixed bug — root cause, mechanism, fix, validation.
- **[scrutinize](./skills/engineering/scrutinize/SKILL.md)** — Outsider-perspective review of a plan, PR, or code change. Questions intent, traces code path, verifies claims.
- **[tdd](./skills/engineering/tdd/SKILL.md)** — RED-GREEN-REFACTOR. Failing test before any code. Delete code written before test.
- **[code-review](./skills/engineering/code-review/SKILL.md)** — Pre-merge checklist: security, performance, naming, dead code, test coverage.
- **[error-handling](./skills/engineering/error-handling/SKILL.md)** — Structured error handling patterns.
- **[security-review](./skills/engineering/security-review/SKILL.md)** — Security-focused code review.
- **[search-first](./skills/engineering/search-first/SKILL.md)** — Search before implementing.
- **[verification-before-completion](./skills/engineering/verification-before-completion/SKILL.md)** — Verify fix works before marking done.
- **[receiving-code-review](./skills/engineering/receiving-code-review/SKILL.md)** — How to receive and act on code review feedback.
- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)** — Multi-session project planning: a shared map of decision tickets, resolved one at a time until the route to a named destination is clear. Plans, doesn't do. Adapted for local markdown tracking (`WAYFINDER.md`/`TASK_BRAIN.md`, no issue tracker).
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)** — Slice a plan/spec into tracer-bullet tickets with blocking edges.
- **[domain-modeling](./skills/engineering/domain-modeling/SKILL.md)** — Build/sharpen a project's domain model: CONTEXT.md, ADRs, glossary. Wayfinder's Grilling sub-skill (paired with `grilling`).

### Productivity

- **[git-workflow](./skills/productivity/git-workflow/SKILL.md)** — Conventional commits, atomic changes, meaningful PR descriptions.
- **[grill-me](./skills/productivity/grill-me/SKILL.md)** — Deep interview for greenfield planning.
- **[grill-with-docs](./skills/productivity/grill-with-docs/SKILL.md)** — Planning session against existing codebase; updates CONTEXT.md + ADRs.
- **[write-a-prd](./skills/productivity/write-a-prd/SKILL.md)** — Product Requirements Document creation.
- **[writing-plans](./skills/productivity/writing-plans/SKILL.md)** — Break work into 2-5 minute tasks with exact file paths.
- **[executing-plans](./skills/productivity/executing-plans/SKILL.md)** — Execute a written plan step by step.
- **[strategic-compact](./skills/productivity/strategic-compact/SKILL.md)** — Long session summarization and context preservation.
- **[verification-loop](./skills/productivity/verification-loop/SKILL.md)** — Build → test → lint → typecheck loop until all pass.
- **[improve-codebase-architecture](./skills/productivity/improve-codebase-architecture/SKILL.md)** — Systematic architecture improvement.
- **[using-git-worktrees](./skills/productivity/using-git-worktrees/SKILL.md)** — Parallel branches via git worktrees.
- **[finishing-a-development-branch](./skills/productivity/finishing-a-development-branch/SKILL.md)** — Checklist for completing a feature branch.
- **[management-talk](./skills/productivity/management-talk/SKILL.md)** — Rewrite engineer-to-engineer content for leadership channels.
- **[grilling](./skills/productivity/grilling/SKILL.md)** — Interview via a design-tree worked in frontier rounds. Wayfinder's Grilling sub-skill (paired with `domain-modeling`); distinct from grill-me/grill-with-docs, which stay this repo's own primary planning skills.

### AI-Agent

- **[subagent-driven-development](./skills/ai-agent/subagent-driven-development/SKILL.md)** — Dispatch fresh subagents per task for spec compliance then code quality.
- **[dispatching-parallel-agents](./skills/ai-agent/dispatching-parallel-agents/SKILL.md)** — Run independent tasks concurrently via parallel agents.
- **[prompt-engineer](./skills/ai-agent/prompt-engineer/SKILL.md)** — Craft and optimize prompts.
- **[agentic-eval](./skills/ai-agent/agentic-eval/SKILL.md)** — Evaluate agentic AI systems.

### Meta

- **[writing-skills](./skills/meta/writing-skills/SKILL.md)** — Meta-skill for creating and maintaining skill documentation.

---

## Sources

| Skills | Source |
|--------|--------|
| 14 migrated | `~/.claude/skills/` via migrate-existing.sh |
| 9 new | [obra/superpowers](https://github.com/obra/superpowers) via install-superpowers.sh |
| grill-with-docs | [mattpocock/skills](https://github.com/mattpocock/skills) via curl |
| wayfinder, to-tickets | [mattpocock/skills](https://github.com/mattpocock/skills), hand-adapted 2026-07-10 (tracker plumbing stripped; local WAYFINDER.md/TASK_BRAIN.md map, uses this repo's own grill-me/grill-with-docs/prototype/research) |
| grilling, domain-modeling | [mattpocock/skills](https://github.com/mattpocock/skills), vendored as-is via `git subtree` (no tracker-specific content, no adaptation needed) — wayfinder refreshed 2026-09-05 to call these instead of grill-me/grill-with-docs for its Grilling ticket type |
