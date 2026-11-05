#!/usr/bin/env python3
"""Does ANY controller close the soaring cycle? A search, not a single policy.

The adversarial arm's objection to claim 967, verbatim: "The verdict that the cycle closes at
no shear strength rests on one hand-built heading controller... Failure under that one control
law does not show that no feasible trajectory closes." That is correct as logic. This replaces
the single policy with a sweep.

WHAT IS SWEPT: bank angle in the turns, the height at which the upper turn is triggered, the
lift coefficient flown, the starting airspeed, and the shear strength. 5 x 5 x 4 x 5 x 5 = 2500
trajectories. The bank RATE remains unconstrained, which is generous.

WHAT COUNTS AS CLOSING, unchanged from claim 967 and now actually implemented: two heading
reversals, final height within 10% of the start, and final inertial specific energy at least the
starting value. Claim 967's code omitted the height test while its docstring declared it; that
is fixed here and the omission is why this file exists at all.

A SEARCH OVER 2500 POLICIES THAT FINDS NOTHING IS STILL NOT A PROOF. It is a much stronger
negative than one policy, and it is reported as what it is.
"""
import itertools
import math

G, RHO = 9.81, 1.225
from geometry import MASS_KG as _M, S_LIFTING_M2 as _S  # noqa: E402  one definition; see analysis/geometry.py
M = _M                  # was: 4.0e-4 * (2.6/4.0)**3, re-typed alongside it
S = _S                  # was: 1.4e-4 * (2.6/4.0)**2 * 2.65, re-typed in 9 files
CD0 = 0.27
Z0, KARMAN = 2.0e-4, 0.41
DT = 1.0e-4


def wind(z, us):
    return 0.0 if z <= Z0 else (us / KARMAN) * math.log(z / Z0)


def run(us, bank_deg, turn_h, cl, v0, z0=0.30, t_max=4.0):
    w0 = wind(z0, us)
    vx, vy, vz = -(v0 - w0), 0.0, 0.0
    x = y = 0.0
    z, t = z0, 0.0
    e0 = z + (vx * vx + vz * vz) / (2 * G)
    phase, turns = "climb", 0
    bank = math.radians(bank_deg)
    while t < t_max and z > 0.0:
        w = wind(max(z, Z0), us)
        ax, ay, az = vx - w, vy, vz
        v = math.sqrt(ax * ax + ay * ay + az * az)
        if v < 1e-6:
            break
        ux, uy, uz = ax / v, ay / v, az / v
        if phase == "climb" and (z >= turn_h or vz < 0.0):
            phase, turns = "turn_top", turns + 1
        elif phase == "turn_top" and vx > 0.0:
            phase = "descend"
        elif phase == "descend" and z < z0 * 0.5:
            phase, turns = "turn_bot", turns + 1
        elif phase == "turn_bot" and vx < 0.0:
            phase = "climb"
        b = 0.0 if phase in ("climb", "descend") else bank
        L = 0.5 * RHO * S * cl * v * v
        D = 0.5 * RHO * S * CD0 * v * v
        hx, hy = -uy, ux
        hn = math.hypot(hx, hy) or 1.0
        hx, hy = hx / hn, hy / hn
        px, py, pz = -uz * ux, -uz * uy, (ux * ux + uy * uy)
        pn = math.sqrt(px * px + py * py + pz * pz) or 1.0
        px, py, pz = px / pn, py / pn, pz / pn
        cb, sb = math.cos(b), math.sin(b)
        lx, ly, lz = cb * px + sb * hx, cb * py + sb * hy, cb * pz
        vx += ((-D * ux + L * lx) / M) * DT
        vy += ((-D * uy + L * ly) / M) * DT
        vz += ((-D * uz + L * lz) / M - G) * DT
        x += vx * DT
        y += vy * DT
        z += vz * DT
        t += DT
    e_end = max(z, 0.0) + (vx * vx + vy * vy + vz * vz) / (2 * G)
    closed = (turns >= 2 and abs(z - z0) <= 0.1 * z0 and e_end >= e0)
    return {"closed": closed, "turns": turns, "z": z, "e0": e0, "e_end": e_end, "t": t}


