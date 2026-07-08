---
name: ai-software-team
description: >
  Run software development as a virtual AI team: the human is Product Owner +
  Chief Architect; an AI orchestrator decomposes a one-line Mission into
  Program → Milestone → Epic → Feature → Task, tracks it on a Kanban, and
  drives implementer/QA/reviewer agents through quality gates to closeout.
  Use when: starting a new product or program ("Start X Program"), setting up
  multi-agent development, delegating a whole project not a task, structuring
  work for AI execution, or designing platform-vs-product architecture.
  Trigger on: mission, program, AI team, orchestrate, "manage the whole
  project", epic, milestone, product owner, "act as my dev team", closeout.
---

# AI Software Team

> The human decides WHAT and WHY. The AI team owns HOW and WHEN.
> You are not asking for code — you are issuing a Mission.

Companion skills: **model-harness** (the laws that keep this safe),
**subagent-driven-development** (the per-task execution engine),
**grill-me / write-a-prd / writing-plans** (the planning chain).

## Team Structure

| Role | Who | Responsibility |
|---|---|---|
| Product Owner / Chief Architect | **Human** | Vision, business decisions, architecture-change approval. Nothing else. |
| Orchestrator | **Strongest available model** | Decompose Mission → Program → Milestone → Epic → Feature → Task; maintain Kanban; dispatch and track every agent to closeout |
| Developer | Implementer agent | Features, code, refactors — via strict TDD |
| Builder | Cheap-model agent | Docs, README, dashboards, reports, mechanical tasks |
| QA | Reviewer agent | Smoke + regression; verifies acceptance criteria by RUNNING things, never by trusting reports |
| Code Reviewer | Reviewer agent (strong model) | Quality, reuse, technical-debt control |
| Safety Reviewer | Reviewer agent | Security, transparency, honest claims — the system must not overstate itself |
| PM / UX Researcher / Analyst | On-demand agent hats | Business value, user experience, evidence quality |

**⚠️ The one rule that makes or breaks this:** orchestration is the
highest-judgment job, so it goes to the **strongest** model — never to the
cheap conversational layer. The cheap model is the *interface* (receives the
Mission as a deterministic command, relays status, keeps the board); the
strong model is the *brain and hands*. Assigning orchestration to a weak
model violates model-harness Law 2 and fails ~25–50% of the time in
measured practice.

## The Mission Workflow

1. **Mission** (human, one line): `Start <Name> Program` — optionally with a
   short vision paragraph. Entry must be a deterministic command/keyword,
   not model intent-detection.
2. **Interview** (orchestrator → human): grill-me style — concrete outcomes,
   explicit non-goals, consumer benefit per feature. Short; the human is
   busy being the boss.
3. **Breakdown**: Program → Milestones → Epics → Features → Tasks, written to
   the Kanban AND a plan file (PRD with acceptance criteria + blocked-by
   graph). Every task sized for one agent session with testable "done".
4. **Execution loop** (per task, from subagent-driven-development):
   fresh implementer (full task text + context) → **spec-compliance review**
   (verify by reading code and re-running tests — never trust the report) →
   **code-quality review** → fix-and-re-review until approved → mark done.
5. **Program gates**: QA pass per Feature; Safety review before anything
   user-facing ships; final cross-cutting review of the seams before
   closeout (run the real end-to-end path; check deployment reality —
   PATH/env/config, not just tests).
6. **Closeout**: update the PRD with DONE notes + recorded deviations,
   deliver a human-readable summary, list what was deferred and why.

## Working Principles

- **Small, atomic changes.** One commit per task; if using PRs, one Feature
  per PR max. Big diffs hide bugs from reviewers — human or AI.
- **Every change passes QA + review.** No exceptions, including "trivial"
  ones — measured experience: reviews caught critical bugs in code that
  passed all its tests (silent-failure holes, deadlocks, config shadowing).
- **Consumer-first.** Every Feature must answer: *what does the user get?*
  If the answer is vague, the Feature goes back to the Epic for rework.
- **Evidence-first.** Measure before adding: instrument the current behavior
  (usage counts, correction counts, error rates — logged by CODE, per
  model-harness Law 5) and let a trend justify the next Feature.
- **Report honestly.** Failed tests are reported with output; skipped steps
  are named; "done" means verified. Agents that can't finish say BLOCKED —
  bad work is worse than no work.

## Platform vs Product

When the program spans reusable logic and user-facing apps, split hard:

- **Platform** (e.g. a simulation/analytics engine): owns reusable logic,
  exposes an SDK/API, has its own tests and versioning. Knows nothing about
  any single product's UX.
- **Product** (e.g. a marketing workbench): owns UX/UI, workflows,
  dashboards, reports. Consumes the platform ONLY through the SDK/API.
- **Never copy code across the boundary.** If a product needs logic the
  platform lacks, that's a platform Feature request — put it on the
  platform's board, not in the product's codebase.

One Kanban per repo; the Orchestrator owns cross-board dependencies
("Product Feature X blocked by Platform Task Y").

## What the Human Actually Does

- Issues Missions and answers interview questions (minutes, not hours)
- Approves architecture changes and anything irreversible/outward-facing
- Reads the trend reports (corrections down? usage up?) and decides direction
- Reviews the closeout summary — then issues the next Mission

Everything else — planning, decomposition, coding, testing, reviewing,
bookkeeping — is the team's job. That's the whole point.
