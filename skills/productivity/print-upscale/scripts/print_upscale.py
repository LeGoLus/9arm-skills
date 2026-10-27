#!/usr/bin/env python3
"""Upscale a low-res image for large-format print and export two Illustrator files.

    <name>_HiRes.ai   AI-upscaled raster (Real-ESRGAN x4plus, detail-restored) on a
                      W x H cm artboard - the file to send to the printer.
    <name>_Vector.ai  full-colour vector trace (vtracer) of the same image - for editing.

Both .ai files are PDF-compatible (Illustrator opens them directly).

usage:
  print_upscale.py <image> --width-cm 100 --height-cm 140 --out <dir> [--name NAME]

Run it with the skill's venv python (see setup.sh), which has numpy, pillow,
reportlab and vtracer.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

TOOLS = os.path.expanduser(os.environ.get("PRINT_UPSCALE_HOME", "~/.local/share/print-upscale"))
ESRGAN = os.path.join(TOOLS, "realesrgan", "realesrgan-ncnn-vulkan")
ESRGAN_MODELS = os.path.join(TOOLS, "realesrgan", "models")

MM_PER_PT = 25.4 / 72
# vtracer silently drops the background layer on very large inputs (seen at 7020x9828:
# whole background came out dark grey). 4914x6880 traced correctly; stay at/below it.
TRACE_MAX_LONG_SIDE = 6880
# Vector check: mean abs difference (0-255) between the rendered vector and the raster.
# Measured on the MIYAMA poster: good traces 6.5-8.3, the broken dark-background trace 65.5.
VECTOR_DIFF_LIMIT = 12.0


# ---------- pure helpers (unit-tested) ----------

def crop_box_for_aspect(w, h, target_w, target_h):
    """Centre crop box (l, t, r, b) giving the target aspect ratio, trimming one axis only."""
    target = target_w / target_h
    if w / h > target:  # too wide -> trim sides
        new_w = round(h * target)
        l = (w - new_w) // 2
        return (l, 0, l + new_w, h)
    new_h = round(w / target)
    t = (h - new_h) // 2
    return (0, t, w, t + new_h)


def trace_size(w, h, limit=TRACE_MAX_LONG_SIDE):
    """Largest size <= limit on the long side, keeping aspect."""
    k = min(1.0, limit / max(w, h))
    return (round(w * k), round(h * k))


_PATH_RE = re.compile(
    r'<path d="([^"]+)" fill="(#[0-9A-Fa-f]{6})" transform="translate\(([-\d.]+),([-\d.]+)\)"')
_TOK_RE = re.compile(r"[MCLZ]|-?\d*\.?\d+(?:e-?\d+)?")


def parse_vtracer_svg(svg):
    """Yield (fill, tx, ty, ops) per path; ops are ('M'|'L', x, y), ('C', 6 floats), ('Z',)."""
    for m in _PATH_RE.finditer(svg):
        dstr, fill, tx, ty = m.group(1), m.group(2), float(m.group(3)), float(m.group(4))
        ts = _TOK_RE.findall(dstr)
        ops, i, cmd = [], 0, None
        while i < len(ts):
            t = ts[i]
            if t in "MCLZ":
                cmd = t
                i += 1
                if t == "Z":
                    ops.append(("Z",))
                continue
            if cmd == "M":
                ops.append(("M", float(ts[i]), float(ts[i + 1])))
                i += 2
                cmd = "L"  # implicit lineto after the first moveto pair
            elif cmd == "L":
                ops.append(("L", float(ts[i]), float(ts[i + 1])))
                i += 2
            elif cmd == "C":
                ops.append(("C", *[float(v) for v in ts[i:i + 6]]))
                i += 6
            else:
                raise ValueError(f"unexpected token {t!r} after {cmd!r}")
        yield fill, tx, ty, ops


# ---------- image steps ----------

def arr(im):
    return np.asarray(im, dtype=np.float32)


def resize_f(a, size, method):
    return np.asarray(Image.fromarray(a).resize(size, method), dtype=np.float32)


def run_esrgan(src, dst):
    if not os.access(ESRGAN, os.X_OK):
        sys.exit(f"Real-ESRGAN not found at {ESRGAN} - run setup.sh first")
    subprocess.run([ESRGAN, "-i", src, "-o", dst, "-n", "realesrgan-x4plus", "-m", ESRGAN_MODELS],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def back_project(orig, up, iters=6, sigma=0.6):
    """Nudge `up` so that box-downsampling it reproduces `orig` (restores dropped detail)."""
    o = orig.filter(ImageFilter.GaussianBlur(sigma)) if sigma > 0 else orig
    sw, sh = o.size
    W, H = up.size
    O = [arr(c) for c in o.split()]
    U = [arr(c) for c in up.split()]
    for _ in range(iters):
        for c in range(3):
            err = O[c] - resize_f(U[c], (sw, sh), Image.BOX)
            U[c] += resize_f(err, (W, H), Image.BICUBIC)
            np.clip(U[c], 0, 255, out=U[c])
    return np.stack(U, axis=-1)


def colour_fix(orig, ai, lf_sigma=2.5):
    """Low-frequency correction: give the AI image the original's colours/tones."""
    W, H = ai.size
    sw, sh = orig.size
    o_lf = arr(orig.filter(ImageFilter.GaussianBlur(lf_sigma)).resize((W, H), Image.BICUBIC))
    a_lf = arr(ai.resize((sw, sh), Image.BOX).filter(ImageFilter.GaussianBlur(lf_sigma)).resize((W, H), Image.BICUBIC))
    return arr(ai) + (o_lf - a_lf)


