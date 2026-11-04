"""Study 2: the colour gamut of a pigment layer over a tunable multilayer reflector.

The stack, top to bottom, as the anatomy has it:

  seawater (n = 1.34, measured by Ghoshal 2013 with a refractometer)
  chromatophore pigment discs      partial areal coverage, three colour classes
  iridophore Bragg stack           N pairs of reflectin lamella / inter-lamellar space
  leucophore backing               broadband diffuse, switchable

The Bragg stack is the part of this design space with the best measurements in it:
layer count, both refractive indices, both thicknesses and the tuning range are all
published numbers from live cells. The pigment layer is the opposite: no absorption
spectrum for cephalopod ommochromes was found, so its spectral shape is a declared
assumption and the gamut it produces inherits that.

Outputs: the achievable gamut in CIE 1976 u'v' under a stated illuminant and the
standard observer, and an ablation saying which layer limits it.
"""
from __future__ import annotations

import json
import math
import os
import sys

import textwrap

import numpy as np
from scipy.spatial import ConvexHull

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Param, param_block, style, OKABE, figure_caption, write_result  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")

LAM = np.arange(380, 781, 1.0)          # nm, the scored band

# ---- sourced optical constants -------------------------------------------
N_LOW = 1.34        # Ghoshal 2013: set to the MEASURED refractive index of the ASW bath
N_HIGH = 1.405      # Ghoshal 2013: mean n_H of live-cell reflectin lamellae, +/- 0.012
N_HIGH_MAX = 1.44   # Ghoshal 2013/2014: maximum, and the directly measured condensed value
N_MEDIUM = 1.34     # seawater
PAIRS_LIVE = (8, 9)         # Ghoshal 2013: pairs contributing in LIVE cells
D_HIGH_LIVE = 120.0         # Ghoshal 2013 table 1, live cells: 120 +/- 15 nm
D_LOW_LIVE = 95.0           # Ghoshal 2013 table 1, live cells: 95 +/- 14 nm
LAMBDA_TUNE = (425.0, 675.0)   # Ghoshal 2013: the measured tuning range, blue to red
D_HIGH_RANGE = (80.0, 160.0)   # Ghoshal 2013: fitted thickness range
D_LOW_RANGE = (50.0, 120.0)

# ---- assumed pigment layer ------------------------------------------------
# Three ommochrome colour classes. Cuttlefish chromatophores progress yellow ->
# orange -> red -> dark with age (Reiter 2018, full text), and xanthommatin was
# localised to the light class. That fixes the ORDER of the classes and nothing
# about their spectra: no measured cephalopod ommochrome absorption spectrum was
# found, so every number below is assumed and the gamut inherits the assumption.
PIGMENTS = [
    {"name": "yellow", "edge_nm": 480.0, "width_nm": 28.0, "od": 1.1},
    {"name": "red",    "edge_nm": 570.0, "width_nm": 32.0, "od": 1.6},
    {"name": "brown",  "edge_nm": 660.0, "width_nm": 60.0, "od": 2.2},
]
AREA_RATIO = 2.5506          # SOURCED: Hadjisolomou 2021
COVERAGE_FULL = 0.85         # ASSUMED (same value as study 3, for consistency)
R_LEUCO = 0.60               # ASSUMED: broadband diffuse reflectance of a leucophore
R_DERMIS = 0.04              # ASSUMED: reflectance of the tissue below everything


# --------------------------------------------------------------------------
# colorimetry
# --------------------------------------------------------------------------
def load_colorimetry():
    cmf = np.loadtxt(os.path.join(DATA, "cie1931_2deg_1nm.csv"), delimiter=",")
    d65 = np.loadtxt(os.path.join(DATA, "cie_d65_5nm.csv"), delimiter=",")
    xb = np.interp(LAM, cmf[:, 0], cmf[:, 1])
    yb = np.interp(LAM, cmf[:, 0], cmf[:, 2])
    zb = np.interp(LAM, cmf[:, 0], cmf[:, 3])
    ill = np.interp(LAM, d65[:, 0], d65[:, 1])
    return np.stack([xb, yb, zb]), ill


CMF, ILLUM = load_colorimetry()
_K = 100.0 / np.trapezoid(CMF[1] * ILLUM, LAM)


def to_XYZ(reflectance: np.ndarray) -> np.ndarray:
    integ = CMF * (ILLUM * reflectance)[None, :]
    return _K * np.trapezoid(integ, LAM, axis=1)


def to_upvp(XYZ: np.ndarray) -> tuple[float, float]:
    X, Y, Z = XYZ
    d = X + 15.0 * Y + 3.0 * Z
    if d <= 0:
        return 0.0, 0.0
    return 4.0 * X / d, 9.0 * Y / d


def to_xy(XYZ: np.ndarray) -> tuple[float, float]:
    s = XYZ.sum()
    return (XYZ[0] / s, XYZ[1] / s) if s > 0 else (0.0, 0.0)


