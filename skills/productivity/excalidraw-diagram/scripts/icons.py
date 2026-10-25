#!/usr/bin/env python3
"""Put a Lucide icon inside every shape that asks for one.

    uv run python icons.py diagram.excalidraw        # writes the icons into the file
    uv run python icons.py --list                    # icon names you can use

A shape asks for an icon with `"customData": {"icon": "rocket"}`. The icon is drawn in the
shape's strokeColor, centred, at 50% of the shape's smaller side (override with
`"iconScale": 0.4` in customData). Re-running replaces the icons it added before, so edit the
shape, then run this again. render.py applies the same step in memory, so the PNG always has them.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from pathlib import Path

ICON_DIR = Path(__file__).resolve().parent.parent / "assets" / "icons"
SUFFIX = "__icon"


def icon_names() -> list[str]:
    return sorted(p.stem for p in ICON_DIR.glob("*.svg"))


def svg_data_url(name: str, color: str) -> str:
    path = ICON_DIR / f"{name}.svg"
    if not path.exists():
        sys.exit(f"bad input: unknown icon '{name}' (see icons.py --list)")
    svg = path.read_text(encoding="utf-8")
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
    svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def apply(scene: dict) -> dict:
    """Return the scene with one image element per icon request (idempotent)."""
    elements = [e for e in scene["elements"] if not e.get("id", "").endswith(SUFFIX)]
    files = {k: v for k, v in (scene.get("files") or {}).items() if not k.startswith("icon-")}
    out = []
    for e in elements:
        out.append(e)
        req = (e.get("customData") or {})
        name = req.get("icon")
        if not name or e.get("isDeleted"):
            continue
        color = e.get("strokeColor", "#1e1e1e")
        file_id = f"icon-{name}-{color.lstrip('#')}"
        files[file_id] = {"mimeType": "image/svg+xml", "id": file_id,
                          "dataURL": svg_data_url(name, color), "created": 1}
        size = min(e["width"], e["height"]) * float(req.get("iconScale", 0.5))
        out.append({
            "id": e["id"] + SUFFIX, "type": "image", "fileId": file_id, "status": "saved",
            "x": e["x"] + (e["width"] - size) / 2, "y": e["y"] + (e["height"] - size) / 2,
            "width": size, "height": size, "angle": 0, "scale": [1, 1], "crop": None,
            "strokeColor": "transparent", "backgroundColor": "transparent", "fillStyle": "solid",
            "strokeWidth": 1, "strokeStyle": "solid", "roughness": 0, "opacity": 100,
            "groupIds": e.get("groupIds", []), "frameId": None, "roundness": None,
            "seed": 1, "version": 1, "versionNonce": 1, "isDeleted": False,
            "boundElements": [], "updated": 1, "link": None, "locked": False,
        })
    return {**scene, "elements": out, "files": files}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path, nargs="?")
    ap.add_argument("--list", action="store_true", help="print available icon names")
    args = ap.parse_args()
    if args.list or not args.source:
        print(" ".join(icon_names()))
        return
    scene = json.loads(args.source.read_text(encoding="utf-8"))
    args.source.write_text(json.dumps(apply(scene), ensure_ascii=False, indent=1), encoding="utf-8")
    print(args.source)


if __name__ == "__main__":
    main()
