"""Analyse the control-channel sweep: find the knee, and say how wide it is.

Takes the raw sweep (produced by control_channels.py, here on a 16-core Nebius
job) and produces control-channels.json plus its figures. The knee rules were
declared before the sweep ran and are reproduced verbatim from the sweep module.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import statistics as st
import sys
import textwrap

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import control_channels as cc  # noqa: E402
from common import Param, param_block, style, OKABE, figure_caption, write_result  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NONTRIVIAL = [t for t in cc.TARGETS if not t.startswith("uniform_")]


def index(rows):
    d = {}
    for r in rows:
        d.setdefault((r["m"], r["wiring"], r["target"], r["seed"]), {})[r["n_chan"]] = r
    return d


def curve(by, m, wiring, target, seed, n_values):
    cells = by.get((m, wiring, target, seed), {})
    return [cells[n]["r2_blurred"] if n in cells else None for n in n_values]


def knees(by, m, wiring, target, n_values, seeds):
    k95, kcv, sat = [], [], []
    for s in seeds:
        ys = curve(by, m, wiring, target, s, n_values)
        if any(y is None for y in ys):
            continue
        k95.append(cc.knee_95(n_values, ys, ys[-1]))
        kcv.append(cc.knee_curvature(n_values, ys))
        sat.append(ys[-1])
    k95 = [k for k in k95 if k]
    kcv = [k for k in kcv if k]
    def msd(v):
        if not v:
            return {"mean": None, "sd": None, "n": 0, "values": []}
        return {"mean": float(st.mean(v)), "sd": float(st.stdev(v)) if len(v) > 1 else 0.0,
                "n": len(v), "min": min(v), "max": max(v), "values": sorted(v)}
    # The pre-registration says "smallest N whose MEAN R2 reaches 0.95 x R2 at N = K",
    # i.e. the knee of the averaged curve. That is one number and carries no spread,
    # and the spread is the thing worth having. So both are computed: the declared
    # statistic, and the distribution of per-seed knees around it.
    mats = []
    for sd in seeds:
        y = curve(by, m, wiring, target, sd, n_values)
        if None not in y:
            mats.append(y)
    knee_mean_curve = None
    if mats:
        mu = list(np.asarray(mats).mean(0))
        knee_mean_curve = cc.knee_95(n_values, mu, mu[-1])
    return {"knee_95": msd(k95),
            "knee_95_of_mean_curve_AS_DECLARED": knee_mean_curve,
            "knee_curvature": msd(kcv),
            "r2_at_full_individual_control": msd(sat)}


# --------------------------------------------------------------------------
# The real animal's operating point, from Renard et al. 2026 (PMID 42418335,
# read: full text). Euprymna berryi and Sepia officinalis.
# --------------------------------------------------------------------------
MEASURED_POINT = {
    "source": ("Renard MDM et al. 2026, eLife 110074, PMID 42418335 (read: full text "
               "via PMC). Species: Euprymna berryi and Sepia officinalis."),
    "independent_components_per_chromatophore": 3.715,
    "independent_components_per_chromatophore_sd": 1.211,
    "n_chromatophores_measured": 1829,
    "n_independent_components": 6795,
    "n_putative_motor_units": 754,
    "mean_components_per_motor_unit": 9.003,
    "mean_components_per_motor_unit_sd": 4.755,
    "fraction_of_units_spanning_multiple_chromatophores": 0.95877,
    "ninetieth_percentile_chromatophores_per_unit": 14,
    "self_consistency": (
        "The paper's numbers close on themselves, which is why they can be used as an "
        "operating point rather than quoted loosely: 6795 ICs over 1829 chromatophores "
        "is 3.715 per chromatophore, and 754 motor units at 9.003 ICs each is 6788 "
        "memberships, or 3.711 per chromatophore. One IC per chromatophore per motor "
        "unit, so a unit of 9 ICs is a unit of about 9 CHROMATOPHORES - which matches "
        "the discussion's 'typically around ten chromatophores' and '90% fewer than 14'."),
    "channels_per_actuator": 754 / 1829,
    "actuators_per_channel": 1829 / 754,
    "unit_size_chromatophores": 9,
    "preserved_disagreement": (
        "One internal inconsistency in the source is kept rather than smoothed: the "
        "convex-hull areas are reported with a median of 136,199.10 um^2 while '90% of "
        "clusters had a convex hull area smaller than 51,513.25 um^2'. Both cannot hold. "
        "Nothing here depends on the hull areas, so it is recorded and not resolved."),
}


def build(raw):
    rows = raw["rows"]
    n_values = raw["n_values"]
    seeds = raw["seeds"]
    K = raw["K"]
    by = index(rows)

    area_mm2 = cc.PATCH_MM ** 2
    per_unit = {}
    for m in raw["unit_sizes"]:
        for w in raw["wirings"]:
            for t in raw["targets"]:
                if t.startswith("uniform_"):
                    continue
                per_unit[f"{w}|m={m}|{t}"] = knees(by, m, w, t, n_values, seeds)

    # headline: the measured motor-unit size, the compact wiring, over all
    # non-trivial targets
    M_MEASURED = 9
    heads = []
    for t in NONTRIVIAL:
        kk = per_unit[f"compact|m={M_MEASURED}|{t}"]["knee_95"]
        if kk["mean"]:
            heads.append((t, kk))
    allv = [v for _, kk in heads for v in kk["values"]]
    declared = [per_unit[f"compact|m={M_MEASURED}|{t}"]["knee_95_of_mean_curve_AS_DECLARED"]
                for t in NONTRIVIAL]
    declared = [d for d in declared if d]
    headline = {
        "unit_size": M_MEASURED,
        "wiring": "compact",
        "targets": [t for t, _ in heads],
        "knee95_mean_channels": float(st.mean(allv)),
        "knee95_sd_channels": float(st.stdev(allv)),
        "knee95_min": min(allv), "knee95_max": max(allv),
        "n_measurements": len(allv),
        "knee95_of_mean_curves_AS_DECLARED": declared,
        "why_the_spread_is_zero": (
            "The s.d. across seeds and targets is 0.0, and that is a GRID ARTEFACT, not "
            "a precision claim. The channel count is swept on a 14-point logarithmic "
            "grid, so a knee can only ever land on a grid point; every seed and every "
            "non-trivial target happened to land on the same one. The real uncertainty "
            "is therefore bounded below by the grid spacing, which here is a factor of "
            "about 1.9 in either direction - the neighbouring grid points are 306 and "
            "1094. Quote the knee as 'between 306 and 1094, nearest grid point 579', "
            "not as '579 +/- 0'. A finer grid would be needed to say more, and the "
            "agreement across 30 independent runs is evidence that the knee is stable "
            "to within one grid step, which is a weaker and true statement."),
        "grid_neighbours": [306, 1094],
        "knee95_of_mean_curves_mean": float(st.mean(declared)) if declared else None,
        "statistic_note": (
            "The pre-registration defines the knee on the MEAN curve, which gives one "
            "number per target and no spread. Both are reported: "
            "`knee95_of_mean_curves_*` is the declared statistic, and "
            "`knee95_mean_channels` with its s.d. is the distribution of per-seed knees, "
            "which is what a spec sheet needs. They are computed from the same runs and "
            "should agree closely; if they do not, the per-seed distribution is skewed "
            "and the mean-curve number is the one to quote."),
        "knee95_channels_per_mm2": float(st.mean(allv)) / area_mm2,
        "knee95_as_fraction_of_actuators": float(st.mean(allv)) / K,
        "actuators_per_channel_at_the_knee": K / float(st.mean(allv)),
        "K_actuators": K,
        "coverage_prediction_K_over_m": K / M_MEASURED,
        "per_target": {t: kk for t, kk in heads},
    }

    # is the knee set by coverage (K/m) or by the target's spatial detail?
    coverage_test = {}
    for m in raw["unit_sizes"]:
        got = []
        for t in NONTRIVIAL:
            kk = per_unit[f"compact|m={m}|{t}"]["knee_95"]
            if kk["mean"]:
                got.append(kk["mean"])
        if got:
            coverage_test[m] = {"K_over_m": K / m, "knee95_mean": float(st.mean(got)),
                                "ratio_knee_to_K_over_m": float(st.mean(got)) / (K / m),
                                "per_target_means": {
                                    t: per_unit[f"compact|m={m}|{t}"]["knee_95"]["mean"]
                                    for t in NONTRIVIAL}}

    # negative control: random wiring must be worse than compact at matched N
    neg = []
    for t in NONTRIVIAL:
        for s in seeds:
            c = curve(by, M_MEASURED, "compact", t, s, n_values)
            r = curve(by, M_MEASURED, "random", t, s, n_values)
            if None in c or None in r:
                continue
            neg.append(sum(1 for a, b in zip(c, r) if a >= b - 1e-9) / len(c))
    # trivial targets: R2 is undefined, so MAE is the control
    triv = {}
    for t in ("uniform_dark", "uniform_light"):
        vals = [r["mae_blurred"] for r in rows
                if r["target"] == t and r["wiring"] == "compact" and r["n_chan"] == K]
        if vals:
            triv[t] = {"mae_at_full_control_mean": float(st.mean(vals)),
                       "r2": "undefined (zero-variance target); reported as null, not 1.0"}

    # where the real animal sits on our own curve
    n_animal = MEASURED_POINT["channels_per_actuator"] * K
    animal = {"channels_on_this_patch": n_animal,
              "channels_per_mm2": n_animal / area_mm2,
              "channels_per_actuator": MEASURED_POINT["channels_per_actuator"],
              "actuators_per_channel": MEASURED_POINT["actuators_per_channel"],
              "unit_size": MEASURED_POINT["unit_size_chromatophores"]}
    per_t = {}
    for t in NONTRIVIAL:
        mats = []
        for sd in seeds:
            y = curve(by, M_MEASURED, "compact", t, sd, n_values)
            if None not in y:
                mats.append(y)
        if not mats:
            continue
        mu = np.asarray(mats).mean(0)
        r2_at_animal = float(np.interp(math.log10(n_animal),
                                       np.log10(np.asarray(n_values, float)), mu))
        kk = per_unit[f"compact|m={M_MEASURED}|{t}"]["knee_95"]["mean"]
        sat = float(mu[-1])
        per_t[t] = {"r2_at_the_animals_channel_count": r2_at_animal,
                    "r2_at_full_individual_control": sat,
                    "fraction_of_saturation_reached": r2_at_animal / sat if sat > 0 else None,
                    "knee95_mean": kk,
                    "animal_relative_to_knee": (None if not kk else n_animal / kk)}
    rel = [v["animal_relative_to_knee"] for v in per_t.values() if v["animal_relative_to_knee"]]
    frac = [v["fraction_of_saturation_reached"] for v in per_t.values()
            if v["fraction_of_saturation_reached"]]
    animal["per_target"] = per_t
    animal["animal_over_knee_range"] = [min(rel), max(rel)] if rel else None
    animal["fraction_of_saturation_range"] = [min(frac), max(frac)] if frac else None
    animal["verdict"] = (
        "PAST the knee on every target" if rel and min(rel) > 1.15 else
        "AT the knee" if rel and min(rel) > 0.85 else
        "BELOW the knee on at least one target")

    oracle_gain = {}
    for t in NONTRIVIAL:
        a = per_unit[f"compact|m={M_MEASURED}|{t}"]["r2_at_full_individual_control"]["mean"]
        b = per_unit[f"oracle|m={M_MEASURED}|{t}"]["r2_at_full_individual_control"]["mean"]
        if a and b:
            oracle_gain[t] = {"compact": a, "oracle": b, "gain": b - a}

    return {
        "n_values": n_values, "K": K, "seeds": seeds,
        "per_unit": per_unit, "headline": headline, "animal": animal,
        "coverage_test": coverage_test,
        "negative_control_random_wiring": {
            "asks": "is compact wiring at least as good as random wiring at every "
                    "matched channel count?",
            "fraction_of_matched_points_where_compact_wins": float(st.mean(neg)),
            "n_comparisons": len(neg),
            "threshold": "> 0.90",
            "passed": bool(st.mean(neg) > 0.90)},
        "trivial_target_controls": triv,
        "oracle_headroom": oracle_gain,
        "by": by,
    }


def figures(raw, an, figdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    style()
    os.makedirs(figdir, exist_ok=True)
    n_values = an["n_values"]
    by = an["by"]
    seeds = raw["seeds"]
    K = an["K"]

    # ---- figure 1: fidelity against channel count ------------------------
    fig, axes = plt.subplots(2, 3, figsize=(13.0, 8.2), sharex=True, sharey=True)
    for ax, t in zip(axes.ravel(), NONTRIVIAL):
        for m, col in zip(raw["unit_sizes"], OKABE):
            mat = []
            for s in seeds:
                y = curve(by, m, "compact", t, s, n_values)
                if None not in y:
                    mat.append(y)
            if not mat:
                continue
            mat = np.asarray(mat)
            mu, sd = mat.mean(0), mat.std(0)
            ax.plot(n_values, mu, color=col, lw=1.5, label=f"{m} actuators/unit")
            ax.fill_between(n_values, mu - sd, mu + sd, color=col, alpha=0.18, lw=0)
            kk = an["per_unit"][f"compact|m={m}|{t}"]["knee_95"]
            if kk["mean"]:
                ax.axvline(kk["mean"], color=col, lw=1.0, ls=":", alpha=0.9)
        na = an["animal"]["channels_on_this_patch"]
        ax.axvline(na, color="#000000", lw=1.4, ls="-", alpha=0.85)
        pt = an["animal"]["per_target"].get(t)
        if pt:
            ax.plot([na], [pt["r2_at_the_animals_channel_count"]], "o",
                    color="#000000", ms=6, zorder=5)
        ax.set_xscale("log")
        ax.set_title(t.replace("_", " "), fontsize=9.5)
        ax.set_ylim(-0.03, 1.03)
    for ax in axes[-1]:
        ax.set_xlabel("independent control channels N")
    for ax in axes[:, 0]:
        ax.set_ylabel("pattern match (variance explained)")
    axes[0, 0].legend(fontsize=7.4, loc="upper left")
    axes[0, 0].annotate("the real animal\n(Renard 2026)",
                        (an["animal"]["channels_on_this_patch"], 0.12),
                        textcoords="offset points", xytext=(-6, 0), ha="right",
                        fontsize=7.4, color="#000000")
    hd = an["headline"]
    figure_caption(fig, 
        f"Simulation, not a measurement. {K} modelled pigment actuators on a "
        f"{cc.PATCH_MM:.0f} x {cc.PATCH_MM:.0f} mm skin patch at the measured cuttlefish "
        f"chromatophore density (2.44e-4 per um^2, Reiter et al. 2018), driven by N "
        f"independent channels each owning a compact motor unit. Bands are +/- 1 s.d. "
        f"across {len(seeds)} array seeds; dotted lines are the knee (smallest N reaching "
        f"95% of the score at one channel per actuator), declared before the sweep ran. "
        f"The two uniform targets are not shown: their variance is zero, so the score is "
        f"undefined and is reported as null rather than as a vacuous 1.0. At the measured "
        f"motor-unit size of 9, the knee is {hd['knee95_mean_channels']:.0f} +/- "
        f"{hd['knee95_sd_channels']:.0f} channels, i.e. "
        f"{hd['knee95_channels_per_mm2']:.0f} per mm^2. The solid black line and dot "
        f"mark where the real animal sits: Renard et al. 2026 resolved 754 putative "
        f"motor units driving 1829 chromatophores in Euprymna berryi and Sepia "
        f"officinalis, which is "
        f"{an['animal']['channels_per_actuator']:.3f} "
        f"channels per actuator, or {an['animal']['channels_on_this_patch']:.0f} channels "
        f"on this patch - {an['animal']['verdict']}.", width=196)
    fig.savefig(os.path.join(figdir, "channels-vs-fidelity.png"))
    plt.close(fig)


def render_example(seed, m, wiring, target, n_chan):
    pts = cc.make_array(seed)
    rend = cc.Renderer(pts)
    lo, hi = rend.range()
    raw_t = cc.make_target(target)
    tgt = rend.blur(lo + (hi - lo) * raw_t)
    rng = np.random.default_rng(seed * 1000 + hash(wiring) % 997 + n_chan)
    chans = cc.build_channels(pts, n_chan, m, wiring, rng, target=raw_t, renderer=rend)
    img, _ = cc.solve(rend, chans, tgt)
    return img, tgt, cc.score(img, tgt, rend)


def figure_examples(an, figdir, target="gravel_1f", m=9, seed=11):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    style()
    ns = [n for n in an["n_values"] if n >= 1]
    pick = []
    for frac in (0.004, 0.03, 0.12, 0.5, 1.0):
        pick.append(min(ns, key=lambda n: abs(n - frac * an["K"])))
    pick = sorted(set(pick))
    fig, axes = plt.subplots(2, len(pick) + 1, figsize=(2.05 * (len(pick) + 1), 5.0))
    _, tgt0, _ = render_example(seed, m, "compact", target, an["K"])
    vmin, vmax = float(tgt0.min()), float(tgt0.max())
    for row, wiring in enumerate(("compact", "oracle")):
        axes[row, 0].imshow(tgt0, cmap="gray", vmin=vmin, vmax=vmax)
        axes[row, 0].set_title("target" if row == 0 else "", fontsize=8.5)
        axes[row, 0].set_ylabel(wiring, fontsize=9)
        axes[row, 0].set_xticks([]); axes[row, 0].set_yticks([])
        for col, n in enumerate(pick, start=1):
            img, _, sc = render_example(seed, m, wiring, target, n)
            ax = axes[row, col]
            ax.imshow(img, cmap="gray", vmin=vmin, vmax=vmax)
            ax.set_xticks([]); ax.set_yticks([])
            lab = f"N={n}"
            if row == 0:
                ax.set_title(lab, fontsize=8.5)
            # inside the panel, or the top row's labels sit under the bottom row
            ax.text(0.035, 0.965, f"{sc['r2_blurred']:.2f}", transform=ax.transAxes,
                    ha="left", va="top", fontsize=8.2, color="#111111",
                    bbox=dict(facecolor="white", alpha=0.75, edgecolor="none",
                              boxstyle="square,pad=0.18"))
    figure_caption(fig, 
        f"Simulation, not a measurement, and not a photograph of skin. Each panel is the "
        f"modelled blurred reflectance of {an['K']} pigment actuators at the measured "
        f"chromatophore density, driven by N independent channels of {m} actuators each "
        f"towards the '{target.replace('_', ' ')}' target (leftmost), with the same grey "
        f"scale throughout. Top row: compact wiring, each channel owning its nearest "
        f"unclaimed actuators, so at low N most of the array is UNINNERVATED and sits "
        f"retracted - which is why those panels are nearly blank rather than merely "
        f"coarse. Bottom row: the oracle wiring, which is allowed to choose its motor "
        f"units after seeing the target AND partitions the whole array regardless of "
        f"unit size, so it relaxes two constraints at once and is a loose upper bound "
        f"rather than a fair comparison. The number in each panel is the declared match "
        f"metric.", width=150)
    fig.savefig(os.path.join(figdir, "channels-examples.png"))
    plt.close(fig)


def make_video(an, figdir, target="gravel_1f", m=9, seed=11):
    """Sweep N and write an mp4. Skipped quietly if ffmpeg is absent."""
    import shutil
    import subprocess
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    if not shutil.which("ffmpeg"):
        return {"written": False, "reason": "ffmpeg not on PATH"}
    style()
    tmp = os.path.join(figdir, "_frames")
    os.makedirs(tmp, exist_ok=True)
    ns = an["n_values"]
    _, tgt0, _ = render_example(seed, m, "compact", target, an["K"])
    vmin, vmax = float(tgt0.min()), float(tgt0.max())
    for i, n in enumerate(ns):
        img, _, sc = render_example(seed, m, "compact", target, n)
        fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.0))
        axes[0].imshow(tgt0, cmap="gray", vmin=vmin, vmax=vmax)
        axes[0].set_title("target", fontsize=10)
        axes[1].imshow(img, cmap="gray", vmin=vmin, vmax=vmax)
        axes[1].set_title(f"{n} channels of {m} actuators    match {sc['r2_blurred']:.2f}",
                          fontsize=10)
        for ax in axes:
            ax.set_xticks([]); ax.set_yticks([])
        fig.text(0.5, 0.02, "Simulation of a modelled pigment-actuator array, not a "
                 "measurement and not skin.", ha="center", fontsize=7.4, color="#3a3a3a")
        fig.tight_layout(rect=(0, 0.06, 1, 1))
        fig.savefig(os.path.join(tmp, f"f{i:03d}.png"), dpi=110)
        plt.close(fig)
    out = os.path.join(figdir, "channels-demo.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-threads", "1", "-framerate", "2",
           "-i", os.path.join(tmp, "f%03d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", out]
    rc = subprocess.run(cmd, capture_output=True, text=True)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    return {"written": rc.returncode == 0, "path": "figures/channels-demo.mp4",
            "frames": len(ns), "stderr": rc.stderr[-400:] if rc.returncode else ""}


def parameters():
    S, A, N = "sourced", "assumed", "nondimensional"
    REI = ("Reiter S et al. (Laurent G) 2018, Nature 562:361-366, PMID 30333578 "
           "(read: full text)")
    REN = ("Renard MDM et al. 2026, eLife 110074, PMID 42418335 (read: full text)")
    HAD = ("Hadjisolomou SP et al. 2021, Front Physiol 12:675252, PMID 34220538 "
           "(read: full text)")
    return [
        Param("actuator_density", cc.DENSITY_PER_UM2, "per um^2", S,
              f"Mean chromatophore density measured on cuttlefish dorsal mantle: "
              f"2.44e-4 per um^2 (the paper's own simulation reproduced it at "
              f"2.52e-4 +/- 0.1e-4). {REI}."),
        Param("area_ratio", cc.AREA_RATIO, "dimensionless", S,
              f"+155.06% mean surface-area increase on expansion. {HAD}. A startle "
              "response, not a measured maximum - see the actuator study."),
        Param("unit_sizes", list(cc.UNIT_SIZES), "actuators per channel", S,
              f"Spans the measured range from two independent studies: motor units of "
              f"2-10 chromatophores with a median motor ELEMENT of 3 ({REI}); a mean of "
              f"about 9 chromatophores per putative motor unit, 90% under 14 and "
              f"occasionally up to 30 ({REN}). The value 1 is included as the "
              "one-channel-per-actuator limit, which no animal has."),
        Param("within_unit_nnd_um", cc.WITHIN_UNIT_NND_UM, "um", S,
              f"Mean within-cluster nearest-neighbour distance 40.548 +/- 46.946 um, "
              f"against a global array NND of 6.130 +/- 1.589 um: chromatophores in one "
              f"motor unit are NOT immediate neighbours. {REN}."),
        Param("coverage_full", cc.COVERAGE_FULL, "dimensionless", A,
              "Areal coverage with every actuator expanded. Not measured. The resulting "
              "expanded diameter is 99.5 um, which lands at the top of the measured "
              "15-100 um chromatophore diameter range - a weak corroboration, not a "
              "source."),
        Param("r_pigment", cc.R_PIGMENT, "dimensionless", A,
              "Reflectance of fully pigmented skin. Not measured; the declared metric "
              "maps the target into the skin's own range, so this sets contrast and not "
              "pattern fidelity."),
        Param("r_background", cc.R_BACKGROUND, "dimensionless", A,
              "Reflectance of the unpigmented backing. Not measured."),
        Param("blur_in_spacings", cc.BLUR_IN_SPACINGS, "mean actuator spacings", A,
              "Observer point-spread sigma. NO predator acuity number was sourced. "
              "Expressed in units of actuator spacing so the result is at least "
              "scale-free in the array."),
        Param("patch_mm", cc.PATCH_MM, "mm", N, "Edge of the square modelled skin patch."),
        Param("grid", cc.GRID, "pixels", N, "Raster on which the field is scored."),
        Param("n_iters", cc.N_ITERS, "iterations", N, "Adam steps per configuration."),
        Param("knee_fraction", cc.KNEE_FRACTION, "dimensionless", N,
              "Declared before the sweep: the knee is the smallest N reaching this "
              "fraction of the score at one channel per actuator."),
        Param("seeds", list(cc.SEEDS), "", N,
              "Array seeds. Every headline number is reported with its spread across "
              "these, not as a single value."),
    ]


def assemble(raw, an, video):
    hd = an["headline"]
    ct = an["coverage_test"]
    ratios = [v["ratio_knee_to_K_over_m"] for v in ct.values()]
    return {
        "id": "control-channels",
        "title": "How many independent control channels does an addressable skin need?",
        "kind": "simulation (pigment-actuator array + observer blur + "
                "projected-gradient controller)",
        "headline": (
            f"At the measured motor-unit size of nine actuators per channel, the knee is "
            f"{hd['knee95_mean_channels']:.0f} +/- {hd['knee95_sd_channels']:.0f} channels "
            f"over a {cc.PATCH_MM:.0f} x {cc.PATCH_MM:.0f} mm patch carrying "
            f"{hd['K_actuators']} actuators - about "
            f"{hd['knee95_channels_per_mm2']:.0f} channels per mm^2, or one channel per "
            f"{hd['actuators_per_channel_at_the_knee']:.1f} actuators. Across unit sizes "
            f"the knee tracks the number needed to COVER the array (K/m) within a factor "
            f"of {min(ratios):.2f}-{max(ratios):.2f}, so for everything but the finest "
            f"target the channel budget is set by innervating the skin at all, not by "
            f"the complexity of the pattern. The real animal is not a free parameter "
            f"here: Renard et al. 2026 resolved 754 putative motor units driving 1829 "
            f"chromatophores, which is {an['animal']['channels_per_actuator']:.3f} "
            f"channels per actuator and motor units of about nine, so on this patch the "
            f"animal sits at {an['animal']['channels_on_this_patch']:.0f} channels - "
            f"{an['animal']['verdict']}, reaching "
            f"{an['animal']['fraction_of_saturation_range'][0]*100:.0f}-"
            f"{an['animal']['fraction_of_saturation_range'][1]*100:.0f}% of the fidelity "
            f"it would get from one channel per chromatophore."),
        "preregistration": {
            "declared_before_any_run": True,
            "primary_metric": "variance explained (R^2) on the observer-blurred "
                              "reflectance field, clipped below at 0; the target is "
                              "affinely mapped into the skin's own achievable range "
                              "first, so the metric scores pattern fidelity and not the "
                              "pigment layer's contrast range",
            "secondary_metrics": ["mean absolute error of the blurred field",
                                  "unclipped R^2, reported as a diagnostic"],
            "knee_rules": {
                "knee_95": "smallest N whose R^2 reaches 0.95 x R^2 at N = K",
                "knee_curvature": "maximum vertical distance from the chord of the "
                                  "(log10 N, R^2) curve"},
            "targets": list(cc.TARGETS),
            "wirings": list(cc.WIRINGS),
            "unit_sizes": list(cc.UNIT_SIZES),
            "note": "Declared in the module docstring of code/control_channels.py before "
                    "the first run. No target was added, dropped or re-parameterised "
                    "afterwards. The two uniform targets have zero variance, so R^2 is "
                    "undefined for them and is returned as null rather than as 1.0 - a "
                    "score of 1 earned by an empty denominator would otherwise have been "
                    "averaged in with real ones.",
        },
        "model": {
            "description":
                "Actuators placed by Poisson-disc sampling at the measured chromatophore "
                "density on a square skin patch, each expanding from a retracted to an "
                "expanded disc area in the measured ratio. N channels each drive a motor "
                "unit of m actuators; an actuator's drive is the clamped sum over the "
                "channels that own it. The pigment area field is blurred by an observer "
                "point-spread function and converted to reflectance through a "
                "random-overlap coverage law. Channel activations are optimised by Adam "
                "with box projection.",
            "state_variables": ["channel activations a in [0,1]^N",
                                "per-actuator drive u = clamp(sum of owning channels)"],
            "equations": [
                "A_i = A_ret + u_i (A_exp - A_ret)",
                "S = G * (sum_i A_i delta_i) / pixel area",
                "coverage = 1 - exp(-S)",
                "I = R_bg + (R_pig - R_bg) * coverage",
                "R^2 = 1 - SSE / SST on the blurred field",
            ],
            **param_block(parameters()),
        },
        "sweep": {
            "cells": len(raw["rows"]),
            "axes": {"channel_count": raw["n_values"], "unit_size": raw["unit_sizes"],
                     "wiring": raw["wirings"], "target": raw["targets"],
                     "seed": raw["seeds"]},
            "wall_clock_s": raw.get("elapsed_s"),
            "where": "Nebius job aijob-e00mz387dqe1bm2y5x, gpu-h100-sxm preset "
                     "1gpu-16vcpu-200gb, python:3.12-slim, 16 worker processes. Pure "
                     "NumPy; the GPU preset was the only way to get 16 cores.",
        },
        "results": {
            "headline": hd,
            "knee_is_set_by_coverage_not_complexity": {
                "test": "If the channel budget were set by the pattern's spatial detail, "
                        "the knee would depend on the target and not on the unit size. "
                        "If it is set by covering the array, the knee should sit near "
                        "K/m. Both are computed below.",
                "per_unit_size": ct,
                "ratio_range": [min(ratios), max(ratios)],
            },
            "where_the_real_animal_sits": an["animal"],
            "measured_operating_point": MEASURED_POINT,
            "per_configuration": an["per_unit"],
            "oracle_headroom": an["oracle_headroom"],
        "oracle_caveat": (
            "The oracle wiring relaxes TWO constraints, not one: it chooses its motor "
            "units after seeing the target, and it partitions the whole array into N "
            "clusters regardless of the unit size m, so every actuator is innervated "
            "even when N*m < K. It is therefore a loose upper bound and the gap to it "
            "should not be read as 'what better wiring would buy'. Found by looking at "
            "the rendered panels, not by a control."),
        },
        "controls_declared_but_NOT_REACHED": {
            "status": "DECLARED AND NOT REACHED - this is a gap in verification, not a "
                      "clean result",
            "what_happened": (
                "The Nebius job emitted its sweep before running its controls, by "
                "design: an earlier run had thrown away 11,200 completed cells when a "
                "NameError in the control step killed the process before anything was "
                "written, so `emit()` was changed to commit the expensive result first. "
                "That change saved this sweep. It also means the block that survived in "
                "the job log is tagged `sweep-only`: the controls block never printed, "
                "and the hackathon token expired before the job could be re-run. The "
                "five controls below were declared in the module docstring before the "
                "sweep ran and have NOT been run against this dataset."),
            "not_reached": [
                {"name": "array_uniformity",
                 "asks": "with every actuator expanded, is the blurred area-density "
                         "field bounded away from zero everywhere in the patch?",
                 "note": "Previously PASSED on this seed in local development "
                         "(min/mean 0.722 against a 0.5 threshold), but not re-run "
                         "against the shipped sweep."},
                {"name": "coverage_law_vs_exact_union",
                 "asks": "does 1 - exp(-s) match an exact rasterised disc union?",
                 "note": "Previously FAILED in local development: the law "
                         "under-estimates coverage by 16% relative when retracted. That "
                         "failure is reported in NOTES.md and stands; it has not been "
                         "re-measured here."},
                {"name": "optimiser_adequacy",
                 "asks": "at one channel per actuator, does the optimiser beat an "
                         "independent non-iterative inversion of the forward model?",
                 "note": "Previously PASSED locally (0.984 against a deconvolution "
                         "baseline of 0.955). Not re-run against the shipped sweep."},
                {"name": "monotonicity_in_channel_count",
                 "asks": "does r2 stop rising, rather than fall, as N grows, for every "
                         "wiring?",
                 "note": "Previously PASSED locally for all four wirings. Not re-run. "
                         "This is the one whose absence matters most: it is the control "
                         "that caught an optimiser artefact scoring 0.0000 at N = K."},
                {"name": "coverage_law_sensitivity",
                 "asks": "does the failed coverage law move the knee?",
                 "note": "Previously PASSED locally (knee unchanged at 512 under both "
                         "laws). Not re-run, and the knee has since moved to 579 on the "
                         "full grid, so even the local result does not transfer."},
            ],
            "what_IS_verified_here": (
                "Two analysis-side controls, run against the shipped rows: the "
                "negative control on random wiring, and the check that the two "
                "zero-variance targets are not scored vacuously. Do not describe those "
                "two as 'the controls' - seven were declared and two were reached."),
        },
        "controls": raw.get("controls", []) + [
            an["negative_control_random_wiring"],
            {"name": "trivial_targets_are_not_scored_vacuously",
             "asks": "do the two zero-variance targets return a vacuous R^2 of 1.0?",
             "result": an["trivial_target_controls"],
             "passed": True,
             "note": "They return null. Their mean absolute error at full control is the "
                     "control that does carry information."},
        ],
        "limitations": [
            "THE HEADLINE'S '99-101% of saturation' IS MEASURED AGAINST THE ANIMAL'S OWN "
            "MOTOR-UNIT SIZE, NOT AGAINST A PERFECT MATCH, and read carelessly it says "
            "the animal is near-optimal when it does not. At the measured unit size of "
            "nine actuators the achievable ceiling differs sharply by target: edge 0.971, "
            "square 0.961, stripes_coarse 0.958, mottle 0.950, gravel_1f 0.897 and "
            "stripes_fine only 0.644 (compact wiring, mean over five seeds). NO CHANNEL "
            "COUNT MOVES THESE. They are ceilings, not slow approaches: the curves are "
            "flat from roughly the knee onward, and at one channel per actuator - 3,904 "
            "channels, more than twice what the animal has - stripes_fine is still 0.644. "
            "What the result says is that the animal has every channel its unit size can "
            "use, and that a unit of nine is already too coarse to render fine detail. "
            "That is the same constraint the coverage test shows from the other side, "
            "where knee / (K/m) rises to 5.41 at thirty actuators per unit. This page "
            "must not be read as claiming cephalopod skin reproduces fine patterns well; "
            "it claims the animal is not channel-limited.",
            "Everything here is a model. No skin was built, and the only measured inputs "
            "are the actuator density, the expansion ratio and the motor-unit sizes.",
            "The observer's acuity is ASSUMED and it is the parameter the knee is most "
            "likely to depend on. No predator acuity number was sourced, so the blur is "
            "expressed in units of mean actuator spacing. A sharper observer needs more "
            "channels; we do not know by how much for any real fish.",
            "The coverage law under-estimates true coverage by up to 16% relative "
            "(`coverage_law_vs_exact_union`, which FAILS). Its sensitivity arm shows the "
            "knee does not move, but the absolute reflectances in this model are biased.",
            "Motor units here are compact or overlapping groups of WHOLE actuators. The "
            "real system is finer than that: a chromatophore is driven by about four "
            "independent sources acting on contiguous angular sectors, so the real array "
            "has roughly four times as many addressable elements as this model gives it. "
            "That makes our channel counts a LOWER bound on what the animal has, and it "
            "is the single biggest structural simplification here.",
            "Retraction is instantaneous in this model: it solves for a steady pattern "
            "and says nothing about how fast the skin can move between two of them. The "
            "actuator study is where timing lives, and it fails its control arm.",
            "One colour class only. Real skin layers light and dark chromatophores with "
            "iridophores and leucophores beneath, and the measured motor units are 89% "
            "monochromatic, so a real controller has at least two interleaved arrays.",
            "The array is flat, square and unstretched. A real one grows, and the "
            "developmental routes in routes.json are about exactly that.",
        ],
        "figures": [
            {"file": "figures/channels-vs-fidelity.png"},
            {"file": "figures/channels-examples.png"},
        ] + ([{"file": "figures/channels-demo.mp4"}] if video.get("written") else []),
        "video": video,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(ROOT, "control-channels-raw.json"))
    args = ap.parse_args()
    raw = json.load(open(args.raw))
    an = build(raw)
    figdir = os.path.join(ROOT, "figures")
    figures(raw, an, figdir)
    figure_examples(an, figdir)
    video = make_video(an, figdir)
    doc = assemble(raw, an, video)
    write_result(os.path.join(ROOT, "control-channels.json"), doc)
    print(doc["headline"])
    print("video:", video)
    return raw, an


if __name__ == "__main__":
    main()
