"""S11-D sensitivity recomputation. CALCULATED, NOT OBSERVED.

Question: does the canonical chain
  K+ channel gain-of-function -> hyperpolarisation -> less voltage-gated Ca2+ entry
  -> less calcineurin -> outgrowth decelerates later -> longer fin
survive changes in its inputs?

Only one number here comes from a source: the "almost two-fold increase in K+ conductance"
of alf Kcnk5b in Xenopus oocytes (Perathoner et al. 2014). Everything else is an ASSUMPTION,
swept over a range, because it has not been measured in fin cells:
  - baseline K+ fraction of resting conductance (f_K)
  - E_K, E_other
  - T-type-like Ca channel Boltzmann parameters (generic illustrative values, NOT measured
    for zebrafish Cacna1g and NOT taken from a source)
"""
import math

def vm(gk, gother, ek=-90.0, eo=0.0):
    return (gk * ek + gother * eo) / (gk + gother)

def window(v, va=-45.0, ka=6.0, vh=-75.0, kh=5.0):
    """Steady-state open probability m_inf^2 * h_inf: activation x inactivation (generic)."""
    m = 1 / (1 + math.exp(-(v - va) / ka))
    h = 1 / (1 + math.exp((v - vh) / kh))
    return m * m * h

def ca_drive(v, eca=60.0, **kw):
    return window(v, **kw) * max(eca - v, 0.0)

print("Part A: Vm shift from multiplying gK, by baseline K+ fraction (assumed E_K=-90, E_other=0)")
print(f"{'f_K':>5} {'Vm0':>7} | " + " | ".join(f"x{m}: Vm, dCa%" for m in (1.5, 2.0, 4.0)))
for fk in (0.3, 0.5, 0.7, 0.9):
    v0 = vm(fk, 1 - fk); c0 = ca_drive(v0)
    cells = []
    for mult in (1.5, 2.0, 4.0):
        v1 = vm(fk * mult, 1 - fk); c1 = ca_drive(v1)
        cells.append(f"{v1:6.1f} {100*(c1-c0)/c0:+7.1f}%")
    print(f"{fk:5.2f} {v0:7.1f} | " + " | ".join(cells))

print("\nPart B: sign of d(Ca drive)/dVm across baseline Vm (generic T-type parameters)")
peak_v = max((v / 10 for v in range(-1000, 0)), key=ca_drive)
print(f"window-current peak at {peak_v:.1f} mV (calculated from assumed parameters)")
for va in (-55, -45, -35):
    for vh in (-85, -75, -65):
        p = max((v / 10 for v in range(-1000, 0)), key=lambda v: ca_drive(v, va=va, vh=vh))
        print(f"  V_act={va} V_inact={vh}: peak {p:6.1f} mV")

print("\nPart C: chain outcome vs. sign of dVm (the input), at baseline Vm0 on either flank")
for v0 in (-80.0, -60.0, -40.0):
    for dv, label in ((-10.0, "hyperpolarising (oocyte TEVC)"), (+10.0, "depolarising (in vivo DiSBAC2(3))")):
        c0, c1 = ca_drive(v0), ca_drive(v0 + dv)
        direction = "less Ca -> less calcineurin -> LONGER fin predicted" if c1 < c0 else "more Ca -> more calcineurin -> SHORTER/normal fin predicted"
        print(f"  Vm0={v0:6.1f} dVm={dv:+5.1f} [{label:34s}] Ca {100*(c1-c0)/c0:+7.1f}% : {direction}")
