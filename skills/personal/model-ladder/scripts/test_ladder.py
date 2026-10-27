"""cd scripts && uv run --with pytest pytest -q test_ladder.py   (ladder.py itself is stdlib only)"""
import json

import pytest

import ladder as L

TIERS = {
    "order": ["free", "google", "claude-small", "claude-top"],
    "tiers": {
        "free": {"runner": "claude", "model": "MiniMax-M3", "base_url": "https://api.minimax.io/anthropic",
                 "key": {"file": "x.env", "name": "MINIMAX_API_KEY"}, "cost": "flat"},
        "google": {"runner": "antigravity-ide", "model": "set in the IDE", "cost": "flat"},
        "claude-small": {"runner": "claude", "model": "claude-haiku-5-5", "cost": "claude"},
        "claude-top": {"runner": "claude", "model": "claude-opus-5-5", "cost": "claude"},
    },
    "spare": {"kimi": {"runner": "claude", "model": "kimi-k3", "base_url": "https://api.moonshot.ai/anthropic"}},
    "judge": "claude-top",
    "spot_check_every": 10,
    "skills": {"finnomena-healthcheck": {"tier": "free", "max_tier": "claude-small"}},
}
FREE = {**TIERS["tiers"]["free"], "id": "free"}
SMALL = {**TIERS["tiers"]["claude-small"], "id": "claude-small"}
CASE = {"name": "c", "mode": "command", "workdir": "/w", "prompt": "do it into {out}",
        "allowed_tools": ["Bash(uv run *)", "Read"], "timeout_s": 60, "checks": ["test -s {out}/a.txt"]}


# --- central tier file -------------------------------------------------------------------------------------------

def test_tier_lookup_by_name_and_the_spare_list():
    assert L.tier(TIERS, "free")["model"] == "MiniMax-M3"
    assert L.tier(TIERS, "kimi")["model"] == "kimi-k3"
    with pytest.raises(SystemExit):
        L.tier(TIERS, "nope")


def test_a_skill_uses_its_routed_tier_or_the_cheapest():
    assert L.skill_route(TIERS, "finnomena-healthcheck") == ("free", "claude-small")
    assert L.skill_route(TIERS, "unknown-skill") == ("free", "claude-top")


def test_escalation_walks_up_the_order_and_stops_at_max():
    assert L.escalation(TIERS, "free", "claude-small") == ["free", "google", "claude-small"]
    assert L.escalation(TIERS, "google", "claude-top") == ["google", "claude-small", "claude-top"]
    assert L.escalation(TIERS, "free", "free") == ["free"]


def test_escalation_can_skip_hand_off_tiers_for_unattended_runs():
    assert L.escalation(TIERS, "free", "claude-small", unattended=True) == ["free", "claude-small"]


def test_ladder_rungs_are_the_order_below_the_judge():
    assert [r["id"] for r in L.ladder_rungs(TIERS)] == ["free", "google", "claude-small"]


# --- commands ----------------------------------------------------------------------------------------------------

def test_read_env_key_without_quotes(tmp_path):
    f = tmp_path / ".env"
    f.write_text('# c\nOTHER=1\nMINIMAX_API_KEY="sk-abc"\n')
    assert L.read_env_key(f, "MINIMAX_API_KEY") == "sk-abc"
    f.write_text("OTHER=1\n")
    with pytest.raises(SystemExit):
        L.read_env_key(f, "MINIMAX_API_KEY")


def test_child_env_drops_nested_session_vars_and_points_a_proxied_tier_at_its_endpoint():
    base = {"CLAUDECODE": "1", "CLAUDE_CODE_ENTRYPOINT": "cli", "CLAUDE_CODE_CHILD_SESSION": "1",
            "ANTHROPIC_API_KEY": "real", "PATH": "/bin"}
    env = L.child_env(FREE, base, key="sk-abc")
    assert not {"CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_CHILD_SESSION", "ANTHROPIC_API_KEY"} & set(env)
    assert env["ANTHROPIC_BASE_URL"] == "https://api.minimax.io/anthropic" and env["ANTHROPIC_AUTH_TOKEN"] == "sk-abc"
    assert env["ANTHROPIC_MODEL"] == env["ANTHROPIC_SMALL_FAST_MODEL"] == "MiniMax-M3" and env["PATH"] == "/bin"
    clean = L.child_env(SMALL, {"ANTHROPIC_BASE_URL": "http://localhost:11434", "ANTHROPIC_AUTH_TOKEN": "ollama"})
    assert "ANTHROPIC_BASE_URL" not in clean and "ANTHROPIC_AUTH_TOKEN" not in clean


