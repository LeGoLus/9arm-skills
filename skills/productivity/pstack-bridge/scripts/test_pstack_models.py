import pytest

import pstack_models as P

TIERS = {
    "order": ["free", "google", "claude-small", "claude-mid", "claude-top"],
    "tiers": {
        "free": {"runner": "claude", "model": "MiniMax-M3", "base_url": "https://api.minimax.io/anthropic"},
        "google": {"runner": "antigravity-ide", "model": "chosen in Antigravity IDE"},
        "claude-small": {"runner": "claude", "model": "claude-haiku-5-5"},
        "claude-mid": {"runner": "claude", "model": "claude-sonnet-5-5"},
        "claude-top": {"runner": "claude", "model": "claude-opus-5-5"},
    },
    "pstack": {"budget": "medium (high)",
               "roles": {"bug-fix": "claude-mid high", "judgment and prose": "claude-top high",
                         "arena runners": ["claude-top high", "claude-mid high"], "how explainer": "inherit-parent"}},
}


def test_roles_are_written_as_claude_code_model_aliases():
    text = P.render(TIERS)
    assert "# budget: medium (high)" in text
    assert "bug-fix: sonnet high" in text and "judgment and prose: opus high" in text
    assert "arena runners: opus high, sonnet high" in text
    assert "how explainer: inherit-parent" in text
    assert not text.startswith("---")                     # Claude Code rules file: no frontmatter


def test_a_role_on_a_tier_the_agent_tool_cannot_run_is_refused():
    bad = {**TIERS, "pstack": {"budget": "x", "roles": {"swarm workers": "free high"}}}
    with pytest.raises(SystemExit, match="free"):
        P.render(bad)
