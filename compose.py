#!/usr/bin/env python3
"""Compose the 18 November 2026 front page: a 1024x1024 newspaper sheet.

Everything textual is drawn here with PIL so no letter can garble.
The four photographic bands come from AI illustrations in assets/; the
other five card pictures are flat icons drawn by hand below. The dotted
world map is built from rough continent polygons and the nine numbered
pins sit on the nine card stories. Output is deterministic: same input
files, same bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

PAGE = 1024
NAVY = (13, 38, 66)
NAVY_DARK = (9, 28, 50)
GOLD = (212, 168, 84)
PAPER = (248, 246, 240)
INK = (18, 20, 24)
GREY = (90, 96, 104)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
RULE = (200, 196, 188)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def band(path, w, h, focus=0.5):
    """Centre-crop an illustration to a wide band, biased to focus height."""
    im = Image.open(path).convert("RGB")
    im = ImageOps.fit(im, (w, h), method=Image.LANCZOS,
                      centering=(0.5, focus))
    return im


def icon_panel(d, kind, x, y, w, h):
    """Draw one flat editorial icon panel for cards without an AI image."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(23, 52, 84))
    cx, cy = x + w // 2, y + h // 2
    if kind == "radar":
        # concentric radar arcs and a small drone
        for r in (34, 24, 14):
            d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340,
                  fill=(120, 200, 190), width=2)
        d.line([cx, cy, cx + 26, cy - 22], fill=(212, 168, 84), width=2)
        d.ellipse([cx + 22, cy - 26, cx + 30, cy - 18], fill=(212, 168, 84))
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(240, 240, 240))
        d.line([cx - 34, cy + 26, cx + 34, cy + 26], fill=(120, 200, 190),
               width=2)
    elif kind == "skyline":
        # Shenzhen towers against a setting sun; baseline near panel bottom
        base = y + h - 10
        d.ellipse([cx + 10, cy - 24, cx + 34, cy], fill=(212, 168, 84))
        heights = [26, 40, 20, 34, 24, 30]
        for i, hh in enumerate(heights):
            tx0 = cx - 48 + i * 17
            d.rectangle([tx0, base - hh, tx0 + 13, base], fill=(10, 26, 46))
            for wy in range(base - hh + 5, base - 4, 8):
                d.rectangle([tx0 + 3, wy, tx0 + 6, wy + 3],
                            fill=(212, 168, 84))
        d.rectangle([x, base, x + w, y + h], fill=(120, 200, 190))
    elif kind == "ship":
        # container ship on waves; boxes sit on the hull
        hull_top = cy + 2
        cols = [(178, 34, 34), (212, 168, 84), (14, 110, 110),
                (200, 200, 200)]
        for i, c in enumerate(cols):
            d.rectangle([cx - 40 + i * 20, hull_top - 26,
                         cx - 22 + i * 20, hull_top - 12], fill=c)
        for i, c in enumerate(cols[:3]):
            d.rectangle([cx - 30 + i * 20, hull_top - 40,
                         cx - 12 + i * 20, hull_top - 26], fill=c)
        d.polygon([(cx - 52, hull_top - 12), (cx + 52, hull_top - 12),
                   (cx + 40, hull_top + 6), (cx - 40, hull_top + 6)],
                  fill=(10, 26, 46))
        for wx in range(x + 8, x + w - 8, 18):
            d.arc([wx, cy + 14, wx + 12, cy + 22], 0, 180,
                  fill=(120, 200, 190), width=2)
    elif kind == "scales":
        # scales of justice
        d.line([cx, cy - 28, cx, cy + 26], fill=(212, 168, 84), width=3)
        d.line([cx - 30, cy - 20, cx + 30, cy - 20], fill=(212, 168, 84),
               width=3)
        for sx in (cx - 30, cx + 30):
            d.line([sx, cy - 20, sx, cy - 2], fill=(212, 168, 84), width=2)
            d.arc([sx - 12, cy - 6, sx + 12, cy + 8], 0, 180,
                  fill=(240, 240, 240), width=2)
        d.rectangle([cx - 22, cy + 26, cx + 22, cy + 30], fill=(212, 168, 84))
    elif kind == "olive":
        # olive branch: one stem, leaves alternating above and below it
        d.line([cx - 36, cy + 18, cx + 34, cy - 18], fill=(120, 200, 190),
               width=3)
        for i in range(5):
            lx = cx - 28 + i * 13
            ly = cy + 13 - i * 7
            if i % 2 == 0:
                d.ellipse([lx - 8, ly - 14, lx + 6, ly - 2],
                          fill=(90, 170, 90))
            else:
                d.ellipse([lx - 6, ly + 2, lx + 8, ly + 14],
                          fill=(60, 140, 70))
        d.ellipse([cx + 28, cy - 24, cx + 36, cy - 16], fill=(212, 168, 84))
        d.ellipse([cx + 20, cy - 16, cx + 28, cy - 8], fill=(212, 168, 84))


