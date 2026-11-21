# Method record — news-image-20261120 (v2)

Bounty: "Sum up 20 November's world news in one image" (make.fun,
slug `news-image-20261120`, $250, 50 places paid, entries close
2026-11-22 00:00 UTC). Judge: AI vision model, pairwise, 3 Swiss rounds +
top-52 playoff. Limits: max 10 submissions/day, max 20 total per account.

## Winning patterns (from the 18 Nov round: 23,362 entries, top 50 paid)
1. Newspaper front-page layout: neat, readable, clear headline hierarchy.
2. Headline = the day's biggest news + one eye-catching number.
3. Cover ALL the day's important news, not just one story.
4. Distinctive style beats generic: Bloomberg-terminal (dark, data-dense,
   monospace), vintage newspaper, clean minimal.
5. Dense but clear: lots of information, still readable; mind small details.
6. Text must be instantly legible to a vision model: big, high contrast.

## v4 — beige-paper redesign after a fresh top-3 study (v3 provisional
97.2784%, 12 games 11 won, 1 drawn, 0 lost; paid top-50 cutoff then
~98.87%)
- Generator: `compose_v4.py` (same Pillow setup as v3). No fact, number
  or date changed from v2/v3 — only layout/craft.
- Warm beige paper; the date itself is the masthead ("FRIDAY 20
  NOVEMBER 2026", largest text); thin red rules between sections.
- Three equal lead cards (Kyiv, Cyclone Akvan, AI sell-off), each with
  a code-drawn flat scene illustration across the top half of the card
  (night Kyiv skyline with missile trails and fire glow; cyclone spiral
  over the Bay of Bengal; red falling chart). The single giant red 110+
  lead and the oversized headline are gone.
- All 10 feature tiles get flat scene illustration banners too
  (tank, summit flags, gavel, interlocking rings, globe + thermometer,
  tower with smoke, jet + radar arcs, candlesticks, broken bridge,
  price tag) — no more ~30px pictogram icons.
- A real map block: navy panel, beige continents at true aspect,
  red numbered dots 1–13 for the 13 main stories (tight Black Sea /
  East Asia pins use cream number badges on leader lines so the
  numbers stay readable); region counts underneath, unchanged.
- ALSO is numbered 14–35, two columns, and the totals are now honest:
  v3's box said "13 MAIN + 21 ALSO = 34" but the Kyiv lead + 13 tiles
  + 21 ALSO was really 35 stories. v4 has 13 main cards (3 leads + 10
  features) and 22 ALSO (BepiColombo moves down to ALSO as item 35),
  total 35 — the same 35-item list the v2 plan locked, so region counts
  are unchanged: Europe 8 · Asia 7 · Americas 7 · Africa 5 ·
  Space/Global 4 · Middle East 3 · Oceania 1.
- DATE CHECK is a red-bordered box with two parts: NOT 20 NOV — LEFT
  OUT (Myanmar ruling, Shenzhen summit, PIF Tower strike, Anthropic
  IPO first trade, Crimea bridge strike — all 19 Nov) and NOT YET —
  DUE 21 NOV (BepiColombo capture; COP31 final text not agreed at
  press time).
- `entry.png.b64` is written as ONE single line, as in v3.
- Image: 1024x1024 PNG, ~195 KB. 300 px preview test passed (see report).

## v3 — same front page, craft fixes (provisional rate of v2: 97.5354%,
12 games 10 won, 2 drawn, 0 lost; paid top-50 cutoff then 98.8722%)
- Generator: `compose_v3.py` (same Pillow setup as v2). No fact, number
  or date changed from v2 — only layout/craft.
- Map: continents are now drawn from longitude/latitude outlines
  (own simplified tracing) instead of schematic blobs, so the strip
  reads as a recognisable world map; the 8 story dots are placed by
  longitude/latitude (Kyiv, Shenzhen, The Hague, Riyadh, Gaza,
  Gopalpur, Tokyo, New York). Region counts unchanged: Europe 8 ·
  Asia 7 · Americas 7 · Africa 5 · Space/Global 4 · Middle East 3 ·
  Oceania 1.
- No duplicate: tile 1 is now the Gaza tank story promoted from the
  ALSO list ("GAZA — TANKS CROSS YELLOW LINE", first ground crossing
  since the Oct 2025 truce; army says a tunnel was demolished; Hamas
  calls it a violation), with its own code-drawn flat tank icon. The
  v2 tile 1 repeated the lead Kyiv headline. ALSO drops to 21 items;
  total is 34 stories; recap box reads 34 STORIES / 13 MAIN + 21 ALSO.
- `entry.png.b64` is written as ONE single line: a wrapped base64 file
  counts as thousands of unwritten lines in the transcript gate, and
  the image itself counts as one line.
- Image: 1024x1024 PNG, ~238 KB. 300 px preview test passed (see report).

## v2 — classic newspaper front page, composed in code (not AI-generated)
- Generator: `compose_v2.py` (Pillow; Liberation Serif/Sans + Noto Serif
  Condensed Bold). Pure code composition, so every word/number is
  pixel-exact — no garbled AI text. White paper, black ink, one red
  accent only (the lead number 110+).
- Masthead: "FRIDAY EDITION" with the full date "FRIDAY 20 NOVEMBER 2026".
- Lead: Kyiv, 110+ missiles and 400+ drones overnight; 9 killed, 28 hurt;
  **3 bridges hit** (Podilsko-Voskresenskyi, Darnytskyi, Pivdennyi) —
  v1 wrongly said a bridge was destroyed; none was reported destroyed.
