---
name: error-handling
description: >
  Error handling and logging skill for production-ready code. Ensures every feature
  includes proper error boundaries, structured logging, retry logic, and graceful
  degradation. Use alongside any implementation task. Trigger on: implement, build,
  error handling, logging, "handle errors", resilience, retry, "what if it fails",
  production-ready, robustness, "add logging", observability, monitoring, "make it
  reliable". Always consider this skill during implementation — agents tend to write
  only the happy path without it.
---

# Error Handling & Logging

Every feature must handle failure gracefully from the start. Don't write the happy path and add error handling later — build it in from the beginning.

## Error Classification

Before handling any error, classify it:

| Type | Action | User sees |
|------|--------|-----------|
| **Recoverable** | Retry, fallback, or degrade | Minimal disruption |
| **Fatal** | Fail fast, clean up | Clear error message |
| **User error** | Validate, guide | Helpful correction |
| **Internal** | Log everything | Generic "something went wrong" |

## Error Handling by Layer

### At Input Boundaries
- Validate ALL inputs before processing
- Return specific validation errors (not just "invalid input")
- Use schema validation (Zod, Joi, etc.) — don't hand-write checks
- Fail early: validate at the edge, not deep in business logic

### At API Boundaries
- Return structured error responses with error codes
- Never expose stack traces, file paths, or internal details to clients
- Include correlation IDs for request tracing
- Use consistent error response format across all endpoints:
  ```json
  {
    "error": {
      "code": "PAYMENT_DECLINED",
      "message": "Your payment was declined. Please try another method.",
      "details": {},
      "requestId": "req_abc123"
    }
  }
  ```

### At Integration Points (external APIs, databases, etc.)
- Set **timeouts** on all external calls (no hanging requests)
- Implement **retry with exponential backoff** for transient failures:
  ```
  Attempt 1: immediate
  Attempt 2: 1s delay
  Attempt 3: 2s delay
  Attempt 4: 4s delay (then fail)
  ```
- Have **fallback behavior** when dependencies are down
- Use **circuit breaker** pattern for repeated failures
- Log every external call with timing information

### In Business Logic
- Use **custom error types** (not generic Error):
  ```
  class PaymentDeclinedError extends AppError { ... }
  class InsufficientPermissionsError extends AppError { ... }
  ```
- Include **context**: what was being attempted, with what inputs
- Fail at the **right level** — don't catch too early
- Never swallow errors silently

## Structured Logging

### Every Log Entry Should Include
- **Timestamp** (ISO 8601)
- **Level** (debug, info, warn, error)
- **Message** (human-readable summary)
- **Context** (structured data: userId, requestId, operationName)
- **Error details** (stack, code) when applicable

### When to Log

| Event | Level | What to include |
|-------|-------|----------------|
| Request received | info | method, path, userId |
| External call made | debug | service, endpoint, duration |
| Retry attempted | warn | service, attempt number, error |
| Error caught | error | full error, context, stack |
| Request completed | info | status, duration, responseSize |
| Security event | warn/error | action, userId, IP, result |

### Logging Anti-Patterns
- ❌ Logging sensitive data (passwords, tokens, PII)
- ❌ Logging inside tight loops (performance killer)
- ❌ Using console.log in production (use structured logger)
- ❌ Logging without context (just the error message, no "what was happening")
- ❌ Not logging at all (flying blind)

## Testing Error Paths

For every feature, write tests for:
- **Invalid inputs**: boundary values, wrong types, missing required fields
- **External failures**: timeout, 500, malformed response, connection refused
- **Race conditions**: concurrent access, stale data
- **Resource limits**: disk full, memory pressure, connection pool exhausted
- **Partial failures**: 3 of 5 items succeed, what happens to the other 2?

## Graceful Degradation

When a dependency is down, the system should still work in a reduced capacity:
- Cache layer down → fall through to database (slower but works)
- Search service down → disable search, show browse interface
- Email service down → queue for retry, tell user "email will arrive shortly"
- Analytics down → silently skip, never block user-facing features

The key question: **What's the worst thing that happens when X fails?** Make sure the answer isn't "everything breaks."
