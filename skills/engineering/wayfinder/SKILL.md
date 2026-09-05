---
name: wayfinder
description: Plan a huge chunk of work — more than one agent session can hold — as a shared map of investigation tickets, and resolve them one at a time until the way to the destination is clear.
disable-model-invocation: true
---

> Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT). Local adaptations noted inline. Imported 2026-07-10; refreshed 2026-09-05 to match upstream's split of the Grilling ticket type into separate `grilling` + `domain-modeling` skills (both now vendored here too).
> Tracker adaptation: no GitHub-issues or Linear. The map lives in `WAYFINDER.md` at the repo root (or the project's `TASK_BRAIN.md` if present); tickets are markdown checklist entries with explicit "blocked by" notes. For very large programs, escalate to the `ai-software-team` mission workflow.

A loose idea has arrived — too big for one agent session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** in the repo, then works its tickets one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting — it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic — engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear — nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. An effort can override this in its **Notes** — carrying execution into the map itself — but absent that, produce decisions, not deliverables.

## Refer by name

Every map and ticket has a **name** — its title. In everything the human reads — narration, the map's Decisions-so-far — refer to it by that name, never by a bare id, number, or slug. Names read at a glance.

## The Map

The map is a single file: `WAYFINDER.md` at the repo root, or the project's `TASK_BRAIN.md` if that file already serves as the task brain. Its tickets are markdown checklist entries (`- [ ]`) under the appropriate section.

The map is an **index**, not a store. It lists the decisions made and points at the tickets that hold their detail; a decision lives in exactly one place — its ticket section — so the map never restates it, only gists it with a link to the heading.

**Blocking** is expressed as an explicit "blocked by: <ticket title>" note on the ticket, since there is no native dependency graph. A ticket is **unblocked** when every ticket listed in its "blocked by" note is checked off; the **frontier** is the set of open, unblocked, unclaimed tickets.

### The map body

```markdown
## Destination

<what reaching the end of this map looks like — the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- one line per closed ticket: enough to judge relevance -->

- [x] <closed ticket title> — <one-line gist of the answer>

## Not yet specified

<!-- fog of war: in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- work ruled beyond the destination; closed, never graduates -->

## Open tickets

- [ ] **<Ticket title>** <!-- blocked by: none -->
  ## Question
  <the decision or investigation this ticket resolves>

- [ ] **<Ticket title>** <!-- blocked by: <other ticket title> -->
  ## Question
  <the decision or investigation this ticket resolves>
```

### Tickets

Each ticket is a checklist entry in the map file. Its body is the question, sized to one 100K token agent session.

A session **claims** a ticket by adding `(claimed)` to its line before any work, so concurrent sessions skip it. An open, unclaimed ticket is takeable.

Blocking is declared as a comment or note on the ticket: `<!-- blocked by: <title> -->`. A ticket is unblocked when every ticket it names is checked off.

The answer isn't part of the body — it's recorded on resolution (see [Work through the map](#work-through-the-map)).

## Ticket Types

Every ticket is either **HITL** — human in the loop, worked *with* a human who speaks for themselves — or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research** (AFK): Reading documentation, third-party APIs, or local resources like knowledge bases. Creates a markdown summary as a linked asset. Use when knowledge outside the current working directory is required. Run via `/research` or delegate as a background task with `/claude <question>`.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to — an outline, a rough take, a stub, or UI/logic code via the `/prototype` skill. Links the prototype as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Grilling** (HITL): Conversation. The default case. Always call the Skill tool twice, for `grilling` (the interview itself, one question at a time) and `domain-modeling` (sharpening the project's CONTEXT.md/ADRs as terms and decisions crystallise) — the two are separate skills so a ticket that's purely conversational doesn't have to also trigger a domain-doc pass, and vice versa.
- **Task** (HITL or AFK): Manual work that must happen before a *decision* can be made — nothing to decide, prototype, or research, but the discussion is blocked until it's done. Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen. This is the one type that *does* rather than decides — and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it hands the human a precise checklist (HITL). Resolved when the work is done; the answer records what was done and any resulting facts (credentials location, new URLs, row counts) later tickets depend on.

## Fog of war

The map is _deliberately_ incomplete: don't chart what you can't yet see. Beyond the live tickets lies the **fog of war** — the dim view of decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog ahead of it, graduating whatever's now specifiable into fresh tickets — one at a time, until the way to the destination is clear and no tickets remain.

The map's **Not yet specified** section is where that dim view is written down: the suspected question, the area to revisit later. It's the undiscovered frontier _toward_ the destination — everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as the view allows; it doubles as a signpost for collaborators reading where the effort is headed.

**Fog or ticket?** The test is whether you can state the question precisely now — _not_ whether you can answer it now.

- **Ticket when** the question is already sharp — even if it's blocked and you can't act on it yet.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces: it's coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live ticket, and what's out of scope (the next section).

## Out of scope

Fog only ever gathers _toward_ the destination. The destination fixes the scope, so work beyond it is **out of scope** — it isn't fog, and it doesn't belong in **Not yet specified**. It gets its own **Out of scope** section on the map: work you've consciously ruled out of _this_ effort. Scope, not sharpness, lands it here.

Out-of-scope work never graduates — the frontier stops at the destination — so it returns only if the destination is redrawn, and then as a fresh effort, not a resumption.

Ruling something out of scope is a scoping act, not a step on the route. When a ticket that already exists turns out to sit past the destination — mis-scoped in while charting, or exposed by a resolution — **check it off** (a checked ticket is unambiguously off the frontier) and leave one line in the **Out of scope** section: the gist plus why it's out of scope. It stays out of **Decisions so far**, which records the route actually walked — a scope boundary isn't a step on it.

## Invocation

Two modes. Either way, **never resolve more than one ticket per session.**

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Call the Skill tool twice, for `grilling` and `domain-modeling`, to pin down what this map is finding its way to — the spec, decision, or change. The destination fixes the scope, so it's settled first.
2. **Map the frontier.** Grill again, **breadth-first** this time: fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first steps takeable now. **If this surfaces no fog** — the way to the destination is already clear, the whole journey small enough for one session — you don't need a map. Stop and ask the user how they'd like to proceed.
3. **Create the map** (`WAYFINDER.md` or `TASK_BRAIN.md`): Destination and Notes filled in, Decisions-so-far empty, the fog sketched into **Not yet specified**.
4. **Create the tickets you can specify now** as checklist entries — then wire blocking edges in a **second pass** (entries need titles before they can reference each other). Wiring sorts them into the frontier and the blocked; everything you can't yet specify stays in the fog — the **Not yet specified** section.
5. Stop — charting the map is one session's work; do not also resolve tickets.

### Work through the map

User invokes with the map file path or name. A ticket is **optional** — without one, you pick the next decision, not the user.

1. Load the **map** — the low-res view, not every ticket body.
2. Choose the ticket. If the user named one, use it. Otherwise take the first frontier ticket in order. **Claim it**: mark it `(claimed)` before any work.
3. Resolve it — **zoom as needed**: read any related or closed ticket body on demand; invoke the skills the `## Notes` block names. If in doubt, call the Skill tool twice, for `grilling` and `domain-modeling`.
4. Record the resolution: append the answer below the ticket's Question, **check off** the ticket, and **append a gist line** to the map's Decisions-so-far.
5. Add newly-surfaced tickets (draft then wire blocking edges); graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified** so it lives only as its new ticket. If the answer reveals a ticket — this one or another — sits beyond the destination, **rule it out of scope** rather than resolving it on the route. If the decision invalidates other parts of the map, update or delete those tickets.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the map concurrently.
