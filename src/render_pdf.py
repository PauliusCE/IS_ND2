"""Render a PDF to PNG pages so the layout can be inspected visually."""

import sys
from pathlib import Path

import pymupdf

pdf = Path(sys.argv[1])
out = Path(sys.argv[2]) if len(sys.argv) > 2 else pdf.parent / "_preview"
out.mkdir(exist_ok=True)
for f in out.glob("*.png"):
    f.unlink()

doc = pymupdf.open(pdf)
for i, page in enumerate(doc, start=1):
    page.get_pixmap(dpi=96).save(out / f"p{i:02d}.png")
print(f"{len(doc)} pages -> {out}")