# --------------------------------------------------------------------------
# multilayer reflectance (transfer matrix, normal incidence)
# --------------------------------------------------------------------------
def bragg_reflectance(d_high, d_low, n_pairs, n_high=N_HIGH, n_low=N_LOW,
                      n_in=N_MEDIUM, n_out=N_LOW, lam=LAM) -> np.ndarray:
    """R(lambda) of n_pairs of (high, low) layers, with a final low-index exit.

    Characteristic-matrix form for a lossless isotropic stack at normal incidence.
    Ghoshal 2013 fitted their own data with the same transfer-matrix model and the
    same structure (N pairs plus a final bottom layer of index n_L).
    """
    layers = [(n_high, d_high), (n_low, d_low)] * int(n_pairs)
    m11 = np.ones_like(lam, dtype=complex)
    m12 = np.zeros_like(lam, dtype=complex)
    m21 = np.zeros_like(lam, dtype=complex)
    m22 = np.ones_like(lam, dtype=complex)
    for n, d in layers:
        delta = 2.0 * math.pi * n * d / lam
        c, s = np.cos(delta), np.sin(delta)
        a11, a12 = c, 1j * s / n
        a21, a22 = 1j * n * s, c
        m11, m12, m21, m22 = (m11 * a11 + m12 * a21, m11 * a12 + m12 * a22,
                              m21 * a11 + m22 * a21, m21 * a12 + m22 * a22)
    num = (m11 + m12 * n_out) * n_in - (m21 + m22 * n_out)
    den = (m11 + m12 * n_out) * n_in + (m21 + m22 * n_out)
    return np.abs(num / den) ** 2


def bragg_for_peak(lam_peak, n_pairs, n_high=N_HIGH, n_low=N_LOW,
                   ratio=D_HIGH_LIVE / D_LOW_LIVE):
    """Layer thicknesses that put the first-order Bragg peak at lam_peak.

    The period's optical thickness fixes the peak: lam = 2 (n_H d_H + n_L d_L).
    One equation, two unknowns, so the live-cell thickness RATIO (120:95, Ghoshal
    2013 table 1) is held and the pair scaled.
    """
    d_low = lam_peak / (2.0 * (n_high * ratio + n_low))
    return ratio * d_low, d_low


def pigment_transmittance(p, lam=LAM) -> np.ndarray:
    """Long-pass absorber: absorbs short wavelengths, transmits long ones."""
    a = 1.0 / (1.0 + np.exp((lam - p["edge_nm"]) / p["width_nm"]))
    return np.power(10.0, -p["od"] * a)


def coverage_range():
    """Areal coverage when retracted and when expanded, from the two anchors."""
    f_exp = COVERAGE_FULL
    s_exp = -math.log(1.0 - f_exp)
    f_ret = 1.0 - math.exp(-s_exp / AREA_RATIO)
    return f_ret, f_exp


def skin_reflectance(cov, lam_peak, n_pairs, leuco_on, n_high=N_HIGH,
                     tune_range=LAMBDA_TUNE) -> np.ndarray:
    """cov: three areal coverages, one per pigment class, each in [f_ret, f_exp]."""
    d_hi, d_lo = bragg_for_peak(lam_peak, n_pairs, n_high=n_high)
    r_bragg = bragg_reflectance(d_hi, d_lo, n_pairs, n_high=n_high)
    backing = R_LEUCO if leuco_on else R_DERMIS
    # one-bounce addition of the diffuse backing beneath the stack
    r_under = r_bragg + (1.0 - r_bragg) ** 2 * backing
    out = r_under
    for f, p in zip(cov, PIGMENTS):
        t2 = pigment_transmittance(p) ** 2       # down and back up
        out = out * (f * t2 + (1.0 - f))
    return np.clip(out, 0.0, 1.0)


# --------------------------------------------------------------------------
# gamut
# --------------------------------------------------------------------------
PEAK_STEP_NM = 31.25     # constant sampling DENSITY over whatever tuning range is used


def gamut_points(cov_levels=4, peak_levels=None, pairs=PAIRS_LIVE, leuco=(True, False),
                 n_high=N_HIGH, tune=LAMBDA_TUNE, area_ratio=AREA_RATIO,
                 fixed_cov=None, fixed_peak=None):
    f_ret, f_exp = coverage_range_for(area_ratio)
    fs = np.linspace(f_ret, f_exp, cov_levels)
    if fixed_cov is not None:
        fs = np.array([f_ret + fixed_cov * (f_exp - f_ret)])
    # A fixed NUMBER of peaks would make a wider tuning range sample more coarsely,
    # which made "widen the Bragg range" look like it SHRANK the gamut by 9%. Sample
    # at a fixed step instead, so the arms differ only in what they cover.
    n_peak = max(2, int(round((tune[1] - tune[0]) / PEAK_STEP_NM)) + 1)
    peaks = np.linspace(tune[0], tune[1], n_peak)
    if fixed_peak is not None:
        peaks = np.array([fixed_peak])
    pts, recs = [], []
    for f0 in fs:
        for f1 in fs:
            for f2 in fs:
                for lp in peaks:
                    for npairs in pairs:
                        for lc in leuco:
                            R = skin_reflectance((f0, f1, f2), lp, npairs, lc,
                                                 n_high=n_high)
                            XYZ = to_XYZ(R)
                            u, v = to_upvp(XYZ)
                            pts.append((u, v))
                            recs.append((f0, f1, f2, lp, npairs, lc, float(XYZ[1])))
    return np.asarray(pts), recs


def coverage_range_for(area_ratio):
    f_exp = COVERAGE_FULL
    s_exp = -math.log(1.0 - f_exp)
    return 1.0 - math.exp(-s_exp / area_ratio), f_exp


def hull_area(pts):
    if len(pts) < 3:
        return 0.0
    try:
        return float(ConvexHull(pts).volume)      # 2-D volume is area
    except Exception:
        return 0.0


