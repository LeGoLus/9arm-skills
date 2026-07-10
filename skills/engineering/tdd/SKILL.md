---
name: tdd
description: >
  Test-Driven Development skill for all implementation tasks. Use whenever the user
  wants to implement a feature, fix a bug, write code, or build anything. Forces a
  strict red-green loop that dramatically improves code quality (refactoring is code-review's job). Trigger on:
  implement, build, code, fix, "write the code", "make it work", any coding task,
  bug fix, feature implementation, "let's build this", "start coding". This should
  be the DEFAULT approach for all implementation work.
---

# TDD — Test-Driven Development

Follow a strict **red-green** loop for every implementation task. (Historically "red-green-refactor" — but see the split below: refactoring has moved out of the loop.)

## Philosophy

- Tests are a **design tool**, not just verification
- Write the test you WISH you could write, then make it possible
- Prefer **deep modules**: large functionality behind thin interfaces
- Mock at **architectural boundaries**, not at every function call
- Pure functions are testable by nature — don't extract them just for testing
- If you can't figure out where to test, the module boundaries are wrong

## Seams — agree where tests go, first

<!-- adapted from mattpocock/skills (MIT) -->
A **seam** is the public boundary you test at — the interface where you observe behavior without reaching inside. **Test only at pre-agreed seams:** before writing any test, write the seams under test down and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything; agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of leaking into incidental internals. Ask: "What's the public interface, and which seams should we test?"

## The Loop

### Step 1: Confirm Interface Changes

Before writing ANY code, review:
- What public interfaces need to change?
- What new interfaces need to be created?
- What existing tests might break?
- What's the simplest interface that solves the problem?

### Step 2: RED — Write Failing Tests

```
Write tests FIRST for the expected behavior.
Run them. They MUST fail.
If they pass, the test is wrong or the feature already exists.
```

Guidelines:
- Start with the **happy path** — the most basic expected behavior
- Test names should read like specifications: `it("returns empty array when no items match filter")`
- Each test should verify **one behavior**
- Cover: happy path → edge cases → error cases (in that order)

### Step 3: GREEN — Make Tests Pass

```
Write the MINIMUM code to make tests pass.
Don't optimize. Don't refactor. Don't write "clean" code yet.
Just make the red go green.
```

Rules:
- Resist the urge to implement more than the test requires
- If you think "I should also handle X..." — write a test for X first
- Hardcoding is fine if only one test checks the value
- The goal is **speed to green**, not elegance

### Step 4: Repeat

Move to the next behavior. Continue until ALL acceptance criteria from the PRD task are met.

> **Where did REFACTOR go?** <!-- adapted from mattpocock/skills (MIT) -->
> Structural improvement is **not part of the loop** — it belongs to the review stage (see the `code-review` skill). The implementation cycle stays strictly **red → green**: write the failing test, then only enough code to pass it. Keeping refactoring out of the loop stops "while I'm here" cleanup from bundling into feature work and blurring what a given cycle actually changed. Clean-up still happens — just after, as a reviewed, separate pass, not silently mid-cycle.

## Deep Modules

AI agents navigate codebases by reading files. When a codebase has many tiny, undifferentiated modules, the agent bounces between files constantly. Restructure into:

- **Fewer, deeper modules** with lots of functionality
- **Thin interfaces** on top (easy to understand from outside)
- **Hidden complexity** inside (the module handles the hard parts)

This makes the codebase dramatically easier for both humans AND agents.

## Mocking Strategy

**Mock at boundaries, not everywhere:**
- ✅ Mock external APIs, databases, file systems
- ✅ Mock time-dependent operations
- ❌ Don't mock internal functions just for testability
- ❌ Don't mock data transformations
- ❌ Don't create mocks that mirror the implementation

**If you need to mock a lot to test something**, it's a sign the code is too tightly coupled. Fix the coupling, not the tests.

## Anti-Patterns

<!-- adapted from mattpocock/skills (MIT) -->
- ❌ Writing tests AFTER implementation (defeats the purpose)
- ❌ **Tautological test** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a hand-derived snapshot, a constant asserted equal to itself). It passes by construction and can never disagree with the code. Expected values must come from an **independent source of truth** — a known-good literal, a worked example, the spec.
- ❌ Mocking everything (tests become meaningless)
- ❌ Huge test files with no organization
- ❌ Tests that test implementation details instead of behavior
- ❌ Testing through incidental internals instead of a pre-agreed seam
- ❌ Testing private methods directly
- ❌ Shared mutable state between tests
