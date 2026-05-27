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

Perform a structured self-review before committing any changes. Read through ALL changed files systematically.

## Review Process

1. **List all changed files** — understand the full scope of changes
2. **Walk through each category** below
3. **Rate each issue found**: critical (must fix) / warning (should fix) / nit (nice to fix)
4. **Fix** all critical and warning issues
5. **Note** nits for future improvement
6. **Re-run tests** after all fixes
7. **Confirm** the changes are ready

## Review Categories

### 1. Security

- [ ] No secrets, credentials, or API keys in code
- [ ] User inputs are validated and sanitized
- [ ] SQL queries use parameterized statements (no string concatenation)
- [ ] Authentication/authorization checks are in place for all endpoints
- [ ] No sensitive data in logs (PII, passwords, tokens)
- [ ] Dependencies don't have known vulnerabilities
- [ ] File uploads are validated (type, size, content)
- [ ] CORS is configured correctly (not wildcard in production)
- [ ] Rate limiting on public endpoints

### 2. Performance

- [ ] No N+1 database queries
- [ ] Large lists are paginated
- [ ] Expensive operations are cached or batched
- [ ] No unnecessary re-renders (React: memoization where needed)
- [ ] Database queries have appropriate indexes
- [ ] No memory leaks (event listeners cleaned up, subscriptions unsubscribed)
- [ ] Large files/images are lazy-loaded
- [ ] No synchronous operations that should be async

### 3. Accessibility (if UI changes)

- [ ] Semantic HTML elements used (`<button>`, `<nav>`, `<main>`, not `<div>` for everything)
- [ ] ARIA labels on interactive elements without visible text
- [ ] Keyboard navigation works (tab order, enter/space to activate)
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Images have meaningful alt text
- [ ] Focus management after dynamic content changes
- [ ] Error messages are announced to screen readers

### 4. Code Quality

- [ ] Names are clear and consistent with codebase conventions
- [ ] No dead code or commented-out blocks
- [ ] Functions have a single responsibility
- [ ] No magic numbers (use named constants)
- [ ] Types are explicit (no `any` in TypeScript unless truly necessary)
- [ ] Error messages are helpful and actionable
- [ ] No premature abstractions
- [ ] No copy-pasted code (DRY within reason)
- [ ] Comments explain WHY, not WHAT
- [ ] No TODO/FIXME/HACK without a linked issue

### 5. Test Coverage

- [ ] Happy path is tested
- [ ] Edge cases are tested (empty input, boundary values)
- [ ] Error paths are tested (what happens when things fail)
- [ ] Tests are independent (no shared mutable state)
- [ ] Test names describe the behavior being verified
- [ ] No flaky tests (time-dependent, order-dependent)
- [ ] Assertions are specific (not just "it doesn't throw")

### 6. API Design (if adding/changing APIs)

- [ ] Endpoints follow REST conventions (or documented alternative)
- [ ] Request/response schemas are documented
- [ ] Error responses are consistent
- [ ] Breaking changes are versioned or migrated
- [ ] Rate limits and timeouts are configured

## Output Format

After review, summarize:

```
## Code Review Summary

### Critical Issues (must fix before commit)
- [file:line] Description of issue

### Warnings (should fix)
- [file:line] Description of issue

### Nits (consider for later)
- [file:line] Description of suggestion

### Looks Good
- [List what was well-done — positive reinforcement matters]
```

Then fix all critical and warning issues before proceeding.
