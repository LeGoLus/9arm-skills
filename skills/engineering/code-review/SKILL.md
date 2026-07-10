---
name: code-review
description: >
  Structured self-review skill for code quality. Performs systematic review checking
  security, performance, accessibility, naming, dead code, and test coverage before
  committing. Use after completing an implementation task and before creating a commit
  or PR. Trigger on: "review this", "check my code", "before I commit", code review,
  "is this ready", quality check, "look over this", "anything I missed", "sanity check",
  pre-commit review. Use this as the final gate before any code leaves the working branch.
---

# Code Review

Review the changes before they leave the branch, along **two independent axes**:

- **Standards** — does the code follow this repo's conventions and hold up as quality code (security, performance, accessibility, naming, dead code, tests, smells)?
- **Spec** — does the code faithfully implement what the originating task asked for?

<!-- adapted from mattpocock/skills (MIT) -->
Run the two axes as **parallel sub-agents with isolated contexts** so they don't pollute each other, then aggregate their findings **side by side without reranking across axes**. A change can pass one axis and fail the other, and reporting them separately stops one from masking the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the task asked but breaks conventions → **Spec pass, Standards fail.**

These two axes map 1:1 onto the reviewers in the `subagent-driven-development` workflow: **spec-reviewer = Spec axis, quality-reviewer = Standards axis.** Keep this skill and that workflow consistent.

## Process

### 1. Pin the scope

Determine the diff under review. Default to the working changes; if the user named a fixed point (a commit SHA, `main`, `HEAD~5`, a branch or tag), diff against it with `git diff <fixed-point>...HEAD` (three-dot, against the merge-base) and note the commits via `git log <fixed-point>..HEAD --oneline`. Confirm the ref resolves and the diff is non-empty before spawning sub-agents — a bad ref or empty diff should fail here, not inside a sub-agent.

### 2. Identify the spec source

Find what defined this work, in this order: the task's **plan file (`plans/*.md`)**, **PRD**, **`TASK_BRAIN.md`**, or **Hermes Kanban entry** — whichever defined the work. Failing those, an issue referenced in commit messages, or a spec path the user passed. If nothing is found, ask the user; if they say there's no spec, the Spec sub-agent skips and reports "no spec available".

### 3. Identify the standards sources

Anything in the repo documenting how code should be written (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, `CONTEXT.md`, ADRs). On top of whatever the repo documents, the Standards axis always carries the **rubric below** — it applies even when the repo documents nothing. Two rules bind it: **the repo overrides** (a documented standard wins where it conflicts), and **it's a judgement call** (each item is a heuristic, not a hard violation — skip anything tooling already enforces).

### 4. Spawn both sub-agents in parallel

Send a single message with two `Agent` tool calls (`general-purpose` subagent for both). Each gets the diff command + commit list and a <400-word brief. If the spec is missing, skip the Spec sub-agent and note it in the report.

**Standards sub-agent** — pass the standards-source files from step 3 **plus the full Standards Rubric below pasted in** (it has no other access to it). Brief: "Report, per file/hunk: (a) every place the diff violates a documented standard — cite the rule; (b) any rubric item it trips — name it and quote the hunk. Documented standards can be hard violations; rubric items are always judgement calls, and a documented repo standard overrides the rubric. Skip anything tooling enforces. Rate each finding critical / warning / nit. Under 400 words."

**Spec sub-agent** — pass the spec path or contents. Brief: "Report: (a) requirements missing or partial; (b) behaviour not asked for (scope creep); (c) requirements implemented but implemented wrong. Quote the spec line for each finding. Rate each critical / warning / nit. Under 400 words."

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings. **Do not merge or rerank findings across the axes.** End with a one-line summary: total findings per axis and the worst issue *within each axis* — never a single winner across axes. Then fix all critical and warning findings before proceeding.

## Standards Rubric

The Standards axis carries two things: our quality checklists (below), then the Fowler smell baseline as the structural fallback.

### Quality checklists

**Security**
- No secrets, credentials, or API keys in code
- User inputs validated and sanitized; SQL uses parameterized statements
- Authn/authz checks on all endpoints; no sensitive data (PII, passwords, tokens) in logs
- File uploads validated (type, size, content); CORS not wildcard in production; rate limiting on public endpoints
- Dependencies free of known vulnerabilities

**Performance**
- No N+1 queries; large lists paginated; expensive ops cached or batched
- Queries have appropriate indexes; no memory leaks (listeners/subscriptions cleaned up)
- No unnecessary re-renders (memoize where needed); large assets lazy-loaded; no sync work that should be async

**Accessibility (if UI changes)**
- Semantic HTML (`<button>`/`<nav>`/`<main>`, not `<div>` for everything)
- ARIA labels on interactive elements without visible text; keyboard navigation works
- Color contrast meets WCAG AA (4.5:1); images have meaningful alt text
- Focus managed after dynamic changes; errors announced to screen readers

**Naming & dead code**
- Names clear and consistent with codebase conventions; no magic numbers (named constants)
- No dead code or commented-out blocks; no TODO/FIXME/HACK without a linked issue
- Types explicit (no `any` unless truly necessary); comments explain WHY not WHAT

**Test coverage**
- Happy path, edge cases (empty/boundary), and error paths tested
- Tests independent (no shared mutable state), non-flaky, with specific assertions
- Test names describe the behavior verified

**API design (if adding/changing APIs)**
- Endpoints follow REST conventions or a documented alternative; schemas documented
- Error responses consistent; breaking changes versioned or migrated; timeouts configured

### Fowler smell baseline

<!-- adapted from mattpocock/skills (MIT) -->
The 12 code smells from *Refactoring* (ch.3). Each reads *what it is* → *how to fix*; match against the diff and label the flag ("possible Feature Envy"), never assert a hard violation:

- **Mysterious Name** — a name that doesn't reveal what it does or holds. → rename; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file. → extract the shared shape, call it from both.
- **Feature Envy** — a method reaching into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields/params keep travelling together. → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive standing in for a domain concept. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs. → replace with polymorphism, or one shared map.
- **Shotgun Surgery** — one logical change forces scattered edits across many files. → gather what changes together into one module.
- **Divergent Change** — one module edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality** — abstraction/hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method.
- **Middle Man** — a class/function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass ignoring or overriding most of what it inherits. → drop the inheritance, use composition.

## Output Format

```
## Standards
### Critical / Warning / Nit
- [file:line] finding (cite standard or name the smell)

## Spec
### Critical / Warning / Nit
- [file:line] finding (quote the spec line)

### Summary
- Standards: N findings (worst: …). Spec: M findings (worst: …).
```

Fix all critical and warning findings, then re-run tests before proceeding.
