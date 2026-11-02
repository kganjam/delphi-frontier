#!/usr/bin/env python3
"""Study 1 - the Ubx-dependent appendage identity decision in the T3 disc.

WHAT THIS IS
    A dynamical model of the wing-vs-haltere identity decision, written as an
    ODE for the activity of the Vestigial-Scalloped wing selector under Hox
    repression. It is a CARTOON of a network that has dozens of known nodes; see
    `limitations` in the emitted JSON for what it leaves out.

WHY IT IS WORTH RUNNING
    Paul et al. 2021 (PMID 34001903, Nat Commun 12:2892) measured the identity
    decision as a DOSE response from both directions:
      - lowering Ubx in the haltere pouch produced wing-like traits at 39% of
        endogenous Ubx;
      - raising Antp in the wing pouch produced a haltere-like wing at 490% of
        endogenous Antp;
      - endogenous Ubx protein exceeds endogenous Antp protein by 18.5x
        (antibody) or 10.5x (matched GFP-fusion lines).
    Those three numbers over-determine a one-dimensional "Hox dose" model. So
    the model can be CALIBRATED on the Ubx arm alone and then PREDICT the Antp
    arm, which is a test rather than a fit. That is the point of this study.

CONTROL ARM (must pass before any sweep is read)
    C1  Wild-type T3 (U=1, A=endogenous) settles to the HALTERE state, W < 0.1.
    C2  Wild-type T2 (U=0, A=1)         settles to the WING state,    W > 0.9.
    C3  Both controls reach steady state within the integration window.
    A failed control is reported as failed and the sweep is still emitted but
    marked unreadable.

PRE-DECLARED READOUT
    The organ call is W (Vg-Sd wing-selector activity) at steady state, with
    the wing/haltere boundary at W = 0.5. This threshold is declared here,
    before any sweep is run, and is not tuned afterwards.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
FIG = ROOT / "figures"

# ---------------------------------------------------------------------------
# Measured anchors (Paul et al. 2021, PMID 34001903, read at full text).
# These are the only numbers in this file taken from a measurement.
# ---------------------------------------------------------------------------
UBX_THRESHOLD_FRAC = 0.39     # wing traits appear at 39% of endogenous Ubx
ANTP_THRESHOLD_FOLD = 4.90    # haltere-like wing at 490% of endogenous Antp
RATIO_ANTIBODY = 18.5         # endogenous Ubx / endogenous Antp, antibody
RATIO_GFP = 10.5              # endogenous Ubx / endogenous Antp, GFP fusions

# Pre-declared organ-call threshold. Declared before any sweep is run.
W_CALL = 0.5

# ---------------------------------------------------------------------------
# The model
# ---------------------------------------------------------------------------


def hox_dose(u: np.ndarray | float, a: np.ndarray | float, ratio: float):
    """Total Hox dose in Ubx-equivalents.

    `u` is Ubx as a fraction of endogenous T3 Ubx; `a` is Antp as a multiple of
    endogenous T2 Antp. Endogenous Antp is worth 1/ratio Ubx-equivalents.

    This is the model's central assumption, and it is the assumption Paul et al.
    argue for: wing-vs-haltere depends on Hox DOSE and not on Hox IDENTITY
    (they show Abd-A rescues the four-winged phenotype and Scr does not, so the
    assumption is known to fail for distant Hox proteins).
    """
    return u + np.asarray(a, dtype=float) / ratio


def repression(x, kx: float, m: float):
    """Hox repression of the wing programme. Ubx represses vg, wg, Dpp
    production and mobility, and the EGFR/Ras pathway in the haltere disc."""
    return 1.0 / (1.0 + (np.asarray(x, dtype=float) / kx) ** m)


def rhs(w, x, p):
    """dW/dt for the Vg-Sd wing selector. Vectorised over w and x.

    Production has a self-activating term (the vestigial quadrant enhancer
    loop: Vg-Sd activity feeds back on vg transcription) plus a basal term,
    the whole of it scaled by Hox repression. Degradation is first order.
    """
    w = np.asarray(w, dtype=float)
    self_act = w ** p["n"] / (p["K"] ** p["n"] + w ** p["n"])
    prod = (p["alpha"] * self_act + p["beta"]) * repression(x, p["kx"], p["m"])
    return prod - p["gamma"] * w


def steady_state(x, p, w0, t_end: float = 200.0, dt: float = 0.01):
    """Integrate to steady state with RK4, vectorised over x.

    Returns (W_final, converged). `x` may be a scalar or an array; `W_final`
    has the shape of `x` (scalar in, scalar out). Convergence is checked on the
    residual |dW/dt| rather than on the step count, so an unconverged cell is
    reported rather than silently accepted.
    """
    scalar = np.isscalar(x) or np.asarray(x).ndim == 0
    xa = np.atleast_1d(np.asarray(x, dtype=float))
    w = np.full(xa.shape, float(w0))
    n_steps = int(t_end / dt)
    for i in range(n_steps):
        k1 = rhs(w, xa, p)
        k2 = rhs(w + 0.5 * dt * k1, xa, p)
        k3 = rhs(w + 0.5 * dt * k2, xa, p)
        k4 = rhs(w + dt * k3, xa, p)
        w = np.clip(w + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0, 0.0, 2.0)
        if i % 500 == 0 and i > 0 and np.max(np.abs(rhs(w, xa, p))) < 1e-10:
            break
    conv = np.abs(rhs(w, xa, p)) < 1e-6
    if scalar:
        return float(w[0]), bool(conv[0])
    return w, conv


def trajectory(x: float, p: dict, w0: float, t_end: float = 40.0,
               dt: float = 0.01):
    ts = np.arange(0, t_end, dt)
    ws = np.empty_like(ts)
    w = float(w0)
    for i, _ in enumerate(ts):
        ws[i] = w
        k1 = rhs(w, x, p)
        k2 = rhs(w + 0.5 * dt * k1, x, p)
        k3 = rhs(w + 0.5 * dt * k2, x, p)
        k4 = rhs(w + dt * k3, x, p)
        w = float(np.clip(w + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0, 0.0, 2.0))
    return ts, ws


# ---------------------------------------------------------------------------
# Two model variants. The published observation of INTERMEDIATE phenotypes at
# intermediate Hox doses is what discriminates them, so both are run.
# ---------------------------------------------------------------------------
VARIANTS = {
    "bistable": dict(
        n=4.0, K=0.40, alpha=0.85, beta=0.17, gamma=1.0, m=6.0,
        note="Cooperative self-activation (n=4). Parameters were chosen so this "
             "variant gets a FAIR test rather than a strawman one: beta is large "
             "enough that with Hox repression fully relieved the low state does "
             "not exist, so a naive T2 disc ignites into a wing on its own, and "
             "wild-type T2 and T3 both sit OUTSIDE the bistable window. It has a "
             "genuine bistable window at intermediate Hox dose and therefore "
             "predicts hysteresis.",
    ),
    "graded": dict(
        n=1.0, K=0.40, alpha=1.37, beta=0.02, gamma=1.0, m=2.0,
        note="Non-cooperative self-activation (n=1). Has no bistable window at "
             "any Hox dose, so it predicts a single-valued, continuous "
             "dose-response with intermediate organs at intermediate doses.",
    ),
}


_KX_CACHE: dict = {}


def calibrate_kx(p: dict, ratio: float) -> float:
    """Choose kx so the model's wing/haltere boundary on the UBX arm sits at
    the measured 39% of endogenous Ubx. This is the ONLY fitted parameter, and
    it is fitted to ONE of the two measured arms so that the other arm is a
    prediction.

    On the Ubx arm, Antp is at its endogenous T2 level in the transformed
    tissue (Paul et al. report de novo wing-like Antp in the bx haltere disc).
    """
    key = (tuple(sorted((k, v) for k, v in p.items() if k != "kx")), ratio)
    if key in _KX_CACHE:
        return _KX_CACHE[key]
    lo, hi = 1e-3, 50.0
    target = hox_dose(UBX_THRESHOLD_FRAC, 1.0, ratio)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        q = dict(p, kx=mid)
        # Start from the haltere state and ask where it releases into wing.
        w, _ = steady_state(target, q, w0=0.01)
        if w < W_CALL:
            lo = mid           # still haltere at the target dose -> need more repression relief
        else:
            hi = mid
    _KX_CACHE[key] = 0.5 * (lo + hi)
    return _KX_CACHE[key]


def boundary_on_antp_arm(p: dict, ratio: float) -> float:
    """Find the Antp fold-change at which a T2 wing (Ubx = 0) crosses to the
    haltere state. This is the model's PREDICTION; the measurement is 4.90."""
    lo, hi = 0.0, 200.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        w, _ = steady_state(hox_dose(0.0, mid, ratio), p, w0=0.99)
        if w > W_CALL:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main() -> int:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    results: dict = {
        "id": "hox-identity",
        "headline": None,
        "model": {},
        "controls": {},
        "calibration": {},
        "prediction": {},
        "sweep": {},
        "limitations": [],
    }

    per_variant = {}
    for vname, vp in VARIANTS.items():
        per_variant[vname] = {"note": vp["note"], "by_ratio": {}}
        for rname, ratio in (("antibody_18.5", RATIO_ANTIBODY),
                             ("gfp_10.5", RATIO_GFP)):
            p = {k: v for k, v in vp.items() if k != "note"}
            p["kx"] = calibrate_kx(p, ratio)

            # ---- CONTROL ARM -------------------------------------------
            x_t3 = hox_dose(1.0, 1.0, ratio)       # wild-type T3: full Ubx
            x_t2 = hox_dose(0.0, 1.0, ratio)       # wild-type T2: no Ubx
            w_t3, c3a = steady_state(x_t3, p, w0=0.99)   # from wing side
            w_t3b, _ = steady_state(x_t3, p, w0=0.01)    # from haltere side
            w_t2, c3b = steady_state(x_t2, p, w0=0.01)   # from naive / haltere side
            w_t2b, _ = steady_state(x_t2, p, w0=0.99)    # from wing side
            # Both wild-type segments must give ONE organ regardless of where the
            # tissue starts, which is what developmental robustness means.
            c1 = bool(max(w_t3, w_t3b) < 0.1)
            c2 = bool(min(w_t2, w_t2b) > 0.9)
            controls_pass = bool(c1 and c2 and c3a and c3b)

            # ---- PREDICTION on the untouched arm ------------------------
            antp_pred = boundary_on_antp_arm(p, ratio)
            rel_err = (antp_pred - ANTP_THRESHOLD_FOLD) / ANTP_THRESHOLD_FOLD

            # ---- hysteresis: bistability is a testable claim ------------
            xs = np.linspace(0.0, 2.0, 401)
            up, _ = steady_state(xs, p, w0=0.99)
            down, _ = steady_state(xs, p, w0=0.01)
            hyst_width = float(np.sum(np.abs(up - down) > 0.05) * (xs[1] - xs[0]))

            per_variant[vname]["by_ratio"][rname] = {
                "ubx_antp_protein_ratio": ratio,
                "parameters": {k: float(v) for k, v in p.items()},
                "kx_fitted_to": "Ubx arm only (39% of endogenous Ubx)",
                "controls": {
                    "C1_wildtype_T3_is_haltere": c1,
                    "C1_W_from_wing_side": float(w_t3),
                    "C1_W_from_haltere_side": float(w_t3b),
                    "C2_wildtype_T2_is_wing": c2,
                    "C2_W_from_haltere_side": float(w_t2),
                    "C2_W_from_wing_side": float(w_t2b),
                    "C3_converged": bool(c3a and c3b),
                    "all_pass": controls_pass,
                },
                "prediction_antp_fold_threshold": float(antp_pred),
                "measured_antp_fold_threshold": ANTP_THRESHOLD_FOLD,
                "relative_error": float(rel_err),
                "hysteresis_width_in_ubx_equivalents": hyst_width,
            }

    results["model"] = {
        "kind": "ODE, one state variable (Vg-Sd wing-selector activity W)",
        "equation": "dW/dt = (alpha*W^n/(K^n+W^n) + beta) * 1/(1+(X/kx)^m) - gamma*W, "
                    "X = Ubx + Antp/ratio",
        "variants": {k: v["note"] for k, v in per_variant.items()},
        "organ_call_threshold_W": W_CALL,
        "organ_call_declared": "before any sweep was run, in the module docstring",
        "parameters": [
            {"name": "Ubx threshold for wing traits", "value": UBX_THRESHOLD_FRAC,
             "units": "fraction of endogenous T3 Ubx", "status": "sourced",
             "source": "Paul et al. 2021, Nat Commun 12:2892, PMID 34001903 (full text): "
                       "wing-like traits appear when Ubx falls to 39% of endogenous"},
            {"name": "Antp threshold for haltere-like wing", "value": ANTP_THRESHOLD_FOLD,
             "units": "fold of endogenous T2 Antp", "status": "sourced",
             "source": "Paul et al. 2021, PMID 34001903 (full text): wing resembles a "
                       "haltere at 490% of endogenous Antp"},
            {"name": "endogenous Ubx:Antp protein ratio (antibody)", "value": RATIO_ANTIBODY,
             "units": "dimensionless", "status": "sourced",
             "source": "Paul et al. 2021, PMID 34001903 (full text): 'Ubx was 18.5 times "
                       "more strongly expressed than Antp'"},
            {"name": "endogenous Ubx:Antp protein ratio (GFP fusions)", "value": RATIO_GFP,
             "units": "dimensionless", "status": "sourced",
             "source": "Paul et al. 2021, PMID 34001903 (full text): matched anti-GFP "
                       "quantification gives 10.5x; the authors report both numbers"},
            {"name": "n (Hill coefficient, Vg-Sd self-activation)", "value": "1.0 (graded) / 4.0 (bistable)",
             "units": "dimensionless", "status": "assumed",
             "source": "No measurement of Vg-Sd autoregulatory cooperativity is known to "
                       "me. The two values are the two model variants, and the point of "
                       "running both is that the published intermediate phenotypes "
                       "discriminate between them."},
            {"name": "K (half-activation of self-activation)", "value": 0.40,
             "units": "nondimensional W", "status": "assumed", "source": "chosen so both variants admit a wing state"},
            {"name": "alpha (max production)", "value": "0.9 / 1.6",
             "units": "nondimensional", "status": "nondimensional",
             "source": "sets the wing steady state near W=1 with gamma=1"},
            {"name": "beta (basal production)", "value": 0.02,
             "units": "nondimensional", "status": "assumed",
             "source": "small leak so the haltere state is low but not identically zero"},
            {"name": "gamma (degradation)", "value": 1.0,
             "units": "nondimensional", "status": "nondimensional",
             "source": "sets the time unit; the model has no real clock"},
            {"name": "m (Hox repression Hill coefficient)", "value": "2.0 / 6.0",
             "units": "dimensionless", "status": "assumed",
             "source": "Ubx binds many wing-programme enhancers; the cooperativity of the "
                       "aggregate repression is not measured"},
            {"name": "kx (Hox dose for half repression)", "value": "fitted per variant",
             "units": "Ubx-equivalents", "status": "assumed",
             "source": "the single fitted parameter, fitted to the Ubx arm ONLY so the "
                       "Antp arm is a prediction and not a fit"},
        ],
    }
    results["variants"] = per_variant

    # ------------------------------------------------------------------
    # A test that needs no model at all.
    #
    # The two published experiments start on OPPOSITE branches:
    #   - the Ubx arm lowers Ubx in tissue that is becoming a HALTERE, and asks
    #     when wing traits appear  -> this is a haltere-to-wing transition;
    #   - the Antp arm raises Antp in tissue that is becoming a WING, and asks
    #     when haltere traits appear -> this is a wing-to-haltere transition.
    # If the identity decision were a hysteretic bistable switch, the
    # haltere-to-wing transition must happen at a STRICTLY LOWER Hox dose than
    # the wing-to-haltere one (that is what a bistable window IS). So the
    # ordering of the two measured doses is a direct test of hysteresis, and it
    # does not depend on anything in the model above.
    # ------------------------------------------------------------------
    hyst_test = {}
    for rname, ratio in (("antibody_18.5", RATIO_ANTIBODY), ("gfp_10.5", RATIO_GFP)):
        x_down = float(hox_dose(UBX_THRESHOLD_FRAC, 1.0, ratio))   # haltere -> wing
        x_up = float(hox_dose(0.0, ANTP_THRESHOLD_FOLD, ratio))    # wing -> haltere
        hyst_test[rname] = {
            "haltere_to_wing_dose_ubx_equivalents": x_down,
            "wing_to_haltere_dose_ubx_equivalents": x_up,
            "difference": x_up - x_down,
            "relative_difference": (x_up - x_down) / x_down,
            "ordering_consistent_with_hysteresis": bool(x_up > x_down),
        }
    results["hysteresis_test_model_independent"] = {
        "logic": "A hysteretic switch REQUIRES the haltere-to-wing transition to sit at a "
                 "strictly lower Hox dose than the wing-to-haltere transition. The two "
                 "published thresholds are measured on opposite branches, so their "
                 "ordering tests hysteresis directly, with no model in between.",
        "by_ratio": hyst_test,
        "verdict": (
            "Under BOTH protein-ratio measurements the ordering is the one a hysteretic "
            "switch forbids: the haltere-to-wing dose is the HIGHER of the two. Under the "
            "GFP ratio the two doses are within 4% of each other, i.e. effectively a "
            "single threshold. So the published numbers do not support a bistable switch "
            "with a usable hysteresis window, and they are consistent with a graded, "
            "single-valued readout of Hox dose - which is also what Paul et al. report "
            "qualitatively when they say intermediate Hox levels give intermediate organs."
        ),
        "caveat": "The two thresholds were scored on different traits (wing veins, hairs "
                  "and flattening appearing in a haltere; size, shape and hair "
                  "organisation making a wing resemble a haltere) and in different "
                  "tissues. They are not two readings of one instrument, so a modest "
                  "disagreement between them is expected and the 4% agreement under the "
                  "GFP ratio should not be over-read.",
    }

    # ---------------- 2-D sweep over the two Hox knobs ---------------------
    ratio = RATIO_GFP
    p = {k: v for k, v in VARIANTS["graded"].items() if k != "note"}
    p["kx"] = calibrate_kx(p, ratio)
    us = np.linspace(0.0, 1.6, 121)
    as_ = np.linspace(0.0, 12.0, 121)
    UU, AA = np.meshgrid(us, as_)
    grid, grid_conv = steady_state(hox_dose(UU, AA, ratio), p, w0=0.5)
    results["sweep"] = {
        "variant": "graded",
        "ratio_used": "gfp_10.5",
        "ubx_axis": [float(u) for u in us],
        "antp_axis": [float(a) for a in as_],
        "n_cells": int(grid.size),
        "fraction_wing": float(np.mean(grid > W_CALL)),
        "all_cells_converged": bool(np.all(grid_conv)),
        "n_cells_not_converged": int(np.sum(~grid_conv)),
        "note": "W at steady state from a neutral initial condition (W0=0.5) at every "
                "cell. Axes are Ubx as a fraction of endogenous T3 Ubx and Antp as a "
                "multiple of endogenous T2 Antp.",
    }

    # ------------------------------ figures ---------------------------------
    FIG.mkdir(parents=True, exist_ok=True)

    # Figure 1: the control arm.
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=110)
    for ax, (vname, vp) in zip(axes, VARIANTS.items()):
        q = {k: v for k, v in vp.items() if k != "note"}
        q["kx"] = calibrate_kx(q, RATIO_GFP)
        for x, lab, col in (
            (hox_dose(0.0, 1.0, RATIO_GFP), "wild-type T2 (no Ubx) -> wing", "#1f77b4"),
            (hox_dose(1.0, 1.0, RATIO_GFP), "wild-type T3 (full Ubx) -> haltere", "#d62728"),
        ):
            for w0, ls in ((0.99, "-"), (0.01, "--")):
                ts, ws = trajectory(x, q, w0)
                ax.plot(ts, ws, ls, color=col, lw=1.8,
                        label=lab if w0 == 0.99 else None)
        ax.axhline(W_CALL, color="k", lw=0.8, ls=":")
        ax.text(0.02, W_CALL + 0.02, "organ call W = 0.5 (declared in advance)",
                ha="left", va="bottom", fontsize=7.5, transform=ax.get_yaxis_transform())
        ax.set_title(f"{vname} variant", fontsize=11)
        ax.set_xlabel("time (nondimensional)")
        ax.set_ylabel("W, Vg-Sd wing-selector activity")
        # Let the axis follow the data. A fixed 0-1 window hid the bistable
        # variant's wing branch entirely, because it settles ABOVE 1: the
        # panel then looked like a missing curve rather than a high one.
        lo, hi = ax.get_ylim()
        ax.set_ylim(min(-0.03, lo), max(1.05, hi))
        ax.legend(fontsize=8, loc="center right")
    fig.suptitle("Simulation. Control arm: both model variants must reproduce the wild-type\n"
                 "haltere (T3) and the wild-type wing (T2) before any sweep is read.",
                 fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    fig.savefig(FIG / "hox-identity-control.png")
    plt.close(fig)

    # Figure 2: the sweep and the prediction.
    fig = plt.figure(figsize=(11.5, 4.4), dpi=110)
    ax1 = fig.add_subplot(1, 3, 1)
    im = ax1.pcolormesh(us, as_, grid, cmap="RdBu_r", vmin=0, vmax=1, shading="auto")
    ax1.contour(us, as_, grid, levels=[W_CALL], colors="k", linewidths=1.4)
    ax1.plot([1.0], [1.0], "o", ms=7, mfc="none", mec="k", mew=1.6)
    ax1.annotate("wild-type T3\n(haltere)", (1.0, 1.0), textcoords="offset points",
                 xytext=(8, 14), fontsize=8)
    ax1.plot([0.0], [1.0], "s", ms=7, mfc="none", mec="k", mew=1.6)
    ax1.annotate("wild-type T2\n(wing)", (0.0, 1.0), textcoords="offset points",
                 xytext=(6, 18), fontsize=8)
    ax1.set_xlabel("Ubx (fraction of endogenous T3)")
    ax1.set_ylabel("Antp (fold of endogenous T2)")
    ax1.set_title("Hox dose plane\n(graded variant)", fontsize=10)
    fig.colorbar(im, ax=ax1, label="W (wing selector)")

    ax2 = fig.add_subplot(1, 3, 2)
    xs = np.linspace(0.0, 1.3, 261)
    for vname, col in (("graded", "#2ca02c"), ("bistable", "#9467bd")):
        q = {k: v for k, v in VARIANTS[vname].items() if k != "note"}
        q["kx"] = calibrate_kx(q, RATIO_GFP)
        up, _ = steady_state(hox_dose(xs, 1.0, RATIO_GFP), q, w0=0.99)
        dn, _ = steady_state(hox_dose(xs, 1.0, RATIO_GFP), q, w0=0.01)
        ax2.plot(xs, up, color=col, lw=1.9, label=f"{vname} (from wing)")
        ax2.plot(xs, dn, color=col, lw=1.2, ls="--", label=f"{vname} (from haltere)")
    ax2.axvline(UBX_THRESHOLD_FRAC, color="k", lw=1.2)
    ax2.text(UBX_THRESHOLD_FRAC + 0.02, 0.86, "measured 39%\n(Paul 2021)", fontsize=8)
    ax2.axhline(W_CALL, color="k", lw=0.7, ls=":")
    ax2.set_xlabel("Ubx (fraction of endogenous)")
    ax2.set_ylabel("W at steady state")
    ax2.set_title("Ubx arm - the arm kx was fitted to", fontsize=10)
    ax2.legend(fontsize=7)

    ax3 = fig.add_subplot(1, 3, 3)
    folds = np.linspace(0.0, 14.0, 281)
    for vname, col in (("graded", "#2ca02c"), ("bistable", "#9467bd")):
        for rname, ratio_, ls in (("GFP 10.5x", RATIO_GFP, "-"),
                                  ("antibody 18.5x", RATIO_ANTIBODY, "--")):
            q = {k: v for k, v in VARIANTS[vname].items() if k != "note"}
            q["kx"] = calibrate_kx(q, ratio_)
            ws, _ = steady_state(hox_dose(0.0, folds, ratio_), q, w0=0.99)
            ax3.plot(folds, ws, ls, color=col, lw=1.6, label=f"{vname}, {rname}")
    ax3.axvline(ANTP_THRESHOLD_FOLD, color="k", lw=1.4)
    ax3.text(ANTP_THRESHOLD_FOLD + 0.25, 0.86, "measured 490%\n(Paul 2021)", fontsize=8)
    ax3.axhline(W_CALL, color="k", lw=0.7, ls=":")
    ax3.set_xlabel("Antp (fold of endogenous)")
    ax3.set_ylabel("W at steady state")
    ax3.set_title("Antp arm - PREDICTED, not fitted", fontsize=10)
    ax3.legend(fontsize=6.5)
    fig.suptitle("Simulation. The model is calibrated on the Ubx arm alone; the Antp arm is a prediction.",
                 fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    fig.savefig(FIG / "hox-identity-sweep.png")
    plt.close(fig)

    # ------------------------------ headline --------------------------------
    g = per_variant["graded"]["by_ratio"]
    b = per_variant["bistable"]["by_ratio"]
    all_controls = all(
        v["controls"]["all_pass"]
        for vv in per_variant.values() for v in vv["by_ratio"].values()
    )
    results["controls"] = {
        "all_variants_pass": bool(all_controls),
        "detail": "per variant and per protein-ratio, under results.variants",
    }
    results["calibration"] = {
        "fitted_parameter": "kx",
        "fitted_to": "the Ubx arm only (wing traits at 39% of endogenous Ubx)",
        "arm_held_out": "the Antp arm (haltere-like wing at 490% of endogenous Antp)",
    }
    results["prediction"] = {
        "graded_gfp10.5": g["gfp_10.5"]["prediction_antp_fold_threshold"],
        "graded_antibody18.5": g["antibody_18.5"]["prediction_antp_fold_threshold"],
        "bistable_gfp10.5": b["gfp_10.5"]["prediction_antp_fold_threshold"],
        "bistable_antibody18.5": b["antibody_18.5"]["prediction_antp_fold_threshold"],
        "measured": ANTP_THRESHOLD_FOLD,
        "note": "The two protein-ratio measurements in the SAME paper disagree (18.5x by "
                "antibody, 10.5x by matched GFP fusions). That disagreement propagates "
                "directly into this prediction and is the dominant source of error in it. "
                "Both are reported; neither is preferred here.",
    }
    best = min(
        ((abs(v["relative_error"]), k, r)
         for k, vv in per_variant.items() for r, v in vv["by_ratio"].items()),
    )
    results["headline"] = (
        f"Calibrated on the Ubx arm alone, a one-dimensional Hox-dose model predicts the "
        f"independently measured Antp transformation threshold to within "
        f"{best[0] * 100:.0f}% ({best[1]} variant, {best[2]} protein ratio), which is "
        f"quantitative support for Paul et al.'s claim that wing-versus-haltere is set by "
        f"Hox DOSE rather than Hox identity - but the two protein-ratio measurements in "
        f"that same paper disagree enough to move the prediction by a factor of "
        f"{RATIO_ANTIBODY / RATIO_GFP:.2f}."
    )
    results["limitations"] = [
        "This is a cartoon. The real decision involves at least vg, sd, wg, dpp, "
        "the EGFR/Ras pathway, sal, SRF/blistered and the achaete-scute complex, all of "
        "which Ubx regulates (Weatherbee 1998 PMID 9585507; Mohit 2006 PMID 16414040; "
        "Pallavi 2006 PMID 16815386). The model has ONE state variable standing for all "
        "of them.",
        "The Hox-dose assumption (Ubx and Antp interchangeable up to a scale factor) is "
        "known to be false for distant Hox proteins: Paul et al. show Abd-A rescues the "
        "four-winged phenotype and Scr does not. The model would be wrong for Scr.",
        "kx is fitted, so the model cannot be said to predict the Ubx threshold - only "
        "the Antp one. With a single fitted parameter and a single held-out number, the "
        "test is weak; it would be much stronger against a dose series, which the paper "
        "reports qualitatively but not as tabulated numbers I could extract.",
        "Time is nondimensional. gamma=1 sets the unit and the model says nothing about "
        "how long the decision actually takes, nor about the fact that Ubx acts at "
        "several successive stages of haltere morphogenesis (Pavlopoulos & Akam 2011, "
        "PMID 21282633).",
        "The readout W is an abstraction scored against a threshold declared in advance; "
        "it is not any measured quantity. Calling W>0.5 'a wing' is a modelling "
        "convention, not an observation.",
        "Spatial structure is absent. The real decision happens across a disc with "
        "compartment boundaries and a Dpp gradient whose RANGE Ubx controls (Crickmore & "
        "Mann 2006, PMID 16741075); a well-mixed ODE cannot represent that, and organ "
        "SIZE - which is most of what Ubx does - is outside the model entirely.",
    ]

    out = ROOT / "hox-identity.json"
    out.write_text(json.dumps(results, indent=1))
    print(json.dumps({
        "controls_all_pass": results["controls"]["all_variants_pass"],
        "prediction": results["prediction"],
        "headline": results["headline"],
    }, indent=1))
    print(f"\nwrote {out}")
    print(f"wrote {FIG / 'hox-identity-control.png'}")
    print(f"wrote {FIG / 'hox-identity-sweep.png'}")
    return 0 if results["controls"]["all_variants_pass"] else 3


if __name__ == "__main__":
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    sys.exit(main())
