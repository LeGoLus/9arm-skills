# Case format

One JSON file = one task run the same way on every rung.

```json
{
  "name": "finnomena-healthcheck-api",          // folder name under runs/
  "skill": "~/9arm-skills/skills/.../SKILL.md", // the skill being tested (for the ledger)
  "mode": "command",                            // or "computer-use" (adds Playwright MCP)
  "workdir": "~/projects/...",                  // agent cwd; Antigravity IDE opens this folder
  "private": "~/Documents/model-ladder/private/x.json",  // {key: value}, used as {private.key}
  "side_effects": "creates 1 real report per run",       // present -> climb needs --confirm
  "goal": "one line for the judge",
  "prompt": "... write results into {out} ... {private.customer} ...",
  "allowed_tools": ["Read", "Write", "Bash(uv run *)"],  // claude-runner tiers (--allowedTools)
  "browser_profile": "~/.local/share/.../profile",       // computer-use: logged-in profile for Playwright
  "timeout_s": 900,
  "checks": ["test -s {out}/a.pdf"],            // shell, run in workdir; exit 0 = pass
  "rubric": "what 'same result' means: which files, numbers, steps"
}
```

(Comments are for reading only; real case files are plain JSON.)

## Writing good cases

- **The prompt is the whole instruction.** Point it at the skill file and say where outputs go (`{out}`) and what
  must NOT happen. Every rung gets the identical text.
- **Outputs into `{out}`, as files.** The judge sees the final message, the file list, small text files and the
  check results. Ask for a `result.json` with the key facts so runs compare on data, not prose.
- **Checks catch the cheap failures** (file missing, PDF still encrypted, wrong count). A failed check stops the
  rung at once: no more runs, no judge call.
- **Rubric = the user's purpose.** Say which differences don't matter (wording, order, timing) and which do
  (a number, a page count, a skipped step, a forbidden side effect).
- Tools: give the least that does the job. A rung that needs more tools than the case allows simply fails;
  that is useful information, not a reason to open everything.

## Computer-use mode

- claude-runner tiers get `--mcp-config` with `@playwright/mcp` (pinned in the tier file), headless, on
  `browser_profile`, downloads into `{out}`; `--strict-mcp-config` so no other MCP servers load.
- The profile must already be logged in (the user logs in; agents never type passwords) and not open elsewhere.
- Antigravity uses its own browser; the case prompt is the same.

## Hand-off tiers (Antigravity)

- The run folder gets `TASK.md`: "read AGENTS.md and .agents/HANDOFF.md first", the prompt, where to write, and
  "write out/DONE.json `{status, summary}` last". The tier waits for DONE.json until `timeout_s`.
- IDE: writes `<run>/ladder-<time>-<pid>-<n>.code-workspace` (folders: workdir + run folder) and opens it in a new
  window, so the window title is unique. With `--drive-screen` it then runs the palette command
  **"Open Chat with Agent"** (`antigravity.toggleChatFocus`), pastes "Read TASK.md and do it", presses Enter, and
  checks that a new conversation folder appeared in `~/.gemini/antigravity-ide/brain/`; if not (a fresh window
  loads its Agent panel late) it retries, 3 tries. Measured 2026-10-27: try 1 too early, try 2 took it.
  - `antigravity-ide chat "<prompt>"` does NOT reach Antigravity's Agent box (it is VS Code's chat command).
  - Cmd+L toggles: it CLOSES the panel when the Agent box already has focus. Use the palette command.
  The model is whatever the IDE is set to (Gemini 3.8 Flash High on 2026-10-27); note it if it matters.
- A folder the IDE has not seen shows a **workspace-trust dialog** and nothing runs until the user answers it:
  runs live under `~/Documents/model-ladder/` so the user trusts that once; real work folders are usually trusted.
- Desktop (`spare.google-desktop`): the prompt is copied to the clipboard; the user pastes it in Antigravity.
- Each hand-off run opens a window: close them after a climb.

## Where things land

```
~/Documents/model-ladder/
  cases/  private/            # yours; never in a repo
  runs/<case>/golden/         # Opus reference (reused until --new-golden)
  runs/<case>/<stamp>/<rung>/run<n>/{prompt.txt,stdout.json,stderr.txt,meta.json,out/}
  runs/<case>/<stamp>/<rung>/judge.json
  runs/<case>/<stamp>/summary.json
  ledger.md                   # one row per climb
  handoff/                    # daily `run` calls that went to Antigravity
~/.agents/tiers.json          # the tiers; ~/.agents/runs/, ~/.agents/logs/{runs,feedback}.jsonl for daily `run`
```