# ---------------------------------------------------------------- stories

CARDS = [
    dict(n=1, tag="THE GULF", art=("icon", "radar", 0.5),
         head="GULF WAR FLARES AGAIN",
         dek="Iranian drones target a US radar in Bahrain; US jets hit a "
             "missile site on Qeshm Island. Kuwait intercepts drones.",
         pin=(50.6, 26.2)),
    dict(n=2, tag="UKRAINE", art=("ai", "bridge", 0.55),
         head="CRIMEA BRIDGE FALLS",
         dek="Ukrainian drones and missiles drop the road span of the Kerch "
             "bridge on a second day of strikes; Russia hits two Kyiv bridges.",
         pin=(36.5, 45.3)),
    dict(n=3, tag="ASIA", art=("ai", "summit", 0.72),
         head="TRUMP'S ASIA SWING",
         dek="Trump meets Quad leaders in Manila, then sees Marcos before "
             "flying to Shenzhen for the APEC summit.",
         pin=(121.0, 14.6)),
    dict(n=4, tag="APEC", art=("icon", "skyline", 0.5),
         head="APEC OPENS IN SHENZHEN",
         dek="Leaders of 21 Pacific economies gather as Xi hosts; a first "
             "Trump\u2013Xi\u2013Putin meeting is due on Thursday.",
         pin=(114.1, 22.5)),
    dict(n=5, tag="TRADE", art=("icon", "ship", 0.5),
         head="CANADA\u2013CHINA CUT TARIFFS",
         dek="Xi and Carney agree C$400m relief for pork and seafood; Canada "
             "extends steel and aluminium remissions two years.",
         pin=(116.4, 39.9)),
    dict(n=6, tag="WEST BANK", art=("icon", "scales", 0.5),
         head="SETTLER SANCTIONS SPREAD",
         dek="Britain sanctions eight settlement firms; Australia follows "
             "with sanctions on three people and four groups.",
         pin=(35.2, 31.9)),
    dict(n=7, tag="GAZA", art=("icon", "olive", 0.5),
         head="GAZA TRUCE \u2018NEAR COLLAPSE\u2019",
         dek="The Board of Peace warns the UN Security Council the year-old "
             "ceasefire could fail without urgent action.",
         pin=(34.45, 31.5)),
    dict(n=8, tag="MARKETS", art=("ai", "chip", 0.5),
         head="NVIDIA DOUBLES ITS SALES",
         dek="Revenue hits $115.8bn, up 103%, with $130bn forecast next "
             "quarter \u2014 its first results since Huang resigned.",
         pin=(-122.0, 37.4)),
    dict(n=9, tag="SPACE", art=("ai", "voyager", 0.5),
         head="VOYAGER 1, A LIGHT-DAY OUT",
         dek="NASA's 1977 probe reaches 25.9bn km from Earth; its radio "
             "signals now take a full day to arrive.",
         pin=(-118.2, 34.2)),
]

ALSO = [
    "EU to propose a \u20ac45bn loan for Ukraine, due before member states today",
    "Cyclone Akvan strengthens in the Bay of Bengal; landfall due Friday",
    "Houthis say they fired five drones at Saudi Arabia's East-West oil pipeline",
    "LPG tanker hit by a projectile in the Strait of Hormuz; crew evacuated",
    "Oil eases: Brent $92.98, WTI $85.45, as US crude stocks rise",
    "Amazon to invest $7bn in renewable energy in India by 2030",
    "MS Dhoni ends his 19-year IPL career and becomes Chennai's mentor",
    "Rival peace efforts fail to halt fighting in eastern DR Congo",
    "Thailand orders an inquiry into the Phuket fire that killed 11",
    "Putin arrives in China ahead of the APEC trilateral",
    "Trump eyes one-to-one talks with Putin and Kim at APEC",
    "Nvidia board rejects a comeback for founder Jensen Huang",
    "Trump signs a preliminary trade deal with Thailand in Manila",
    "Quad plans joint military exercises and an AI accelerator for next year",
    "Mexico's Sheinbaum meets Xi and urges trade that helps developing states",
    "Houthis seize Hanish islands and the Red Sea port of Mocha",
    "Iran's Guards claim they shot down a US MQ-1 drone near Qeshm",
    "Canada plans a 2027 trade mission to China and new Vancouver\u2013Guangzhou flights",
    "EU leaders to debate the Ukraine loan at their summit on 26\u201327 November",
    "Malaysia's Anwar to address the APEC CEO Summit and meet Xi on Friday",
    "Bahrain issues a danger alert and tells residents to take shelter",
]

