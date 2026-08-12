# Methodology (condensed)

Nine steps, learned from the first two concierge cases. Full narrative in the
companion PDF ("Pulse — from BOSS history to a bid recommendation").

1. **Collect** — Overall BOSS Results per course, 2+ years, freshman windows only.
2. **Decode & verify** — bef/aft = vacancies before/after; verify by falsification
   (the rival "bids/failed-bids" reading implies bids failing into empty seats).
3. **Reconstruct state** — seats left, cleared bids, and *where failures happened*:
   failed bidders are next window's most predictable demand.
4. **Join on instructor** — section letters reshuffle yearly; a new professor has
   no history and must be treated as a wildcard, not an heir.
5. **Estimate demand** — carryover ratio (~0.25–0.33 observed) x this year's
   volume + rebidder wave, spread by supply-and-desirability weights; every
   input becomes a cold/base/hot scenario axis.
6. **Simulate** — 20–40k Monte Carlo windows: Poisson rivals, lognormal bids
   anchored on last window's median. Outputs P(win) per bid, P(fill), clearing
   price p50/p90/p99.
7. **Stress-test** — rerun with premiums (x1.3–1.45), fat tails, hot demand, and
   targeted rushes at the recommended section. Ship only what survives being wrong.
   Anchor final numbers on real precedents (worst historical clearing for a
   comparable section).
8. **Decide** — constraint triangle (prof / slot / certainty: pick two on a tight
   budget); all-in on must-haves (failed bids refund); shade near-certain bids
   (unspent e$ rolls forward); never floor-bid tight sections; prefer undominated
   strategies (fail only in worlds where nothing wins).
9. **Deliver** — probabilities not promises; morning-of checklist; named fallbacks
   and failure modes. "100%" always means "never failed in N simulated futures
   sharing our assumptions."

Case studies: COR1703 (abundant regime — 106 seats vs ~22 expected bidders, bid
amount nearly irrelevant) vs STAT1202 (contested regime — rebidder wave, budget
inside the historical clearing range, section choice decisive).