# --------------------------------------------------------------------------
# controls
# --------------------------------------------------------------------------
def control_white_point():
    """The loaded CMFs and illuminant must put D65 at its published chromaticity."""
    XYZ = to_XYZ(np.ones_like(LAM))
    x, y = to_xy(XYZ)
    return {"name": "illuminant_white_point",
            "asks": "does a perfect diffuse white under the loaded D65 and CIE 1931 "
                    "2-degree CMFs land on the published D65 chromaticity?",
            "computed_xy": [x, y], "published_xy": [0.3127, 0.3290],
            "abs_error": [abs(x - 0.3127), abs(y - 0.3290)],
            "threshold": "both < 0.002",
            "passed": bool(abs(x - 0.3127) < 0.002 and abs(y - 0.3290) < 0.002),
            "note": "This is the control for the data files, not for the model. It is "
                    "the positive control that makes the gamut numbers below readable: "
                    "a mis-parsed CMF table and a correct one both produce a gamut."}


def control_tmm_against_quarter_wave():
    """Compare the transfer matrix against the closed form for a quarter-wave stack."""
    lam0 = 550.0
    n_h, n_l = N_HIGH, N_LOW
    d_h, d_l = lam0 / (4 * n_h), lam0 / (4 * n_l)
    out = []
    for npairs in (2, 4, 8, 9):
        R = bragg_reflectance(d_h, d_l, npairs, n_in=N_MEDIUM, n_out=n_l)
        r_num = np.interp(lam0, LAM, R)
        # Closed form: a stack of N quarter-wave (HL) pairs has effective
        # admittance Y = (n_H/n_L)^(2N) * n_out, and R = ((n_in - Y)/(n_in + Y))^2.
        y = (n_h / n_l) ** (2 * npairs) * n_l
        r_ana = ((N_MEDIUM - y) / (N_MEDIUM + y)) ** 2
        out.append({"pairs": npairs, "tmm": float(r_num), "closed_form": float(r_ana),
                    "abs_error": float(abs(r_num - r_ana))})
    worst = max(o["abs_error"] for o in out)
    return {"name": "tmm_vs_quarter_wave_closed_form",
            "asks": "does the transfer matrix reproduce the textbook quarter-wave "
                    "reflectance at the design wavelength?",
            "cases": out, "worst_abs_error": worst,
            "threshold": "worst absolute error < 0.01",
            "passed": bool(worst < 0.01),
            "note": "This control failed on its first run with a worst error of 0.033, "
                    "and reading it showed the error was in the CLOSED FORM, not in the "
                    "transfer matrix: the admittance had been written as "
                    "(n_H/n_L)^2N * n_H^2/(n_in n_L) instead of (n_H/n_L)^2N * n_out. "
                    "The wrong side is recorded because a control that is itself wrong "
                    "is the failure mode this check exists to make visible."}


def control_index_matched_stack():
    """NEGATIVE CONTROL: with n_high = n_low there is no stack and R must be ~0."""
    R = bragg_reflectance(D_HIGH_LIVE, D_LOW_LIVE, 9, n_high=N_LOW, n_low=N_LOW,
                          n_in=N_LOW, n_out=N_LOW)
    Rreal = bragg_reflectance(D_HIGH_LIVE, D_LOW_LIVE, 9)
    return {"name": "index_matched_stack_is_dark",
            "asks": "with the two indices equal, does the stack reflect nothing?",
            "max_R_index_matched": float(R.max()),
            "max_R_real_stack": float(Rreal.max()),
            "threshold": "index-matched max R < 1e-6 while the real stack is > 0.1",
            "passed": bool(R.max() < 1e-6 and Rreal.max() > 0.1),
            "note": "The positive arm is shipped beside the negative one: a transfer "
                    "matrix that silently returned zero would pass the negative arm "
                    "alone."}


def control_reproduce_ghoshal_tuning():
    """Does the published tuning range follow from the published dimensions?"""
    lam_live = 2 * (N_HIGH * D_HIGH_LIVE + N_LOW * D_LOW_LIVE)
    R_live = bragg_reflectance(D_HIGH_LIVE, D_LOW_LIVE, 9)
    lam_peak_num = float(LAM[int(np.argmax(R_live))])
    ends = {}
    for label, (dh, dl), stated in (("red_end", (150.0, 120.0), 675.0),
                                    ("blue_end", (80.0, 50.0), 425.0)):
        R = bragg_reflectance(dh, dl, 9)
        ends[label] = {"stated_peak_nm": stated,
                       "bragg_condition_nm": 2 * (N_HIGH * dh + N_LOW * dl),
                       "tmm_peak_nm": float(LAM[int(np.argmax(R))]),
                       "quoted_thicknesses_nm": [dh, dl]}
    err = max(abs(v["bragg_condition_nm"] - v["stated_peak_nm"]) for v in ends.values())
    return {"name": "reproduce_published_tuning",
            "asks": "do the paper's quoted endpoint thicknesses reproduce its quoted "
                    "425-675 nm tuning range?",
            "live_average_stack": {"d_high_nm": D_HIGH_LIVE, "d_low_nm": D_LOW_LIVE,
                                   "bragg_condition_nm": lam_live,
                                   "tmm_peak_nm": lam_peak_num},
            "endpoints": ends, "worst_discrepancy_nm": err,
            "passed": False,
            "finding": "FAILS, and the failure is in the source rather than in this "
                       "model. Ghoshal 2013's abstract and conclusion give the tuning "
                       "excursion as 'ca 150 to 80 nm' for the high-index lamellae and "
                       "'ca 120 to 50 nm' for the inter-lamellar spaces, for a measured "
                       "peak moving 675 -> 425 nm. Taking those four numbers literally "
                       "with the paper's own n_L = 1.34 and mean n_H = 1.405, the "
                       "first-order Bragg condition gives 743 nm and 359 nm. No constant "
                       "pair of indices satisfies both endpoints: matching 675 nm at "
                       "d_H = 150 needs n_L = 1.06, and matching 425 nm at d_H = 80 "
                       "needs n_L = 2.0. The quoted excursions are evidently rounded "
                       "('ca'). We therefore drive the model from the MEASURED peak "
                       "range 425-675 nm and solve for thicknesses at the measured "
                       "live-cell thickness ratio, rather than from the quoted "
                       "endpoint dimensions. The live-cell averages are consistent: "
                       "d_H = 120, d_L = 95 give 592 nm, a green, inside the range."}


