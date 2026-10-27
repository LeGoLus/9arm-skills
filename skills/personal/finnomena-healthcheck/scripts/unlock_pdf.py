# Unlock the user's own Finnomena PDFs: password is taken from the "_PW-<pw>.pdf" file name.
import sys, re, os
from pypdf import PdfReader, PdfWriter
for src in sys.argv[1:]:
    m = re.search(r'_PW-([^_/]+)\.pdf$', src)
    r = PdfReader(src)
    if r.is_encrypted and r.decrypt(m.group(1)) == 0:
        print("WRONG PASSWORD:", os.path.basename(src)); continue
    dst = src[:m.start()] + ".pdf"
    if os.path.exists(dst): print("exists, skipped:", os.path.basename(dst)); continue
    w = PdfWriter(); w.append(r)
    with open(dst, "wb") as f: w.write(f)
    print(f"OK {len(r.pages)} pages -> {os.path.basename(dst)}")
