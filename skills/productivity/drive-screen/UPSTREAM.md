# Upstream

- Source: https://github.com/coleam00/skills/tree/main/.claude/skills/drive-screen @ dfaa910
- Author: Cole Medin
- License: MIT (see ./LICENSE)
- Local changes: none (vendored verbatim; LICENSE copied from the repo root).
- Known upstream test failure on macOS: `_test_screenctl.py` "drive letter and separators" (feeds a Windows path `C:\Users\me\proj` to a POSIX slug function) — not a runtime issue.
- macOS: run `python3 scripts/screenctl.py doctor` once; needs Accessibility + Screen Recording granted to the terminal app.