def run_controls():
    return [control_white_point(), control_tmm_against_quarter_wave(),
            control_index_matched_stack(), control_reproduce_ghoshal_tuning()]





# --------------------------------------------------------------------------
# the gamut itself, and the ablation that names the limiting layer
# --------------------------------------------------------------------------
def spectral_locus():
    pts = []
    for i, lam in enumerate(LAM):
        R = np.zeros_like(LAM)
        R[i] = 1.0
        X = np.trapezoid(CMF * (ILLUM * R)[None, :], LAM, axis=1)
        if X.sum() > 0:
            pts.append(to_upvp(X))
    return np.asarray(pts)


ARMS = [
    ("full", "every dial free", {}),
    ("bragg_fixed_at_live_mean", "iridophore held at the live-cell mean stack",
     {"fixed_peak": 2 * (N_HIGH * D_HIGH_LIVE + N_LOW * D_LOW_LIVE)}),
    ("chromatophores_retracted", "all chromatophores held retracted", {"fixed_cov": 0.0}),
    ("chromatophores_expanded", "all chromatophores held expanded", {"fixed_cov": 1.0}),
    ("no_leucophore", "leucophore backing removed", {"leuco": (False,)}),
    ("eight_pairs_only", "stack fixed at eight pairs", {"pairs": (8,)}),
    ("wider_area_ratio_10x", "WIDENING: chromatophore area ratio 10x, not the "
     "measured 2.55x", {"area_ratio": 10.0}),
    ("wider_bragg_380_780", "WIDENING: Bragg tuning over the whole visible band",
     {"tune": (380.0, 780.0)}),
    ("higher_n_high_1p44", "WIDENING: n_H at the measured maximum 1.44, not the mean "
     "1.405", {"n_high": N_HIGH_MAX}),
    ("wider_area_ratio_50x", "WIDENING: chromatophore area ratio 50x, i.e. a retracted "
     "state that is nearly transparent", {"area_ratio": 50.0}),
    ("wider_bragg_and_n_high", "WIDENING: both optical dials at once",
     {"tune": (380.0, 780.0), "n_high": N_HIGH_MAX}),
]


def compute(cov_levels=5, peak_levels=None):
    locus = spectral_locus()
    results = {}
    for key, label, kw in ARMS:
        pts, recs = gamut_points(cov_levels=cov_levels, peak_levels=peak_levels, **kw)
        ys = [r[6] for r in recs]
        results[key] = {
            "label": label,
            "hull_area_upvp": hull_area(pts),
            "n_states": len(pts),
            "Y_min": float(min(ys)), "Y_max": float(max(ys)),
            "upvp": pts.tolist(),
        }
    base = results["full"]["hull_area_upvp"]
    for k, v in results.items():
        v["gamut_relative_to_full"] = v["hull_area_upvp"] / base if base > 0 else None
    return results, locus


def sweeps(cov_levels=4):
    """One-dimensional sweeps of the two optical dials the ablation points at."""
    out = {}
    rows = []
    for npairs in range(1, 13):
        pts, _ = gamut_points(cov_levels=cov_levels, pairs=(npairs,))
        d_hi, d_lo = bragg_for_peak(550.0, npairs)
        rpk = float(bragg_reflectance(d_hi, d_lo, npairs).max())
        rows.append({"n_pairs": npairs, "hull_area_upvp": hull_area(pts),
                     "peak_reflectance_at_550nm": rpk})
    out["lamella_pair_count"] = rows
    rows = []
    for nh in np.arange(1.35, 1.601, 0.025):
        pts, _ = gamut_points(cov_levels=cov_levels, n_high=float(nh))
        d_hi, d_lo = bragg_for_peak(550.0, 9, n_high=float(nh))
        rpk = float(bragg_reflectance(d_hi, d_lo, 9, n_high=float(nh)).max())
        rows.append({"n_high": round(float(nh), 4),
                     "index_contrast_n_high_over_n_low": round(float(nh) / N_LOW, 4),
                     "hull_area_upvp": hull_area(pts),
                     "peak_reflectance_at_550nm": rpk})
    out["reflectin_refractive_index"] = rows
    rows = []
    for ar in (1.5, 2.0, AREA_RATIO, 4.0, 6.0, 10.0, 20.0, 50.0, 100.0):
        pts, _ = gamut_points(cov_levels=cov_levels, area_ratio=ar)
        f_ret, f_exp = coverage_range_for(ar)
        rows.append({"area_ratio": ar, "coverage_retracted": f_ret,
                     "coverage_expanded": f_exp, "hull_area_upvp": hull_area(pts)})
    out["chromatophore_area_ratio"] = rows
    return out


def single_pigment_arms(cov_levels=5, peak_levels=None):
    """Which pigment class carries the gamut? Drop each in turn."""
    out = {}
    original = list(PIGMENTS)
    for drop in range(len(original)):
        PIGMENTS[:] = [p for i, p in enumerate(original) if i != drop]
        pts, _ = gamut_points(cov_levels=cov_levels, peak_levels=peak_levels)
        out[f"without_{original[drop]['name']}"] = hull_area(pts)
    PIGMENTS[:] = original
    return out


