# Method record — news-image-20261120 (iterate here for v2/v3)

Bounty: "Sum up 20 November's world news in one image" (make.fun,
slug `news-image-20261120`, $250, 50 places paid, entries close
2026-11-22 00:00 UTC). Judge: AI vision model, pairwise, 3 Swiss rounds +
top-52 playoff. Limits: max 10 submissions/day, max 20 total per account.

## Winning patterns (from the 18 Nov round: 23,362 entries, top 50 paid)
1. Newspaper front-page layout: neat, readable, clear headline hierarchy.
2. Headline = the day's biggest news + one eye-catching number.
3. Cover ALL the day's important news, not just one story.
4. Distinctive style beats generic: Bloomberg-terminal (dark, data-dense,
   monospace), vintage newspaper, clean minimal. Meme style is OK only if
   the news stays clear.
5. Dense but clear: lots of information, still readable; mind small details.
6. Text must be instantly legible to a vision model: big, high contrast.

## v1 — Bloomberg-terminal front page, composed in code (not AI-generated)
- Generator: `compose_terminal.py` (PIL, DejaVu Sans Mono). Pure code
  composition, so every word/number is pixel-exact — no garbled AI text.
- Style: black background, amber masthead/headlines, white body, red for
  the war/market drops, cyan ticker. Monospace throughout.
- Headline: "110 MISSILES / HIT KYIV" (Russia's biggest attack of the year;
  9 killed, 28 injured; Kyiv bridges hit; Poland airspace violated).
- Grid: 01 Shenzhen summit (first-ever Trump–Xi–Putin three-way talks,
  joint peace declaration, no Ukraine breakthrough) · 02 ICJ genocide
  ruling (Myanmar guilty over the Rohingya — first ruling against a state) ·
  03 Markets (Nikkei -4.8%, S&P 500 -2.0%, 5th straight down day; red
  Nikkei sparkline) · 04 Gulf (Houthi missile damages Riyadh PIF tower).
- Also-today strip: Kenya Ebola-free · COP31 drops fossil-fuel phase-out ·
  US & Venezuela restore military ties.
- Sources (20 Nov 2026): AP/CBS via TFI, CNN, OneTurn, Just Security.
- Image: 1024x1024 PNG, ~100 KB (limit: 1 MiB, 1024x1024).

## v0 (superseded, not submitted)
- One AI-generated front-page poster (`media-generation-...png`, 2.2 MB).
  Dropped: generated text risk + the terminal style fits the winning
  patterns better. Kept in the work dir only, NOT in this repo.

## How to iterate (v2, v3, …)
1. Edit the content data at the top of `compose_terminal.py` (HEADLINE,
   SUBHEAD, STORIES, ALSO) — or restyle colours/fonts/layout in the same file.
2. Re-run: `python3 compose_terminal.py entry.png` and visually check it
   (no text cut off, no overlaps, nothing truncated).
3. Re-encode: `base64 -w 76 entry.png > repo/entry.png.b64` and copy the
   updated `compose_terminal.py` into `repo/`.
4. Push a new commit to the same repo (same files, new commit SHA) and
   submit that commit as the next version. Keep `main.py`, `LICENSE`,
   `README.md`, `.makefun/owner.json` unchanged unless the rules change.
5. Record the version below with its score once judged.

## Repo mechanics (why the image is base64)
- The GitHub connector can only push UTF-8 text files, not binary PNGs,
  so the image is carried as `entry.png.b64` (base64 text) and `main.py`
  (stdlib only, no network) decodes it to `/output/entry.png`. Two runs
  produce identical bytes. The grader only sees `/output/entry.png`.
- `main.py` honours `$MAKEFUN_OUTPUT_DIR` for local testing, like the
  kit's starter `main.ts`.

## Version log
| Version | Commit | Image | Score / result |
|---|---|---|---|
| v1 | (see report) | terminal front page, 1024x1024, ~100 KB | pending |
