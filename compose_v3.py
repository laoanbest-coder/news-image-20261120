#!/usr/bin/env python3
"""Compose v3: newspaper front page, 20 November 2026 world news.

Pure-code composition with Pillow (no AI-generated image, no network):
every word and number is drawn from the verified fact list in the build
plan, so text is pixel-exact. White paper, black ink, one red accent
(the lead number 110+ only).

v3 changes vs v2 (craft only — no fact, number or date changed):
- the world-map strip now draws recognisable continent outlines from
  longitude/latitude data instead of schematic blobs;
- the duplicate Kyiv tile is replaced by the Gaza tank story promoted
  from the ALSO list (ALSO drops to 21 items, total 34 stories);
- the recap box reads 34 STORIES / 13 MAIN + 21 ALSO.

Layout (1024x1024):
  masthead 0-76 | lead Kyiv 76-268 | 6-stat strip 268-328 |
  13-story grid 328-728 | world-map strip 728-790 |
  ALSO list 790-974 | DATE CHECK 974-1012 | sources footer 1012-1024

Usage: python3 compose_v3.py [out.png]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
INK = (0, 0, 0)
RED = (178, 34, 34)
PAPER = (255, 255, 255)
PANEL = (238, 238, 234)
MAPFILL = (188, 188, 183)
RULE = (170, 170, 165)
GREY = (110, 110, 105)

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
# 6 big-number stats: (number, label <= ~44 chars so it wraps to 2 lines)
STATS = [
    ("110+", "missiles fired at Ukraine overnight"),
    ("9", "killed nationwide; 28 injured"),
    ("3", "Kyiv bridges hit across the Dnipro"),
    ("300,000+", "moved to shelters in Odisha"),
    ("\u22126.2%", "Taiwan Taiex on Friday"),
    ("$81.3bn", "Anthropic IPO, largest ever"),
]

# 13 main stories: (headline, deck, icon key). Decks condensed from the
# verified plan decks to fit 2 lines at 15 px; every number is unchanged.
# v3: tile 1 is the Gaza tank story promoted from the ALSO list (the v2
# tile 1 repeated the lead Kyiv headline); the Gaza ALSO line is removed.
TILES = [
    ("GAZA \u2014 TANKS CROSS YELLOW LINE",
     "First ground crossing since the Oct 2025 truce; army says a tunnel "
     "was demolished; Hamas calls it a violation.",
     "tank", True),
    ("SHENZHEN: TRUMP\u2013XI\u2013PUTIN MEET",
     "19 Nov: 90 min at Kylin Villa; backs nuclear talks, UN reform.",
     "summit", False),
    ("THE HAGUE: MYANMAR GUILTY OF GENOCIDE",
     "19 Nov: ICJ, 9\u20136 \u2014 first state found guilty; reparations ordered.",
     "gavel", False),
    ("MARKETS: AI SELL-OFF IN ASIA",
     "Taiex \u22126.2%, Kospi \u22125.2%, Nikkei \u22124.8%; S&P \u22122.0%, 6th straight loss.",
     "chart", False),
    ("INDIA: CYCLONE AKVAN HITS ODISHA",
     "Landfall near Gopalpur; 70\u201380 km/h winds; 300,000+ out, no deaths.",
     "cyclone", False),
    ("BRUSSELS: EU\u2013UK RESET DEAL SEALED",
     "Food checks from Mar 2028, \u00a35.1bn a year; youth scheme agreed.",
     "rings", False),
    ("ANTALYA: COP31 ENDS WITH NO EXIT PLAN",
     "Final draft drops fossil-fuel phase-out; talks run into overtime.",
     "globe", False),
    ("RIYADH: STRIKE HITS TALLEST TOWER",
     "19 Nov: PIF Tower hit; windows out on 7\u20138 floors; no injuries.",
     "tower", False),
    ("POLAND: NATO AIRSPACE BREACH",
     "3 objects cross in; Kh-101 found; jets scrambled, no injuries.",
     "jet", False),
    ("NEW YORK: RECORD IPO DEBUT",
     "19 Nov: largest IPO ever, $81.3bn; priced $83, closed $97.17, +17%.",
     "candles", False),
    ("CRIMEA: 3RD BRIDGE STRIKE",
     "19 Nov: Neptune missiles damage rail tracks on the Kerch bridge.",
     "railbridge", False),
    ("SPACE: BEPICOLOMBO DUE AT MERCURY",
     "Due tomorrow: after 8 years, 10bn km, twin orbiters near Mercury.",
     "planet", False),
    ("TOKYO: JAPAN INFLATION STAYS HIGH",
     "Oct CPI: headline 2.3%, core 2.2%; Dec rate hike expected.",
     "tag", False),
]

# ALSO list: 21 one-liners, each <= ~68 chars to fit one 14 px line.
# v3: Gaza moved up to a main tile, so it is no longer listed here.
ALSO = [
    "SENEGAL \u2014 Boat capsizes off Yenne; 4 dead, dozens missing.",
    "SUDAN \u2014 Drone strike on Bajoun gold mine kills at least 10.",
    "CARACAS \u2014 US and Venezuela sign military-cooperation deal.",
    "SAN SALVADOR \u2014 Bukele registers for a third term; vote Feb 2027.",
    "NAIROBI \u2014 Kenya's last Ebola patient went home 11 Nov.",
    "KENYA \u2014 Frontier Minerals wins Mrima Hill tender; $60bn+ deposits.",
    "SHENZHEN \u2014 Philippines and Chile sign a trade deal.",
    "ITALY \u2014 CGIL general strike in 100+ cities over pay, services.",
    "PACIFIC \u2014 Fiji declares disaster; Tonga emergency as drought bites.",
    "KYIV \u2014 UNICEF: 1,144 children killed or injured, Jan\u2013Oct 2026.",
    "HORMUZ \u2014 Iran war in 9th month; tanker attacks continue; Brent ~$90.",
    "VIENNA \u2014 IAEA: North Korea expanding enrichment at Yongbyon.",
    "COPENHAGEN \u2014 Denmark ratifies Greenland security deal with US.",
    "NEW YORK \u2014 Race for UN secretary-general stalls after 8 votes.",
    "WASHINGTON \u2014 IMF warns global debt will near 100% of GDP.",
    "WASHINGTON \u2014 US Senate passes energy-permitting overhaul, 62\u201333.",
    "BRAS\u00cdLIA \u2014 Brazil's central bank sells $1bn to curb the dollar.",
    "MARKETS \u2014 Gold fell 4.2% for the week; Brent ~$90.05, +0.7%.",
    "WASHINGTON \u2014 Trump pardons late baseball star Pete Rose.",
    "HAITI \u2014 Forces kill 34 suspected gang members in Martissant raid.",
    "SPORT \u2014 Marathon champion Jepchirchir banned 3 years for doping.",
]

DATE_BODY = (
    "20 Nov: Kyiv attack, Akvan, EU\u2013UK deal, COP31, Italy strike, Japan CPI. "
    "19 Nov: Myanmar ruling, Shenzhen summit, PIF Tower, Anthropic debut, "
    "Crimea bridge, Bukele. 18 Nov: Sudan mine drone, US\u2013Venezuela deal, "
    "Fiji disaster. 11 Nov: Kenya Ebola patient home. "
    "21 Nov: BepiColombo due."
)

FOOTER = ("Sources: Reuters, AP, CNN, BBC, UNICEF, IMD, Statistics Bureau of "
          "Japan, Fiji Government. Figures as reported on 20 Nov 2026; early "
          "casualty counts were updated during the day.")

# ---------------------------------------------------------------- icons
# Each icon draws flat black shapes inside a 46x76 panel (x0, y0 = panel
# top-left). Shapes are drawn in a centred 40x40 box (y0+18 .. y0+58).


def icon_bridge(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    d.line([(cx - 19, cy + 12), (cx + 19, cy + 12)], fill=INK, width=3)
    d.arc([cx - 17, cy - 8, cx + 17, cy + 14], 180, 360, fill=INK, width=3)
    for dx in (-10, 0, 10):
        d.line([(cx + dx, cy + 12), (cx + dx, cy - 2)], fill=INK, width=2)
    for dx, dy in ((-14, -14), (0, -18), (14, -14)):
        d.line([(cx + dx - 3, cy + dy), (cx + dx + 3, cy + dy)], fill=INK, width=2)
        d.line([(cx + dx, cy + dy - 3), (cx + dx, cy + dy + 3)], fill=INK, width=2)


def icon_summit(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    d.rectangle([cx - 18, cy + 2, cx + 18, cy + 6], fill=INK)
    d.line([(cx - 14, cy + 6), (cx - 14, cy + 16)], fill=INK, width=2)
    d.line([(cx + 14, cy + 6), (cx + 14, cy + 16)], fill=INK, width=2)
    for dx in (-12, 0, 12):
        d.line([(cx + dx, cy + 2), (cx + dx, cy - 12)], fill=INK, width=2)
        d.polygon([(cx + dx, cy - 12), (cx + dx + 8, cy - 9), (cx + dx, cy - 6)],
                  fill=INK)


def icon_gavel(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    d.line([(cx - 14, cy - 10), (cx + 4, cy - 16)], fill=INK, width=8)
    d.line([(cx - 4, cy - 6), (cx + 12, cy + 12)], fill=INK, width=4)
    d.rectangle([cx - 14, cy + 12, cx + 14, cy + 16], fill=INK)


def icon_chart(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    d.line([(cx - 18, cy - 14), (cx - 18, cy + 14)], fill=INK, width=2)
    d.line([(cx - 18, cy + 14), (cx + 18, cy + 14)], fill=INK, width=2)
    d.line([(cx - 15, cy - 10), (cx - 5, cy - 2), (cx + 3, cy + 2),
            (cx + 15, cy + 10)], fill=INK, width=3)
    d.polygon([(cx + 15, cy + 10), (cx + 8, cy + 8), (cx + 13, cy + 3)],
              fill=INK)


def icon_cyclone(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    for r, a0, a1 in ((16, 20, 300), (11, 200, 120), (6, 20, 300)):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=INK, width=3)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=INK)


def icon_rings(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    d.ellipse([cx - 18, cy - 10, cx - 2, cy + 10], outline=INK, width=3)
    d.ellipse([cx + 2, cy - 10, cx + 18, cy + 10], outline=INK, width=3)


def icon_globe(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], outline=INK, width=3)
    d.ellipse([cx - 6, cy - 15, cx + 6, cy + 15], outline=INK, width=2)
    d.line([(cx - 15, cy), (cx + 15, cy)], fill=INK, width=2)
    d.line([(cx - 13, cy - 8), (cx + 13, cy - 8)], fill=INK, width=1)
    d.line([(cx - 13, cy + 8), (cx + 13, cy + 8)], fill=INK, width=1)


def icon_tower(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    d.rectangle([cx - 8, cy - 18, cx + 8, cy + 16], fill=INK)
    for wy in (-12, -5, 2, 9):
        for wx in (-4, 3):
            d.rectangle([cx + wx - 2, cy + wy - 2, cx + wx + 1, cy + wy + 1],
                        fill=PAPER)
    d.line([(cx + 10, cy - 14), (cx + 5, cy - 6), (cx + 11, cy + 2),
            (cx + 6, cy + 8)], fill=INK, width=2)


def icon_jet(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    d.polygon([(cx + 18, cy - 2), (cx - 14, cy - 10), (cx - 18, cy - 2),
               (cx - 14, cy + 6)], fill=INK)
    d.polygon([(cx - 2, cy - 2), (cx - 8, cy - 14), (cx - 2, cy - 12)],
              fill=INK)
    d.polygon([(cx - 2, cy - 2), (cx - 8, cy + 10), (cx - 2, cy + 8)],
              fill=INK)


def icon_candles(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    for dx, top, bot in ((-13, -6, 10), (0, -14, 4), (13, -2, 14)):
        d.line([(cx + dx, top + cy - 4), (cx + dx, bot + cy + 4)], fill=INK,
               width=2)
        d.rectangle([cx + dx - 4, cy + top, cx + dx + 4, cy + bot], fill=INK)


def icon_railbridge(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    d.line([(cx - 19, cy - 6), (cx + 19, cy - 6)], fill=INK, width=2)
    d.line([(cx - 19, cy - 2), (cx + 19, cy - 2)], fill=INK, width=2)
    for dx in range(-16, 17, 8):
        d.line([(cx + dx, cy - 6), (cx + dx, cy - 2)], fill=INK, width=2)
    d.arc([cx - 15, cy - 2, cx + 15, cy + 16], 180, 360, fill=INK, width=3)
    d.line([(cx - 19, cy + 14), (cx + 19, cy + 14)], fill=INK, width=3)


def icon_planet(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=INK)
    d.arc([cx - 19, cy - 7, cx + 19, cy + 7], 195, 345, fill=INK, width=2)
    d.arc([cx - 19, cy - 7, cx + 19, cy + 7], 15, 165, fill=INK, width=2)
    d.ellipse([cx + 14, cy - 12, cx + 17, cy - 9], fill=INK)


def icon_tank(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    # tracks with wheels
    d.rounded_rectangle([cx - 18, cy + 4, cx + 18, cy + 15], radius=5,
                        fill=INK)
    for wx in (-12, 0, 12):
        d.ellipse([cx + wx - 3, cy + 7, cx + wx + 3, cy + 13], fill=PAPER)
    # hull and turret, barrel pointing right
    d.rectangle([cx - 15, cy - 4, cx + 15, cy + 4], fill=INK)
    d.rectangle([cx - 7, cy - 12, cx + 7, cy - 4], fill=INK)
    d.line([(cx + 7, cy - 8), (cx + 19, cy - 8)], fill=INK, width=3)


def icon_tag(d, x0, y0):
    cx, cy = x0 + 23, y0 + 38
    d.polygon([(cx - 14, cy - 8), (cx + 6, cy - 8), (cx + 16, cy + 2),
               (cx + 6, cy + 12), (cx - 14, cy + 12)], fill=INK)
    d.ellipse([cx - 10, cy - 3, cx - 4, cy + 3], fill=PAPER)
    d.text((cx - 1, cy - 1), "%", font=F(SANS_B, 13), fill=PAPER)


ICONS = {"bridge": icon_bridge, "summit": icon_summit, "gavel": icon_gavel,
         "chart": icon_chart, "cyclone": icon_cyclone, "rings": icon_rings,
         "globe": icon_globe, "tower": icon_tower, "jet": icon_jet,
         "candles": icon_candles, "railbridge": icon_railbridge,
         "planet": icon_planet, "tag": icon_tag, "tank": icon_tank}

# ---------------------------------------------------------------- sections


def draw_masthead(d):
    text(d, 24, 22, "THE WORLD \u2014 FRIDAY", F(SANS_B, 15))
    centered(d, 512, 4, "FRIDAY EDITION", F(SERIF_B, 44))
    right(d, 1000, 20, "FRIDAY 20 NOVEMBER 2026", F(SANS_B, 17))
    centered(d, 512, 54, "One day. One page. Every region.",
           F(SERIF_I, 13))
    d.line([(24, 70), (1000, 70)], fill=INK, width=2)
    d.line([(24, 73), (1000, 73)], fill=INK, width=1)


def draw_lead(d):
    # Left: the one red accent.
    text(d, 24, 82, "110+", F(COND_BLK, 104), fill=RED)
    text(d, 24, 194, "MISSILES FIRED", F(SANS_B, 13))
    text(d, 24, 212, "AT UKRAINE OVERNIGHT", F(SANS_B, 13))
    text(d, 24, 230, "27 BALLISTIC \u00b7 400+ DRONES", F(SANS, 12))
    d.line([(268, 88), (268, 256)], fill=RULE, width=1)
    # Right: kicker, headline, deck.
    text(d, 288, 86, "KYIV \u2014 UKRAINE", F(SANS_B, 14))
    hf = F(COND_B, 64)
    for i, line in enumerate(["RUSSIA'S BIGGEST", "AIR ATTACK THIS YEAR"]):
        w = d.textlength(line, font=hf)
        if w > 712:
            warn("lead headline line too wide: %r %.0fpx" % (line, w))
        text(d, 288, 104 + i * 64, line, hf)
    df = F(SANS, 15)
    deck = ("110+ missiles and 400+ drones overnight; 9 killed, 28 hurt; "
            "3 bridges hit; power and water cut in parts of the capital.")
    lines = wrap(d, deck, df, 712)
    if len(lines) > 2:
        warn("lead deck wraps to %d lines: %s" % (len(lines), lines))
    for i, line in enumerate(lines[:2]):
        text(d, 288, 234 + i * 17, line, df)


def draw_stats(d):
    d.line([(24, 268), (1000, 268)], fill=INK, width=1)
    d.line([(24, 327), (1000, 327)], fill=INK, width=1)
    box_w = 156
    for i, (num, label) in enumerate(STATS):
        x = 24 + i * 164
        if i:
            d.line([(x - 4, 274), (x - 4, 322)], fill=RULE, width=1)
        size = 30
        nf = F(SANS_B, size)
        while d.textlength(num, font=nf) > box_w - 6 and size > 22:
            size -= 1
            nf = F(SANS_B, size)
        text(d, x, 274, num, nf)
        lf = F(SANS, 11)
        llines = wrap(d, label, lf, box_w - 4)
        if len(llines) > 2:
            warn("stat label wraps to %d lines: %r" % (len(llines), label))
        for j, line in enumerate(llines[:2]):
            text(d, x, 302 + j * 11, line, lf, fill=(60, 60, 60))


def draw_grid(d):
    cols = [24, 353, 682]
    rows = [328, 408, 488, 568, 648]
    # Row 1: tile 1 spans 2 cols, tile 2 in col 3. Rows 2-4: 3 tiles each.
    # Row 5: tiles 12, 13 + a black recap box in col 3.
    layout = [(0, 0, 2, TILES[0]), (0, 2, 1, TILES[1]),
              (1, 0, 1, TILES[2]), (1, 1, 1, TILES[3]), (1, 2, 1, TILES[4]),
              (2, 0, 1, TILES[5]), (2, 1, 1, TILES[6]), (2, 2, 1, TILES[7]),
              (3, 0, 1, TILES[8]), (3, 1, 1, TILES[9]), (3, 2, 1, TILES[10]),
              (4, 0, 1, TILES[11]), (4, 1, 1, TILES[12])]
    hf = F(SANS_B, 22)
    df = F(SANS, 15)
    for r, c, span, (head, deck, icon, _wide) in layout:
        x = cols[c]
        y = rows[r]
        w = 317 * span + 12 * (span - 1)
        d.rectangle([x, y, x + 46, y + 76], fill=PANEL)
        ICONS[icon](d, x, y)
        tx = x + 54
        tw = w - 54 - 6
        hlines = wrap(d, head, hf, tw)
        if len(hlines) > 2:
            warn("tile headline %d lines: %r -> %s" % (len(hlines), head, hlines))
        for j, line in enumerate(hlines[:2]):
            text(d, tx, y + 2 + j * 22, line, hf)
        dlines = wrap(d, deck, df, tw)
        if len(dlines) > 2:
            warn("tile deck %d lines: %r -> %s" % (len(dlines), deck, dlines))
        for j, line in enumerate(dlines[:2]):
            text(d, tx, y + 46 + j * 15, line, df)
        d.line([(x, y + 76), (x + w, y + 76)], fill=RULE, width=1)
    for vx in (347, 676):
        d.line([(vx, 328), (vx, 724)], fill=RULE, width=1)
    # Recap box, row 5 col 3.
    bx, by = cols[2], rows[4]
    d.rectangle([bx, by, bx + 317, by + 76], fill=INK)
    centered(d, bx + 158, by + 6, "34 STORIES", F(SANS_B, 26), fill=PAPER)
    centered(d, bx + 158, by + 38, "7 REGIONS \u00b7 ONE DAY", F(SANS_B, 13),
             fill=PAPER)
    centered(d, bx + 158, by + 56, "13 MAIN + 21 ALSO", F(SANS, 11),
             fill=(200, 200, 195))


def _proj(lon, lat):
    """Equirectangular projection into the map strip (x 30..600, y 730..786)."""
    return (30 + (lon + 168) * 1.583, 730 + (83 - lat) * 0.4)


# Continent outlines as (lon, lat) points, own simplified tracing from
# a world atlas — no copied map data. Rendered filled, they read as a
# recognisable world map even at this small size.
CONTINENTS = [
    # North America (Alaska, Arctic coast, east coast, Gulf, Central
    # America, Pacific coast back to Alaska)
    [(-168, 66), (-140, 70), (-120, 72), (-100, 74), (-85, 74), (-70, 72),
     (-60, 60), (-55, 48), (-60, 45), (-65, 44), (-70, 40), (-75, 35),
     (-80, 32), (-81, 26), (-80, 25), (-85, 29), (-90, 29), (-97, 26),
     (-97, 22), (-95, 19), (-90, 21), (-88, 18), (-86, 15), (-83, 10),
     (-79, 9), (-83, 9), (-86, 12), (-90, 14), (-94, 16), (-100, 17),
     (-105, 20), (-105, 22), (-110, 24), (-110, 28), (-114, 31),
     (-117, 33), (-122, 37), (-124, 42), (-124, 48), (-130, 55),
     (-140, 60), (-150, 60), (-160, 58)],
    # Greenland
    [(-58, 64), (-45, 60), (-32, 68), (-25, 74), (-35, 78), (-50, 80),
     (-58, 76), (-60, 70)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-78, -10), (-75, -15),
     (-70, -18), (-70, -23), (-65, -28), (-62, -35), (-65, -40),
     (-68, -48), (-70, -52), (-66, -55), (-63, -50), (-62, -42),
     (-58, -35), (-52, -32), (-48, -27), (-41, -22), (-38, -15),
     (-35, -8), (-38, -5), (-44, -3), (-50, 0), (-53, 4), (-58, 6),
     (-62, 9), (-68, 11), (-72, 12), (-77, 8)],
    # Europe
    [(-10, 36), (-9, 43), (-4, 48), (-1, 50), (3, 52), (7, 54), (8, 57),
     (10, 59), (13, 56), (18, 56), (21, 58), (24, 60), (28, 62),
     (30, 64), (30, 69), (25, 71), (20, 70), (14, 67), (10, 64),
     (5, 60), (5, 58), (0, 53), (-5, 50), (-8, 43), (-9, 37)],
    # Africa
    [(-17, 15), (-15, 25), (-10, 31), (-5, 35), (0, 36), (10, 37),
     (15, 33), (20, 32), (25, 32), (30, 31), (34, 28), (37, 22),
     (40, 15), (43, 12), (48, 11), (51, 10), (46, 5), (42, -2),
     (40, -10), (38, -18), (35, -25), (32, -29), (28, -33), (20, -35),
     (16, -30), (13, -20), (12, -12), (9, -2), (9, 4), (4, 6), (-4, 5),
     (-8, 5), (-13, 8), (-17, 12)],
    # Asia
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
    # Australia
    [(114, -22), (118, -18), (122, -14), (128, -13), (132, -12),
     (136, -13), (140, -14), (142, -11), (144, -15), (146, -19),
     (149, -22), (150, -25), (153, -27), (153, -32), (150, -37),
     (146, -39), (140, -38), (136, -35), (132, -32), (128, -32),
     (124, -33), (120, -34), (116, -35), (114, -30), (113, -25)],
]

# Story dots, by (lon, lat) of the place they mark.
DOTS = [(31, 50), (114, 22), (4, 52), (47, 25), (34, 31), (85, 19),
        (140, 36), (-74, 41)]


def draw_map(d):
    for pts in CONTINENTS:
        d.polygon([_proj(lon, lat) for lon, lat in pts], fill=MAPFILL,
                  outline=INK)
    for lon, lat in DOTS:
        dx, dy = _proj(lon, lat)
        r = 3.5
        d.ellipse([dx - r, dy - r, dx + r, dy + r], fill=INK)
    text(d, 620, 732, "WHERE THE NEWS IS", F(SANS_B, 14))
    text(d, 620, 752, "EUROPE 8 \u00b7 ASIA 7 \u00b7 AMERICAS 7", F(SANS_B, 13))
    line2 = "AFRICA 5 \u00b7 SPACE/GLOBAL 4 \u00b7 MIDDLE EAST 3 \u00b7 OCEANIA 1"
    f2 = F(SANS_B, 12)
    if d.textlength(line2, font=f2) > 380:
        warn("map counts line 2 too wide: %.0fpx"
             % d.textlength(line2, font=f2))
    text(d, 620, 770, line2, f2)


def draw_also(d):
    text(d, 24, 792, "ALSO ON FRIDAY", F(SANS_B, 15))
    d.line([(24, 810), (1000, 810)], fill=INK, width=1)
    f_place = F(SANS_B, 14)
    f_body = F(SANS, 14)
    for i, item in enumerate(ALSO):
        col = i // 11
        row = i % 11
        x = 24 if col == 0 else 512
        y = 814 + int(row * 14.5)
        place, _, rest = item.partition(" \u2014 ")
        w = d.textlength(item, font=f_body)
        if w > 488:
            warn("ALSO item too wide (%.0fpx): %r" % (w, item))
        text(d, x, y, place + " \u2014", f_place)
        text(d, x + d.textlength(place + " \u2014 ", font=f_place), y,
             rest, f_body)


def draw_datecheck(d):
    d.line([(24, 974), (1000, 974)], fill=INK, width=2)
    label = "DATE CHECK \u2014 "
    lf = F(SANS_B, 13)
    bf = F(SANS, 13)
    lw = d.textlength(label, font=lf)
    words = DATE_BODY.split(" ")
    line1, cur = "", ""
    for wd in words:
        cand = (cur + " " + wd).strip()
        if d.textlength(cand, font=bf) <= 976 - lw:
            cur = cand
        else:
            break
    line1 = cur
    remaining = " ".join(words[len(line1.split(" ")):])
    rest = wrap(d, remaining, bf, 976)
    lines = [line1] + rest
    if len(lines) > 2:
        warn("DATE CHECK wraps to %d lines" % len(lines))
    text(d, 24, 979, label, lf)
    text(d, 24 + lw, 979, lines[0], bf)
    if len(lines) > 1:
        text(d, 24, 993, lines[1], bf)
    d.line([(24, 1010), (1000, 1010)], fill=INK, width=1)


def draw_footer(d):
    text(d, 24, 1013, FOOTER, F(SANS, 9), fill=(80, 80, 80))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead(d)
    draw_stats(d)
    draw_grid(d)
    draw_map(d)
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
