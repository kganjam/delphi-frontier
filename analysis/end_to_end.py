#!/usr/bin/env python3
"""End to end: water exit -> climb -> sustained soaring, in ONE integration.

THE LAST STRUCTURAL CAVEAT ON CLAIM 971. The soaring result started the animal ALREADY FLYING
at 30 cm with an entry airspeed taken from the wind profile. Claim 971 said so: "the entry
condition still assumes the animal gets to 30 cm, which claim 965 supports in wind but which is
not integrated end-to-end with this phase." This integrates it.

ONE TRAJECTORY, NO HAND-OFF. The animal leaves the water at the surface with the exit speed its
muscle can supply -- 1.60 m/s relative to the WATER (claims 546, 583) -- into a logarithmic wind
profile, and is then flown by the same four-phase controller the soaring sweep used. Nothing is
seeded: the airspeed at every instant is whatever the trajectory has produced, and the wind the
animal feels at the surface is near zero because the log profile goes to zero at the roughness
height.

THAT LAST POINT IS THE DIFFICULTY, AND IT IS WHY THIS TEST CAN FAIL. The soaring result needs
roughly 12 m/s of airspeed. At the surface the wind is ~0, so the animal leaves with 1.6 m/s and
must CLIMB into the fast air before it can use it -- on lift generated at 1.6 m/s, which claim
964 put at 15.8% of its weight in still air. The question is whether the climb is self-starting.
"""
import math

G, RHO = 9.81, 1.225
M = 4.0e-4 * (2.6 / 4.0) ** 3
S = 1.4e-4 * (2.6 / 4.0) ** 2 * 2.65
CD0 = 0.27
Z0, KARMAN = 2.0e-4, 0.41
DT = 5.0e-5
V_EXIT = 1.60


def wind(z, us):
    return 0.0 if z <= Z0 else (us / KARMAN) * math.log(z / Z0)


def fly(us, cl, bank_deg, turn_h, angle_deg, t_max=6.0):
    th = math.radians(angle_deg)
    vx, vy, vz = -V_EXIT * math.cos(th), 0.0, V_EXIT * math.sin(th)   # into wind, upward
    z, t = 0.0, 0.0
    zmax = 0.0
    bank = math.radians(bank_deg)
    phase, turns = "climb", 0
    e0 = None
    vair_max = 0.0
    while t < t_max:
        w = wind(max(z, 0.0), us)
        ax, ay, az = vx + w, vy, vz      # headwind: air moves toward +x relative to ground
        v = math.sqrt(ax * ax + ay * ay + az * az)
        if v < 1e-9:
            break
        vair_max = max(vair_max, v)
        if e0 is None:
            e0 = z + (vx * vx + vy * vy + vz * vz) / (2 * G)
        ux, uy, uz = ax / v, ay / v, az / v
        if phase == "climb" and (z >= turn_h or vz < 0.0):
            phase, turns = "turn_top", turns + 1
        elif phase == "turn_top" and vx > 0.0:
            phase = "descend"
        elif phase == "descend" and z < turn_h * 0.3:
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
        z += vz * DT
        t += DT
        zmax = max(zmax, z)
        if z < 0.0 and t > DT * 100:
            break
    e_end = max(z, 0.0) + (vx * vx + vy * vy + vz * vz) / (2 * G)
    return {"t": t, "z": z, "zmax": zmax, "turns": turns, "e0": e0 or 0.0,
            "e_end": e_end, "vair_max": vair_max,
            "aloft": t >= t_max - DT * 2 and z > 0.0}


def main():
    print("=" * 78)
    print("END TO END: WATER EXIT AT 1.60 m/s -> ?")
    print("=" * 78)
    print(f"\n  no seeded entry: the animal starts at the SURFACE where the wind is ~0\n")
    print(f"  {'u*':>6} {'U(1m)':>8} {'best peak':>11} {'max airspeed':>14} {'aloft at 6 s':>14}")
    print("  " + "-" * 60)
    for us in (0.25, 0.40, 0.60, 0.90, 1.20):
        best = None
        n_aloft = 0
        for cl in (1.07, 1.5, 1.75):
            for bank in (30.0, 45.0, 60.0):
                for th in (0.3, 0.5, 1.0, 2.0):
                    for ang in (20.0, 30.0, 45.0, 60.0):
                        r = fly(us, cl, bank, th, ang)
                        if r["aloft"]:
                            n_aloft += 1
                        if best is None or r["zmax"] > best["zmax"]:
                            best = r
        print(f"  {us:>6.2f} {wind(1.0,us):>6.1f}m/s {best['zmax']*100:>9.1f}cm "
              f"{best['vair_max']:>12.1f}m/s {n_aloft:>9} of 144")
    print("\n" + "-" * 78)
    print("READING IT")
    print("-" * 78)
    print("  The soaring result needs ~12 m/s of airspeed. At the surface the wind is ~0,")
    print("  so the animal leaves with 1.6 m/s and must climb into the fast air using lift")
    print("  generated at 1.6 m/s -- which claim 964 put at 15.8% of weight in still air.")
    print("  Whether the climb is self-starting is what the table above answers.")
    print("=" * 78)


def controls():
    print("\nCONTROLS")
    ok = True
    r0 = fly(0.0, 1.07, 45.0, 0.5, 45.0)
    arm1 = not r0["aloft"]
    print(f"  [{'ok' if arm1 else 'FAIL'}] with NO wind it is not aloft at 6 s "
          f"(peak {r0['zmax']*100:.1f} cm) -- no free lunch")
    ok &= arm1
    r1 = fly(0.90, 1.07, 45.0, 0.5, 45.0)
    arm2 = r1["zmax"] > r0["zmax"]
    print(f"  [{'ok' if arm2 else 'FAIL'}] wind raises the peak "
          f"({r0['zmax']*100:.1f} -> {r1['zmax']*100:.1f} cm)")
    ok &= arm2
    arm3 = wind(0.0, 0.9) == 0.0 and wind(2.0, 0.9) > wind(0.2, 0.9)
    print(f"  [{'ok' if arm3 else 'FAIL'}] wind is zero at the surface and rises with height "
          f"-- the animal gets no free airspeed at launch")
    ok &= arm3
    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    if not controls():
        raise SystemExit("controls failed")
