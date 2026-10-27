#!/usr/bin/env python3
"""Write pstack's per-role model rule for Claude Code from the one tier file.

pstack reads ~/.claude/rules/pstack-models.md (one `role: model effort` line per role). Our models are named only in
~/.agents/tiers.json, so its "pstack" section names a TIER per role and this script turns tiers into the aliases the
Agent tool accepts (opus / sonnet / haiku). A role on a tier the Agent tool cannot run (MiniMax, Antigravity) is
refused: send that work through model-ladder instead.

  python3 pstack_models.py            # write ~/.claude/rules/pstack-models.md
  python3 pstack_models.py --print    # show it, write nothing
"""

import json
import os
import sys
from pathlib import Path

TIERS_FILE = Path(os.environ.get("AGENT_TIERS", Path.home() / ".agents" / "tiers.json"))
RULE = Path.home() / ".claude" / "rules" / "pstack-models.md"
ALIASES = {"haiku": "haiku", "sonnet": "sonnet", "opus": "opus", "fable": "fable"}
PASSTHROUGH = {"inherit-parent", "auto"}


def alias(t: dict, value: str) -> str:
    if value in PASSTHROUGH:
        return value
    name, _, effort = value.partition(" ")
    found = t["tiers"].get(name)
    if not found:
        sys.exit(f"pstack role uses unknown tier {name!r}")
    model = found["model"]
    family = next((a for k, a in ALIASES.items() if f"claude-{k}" in model), None)
    if found.get("runner") != "claude" or found.get("base_url") or not family:
        sys.exit(f"tier {name!r} ({model}) cannot run as a Claude Code subagent; use model-ladder for it")
    return f"{family} {effort}".strip()


def render(t: dict) -> str:
    p = t.get("pstack") or {}
    lines = ["# pstack model configuration, generated from ~/.agents/tiers.json by",
             "# ~/9arm-skills/skills/productivity/pstack-bridge/scripts/pstack_models.py. Edit the tier file, not this.",
             "# `inherit-parent` or `auto`: the role runs on the parent chat model (omit Agent `model`).",
             f"# budget: {p.get('budget', 'large (xhigh)')}"]
    for role, value in (p.get("roles") or {}).items():
        vals = value if isinstance(value, list) else [value]
        lines.append(f"{role}: {', '.join(alias(t, v) for v in vals)}")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> None:
    text = render(json.loads(TIERS_FILE.read_text(encoding="utf-8")))
    if "--print" in argv:
        print(text, end="")
        return
    RULE.parent.mkdir(parents=True, exist_ok=True)
    RULE.write_text(text, encoding="utf-8")
    print(f"wrote {RULE} (applies to new sessions)")


if __name__ == "__main__":
    main(sys.argv[1:])
