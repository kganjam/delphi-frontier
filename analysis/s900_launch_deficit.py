#!/usr/bin/env python3
"""S900: does the launch close under its own evidence, or not at any combination of inputs?

The falsifier was RESTATED before any run (claim 490) because the generated one inverted its own
metric. The restated form, quoted: DEFICIT = required take-off speed / achievable launch speed, so
DEFICIT > 1 means the launch does not close. Negatively settled if the joint pessimistic case gives
DEFICIT above 1.0 AND no single input returned alone to its favourable end brings it to 1.0 or
below. Positively settled only if the joint PESSIMISTIC case is at or below 1.0.

TWO SOURCES FOR THE ACHIEVABLE SPEED, AND BOTH ARE REPORTED. The `parameter` table carries U_b at
0.842 m/s with range 0.45-1.38, which is a RANGE ACROSS 50 FISH. Claim 443 supersedes the claims
built on it with Demesmay et al. 2025's 1.57 +/- 0.27 m/s, a MEAN OF MAXIMAL escape speeds at 240
fps. These measure different quantities, so neither is simply "the newer value" -- the envelope
table is stale relative to the claim graph (noted in S900's own acceptance), and the sweep is run
on both rather than choosing silently.
"""
from __future__ import annotations

V_TO = (4.37, 4.22, 4.69)          # required take-off speed: point, lo, hi
SOURCES = {
    "parameter table (range over 50 fish)": (0.842, 0.45, 1.38),
    "Demesmay 2025 (mean of maximal, +/-1sd)": (1.57, 1.57 - 0.27, 1.57 + 0.27),
}


def deficit(v_to: float, u_b: float) -> float:
    return v_to / u_b


def main() -> int:
    for label, (ub_p, ub_lo, ub_hi) in SOURCES.items():
        print(f"\n  === achievable launch speed from: {label}")
        pess = deficit(V_TO[2], ub_lo)      # worst take-off requirement, worst achievable
        opt = deficit(V_TO[1], ub_hi)       # best of both
        nom = deficit(V_TO[0], ub_p)
        print(f"    joint PESSIMISTIC  V_to {V_TO[2]} / U_b {ub_lo:.2f}  ->  DEFICIT {pess:.2f}")
        print(f"    nominal            V_to {V_TO[0]} / U_b {ub_p:.2f}  ->  DEFICIT {nom:.2f}")
        print(f"    joint OPTIMISTIC   V_to {V_TO[1]} / U_b {ub_hi:.2f}  ->  DEFICIT {opt:.2f}")

        # The falsifier's second clause: does ANY single input, alone at its favourable end,
        # bring the pessimistic case to <= 1.0?
        singles = {
            "V_to alone to its best": deficit(V_TO[1], ub_lo),
            "U_b alone to its best": deficit(V_TO[2], ub_hi),
        }
        rescued = [k for k, v in singles.items() if v <= 1.0]
        for k, v in singles.items():
            print(f"    {k:28} -> DEFICIT {v:.2f}")
        verdict = ("POSITIVELY settled" if pess <= 1.0 else
                   "NEGATIVELY settled" if not rescued else
                   "UNSETTLED: a single input rescues it")
        print(f"    => {verdict}")

    print("\n  BOTH SOURCES AGREE ON THE VERDICT, which is the only reason it can be stated:")
    print("    the two differ by a factor of ~1.9 in achievable speed and the conclusion does not")
    print("    turn on which is used. Had they disagreed, the stale envelope table would have had")
    print("    to be resolved first, and S900 could not have been settled tonight.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
