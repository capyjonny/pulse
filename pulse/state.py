"""Reconstruct the current board from the most recently completed window."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class SectionState:
    section: str
    instructor: str
    smux: bool
    seats_left: int      # aft_proc of completed window
    cleared: int         # bids that won in completed window
    median: Optional[float]
    min_succ: Optional[float]

def build(rows, completed_window: str, course: str):
    sel = [r for r in rows if r.window == completed_window and r.course == course]
    if not sel:
        raise SystemExit(f"No rows for window '{completed_window}' and course '{course}'. "
                         f"Windows present: {sorted({r.window for r in rows if r.course == course})}")
    state = {}
    for r in sel:
        if r.vacancy <= 4:   # tiny SG8x special sections: ignore
            continue
        state[r.section] = SectionState(r.section, r.instructor, r.smux,
                                        r.aft_proc, r.cleared, r.median, r.min_succ)
    return state

def summarise(state):
    total_seats = sum(s.seats_left for s in state.values())
    total_cleared = sum(s.cleared for s in state.values())
    no_failures = all(s.seats_left > 0 for s in state.values())
    full = [s.section for s in state.values() if s.seats_left == 0]
    return {"total_seats_left": total_seats, "total_cleared": total_cleared,
            "zero_failures": no_failures, "full_sections": full}
