#!/usr/bin/env python3
"""
colony_morphology.py — accretive colony growth driven by a diffusive resource,
a flow field and a light field.

WHAT THIS IS: a simulation. No coral was measured. Every figure caption says so.

THE MODEL CLASS IS PUBLISHED; THIS IMPLEMENTATION IS NOT
--------------------------------------------------------
Accretive coral growth driven by a resource field computed from an
advection-diffusion equation is a published, runnable model class:

  Kaandorp, Lowe, Frenkel & Sloot 1996, Phys Rev Lett 77:2328 (PMID 10061916)
  Kaandorp & Sloot 2001, J Theor Biol 209:257               (PMID 11312588)
  Merks, Hoekstra, Kaandorp & Sloot 2003, J Theor Biol 224:153 (PMID 12927523)
  Merks et al. 2004, J Theor Biol 228:559                   (PMID 15178203)
  Chindapol, Kaandorp, Cronemberger, Mass & Genin 2013, PLoS Comput Biol 9:e1002849
                                                            (PMID 23326222)

This file is NOT a port of any of them. Chindapol et al. couple steady
Navier-Stokes to steady advection-diffusion on a deforming triangulated surface;
what follows is a voxel-lattice Laplacian-growth model with an advective bias. It is
in the same FAMILY and it is a different model, and no number it produces should be
compared with theirs as if it were a reimplementation. Their full text was read (first
100,000 of 100,162 characters) and their parameter table is reproduced in
CHINDAPOL_REFERENCE below for orientation, not because this model uses it.

THE CONTROL PARAMETER
---------------------
Merks et al. 2003 report that compactness "depends on the ratio of the rates of growth
and nutrient transport" and that an explicit curvature rule is NOT needed for branching.
That ratio is a Damkohler number, and it is this model's primary knob:

    Da = k * h / D        uptake rate x lattice spacing / diffusivity

  Da -> large   the surface is a near-perfect sink, the resource field is Laplacian,
                tips screen the interior, branching
  Da -> small   the surface barely perturbs the field, growth is nearly uniform,
                compact

Secondary knobs: Pe (advective bias, "flow") and w_light (how much of the growth
response is driven by a light field attenuating from above rather than by the diffusive
resource).

METRICS ARE DECLARED BEFORE ANY PICTURE IS LOOKED AT
----------------------------------------------------
See METRIC_DEFINITIONS. Four metrics, each with an exact rule, written and committed
before the first sweep was run. Every one is reported as a mean and a spread over
`n_seeds` independent random seeds, because the growth rule is stochastic.

EXTERNAL CHECK
--------------
Chandler et al. 2024 (PMID 39232103, read at full text) fitted three-dimensional total
surface area against maximum colony diameter for real colonies, TSA = a * D^b, and
measured b of about 2.4-2.5 for branching Pocillopora, Seriatopora and Stylophora
against about 1.8-2.0 for tabular Acropora and massive Porites. That exponent is
dimensionless, is measured on real colonies, and can be computed from this model's own
growth history. It is the one number here that can be checked against a measurement,
and it is computed whether or not it agrees.

Usage
  python3 colony_morphology.py --probe        one quick run, timing only
  python3 colony_morphology.py --run          the full sweep
  python3 colony_morphology.py --figures      redraw from the cache
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np
from concurrent.futures import ProcessPoolExecutor
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIGDIR = os.path.join(ROOT, "figures")
CACHE = os.path.join(ROOT, "morphology-cache.json")
RESULT = os.path.join(ROOT, "colony-morphology.json")
FRAMEDIR = os.path.join(ROOT, "frames")

# --------------------------------------------------------------------------------------
# Chindapol et al. 2013's own settings, for orientation. NOT used by this model.
# --------------------------------------------------------------------------------------
CHINDAPOL_REFERENCE = dict(
    note="Read from the full text of PMID 23326222. Reproduced so a reader can see what "
         "a calibrated implementation of this model class uses. THIS FILE DOES NOT USE "
         "THESE VALUES: it is a different model on a different discretisation.",
    domain="60 x 60 x 40 cm simulated channel",
    initial_object="sphere of diameter 6 cm",
    inlet_velocity="0.05 m/s",
    dynamic_viscosity="5.0e-2 Pa s (50x water, used to force Re_branch ~ 20)",
    diffusion_coefficient="1.0 down to 1e-5 m2/s in decade steps (eddy-scale, "
                          "physically unrealistic as a molecular diffusivity)",
    Pe_branch_simulated=[0, 0.00113, 0.0105, 0.097, 1.13, 11.3],
    Pe_branch_real_colonies=[0.136, 0.0163, 0.188, 0.227, 0.288],
    L_max="1.0e-3 m maximum layer added per growth step",
    K="1 mol/m3 half-saturation",
    hill_exponent=1.2,
    growth="about 0.5 mm per step; 150 steps is about 10 cm",
    surface_volume_benchmark="S/V 289 /m with no flow, 416 /m advection-dominated at "
                             "step 98. NOTE S/V ROSE with flow, i.e. the 'more compact' "
                             "form had MORE surface per volume in that pair, so do not "
                             "assume compactness lowers S/V.",
    flume_speeds="text says 1e-2 cm/s reduced and 15 cm/s enhanced; the figure caption "
                 "says about 1 cm/s and 15-20 cm/s. THE SOURCE DISAGREES WITH ITSELF.",
)

METRIC_DEFINITIONS = dict(
    declared_before_any_figure_was_viewed=True,
    surface_to_volume=dict(
        rule="Count exposed voxel faces (a face of an occupied voxel whose neighbour is "
             "empty or outside the lattice, excluding the substrate plane) and divide by "
             "the number of occupied voxels.",
        units="1 / voxel",
        why="The field's most-used shape metric. Reported knowing that Chindapol et al. "
            "measured S/V RISING with flow in the pair they report, so it does not "
            "simply track compactness."),
    branch_count=dict(
        rule="For each horizontal slice z in the UPPER HALF of the colony "
             "(z > z_max/2), label 4-connected components of occupied voxels in that "
             "slice and count only those with at least 8 voxels. The branch count is the "
             "MAXIMUM over those slices. Slices with fewer than 8 occupied voxels are "
             "skipped. THE MINIMUM COMPONENT SIZE WAS ADDED AFTER THE FIRST CONTROL RUN: "
             "without it, the ragged top of a rough mound counted as many branches, and "
             "the low-Da control failed for that reason rather than for a modelling one. "
             "The change was made to the RULE and the control was then re-run; it was not "
             "made after seeing a sweep result.",
        units="count",
        why="A branch is a thing that is separate from its neighbours somewhere above "
            "the base. The upper-half restriction is what stops a single hemispherical "
            "mound with a ragged rim counting as many branches, and it is the arbitrary "
            "part of the rule."),
    box_counting_dimension=dict(
        rule="Box-count the occupied voxel set at box sizes 1, 2, 4, 8 and 16 voxels; "
             "fit log N(eps) against log(1/eps) by least squares; report the slope.",
        units="dimensionless",
        why="Reichert et al. 2017 report that three-dimensional fractal dimension "
            "discriminated coral species at least as well as surface-volume ratio and "
            "rugosity, and considerably better within species. Five box sizes on a "
            "lattice of this size is a SHORT scaling range and the estimate is "
            "correspondingly crude; the spread across seeds is the honest error bar."),
    bounding_box_fill=dict(
        rule="Occupied voxels divided by the volume of the colony's axis-aligned "
             "bounding box.",
        units="fraction",
        why="A compactness measure that does not need a convex hull. A dense mound "
            "approaches a high value; an open branching colony is low."),
    area_diameter_exponent=dict(
        rule="During a run, record exposed surface area S and maximum horizontal "
             "diameter D at every growth generation after the colony exceeds 12 voxels "
             "across; fit log S = log a + b log D by least squares; report b.",
        units="dimensionless",
        why="THE EXTERNAL CHECK. Chandler et al. 2024 measured this exponent on real "
            "colonies by photogrammetry: about 2.4-2.5 for branching genera and about "
            "1.8-2.0 for tabular and massive ones. It is dimensionless, so a lattice "
            "model and a reef colony can be compared on it directly."),
)


# --------------------------------------------------------------------------------------
# The model
# --------------------------------------------------------------------------------------

# An ISOTROPIC 27-point neighbour kernel. Weights go as 1/distance, so face, edge and
# corner neighbours contribute in proportion to how close they are: 1, 1/sqrt(2), 1/sqrt(3).
#
# WHY THIS AND NOT THE SIX FACE NEIGHBOURS. The first version of this model used the
# 6-point stencil and 6-connected growth, and the result was dominated by the lattice
# rather than by the physics: plan views came out as four-pointed stars aligned with the
# x and y axes at every Damkohler number, and the low-Da control, which should be a
# hemispherical mound, was a square-based octahedron. That is the classic cubic-lattice
# artefact in Laplacian growth. It was found by LOOKING at the projections after the
# metrics had been declared, and it would not have been visible in any of the four
# metrics: surface-to-volume, box dimension and bounding-box fill all varied smoothly
# and plausibly with Da while the shapes were lattice artefacts.
_W = np.zeros((3, 3, 3), dtype=np.float32)
for _i in (-1, 0, 1):
    for _j in (-1, 0, 1):
        for _k in (-1, 0, 1):
            if (_i, _j, _k) != (0, 0, 0):
                _W[_i + 1, _j + 1, _k + 1] = 1.0 / np.sqrt(_i * _i + _j * _j + _k * _k)
_WSUM = float(_W.sum())
_WBIN = (_W > 0).astype(np.float32)        # for 26-connected candidate detection


def _conv(a, top_value):
    """Weighted neighbour sum with a benthic channel's boundary conditions.

    TOP face      far field, held at `top_value` (the resource source)
    SIDE faces    no flux (replicated)
    BOTTOM face   the substrate, no flux (replicated)

    An earlier version pinned ALL SIX faces at the far-field value. That had a defect
    that was easy to miss: the colony spread sideways until it touched a side wall, where
    the pinned source gave it unlimited supply, and the result was a wide flat mat at
    every Da. Nothing about that was a property of the growth law.
    """
    pad = np.pad(a, 1, mode="edge")
    pad[:, :, -1] = top_value
    return ndimage.convolve(pad, _W, mode="constant", cval=0.0)[1:-1, 1:-1, 1:-1]


def solve_field(occ, Da, Pe, c0=None, sweeps=120, tol=1e-4):
    """Steady resource field outside the colony.

    Solves, by damped Jacobi iteration on an isotropic 27-point stencil,

        0 = D laplacian(c) - u . grad(c)      outside the colony
        c = 1                                 at the top of the lattice (far field)
        -D dc/dn = k c                        at the colony surface (Robin uptake)

    in lattice units where D = 1 and h = 1, so Da = k and Pe = |u|. The Robin condition
    is imposed by having an occupied neighbour return c * 1/(1+Da) rather than acting as
    a hard c = 0 wall: Da -> infinity recovers the absorbing (pure Laplacian) limit and
    Da -> 0 recovers no uptake at all.

    Advection is a first-order upwind bias along +x, which is a crude discretisation and
    is the reason Pe here is a model knob and not a reef flow speed.
    """
    free = ~occ
    c = np.ones(occ.shape, dtype=np.float32) if c0 is None else c0.copy()
    c[occ] = 0.0
    refl = np.float32(1.0 / (1.0 + Da))
    occf = occ.astype(np.float32)
    occ_nb = _conv(occf, 0.0)
    for it in range(sweeps):
        cc = np.where(occ, 0.0, c).astype(np.float32)
        s = _conv(cc, np.float32(1.0)) + occ_nb * c * refl
        new = s / _WSUM
        if Pe > 0.0:
            up = np.empty_like(cc)
            up[1:] = cc[:-1]
            up[0] = cc[0]
            new = (new + Pe * up) / (1.0 + Pe)
        new = np.where(free, 0.65 * new + 0.35 * c, 0.0).astype(np.float32)
        delta = float(np.max(np.abs(new - c)))
        c = new
        if delta < tol and it > 10:
            break
    return c


def light_field(occ, attenuation):
    """Irradiance reaching each voxel: collimated from +z, attenuated by the colony above.

    I(x, y, z) = exp(-attenuation * (number of occupied voxels directly above)).
    Crude: no scattering, no off-vertical rays, no diffuse sky. It is here to ask whether
    a vertical light gradient alone produces plating, which is a question with a
    published answer (it does not, per Lesser et al.), not to model light properly.
    """
    above = np.cumsum(occ[:, :, ::-1], axis=2)[:, :, ::-1] - occ
    return np.exp(-attenuation * above).astype(np.float32)


def grow(Da=8.0, Pe=0.0, w_light=0.0, light_attenuation=0.35, n_gen=400,
         target_volume=7000, deposit_rate=0.45, noise=0.15, hill_n=3.0, hill_K=0.4,
         smooth_sigma=0.35, speed_sigma=0.6, nx=88, ny=88, nz=72, seed=0, seed_radius=3,
         record_every=0, frames=None):
    """Grow one colony as a PHASE FIELD whose interface is advanced by the local flux.

    phi is a continuous occupancy in [0, 1]; the colony is phi > 0.5. Each generation the
    interface advances along its own normal at a speed set by the local resource flux,
    phi += rate * f * |grad phi|, and phi is then smoothed with a small Gaussian. The
    smoothing is what makes the interface isotropic, and it also supplies a weak surface
    tension that keeps the front from fragmenting at the voxel scale.

    WHY NOT A VOXEL AUTOMATON. Two earlier versions filled voxels directly and both were
    dominated by the lattice rather than by the growth law, in ways that NONE of the four
    declared metrics revealed and that were found only by looking at the projections:

      * 6-connected growth with a 6-point Laplacian gave square-based OCTAHEDRA at low Da
        and four-pointed stars aligned with the x and y axes at high Da.
      * 26-connected growth with an isotropic 27-point Laplacian gave CUBES and hollow
        square boxes, because dilation by a 3x3x3 cube grows in the Chebyshev metric.

    The two lattice metrics (L1 and L-infinity) each imprinted their own unit ball on the
    colony. Surface-to-volume, box dimension and bounding-box fill all varied smoothly and
    plausibly with Da through both of them. That is the cautionary part: a metric sweep
    can look entirely reasonable while the shapes being measured are artefacts.
    """
    rng = np.random.default_rng(seed)
    gx, gy, gz = np.ogrid[:nx, :ny, :nz]
    cx, cy = nx // 2, ny // 2
    r = np.sqrt((gx - cx) ** 2 + (gy - cy) ** 2 + gz ** 2)
    phi = np.clip(seed_radius + 0.5 - r, 0.0, 1.0).astype(np.float32)

    c = None
    hist = []
    occ = phi > 0.5
    for gen in range(n_gen):
        c = solve_field(occ, Da, Pe, c0=c, sweeps=250 if gen == 0 else 70)
        flux = (Da * c).astype(np.float32)
        if w_light > 0.0:
            li = light_field(occ, light_attenuation)
            flux = ((1.0 - w_light) * flux / max(float(flux.max()), 1e-30)
                    + w_light * li).astype(np.float32)
        gxp, gyp, gzp = np.gradient(phi)
        gmag = np.sqrt(gxp * gxp + gyp * gyp + gzp * gzp).astype(np.float32)
        band = gmag > 1e-3
        if not band.any():
            break
        fmax = float(flux[band].max())
        if fmax <= 0:
            break
        f = np.where(band, flux / fmax, 0.0).astype(np.float32)
        f = f ** hill_n / (hill_K ** hill_n + f ** hill_n)
        # Smooth the SPEED, not the colony. This is what supplies isotropy: the interface
        # advances along a direction averaged over a small neighbourhood rather than
        # along a lattice axis. An earlier version instead smoothed phi itself by 0.75
        # voxels EVERY generation, which compounds to an effective sigma of about six
        # voxels over a run and erased the result completely: every Damkohler number from
        # 0.02 to 80 returned the same compact mound, to three significant figures in all
        # four metrics. Over-regularising looks exactly like "the control parameter does
        # nothing", which is why the low-Da / high-Da control arm is the thing that has
        # to pass first.
        if speed_sigma > 0:
            f = ndimage.gaussian_filter(f, speed_sigma).astype(np.float32)
        if noise > 0.0:
            f = f * np.exp(rng.normal(0.0, noise, size=f.shape)).astype(np.float32)
        phi = phi + deposit_rate * f * gmag
        phi = ndimage.gaussian_filter(phi, smooth_sigma).astype(np.float32)
        # ACCRETION IS MONOTONE: skeleton already laid down does not dissolve. Without
        # this the Gaussian regularisation erodes the colony faster than the flux builds
        # it, and a small seed disappears entirely within a few generations -- which is
        # how this line came to be here.
        phi = np.maximum(np.clip(phi, 0.0, 1.0), occ.astype(np.float32))
        occ = phi > 0.5
        if not occ.any():
            break
        hist.append(_history_row(occ, gen))
        if occ[0].any() or occ[-1].any() or occ[:, 0].any() or occ[:, -1].any() \
                or occ[:, :, -1].any():
            hist[-1]["stopped"] = "lattice wall"
            break
        if target_volume and occ.sum() >= target_volume:
            hist[-1]["stopped"] = "target volume"
            break
        if record_every and frames is not None and gen % record_every == 0:
            frames.append(occ.copy())
    return occ, hist


def _exposed_faces(occ):
    """Exposed voxel faces, excluding the substrate plane at z = 0."""
    n = 0
    n += int((occ[:-1] & ~occ[1:]).sum()) + int((occ[1:] & ~occ[:-1]).sum())
    n += int(occ[-1].sum()) + int(occ[0].sum())
    n += int((occ[:, :-1] & ~occ[:, 1:]).sum()) + int((occ[:, 1:] & ~occ[:, :-1]).sum())
    n += int(occ[:, -1].sum()) + int(occ[:, 0].sum())
    n += int((occ[:, :, :-1] & ~occ[:, :, 1:]).sum())
    n += int((occ[:, :, 1:] & ~occ[:, :, :-1]).sum())
    n += int(occ[:, :, -1].sum())
    return n


def _max_diameter(occ):
    xs, ys, _ = np.nonzero(occ)
    if len(xs) == 0:
        return 0.0
    return float(max(xs.max() - xs.min(), ys.max() - ys.min()) + 1)


def _history_row(occ, gen):
    return dict(gen=int(gen), volume=int(occ.sum()), area=_exposed_faces(occ),
                diameter=_max_diameter(occ), height=int(np.nonzero(occ)[2].max() + 1))


# --------------------------------------------------------------------------------------
# Metrics -- exactly as declared in METRIC_DEFINITIONS
# --------------------------------------------------------------------------------------

def _label_2d(mask, min_size=8):
    """4-connected components of a 2-D boolean mask, counting only those with at least
    `min_size` voxels. Without scipy."""
    h, w = mask.shape
    seen = np.zeros((h, w), dtype=bool)
    n_big = 0
    for i in range(h):
        for j in range(w):
            if mask[i, j] and not seen[i, j]:
                stack = [(i, j)]
                seen[i, j] = True
                size = 0
                while stack:
                    a, b = stack.pop()
                    size += 1
                    for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        p, q = a + da, b + db
                        if 0 <= p < h and 0 <= q < w and mask[p, q] and not seen[p, q]:
                            seen[p, q] = True
                            stack.append((p, q))
                if size >= min_size:
                    n_big += 1
    return n_big


def metrics(occ):
    vol = int(occ.sum())
    area = _exposed_faces(occ)
    zs = np.nonzero(occ)[2]
    zmax = int(zs.max())
    # branch count, per the declared rule
    counts = []
    for z in range(zmax // 2 + 1, zmax + 1):
        sl = occ[:, :, z]
        if sl.sum() >= 8:
            counts.append(_label_2d(sl))
    branch = int(max(counts)) if counts else 1
    # box-counting dimension
    eps, ns = [], []
    for e in (1, 2, 4, 8, 16):
        if e == 1:
            n = vol
        else:
            nx, ny, nz = occ.shape
            pad = occ[:nx // e * e, :ny // e * e, :nz // e * e]
            blocks = pad.reshape(nx // e, e, ny // e, e, nz // e, e)
            n = int(blocks.any(axis=(1, 3, 5)).sum())
        if n > 0:
            eps.append(e); ns.append(n)
    D = float(np.polyfit(np.log(1.0 / np.array(eps, float)),
                         np.log(np.array(ns, float)), 1)[0]) if len(eps) > 2 else None
    xs, ys, zz = np.nonzero(occ)
    bbox = ((xs.max() - xs.min() + 1) * (ys.max() - ys.min() + 1) *
            (zz.max() - zz.min() + 1))
    return dict(volume=vol, area=area, surface_to_volume=area / max(vol, 1),
                branch_count=branch, box_counting_dimension=D,
                bounding_box_fill=vol / max(bbox, 1),
                height=int(zmax + 1), diameter=_max_diameter(occ))


def area_diameter_exponent(hist, min_diameter=12.0):
    rows = [h for h in hist if h["diameter"] >= min_diameter and h["area"] > 0]
    if len(rows) < 4:
        return None
    d = np.log([r["diameter"] for r in rows])
    a = np.log([r["area"] for r in rows])
    b, _ = np.polyfit(d, a, 1)
    return float(b)


# --------------------------------------------------------------------------------------
# Control arm
# --------------------------------------------------------------------------------------

def _one(job):
    """Worker: one colony, returned as metrics. Top-level so it is picklable."""
    params, seed = job
    occ, hist = grow(seed=seed, **params)
    m = metrics(occ)
    m["area_diameter_exponent"] = area_diameter_exponent(hist)
    m["aspect_ratio"] = m["height"] / max(m["diameter"], 1.0)
    m["stopped"] = hist[-1].get("stopped") if hist else None
    return m


def _run_many(jobs, workers=4):
    import os as _os
    _os.environ.setdefault("OMP_NUM_THREADS", "1")
    _os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    _os.environ.setdefault("MKL_NUM_THREADS", "1")
    with ProcessPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(_one, jobs))


def control_arm(n_seeds=5, workers=4, **kw):
    """Two pre-declared controls that must pass before any sweep is read.

    CONTROL 1 -- the no-uptake limit. With Da very small the colony barely perturbs the
    resource field, so growth should be close to isotropic: a compact mound, branch
    count 1, box-counting dimension near 3.

    CONTROL 2 -- the absorbing limit. With Da very large the surface is a near-perfect
    sink, tips screen the interior, and the colony must branch: branch count above 1 and
    a box-counting dimension clearly below 3.

    If the two limits are not distinguishable, the control parameter does nothing and
    nothing else in this file means anything.
    """
    out = {}
    for name, Da in (("low_Da_isotropic", 0.02), ("high_Da_absorbing", 50.0)):
        runs = _run_many([(dict(Da=Da, **kw), s) for s in range(n_seeds)], workers)
        out[name] = _summarise(runs)
    lo, hi = out["low_Da_isotropic"], out["high_Da_absorbing"]
    est = estimator_control(kw.get("shape_for_control", (kw.get("nx", 88),
                                                          kw.get("ny", 88),
                                                          kw.get("nz", 72))),
                            lo["volume"]["mean"])
    hemi = est["solid_hemisphere"]["measured_box_dimension"]
    checks = {
        "low_Da_is_compact": bool(lo["branch_count"]["mean"] < 1.5),
        "low_Da_fills_space": bool(lo["box_counting_dimension"]["mean"] > 2.6),
        "low_Da_fills_space_vs_estimator_control": bool(
            lo["box_counting_dimension"]["mean"] > hemi - 0.05),
        "high_Da_branches": bool(hi["branch_count"]["mean"] > 1.5),
        "high_Da_is_not_space_filling": bool(
            hi["box_counting_dimension"]["mean"] < lo["box_counting_dimension"]["mean"]),
        "limits_are_distinguishable": bool(
            hi["surface_to_volume"]["mean"] > lo["surface_to_volume"]["mean"]),
    }
    declared = ["low_Da_is_compact", "low_Da_fills_space", "high_Da_branches",
                "high_Da_is_not_space_filling", "limits_are_distinguishable"]
    return dict(
        arms=out, checks=checks,
        n_checks=len(checks), n_failed=sum(1 for v in checks.values() if not v),
        failed_checks=[k for k, v in checks.items() if not v],
        declared_before_the_run=declared,
        # `passed` is the STRICT reading: every check declared before the run. An earlier
        # version of this file defined `passed` to exclude low_Da_fills_space once that
        # check had failed and been diagnosed, which made `passed` True while a declared
        # check was False in the same object. That is relaxing an aggregate to make it
        # pass, and it is not what `passed` may mean. Both readings are now reported and
        # the strict one keeps the plain name.
        passed=bool(all(checks[k] for k in declared)),
        # The exclusion travels WITH the boolean, not two fields away, so a reader or a
        # renderer that reads only `passed` cannot get "all clear" from a study with a
        # failed check in it.
        passed_meaning="STRICT: every check declared before the run, including the one "
                       "that failed and was later superseded. False here.",
        passed_excludes_superseded_check=None,
        passed_after_diagnosis_excludes_superseded_check="low_Da_fills_space",
        passed_after_diagnosis_meaning=(
            "Excludes `low_Da_fills_space`, which failed and was then shown to be a "
            "mis-specified criterion rather than a model failure: a solid hemisphere of "
            "the same voxel count measures 2.46 and a solid cube 2.47, both with true "
            "dimension 3, so NO object of any shape reaches the declared >2.6 at this "
            "size. The original failure stays visible in `checks` and `failed_checks`."),
        passed_as_declared=bool(all(checks[k] for k in declared)),
        passed_after_diagnosis=bool(all(
            v for k, v in checks.items() if k != "low_Da_fills_space")),
        estimator_control=est,
        n_seeds=n_seeds,
        note_on_the_failed_check=(
            "`low_Da_fills_space` required a box-counting dimension above 2.6 for the "
            "compact low-Da mound and was DECLARED BEFORE THE RUN. It fails. The "
            "criterion was wrong, not the model, and the estimator control is how that "
            "was established rather than assumed: a SOLID HEMISPHERE of the same voxel "
            f"count, whose true dimension is 3, measures {hemi:.3f} with the same code "
            "over the same five box sizes. The threshold of 2.6 was set without knowing "
            "the estimator's bias at this size. The check is reported as failed and is "
            "NOT counted toward `passed`; the replacement check compares the colony "
            "against the solid control instead of against an invented number, and that "
            "replacement was written only after the failure was diagnosed, which is why "
            "both are shown."))


def estimator_control(shape, n_voxels):
    """POSITIVE CONTROL FOR THE BOX-COUNTING ESTIMATOR ITSELF.

    Build a solid hemisphere with the same voxel count as a simulated colony and measure
    its box-counting dimension with exactly the same code. A solid object has a true
    dimension of 3, so whatever this returns is the estimator's bias at this size and
    over this range of box sizes -- and it is the number against which the colonies'
    dimensions should be read.

    This exists because the control arm's `low_Da_fills_space` check FAILED: it required
    a box dimension above 2.6 for the compact low-Da mound and measured about 2.44. The
    question that then matters is whether the mound is not space-filling or whether the
    estimator cannot say. Asking it needs a case whose answer is known.
    """
    nx, ny, nz = shape
    cx, cy = nx // 2, ny // 2
    gx, gy, gz = np.ogrid[:nx, :ny, :nz]
    r2 = (gx - cx) ** 2 + (gy - cy) ** 2 + gz ** 2
    order = np.argsort(r2.ravel())[:int(n_voxels)]
    occ = np.zeros(nx * ny * nz, dtype=bool)
    occ[order] = True
    occ = occ.reshape(shape)
    m = metrics(occ)
    # and a solid cube of the same count, as a second known case
    side = int(round(n_voxels ** (1 / 3)))
    cube = np.zeros(shape, dtype=bool)
    cube[cx - side // 2:cx - side // 2 + side,
         cy - side // 2:cy - side // 2 + side, 0:side] = True
    mc = metrics(cube)
    return dict(
        n_voxels=int(n_voxels), box_sizes=[1, 2, 4, 8, 16],
        solid_hemisphere=dict(true_dimension=3.0,
                              measured_box_dimension=m["box_counting_dimension"],
                              surface_to_volume=m["surface_to_volume"],
                              bounding_box_fill=m["bounding_box_fill"]),
        solid_cube=dict(true_dimension=3.0, n_voxels=int(cube.sum()),
                        measured_box_dimension=mc["box_counting_dimension"]),
        interpretation=(
            "Both objects are solid and have a true dimension of 3. Whatever the "
            "estimator returns for them is its bias at this size over this range of box "
            "sizes: the largest boxes span most of the object, so the log-log fit is "
            "pulled down. Colony dimensions in this study should be read against these "
            "numbers and not against 3."),
        is_observation=False)


def _summarise(runs):
    keys = [k for k in runs[0] if runs[0][k] is not None and
            isinstance(runs[0][k], (int, float))]
    out = {}
    for k in keys:
        v = np.array([r[k] for r in runs if r.get(k) is not None], dtype=float)
        out[k] = dict(mean=float(v.mean()), sd=float(v.std(ddof=1)) if len(v) > 1 else 0.0,
                      min=float(v.min()), max=float(v.max()), n=int(len(v)))
    return out


# --------------------------------------------------------------------------------------
# Sweeps
# --------------------------------------------------------------------------------------

DA_VALUES = [0.02, 0.05, 0.12, 0.3, 0.8, 2.0, 5.0, 12.0, 30.0, 80.0]
PE_VALUES = [0.0, 0.05, 0.2]
LIGHT_VALUES = [0.0, 0.5, 0.9]


def sweep_da(n_seeds=5, workers=4, **kw):
    rows = []
    for Da in DA_VALUES:
        runs = _run_many([(dict(Da=Da, **kw), s) for s in range(n_seeds)], workers)
        rows.append(dict(Da=Da, **_summarise(runs)))
        print(f"    Da={Da:<6g} branches={rows[-1]['branch_count']['mean']:.2f}"
              f" +/-{rows[-1]['branch_count']['sd']:.2f}"
              f"  S/V={rows[-1]['surface_to_volume']['mean']:.3f}"
              f"  D={rows[-1]['box_counting_dimension']['mean']:.3f}", flush=True)
    return rows


def sweep_pe_light(n_seeds=3, Da=12.0, workers=4, **kw):
    rows = []
    for Pe in PE_VALUES:
        for wl in LIGHT_VALUES:
            runs = _run_many([(dict(Da=Da, Pe=Pe, w_light=wl, **kw), s)
                              for s in range(n_seeds)], workers)
            rows.append(dict(Pe=Pe, w_light=wl, **_summarise(runs)))
            print(f"    Pe={Pe:<5g} w_light={wl:<4g} "
                  f"branches={rows[-1]['branch_count']['mean']:.2f}"
                  f"  aspect={rows[-1]['aspect_ratio']['mean']:.3f}", flush=True)
    return rows


def transition_sharpness(rows):
    """Is the branching transition sharp or graded? DECLARED TEST, written before the run.

    Fit a logistic in log10(Da) to the mean branch count, normalised to its own range,
    and report the width over which it goes from 10% to 90% of that range, in DECADES of
    Da. Declared cut: SHARP if that width is under half a decade, GRADED otherwise.

    The cut is arbitrary. It is written down first so that the answer is not chosen after
    looking at the curve, which is the only protection available when the quantity being
    judged is the shape of a curve.
    """
    x = np.log10(np.array([r["Da"] for r in rows], float))
    y = np.array([r["branch_count"]["mean"] for r in rows], float)
    lo, hi = y.min(), y.max()
    if hi - lo < 1e-9:
        return dict(verdict="no transition", width_decades=None, span=float(hi - lo))
    yn = (y - lo) / (hi - lo)

    def logistic(p):
        x0, k = p
        return 1.0 / (1.0 + np.exp(-k * (x - x0)))

    best, bestp = None, None
    for x0 in np.linspace(x.min(), x.max(), 60):
        for k in np.logspace(-1, 1.6, 60):
            r = float(((logistic((x0, k)) - yn) ** 2).sum())
            if best is None or r < best:
                best, bestp = r, (x0, k)
    x0, k = bestp
    width = float(2.0 * np.log(9.0) / k)          # 10% to 90%, in decades of Da
    return dict(verdict="sharp" if width < 0.5 else "graded",
                width_decades=width, midpoint_log10_Da=float(x0), logistic_k=float(k),
                residual=best, span=float(hi - lo),
                declared_cut="sharp if the 10-90% width is under 0.5 decades of Da",
                spread_note="The fit is to the MEAN over seeds; the per-Da spread is in "
                            "the sweep rows and is what says whether the mean is worth "
                            "fitting.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--gen", type=int, default=400)
    ap.add_argument("--nx", type=int, default=88)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--volume", type=int, default=7000)
    args = ap.parse_args()
    os.makedirs(FIGDIR, exist_ok=True)
    kw = dict(n_gen=args.gen, nx=args.nx, ny=args.nx, nz=int(args.nx * 0.82),
              target_volume=args.volume)

    if args.probe:
        for Da in (0.02, 12.0):
            t0 = time.time()
            occ, hist = grow(Da=Da, seed=0, **kw)
            m = metrics(occ)
            print(f"Da={Da}: {time.time()-t0:.1f}s vol={m['volume']} "
                  f"branches={m['branch_count']} S/V={m['surface_to_volume']:.3f} "
                  f"D={m['box_counting_dimension']:.3f} "
                  f"fill={m['bounding_box_fill']:.3f} h={m['height']} "
                  f"d={m['diameter']:.0f} b={area_diameter_exponent(hist)}")
        return

    if args.figures:
        with open(CACHE) as fh:
            cache = json.load(fh)
        make_figures(cache)
        return

    print("control arm ...", flush=True)
    ctrl = control_arm(n_seeds=args.seeds, workers=args.workers, **kw)
    for k, v in ctrl["checks"].items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    print(f"Da sweep, {args.seeds} seeds x {len(DA_VALUES)} values ...", flush=True)
    da = sweep_da(n_seeds=args.seeds, workers=args.workers, **kw)
    tr = transition_sharpness(da)
    print(f"  transition: {tr['verdict']} "
          f"(10-90% width {tr['width_decades']:.2f} decades of Da)", flush=True)
    print("flow x light sweep ...", flush=True)
    pl = sweep_pe_light(n_seeds=max(3, args.seeds - 2), workers=args.workers, **kw)

    print("forms for the figure ...", flush=True)
    forms = {}
    for label, p in (("Da 0.02 (no uptake limit)", dict(Da=0.02)),
                     ("Da 0.8", dict(Da=0.8)),
                     ("Da 12", dict(Da=12.0)),
                     ("Da 80 (absorbing)", dict(Da=80.0)),
                     ("Da 12, flow Pe 0.2", dict(Da=12.0, Pe=0.2)),
                     ("Da 12, light-weighted 0.9", dict(Da=12.0, w_light=0.9))):
        occ, hist = grow(seed=0, **p, **kw)
        forms[label] = dict(occ=occ.astype(np.uint8).tolist() if False else None,
                            shape=list(occ.shape),
                            projection_xz=occ.any(axis=1).astype(np.uint8).tolist(),
                            projection_xy=occ.any(axis=2).astype(np.uint8).tolist(),
                            heightmap=(occ * np.arange(occ.shape[2])).max(
                                axis=2).astype(np.int16).tolist(),
                            metrics=metrics(occ),
                            area_diameter_exponent=area_diameter_exponent(hist),
                            params=p)

    cache = dict(control_arm=ctrl, da_sweep=da, transition=tr, pe_light_sweep=pl,
                 forms=forms, settings=dict(n_seeds=args.seeds, **kw))
    with open(CACHE, "w") as fh:
        json.dump(cache, fh)
    make_figures(cache)
    write_result(cache)


def _style():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.dpi": 150, "savefig.dpi": 150, "font.size": 8.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": 9, "axes.labelsize": 8.5, "legend.frameon": False,
        "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.5,
        "savefig.bbox": "tight", "savefig.facecolor": "white"})
    return plt


def make_figures(cache):
    plt = _style()
    # ---- morphology-forms.png -------------------------------------------------------
    forms = cache["forms"]
    fig, axes = plt.subplots(2, len(forms), figsize=(2.05 * len(forms), 4.6))
    for col, (label, f) in enumerate(forms.items()):
        xz = np.array(f["projection_xz"]).T       # (z, x)
        xy = np.array(f["projection_xy"]).T
        axes[0, col].imshow(xz, origin="lower", cmap="bone_r", aspect="auto",
                            interpolation="nearest")
        axes[0, col].set_title(label, fontsize=6.8, loc="left")
        m = f["metrics"]
        axes[0, col].text(0.02, 0.97,
                          f"branches {m['branch_count']}\nS/V {m['surface_to_volume']:.2f}"
                          f"\nD {m['box_counting_dimension']:.2f}"
                          f"\nfill {m['bounding_box_fill']:.2f}",
                          transform=axes[0, col].transAxes, fontsize=5.8, va="top")
        axes[1, col].imshow(xy, origin="lower", cmap="bone_r", aspect="auto",
                            interpolation="nearest")
        for ax in (axes[0, col], axes[1, col]):
            ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        if col == 0:
            axes[0, col].set_ylabel("side view (x-z)")
            axes[1, col].set_ylabel("plan view (x-y)")
    fig.suptitle("SIMULATED colonies, one seed each. Silhouettes, not renderings: each "
                 "panel is the occupied-voxel projection. No coral was measured.",
                 fontsize=8.0, x=0.012, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(os.path.join(FIGDIR, "morphology-forms.png"))
    plt.close(fig)

    # ---- morphology-transition.png --------------------------------------------------
    da = cache["da_sweep"]; tr = cache["transition"]
    x = np.array([r["Da"] for r in da])
    fig, axes = plt.subplots(1, 4, figsize=(11.2, 3.0))
    panels = [("branch_count", "branch count (declared rule)"),
              ("surface_to_volume", "surface / volume (1 / voxel)"),
              ("box_counting_dimension", "box-counting dimension"),
              ("area_diameter_exponent", "area-diameter exponent b")]
    for ax, (key, lab) in zip(axes, panels):
        mu = np.array([r[key]["mean"] for r in da])
        sd = np.array([r[key]["sd"] for r in da])
        ax.fill_between(x, mu - sd, mu + sd, color="#4b5ea8", alpha=0.22, lw=0)
        ax.plot(x, mu, color="#1b4f72", lw=1.6, marker="o", ms=3)
        ax.set_xscale("log"); ax.set_xlabel("Da  (uptake / transport)")
        ax.set_title(lab, fontsize=7.8, loc="left")
        if key == "area_diameter_exponent":
            ax.axhspan(2.4, 2.5, color="#2e8b57", alpha=0.18, lw=0)
            ax.axhspan(1.8, 2.0, color="#b2452e", alpha=0.18, lw=0)
            ax.text(0.03, 0.93, "green: measured branching\nred: measured massive/tabular\n"
                                "(Chandler 2024, real colonies)",
                    transform=ax.transAxes, fontsize=5.6, va="top")
    axes[0].axvline(10 ** tr["midpoint_log10_Da"], color="#b2452e", ls="--", lw=0.9)
    axes[0].text(0.03, 0.93,
                 f"{tr['verdict']}: 10-90% over\n{tr['width_decades']:.2f} decades of Da\n"
                 f"(declared cut: sharp < 0.5)",
                 transform=axes[0].transAxes, fontsize=5.8, va="top", color="#b2452e")
    fig.suptitle("SIMULATED. Band is +/- 1 SD over independent random seeds, not a "
                 "confidence interval. Only the rightmost panel can be compared with a "
                 "measurement.", fontsize=8.0, x=0.012, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(os.path.join(FIGDIR, "morphology-transition.png"))
    plt.close(fig)
    print("figures written")


def write_result(cache):
    da = cache["da_sweep"]; tr = cache["transition"]; ctrl = cache["control_arm"]
    pl = cache["pe_light_sweep"]
    exps = [r["area_diameter_exponent"]["mean"] for r in da
            if r.get("area_diameter_exponent")]
    # THE CONTROL SENTENCE IS GENERATED FROM control_arm, NOT WRITTEN BESIDE IT.
    # An earlier version asserted "Both pre-declared controls pass" in prose while the
    # control block recorded six checks with one failing, and offered the FAILING
    # measurement (box dimension 2.43) as evidence that it passed. The sentence is now
    # derived, so it cannot drift from the thing it describes.
    n_ck = len(ctrl["checks"])
    n_fail = sum(1 for v in ctrl["checks"].values() if not v)
    n_pass = n_ck - n_fail
    _est = ctrl.get("estimator_control", {}).get("solid_hemisphere", {})
    _hemi = _est.get("measured_box_dimension")
    _lo_D = ctrl["arms"]["low_Da_isotropic"]["box_counting_dimension"]["mean"]
    if n_fail == 0:
        control_sentence = f"All {n_ck} pre-declared controls pass."
    else:
        _names = ", ".join(f"`{k}`" for k, v in ctrl["checks"].items() if not v)
        control_sentence = (
            f"{n_pass} of {n_ck} pre-declared controls pass and {n_fail} FAILS: "
            f"{_names}. The compact low-Da mound measures a box-counting dimension of "
            f"{_lo_D:.2f} against the >2.6 declared before the run, and the criterion "
            f"was not moved.")
        if _hemi is not None:
            control_sentence += (
                f" What makes that failure interpretable is a positive control for the "
                f"ESTIMATOR: a solid hemisphere of the same voxel count, whose true "
                f"dimension is 3, measures {_hemi:.2f} with the same code over the same "
                f"five box sizes, and a solid cube "
                f"{ctrl['estimator_control']['solid_cube']['measured_box_dimension']:.2f}. "
                f"So the mound is within {abs(_lo_D - _hemi):.2f} of a solid object and "
                f"the 2.6 threshold was wrong about what this estimator can return at "
                f"this size -- the model is not failing, the criterion was.")
    br_lo = ctrl["arms"]["low_Da_isotropic"]["branch_count"]["mean"]
    br_hi = ctrl["arms"]["high_Da_absorbing"]["branch_count"]["mean"]
    sv_lo = ctrl["arms"]["low_Da_isotropic"]["surface_to_volume"]["mean"]
    sv_hi = ctrl["arms"]["high_Da_absorbing"]["surface_to_volume"]["mean"]
    fill_lo = ctrl["arms"]["low_Da_isotropic"]["bounding_box_fill"]["mean"]
    fill_hi = ctrl["arms"]["high_Da_absorbing"]["bounding_box_fill"]["mean"]
    headline = (
        f"{control_sentence} "
        f"A voxel accretive-growth model in the published Kaandorp-Merks family, with a "
        f"single declared control parameter Da -- uptake rate over transport rate, the "
        f"ratio Merks et al. 2003 identify as controlling compactness. Da moves the "
        f"colony a long way: surface-to-volume from "
        f"{sv_lo:.2f} to {sv_hi:.2f} and bounding-box fill from {fill_lo:.2f} to "
        f"{fill_hi:.2f}, with the transition {tr['verdict'].upper()} -- by the cut "
        f"declared before the sweep, the branch count crosses from 10% to 90% of its "
        f"range over {tr['width_decades']:.2f} decades of Da. "
        f"THE STUDY ALSO FAILS AT WHAT IT WAS BUILT FOR, and that is reported rather "
        f"than buried: the model spans a compact mound to an open LOBED MOUND and does "
        f"not reach either true branching or plating. Branch counts stay in single "
        f"figures ({br_lo:.1f} to {br_hi:.1f}) and inspection of the projections shows "
        f"roughened domes, not separated branches, at every Da, flow and light weight "
        f"tried. So the branching-through-plating-through-massive span this study set "
        f"out to produce was not achieved, and the one metric comparable with real "
        f"colonies -- the area-diameter exponent, {min(exps):.2f} to {max(exps):.2f} "
        f"here against Chandler et al.'s measured 2.4-2.5 for branching genera and "
        f"1.8-2.0 for massive and tabular ones -- should be read in that light. "
        f"The most transferable result is a methodological one: getting even this far "
        f"took three rewrites of the growth rule, because two earlier voxel versions "
        f"were dominated by the lattice rather than the physics, and NONE of the four "
        f"declared metrics revealed it -- they all varied smoothly and plausibly with Da "
        f"while the shapes being measured were cubes and octahedra.")
    out = dict(
        schema="design-space-result-0.1",
        study_id="colony-morphology",
        title="Colony morphology as a growth-geometry problem",
        is_observation=False,
        headline=headline,
        provenance=dict(generated_at=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                        code="results/coral/code/colony_morphology.py"),
        model=dict(
            name="voxel Laplacian accretive growth with advective bias and a light field",
            kind="stochastic lattice growth on a steady resource field",
            is_observation=False,
            model_class_is_published=True,
            this_implementation_is_a_port=False,
            relationship_to_published_models=(
                "Same FAMILY as Kaandorp et al. 1996, Kaandorp & Sloot 2001, Merks et al. "
                "2003/2004 and Chindapol et al. 2013; NOT a port of any of them. "
                "Chindapol et al. couple steady Navier-Stokes to advection-diffusion on a "
                "deforming triangulated surface; this is a voxel lattice with an upwind "
                "advective bias. No number here should be compared with theirs as if it "
                "were a reimplementation."),
            chindapol_reference_settings=CHINDAPOL_REFERENCE,
            parameters=[
                dict(name="Da", value="swept " + str(DA_VALUES), units="nondimensional",
                     status="nondimensional",
                     source="Uptake rate times lattice spacing over diffusivity. The "
                            "ratio Merks et al. 2003 (PMID 12927523) identify as "
                            "controlling compactness: 'compactness of the growth form "
                            "depends on the ratio of the rates of growth and nutrient "
                            "transport'. No published numeric value exists for it, which "
                            "is why it is swept over four decades rather than set."),
                dict(name="Pe", value="swept " + str(PE_VALUES), units="nondimensional",
                     status="nondimensional",
                     source="Advective bias in lattice units. NOT comparable with "
                            "Chindapol et al.'s branch-scale Peclet numbers (0.016-0.288 "
                            "for real colonies) because the discretisation and the "
                            "velocity field are different."),
                dict(name="w_light", value="swept " + str(LIGHT_VALUES),
                     units="nondimensional", status="assumed",
                     source="Fraction of the growth response driven by the light field "
                            "rather than the diffusive resource. Invented; no study "
                            "partitions coral growth response between light and mass "
                            "transfer in these terms."),
                dict(name="light_attenuation", value=0.35, units="1 / voxel",
                     status="assumed",
                     source="Self-shading coefficient. No published value in any units "
                            "this could be converted from; the research block records "
                            "that NO irradiance threshold tied to a morphometric change "
                            "was found in any source."),
                dict(name="n_gen", value=cache["settings"]["n_gen"], units="generations",
                     status="nondimensional",
                     source="Growth generations. The colony is grown until it would touch "
                            "a lattice wall or this many generations pass, whichever is "
                            "first."),
                dict(name="hill_n", value=3.0, units="nondimensional",
                     status="assumed",
                     source="Hill exponent of the growth response to local flux. "
                            "Chindapol et al. 2013 use 1.2 in their own units; 3.0 here "
                            "is NOT theirs and is not comparable, because their argument "
                            "is an absolute concentration against a half-saturation in "
                            "mol/m3 and this one is a flux normalised to the "
                            "best-supplied site on the colony. Set to the smallest value "
                            "that makes screened sites fall behind permanently."),
                dict(name="hill_K", value=0.4, units="fraction of the maximum flux",
                     status="assumed",
                     source="Half-saturation of that response. Invented."),
                dict(name="speed_sigma", value=0.6, units="voxels",
                     status="assumed",
                     source="Gaussian smoothing of the SPEED field, which is what makes "
                            "the interface isotropic on a cubic lattice. It also sets "
                            "the finest feature the model can resolve, at roughly two "
                            "voxels, so the branch counts here are a lower bound."),
                dict(name="smooth_sigma", value=0.35, units="voxels",
                     status="assumed",
                     source="Gaussian regularisation of the phase field each generation. "
                            "It is what makes the interface isotropic on a cubic lattice "
                            "and it supplies a weak surface tension. It also sets the "
                            "FINEST BRANCH THE MODEL CAN RESOLVE, at roughly two voxels, "
                            "so the branch counts reported here are a lower bound: a "
                            "colony whose real branches were thinner than that would come "
                            "back smoother than it is."),
                dict(name="deposit_rate", value=0.45, units="voxels / generation",
                     status="nondimensional",
                     source="How fast the BEST-SUPPLIED surface site advances. Sets the "
                            "accretion step, not a biological rate."),
                dict(name="noise", value=0.15, units="lognormal sigma",
                     status="assumed",
                     source="Multiplicative jitter on the local flux. It is what makes "
                            "random seeds differ, and the seed-to-seed spread it produces "
                            "is reported beside every metric. Declared, not tuned."),
                dict(name="lattice", value=f"{cache['settings']['nx']}x"
                                           f"{cache['settings']['ny']}x"
                                           f"{cache['settings']['nz']}",
                     units="voxels", status="nondimensional",
                     source="Lattice size. A voxel has no length: nothing here is in "
                            "centimetres, and the model is deliberately not given a "
                            "length scale because the mapping from Da to a reef flow "
                            "speed is exactly what is NOT established."),
            ],
            metric_definitions=METRIC_DEFINITIONS,
        ),
        control_arm=ctrl,
        sweeps=dict(da=da, pe_light=pl),
        transition=tr,
        forms={k: {kk: vv for kk, vv in v.items()
                   if kk not in ("projection_xz", "projection_xy", "heightmap")}
               for k, v in cache["forms"].items()},
        what_this_model_does_not_do=dict(
            target="branching, plating and massive colonies from one control parameter",
            achieved="compact mound to open lobed mound",
            not_achieved=["separated branches", "plates or laminae"],
            plating_evidence=(
                "The light field does not produce plating, and the measurement that says "
                "so is the aspect ratio (height over maximum diameter) across the "
                "flow-by-light sweep: it sits at about 0.52 at EVERY light weight from 0 "
                "to 0.9, while the branch count collapses to 1. In other words, weighting "
                "growth toward a vertical light gradient makes the colony smoother "
                "without making it flatter. That is a negative with a published "
                "counterpart: Lesser et al. report that hemispherical colonies fix more "
                "carbon at all depths than plating or branching forms and yet plating "
                "dominates deeper reefs, so light geometry ALONE does not explain depth "
                "zonation. This model agrees with that, which is the most that can be "
                "claimed for it."),
            flow_result=(
                "Flow does something clear and in the published direction: raising the "
                "advective bias from 0 to 0.2 drops the mean branch count from about 4.7 "
                "to about 1.3, i.e. flow makes the colony more compact. That matches "
                "Kaandorp & Sloot 2001 and Chindapol et al. 2013 and NOT Merks et al. "
                "2003, who 'did not find an effect of flow'. A lattice model agreeing "
                "with one side of a modelling disagreement is not evidence about corals; "
                "it is evidence about which approximations reproduce which result."),
            evidence="Branch counts by the declared slice rule stay in single figures "
                     "across the whole Da sweep, and the projections in "
                     "morphology-forms.png show roughened domes rather than branches. "
                     "Four settings were tried beyond the sweep: lower interface "
                     "regularisation (speed_sigma 0.9 -> 0.6), a larger lattice with a "
                     "proportionally larger colony (88 -> 112 voxels, target volume "
                     "7,000 -> 14,000), and a steeper growth response (Hill exponent "
                     "3 -> 5, half-saturation 0.4 -> 0.6). All four gave the same "
                     "qualitative form.",
            diagnosis="A Mullins-Sekerka fingering instability needs the destabilising "
                      "flux gradient to beat the stabilising surface regularisation at "
                      "the branch wavelength. In this model the regularisation that "
                      "makes the interface isotropic on a cubic lattice is also what "
                      "suppresses fingering, and at the system sizes tried the two could "
                      "not be separated. A mesh-based implementation of the kind "
                      "Chindapol et al. use does not face that trade-off, which is "
                      "probably why the published models in this family are mesh-based.",
            what_it_means_for_the_page="The flow and light routes on the route table "
                                       "should NOT cite this study as showing that a "
                                       "growth model reproduces branching. It does not. "
                                       "It shows that one dimensionless ratio moves a "
                                       "colony between compact and open, which is a "
                                       "weaker and still useful statement.",
            is_observation=False),
        lattice_artefact_history=dict(
            note="Kept because it is the most transferable thing in this study.",
            attempt_1=dict(rule="6-connected growth, 6-point Laplacian",
                           result="square-based octahedra at low Da; four-pointed stars "
                                  "aligned with the x and y axes at high Da",
                           detected_by="looking at the projections"),
            attempt_2=dict(rule="26-connected growth, isotropic 27-point Laplacian",
                           result="cubes and hollow square boxes, because dilation by a "
                                  "3x3x3 cube grows in the Chebyshev metric",
                           detected_by="looking at the projections"),
            attempt_3=dict(rule="phase field, interface advanced by flux, speed field "
                                "smoothed for isotropy",
                           result="round hemispherical mounds at low Da; isotropic in "
                                  "plan view",
                           detected_by="looking at the projections"),
            two_further_failures=dict(
                all_six_faces_pinned_at_the_far_field=(
                    "The colony spread sideways until it touched a side wall, where the "
                    "pinned source gave it unlimited supply; the result was a wide flat "
                    "mat at every Da. Fixed by making only the TOP face a source."),
                smoothing_phi_instead_of_the_speed=(
                    "Smoothing the colony itself by 0.75 voxels every generation "
                    "compounds to an effective sigma of about six voxels over a run. "
                    "Every Da from 0.02 to 80 then returned the same compact mound to "
                    "three significant figures in all four metrics. Over-regularising "
                    "looks exactly like 'the control parameter does nothing'."),
                and_one_more=(
                    "Gaussian regularisation also erodes a small seed faster than flux "
                    "builds it, so the colony vanished entirely. Fixed by enforcing that "
                    "accretion is monotone, which it is: skeleton already laid down does "
                    "not dissolve.")),
            the_lesson="Four of these five failures were invisible in the declared "
                       "metrics and visible immediately in a picture. Surface-to-volume, "
                       "box-counting dimension and bounding-box fill all varied smoothly "
                       "and plausibly with the control parameter through the octahedron "
                       "phase and the cube phase alike. Declaring metrics before looking "
                       "protects against choosing the metric that flatters the result; "
                       "it does not protect against measuring an artefact, and nothing "
                       "except looking does."),
        external_check=dict(
            name="area-diameter exponent against Chandler et al. 2024",
            source=dict(cite="Chandler et al. 2024, Sci Rep 14:20549, 'Predicting 3D and "
                             "2D surface area of corals from simple field measurements'",
                        pmid="39232103", read_level="full-text"),
            measured_real_colonies=dict(
                branching="Pocillopora 2.50 (n=13, R2 0.95); Seriatopora 2.451 (n=9); "
                          "Stylophora 2.413 (n=10)",
                tabular_and_massive="Acropora table 1.947 (n=13, R2 0.95); staghorn "
                                    "Acropora 2.024 (n=14, R2 0.81); massive Porites "
                                    "1.836 (n=9, R2 0.75); encrusting Montipora 1.875",
                caveats="Single sites, n of 6 to 14 per form, and the paper disagrees "
                        "with itself on one R2 (table 0.98 in the table against 0.95 in "
                        "the text). The staghorn model is stated not to apply above "
                        "about 80 cm."),
            simulated_range=[min(exps), max(exps)],
            verdict=("The simulated exponents are reported whether or not they agree. "
                     "A match would be weak evidence that the model's growth geometry "
                     "resembles a real colony's; a mismatch says the lattice model's "
                     "surface roughness is not a reef colony's, which would be "
                     "unsurprising since a voxel surface has a texture of its own."),
        ),
        limitations=[
            "This is a SIMULATION on a cubic lattice. No coral was measured, and nothing "
            "here has a length in centimetres.",
            "It is NOT a port of any published coral growth model. It is in the same "
            "family and it makes different approximations, so its numbers are not "
            "comparable with Chindapol et al.'s even where they share a symbol.",
            "A cubic lattice imposes its own anisotropy. Growth along the axes is "
            "cheaper than growth along a diagonal, so branch directions carry a "
            "six-fold bias that no coral has. The metrics most exposed to this are the "
            "box-counting dimension and the area-diameter exponent, both of which read "
            "the surface texture.",
            "Advection is a first-order upwind bias, not a flow field. There is no "
            "boundary layer, no wake, no Reynolds number and no momentum. So Pe here is "
            "a knob, not a Peclet number that could be set from a reef measurement.",
            "The light field is collimated from directly above with no scattering, no "
            "diffuse sky and no off-vertical rays. It is there to ask one question -- "
            "does a vertical light gradient alone produce plating -- and the answer is "
            "reported either way.",
            "The branch-count rule is the arbitrary part of the metric set. Restricting "
            "to the upper half of the colony is what stops a ragged mound counting as "
            "many branches, and a different cut would give different counts. The rule was "
            "written before the first sweep and is not adjusted.",
            "Five box sizes is a short scaling range for a box-counting dimension on a "
            "lattice this size. The number is a crude estimate and the seed-to-seed "
            "spread, reported beside it, is the honest error bar.",
            "The sharp-versus-graded verdict rests on a cut declared in advance (10-90% "
            "within half a decade of Da). The cut is arbitrary; declaring it first is "
            "the only protection available when the thing being judged is the shape of a "
            "curve. Note that every published source the research block covers uses "
            "GRADED language and none states a numeric branching threshold, so a 'sharp' "
            "verdict here would be a statement about this model and not about corals.",
            "Growth is stochastic and the reported spread is across random seeds only. "
            "It is not an uncertainty on anything biological.",
            "No mechanics. The storm-vulnerability argument that makes shape matter "
            "ecologically (Madin et al. 2014) needs a colony shape factor and a "
            "substrate tenacity, neither of which this model has; the research block "
            "records that the coefficients and the dislodgement threshold could not be "
            "retrieved anyway.",
            "No biology: no polyps, no skeleton density, no calcification, no energy "
            "budget, no symbionts. The branching mechanism Merks et al. 2004 call 'more "
            "potent' than Laplacian growth -- polyp fanning on convex surfaces -- is not "
            "represented, so this model tests only one of the three candidate controls "
            "the literature offers.",
        ],
        sources=[
            dict(cite="Merks, Hoekstra, Kaandorp & Sloot 2003, J Theor Biol 224:153, "
                      "'Models of coral growth: spontaneous branching, compactification "
                      "and the Laplacian growth assumption'", pmid="12927523",
                 read_level="abstract",
                 note="The source of this model's control parameter. Also the source of "
                      "the disagreement: these authors 'did not find an effect of flow' "
                      "and say earlier computational evidence for one 'may not be "
                      "conclusive'."),
            dict(cite="Chindapol, Kaandorp, Cronemberger, Mass & Genin 2013, PLoS Comput "
                      "Biol 9:e1002849", pmid="23326222", read_level="full-text",
                 note="The calibrated member of this model family, validated against CT "
                      "scans of flume-grown Pocillopora verrucosa. Finds, against Merks, "
                      "that flow DOES change form. The disagreement is preserved, not "
                      "resolved."),
            dict(cite="Kaandorp & Sloot 2001, J Theor Biol 209:257", pmid="11312588",
                 read_level="abstract",
                 note="Forms 'gradually transformed from thin-branching ones into more "
                      "spherical and compact morphologies' -- GRADED language, which is "
                      "what every source in this literature uses."),
            dict(cite="Merks, Hoekstra, Kaandorp & Sloot 2004, J Theor Biol 228:559",
                 pmid="15178203", read_level="abstract",
                 note="The competing branching mechanism, polyp fanning on convex "
                      "surfaces, which this model does not implement."),
            dict(cite="Kaandorp, Lowe, Frenkel & Sloot 1996, Phys Rev Lett 77:2328",
                 pmid="10061916", read_level="abstract",
                 note="The founding paper. NOTE the commonly cited 'Kaandorp et al. 2005 "
                      "PRL' does not exist; that title belongs to Kaandorp 1999 in Marine "
                      "Biology, which is not in PubMed."),
            dict(cite="Chandler et al. 2024, Sci Rep 14:20549", pmid="39232103",
                 read_level="full-text", note="The external check."),
            dict(cite="Reichert et al. 2017, Methods Ecol Evol — three-dimensional "
                      "fractal dimension discriminated coral species at least as well as "
                      "surface-volume ratio and rugosity, and considerably better within "
                      "species. Not in PubMed by my search; no values retrieved.",
                 pmid=None, read_level="search-summary"),
            dict(cite="Todd 2008, Biol Rev 83:315 — of 1,314 extant species, fewer than "
                      "20 have been tested for morphological plasticity.",
                 pmid="18979594", read_level="abstract"),
        ],
    )
    with open(RESULT, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"wrote {RESULT}")


if __name__ == "__main__":
    main()
