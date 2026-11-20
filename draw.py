#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261119.

A one-page newspaper front page summing up Thursday 19 November 2026:
the Shenzhen summit, the ICJ genocide ruling, the GTA VI launch, the
Anthropic IPO and the Crimea bridge strike, plus a ticker of the day's
other stories. Everything is drawn with Pillow primitives (no external
assets), so the picture is fully deterministic and its text is crisp.

Run:  python3 draw.py        (writes entry.png beside this file)
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (179, 32, 44)
NAVY = (27, 42, 74)
GOLD = (176, 141, 45)
GREY = (90, 90, 86)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SERIF_I = os.path.join(FONT_DIR, "DejaVuSerif-Italic.ttf")


def font(path, size):
    if not os.path.exists(path):
        path = SERIF if "Serif" in path else SANS
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, leading, fill=INK):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def star(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flag_us(draw, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    cw, ch = w * 0.42, stripe * 4
    draw.rectangle([x, y, x + cw, y + ch], fill=(30, 50, 110))
    for r in range(3):
        for c in range(4):
            draw.ellipse([x + 4 + c * cw / 4, y + 3 + r * ch / 3,
                          x + 8 + c * cw / 4, y + 7 + r * ch / 3],
                         fill=(255, 255, 255))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.20, y + h * 0.30, h * 0.22, (255, 222, 0))
    for sx, sy in [(0.42, 0.16), (0.52, 0.28), (0.52, 0.44), (0.42, 0.54)]:
        star(draw, x + w * sx, y + h * sy, h * 0.09, (255, 222, 0))


def flag_ru(draw, x, y, w, h):
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)


def skyline(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(23, 32, 68))
    rnd = random.Random(7)
    bx = x
    while bx < x + w - 18:
        bw = rnd.randint(22, 46)
        bh = rnd.randint(int(h * 0.35), int(h * 0.92))
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(12, 18, 44))
        for wy in range(y + h - bh + 8, y + h - 6, 12):
            for wx in range(bx + 5, bx + bw - 4, 11):
                if rnd.random() < 0.45:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 214, 110))
        bx += bw + 4
    # three flags along the bottom
    fw, fh = 74, 44
    fx = x + 14
    for fn in (flag_us, flag_cn, flag_ru):
        fn(draw, fx, y + h - fh - 8, fw, fh)
        draw.rectangle([fx, y + h - fh - 8, fx + fw, y + h - 8],
                       outline=(255, 255, 255), width=2)
        fx += fw + 12


def scales(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 228, 214))
    cx, cy = x + w // 2, y + 16
    draw.line([cx, cy, cx, y + h - 26], fill=GOLD, width=5)
    draw.line([cx - 52, cy + 12, cx + 52, cy + 12], fill=GOLD, width=5)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GOLD)
    for s in (-1, 1):
        px = cx + s * 52
        draw.line([px, cy + 12, px - 24, cy + 44], fill=GOLD, width=3)
        draw.line([px, cy + 12, px + 24, cy + 44], fill=GOLD, width=3)
        draw.line([px, cy + 12, px, cy + 44], fill=GOLD, width=3)
        draw.pieslice([px - 26, cy + 38, px + 26, cy + 62], 0, 180, fill=GOLD)
    draw.rectangle([cx - 34, y + h - 26, cx + 34, y + h - 16], fill=GOLD)


def sunset(draw, x, y, w, h):
    top = (43, 16, 85)
    mid = (194, 24, 122)
    bot = (255, 123, 47)
    for i in range(h):
        t = i / max(h - 1, 1)
        if t < 0.5:
            c = tuple(int(top[k] + (mid[k] - top[k]) * t * 2) for k in range(3))
        else:
            c = tuple(int(mid[k] + (bot[k] - mid[k]) * (t - 0.5) * 2) for k in range(3))
        draw.line([x, y + i, x + w, y + i], fill=c)
    draw.ellipse([x + w - 92, y + 10, x + w - 24, y + 78], fill=(255, 226, 150))
    # palm silhouettes (kept to the edges so the VI stays clean)
    palm = (26, 8, 48)
    for px, ph, lean in [(x + 12, 70, -10), (x + w - 24, 64, 10)]:
        draw.line([px, y + h, px + lean, y + h - ph], fill=palm, width=6)
        tx, ty = px + lean, y + h - ph
        for a in range(-70, 71, 28):
            import math
            rad = math.radians(a - 90)
            ex = tx + int(30 * math.cos(rad))
            ey = ty + int(18 * math.sin(rad)) - 6
            draw.line([tx, ty, ex, ey], fill=palm, width=4)
    draw.text((x + 150, y + 8), "VI", font=font(SERIF_B, 64),
              fill=(255, 255, 255), stroke_width=2, stroke_fill=(43, 16, 85))


def chart(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    for gy in range(y + 16, y + h - 8, 22):
        draw.line([x + 8, gy, x + w - 8, gy], fill=(225, 225, 225), width=1)
    pts = [(x + 14, y + h - 34), (x + 44, y + h - 44), (x + 74, y + h - 30),
           (x + 104, y + h - 52), (x + 134, y + h - 40), (x + 164, y + h - 66),
           (x + 194, y + h - 56), (x + 224, y + h - 84), (x + 246, y + h - 96)]
    draw.line(pts, fill=(16, 133, 60), width=5, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 14, ey + 2), (ex - 2, ey + 14)], fill=(16, 133, 60))
    draw.text((x + 12, y + 8), "$83", font=font(SANS_B, 22), fill=GREY)
    draw.text((x + w - 62, y + 8), "$97", font=font(SANS_B, 22), fill=(16, 133, 60))


