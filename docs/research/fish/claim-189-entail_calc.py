#!/usr/bin/env python3
"""Arithmetic for the claim-189 entailment note (docs/research/fish/claim-189-entail.md).

Every number printed here is a CALCULATION on the inputs listed in the note.
Nothing here is an observation. No new measurement was made.
"""

RHO_AIR = 1.225  # kg m^-3
RHO_WATER = 998.0  # kg m^-3
G = 9.81  # m s^-2


def weight(m_kg: float) -> float:
    return m_kg * G


def area_for_weight_support(m_kg: float, v: float, cl: float) -> float:
    """Wing area (m^2) at which L = W, from L = 0.5 rho V^2 S CL."""
    return 2.0 * weight(m_kg) / (RHO_AIR * v * v * cl)


def main() -> None:
    # --- inputs (levels given in the note) -------------------------------
    m = 0.25e-3          # kg, ASSUMED body mass (S28 back-solve)
    m_hi = 0.43e-3       # kg, ASSUMED isometric 3.6 cm body
    sl = 0.030           # m, ASSUMED standard length
    cl = 1.07            # project-derived quasi-steady CL_max
    l_fin_over_sl = 0.463  # FIGURE-READ median, double het (S28-D-D digitisation)
    shape_lo, shape_hi = 0.13, 0.25  # FIGURE-READ A/L^2 per fin (S28-D-D)
    shape_caseC = 0.52   # ASSUMED AR-5 planform (S28 case C)
    speeds = {
        "0.95 (Demesmay 40 ms floor)": 0.95,
        "1.38 (Miln per-fish max)": 1.38,
        "1.57 (Demesmay mean)": 1.57,
        "2.11 (Demesmay mean + 2 SD)": 2.11,
    }
    skim_freq_needed = (132.0, 199.0)  # Hz, project taxiing requirement

    print("W (0.25 g) = %.4e N ; W (0.43 g) = %.4e N" % (weight(m), weight(m_hi)))

    # --- organ constraint 1: spread paired-fin planform area ------------
    l_fin = l_fin_over_sl * sl
    a_lo = 2.0 * shape_lo * l_fin ** 2
    a_hi = 2.0 * shape_hi * l_fin ** 2
    a_cc = 2.0 * shape_caseC * l_fin ** 2
    print("\nfin length per fin = %.2f mm" % (l_fin * 1e3))
    print("paired-fin planform, figure-read shape: %.0f-%.0f mm^2"
          % (a_lo * 1e6, a_hi * 1e6))
    print("paired-fin planform, case-C assumption:  %.0f mm^2" % (a_cc * 1e6))
    print("\n%-30s %10s %10s %10s" % ("speed (m/s)", "S_need", "/S_figmax", "/S_caseC"))
    for label, v in speeds.items():
        s_need = area_for_weight_support(m, v, cl)
        print("%-30s %9.0f %10.1f %10.1f"
              % (label, s_need * 1e6, s_need / a_hi, s_need / a_cc))
    v = 2.11
    s_need = area_for_weight_support(m_hi, v, cl)
    print("at 2.11 m/s with the 0.43 g body: S_need = %.0f mm^2 (x%.1f the figure-read max)"
          % (s_need * 1e6, s_need / a_hi))

    # --- organ constraint 2: tail oscillation period --------------------
    print("\nskim needs %.0f-%.0f Hz -> period %.2f-%.2f ms"
          % (skim_freq_needed[0], skim_freq_needed[1],
             1e3 / skim_freq_needed[1], 1e3 / skim_freq_needed[0]))
    for label, f in (("larval measured 95 Hz", 95.0),
                     ("project input 52 Hz", 52.0),
                     ("adult relayed ~21 Hz", 21.0)):
        print("  %-24s period %6.2f ms ; short of the skim requirement by x%.1f-%.1f"
              % (label, 1e3 / f, skim_freq_needed[0] / f, skim_freq_needed[1] / f))

    # --- behaviour constraint: exit speed bounds ------------------------
    # V_to for the case-C area (the generous one) and for the figure-read area.
    for name, area in (("case C", a_cc), ("figure-read max", a_hi),
                       ("figure-read min", a_lo)):
        v_to = (2.0 * weight(m) / (RHO_AIR * area * cl)) ** 0.5
        print("V_to (%s, %.0f mm^2) = %.2f m/s ; deficit vs 1.57 m/s = x%.2f, vs 2.11 = x%.2f"
              % (name, area * 1e6, v_to, v_to / 1.57, v_to / 2.11))
    print("3x the 19.4 cm ballistic range needs %.2f m/s (= sqrt(3) x 1.38)"
          % (3 ** 0.5 * 1.38))
    # Range implied by the reported terrestrial jump maxima, 45 deg, vacuum.
    for r in (0.10, 0.27):
        print("a %.2f m ballistic range at 45 deg implies an exit speed of %.2f m/s"
              % (r, (r * G) ** 0.5))

    # --- in-air tail thrust, density argument ---------------------------
    print("\nair/water density ratio = %.2e (1/%.0f): the momentum flux of a tail beat"
          % (RHO_AIR / RHO_WATER, RHO_WATER / RHO_AIR))
    print("at matched kinematics in air is that fraction of its in-water value")


if __name__ == "__main__":
    main()
