---
name: dynamic-skill-init
description: >
  Picks a tailored skill set for a project's CLAUDE.md by reading its own planning
  document (IMPLEMENTATION.md, PRD.md, CONTEXT.md, or TASK_BRAIN.md) and reasoning about
  which skills from the 9arm-skills catalog actually apply — instead of picking one of
  the 5 fixed profiles (engineering/ai-agent/hermes/planning/full) that init-project.sh
  offers. Use this right after a grill-me session produces IMPLEMENTATION.md, or whenever
  the user says "set up skills for this project", "pick skills based on the plan", "init
  project from implementation.md", or "recheck skills". Also use at the start of any
  session in a project that already has a dynamic-skill-init-generated CLAUDE.md, to check
  whether the source planning doc changed since skills were last picked.
---

# Dynamic Skill Init

Tailors a project's `CLAUDE.md` Active Skills list to what the project actually needs,
by reading its own planning doc instead of guessing from a generic profile name.

## When there's no CLAUDE.md yet — [SELECT]

### 1. Find the source doc

Check the project root in this order, use the **first one found**:

```
IMPLEMENTATION.md → PRD.md → CONTEXT.md → TASK_BRAIN.md
```

If **none** exist: stop here, tell the user no planning doc was found, and fall back to
`bash ~/9arm-skills/scripts/init-project.sh <path> <type>` with one of the 5 fixed profiles instead.
Don't guess a skill list from nothing.

### 2. Refresh the catalog

```bash
git -C ~/9arm-skills pull origin main
```

Always — the user edits skills from other machines and pushes to GitHub, so the local
catalog can be stale. Don't skip this even if it was just pulled recently.

### 3. Re-confirm the doc is still accurate

Skim the source doc against the actual project state (files present, recent commits) before
trusting it. If it looks stale or contradicts what's on disk, say so and ask before proceeding
— don't silently pick skills based on a plan that's already out of date.

### 4. Pick skills by reasoning, not keyword matching

Read `~/9arm-skills/catalog.json` (treat every entry as one flat list — don't special-case
skills that originated from the vendored `upstream/superpowers/` subtree vs native ones,
they're already unified with the same tier/tags structure). Read each skill's `description`
and `tags`. Decide which ones the project's planning doc actually implies are needed —
infer from what's being built, not just literal word overlap. `systematic-debugging`,
`git-workflow`, and `grill-me`/`grill-with-docs` (tier 0) are always included regardless
of match — they're foundational, not topic-specific.

### 5. Write CLAUDE.md

Same format `init-project.sh` produces (see its heredoc for the exact template: header
with type/created/budget, Active Skills list, Planning auto-select, Debug Protocol, Dev
Flow, Repo Context, On-Demand Skills as commented-out lines for everything not selected).
Use `type: dynamic` in the header instead of one of the 5 fixed types. Estimate the budget
the same way `token-audit.sh` does (`chars / 4` per SKILL.md, summed).

**Also record the tracking marker** at the very bottom of CLAUDE.md, so future sessions can
detect drift:

```
<!-- dynamic-skill-init: source=<filename> mtime=<ISO8601 mtime of source doc at selection time> -->
```

## When CLAUDE.md already has this marker — [RECHECK]

Run this at the start of every session in a project with a `dynamic-skill-init:` marker:

1. Read the marker's `source` filename and `mtime`.
2. Stat that file now. If it no longer exists, or its current mtime is newer than the
   recorded one: the plan changed since skills were picked.
3. **Flag it, don't silently fix it**: tell the user `<source file> changed since skills
   were last selected (recorded: <date>) — want me to re-run selection?` and wait for a yes.
4. If yes: repeat steps 2–5 of [SELECT], overwrite CLAUDE.md, update the marker.
5. If no: leave CLAUDE.md untouched, just note the drift exists.

## Rules

- ❌ Never silently rewrite an existing CLAUDE.md's Active Skills list — always flag and ask first
- ❌ Never skip the `git pull` step
- ❌ Never pick skills from keyword grep alone — read descriptions and reason
- ❌ Never invent a skill list when no planning doc exists — fall back to the fixed profiles instead