def test_claude_command_uses_model_tools_and_json_without_bypassing_permissions():
    cmd = L.claude_cmd(SMALL, CASE, "PROMPT", mcp_file=None, out="/o")
    assert cmd[:3] == ["claude", "-p", "PROMPT"] and cmd[cmd.index("--model") + 1] == "claude-haiku-5-5"
    assert cmd[cmd.index("--output-format") + 1] == "stream-json" and "--verbose" in cmd
    assert cmd[cmd.index("--allowedTools") + 1] == "Bash(uv run *),Read"
    assert "--dangerously-skip-permissions" not in cmd


def test_claude_command_with_browser_adds_strict_mcp_and_its_tools():
    cmd = L.claude_cmd(FREE, {**CASE, "mode": "computer-use"}, "P", mcp_file="/o/mcp.json", out="/o")
    assert cmd[cmd.index("--mcp-config") + 1] == "/o/mcp.json" and "--strict-mcp-config" in cmd
    assert "mcp__playwright" in cmd[cmd.index("--allowedTools") + 1]


def test_hand_off_task_file_tells_any_agent_where_to_write_and_how_to_finish(tmp_path):
    text = L.task_text("Make the report.", out=str(tmp_path / "out"), done=str(tmp_path / "out" / "DONE.json"))
    assert "Make the report." in text and "DONE.json" in text and '"status"' in text
    assert "AGENTS.md" in text   # the shared-workspace rules come first


def test_ide_workspace_file_gives_the_window_a_unique_title(tmp_path):
    # window handles from `screenctl list` are positions that shift; a unique workspace name is a stable target
    ws = L.ide_workspace(tmp_path, "/w", "ladder-113429")
    assert ws.name == "ladder-113429.code-workspace"
    assert json.loads(ws.read_text())["folders"] == [{"path": "/w"}, {"path": str(tmp_path)}]
    assert L.ide_title("ladder-113429") == "ladder-113429 (Workspace)"
    assert L.ide_cmds(ws) == [["antigravity-ide", "-n", str(ws)]]


def test_fill_out_and_private_values():
    assert L.fill("x {out} {private.codes}", "/o", {"codes": "K-A,K-B"}) == "x /o K-A,K-B"
    with pytest.raises(SystemExit):
        L.fill("{private.nope}", "/o", {})


def test_redact_hides_the_key_in_saved_logs():
    assert L.redact("auth sk-abc failed", ["sk-abc", "", None]) == "auth *** failed"


def test_final_text_from_each_runner():
    assert L.final_text(json.dumps({"result": "done", "usage": {}})) == "done"
    assert L.final_text(json.dumps({"status": "done", "summary": "ok"})) == "ok"
    assert L.final_text("plain words") == "plain words"


def test_parse_judge_takes_the_json_block():
    raw = 'thinking...\n```json\n{"runs": [{"run": 1, "pass": true, "why": "same"}]}\n```'
    assert L.parse_judge(raw)["runs"][0]["pass"] is True
    assert L.parse_judge(json.dumps({"result": '{"runs": []}'})) == {"runs": []}


# --- ladder verdicts ---------------------------------------------------------------------------------------------

def run(ok=True, checks=True):
    return {"exit": 0 if ok else 1, "timed_out": False, "checks_ok": checks}


def test_rung_passes_only_with_every_run_clean_and_judged_same():
    judge = {"runs": [{"run": i, "pass": True} for i in (1, 2, 3)]}
    assert L.rung_passed([run(), run(), run()], judge, need=3)
    assert not L.rung_passed([run(), run()], judge, need=3)
    assert not L.rung_passed([run(), run(checks=False), run()], judge, need=3)
    assert not L.rung_passed([run(), run(), run()], {"runs": [{"run": 1, "pass": False}]}, need=3)
    assert not L.rung_passed([run(), run(), run()], None, need=3)


def test_climb_stops_at_the_first_rung_that_passes():
    tried = []

    def attempt(rung):
        tried.append(rung["id"])
        return rung["id"] == "google"

    assert L.climb(L.ladder_rungs(TIERS), attempt) == "google" and tried == ["free", "google"]
    assert L.climb([FREE], lambda r: False) is None


def test_side_effect_case_needs_confirm():
    with pytest.raises(SystemExit):
        L.guard({**CASE, "side_effects": "creates a report"}, confirm=False)
    L.guard({**CASE, "side_effects": "creates a report"}, confirm=True)
    L.guard(CASE, confirm=False)


# --- daily use: spot checks, feedback, shared folder log -----------------------------------------------------------

def test_spot_check_every_nth_success():
    assert [L.spot_check_due(n, 10) for n in (1, 9, 10, 11, 20)] == [False, False, True, False, True]
    assert not L.spot_check_due(10, 0)


