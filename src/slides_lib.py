"""Minimal 16:9 slide renderer on top of reportlab's canvas.

Slides are described declaratively (see make_slides.py); this module only
handles layout, wrapping and drawing. Lithuanian diacritics require a TrueType
font, so Calibri/Consolas are registered from the Windows font directory.
"""

import re

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

W, H = 960, 540                      # 16:9 in points
MARGIN = 54

INK = HexColor("#16202B")
MUTED = HexColor("#5C6B7A")
ACCENT = HexColor("#1F4E79")
ACCENT_SOFT = HexColor("#E8EEF5")
RULE = HexColor("#C9D4E0")
FLAG = HexColor("#B03A2E")
FLAG_SOFT = HexColor("#FBEBE9")
GOOD = HexColor("#1E6B52")

FONTS = {
    "regular": ("LT", r"C:\Windows\Fonts\calibri.ttf"),
    "bold": ("LT-B", r"C:\Windows\Fonts\calibrib.ttf"),
    "italic": ("LT-I", r"C:\Windows\Fonts\calibrii.ttf"),
    "mono": ("LT-M", r"C:\Windows\Fonts\consola.ttf"),
}
F = {k: v[0] for k, v in FONTS.items()}


def register_fonts():
    for name, path in FONTS.values():
        pdfmetrics.registerFont(TTFont(name, path))


MARK = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)")


def plain(text):
    """Strip inline markers so the text can be measured."""
    return text.replace("**", "").replace("*", "").replace("`", "")


