# Palette (the only place colors are defined)

Edit this file to re-brand every diagram. Pick a color by the **role** of the thing, never by taste.
Rule of thumb: dark stroke + light fill, same hue. Background `#ffffff`. Always `opacity: 100`.

## Roles

| Role | Use for | stroke | fill |
|---|---|---|---|
| input | start, trigger, source, user action | `#047857` | `#d1fae5` |
| process | a step, service, component | `#1d4ed8` | `#dbeafe` |
| decision | branch, condition, gate | `#b45309` | `#fef3c7` |
| ai | model, agent, automation | `#6d28d9` | `#ede9fe` |
| output | result, deliverable, end state | `#0f766e` | `#ccfbf1` |
| risk | error, warning, blocker, "do not" | `#b91c1c` | `#fee2e2` |
| neutral | storage, external system, grouping zone | `#475569` | `#f1f5f9` |

Zones (big background regions that group things): neutral fill `#f8fafc`, stroke `#cbd5e1`, `strokeStyle: "dashed"`.

## Text

| Level | color | size |
|---|---|---|
| title | `#0f172a` | 28 |
| section label | `#334155` | 20 |
| node label | matches the node's stroke color, or `#0f172a` | 16 |
| annotation / detail | `#64748b` | 14 |

## Code / data snippets (dark card)

- card: fill `#0f172a`, stroke `#1e293b`
- text: default `#e2e8f0`; keys `#7dd3fc`; strings `#86efac`; numbers/values `#fcd34d`; comments `#94a3b8`
- font: `fontFamily: 3` (monospace), size 14

## Lines

Arrows and connectors use `#334155`, width 2 (main flow: 3, hints/dividers: 1). A warning path may use the risk stroke.

---

# Icon style (same light theme) — overviews, slides, "get it at a glance"

Same background `#ffffff` and the same role colors as above: the circle uses the role's stroke + fill, and the icon
and the label under it use the role's stroke. Use when the diagram is a **story of a process** (circle icon nodes,
label underneath, one container for the core loop, part brackets below); plain boxes stay best for dense technical
diagrams.

| Element | stroke | fill / color | size |
|---|---|---|---|
| loop / system container | `#93c5fd`, width 2, roundness 3 | `#f8fafc` | — |
| part bracket | `#93c5fd`, width 2 | — | — |
| title | — | `#1d4ed8` | 36 |
| subtitle (one-line message) | — | `#334155` | 18 |
| node label under circle | — | node stroke | 20 hero / 16 |
| detail under label | — | `#475569` | 14 |
| arrow / part label | — | `#1d4ed8` (or the path's color) | 14 / 16 |

Lines `#334155` width 2; the success path (into the final step) uses the input/success green `#047857`.
Font: `fontFamily: 8` (Comic Shanns, hand-drawn monospace). Thai falls back to the system font — size for Thai width.
