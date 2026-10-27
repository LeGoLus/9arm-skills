---
name: model-ladder
description: >
  Spend Claude quota only where it is needed. One tier file (~/.agents/tiers.json) names the models:
  free (MiniMax) → claude-small (Haiku) → claude-mid (Sonnet) → claude-top (Opus). `climb` proves the cheapest
  tier that does a skill's task as well as Opus (3/3 runs, Opus judges); `run` then does the skill's work on that
  tier, climbs one tier on failure with a diagnosis, spot-checks 1 in 10, and takes the user's feedback.
  Use when: "model ไหนพอ", "ต้องใช้ Opus ไหม", optimize cost, cheaper model, switch MiniMax to another model,
  "ให้ MiniMax/Antigravity ทำ", a delegated run failed, "ข้อมูลไม่ดี" about a delegated result.
---

# Model Ladder

> Use the cheapest brain that gets the same result. MiniMax (flat 300 ฿/month) costs
> nothing extra; Haiku is cheap Claude; Opus only when nothing below it matches.

## One control file: `~/.agents/tiers.json`

The only place a model is named (template: `scripts/tiers.example.json`). Skills and folders name a **tier**.

| Tier | Runner | Today |
|---|---|---|
| `free` | `claude -p` pointed at an Anthropic-compatible API | MiniMax-M3 (key path `~/.hermes/.env`) |
| `claude-small` | `claude -p --model` | Haiku 5.5 |
| `claude-mid` | `claude -p --model` | Sonnet 5.5 |
| `claude-top` | `claude -p --model` — also the judge | Opus 5.5 |

`spare` holds alternatives (Antigravity IDE and desktop, Kimi, …; Antigravity left the order on 2026-10-27 because a
run's task never reached the IDE agent unattended); `skills` holds each proven skill's route
(`{"tier": "free", "max_tier": "claude-top", "skip": ["google"], "proven": {...}}`; `skip` = tiers its climb
failed, left out of its chain).
Change of provider = edit the tier there, run `doctor`, re-climb the skills that use it. Nothing else changes.

`doctor` asks a proxied endpoint which model actually answers: MiniMax silently serves `MiniMax-M3.1-Flash` for
an unknown model name, so a typo would otherwise go unnoticed.

## Hard rules

- **Real side effects need a yes in chat first.** A case with `side_effects` refuses to climb without
  `--confirm`; tell the user what happens and how often (golden 1 + up to 3 tiers × 3 runs).
- **Typing into Antigravity IDE takes the keyboard** (~10 s per run): only with `--drive-screen`, which needs the
  user's handover for this session. Without it the prompt is copied and the user pastes it. Target windows ONLY by
  the run's unique title (`ladder-<time>-<pid>-<n> (Workspace)`); screenctl's `Electron#N` handles are positions
  that shift when a window opens — on 2026-10-27 one pointed a prompt at the user's own window.
- **Never bypass a CLI's permission checks.** Each agent gets only the tools the case or call lists.
  Antigravity IDE asks in its own window; the user answers there. Never click an app's trust or permission
  dialog for the user.
- **Private values stay out of the repo**: cases in `~/Documents/model-ladder/cases/`, values in
  `~/Documents/model-ladder/private/` (chmod 600). Values in a prompt go to that tier's provider: test or own data only.
- Keys go to the child process only; saved logs are redacted. Never print them.
- Runs are sequential (a logged-in browser profile opens in one browser at a time).

## Prove a skill's tier (`climb`)

1. **Case** (`references/case-format.md`): prompt, tools, `checks` (cheap shell checks; one failure ends the tier
   without spending the judge), `rubric` (what "same result" means).
2. `python3 scripts/ladder.py doctor`
3. Debug the case cheaply: `climb CASE --runs 1 --tiers free`.
4. `climb CASE [--confirm]` → Opus reference once, then each tier ×3 until one passes. Results:
   `~/Documents/model-ladder/runs/<case>/<stamp>/summary.json` + a row in `~/Documents/model-ladder/ledger.md`.
5. Report winner, clean runs, seconds, the judge's reasons (`report <case>`), from the files.
6. Propose (don't apply) the route in `tiers.json` `skills` and the routing block below for the skill. Apply on yes.

## Use the tier (`run`) — the block a proven skill gets

```markdown
## Model routing (model-ladder: tier from ~/.agents/tiers.json "skills.<name>")
Do the heavy part on the routed tier, not in this session:
  python3 ~/9arm-skills/skills/personal/model-ladder/scripts/ladder.py run --skill <name> \
    --cwd <workdir> --prompt-file <task.txt> --tools "<tools>" --check "<check with {out}>" \
    --goal "<one line>" --rubric "<what good looks like>" [--browser <profile>] [--unattended]
Then check its reply and files yourself before reporting.
```

`run` starts at the skill's tier and climbs to `max_tier`; `--unattended` skips hand-off tiers (no one at the
screen); `--tier X` forces a start. Each call is logged in `~/.agents/logs/runs.jsonl` and, if the folder uses
shared-workspace, in its `.agents/LOG.md`.

Runs stop at claude's `result` event (stream-json) even if the agent left a background task running, and save
`stream.jsonl` + `served_models.json` (the model the endpoint really answered with). A proxied tier maps
`ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` to its own model, so subagents it spawns stay on that model.

## When it goes wrong — diagnose, don't just relay

- A failed tier prints a report: exit, failed checks, the agent's last words, stderr tail, run folder.
  **Read those files and find the cause** (wrong tool missing? site changed? model gave up? timeout?) before the
  next try. Tell the user the cause and the fix, then record it:
  `ladder.py feedback <skill> bad "cause: ..."`.
- **Spot checks:** every `spot_check_every`-th success (10) is judged by Opus against the rubric; a fail is
  logged as bad feedback automatically.
- **User feedback:** "ข้อมูลไม่ดี" → `feedback <skill> bad "<why>"`; good results can be marked `good`.
  Two bad marks in the last ten → `status` says to raise the skill's tier and re-climb. Propose it; the user decides.
- `status [skill]` shows tiers, routes, the last runs and any advice.

## Files

| Path | What |
|---|---|
| `scripts/ladder.py` | `doctor`, `climb`, `run`, `feedback`, `status`, `report` (stdlib only) |
| `scripts/tiers.example.json` | template of `~/.agents/tiers.json` |
| `scripts/test_ladder.py` | `uv run --with pytest pytest -q test_ladder.py` |
| `references/case-format.md` | case fields, checks, computer-use and hand-off modes |
| `examples/smoke.case.json` | harmless case to prove a tier runs |

Related: `shared-workspace` (AGENTS.md + `.agents/LOG.md` + `.agents/HANDOFF.md`, so any tier can continue work).
