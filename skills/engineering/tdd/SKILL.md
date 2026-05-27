---
name: tdd
description: >
  Test-Driven Development skill for all implementation tasks. Use whenever the user
  wants to implement a feature, fix a bug, write code, or build anything. Forces a
  strict red-green-refactor loop that dramatically improves code quality. Trigger on:
  implement, build, code, fix, "write the code", "make it work", any coding task,
  bug fix, feature implementation, "let's build this", "start coding". This should
  be the DEFAULT approach for all implementation work.
---

# TDD — Test-Driven Development

Follow a strict **red-green-refactor** loop for every implementation task.

## Philosophy

- Tests are a **design tool**, not just verification
- Write the test you WISH you could write, then make it possible
- Prefer **deep modules**: large functionality behind thin interfaces
- Mock at **architectural boundaries**, not at every function call
- Pure functions are testable by nature — don't extract them just for testing
- If you can't figure out where to test, the module boundaries are wrong

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

### Step 4: REFACTOR

```
Now clean up. Tests are your safety net.
Run tests after every change — they must stay green.
```

Look for:
- **Duplication** between implementation and tests
- **Deep module opportunities**: combine small files always used together
- **Unnecessary abstractions**: if a wrapper just forwards calls, inline it
- **Naming**: does every name communicate intent?
- **Complexity**: can you simplify without losing capability?

### Step 5: Repeat

Move to the next behavior. Continue until ALL acceptance criteria from the PRD task are met.

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

## Refactoring Patterns

During the refactor step, look for:

1. **Extract when duplicated**: Only extract shared code when you see actual duplication, not "potential" reuse
2. **Inline when trivial**: If a function is called once and adds no clarity, inline it
3. **Deepen when scattered**: If understanding one concept requires 5 files, merge them
4. **Simplify when complex**: If a test is hard to write, the interface is too complex

## Anti-Patterns

- ❌ Writing tests AFTER implementation (defeats the purpose)
- ❌ Mocking everything (tests become meaningless)
- ❌ Huge test files with no organization
- ❌ Tests that test implementation details instead of behavior
- ❌ Skipping the refactor step (debt accumulates)
- ❌ Testing private methods directly
- ❌ Shared mutable state between tests
