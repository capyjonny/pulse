"""Monte Carlo engine: musical chairs with clearing prices.

Mechanic: if rivals < seats, every bid wins (bid amount irrelevant).
Otherwise the clearing price is the k-th highest rival bid; you win iff
your bid exceeds it.
"""
import numpy as np
from .demand import FLOOR

SCARCITY_SEATS = 8      # visible scarcity provokes aggression
SCARCITY_MULT = 1.5

def simulate_section(seats, expected_rivals, anchor_median, bid_grid, *,
                     premium=1.0, sigma=0.6, n_sims=20000, floor=FLOOR, rng=None):
    rng = rng or np.random.default_rng()
    grid = np.asarray(bid_grid, float)
    markup = max((anchor_median or floor + 3) - floor, 1.5) * premium
    if seats <= SCARCITY_SEATS:
        markup *= SCARCITY_MULT
    wins = np.zeros(len(grid))
    th = np.empty(n_sims)
    fills = 0
    for i in range(n_sims):
        r = rng.poisson(expected_rivals)
        if r < seats:
            th[i] = floor + 0.01
            wins += 1
            continue
        fills += 1
        bids = floor + rng.lognormal(np.log(markup), sigma, r)
        kth = np.partition(bids, -seats)[-seats]
        th[i] = kth
        wins += grid > kth
    return {"p_win": wins / n_sims, "p_fill": fills / n_sims,
            "clr_p50": float(np.percentile(th, 50)),
            "clr_p90": float(np.percentile(th, 90)),
            "clr_p99": float(np.percentile(th, 99))}

def run_matrix(state, weights, demand_scenarios, bid_grid, *,
               premium=1.0, sigma=0.6, n_sims=20000, seed=42):
    """Base/stress matrix across all open sections and demand scenarios."""
    rng = np.random.default_rng(seed)
    out = {}
    for scen, total in demand_scenarios.items():
        out[scen] = {}
        for sect, w in weights.items():
            s = state[sect]
            out[scen][sect] = simulate_section(
                s.seats_left, total * w, s.median, bid_grid,
                premium=premium, sigma=sigma, n_sims=n_sims, rng=rng)
    return out

def targeted_rush(state, section, bid_grid, rival_levels=(25, 35, 45), *,
                  premium=1.3, sigma=0.7, n_sims=20000, seed=7,
                  imported_anchor=None):
    """Locked-out bidders converge on one section. The scenario that breaks
    smooth-demand conclusions. imported_anchor: model refugees bringing a
    pricier section's anchor with them."""
    rng = np.random.default_rng(seed)
    s = state[section]
    anchor = imported_anchor or s.median
    return {lam: simulate_section(s.seats_left, lam, anchor, bid_grid,
                                  premium=premium, sigma=sigma, n_sims=n_sims, rng=rng)
            for lam in rival_levels}