# Rough continent outlines in (lon, lat); drawn as a field of dots.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73),
     (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35), (-80, 26),
     (-90, 21), (-97, 16), (-105, 20), (-115, 30), (-125, 40), (-125, 49),
     (-140, 60), (-158, 58)],
    [(-80, 10), (-72, 12), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -41), (-68, -52), (-70, -55),
     (-73, -45), (-73, -30), (-77, -20), (-80, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (30, 70),
     (25, 71), (18, 69), (12, 65), (5, 60), (-5, 58), (-10, 54), (-10, 43)],
    [(-6, 35), (-10, 31), (-17, 15), (-17, 5), (-13, -12), (12, -18),
     (16, -28), (20, -35), (28, -33), (33, -26), (40, -15), (41, -10),
     (51, 10), (44, 11), (38, 18), (33, 27), (30, 31), (22, 33), (11, 34)],
    [(30, 70), (40, 68), (55, 69), (70, 72), (90, 75), (110, 76),
     (130, 72), (160, 70), (178, 66), (170, 60), (162, 55), (158, 50),
     (142, 45), (140, 40), (130, 35), (127, 33), (122, 30), (120, 25),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20),
     (80, 13), (77, 8), (72, 20), (66, 25), (60, 25), (55, 27), (50, 29),
     (48, 30), (44, 29), (40, 30), (36, 36), (30, 36), (30, 42)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32),
     (137, -35), (140, -38), (147, -39), (150, -37), (153, -32),
     (153, -27), (150, -22), (146, -19), (142, -11), (136, -12),
     (132, -11), (126, -14), (122, -17), (118, -20)],
]

# Per-pin pixel nudges so close pins (Gaza/West Bank, Nvidia/Voyager,
# Shenzhen/Beijing) stay apart on the small map.
PIN_DXDY = {1: (5, 2), 2: (0, 0), 3: (0, 0), 4: (0, -13), 5: (7, 16),
            6: (-11, -13), 7: (13, 14), 8: (-9, -13), 9: (9, 13)}


def inside_poly(lon, lat, poly):
    """Ray-casting point-in-polygon test."""
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)) and (
                lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def lonlat_to_xy(lon, lat, x0, y0, w, h):
    px = x0 + (lon + 180.0) / 360.0 * w
    py = y0 + (84.0 - lat) / 139.0 * h
    return px, py


def draw_map(d, x, y, w, h):
    pin_f = f(SANS_B, 10)
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(232, 238, 244))
    step = 6
    r = 2
    yy = y + 4
    while yy < y + h - 3:
        xx = x + 4
        while xx < x + w - 3:
            lon = (xx - x) / w * 360.0 - 180.0
            lat = 84.0 - (yy - y) / h * 139.0
            if any(inside_poly(lon, lat, p) for p in CONTINENTS):
                d.ellipse([xx - r, yy - r, xx + r, yy + r],
                          fill=(52, 84, 120))
            xx += step
        yy += step
    for c in CARDS:
        lon, lat = c["pin"]
        px, py = lonlat_to_xy(lon, lat, x, y, w, h)
        dx, dy = PIN_DXDY[c["n"]]
        px, py = px + dx, py + dy
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        num = str(c["n"])
        tw = d.textlength(num, font=pin_f)
        d.text((px - tw / 2, py - 7), num, font=pin_f, fill=(255, 255, 255))


