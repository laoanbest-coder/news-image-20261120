[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/laoanbest-coder/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/laoanbest-coder/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# Friday 20 November 2026 — the world in one image

One 1024×1024 front page for Friday 20 November 2026. The lead is
the overnight attack on Kyiv: 110+ missiles fired, 9 killed, 28 hurt,
3 bridges across the Dnipro hit. Thirteen main stories and 21 shorter
ones add up to 34, spanning Europe, Asia, the Americas, Africa, the
Middle East, Oceania and space — with a world map, region counts and
a DATE CHECK strip that keeps every story on the day it really
happened, so 19 November news is never passed off as 20 November news.

## How to run it

```sh
python3 main.py
```

The program writes the image to /output/entry.png. It needs no network
and writes the same bytes on every run. The image data sits in
entry.png.b64 beside it, and main.py decodes it with the standard
library only.

## Files

- main.py — the entry program
- compose_v3.py — the script that drew the front page
- entry.png.b64 — the finished image, base64, one line
- METHOD.md — how the stories were checked and chosen
