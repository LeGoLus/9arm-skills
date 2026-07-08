---
name: model-harness
description: >
  Make ANY model — weak or strong, any provider — behave like a frontier agent by
  moving intelligence out of the model and into deterministic architecture and
  process. Distilled from the Hermes infrastructure upgrade (2026-07): the same
  harness that makes MiniMax M3 reliable also hardens Claude, GPT, or local models.
  Use when: building an AI feature or agent, choosing a model, "the model isn't
  smart enough", "output keeps changing", "the AI forgot what I told it", switching
  providers, "make it work like Fable/Opus", designing tool calling, or any system
  where an LLM's mistake reaches the user. Trigger on: harness, model-agnostic,
  weak model, cheap model, reliability, deterministic, "model keeps missing",
  "inconsistent output", provider switch, self-improving, escalation.
---

# Model Harness

> The model's IQ is rented. The harness is yours.
> A weak model in a strong harness beats a strong model in no harness —
> and when you upgrade or switch providers, the harness keeps working.

**Source of truth:** these rules were not theorized — each was extracted from a
measured failure and a shipped fix in the Hermes gateway (MiniMax M3 + Claude
Code delegation, 2026-07). Evidence noted inline.

## The Five Laws

### Law 1 — Code decides, the model writes
Routing, formatting, memory, and side effects belong to deterministic code.
The model's job is language: translate, summarize, draft, converse.
If a decision matters (which handler runs, what file is written, what gets
sent), it must be reachable by `grep`, not by hoping the model chooses well.

*Evidence:* 6 daily cron reports drifted in format every single day while the
model owned layout. Moving layout to code made them byte-stable; the model now
fills only language slots.

### Law 2 — Never gate a critical path on model intent-detection
Measured: a mid-tier model misses *clear* tool-call intents 25–50% of the time.
No prompt fixes this. For every intent that matters, add a **deterministic
pre-filter** — keyword/regex in code, running BEFORE any LLM call:

```python
# runs before the model ever sees the message — zero cost, zero miss
if any(k in text.lower() for k in DELEGATION_KEYWORDS):
    queue_hint_or_route(...)
```

Filters may *offer* (append a hint, show a confirm) or *route* (dispatch to a
handler). They must never need the model's cooperation to fire.

### Law 3 — Code owns the output format
For any recurring output (reports, statuses, notifications):
- Code builds the full layout; the model fills bounded text slots (or nothing).
- Sanitize model output into slots (truncate, strip newlines) — never re-ask.
- Pin the format with a **golden test**: assert the entire rendered string,
  not substrings. Format drift is a test failure, not a vibe.

### Law 4 — Failures are never silent
Every async/background path must end in a user-visible signal — success,
failure, or timeout. Audit every raise-path: an exception that escapes without
a notification is a bug even if it "can't happen."

*Evidence:* the delegation worker originally had 4 raise-paths (broken pipe,
corrupt registry, log OSError, import failure) that left tasks "running"
forever with zero notification. Pattern that fixed it:

```python
try:
    return _body(...)
except Exception as exc:
    try:
        registry.update(task_id, status="failed", summary=f"crashed: {exc!r}")
    except Exception:
        pass          # if the registry IS the failure, the push below still fires
    notify_user(f"❌ task crashed: {exc!r}")
    return 3
```

Corollaries: cosmetic updates (progress phases) get `try/except: pass` so they
can't abort real work; long tasks get a hard watchdog with a DISTINCT timeout
message; status displays check pid-liveness so a dead worker shows "⚠ stale",
not a lie.

### Law 5 — Metrics are external; the model never grades itself
A prompt saying "Logic Accuracy Score: 9.2/10, update your Evolution Ledger"
is theater — the model will hallucinate improvement. The honest loop:
1. Log every user correction as a JSONL event **from code** (command handler +
   deterministic phrase detector — Law 2).
2. A cron job counts events per week and reports the trend. Falling count =
   real improvement. That's the only self-improvement metric that exists.

## The Correction-Memory Loop (portable self-improvement)

Works with any model because the model only *reads* the result:

1. **Capture:** an explicit `/learn <lesson>` command appends a one-line rule to
   `LESSONS.md` (locked, threat-scanned, length-capped ~2k chars/lesson).
   A phrase detector ("wrong", "fix this", "ไม่ใช่แบบนี้") may *offer* to save —
   it must NEVER auto-save; a misread lesson poisons every future session.
2. **Inject:** render `LESSONS.md` into the system prompt of every new session,
   frozen per session (prefix-cache stable), newest-wins under a char cap,
   return empty (skip injection) rather than an empty header.