def edge_mask(orig, size):
    """1 on strong edges of the original (keep AI sharpness), 0 on flat/soft areas."""
    g = orig.convert("L").filter(ImageFilter.GaussianBlur(0.7))
    ex = np.abs(arr(g.filter(ImageFilter.Kernel((3, 3), [-1, 0, 1, -2, 0, 2, -1, 0, 1], 1))))
    ey = np.abs(arr(g.filter(ImageFilter.Kernel((3, 3), [-1, -2, -1, 0, 0, 0, 1, 2, 1], 1))))
    m = np.clip((np.hypot(ex, ey) - 25) / 60, 0, 1)
    mi = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
    return arr(mi.resize(size, Image.BICUBIC))[..., None] / 255.0


def to_img(a):
    return Image.fromarray(np.clip(np.round(a), 0, 255).astype(np.uint8))


# ---------- .ai writers ----------

def write_raster_ai(path, jpg, w_pt, h_pt, title):
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(path, pagesize=(w_pt, h_pt))
    c.setTitle(title)
    c.drawImage(jpg, 0, 0, w_pt, h_pt)
    c.showPage()
    c.save()


def write_vector_ai(path, svg, w_pt, h_pt, title):
    from reportlab.pdfgen import canvas
    sw = float(re.search(r'width="([\d.]+)"', svg).group(1))
    k = w_pt / sw
    c = canvas.Canvas(path, pagesize=(w_pt, h_pt))
    c.setTitle(title)
    n = 0
    for fill, tx, ty, ops in parse_vtracer_svg(svg):
        P = lambda x, y: ((x + tx) * k, h_pt - (y + ty) * k)
        p = c.beginPath()
        for op in ops:
            if op[0] == "M":
                p.moveTo(*P(op[1], op[2]))
            elif op[0] == "L":
                p.lineTo(*P(op[1], op[2]))
            elif op[0] == "C":
                p.curveTo(*P(op[1], op[2]), *P(op[3], op[4]), *P(op[5], op[6]))
            else:
                p.close()
        c.setFillColor(fill)
        c.drawPath(p, stroke=0, fill=1, fillMode=1)  # nonzero, same as SVG default
        n += 1
    c.showPage()
    c.save()
    return n


