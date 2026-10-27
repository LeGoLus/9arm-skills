---
name: print-upscale
description: Make a low-resolution image sharp enough for large-format print (posters, banners, vinyl, signage, e.g. 100x140 cm) and deliver it as two Adobe Illustrator files - <name>_HiRes.ai (AI-upscaled raster that keeps the original's details, the file for the printer) and <name>_Vector.ai (full-colour vector trace for editing). Use whenever the user says "ภาพแตก", "ทำให้ชัด", "ขยายภาพ", "ทำให้ชัดระดับ 4K", "upscale", "เอาไปพิมพ์ขนาดใหญ่", "ขอไฟล์ .ai", "ทำเป็นเวกเตอร์", or sends an image with a print size in cm, even if they don't say upscale.
---

# Print Upscale

Turns a small image (a phone/AI-generated poster, a JPEG off LINE) into print files at a
given size in cm. One command does the whole pipeline; your job is to set up once, run it,
**inspect the result yourself**, and only then deliver.

Tools live in `~/.local/share/print-upscale/` (Real-ESRGAN macOS build + a venv with
vtracer, numpy, pillow, reportlab). Scripts are in `scripts/` next to this file.

## Workflow

1. **Get the size.** Print size in cm (width x height) is required. If the user only says
   "ขนาดใหญ่", ask for it. Note the source resolution: `sips -g pixelWidth -g pixelHeight <img>`.
2. **Setup (once).** If `~/.local/share/print-upscale/venv/bin/python` is missing, tell the
   user it downloads Real-ESRGAN (~52 MB, github.com/xinntao/Real-ESRGAN) and 4 PyPI
   packages, get a yes, then run `bash scripts/setup.sh`.
3. **Run:**
   ```bash
   ~/.local/share/print-upscale/venv/bin/python scripts/print_upscale.py <image> \
     --width-cm 100 --height-cm 140 --out <out-dir> --name <CLIENT_SUBJECT>
   ```
   ~2 min for a 1755x2481 source. Output: `<name>_<W>x<H>cm_HiRes.ai`, `_Vector.ai`,
   a full-res PNG, and `_preview/` renders. Read the 6 progress lines - they report the
   source dpi, crop trim and final dpi you will quote to the user.
4. **Self-check - never skip.** Step [6/6] must say `OK` (vector-vs-raster diff under 12).
   Then look with your own eyes (the Read tool on PNGs):
   - `_preview/hires_vs_vector.png` - whole page, both files side by side.
   - Zoomed crops of the **smallest text** (logo sub-lines), **Thai text** (tone marks,
     สระบน/ล่าง), **faces/eyes**, and **soft background**. Crop from
     `<out>/<name>_<px>.png` for the raster; for the vector, render the .ai larger
     (`qlmanage -t -s 6000`) or render `_work/trace.svg` in headless Chrome with a
     `viewBox` zoom.
   - Compare against the source upscaled with plain LANCZOS, so you are judging what the
     AI changed, not just sharpness.
   Anything wrong -> fix and re-run before sending. Do not send a file you have not looked at.
5. **Deliver** with SendUserFile (`display: attach`) and say plainly: final dpi at print
   size, how much was trimmed to fit the aspect ratio, colour mode (RGB) and bleed (none),
   and that HiRes.ai is the one to print while Vector.ai is for editing.

## What the pipeline does (and why)

| Step | Why it's there |
|------|----------------|
| Real-ESRGAN **x4plus** (not x4plus-anime) | Both kept Thai glyphs intact; anime model adds bright halos round letters. |
| Detail restore: AI pixels only on strong edges, back-projected original elsewhere, plus low-frequency colour correction | Plain AI upscaling "redraws" details: it flattened a logo's blue gradient to navy, whitened skin/eyes, erased a faded background skyline, and invented scratches. Customers notice. Full back-projection alone brings back blur and ringing, so it's only used off-edge. |
| Centre crop to the print aspect | A-series art at 100x140 trims ~1% height. If the trim is large (>3%), stop and ask: crop, or pad with a background colour. |
| Vector trace at <= 6880 px long side, median-filtered colour-fixed input, `filter_speckle=6` | vtracer silently loses the background (page turns dark grey) on 7020x9828 input. Too-high `filter_speckle` deletes the dots on "i". 0.7x of the 4x size gave the smoothest outlines. |
| `.ai` = PDF-compatible file via reportlab, nonzero fill | Illustrator opens it directly; nonzero matches the SVG's fill rule. |
| Self-check diff | Catches the broken-trace failure automatically (measured: good 6.5-8.3, broken 65.5). |

## Limits to tell the user

- **Vector.ai is an auto-trace.** Up close, shading turns into colour steps and some edges
  are a little rough. A truly clean vector needs a designer to redraw it in Illustrator.
- Output is **RGB, no bleed**. If the printer asks for CMYK or 3-5 mm bleed, do it as a
  follow-up (macOS has `/System/Library/ColorSync/Profiles/Generic CMYK Profile.icc`;
  ask the printer for their profile if they have one).
- If the user says details still differ, ask *where*, crop that spot (source vs output),
  and fix it locally. Don't re-tune the whole pipeline blind.
- No Illustrator on this Mac, so .ai files are checked via Quick Look renders only. Say so.
