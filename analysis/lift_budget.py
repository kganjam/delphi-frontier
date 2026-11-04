#!/usr/bin/env python3
"""The lift budget behind this project's headline numbers, re-derivable from its stated inputs.

Computes, from mass / lifting area / C_L,max alone:
  * v_min, the slowest speed at which lift can equal weight           v = sqrt(2W / (rho S C_L))
  * S_needed, the lifting area required at a chosen airspeed          S = 2W / (rho v^2 C_L)
  * the shortfall against the area actually available

CONTROL, and it is an independent one. The Delphi Lean law registry (lawset 1.6.0, constraint C9 /
thompson1917-ch02-06, status accepted, band proved) was given the same design through its own
evaluator -- a separately written implementation this project does not maintain -- and returned
vmin 7.561853784163062 m/s and liftingAreaNeeded 4.116303685927453e-4 m^2. This script must
reproduce both to within 0.1%, or one of the two is wrong.

    python3 lift_budget.py
"""
import sys

RHO_AIR = 1.225       # kg/m^3, ISA sea level
G = 9.80665           # m/s^2


def v_min(mass_kg, area_m2, cl_max, rho=RHO_AIR):
    """Slowest speed at which lift can reach weight."""
    return ((2.0 * mass_kg * G) / (rho * area_m2 * cl_max)) ** 0.5


def area_needed(mass_kg, airspeed_m_s, cl_max, rho=RHO_AIR):
    """Lifting area required to carry the weight at a given airspeed."""
    return (2.0 * mass_kg * G) / (rho * airspeed_m_s ** 2 * cl_max)


def main():
    # The zebrafish design, as recorded in docs/FINDINGS.md.
    MASS = 4.0e-4         # kg, ~0.4 g adult
    AREA = 1.4e-4         # m^2, ~1.4 cm^2 whole-body dorsal silhouette
    CL = 0.8
    GLIDE = 4.41          # m/s, the glide speed S32 requires

    vm = v_min(MASS, AREA, CL)
    sn = area_needed(MASS, GLIDE, CL)
    print(f"weight                 {MASS * G:.6f} N")
    print(f"v_min at {AREA*1e4:.1f} cm^2      {vm:.4f} m/s   "
          f"({vm/GLIDE:.2f}x the {GLIDE} m/s glide speed)")
    print(f"area needed at {GLIDE} m/s  {sn*1e4:.3f} cm^2  "
          f"({sn/AREA:.2f}x the {AREA*1e4:.1f} cm^2 available)")

    # --- CONTROL: an independent implementation must agree -------------------
    LEAN_VMIN = 7.561853784163062
    LEAN_AREA = 4.116303685927453e-4
    dv = abs(vm - LEAN_VMIN) / LEAN_VMIN * 100
    da = abs(sn - LEAN_AREA) / LEAN_AREA * 100
    print(f"\ncontrol vs Delphi Lean C9 (lawset 1.6.0, independent implementation):")
    print(f"  v_min        here {vm:.9f}  registry {LEAN_VMIN:.9f}  diff {dv:.5f}%")
    print(f"  area needed  here {sn:.12f}  registry {LEAN_AREA:.12f}  diff {da:.5f}%")
    if dv > 0.1 or da > 0.1:
        print("  CONTROL FAILED: this script and the law registry disagree.")
        return 1
    print("  control passed: two independent implementations agree.")

    # The project's own 2 m/s figure, propagated, as a second consistency check.
    s2 = area_needed(MASS, 2.0, CL)
    print(f"\narea needed at 2.00 m/s    {s2*1e4:.2f} cm^2  "
          f"(FINDINGS states ~20 cm^2 at this speed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
