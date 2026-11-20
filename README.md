# Friday 20 November 2026 — the world in one picture

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/sosissausage35-collab/news-image-20261120-r3/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/sosissausage35-collab/news-image-20261120-r3/reward.svg)](https://make.fun/bounty/news-image-20261120)

An entry for the [news-image-20261120 bounty](https://make.fun/bounty/news-image-20261120):
sum up 20 November's world news in one image.

## The picture

A visual-first news poster (1024×1024), drawn entirely in code — no photos,
no downloaded images, no network. One huge hero dominates the top half:
**Cyclone Akvan**, with its spiral storm and the day's biggest human number,
**300,000 evacuated** in India. Below it, six story cards, each with one big
vector icon, a two-word title and one big number. A footer ticker carries three
more of the day's big stories. No paragraphs, no small text — everything stays
readable when the image is shrunk to a ~300px thumbnail.

## The stories (all happened or first reported on Friday 20 November 2026)

| # | Story | Big number on the poster |
|---|-------|--------------------------|
| HERO | **Cyclone Akvan** — 300,000 people evacuated, 423 rescue teams deployed as the cyclone heads for Odisha landfall | 300,000 EVACUATED |
| 1 | **Kyiv hit** — four ballistic missiles strike Kyiv in the early hours | 4 MISSILES |
| 2 | **Drones shut Genoa** — unidentified drones suspend all Genoa airport flights | 4 HOURS |
| 3 | **Houthi hit Riyadh** — drone and missile strikes on four Saudi targets; a Riyadh landmark tower damaged | 4 TARGETS |
| 4 | **Tanker burns** — a tanker catches fire after hitting a mine east of the Strait of Hormuz | HORMUZ MINE |
| 5 | **Anthropic debuts** — the first purely AI company lists on the stock market | +17% |
| 6 | **GTA 6 beats Odyssey** — GTA 6 sales pass The Odyssey's $1.80 billion global run | $1.8 BILLION |
| Footer | **Also today:** Korea's exports top $1 trillion for the first time · Taiwan unveils five measures to calm markets · Europe ready for talks with Russia | — |

## Sources

- Cyclone Akvan evacuation (300,000 / 423 rescue teams): The Hindu, 20 Nov 2026.
- Kyiv ballistic missiles (four, early hours 20 Nov): reported 04:07, 20 Nov 2026;
  corroborated by Daily Baku world roundup, 20 Nov 2026.
- Genoa airport drone shutdown (four hours, overnight 19–20 Nov): reported
  04:22, 20 Nov 2026; corroborated by Daily Baku, 20 Nov 2026.
- Houthi strikes on Riyadh (four targets; landmark tower damaged): reported
  03:47, 20 Nov 2026; corroborated by Daily Baku and The Daily Brief, 20 Nov 2026.
- Tanker fire after mine strike east of the Strait of Hormuz: reported 01:27,
  20 Nov 2026; corroborated by Daily Baku, 20 Nov 2026.
- Anthropic stock-market debut (+17% on debut, Nasdaq: ANT): BBC, 20 Nov 2026;
  SimpleLife.news daily brief, 20 Nov 2026.
- GTA 6 passing The Odyssey's $1.80bn: reported 20 Nov 01:23, 2026.
- Korea exports top $1 trillion (first time): 20 Nov 2026.
- Taiwan market measures (five measures; short-selling limits from 20 Nov):
  20 Nov 2026; SimpleLife.news, 20 Nov 2026.
- Europe ready for talks with Russia on ending the war in Ukraine: BBC,
  20 Nov 2026.
- Research notes: `~/workspace/makefun/news-2026-11-20-r3.md` (builder's copy;
  the round-1/2 research file is `~/workspace/makefun/news-2026-11-20.md`).

Stories from 19 November (Trump–Xi–Putin Shenzhen summit, ICJ Myanmar ruling,
Voyager 1 milestone, Anthropic IPO pricing) were deliberately left out: they are
not 20 November news.

## How to run

```sh
python3 main.py
# writes ./entry.png (1024x1024 PNG, under 1 MiB)

MAKEFUN_OUTPUT_DIR=/output python3 main.py
# writes /output/entry.png
```

Requirements: Python 3.12+ and Pillow (`pip install pillow`). No network access
is used or needed. Fonts: DejaVu Sans (Bold), shipped with the system at
`/usr/share/fonts/truetype/dejavu/`.

## Deterministic

The program uses fixed colours, fixed fonts, fixed coordinates and no
randomness, no clock and no network, so two runs produce byte-identical PNGs.
Verified locally: two runs into different output directories compared with
`cmp` — byte-identical; 98,580 bytes (limit 1 MiB); 1024×1024 (limit
1024×1024); valid PNG; a 300px downscale keeps the date, the hero number and
all six cards readable.

## License

MIT — see [LICENSE](LICENSE).
