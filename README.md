# Friday 20 November 2026 — the world in one image

A single 1024×1024 front page that sums up Friday 20 November 2026.
The lead is the overnight missile attack on Kyiv, with 110+ missiles
fired, 9 people killed and 28 hurt, and 3 bridges across the Dnipro hit.
Around it sit 12 more main stories and 22 shorter ones, 35 in total,
covering Europe, Asia, the Americas, Africa, the Middle East, Oceania
and space. A DATE CHECK strip at the bottom keeps every story on the
day it really happened, so nothing from 19 November is passed off as
20 November news.

## How to run it

```sh
python3 main.py
```

The program writes the image to /output/entry.png. It needs no network
and writes the same bytes on every run. The image data is stored in
entry.png.b64 beside it, and main.py decodes it with the standard
library only.

## Files

- main.py — the entry program
- compose_v2.py — the script that drew the front page
- entry.png.b64 — the finished image, base64
- METHOD.md — how the stories were checked and chosen
