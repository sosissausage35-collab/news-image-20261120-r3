#!/usr/bin/env python3
"""Friday 20 November 2026 -- the world in one picture.

Draws a 1024x1024 news poster with PIL only (stdlib + Pillow, no network).
Visual-first: one huge cyclone hero, six story cards with big vector icons,
and a one-line footer ticker. Fully deterministic: fixed fonts, fixed colours,
no randomness, no clock, no network -- two runs produce byte-identical PNGs.

Usage:
    MAKEFUN_OUTPUT_DIR=/output python3 main.py   # writes /output/entry.png
    python3 main.py                              # writes ./entry.png
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette: bold dark news-magazine cover, one accent per story ----
INK = (11, 16, 38)        # deep night blue background
INK2 = (16, 24, 54)       # panel blue
PAPER = (255, 255, 255)
MUTE = (178, 190, 214)    # muted blue-grey text
RED = (232, 48, 48)
YELLOW = (255, 196, 0)
CYAN = (64, 224, 224)
TEAL = (18, 92, 110)
TEAL2 = (10, 60, 78)
ORANGE = (255, 122, 26)
GREEN = (58, 214, 132)
MAGENTA = (255, 92, 168)
VIOLET = (150, 110, 255)
CARD_BG = (22, 32, 66)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def text_fit(draw, text, size, max_w, bold=True, min_size=14):
    """Largest font size (<= size) that fits text within max_w pixels."""
    s = size
    while s > min_size:
        f = font(s, bold)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 2
    return font(min_size, bold)


def centre(draw, cx, y, text, size, fill, bold=True, max_w=None):
    """Draw text centred on cx at y; shrink to max_w if given."""
    f = font(size, bold)
    if max_w is not None:
        f = text_fit(draw, text, size, max_w, bold)
    w = draw.textlength(text, font=f)
    draw.text((cx - w / 2, y), text, font=f, fill=fill)
    return f


def left(draw, x, y, text, size, fill, bold=True, max_w=None):
    f = font(size, bold)
    if max_w is not None:
        f = text_fit(draw, text, size, max_w, bold)
    draw.text((x, y), text, font=f, fill=fill)
    return f


def draw_spiral(draw, cx, cy, colour, width=14):
    """A cyclone: concentric broken arcs whose gaps rotate, plus a calm eye."""
    for i, r in enumerate(range(28, 208, 26)):
        start = (i * 67) % 360
        end = start + 235
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, end,
                 fill=colour, width=width)
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=INK2,
                 outline=colour, width=5)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=colour)


def draw_header(draw):
    """Masthead: the day, huge, plus a red rule and a one-line kicker."""
    draw.rectangle([0, 0, W, 148], fill=(8, 10, 26))
    draw.rectangle([0, 0, 14, 148], fill=RED)
    centre(draw, W // 2 + 7, 18, "FRIDAY 20 NOVEMBER 2026", 62, PAPER,
           max_w=950)
    centre(draw, W // 2 + 7, 96, "T H E   W O R L D   T O D A Y", 26,
           YELLOW, max_w=950)
    draw.rectangle([0, 148, W, 156], fill=RED)


def draw_hero(draw):
    """Hero panel: Cyclone Akvan. Giant spiral on the right, the big number
    on the left -- readable even at thumbnail size."""
    y0, y1 = 156, 566
    # sea bands: flat horizontal strips, darker at the bottom
    bands = [TEAL, (16, 84, 102), (14, 76, 94), (12, 68, 86), TEAL2]
    bh = (y1 - y0) // len(bands)
    for i, col in enumerate(bands):
        draw.rectangle([0, y0 + i * bh, W, y0 + (i + 1) * bh], fill=col)
    draw.rectangle([0, y0 + len(bands) * bh, W, y1], fill=TEAL2)
    # rain streaks, kept clear of the hero copy (right side only)
    for x in range(620, 1010, 52):
        draw.line([x, y0 + 200, x - 18, y0 + 252], fill=(120, 200, 210),
                  width=4)
    # the cyclone itself, dominating the right half
    draw_spiral(draw, 800, 362, CYAN, width=15)
    draw_spiral(draw, 800, 362, (255, 255, 255), width=5)
    # hero copy on the left
    left(draw, 34, 186, "CYCLONE", 64, PAPER, max_w=430)
    left(draw, 34, 258, "AKVAN", 64, PAPER, max_w=430)
    left(draw, 34, 336, "300,000", 96, YELLOW, max_w=470)
    left(draw, 34, 446, "EVACUATED", 52, PAPER, max_w=470)
    left(draw, 34, 506, "IN INDIA  •  ODISHA LANDFALL", 25, MUTE,
         max_w=470)


def draw_missile(draw, x, y, col):
    """Horizontal missile with a flame tail, pointing right."""
    draw.polygon([(x, y + 22), (x - 12, y + 14), (x - 6, y + 26),
                  (x - 12, y + 38), (x, y + 30)], fill=ORANGE)
    draw.rectangle([x, y + 16, x + 48, y + 36], fill=col)
    draw.polygon([(x + 48, y + 16), (x + 68, y + 26), (x + 48, y + 36)],
                 fill=col)
    draw.polygon([(x + 2, y + 16), (x + 12, y + 4), (x + 20, y + 16)],
                 fill=col)
    draw.polygon([(x + 2, y + 36), (x + 12, y + 48), (x + 20, y + 36)],
                 fill=col)
    for dy in (-14, 0, 14):
        draw.line([x - 16, y + 26 + dy, x - 24, y + 26 + dy],
                  fill=col, width=3)


def draw_drone(draw, x, y, col):
    """Quadcopter seen from above: body, four arms, four rotors."""
    for rx, ry in ((x, y), (x + 52, y), (x, y + 44), (x + 52, y + 44)):
        draw.line([x + 32, y + 28, rx + 6, ry + 6], fill=col, width=5)
        draw.line([rx - 8, ry + 6, rx + 20, ry + 6], fill=col, width=5)
        draw.ellipse([rx, ry, rx + 12, ry + 12], fill=col)
    draw.ellipse([x + 16, y + 14, x + 48, y + 42], fill=col)
    draw.ellipse([x + 26, y + 22, x + 38, y + 34], fill=INK)


def draw_tower(draw, x, y, col):
    """A landmark tower with a blast burst at its crown."""
    draw.polygon([(x + 26, y), (x + 32, y + 14), (x + 38, y)], fill=col)
    draw.rectangle([x + 20, y + 14, x + 44, y + 58], fill=col)
    for wy in (22, 32, 42):
        draw.rectangle([x + 26, y + wy, x + 38, y + wy + 4], fill=INK)
    for ang in range(0, 360, 45):
        import math
        r1, r2 = 8, 20
        a = math.radians(ang)
        x1, y1 = x + 56 + r1 * math.cos(a), y + 8 + r1 * math.sin(a)
        x2, y2 = x + 56 + r2 * math.cos(a), y + 8 + r2 * math.sin(a)
        draw.line([x1, y1, x2, y2], fill=YELLOW, width=4)
    draw.ellipse([x + 50, y + 2, x + 62, y + 14], fill=YELLOW)


def draw_tanker(draw, x, y, col):
    """A tanker hull with flames above it."""
    draw.polygon([(x + 18, y + 8), (x + 28, y + 26), (x + 38, y + 8)],
                 fill=YELLOW)
    draw.polygon([(x + 34, y + 4), (x + 44, y + 26), (x + 54, y + 4)],
                 fill=ORANGE)
    draw.polygon([(x, y + 30), (x + 8, y + 54), (x + 62, y + 54),
                  (x + 70, y + 30)], fill=col)
    draw.rectangle([x + 40, y + 16, x + 52, y + 30], fill=col)
    draw.line([x - 6, y + 58, x + 76, y + 58], fill=CYAN, width=4)


def draw_chart(draw, x, y, col):
    """Rising bars with an arrow: a stock-market debut."""
    for i, h in enumerate((18, 32, 48)):
        draw.rectangle([x + i * 20, y + 52 - h, x + i * 20 + 13, y + 52],
                       fill=col)
    draw.line([x - 2, y + 52, x + 66, y + 2], fill=YELLOW, width=5)
    draw.polygon([(x + 66, y + 2), (x + 50, y + 2), (x + 66, y + 18)],
                 fill=YELLOW)


def draw_pad(draw, x, y, col):
    """A game controller: body, d-pad cross, two buttons."""
    draw.rounded_rectangle([x, y + 10, x + 70, y + 50], radius=14, fill=col)
    draw.rectangle([x + 14, y + 22, x + 26, y + 38], fill=INK)
    draw.rectangle([x + 8, y + 28, x + 32, y + 32], fill=INK)
    draw.ellipse([x + 44, y + 20, x + 54, y + 30], fill=YELLOW)
    draw.ellipse([x + 56, y + 28, x + 66, y + 38], fill=YELLOW)


CARDS = [
    # (title line 1, title line 2, big line, accent, icon function)
    ("KYIV", "HIT", "4 MISSILES", RED, draw_missile),
    ("DRONES SHUT", "GENOA", "4 HOURS", ORANGE, draw_drone),
    ("HOUTHI HIT", "RIYADH", "4 TARGETS", MAGENTA, draw_tower),
    ("TANKER", "BURNS", "HORMUZ MINE", YELLOW, draw_tanker),
    ("ANTHROPIC", "DEBUTS", "+17%", GREEN, draw_chart),
    ("GTA 6 BEATS", "ODYSSEY", "$1.8 BILLION", VIOLET, draw_pad),
]


def draw_cards(draw):
    """Six story cards, 2 rows x 3 columns. One big icon, a 2-line title
    and one big number per card -- nothing small enough to vanish at 300px."""
    x0, y0 = 24, 580
    cw, chh, gap = 316, 168, 14
    for i, (t1, t2, big, accent, icon) in enumerate(CARDS):
        cx = x0 + (i % 3) * (cw + gap)
        cy = y0 + (i // 3) * (chh + gap)
        draw.rounded_rectangle([cx, cy, cx + cw, cy + chh], radius=16,
                               fill=CARD_BG)
        draw.rectangle([cx, cy, cx + cw, cy + 8], fill=accent)
        icon(draw, cx + 30, cy + 26, accent)
        left(draw, cx + 104, cy + 22, t1, 27, PAPER, max_w=196)
        left(draw, cx + 104, cy + 54, t2, 27, PAPER, max_w=196)
        left(draw, cx + 18, cy + 112, big, 38, accent, max_w=280)


def draw_footer(draw):
    """One-line ticker of the day's other big stories, two short lines."""
    draw.rectangle([0, 944, W, H], fill=(120, 16, 16))
    centre(draw, W // 2, 952, "ALSO TODAY:  KOREA EXPORTS TOP $1 TRILLION",
           25, YELLOW, max_w=980)
    centre(draw, W // 2, 984, "TAIWAN CALMS MARKETS  •  EUROPE READY FOR RUSSIA TALKS",
           25, PAPER, max_w=980)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "."
    img = Image.new("RGB", (W, H), INK)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_hero(draw)
    draw_cards(draw)
    draw_footer(draw)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    print("wrote", path)


if __name__ == "__main__":
    main()
