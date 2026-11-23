#!/usr/bin/env python3
"""Draw the front page summing up Monday 23 November 2026.

A 1024x1024 newspaper front page drawn with PIL from the stories
reported on that day. Deterministic: no clock, no network, no
randomness, no downloaded pictures. Running it twice writes the
same bytes.

Run:  python3 draw_news.py        (writes entry.png next to this file)
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
EDGE_MARGIN = 34
GAP = 16
FONTS = "/usr/share/fonts/truetype/noto/"

NEWS = (248, 244, 236)      # newsprint
PAPER_CARD = (255, 253, 248)
INK = (20, 20, 20)
GREY = (74, 72, 66)
PALE = (140, 134, 122)
LINE = (202, 195, 180)
CRIMSON = (176, 38, 30)
FOREST = (44, 108, 66)
INDIGO = (36, 64, 128)
OCHRE = (178, 122, 20)
RUST = (196, 92, 24)
PLUM = (96, 70, 150)
SLATE = (38, 62, 90)
TEAL = (22, 104, 108)

TAGS = {
    "CLIMATE": FOREST,
    "WAR": CRIMSON,
    "CONFLICT": RUST,
    "POLITICS": INDIGO,
    "DISASTER": CRIMSON,
    "SCIENCE": TEAL,
    "TECH": PLUM,
    "ASIA": SLATE,
}


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


F_TITLE = font("NotoSans-ExtraBold.ttf", 54)
F_DATE = font("NotoSans-Bold.ttf", 23)
F_SUB = font("NotoSans-Bold.ttf", 20)
F_LEAD_HEAD = font("NotoSans-ExtraBold.ttf", 38)
F_HEAD = font("NotoSans-Bold.ttf", 26)
F_LEAD_BODY = font("NotoSans-Regular.ttf", 22)
F_BODY = font("NotoSans-Regular.ttf", 20)
F_STRIP = font("NotoSans-Regular.ttf", 17)
F_FOOT = font("NotoSans-Regular.ttf", 16)


def fit_lines(d, text, f, width, most):
    """Greedy word wrap, capped at `most` lines."""
    out, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out[:most]


def block(d, x, y, text, f, colour, width, most, step):
    """Draw wrapped text; return y below the last line."""
    for line in fit_lines(d, text, f, width, most):
        d.text((x, y), line, font=f, fill=colour)
        y += step
    return y


def chip(d, x, y, label):
    """Coloured tag chip; returns the x just past it."""
    c = TAGS[label]
    w = int(d.textlength(label, font=F_SUB)) + 18
    d.rounded_rectangle([x, y, x + w, y + 28], radius=4, fill=c)
    d.text((x + 9, y + 3), label, font=F_SUB, fill=(255, 255, 255))
    return x + w


def card(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=6,
                        fill=PAPER_CARD, outline=LINE, width=2)


def star(d, cx, cy, r, colour):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=colour)


# ---------- small scene drawings ----------

def scene_cop(d, x, y, w, h):
    """A cracked globe under a hot sun: the climate talks collapse."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=(24, 54, 84))
    cx, cy, r = x + w // 2 - 30, y + h // 2 + 8, 92
    # sun
    sx, sy = x + w - 62, y + 48
    d.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], fill=(240, 172, 44))
    for i in range(8):
        a = math.pi * i / 4
        d.line([(sx + 32 * math.cos(a), sy + 32 * math.sin(a)),
                (sx + 42 * math.cos(a), sy + 42 * math.sin(a))],
               fill=(240, 172, 44), width=5)
    # globe
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 140, 96))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=3)
    d.ellipse([cx - 58, cy - 62, cx - 2, cy - 6], fill=(44, 108, 66))
    d.ellipse([cx + 8, cy + 12, cx + 66, cy + 66], fill=(44, 108, 66))
    d.ellipse([cx - 66, cy + 34, cx - 14, cy + 74], fill=(44, 108, 66))
    # crack across the globe
    d.line([(cx - 70, cy - 84), (cx - 20, cy - 30), (cx - 44, cy + 8),
            (cx + 6, cy + 52), (cx + 62, cy + 84)],
           fill=(255, 255, 255), width=5)
    # thermometer
    d.rounded_rectangle([x + w - 40, y + h - 118, x + w - 22, y + h - 26],
                        radius=8, fill=(255, 255, 255), outline=CRIMSON, width=3)
    d.rectangle([x + w - 36, y + h - 76, x + w - 26, y + h - 36], fill=CRIMSON)
    d.ellipse([x + w - 41, y + h - 40, x + w - 21, y + h - 20], fill=CRIMSON)
    d.text((x + 14, y + h - 28), "ANTALYA, TÜRKIYE", font=F_SUB,
           fill=(255, 255, 255))