- 6-stat strip: 110+ missiles · 9 killed · 3 bridges hit · 300,000+
  evacuated in Odisha · Taiex −6.2% · Anthropic IPO $81.3bn.
- 13 main illustrated stories in a 3-column grid, each with a small flat
  illustration drawn in code (bridge, summit table, gavel, chart, cyclone,
  deal rings, globe, tower, jet, candlesticks, rail bridge, planet,
  price tag) — no copied images.
- World-map strip: schematic continents drawn in code, 8 story dots,
  region counts Europe 8 · Asia 7 · Americas 7 · Africa 5 · Space/Global 4
  · Middle East 3 · Oceania 1 = 35 stories.
- ALSO ON FRIDAY: 22 one-liners, taking the total from 13 to 35 stories.
- DATE CHECK box: every story kept on its real date — 19 Nov: ICJ Myanmar
  ruling, Shenzhen summit, PIF Tower strike, Anthropic first trade, Crimea
  bridge strike, Bukele registration. 18 Nov: Sudan gold-mine drone,
  US–Venezuela deal, Fiji disaster declared. 11 Nov: Kenya's last Ebola
  patient discharged. 21 Nov (tomorrow): BepiColombo Mercury orbit capture.
- Sources (20 Nov 2026): Reuters, AP, CNN, BBC, UNICEF, IMD, Statistics
  Bureau of Japan, Fiji Government. Conservative closes used where wires
  disagreed (Taiex −6.2%, Kospi −5.2%, Nikkei −4.8%, S&P 500 −2.0%,
  6th straight loss per Reuters); single-wire extremes not printed.
- Image: 1024x1024 PNG, ~235 KB (limit: 1 MiB, 1024x1024).
- Type floors kept: lead headline 64 px, tile headlines 22 px, decks
  15 px, ALSO 14 px, DATE CHECK 13 px. 300 px preview test passed:
  masthead date, lead 110+, and all 6 stat numbers still readable.
- Wording shortened only to fit the layout (never the numbers): 4 tile
  headlines trimmed ("AI SELL-OFF SWEEPS ASIA" → "AI SELL-OFF IN ASIA",
  "WEAPONS CROSS NATO AIRSPACE" → "NATO AIRSPACE BREACH",
  "ANTHROPIC'S RECORD DEBUT" → "RECORD IPO DEBUT",
  "THIRD BRIDGE STRIKE IN A WEEK" → "3RD BRIDGE STRIKE"); decks
  condensed from the plan decks with all figures unchanged; the Kenya
  Mrima Hill item says "$60bn+ deposits" (in the ground, not revenue).
- Nothing copied from the leaderboard's top entries: own masthead name,
  own layout, own wording, own illustrations; only the structural idea
  (newspaper front page, region counts, DATE CHECK) follows the pattern
  the 18 Nov round rewarded.

## v1 — Bloomberg-terminal front page (superseded)
- Black background, amber masthead, monospace. Covered ~5 stories, said
  "a Kyiv bridge destroyed" (wrong: 3 hit, none reported destroyed),
  dated nothing, no region counts, no map, no DATE CHECK, no ALSO list.
  See the v1 report for details.

## How to iterate (v4, …)
1. Edit the content data at the top of `compose_v4.py` (STATS, LEADS,
   FEATURES, ALSO, DATE_LEFT/DATE_RIGHT) — or restyle colours/fonts/
   layout in the same file.
2. Re-run: `python3 compose_v4.py entry.png` and visually check it
   (the script warns on any headline/deck wrapping past its line cap,
   any ALSO item wider than its column, any DATE CHECK past 3 lines).
3. Re-encode as ONE line: `python3 -c "import base64; open('entry.png.b64','w').write(base64.b64encode(open('entry.png','rb').read()).decode())"` — never wrap it (wrapped base64 counts as
   thousands of unwritten lines in the transcript gate).
4. Push a new commit to the same repo (same files, new commit SHA) and
   submit that commit as the next version. Keep `main.py`, `LICENSE`,
   `README.md`, `.makefun/owner.json` unchanged unless the rules change.
5. Record the version below with its score once judged.

## Repo mechanics (why the image is base64)
- The GitHub connector can only push UTF-8 text files, not binary PNGs,
  so the image is carried as `entry.png.b64` (base64 text) and `main.py`
  (stdlib only, no network) decodes it to `/output/entry.png`. Two runs
  produce identical bytes. The grader only sees `/output/entry.png`.
- `main.py` honours `$MAKEFUN_OUTPUT_DIR` for local testing, checks the
  PNG magic, and writes atomically (temp file + rename).

## Version log
| Version | Commit | Image | Score / result |
|---|---|---|---|
| v1 | 1b1d2263a5287e19a87f2697d5b16d921b56d01b | terminal front page, 1024x1024, ~100 KB | not submitted (superseded by v2) |
| v2 | 5e7b84fc2b21ff7941e82bcc4fe4696a74b80e8f | newspaper front page, 1024x1024, ~235 KB, 35 stories | provisional 97.5354% (10W 2D 0L of 12); top-50 cutoff then 98.8722% |
| v3 | (see report) | newspaper front page, 1024x1024, ~238 KB, 34 stories, real map, Gaza tile | provisional 97.2784% (11W 1D 0L of 12); top-50 cutoff then ~98.87% |
| v4 | (see report) | beige-paper front page, 1024x1024, ~195 KB, 35 stories, 3 illustrated leads, real map block, boxed DATE CHECK | pending |
