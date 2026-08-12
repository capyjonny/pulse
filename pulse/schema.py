"""Load and validate BOSS Overall Results data (Pulse CSV format).

Columns: term,window,course,section,instructor,smux,median,min_succ,
         vacancy,open_quota,bef_proc,aft_proc,enrolled

Decoding (verified by falsification against 2 courses / 3 years):
  bef_proc / aft_proc = section vacancies BEFORE / AFTER the window processed
  => cleared bids = bef_proc - aft_proc
  => enrolled     = quota - aft_proc          (consistency check)
  => aft_proc > 0 implies EVERY bid in that section cleared (no failures)
"""
import csv
from dataclasses import dataclass
from typing import Optional

@dataclass
class Row:
    term: str
    window: str
    course: str
    section: str
    instructor: str
    smux: bool
    median: Optional[float]
    min_succ: Optional[float]
    vacancy: int
    open_quota: int
    bef_proc: int
    aft_proc: int
    enrolled: int

    @property
    def cleared(self) -> int:
        return self.bef_proc - self.aft_proc

def _f(x):
    x = (x or "").strip()
    return None if x in ("", "-", "0.00") else float(x)

def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append(Row(
                term=r["term"].strip(), window=r["window"].strip(),
                course=r["course"].strip(), section=r["section"].strip(),
                instructor=r["instructor"].strip(),
                smux=r.get("smux", "0").strip() in ("1", "true", "True", "y"),
                median=_f(r.get("median")), min_succ=_f(r.get("min_succ")),
                vacancy=int(r["vacancy"]), open_quota=int(r["open_quota"]),
                bef_proc=int(r["bef_proc"]), aft_proc=int(r["aft_proc"]),
                enrolled=int(r["enrolled"])))
    return rows

def validate(rows):
    """Falsification checks on the schema decoding. Returns list of warnings."""
    warns = []
    for r in rows:
        if r.aft_proc > r.bef_proc:
            warns.append(f"{r.window} {r.section}: aft_proc > bef_proc (impossible under decoding)")
        if r.open_quota and abs((r.open_quota - r.aft_proc) - r.enrolled) > 2:
            warns.append(f"{r.window} {r.section}: enrolled={r.enrolled} != quota-aft={r.open_quota - r.aft_proc} "
                         "(check decoding or a drop/add occurred)")
        if r.aft_proc > 0 and r.median is not None and r.min_succ is not None and r.min_succ > r.median:
            warns.append(f"{r.window} {r.section}: min_succ > median (data entry error?)")
    return warns
