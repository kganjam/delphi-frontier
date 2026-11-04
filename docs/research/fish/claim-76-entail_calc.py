"""Calculations for claim-76-entail.md. Run with: python3 -I claim-76-entail_calc.py

Everything here is a CALCULATION from stated inputs. Nothing here is a measurement.
"""
import math

DT = 1 / 120  # s, Miln et al. 2021 frame interval (120 frames/s, full-text)
THRESH = 5.84  # m/s, 1-BL-span glide speed (zebrafish-glide-physics.md, derived)
V_FAST = 1.38  # m/s, fastest of 50 adults (Miln Fig 1a, digitised in S21-D and challenge-75)


def box_peak_ratio(sigma, window):
    """Peak of a Gaussian velocity pulse v=exp(-t^2/2s^2) after averaging over a
    window centred on the true peak (best-case phase)."""
    a = window / (2 * math.sqrt(2) * sigma)
    return math.erf(a) * math.sqrt(2 * math.pi) * sigma / window


def worst_phase_ratio(sigma, window, dt):
    """Same, but the sample grid is offset by dt/2 from the peak (worst phase)."""
    # average of a Gaussian over [c - w/2, c + w/2] with centre c = dt/2
    c = dt / 2
    lo, hi = c - window / 2, c + window / 2
    s2 = math.sqrt(2) * sigma
    return (math.erf(hi / s2) - math.erf(lo / s2)) / 2 * math.sqrt(2 * math.pi) * sigma / window


def fwhm(sigma):
    return 2 * math.sqrt(2 * math.log(2)) * sigma


def sigma_for_bias(bias, window, phase="best"):
    """Largest sigma at which the read-out peak is <= (1 - bias) of the true peak."""
    f = box_peak_ratio if phase == "best" else (lambda s, w: worst_phase_ratio(s, w, DT))
    lo, hi = 1e-5, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid, window) < 1 - bias:
            lo = mid
        else:
            hi = mid
    return lo


print("C1: velocity-peak FWHM below which 120 fps under-reads the peak by >= bias")
for label, window in [("1-frame difference (8.3 ms window)", DT),
                      ("2-frame central difference (16.7 ms window)", 2 * DT)]:
    for phase in ("best", "worst"):
        for bias in (0.05, 0.10):
            s = sigma_for_bias(bias, window, phase)
            print(f"  {label:45s} phase={phase:5s} bias>={bias:.0%}: FWHM <= {fwhm(s)*1e3:5.1f} ms")

print("\n  under-read needed to close the gap entirely: x", round(THRESH / V_FAST, 2))
for fw_ms in (5, 10, 15, 20, 30):
    s = fw_ms / 1e3 / fwhm(1.0)
    print(f"  FWHM {fw_ms:2d} ms: 1-frame best {box_peak_ratio(s, DT):.3f}, worst {worst_phase_ratio(s, DT, DT):.3f}; "
          f"2-frame best {box_peak_ratio(s, 2*DT):.3f}")

print("\nC4: temperature sensitivity that keeps the fastest fish's margin >= 4 at 28 C")
m23 = THRESH / V_FAST
fac = m23 / 4.0
print(f"  margin at 23 C = {m23:.3f}; allowed speed factor = {fac:.4f}")
print(f"  max Q10 over 23->28 C = {fac ** (10 / 5):.3f}")
for q10, who in [(1.81, "whiting (Ozbilgin 2002, search-summary)"),
                 (1.90, "Eleginops maclovinus (Fernandez 2002, search-summary)")]:
    v = V_FAST * q10 ** 0.5
    print(f"  if Q10={q10} [{who}]: 28 C speed {v:.2f} m/s, margin {THRESH / v:.2f}")

print("\nC2: size sensitivity. Threshold V ~ sqrt(W/S) ~ L^0.5 for a 1-BL-span wing (m ~ L^3, S ~ L^2).")
print("  fast-start speed ~ L^a; margin ~ L^(0.5 - a)")
r = 40 / 33.0
for a in (0.0, 0.5, 1.0):
    print(f"  a={a}: margin shift for 40 vs 33 mm = x{r ** (0.5 - a):.3f}")
