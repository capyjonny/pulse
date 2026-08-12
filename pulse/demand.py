"""Estimate next-window demand and allocate it across open sections."""
FLOOR = 10.0

def scenarios(total_cleared, ratios=(0.18, 0.30, 0.45)):
    """Window-over-window carryover ratios observed historically ~0.25-0.33;
    bracketed cold/base/hot. Rebidder waves (failures) push toward hot."""
    return {name: max(4, round(total_cleared * r))
            for name, r in zip(("cold", "base", "hot"), ratios)}

def allocation_weights(state, supply_weight=0.5):
    """Blend seat availability with desirability (revealed by last-window median)."""
    open_secs = {k: s for k, s in state.items() if s.seats_left > 0}
    seats = {k: s.seats_left for k, s in open_secs.items()}
    desir = {k: max(((s.median or FLOOR + 3) - FLOOR + 1), 0.5) for k, s in open_secs.items()}
    ts, td = sum(seats.values()), sum(desir.values())
    w = {k: supply_weight * seats[k] / ts + (1 - supply_weight) * desir[k] / td
         for k in open_secs}
    tw = sum(w.values())
    return {k: v / tw for k, v in w.items()}