def bridge(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    import math
    for tx in (x + 62, x + w - 62):
        draw.rectangle([tx - 7, y + 18, tx + 7, y + h - 34], fill=(70, 90, 120))
    draw.line([x + 10, y + h - 34, x + w - 10, y + h - 34], fill=(70, 90, 120), width=6)
    for i in range(9):
        cx = x + 20 + i * (w - 40) / 8
        draw.line([x + 62, y + 22, cx, y + h - 34], fill=(120, 140, 165), width=2)
        draw.line([x + w - 62, y + 22, cx, y + h - 34], fill=(120, 140, 165), width=2)
    # blast burst on the deck
    bx, by = x + w // 2, y + h - 52
    star(draw, bx, by, 30, (255, 140, 0))
    star(draw, bx, by, 16, (255, 210, 60))
    draw.text((x + 12, y + 6), "KERCH STRAIT", font=font(SANS_B, 17), fill=(70, 90, 120))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

    # ---- masthead ----
    d.text((W // 2, 10), "THE WORLD", font=font(SERIF_B, 92),
           fill=INK, anchor="ma")
    d.line([28, 118, W - 28, 118], fill=RED, width=4)
    d.text((W // 2, 126), "THURSDAY, 19 NOVEMBER 2026",
           font=font(SANS_B, 28), fill=INK, anchor="ma")
    d.text((W // 2, 160), "THE DAY IN FULL  •  ONE PAGE",
           font=font(SANS, 18), fill=GREY, anchor="ma")
    d.line([28, 188, W - 28, 188], fill=INK, width=2)

    # ---- lead story: Shenzhen summit ----
    y = 196
    d.text((30, y), "SHENZHEN, CHINA  —  THE SUMMIT",
           font=font(SANS_B, 20), fill=RED)
    y += 28
    y = text_block(d, 30, y, "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
                   font(SERIF_B, 40), 600, 48)
    y += 6
    y = text_block(d, 30, y,
                   "First three-way summit ends with a four-point "
                   "\u201cDeclaration toward Peace\u201d.",
                   font(SERIF, 22), 600, 29)
    skyline(d, 656, 196, 338, 188)
    d.text((656, 388), "The three leaders in Shenzhen.",
           font=font(SERIF_I, 17), fill=GREY)
    d.line([28, 414, W - 28, 414], fill=INK, width=2)

    # ---- row 2: ICJ | GTA VI ----
    y0 = 426
    col_w = 470
    # ICJ, left column
    scales(d, 30, y0, col_w, 92)
    yy = y0 + 100
    d.text((30, yy), "THE HAGUE", font=font(SANS_B, 19), fill=RED)
    yy += 26
    yy = text_block(d, 30, yy, "COURT: MYANMAR COMMITTED GENOCIDE",
                    font(SERIF_B, 30), col_w, 36)
    yy += 4
    text_block(d, 30, yy, "Judges rule 9\u20136 on the Rohingya \u2014 the "
               "court's first such finding against a state.",
               font(SERIF, 18), col_w, 22)
    # GTA VI, right column
    rx = 524
    sunset(d, rx, y0, col_w, 92)
    yy = y0 + 100
    d.text((rx, yy), "VICE CITY", font=font(SANS_B, 19), fill=RED)
    yy += 26
    yy = text_block(d, rx, yy, "GTA VI IS OUT, SCORES 99",
                    font(SERIF_B, 30), col_w, 36)
    yy += 4
    text_block(d, rx, yy, "Rockstar's epic launches at midnight to "
               "near-perfect reviews.",
               font(SERIF, 18), col_w, 22)
    d.line([28, 678, W - 28, 678], fill=INK, width=2)

    # ---- row 3: Anthropic | Crimea bridge ----
    y0 = 690
    chart(d, 30, y0, col_w, 92)
    yy = y0 + 100
    d.text((30, yy), "WALL STREET", font=font(SANS_B, 19), fill=RED)
    yy += 26
    yy = text_block(d, 30, yy, "ANTHROPIC SOARS ON $83 DEBUT",
                    font(SERIF_B, 30), col_w, 36)
    yy += 4
    text_block(d, 30, yy, "Shares close near $97; the AI maker is "
               "valued at $1.5 trillion.",
               font(SERIF, 18), col_w, 22)
    bridge(d, rx, y0, col_w, 92)
    yy = y0 + 100
    d.text((rx, yy), "UKRAINE", font=font(SANS_B, 19), fill=RED)
    yy += 26
    yy = text_block(d, rx, yy, "KYIV HITS CRIMEA BRIDGE AGAIN",
                    font(SERIF_B, 30), col_w, 36)
    yy += 4
    text_block(d, rx, yy, "Third strike in four days; Moscow vows a "
               "harsh reply.",
               font(SERIF, 18), col_w, 22)

    # ---- ticker ----
    d.rectangle([28, 944, W - 28, 1006], fill=NAVY)
    d.text((W // 2, 952), "MARKETS SLIDE:  S&P \u22122%  •  NIKKEI \u22124.8%",
           font=font(SANS_B, 21), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 980),
           "BANGLADESH IN TURMOIL  •  COP31 TALKS STALL  •  KENYA'S LAST EBOLA PATIENT GOES HOME",
           font=font(SANS_B, 17), fill=(255, 255, 255), anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
