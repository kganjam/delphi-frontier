#!/usr/bin/env python3
"""Can elastic strain-energy storage recover the inertial term in the flapping budget?

THE QUESTION. Claim 588 computed the powered-flapping budget as induced 33 + profile 2 +
inertial 18 = 53 W/kg, against 35-71 W/kg available. The 18 W/kg inertial term is the cost of
accelerating and decelerating the fin twice per cycle. If the fin stores that kinetic energy
elastically at stroke reversal and returns it, the budget falls to ~35 W/kg and the route is
comfortable. If it does not, the budget is ~53 W/kg and the route survives only in the upper
half of the available range. The project has carried "35 or 52" as an open disjunction for
this reason.

WHY IT LOOKED UNANSWERABLE. PubMed returns ZERO for every phrasing of fin elastic energy
storage (checked: "actinotrichia elastoidin mechanical properties fish fin", "actinotrichia
collagen fin ray elasticity", "fish fin ray elastic energy storage"), against six substantive
hits for the control "actinotrichia fin". So no one has measured the storage fraction.

WHY IT IS ANSWERABLE ANYWAY. Elastic storage recovers inertial work only near mechanical
resonance. A structure driven far BELOW its natural frequency is quasi-static: it deflects in
phase with the load, stores negligible strain energy at reversal, and returns none of the
kinetic energy. So the question "is the storage fraction large" is the question "is the fin's
natural frequency near the 53 Hz beat frequency" -- and that is computable from a stiffness
that HAS been measured.

THE MEASURED INPUT. Flammang, Alben, Madden & Lauder 2013, J Morphol 274:1044-59
(PMID 23720195, doi 10.1002/jmor.20161), abstract, read_level=abstract:
  "Flexural stiffness of the fin ray was calculated to be 565 x 10^-6 Nm2"
for a bluegill sunfish (Lepomis macrochirus) pectoral fin ray.

THE CROSS-SPECIES PROBLEM, AND WHY IT DOES NOT SINK THIS. Bluegill is not zebrafish, and an
earlier claim in this project was corrected for exactly this kind of mapping. Scaling EI alone
across species would be indefensible. But the natural frequency is far more robust than EI,
because stiffness and inertia scale together. Under geometric similarity:
    k ~ EI/L^3 ~ L^4/L^3 = L        m ~ L^3        f ~ sqrt(k/m) ~ sqrt(L/L^3) = 1/L
so the dimensional errors partly cancel and f scales as the INVERSE of length. The script
therefore reports the sensitivity explicitly: how wrong would the assumed geometry have to be
for the conclusion to flip? If the margin is orders of magnitude, the conclusion stands on the
measured stiffness and not on the assumed dimensions.

WHAT IS ASSUMED, STATED SO IT CANNOT BE MISTAKEN FOR MEASUREMENT. The bluegill ray length and
cross-section below are ASSUMED, not read. They are labelled ASSUMED in the output and the
sensitivity analysis exists precisely because they are not measurements.
"""
import math

# ---------------------------------------------------------------- measured
EI_BLUEGILL = 565e-6        # N m^2   MEASURED, Flammang 2013 abstract
BEAT_HZ     = 53.0          # the flapping frequency claim 588's budget requires

# ---------------------------------------------------------------- assumed
L_BLUEGILL   = 0.035        # m       ASSUMED pectoral ray length, ~15 cm fish
D_RAY        = 0.5e-3       # m       ASSUMED ray diameter
RHO_BONE     = 2000.0       # kg/m^3  bone/collagen composite
L_ZEBRAFISH  = 0.007        # m       ASSUMED zebrafish pectoral ray length, ~30 mm fish
RHO_AIR      = 1.2          # kg/m^3  the flight phase is in AIR, not water
CHORD_FRAC   = 10.0         # entrained-air column width, in ray diameters (generous)

BETA1_SQ = 1.875104**2      # first cantilever mode


def cantilever_hz(EI, mass_per_len, L):
    """First bending mode of a cantilever. f = (b1^2/2pi) sqrt(EI / (mu L^4))."""
    return (BETA1_SQ / (2 * math.pi)) * math.sqrt(EI / (mass_per_len * L**4))


def ray_mass_per_len(d, rho=RHO_BONE):
    return rho * math.pi * (d / 2) ** 2


def added_mass_per_len(d, chord_frac=CHORD_FRAC):
    """Air entrained by a flapping ray, as a cylinder of air of diameter chord_frac*d."""
    b = chord_frac * d
    return RHO_AIR * math.pi * (b / 2) ** 2


