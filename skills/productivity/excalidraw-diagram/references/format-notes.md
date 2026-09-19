# .excalidraw format — what you actually need to write

A file is one JSON object:

```json
{ "type": "excalidraw", "version": 2, "source": "claude", "elements": [ ... ],
  "appState": { "viewBackgroundColor": "#ffffff" }, "files": {} }
```

Use short, readable string ids (`api_box`, `arr_api_db`). `scripts/render.py` fails fast if a reference dangles.

## Fields every element carries

```json
{ "id": "…", "type": "rectangle|ellipse|diamond|text|arrow|line",
  "x": 0, "y": 0, "width": 180, "height": 80, "angle": 0,
  "strokeColor": "#1d4ed8", "backgroundColor": "#dbeafe", "fillStyle": "solid",
  "strokeWidth": 2, "strokeStyle": "solid", "roughness": 0, "opacity": 100,
  "groupIds": [], "frameId": null, "roundness": {"type": 3}, "seed": 1,
  "version": 1, "versionNonce": 1, "isDeleted": false, "boundElements": [],
  "updated": 1, "link": null, "locked": false }
```

`roughness: 0` = clean lines (default for documents); `1` = hand-drawn feel. `roundness: null` gives sharp corners
(use for diamonds). `seed` just needs to differ per element.

## Label inside a shape (two linked elements)

Shape lists the text in `boundElements: [{"type":"text","id":"api_box_t"}]`. The text element adds
`"containerId": "api_box"`, `"text"`, `"originalText"` (same string), `"fontSize": 16`, `"fontFamily": 3`,
`"textAlign": "center"`, `"verticalAlign": "middle"`, `"lineHeight": 1.25`, and is placed inside the shape's box.
Size the shape from the text: width ≈ chars × fontSize × 0.6 (Latin) or × 0.7 (Thai) + 40 padding; one line ≈
fontSize × 1.25 tall. Use `\n` for manual line breaks. Free-floating text is the same element without `containerId`.

## Arrow between two shapes

```json
{ "type": "arrow", "x": 230, "y": 100, "width": 120, "height": 0,
  "points": [[0,0],[120,0]], "startArrowhead": null, "endArrowhead": "arrow",
  "startBinding": {"elementId": "a", "focus": 0, "gap": 4},
  "endBinding":   {"elementId": "b", "focus": 0, "gap": 4}, "…": "common fields" }
```

- `x,y` is the arrow's start; `points` are offsets from it (first point is `[0,0]`).
- Bind **both ways**: the arrow has start/endBinding, and each shape lists the arrow in
  `boundElements: [{"type":"arrow","id":"arr_a_b"}]`.
- Bend a route with extra points (`[[0,0],[0,60],[120,60]]`); `width`/`height` = bounding box of the points.
- Label an arrow with a free-floating text placed next to its midpoint.

## Line / divider / timeline spine

`"type": "line"` with `points` like an arrow but no arrowheads; `strokeStyle: "dashed"` for dividers.

## Small dot marker

`ellipse`, 12×12, solid fill — use on timelines and as bullet anchors.