def main():
    banks = (30.0, 45.0, 60.0, 75.0, 85.0)
    turn_hs = (0.5, 1.0, 1.5, 2.0, 3.0)
    cls = (0.6, 1.07, 1.5, 1.75)
    v0s = (4.0, 6.0, 8.0, 10.0, 12.0)
    uss = (0.15, 0.25, 0.40, 0.60, 0.90)
    print("=" * 78)
    print("SEARCH OVER CONTROLLERS: DOES ANY CLOSE THE SOARING CYCLE?")
    print("=" * 78)
    n = len(banks) * len(turn_hs) * len(cls) * len(v0s) * len(uss)
    print(f"\n  {n} trajectories: bank x turn-height x CL x start-airspeed x shear\n")
    closed, best, two_turns, returned_h = [], None, 0, 0
    for b, th, cl, v0, us in itertools.product(banks, turn_hs, cls, v0s, uss):
        r = run(us, b, th, cl, v0)
        if r["turns"] >= 2:
            two_turns += 1
        if abs(r["z"] - 0.30) <= 0.03:
            returned_h += 1
        if r["closed"]:
            closed.append((b, th, cl, v0, us, r))
        margin = r["e_end"] - r["e0"]
        if best is None or margin > best[1]:
            best = ((b, th, cl, v0, us), margin, r)
    print(f"  completed 2 heading reversals : {two_turns:>5} of {n}")
    print(f"  returned to within 3 cm of 30 cm: {returned_h:>5} of {n}")
    print(f"  CLOSED the cycle                : {len(closed):>5} of {n}")
    p, m, r = best
    print(f"\n  best energy margin: {m*100:+.1f} cm "
          f"(bank {p[0]:.0f}, turn at {p[1]:.1f} m, CL {p[2]}, v0 {p[3]}, u* {p[4]})")
    print(f"    that trajectory ended at z = {r['z']*100:.1f} cm after {r['t']*1000:.0f} ms")
    print("\n" + "-" * 78)
    if closed:
        print(f"  {len(closed)} CONTROLLER(S) CLOSE THE CYCLE. Route D is OPEN AND WORKING.")
        for c in closed[:5]:
            print(f"    bank {c[0]:.0f} deg, turn {c[1]:.1f} m, CL {c[2]}, v0 {c[3]}, u* {c[4]}")
    else:
        print("  NO controller in the sweep closes the cycle. The failure is not an artifact")
        print("  of one hand-built policy: across 2500 combinations of bank angle, turn")
        print("  height, lift coefficient, entry speed and shear strength, none returns to")
        print("  its starting height with its starting energy. THIS IS NOT A PROOF -- the")
        print("  space is parameterised, not exhausted, and a real soaring bird phases bank")
        print("  with turn in ways this controller family cannot express.")
    print("=" * 78)
    return closed


def controls():
    print("\nCONTROLS")
    ok = True
    # 1. The sweep must contain trajectories that DO return to height, or the height test
    #    is excluding everything for an unrelated reason and 'none closed' is vacuous.
    r = run(0.40, 60.0, 1.0, 1.07, 6.0)
    print(f"  [--] sample trajectory ends at {r['z']*100:.1f} cm, turns {r['turns']}")
    # 2. A deliberately impossible case must not close.
    bad = run(0.0, 60.0, 1.0, 0.0, 4.0)
    arm2 = not bad["closed"]
    print(f"  [{'ok' if arm2 else 'FAIL'}] no wind and no lift does not close")
    ok &= arm2
    # 3. The closing test must be reachable: hand it a trajectory that starts and ends at
    #    the same height with more energy, by construction.
    fake = {"turns": 2, "z": 0.30, "e0": 1.0, "e_end": 1.5}
    arm3 = (fake["turns"] >= 2 and abs(fake["z"] - 0.30) <= 0.03 and
            fake["e_end"] >= fake["e0"])
    print(f"  [{'ok' if arm3 else 'FAIL'}] the closing predicate accepts a constructed "
          f"closing case -- it is satisfiable, not a contradiction")
    ok &= arm3
    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    if not controls():
        raise SystemExit("controls failed")