3. **Measure:** weekly correction count, by code (Law 5).

Provenance rule to inject alongside: *facts about the user's own data must cite
their source file; if not in context, say "not in your files — search?" instead
of guessing.*

## Model Tiering (cheap chat, strong hands)

- Cheap/fast model = conversation, translation, slot-filling.
- Strong model (e.g. Claude Code) = planning, multi-step coding — dispatched by
  a deterministic command/keyword (Law 2), run as a **detached background
  process** that survives the parent's restart, with:
  - instant "🚀 task #N started" acknowledgment,
  - throttled progress pushes (≥60s apart; parse the strong model's event
    stream: tool-use names, todo-list progress → "📋 2/5 done"),
  - a status command reading a crash-safe registry file (atomic write + flock),
  - distinct ✅/❌/⏱ terminal notifications (Law 4).
- Pin the worker's interpreter/binary paths explicitly — never inherit
  "whatever python/PATH the caller had."

## Process Harness (how to BUILD with any model)

The coding model is also just a model — harness it too:

1. **Interview before code** (grill-me): concrete failure examples, not
   categories. "Which message disappointed you, exactly?"
2. **Plan with complete code**: every task carries full test code + full
   implementation + exact anchors + expected command output. The implementer
   transcribes; judgment was spent at plan time.
3. **TDD, strictly**: failing test first, watch it fail, minimal code, green.
4. **Two-stage review per task**: spec-compliance first (did they build exactly
   what was asked — verify by reading code and RE-RUNNING tests, never trust
   the report), then code-quality (is it well-built). Reviewer found → same
   implementer fixes → reviewer re-reviews. No skipping.
5. **Final cross-cutting review**: the seams no per-task review saw — actually
   run the end-to-end round trip; check deployment reality (PATH, env
   inheritance, duplicate config keys).
6. Fresh context per task; the orchestrator curates exactly what each worker
   needs.

*Evidence this works:* across two workstreams the review stages caught — a
silent-crash hole, a pipe deadlock class, an fd leak, a parser raise-path on
the terminal event, an oversized-input eviction bug, a command-name collision,
and a duplicate YAML key silently shadowing live config. Zero of these were in
the (already careful) plans.

## Per-Request Prompt Harness

Safe to use with any model (unlike self-scoring):
- **THINK → PLAN → EXECUTE → VERIFY** phase structure for complex requests.
- Non-negotiable rules block (TDD, verification-before-completion,
  conventional commits) restated in every delegated prompt.
- Frozen context blocks (memory, lessons, project summary) injected by code at
  session start — the model never fetches its own context on critical paths.
- Escape hatches are deterministic too: a prefix or command forces the cheap
  path; nothing relies on the model "deciding not to" do something.

## Anti-Patterns (each one burned us)

| Anti-pattern | Why it fails | Harness replacement |
|---|---|---|
| Self-scoring prompt ("Evolution Ledger 9.2/10") | Hallucinated improvement | External correction count (Law 5) |
| "A better prompt will fix the misses" | 25–50% intent-miss is a model property | Deterministic pre-filter (Law 2) |
| Model invokes a side-effect tool ("send the file") | Model hallucinates fake tool logs; effect never fires | Code-parsed directive in output (e.g. `MEDIA:` line) or command handler |
| Model formats the recurring report | Drifts every run | Code-owned layout + golden test (Law 3) |
| Blocking call with a timeout as the only failure plan | Long tasks die silently | Detached worker + watchdog + terminal notify (Law 4) |
| Auto-saving inferred lessons/memory | One misread poisons all sessions | Offer-only; explicit user confirm |
| Trusting the worker's inherited env | Wrong interpreter/PATH in launchd/cron | Pin absolute paths |

## Checklist for any new AI feature

- [ ] What decision is the model making that code could make? Move it.
- [ ] Every critical intent has a pre-LLM deterministic filter.
- [ ] Recurring output has a code-owned layout and a golden full-string test.
- [ ] Every async path ends in ✅/❌/⏱ the user can see; raise-paths audited.
- [ ] Corrections are captured (explicit command), injected (every session),
      and counted (by code, weekly).
- [ ] Facts must cite sources or admit absence.
- [ ] Cheap model for talk, strong model for work, deterministic escalation.
- [ ] Building it: plan-with-code → TDD → two-stage review → final seam review.

If you keep the checklist green, the model becomes a swappable part —
upgrade it, downgrade it, change provider: the product stays good.
