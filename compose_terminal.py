#!/usr/bin/env python3
"""Compose the Nov 20 2026 world-news image, v1 — Bloomberg-terminal style.

Method (see METHOD.md for the full record):
  - Pure PIL composition (no AI image generation), so every word and number is
    pixel-exact and legible to the vision-model judge.
  - Style: dark terminal, monospace (DejaVu Sans Mono), amber/white/red/green.
  - Layout: masthead + ticker, one big headline with a key number, 2x2 story
    grid, an "ALSO TODAY" strip, footer.
  - To iterate (v2/v3): edit the STORIES / HEADLINE / ALSO data below, re-run
    this script, re-check the PNG, then re-encode to entry.png.b64.

Usage: python3 compose_terminal.py [output-path]
Default output: entry.png next to this script.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN  # 952

# ---- palette (Bloomberg-terminal) ----
BG = (10, 10, 10)
PANEL = (14, 17, 19)
RULE = (38, 42, 47)
AMBER = (255, 176, 0)
WHITE = (242, 242, 242)
BODY = (215, 215, 215)
MUTED = (154, 160, 166)
CYAN = (77, 208, 225)
RED = (255, 69, 58)
GREEN = (0, 200, 83)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
MONO = f"{FONT_DIR}/DejaVuSansMono.ttf"
MONO_BOLD = f"{FONT_DIR}/DejaVuSansMono-Bold.ttf"

# ---- content (verified against AP/CBS, CNN, OneTurn, Just Security, 20 Nov 2026) ----
MASTHEAD = "THE WORLD TODAY"
DATE = "FRI 20 NOV 2026"
TICKER = "SHENZHEN SUMMIT  \u2022  KYIV  \u2022  ICJ RULING  \u2022  NIKKEI -4.8%  \u2022  RIYADH"

KICKER = "TOP STORY \u2014 UKRAINE WAR"
HEADLINE = ["110 MISSILES", "HIT KYIV"]
SUBHEAD = (
    "Russia launches its biggest attack of the year, hours after the first "
    "Trump\u2013Xi\u2013Putin summit. 9 killed, 28 injured; Kyiv's bridges hit; "
    "Poland scrambles jets as airspace is violated."
)

STORIES = [
    {
        "num": "01",
        "label": "SHENZHEN SUMMIT",
        "title": "THREE LEADERS, ONE TABLE",
        "body": "Trump, Xi & Putin hold first-ever three-way talks; joint peace "
                "declaration, no Ukraine breakthrough.",
    },
    {
        "num": "02",
        "label": "GENOCIDE RULING",
        "title": "MYANMAR GUILTY",
        "body": "The UN's top court finds Myanmar committed genocide against the "
                "Rohingya \u2014 the first such ruling against a state.",
    },
    {
        "num": "03",
        "label": "MARKETS",
        "title": "STOCKS SINK: NIKKEI -4.8%",
        "body": "AI doubts drag global shares down a fifth straight day; S&P 500 -2.0%.",
        "chart": True,
    },
    {
        "num": "04",
        "label": "GULF",
        "title": "MISSILE HITS RIYADH TOWER",
        "body": "A Houthi missile damages Saudi Arabia's sovereign wealth fund tower "
                "in the capital's financial district.",
    },
]

ALSO_LABEL = "ALSO TODAY"
ALSO = ("KENYA EBOLA-FREE  \u2022  COP31 DROPS FUEL PHASE-OUT  "
        "\u2022  US & VENEZUELA DEAL")
FOOTER = "20 NOV 2026  \u2022  THE WORLD IN ONE IMAGE"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, x, y, w, h, story):
    """One story panel: number/label, title, body, optional sparkline chart.

    When a chart is present, the bottom 56 px of the panel is reserved for it
    and the body is capped so it never overlaps the chart.
    """
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=PANEL,
                           outline=RULE, width=1)
    pad = 16
    tx = x + pad
    ty = y + 12
    # label
    f_label = font(MONO_BOLD, 19)
    draw.text((tx, ty), f"{story['num']} / {story['label']}", font=f_label, fill=AMBER)
    ty += 28
    # title
    f_title = font(MONO_BOLD, 25)
    title_lines = wrap(draw, story["title"], f_title, w - 2 * pad)
    for ln in title_lines:
        draw.text((tx, ty), ln, font=f_title, fill=WHITE)
        ty += 30
    ty += 2
    # body (capped to the space above the chart strip, if any)
    reserve = 46 if story.get("chart") else 10
    f_body = font(MONO, 18)
    body_w = w - 2 * pad
    body_lines = wrap(draw, story["body"], f_body, body_w)
    max_body_lines = max(1, (y + h - reserve - ty) // 24)
    for ln in body_lines[:max_body_lines]:
        draw.text((tx, ty), ln, font=f_body, fill=BODY)
        ty += 24
    # sparkline chart for markets, in its own reserved strip
    if story.get("chart"):
        cx0 = x + pad
        cw = w - 2 * pad
        label_y = y + h - 46
        draw.text((cx0, label_y), "NIKKEI 225", font=font(MONO, 15), fill=MUTED)
        cy0, ch = y + h - 28, 20
        for gy in (cy0, cy0 + ch):
            draw.line([(cx0, gy), (cx0 + cw, gy)], fill=(30, 34, 38), width=1)
        pts = [(cx0 + i * cw / 7,
                cy0 + ch * (0.08 + 0.90 * (i / 7) ** 1.1
                            + (0.05 if i in (2, 5) else 0)))
               for i in range(8)]
        draw.line(pts, fill=RED, width=3, joint="curve")
        draw.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
                     fill=RED)


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "entry.png"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    f_mast = font(MONO_BOLD, 58)
    d.text((MARGIN, 30), MASTHEAD, font=f_mast, fill=AMBER)
    f_date = font(MONO_BOLD, 26)
    date_w = d.textlength(DATE, font=f_date)
    d.text((W - MARGIN - date_w, 44), DATE, font=f_date, fill=WHITE)
    # amber rule + ticker
    d.line([(MARGIN, 108), (W - MARGIN, 108)], fill=AMBER, width=3)
    f_tick = font(MONO, 19)
    d.text((MARGIN, 120), TICKER, font=f_tick, fill=CYAN)
    d.line([(MARGIN, 152), (W - MARGIN, 152)], fill=RULE, width=1)

    # ---- headline ----
    y = 166
    d.text((MARGIN, y), KICKER, font=font(MONO_BOLD, 21), fill=RED)
    y += 34
    f_hl = font(MONO_BOLD, 88)
    d.text((MARGIN, y), HEADLINE[0], font=f_hl, fill=AMBER)
    y += 100
    d.text((MARGIN, y), HEADLINE[1], font=f_hl, fill=WHITE)
    y += 100
    f_sub = font(MONO, 23)
    for ln in wrap(d, SUBHEAD, f_sub, CONTENT_W):
        d.text((MARGIN, y), ln, font=f_sub, fill=WHITE)
        y += 31
    y += 6
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)

    # ---- 2x2 story grid ----
    gap = 20
    bw = (CONTENT_W - gap) // 2
    bh = 168
    gy = y + 16
    draw_block(d, MARGIN, gy, bw, bh, STORIES[0])
    draw_block(d, MARGIN + bw + gap, gy, bw, bh, STORIES[1])
    draw_block(d, MARGIN, gy + bh + gap, bw, bh, STORIES[2])
    draw_block(d, MARGIN + bw + gap, gy + bh + gap, bw, bh, STORIES[3])

    # ---- also-today strip (one line) ----
    ay = gy + 2 * bh + gap + 18
    d.line([(MARGIN, ay), (W - MARGIN, ay)], fill=RULE, width=1)
    ay += 14
    d.text((MARGIN, ay), ALSO_LABEL, font=font(MONO_BOLD, 19), fill=AMBER)
    ay += 30
    d.text((MARGIN, ay), ALSO, font=font(MONO, 19), fill=BODY)

    # ---- footer ----
    d.line([(MARGIN, H - 52), (W - MARGIN, H - 52)], fill=RULE, width=1)
    f_foot = font(MONO, 17)
    fw = d.textlength(FOOTER, font=f_foot)
    d.text(((W - fw) / 2, H - 40), FOOTER, font=f_foot, fill=MUTED)

    img.save(out, "PNG", optimize=True)
    print(f"saved {out}  {out.stat().st_size} bytes  {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
