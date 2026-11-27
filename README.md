[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/herusetiawan27/news-image-20261127/rank.svg)](https://make.fun/leaderboard)
[![reward](https://make.fun/badge/news-image-20261127/herusetiawan27/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

# news-image-20261127

One image that sums up 27 November 2026's world news — a newspaper front page,
"The World Today", Friday 27 November 2026.

Run `node main.ts` and it writes the image byte-identically to
`/output/entry.png`. No network access at runtime: the image ships in this
repository as `entry.png` (1024x1024) and the entrypoint validates it
(PNG signature, size cap, and a CRC-32 pass over every chunk) before
copying it to the output path.

## The day's stories

All six stories happened or were first reported on Friday 27 November 2026:

- **TWO ITALIANS KILLED IN KUWAIT DRONE STRIKE — IRAN DENIES INVOLVEMENT** — Two Rheinmetall technicians died when drones struck an air-defence surveillance site in Kuwait; Kuwait called it an Iranian attack and Tehran denied any involvement (Reuters / BBC, 27 Nov 2026)
- **EU DEADLOCKED ON BUDGET AND UKRAINE LOAN** — After more than 12 hours of talks in Brussels, EU leaders failed to agree the 2028–34 budget or a new $49 billion loan for Ukraine; Macron set an end-of-year deadline (AP, 27 Nov 2026)
- **THANKSGIVING STORM BATTERS US COASTS** — A coastal storm flooded East Coast towns, brought 70 mph gusts and left over 900,000 customers without power; 400+ flights were cancelled and the Macy's parade was postponed for the first time in 100 years (AP / Reuters, 27 Nov 2026)
- **RULING COALITION FALLS ONE SEAT SHORT** — Final election results gave New Zealand PM Christopher Luxon's coalition 65 of 130 seats, one short of a majority, leaving him reliant on the centrist Opportunity Party (Reuters, 27 Nov 2026)
- **TOKYO EYES $353 BILLION FIVE-YEAR DEFENCE PLAN** — Japan's government is considering ¥56.3 trillion ($353 billion) of defence spending over five years from fiscal 2027, a record plan but below the military's request (Reuters, 27 Nov 2026)
- **SHARES STEADY AS TOKYO INFLATION HITS 16-MONTH HIGH** — Asian shares steadied after a bruising month and the dollar rose for a third month; Tokyo core inflation hit 2.9%, a 16-month high, fuelling Bank of Japan rate-hike bets (Reuters, 27 Nov 2026)

## Files

- `main.ts` — entrypoint: validates `entry.png` and copies it to `/output/entry.png`
- `entry.png` — the front-page image itself (1024x1024 PNG, under 1 MiB)
- `compose.py` — the program that drew the front page (not run by the entry)
- `LICENSE` — MIT
