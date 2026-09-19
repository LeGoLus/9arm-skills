#!/usr/bin/env python3
"""Render an .excalidraw file to PNG with headless Chromium.

    uv run python render.py diagram.excalidraw [--out diagram.png] [--scale 2] [--padding 24]

Needs network at render time: Excalidraw's export code is loaded from esm.sh, pinned
to EXCALIDRAW_VERSION (an unpinned import broke once when a transitive dependency 404'd).
Exit codes: 0 ok, 1 bad input, 2 renderer failure.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXCALIDRAW_VERSION = "0.18.0"
MODULE_URL = f"https://esm.sh/@excalidraw/excalidraw@{EXCALIDRAW_VERSION}?bundle"
LOAD_TIMEOUT_MS = 45_000
EXPORT_TIMEOUT_MS = 20_000

PAGE = """<!doctype html>
<html><head><meta charset="utf-8">
<style>html,body{margin:0;background:#fff}#stage svg{display:block}</style></head>
<body><div id="stage"></div>
<script type="module">
  const scene = %(scene)s;
  window.__status = "loading";
  try {
    const { exportToSvg } = await import("%(module)s");
    const svg = await exportToSvg({
      elements: scene.elements.filter(e => !e.isDeleted),
      appState: { ...(scene.appState || {}), exportBackground: true,
                  viewBackgroundColor: (scene.appState || {}).viewBackgroundColor || "#ffffff" },
      files: scene.files || {},
      exportPadding: %(padding)d,
    });
    document.getElementById("stage").appendChild(svg);
    await document.fonts.ready;
    window.__status = "done";
  } catch (err) {
    window.__status = "error: " + (err && err.message ? err.message : String(err));
  }
</script></body></html>
"""


def load_scene(path: Path) -> dict:
    try:
        scene = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        sys.exit(f"bad input: cannot read {path}: {err}")
    if scene.get("type") != "excalidraw" or not isinstance(scene.get("elements"), list):
        sys.exit("bad input: expected {'type': 'excalidraw', 'elements': [...]}")
    live = [e for e in scene["elements"] if not e.get("isDeleted")]
    if not live:
        sys.exit("bad input: no elements to draw")
    ids = {e.get("id") for e in live}
    problems = []
    for e in live:
        for bound in e.get("boundElements") or []:
            if bound.get("id") not in ids:
                problems.append(f"{e['id']}: boundElements -> missing {bound.get('id')}")
        for side in ("startBinding", "endBinding"):
            target = (e.get(side) or {}).get("elementId")
            if target and target not in ids:
                problems.append(f"{e['id']}: {side} -> missing {target}")
        if e.get("containerId") and e["containerId"] not in ids:
            problems.append(f"{e['id']}: containerId -> missing {e['containerId']}")
    if problems:
        sys.exit("bad input: dangling references\n  " + "\n  ".join(problems))
    return scene


def render(scene: dict, out: Path, scale: float, padding: int) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright missing: run `uv sync && uv run playwright install chromium` in scripts/")

    # "</" would end the inline <script>; escape it inside the JSON blob.
    blob = json.dumps(scene).replace("</", "<\\/")
    html = PAGE % {"scene": blob, "module": MODULE_URL, "padding": padding}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(device_scale_factor=scale)
            page.set_content(html)
            try:
                page.wait_for_function(
                    "window.__status && window.__status !== 'loading'", timeout=LOAD_TIMEOUT_MS
                )
            except Exception:
                print(f"renderer timeout: could not load {MODULE_URL} (network? esm.sh down?)", file=sys.stderr)
                sys.exit(2)
            status = page.evaluate("window.__status")
            if status != "done":
                print(f"renderer failure: {status}", file=sys.stderr)
                sys.exit(2)
            page.locator("#stage svg").screenshot(path=str(out), timeout=EXPORT_TIMEOUT_MS)
        finally:
            browser.close()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path, help=".excalidraw file")
    ap.add_argument("--out", type=Path, help="PNG path (default: next to the source)")
    ap.add_argument("--scale", type=float, default=2.0, help="pixel density (default 2)")
    ap.add_argument("--padding", type=int, default=24, help="canvas padding in px (default 24)")
    args = ap.parse_args()

    scene = load_scene(args.source)
    out = args.out or args.source.with_suffix(".png")
    out.parent.mkdir(parents=True, exist_ok=True)
    render(scene, out, args.scale, args.padding)
    print(out)


if __name__ == "__main__":
    main()
