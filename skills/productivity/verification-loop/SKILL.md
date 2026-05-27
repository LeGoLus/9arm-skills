---
name: verification-loop
description: >
  Continuous verification skill. Runs build → test → lint → typecheck → security
  in a loop until everything passes. Use after implementation to ensure nothing is
  broken. Trigger on: verify, "does it work", "check everything", "make sure it
  passes", "run all checks", CI, "before merge", "before PR", "is it ready",
  pre-deployment, integration check, "run the suite". Use this as the final
  quality gate before any commit or PR.
---

# Verification Loop

Run all quality checks in a loop until everything passes. This is the final gate
before code leaves your machine.

## The Loop

```
┌─────────────────────────────────────────┐
│                                         │
│  1. BUILD    → Does it compile?         │
│  2. TEST     → Do tests pass?           │
│  3. LINT     → Is the style correct?    │
│  4. TYPECHECK→ Are types sound?         │
│  5. SECURITY → Any vulnerabilities?     │
│                                         │
│  ALL PASS? → ✅ Ready to commit         │
│  ANY FAIL? → Fix and restart loop       │
│                                         │
└─────────────────────────────────────────┘
```

## Process

### Step 1: BUILD
Run the project's build command:
```bash
# Detect and run the appropriate build command
npm run build        # Node.js/TypeScript
go build ./...       # Go
cargo build          # Rust
python -m py_compile # Python
```

**If build fails**: Fix compilation errors. Don't proceed until the build is clean.

### Step 2: TEST
Run the full test suite:
```bash
npm test             # Node.js
go test ./...        # Go
pytest               # Python
cargo test           # Rust
```

Check results:
- **All pass?** → Continue to Step 3
- **Any fail?** → Fix the failing tests, then restart from Step 1
- **Coverage dropped?** → Write missing tests before proceeding

Target: **80%+ coverage** for new code.

### Step 3: LINT
Run the project's linter:
```bash
npm run lint         # ESLint
golangci-lint run    # Go
ruff check .         # Python
cargo clippy         # Rust
```

**If lint fails**: Fix lint issues. Most are auto-fixable:
```bash
npm run lint -- --fix
ruff check . --fix
```

### Step 4: TYPECHECK
Run the type checker:
```bash
npx tsc --noEmit     # TypeScript
mypy .               # Python
go vet ./...         # Go
```

**If typecheck fails**: Fix type errors. Don't use `any` or `# type: ignore` to suppress.

### Step 5: SECURITY
Quick security checks:
```bash
npm audit            # Node.js
pip audit            # Python (if pip-audit installed)
go vuln check ./...  # Go (if govulncheck installed)
```

Also check:
- No secrets in code (`grep -r "sk-" --include="*.ts"`)
- No `.env` files committed
- No debug/development endpoints exposed

## After All Pass

When all 5 steps pass cleanly:

1. **Summarize results**:
   ```
   ✅ Build: clean
   ✅ Tests: 47/47 pass (92% coverage)
   ✅ Lint: no issues
   ✅ Typecheck: no errors
   ✅ Security: no vulnerabilities
   ```

2. **Ready for commit**: proceed with `/git-workflow`
3. **Ready for PR**: generate a PR description

## Fixing Failures

When something fails, follow this priority:

1. **Build errors first** — nothing else matters if it doesn't compile
2. **Test failures second** — fix the logic before fixing style
3. **Type errors third** — these often reveal real bugs
4. **Lint issues fourth** — most auto-fixable
5. **Security last** — unless it's a critical vulnerability

After fixing, **always restart from Step 1**. A lint fix might break the build.
A test fix might introduce type errors. Always verify the full chain.

## Checkpointing

For long implementation sessions, run the verification loop at milestones:

- After implementing a major component
- After a significant refactor
- Before switching to a different part of the codebase
- Before taking a break or compacting context

This catches issues early when they're easy to fix.

## Anti-Patterns

- ❌ Skipping steps ("tests pass, that's good enough")
- ❌ Suppressing lint/type errors instead of fixing them
- ❌ Running only the tests for the files you changed
- ❌ Not restarting from Step 1 after fixes
- ❌ Committing with known failures ("I'll fix it later")
- ❌ Ignoring security warnings ("it's just a dev dependency")
