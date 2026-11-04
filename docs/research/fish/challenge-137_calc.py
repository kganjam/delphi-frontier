"""challenge-137: an independent check on S10-D-D-D's muscle power at 21.9 Hz.

Every printed number is a CALCULATION. Nothing here is a measurement.

Measured inputs (Mead et al. 2020, Biophys J 119:806, PMC7451861, read full-text in this challenge):
  sigma0 = 76 mN/mm^2; twitch/tetanus = 0.91; twitch FWHM = 11 ms, complete within 25 ms;
  force = 0.86 of isometric at a constant shortening speed of 7 L/s; Vmax estimated at >= 45 L/s;
  work loops of 8 % peak-to-peak sinusoidal strain (1.01-1.09 L0), 28 C, one 0.4 ms pulse per cycle;
  net work 2.63 J/kg at 40 Hz, and power of 134.4 W/kg at 80 Hz and 122.9 W/kg at 100 Hz.

Model (an ASSUMPTION, written by me): force = sigma0 * A(t) * FV(v).
  A(t) is a saturating sum of twitches, each shaped (t/tp)exp(1 - t/tp) with tp = 4.5 ms, which gives
  an 11 ms FWHM and 6 % of peak left at 25 ms. Saturation is chosen so that a single twitch peaks at 0.91.
  FV is linear on the shortening side, with Vmax = 50 L/s, so FV(7 L/s) = 0.86.
  FV on the lengthening side is 1 + 0.3 * (1 - exp(-|v| / 5 L/s)).
  Muscle density is 1060 kg/m^3.
The model is calibrated against the measured 40 / 80 / 100 Hz single-twitch values. Phase is then
optimised, and the model is used to predict 21.9 Hz with 1 to 4 pulses per cycle.
"""
import math

SIG0, RHO, STRAIN, TP = 76e3, 1060.0, 0.08, 4.5e-3
C_SAT = -math.log(1 - 0.91)          # gives a single-twitch peak of 0.91
VMAX = 50.0


def tw(t):
    if t <= 0:
        return 0.0
    x = t / TP
    return x * math.exp(1 - x)


def fv(v):  # v > 0 means shortening, in L/s
    if v >= 0:
        return max(0.0, 1 - v / VMAX)
    return 1 + 0.3 * (1 - math.exp(v / 5.0))


def net_work(freq, n_pulses, phase, ipi, eps=STRAIN, n=4000):
    """Net work per cycle (J/kg) at steady state. Pulses repeat every cycle, and the
    activation left over from earlier cycles is included."""
    T = 1 / freq
    dt = T / n
    W = 0.0
    for i in range(n):
        t = i * dt
        # length = L0 * (1.05 + eps/2 * cos(2 pi f t)); shortening runs from t = 0 to T/2
        v = eps / 2 * 2 * math.pi * freq * math.sin(2 * math.pi * freq * t)   # shortening speed
        s = 0.0
        for k in range(-6, 1):            # this cycle and the six before it
            for p in range(n_pulses):
                s += tw(t - (k * T + phase * T + p * ipi))
        A = 1 - math.exp(-C_SAT * s)
        F = SIG0 * A * fv(v)
        W += F * v * dt                  # positive while shortening, negative while lengthening
    return W / RHO


def best(freq, n_pulses, eps=STRAIN):
    out = (-1e9, None)
    phases = [i / 40 - 0.5 for i in range(40)]
    ipis = [None] if n_pulses == 1 else [x * 1e-3 for x in (3, 4, 5, 6, 8, 10)]
    for ph in phases:
        for ipi in ipis:
            w = net_work(freq, n_pulses, ph, ipi or 0, eps, n=600)
            if w > out[0]:
                out = (w, (ph, ipi))
    w = net_work(freq, n_pulses, out[1][0], out[1][1] or 0, eps)
    return w, out[1]


rect = SIG0 * STRAIN / RHO
print(f"rectangle at 8 %: {rect:.2f} J/kg")
print("== Calibration, single twitch, optimal phase (measured: 40 Hz 2.63; 80 Hz 1.68; 100 Hz 1.23 J/kg)")
for fr in (40, 60, 80, 100, 120):
    w, p = best(fr, 1)
    print(f"  {fr:3d} Hz: model {w:.2f} J/kg = {w*fr:.0f} W/kg, fill {w/rect:.2f}")
