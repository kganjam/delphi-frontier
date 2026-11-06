#!/usr/bin/env python3
"""S911: at the wind route D needs, how big are the waves the fish must fly over?

Claim 1044 established that claim 971's 12.5 m/s threshold at 1 m is Beaufort 7 at the 10 m
reference, not Beaufort 6. The frontier generator then asked the obvious next question, which
nobody here had: a Beaufort 7-9 wind over open water raises a sea of several metres, and the
design "sustains flight above 1 metre". Flying at 1 m over a 5 m sea is not flight.

The answer turns on FETCH, and that is what saves it -- for a reason that then creates a worse
problem. Wave height is fetch-limited, and the zebrafish's habitat (floodplain ponds, paddies
and slow streams) has almost none. So the waves never build. But a water body with no fetch
is also a water body sheltered enough that the required wind is implausible, which is S916.

RELATIONS USED, both standard fetch-limited growth laws in non-dimensional form:
    H* = 0.0016 * (F*)^0.5      with H* = g*Hs/U10^2 and F* = g*F/U10^2   (SPM/JONSWAP)
    H*  capped at 0.243                                                   (Pierson-Moskowitz)
Checked below against two independent reference points before use.
"""
from __future__ import annotations

import math

G = 9.81
PM_CAP = 0.243        # fully developed limit on g*Hs/U^2
COEF = 0.0016


def hs(u10: float, fetch_m: float) -> float:
    """Significant wave height for a 10 m wind over a straight-line fetch."""
    fstar = G * fetch_m / (u10 * u10)
    hstar = min(COEF * math.sqrt(fstar), PM_CAP)
    return hstar * u10 * u10 / G


def fetch_for_hs(u10: float, target: float) -> float | None:
    """Fetch at which Hs first reaches `target`; None if the fully developed sea never does."""
    if PM_CAP * u10 * u10 / G < target:
        return None
    hstar = G * target / (u10 * u10)
    return (hstar / COEF) ** 2 * u10 * u10 / G


def main() -> int:
    print("  CONTROLS -- the relations must reproduce two independently known points before use.")
    a = hs(10.0, 1e5)
    b = PM_CAP * 10.0**2 / G
    print(f"    10 m/s over 100 km fetch -> Hs {a:.2f} m   (textbook fetch-limited value ~1.5-2 m)"
          f"   {'OK' if 1.4 < a < 2.1 else 'OUT OF RANGE'}")
    print(f"    10 m/s fully developed   -> Hs {b:.2f} m   (Pierson-Moskowitz ~2.5 m)"
          f"   {'OK' if 2.3 < b < 2.7 else 'OUT OF RANGE'}")
    print(f"    monotone in fetch: {hs(15.83, 100) < hs(15.83, 1000) < hs(15.83, 10000)}")
    # Compare with a tolerance, not ==. hs() evaluates (h*u)*u/G and this line would write
    # h*u**2/G; float multiplication is not associative, so an exact test reports a difference
    # that is not there. The first version of this control did exactly that and printed False
    # for a cap that works.
    capped, expect = hs(15.83, 1e9), PM_CAP * 15.83 * 15.83 / G
    print(f"    capped at the PM limit: {capped:.4f} m vs {expect:.4f} m  "
          f"{'OK' if math.isclose(capped, expect, rel_tol=1e-12) else 'DIFFERS'}")

    U10 = 15.83          # claim 1044: the 10 m wind equivalent to 12.5 m/s at 1 m
    FLIGHT = 1.0         # claim 971's altitude floor
    print(f"\n  AT ROUTE D'S WIND, U10 = {U10} m/s (Beaufort 7):")
    print(f"  {'fetch':>12}   {'Hs (m)':>8}   vs the 1 m flight altitude")
    for f, lbl in ((30, "paddy field"), (100, "floodplain pond"), (300, "large pond"),
                   (1000, "1 km"), (3800, "3.8 km"), (1e4, "10 km"), (1e5, "100 km"),
                   (1e9, "fully developed")):
        h = hs(U10, f)
        flag = "waves exceed the flight height" if h > FLIGHT else ""
        print(f"  {lbl:>17}   {h:8.2f}   {flag}")

    half = fetch_for_hs(U10, 0.5)
    one = fetch_for_hs(U10, 1.0)
    print("\n  S911 asked: is Hs below 0.5 m (half the flight height) at any fetch of 1 km or more?")
    print(f"    Hs at 1 km fetch        = {hs(U10, 1000):.2f} m")
    print(f"    Hs reaches 0.5 m at     = {half/1000:.2f} km of fetch")
    print(f"    Hs reaches 1.0 m at     = {one/1000:.2f} km of fetch")
    print(f"    ANSWER: yes at 1 km ({hs(U10,1000):.2f} m < 0.5 m), and the 0.5 m crossing is at "
          f"{half/1000:.1f} km.")
    print("\n  The fetch that would drown the design is far longer than any water body the")
    print("  zebrafish lives in -- which makes the WIND, not the waves, the binding question (S916).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
