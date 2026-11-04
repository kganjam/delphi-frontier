# S21-D-D-D: re-run S21-D-D's frame-rate bias calculation with a MEASURED speed-profile shape.
# Every number this script prints is CALCULATED or SIMULATED, not observed.
# The only observed input is the digitised trace in S21-D-D-fig2b-trace.txt
# (Danos & Lauder 2012 J Exp Biol 215:1854, Fig. 2B, 1 mPa s panel, digitised by me from the PDF).
# Run: python3 S21-D-D-deepen-sim.py   (numpy only; seed fixed)
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(1)
FIX_ONSET = True

# ---------- (A) S21-D-D's alpha-pulse model, extended to shorter rise times ----------
def alpha_x(tp, dt=1e-5, T=0.25):
    t = np.arange(0, T, dt)
    v = (t / tp) * np.exp(1 - t / tp)           # peak 1 m/s at t = tp
    return t, np.cumsum(v) * dt

def max_of_trials(t, x, fps, sx, ntrial, nsim, tmax):
    dt = 1 / fps
    out = np.empty(nsim)
    for i in range(nsim):
        best = 0.0
        for _ in range(ntrial):
            # start one frame BEFORE motion onset (x = 0 there), so no displacement is lost.
            # S21-D-D's script started sampling at t in [0, dt) and so discarded the first
            # partial frame of motion; FIX_ONSET=False reproduces that behaviour.
            t0 = rng.uniform(0, dt) - (dt if FIX_ONSET else 0.0)
            ts = np.arange(t0, tmax, dt)
            xs = np.interp(ts, t, x, left=0.0) + rng.normal(0, sx, len(ts))
            best = max(best, np.max(np.abs(np.diff(xs))) / dt)
        out[i] = best
    return out

print("(A0) S21-D-D's original sampling (onset artefact kept), alpha pulse, 120 fps, max of 4, sx=0")
FIX_ONSET = False
for tp in [0.005, 0.010, 0.020]:
    t, x = alpha_x(tp)
    r = max_of_trials(t, x, 120, 0.0, 4, 1500, 0.15)
    print(f"  tp={tp*1e3:5.1f} ms  mean={r.mean():.3f}")
FIX_ONSET = True
print("(A) alpha pulse, 120 fps, max of 4: mean measured/true peak  [p5, p95]")
for tp in [0.00125, 0.0025, 0.005, 0.010, 0.0256]:
    t, x = alpha_x(tp)
    for sx in [0.0, 1.0e-3]:
        r = max_of_trials(t, x, 120, sx, 4, 1500, min(0.24, 8 * tp + 0.05))
        print(f"  tp={tp*1e3:6.2f} ms  sx={sx*1e3:.1f} mm  mean={r.mean():.3f}  "
              f"p5={np.percentile(r,5):.3f}  p95={np.percentile(r,95):.3f}")

# Rise time at which a noise-free 120 fps max-of-4 reads only 0.316 of the true peak
# (the reading needed for 1.38 m/s to hide a 4.37 m/s true peak).
print("  noise-free 120 fps under-read vs rise time (worst phase over 4 trials ~ mean):")
for tp in [0.0002, 0.0004, 0.0006, 0.0008, 0.001]:
    t, x = alpha_x(tp, dt=1e-6, T=0.05)
    r = max_of_trials(t, x, 120, 0.0, 4, 400, 0.04)
    print(f"    tp={tp*1e3:.1f} ms  mean={r.mean():.3f}")

# ---------- (B) the measured profile shape ----------
d = np.loadtxt(os.path.join(HERE, "S21-D-D-fig2b-trace.txt"))
tm, vm = d[:, 0] * 1e-3, d[:, 1]
tg = np.arange(0, tm.max(), 1e-5)
vg = np.interp(tg, tm, vm)
# The published trace is unsmoothed 1 ms differencing (author's method), so it carries noise.
# Use a 3 ms running mean as the 'true' smooth profile.
k = int(0.003 / 1e-5)
vs = np.convolve(vg, np.ones(k) / k, mode="same")
vs[: k // 2] = vg[: k // 2]
vs[-k // 2:] = vg[-k // 2:]
xs_true = np.cumsum(vs) * 1e-5
# Residual jitter of the published 1 ms trace about the smooth curve (noise proxy)
resid = vm - np.interp(tm, tg, vs)
print("\n(B) measured profile (Danos & Lauder Fig 2B, 1 mPa s)")
print(f"  raw digitised max {vm.max():.3f} m/s at {tm[vm.argmax()]*1e3:.1f} ms;"
      f" smoothed max {vs.max():.3f} m/s at {tg[vs.argmax()]*1e3:.1f} ms")
print(f"  raw max / smoothed max = {vm.max()/vs.max():.3f};"
      f"  residual SD of raw about smooth = {resid.std():.3f} m/s")
# time from 10% to 90% of smoothed peak
pk = vs.max()
i10 = np.argmax(vs >= 0.1 * pk); i90 = np.argmax(vs >= 0.9 * pk)
print(f"  smoothed rise 10->90% of peak: {(tg[i90]-tg[i10])*1e3:.1f} ms;"
      f" time above 90% of peak: {(vs >= 0.9*pk).sum()*1e-5*1e3:.1f} ms")

# Noise-free 120 fps, all phases, single trial: min and max reading over phase
ph = np.linspace(0, 1 / 120, 200, endpoint=False)
reads = []
for p in ph:
    ts = np.arange(p - 1 / 120, tg.max(), 1 / 120)
    xx = np.interp(ts, tg, xs_true, left=0.0)
    reads.append(np.max(np.diff(xx)) * 120)
reads = np.array(reads) / pk
print(f"  120 fps noise-free, single trial, over phase: min={reads.min():.3f} "
      f"mean={reads.mean():.3f} max={reads.max():.3f} (x true smoothed peak)")

print("  120 fps, max of 4, with position noise (mean [p5, p95] of measured/true):")
for sx in [0.0, 0.25e-3, 0.5e-3, 1.0e-3]:
    r = max_of_trials(tg, xs_true, 120, sx, 4, 1500, tg.max()) / pk
    print(f"    sx={sx*1e3:.2f} mm  mean={r.mean():.3f}  p5={np.percentile(r,5):.3f}"
          f"  p95={np.percentile(r,95):.3f}")