print("== Prediction at 21.9 Hz")
for npul in (1, 2, 3, 4):
    w, p = best(21.9, npul)
    print(f"  {npul} pulse(s): {w:.2f} J/kg -> {w*21.9:.0f} W/kg, fill {w/rect:.2f}, (phase, ipi)={p}")
for eps in (0.10, 0.12):
    w, p = best(21.9, 3, eps)
    print(f"  3 pulses, strain {eps:.2f}: {w:.2f} J/kg -> {w*21.9:.0f} W/kg (FL penalty NOT applied)")

# ---------------------------------------------------------------------------------------------
# Part 2. The fixed 11 ms twitch above FAILS calibration: it gives negative net work at 80 and
# 100 Hz, where the measured values are +1.68 and +1.23 J/kg. So I fit an empirical in-loop twitch,
# (1 - exp(-t/tr)) * exp(-t/td) normalised to 1, against the three measured single-twitch points.
# I then use the fitted shape to predict 21.9 Hz with a burst of pulses. This is a CALCULATION.
# The fitted FWHM is about 4 ms, while the measured isometric FWHM is 11 ms. Read the fit as an
# in-loop effective activation that absorbs shortening deactivation; it is not a twitch measurement.
MEAS = {40: 2.63, 80: 134.4 / 80, 100: 122.9 / 100}


def make_tw(tr, td):
    norm = max((1 - math.exp(-t * 1e-5 / tr)) * math.exp(-t * 1e-5 / td) for t in range(1, 20000))
    return lambda t: 0.0 if t <= 0 else (1 - math.exp(-t / tr)) * math.exp(-t / td) / norm


def opt(freq, npul, ipis, n=400):
    b = (-9.0, None)
    for i in range(40):
        for ipi in ipis:
            w = net_work(freq, npul, i / 40 - 0.5, ipi, n=n)
            if w > b[0]:
                b = (w, (i / 40 - 0.5, ipi))
    return net_work(freq, npul, b[1][0], b[1][1], n=2000), b[1]


fits = []
for tr in (0.5e-3, 1e-3, 1.5e-3, 2e-3, 3e-3):
    for td in (2e-3, 3e-3, 4e-3, 5e-3, 6e-3, 8e-3):
        tw = make_tw(tr, td)
        ws = {f: max(net_work(f, 1, i / 30 - 0.5, 0, n=300) for i in range(30)) for f in MEAS}
        fits.append((sum((ws[f] - MEAS[f]) ** 2 for f in MEAS), tr, td, ws))
fits.sort(key=lambda r: r[0])
print("\n== Part 2: in-loop twitch fitted to measured single-twitch work (J/kg)")
for err, tr, td, ws in fits[:3]:
    print(f"  tr={tr*1e3:.1f} ms td={td*1e3:.1f} ms  SSE={err:.3f}  model 40/80/100 Hz = "
          + " / ".join(f"{ws[f]:.2f}" for f in MEAS) + "  (measured 2.63 / 1.68 / 1.23)")
need = 96.5  # W/kg: S10-D-D-D's flip threshold for its most generous corner, recomputed independently
need2 = 120.5  # the same corner at C_D,pro = 0.10
for err, tr, td, ws in fits[:3]:
    tw = make_tw(tr, td)
    print(f"  -- shape tr={tr*1e3:.1f} td={td*1e3:.1f}: prediction at 21.9 Hz, 8 % strain")
    for npul in (1, 2, 3, 4, 5, 6, 8):
        ipis = [0] if npul == 1 else [2e-3, 2.5e-3, 3e-3, 4e-3, 6e-3]
        w, p = opt(21.9, npul, ipis)
        P = w * 21.9
        print(f"     {npul} pulse(s): {w:.2f} J/kg -> {P:5.1f} W/kg, fill {w/rect:.2f};"
              f" corner CDpro=0.05 {'FLIPS' if P >= need else 'fails'} (need {need}),"
              f" CDpro=0.10 {'FLIPS' if P >= need2 else 'fails'} (need {need2})")