def build():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, PAGE - 1, 96], fill=NAVY)
    d.rectangle([0, 96, PAGE - 1, 99], fill=GOLD)
    title = f(SERIF, 40)
    d.text((18, 8), "THE WORLD IN ONE DAY", font=title, fill=(255, 255, 255))
    date_f = f(SERIF, 21)
    d.text((18, 56), "WEDNESDAY, 18 NOVEMBER 2026", font=date_f,
           fill=GOLD)
    kick = f(SANS_B, 13)
    kt = "30 STORIES  \u00b7  6 CONTINENTS  \u00b7  AS REPORTED TODAY"
    d.text((PAGE - 18 - d.textlength(kt, font=kick), 66), kt, font=kick,
           fill=(200, 214, 228))

    # ---- 3x3 story cards ----------------------------------------------
    cw, ch, gap = 324, 160, 8
    gx, gy = 18, 106
    head_f = f(SANS_B, 15)
    tag_f = f(SANS_B, 11)
    dek_f = f(SANS, 11)
    num_f = f(SANS_B, 12)
    for idx, c in enumerate(CARDS):
        cx = gx + (idx % 3) * (cw + gap)
        cy = gy + (idx // 3) * (ch + gap)
        d.rectangle([cx, cy, cx + cw - 1, cy + ch - 1], fill=(255, 255, 255),
                    outline=RULE, width=1)
        kind, name, focus = c["art"]
        if kind == "ai":
            path = os.path.join(ASSETS, "media-generation-%s-0-" % name)
            files = [p for p in os.listdir(ASSETS)
                     if p.startswith("media-generation-%s-0-" % name)
                     and p.endswith(".png")]
            im = band(os.path.join(ASSETS, files[0]), cw, 54, focus)
            img.paste(im, (cx, cy))
        else:
            icon_panel(d, name, cx, cy, cw, 54)
        # number badge over the picture's corner
        d.ellipse([cx + 6, cy + 6, cx + 28, cy + 28], fill=RED,
                  outline=(255, 255, 255), width=2)
        n = str(c["n"])
        d.text((cx + 17 - d.textlength(n, font=num_f) / 2, cy + 9), n,
               font=num_f, fill=(255, 255, 255))
        tx = cx + 10
        ty = cy + 62
        d.text((tx, ty), c["tag"], font=tag_f, fill=RED)
        lines = wrap_text(d, c["head"], head_f, cw - 20)
        hy = ty + 15
        for ln in lines[:2]:
            d.text((tx, hy), ln, font=head_f, fill=INK)
            hy += 18
        dlines = wrap_text(d, c["dek"], dek_f, cw - 20)
        dy = hy + 2
        for ln in dlines[:3]:
            d.text((tx, dy), ln, font=dek_f, fill=(52, 56, 62))
            dy += 14

    # ---- world map ------------------------------------------------------
    my = gy + 3 * ch + 2 * gap + 10
    sec_f = f(SANS_B, 13)
    d.text((18, my), "WHERE IT HAPPENED \u2014 9 STORIES, 9 PLACES",
           font=sec_f, fill=NAVY)
    map_y = my + 20
    draw_map(d, 18, map_y, PAGE - 36, 128)

    # ---- also today -----------------------------------------------------
    ay = map_y + 128 + 12
    total = len(CARDS) + len(ALSO)
    d.text((18, ay), "ALSO ON WEDNESDAY 18 NOVEMBER \u2014 %d MORE STORIES"
           % len(ALSO), font=sec_f, fill=NAVY)
    d.line([18, ay + 18, PAGE - 18, ay + 18], fill=RULE, width=1)
    item_f = f(SANS, 11)
    rows = (len(ALSO) + 1) // 2
    col_w = (PAGE - 36) // 2
    for i, text in enumerate(ALSO):
        col = i // rows
        row = i % rows
        ix = 18 + col * col_w
        iy = ay + 24 + row * 17
        label = "%d." % (len(CARDS) + i + 1)
        d.text((ix, iy), label, font=f(SANS_B, 11), fill=RED)
        lx = ix + d.textlength("30. ", font=f(SANS_B, 11)) + 2
        line = text
        while d.textlength(line, font=item_f) > col_w - (lx - ix) - 6 \
                and len(line) > 4:
            line = line[:-1]
        if line != text:
            line = line.rstrip()[:-1] + "\u2026"
        d.text((lx, iy), line, font=item_f, fill=INK)

    # ---- footer ---------------------------------------------------------
    fy = PAGE - 26
    d.line([18, fy - 6, PAGE - 18, fy - 6], fill=RULE, width=1)
    foot = ("Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera "
            "\u00b7 UN News \u2014 every story above was reported on "
            "Wednesday 18 November 2026.")
    ff = f(SANS, 10)
    d.text(((PAGE - d.textlength(foot, font=ff)) / 2, fy), foot, font=ff,
           fill=GREY)
    return img


if __name__ == "__main__":
    out = build()
    out.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("saved entry.png", out.size)
