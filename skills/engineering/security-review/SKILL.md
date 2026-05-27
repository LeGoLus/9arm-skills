---
name: security-review
description: >
  Comprehensive security review skill. Performs OWASP Top 10 audit, checks for
  injection vulnerabilities, authentication/authorization issues, data exposure,
  and dependency risks. Trigger on: security, "is this secure", "security review",
  "before production", "before deploy", vulnerability, OWASP, penetration test,
  "check for security issues", audit, "preparing for launch". Use before any
  production deployment or when handling sensitive data.
---

# Security Review

Perform a comprehensive security audit against OWASP Top 10 and common vulnerability patterns.

## When to Use

- Before deploying to production
- After adding authentication/authorization
- When handling user input, file uploads, or payments
- When adding new API endpoints
- When integrating third-party services
- During periodic security audits (monthly recommended)

## The OWASP Top 10 Checklist

### 1. Injection (SQL, NoSQL, Command, LDAP)
- [ ] All database queries use parameterized statements or ORM
- [ ] No string concatenation in queries: `"SELECT * FROM users WHERE id = " + userId`
- [ ] Command execution inputs are escaped and validated
- [ ] GraphQL queries have depth/complexity limits
- [ ] Template engines auto-escape output by default

**Test**: Try `'; DROP TABLE users; --` in every text input.

### 2. Broken Authentication
- [ ] Passwords hashed with bcrypt/scrypt/argon2 (NOT MD5/SHA1)
- [ ] Rate limiting on login endpoints (prevent brute force)
- [ ] Session tokens are cryptographically random
- [ ] Sessions expire after reasonable timeout
- [ ] Password reset tokens expire and are single-use
- [ ] Multi-factor authentication available for sensitive operations
- [ ] No default credentials in any environment

### 3. Sensitive Data Exposure
- [ ] HTTPS enforced everywhere (HSTS headers)
- [ ] Sensitive data encrypted at rest (PII, payment info)
- [ ] API responses don't include unnecessary sensitive fields
- [ ] Logs don't contain passwords, tokens, or PII
- [ ] Error messages don't expose stack traces or internal paths
- [ ] Database backups are encrypted
- [ ] Removed all console.log/print statements with sensitive data

### 4. XML External Entities (XXE)
- [ ] XML parsing disables external entity resolution
- [ ] Use JSON instead of XML where possible
- [ ] File upload validation doesn't rely on XML parsing

### 5. Broken Access Control
- [ ] Every endpoint checks authorization (not just authentication)
- [ ] Users can't access other users' data by changing IDs
- [ ] Admin endpoints are properly restricted
- [ ] CORS configuration is restrictive (not `*` in production)
- [ ] Directory listing is disabled
- [ ] API keys have minimum required permissions
- [ ] Role-based access control is enforced server-side

**Test**: Log in as User A, try accessing User B's resources by changing the ID.

### 6. Security Misconfiguration
- [ ] Debug mode is OFF in production
- [ ] Default accounts/passwords are removed
- [ ] Security headers set: CSP, X-Frame-Options, X-Content-Type-Options
- [ ] Unnecessary features/endpoints are disabled
- [ ] Server version headers are hidden
- [ ] Directory browsing is disabled
- [ ] Stack traces don't leak to end users

### 7. Cross-Site Scripting (XSS)
- [ ] All user input is escaped before rendering
- [ ] Content Security Policy (CSP) headers are configured
- [ ] React/Vue/Angular auto-escaping is not bypassed (no dangerouslySetInnerHTML)
- [ ] Rich text input is sanitized with a whitelist library (DOMPurify)
- [ ] URL parameters are validated before use in DOM
- [ ] SVG uploads are sanitized (they can contain scripts)

### 8. Insecure Deserialization
- [ ] User input is never directly deserialized into objects
- [ ] JSON.parse() inputs are validated against a schema
- [ ] Pickle/Marshal/eval() never processes user input
- [ ] JWT tokens are verified with proper signature checking

### 9. Using Components with Known Vulnerabilities
- [ ] `npm audit` / `pip audit` / `go vuln check` shows no critical issues
- [ ] Dependencies are regularly updated
- [ ] Lock files are committed and reviewed
- [ ] No dependencies with known CVEs in production
- [ ] Unused dependencies are removed

### 10. Insufficient Logging & Monitoring
- [ ] Authentication events are logged (login, logout, failed attempts)
- [ ] Authorization failures are logged
- [ ] Input validation failures are logged
- [ ] Server errors are logged with context (but not with sensitive data)
- [ ] Logs are tamper-resistant (append-only or external service)
- [ ] Alerting exists for suspicious patterns (many failed logins, etc.)

## Additional Checks

### API Security
- [ ] Rate limiting on all public endpoints
- [ ] Request size limits configured
- [ ] API versioning in place
- [ ] Input validation on all parameters (type, range, format)
- [ ] Pagination limits prevent data dumps
- [ ] Webhook signatures verified

### File Upload Security
- [ ] File type validated by content (magic bytes), not just extension
- [ ] File size limits enforced
- [ ] Uploaded files stored outside web root
- [ ] Filenames are sanitized (no path traversal)
- [ ] Images are re-processed to strip metadata/embedded scripts
- [ ] Virus scanning for uploaded files (production)

### Environment & Secrets
- [ ] No secrets in source code or config files
- [ ] `.env` files are in `.gitignore`
- [ ] Environment variables for all secrets
- [ ] Different secrets for dev/staging/production
- [ ] Secret rotation plan exists
- [ ] No secrets in Docker images or build artifacts

## Output Format

```markdown
## Security Review Report

### Critical (must fix before deploy)
- [Category] Description and location
- [Category] Description and location

### High (fix within 1 sprint)
- [Category] Description and location

### Medium (schedule for fix)
- [Category] Description and location

### Low (improve when possible)
- [Category] Description and location

### Passed
- [List of categories that passed all checks]
```

## Process

1. Run through the full OWASP checklist above
2. Check additional categories relevant to the project
3. Categorize findings by severity
4. For each critical/high finding, suggest a specific fix
5. Verify fixes don't introduce new issues
