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

import icons

EXCALIDRAW_VERSION = "0.18.0"
MODULE_URL = f"https://esm.sh/@excalidraw/excalidraw@{EXCALIDRAW_VERSION}?bundle"
LOAD_TIMEOUT_MS = 45_000
EXPORT_TIMEOUT_MS = 20_000

PAGE = """<!doctype html>
<html><head><meta charset="utf-8">
<style>html,body{margin:0;background:transparent}#stage svg{display:block}</style></head>
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


def _segment_hits_box(p, q, box) -> bool:
    """Liang-Barsky: does segment p-q pass through the rectangle (x0, y0, x1, y1)?"""
    (x0, y0, x1, y1), (px, py), (dx, dy) = box, p, (q[0] - p[0], q[1] - p[1])
    lo, hi = 0.0, 1.0
    for d, near, far in ((dx, x0 - px, x1 - px), (dy, y0 - py, y1 - py)):
        if d == 0:
            if near > 0 or far < 0:
                return False
            continue
        a, b = sorted((near / d, far / d))
        lo, hi = max(lo, a), min(hi, b)
        if lo > hi:
            return False
    return True


def lines_over_text(scene: dict, pad: float = 4) -> list[str]:
    """Arrows/lines that cross a text element they do not own (labels must sit beside the line)."""
    live = [e for e in scene["elements"] if not e.get("isDeleted")]
    texts = [e for e in live if e["type"] == "text"]
    found = []
    for ln in (e for e in live if e["type"] in ("arrow", "line")):
        pts = [(ln["x"] + x, ln["y"] + y) for x, y in ln.get("points") or []]
        for t in texts:
            if t.get("containerId") == ln["id"]:
                continue
            box = (t["x"] - pad, t["y"] - pad, t["x"] + t["width"] + pad, t["y"] + t["height"] + pad)
            if any(_segment_hits_box(a, b, box) for a, b in zip(pts, pts[1:])):
                found.append(f"{ln['id']} crosses text {t['id']} ({t.get('text', '')[:24]!r})")
    return found


def text_over_borders(scene: dict, pad: float = 2) -> list[str]:
    """Text that straddles the edge of a box, circle or zone (partly inside, partly outside).
    Text must sit fully inside a shape or fully outside it; labels between two zones go in the gap."""
    live = [e for e in scene["elements"] if not e.get("isDeleted")]
    shapes = [e for e in live if e["type"] in ("rectangle", "ellipse", "diamond")]
    found = []
    for t in (e for e in live if e["type"] == "text"):
        tx0, ty0 = t["x"] + pad, t["y"] + pad
        tx1, ty1 = t["x"] + t["width"] - pad, t["y"] + t["height"] - pad
        for s in shapes:
            if t.get("containerId") == s["id"]:
                continue
            sx0, sy0, sx1, sy1 = s["x"], s["y"], s["x"] + s["width"], s["y"] + s["height"]
            overlaps = tx0 < sx1 and tx1 > sx0 and ty0 < sy1 and ty1 > sy0
            inside = tx0 >= sx0 and tx1 <= sx1 and ty0 >= sy0 and ty1 <= sy1
            if overlaps and not inside:
                found.append(f"text {t['id']} ({t.get('text', '')[:24]!r}) crosses the edge of {s['id']}")
    return found


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
    ap.add_argument("--strict", action="store_true", help="exit 1 when a line crosses text or text crosses a box edge")
    args = ap.parse_args()

    scene = icons.apply(load_scene(args.source))
    overlaps = lines_over_text(scene) + text_over_borders(scene)
    for msg in overlaps:
        print(f"warning: {msg}", file=sys.stderr)
    if overlaps and args.strict:
        sys.exit("bad layout: move the line or the text (or widen the gap between boxes), then render again")
    out = args.out or args.source.with_suffix(".png")
    out.parent.mkdir(parents=True, exist_ok=True)
    render(scene, out, args.scale, args.padding)
    print(out)


if __name__ == "__main__":
    main()
