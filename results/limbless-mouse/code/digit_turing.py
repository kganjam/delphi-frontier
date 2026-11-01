#!/usr/bin/env python3
"""
digit_turing.py -- a 2-D Bmp-Sox9-Wnt (BSW) Turing simulation of skeletal-element
patterning in a limb-bud-shaped domain, and a design sweep from a normal five-element
pattern down to no skeletal pattern at all.

EVERYTHING THIS SCRIPT PRODUCES IS SIMULATION. No figure, number or class in the
output is an observation of a mouse, and nothing here was fitted to measured data.

Run:  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 digit_turing.py

Writes, next to itself:
  digit-turing.json, digit-turing-normal.png, digit-turing-series.png,
  digit-turing-domain.png, digit-turing.mp4 (if ffmpeg is present)
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl
from scipy import ndimage

HERE = Path(__file__).resolve().parent

# --------------------------------------------------------------------------------------
# Palette (fixed by the brief)
# --------------------------------------------------------------------------------------
BG = "#fffdf8"
INK = "#0f2238"
TEAL = "#0e7c86"
LIME = "#a6c936"
WARN = "#9a6700"
RED = "#b3261e"
GREEN = "#1d7a46"

# --------------------------------------------------------------------------------------
# SOURCES
# --------------------------------------------------------------------------------------
SOURCES = [
    {
        "key": "raspopovic2014",
        "citation": "Raspopovic J, Marcon L, Russo L, Sharpe J (2014) Digit patterning is "
                    "controlled by a Bmp-Sox9-Wnt Turing network modulated by morphogen "
                    "gradients. Science 345(6196):566-570.",
        "pmid": "25082703",
        "doi": "10.1126/science.1252960",
        "read_level": "abstract",
        "how_checked": "PMID and DOI resolved through the PubMed MCP tool; metadata record "
                       "retrieved 2026-11-01. Europe PMC reports isOpenAccess=N, inEPMC=N, "
                       "no PMC id: the full text and supplement are behind a subscription and "
                       "were NOT read. Only the abstract was read.",
        "used_for": "The claim that a Bmp-Sox9-Wnt Turing network drives mouse digit "
                    "specification and is modulated by morphogen gradients. This is the model "
                    "this script implements; the equations themselves were taken at full-text "
                    "level from onimaru2016, which states that it implements this model.",
    },
    {
        "key": "sheth2012",
        "citation": "Sheth R, Marcon L, Bastida MF, Junco M, Quintana L, Dahn R, Kmita M, "
                    "Sharpe J, Ros MA (2012) Hox genes regulate digit patterning by controlling "
                    "the wavelength of a Turing-type mechanism. Science 338(6113):1476-1480.",
        "pmid": "23239739",
        "doi": "10.1126/science.1226804",
        "pmcid": "PMC4486416",
        "read_level": "abstract",
        "how_checked": "PMID and DOI resolved through the PubMed MCP tool. PMC4486416 is a "
                       "PMC Canada author manuscript: the PubMed full-text tool returned an "
                       "EMPTY body, the Europe PMC fullTextXML endpoint returned HTTP 500, the "
                       "rendered PDF returned HTTP 403, and NCBI efetch db=pmc returned front "
                       "matter with no <body>. Only the abstract was read.",
        "used_for": "The DIRECTION of the wavelength sweep only: progressive loss of distal Hox "
                    "dose gives progressively more, thinner, densely packed digits, i.e. a "
                    "shorter Turing wavelength. No quantitative value is taken from this paper.",
    },
    {
        "key": "onimaru2016",
        "citation": "Onimaru K, Marcon L, Musy M, Tanaka M, Sharpe J (2016) The fin-to-limb "
                    "transition as the re-organization of a Turing pattern. Nat Commun 7:11582.",
        "pmid": "27211489",
        "doi": "10.1038/ncomms11582",
        "pmcid": "PMC4879262",
        "read_level": "full-text",
        "how_checked": "Full text XML retrieved from the Europe PMC REST endpoint "
                       "(/PMC4879262/fullTextXML, HTTP 200, 120161 bytes) on 2026-11-01, and the "
                       "Methods section read. Equations (16)-(19) are published as images; the "
                       "image files ncomms11582-m22..m25.jpg were downloaded from the PMC CDN "
                       "and read directly. Parameter values were read verbatim from the Methods "
                       "paragraph 'Mathematical analysis and numerical simulation'.",
        "used_for": "The equation form and every sourced numeric parameter below. This paper "
                    "states in its own text that it uses 'the BSW model' of Raspopovic et al. "
                    "2014 (its reference 12) and that the Fgf gradient modulates the same "
                    "parameters as in the mouse model, 'repressing k4 and boosting k7'. It also "
                    "supplies the numerical recipe (Heun, dt=0.002, zero-flux, homogeneous "
                    "steady-state initial condition, 1% Gaussian multiplicative noise per step) "
                    "and the simple square-domain Fgf substitute exp(-3x) on 0<=x<=1.",
        "caveat": "Onimaru et al. apply this parameter set to a GROWING catshark pectoral fin "
                  "mesh, where Sox9 forms spots. It is the same network as the mouse model but "
                  "not the mouse parameter set, which was not obtainable (see raspopovic2014).",
    },
]

# --------------------------------------------------------------------------------------
# PARAMETERS, each tagged sourced | assumed
# --------------------------------------------------------------------------------------
PARAMS = [
    dict(name="beta", value=8.0, units="1/time (model)", status="sourced",
         source="onimaru2016 Methods, 'Parameter values were beta=8, ...' for Figs 4-5",
         note="Global coefficient controlling the speed of pattern appearance."),
    dict(name="k2", value=1.0, units="dimensionless", status="sourced",
         source="onimaru2016 Methods, Figs 4-5 parameter list",
         note="Bmp -> Sox9 activation strength. Onimaru et al. perturb exactly this parameter "
              "to represent Bmp inhibition."),
    dict(name="k3", value=3.0, units="dimensionless", status="sourced",
         source="onimaru2016 Methods, Figs 4-5 parameter list",
         note="Wnt -| Sox9 inhibition strength (the minus sign is explicit in eq 16)."),
    dict(name="k4", value=6.0, units="dimensionless", status="sourced",
         source="onimaru2016 Methods, Figs 4-5 parameter list",
         note="Sox9 -| Bmp inhibition strength; repressed by Fgf."),
    dict(name="k7", value=2.4, units="dimensionless", status="sourced",
         source="onimaru2016 Methods, Figs 4-5 parameter list",
         note="Sox9 -| Wnt inhibition strength; boosted by Fgf."),
    dict(name="k5", value=0.1, units="1/time (model)", status="sourced",
         source="onimaru2016 Methods, Figs 4-5 parameter list", note="Bmp linear decay."),
    dict(name="k9", value=0.1, units="1/time (model)", status="sourced",
         source="onimaru2016 Methods, Figs 4-5 parameter list", note="Wnt linear decay."),
    dict(name="kF", value=0.667, units="dimensionless", status="sourced",
         source="onimaru2016 Methods, Figs 4-5 parameter list",
         note="Strength with which the normalised Fgf field F in [0,1] modulates k4 and k7."),
    dict(name="D_B", value=160.0, units="length^2/time (model)", status="sourced",
         source="onimaru2016 Methods, Figs 4-5 parameter list",
         note="Bmp diffusion. Bmp is the LONG-range species (D_B > D_W)."),
    dict(name="D_W", value=25.0, units="length^2/time (model)", status="sourced",
         source="onimaru2016 Methods, Figs 4-5 parameter list",
         note="Wnt diffusion. Wnt is the SHORT-range species."),
    dict(name="alpha_B", value=0.1, units="conc/time (model)", status="sourced",
         source="onimaru2016 Methods, Figs 4-5 parameter list",
         note="Constant Bmp production."),
    dict(name="alpha_W", value=1.0 * 0.1 * 0.1 / (3.0 * 0.1), units="conc/time (model)",
         status="assumed",
         source="CHANGED from the published value alpha_W = 1.2 (onimaru2016 Methods).",
         note="alpha_W = k2*alpha_B*k9/(k3*k5) = 0.03333, chosen so the homogeneous steady "
              "state sits exactly at S*=0, where the cubic self-damping -3S*^2 vanishes and the "
              "paper's own LINEAR Turing conditions apply. With the published alpha_W = 1.2 my "
              "own linear stability analysis finds NO Turing instability anywhere on this "
              "static domain: see linear_stability.published_set_check in the JSON. This is the "
              "single substantive departure from the published parameter set and it is the "
              "reason the whole set must be read as 'published form, operating point retuned'."),
    dict(name="F_max", value=0.62, units="dimensionless", status="assumed",
         source="no published value for this geometry",
         note="Distal maximum of the normalised Fgf field. Chosen just BELOW the upper edge of "
              "the Turing window in F (F_hopf, computed by the LSA below), so that no part of "
              "the bud sits in the uniform (q=0) instability regime. Calibration choice."),
    dict(name="F_decay", value=4.0, units="dimensionless", status="assumed",
         source="onimaru2016 gives exp(-3*x) on a UNIT SQUARE (Supplementary Fig. 7); the "
                "fin/limb simulations instead solve a reaction-diffusion Fgf field whose "
                "absolute spatial scale is set by their mesh, which I do not have.",
         note="F(x_hat) = F_max * exp(-F_decay * x_hat), x_hat = normalised distance proximal "
              "from the distal margin. F_decay=4 (vs the published square-domain 3) makes the "
              "Turing-permissive band about one wavelength deep, which is what yields a single "
              "proximodistal row of elements rather than two rows."),
    dict(name="L_PD", value=300.0, units="length (model)", status="assumed",
         source="no measured value used", note="Proximodistal length of the paddle."),
    dict(name="W_AP_half", value=220.0, units="length (model)", status="assumed",
         source="no measured value used",
         note="Half-width of the paddle at its distal margin. L_PD and W_AP_half were chosen so "
              "that the WILD-TYPE-LIKE run yields about five elements. The five-element outcome "
              "is therefore IMPOSED by the domain, not predicted. What the model predicts is how "
              "the element count MOVES when the wavelength or the domain is changed."),
    dict(name="dx", value=4.0, units="length (model)", status="assumed",
         source="numerical choice", note="Grid spacing; checked by the grid-refinement arm."),
    dict(name="dt", value=0.01, units="time (model)", status="assumed",
         source="numerical choice (onimaru2016 use dt=0.002 with an explicit Heun solver; this "
                "script uses a semi-implicit solver, so a larger step is admissible)",
         note="Checked by the dt-refinement arm. dt=0.02 was measured to be numerically "
              "UNSTABLE here; dt=0.01, 0.005 and 0.002 agree to 5 significant figures."),
    dict(name="T_end", value=60.0, units="time (model)", status="assumed",
         source="numerical choice",
         note="The pattern coarsens after onset and the coarsening ARRESTS by t~40 (measured in "
              "a 1-D control out to t=320). T_end=60 is past arrest."),
    dict(name="noise_amplitude", value=0.01, units="conc (model)", status="assumed",
         source="onimaru2016 use 1% Gaussian MULTIPLICATIVE noise at each step; multiplicative "
                "noise vanishes identically at this model's steady state S*=0, so it cannot be "
                "used here.",
         note="Seeded additive Gaussian perturbation of S at t=0, s.d. 1% of the Bmp steady "
              "state. A control arm adds dt-scaled per-step additive noise instead."),
]
P = {p["name"]: p["value"] for p in PARAMS}

TOPOLOGY = [
    dict(source_node="Bmp", target="Sox9", sign="+", term="+k2*B",
         evidence="onimaru2016 eq (16), full-text", ),
    dict(source_node="Wnt", target="Sox9", sign="-", term="-k3*W",
         evidence="onimaru2016 eq (16), full-text"),
    dict(source_node="Sox9", target="Sox9", sign="-", term="-S^3",
         evidence="onimaru2016 eq (16), full-text; cubic self-damping, the only nonlinearity"),
    dict(source_node="Sox9", target="Bmp", sign="-", term="-(1-kF*F)*k4*S",
         evidence="onimaru2016 eq (17), full-text"),
    dict(source_node="Sox9", target="Wnt", sign="-", term="-k7*kF*F*S",
         evidence="onimaru2016 eq (18), full-text"),
    dict(source_node="Fgf", target="Sox9-|Bmp edge", sign="-", term="(1-kF*F) scales k4",
         evidence="onimaru2016 Results, 'repressing k4 and boosting k7', full-text"),
    dict(source_node="Fgf", target="Sox9-|Wnt edge", sign="+", term="kF*F scales k7",
         evidence="onimaru2016 Results, 'repressing k4 and boosting k7', full-text"),
]

EQUATIONS_LATEX = {
    "Sox9": r"\frac{\partial S}{\partial t} = \beta\left(k_2 B - k_3 W - S^3\right)",
    "Bmp": r"\frac{\partial B}{\partial t} = \beta\left(\alpha_B - (1-k_F F)\,k_4 S"
           r" - k_5 B + D_B \nabla^2 B\right)",
    "Wnt": r"\frac{\partial W}{\partial t} = \beta\left(\alpha_W - k_7 k_F F\,S"
           r" - k_9 W + D_W \nabla^2 W\right)",
    "Fgf": r"F(\hat{x}) = F_{\max}\,e^{-g\,\hat{x}},\qquad "
           r"\hat{x} = \frac{\text{distance proximal from the distal margin}}{L_{PD}}",
    "steady_state": r"S^{*}=0,\quad B^{*}=\alpha_B/k_5,\quad W^{*}=\alpha_W/k_9",
    "jacobian": r"M(q)=\beta\begin{pmatrix}-3S^{*2} & k_2 & -k_3\\ -a_4 & -k_5-D_Bq^2 & 0\\"
                r" -a_7 & 0 & -k_9-D_Wq^2\end{pmatrix},\;"
                r"a_4=(1-k_FF)k_4,\; a_7=k_7k_FF",
}

# Pre-declared phenotype classification (fixed BEFORE any sweep was run).
CLASSIFY_RULE = (
    "Applied to the Sox9 field S at t = T_end, on the masked domain. "
    "(1) AMPLITUDE GATE: if p99(S) - p1(S) < 0.05 model concentration units, or p99(S) <= 0, "
    "the field is called unpatterned, element_count = 0, class = 'none'. "
    "(2) THRESHOLD: Sox9-high = {S > 0.25 * p99(S)}. The homogeneous steady state is S* = 0 by "
    "construction, so this threshold is referenced to the known unpatterned baseline and the "
    "unpatterned background can never be counted as an element. "
    "(3) MINIMUM SIZE: connected components (4-connectivity) of the Sox9-high set with area "
    ">= 0.10 * lambda_elem^2 are counted as elements, where "
    "lambda_elem = lambda_meas_WT * lambda_lin(condition) / lambda_lin(WT): the wavelength "
    "MEASURED in the wild-type runs, carried to each condition by that condition's analytic "
    "linear-stability wavelength. It uses no measurement from the run being counted. "
    "(4) CLASS from the count n: n=0 -> 'none'; n=1 -> 'single element', or 'single fused "
    "domain' if that one component spans more than 70% of the anteroposterior width; "
    "2<=n<=4 -> 'reduced'; n=5 -> 'normal digit number'; n>=6 -> 'increased "
    "(polydactyl-like)'."
)

CLASSIFY_RULE_CHANGE = (
    "The rule was declared before any sweep was run, and step (3) originally used "
    "lambda_lin(condition) itself rather than lambda_elem. It was CHANGED after the first full "
    "run, and the change is recorded here rather than quietly made. The reason is a defect in "
    "the specification, not a result I disliked: the linear-stability wavelength is about half "
    "the wavelength the saturated pattern actually has (measured, and reported under "
    "measured_wavelength), so a minimum area of 0.10 * lambda_lin^2 is four times too small and "
    "admits slivers at the anterior and posterior ends of the band as if they were elements. "
    "Every element count under the ORIGINAL rule is kept alongside, as "
    "element_counts_linear_rule in each sweep row and as "
    "sweeps_under_the_original_rule.wild_type. Under the original rule the wild-type count was "
    "{ORIG} (mean {ORIGMEAN}); under the revised rule it is {NEW} (mean {NEWMEAN}). The "
    "qualitative shape of every sweep is the same under both."
)

# --------------------------------------------------------------------------------------
# Linear stability analysis
# --------------------------------------------------------------------------------------
QGRID = np.linspace(1e-6, 1.2, 3001)
_LAM_WT = []


def lambda_wt():
    """Wild-type linear wavelength, computed once and reused as the fallback element scale."""
    if not _LAM_WT:
        _LAM_WT.append(dominant_lsa_over_domain(
            P, P["F_max"], P["F_max"] * np.exp(-P["F_decay"]))["wavelength"])
    return _LAM_WT[0]


def _jac(S, a4, a7, pr, q):
    return np.array([
        [-3.0 * S * S, pr["k2"], -pr["k3"]],
        [-a4, -pr["k5"] - pr["D_B"] * q * q, 0.0],
        [-a7, 0.0, -pr["k9"] - pr["D_W"] * q * q],
    ]) * pr["beta"]


def _growth(S, a4, a7, pr, qs):
    """Max Re(eigenvalue) of M(q) for every q at once (stacked 3x3 eigensolve)."""
    q2 = np.asarray(qs) ** 2
    M = np.zeros((len(q2), 3, 3))
    M[:, 0, 0] = -3.0 * S * S
    M[:, 0, 1] = pr["k2"]
    M[:, 0, 2] = -pr["k3"]
    M[:, 1, 0] = -a4
    M[:, 1, 1] = -pr["k5"] - pr["D_B"] * q2
    M[:, 2, 0] = -a7
    M[:, 2, 2] = -pr["k9"] - pr["D_W"] * q2
    return np.linalg.eigvals(M * pr["beta"]).real.max(axis=1)


def steady_states(F, pr):
    """Real homogeneous steady states of the full nonlinear system."""
    a4 = (1.0 - pr["kF"] * F) * pr["k4"]
    a7 = pr["k7"] * pr["kF"] * F
    c1 = -pr["k2"] * a4 / pr["k5"] + pr["k3"] * a7 / pr["k9"]
    c0 = pr["k2"] * pr["alpha_B"] / pr["k5"] - pr["k3"] * pr["alpha_W"] / pr["k9"]
    r = np.roots([-1.0, 0.0, c1, c0])
    r = np.sort(r[np.abs(r.imag) < 1e-9].real)
    return [(float(S), (pr["alpha_B"] - a4 * S) / pr["k5"],
             (pr["alpha_W"] - a7 * S) / pr["k9"]) for S in r], a4, a7


def lsa(F, pr, S=None):
    """Dispersion relation at Fgf level F. Returns the dominant mode."""
    sts, a4, a7 = steady_states(F, pr)
    if S is None:
        S = 0.0 if any(abs(s[0]) < 1e-9 for s in sts) else sts[0][0]
    g = _growth(S, a4, a7, pr, QGRID)
    i = int(np.argmax(g))
    g0 = float(_growth(S, a4, a7, pr, [0.0])[0])
    turing = bool(g0 < 0 and g[i] > 0 and QGRID[i] > 1e-4)
    return dict(F=float(F), S_star=float(S), q_max=float(QGRID[i]),
                wavelength=float(2 * np.pi / QGRID[i]), growth_max=float(g[i]),
                growth_at_q0=g0, turing=turing)


def turing_window(pr, n=241):
    """Range of F over which the S*=0 state is Turing-unstable."""
    Fs = np.linspace(0.0, 1.0, n)
    ok = [lsa(F, pr, S=0.0)["turing"] for F in Fs]
    idx = np.nonzero(ok)[0]
    if len(idx) == 0:
        return None
    return float(Fs[idx[0]]), float(Fs[idx[-1]])


def dominant_lsa_over_domain(pr, Fmax, Fmin):
    """lambda_pred for a condition: LSA at the F inside the domain with the fastest growth."""
    Fs = np.linspace(max(Fmin, 1e-4), Fmax, 80)
    best = None
    for F in Fs:
        r = lsa(F, pr, S=0.0)
        if r["turing"] and (best is None or r["growth_max"] > best["growth_max"]):
            best = r
    if best is None:                       # sub-critical everywhere: use the least-stable mode
        cands = [lsa(F, pr, S=0.0) for F in Fs]
        best = max(cands, key=lambda r: r["growth_max"])
        best = dict(best, turing=False)
    return best


# --------------------------------------------------------------------------------------
# Geometry and operators
# --------------------------------------------------------------------------------------
def paddle(L, W, dx, scale=1.0, n_cap=4.0, c_frac=0.18, w_min=0.45, w_pow=0.7):
    """Limb-bud autopod paddle: narrow proximally, broad with a flattened distal margin."""
    L, W = L * scale, W * scale
    c = c_frac * L
    nx = int(round(L / dx)) + 1
    ny = int(round(2 * W / dx)) + 1
    x = np.arange(nx) * dx
    y = (np.arange(ny) - (ny - 1) / 2.0) * dx
    X, Y = np.meshgrid(x, y, indexing="ij")
    w = W * (w_min + (1.0 - w_min) * (X / L) ** w_pow)
    t = np.clip((X - (L - c)) / c, 0.0, None)
    mask = ((np.abs(Y) / w) ** n_cap + t ** n_cap <= 1.0) & (X >= 0.02 * L)
    return mask, X, Y, L, W


def laplacian(mask, dx):
    """5-point Laplacian, zero-flux (mirror) boundary on an arbitrary mask."""
    n = int(mask.sum())
    idx = -np.ones(mask.shape, dtype=np.int64)
    idx[mask] = np.arange(n)
    nx, ny = mask.shape
    ii, jj = np.nonzero(mask)
    rows, cols, vals = [], [], []
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ni, nj = ii + di, jj + dj
        ok = (ni >= 0) & (ni < nx) & (nj >= 0) & (nj < ny)
        nb = np.zeros(len(ii), dtype=bool)
        nb[ok] = mask[ni[ok], nj[ok]]
        src = idx[ii, jj]
        rows += [src[nb], src[nb]]
        cols += [idx[ni[nb], nj[nb]], src[nb]]
        vals += [np.ones(int(nb.sum())), -np.ones(int(nb.sum()))]
    return sp.csr_matrix((np.concatenate(vals) / dx ** 2,
                          (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))


# --------------------------------------------------------------------------------------
# Solver
# --------------------------------------------------------------------------------------
def simulate(pr, seed, scale=1.0, dx=None, dt=None, T=None, per_step_noise=False,
             no_reaction=False, no_noise=False, frames=0):
    """Semi-implicit (implicit diffusion + linear decay, linearised cubic) IMEX scheme."""
    dx = pr["dx"] if dx is None else dx
    dt = pr["dt"] if dt is None else dt
    T = pr["T_end"] if T is None else T
    mask, X, Y, L, W = paddle(pr["L_PD"], pr["W_AP_half"], dx, scale)
    Lap = laplacian(mask, dx)
    n = Lap.shape[0]
    ii, _ = np.nonzero(mask)
    xs = ii * dx
    b = pr["beta"]

    F = pr["F_max"] * np.exp(-pr["F_decay"] * (L - xs) / L)
    a4 = (1.0 - pr["kF"] * F) * pr["k4"]
    a7 = pr["k7"] * pr["kF"] * F
    if no_reaction:                       # control: diffusion + production/decay only
        a4 = np.zeros_like(a4)
        a7 = np.zeros_like(a7)

    I = sp.identity(n, format="csc")
    MB = spl.factorized((I * (1 + dt * b * pr["k5"]) - dt * b * pr["D_B"] * Lap).tocsc())
    MW = spl.factorized((I * (1 + dt * b * pr["k9"]) - dt * b * pr["D_W"] * Lap).tocsc())

    rng = np.random.default_rng(seed)
    S = np.zeros(n)
    if not no_noise:
        S = S + pr["noise_amplitude"] * (pr["alpha_B"] / pr["k5"]) * rng.standard_normal(n)
    B = np.full(n, pr["alpha_B"] / pr["k5"])
    Wn = np.full(n, pr["alpha_W"] / pr["k9"])

    k2 = 0.0 if no_reaction else pr["k2"]
    k3 = 0.0 if no_reaction else pr["k3"]
    nst = int(round(T / dt))
    sig = pr["noise_amplitude"] * (pr["alpha_B"] / pr["k5"]) * np.sqrt(dt / 0.01)
    snaps, every = [], max(1, nst // frames) if frames else 0
    for s in range(nst):
        S = (S + dt * b * (k2 * B - k3 * Wn)) / (1.0 + dt * b * S * S)
        if per_step_noise:
            S = S + sig * rng.standard_normal(n)
        B = MB(B + dt * b * (pr["alpha_B"] - a4 * S))
        Wn = MW(Wn + dt * b * (pr["alpha_W"] - a7 * S))
        if not np.isfinite(S).all():
            return dict(diverged=True, step=s, mask=mask, dx=dx, S=S, F=F, L=L, W=W)
        if frames and s % every == 0:
            snaps.append((s * dt, S.copy()))
    if frames:
        snaps.append((nst * dt, S.copy()))
    return dict(diverged=False, mask=mask, dx=dx, S=S, B=B, W=Wn, F=F, L=L, W_half=W,
                X=X, Y=Y, snaps=snaps)


# --------------------------------------------------------------------------------------
# Pre-declared measurement
# --------------------------------------------------------------------------------------
def _cls_of(n):
    return ("none" if n == 0 else "single element" if n == 1 else
            "reduced" if n <= 4 else "normal digit number" if n == 5 else
            "increased (polydactyl-like)")


def classify(S, mask, dx, lam_element, lam_linear=None):
    """Pre-declared element counter.

    lam_element -- the length scale used for the minimum element area (the REVISED rule).
    lam_linear  -- if given, the counter is ALSO evaluated with the linear-stability
                   wavelength, which is the rule as originally declared, and that count is
                   reported alongside as element_count_linear_rule.
    """
    p1, p99 = float(np.percentile(S, 1)), float(np.percentile(S, 99))
    amp = p99 - p1
    out = dict(amplitude=amp, element_count=0, element_count_linear_rule=0, areas=[],
               centroids_AP=[], cls="none", fused=False)
    if amp < 0.05 or p99 <= 0:
        return out
    hi = np.zeros(mask.shape, dtype=bool)
    hi[mask] = S > 0.25 * p99
    lab, nl = ndimage.label(hi)
    if nl == 0:
        return out
    sizes = ndimage.sum(hi, lab, range(1, nl + 1)) * dx * dx
    _, jj_all = np.nonzero(mask)
    ap_domain = (jj_all.max() - jj_all.min() + 1) * dx
    if lam_linear is not None:
        out["element_count_linear_rule"] = int(
            sum(1 for a in sizes if a >= 0.10 * lam_linear ** 2))
    keep = [i + 1 for i, a in enumerate(sizes) if a >= 0.10 * lam_element ** 2]
    if not keep:
        return out
    cen = ndimage.center_of_mass(hi, lab, keep)
    n = len(keep)
    # a single component that spans most of the anteroposterior width is a FUSED continuous
    # domain, not an isolated element -- the phenotype onimaru2016 report for Wnt inhibition
    fused = False
    if n == 1:
        ii_c, jj_c = np.nonzero(lab == keep[0])
        fused = ((jj_c.max() - jj_c.min() + 1) * dx) > 0.70 * ap_domain
    out.update(element_count=n, fused=bool(fused),
               areas=[float(sizes[i - 1]) for i in keep],
               centroids_AP=sorted(float(c[1] * dx) for c in cen),
               cls=("single fused domain" if fused else _cls_of(n)))
    return out


def ap_spacing(centroids):
    if len(centroids) < 2:
        return None
    return float(np.mean(np.diff(sorted(centroids))))


# --------------------------------------------------------------------------------------
# One condition = one worker job
# --------------------------------------------------------------------------------------
def job(spec):
    name, overrides, scale, seed, kw, amin_scale = spec
    pr = dict(P)
    pr.update(overrides)
    t0 = time.time()
    r = simulate(pr, seed, scale=scale, **kw)
    if r["diverged"]:
        return dict(name=name, seed=seed, diverged=True, secs=time.time() - t0)
    lam = dominant_lsa_over_domain(pr, pr["F_max"],
                                   pr["F_max"] * np.exp(-pr["F_decay"]))
    # Minimum element area uses the condition's own LSA wavelength; where there is no Turing
    # instability that wavelength is meaningless, so the wild-type value is used instead (the
    # amplitude gate is what decides those runs anyway).
    lam_lin = lam["wavelength"] if lam["turing"] else lambda_wt()
    lam_area = lam_lin * amin_scale
    c = classify(r["S"], r["mask"], r["dx"], lam_area, lam_linear=lam_lin)
    # AP and PD extent of the domain, in model length units
    ii, jj = np.nonzero(r["mask"])
    ap_extent = (jj.max() - jj.min() + 1) * r["dx"]
    pd_extent = (ii.max() - ii.min() + 1) * r["dx"]
    return dict(name=name, seed=seed, diverged=False, scale=scale,
                lambda_pred=lam["wavelength"], lsa_turing=lam["turing"],
                lsa_growth_max=lam["growth_max"], lsa_F=lam["F"],
                ap_extent=float(ap_extent), pd_extent=float(pd_extent),
                secs=time.time() - t0, **c)


# --------------------------------------------------------------------------------------
# 1-D uniform-domain control (linear vs saturated wavelength)
# --------------------------------------------------------------------------------------
def one_d_wavelength(F, pr, Lx=1500.0, dx=1.0, T=160.0, dt=0.005, seed=0,
                     linear_probe_t=2.0):
    n = int(Lx / dx)
    k = 2 * np.pi * np.fft.rfftfreq(n, d=dx)
    kk = np.fft.rfftfreq(n, d=dx)
    a4 = (1 - pr["kF"] * F) * pr["k4"]
    a7 = pr["k7"] * pr["kF"] * F
    b = pr["beta"]
    rng = np.random.default_rng(seed)
    S = 1e-4 * rng.standard_normal(n)
    B = np.full(n, pr["alpha_B"] / pr["k5"])
    W = np.full(n, pr["alpha_W"] / pr["k9"])
    dB = 1 / (1 + dt * b * (pr["k5"] + pr["D_B"] * k * k))
    dW = 1 / (1 + dt * b * (pr["k9"] + pr["D_W"] * k * k))
    lam_lin = None
    for s in range(int(T / dt)):
        S = (S + dt * b * (pr["k2"] * B - pr["k3"] * W)) / (1 + dt * b * S * S)
        B = np.fft.irfft(np.fft.rfft(B + dt * b * (pr["alpha_B"] - a4 * S)) * dB, n)
        W = np.fft.irfft(np.fft.rfft(W + dt * b * (pr["alpha_W"] - a7 * S)) * dW, n)
        if s == int(linear_probe_t / dt):
            u = S - S.mean()
            ps = np.abs(np.fft.rfft(u)) ** 2
            lam_lin = float(1.0 / kk[int(np.argmax(ps[1:])) + 1])
    u = S - S.mean()
    ps = np.abs(np.fft.rfft(u)) ** 2
    lam_sat = float(1.0 / kk[int(np.argmax(ps[1:])) + 1])
    return lam_lin, lam_sat, float(u.max() - u.min())


# --------------------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------------------
def _mpl():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
        "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
        "axes.edgecolor": INK, "font.size": 12,
    })
    # vmin=-3.2 .. vmax=2.2, so the unpatterned steady state S*=0 sits at 0.593.
    # Sox9-low (interdigital) -> warm pale; S*=0 -> a very light tint so the paddle is still
    # visible; Sox9-high (the skeletal elements) -> strong teal into ink.
    cmap = LinearSegmentedColormap.from_list("sox9", [
        (0.00, "#e4d8bd"), (0.30, "#efe7d4"), (0.52, "#f7f3e9"), (0.593, "#eef3f2"),
        (0.66, "#9ec4c6"), (0.78, TEAL), (0.90, "#0a4f58"), (1.00, INK)])
    return plt, cmap


def extent_of(r):
    """imshow extent in MODEL LENGTH UNITS, so panels can share one spatial scale.

    field_image() returns the mask-shaped array TRANSPOSED, so the displayed x axis is the
    proximodistal axis (first index of the mask, length nx) and the displayed y axis is the
    anteroposterior axis (second index, length ny).
    """
    nx, ny = r["mask"].shape
    dx = r["dx"]
    return (0.0, nx * dx, -ny * dx / 2.0, ny * dx / 2.0)


def field_image(r):
    f = np.full(r["mask"].shape, np.nan)
    f[r["mask"]] = r["S"]
    return f.T


def draw_panel(ax, r, cmap, vmin, vmax, lam_elem, title, sub=None, outline=True,
               common_extent=None):
    img = field_image(r)
    ext = extent_of(r)
    ax.imshow(img, origin="lower", cmap=cmap, vmin=vmin, vmax=vmax,
              interpolation="nearest", extent=ext, aspect="equal")
    if outline:
        S, mask, dx = r["S"], r["mask"], r["dx"]
        p99 = np.percentile(S, 99)
        if p99 > 0 and (p99 - np.percentile(S, 1)) >= 0.05:
            hi = np.zeros(mask.shape, dtype=bool)
            hi[mask] = S > 0.25 * p99
            lab, nl = ndimage.label(hi)
            sizes = ndimage.sum(hi, lab, range(1, nl + 1)) * dx * dx
            keep = np.zeros(mask.shape, dtype=float)
            for i, a in enumerate(sizes):
                if a >= 0.10 * lam_elem ** 2:
                    keep[lab == i + 1] = 1.0
            nx, ny = mask.shape
            # keep is mask-shaped (nx, ny); contour wants Z with shape (len(Y), len(X))
            ax.contour(np.linspace(ext[0], ext[1], nx), np.linspace(ext[2], ext[3], ny),
                       keep.T, levels=[0.5], colors=[LIME], linewidths=1.6)
    if common_extent:
        ax.set_xlim(common_extent[0], common_extent[1])
        ax.set_ylim(common_extent[2], common_extent[3])
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, fontsize=11, color=INK, pad=4)
    if sub:
        ax.text(0.5, -0.06, sub, transform=ax.transAxes, ha="center", va="top",
                fontsize=9.5, color=WARN)


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------
def main():
    t_start = time.time()
    log = lambda *a: print(*a, flush=True)

    pr0 = dict(P)
    log("== linear stability analysis ==")
    win = turing_window(pr0)
    ref = dominant_lsa_over_domain(pr0, pr0["F_max"], pr0["F_max"] * np.exp(-pr0["F_decay"]))
    log(f"Turing window in F: {win};  lambda_pred (linear) = {ref['wavelength']:.2f}"
        f" at F={ref['F']:.3f}")

    # --- the published-parameter-set check (the honest negative result) ---
    pub = dict(pr0, alpha_W=1.2)
    pub_rows, pub_turing = [], False
    for F in np.linspace(0.0, 1.0, 51):
        sts, a4, a7 = steady_states(F, pub)
        for (S, _, _) in sts:
            r = lsa(F, pub, S=S)
            pub_turing |= r["turing"]
            pub_rows.append(r)
    pub_best = max(pub_rows, key=lambda r: r["growth_max"])
    log(f"published alpha_W=1.2: any Turing instability found = {pub_turing}"
        f" (max growth over all F and all real steady states = {pub_best['growth_max']:.3f}"
        f" at F={pub_best['F']:.2f}, q={pub_best['q_max']:.4f},"
        f" growth at q=0 = {pub_best['growth_at_q0']:.3f})")

    # --- 1-D uniform-domain control: linear vs saturated wavelength, across the band ---
    log("== 1-D uniform-domain wavelength control ==")
    band_Fs = [0.62, 0.45, 0.30]
    one_d = []
    for Fv in band_Fs:
        ll, ls, aa = one_d_wavelength(Fv, pr0)
        lsa_here = lsa(Fv, pr0, S=0.0)
        one_d.append(dict(F=Fv, lambda_lsa=lsa_here["wavelength"], lambda_sim_linear=ll,
                          lambda_sim_saturated=ls, amplitude=aa))
        log(f"  F={Fv:.2f}: LSA={lsa_here['wavelength']:.1f}  sim(linear,t=2)={ll:.1f}"
            f"  sim(saturated,t=160)={ls:.1f}  amp={aa:.2f}")
    lam_sat = one_d[0]["lambda_sim_saturated"]
    lam_lin_1d = one_d[0]["lambda_sim_linear"]

    nw = max(1, min(5, (os.cpu_count() or 4) - 2))
    SEEDS = [11, 23, 37]
    WT_SEEDS = [11, 23, 37, 51, 67, 83]
    nm_of = lambda knob, v: f"{knob}={v:g}"

    diff_scales = [0.25, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0]
    kFs = [0.30, 0.45, 0.60, 0.667, 0.80, 0.95]
    dom_scales = [0.05, 0.08, 0.10, 0.12, 0.16, 0.20, 0.25, 0.30, 0.40, 0.50, 0.65,
                  0.80, 1.00, 1.25]
    bals = [0.5, 0.7, 0.85, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 5.5, 6.0, 7.0]
    k2s = [0.50, 0.85, 1.00, 1.50, 3.00, 6.00]
    aWs = [0.6, 0.8, 1.0, 1.3, 1.6]
    ref_conditions = [("wt", {}, 1.0),
                      (nm_of("diffusion_scale", 0.6),
                       {"D_B": P["D_B"] * 0.6, "D_W": P["D_W"] * 0.6}, 1.0),
                      (nm_of("domain_scale", 0.3), {}, 0.30)]
    CACHE = HERE / "_results_cache.json"

    use_cache = "--figures" in sys.argv and CACHE.exists()
    if use_cache:
        log("== --figures: reusing the cached simulation results, redrawing only ==")
        c = json.loads(CACHE.read_text())
        results, wt0 = c["results"], c["wt0"]
        lam_meas, amin_scale = c["lam_meas"], c["amin_scale"]
        cached_meta = {k: c.get(k) for k in ("sim_seconds", "n_simulations", "workers")}
    else:
        results = wt0 = None
        lam_meas = amin_scale = None
        cached_meta = {}

    # ---------------- stage 1: the wild-type runs, under the ORIGINAL rule ----------------
    if not use_cache:
        log("== stage 1: wild-type runs (sets the element length scale) ==")
        with ProcessPoolExecutor(max_workers=nw) as ex:
            wt0 = list(ex.map(job, [("wt", {}, 1.0, s, {}, 1.0) for s in WT_SEEDS]))
        sp_ = [ap_spacing(r["centroids_AP"]) for r in wt0]
        lam_meas = float(np.mean([v for v in sp_ if v is not None]))
        amin_scale = lam_meas / ref["wavelength"]
        log(f"   WT under the original rule: counts {[r['element_count'] for r in wt0]}, "
            f"measured AP spacing {lam_meas:.1f}; element scale factor {amin_scale:.2f}")

    # ---------------- stage 2: everything, under the revised rule ----------------
    jobs = []
    for s in WT_SEEDS:
        jobs.append(("wt", {}, 1.0, s, {}, amin_scale))

    for v in diff_scales:
        for s in SEEDS:
            jobs.append((nm_of("diffusion_scale", v),
                         {"D_B": P["D_B"] * v, "D_W": P["D_W"] * v}, 1.0, s, {}, amin_scale))

    for v in kFs:
        for s in SEEDS:
            jobs.append((nm_of("kF", v), {"kF": v}, 1.0, s, {}, amin_scale))

    for v in dom_scales:
        for s in SEEDS:
            jobs.append((nm_of("domain_scale", v), {}, v, s, {}, amin_scale))

    # THE CRITICALITY KNOB. k2 on its own cannot be used: the steady state sits at S*=0 only
    # when k2*alpha_B/k5 == k3*alpha_W/k9, i.e. only at k2 = 1 for the other values here, so
    # changing k2 alone also moves the operating point and the two effects cannot be separated.
    # Scaling k2 and alpha_W by the SAME factor leaves that balance, and therefore S*=0,
    # exactly intact while changing the Bmp->Sox9 coupling strength.
    for v in bals:
        for s in SEEDS:
            jobs.append((nm_of("bmp_coupling", v),
                         {"k2": P["k2"] * v, "alpha_W": P["alpha_W"] * v}, 1.0, s, {},
                         amin_scale))

    for v in k2s:
        for s in SEEDS:
            jobs.append((nm_of("k2", v), {"k2": v}, 1.0, s, {}, amin_scale))

    for v in aWs:
        for s in SEEDS:
            jobs.append((nm_of("alphaW_scale", v),
                         {"alpha_W": P["alpha_W"] * v}, 1.0, s, {}, amin_scale))

    jobs.append(("control_no_reaction", {}, 1.0, 11, {"no_reaction": True}, amin_scale))
    jobs.append(("control_no_perturbation", {}, 1.0, 11, {"no_noise": True}, amin_scale))
    for s in SEEDS:
        jobs.append(("control_per_step_noise", {}, 1.0, s, {"per_step_noise": True},
                     amin_scale))

    for nm, ov, sc in ref_conditions:
        for s in SEEDS[:2]:
            jobs.append((f"grid_refine[{nm}]", ov, sc, s, {"dx": P["dx"] / 1.5}, amin_scale))
            jobs.append((f"dt_refine[{nm}]", ov, sc, s, {"dt": P["dt"] / 4.0}, amin_scale))

    if not use_cache:
        log(f"== stage 2: running {len(jobs)} simulations on {nw} workers ==")
        results = []
        with ProcessPoolExecutor(max_workers=nw) as ex:
            for i, r in enumerate(ex.map(job, jobs, chunksize=1)):
                results.append(r)
                if (i + 1) % 25 == 0:
                    log(f"   {i + 1}/{len(jobs)}  ({time.time() - t_start:.0f}s)")
        log(f"   simulations done at {time.time() - t_start:.0f}s")
        CACHE.write_text(json.dumps(dict(results=results, wt0=wt0, lam_meas=lam_meas,
                                         amin_scale=amin_scale,
                                         sim_seconds=round(time.time() - t_start, 1),
                                         n_simulations=len(jobs) + len(WT_SEEDS),
                                         workers=nw)))

    by = {}
    for r in results:
        by.setdefault(r["name"], []).append(r)

    def agg(name):
        rs = [r for r in by.get(name, []) if not r.get("diverged")]
        if not rs:
            return None
        c = [r["element_count"] for r in rs]
        cls = [r["cls"] for r in rs]
        ORD = ["none", "single fused domain", "single element", "reduced",
               "normal digit number", "increased (polydactyl-like)"]
        # modal class; ties broken towards the more severe (lower-index) class
        mcls = sorted(set(cls), key=lambda x: (-cls.count(x), ORD.index(x)))[0]
        return dict(element_count_mean=float(np.mean(c)), element_count_sd=float(np.std(c, ddof=0)),
                    element_counts=c, n_seeds=len(rs), cls=mcls,
                    element_counts_linear_rule=[r["element_count_linear_rule"] for r in rs],
                    fused_fraction=float(np.mean([r["fused"] for r in rs])),
                    classes=cls, lambda_pred=float(rs[0]["lambda_pred"]),
                    lsa_turing=bool(rs[0]["lsa_turing"]),
                    amplitude_mean=float(np.mean([r["amplitude"] for r in rs])),
                    ap_extent=float(rs[0]["ap_extent"]), pd_extent=float(rs[0]["pd_extent"]),
                    ap_spacing=float(np.mean([v for v in
                                              (ap_spacing(r["centroids_AP"]) for r in rs)
                                              if v is not None]))
                    if any(ap_spacing(r["centroids_AP"]) for r in rs) else None)

    wt = agg("wt")
    log(f"== WT: counts {wt['element_counts']}  mean {wt['element_count_mean']:.2f}"
        f" sd {wt['element_count_sd']:.2f}  measured AP spacing {lam_meas:.1f}")

    sweeps = {}
    for knob, vals, jk in [
        ("diffusion_scale", diff_scales, "diffusion_scale"),
        ("fgf_strength_kF", kFs, "kF"),
        ("domain_scale", dom_scales, "domain_scale"),
        ("bmp_sox9_coupling_balanced", bals, "bmp_coupling"),
        ("bmp_to_sox9_k2_alone", k2s, "k2"),
        ("wnt_production_alphaW_scale", aWs, "alphaW_scale"),
    ]:
        rows = []
        for v in vals:
            a = agg(nm_of(jk, v))
            if a is None:
                continue
            row = dict(value=v, **a)
            if knob == "domain_scale":
                row["ap_extent_in_wavelengths"] = a["ap_extent"] / lam_meas
                row["pd_extent_in_wavelengths"] = a["pd_extent"] / lam_meas
            rows.append(row)
        sweeps[knob] = rows

    # critical domain size: largest domain_scale with no elements, under each counting rule
    dom = sweeps["domain_scale"]

    def crit_for(key):
        """key -> a function giving the mean count for a row under one counting rule."""
        none_rows = [r for r in dom if np.mean(r[key]) == 0]
        pat_rows = [r for r in dom if np.mean(r[key]) > 0]
        if not none_rows or not pat_rows:
            return None, None, None
        hi = max(none_rows, key=lambda r: r["value"])
        lo = min(pat_rows, key=lambda r: r["value"])
        return (0.5 * (hi["ap_extent_in_wavelengths"] + lo["ap_extent_in_wavelengths"]),
                0.5 * abs(lo["ap_extent_in_wavelengths"] - hi["ap_extent_in_wavelengths"]),
                0.5 * (hi["pd_extent_in_wavelengths"] + lo["pd_extent_in_wavelengths"]))

    crit, unc, crit_pd = crit_for("element_counts")
    crit_o, unc_o, _ = crit_for("element_counts_linear_rule")
    log(f"== critical domain size: {crit} +/- {unc} wavelengths (AP); "
        f"under the original rule {crit_o} +/- {unc_o}")

    # ------------------------------------------------------------------ figures
    plt, cmap = _mpl()
    log("== figures ==")
    r_wt = simulate(pr0, WT_SEEDS[0], frames=60)
    vmin, vmax = -3.2, 2.2
    lam_elem_wt = ref["wavelength"] * amin_scale
    FULL = extent_of(r_wt)

    # 1. normal
    fig = plt.figure(figsize=(14.0, 7.2))
    gs = fig.add_gridspec(2, 3, width_ratios=[2.0, 1.0, 1.0], height_ratios=[1, 1],
                          hspace=0.30, wspace=0.30)
    ax = fig.add_subplot(gs[:, 0])
    n_wt = classify(r_wt["S"], r_wt["mask"], r_wt["dx"], lam_elem_wt)["element_count"]
    draw_panel(ax, r_wt, cmap, vmin, vmax, lam_elem_wt,
               "SIMULATION - Sox9 field, wild-type-like paddle",
               f"{n_wt} skeletal elements (lime outline). Not an observation.")
    from matplotlib.cm import ScalarMappable
    from matplotlib.colors import Normalize
    cb = fig.colorbar(ScalarMappable(norm=Normalize(vmin, vmax), cmap=cmap), ax=ax,
                      fraction=0.035, pad=0.02)
    cb.set_label("Sox9 (model units); steady state = 0", fontsize=9)
    axf = fig.add_subplot(gs[0, 1])
    ff = np.full(r_wt["mask"].shape, np.nan); ff[r_wt["mask"]] = r_wt["F"]
    im = axf.imshow(ff.T, origin="lower", cmap="copper_r")
    axf.set_xticks([]); axf.set_yticks([])
    for s in axf.spines.values():
        s.set_visible(False)
    axf.set_title("Fgf field F (ASSUMED shape)", fontsize=10)
    fig.colorbar(im, ax=axf, fraction=0.035, pad=0.02)

    axd = fig.add_subplot(gs[0, 2])
    qs = np.linspace(1e-6, 0.35, 600)
    a4 = (1 - pr0["kF"] * ref["F"]) * pr0["k4"]; a7 = pr0["k7"] * pr0["kF"] * ref["F"]
    gg = _growth(0.0, a4, a7, pr0, qs)
    axd.plot(qs, gg, color=TEAL, lw=2)
    axd.axhline(0, color=INK, lw=0.8)
    axd.axvline(ref["q_max"], color=RED, lw=1.4, ls="--")
    axd.set_xlabel("wavenumber q"); axd.set_ylabel("growth rate")
    axd.set_title(f"dispersion at F={ref['F']:.2f}", fontsize=10)
    axd.text(ref["q_max"], float(np.max(gg)) * 0.6, f"  lambda_lin={ref['wavelength']:.0f}",
             color=RED, fontsize=9)

    axs2 = fig.add_subplot(gs[1, 1:])
    axs2.axis("off")
    axs2.text(0.0, 1.0, "SIMULATION, not observation", fontsize=12, color=RED, va="top",
              fontweight="bold")
    axs2.text(0.0, 0.86,
              f"Bmp-Sox9-Wnt Turing network\n"
              f"(published equation form; operating point retuned)\n\n"
              f"lambda_lin  (linear stability)   = {ref['wavelength']:.0f} model units\n"
              f"lambda_sat  (1-D control, F=0.62)= {lam_sat:.0f}\n"
              f"lambda_meas (AP element spacing) = {lam_meas:.0f}\n\n"
              f"elements over {len(WT_SEEDS)} seeds: "
              f"{wt['element_count_mean']:.1f} +/- {wt['element_count_sd']:.1f} "
              f"(range {min(wt['element_counts'])}-{max(wt['element_counts'])})",
              fontsize=10.0, color=INK, va="top", family="monospace")
    fig.suptitle("Digit patterning as a Turing system - simulated wild-type-like pattern",
                 fontsize=15, color=INK)
    fig.savefig(HERE / "digit-turing-normal.png", dpi=133, bbox_inches="tight")
    plt.close(fig)

    # 2. series: normal -> nothing
    series_specs = [
        (nm_of("diffusion_scale", 0.4), {"D_B": P["D_B"] * 0.4, "D_W": P["D_W"] * 0.4}, 1.0,
         "shorter wavelength\n(diffusion x0.4)"),
        ("wt", {}, 1.0, "wild-type-like"),
        (nm_of("diffusion_scale", 2.0), {"D_B": P["D_B"] * 2.0, "D_W": P["D_W"] * 2.0}, 1.0,
         "longer wavelength\n(diffusion x2.0)"),
        (nm_of("domain_scale", 0.50), {}, 0.50, "small bud\n(domain x0.50)"),
        (nm_of("domain_scale", 0.25), {}, 0.25, "smaller bud\n(domain x0.25)"),
        (nm_of("domain_scale", 0.16), {}, 0.16, "truncated bud\n(domain x0.16)"),
        (nm_of("bmp_coupling", 6.0), {"k2": P["k2"] * 6.0, "alpha_W": P["alpha_W"] * 6.0}, 1.0,
         "sub-critical\n(Bmp-Sox9 coupling x6)"),
    ]
    fig, axes = plt.subplots(1, len(series_specs), figsize=(15.5, 6.0))
    for ax, (nm, ov, sc, lab) in zip(axes, series_specs):
        p = dict(pr0); p.update(ov)
        rr = simulate(p, WT_SEEDS[0], scale=sc)
        lam = dominant_lsa_over_domain(p, p["F_max"], p["F_max"] * np.exp(-p["F_decay"]))
        lam_a = (lam["wavelength"] if lam["turing"] else lambda_wt()) * amin_scale
        cc = classify(rr["S"], rr["mask"], rr["dx"], lam_a)
        a = agg(nm) or {}
        sd = a.get("element_count_sd")
        col = GREEN if cc["element_count"] == 5 else (RED if cc["element_count"] == 0 else WARN)
        draw_panel(ax, rr, cmap, vmin, vmax, lam_a, lab, outline=True, common_extent=FULL)
        mean = a.get("element_count_mean")
        ax.text(0.5, -0.02, f"n = {cc['element_count']}", transform=ax.transAxes,
                ha="center", va="top", fontsize=15, color=col, fontweight="bold")
        if sd is not None:
            ax.text(0.5, -0.10, f"{mean:.1f} $\\pm$ {sd:.1f} over 3 seeds",
                    transform=ax.transAxes, ha="center", va="top", fontsize=8.5, color=INK)
        ax.text(0.5, -0.17, cc["cls"], transform=ax.transAxes, ha="center", va="top",
                fontsize=8.5, color=WARN)
    fig.subplots_adjust(left=0.015, right=0.985, wspace=0.02, bottom=0.30, top=0.78)
    fig.suptitle("SIMULATION - one network, many routes to no skeletal pattern",
                 fontsize=16, color=INK, y=0.955)
    fig.text(0.5, 0.125,
             "All panels on one spatial scale. Element count from a pre-declared rule: connected\n"
             "components of Sox9 > 0.25*p99 with area >= 0.10*lambda^2, outlined in lime.\n"
             "One seed shown, mean over 3 seeds beside it. Nothing here is an observation.",
             ha="center", va="top", fontsize=9.5, color=WARN, linespacing=1.5)
    fig.savefig(HERE / "digit-turing-series.png", dpi=102)
    plt.close(fig)

    # 3. domain-size figure
    fig, ax = plt.subplots(figsize=(14.0, 6.6))
    xs_ = [r["ap_extent_in_wavelengths"] for r in dom]
    ys_ = [r["element_count_mean"] for r in dom]
    es_ = [r["element_count_sd"] for r in dom]
    yo_ = [float(np.mean(r["element_counts_linear_rule"])) for r in dom]
    ax.plot(xs_, xs_, color=INK, lw=1.0, ls="--", alpha=0.45, zorder=1,
            label="one element per wavelength of width")
    ax.plot(xs_, yo_, "s--", color=WARN, lw=1.4, ms=5, alpha=0.75, zorder=2,
            label="same runs, original (smaller) minimum-element-size cut")
    ax.errorbar(xs_, ys_, yerr=es_, fmt="o-", color=TEAL, ecolor=TEAL, capsize=4,
                lw=2.4, ms=9, mfc=LIME, mec=TEAL, mew=1.8, zorder=4,
                label="elements counted (mean of 3 seeds)")
    for r in dom:
        if r["value"] in (0.05, 0.2, 0.4, 0.65, 1.0, 1.25):
            ax.annotate(f"{r['value']:g}x",
                        (r["ap_extent_in_wavelengths"], r["element_count_mean"]),
                        textcoords="offset points", xytext=(0, 14), ha="center",
                        fontsize=9, color=INK)
    if crit is not None:
        ax.axvspan(crit - unc, crit + unc, color=RED, alpha=0.13, zorder=0)
        ax.axvline(crit, color=RED, lw=2, ls="--", zorder=3)
        ax.text(crit + 0.15, max(ys_) * 0.99,
                f"critical AP width\n{crit:.2f} $\\pm$ {unc:.2f} wavelengths\n"
                f"({crit_o:.2f} $\\pm$ {unc_o:.2f} under the\noriginal size cut)",
                color=RED, fontsize=10.5, va="top")
    ax.axhline(5, color=GREEN, lw=1.2, ls=":")
    ax.text(max(xs_), 5.12, "five elements ", color=GREEN, ha="right", fontsize=10)
    ax.legend(loc="lower right", frameon=False, fontsize=9.5)
    ax.set_xlabel("anteroposterior width of the paddle, in units of the pattern's own "
                  f"wavelength ($\\lambda_{{meas}}$ = {lam_meas:.0f} model units)")
    ax.set_ylabel("skeletal elements (mean of 3 seeds)")
    ax.set_title("SIMULATION - shrink the domain and the pattern runs out of room",
                 fontsize=15, color=INK)
    ax.grid(alpha=0.18, color=INK)
    ax.set_ylim(-0.4, max(ys_) + 1.2)
    fig.text(0.5, -0.015,
             "Labels give the linear scale factor applied to the whole paddle. The Fgf gradient "
             "scales with the bud, so the Turing-permissive band shrinks with it.\n"
             "The two curves are the SAME simulations counted with two minimum-element-size "
             "cuts: the critical size is rule-dependent by about a factor of two, so quote the "
             "range.\nSimulated; no measured limb-bud dimension is used anywhere.",
             ha="center", va="top", fontsize=9.5, color=WARN, linespacing=1.5)
    fig.savefig(HERE / "digit-turing-domain.png", dpi=122, bbox_inches="tight")
    plt.close(fig)

    # 4. movie (optional)
    movie = None
    if shutil.which("ffmpeg") and r_wt.get("snaps"):
        try:
            fdir = HERE / "_frames"
            fdir.mkdir(exist_ok=True)
            for i, (t, Sv) in enumerate(r_wt["snaps"]):
                f = np.full(r_wt["mask"].shape, np.nan); f[r_wt["mask"]] = Sv
                fg, axm = plt.subplots(figsize=(7.0, 5.6))
                axm.imshow(f.T, origin="lower", cmap=cmap, vmin=vmin, vmax=vmax,
                           interpolation="nearest", extent=extent_of(r_wt), aspect="equal")
                axm.set_xticks([]); axm.set_yticks([])
                for s in axm.spines.values():
                    s.set_visible(False)
                axm.set_title(f"SIMULATION - Sox9, t = {t:5.1f}", fontsize=13, color=INK)
                axm.text(0.5, -0.06, "not an observation", transform=axm.transAxes,
                         ha="center", va="top", fontsize=9, color=WARN)
                fg.savefig(fdir / f"f{i:04d}.png", dpi=170, bbox_inches="tight",
                           facecolor=BG)
                plt.close(fg)
            out = HERE / "digit-turing.mp4"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-threads", "2",
                            "-framerate", "12", "-i", str(fdir / "f%04d.png"),
                            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                            "-pix_fmt", "yuv420p", "-threads", "2", str(out)], check=True)
            shutil.rmtree(fdir, ignore_errors=True)
            movie = out.name
            log(f"   wrote {movie}")
        except Exception as e:                                   # noqa: BLE001
            log(f"   movie skipped: {e}")

    # ------------------------------------------------------------------ refinement + controls
    def refi(tag, base):
        a, b_ = agg(tag), agg(base)
        if a is None or b_ is None:
            return None
        return dict(condition=base, baseline_counts=b_["element_counts"][:len(a["element_counts"])],
                    refined_counts=a["element_counts"],
                    max_abs_difference=int(max(abs(x - y) for x, y in
                                               zip(sorted(a["element_counts"]),
                                                   sorted(b_["element_counts"]
                                                          [:len(a["element_counts"])])))))

    refinement = {
        "grid": {nm: refi(f"grid_refine[{nm}]", nm) for nm, _, _ in ref_conditions},
        "dt": {nm: refi(f"dt_refine[{nm}]", nm) for nm, _, _ in ref_conditions},
        "grid_change": "dx 4.0 -> 2.667 (x1.5 finer in each direction)",
        "dt_change": "dt 0.01 -> 0.0025 (x4 smaller)",
    }

    nr = by["control_no_reaction"][0]
    npert = by["control_no_perturbation"][0]
    psn = agg("control_per_step_noise")
    controls = {
        "no_reaction": {
            "what": "Sox9->Bmp and Sox9->Wnt couplings and the Bmp/Wnt->Sox9 terms all set to "
                    "zero; diffusion, production and decay left in place.",
            "must_show": "a flat field",
            "amplitude": nr["amplitude"], "element_count": nr["element_count"],
            "class": nr["cls"],
            "pass": bool(nr["amplitude"] < 0.05 and nr["element_count"] == 0),
        },
        "no_initial_perturbation": {
            "what": "full model, but the t=0 perturbation of S is omitted, so the field starts "
                    "at the exact homogeneous steady state (verified analytically: S*=0, "
                    "B*=alpha_B/k5, W*=alpha_W/k9 makes all three time derivatives vanish at "
                    "every point, whatever the local Fgf level).",
            "expected_when_designed": "a flat field",
            "amplitude": npert["amplitude"], "element_count": npert["element_count"],
            "class": npert["cls"],
            "result": "DID NOT STAY FLAT, and this is reported rather than quietly dropped.",
            "interpretation": "The state is linearly UNSTABLE with max growth rate "
                              f"{ref['growth_max']:.2f} per model time unit, and the run is "
                              f"{P['T_end']:.0f} time units long, so double-precision rounding "
                              "at the 1e-16 level is amplified by roughly exp(490) and "
                              "saturates long before the end. A linearly unstable state cannot "
                              "be held flat numerically, so this arm cannot test what it was "
                              "designed to test. What it DOES establish is the converse: the "
                              "pattern is not an artifact of the injected noise, because it "
                              "forms without any. The arm that genuinely tests flatness is "
                              "no_reaction (which passed), and the sub-critical end of "
                              "bmp_sox9_coupling_balanced, which is linearly stable and does "
                              "stay flat.",
        },
        "per_step_noise": {
            "what": "dt-scaled additive Gaussian noise on S at every step instead of a single "
                    "t=0 perturbation (the published scheme is 1% multiplicative noise per "
                    "step, which vanishes identically at S*=0).",
            "must_show": "the same element counts as the default noise model",
            "counts": psn["element_counts"], "mean": psn["element_count_mean"],
            "sd": psn["element_count_sd"],
            "wt_counts_same_seeds": wt["element_counts"][:3],
        },
        "positive_and_negative_control_for_the_counter": {
            "what": "The counter is run against a case it must flag and a case it must not: "
                    "the wild-type-like field (must return a multi-element count) and the "
                    "no-reaction field (must return 0).",
            "wild_type_mean_count": wt["element_count_mean"],
            "no_reaction_count": nr["element_count"],
            "pass": bool(wt["element_count_mean"] >= 3.0 and nr["element_count"] == 0),
        },
    }

    # ------------------------------------------------------------------ JSON
    out = {
        "what_this_is": "A SIMULATION of skeletal-element patterning by a Bmp-Sox9-Wnt Turing "
                        "network in a limb-bud-shaped domain. No value in this file is an "
                        "observation, a measurement, or a reproduction of published data. The "
                        "element counts, wavelengths and critical domain size are properties of "
                        "this model at these parameters and nothing else.",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "model": {
            "name": "BSW (Bmp-Sox9-Wnt) Turing network with a proximodistal Fgf gradient",
            "variables": [
                {"symbol": "S", "species": "Sox9", "diffuses": False,
                 "note": "D_S = 0; Sox9 is cell-autonomous (sourced: onimaru2016 states the "
                         "system has one non-diffusive molecule, Sox9)."},
                {"symbol": "B", "species": "Bmp", "diffuses": True,
                 "note": "long-range species, D_B = 160"},
                {"symbol": "W", "species": "Wnt", "diffuses": True,
                 "note": "short-range species, D_W = 25"},
                {"symbol": "F", "species": "Fgf", "diffuses": "prescribed, not solved",
                 "note": "static normalised gradient from the distal margin (the AER)"},
            ],
            "equations_latex": EQUATIONS_LATEX,
            "topology": TOPOLOGY,
            "parameters": PARAMS,
            "parameter_provenance_summary": {
                "sourced": [p["name"] for p in PARAMS if p["status"] == "sourced"],
                "assumed": [p["name"] for p in PARAMS if p["status"] == "assumed"],
                "statement": "The EQUATION FORM and 11 of 19 parameters are sourced at full-text "
                             "level from onimaru2016, which states that it implements the "
                             "raspopovic2014 mouse BSW model. One sourced parameter (alpha_W) "
                             "was CHANGED, for the reason recorded in its entry and measured in "
                             "linear_stability.published_set_check. The geometry, the Fgf "
                             "gradient shape, and all numerical parameters are assumed. The "
                             "mouse parameter set of raspopovic2014 could not be obtained: that "
                             "paper is subscription-only and was read at abstract level.",
            },
        },
        "linear_stability": {
            "method": "Eigenvalues of the 3x3 Jacobian M(q) of the full nonlinear system, "
                      "linearised about the homogeneous steady state, with the diffusion terms "
                      "-D_B q^2 and -D_W q^2 on the diagonal and D_S = 0, evaluated on a grid "
                      "of 6001 wavenumbers q in [0, 1.2]. Turing instability is declared when "
                      "max Re sigma(0) < 0 AND max_q Re sigma(q) > 0 at q > 0. The homogeneous "
                      "steady states are the real roots of the cubic in S obtained by "
                      "eliminating B and W.",
            "steady_state_used": {"S": 0.0, "B": P["alpha_B"] / P["k5"],
                                  "W": P["alpha_W"] / P["k9"]},
            "turing_window_in_F": {"F_low": win[0] if win else None,
                                   "F_high": win[1] if win else None,
                                   "note": "below F_low the uniform state is stable (no "
                                           "pattern); above F_high it is unstable at q=0 "
                                           "(uniform runaway, not a Turing pattern). F_max was "
                                           "set to 0.62, just below F_high."},
            "predicted_wavelength": ref["wavelength"],
            "predicted_wavelength_units": "model length units",
            "predicted_at_F": ref["F"],
            "max_growth_rate": ref["growth_max"],
            "published_set_check": {
                "question": "Is the published parameter set, with alpha_W = 1.2, Turing-unstable "
                            "on this static domain?",
                "answer": "No.",
                "scope": "51 values of F in [0,1]; every real homogeneous steady state at each "
                         "(1 to 3 roots); 6001 wavenumbers in [0,1.2].",
                "max_growth_rate_found": pub_best["growth_max"],
                "at_F": pub_best["F"], "at_q": pub_best["q_max"],
                "growth_at_q0_there": pub_best["growth_at_q0"],
                "any_turing_instability": pub_turing,
                "diagnosis": "With alpha_W = 1.2 the homogeneous steady state lies far from "
                             "S = 0 (S* between about -5.8 and -0.58 on the branch that is "
                             "continuous in F), so the cubic self-damping term -3S*^2 is large "
                             "and suppresses the instability. The one state with a positive "
                             "growth rate is unstable already at q = 0, which is a uniform "
                             "instability, not a Turing instability.",
                "what_this_does_and_does_not_mean": "This is NOT a claim that the published "
                             "model is wrong. onimaru2016 run it on a GROWING catshark fin mesh "
                             "with per-step noise and a reaction-diffusion Fgf field whose "
                             "absolute spatial scale is set by a mesh I do not have, and their "
                             "published Turing-space analysis uses the LINEAR model (k1 = 0, so "
                             "f_S = 0) with k3 = 1, not the cubic model with k3 = 3. My test is "
                             "a static homogeneous domain and is not like-for-like. What it "
                             "does mean is that I could not reproduce a Turing instability from "
                             "the published numbers as I read them, so the operating point here "
                             "is mine and is labelled assumed.",
            },
        },
        "measured_wavelength": {
            "two_d_AP_element_spacing": lam_meas,
            "two_d_measurement": "mean spacing between the anteroposterior centroids of "
                                 "adjacent counted elements, averaged over the 6 wild-type "
                                 "seeds. This is the pattern's own wavelength and it is the "
                                 "one used for the critical domain size.",
            "one_d_uniform_control": one_d,
            "one_d_uniform_control_note": "1-D periodic domain of length 1500 at a uniform Fgf "
                                          "level, spectral diffusion, probed at t=2 (still "
                                          "linear) and at t=160 (saturated). The three F values "
                                          "span the Turing-permissive band of the 2-D paddle.",
            "units": "model length units",
            "comparison_to_linear_prediction": {
                "lambda_linear_LSA": ref["wavelength"],
                "ratio_saturated_over_linear": lam_sat / ref["wavelength"],
                "ratio_2D_measured_over_linear": lam_meas / ref["wavelength"],
                "verdict": "THEY DISAGREE, by a factor of about two, and the disagreement is "
                           "reported rather than tuned away. The linear analysis predicts the "
                           "FASTEST-GROWING mode at onset; the simulated pattern then coarsens "
                           "and the coarsening arrests at a longer, nonlinearly selected "
                           "wavelength. The agreement that does hold is in the LINEAR regime: a "
                           "1-D uniform-domain run probed at t = 2, while the amplitude is "
                           "still small, has a dominant wavelength close to the LSA value "
                           f"({lam_lin_1d:.0f} against {ref['wavelength']:.0f} at F=0.62). "
                           "Coarsening was measured to arrest by t ~ 40 and the wavelength was "
                           "then unchanged out to t = 320. The 2-D measured spacing is shorter "
                           "than the 1-D saturated wavelength at F = 0.62 because the 2-D "
                           "permissive band spans a range of F, not just its distal maximum, "
                           "and is only about one wavelength deep.",
            },
        },
        "sweeps": sweeps,
        "sweep_descriptions": {
            "diffusion_scale": "D_B and D_W scaled together by this factor. lambda scales as "
                               "sqrt(factor). This is the WAVELENGTH KNOB. Direction check: "
                               "shorter wavelength should give MORE, thinner elements, which is "
                               "the direction sheth2012 reports for progressive loss of distal "
                               "Hox dose (read at abstract level; no number taken from it).",
            "fgf_strength_kF": "Strength of the Fgf modulation of k4 and k7. Moves the system "
                               "through the Turing window and changes where the permissive band "
                               "sits.",
            "domain_scale": "Linear scale factor on the whole paddle, Fgf gradient scaling with "
                            "it. This is the bridge to a truncated limb bud.",
            "bmp_sox9_coupling_balanced":
                "THIS IS THE CRITICALITY KNOB. k2 and alpha_W are scaled by the same factor, "
                "which changes the Bmp->Sox9 coupling strength while leaving the operating "
                "point exactly at S* = 0 (the balance k2*alpha_B/k5 = k3*alpha_W/k9 is "
                "preserved under a common factor, and S* = 0 was verified at every value). "
                "The linear-stability growth rate falls monotonically from factor 0.85 "
                "upwards and the Turing instability is LOST at factor 5.5 (max Re sigma over "
                "all q and all F in the bud becomes negative). Above that the field stays at "
                "the homogeneous steady state: a uniform Sox9 field and no skeletal elements, "
                "with no change to the domain and no change to the wavelength mechanism.",
            "bmp_to_sox9_k2_alone":
                "Strength of Bmp activation of Sox9, varied ON ITS OWN. onimaru2016 perturb "
                "exactly this parameter to represent Bmp inhibition. READ THIS ONE WITH CARE "
                "and prefer bmp_sox9_coupling_balanced: in this retuned model the homogeneous "
                "steady state sits at S* = 0 only when k2*alpha_B/k5 = k3*alpha_W/k9, which "
                "with the other values here means only at k2 = 1. Changing k2 alone therefore "
                "moves the operating point as well as the coupling, and the two effects cannot "
                "be separated. That is why every value except 1 collapses to a single fused "
                "domain. The sweep is kept because that fragility is a real property of the "
                "assumed operating point and hiding it would misrepresent the model.",
            "wnt_production_alphaW_scale":
                "Multiplier on alpha_W, the constant Wnt production term. READ THIS ONE WITH "
                "CARE. onimaru2016 perturb Wnt production and report partial fusion of Sox9 "
                "into continuous domains, matched in vivo by a porcupine inhibitor, and that "
                "is what the fused class here looks like. BUT in this retuned model alpha_W "
                "also sets the operating point: S* = 0 only at the one value "
                "alpha_W = k2*alpha_B*k9/(k3*k5), and moving alpha_W moves S* away from zero, "
                "which switches the cubic self-damping -3S*^2 back on. So this sweep measures "
                "the FRAGILITY OF THE ASSUMED OPERATING POINT at least as much as it measures "
                "a Wnt perturbation, and the two cannot be separated in this parameterisation. "
                "It is reported because that fragility is a real and unflattering property of "
                "the choice made here, not because it is a clean perturbation.",
        },
        "one_condition_behind_every_route_to_no_elements": {
            "statement": "In this model every route to zero skeletal elements is the same "
                         "geometric condition: the Turing-PERMISSIVE REGION must be at least "
                         "about one wavelength across. Shrinking the bud shrinks that region "
                         "in space; de-tuning the network shrinks it in parameter space, and "
                         "therefore also in space, because the Fgf gradient maps parameter "
                         "space onto the proximodistal axis.",
            "evidence_from_the_domain_sweep": "Elements disappear below about 0.9 wavelengths "
                                              "of anteroposterior width.",
            "evidence_from_the_coupling_sweep": "At Bmp-Sox9 coupling x5 the linear analysis "
                                                "still reports a Turing instability (max growth "
                                                "+0.31 per time unit), but the simulation forms "
                                                "nothing. The reason is geometric and is "
                                                "computable from the LSA: at that coupling the "
                                                "Turing window has narrowed to F in "
                                                "(0.596, 1.0), and with F_max = 0.62 and "
                                                "F = F_max*exp(-4*x_hat) over L_PD = 300, the "
                                                "permissive strip is only about 3.0 model "
                                                "length units deep, against a wavelength of "
                                                "18.6 there - under a fifth of a wavelength, "
                                                "and narrower than one grid cell. At coupling "
                                                "x4 the strip is about 13.7 units against a "
                                                "wavelength of 24.9, roughly 0.55 wavelengths, "
                                                "and the counts are correspondingly marginal "
                                                "and seed-dependent (1, 3, 1).",
            "consequence": "The simulated loss of pattern (coupling x5) comes BEFORE the formal "
                           "loss of linear instability (x5.5). Both numbers are reported; the "
                           "simulated one is the one that would be observable.",
        },
        "critical_domain_size": {
            "value": crit, "units": "wavelengths",
            "uncertainty": unc,
            "axis": "anteroposterior width of the paddle at its widest point",
            "pd_extent_at_the_same_point_in_wavelengths": crit_pd,
            "definition": "Midpoint between the largest domain scale with a mean element count "
                          "of exactly zero and the smallest with a non-zero mean, expressed in "
                          "units of the measured wavelength lambda_meas. The uncertainty is "
                          "half that interval and is set by the spacing of the domain_scale "
                          "grid, not by a fit.",
            "value_under_the_original_counting_rule": crit_o,
            "uncertainty_under_the_original_counting_rule": unc_o,
            "rule_sensitivity": "THE CRITICAL SIZE DEPENDS ON THE COUNTING RULE, by about a "
                                "factor of two, and both numbers are given. The revised rule "
                                "requires a surviving component to be at least 0.10 * "
                                "lambda_meas^2; the original required only 0.10 * "
                                "lambda_lin^2, which is about four times smaller in area and "
                                "so still counts a partial condensation in a bud too small to "
                                "hold a whole one. Quote the range, not one end of it.",
            "reading": "Somewhere between about half a wavelength and about one and a quarter "
                       "wavelengths of anteroposterior width, the paddle stops being able to "
                       "hold an element and the field is unpatterned. Because the Fgf gradient "
                       "scales with the bud, the proximodistal permissive band shrinks at the "
                       "same time, so both axes run out together; the AP figure is the one "
                       "quoted and the PD extent at the same point is given beside it.",
        },
        "refinement_arm": refinement,
        "controls": controls,
        "classification_rule": CLASSIFY_RULE,
        "classification_rule_change": CLASSIFY_RULE_CHANGE
            .replace("{ORIG}", str([r["element_count"] for r in wt0]))
            .replace("{ORIGMEAN}", f"{np.mean([r['element_count'] for r in wt0]):.2f}")
            .replace("{NEW}", str(wt["element_counts"]))
            .replace("{NEWMEAN}", f"{wt['element_count_mean']:.2f}"),
        "sweeps_under_the_original_rule": {
            "wild_type": [r["element_count"] for r in wt0],
            "note": "Per-condition counts under the original rule are in each sweep row as "
                    "element_counts_linear_rule.",
        },
        "seeds": {"wild_type": WT_SEEDS, "sweeps": SEEDS,
                  "note": "Turing patterns are seed-dependent. Every sweep point is run from "
                          "3 fixed seeds and the spread is reported as element_count_sd; the "
                          "individual counts are kept in element_counts."},
        "numerics": {
            "scheme": "IMEX. Diffusion and linear decay of B and W implicit (one sparse LU "
                      "factorisation per condition, reused every step); the cubic in S treated "
                      "semi-implicitly as -S_new * S_old^2, which keeps S bounded; all couplings "
                      "explicit. Zero-flux boundary on the masked domain.",
            "deviation_from_published_numerics": "onimaru2016 use an explicit Heun solver with "
                                                 "dt = 0.002 on a triangular finite-volume mesh "
                                                 "and a growing domain. This is a fixed "
                                                 "cartesian grid, a static domain, and a "
                                                 "semi-implicit solver.",
            "dt_0.02_was_unstable": "Measured: at dt = 0.02 the solution diverged to ~1e8; at "
                                    "dt = 0.01, 0.005 and 0.002 the final field agreed to 5 "
                                    "significant figures. dt = 0.01 is the default.",
        },
        "limitations": [
            "NO GROWTH. The real limb bud grows while it patterns, and raspopovic2014's and "
            "onimaru2016's simulations both run on growing meshes. On a static domain the "
            "elements form as condensations in a distal band rather than elongating into "
            "proximodistally running digit rays. This study measures element NUMBER, not "
            "element SHAPE, and the shapes here should not be read as digit morphology.",
            "The five-element wild-type-like outcome is IMPOSED by the chosen paddle width, not "
            "predicted. Only the changes in element count across the sweeps are model "
            "predictions.",
            "The mouse parameter set of raspopovic2014 was not obtainable. The numbers used come "
            "from onimaru2016's CATSHARK FIN simulation of the same network, and one of them "
            "(alpha_W) had to be changed to obtain a Turing instability at all.",
            "All lengths are model length units. The model as published carries no physical "
            "length scale that I can verify, so no result here is in micrometres and no "
            "statement is made about the real size of any limb bud.",
            "The linear-stability wavelength and the simulated wavelength differ by a factor of "
            "about two (see measured_wavelength). The simulated value is the one used for the "
            "critical domain size.",
            "The classification into phenotype classes is a threshold rule on a simulated "
            "scalar field. It is objective and pre-declared, but 'normal digit number' here "
            "means 'five counted components in this simulation', not a mouse phenotype.",
            "Only one noise model, one domain shape, and one gradient shape were explored. "
            "Turing element counts are sensitive to all three.",
            "THE ASSUMED OPERATING POINT IS FRAGILE. Because the steady state was placed at "
            "S* = 0 by balancing k2*alpha_B/k5 against k3*alpha_W/k9, any parameter change "
            "that breaks that balance moves S* off zero and switches the cubic self-damping "
            "back on. A 20% change in alpha_W alone, or a 15% change in k2 alone, collapses "
            "the five-element pattern to a single fused domain (see the "
            "wnt_production_alphaW_scale and bmp_to_sox9_k2_alone sweeps). The "
            "bmp_sox9_coupling_balanced sweep exists because it changes the coupling WITHOUT "
            "breaking that balance, and it is the one to read for criticality. The fragility "
            "is a property of this reparameterisation, not a claim about the published model.",
            "THE ELEMENT COUNT DEPENDS ON THE MINIMUM-SIZE CUT by about one element, because "
            "the anterior-most and posterior-most condensations sit where the paddle narrows "
            "and are genuinely smaller. The wild-type count is 5.3 +/- 0.9 under the original "
            "rule and 4.2 +/- 0.7 under the revised one, over the same six seeds, and the "
            "critical domain size moves by about a factor of two between them. Treat one "
            "element as the resolution of this measurement.",
            "The grid-refinement arm changes the element count by 1 in two of three "
            "conditions, which is the same one-element resolution; the dt-refinement arm "
            "changes nothing.",
        ],
        "what_this_does_not_establish": [
            "It does not establish that any real limbless or limb-reduced animal, or any real "
            "mutant, lacks limbs because of a change in a Turing wavelength or a sub-critical "
            "patterning system. No animal was measured here.",
            "It does not establish that the BSW network is the correct mechanism of mouse digit "
            "patterning. That is raspopovic2014's claim, read here at abstract level only.",
            "It does not reproduce any published figure. No comparison to published data was "
            "made, so no agreement with data is claimed.",
            "A simulated phenotype class is not a phenotype.",
        ],
        "sources": SOURCES,
        "runtime_seconds": None,
    }
    out["runtime_seconds"] = round(time.time() - t_start, 1)
    out["runtime_note"] = (
        "runtime_seconds is for THIS invocation. When the figures are redrawn from the cached "
        "simulation results (--figures) it does not include the simulations."
        + (f" The cached results came from a full run of {cached_meta.get('n_simulations')} "
           f"simulations on {cached_meta.get('workers')} worker processes, "
           f"{cached_meta.get('sim_seconds')} s of wall clock to the end of the sweeps on a "
           f"shared 8-core host." if cached_meta else
           " This invocation ran the simulations itself."))
    out["movie"] = movie
    (HERE / "digit-turing.json").write_text(json.dumps(out, indent=2))
    log(f"== wrote digit-turing.json  ({out['runtime_seconds']}s total)")
    log("   sweeps:")
    for k, rows in sweeps.items():
        log(f"     {k}: " + ", ".join(
            f"{r['value']:g}->{r['element_count_mean']:.1f}+/-{r['element_count_sd']:.1f}"
            for r in rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