# --------------------------------------------------------------------------
# figures and the result file
# --------------------------------------------------------------------------
def parameters() -> list[Param]:
    S = "sourced"; A = "assumed"; N = "nondimensional"
    G13 = ("Ghoshal A, DeMartini DG, Eck E, Morse DE 2013, J R Soc Interface 10:20130386, "
           "PMID 23740489 (read: full text via PMC)")
    G14 = ("Ghoshal A et al. 2014, J R Soc Interface 11:20140106, PMID 24694894 "
           "(read: abstract)")
    HAD = ("Hadjisolomou SP et al. 2021, Front Physiol 12:675252, PMID 34220538 "
           "(read: abstract here; the actuator study read the full text)")
    REI = ("Reiter S, Laurent G et al. 2018, Nature 562:361-366, PMID 30333578 "
           "(read: full text)")
    return [
        Param("n_low", N_LOW, "dimensionless", S,
              f"Inter-lamellar space. {G13} set n_L = 1.34 to match the refractive "
              "index of the artificial-seawater bath, which they measured with a "
              "refractometer, because the spaces are continuous with it."),
        Param("n_high", N_HIGH, "dimensionless", S,
              f"Reflectin-filled lamellae in LIVE cells: 1.405 +/- 0.012, range "
              f"1.38-1.44, rarely to 1.48. {G13}. {G14} measured the condensed "
              "lamellae directly at about 1.44 by index matching."),
        Param("n_medium", N_MEDIUM, "dimensionless", A,
              "Incident medium taken as the same seawater index. Not separately "
              "measured for the skin surface, which carries mucus and epidermis."),
        Param("n_pairs", list(PAIRS_LIVE), "pairs", S,
              f"Eight or nine pairs contribute in live cells; six or seven in "
              f"chemically fixed ones. {G13}."),
        Param("d_high_live", D_HIGH_LIVE, "nm", S, f"120 +/- 15 nm, live cells, table 1. {G13}."),
        Param("d_low_live", D_LOW_LIVE, "nm", S, f"95 +/- 14 nm, live cells, table 1. {G13}."),
        Param("lambda_tuning_range", list(LAMBDA_TUNE), "nm", S,
              f"Measured peak tuning, 675 nm (red) to 425 nm (blue). {G13}."),
        Param("thickness_ratio", D_HIGH_LIVE / D_LOW_LIVE, "dimensionless", A,
              "Held constant while scaling the pair to a target peak. The Bragg "
              "condition is one equation in two thicknesses; the live-cell mean ratio "
              "is used to close it. The paper reports a weak positive correlation "
              "(Pearson R ~ 0.59) of BOTH thicknesses with peak wavelength, which is "
              "consistent with scaling at fixed ratio but does not establish it."),
        Param("pigment_edge_nm", [p["edge_nm"] for p in PIGMENTS], "nm", A,
              "Long-pass absorption edges of the three ommochrome classes. NO measured "
              f"cephalopod ommochrome absorption spectrum was found. {REI} measured "
              "chromatophore transmission spectra, found them bimodal at 615 nm, and "
              "localised xanthommatin to the light class, which fixes the ORDER "
              "yellow < red < brown and the long-pass SHAPE. The three numbers are "
              "chosen by hand inside that ordering."),
        Param("pigment_width_nm", [p["width_nm"] for p in PIGMENTS], "nm", A,
              "Sharpness of each absorption edge. No measurement; chosen by hand."),
        Param("pigment_od", [p["od"] for p in PIGMENTS], "dimensionless", A,
              "Peak optical density of one expanded pigment disc. No measurement."),
        Param("area_ratio", AREA_RATIO, "dimensionless", S,
              f"+155.06% mean chromatophore surface area on expansion. {HAD}. This is "
              "a startle response, not a measured maximum."),
        Param("coverage_full", COVERAGE_FULL, "dimensionless", A,
              "Areal coverage with every chromatophore of a class expanded. Not "
              "measured. The retracted coverage is then DERIVED from the sourced area "
              "ratio rather than assumed separately, and comes out at 0.52."),
        Param("r_leucophore", R_LEUCO, "dimensionless", A,
              "Broadband diffuse reflectance of the leucophore layer. Not measured in "
              "any source read; leucophores are described as broadband scatterers."),
        Param("r_dermis", R_DERMIS, "dimensionless", A,
              "Reflectance of the tissue below the stack when no leucophore is present."),
        Param("illuminant", "CIE D65", "", S,
              "CIE standard illuminant D65, 1 nm, from the CVRL database "
              "(cvrl.ioo.ucl.ac.uk/database/data/cie/Illuminantd65.csv, retrieved "
              "2026-11-02). NOT a measured underwater spectrum; see limitations."),
        Param("observer", "CIE 1931 2-degree", "", S,
              "CIE 1931 2-degree colour-matching functions, 1 nm, from the CVRL "
              "database (ciexyz31_1.csv, retrieved 2026-11-02). A HUMAN observer; "
              "cephalopods are colour-blind and their fish predators are not human."),
        Param("peak_sampling_step", PEAK_STEP_NM, "nm", N,
              "Sampling step of the Bragg peak across whatever tuning range an arm "
              "uses. Held constant so arms differ in coverage, not in sampling."),
    ]


