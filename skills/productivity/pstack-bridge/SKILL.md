---
name: pstack-bridge
description: >
  How our system works with pstack (Cursor's poteto-mode skill pack, installed as a Claude Code plugin): which of
  our rules win over pstack's, how pstack's subagent roles get their models from ~/.agents/tiers.json, and how its
  multi-agent flow (playbook → subagents → verify) fits model-ladder and shared-workspace.
  Use when: /pstack:poteto-mode, pstack, "ทำแบบ pstack", multi-agent or parallel agents, swarm, arena,
  interrogate, setting up pstack models, a pstack step conflicts with a house rule.
---

# pstack bridge

> pstack = think first, delegate to many agents, prove the result. Our rules decide what is allowed;
> pstack decides how to work.

## What pstack is

`pstack@cursor-plugins` (github.com/cursor/plugins/tree/main/pstack, MIT): 58 skills + 2 agents. Main entry
`/pstack:poteto-mode`: matches the task to one of 23 playbooks (bug fix, feature, refactoring, investigation,
eval, autonomous run, orchestrate…), copies the playbook steps into a todo list, and calls the other skills
when a step needs them (`how`, `why`, `architect`, `arena`, `swarm`, `interrogate`, `tdd`, `unslop`, 24
`principle-*` skills). The plugin's `docs/harness/claude-code.md` maps Cursor names to Claude Code; read it once
per session before following a pstack skill.

- Install (done 2026-10-27): `claude plugin marketplace add cursor/plugins` then
  `claude plugin install pstack@cursor-plugins`. Update by hand: `claude plugin update pstack@cursor-plugins`.
- Commands are prefixed: `/pstack:poteto-mode`, `/pstack:swarm`, `/pstack:interrogate`, `/pstack:how`.
- Not bundled (Cursor-only or other plugin): `deslop`, `control-cli`, `control-ui`, Bugbot, Automations.
  Skip that step with one line, as the harness doc says.

## Our rules win (precedence)

`~/CLAUDE.md`, the project's `CLAUDE.md`/`AGENTS.md` and the safety rules come first. pstack fills the rest.

| pstack says | Here |
|---|---|
| Autonomy "just do it": external actions (chat, tickets) without asking | Ask first for send, post, submit, delete, commit, push. 9arm-skills is public: always ask before commit or push. |
| Never block on the human | Yes for reversible local work (edits, tests, scratch files). Still ask for anything above. |
| Opening a PR at the end of every playbook | Only when the user asked for a PR. Otherwise stop at verified local changes. |
| Worktree cleanup, deleting stale things | Never bulk delete. Show the list, ask, move to Trash. |
| Default models grok + opus xhigh | Roles come from the tier file (below). Grok does not exist here. |

Same spirit, keep both: pstack's `tdd`, `prove-it-works` and `fix-root-causes` match our TDD,
verification-before-completion and systematic-debugging rules.

## Models: one file

pstack reads `~/.claude/rules/pstack-models.md`. Do not edit it by hand: it is generated from the `pstack` section
of `~/.agents/tiers.json`, where each role names a **tier** plus an effort (`"bug-fix": "claude-mid high"`).

```
python3 ~/9arm-skills/skills/productivity/pstack-bridge/scripts/pstack_models.py [--print]
```

Only Claude tiers can be pstack roles: the Agent tool runs opus / sonnet / haiku only. The script refuses
`free`. To put MiniMax on a job, prove it with model-ladder and call
`ladder.py run --skill <name>` from inside the pstack step.

Defaults written 2026-10-27 (budget medium): code roles and swarm workers on Sonnet; judgment, prose and
explainers on Opus high; hardest tasks Opus xhigh; panels (arena, architect, interrogate) Opus + Sonnet so two
model families still disagree usefully.

## Data gathering on MiniMax (fan-out without Claude quota)

A pstack step that only gathers data (fetch pages or APIs, read files, collect numbers) can run on MiniMax with
MiniMax sub-agents instead of Claude subagents. Not proven as good as Haiku yet: kept as an option, use it for
low-risk gathering and check the numbers yourself.

```
python3 ~/9arm-skills/skills/personal/model-ladder/scripts/ladder.py run --skill <name> --tier free \
  --cwd <dir> --prompt-file task.txt --tools "Agent,WebFetch,Read,Write" \
  --check "<check on {out}/result.json>" --goal "<one line>"
```

- The prompt says how many sub-agents to start in one message and what each fetches; results go to `{out}/result.json`.
- Every model name (opus / sonnet / haiku) is mapped to the tier's model, so sub-agents run MiniMax-M3, never the
  silent Flash fallback. `served_models.json` in the run folder shows what actually answered.
- Tested 2026-10-27: lead + 2 sub-agents fetching two GitHub repo stats in parallel, 39.7 s, every answer served
  by MiniMax-M3, numbers matched GitHub.

**Every day, unattended → Hermes, not this.** Scheduled jobs run in Hermes on MiniMax's own API
(`~/.hermes/config.yaml`: `model.provider: minimax`; `delegation` with empty model = children inherit MiniMax,
`max_concurrent_children: 3`, `max_spawn_depth: 1`, `child_timeout_seconds: 600`; jobs in `~/.hermes/cron`).
Deterministic fetching first goes into a plain script (no model), like `hc_runner.py`.

## The flow, with our pieces

1. **Start**: read the folder's `AGENTS.md`, `.agents/HANDOFF.md`, last LOG entries (shared-workspace).
2. **Pick the playbook** (`/pstack:poteto-mode`) and copy its steps into the todo list.
3. **Data shape first**, then design (`architect`) when code crosses a function boundary.
4. **Delegate**: subagents per pstack roles. Bulk, repeatable work a skill already proved on a cheaper tier
   goes through `ladder.py run` (MiniMax first) instead of a Claude subagent.
5. **Parallel**: `swarm` for coverage or slices, `arena` for competing designs, `interrogate` for review by two
   model families. Only fan out when the user asked for this mode or the playbook calls for it: every subagent
   costs Claude quota.
   **Tell the user who is working**, in the chat, every time work leaves this session:
   ```
   | agent | model / tier | task | status |
   |---|---|---|---|
   | poteto-agent #1 | sonnet high | fix load() in portfolio.py | running |
   | ladder run | free (MiniMax-M3) | fetch 2 repo stats | done 39.7 s |
   ```
   Post it before spawning, update it as each one finishes or fails, and end with what is still running.
6. **Prove it**: run the real thing, read the real output. Never relay a subagent's "done".
7. **End**: append `.agents/LOG.md`, rewrite `.agents/HANDOFF.md`, name the principles that changed a decision.

## Files

| Path | What |
|---|---|
| `scripts/pstack_models.py` | tier file `pstack` section → `~/.claude/rules/pstack-models.md` |
| `scripts/test_pstack_models.py` | `uv run --with pytest pytest -q` |

Related: model-ladder (prove the cheapest tier), shared-workspace (rules + log + handoff per folder).