def render_pdf(pdf, out_dir, size):
    """Render page 1 of a PDF/.ai with macOS Quick Look; returns PNG path or None."""
    tmp = os.path.join(out_dir, os.path.basename(pdf) + ".pdf")
    shutil.copy(pdf, tmp)
    subprocess.run(["qlmanage", "-t", "-s", str(size), "-o", out_dir, tmp],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    png = tmp + ".png"
    return png if os.path.exists(png) else None


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--width-cm", type=float, required=True)
    ap.add_argument("--height-cm", type=float, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--name")
    a = ap.parse_args()

    name = a.name or os.path.splitext(os.path.basename(a.image))[0]
    out = os.path.abspath(a.out)
    work = os.path.join(out, "_work")
    os.makedirs(work, exist_ok=True)
    w_pt, h_pt = a.width_cm * 10 / MM_PER_PT, a.height_cm * 10 / MM_PER_PT

    orig = Image.open(a.image).convert("RGB")
    src_png = os.path.join(work, "src.png")
    orig.save(src_png)
    print(f"[1/6] source {orig.size[0]}x{orig.size[1]} px -> "
          f"{orig.size[0] / (a.width_cm / 2.54):.0f} dpi at {a.width_cm:g}x{a.height_cm:g} cm")

    up_png = os.path.join(work, "esrgan_x4.png")
    run_esrgan(src_png, up_png)
    ai = Image.open(up_png).convert("RGB")
    W, H = ai.size
    print(f"[2/6] Real-ESRGAN x4plus -> {W}x{H}")

    bp = back_project(orig, ai)
    fixed = colour_fix(orig, ai)
    m = edge_mask(orig, (W, H))
    hires = to_img(m * fixed + (1 - m) * bp)
    del bp
    print(f"[3/6] detail restore: edges from AI ({float(m.mean()):.0%} of area), rest from original")

    box = crop_box_for_aspect(W, H, a.width_cm, a.height_cm)
    hires = hires.crop(box)
    fixed_img = to_img(fixed).crop(box)
    del fixed
    trim_w = (W - (box[2] - box[0])) / W * 100
    trim_h = (H - (box[3] - box[1])) / H * 100
    dpi = hires.size[0] / (a.width_cm / 2.54)
    print(f"[4/6] crop to {a.width_cm:g}:{a.height_cm:g} (trimmed {trim_w:.1f}% width, {trim_h:.1f}% height) "
          f"-> {hires.size[0]}x{hires.size[1]} = {dpi:.0f} dpi")

    png_out = os.path.join(out, f"{name}_{hires.size[0]}x{hires.size[1]}.png")
    hires.save(png_out, dpi=(dpi, dpi))
    jpg = os.path.join(work, "hires_q95.jpg")
    hires.save(jpg, quality=95, subsampling=0, dpi=(dpi, dpi))
    size_tag = f"{a.width_cm:g}x{a.height_cm:g}cm"
    hires_ai = os.path.join(out, f"{name}_{size_tag}_HiRes.ai")
    write_raster_ai(hires_ai, jpg, w_pt, h_pt, f"{name} {size_tag} hi-res")

    import vtracer
    tw, th = trace_size(*fixed_img.size)
    vin = os.path.join(work, "trace_in.png")
    fixed_img.filter(ImageFilter.MedianFilter(5)).resize((tw, th), Image.LANCZOS).save(vin)
    svg_p = os.path.join(work, "trace.svg")
    vtracer.convert_image_to_svg_py(
        vin, svg_p, colormode="color", hierarchical="stacked", mode="spline",
        filter_speckle=6, color_precision=8, layer_difference=8, corner_threshold=60,
        length_threshold=4.0, max_iterations=10, splice_threshold=45, path_precision=1)
    vector_ai = os.path.join(out, f"{name}_{size_tag}_Vector.ai")
    n = write_vector_ai(vector_ai, open(svg_p).read(), w_pt, h_pt, f"{name} {size_tag} vector")
    print(f"[5/6] vector trace at {tw}x{th}: {n} paths")

    # self-check: render both .ai files and compare against the raster
    prev = os.path.join(out, "_preview")
    os.makedirs(prev, exist_ok=True)
    rh = render_pdf(hires_ai, prev, 1400)
    rv = render_pdf(vector_ai, prev, 1400)
    if rh and rv:
        A = arr(Image.open(rh).convert("RGB"))
        B = arr(Image.open(rv).convert("RGB").resize(Image.open(rh).size))
        diff = float(np.abs(A - B).mean())
        side = Image.new("RGB", (A.shape[1] * 2 + 10, A.shape[0]), "white")
        side.paste(Image.open(rh).convert("RGB"), (0, 0))
        side.paste(Image.open(rv).convert("RGB").resize(Image.open(rh).size), (A.shape[1] + 10, 0))
        side.save(os.path.join(prev, "hires_vs_vector.png"))
        status = "OK" if diff <= VECTOR_DIFF_LIMIT else "FAIL - vector differs from raster, inspect"
        print(f"[6/6] vector-vs-raster mean diff {diff:.1f} (limit {VECTOR_DIFF_LIMIT}) -> {status}")
    else:
        print("[6/6] could not render previews with qlmanage - inspect the .ai files manually")
    print("\nOUTPUT")
    for p in (hires_ai, vector_ai, png_out):
        print(f"  {p}  ({os.path.getsize(p) / 1e6:.1f} MB)")
    print(f"  previews: {prev}")


if __name__ == "__main__":
    main()
