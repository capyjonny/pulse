"""Pulse CLI.

Example:
  python -m pulse data/sample_cor1703.csv \
      --course COR1703 --window "Incoming Freshmen Rnd 1 Win 1" \
      --budget 55 --bids 12,15,18,20,25 --rush G4
"""
import argparse
from . import schema, state as state_mod, demand, simulate, report

def main(argv=None):
    ap = argparse.ArgumentParser(prog="pulse", description="BOSS bid probability engine")
    ap.add_argument("csv", help="BOSS history CSV (Pulse format)")
    ap.add_argument("--course", required=True)
    ap.add_argument("--window", required=True,
                    help="the just-COMPLETED window, e.g. 'Incoming Freshmen Rnd 1 Win 1'")
    ap.add_argument("--budget", type=float, required=True)
    ap.add_argument("--bids", default="12,15,18,20,25,28,30,32,35",
                    help="comma-separated bid grid")
    ap.add_argument("--rush", default=None,
                    help="section to stress with a targeted rush, e.g. G9")
    ap.add_argument("--rush-anchor", type=float, default=None,
                    help="model rush rivals importing this anchor median")
    ap.add_argument("--sims", type=int, default=20000)
    args = ap.parse_args(argv)

    rows = schema.load(args.csv)
    warns = schema.validate(rows)
    if warns:
        print("SCHEMA WARNINGS:")
        for w in warns[:10]:
            print("  !", w)
        print()

    st = state_mod.build(rows, args.window, args.course)
    summ = state_mod.summarise(st)
    bid_grid = [float(x) for x in args.bids.split(",") if float(x) <= args.budget + 0.01]

    print(f"=== {args.course} | completed window: {args.window} ===")
    print(report.fmt_state(st))
    print(f"\nTotal seats left: {summ['total_seats_left']} | cleared last window: {summ['total_cleared']}"
          f" | full sections: {summ['full_sections'] or 'none'}")
    if summ["zero_failures"]:
        print("NOTE: every section had leftover seats -> ZERO failed bids last window: no rebidder wave.")
    else:
        print("NOTE: some sections filled -> failed bidders WILL rebid next window (rebidder wave).")

    scen = demand.scenarios(summ["total_cleared"])
    weights = demand.allocation_weights(st)
    open_state = {k: st[k] for k in weights}

    base = simulate.run_matrix(open_state, weights, scen, bid_grid, n_sims=args.sims)
    stress = simulate.run_matrix(open_state, weights, scen, bid_grid,
                                 premium=1.45, sigma=0.8, n_sims=args.sims, seed=99)

    print("\n================ BASE MODEL ================")
    print(report.fmt_matrix(base, bid_grid))
    print("\n================ STRESS (price premium x1.45, fat tails) ================")
    print(report.fmt_matrix(stress, bid_grid))

    recs = report.recommend(stress["hot"], bid_grid, args.budget)
    print(report.fmt_recommendations(recs, args.budget))

    if args.rush:
        print(f"\n================ TARGETED RUSH on {args.rush} ================")
        rr = simulate.targeted_rush(open_state, args.rush, bid_grid,
                                    imported_anchor=args.rush_anchor, n_sims=args.sims)
        for lam, r in rr.items():
            print(f"  ~{lam} rivals: clr p50={r['clr_p50']:.2f} p90={r['clr_p90']:.2f} | " +
                  " ".join(f"e${b}:{p:.0%}" for b, p in zip(bid_grid, r["p_win"])))
        print("  (rush = locked-out bidders converging; the scenario that breaks smooth-demand conclusions)")

if __name__ == "__main__":
    main()
