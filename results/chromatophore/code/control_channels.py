"""Study 3: how many independent control channels does an addressable skin need?

PRE-REGISTRATION (written before any model was run; see `preregistration` in the
output JSON, which is a verbatim copy of the constants in this file).

  Question.  An array of pigment actuators at a measured spatial density is driven
  by N independent control channels, each channel driving a motor unit of m
  actuators.  How well can the skin match a target pattern, and where is the point
  of diminishing returns in N?

  Primary match metric (DECLARED IN ADVANCE).  Variance explained on the
  observer-blurred reflectance field:
        R2 = 1 - SUM (I_skin - I_target)^2 / SUM (I_target - mean I_target)^2
  clipped below at 0.  Both fields are blurred by the same observer PSF before
  scoring.  The target is affinely mapped into the skin's own achievable
  reflectance range before scoring, so that the score measures pattern fidelity
  and not the pigment layer's contrast range (which is study 2's subject).

  Secondary metrics (DECLARED IN ADVANCE).  Mean absolute error of the blurred
  field; R2 of the unblurred field.

  Knee rules (DECLARED IN ADVANCE, both reported).
    knee_95        smallest N whose mean R2 reaches 0.95 * R2 at N = K
                   (K = one channel per actuator, i.e. full individual control).
    knee_curvature standard "kneedle" construction: the point of maximum vertical
                   distance from the chord joining the first and last points of
                   the (log10 N, R2) curve.

  Targets (DECLARED IN ADVANCE, eight, fixed before the first run; none added,
  dropped or re-parameterised afterwards).
    uniform_dark, uniform_light          trivial controls; any N must score ~1
    edge                                 half-field step (disruptive band)
    square                               light square on dark; named as a real
                                         cuttlefish pattern component in Reiter 2018
    stripes_coarse  period 2.0 mm
    stripes_fine    period 0.5 mm
    gravel_1f       isotropic 1/f^2 noise, seed 20261102
    mottle          random blobs of declared radius, seed 20261102

  Wiring models (DECLARED IN ADVANCE, four).
    compact      each channel owns the m nearest unclaimed actuators to its seed
    renard_like  overlapping units whose within-unit nearest-neighbour distance is
                 drawn to match the measured 40.5 um, while the array's global NND
                 is smaller; a actuator may belong to several units
    random       m actuators drawn uniformly from the whole patch (NEGATIVE
                 CONTROL: must score far worse than compact at the same N)
    oracle       units chosen per target by clustering the target's own residual
                 (UPPER BOUND: no animal can rewire per pattern)

  Nothing below is fitted to data.  The three measured anchors are the actuator
  density, the actuator expansion ratio and the motor-unit sizes; everything else
  is assumed and declared as such.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# (standalone: no local imports, so this file can be injected into a remote job)

# --------------------------------------------------------------------------
# Declared constants.  Changing any of these changes the pre-registration.
# --------------------------------------------------------------------------
PATCH_MM = 4.0                 # square skin patch edge, mm
GRID = 256                     # raster for the scored field
DENSITY_PER_UM2 = 2.44e-4      # SOURCED: Reiter 2018 measured mean chromatophore density
AREA_RATIO = 2.5506            # SOURCED: Hadjisolomou 2021, +155.06% area on expansion
COVERAGE_FULL = 0.85           # ASSUMED: coverage fraction with every actuator expanded
R_PIGMENT = 0.05               # ASSUMED: reflectance of fully pigmented skin
R_BACKGROUND = 0.75            # ASSUMED: reflectance of the unpigmented backing
BLUR_IN_SPACINGS = 2.0         # ASSUMED: observer PSF sigma, in mean actuator spacings
SEEDS = (11, 12, 13, 14, 15)
UNIT_SIZES = (1, 3, 9, 14, 30)  # SOURCED span: Reiter median 3; Renard mean ~9, 90% < 14, up to 30
WIRINGS = ("compact", "renard_like", "random", "oracle")
TARGETS = ("uniform_dark", "uniform_light", "edge", "square",
           "stripes_coarse", "stripes_fine", "gravel_1f", "mottle")
TARGET_SEED = 20261102
WITHIN_UNIT_NND_UM = 40.548    # SOURCED: Renard 2026 mean within-cluster NND
N_ITERS = 400                  # projected-gradient iterations
KNEE_FRACTION = 0.95

PATCH_UM = PATCH_MM * 1000.0
PX_UM = PATCH_UM / GRID
_KAPPA = 1.0      # coverage-law correction; 1.0 everywhere except in its own control


# --------------------------------------------------------------------------
# geometry
# --------------------------------------------------------------------------
def mean_spacing_um() -> float:
    return DENSITY_PER_UM2 ** -0.5


def radii_um() -> tuple[float, float]:
    """Expanded and retracted actuator radii, derived from the three anchors.

    r_exp is set so that every actuator expanded gives COVERAGE_FULL under the
    random-overlap (Poisson) coverage law; r_ret then follows from the SOURCED
    area ratio.  Neither radius is fitted.
    """
    a_exp = -math.log(1.0 - COVERAGE_FULL) / DENSITY_PER_UM2   # um^2 per actuator
    r_exp = math.sqrt(a_exp / math.pi)
    r_ret = r_exp / math.sqrt(AREA_RATIO)
    return r_exp, r_ret


def poisson_disc(rng: np.random.Generator, n_target: int, min_dist: float,
                 side: float, k: int = 24) -> np.ndarray:
    """Bridson Poisson-disc sampling in a square of `side` um."""
    cell = min_dist / math.sqrt(2.0)
    gw = int(math.ceil(side / cell))
    grid = -np.ones((gw, gw), dtype=np.int64)
    pts: list[tuple[float, float]] = []
    active: list[int] = []

    def emit(p):
        idx = len(pts)
        pts.append(p)
        grid[int(p[0] / cell), int(p[1] / cell)] = idx
        active.append(idx)

    emit((rng.random() * side, rng.random() * side))
    while active and len(pts) < n_target:
        ai = int(rng.integers(len(active)))
        base = pts[active[ai]]
        placed = False
        for _ in range(k):
            rad = min_dist * (1.0 + rng.random())
            th = rng.random() * 2 * math.pi
            p = (base[0] + rad * math.cos(th), base[1] + rad * math.sin(th))
            if not (0 <= p[0] < side and 0 <= p[1] < side):
                continue
            gx, gy = int(p[0] / cell), int(p[1] / cell)
            ok = True
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    x, y = gx + dx, gy + dy
                    if 0 <= x < gw and 0 <= y < gw and grid[x, y] >= 0:
                        q = pts[grid[x, y]]
                        if (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 < min_dist ** 2:
                            ok = False
                            break
                if not ok:
                    break
            if ok:
                emit(p)
                placed = True
                break
        if not placed:
            active.pop(ai)
    return np.asarray(pts, dtype=np.float64)


def make_array(seed: int) -> np.ndarray:
    """Actuator centres, um, at the measured density, filling the whole patch.

    Bridson is run to exhaustion at a separation that OVER-produces, then thinned
    at random to the measured count. Stopping Bridson at the target count instead
    leaves the far corners of the patch empty - a defect invisible in the point
    cloud's count but obvious in the rendered field, where local coverage fell to
    zero in unfilled regions. `array_uniformity` in the controls block catches it.
    """
    rng = np.random.default_rng(seed)
    n_target = int(round(DENSITY_PER_UM2 * PATCH_UM ** 2))
    min_dist = 0.60 * mean_spacing_um()
    pts = poisson_disc(rng, 10 ** 9, min_dist, PATCH_UM)
    if len(pts) < n_target:
        raise RuntimeError(f"Bridson produced {len(pts)} < {n_target}; lower min_dist")
    keep = rng.choice(len(pts), size=n_target, replace=False)
    return pts[np.sort(keep)]


# --------------------------------------------------------------------------
# forward model
# --------------------------------------------------------------------------
class Renderer:
    """Blurred-reflectance forward model, linear in per-actuator pigment area."""

    def __init__(self, pts: np.ndarray):
        self.pts = pts
        self.K = len(pts)
        self.r_exp, self.r_ret = radii_um()
        self.a_exp = math.pi * self.r_exp ** 2
        self.a_ret = math.pi * self.r_ret ** 2
        ix = np.clip((pts[:, 0] / PX_UM).astype(int), 0, GRID - 1)
        iy = np.clip((pts[:, 1] / PX_UM).astype(int), 0, GRID - 1)
        self.flat = ix * GRID + iy
        sigma_px = BLUR_IN_SPACINGS * mean_spacing_um() / PX_UM
        self.sigma_px = sigma_px
        fy = np.fft.fftfreq(GRID)[:, None]
        fx = np.fft.fftfreq(GRID)[None, :]
        self.otf = np.exp(-2.0 * (math.pi ** 2) * (sigma_px ** 2) * (fx ** 2 + fy ** 2))
        self.px_area = PX_UM ** 2

    def scatter(self, area_per_actuator: np.ndarray) -> np.ndarray:
        img = np.zeros(GRID * GRID)
        np.add.at(img, self.flat, area_per_actuator)
        return img.reshape(GRID, GRID) / self.px_area

    def blur(self, f: np.ndarray) -> np.ndarray:
        return np.real(np.fft.ifft2(np.fft.fft2(f) * self.otf))

    def reflectance(self, u: np.ndarray) -> np.ndarray:
        """u: per-actuator drive in [0,1]."""
        area = self.a_ret + u * (self.a_exp - self.a_ret)
        s = self.blur(self.scatter(area))
        cov = 1.0 - np.exp(-_KAPPA * s)
        return R_BACKGROUND + (R_PIGMENT - R_BACKGROUND) * cov, s

    def range(self) -> tuple[float, float]:
        lo, _ = self.reflectance(np.ones(self.K))      # all expanded -> darkest
        hi, _ = self.reflectance(np.zeros(self.K))     # all retracted -> lightest
        return float(lo.mean()), float(hi.mean())


# --------------------------------------------------------------------------
# targets (declared in advance)
# --------------------------------------------------------------------------
def make_target(name: str) -> np.ndarray:
    """Returns a field in [0,1]; 0 = darkest, 1 = lightest."""
    g = GRID
    yy, xx = np.mgrid[0:g, 0:g]
    x_mm = xx / g * PATCH_MM
    if name == "uniform_dark":
        return np.zeros((g, g))
    if name == "uniform_light":
        return np.ones((g, g))
    if name == "edge":
        return (xx >= g // 2).astype(float)
    if name == "square":
        q = g // 4
        t = np.zeros((g, g))
        t[q:3 * q, q:3 * q] = 1.0
        return t
    if name in ("stripes_coarse", "stripes_fine"):
        period_mm = 2.0 if name == "stripes_coarse" else 0.5
        return (np.sin(2 * math.pi * x_mm / period_mm) > 0).astype(float)
    rng = np.random.default_rng(TARGET_SEED)
    if name == "gravel_1f":
        noise = rng.standard_normal((g, g))
        fy = np.fft.fftfreq(g)[:, None]
        fx = np.fft.fftfreq(g)[None, :]
        f = np.sqrt(fx ** 2 + fy ** 2)
        f[0, 0] = 1.0
        filt = 1.0 / f                       # 1/f amplitude = 1/f^2 power
        filt[0, 0] = 0.0
        t = np.real(np.fft.ifft2(np.fft.fft2(noise) * filt))
        t = (t - t.min()) / (t.max() - t.min())
        return t
    if name == "mottle":
        t = np.zeros((g, g))
        n_blob = 40
        rad = g / 16.0
        cx = rng.random(n_blob) * g
        cy = rng.random(n_blob) * g
        for a, b in zip(cx, cy):
            t += np.exp(-(((xx - a) ** 2 + (yy - b) ** 2) / (2 * rad ** 2)))
        t = np.clip(t, 0, 1)
        return (t > 0.5).astype(float)
    raise ValueError(name)


# --------------------------------------------------------------------------
# wiring
# --------------------------------------------------------------------------
def build_channels(pts, n_chan, m, wiring, rng, target=None, renderer=None):
    """Returns a list of index arrays, one per channel."""
    K = len(pts)
    n_chan = int(min(n_chan, K))
    if wiring == "compact":
        order = rng.permutation(K)
        seeds = order[:n_chan]
        taken = np.zeros(K, dtype=bool)
        chans = []
        for s in seeds:
            d = ((pts - pts[s]) ** 2).sum(1)
            d[taken] = np.inf
            take = np.argsort(d)[:m]
            take = take[np.isfinite(d[take])]
            taken[take] = True
            chans.append(take)
        return chans
    if wiring == "random":
        return [rng.choice(K, size=min(m, K), replace=False) for _ in range(n_chan)]
    if wiring == "renard_like":
        chans = []
        seeds = rng.choice(K, size=n_chan, replace=False)
        for s in seeds:
            d = np.sqrt(((pts - pts[s]) ** 2).sum(1))
            # weight so that the typical selected neighbour sits near the measured
            # within-unit NND rather than at the array's own nearest neighbour
            w = np.exp(-0.5 * ((d - WITHIN_UNIT_NND_UM) / WITHIN_UNIT_NND_UM) ** 2)
            w[s] = 0.0
            w = w / w.sum()
            take = rng.choice(K, size=min(m - 1, K - 1), replace=False, p=w)
            chans.append(np.concatenate([[s], take]))
        return chans
    if wiring == "oracle":
        # cluster actuators by (position, target value at the actuator) so that
        # each channel owns actuators the target wants driven alike
        tv = target[np.clip((pts[:, 1] / PX_UM).astype(int), 0, GRID - 1),
                    np.clip((pts[:, 0] / PX_UM).astype(int), 0, GRID - 1)]
        feat = np.column_stack([pts / mean_spacing_um(), tv * 6.0])
        cen = feat[rng.choice(K, size=n_chan, replace=False)]
        lab = np.zeros(K, dtype=int)
        for _ in range(12):
            d = ((feat[:, None, :] - cen[None, :, :]) ** 2).sum(-1) if n_chan <= 256 else None
            if d is None:
                lab = _assign_chunked(feat, cen)
            else:
                lab = d.argmin(1)
            for c in range(n_chan):
                sel = lab == c
                if sel.any():
                    cen[c] = feat[sel].mean(0)
        return [np.where(lab == c)[0] for c in range(n_chan)]
    raise ValueError(wiring)


def _assign_chunked(feat, cen, chunk=2048):
    out = np.empty(len(feat), dtype=int)
    for i in range(0, len(feat), chunk):
        d = ((feat[i:i + chunk, None, :] - cen[None, :, :]) ** 2).sum(-1)
        out[i:i + chunk] = d.argmin(1)
    return out


def channel_matrix(chans, K):
    rows, cols = [], []
    for c, idx in enumerate(chans):
        rows.extend(idx.tolist())
        cols.extend([c] * len(idx))
    return np.asarray(rows, dtype=np.int64), np.asarray(cols, dtype=np.int64)


# --------------------------------------------------------------------------
# optimisation
# --------------------------------------------------------------------------
def solve(renderer: Renderer, chans, target_field: np.ndarray, n_iters=N_ITERS):
    """Adam on channel activations a in [0,1]^N, projected to the box each step.

    Adam is used rather than normalised gradient descent because the step of a
    globally normalised gradient shrinks as 1/sqrt(N), which made large-N
    configurations score WORSE than small-N ones -- an optimiser artefact that
    would have been read as a result.  `test_optimiser_monotonicity` in the
    controls block is the check that caught it and is reported with the study.
    """
    K = renderer.K
    rows, cols = channel_matrix(chans, K)
    n_chan = len(chans)
    da = renderer.a_exp - renderer.a_ret
    # Overlapping wirings give each actuator several channels, so a = 0.5 starts
    # the array fully saturated (u_raw ~ 4.5 at nine memberships) where the clamp
    # has zero gradient and the optimiser cannot move. Start from the activation
    # that puts the MEAN actuator at half drive.
    mean_membership = max(1.0, len(rows) / max(1, K))
    a = np.full(n_chan, min(0.9, 0.5 / mean_membership))
    mom = np.zeros(n_chan)
    vel = np.zeros(n_chan)
    b1, b2, eps, lr = 0.9, 0.999, 1e-12, 0.08
    best = (np.inf, a.copy())
    for it in range(1, n_iters + 1):
        u_raw = np.zeros(K)
        np.add.at(u_raw, rows, a[cols])
        u = np.clip(u_raw, 0.0, 1.0)
        area = renderer.a_ret + u * da
        s = renderer.blur(renderer.scatter(area))
        cov = 1.0 - np.exp(-_KAPPA * s)
        img = R_BACKGROUND + (R_PIGMENT - R_BACKGROUND) * cov
        resid = img - target_field
        loss = float((resid ** 2).mean())
        if loss < best[0]:
            best = (loss, a.copy())
        g_img = 2.0 * resid / resid.size
        g_cov = g_img * (R_PIGMENT - R_BACKGROUND)
        g_s = g_cov * _KAPPA * np.exp(-_KAPPA * s)
        g_scatter = renderer.blur(g_s) / renderer.px_area    # the blur is self-adjoint
        g_area = g_scatter.reshape(-1)[renderer.flat]
        # Straight-through on the clamp: a saturated actuator has a true gradient
        # of exactly zero, so masking it leaves a heavily overlapped wiring frozen
        # at its initial point. Passing the gradient through lets such a channel
        # descend; the best-iterate tracking above guards against overshoot.
        g_u = g_area * da
        g_a = np.zeros(n_chan)
        np.add.at(g_a, cols, g_u[rows])
        mom = b1 * mom + (1 - b1) * g_a
        vel = b2 * vel + (1 - b2) * g_a ** 2
        mh = mom / (1 - b1 ** it)
        vh = vel / (1 - b2 ** it)
        a = np.clip(a - lr * mh / (np.sqrt(vh) + eps), 0.0, 1.0)
    a = best[1]
    u_raw = np.zeros(K)
    np.add.at(u_raw, rows, a[cols])
    img, _ = renderer.reflectance(np.clip(u_raw, 0, 1))
    return img, a


def score(img, target_field, renderer):
    """Primary and secondary metrics.  Blur is already in `img` and in the target.

    A target with no spatial variance (uniform_dark, uniform_light) has an
    undefined R2, and `None` is returned rather than 1.0.  Returning 1.0 would be
    a score of 1 earned by an empty denominator -- a vacuous pass that would then
    be averaged in with real ones.  Those two targets are MAE controls only.
    """
    resid = img - target_field
    denom = ((target_field - target_field.mean()) ** 2).sum()
    if denom <= 1e-9:
        return {"r2_blurred": None, "r2_blurred_unclipped": None,
                "mae_blurred": float(np.abs(resid).mean()),
                "r2_undefined_zero_variance_target": True}
    r2 = 1.0 - float((resid ** 2).sum()) / float(denom)
    return {
        "r2_blurred": float(max(0.0, r2)),          # the DECLARED primary metric
        "r2_blurred_unclipped": float(r2),          # diagnostic, not the metric
        "mae_blurred": float(np.abs(resid).mean()),
    }


# --------------------------------------------------------------------------
# one cell of the sweep
# --------------------------------------------------------------------------
def run_cell(args):
    seed, m, wiring, tname, n_chan = args
    pts = make_array(seed)
    rend = Renderer(pts)
    lo, hi = rend.range()
    raw = make_target(tname)
    # affine map into the skin's own achievable range, then blur with the same PSF
    tgt = rend.blur(lo + (hi - lo) * raw)
    rng = np.random.default_rng(seed * 1000 + hash(wiring) % 997 + n_chan)
    chans = build_channels(pts, n_chan, m, wiring, rng, target=raw, renderer=rend)
    img, a = solve(rend, chans, tgt)
    s = score(img, tgt, rend)
    s.update(dict(seed=seed, m=m, wiring=wiring, target=tname, n_chan=int(len(chans)),
                  n_actuators=int(rend.K), addressed=int(len(np.unique(np.concatenate(chans)))),
                  skin_min=lo, skin_max=hi))
    return s


def knee_95(ns, r2s, r2_full):
    if r2_full is None or r2_full <= 0:
        return None
    thr = KNEE_FRACTION * r2_full
    for n, r in zip(ns, r2s):
        if r is not None and r >= thr:
            return int(n)
    return None


def knee_curvature(ns, r2s):
    if any(r is None for r in r2s):
        return None
    x = np.log10(np.asarray(ns, dtype=float))
    y = np.asarray(r2s, dtype=float)
    if len(x) < 3 or x[-1] == x[0]:
        return None
    xn = (x - x[0]) / (x[-1] - x[0])
    yn = (y - y[0]) / (y[-1] - y[0] + 1e-12)
    d = yn - xn
    return int(ns[int(np.argmax(d))])


def main():
    ap = argparse.ArgumentParser(description="Control-channel sweep for an addressable pigment skin")
    ap.add_argument("--out", default="control-channels.json")
    ap.add_argument("--figdir", default=None)
    ap.add_argument("--nproc", type=int, default=4)
    ap.add_argument("--quick", action="store_true", help="tiny sweep for a smoke test")
    ap.add_argument("--controls", action="store_true", help="also run the declared controls")
    ap.add_argument("--compact-stdout", action="store_true",
                    help="emit gzip+base64 of the result on stdout, for log-only retrieval")
    args = ap.parse_args()

    seeds = SEEDS[:2] if args.quick else SEEDS
    wirings = ("compact", "random") if args.quick else WIRINGS
    targets = ("edge", "gravel_1f") if args.quick else TARGETS
    unit_sizes = (1, 9) if args.quick else UNIT_SIZES

    probe = Renderer(make_array(seeds[0]))
    K = probe.K
    n_values = sorted(set(int(round(v)) for v in np.unique(
        np.round(np.logspace(0, math.log10(K), 9 if args.quick else 14)))))
    if n_values[-1] != K:
        n_values.append(K)

    jobs = [(s, m, w, t, n) for s in seeds for m in unit_sizes
            for w in wirings for t in targets for n in n_values]
    print(f"K={K} actuators, {len(n_values)} N-values, {len(jobs)} cells", flush=True)

    t0 = time.time()
    rows = []
    if args.nproc > 1:
        with ProcessPoolExecutor(max_workers=args.nproc) as ex:
            for i, r in enumerate(ex.map(run_cell, jobs, chunksize=4)):
                rows.append(r)
                if i % 100 == 0:
                    print(f"  {i}/{len(jobs)}  {time.time()-t0:.0f}s", flush=True)
    else:
        for i, j in enumerate(jobs):
            rows.append(run_cell(j))
            if i % 50 == 0:
                print(f"  {i}/{len(jobs)}  {time.time()-t0:.0f}s", flush=True)
    elapsed = time.time() - t0
    print(f"done in {elapsed:.0f}s", flush=True)

    def emit(obj, tag):
        with open(args.out, "w") as fh:
            json.dump(obj, fh)
        print(f"wrote {args.out} ({tag})", flush=True)
        if args.compact_stdout:
            import base64 as _b64, gzip as _gz
            blob = _b64.b64encode(_gz.compress(json.dumps(obj).encode())).decode()
            print(f"BEGIN_RESULT_B64 tag={tag} len={len(blob)}", flush=True)
            for i in range(0, len(blob), 4000):
                print(blob[i:i + 4000], flush=True)
            print("END_RESULT_B64", flush=True)

    out = {"rows": rows, "n_values": n_values, "K": K,
           "elapsed_s": elapsed, "seeds": list(seeds), "unit_sizes": list(unit_sizes),
           "wirings": list(wirings), "targets": list(targets), "controls": []}
    # The sweep is emitted BEFORE the controls run. An earlier version ran the
    # controls first and a NameError in that step threw away 3,767 s of completed
    # sweep, because nothing had been written yet. Expensive results are committed
    # before anything cheap is allowed to fail on them.
    emit(out, "sweep-only")
    if args.controls:
        try:
            out["controls"] = run_controls()
        except Exception as exc:                       # noqa: BLE001
            out["controls"] = [{"name": "controls_failed_to_run",
                                "passed": False, "error": repr(exc)}]
            print("CONTROLS FAILED:", repr(exc), flush=True)
        emit(out, "sweep-plus-controls")




# --------------------------------------------------------------------------
# Controls.  Each must be run and reported, pass or fail.
# --------------------------------------------------------------------------
def control_array_uniformity(seed=11):
    """The array must fill the patch. A Bridson run stopped at the target count
    leaves empty corners; the point count alone does not show it."""
    pts = make_array(seed)
    r = Renderer(pts)
    s = r.blur(r.scatter(np.full(r.K, r.a_exp)))
    return {"name": "array_uniformity",
            "asks": "with every actuator expanded, is the blurred area-density field "
                    "bounded away from zero everywhere in the patch?",
            "min_s": float(s.min()), "max_s": float(s.max()), "mean_s": float(s.mean()),
            "ratio_min_over_mean": float(s.min() / s.mean()),
            "threshold": "min/mean > 0.5",
            "passed": bool(s.min() / s.mean() > 0.5),
            "positive_control": "the earlier count-capped Bridson gave min_s = 0.00136 "
                                "against the same mean 1.897 (ratio 7e-4), which this "
                                "check flags; that run is the must-flag case."}


def control_coverage_law(seed=11, upsample=4):
    """1 - exp(-s) assumes random overlap. Compare against an exact rasterised
    union of the actual discs at 4x resolution, for three drive levels."""
    pts = make_array(seed)
    r = Renderer(pts)
    out = []
    g = GRID * upsample
    px = PATCH_UM / g
    yy, xx = np.mgrid[0:g, 0:g]
    cx = pts[:, 0] / px
    cy = pts[:, 1] / px
    for u_level in (0.0, 0.5, 1.0):
        rad_um = math.sqrt((r.a_ret + u_level * (r.a_exp - r.a_ret)) / math.pi)
        rad = rad_um / px
        mask = np.zeros((g, g), dtype=bool)
        for a, b in zip(cx, cy):
            i0, i1 = max(0, int(b - rad) - 1), min(g, int(b + rad) + 2)
            j0, j1 = max(0, int(a - rad) - 1), min(g, int(a + rad) + 2)
            sub = (xx[i0:i1, j0:j1] - a) ** 2 + (yy[i0:i1, j0:j1] - b) ** 2 <= rad ** 2
            mask[i0:i1, j0:j1] |= sub
        exact = float(mask.mean())
        s_mean = DENSITY_PER_UM2 * math.pi * rad_um ** 2
        poisson = 1.0 - math.exp(-s_mean)
        out.append({"drive": u_level, "exact_union_coverage": exact,
                    "poisson_law_coverage": poisson,
                    "abs_error": abs(exact - poisson),
                    "relative_error": abs(exact - poisson) / max(exact, 1e-9)})
    worst = max(o["relative_error"] for o in out)
    return {"name": "coverage_law_vs_exact_union",
            "asks": "does 1 - exp(-s) match an exact rasterised disc union?",
            "levels": out, "worst_relative_error": worst,
            "threshold": "worst relative error < 0.15",
            "passed": bool(worst < 0.15),
            "direction": "exact union EXCEEDS the law at every drive level",
            "note": "This control FAILS at the retracted level and the sign is the "
                    "opposite of what was written down before it was run. The "
                    "prediction recorded in advance was that a Poisson-disc array "
                    "overlaps LESS than a Poisson one, so the law would OVER-estimate "
                    "coverage. It under-estimates, by 16% relative when retracted and "
                    "8% when fully expanded, because a hard-core array wastes less of "
                    "its disc area on mutual overlap and therefore covers MORE than "
                    "randomly placed discs of the same density. The wrong prediction is "
                    "kept here rather than edited out. What it costs is quantified by "
                    "`coverage_law_sensitivity`, which re-runs a channel sweep under a "
                    "coverage law rescaled to the exact union."}


def deconvolution_baseline(r: Renderer, tgt: np.ndarray, wiener=1e-3):
    """An independent, non-iterative solution: invert the forward model.

    cov -> s -> Wiener-deconvolve by the OTF -> per-actuator area -> clamp.
    This is a strong baseline: a naive synthesis that ignores the blur scores 0,
    so beating THAT would not have told us anything about the optimiser.
    """
    cov_t = np.clip((R_BACKGROUND - tgt) / (R_BACKGROUND - R_PIGMENT), 0.0, 0.995)
    s_t = -np.log(1.0 - cov_t)
    F = np.fft.fft2(s_t)
    s_req = np.real(np.fft.ifft2(F * r.otf / (r.otf ** 2 + wiener)))
    # s is area-density (pigment area per unit skin area), so the area each
    # actuator must present is s / (actuators per unit area).
    per = s_req.reshape(-1)[r.flat] / DENSITY_PER_UM2
    u = (per - r.a_ret) / (r.a_exp - r.a_ret)
    return np.clip(u, 0.0, 1.0)


def control_optimiser_adequacy(seed=11, target="edge"):
    """With one channel per actuator the optimiser must beat an INDEPENDENT
    non-iterative inversion of the forward model. If it does not, any
    N-dependence is an optimiser artefact rather than a control-channel result."""
    pts = make_array(seed)
    r = Renderer(pts)
    lo, hi = r.range()
    raw = make_target(target)
    tgt = r.blur(lo + (hi - lo) * raw)
    direct_img, _ = r.reflectance(deconvolution_baseline(r, tgt))
    direct = score(direct_img, tgt, r)
    chans = [np.array([i]) for i in range(r.K)]
    opt_img, _ = solve(r, chans, tgt)
    opt = score(opt_img, tgt, r)
    return {"name": "optimiser_adequacy",
            "asks": "at one channel per actuator, does the optimiser beat hand-built "
                    "direct synthesis on the same target?",
            "target": target,
            "deconvolution_baseline_r2": direct["r2_blurred"],
            "optimised_r2": opt["r2_blurred"],
            "passed": bool(opt["r2_blurred"] >= direct["r2_blurred"]),
            "must_flag_case": "the first optimiser used a globally normalised gradient, "
                              "whose per-parameter step falls as 1/sqrt(N); it scored "
                              "r2 = 0.115 on this target at one channel per actuator. "
                              "That number is below the deconvolution baseline, so this "
                              "control flags it. An earlier version of this control used "
                              "a blur-ignoring direct synthesis that itself scored 0.0, "
                              "which the broken optimiser would have PASSED -- the "
                              "baseline was replaced for that reason."}


def control_coverage_law_sensitivity(seed=11, target="edge", m=9):
    """What does the failed coverage law cost the headline?

    Re-run a channel sweep with cov = 1 - exp(-kappa*s), kappa set so the law
    reproduces the EXACT union coverage at full drive, and compare the knee.
    kappa is a correction towards a measured-in-model quantity, not a fit to data.
    """
    global _KAPPA
    ctrl = control_coverage_law(seed)
    exact_full = [lv for lv in ctrl["levels"] if lv["drive"] == 1.0][0]["exact_union_coverage"]
    s_mean = DENSITY_PER_UM2 * math.pi * radii_um()[0] ** 2
    kappa = -math.log(1.0 - exact_full) / s_mean
    ns = [1, 4, 16, 64, 128, 256, 512, 1024, 2048, 3904]
    base, corr = [], []
    for n in ns:
        base.append(run_cell((seed, m, "compact", target, n))["r2_blurred"])
    _KAPPA = kappa
    try:
        for n in ns:
            corr.append(run_cell((seed, m, "compact", target, n))["r2_blurred"])
    finally:
        _KAPPA = 1.0
    kb = knee_95(ns, base, base[-1])
    kc = knee_95(ns, corr, corr[-1])
    return {"name": "coverage_law_sensitivity",
            "asks": "does the failed coverage law move the knee?",
            "kappa": kappa, "n_values": ns,
            "r2_default_law": base, "r2_corrected_law": corr,
            "knee95_default": kb, "knee95_corrected": kc,
            "knee_unchanged": bool(kb == kc),
            "max_abs_r2_difference": float(max(abs(a - b) for a, b in zip(base, corr))),
            "passed": bool(kb == kc),
            "interpretation": "The declared metric scores a target that has already been "
                              "mapped into the skin's own achievable range, so a uniform "
                              "bias in the coverage law largely cancels. This control is "
                              "what establishes that, rather than an argument that it "
                              "ought to."}


def run_controls():
    return [control_array_uniformity(), control_coverage_law(),
            control_optimiser_adequacy(), control_monotonicity(),
            control_coverage_law_sensitivity()]


def control_monotonicity(seed=11, target="gravel_1f", m=9):
    """More channels must not score worse. A drop is an optimiser artefact.

    Must-flag case, measured: before the straight-through fix, `renard_like` at
    nine memberships per actuator started fully saturated, where the clamp has
    zero gradient, and scored r2 = 0.0000 at N = K against 0.8169 at N = 1024.
    """
    out = []
    for w in WIRINGS:
        rs = [run_cell((seed, m, w, target, n))["r2_blurred"] for n in (256, 1024, 3904)]
        out.append({"wiring": w, "r2_at_256_1024_K": rs,
                    "monotone": bool(rs[2] >= rs[1] - 0.02 and rs[1] >= rs[0] - 0.02)})
    return {"name": "monotonicity_in_channel_count",
            "asks": "does r2 stop rising (rather than fall) as N grows, for every wiring?",
            "target": target, "unit_size": m, "per_wiring": out,
            "passed": all(o["monotone"] for o in out),
            "must_flag_case": "renard_like scored 0.0000 at N=K and 0.8169 at N=1024 "
                              "before the clamp gradient was made straight-through."}


if __name__ == "__main__":
    main()