def figures(res, locus, pig_drop, swp, figdir):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    style()
    os.makedirs(figdir, exist_ok=True)

    # ---- figure 1: the gamut in u'v' ------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 6.0))
    ax = axes[0]
    ax.plot(locus[:, 0], locus[:, 1], color="#999999", lw=1.0, zorder=1)
    ax.plot([locus[0, 0], locus[-1, 0]], [locus[0, 1], locus[-1, 1]],
            color="#999999", lw=1.0, ls=":", zorder=1)
    show = [("wider_bragg_and_n_high", OKABE[3], "if n$_H$ were at its measured max 1.44"),
            ("full", OKABE[0], "achievable, every dial free"),
            ("chromatophores_expanded", OKABE[2], "chromatophores held expanded"),
            ("bragg_fixed_at_live_mean", OKABE[1], "iridophore stack held fixed")]
    for key, col, lab in show:
        pts = np.asarray(res[key]["upvp"])
        if len(pts) >= 3:
            h = ConvexHull(pts)
            poly = pts[h.vertices]
            ax.add_patch(Polygon(poly, closed=True, facecolor=col, alpha=0.26,
                                 edgecolor=col, lw=1.6,
                                 label=f"{lab}  ({res[key]['hull_area_upvp']:.4f})"))
        else:
            ax.plot(pts[:, 0], pts[:, 1], "o", color=col, ms=3, label=lab)
    wp = to_upvp(to_XYZ(np.ones_like(LAM)))
    ax.plot(*wp, "k+", ms=11, mew=1.6)
    ax.annotate("D65", wp, textcoords="offset points", xytext=(7, 4), fontsize=8)
    ax.set_xlabel("CIE 1976 u'"); ax.set_ylabel("CIE 1976 v'")
    ax.set_xlim(0, 0.63); ax.set_ylim(0, 0.61)
    ax.set_title("Achievable chromaticities of the modelled skin")
    ax.legend(loc="lower right", fontsize=7.2)

    ax = axes[1]
    for lp, col in zip((440.0, 520.0, 600.0, 660.0), OKABE):
        d_hi, d_lo = bragg_for_peak(lp, 9)
        ax.plot(LAM, bragg_reflectance(d_hi, d_lo, 9), color=col, lw=1.4,
                label=f"stack tuned to {lp:.0f} nm  (d$_H$={d_hi:.0f}, d$_L$={d_lo:.0f} nm)")
    f_ret, f_exp = coverage_range()
    ax.plot(LAM, skin_reflectance((f_exp,) * 3, 520.0, 9, True), color="#444444",
            lw=1.6, ls="--", label="whole skin, all pigment expanded")
    ax.plot(LAM, skin_reflectance((f_ret,) * 3, 520.0, 9, True), color="#444444",
            lw=1.6, ls="-", label="whole skin, all pigment retracted")
    ax.set_xlabel("wavelength (nm)"); ax.set_ylabel("reflectance")
    ax.set_xlim(380, 780); ax.set_title("Stack reflectance, and the skin above it")
    ax.legend(fontsize=7.0, loc="upper left")
    figure_caption(fig, 
             "Optical model, not a measurement. Transfer-matrix reflectance of a "
             "reflectin/inter-lamellar Bragg stack whose layer count, both refractive "
             "indices, both thicknesses and 425-675 nm tuning range are measured "
             "(Ghoshal et al. 2013, live Doryteuthis opalescens iridocytes), under a "
             "pigment layer whose absorption spectrum is ASSUMED because none was "
             "found. Chromaticities are CIE 1976 u'v' under CIE D65 and the CIE 1931 "
             "2-degree observer - a human observer, which a cephalopod's predators are "
             "not. Hull areas in parentheses.", width=168)
    fig.savefig(os.path.join(figdir, "gamut-space.png"))
    plt.close(fig)

    # ---- figure 2: which layer limits it --------------------------------
    hold = [k for k, _, _ in ARMS if not k.startswith(("wider", "higher", "full"))]
    widen = [k for k, _, _ in ARMS if k.startswith(("wider", "higher"))]
    fig, axes = plt.subplots(1, 3, figsize=(15.2, 6.7),
                             gridspec_kw={"width_ratios": [1.5, 0.8, 1.0]})
    ax = axes[0]
    keys = hold + widen
    vals = [res[k]["gamut_relative_to_full"] for k in keys]
    cols = [OKABE[1]] * len(hold) + [OKABE[2]] * len(widen)
    ypos = np.arange(len(keys))[::-1]
    ax.barh(ypos, vals, color=cols, alpha=0.85)
    ax.axvline(1.0, color="k", lw=1.2)
    ax.set_yticks(ypos)
    ax.set_yticklabels([res[k]["label"] for k in keys], fontsize=7.4)
    for y, v, k in zip(ypos, vals, keys):
        extra = ""
        if k == "no_leucophore":
            extra = (f"  (chromaticity unchanged, but peak Y falls "
                     f"{res['full']['Y_max']:.0f} -> {res[k]['Y_max']:.1f})")
        ax.text(v + 0.02, y, f"{v:.2f}x{extra}", va="center", fontsize=7.4)
    ax.set_xlabel("gamut area relative to the full model")
    ax.set_xlim(0, max(vals) * 1.75)
    ax.set_title("Hold one layer (orange) / widen one dial (green)")

    ax = axes[1]
    names = list(pig_drop.keys())
    base = res["full"]["hull_area_upvp"]
    ax.barh(np.arange(len(names))[::-1], [pig_drop[n] / base for n in names],
            color=OKABE[4], alpha=0.85)
    ax.axvline(1.0, color="k", lw=1.2)
    ax.set_yticks(np.arange(len(names))[::-1])
    ax.set_yticklabels([n.replace("_", " ") for n in names], fontsize=8)
    ax.set_xlabel("gamut area relative to the full model")
    ax.set_title("Remove one pigment class")

    ax = axes[2]
    rows = swp["reflectin_refractive_index"]
    base = res["full"]["hull_area_upvp"]
    xs = [r["index_contrast_n_high_over_n_low"] for r in rows]
    ax.plot(xs, [r["hull_area_upvp"] / base for r in rows], "o-", color=OKABE[0],
            lw=1.6, ms=4, label="gamut area (relative)")
    ax2 = ax.twinx()
    ax2.plot(xs, [r["peak_reflectance_at_550nm"] for r in rows], "s--", color=OKABE[1],
             lw=1.4, ms=3.5, label="peak reflectance")
    ax2.set_ylabel("peak stack reflectance at 550 nm", color=OKABE[1], fontsize=8.5)
    ax2.grid(False)
    live = N_HIGH / N_LOW
    ax.axvline(live, color="#333333", lw=1.1, ls=":")
    ax.annotate(f"live cells\nn$_H$=1.405\ncontrast {live:.3f}", (live, 0.12),
                textcoords="offset points", xytext=(7, 0), fontsize=7.6, color="#333333")
    ax.axvline(N_HIGH_MAX / N_LOW, color=OKABE[2], lw=1.1, ls=":")
    ax.annotate("measured max 1.44", (N_HIGH_MAX / N_LOW, 0.45), rotation=90,
                textcoords="offset points", xytext=(5, 0), fontsize=7.6,
                color=OKABE[2], va="bottom")
    ax.set_xlabel("refractive-index contrast  n$_H$ / n$_L$")
    ax.set_ylabel("gamut area relative to the full model")
    ax.set_title("The dial that actually matters")
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=7.6, loc="upper left")

    figure_caption(fig, 
             "Optical model, not a measurement. Each bar is the convex-hull area of the "
             "achievable u'v' set when one layer is frozen or one dial widened, "
             "relative to the full model. Freezing the iridophore costs 88% of the "
             "gamut, so the stack is what PROVIDES the colour; but widening its tuning "
             "range buys 1%, while raising the reflectin refractive index to the "
             "measured maximum buys 68%, so index contrast is what LIMITS it. Removing "
             "the yellow pigment class ENLARGES the gamut, because at the one sourced "
             "expansion ratio a retracted chromatophore still covers 52% of the skin "
             "and that floor is a pure loss. Right: a one-dimensional sweep of the "
             "reflector's index contrast, holding everything else at the measured "
             "values. The animal sits on the steep part of that curve, which is why it "
             "is the lever worth pulling - and the whole range plotted stays below the "
             "contrast of a dried reflectin film (1.56/1.34), so a higher-index "
             "reflectin is not obviously unphysical for a protein.", width=238)
    fig.savefig(os.path.join(figdir, "gamut-limiting-layer.png"))
    plt.close(fig)


