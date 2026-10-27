---
name: shared-workspace
description: >
  Make a folder work the same for every agent and model: Claude Code, MiniMax (via claude -p), Antigravity
  desktop / IDE, Gemini. One AGENTS.md holds the folder's rules; .agents/LOG.md records who did what with which
  model; .agents/HANDOFF.md says where the work stands, so the next agent continues instead of starting over.
  Use when: starting work in a folder, "ให้ agent อื่นทำต่อได้", switching model or tool mid-task, handing a task
  to Antigravity or MiniMax, "agent อื่นไม่รู้เรื่อง", setting up a new project folder.
---

# Shared Workspace

> Rules live in the folder, not in one agent's memory. Any agent that opens the folder reads the same three
> files and can carry on.

## Who reads what

| Agent | Reads on its own | So |
|---|---|---|
| Claude Code (any model, incl. MiniMax via `claude -p`) | `CLAUDE.md` | `CLAUDE.md` holds one line: `@AGENTS.md` (plus Claude-only notes) |
| Antigravity desktop, Antigravity IDE | `AGENTS.md`, `GEMINI.md` | nothing extra; don't make a GEMINI.md copy |
| Gemini CLI, Codex, others | `AGENTS.md` (`GEMINI.md` for Gemini) | same |

**AGENTS.md is the single source.** Never put the same rule in two files; they drift.

## The files

| File | Job | Who writes |
|---|---|---|
| `AGENTS.md` | what this folder is, its layout, how to run things, what never to do | updated when a rule is learned |
| `CLAUDE.md` | `@AGENTS.md` + Claude-only notes | rarely |
| `.agents/LOG.md` | append-only diary: one entry per work session | every agent, at the end |
| `.agents/HANDOFF.md` | current state: status, next step, open questions, traps | every agent, rewritten at the end |

LOG entry format (also written by `model-ladder run`):

```markdown
## 2026-10-27 11:07 — <agent> (<tier>: <model>)
- did: what was done (files touched)
- result: ok / failed + why, numbers that matter
- next: the next concrete step, or -
```

## Workflow

**Start (every agent, every session):** read `AGENTS.md`, then `.agents/HANDOFF.md`, then the last 3–5 entries of
`.agents/LOG.md`. Don't redo what the log says is done; don't ask what the handoff already answers.

**End:** append one LOG entry; rewrite HANDOFF.md to the true state (what is left, the next command to run,
anything that bit you). Learned a lasting rule ("this script must run from pipeline/")? Put it in AGENTS.md.

**New folder:** `bash scripts/init.sh <folder>` creates whatever is missing from templates and never overwrites.
If the folder already has a CLAUDE.md with real rules, init leaves it alone and says so: move the shared rules
into AGENTS.md (show the user the split first), keep Claude-only notes, add `@AGENTS.md` at the top.

## Rules

- No secrets, passwords or client data in any of these files: they get read by every agent and its provider.
  Point to where a secret lives (`key in ~/.hermes/.env`), never the value.
- Write facts the next agent can act on: paths, commands, numbers, dates (absolute). No "as discussed".
- Models are named only in `~/.agents/tiers.json`; folder files say a tier ("run with tier free"), not a model.
- A handoff that is wrong is worse than none: if you could not finish, say exactly where it stopped.

## Files

| Path | What |
|---|---|
| `scripts/init.sh` | create AGENTS.md / CLAUDE.md / .agents/{LOG,HANDOFF}.md if missing |
| `templates/` | the starting text of each file |