def report():
    print(__doc__.split("THE MEASURED INPUT")[0].strip()[:0] or "", end="")
    print("=" * 78)
    print("FIN RESONANCE vs THE 53 Hz BEAT")
    print("=" * 78)

    mu_ray = ray_mass_per_len(D_RAY)
    mu_air = added_mass_per_len(D_RAY)
    mu_tot = mu_ray + mu_air

    print(f"\n  MEASURED  bluegill ray flexural stiffness EI = {EI_BLUEGILL*1e6:.0f}e-6 N m^2")
    print(f"            (Flammang 2013, PMID 23720195, read_level=abstract)")
    print(f"  ASSUMED   bluegill ray length  {L_BLUEGILL*1000:.0f} mm, diameter {D_RAY*1000:.2f} mm")
    print(f"  ASSUMED   zebrafish ray length {L_ZEBRAFISH*1000:.0f} mm")
    print(f"\n  ray mass/length     {mu_ray*1e3:.4f} g/m")
    print(f"  entrained air/length{mu_air*1e3:.4f} g/m   ({100*mu_air/mu_tot:.1f}% of total)")
    print("  -> in AIR the ray's own inertia dominates; added mass is a minor correction.")
    print("     (In water it would not be, which is why the flight phase matters.)")

    f_blue = cantilever_hz(EI_BLUEGILL, mu_tot, L_BLUEGILL)
    print(f"\n  bluegill first bending mode      {f_blue:>9.0f} Hz")

    # scale to zebrafish: geometric similarity gives f ~ 1/L
    ratio = L_BLUEGILL / L_ZEBRAFISH
    f_zeb = f_blue * ratio
    print(f"  zebrafish, scaled by 1/L ({ratio:.1f}x)   {f_zeb:>9.0f} Hz")
    print(f"  required beat frequency          {BEAT_HZ:>9.0f} Hz")
    print(f"  ratio f_natural / f_beat         {f_zeb/BEAT_HZ:>9.1f}x")

    # the actuation effect: Alben 2007 measured >10x stiffness variation with muscle actuation
    f_soft = f_zeb / math.sqrt(10.0)
    print(f"\n  Alben 2007 (PMID 17251142) measured >10x stiffness variation with actuation.")
    print(f"  At the SOFTEST end (EI/10):      {f_soft:>9.0f} Hz  -> still {f_soft/BEAT_HZ:.1f}x the beat")

    # ---------------------------------------------------------- sensitivity
    print("\n" + "-" * 78)
    print("SENSITIVITY -- how wrong must the ASSUMED geometry be to flip the conclusion?")
    print("-" * 78)
    need = f_zeb / BEAT_HZ
    print(f"  f_natural must fall by {need:.0f}x to reach the beat frequency.")
    print(f"  via ray length alone   : L must be {need**0.5:>6.2f}x longer   "
          f"({L_ZEBRAFISH*1000*need**0.5:.0f} mm on a 30 mm fish)")
    print(f"  via stiffness alone    : EI must be {need**2:>6.0f}x smaller")
    print(f"  via ray mass alone     : mu must be {need**2:>6.0f}x heavier")
    needsoft = f_soft / BEAT_HZ
    print(f"  with the 10x soft state, length must still be {needsoft**0.5:.2f}x longer "
          f"({L_ZEBRAFISH*1000*needsoft**0.5:.0f} mm)")

    # ---------------------------------------------------------- verdict
    print("\n" + "=" * 78)
    quasi = f_zeb > 5 * BEAT_HZ
    if quasi:
        print("VERDICT: the fin is driven FAR BELOW resonance -- quasi-static.")
        print("  A structure driven well below its natural frequency deflects in phase with")
        print("  the load and stores negligible strain energy at stroke reversal. The 18 W/kg")
        print("  inertial term is therefore NOT recovered elastically.")
        print(f"  The flapping budget is ~53 W/kg, NOT ~35 W/kg.")
        print("  Against 35-71 W/kg available, the route survives only in the UPPER HALF")
        print("  of the available muscle-power range. It is not excluded; it is tight.")
    else:
        print("VERDICT: the fin is near resonance -- elastic storage is available.")
    print("=" * 78)

    return {"f_zebrafish_hz": f_zeb, "f_bluegill_hz": f_blue,
            "ratio_to_beat": f_zeb / BEAT_HZ, "quasi_static": quasi}


# -------------------------------------------------------------------- controls
def controls():
    """Both arms must exercise the verdict. A control that can only pass is not a control."""
    print("\nCONTROLS")
    ok = True

    # 1. POSITIVE: a deliberately floppy ray MUST come out near resonance. If this says
    #    'quasi-static' too, the verdict is a constant and the whole script proves nothing.
    mu = ray_mass_per_len(D_RAY) + added_mass_per_len(D_RAY)
    f_floppy = cantilever_hz(EI_BLUEGILL / 1e5, mu, L_BLUEGILL) * (L_BLUEGILL / L_ZEBRAFISH)
    arm1 = f_floppy < 5 * BEAT_HZ
    print(f"  [{'ok' if arm1 else 'FAIL'}] floppy ray (EI/1e5) -> {f_floppy:.0f} Hz, "
          f"NOT quasi-static as required")
    ok &= arm1

    # 2. NEGATIVE: the real stiffness must come out quasi-static.
    f_real = cantilever_hz(EI_BLUEGILL, mu, L_BLUEGILL) * (L_BLUEGILL / L_ZEBRAFISH)
    arm2 = f_real > 5 * BEAT_HZ
    print(f"  [{'ok' if arm2 else 'FAIL'}] measured stiffness  -> {f_real:.0f} Hz, quasi-static")
    ok &= arm2

    # 3. The scaling must actually depend on L. A formula ignoring its argument would pass
    #    arms 1 and 2 and be wrong.
    a = cantilever_hz(EI_BLUEGILL, mu, 0.01)
    b = cantilever_hz(EI_BLUEGILL, mu, 0.02)
    arm3 = abs(a / b - 4.0) < 0.01     # f ~ 1/L^2 at fixed mu
    print(f"  [{'ok' if arm3 else 'FAIL'}] f depends on L as 1/L^2 at fixed mu "
          f"(got {a/b:.3f}x for a 2x length change)")
    ok &= arm3

    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    r = report()
    if not controls():
        raise SystemExit("controls failed -- the verdict above is not trustworthy")
