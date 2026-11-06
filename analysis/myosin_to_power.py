#!/usr/bin/env python3
"""PROTEIN -> TISSUE -> ORGAN -> ORGANISM: myosin kinetics to the muscle fraction a fish would need.

This is the chain claim 1103 said the project did not have. develop_to_flight.py starts at an
organ-scale allometry and routes AROUND the unmeasured potential-to-rate junction, so it spans
organ to organism. This one starts at measured PROTEIN-SCALE kinetics and never needs that
junction, because the myosin route to power does not pass through membrane potential at all.

THE MEASURED MOLECULAR INPUTS, all from Bloemink et al. 2013 (PMID 23908353, PMC3779741, full
text, recorded as claim 1099) -- transient kinetics of recombinant human myosin motor domains:

    isoform   K_AD (uM)   K'1k'+2 (uM^-1 s^-1)
    EO/MYH13      352           3.2        <- the superfast candidate, extraocular
    IId           118           1.7
    IIa            80           1.7
    IIb            55           1.7

K_AD is the ADP affinity of actin-bound myosin. A HIGHER K_AD means ADP leaves faster, and ADP
release is the step that limits cross-bridge detachment in fast muscle. Detachment rate sets
maximum shortening velocity. So K_AD is a protein-scale quantity with a standard route to a
whole-muscle one.

THE MODEL STEP IS A MODEL AND IS LABELLED AS ONE. V_max scaling with the ADP-release rate is
textbook muscle biophysics, not a measurement made here, and the proportionality constant is
unknown -- so this computes RATIOS against the fast isoforms rather than absolute velocities.
Everything downstream of the kinetics is therefore a prediction about relative behaviour.

WHAT IT CANNOT DO, stated before the numbers: power is force times velocity, and this chain
carries NO force information. A myosin that cycles faster may generate less force per
cross-bridge, and the Fenn effect and the force-velocity curve mean peak power does not scale
with V_max. So the output is an UPPER BOUND on the velocity gain, and an upper bound on power
only under the explicit assumption that force per cross-bridge is unchanged -- which claim 1099
notes is exactly what Comai et al. 2026 dispute, reporting that myosin-binding protein
composition rather than the motor sets superfast behaviour.
"""
from __future__ import annotations

#: Bloemink 2013, claim 1099. (label, K_AD uM, K'1k'+2 uM^-1 s^-1)
ISOFORMS = [("EO / MYH13 (superfast)", 352.0, 3.2),
            ("IId", 118.0, 1.7),
            ("IIa", 80.0, 1.7),
            ("IIb", 55.0, 1.7)]

REQUIRED_W_PER_KG = 53.0     # claim 998 / 588, the flapping route's requirement
MEASURED_SUPERFAST_W_PER_KG = (6.0, 15.0)   # claims 979, 998
MEASURED_FAST_W_PER_KG = 142.7              # claim 309, Scorpaena fast myotomal, FAST-START
BREAKEVEN_MUSCLE_FRACTION = 0.539           # claim 959, scale=organism; break-even at 53 W/kg