def wrap(text, font, size, width):
    """Greedy word wrap; returns a list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if pdfmetrics.stringWidth(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class _Null:
    """Stand-in canvas used for the measuring pass; swallows every draw call."""

    def __getattr__(self, _):
        return lambda *a, **k: None


class Deck:
    def __init__(self, path):
        register_fonts()
        self.c = rl_canvas.Canvas(path, pagesize=(W, H))
        self.n = 0

    # ---------------------------------------------------------------- chrome
    def _footer(self, tag=None):
        self.c.setFont(F["regular"], 8)
        self.c.setFillColor(MUTED)
        if tag:
            self.c.drawString(MARGIN, 24, tag)
        self.c.drawRightString(W - MARGIN, 24, str(self.n))

    def _header(self, title, kicker=None):
        y = H - MARGIN
        if kicker:
            self.c.setFont(F["bold"], 10)
            self.c.setFillColor(ACCENT)
            self.c.drawString(MARGIN, y, kicker.upper())
            y -= 20
        self.c.setFont(F["bold"], 21)
        self.c.setFillColor(INK)
        for line in wrap(title, F["bold"], 21, W - 2 * MARGIN):
            self.c.drawString(MARGIN, y - 16, line)
            y -= 27
        y -= 4
        self.c.setStrokeColor(RULE)
        self.c.setLineWidth(1)
        self.c.line(MARGIN, y, W - MARGIN, y)
        return y - 26

    # ---------------------------------------------------------------- slides
    def title_slide(self, title, subtitle, meta):
        self.n += 1
        self.c.setFillColor(ACCENT)
        self.c.rect(0, 0, 14, H, stroke=0, fill=1)

        y = H - 170
        self.c.setFont(F["bold"], 34)
        self.c.setFillColor(INK)
        for line in wrap(title, F["bold"], 34, W - 2 * MARGIN - 40):
            self.c.drawString(MARGIN + 26, y, line)
            y -= 44

        y -= 12
        self.c.setFont(F["regular"], 16)
        self.c.setFillColor(MUTED)
        for line in wrap(subtitle, F["regular"], 16, W - 2 * MARGIN - 40):
            self.c.drawString(MARGIN + 26, y, line)
            y -= 23

        y -= 26
        self.c.setStrokeColor(RULE)
        self.c.line(MARGIN + 26, y, MARGIN + 260, y)
        y -= 26
        self.c.setFont(F["regular"], 13)
        self.c.setFillColor(INK)
        for line in meta:
            self.c.drawString(MARGIN + 26, y, line)
            y -= 20
        self.c.showPage()

    def slide(self, title, blocks, kicker=None, tag=None):
        """Render one slide.

        Content is laid out twice: a measuring pass against a null canvas
        determines how much of the slide the body fills, so a short slide can be
        nudged down and sit optically centred instead of hugging the header.
        """
        self.n += 1
        top = self._header(title, kicker)

        real, self.c = self.c, _Null()
        y = top
        for block in blocks:
            y = self._draw(block, y)
        self.c = real

        # A small nudge only: a large offset leaves an obvious hole under the
        # title, which looks worse than plain top alignment.
        slack = y - 58
        offset = min(max(0.0, slack) * 0.35, 30.0)

        self._header(title, kicker)
        y = top - offset
        for block in blocks:
            y = self._draw(block, y)
        self._footer(tag)
        self.c.showPage()

    # ---------------------------------------------------------------- blocks
    def _draw(self, block, y):
        kind = block[0]
        if kind == "b":
            return self._bullet(block[1], y, size=block[2] if len(block) > 2 else 11.5)
        if kind == "sub":
            return self._bullet(block[1], y, indent=22, size=10.5, dash=True)
        if kind == "p":
            return self._para(block[1], y)
        if kind == "kv":
            return self._kv(block[1], y)
        if kind == "table":
            return self._table(block[1], block[2], y,
                               widths=block[3] if len(block) > 3 else None)
        if kind == "note":
            return self._note(block[1], block[2], y)
        if kind == "gap":
            return y - block[1]
        raise ValueError(kind)

    def _bullet(self, text, y, indent=0, size=11.5, dash=False):
        x = MARGIN + indent
        self.c.setFillColor(ACCENT if not dash else MUTED)
        self.c.setFont(F["bold"], size)
        self.c.drawString(x, y, "–" if dash else "•")
        avail = W - 2 * MARGIN - indent - 14
        lines = self._rich(text, F["regular"], size, avail)
        for i, line in enumerate(lines):
            self._draw_rich(line, x + 14, y, size)
            y -= size + 4.5
        return y - 4

    def _para(self, text, y):
        for line in self._rich(text, F["regular"], 11.5, W - 2 * MARGIN):
            self._draw_rich(line, MARGIN, y, 11.5)
            y -= 16.5
        return y - 6

    def _rich(self, text, font, size, width):
        """Wrap text containing **bold**, *italic* and `code`, keeping markers.

        Explicit newlines are honoured as forced breaks.
        """
        lines = []
        for para in str(text).split("\n"):
            words, cur = para.split(), ""
            for w in words:
                trial = f"{cur} {w}".strip()
                if pdfmetrics.stringWidth(plain(trial), font, size) <= width or not cur:
                    cur = trial
                else:
                    lines.append(cur)
                    cur = w
            lines.append(cur)
        return lines or [""]

    def _draw_rich(self, line, x, y, size, color=INK):
        self.c.setFillColor(color)
        for part in MARK.split(line):
            if not part:
                continue
            if part.startswith("**"):
                font, body = F["bold"], part[2:-2]
            elif part.startswith("`"):
                font, body = F["mono"], part[1:-1]
            elif part.startswith("*"):
                font, body = F["italic"], part[1:-1]
            else:
                font, body = F["regular"], part
            self.c.setFont(font, size)
            self.c.drawString(x, y, body)
            x += pdfmetrics.stringWidth(body, font, size)

    def _kv(self, rows, y):
        key_w = 168
        for key, val in rows:
            self.c.setFont(F["bold"], 11)
            self.c.setFillColor(ACCENT)
            self.c.drawString(MARGIN, y, key)
            lines = self._rich(val, F["regular"], 11, W - 2 * MARGIN - key_w)
            for line in lines:
                self._draw_rich(line, MARGIN + key_w, y, 11)
                y -= 15.5
            y -= 4
        return y - 4

    def _table(self, header, rows, y, widths=None):
        avail = W - 2 * MARGIN
        n = len(header)
        widths = widths or [avail / n] * n
        scale = avail / sum(widths)
        widths = [w * scale for w in widths]
        size = 9 if n <= 4 else 8.2
        pad = 6

        def row_h(cells, font):
            return max(len(self._rich(str(c), font, size, widths[i] - 2 * pad))
                       for i, c in enumerate(cells)) * (size + 3.2) + 8

        # header
        h = row_h(header, F["bold"])
        self.c.setFillColor(ACCENT)
        self.c.rect(MARGIN, y - h, avail, h, stroke=0, fill=1)
        x = MARGIN
        for i, cell in enumerate(header):
            yy = y - size - 5
            for line in self._rich(str(cell), F["bold"], size, widths[i] - 2 * pad):
                self._draw_rich(f"**{plain(line)}**", x + pad, yy, size,
                                color=HexColor("#FFFFFF"))
                yy -= size + 3.2
            x += widths[i]
        y -= h

        # body
        for r, row in enumerate(rows):
            h = row_h(row, F["regular"])
            if r % 2 == 0:
                self.c.setFillColor(ACCENT_SOFT)
                self.c.rect(MARGIN, y - h, avail, h, stroke=0, fill=1)
            x = MARGIN
            for i, cell in enumerate(row):
                yy = y - size - 5
                for line in self._rich(str(cell), F["regular"], size, widths[i] - 2 * pad):
                    self._draw_rich(line, x + pad, yy, size)
                    yy -= size + 3.2
                x += widths[i]
            y -= h
            self.c.setStrokeColor(RULE)
            self.c.setLineWidth(0.5)
            self.c.line(MARGIN, y, W - MARGIN, y)
        return y - 12

    def _note(self, label, text, y):
        size = 10.5
        avail = W - 2 * MARGIN - 20
        lines = self._rich(text, F["regular"], size, avail)
        h = len(lines) * (size + 4) + 30
        self.c.setFillColor(FLAG_SOFT)
        self.c.rect(MARGIN, y - h, W - 2 * MARGIN, h, stroke=0, fill=1)
        self.c.setFillColor(FLAG)
        self.c.rect(MARGIN, y - h, 3.5, h, stroke=0, fill=1)
        self.c.setFont(F["bold"], 9.5)
        self.c.drawString(MARGIN + 14, y - 16, label.upper())
        yy = y - 32
        for line in lines:
            self._draw_rich(line, MARGIN + 14, yy, size)
            yy -= size + 4
        return y - h - 12

    def save(self):
        self.c.save()
