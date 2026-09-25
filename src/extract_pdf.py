"""Extract the text of the paper PDF so its methodology can be checked."""

import sys

from pypdf import PdfReader

path = sys.argv[1]
lo, hi = (int(x) for x in sys.argv[2].split("-"))
reader = PdfReader(path)
for i in range(lo - 1, min(hi, len(reader.pages))):
    print(f"\n===== PAGE {i + 1} =====")
    print(reader.pages[i].extract_text())
