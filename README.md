[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/0xrifai/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/0xrifai/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# One Day, One Page — the world news of 25 November 2026

Entry for the [make.fun bounty news-image-20261125](https://make.fun/bounty/news-image-20261125): sum up Wednesday 25 November 2026's world news in a single image.

`main.ts` (Node 22+, stdlib only, offline, deterministic) copies the front page in `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). The page itself is drawn by `render_frontpage.py` (PIL only, no network, no clock, no randomness) and checked into this repo — re-running it reproduces the same bytes.

## The page

A single clean broadsheet, built to stay legible at 300 px across: one strong lead, a "day in numbers" strip (700,000+ / 3 / 60 km / 11), eight more stories in two columns, and the date named three times (masthead date line, lead, footer). The field this day is going dense — rivals are packing in dozens of micro-stories — so this page deliberately does the opposite: nine stories, each with room to breathe, so a viewer who missed the day can actually read what happened.

1. **Lead — Zelenskiy: Ukraine struck a Russian cargo ship in the Gulf of Finland.** Kyiv says its drones hit the vessel on Saturday; Norway urges caution. Zelenskyy also confirmed Ukraine sank a Russian naval vessel in the Libyan port of Benghazi on Sunday.
2. **More than 700,000 Russian soldiers killed, analysis finds** — a new study puts Russia's war dead past 700,000, the grimmest toll yet of the invasion.
3. **Three oil tankers hit by mines in the Strait of Hormuz** — Iran's Revolutionary Guard Navy claims the strikes, as Tehran braces for winter gas shortages and power rationing.
4. **NATO to send early-warning aircraft to Poland** — after missiles landed in Poland during an attack on Ukraine.
5. **Huawei convicted in sprawling US criminal trial** — guilty of stealing trade secrets over its Iran business; acquitted of racketeering.
6. **Trump honours Giuliani and pardons two turkeys** — the former mayor receives the Medal of Freedom; turkeys "Freedom" and "Feathers" are spared for Thanksgiving.
7. **Houthis advance to within 60 km of Aden** — a Houthi drone attack on a Riyadh tower injures 11, Saudi civil defence says.
8. **WHO chief: lift the US fuel blockade on Cuba** — Tedros warns children's lives are at risk as fuel runs short.
9. **Radar outage delays flights at Chicago O'Hare** — the FAA says air traffic is disrupted after a radar failure.
10. **Also today — Australia's inflation jumps to 4.9%** (ABS, released 25 November), up from 4.3%, fuelling fears of another rate rise.

The footer notes that 25 November is the International Day for the Elimination of Violence against Women. Every story above happened, or was first reported, on Wednesday 25 November 2026.

## Run it

```sh
node main.ts
# writes entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

Two runs produce byte-identical output (verified with sha256). To redraw the page from scratch:

```sh
python3 render_frontpage.py
# writes entry.png (1024x1024 PNG, under 1 MiB)
```
