"""Turn simulation output into a readable report with recommendations."""
from .demand import FLOOR

CERTAIN = 0.98

def fmt_state(state):
    lines = [f"{'sect':<6}{'instructor':<22}{'smux':<6}{'seats':<7}{'cleared':<9}{'median':<9}{'min_succ'}"]
    for k in sorted(state):
        s = state[k]
        lines.append(f"{k:<6}{s.instructor:<22}{'Y' if s.smux else '-':<6}{s.seats_left:<7}"
                     f"{s.cleared:<9}{(f'{s.median:.2f}' if s.median else '-'):<9}"
                     f"{(f'{s.min_succ:.2f}' if s.min_succ else '-')}")
    return "\n".join(lines)

def fmt_matrix(results, bid_grid):
    lines = []
    for scen, secs in results.items():
        lines.append(f"\n--- scenario: {scen} ---")
        lines.append(f"{'sect':<6}{'E[riv]':<8}{'seats':<7}{'P(fill)':<9}{'clr p50':<9}{'p90':<8}{'p99':<8}| " +
                     " ".join(f"e${b:>4}" for b in bid_grid))
        for k in sorted(secs):
            r = secs[k]
            lines.append(f"{k:<6}{r.get('e_rivals',0):<8.1f}{r.get('seats',''):<7}{r['p_fill']:<9.1%}{r['clr_p50']:<9.2f}{r['clr_p90']:<8.2f}"
                         f"{r['clr_p99']:<8.2f}| " +
                         " ".join(f"{p:>5.0%}" for p in r["p_win"]))
    return "\n".join(lines)

def recommend(stress_results, bid_grid, budget):
    """Per section: smallest bid on the grid that clears >=98% under stress."""
    recs = {}
    for sect, r in stress_results.items():
        pick = None
        for b, p in zip(bid_grid, r["p_win"]):
            if p >= CERTAIN and b <= budget:
                pick = (b, p)
                break
        recs[sect] = pick
    return recs

def fmt_recommendations(recs, budget):
    lines = [f"\nRECOMMENDATIONS (smallest bid clearing >=98% under STRESS, budget e${budget}):"]
    for sect in sorted(recs):
        if recs[sect]:
            b, p = recs[sect]
            lines.append(f"  {sect}: bid e${b}  (stress P(win) {p:.0%})")
        else:
            lines.append(f"  {sect}: no bid within budget reaches 98% under stress "
                         f"-> all-in e${budget} or pick another section")
    lines.append(f"\nRules: never floor-bid a section with <= 8 seats; failed bids refund fully;")
    lines.append("check LIVE seat counts on the morning of the bid (concurrent rounds nibble seats).")
    lines.append("These are model estimates, not guarantees.")
    return "\n".join(lines)
