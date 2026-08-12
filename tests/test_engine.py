"""Sanity tests: python -m pytest, or just python tests/test_engine.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
from pulse.simulate import simulate_section

def test_empty_section_any_bid_wins():
    r = simulate_section(seats=30, expected_rivals=3, anchor_median=14,
                         bid_grid=[10.51, 40], n_sims=4000, rng=np.random.default_rng(1))
    assert r["p_win"][0] > 0.99 and r["p_win"][1] > 0.99
    assert r["p_fill"] < 0.01

def test_oversubscribed_low_bid_loses():
    r = simulate_section(seats=5, expected_rivals=40, anchor_median=30,
                         bid_grid=[10.51, 120], n_sims=4000, rng=np.random.default_rng(2))
    assert r["p_win"][0] < 0.05      # floor bid dies
    assert r["p_win"][1] > 0.90      # extreme bid survives
    assert r["p_fill"] > 0.99

def test_higher_bid_never_worse():
    r = simulate_section(seats=10, expected_rivals=15, anchor_median=20,
                         bid_grid=[12, 18, 25, 33], n_sims=4000, rng=np.random.default_rng(3))
    p = list(r["p_win"])
    assert p == sorted(p)

if __name__ == "__main__":
    test_empty_section_any_bid_wins()
    test_oversubscribed_low_bid_loses()
    test_higher_bid_never_worse()
    print("all tests passed")