def build():
    res, locus = compute()
    swp = sweeps()
    pig_drop = single_pigment_arms()
    controls = run_controls()
    f_ret, f_exp = coverage_range()
    base = res["full"]["hull_area_upvp"]
    holds = {k: res[k]["gamut_relative_to_full"] for k, _, _ in ARMS
             if not k.startswith(("wider", "higher", "full"))}
    widens = {k: res[k]["gamut_relative_to_full"] for k, _, _ in ARMS
              if k.startswith(("wider", "higher"))}
    limiting = min(holds, key=holds.get)
    best_widen = max(widens, key=widens.get)
    single = {k: v for k, v in widens.items() if k != "wider_bragg_and_n_high"}
    best_single = max(single, key=single.get)
    out = {
        "id": "optical-gamut",
        "title": "A pigment layer over a tunable Bragg reflector: how much colour is "
                 "reachable, and which layer stops it",
        "kind": "optical model (transfer-matrix multilayer + areal pigment mixing + "
                "CIE colorimetry)",
        "headline":
            "Freezing the iridophore stack removes 88% of the achievable gamut, so the "
            "multilayer is what produces the colour; but widening its measured "
            "425-675 nm tuning range buys 1%, whereas raising the reflectin refractive "
            "index from the live-cell mean 1.405 to the measured maximum 1.44 buys 68% "
            "and a nearly transparent retracted state buys 61%. The limit is refractive-"
            "index contrast and the chromatophore's retraction floor, not tuning range. "
            "Removing the yellow pigment class makes the gamut BIGGER, because at the "
            "only sourced expansion ratio a retracted chromatophore still covers 52% of "
            "the skin.",
        "model": {
            "description":
                "Seawater over three independently driven ommochrome pigment classes "
                "(areal coverage each, double-pass absorbers), over an N-pair "
                "reflectin/inter-lamellar Bragg stack computed by transfer matrix at "
                "normal incidence, over a switchable broadband leucophore backing. "
                "Chromaticity in CIE 1976 u'v' under CIE D65 and the CIE 1931 "
                "2-degree observer; gamut is the convex-hull area of the achievable "
                "u'v' set.",
            "state_variables": [
                "areal coverage of each of three pigment classes, in [f_retracted, f_expanded]",
                "Bragg peak wavelength (set by scaling the layer pair at fixed ratio)",
                "number of lamella pairs (8 or 9)",
                "leucophore backing present or absent",
            ],
            "equations": [
                "stack: characteristic-matrix product over N (high, low) pairs at normal incidence",
                "first-order Bragg peak: lambda = 2 (n_H d_H + n_L d_L)",
                "pigment: T(lambda) = 10^(-OD * a(lambda)), a a long-pass sigmoid",
                "areal mixing, double pass: R = R_under * prod_k (f_k T_k^2 + 1 - f_k)",
                "backing: R_under = R_bragg + (1 - R_bragg)^2 * R_backing (one bounce)",
                "XYZ = k * integral CMF(lambda) * E(lambda) * R(lambda) d lambda",
            ],
            **param_block(parameters()),
        },
        "derived": {
            "coverage_retracted": f_ret,
            "coverage_expanded": f_exp,
            "note_on_coverage": (
                "f_expanded is assumed at 0.85; f_retracted is then DERIVED from the "
                "sourced 2.5506x area ratio and comes out at 0.52. The model therefore "
                "has no transparent state, and that is a consequence of the only "
                "sourced expansion number rather than a choice."),
            "live_mean_stack_peak_nm": 2 * (N_HIGH * D_HIGH_LIVE + N_LOW * D_LOW_LIVE),
        },
        "gamut": {k: {kk: vv for kk, vv in v.items() if kk != "upvp"}
                  for k, v in res.items()},
        "sweeps": swp,
        "sweep_note": (
            "Each sweep moves ONE dial and recomputes the whole achievable set. The "
            "pair-count and refractive-index sweeps are the quantitative form of the "
            "ablation's claim that index contrast, not tuning range, is the limit; the "
            "area-ratio sweep shows what a chromatophore with a transparent off-state "
            "would be worth. The live animal sits at 8-9 pairs, n_H = 1.405 and an area "
            "ratio of 2.55, all three of which are measured."),
        "pigment_drop_one": {k: {"hull_area_upvp": v,
                                 "relative_to_full": v / base} for k, v in pig_drop.items()},
        "which_layer_limits": {
            "largest_loss_when_frozen": limiting,
            "largest_loss_fraction": 1.0 - holds[limiting],
            "largest_gain_when_widened": best_widen,
            "largest_gain_factor": widens[best_widen],
            "largest_gain_from_a_SINGLE_dial": best_single,
            "largest_single_dial_gain_factor": single[best_single],
            "field_note": "`largest_gain_when_widened` can name a combination arm, which "
                          "is not a dial anyone could turn on its own. The single-dial "
                          "winner is reported separately, and it is the number quoted in "
                          "the headline.",
            "answer":
                "Two different questions have two different answers, and conflating "
                "them is the easy mistake. The layer that PROVIDES the gamut is the "
                "iridophore stack: freeze it and 88% of the chromaticity area goes. "
                "The layer that LIMITS the gamut is not the same one. Widening the "
                "stack's tuning range beyond the measured 425-675 nm gains 1%, because "
                "that range already spans the visually useful band. What gains is "
                "refractive-index contrast (n_H 1.405 -> 1.44, the measured maximum: "
                "+68%) and chromatophore retraction (area ratio 2.55 -> 50, i.e. a "
                "retracted state that gets out of the way: +61%). Both are measured "
                "quantities that the animal is already at the edge of, so neither is a "
                "free lunch; the engineering reading is that a synthetic version should "
                "spend its effort on index contrast in the reflector and on a pigment "
                "actuator with a genuinely transparent off-state, and not on a wider "
                "tunable range.",
        },
        "controls": controls,
        "limitations": [
            "The illuminant is CIE D65, not a measured underwater downwelling spectrum. "
            "We did not find one we could read, and did not invent one. Seawater "
            "attenuates red strongly with depth, so the real gamut of a cephalopod in "
            "its own light field is smaller than this and shifted blue-green; we do not "
            "estimate by how much.",
            "The observer is the CIE 1931 2-degree HUMAN observer. Cephalopods are "
            "colour-blind (one visual pigment in the species studied) and the predators "
            "they hide from are fish, often tetrachromatic. A gamut area in human u'v' "
            "is a convenient common currency, not the quantity that matters to either "
            "animal.",
            "No measured absorption spectrum for a cephalopod ommochrome was found, so "
            "all nine pigment numbers (three edges, three widths, three optical "
            "densities) are assumed. The ORDER of the classes and the long-pass SHAPE "
            "are supported by Reiter et al. 2018's measured transmission spectra and "
            "xanthommatin localisation; the positions are not.",
            "The stack is computed at normal incidence only. Real iridophore reflectance "
            "is strongly angle-dependent and the lamellae are not parallel to the skin "
            "surface, so an off-axis observer sees a different colour. This model cannot "
            "say anything about the angular gamut.",
            "Scattering is ignored. The leucophore is a diffuse backing with a single "
            "number; pigment granules are treated as a pure absorber with no surface "
            "reflection, so the pigment can only darken and filter, never add a "
            "specular highlight.",
            "The one-bounce addition of the backing beneath the stack is an "
            "approximation; a full multiple-scattering treatment would raise the "
            "reflectance of the leucophore-on states somewhat.",
            "The Bragg peak is placed by holding the live-cell thickness RATIO constant "
            "and scaling the pair. The source reports both thicknesses correlating with "
            "peak wavelength, which is consistent with that but does not establish it; "
            "the animal may move the two thicknesses independently, which would make "
            "the reachable set larger than modelled.",
            "Iridophores and chromatophores run at timescales two orders of magnitude "
            "apart (chromatophore expansion ~0.2 s; neurally evoked iridophore colour "
            "shift 17 s and brightness 32 s, Wardill et al. 2012). This model is "
            "steady-state and says nothing about what gamut is reachable QUICKLY.",
        ],
        "figures": [
            {"file": "figures/gamut-space.png"},
            {"file": "figures/gamut-limiting-layer.png"},
        ],
    }
    return out, res, locus, pig_drop, swp


if __name__ == "__main__":
    out, res, locus, pig_drop, swp = build()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    figures(res, locus, pig_drop, swp, os.path.join(root, "figures"))
    write_result(os.path.join(root, "optical-gamut.json"), out)
    print("wrote optical-gamut.json")
    print(out["headline"])