def scene_dymer(d, x, y, s):
    """A damaged apartment block with smoke rising."""
    bx, by = x + 8, y + 22
    d.rectangle([bx, by, bx + 56, by + 64], fill=SLATE)
    for row in range(4):
        for col in range(3):
            wx, wy = bx + 8 + col * 17, by + 8 + row * 15
            d.rectangle([wx, wy, wx + 10, wy + 9],
                        fill=(255, 214, 120) if (row + col) % 2 else (40, 48, 64))
    # broken corner
    d.polygon([(bx + 56, by), (bx + 56, by + 22), (bx + 34, by + 22),
               (bx + 44, by + 10)], fill=(20, 28, 40))
    d.line([(bx + 44, by + 10), (bx + 56, by + 22)], fill=(255, 255, 255), width=2)
    # smoke puffs
    for i, (sx, sy, sr) in enumerate([(bx + 44, by - 8, 9), (bx + 58, by - 20, 12),
                                      (bx + 40, by - 32, 8)]):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                  fill=(150, 148, 142) if i % 2 else (120, 118, 112))
    # small drone: body, arms and rotor dots
    dx, dy = x + s - 30, y + 16
    d.rectangle([dx - 8, dy - 4, dx + 8, dy + 4], fill=INK)
    d.line([(dx - 16, dy - 10), (dx + 16, dy - 10)], fill=INK, width=2)
    d.line([(dx - 16, dy + 10), (dx + 16, dy + 10)], fill=INK, width=2)
    for rx in (dx - 16, dx + 16):
        d.ellipse([rx - 3, dy - 13, rx + 3, dy - 7], fill=INK)
        d.ellipse([rx - 3, dy + 7, rx + 3, dy + 13], fill=INK)


def scene_oil(d, x, y, s):
    """An oil barrel with a flame, for the Iran standoff."""
    bx, by = x + s // 2 - 26, y + 34
    d.rounded_rectangle([bx, by, bx + 52, by + 52], radius=6, fill=(30, 30, 30))
    d.line([(bx, by + 14), (bx + 52, by + 14)], fill=(120, 120, 120), width=3)
    d.line([(bx, by + 34), (bx + 52, by + 34)], fill=(120, 120, 120), width=3)
    d.text((bx + 14, by + 18), "$90", font=font("NotoSans-Bold.ttf", 18),
           fill=(255, 214, 120))
    # flame
    fx, fy = x + s // 2, y + 18
    d.polygon([(fx - 14, fy + 8), (fx, fy - 16), (fx + 14, fy + 8),
               (fx + 6, fy + 2), (fx, fy + 12), (fx - 6, fy + 2)],
              fill=(232, 96, 30))
    d.polygon([(fx - 6, fy + 6), (fx, fy - 4), (fx + 6, fy + 6)],
              fill=(255, 214, 90))


def scene_capitol(d, x, y, s):
    """A capitol dome with the House seat count in a pill above it."""
    cx = x + s // 2
    # seat-count pill
    d.rounded_rectangle([cx - 30, y + 2, cx + 30, y + 28], radius=12,
                        fill=(255, 255, 255), outline=INDIGO, width=2)
    d.text((cx - 20, y + 5), "258", font=font("NotoSans-ExtraBold.ttf", 20),
           fill=INDIGO)
    d.polygon([(cx - 40, y + 82), (cx + 40, y + 82), (cx + 40, y + 56),
               (cx - 40, y + 56)], fill=INDIGO)
    d.polygon([(cx - 28, y + 56), (cx + 28, y + 56), (cx, y + 32)],
              fill=INDIGO)
    d.rectangle([cx - 2, y + 26, cx + 2, y + 34], fill=INDIGO)
    for i in range(3):
        px = cx - 30 + i * 24
        d.rectangle([px, y + 62, px + 12, y + 76], fill=(255, 255, 255))


def scene_factory(d, x, y, s):
    """A factory roofline with flames and smoke."""
    d.rectangle([x + 8, y + 44, x + s - 8, y + 86], fill=(70, 66, 60))
    d.polygon([(x + 14, y + 44), (x + 34, y + 20), (x + 54, y + 44)],
              fill=(70, 66, 60))
    d.polygon([(x + 58, y + 44), (x + 78, y + 20), (x + 98, y + 44)],
              fill=(70, 66, 60))
    d.rectangle([x + s - 26, y + 12, x + s - 14, y + 44], fill=(70, 66, 60))
    for sx, sy, sr in [(x + 26, y + 14, 9), (x + 40, y + 2, 11), (x + 60, y + 12, 8)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 148, 142))
    star(d, x + s // 2, y + 62, 16, (232, 96, 30))


def scene_mercury(d, x, y, s):
    """Mercury with the BepiColombo probe flying past."""
    cx, cy = x + s // 2, y + s // 2 + 6
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(176, 140, 110))
    for mx, my, mr in [(cx - 12, cy - 8, 6), (cx + 10, cy + 6, 8), (cx - 2, cy + 16, 5)]:
        d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(140, 108, 82))
    # probe body and panels
    px, py = x + s - 34, y + 10
    d.rectangle([px, py, px + 18, py + 10], fill=SLATE)
    d.line([(px - 12, py + 5), (px, py + 5)], fill=SLATE, width=3)
    d.line([(px + 18, py + 5), (px + 30, py + 5)], fill=SLATE, width=3)
    d.line([(cx + 30, cy - 10), (px - 6, py + 2)], fill=PALE, width=2)


