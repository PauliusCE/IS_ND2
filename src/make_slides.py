"""Render the review deck to REFERATAS.pdf."""

from pathlib import Path

from slides_content import build
from slides_lib import Deck

OUT = Path(__file__).resolve().parent.parent / "REFERATAS.pdf"


def main():
    d = Deck(str(OUT))
    build(d)
    d.save()
    print(f"wrote {OUT}  ({d.n} slides)")


if __name__ == "__main__":
    main()
