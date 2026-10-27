#!/usr/bin/env python3
"""Model tiers for every skill: prove the cheapest tier that does a task (climb), then use it (run).

The tiers live in ONE file, ~/.agents/tiers.json (AGENT_TIERS overrides; template: tiers.example.json):
free (MiniMax) -> google (Antigravity IDE) -> claude-small (Haiku) -> claude-top (Opus). Skills name a tier,
never a model, so swapping MiniMax for another model is one edit there.

  python3 ladder.py doctor
  python3 ladder.py climb CASE.json [--runs 3] [--tiers free,google] [--confirm] [--new-golden]
  python3 ladder.py run --skill NAME --cwd DIR --prompt-file F [--tools T] [--check CMD]... [--rubric R]
                        [--browser PROFILE] [--tier T] [--unattended]
  python3 ladder.py feedback SKILL good|bad "why"
  python3 ladder.py status [SKILL]
  python3 ladder.py report CASE_NAME

climb: Opus does the task once (reference), then each tier below the judge does it N times; a tier passes when
every run is clean, passes the case's checks and the judge (one Opus call per tier) rules each run the same.
run: the skill's routed tier does the task; on failure it prints what went wrong and moves one tier up; every
Nth success is spot-checked by the judge; the call is logged (and noted in the folder's .agents/LOG.md).

Nothing here bypasses a CLI's permission checks. Keys go to the child process only; saved logs are redacted.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import threading
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIERS_FILE = Path(os.environ.get("AGENT_TIERS", Path.home() / ".agents" / "tiers.json"))
LOGS = TIERS_FILE.parent / "logs"
LAB = Path(os.environ.get("MODEL_LADDER_HOME", Path.home() / "Documents" / "model-ladder"))
NESTED = ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_CHILD_SESSION")
ALIASES = ("ANTHROPIC_DEFAULT_OPUS_MODEL", "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_HAIKU_MODEL")
PROXY = ("ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_MODEL", "ANTHROPIC_SMALL_FAST_MODEL", *ALIASES)
POLL_S = 5
SCREENCTL = Path.home() / ".claude" / "skills" / "drive-screen" / "scripts" / "screenctl.py"


# --- the tier file ----------------------------------------------------------------------------------------------

def load_tiers(path: Path = TIERS_FILE) -> dict:
    if not path.exists():
        sys.exit(f"no tier file at {path}; copy {HERE / 'tiers.example.json'} there and edit it")
    return json.loads(path.read_text(encoding="utf-8"))


def tier(t: dict, name: str) -> dict:
    found = t["tiers"].get(name) or (t.get("spare") or {}).get(name)
    if not found:
        sys.exit(f"no tier {name!r} in the tier file (have {', '.join([*t['tiers'], *(t.get('spare') or {})])})")
    return {**found, "id": name}


def skill_route(t: dict, skill: str) -> tuple[str, str]:
    """(starting tier, highest tier it may climb to) for a skill; unknown skills start cheapest."""
    route = (t.get("skills") or {}).get(skill) or {}
    return route.get("tier", t["order"][0]), route.get("max_tier", t["order"][-1])


def skill_skip(t: dict, skill: str) -> list[str]:
    """Tiers a skill's climb proved it cannot use (the route's "skip")."""
    return list(((t.get("skills") or {}).get(skill) or {}).get("skip") or [])


def escalation(t: dict, start: str, top: str, unattended: bool = False, skip=()) -> list[str]:
    order = t["order"]
    lo = order.index(start) if start in order else 0
    hi = order.index(top) if top in order else len(order) - 1
    chain = [start, *order[lo + 1:hi + 1]]
    return [n for n in chain if n not in skip and not (unattended and is_handoff(tier(t, n)))]


def is_handoff(x: dict) -> bool:
    """Needs a person or an app window (Antigravity); everything not run by the claude CLI counts."""
    return x.get("handoff", x["runner"] != "claude")


def ladder_rungs(t: dict) -> list[dict]:
    return [tier(t, n) for n in t["order"] if n != t["judge"]]


# --- building one run -------------------------------------------------------------------------------------------

def read_env_key(path, name: str) -> str:
    for line in Path(path).expanduser().read_text(encoding="utf-8").splitlines():
        k, sep, v = line.strip().partition("=")
        if sep and k.strip().removeprefix("export ").strip() == name:
            return v.strip().strip("'\"")
    sys.exit(f"{name} not found in {path}")


def child_env(rung: dict, base: dict, key: str | None = None) -> dict:
    env = {k: v for k, v in base.items() if k not in NESTED and k not in PROXY}
    if rung.get("base_url"):
        env.pop("ANTHROPIC_API_KEY", None)
        env.update(ANTHROPIC_BASE_URL=rung["base_url"], ANTHROPIC_AUTH_TOKEN=key or "",
                   ANTHROPIC_MODEL=rung["model"], ANTHROPIC_SMALL_FAST_MODEL=rung["model"])
        env.update({a: rung["model"] for a in ALIASES})   # subagents asking for opus/sonnet/haiku stay on this model
    return env


def claude_cmd(rung: dict, case: dict, prompt: str, mcp_file: str | None, out: str) -> list[str]:
    tools = list(case.get("allowed_tools") or [])
    cmd = ["claude", "-p", prompt, "--model", rung["model"], "--output-format", "stream-json", "--verbose",
           "--no-session-persistence", "--add-dir", out]
    if mcp_file:
        cmd += ["--mcp-config", mcp_file, "--strict-mcp-config"]
        tools.append("mcp__playwright")
    return cmd + ["--allowedTools", ",".join(tools)] if tools else cmd


def task_text(prompt: str, out: str, done: str) -> str:
    return (f"# Task (handed off by model-ladder)\n\nFirst read AGENTS.md in the workspace root and .agents/HANDOFF.md "
            f"if they exist, and follow their rules.\n\n{prompt}\n\nWrite every output file into: {out}\n\n"
            f"When you are finished, or stuck, write {done} as JSON:\n"
            '{"status": "done" or "failed", "summary": "what you did and found, one paragraph"}\n'
            "Write DONE.json last, only when the work is over.\n")


def ide_workspace(run_dir: Path, workdir: str, name: str) -> Path:
    """A workspace file with a unique name: the IDE window is titled '<name> (Workspace)', a stable target
    (screenctl's window handles are positions that shift when another window opens)."""
    ws = Path(run_dir) / f"{name}.code-workspace"
    ws.write_text(json.dumps({"folders": [{"path": workdir}, {"path": str(run_dir)}]}, indent=2))
    return ws


def ide_title(name: str) -> str:
    return f"{name} (Workspace)"


def ide_cmds(workspace: Path, bin_path: str = "antigravity-ide") -> list[list[str]]:
    return [[bin_path, "-n", str(workspace)]]


def screen_steps(screenctl, title: str, text: str) -> list[list[str]]:
    """Antigravity IDE: run "Open Chat with Agent" from the palette (focuses the Agent box whatever its state;
    Cmd+L would close the panel if the box already had focus), paste the prompt, Enter sends it."""
    base = ["python3", str(screenctl)]
    act = lambda kind, flag, value: base + [kind, "--title", title, flag, value]  # noqa: E731
    return [act("key", "--keys", "cmd+shift+p"), act("paste", "--text", "Open Chat with Agent"),
            act("key", "--keys", "enter"), act("paste", "--text", text), act("key", "--keys", "enter")]


def conversations(brain) -> set[str]:
    """Antigravity IDE makes one folder per agent conversation under its brain dir."""
    b = Path(brain).expanduser()
    return {d.name for d in b.iterdir() if d.is_dir()} if b.is_dir() else set()


def agent_started(before: set[str], brain) -> bool:
    return bool(conversations(brain) - before)


_IDE_SEQ = [0]


def ide_name() -> str:
    _IDE_SEQ[0] += 1
    return f"ladder-{datetime.now():%m%d-%H%M%S}-{os.getpid()}-{_IDE_SEQ[0]}"


def fill(template: str, out: str, private: dict) -> str:
    def sub(m):
        if m.group(1) not in private:
            sys.exit(f"case prompt needs private.{m.group(1)} but the private file has no such key")
        return str(private[m.group(1)])
    return re.sub(r"\{private\.(\w+)\}", sub, template.replace("{out}", out))


def redact(text: str, secrets) -> str:
    for s in secrets:
        if s:
            text = text.replace(s, "***")
    return text


def final_text(stdout: str) -> str:
    try:
        data = json.loads(stdout)
    except (json.JSONDecodeError, TypeError):
        return stdout
    if isinstance(data, dict):
        for k in ("result", "response", "summary", "text", "output"):
            if isinstance(data.get(k), str):
                return data[k]
    return stdout


def parse_judge(raw: str) -> dict | None:
    text = final_text(raw)
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    for candidate in [text, *fenced, *re.findall(r"\{.*\}", text, re.S)]:
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and "runs" in data:
            return data
    return None


def _post_json(url: str, headers: dict, body: dict) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def probe_model(rung: dict, key: str, post=_post_json) -> tuple[str, bool]:
    """Ask a proxied endpoint which model really answers: MiniMax quietly swaps an unknown name for another model."""
    data = post(rung["base_url"].rstrip("/") + "/v1/messages",
                {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                {"model": rung["model"], "max_tokens": 8, "messages": [{"role": "user", "content": "hi"}]})
    served = str(data.get("model") or "")
    return served, served.lower() == rung["model"].lower()


# --- verdicts ---------------------------------------------------------------------------------------------------

def rung_passed(runs: list[dict], judge: dict | None, need: int) -> bool:
    if len(runs) < need or not all(map(clean, runs)):
        return False
    verdicts = (judge or {}).get("runs") or []
    return len(verdicts) >= need and all(v.get("pass") is True for v in verdicts)


def clean(m: dict) -> bool:
    return m["exit"] == 0 and not m["timed_out"] and m["checks_ok"]


def climb(rungs: list[dict], attempt) -> str | None:
    for rung in rungs:
        if attempt(rung):
            return rung["id"]
    return None


def guard(case: dict, confirm: bool) -> None:
    if case.get("side_effects") and not confirm:
        sys.exit(f"this case has real side effects ({case['side_effects']}); ask the user, then add --confirm")


def spot_check_due(successes: int, every: int) -> bool:
    return every > 0 and successes > 0 and successes % every == 0


def feedback_advice(rows: list[dict], skill: str, window: int = 10, limit: int = 2) -> str | None:
    recent = [r for r in rows if r.get("skill") == skill][-window:]
    bad = sum(r.get("verdict") == "bad" for r in recent)
    if bad >= limit:
        return (f"{skill}: {bad} bad marks in the last {len(recent)} — move it one tier up in the tier file and "
                f"re-run model-ladder on its case")
    return None


def log_to_folder(folder, entry: dict) -> bool:
    log = Path(folder).expanduser() / ".agents" / "LOG.md"
    if not log.exists():
        return False
    with log.open("a", encoding="utf-8") as f:
        f.write(f"\n## {entry['when']} — {entry['agent']} ({entry['tier']}: {entry['model']})\n"
                f"- did: {entry['did']}\n- result: {entry['result']}\n- next: {entry['next']}\n")
    return True


# --- running ----------------------------------------------------------------------------------------------------

def _mcp_servers(t: dict, profile: str, out: str) -> dict:
    args = ["-y", t["playwright_mcp"], "--headless", "--output-dir", out]
    if profile:
        args += ["--user-data-dir", str(Path(profile).expanduser())]
    return {"playwright": {"command": "npx", "args": args}}


def read_until_result(lines) -> tuple[str | None, list[str], dict]:
    """Read claude's stream-json until its result event. Returns (result line or None, lines seen, served models)."""
    seen, models = [], {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        seen.append(line)
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "assistant":
            m = (ev.get("message") or {}).get("model")
            if m:
                models[m] = models.get(m, 0) + 1
        if ev.get("type") == "result":
            return line, seen, models
    return None, seen, models


def _run_claude(t, rung, case, prompt, run_dir, out):
    mcp_file = None
    if case.get("mode") == "computer-use":
        mcp_file = str(run_dir / "mcp.json")
        Path(mcp_file).write_text(json.dumps({"mcpServers": _mcp_servers(t, case.get("browser_profile", ""), str(out))}))
    key = read_env_key(rung["key"]["file"], rung["key"]["name"]) if rung.get("key") else None
    cmd = claude_cmd(rung, case, prompt, mcp_file, str(out))
    err = run_dir / "stderr.raw"
    with err.open("w") as ef:
        p = subprocess.Popen(cmd, cwd=Path(case["workdir"]).expanduser(), env=child_env(rung, dict(os.environ), key),
                             stdout=subprocess.PIPE, stderr=ef, text=True, stdin=subprocess.DEVNULL)
        timer = threading.Timer(case.get("timeout_s", 900), p.kill)
        timer.start()
        try:
            result, seen, models = read_until_result(p.stdout)
        finally:
            timer.cancel()
            if p.poll() is None:   # the result is in; background tasks it left running must not hold the run open
                p.terminate()
            p.wait()
    (run_dir / "stream.jsonl").write_text(redact("\n".join(seen), [key]), encoding="utf-8")
    (run_dir / "served_models.json").write_text(json.dumps(models), encoding="utf-8")
    stderr = redact(err.read_text(errors="replace"), [key])
    err.unlink()
    if result is None:
        return (p.returncode or -1), p.returncode in (-9, None), "", stderr
    return (1 if json.loads(result).get("is_error") else 0), False, redact(result, [key]), stderr


def _run_handoff(t, rung, case, prompt, run_dir, out):
    """Antigravity: the agent reads TASK.md in the folder and signals the end by writing out/DONE.json."""
    done = out / "DONE.json"
    task = run_dir / "TASK.md"
    task.write_text(task_text(prompt, str(out), str(done)), encoding="utf-8")
    chat = f"Read {task} and do the task it describes."
    workdir = str(Path(case["workdir"]).expanduser())
    sent = False
    if rung["runner"] == "antigravity-ide":
        name = ide_name()
        for cmd in ide_cmds(ide_workspace(run_dir, workdir, name), rung.get("bin", "antigravity-ide")):
            subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        title = ide_title(name)
        for _ in range(20):   # wait for the window to exist before typing into it
            time.sleep(1)
            found = subprocess.run(["python3", str(SCREENCTL), "find", "--title", title], capture_output=True,
                                   text=True).returncode == 0 if SCREENCTL.exists() else False
            if found:
                break
        if case.get("drive_screen") and found:
            brain = rung.get("brain", "~/.gemini/antigravity-ide/brain")
            for attempt in range(1, 4):   # a fresh window loads its Agent panel late: check it took the task
                time.sleep(8 if attempt == 1 else 12)
                before = conversations(brain)
                print(f"    typing the task into '{title}' (try {attempt}/3): hands off the keyboard ~10s")
                for step in screen_steps(SCREENCTL, title, chat):
                    subprocess.run(step, capture_output=True, text=True, timeout=60)
                    time.sleep(1.5)   # palette and Agent panel need a moment between keys
                for _ in range(15):
                    if agent_started(before, brain):
                        sent = True
                        break
                    time.sleep(1)
                if sent:
                    break
            if not sent:
                print("    the IDE agent did not take the task after 3 tries; falling back to paste-by-hand")
    if not sent:
        subprocess.run(["pbcopy"], input=chat, text=True)
        where = "the Antigravity IDE window that just opened (Cmd+L)" if rung["runner"] == "antigravity-ide" \
            else f"Antigravity on {workdir}"
        print(f"    paste the prompt (copied to the clipboard) into {where} and press Enter: {chat}")
    else:
        print("    Antigravity IDE is working (approve its prompts there if it asks)")
    deadline = time.time() + case.get("timeout_s", 900)
    while time.time() < deadline:
        if done.exists():
            time.sleep(1)
            text = done.read_text(encoding="utf-8", errors="replace")
            try:
                status = json.loads(text).get("status")
            except json.JSONDecodeError:
                status = "unreadable DONE.json"
            return (0 if status == "done" else 1), False, text, "" if status == "done" else f"status: {status}"
        time.sleep(POLL_S)
    return -1, True, "", f"no DONE.json after {case.get('timeout_s', 900)}s"


def run_once(t: dict, rung: dict, case: dict, run_dir: Path, private: dict) -> dict:
    out = run_dir / "out"
    out.mkdir(parents=True, exist_ok=True)
    prompt = fill(case["prompt"], str(out), private)
    (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    t0 = time.time()
    runner = _run_claude if rung["runner"] == "claude" else _run_handoff
    code, timed_out, stdout, stderr = runner(t, rung, case, prompt, run_dir, out)
    secs = round(time.time() - t0, 1)
    (run_dir / "stdout.json").write_text(stdout, encoding="utf-8")
    (run_dir / "stderr.txt").write_text(stderr, encoding="utf-8")
    checks = [_check(c, out, Path(case["workdir"]).expanduser()) for c in case.get("checks") or []]
    meta = {"tier": rung["id"], "model": rung["model"], "exit": code, "timed_out": timed_out, "seconds": secs,
            "checks": checks, "checks_ok": all(c["ok"] for c in checks), **_usage(stdout, rung)}
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    print(f"  {rung['id']} {run_dir.name}: exit {code}{' TIMEOUT' if timed_out else ''}, {secs}s, "
          f"checks {sum(c['ok'] for c in checks)}/{len(checks)}")
    return meta


def _check(cmd: str, out: Path, cwd: Path) -> dict:
    c = cmd.replace("{out}", str(out))
    p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True, timeout=120)
    return {"cmd": c, "ok": p.returncode == 0, "output": (p.stdout + p.stderr)[-400:]}


def _usage(stdout: str, rung: dict) -> dict:
    try:
        data = json.loads(stdout)
    except (json.JSONDecodeError, TypeError):
        return {}
    if not isinstance(data, dict):
        return {}
    u = data.get("usage") or {}
    tokens = sum(u.get(k) or 0 for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens",
                                         "cache_read_input_tokens"))
    info = {"turns": data.get("num_turns"), "tokens": tokens or u.get("total_tokens") or None}
    if rung.get("cost") == "claude":   # a proxied model's figure is priced as if it were Claude: meaningless
        info["claude_usd"] = data.get("total_cost_usd")
    return info


def _snapshot(run_dir: Path, limit=3000) -> str:
    meta = json.loads((run_dir / "meta.json").read_text())
    files = []
    for f in sorted((run_dir / "out").rglob("*")):
        if f.is_file():
            line = f"- {f.relative_to(run_dir / 'out')} ({f.stat().st_size} bytes)"
            if f.suffix in (".txt", ".md", ".json", ".csv", ".log") and f.stat().st_size <= limit:
                line += "\n```\n" + f.read_text(errors="replace") + "\n```"
            files.append(line)
    answer = final_text((run_dir / "stdout.json").read_text())[-limit:]
    checks = "\n".join(f"- {'PASS' if c['ok'] else 'FAIL'} `{c['cmd']}`" for c in meta["checks"]) or "- (none)"
    return f"Final message:\n{answer}\n\nFiles in out/:\n" + ("\n".join(files) or "- (none)") + f"\n\nChecks:\n{checks}"


def judge(t: dict, case: dict, golden: Path | None, runs: list[Path], label: str) -> dict | None:
    """One call to the judge tier, no tools: each candidate vs the reference (or vs the rubric alone)."""
    packet = [f"# Task\n{case.get('goal') or case['prompt']}\n\n# What counts as a good / the same result\n"
              f"{case.get('rubric') or 'Same facts, numbers and files as the reference; wording may differ.'}"]
    if golden:
        packet.append(f"# Reference run (Opus)\n{_snapshot(golden)}")
    packet += [f"# Candidate run {i} ({label})\n{_snapshot(r)}" for i, r in enumerate(runs, 1)]
    ask = ("You are the judge. For each candidate run decide whether it " +
           ("reached the SAME result as the reference" if golden else "did the task correctly by the rubric") +
           " for the user's purpose (ignore wording, order and speed; a missing file, a wrong number or a skipped "
           "step is a fail). Reply with JSON only: "
           '{"runs":[{"run":1,"pass":true,"why":"..."}],"summary":"..."}')
    j = tier(t, t["judge"])
    cmd = ["claude", "-p", ask, "--model", j["model"], "--output-format", "json", "--no-session-persistence",
           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
           "--disallowedTools", "Bash,Edit,Write,NotebookEdit,WebFetch,WebSearch,Task"]
    p = subprocess.run(cmd, input="\n\n".join(packet), capture_output=True, text=True, timeout=900,
                       env=child_env(j, dict(os.environ)))
    verdict = parse_judge(p.stdout)
    (runs[0].parent / "judge.json").write_text(json.dumps(
        {"verdict": verdict, "usage": _usage(p.stdout, {"cost": "claude"}), "raw": p.stdout[-4000:]},
        indent=2, ensure_ascii=False))
    return verdict


def _failure_report(run_dir: Path, meta: dict) -> str:
    err = (run_dir / "stderr.txt").read_text(errors="replace")[-1200:]
    said = final_text((run_dir / "stdout.json").read_text(errors="replace"))[-1200:]
    failed = [c for c in meta["checks"] if not c["ok"]]
    return (f"--- {meta['tier']} ({meta['model']}) FAILED: exit {meta['exit']}"
            f"{', timed out' if meta['timed_out'] else ''}\n"
            + "".join(f"check failed: {c['cmd']}\n  {c['output'].strip()}\n" for c in failed)
            + f"last words: {said.strip() or '(none)'}\nstderr tail: {err.strip() or '(none)'}\nfiles: {run_dir}\n"
            "Diagnose the cause from these files before trying again, then record it with `feedback`.\n")


def _append(name: str, row: dict) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    with (LOGS / name).open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _rows(name: str) -> list[dict]:
    f = LOGS / name
    return [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()] if f.exists() else []


# --- commands ---------------------------------------------------------------------------------------------------

def cmd_climb(a) -> None:
    t = load_tiers()
    case = json.loads(Path(a.case).expanduser().read_text(encoding="utf-8"))
    case["drive_screen"] = a.drive_screen
    guard(case, a.confirm)
    private = json.loads(Path(case["private"]).expanduser().read_text()) if case.get("private") else {}
    rungs = [tier(t, n) for n in a.tiers.split(",")] if a.tiers else ladder_rungs(t)
    base = LAB / "runs" / case["name"]
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    golden = base / "golden"
    if a.new_golden or not (golden / "meta.json").exists():
        print(f"golden: {tier(t, t['judge'])['model']}")
        if not clean(run_once(t, tier(t, t["judge"]), case, golden, private)):
            sys.exit(f"the Opus reference run itself failed; fix the case first ({golden})")
    results = {}

    def attempt(rung):
        print(f"tier {rung['id']} ({rung['model']}) x{a.runs}")
        dirs = [base / stamp / rung["id"] / f"run{i}" for i in range(1, a.runs + 1)]
        metas = []
        for d in dirs:
            metas.append(run_once(t, rung, case, d, private))
            if not clean(metas[-1]):
                print(_failure_report(d, metas[-1]))
                break   # one hard failure already fails the tier; don't spend more runs or the judge
        verdict = judge(t, case, golden, dirs, rung["id"]) if len(metas) == a.runs and all(map(clean, metas)) else None
        ok = rung_passed(metas, verdict, a.runs)
        results[rung["id"]] = {"passed": ok, "model": rung["model"], "runs": metas, "judge": verdict}
        print(f"  -> {'PASS' if ok else 'fail'}" + (f": {verdict.get('summary', '')}" if verdict else ""))
        return ok

    winner = climb(rungs, attempt)
    summary = {"case": case["name"], "skill": case.get("skill"), "mode": case.get("mode"), "when": stamp,
               "runs_per_tier": a.runs, "winner": winner or t["judge"], "rungs": results}
    (base / stamp).mkdir(parents=True, exist_ok=True)
    (base / stamp / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    _ledger(summary)
    print(f"\nwinner: {summary['winner']}" + ("" if winner else " (no cheaper tier matched)")
          + f"\nsummary: {base / stamp / 'summary.json'}")


def _ledger(s: dict) -> None:
    LAB.mkdir(parents=True, exist_ok=True)
    led = LAB / "ledger.md"
    if not led.exists():
        led.write_text("| when | case | mode | winner | tried (clean runs, avg s) |\n|---|---|---|---|---|\n")
    tried = "; ".join(f"{k}={v['model']} {'PASS' if v['passed'] else 'fail'} "
                      f"{sum(map(clean, v['runs']))}/{s['runs_per_tier']}, "
                      f"{round(sum(m['seconds'] for m in v['runs']) / max(len(v['runs']), 1))}s"
                      for k, v in s["rungs"].items())
    with led.open("a", encoding="utf-8") as f:
        f.write(f"| {s['when']} | {s['case']} | {s['mode']} | **{s['winner']}** | {tried} |\n")


def cmd_run(a) -> None:
    t = load_tiers()
    start, top = skill_route(t, a.skill)
    chain = escalation(t, a.tier or start, top, unattended=a.unattended, skip=skill_skip(t, a.skill))
    case = {"workdir": a.cwd, "allowed_tools": [x for x in (a.tools or "").split(",") if x],
            "mode": "computer-use" if a.browser else "command", "browser_profile": a.browser or "",
            "timeout_s": a.timeout, "prompt": Path(a.prompt_file).read_text(encoding="utf-8"),
            "checks": a.check or [], "rubric": a.rubric, "goal": a.goal, "drive_screen": a.drive_screen}
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    for name in chain:
        rung = tier(t, name)
        # hand-off runs live under the ladder lab: one folder the user trusts once in Antigravity IDE
        run_dir = (LAB / "handoff" if is_handoff(rung) else LOGS.parent / "runs") / a.skill / f"{stamp}_{name}"
        meta = run_once(t, rung, case, run_dir, {})
        row = {"when": stamp, "skill": a.skill, "tier": name, "model": rung["model"], "ok": clean(meta),
               "seconds": meta["seconds"], "dir": str(run_dir)}
        if not clean(meta):
            _append("runs.jsonl", row)
            print(_failure_report(run_dir, meta), file=sys.stderr)
            continue
        wins = sum(r["ok"] for r in _rows("runs.jsonl") if r["skill"] == a.skill) + 1
        if spot_check_due(wins, t.get("spot_check_every", 0)):
            v = judge(t, case, None, [run_dir], name)
            row["spot_check"] = bool(v and all(x.get("pass") for x in v.get("runs") or []))
            print(f"[spot check by {t['judge']}: {'pass' if row['spot_check'] else 'FAIL'}"
                  f"{' — ' + v.get('summary', '') if v else ''}]", file=sys.stderr)
            if not row["spot_check"]:
                _append("feedback.jsonl", {"when": stamp, "skill": a.skill, "tier": name, "verdict": "bad",
                                           "why": "spot check failed: " + ((v or {}).get("summary") or "no verdict")})
        _append("runs.jsonl", row)
        log_to_folder(a.cwd, {"when": datetime.now().strftime("%Y-%m-%d %H:%M"), "agent": f"ladder run {a.skill}",
                              "tier": name, "model": rung["model"], "did": a.goal or "delegated task",
                              "result": f"ok in {meta['seconds']}s, files {run_dir / 'out'}", "next": "-"})
        print(final_text((run_dir / "stdout.json").read_text()))
        print(f"\n[{a.skill} on {name} ({rung['model']}), {meta['seconds']}s, files: {run_dir / 'out'}]", file=sys.stderr)
        return
    sys.exit(f"{a.skill}: every tier in {chain} failed; see the reports above")


def cmd_feedback(a) -> None:
    last = next((r for r in reversed(_rows("runs.jsonl")) if r["skill"] == a.skill), {})
    _append("feedback.jsonl", {"when": datetime.now().strftime("%Y-%m-%d_%H%M%S"), "skill": a.skill,
                               "tier": last.get("tier"), "verdict": a.verdict, "why": a.why})
    print(f"noted: {a.skill} {a.verdict} (last run on {last.get('tier', '?')})")
    advice = feedback_advice(_rows("feedback.jsonl"), a.skill)
    if advice:
        print(advice)


def cmd_status(a) -> None:
    t = load_tiers()
    print(f"tier file: {TIERS_FILE}")
    for n in t["order"]:
        x = tier(t, n)
        print(f"  {n:<13} {x['runner']:<17} {x['model']}{'  (judge)' if n == t['judge'] else ''}")
    runs, fb = _rows("runs.jsonl"), _rows("feedback.jsonl")
    skills = [a.skill] if a.skill else sorted({*(t.get("skills") or {}), *(r["skill"] for r in runs)})
    for s in skills:
        start, top = skill_route(t, s)
        mine = [r for r in runs if r["skill"] == s]
        oks = sum(r["ok"] for r in mine)
        print(f"{s}: tier {start} (max {top}); runs {oks}/{len(mine)} ok"
              + "".join(f"\n  {r['when']} {r['tier']} {'ok' if r['ok'] else 'FAIL'} {r['seconds']}s" for r in mine[-5:]))
        advice = feedback_advice(fb, s)
        if advice:
            print("  ! " + advice)


def cmd_doctor(_a) -> None:
    t = load_tiers()
    ok = True
    for n in [*t["order"], *(t.get("spare") or {})]:
        x, note, have = tier(t, n), "", True
        if x["runner"] == "claude":
            have = subprocess.run(["which", "claude"], capture_output=True).returncode == 0
        elif x["runner"] == "antigravity-ide":
            have = Path(x.get("bin", "")).exists()
        if have and x.get("key"):
            try:
                key = read_env_key(x["key"]["file"], x["key"]["name"])
                served, same = probe_model(x, key)
                note = "answers as " + served + ("" if same else "  <-- NOT the configured model: fix the tier file")
                have &= same
            except SystemExit as e:
                have, note = False, str(e)
            except Exception as e:   # network / auth trouble: say it, don't crash the report
                have, note = False, f"probe failed: {type(e).__name__}: {str(e)[:120]}"
        spare = n not in t["order"]
        print(f"{'ok ' if have else ('-- ' if spare else 'NO ')} {n:<15} {x['runner']:<19} {x['model']} {note}"
              + (" (spare)" if spare else ""))
        ok &= have or spare
    print(f"tier file: {TIERS_FILE}\nlogs: {LOGS}\nladder lab: {LAB}")
    sys.exit(0 if ok else 1)


def cmd_report(a) -> None:
    latest = sorted((LAB / "runs" / a.case).glob("*/summary.json"))
    if not latest:
        sys.exit(f"no climbs for {a.case} under {LAB / 'runs'}")
    s = json.loads(latest[-1].read_text())
    print(f"{s['case']} ({s['mode']}) {s['when']}: winner {s['winner']}")
    for k, v in s["rungs"].items():
        why = "; ".join(j.get("why", "") for j in ((v.get("judge") or {}).get("runs") or []) if not j.get("pass"))
        print(f"  {k} ({v['model']}): {'PASS' if v['passed'] else 'fail'}" + (f" - {why}" if why else ""))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("climb")
    c.add_argument("case")
    c.add_argument("--runs", type=int, default=3)
    c.add_argument("--tiers", help="comma list of tiers to try instead of the whole order")
    c.add_argument("--confirm", action="store_true", help="the user agreed to the case's real side effects")
    c.add_argument("--new-golden", action="store_true", help="redo the Opus reference run")
    c.add_argument("--drive-screen", action="store_true",
                   help="the user handed over the keyboard: type hand-off prompts into Antigravity IDE")
    r = sub.add_parser("run")
    r.add_argument("--skill", required=True)
    r.add_argument("--cwd", required=True)
    r.add_argument("--prompt-file", required=True)
    r.add_argument("--tools", help="Claude-style allowed tools, comma separated")
    r.add_argument("--check", action="append", help="shell check, {out} = output folder; repeatable")
    r.add_argument("--rubric", help="what a good result is (for spot checks)")
    r.add_argument("--goal", help="one line: what the task is (log + spot check)")
    r.add_argument("--browser", help="browser profile dir: gives the agent Playwright MCP")
    r.add_argument("--tier", help="start here instead of the skill's routed tier")
    r.add_argument("--unattended", action="store_true", help="skip hand-off tiers (no one at the screen)")
    r.add_argument("--drive-screen", action="store_true",
                   help="the user handed over the keyboard: type hand-off prompts into Antigravity IDE")
    r.add_argument("--timeout", type=int, default=900)
    f = sub.add_parser("feedback")
    f.add_argument("skill")
    f.add_argument("verdict", choices=["good", "bad"])
    f.add_argument("why")
    s = sub.add_parser("status")
    s.add_argument("skill", nargs="?")
    sub.add_parser("doctor")
    p = sub.add_parser("report")
    p.add_argument("case")
    a = ap.parse_args()
    {"climb": cmd_climb, "run": cmd_run, "feedback": cmd_feedback, "status": cmd_status,
     "doctor": cmd_doctor, "report": cmd_report}[a.cmd](a)


if __name__ == "__main__":
    main()
