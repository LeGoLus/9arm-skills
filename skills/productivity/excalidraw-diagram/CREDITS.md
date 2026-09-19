# Credits

Inspired by **coleam00/excalidraw-diagram-skill** by Cole Medin — https://github.com/coleam00/excalidraw-diagram-skill

The idea of a skill that makes Claude draw Excalidraw diagrams, render them to PNG and iterate on what it sees comes from
that project. This skill is an independent rewrite: the instructions, palette, format notes, patterns and renderer were
written from scratch for the 9arm-skills library, and no upstream text or code is included. Excalidraw itself
(https://github.com/excalidraw/excalidraw, MIT) is loaded at render time from esm.sh.

Tune it to taste: colors in `references/palette.md`, drawing guidance in `references/patterns.md`.