def main() -> int:
    print("  MEASURED PROTEIN-SCALE INPUTS (Bloemink 2013, claim 1099):\n")
    print(f"    {'isoform':26} {'K_AD (uM)':>10} {'K1k2':>7}  {'K_AD / IIb':>11}")
    base = ISOFORMS[-1][1]
    for label, kad, k1k2 in ISOFORMS:
        print(f"    {label:26} {kad:10.0f} {k1k2:7.1f}  {kad/base:11.2f}")

    eo = ISOFORMS[0]
    print("\n  STEP 1 (MODEL): V_max scales with the ADP-release rate, which K_AD reports.")
    for label, kad, _ in ISOFORMS[1:]:
        print(f"    EO vs {label:4} -> velocity ratio about {eo[1]/kad:5.2f}x")
    print(f"    EO vs the FASTEST comparator (IId) is the conservative read: {eo[1]/118:.2f}x")

    print("\n  STEP 2 (ASSUMPTION, stated): if force per cross-bridge is UNCHANGED, power scales")
    print("  with velocity, so power would scale by the same factors.")
    lo, hi = MEASURED_SUPERFAST_W_PER_KG
    print(f"    measured superfast muscle power: {lo}-{hi} W/kg (claims 979, 998)")
    for label, kad, _ in ISOFORMS[1:3]:
        r = eo[1] / kad
        print(f"    scaled by the EO/{label} ratio {r:4.2f}x -> {lo*r:5.1f}-{hi*r:5.1f} W/kg "
              f"against the {REQUIRED_W_PER_KG:.0f} W/kg required")

    # DERIVED, NOT WRITTEN. Three earlier modules tonight printed a hand-written verdict that
    # contradicted the table above it, and the first draft of THIS one said "even on the most
    # favourable comparator ... short by 1.2x" while computing the CONSERVATIVE comparator. The
    # range below is computed from every comparator so the sentence cannot disagree with it.
    ceilings = [(label, lo * (eo[1] / kad), hi * (eo[1] / kad))
                for label, kad, _ in ISOFORMS[1:]]
    worst = min(c[2] for c in ceilings)
    best = max(c[2] for c in ceilings)
    print(f"\n  THE PREDICTED CEILING SPANS {worst:.0f} TO {best:.0f} W/kg across the three")
    print(f"  comparators, against {REQUIRED_W_PER_KG:.0f} W/kg required:")
    for label, c_lo, c_hi in ceilings:
        verdict = "CLEARS" if c_hi >= REQUIRED_W_PER_KG else "short"
        print(f"    vs {label:4} -> {c_lo:5.1f}-{c_hi:5.1f} W/kg   {verdict}")
    clears = sum(1 for _, _, c in ceilings if c >= REQUIRED_W_PER_KG)
    print(f"\n  {clears} of {len(ceilings)} comparators clear the requirement at the top of the")
    print("  measured power range, and none clear it at the bottom. So this does NOT show the")
    print("  kinetics rescue the flapping route, and it does NOT show they cannot -- the answer")
    print("  depends entirely on which fast isoform is the right baseline, and on taking the")
    print("  upper end of a 6-15 W/kg measured range. The honest reading is UNDETERMINED.")
    print("  Choosing IIb as the baseline would make this look like a solved problem; choosing")
    print("  IId would make it look closed. Neither choice is defensible from the kinetics.")

    # ---- the two scales the first version JUMPED OVER ----
    # TISSUE -> ORGAN: whole-animal power is (W/kg of muscle) x (muscle mass). Claim 959 fixes
    # the break-even at 53.9% muscle fraction when muscle delivers the 53 W/kg requirement, so
    # a muscle delivering W W/kg needs a fraction f = 0.539 * (53 / W) to deliver the same
    # whole-animal power. That is an ORGAN-scale quantity -- how much of the animal is muscle --
    # derived from a TISSUE-scale one, and it is what the protein-scale kinetics finally buy.
    print(f"\n  TISSUE -> ORGAN: muscle FRACTION needed, from claim 959's {BREAKEVEN_MUSCLE_FRACTION:.1%}")
    print(f"  break-even at {REQUIRED_W_PER_KG:.0f} W/kg. f = {BREAKEVEN_MUSCLE_FRACTION:.3f} x ({REQUIRED_W_PER_KG:.0f} / W):")
    fracs = []
    for label, c_lo, c_hi in ceilings:
        f_hi = BREAKEVEN_MUSCLE_FRACTION * REQUIRED_W_PER_KG / c_hi
        f_lo = BREAKEVEN_MUSCLE_FRACTION * REQUIRED_W_PER_KG / c_lo
        fracs.append((label, f_hi, f_lo))
        print(f"    vs {label:4} -> {f_hi:5.1%} to {f_lo:5.1%} of body mass as flight muscle")
    print("\n  ORGAN -> ORGANISM: is that anatomically available? Claim 959 records that active")
    print(f"  teleosts REPORTEDLY exceed {BREAKEVEN_MUSCLE_FRACTION:.1%}, which is the only")
    print("  benchmark this project holds, and records it as reported rather than measured here.")
    best_f = min(f for _, f, _ in fracs)
    worst_f = max(f for _, _, f in fracs)
    print(f"    the chain's range is {best_f:.1%} to {worst_f:.1%}. The favourable end is well")
    print(f"    inside what teleosts reportedly reach; the unfavourable end is "
          f"{worst_f/BREAKEVEN_MUSCLE_FRACTION:.1f}x that benchmark and")
    print("    is not anatomically plausible for an animal that must also swim and feed.")
    print("    So the SAME undeterminacy propagates: the protein-scale ambiguity becomes an")
    print("    organ-scale one, and nothing downstream resolves it.")

    print("\n  CELL SCALE IS SKIPPED AND CANNOT BE ADDED (claim 1109). This project holds ZERO")
    print("  live claims carrying a sarcomere, cross-bridge, fibre-type or myofibril quantity --")
    print("  its three cell-scale claims are all about the bioelectric pathway. Adding the step")
    print("  would mean inventing cross-bridge density for zebrafish flight muscle, and the")
    print("  textbook values for other animals would not look invented. Four scales of five.")
    print("  WHAT THE SKIP ASSUMES: that cross-bridge density and sarcomere geometry are")
    print("  unchanged between the myosin whose kinetics were measured (human MYH13, in C2C12")
    print("  cells) and the muscle whose power was measured (bird syrinx, toadfish swimbladder).")

    print("\n  THE ASSUMPTION IS THE WEAK POINT AND IT IS LOAD-BEARING. Power is force times")
    print("  velocity and this chain carries no force data. Comai et al. 2026 (claim 1099,")
    print("  abstract) report that myosin-binding protein composition rather than the motor sets")
    print("  superfast behaviour -- if so, step 2 fails outright and the velocity gain buys")
    print(f"  nothing. Note also that ordinary FAST muscle reaches {MEASURED_FAST_W_PER_KG} W/kg")
    print("  (claim 309) under FAST-START strain, far above any superfast figure, which is the")
    print("  power-versus-frequency trade-off this whole route runs into.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
