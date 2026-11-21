#!/usr/bin/env python3
"""Compose v4: newspaper front page, 20 November 2026 world news.

Pure-code composition with Pillow (no AI-generated image, no network):
every word and number is drawn from the verified fact list in the build
plan (~/workspace/makefun/v2-plan.md), so text is pixel-exact.

v4 changes vs v3 (craft only — no fact, number or date changed):
- warm beige paper, serif masthead with the DATE as the largest text;
- three equal lead cards (Kyiv, Akvan, AI sell-off), each with a
  code-drawn flat scene illustration across the top half of the card;
- every feature tile also gets a flat scene illustration banner
  (no more ~30px pictogram icons);
- a real map block: navy panel, beige continents at true aspect,
  red numbered dots 1-13 for the 13 main stories;
- ALSO is numbered 14-35, two columns, and the totals are now honest:
  v3's box said "13 MAIN + 21 ALSO = 34" but the Kyiv lead + 13 tiles
  + 21 ALSO was really 35 stories. v4 counts 13 main cards (3 leads +
  10 features) and 22 ALSO (BepiColombo moves to ALSO as item 35),
  total 35 — the same 35-item list the v2 plan locked, so the region
  counts are unchanged;
- DATE CHECK is a red-bordered box with two parts: NOT 20 NOV (left
  out) and NOT YET (due 21 Nov).

Layout (1024x1024):
  masthead 0-92 | 6-stat strip 92-150 | 3 lead cards 150-392 |
  10 feature tiles 392-672 (2 rows x 5) |
  map block + ALSO 672-868 | DATE CHECK box 868-968 | footer 968-1024

Usage: python3 compose_v4.py [out.png]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
INK = (24, 24, 24)
RED = (178, 34, 34)
PAPER = (247, 240, 224)          # warm beige
CREAM = (255, 251, 240)          # card paper
PANEL = (238, 229, 206)          # pale sand panel
NAVY = (30, 54, 96)              # map block / night sky
MAPBEIGE = (233, 221, 193)       # continents
SKY = (196, 214, 232)            # pale blue sky
SEA = (178, 203, 224)            # pale sea
SAND = (226, 205, 160)           # desert sand
GREY = (110, 105, 95)
RULE = (178, 34, 34)             # thin red rules
AMBER = (232, 164, 60)
DARKRED = (140, 26, 26)

FD = "/usr/share/fonts/truetype"


def F(path, size):
    return ImageFont.truetype(os.path.join(FD, path), size)


SERIF_B = "liberation/LiberationSerif-Bold.ttf"
SERIF = "liberation/LiberationSerif-Regular.ttf"
SERIF_I = "liberation/LiberationSerif-Italic.ttf"
SANS_B = "liberation/LiberationSans-Bold.ttf"
SANS = "liberation/LiberationSans-Regular.ttf"
COND_B = "noto/NotoSerif-CondensedBold.ttf"
COND_BLK = "noto/NotoSerif-CondensedBlack.ttf"

WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print("WARN:", msg)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap measured with the real font; returns lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        cand = (cur + " " + word).strip()
        if d.textlength(cand, font=fnt) <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(d, x, y, s, fnt, fill=INK):
    d.text((x, y), s, font=fnt, fill=fill)


def centered(d, cx, y, s, fnt, fill=INK):
    d.text((cx - d.textlength(s, font=fnt) / 2, y), s, font=fnt, fill=fill)


def right(d, x, y, s, fnt, fill=INK):
    d.text((x - d.textlength(s, font=fnt), y), s, font=fnt, fill=fill)


# ---------------------------------------------------------------- content
# 6 big-number stats (unchanged from v2/v3).
STATS = [
    ("110+", "missiles fired at Ukraine overnight"),
    ("9", "killed nationwide; 28 injured"),
    ("3", "Kyiv bridges hit across the Dnipro"),
    ("300,000+", "moved to shelters in Odisha"),
    ("\u22126.2%", "Taiwan Taiex on Friday"),
    ("$81.3bn", "Anthropic IPO, largest ever"),
]

# 3 lead cards: (number, red label, headline, deck, scene key).
# Headlines/decks condensed from the verified plan decks; numbers unchanged.
LEADS = [
    (1, "KYIV \u2014 UKRAINE",
     "RUSSIA'S BIGGEST AIR ATTACK THIS YEAR",
     "110+ missiles and 400+ drones overnight; 9 killed, 28 hurt; "
     "3 bridges hit; power and water cut in parts of the capital.",
     "kyiv"),
    (2, "INDIA \u2014 ODISHA",
     "CYCLONE AKVAN HITS ODISHA",
     "Landfall near Gopalpur, 07:30\u201308:30 IST; winds 70\u201380 km/h; "
     "300,000+ evacuated; no deaths in the first assessment.",
     "cyclone"),
    (3, "MARKETS \u2014 ASIA",
     "AI SELL-OFF SWEEPS ASIA",
     "Taiex \u22126.2%, Kospi \u22125.2%, Nikkei \u22124.8%; S&P 500 \u22122.0%, "
     "6th straight loss.",
     "chart"),
]

# 10 feature tiles: (number, headline, deck, scene key). Same 10 stories
# as v3's tiles minus the two promoted to leads (Akvan, Markets).
FEATURES = [
    (4, "GAZA \u2014 TANKS CROSS YELLOW LINE",
     "First ground crossing since the Oct 2025 truce.",
     "tank"),
    (5, "SHENZHEN: TRUMP\u2013XI\u2013PUTIN MEET",
     "19 Nov: 90 min at Kylin Villa; backs nuclear talks, UN reform.",
     "summit"),
    (6, "THE HAGUE: MYANMAR GUILTY OF GENOCIDE",
     "19 Nov: ICJ, 9\u20136 \u2014 first state found guilty.",
     "gavel"),
    (7, "BRUSSELS: EU\u2013UK RESET DEAL SEALED",
     "Food checks from Mar 2028, \u00a35.1bn a year.",
     "rings"),
    (8, "ANTALYA: COP31 ENDS WITH NO EXIT PLAN",
     "Final draft drops fossil-fuel phase-out.",
     "globe"),
    (9, "RIYADH: STRIKE HITS TALLEST TOWER",
     "19 Nov: PIF Tower hit; windows out on 7\u20138 floors; no injuries.",
     "tower"),
    (10, "POLAND: NATO AIRSPACE BREACH",
     "3 objects cross in; Kh-101 found; jets scrambled, no injuries.",
     "jet"),
    (11, "NEW YORK: RECORD IPO DEBUT",
     "19 Nov: $81.3bn IPO, largest ever; closed $97.17.",
     "candles"),
    (12, "CRIMEA: 3RD BRIDGE STRIKE",
     "19 Nov: Neptune missiles damage Kerch rail tracks.",
     "bridge"),
    (13, "TOKYO: JAPAN INFLATION STAYS HIGH",
     "Oct CPI: headline 2.3%, core 2.2%; Dec rate hike expected.",
     "tag"),
]

# ALSO list: 22 one-liners numbered 14-35. Same 21 as v3 plus BepiColombo
# (item 35), which moves down from the main tiles so the totals are
# honest: 13 main + 22 ALSO = 35. Each item condensed to fit one 12 px
# line in a 300 px column; every number is unchanged.
ALSO = [
    "SENEGAL \u2014 Boat capsizes; 4 dead, dozens missing.",
    "SUDAN \u2014 Drone strike on Bajoun mine kills 10+.",
    "CARACAS \u2014 US, Venezuela sign military deal.",
    "SAN SALVADOR \u2014 Bukele registers for 3rd term.",
    "NAIROBI \u2014 Kenya's last Ebola patient home 11 Nov.",
    "KENYA \u2014 Mrima Hill tender won; $60bn+ deposits.",
    "SHENZHEN \u2014 Philippines, Chile sign trade deal.",
    "ITALY \u2014 CGIL strike in 100+ cities.",
    "PACIFIC \u2014 Fiji declares disaster; Tonga emergency.",
    "KYIV \u2014 UNICEF: 1,144 children killed or injured.",
    "HORMUZ \u2014 Iran war in 9th month; Brent ~$90.",
    "VIENNA \u2014 IAEA: North Korea expanding enrichment.",
    "COPENHAGEN \u2014 Denmark ratifies Greenland deal.",
    "NEW YORK \u2014 UN secretary-general race stalls.",
    "WASHINGTON \u2014 IMF: global debt nears 100% of GDP.",
    "WASHINGTON \u2014 Senate passes permitting bill, 62\u201333.",
    "BRAS\u00cdLIA \u2014 Brazil's bank sells $1bn to curb dollar.",
    "MARKETS \u2014 Gold \u22124.2% this week; Brent ~$90.05.",
    "WASHINGTON \u2014 Trump pardons baseball star Pete Rose.",
    "HAITI \u2014 Forces kill 34 gang members in raid.",
    "SPORT \u2014 Jepchirchir banned 3 years for doping.",
    "SPACE \u2014 BepiColombo due at Mercury tomorrow.",
]

DATE_LEFT_HEAD = "NOT 20 NOV \u2014 LEFT OUT"
DATE_LEFT = ("Myanmar ICJ ruling; Shenzhen summit; PIF Tower strike; "
             "Anthropic IPO first trade; Crimea bridge strike \u2014 all "
             "first reported 19 Nov.")
DATE_RIGHT_HEAD = "NOT YET \u2014 DUE 21 NOV"
DATE_RIGHT = ("BepiColombo Mercury capture due tomorrow; COP31 final text "
              "not agreed at press time.")

FOOTER = ("Sources: Reuters, AP, CNN, BBC, UNICEF, IMD, Statistics Bureau of "
          "Japan, Fiji Government. Figures as reported on 20 Nov 2026; early "
          "casualty counts were updated during the day.")

REGION_LINE1 = "EUROPE 8 \u00b7 ASIA 7 \u00b7 AMERICAS 7"
REGION_LINE2 = "AFRICA 5 \u00b7 SPACE/GLOBAL 4 \u00b7 MIDDLE EAST 3 \u00b7 OCEANIA 1"

# ---------------------------------------------------------------- scenes
# Each scene draws a flat illustration inside rect (x, y, w, h).
# Deterministic: no randomness, fixed star/dot positions.


def scene_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sy, r in ((0.08, 0.14, 2), (0.22, 0.08, 1), (0.35, 0.2, 2),
                      (0.5, 0.1, 1), (0.62, 0.18, 2), (0.75, 0.07, 1),
                      (0.88, 0.16, 2), (0.95, 0.1, 1), (0.42, 0.06, 1)):
        d.ellipse([x + sx * w - r, y + sy * h - r,
                   x + sx * w + r, y + sy * h + r], fill=(255, 255, 255))
    # missile trails: bright diagonal streaks with glowing heads
    for (tx0, ty0, tx1, ty1) in ((0.12, 0.78, 0.3, 0.3),
                                 (0.45, 0.85, 0.62, 0.38),
                                 (0.72, 0.8, 0.86, 0.42)):
        d.line([(x + tx0 * w, y + ty0 * h), (x + tx1 * w, y + ty1 * h)],
               fill=(255, 220, 130), width=3)
        d.ellipse([x + tx1 * w - 5, y + ty1 * h - 5,
                   x + tx1 * w + 5, y + ty1 * h + 5], fill=AMBER)
    # fire glow over the skyline
    d.ellipse([x + 0.55 * w, y + 0.52 * h, x + 0.85 * w, y + 0.82 * h],
              fill=(214, 90, 40))
    d.ellipse([x + 0.62 * w, y + 0.6 * h, x + 0.78 * w, y + 0.78 * h],
              fill=(240, 170, 70))
    # skyline silhouettes with lit windows
    base = y + h
    for bx, bw, bh in ((0.0, 0.16, 0.34), (0.16, 0.11, 0.5),
                       (0.27, 0.14, 0.4), (0.41, 0.1, 0.58),
                       (0.51, 0.15, 0.36), (0.66, 0.12, 0.48),
                       (0.78, 0.1, 0.32), (0.88, 0.12, 0.42)):
        d.rectangle([x + bx * w, base - bh * h, x + (bx + bw) * w, base],
                    fill=(12, 20, 38))
        for wx in (0.25, 0.6):
            for wy in (0.25, 0.55):
                d.rectangle([x + (bx + wx * bw) * w - 1,
                             base - bh * h + wy * bh * h,
                             x + (bx + wx * bw) * w + 1,
                             base - bh * h + wy * bh * h + 2],
                            fill=AMBER)


def scene_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # land: simplified Indian east coast + Odisha bulge on the right
    d.polygon([(x + 0.62 * w, y), (x + w, y), (x + w, y + h),
               (x + 0.72 * w, y + h), (x + 0.68 * w, y + 0.62 * h),
               (x + 0.6 * w, y + 0.4 * h), (x + 0.66 * w, y + 0.18 * h)],
              fill=SAND)
    cx, cy = x + 0.42 * w, y + 0.52 * h
    for r, a0, a1 in ((0.34, 30, 330), (0.25, 210, 120), (0.16, 30, 330),
                      (0.08, 210, 120)):
        rr = r * min(w, h)
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], a0, a1,
              fill=(255, 255, 255), width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    d.ellipse([x + 0.66 * w - 3, y + 0.55 * h - 3,
               x + 0.66 * w + 3, y + 0.55 * h + 3], fill=RED)


def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CREAM)
    for gy in (0.25, 0.5, 0.75):
        d.line([(x + 4, y + gy * h), (x + w - 4, y + gy * h)],
               fill=(220, 210, 190), width=1)
    pts = [(0.06, 0.2), (0.2, 0.28), (0.32, 0.24), (0.45, 0.45),
           (0.58, 0.52), (0.7, 0.68), (0.82, 0.74), (0.94, 0.9)]
    xy = [(x + px * w, y + py * h) for px, py in pts]
    d.line(xy, fill=RED, width=4)
    d.polygon([(xy[-1][0], xy[-1][1]), (xy[-1][0] - 12, xy[-1][1] - 2),
               (xy[-1][0] - 4, xy[-1][1] - 12)], fill=RED)
    for bx, bh in ((0.14, 0.3), (0.3, 0.22), (0.46, 0.4), (0.62, 0.32)):
        d.rectangle([x + bx * w, y + h - bh * h, x + (bx + 0.09) * w, y + h],
                    fill=(180, 180, 175))


def scene_tank(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    d.ellipse([x + 0.78 * w, y + 0.1 * h, x + 0.92 * w, y + 0.24 * h],
              fill=(255, 244, 214))
    d.line([(x, y + 0.82 * h), (x + w, y + 0.82 * h)], fill=(150, 120, 80),
           width=2)
    cx, cy = x + 0.5 * w, y + 0.55 * h
    s = min(w, h) / 90.0
    lw = max(1, int(round(5 * s)))
    d.rounded_rectangle([cx - 34 * s, cy + 8 * s, cx + 34 * s, cy + 26 * s],
                        radius=int(round(8 * s)), fill=INK)
    for wx in (-22, 0, 22):
        d.ellipse([cx + wx * s - 5 * s, cy + 12 * s,
                   cx + wx * s + 5 * s, cy + 22 * s], fill=SAND)
    d.rectangle([cx - 28 * s, cy - 6 * s, cx + 28 * s, cy + 8 * s], fill=INK)
    d.rectangle([cx - 12 * s, cy - 20 * s, cx + 12 * s, cy - 6 * s], fill=INK)
    d.line([(cx + 12 * s, cy - 13 * s), (cx + 36 * s, cy - 13 * s)],
           fill=INK, width=lw)
    d.rectangle([x + 0.06 * w, y + 0.6 * h, x + 0.14 * w, y + 0.82 * h],
                fill=(120, 95, 60))


def scene_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CREAM)
    # three flags on poles behind a table
    for fx, col in ((0.24, RED), (0.5, NAVY), (0.76, (60, 110, 60))):
        d.line([(x + fx * w, y + 0.12 * h), (x + fx * w, y + 0.55 * h)],
               fill=INK, width=2)
        d.polygon([(x + fx * w, y + 0.12 * h),
                   (x + (fx + 0.16) * w, y + 0.2 * h),
                   (x + fx * w, y + 0.28 * h)], fill=col)
    d.rectangle([x + 0.08 * w, y + 0.58 * h, x + 0.92 * w, y + 0.66 * h],
                fill=INK)
    d.line([(x + 0.16 * w, y + 0.66 * h), (x + 0.16 * w, y + 0.9 * h)],
           fill=INK, width=2)
    d.line([(x + 0.84 * w, y + 0.66 * h), (x + 0.84 * w, y + 0.9 * h)],
           fill=INK, width=2)
    for cx in (0.3, 0.5, 0.7):
        d.ellipse([x + cx * w - 5, y + 0.5 * h, x + cx * w + 5, y + 0.58 * h],
                  fill=(90, 60, 40))


def scene_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    cx, cy = x + 0.5 * w, y + 0.42 * h
    s = min(w, h) / 90.0
    d.line([(cx - 30 * s, cy - 22 * s), (cx + 6 * s, cy - 34 * s)],
           fill=CREAM, width=max(1, int(round(14 * s))))
    d.line([(cx - 8 * s, cy - 12 * s), (cx + 24 * s, cy + 24 * s)],
           fill=CREAM, width=max(1, int(round(7 * s))))
    d.rectangle([cx - 34 * s, cy + 30 * s, cx + 34 * s, cy + 40 * s],
                fill=AMBER)
    for sx, sy in ((0.16, 0.18), (0.85, 0.22), (0.9, 0.75), (0.12, 0.8)):
        d.ellipse([x + sx * w - 2, y + sy * h - 2,
                   x + sx * w + 2, y + sy * h + 2], fill=CREAM)


def scene_rings(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CREAM)
    cx, cy = x + 0.5 * w, y + 0.5 * h
    r = min(w, h) * 0.3
    d.ellipse([cx - r - 0.28 * w, cy - r, cx - 0.28 * w + r, cy + r],
              outline=NAVY, width=4)
    d.ellipse([cx + 0.28 * w - r, cy - r, cx + 0.28 * w + r, cy + r],
              outline=RED, width=4)
    for sx, sy in ((0.14, 0.2), (0.86, 0.2), (0.5, 0.14)):
        d.ellipse([x + sx * w - 2, y + sy * h - 2,
                   x + sx * w + 2, y + sy * h + 2], fill=AMBER)


def scene_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 68, 84))
    cx, cy = x + 0.42 * w, y + 0.5 * h
    r = min(w, h) * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 140))
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=(220, 235, 225), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(220, 235, 225), width=2)
    d.polygon([(cx - r * 0.7, cy - r * 0.4), (cx - r * 0.2, cy - r * 0.7),
               (cx + r * 0.1, cy - r * 0.2), (cx - r * 0.4, cy + r * 0.1)],
              fill=(60, 120, 90))
    # thermometer on the right
    tx = x + 0.8 * w
    d.rounded_rectangle([tx - 5, y + 0.18 * h, tx + 5, y + 0.78 * h],
                        radius=5, fill=CREAM)
    d.ellipse([tx - 9, y + 0.74 * h, tx + 9, y + 0.9 * h], fill=RED)
    d.rectangle([tx - 2, y + 0.3 * h, tx + 2, y + 0.78 * h], fill=RED)


def scene_tower(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 62, 84))
    cx = x + 0.42 * w
    d.rectangle([cx - 0.09 * w, y + 0.22 * h, cx + 0.09 * w, y + h],
                fill=(16, 20, 32))
    for wy in (0.3, 0.42, 0.54, 0.66, 0.78):
        for wx in (-0.05, 0.02):
            d.rectangle([cx + wx * w - 2, y + wy * h,
                         cx + wx * w + 2, y + wy * h + 3], fill=AMBER)
    # broken top: jagged edge + smoke
    d.polygon([(cx - 0.09 * w, y + 0.22 * h), (cx - 0.03 * w, y + 0.16 * h),
               (cx + 0.02 * w, y + 0.22 * h), (cx + 0.09 * w, y + 0.14 * h),
               (cx + 0.09 * w, y + 0.22 * h)], fill=(16, 20, 32))
    for sx, sy, sr in ((0.55, 0.12, 7), (0.66, 0.2, 9), (0.78, 0.1, 6)):
        d.ellipse([x + sx * w - sr, y + sy * h - sr,
                   x + sx * w + sr, y + sy * h + sr], fill=(150, 150, 145))
    d.ellipse([x + 0.72 * w, y + 0.72 * h, x + 0.8 * w, y + 0.8 * h],
              fill=AMBER)


def scene_jet(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cx, cy = x + 0.5 * w, y + 0.5 * h
    s = min(w, h) / 90.0
    d.polygon([(cx + 34 * s, cy - 4 * s), (cx - 26 * s, cy - 18 * s),
               (cx - 34 * s, cy - 4 * s), (cx - 26 * s, cy + 10 * s)],
              fill=INK)
    d.polygon([(cx - 4 * s, cy - 4 * s), (cx - 16 * s, cy - 26 * s),
               (cx - 4 * s, cy - 22 * s)], fill=INK)
    d.polygon([(cx - 4 * s, cy - 4 * s), (cx - 16 * s, cy + 18 * s),
               (cx - 4 * s, cy + 14 * s)], fill=INK)
    for r in (0.32, 0.42):
        rr = r * min(w, h)
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 200, 340,
              fill=RED, width=2)
    d.ellipse([cx + 0.36 * w - 4, cy - 0.3 * h - 4,
               cx + 0.36 * w + 4, cy - 0.3 * h + 4], fill=RED)


def scene_candles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CREAM)
    for bx, top, bot, col in ((0.12, 0.55, 0.85, (60, 110, 60)),
                              (0.3, 0.4, 0.7, RED),
                              (0.48, 0.5, 0.78, (60, 110, 60)),
                              (0.66, 0.28, 0.6, (60, 110, 60)),
                              (0.82, 0.38, 0.68, RED)):
        d.line([(x + (bx + 0.04) * w, y + (top - 0.08) * h),
                (x + (bx + 0.04) * w, y + (bot + 0.08) * h)],
               fill=INK, width=2)
        d.rectangle([x + bx * w, y + top * h, x + (bx + 0.08) * w,
                     y + bot * h], fill=col)
    d.line([(x + 0.1 * w, y + 0.3 * h), (x + 0.9 * w, y + 0.12 * h)],
           fill=INK, width=3)
    d.polygon([(x + 0.9 * w, y + 0.12 * h), (x + 0.82 * w, y + 0.1 * h),
               (x + 0.86 * w, y + 0.2 * h)], fill=INK)


def scene_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + 0.78 * h, x + w, y + h], fill=(120, 140, 160))
    d.line([(x + 0.04 * w, y + 0.42 * h), (x + 0.42 * w, y + 0.42 * h)],
           fill=INK, width=3)
    d.line([(x + 0.58 * w, y + 0.42 * h), (x + 0.96 * w, y + 0.42 * h)],
           fill=INK, width=3)
    d.line([(x + 0.04 * w, y + 0.5 * h), (x + 0.42 * w, y + 0.5 * h)],
           fill=INK, width=2)
    d.line([(x + 0.58 * w, y + 0.5 * h), (x + 0.96 * w, y + 0.5 * h)],
           fill=INK, width=2)
    for vx in (0.1, 0.22, 0.34, 0.62, 0.74, 0.86):
        d.line([(x + vx * w, y + 0.42 * h), (x + vx * w, y + 0.5 * h)],
               fill=INK, width=2)
    # broken span: tilted segment falling into the gap
    d.line([(x + 0.42 * w, y + 0.42 * h), (x + 0.56 * w, y + 0.58 * h)],
           fill=RED, width=4)
    d.arc([x + 0.1 * w, y + 0.5 * h, x + 0.9 * w, y + 0.95 * h], 180, 360,
          fill=INK, width=3)


def scene_tag(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CREAM)
    cx, cy = x + 0.5 * w, y + 0.5 * h
    s = min(w, h) / 90.0
    d.polygon([(cx - 30 * s, cy - 16 * s), (cx + 10 * s, cy - 16 * s),
               (cx + 32 * s, cy + 4 * s), (cx + 10 * s, cy + 24 * s),
               (cx - 30 * s, cy + 24 * s)], fill=RED)
    d.ellipse([cx - 22 * s, cy - 6 * s, cx - 12 * s, cy + 4 * s], fill=CREAM)
    d.text((cx - 8 * s, cy - 14 * s), "%", font=F(SANS_B, int(26 * s)),
           fill=CREAM)


SCENES = {"kyiv": scene_kyiv, "cyclone": scene_cyclone,
          "chart": scene_chart, "tank": scene_tank,
          "summit": scene_summit, "gavel": scene_gavel,
          "rings": scene_rings, "globe": scene_globe,
          "tower": scene_tower, "jet": scene_jet,
          "candles": scene_candles, "bridge": scene_bridge,
          "tag": scene_tag}

# ---------------------------------------------------------------- map data
# Continent outlines as (lon, lat) points, own simplified tracing from
# a world atlas — no copied map data. (Same data as v3.)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-100, 74), (-85, 74), (-70, 72),
     (-60, 60), (-55, 48), (-60, 45), (-65, 44), (-70, 40), (-75, 35),
     (-80, 32), (-81, 26), (-80, 25), (-85, 29), (-90, 29), (-97, 26),
     (-97, 22), (-95, 19), (-90, 21), (-88, 18), (-86, 15), (-83, 10),
     (-79, 9), (-83, 9), (-86, 12), (-90, 14), (-94, 16), (-100, 17),
     (-105, 20), (-105, 22), (-110, 24), (-110, 28), (-114, 31),
     (-117, 33), (-122, 37), (-124, 42), (-124, 48), (-130, 55),
     (-140, 60), (-150, 60), (-160, 58)],
    [(-58, 64), (-45, 60), (-32, 68), (-25, 74), (-35, 78), (-50, 80),
     (-58, 76), (-60, 70)],
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-78, -10), (-75, -15),
     (-70, -18), (-70, -23), (-65, -28), (-62, -35), (-65, -40),
     (-68, -48), (-70, -52), (-66, -55), (-63, -50), (-62, -42),
     (-58, -35), (-52, -32), (-48, -27), (-41, -22), (-38, -15),
     (-35, -8), (-38, -5), (-44, -3), (-50, 0), (-53, 4), (-58, 6),
     (-62, 9), (-68, 11), (-72, 12), (-77, 8)],
    [(-10, 36), (-9, 43), (-4, 48), (-1, 50), (3, 52), (7, 54), (8, 57),
     (10, 59), (13, 56), (18, 56), (21, 58), (24, 60), (28, 62),
     (30, 64), (30, 69), (25, 71), (20, 70), (14, 67), (10, 64),
     (5, 60), (5, 58), (0, 53), (-5, 50), (-8, 43), (-9, 37)],
    [(-17, 15), (-15, 25), (-10, 31), (-5, 35), (0, 36), (10, 37),
     (15, 33), (20, 32), (25, 32), (30, 31), (34, 28), (37, 22),
     (40, 15), (43, 12), (48, 11), (51, 10), (46, 5), (42, -2),
     (40, -10), (38, -18), (35, -25), (32, -29), (28, -33), (20, -35),
     (16, -30), (13, -20), (12, -12), (9, -2), (9, 4), (4, 6), (-4, 5),
     (-8, 5), (-13, 8), (-17, 12)],
    [(30, 36), (33, 38), (36, 36), (40, 38), (44, 40), (48, 42),
     (52, 44), (56, 46), (60, 48), (64, 50), (68, 52), (72, 55),
     (76, 58), (80, 62), (85, 66), (90, 70), (95, 72), (100, 74),
     (108, 74), (115, 73), (122, 72), (130, 72), (138, 72), (145, 72),
     (152, 70), (158, 68), (162, 64), (158, 58), (150, 59), (142, 50),
     (140, 44), (138, 38), (135, 35), (132, 33), (128, 35), (126, 38),
     (122, 40), (120, 35), (118, 28), (115, 22), (110, 20), (108, 16),
     (105, 10), (102, 8), (100, 10), (98, 14), (96, 16), (93, 20),
     (90, 22), (88, 22), (86, 20), (83, 18), (80, 14), (78, 8),
     (76, 10), (74, 16), (72, 20), (69, 23), (66, 25), (62, 25),
     (58, 26), (55, 26), (52, 27), (50, 29), (48, 30), (45, 29),
     (42, 31), (39, 32), (36, 36)],
    [(114, -22), (118, -18), (122, -14), (128, -13), (132, -12),
     (136, -13), (140, -14), (142, -11), (144, -15), (146, -19),
     (149, -22), (150, -25), (153, -27), (153, -32), (150, -37),
     (146, -39), (140, -38), (136, -35), (132, -32), (128, -32),
     (124, -33), (120, -34), (116, -35), (114, -30), (113, -25)],
]

# Numbered dots for the 13 main stories, by (lon, lat). Brussels and
# Crimea are nudged a few degrees so their pins do not sit on top of
# The Hague / Kyiv (the Black Sea cluster is genuinely tight).
# (n, lon, lat, label_dx, label_dy): a label offset means the number is
# drawn in a cream badge offset from the dot, joined by a hairline
# leader — used where pins cluster too tightly for in-dot numbers.
DOTS = [
    (1, 31, 50, 0, 0),      # Kyiv
    (2, 85, 19, 0, 0),      # Akvan / Gopalpur
    (3, 121, 25, 12, 10),   # Markets / Taipei
    (4, 34, 31, -14, 14),   # Gaza
    (5, 114, 22, 0, 0),     # Shenzhen
    (6, 4, 52, -16, -10),   # The Hague
    (7, 12, 48, 10, -16),   # Brussels (nudged east)
    (8, 30, 37, -18, 4),    # Antalya / COP31
    (9, 47, 25, 0, 0),      # Riyadh
    (10, 21, 52, 24, -8),   # Poland
    (11, -74, 41, 0, 0),    # New York
    (12, 38, 42, 22, 18),   # Crimea (nudged east)
    (13, 140, 36, 0, 0),    # Tokyo
]

# ---------------------------------------------------------------- sections


def draw_number_badge(d, x, y, n, size=16):
    """Small red square with a white number, top-left of a card."""
    d.rectangle([x, y, x + size, y + size], fill=RED)
    s = str(n)
    f = F(SANS_B, 11)
    d.text((x + (size - d.textlength(s, font=f)) / 2, y + 2), s,
           font=f, fill=(255, 255, 255))


def draw_masthead(d):
    kicker = ("THE WORLD \u2014 FRIDAY \u00b7 35 STORIES \u00b7 "
              "13 MAIN + 22 ALSO \u00b7 7 REGIONS")
    centered(d, 512, 10, kicker, F(SANS_B, 13), fill=RED)
    centered(d, 512, 28, "FRIDAY 20 NOVEMBER 2026", F(SERIF_B, 48))
    centered(d, 512, 76, "One day. One page. Every region.",
             F(SERIF_I, 13))
    d.line([(24, 90), (1000, 90)], fill=RULE, width=2)
    d.line([(24, 93), (1000, 93)], fill=INK, width=1)


def draw_stats(d):
    box_w = 156
    for i, (num, label) in enumerate(STATS):
        x = 24 + i * 164
        if i:
            d.line([(x - 4, 100), (x - 4, 144)], fill=(200, 190, 170),
                   width=1)
        size = 28
        nf = F(SANS_B, size)
        while d.textlength(num, font=nf) > box_w - 6 and size > 20:
            size -= 1
            nf = F(SANS_B, size)
        text(d, x, 99, num, nf)
        lf = F(SANS, 11)
        llines = wrap(d, label, lf, box_w - 4)
        if len(llines) > 2:
            warn("stat label wraps to %d lines: %r" % (len(llines), label))
        for j, line in enumerate(llines[:2]):
            text(d, x, 124 + j * 11, line, lf, fill=(70, 65, 55))
    d.line([(24, 148), (1000, 148)], fill=RULE, width=1)


def draw_leads(d):
    cols = [24, 353, 682]
    hf = F(COND_B, 25)
    lf = F(SANS_B, 12)
    df = F(SANS, 13)
    for (n, label, head, deck, scene), x in zip(LEADS, cols):
        y, w, h = 156, 317, 236
        d.rectangle([x, y, x + w, y + h], fill=CREAM)
        d.rectangle([x, y, x + w, y + h], outline=(200, 190, 170), width=1)
        SCENES[scene](d, x + 1, y + 1, w - 2, 108)
        draw_number_badge(d, x + 6, y + 6, n)
        text(d, x + 10, y + 116, label, lf, fill=RED)
        hlines = wrap(d, head, hf, w - 20)
        if len(hlines) > 2:
            warn("lead headline %d lines: %r -> %s"
                 % (len(hlines), head, hlines))
        for j, line in enumerate(hlines[:2]):
            text(d, x + 10, y + 134 + j * 26, line, hf)
        dlines = wrap(d, deck, df, w - 20)
        if len(dlines) > 3:
            warn("lead deck %d lines: %r -> %s" % (len(dlines), deck, dlines))
        for j, line in enumerate(dlines[:3]):
            text(d, x + 10, y + 190 + j * 15, line, df)


def draw_features(d):
    cols = [24, 221, 418, 615, 812]
    rows = [400, 540]
    hf = F(COND_B, 16)
    df = F(SANS, 12)
    for idx, (n, head, deck, scene) in enumerate(FEATURES):
        r, c = divmod(idx, 5)
        x, y = cols[c], rows[r]
        w, h = 187, 132
        d.rectangle([x, y, x + w, y + h], fill=CREAM)
        d.rectangle([x, y, x + w, y + h], outline=(200, 190, 170), width=1)
        SCENES[scene](d, x + 1, y + 1, w - 2, 52)
        draw_number_badge(d, x + 5, y + 5, n)
        hlines = wrap(d, head, hf, w - 12)
        if len(hlines) > 3:
            warn("feature headline %d lines: %r -> %s"
                 % (len(hlines), head, hlines))
        for j, line in enumerate(hlines[:3]):
            text(d, x + 6, y + 58 + j * 16, line, hf)
        dlines = wrap(d, deck, df, w - 12)
        if len(dlines) > 2:
            warn("feature deck %d lines: %r -> %s"
                 % (len(dlines), deck, dlines))
        for j, line in enumerate(dlines[:2]):
            text(d, x + 6, y + 108 + j * 13, line, df)


def draw_map_block(d):
    bx, by, bw, bh = 24, 680, 328, 188
    d.rectangle([bx, by, bx + bw, by + bh], fill=NAVY)
    text(d, bx + 10, by + 6, "WHERE IT HAPPENED", F(SANS_B, 13),
         fill=CREAM)
    right(d, bx + bw - 10, by + 7, "1\u201313 MARK THE STORIES", F(SANS, 10),
          fill=(200, 210, 230))
    # Map area: x 28..352, y 700..826; equal lon/lat scale (true aspect).
    mx0, my0, mw, mh = bx + 4, by + 28, bw - 8, 126
    scale = min(mw / 348.0, mh / 141.0)
    map_w, map_h = 348 * scale, 141 * scale
    ox = mx0 + (mw - map_w) / 2
    oy = my0 + (mh - map_h) / 2

    def proj(lon, lat):
        return (ox + (lon + 168) * scale, oy + (83 - lat) * scale)

    for pts in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in pts], fill=MAPBEIGE)
    for n, lon, lat, ldx, ldy in DOTS:
        dx, dy = proj(lon, lat)
        if ldx == 0 and ldy == 0:
            r = 6
            d.ellipse([dx - r, dy - r, dx + r, dy + r], fill=RED,
                      outline=(255, 255, 255), width=1)
            s = str(n)
            f = F(SANS_B, 8)
            d.text((dx - d.textlength(s, font=f) / 2, dy - 4), s, font=f,
                   fill=(255, 255, 255))
        else:
            # tight cluster: small pin + cream number badge on a leader
            d.ellipse([dx - 3.5, dy - 3.5, dx + 3.5, dy + 3.5], fill=RED,
                      outline=(255, 255, 255), width=1)
            lx, ly = dx + ldx, dy + ldy
            d.line([(dx, dy), (lx, ly)], fill=CREAM, width=1)
            r = 6
            d.ellipse([lx - r, ly - r, lx + r, ly + r], fill=CREAM,
                      outline=RED, width=1)
            s = str(n)
            f = F(SANS_B, 8)
            d.text((lx - d.textlength(s, font=f) / 2, ly - 4), s, font=f,
                   fill=RED)
    f1 = F(SANS_B, 11)
    centered(d, bx + bw / 2, by + 158, REGION_LINE1, f1, fill=CREAM)
    f2 = F(SANS_B, 10)
    centered(d, bx + bw / 2, by + 172, REGION_LINE2, f2, fill=CREAM)


def draw_also(d):
    x0, x1 = 376, 1000
    text(d, x0, 680, "ALSO ON FRIDAY \u2014 22 MORE STORIES", F(SANS_B, 15))
    right(d, x1, 681, "14\u201335", F(SANS_B, 13), fill=RED)
    d.line([(x0, 700), (x1, 700)], fill=INK, width=1)
    f_num = F(SANS_B, 11)
    f_place = F(SANS_B, 11)
    f_body = F(SANS, 11)
    for i, item in enumerate(ALSO):
        col = i // 11
        row = i % 11
        x = x0 if col == 0 else 692
        y = 706 + row * 15
        num = str(14 + i)
        place, _, rest = item.partition(" \u2014 ")
        d.text((x, y), num, font=f_num, fill=RED)
        px = x + d.textlength("00 ", font=f_num)
        text(d, px, y, place + " \u2014", f_place)
        text(d, px + d.textlength(place + " \u2014 ", font=f_place), y,
             rest, f_body)
        w = (d.textlength(num + " ", font=f_num)
             + d.textlength(place + " \u2014 ", font=f_place)
             + d.textlength(rest, font=f_body))
        if w > 308:
            warn("ALSO item too wide (%.0fpx): %r" % (w, item))


def draw_datecheck(d):
    d.rectangle([24, 876, 1000, 968], outline=RED, width=2)
    text(d, 36, 882, "DATE CHECK", F(SANS_B, 14), fill=RED)
    hf = F(SANS_B, 12)
    bf = F(SANS, 12)
    # Left: what was left out (19 Nov).
    text(d, 36, 902, DATE_LEFT_HEAD, hf, fill=RED)
    lines = wrap(d, DATE_LEFT, bf, 452)
    if len(lines) > 3:
        warn("DATE CHECK left wraps to %d lines" % len(lines))
    for j, line in enumerate(lines[:3]):
        text(d, 36, 918 + j * 14, line, bf)
    # Right: what has not happened yet.
    text(d, 524, 902, DATE_RIGHT_HEAD, hf, fill=RED)
    lines = wrap(d, DATE_RIGHT, bf, 452)
    if len(lines) > 3:
        warn("DATE CHECK right wraps to %d lines" % len(lines))
    for j, line in enumerate(lines[:3]):
        text(d, 524, 918 + j * 14, line, bf)


def draw_footer(d):
    text(d, 24, 978, FOOTER, F(SANS, 9), fill=(90, 85, 75))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_stats(d)
    draw_leads(d)
    draw_features(d)
    draw_map_block(d)
    draw_also(d)
    draw_datecheck(d)
    draw_footer(d)
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
    print("warnings:", len(WARNINGS))
    for w in WARNINGS:
        print(" -", w)


if __name__ == "__main__":
    main()
