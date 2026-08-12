# Pulse

**Probability-based bid recommendations for SMU BOSS course bidding.**

You give Pulse the bidding history of a course (from the Overall BOSS Results page)
and your budget. It reconstructs the current state of every section, simulates the
next bidding window tens of thousands of times, and tells you the probability that
any given bid wins — under normal demand, under deliberately pessimistic
assumptions, and under a targeted rush on your section.

Born as a concierge service for two real freshmen in AY26/27 Round 1. Their cases
(and the full methodology) are documented in [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

## Quickstart

```bash
git clone <this repo> && cd pulse
pip install numpy
python -m pulse data/sample_cor1703.csv \
    --course COR1703 --window "Incoming Freshmen Rnd 1 Win 1" \
    --budget 55 --bids 12,15,18,20,25 --rush G4
```

You'll get: the seat board, base + stress simulation matrices with clearing-price
percentiles (p50/p90/p99), per-section recommendations, and a targeted-rush
stress test on G4.

## The core mechanic (read this before trusting anything)

BOSS is **musical chairs, not price tags**. If fewer rivals bid a section than it
has seats, *every* bid wins and the amount is irrelevant. A clearing price only
exists once a section overfills — then it's the bid of the last person seated.
Pulse's job is mostly to estimate whether the music will play at all, and only
secondarily what it costs when it does.

Key schema fact (verified by falsification): `Bef Proc` / `Aft Proc` in the BOSS
results are section **vacancies before/after** the window processed. So
`cleared = bef - aft`, `enrolled = quota - aft`, and `aft > 0` means **no bid in
that section failed** — which tells you whether a rebidder wave exists.

## Data format

CSV, one row per (window, section):

```
term,window,course,section,instructor,smux,median,min_succ,vacancy,open_quota,bef_proc,aft_proc,enrolled
```

Transcribe from the Overall BOSS Results page (freshman rounds: filter
`Incoming Freshmen` windows; senior rounds use different quota pools — leave them
out). **Join history across years on `instructor`, never on section letter** —
sections reshuffle professors every year.

## What the output means

- `P(fill)` — probability the section even overfills. If ~0%, your bid amount doesn't matter.
- `clr p50/p90/p99` — median / 90th / 99th percentile clearing price across simulated futures. Bid above p99 and you survive all but the weirdest 1%.
- Recommendations use the **stress** run (prices +45%, fat tails, hot demand): the number shown already assumes the assumptions are wrong against you.

## Honest limitations

1. The model extrapolates behaviour; it cannot see news (timetable changes, quota shifts, concurrent exchange rounds nibbling seats).
2. Friends bid in cliques; Poisson rival counts understate coordinated pile-ons.
3. Stress tests prove robustness *within our assumptions*, not truth. The raw facts (seats left, cleared counts, historical extremes) carry the real weight.
4. Reflexivity: if everyone runs Pulse, cheap sections stop being cheap.

**These are estimates, not guarantees. Never bid money you can't afford to lock up
for a window. Check live seat counts the morning you bid.**

## Roadmap

- [ ] Ingest the Overall BOSS Results CSV download directly (no manual transcription)
- [ ] Clique-aware demand (negative binomial rival counts)
- [ ] Web UI + per-course insight blog
- [ ] Post-window calibration tracking: predicted vs actual clearing prices

## Contributing

Concierge-first: run a real case for a real person, then generalise what the case
needed. PRs welcome — bring data.

MIT licensed. Not affiliated with SMU.
