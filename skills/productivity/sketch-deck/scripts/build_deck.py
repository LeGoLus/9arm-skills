#!/usr/bin/env python3
"""Build a sketch-deck HTML file from a slides.js file.

Usage:
    python build_deck.py slides.js out.html --title "Deck title"

slides.js must define `const SLIDES = [...]` and may define `const CONFIG = {...}`.
After building, the script runs a Node check (if node is installed) that:
  * verifies JS syntax,
  * renders every slide and flags NaN/undefined in the SVG output,
  * warns about elements drawn outside the 1600x900 canvas (rough check on x/y attrs),
  * warns about slides with more than 6 build steps.
"""
import argparse, html, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, '..', 'assets', 'engine.html')

CHECK_JS = r"""
const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
const kit = src.split('/* ---------- rendering')[0];
let report = [];
try {
  eval(kit + `
    for (let i = 0; i < SLIDES.length; i++) {
      const sl = SLIDES[i]; const out = [];
      seed = 1000 + i * 97;
      if (sl.n) out.push(heading(sl.n, sl.t, sl.c));
      let maxStep = -1;
      sl.draw((s, svg, e) => { out.push(svg); maxStep = Math.max(maxStep, s); });
      const all = out.join('');
      const label = 'slide ' + i + (sl.t ? ' (' + sl.t + ')' : '');
      if (/NaN|undefined/.test(all)) report.push('ERROR ' + label + ': NaN/undefined in SVG');
      if (maxStep >= sl.steps) report.push('ERROR ' + label + ': element uses step ' + maxStep + ' but steps=' + sl.steps);
      if (sl.steps > 6) report.push('WARN  ' + label + ': ' + sl.steps + ' build steps (keep <= 6)');
      const xs = [...all.matchAll(/ x="(-?[\\d.]+)"/g)].map(m => +m[1]);
      const ys = [...all.matchAll(/ y="(-?[\\d.]+)"/g)].map(m => +m[1]);
      if (xs.some(v => v < -50 || v > 1600) || ys.some(v => v < -50 || v > 900))
        report.push('WARN  ' + label + ': some x/y outside 1600x900 canvas');
    }
  `);
} catch (e) { report.push('ERROR runtime: ' + e.message); }
console.log(report.length ? report.join('\n') : 'All slides rendered cleanly.');
process.exit(report.some(r => r.startsWith('ERROR')) ? 1 : 0);
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slides')
    ap.add_argument('out')
    ap.add_argument('--title', default='Presentation')
    a = ap.parse_args()

    engine = open(ENGINE, encoding='utf-8').read()
    slides = open(a.slides, encoding='utf-8').read()
    if 'const SLIDES' not in slides:
        sys.exit('slides.js must define `const SLIDES = [...]`')
    out = engine.replace('/*__SLIDES__*/', slides).replace('__TITLE__', html.escape(a.title))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, 'w', encoding='utf-8').write(out)
    print('Wrote', a.out)

    if not shutil.which('node'):
        print('node not found: skipped validation')
        return
    script = re.search(r'<script>(.*)</script>', out, re.S).group(1)
    with tempfile.TemporaryDirectory() as d:
        js = os.path.join(d, 'deck.js'); chk = os.path.join(d, 'check.js')
        open(js, 'w', encoding='utf-8').write(script)
        open(chk, 'w', encoding='utf-8').write(CHECK_JS)
        syn = subprocess.run(['node', '--check', js], capture_output=True, text=True)
        if syn.returncode:
            print(syn.stderr); sys.exit('Syntax error in deck script')
        res = subprocess.run(['node', chk, js], capture_output=True, text=True)
        print(res.stdout.strip() or res.stderr.strip())
        if res.returncode:
            sys.exit(1)


if __name__ == '__main__':
    main()
