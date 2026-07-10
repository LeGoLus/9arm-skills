---
name: git-guardrails
description: Set up Claude Code hooks to block destructive git commands before they execute. Use when the user wants to prevent accidental destructive git operations, add git safety hooks, or block hard-resets and force-pushes in Claude Code.
---

> Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT). Local adaptations noted inline.
> Default block list excludes plain `git push` — this workflow pushes deliberately via instruction. See commented opt-in in the script if you want to block plain push too.

# Setup Git Guardrails

Sets up a PreToolUse hook that intercepts and blocks destructive git commands before Claude executes them.

## What Gets Blocked (defaults)

- `git push --force` / `push -f` (force push only — plain push is NOT blocked by default)
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .` (wholesale working-tree discards)

Plain `git push` is **not** blocked by default because this machine's workflow pushes deliberately via instruction. To also block plain push, uncomment the `"git push"` line in the copied script.

When blocked, Claude sees a message telling it that it does not have authority to access these commands.

## Steps

### 1. Ask scope

Ask the user: install for **this project only** (`.claude/settings.json`) or **all projects** (`~/.claude/settings.json`)?

### 2. Copy the hook script

The bundled script is at: [scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh)

Copy it to the target location based on scope:

- **Project**: `.claude/hooks/block-dangerous-git.sh`
- **Global**: `~/.claude/hooks/block-dangerous-git.sh`

Make it executable with `chmod +x`.

### 3. Add hook to settings

Add to the appropriate settings file:

**Project** (`.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

**Global** (`~/.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

If the settings file already exists, merge the hook into existing `hooks.PreToolUse` array — don't overwrite other settings.

### 4. Ask about customization

Ask if user wants to add or remove any patterns from the blocked list. Edit the copied script accordingly. In particular, ask whether they want to enable plain `git push` blocking (uncomment the opt-in line).

### 5. Verify

Run a quick test:

```bash
echo '{"tool_input":{"command":"git push --force origin main"}}' | <path-to-script>
```

Should exit with code 2 and print a BLOCKED message to stderr.