def test_feedback_advice_after_two_bad_marks_in_the_last_ten():
    rows = [{"skill": "s", "verdict": "good"}] * 8 + [{"skill": "s", "verdict": "bad"}] * 2
    assert "re-run model-ladder" in L.feedback_advice(rows, "s")
    assert L.feedback_advice(rows[:9], "s") is None
    assert L.feedback_advice(rows, "other") is None


def test_folder_log_entry_goes_to_dot_agents_only_when_the_folder_uses_it(tmp_path):
    entry = {"when": "2026-10-27 11:00", "agent": "ladder run", "tier": "free", "model": "MiniMax-M3",
             "did": "made report", "result": "ok", "next": "-"}
    assert not L.log_to_folder(tmp_path, entry)
    (tmp_path / ".agents").mkdir()
    (tmp_path / ".agents" / "LOG.md").write_text("# Log\n")
    assert L.log_to_folder(tmp_path, entry)
    text = (tmp_path / ".agents" / "LOG.md").read_text()
    assert "MiniMax-M3" in text and "made report" in text and text.startswith("# Log\n")


def test_probe_flags_a_proxy_that_quietly_serves_another_model():
    calls = []

    def post(url, headers, body):
        calls.append((url, headers, body))
        return {"model": "MiniMax-M3.1-Flash", "type": "message"}

    served, ok = L.probe_model({**FREE, "model": "MiniMax-TYPO"}, "sk-abc", post=post)
    assert (served, ok) == ("MiniMax-M3.1-Flash", False)
    assert calls[0][0] == "https://api.minimax.io/anthropic/v1/messages" and calls[0][1]["x-api-key"] == "sk-abc"
    assert L.probe_model(FREE, "k", post=lambda u, h, b: {"model": "minimax-m3"}) == ("minimax-m3", True)


def test_screen_send_opens_the_agent_box_through_the_palette_then_pastes_and_sends():
    # Cmd+L toggles: it CLOSES the panel when the box already has focus. The palette command
    # "Open Chat with Agent" (antigravity.toggleChatFocus) only focuses, so it is safe in any state.
    steps = L.screen_steps("/s/screenctl.py", "ladder-1 (Workspace)", "Read /r/TASK.md and do it.")
    acts = [(x[2], x[-1]) for x in steps]
    assert acts == [("key", "cmd+shift+p"), ("paste", "Open Chat with Agent"), ("key", "enter"),
                    ("paste", "Read /r/TASK.md and do it."), ("key", "enter")]
    assert all(x[x.index("--title") + 1] == "ladder-1 (Workspace)" for x in steps)


def test_ide_window_names_differ_between_runs():
    assert L.ide_name() != L.ide_name()


def test_agent_started_when_a_new_conversation_folder_appears(tmp_path):
    (tmp_path / "old").mkdir()
    before = L.conversations(tmp_path)
    assert not L.agent_started(before, tmp_path)
    (tmp_path / "new-uuid").mkdir()
    assert L.agent_started(before, tmp_path)
    assert L.conversations(tmp_path / "missing") == set()


def test_a_skill_can_skip_a_tier_it_failed():
    t = {**TIERS, "order": ["free", "google", "claude-small", "claude-mid", "claude-top"],
         "tiers": {**TIERS["tiers"], "claude-mid": {"runner": "claude", "model": "claude-sonnet-5-5"}},
         "skills": {"hc": {"tier": "free", "max_tier": "claude-top", "skip": ["google"]}}}
    assert L.skill_skip(t, "hc") == ["google"] and L.skill_skip(t, "other") == []
    assert L.escalation(t, "free", "claude-top", skip=["google"]) == ["free", "claude-small", "claude-mid", "claude-top"]


def test_subagents_of_a_proxied_tier_ask_for_the_tier_model_under_every_alias():
    env = L.child_env(FREE, {"PATH": "/bin"}, key="sk-abc")
    for alias in ("OPUS", "SONNET", "HAIKU"):
        assert env[f"ANTHROPIC_DEFAULT_{alias}_MODEL"] == "MiniMax-M3"   # else MiniMax silently serves Flash
    clean = L.child_env(SMALL, {"ANTHROPIC_DEFAULT_SONNET_MODEL": "x", "PATH": "/bin"})
    assert "ANTHROPIC_DEFAULT_SONNET_MODEL" not in clean


def test_a_run_ends_at_its_result_event_even_if_background_tasks_linger():
    lines = ['{"type":"system","subtype":"init"}',
             '{"type":"assistant","message":{"model":"MiniMax-M3","content":[]}}',
             '{"type":"result","subtype":"success","result":"done.","num_turns":14}',
             '{"type":"system","subtype":"task_notification"}']
    result, seen, models = L.read_until_result(iter(lines))
    assert json.loads(result)["result"] == "done." and len(seen) == 3 and models == {"MiniMax-M3": 1}
    assert L.read_until_result(iter(lines[:2]))[0] is None             # no result: the caller treats it as a failure