# ---------- page ----------

def main():
    img = Image.new("RGB", (W, H), NEWS)
    d = ImageDraw.Draw(img)
    usable = W - 2 * EDGE_MARGIN

    # Masthead
    d.line([(EDGE_MARGIN, 28), (W - EDGE_MARGIN, 28)], fill=CRIMSON, width=5)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 38), title, font=F_TITLE, fill=INK)
    dateline = "MONDAY, 23 NOVEMBER 2026"
    dw = d.textlength(dateline, font=F_DATE)
    d.text(((W - dw) / 2, 104), dateline, font=F_DATE, fill=CRIMSON)
    strap = "THE DAY'S WORLD NEWS IN ONE IMAGE"
    sw = d.textlength(strap, font=F_SUB)
    d.text(((W - sw) / 2, 132), strap, font=F_SUB, fill=GREY)
    d.line([(EDGE_MARGIN, 160), (W - EDGE_MARGIN, 160)], fill=INK, width=3)

    # Lead: COP31 collapses
    ly, lh = 176, 272
    card(d, EDGE_MARGIN, ly, usable, lh)
    chip(d, EDGE_MARGIN + 18, ly + 16, "CLIMATE")
    d.text((EDGE_MARGIN + 148, ly + 18), "ANTALYA", font=F_SUB, fill=PALE)
    y = block(d, EDGE_MARGIN + 18, ly + 52,
              "Climate summit ends with no deal",
              F_LEAD_HEAD, INK, 536, 3, 44)
    block(d, EDGE_MARGIN + 18, y + 6,
          "COP31 collapses after a record two days of overtime: "
          "the EU and about 130 nations reject a final text with "
          "no fossil-fuel phase-out.",
          F_LEAD_BODY, GREY, 536, 5, 28)
    scene_cop(d, EDGE_MARGIN + 580, ly + 16, 356, lh - 32)

    # Middle grid: four stories
    half = (usable - GAP) // 2
    gy, gh = 464, 196
    stories = [
        ("WAR", "Russian drone kills five near Kyiv",
         "A drone hits a five-storey block in Dymer, killing "
         "five; a child is pulled out alive.",
         scene_dymer),
        ("CONFLICT", "Trump \u2018inclined\u2019 to hit Iran again",
         "Trump says he is inclined to resume strikes without "
         "a deal by New Year; Iran wants a way out.",
         scene_oil),
        ("POLITICS", "Democrats win historic House majority",
         "Democrats clinch at least 258 seats in the US House, "
         "their largest majority since 1992.",
         scene_capitol),
        ("DISASTER", "Factory fire kills 24 in Indonesia",
         "A blaze at a candy factory in Banten leaves 24 dead; "
         "dozens of workers are still unaccounted for.",
         scene_factory),
    ]
    for i, (tag_label, head, body, scene) in enumerate(stories):
        x = EDGE_MARGIN + (i % 2) * (half + GAP)
        yy = gy + (i // 2) * (gh + GAP)
        card(d, x, yy, half, gh)
        chip(d, x + 16, yy + 14, tag_label)
        y = block(d, x + 16, yy + 50, head, F_HEAD, INK, 320, 2, 31)
        block(d, x + 16, y + 4, body, F_BODY, GREY, 320, 4, 25)
        scene(d, x + half - 108, yy + 96, 92)

    # Bottom strip: science, tech, asia
    by, bh = 888, 84
    card(d, EDGE_MARGIN, by, usable, bh)
    third = usable // 3
    strip = [
        ("SCIENCE", "BepiColombo reaches Mercury after an eight-year journey"),
        ("TECH", "Trump urges Nvidia to rehire ex-CEO Jensen Huang"),
        ("ASIA", "Seoul minister quits over AI exam-cheating scandal"),
    ]
    for i, (label, text) in enumerate(strip):
        x = EDGE_MARGIN + 16 + i * third
        d.text((x, by + 12), label, font=F_SUB, fill=TAGS[label])
        block(d, x, by + 38, text, F_STRIP, INK, third - 32, 2, 21)
        if i:
            d.line([(EDGE_MARGIN + i * third, by + 12),
                    (EDGE_MARGIN + i * third, by + bh - 12)],
                   fill=LINE, width=2)

    # Footer
    foot = ("All events reported on Monday 23 November 2026  ·  "
            "make.fun news-image-20261123")
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, 986), foot, font=F_FOOT, fill=PALE)

    img.save("entry.png", optimize=True)
    print(f"wrote entry.png ({W}x{H})")


if __name__ == "__main__":
    main()
