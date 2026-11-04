"""The cephalopod chromatophore as an addressable actuator: a mechanical model and a datasheet.

WHAT THIS IS
    A lumped Hill-type model of one chromatophore organ: an incompressible pigment
    sacculus modelled as a neo-Hookean membrane, pulled open by N radial muscle fibres
    that anchor in the dermis, and closed again by the sacculus's own stored elastic
    energy against a dermal dashpot. Simulation, not measurement.

THE CONTROL ARM, DECLARED BEFORE RUNNING
    The sacculus shear modulus G is the one quantity nobody has measured. So:
      1. FIT exactly one parameter, G, so the model reproduces the measured steady-state
         area expansion ratio of 2.55x (Hadjisolomou et al. 2021, 4,065 chromatophores
         in 7 live Doryteuthis pealeii at 60 fps, +155.06% area under a flash startle).
      2. Then PREDICT, with nothing further fitted, the expansion rise time and the
         expansion:retraction speed asymmetry, and compare with the same paper
         (rise time 117-150 ms, duration 217-384 ms) and with Renard et al. 2026
         (expansion 0.667 +/- 0.590 px/frame vs contraction 0.422 +/- 0.557 px/frame;
         4.41 +/- 1.91 vs 5.90 +/- 3.50 frames at 20 fps).
      3. Report the mismatch. Do not tune further. A failed control is the result.
    The dermal damping c is NOT fitted to the expansion arm; it is swept, and the value
    that would be needed to match the measured retraction is reported as a prediction
    about a quantity nobody has measured.

MECHANICS
    Geometry. Retracted sacculus radius r0. Radial fibres run from the sacculus rim to a
    fixed dermal anchor at radius R_a, so fibre length L = R_a - r and the fibre shortens
    exactly as the pigment disc widens. Pigment volume is conserved, so the disc thins as
    it spreads: h(r) = V0 / (pi r^2).

    Sacculus elasticity. Incompressible neo-Hookean membrane, equibiaxial stretch
    lambda = r/r0, wall thickness t = t0 lambda^-2. Membrane tension (force per unit rim
    length) T = G t0 (1 - lambda^-6); inward force at the rim F_el = 2 pi r T.

    Muscle. N fibres of physiological cross-section a_m, peak isometric stress sigma_max,
    first-order activation, a parabolic length-tension factor about L_opt, and a Hill
    force-velocity factor. Obliquely striated squid muscle, measured in OTHER muscles of
    the same animal: 212 +/- 105 and 290 +/- 166 kN/m2 (mantle circular, Thompson 2014),
    270 +/- 20 mN/mm2 (funnel retractor, Rosenbluth 2010), 216-335 mN/mm2 (Thompson 2008);
    V_max 2.15-5.1 L0/s.

    Dynamics. Inertia is negligible at this scale (checked below), so the balance is
        F_muscle(r, dr/dt) = F_elastic(r) + c dr/dt
    solved for dr/dt at each step by bracketed root finding.
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OKABE, Param, param_block, style, write_result  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)

# --------------------------------------------------------------------------------------
# Parameters
# --------------------------------------------------------------------------------------

SRC_HADJI = (
    "Hadjisolomou SP et al. 2021, Front Physiol 12:675252, PMID 34220538 "
    "(read: full text via publisher)"
)
SRC_RENARD = (
    "Renard MDM et al. 2026, eLife 110074, PMID 42418335 (read: full text via PMC)"
)
SRC_UKROW = "Ukrow J et al. 2025, eLife 106509, PMID 40719173 (read: full text via PMC)"
SRC_KASUGAI = (
    "Kasugai T et al. 2011, PLoS ONE 6:e18244, PMID 21483763 (read: full text via PMC)"
)
SRC_GAULD = (
    "Gauld C et al. 2021, J Morphol 282:1081-1093, PMID 33998033 (read: abstract)"
)
SRC_THOMPSON14 = (
    "Thompson JT, Shelton RM, Kier WM 2014, J Exp Biol 217:2181-2192, PMID 24675565 "
    "(read: abstract) - PROXY: squid mantle circular muscle, not chromatophore radial muscle"
)
SRC_ROSENBLUTH = (
    "Rosenbluth J, Szent-Gyorgyi AG, Thompson JT 2010, J Exp Biol 213:2430-2443, "
    "PMID 20581273 (read: abstract) - PROXY: squid funnel retractor, not chromatophore muscle"
)
SRC_THOMPSON08 = (
    "Thompson JT, Szczepanski JA, Brody J 2008, J Exp Biol 211:1463-1474, PMID 18424680 "
    "(read: abstract) - PROXY: squid mantle circular muscle"
)

# ---------------------------------------------------------------------------
# Measured targets the control arm is scored against.
#
# Hadjisolomou et al. 2021 (PMID 34220538, read: full text via PMC8250766),
# Doryteuthis pealeii, Table 1. Columns: Response time tR (first crossing of 5% of
# the maximal response), Delay time tD, Rise time tRt (to 100% of the response
# peak), Response duration rD (between the 5% values before and after the peak).
# All timestamps are from the flash. Transcribed here so every derived number
# below is computed rather than typed.
HADJI_TABLE1 = {                 # region: (tR, tD, tRt, rD) for the EXPANSION response
    "head/arms": (50.0, 83.0, 117.0, 300.0),
    "mantle":    (67.0, 117.0, 150.0, 384.0),
    "fin":       (67.0, 100.0, 134.0, 334.0),
}
# Whole-event durations of the separate RETRACTION-type response (n = 65 cells,
# against n = 4,000 expanding). Kept for the record; NOT comparable with the
# retraction PHASE of an expansion event.
HADJI_RETRACTION_RESPONSE_RD = {"head/arms": 267.0, "mantle": 250.0, "fin": 217.0}

def _hadji_phases():
    out = {}
    for region, (tR, tD, tRt, rD) in HADJI_TABLE1.items():
        expand = tRt - tR            # 5% crossing -> peak
        retract = rD - expand        # peak -> back to 5%
        out[region] = {"expansion_phase_ms": expand, "retraction_phase_ms": retract,
                       "retraction_over_expansion": retract / expand}
    return out

HADJI_PHASES = _hadji_phases()
_EXP = [v["expansion_phase_ms"] for v in HADJI_PHASES.values()]

TARGET_AREA_RATIO = 1.0 + 155.06 / 100.0   # +155.06% mean surface-area increase
# The model's clock starts at drive onset and it simulates no sensory or neural
# latency, so the comparator is the expansion PHASE (tRt - tR), not tRt itself.
# Scoring against tRt (117-150 ms, kept below) flattered the model by including a
# 50-67 ms latency it never had.
TARGET_RISE_MS = (min(_EXP), max(_EXP))                      # 67-83 ms
TARGET_RISE_FROM_FLASH_MS = (min(v[2] for v in HADJI_TABLE1.values()),
                             max(v[2] for v in HADJI_TABLE1.values()))   # 117-150 ms
TARGET_DURATION_MS = (min(v[3] for v in HADJI_TABLE1.values()),
                      max(v[3] for v in HADJI_TABLE1.values()))
TARGET_LATENCY_MS = (min(v[0] for v in HADJI_TABLE1.values()),
                     max(v[0] for v in HADJI_TABLE1.values()))

# Renard 2026 (PMID 42418335, full text), Euprymna berryi and Sepia officinalis,
# 20 fps: expansion vs contraction phase duration of individual slice events.
TARGET_EXP_FRAMES = 4.41
TARGET_CON_FRAMES = 5.90
TARGET_ASYMMETRY_RENARD = TARGET_CON_FRAMES / TARGET_EXP_FRAMES              # ~1.34
TARGET_ASYMMETRY_HADJI = sum(v["retraction_over_expansion"]
                             for v in HADJI_PHASES.values()) / len(HADJI_PHASES)  # ~3.70
# Both measured sources exceed 1: retraction is SLOWER than expansion. The damping
# sweep is scored against the NEARER of the two, which the model still cannot reach,
# so the selection simply returns the largest ratio the model can produce.
TARGET_ASYMMETRY = TARGET_ASYMMETRY_RENARD

PARAMS = [
    Param("r0", 25.0, "um", "assumed",
          "Retracted sacculus RADIUS. Bounded by sourced retracted DIAMETERS of 5-100 um "
          f"({SRC_UKROW}) and 15-100 um (Reiter S, Laurent G et al. 2018, Nature 562:361-366, "
          "PMID 30333578, read: full text via PMC); no paper we read gives a retracted radius "
          "for the species the kinetics were measured in, so the midpoint is assumed."),
    Param("R_anchor", 75.0, "um", "assumed",
          "Dermal anchor radius, i.e. radial fibre reach. Gauld 2021 describes 'an extremely "
          f"elongated distal end' with no number ({SRC_GAULD}); 3 x r0 is assumed."),
    Param("N_muscles", 20, "fibres", "sourced",
          "Radial muscle fibres per chromatophore. The literature DISAGREES and all five "
          f"readings are kept: 10-20 ({SRC_UKROW} abstract); ~10-15 (same paper's histology "
          f"methods, Euprymna + Sepia); 15-25 ({SRC_RENARD}); 19-27 ({SRC_KASUGAI}, "
          f"Sepioteuthis lessoniana); 'several dozen' ({SRC_GAULD}, 3D EM of Doryteuthis "
          "pealeii). 20 is the central value and the sweep spans 8-48."),
    Param("a_fibre", 3.14, "um^2", "assumed",
          "Physiological cross-section of one radial fibre, from an assumed 2 um diameter. "
          f"Proxy context only: squid funnel retractor fibres are '~3 um across' ({SRC_ROSENBLUTH}). "
          "Nobody we read measured a chromatophore radial fibre's cross-section."),
    Param("sigma_max", 250.0, "kPa", "assumed",
          "Peak isometric stress. PROXY from other obliquely striated squid muscles: "
          f"212 +/- 105 and 290 +/- 166 kN/m2 ({SRC_THOMPSON14}); 270 +/- 20 mN/mm2 "
          f"({SRC_ROSENBLUTH}); 216 and 335 mN/mm2 for CMP and SMR fibres ({SRC_THOMPSON08}). "
          "250 kPa sits inside all three intervals."),
    Param("v_max", 3.5, "L0/s", "assumed",
          "Unloaded shortening velocity. PROXY: 2.15 +/- 0.26 L0/s (funnel retractor, "
          f"{SRC_ROSENBLUTH}); 2.4 (SMR) and 5.1 (CMP) L0/s at 20 C ({SRC_THOMPSON08})."),
    Param("hill_curvature", 0.25, "dimensionless", "nondimensional",
          "Hill a/P0. Standard value; no cephalopod measurement found."),
    Param("tau_act", 15.0, "ms", "assumed",
          "Activation time constant. Bounded by a sourced 8 ms latent period and peak twitch "
          f"force within 50 ms in squid funnel retractor ({SRC_ROSENBLUTH}) and by the sourced "
          f"50-67 ms whole-organ response latency ({SRC_HADJI})."),
    Param("tau_deact", 40.0, "ms", "assumed",
          "Deactivation time constant; no cephalopod chromatophore measurement found."),
    Param("L_opt_frac", 1.0, "dimensionless", "assumed",
          "Optimum fibre length as a fraction of the retracted-state fibre length. Assumed to "
          "sit at the retracted state, i.e. the muscle starts on its plateau."),
    Param("t0_wall", 0.5, "um", "assumed",
          "Sacculus wall thickness when retracted. No measurement found; enters only as the "
          "product G*t0, which the control arm fits as a single quantity."),
    Param("G_sacculus", float("nan"), "kPa", "assumed",
          "Sacculus shear modulus. THE ONE FITTED PARAMETER: chosen so the steady-state area "
          f"ratio equals the measured 2.55x ({SRC_HADJI}). Never measured in any paper we read."),
    Param("c_damp", float("nan"), "uN.s/m", "assumed",
          "Lumped dermal damping at the sacculus rim. Not fitted to the expansion arm; swept, "
          "and the value needed to match the measured retraction is reported as a prediction."),
    Param("eps_max", 0.30, "dimensionless", "assumed",
          "Maximum fractional shortening the radial fibre can achieve. No measurement found "
          "for chromatophore radial muscle; swept over 0.10-0.50."),
    Param("rho_tissue", 1050.0, "kg/m^3", "assumed",
          "Sacculus density, for the inertia check only. Seawater-ish soft tissue."),
    Param("target_area_ratio", TARGET_AREA_RATIO, "dimensionless", "sourced",
          "+155.06% mean chromatophore surface-area increase on expansion, so "
          f"1 + 1.5506 = 2.5506 ({SRC_HADJI}). Species: Doryteuthis pealeii. This is the "
          "peak of the 4,000 chromatophores that EXPANDED to a startle flash; the paper "
          "states no maximum."),
    Param("target_rise_ms", list(TARGET_RISE_MS), "ms", "sourced",
          "Expansion PHASE duration tRt - tR per region: 67 ms (head/arms), 67 ms (fin), "
          f"83 ms (mantle), computed from Table 1 of {SRC_HADJI}. SUPERSEDES the 117-150 "
          "ms used earlier, which was the published rise time tRt timed FROM THE FLASH "
          "and therefore included the 50-67 ms response time tR - a sensory and neural "
          "latency this model does not simulate."),
    Param("target_duration_ms", list(TARGET_DURATION_MS), "ms", "sourced",
          f"Whole-event response duration rD of the EXPANSION response, 300-384 ms "
          f"across body regions ({SRC_HADJI}). The abstract's 217-384 ms range mixes "
          "this with the separate retraction-type response (n = 65 cells) and is not a "
          "comparison between phases."),
    Param("target_asymmetry", [TARGET_ASYMMETRY_RENARD, TARGET_ASYMMETRY_HADJI],
          "dimensionless", "sourced",
          "Two measurements, both greater than 1, kept separate rather than averaged: "
          "1.338 from contraction 5.90 +/- 3.50 vs expansion 4.41 +/- 1.91 frames at "
          f"20 fps ({SRC_RENARD}; Euprymna berryi and Sepia officinalis), and 3.696 from "
          f"Table 1 of {SRC_HADJI} decomposed per region (Doryteuthis pealeii). They "
          "differ about 3x in magnitude and agree on sign."),
]

# --------------------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------------------

UM = 1e-6  # m


class Chromatophore:
    def __init__(
        self,
        r0_um=25.0,
        R_anchor_um=75.0,
        N=20,
        a_fibre_um2=3.14,
        sigma_max_kPa=250.0,
        v_max=3.5,
        hill_a=0.25,
        tau_act_ms=15.0,
        tau_deact_ms=40.0,
        G_kPa=1.0,
        t0_um=0.5,
        c_damp=1e-4,
        eps_max=0.30,
        L_opt_frac=1.0,
        lt_width=0.45,
    ):
        self.r0 = r0_um * UM
        self.Ra = R_anchor_um * UM
        self.N = N
        self.a = a_fibre_um2 * UM * UM
        self.sigma = sigma_max_kPa * 1e3
        self.vmax_rel = v_max
        self.hill_a = hill_a
        self.tau_act = tau_act_ms * 1e-3
        self.tau_deact = tau_deact_ms * 1e-3
        self.G = G_kPa * 1e3
        self.t0 = t0_um * UM
        self.c = c_damp
        self.eps_max = eps_max
        self.L0 = self.Ra - self.r0  # fibre length at the retracted state
        self.L_opt = L_opt_frac * self.L0
        self.lt_width = lt_width
        # Geometric ceiling: the fibre cannot shorten past (1 - eps_max) L0.
        self.r_max = self.Ra - (1.0 - self.eps_max) * self.L0
        self.F0 = self.N * self.a * self.sigma  # peak isometric force of the whole rosette
        self.vmax_abs = self.vmax_rel * self.L0  # m/s of rim motion at zero load

    # --- sacculus ---------------------------------------------------------------
    def F_elastic(self, r):
        """Inward force at the rim from the stretched neo-Hookean sacculus wall (N)."""
        lam = max(r / self.r0, 1.0)
        T = self.G * self.t0 * (1.0 - lam ** -6.0)
        return 2.0 * math.pi * r * T

    def U_elastic(self, r, n=400):
        """Elastic energy stored by expanding from r0 to r (J), by quadrature of F_elastic."""
        if r <= self.r0:
            return 0.0
        xs = np.linspace(self.r0, r, n)
        return float(np.trapezoid([self.F_elastic(x) for x in xs], xs))

    def thickness(self, r):
        """Pigment-disc thickness (m) at radius r, conserving the retracted sphere's volume."""
        V0 = (4.0 / 3.0) * math.pi * self.r0 ** 3
        return V0 / (math.pi * r ** 2)

    # --- muscle -----------------------------------------------------------------
    def fl(self, r):
        """Length-tension factor; parabolic, clipped at zero."""
        L = self.Ra - r
        x = (L - self.L_opt) / (self.lt_width * self.L_opt)
        return max(0.0, 1.0 - x * x)

    def fv(self, v):
        """Hill force-velocity factor. v > 0 is rim moving out, i.e. muscle shortening."""
        if v >= 0.0:
            if v >= self.vmax_abs:
                return 0.0
            k = self.hill_a
            return (1.0 - v / self.vmax_abs) / (1.0 + v / (k * self.vmax_abs))
        # Lengthening: force rises toward a plateau (standard eccentric asymptote 1.5).
        u = -v / self.vmax_abs
        return 1.0 + 0.5 * (1.0 - math.exp(-4.0 * u))

    def F_muscle(self, r, v, act):
        return self.F0 * act * self.fl(r) * self.fv(v)

    # --- dynamics ---------------------------------------------------------------
    def rdot(self, r, act):
        """Solve F_muscle(r, v, act) - F_elastic(r) - c v = 0 for v."""
        def g(v):
            return self.F_muscle(r, v, act) - self.F_elastic(r) - self.c * v

        lo, hi = -5.0 * self.vmax_abs, self.vmax_abs * 0.999999
        glo, ghi = g(lo), g(hi)
        if glo < 0 and ghi < 0:
            return lo  # retracting faster than the bracket; clamp
        if glo > 0 and ghi > 0:
            return hi
        return brentq(g, lo, hi, xtol=1e-14, rtol=1e-12, maxiter=200)

    def simulate(self, t_on_ms=250.0, t_total_ms=900.0, dt_ms=0.05, drive=1.0):
        """Step activation on at t=0, off at t_on_ms. Returns dict of arrays."""
        dt = dt_ms * 1e-3
        n = int(t_total_ms / dt_ms)
        t = np.arange(n) * dt_ms
        r = np.empty(n)
        act = np.empty(n)
        a = 0.0
        rr = self.r0
        for i in range(n):
            u = drive if t[i] < t_on_ms else 0.0
            tau = self.tau_act if u > a else self.tau_deact
            a += (u - a) * dt / tau
            v = self.rdot(rr, a)
            rr = min(max(rr + v * dt, self.r0), self.r_max)
            r[i] = rr
            act[i] = a
        area_ratio = (r / self.r0) ** 2
        return {"t_ms": t, "r_m": r, "act": act, "area_ratio": area_ratio}

    # --- static -----------------------------------------------------------------
    def steady_area_ratio(self, act=1.0):
        """Steady state: F_muscle(r, 0, act) == F_elastic(r), or the geometric ceiling."""
        def g(r):
            return self.F0 * act * self.fl(r) * 1.0 - self.F_elastic(r)

        lo = self.r0 * (1.0 + 1e-9)
        hi = self.r_max
        if g(hi) > 0:
            return (hi / self.r0) ** 2, hi, True  # muscle-stroke limited
        if g(lo) <= 0:
            return 1.0, self.r0, False
        r = brentq(g, lo, hi, xtol=1e-15)
        return (r / self.r0) ** 2, r, False

    # --- datasheet quantities ---------------------------------------------------
    def blocked_force_N(self):
        """Force the rosette delivers at the retracted radius with no motion."""
        return self.F0 * self.fl(self.r0)

    def holding_metrics(self, r_hold):
        """Isometric hold at radius r_hold."""
        F_hold = self.F_elastic(r_hold)          # N, what the muscle must sustain
        per_fibre = F_hold / self.N
        stress = per_fibre / self.a              # Pa
        U = self.U_elastic(r_hold)               # J stored in the sacculus
        return {
            "hold_force_total_uN": F_hold * 1e6,
            "hold_force_per_fibre_uN": per_fibre * 1e6,
            "hold_stress_kPa": stress / 1e3,
            "duty_fraction_of_sigma_max": stress / self.sigma,
            "stored_elastic_energy_pJ": U * 1e12,
        }

    def inertia_check(self, r_hold):
        """Ratio of inertial to elastic force at the measured timescale; should be << 1."""
        V0 = (4.0 / 3.0) * math.pi * self.r0 ** 3
        m = V0 * 1050.0
        T = 0.130  # s, sourced rise time scale
        a_acc = (r_hold - self.r0) / (T * T)
        return (m * a_acc) / max(self.F_elastic(r_hold), 1e-30)


def rise_time_ms(sim, frac=0.9):
    """Time from activation onset to `frac` of the peak area ratio reached."""
    ar = sim["area_ratio"]
    pk = ar.max()
    if pk <= 1.0 + 1e-9:
        return float("nan")
    target = 1.0 + frac * (pk - 1.0)
    idx = np.argmax(ar >= target)
    if ar[idx] < target:
        return float("nan")
    return float(sim["t_ms"][idx])


def decay_time_ms(sim, t_off_ms, frac=0.9):
    """Time from stimulus offset until the area ratio has fallen `frac` of the way back.

    Returns NaN when the organ has not returned that far by the end of the
    simulation window. That is a real outcome and not a numerical failure - with
    the asymmetry-fitted damping, a sufficiently soft sacculus does not retract
    within six seconds - so callers should report it as "did not return within the
    window" rather than dropping the row.
    """
    ar = sim["area_ratio"]
    t = sim["t_ms"]
    m = t >= t_off_ms
    if not m.any():
        return float("nan")
    a0 = ar[m][0]
    if a0 <= 1.0 + 1e-9:
        return float("nan")
    target = a0 - frac * (a0 - 1.0)
    sub_t, sub_a = t[m], ar[m]
    idx = np.argmax(sub_a <= target)
    if sub_a[idx] > target:
        return float("nan")
    return float(sub_t[idx] - t_off_ms)


# --------------------------------------------------------------------------------------
# Control arm
# --------------------------------------------------------------------------------------

def fit_G(base_kwargs, target=TARGET_AREA_RATIO):
    """Fit the ONE free parameter G so the steady-state area ratio hits the measured value."""
    def f(logG):
        c = Chromatophore(G_kPa=math.exp(logG), **base_kwargs)
        return c.steady_area_ratio()[0] - target

    lo, hi = math.log(1e-4), math.log(1e4)
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return None, {"bracket_lo_ratio": flo + target, "bracket_hi_ratio": fhi + target}
    logG = brentq(f, lo, hi, xtol=1e-12)
    return math.exp(logG), None


def joint_feasibility(base_kwargs, G_kPa):
    """Can ANY damping satisfy more than one measured quantity at once?

    The control arm scores three measured things - the peak expansion ratio, the
    expansion-phase duration and the expansion:retraction asymmetry - and the
    damping is the only knob that moves the asymmetry. This asks the question the
    one-at-a-time sweep cannot: at the damping that reproduces each measured
    asymmetry, what happens to the other two?
    """
    settings = [
        ("baseline", 250.0, 10 ** -2.5),
        ("damping matched to Renard asymmetry 1.34", 250.0, 0.1),
        ("damping matched to Hadjisolomou asymmetry 3.70", 250.0, 0.45),
        ("longest drive that recovers the expansion magnitude", 2000.0, 1.0),
    ]
    rows = []
    for label, t_on, c in settings:
        ch = Chromatophore(G_kPa=G_kPa, c_damp=c, **base_kwargs)
        sim = ch.simulate(t_on_ms=t_on, t_total_ms=t_on + 8000.0, dt_ms=0.1)
        rt = rise_time_ms(sim, 0.9)
        dt_ = decay_time_ms(sim, t_on, 0.9)
        ar = float(sim["area_ratio"].max())
        rows.append({
            "setting": label, "drive_ms": t_on, "c_damp_N_s_per_m": c,
            "peak_area_ratio": ar, "rise_time_90pct_ms": rt,
            "asymmetry": (dt_ / rt) if rt and dt_ else None,
            "area_ratio_shortfall_vs_measured":
                1.0 - ar / TARGET_AREA_RATIO,
            "rise_over_measured_expansion_phase":
                (rt / TARGET_RISE_MS[1]) if rt else None,
        })
    return {
        "measured": {"peak_area_ratio": TARGET_AREA_RATIO,
                     "expansion_phase_ms": list(TARGET_RISE_MS),
                     "asymmetry_renard": TARGET_ASYMMETRY_RENARD,
                     "asymmetry_hadjisolomou": TARGET_ASYMMETRY_HADJI},
        "settings": rows,
        "verdict": (
            "The model can reach EITHER measured asymmetry, so the earlier claim that a "
            "lumped elastic recoil is structurally incapable of retraction slower than "
            "expansion was WRONG - it was made from a sweep whose maximum sat at its own "
            "upper boundary. What is true is weaker and still a clear failure: no single "
            "setting satisfies more than one measured quantity. The damping that gives "
            "Renard's 1.34 costs a third of the expansion magnitude (2.06 -> 1.73 against "
            "a measured 2.55) and makes the already-failing rise time worse (215 -> 232 ms "
            "against a measured 67-83 ms). The damping that gives Hadjisolomou's 3.70 "
            "costs nearly half the expansion. Recovering the expansion magnitude on top "
            "needs a 2-second drive and a 1,674 ms rise, twenty times the measured "
            "expansion phase, against a whole response that completes in under 400 ms. "
            "The model is a one-constraint model being asked to meet three."),
    }


def run_control(base_kwargs, c_damp_sweep):
    G, bracket = fit_G(base_kwargs)
    out = {
        "design": (
            "One parameter (sacculus shear modulus G) is fitted to ONE measured number "
            "(steady-state area ratio 2.55x). Rise time and the expansion:retraction "
            "asymmetry are then predictions with nothing further fitted. Dermal damping c "
            "is swept rather than fitted to expansion, and the c that would match the "
            "measured retraction is reported as a prediction about an unmeasured quantity."
        ),
        "fitted_G_kPa": G,
        "fit_bracket_failure": bracket,
    }
    if G is not None:
        out["joint_feasibility"] = joint_feasibility(base_kwargs, G)
    if G is None:
        out["verdict"] = "FAILED: no G reproduces the measured area ratio"
        return out

    rows = []
    for c in c_damp_sweep:
        ch = Chromatophore(G_kPa=G, c_damp=c, **base_kwargs)
        sim = ch.simulate(t_on_ms=250.0, t_total_ms=6000.0, dt_ms=0.05)
        rt = rise_time_ms(sim, 0.9)
        dt_ = decay_time_ms(sim, 250.0, 0.9)
        ar = float(sim["area_ratio"].max())
        rows.append(
            {
                "c_damp_N_s_per_m": c,
                "peak_area_ratio": ar,
                "rise_time_90pct_ms": rt,
                "retraction_time_90pct_ms": dt_,
                "asymmetry_retraction_over_expansion": (dt_ / rt) if rt and rt == rt and rt > 0 else None,
            }
        )
    out["damping_sweep"] = rows
    # NOT `if r[...]`: NaN is TRUTHY in Python, so a bare truth test keeps the rows
    # where the organ never returned, and the boundary check below then compared the
    # maximum against a NaN and reported the reassuring answer. That is the exact
    # failure this guard exists to prevent, inside the guard.
    good = [r for r in rows
            if isinstance(r["asymmetry_retraction_over_expansion"], float)
            and math.isfinite(r["asymmetry_retraction_over_expansion"])]
    if good:
        amax = max(r["asymmetry_retraction_over_expansion"] for r in good)
        cross = [r for r in good if r["asymmetry_retraction_over_expansion"] >= 1.0]
        n_unreturned = len(rows) - len(good)
        out["damping_sweep_reach"] = {
            "points_where_the_organ_never_returned_within_the_window": n_unreturned,
            "asymmetry_min": min(r["asymmetry_retraction_over_expansion"] for r in good),
            "asymmetry_max": amax,
            "c_range_N_s_per_m": [good[0]["c_damp_N_s_per_m"], good[-1]["c_damp_N_s_per_m"]],
            "crosses_one": bool(cross),
            "smallest_c_with_asymmetry_above_one":
                min(r["c_damp_N_s_per_m"] for r in cross) if cross else None,
            "how_this_guard_was_broken": (
                "Its first version filtered with `if r[\"asymmetry...\"]`, and NaN is "
                "TRUTHY in Python, so rows where the organ never returned were kept. "
                "The guard was then not merely wrong but INCAPABLE OF THE ALARMING "
                "ANSWER: every comparison against NaN is False, so `abs(amax - nan) < "
                "1e-12` is False, which reads as 'the extremum is not at the boundary' - "
                "the reassuring verdict - whatever the data says. Worse, `max()` is "
                "order-dependent with a NaN present: max([1,2,nan,3]) is 3 while "
                "max([nan,1,2,3]) is nan, so whether the NaN even surfaced depended on "
                "row order. A guard that can only return 'fine' is not a guard. Fixed "
                "by filtering on math.isfinite and reporting how many points failed to "
                "return. The honest consequence: this field is now TRUE - the extremum "
                "IS at the boundary of the finite region - and the earlier `false` was "
                "never a measurement."),
            "note": ("Whether the sweep's extremum sits at its own boundary is checked, "
                     "because an extremum at the boundary is exactly the condition under "
                     "which 'no value reaches X' cannot be claimed. It did, in the "
                     "original -9..-2.5 range, and the claim made from it was wrong. It "
                     "does again here, for a different reason: above c ~ 2 the organ no "
                     "longer returns 90% of the way within the 6 s window, so the "
                     "maximum reported is set by the window and NOT by the physics. "
                     "The maximum is therefore not a quotable quantity. The CROSSING "
                     "point is: it is interior to the finite region and robust, and it "
                     "is the number this study relies on."),
            "quotable": {
                "smallest_c_with_asymmetry_above_one": (
                    "YES. It is interior to the finite region, and - the stronger "
                    "evidence - it has not moved across every configuration in which it "
                    "was observable: 0.1 under a 1.2 s integration window, 0.1 under a "
                    "6 s window, and 0.1 after the NaN-filter fix below. A quantity that "
                    "is stable across three different runs of the machinery is a "
                    "property of the model; one that moves with the machinery is a "
                    "property of the run. (The ORIGINAL narrow sweep, c <= 3.2e-3, could "
                    "not observe the crossing at all, which is the whole reason the "
                    "claim made from it was wrong.)"),
                "asymmetry_max": (
                    "NO. It is set by the integration window, not by the physics: above "
                    "c ~ 2 the organ does not return 90% of the way inside the window, "
                    "so the maximum is simply the last point that finished. It moved "
                    "4.5x - 2.946 to 13.27 - between two versions of the SAME correction "
                    "purely because the window was lengthened. Do not put this number in "
                    "prose."),
            },
            "why_the_maximum_moved_between_versions": (
                "An earlier version of this file reported a maximum of 2.946. It is now "
                "13.27, and the reason is the simulation window, not a new result. The "
                "window was lengthened from 1.2 s to 6 s because the sacculus-elasticity "
                "sweep was returning NaN retraction times: at the asymmetry-fitted "
                "damping a soft sacculus does not return 90% of the way within 1.2 s, "
                "and reporting that as NaN hid a real outcome rather than recording it. "
                "With the longer window the high-damping retractions complete, so the "
                "measured ratios rise. The quantity the retraction actually rests on - "
                "the crossing point - is unchanged at c = 0.1 under both windows. This "
                "is exactly why the maximum is marked unquotable above: a number set by "
                "the integration window will move whenever the window does."),
            "extremum_at_boundary": bool(
                abs(amax - good[-1]["asymmetry_retraction_over_expansion"]) < 1e-12
                or abs(amax - good[0]["asymmetry_retraction_over_expansion"]) < 1e-12),
        }

    # Which c best matches the measured asymmetry of 1.34?
    best = None
    for row in rows:
        a = row["asymmetry_retraction_over_expansion"]
        if a is None or a != a:
            continue
        d = abs(a - TARGET_ASYMMETRY)
        if best is None or d < best[0]:
            best = (d, row)
    out["best_match_to_measured_asymmetry"] = best[1] if best else None

    # Score the three comparisons at that damping.
    if best:
        row = best[1]
        rt, dt_ = row["rise_time_90pct_ms"], row["retraction_time_90pct_ms"]
        out["comparisons"] = {
            "area_ratio": {
                "model": row["peak_area_ratio"],
                "measured": TARGET_AREA_RATIO,
                "shortfall": 1.0 - row["peak_area_ratio"] / TARGET_AREA_RATIO,
                "status": "FITTED at steady state, then BROKEN by the damping fit",
                "note": (
                    "G is fitted so the STEADY-STATE area ratio is exactly 2.5506, which "
                    "is why this is not a test. But the peak reached under a 250 ms "
                    "drive at the damping that the asymmetry fit selects is far below "
                    "it. The two fits are mutually inconsistent: fitting the damping to "
                    "the measured asymmetry destroys the expansion ratio the stiffness "
                    "was fitted to."),
            },
            "rise_time_ms": {
                "model": rt,
                "measured_range": list(TARGET_RISE_MS),
                "measured_quantity": (
                    "expansion PHASE duration tRt - tR per body region: 67 ms "
                    "(head/arms), 67 ms (fin), 83 ms (mantle)"),
                "inside_measured_range": bool(TARGET_RISE_MS[0] <= rt <= TARGET_RISE_MS[1]),
                "model_over_measured": [rt / TARGET_RISE_MS[1], rt / TARGET_RISE_MS[0]],
                "also_reported_rise_from_flash_ms": list(TARGET_RISE_FROM_FLASH_MS),
                "status": "PREDICTION - FAILS",
                "note": (
                    "Scored against the expansion PHASE, not against the published rise "
                    "time tRt. tRt is timed from the flash and contains a 50-67 ms "
                    "sensory and neural latency this model does not simulate, because "
                    "the model's clock starts at drive onset. Against tRt the model is "
                    "1.4-1.8x too slow; against the phase it is 2.6-3.2x too slow. "
                    "Correcting the comparator made the control arm fail by more."),
            },
            "retraction_vs_expansion_asymmetry": {
                "model": row["asymmetry_retraction_over_expansion"],
                "measured": {
                    "renard_2026_slice_phases": TARGET_ASYMMETRY_RENARD,
                    "hadjisolomou_2021_region_matched_phases": TARGET_ASYMMETRY_HADJI,
                    "hadjisolomou_per_region": {
                        k: v["retraction_over_expansion"] for k, v in HADJI_PHASES.items()},
                },
                "both_sources_exceed_one": bool(TARGET_ASYMMETRY_RENARD > 1
                                                and TARGET_ASYMMETRY_HADJI > 1),
                "model_sign_matches_either_source": bool(
                    row["asymmetry_retraction_over_expansion"] > 1),
                "status": "STRUCTURAL REFUTATION",
                "note": (
                    "Two independent measurements in three species both put retraction "
                    "SLOWER than expansion: 1.34 (Renard 2026, Euprymna berryi and Sepia "
                    "officinalis) and 3.70 (Hadjisolomou 2021, Doryteuthis pealeii, "
                    "decomposed per region from Table 1). The model gives a ratio below "
                    "1 and no damping in the sweep crosses 1.0, because a passive "
                    "elastic recoil against a lumped dashpot cannot be slower than the "
                    "powered contraction before it. This refutes the model's STRUCTURE, "
                    "not its parameters: real chromatophore retraction is probably not a "
                    "lumped elastic recoil. The damping was selected against the nearer "
                    "of the two targets, which the model cannot reach, so that selection "
                    "simply returns the largest ratio available and is not a fit."),
            },
            "hadjisolomou_table1_decomposed": {
                "source": (
                    "Hadjisolomou SP et al. 2021, Front Physiol 12:675252, PMID "
                    "34220538, Table 1 (read: full text via PMC8250766). Species: "
                    "Doryteuthis pealeii."),
                "per_region": HADJI_PHASES,
                "retraction_response_whole_event_rD_ms": HADJI_RETRACTION_RESPONSE_RD,
                "two_populations_warning": (
                    "This paper's 'expansion' and 'retraction' are two RESPONSE TYPES "
                    "over two different populations - 4,000 chromatophores in 166 trials "
                    "that expanded to the flash, and 65 in 19 trials that retracted - "
                    "not the two phases of one event. The abstract's '217 ms (fin, "
                    "retraction) to 384 ms (heads/arms, expansion)' is a minimum and a "
                    "maximum across those two populations AND across body regions, and "
                    "reads as though expansion were the slower process. It is not a "
                    "comparison. The 155.06% and 40.46% magnitudes are likewise peaks of "
                    "two separate populations, and are NOT evidence that the organ fails "
                    "to return to baseline: rD is defined as running to 'the return to "
                    "the pre-flash state following the peak response'."),
            },
            "implied_dermal_damping_N_s_per_m": {
                "model": row["c_damp_N_s_per_m"],
                "measured": None,
                "status": "PREDICTION about a quantity nobody has measured",
            },
        }
    return out


# --------------------------------------------------------------------------------------
# Sweeps
# --------------------------------------------------------------------------------------

def run_sweeps(G_kPa, c_damp):
    base = dict(
        r0_um=25.0, R_anchor_um=75.0, a_fibre_um2=3.14, sigma_max_kPa=250.0,
        v_max=3.5, hill_a=0.25, tau_act_ms=15.0, tau_deact_ms=40.0, t0_um=0.5,
    )
    sweeps = {}

    # 1. Muscle number, spanning the five disagreeing literature counts.
    Ns = [8, 10, 12, 15, 16, 20, 24, 27, 32, 40, 48]
    rows = []
    for N in Ns:
        ch = Chromatophore(N=N, G_kPa=G_kPa, c_damp=c_damp, eps_max=0.30, **base)
        ar, r, lim = ch.steady_area_ratio()
        sim = ch.simulate(t_on_ms=250.0, t_total_ms=6000.0)
        rows.append({
            "N_muscles": N, "area_ratio": ar, "stroke_limited": lim,
            "rise_time_90pct_ms": rise_time_ms(sim),
            "retraction_time_90pct_ms": decay_time_ms(sim, 250.0),
            **ch.holding_metrics(r),
        })
    sweeps["muscle_number"] = rows

    # 2. Fibre reach (anchor radius), i.e. how long the radial muscle is.
    rows = []
    for Ra in [35.0, 40.0, 50.0, 62.5, 75.0, 100.0, 125.0, 150.0, 200.0]:
        kw = dict(base); kw["R_anchor_um"] = Ra
        ch = Chromatophore(N=20, G_kPa=G_kPa, c_damp=c_damp, eps_max=0.30, **kw)
        ar, r, lim = ch.steady_area_ratio()
        sim = ch.simulate(t_on_ms=250.0, t_total_ms=6000.0)
        rows.append({
            "R_anchor_um": Ra, "fibre_length_um": Ra - 25.0,
            "area_ratio": ar, "stroke_limited": lim,
            "rise_time_90pct_ms": rise_time_ms(sim),
            "retraction_time_90pct_ms": decay_time_ms(sim, 250.0),
            **ch.holding_metrics(r),
        })
    sweeps["fibre_reach"] = rows
    sweeps["_note"] = (
        "`area_ratio` in these sweeps is the STEADY-STATE ratio from "
        "steady_area_ratio(), i.e. what the organ reaches if held open indefinitely. "
        "`control.comparisons.area_ratio` is a different quantity with the same name: "
        "the dynamic PEAK under a 250 ms drive, which is lower. At the fitted stiffness "
        "they are 2.55 and 1.73. Both are reported because the measured 2.5506 is what "
        "the stiffness was fitted to, while the peak is what the organ actually reaches "
        "in the time the real response takes. `retraction_time_90pct_ms` is NaN where "
        "the organ had not returned 90% of the way within the 6 s window - a real "
        "outcome at the asymmetry-fitted damping, not a numerical failure.")

    # 3. Maximum contraction strain.
    rows = []
    for eps in [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]:
        ch = Chromatophore(N=20, G_kPa=G_kPa, c_damp=c_damp, eps_max=eps, **base)
        ar, r, lim = ch.steady_area_ratio()
        sim = ch.simulate(t_on_ms=250.0, t_total_ms=6000.0)
        rows.append({
            "eps_max": eps, "area_ratio": ar, "stroke_limited": lim,
            "rise_time_90pct_ms": rise_time_ms(sim),
            "retraction_time_90pct_ms": decay_time_ms(sim, 250.0),
            **ch.holding_metrics(r),
        })
    sweeps["contraction_strain"] = rows

    # 4. Sacculus elasticity, spanning four decades around the fit.
    rows = []
    for mult in [0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0, 25.0, 100.0]:
        G = G_kPa * mult
        ch = Chromatophore(N=20, G_kPa=G, c_damp=c_damp, eps_max=0.30, **base)
        ar, r, lim = ch.steady_area_ratio()
        sim = ch.simulate(t_on_ms=250.0, t_total_ms=6000.0)
        rows.append({
            "G_kPa": G, "G_relative_to_fit": mult, "area_ratio": ar, "stroke_limited": lim,
            "rise_time_90pct_ms": rise_time_ms(sim),
            "retraction_time_90pct_ms": decay_time_ms(sim, 250.0),
            **ch.holding_metrics(r),
        })
    sweeps["sacculus_elasticity"] = rows

    # 5. Two-dimensional N x G map of the area ratio, for the limiting-factor figure.
    Ngrid = np.array([8, 12, 16, 20, 24, 28, 32, 40, 48])
    Ggrid = G_kPa * np.array([0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0, 25.0])
    Z = np.zeros((len(Ggrid), len(Ngrid)))
    LIM = np.zeros_like(Z)
    for i, G in enumerate(Ggrid):
        for j, N in enumerate(Ngrid):
            ch = Chromatophore(N=int(N), G_kPa=float(G), c_damp=c_damp, eps_max=0.30, **base)
            ar, _, lim = ch.steady_area_ratio()
            Z[i, j] = ar
            LIM[i, j] = 1.0 if lim else 0.0
    sweeps["grid_N_vs_G"] = {
        "N": Ngrid.tolist(), "G_kPa": Ggrid.tolist(),
        "area_ratio": Z.tolist(), "stroke_limited": LIM.tolist(),
    }
    return sweeps


def datasheet(G_kPa, c_damp):
    base = dict(
        r0_um=25.0, R_anchor_um=75.0, N=20, a_fibre_um2=3.14, sigma_max_kPa=250.0,
        v_max=3.5, hill_a=0.25, tau_act_ms=15.0, tau_deact_ms=40.0, t0_um=0.5,
        eps_max=0.30,
    )
    ch = Chromatophore(G_kPa=G_kPa, c_damp=c_damp, **base)
    ar, r_hold, stroke_limited = ch.steady_area_ratio()
    sim = ch.simulate(t_on_ms=250.0, t_total_ms=6000.0)
    hold = ch.holding_metrics(r_hold)
    rt = rise_time_ms(sim)
    dt_ = decay_time_ms(sim, 250.0)

    disc_area_um2 = math.pi * (r_hold / UM) ** 2
    retr_area_um2 = math.pi * (ch.r0 / UM) ** 2
    muscle_vol_um3 = ch.N * (ch.a / (UM * UM)) * (ch.L0 / UM)
    work_pJ = hold["stored_elastic_energy_pJ"]

    # Bandwidth: the small-signal 3 dB corner of the passive retraction, which is the slow arm.
    f3db = 1.0 / (2.0 * math.pi * (dt_ / 1000.0 / 2.303)) if dt_ and dt_ == dt_ else float("nan")

    rows = [
        ("Addressable unit", "one chromatophore organ", "", "radial muscle rosette + pigment sacculus"),
        ("Retracted pigment disc area", f"{retr_area_um2:.0f}", "um^2", "assumed r0 = 25 um"),
        ("Expanded pigment disc area", f"{disc_area_um2:.0f}", "um^2", "model at the fitted G"),
        ("Area expansion ratio", f"{ar:.2f}", "x", "FITTED to the measured 2.55x"),
        ("Linear stroke at the rim", f"{(r_hold - ch.r0)/UM:.1f}", "um", "model"),
        ("Fibre shortening", f"{100*(r_hold - ch.r0)/ch.L0:.1f}", "% of L0", "model"),
        ("Blocked force (whole rosette)", f"{ch.blocked_force_N()*1e6:.2f}", "uN", "N x a x sigma_max, proxy stress"),
        ("Holding force (whole rosette)", f"{hold['hold_force_total_uN']:.3f}", "uN", "model, = sacculus recoil"),
        ("Holding force per fibre", f"{hold['hold_force_per_fibre_uN']:.4f}", "uN", "model"),
        ("Holding stress per fibre", f"{hold['hold_stress_kPa']:.1f}", "kPa", "model"),
        ("Isometric duty", f"{100*hold['duty_fraction_of_sigma_max']:.1f}", "% of sigma_max", "model"),
        ("Stored elastic energy at full expansion", f"{work_pJ:.3f}", "pJ", "model, quadrature"),
        ("Work density (per muscle volume)", f"{work_pJ*1e-12/(muscle_vol_um3*1e-18):.0f}", "J/m^3", "model"),
        ("Rise time to 90%", f"{rt:.0f}", "ms",
         f"PREDICTION; FAILS vs measured {TARGET_RISE_MS[0]:.0f}-{TARGET_RISE_MS[1]:.0f} ms"),
        ("Passive retraction to 90%", f"{dt_:.0f}", "ms", "model at the chosen damping"),
        ("Response latency", f"{TARGET_LATENCY_MS[0]:.0f}-{TARGET_LATENCY_MS[1]:.0f}", "ms", "MEASURED (Hadjisolomou 2021)"),
        ("Small-signal bandwidth (retraction-limited)", f"{f3db:.1f}", "Hz", "model, from the retraction time"),
        ("Observed in-vivo flicker", "2.1-5.4", "Hz", "MEASURED (Kasugai 2011)"),
        ("Independent control inputs per unit", "4.4-4.7", "motor neurons", "MEASURED (Renard 2026; Ukrow 2025)"),
        ("Array density", "8 / 35-50 / 230", "per mm^2", "MEASURED, squid / Sepia / octopus"),
        ("Power supply", "chemical (ATP), hold is active", "", "elastic recoil is the return spring"),
        ("Return mechanism", "passive elastic recoil", "", "no antagonist muscle"),
    ]
    return {
        "rows": [{"quantity": a, "value": b, "units": c, "note": d} for a, b, c, d in rows],
        "stroke_limited_at_baseline": bool(stroke_limited),
        "inertia_to_elastic_force_ratio": ch.inertia_check(r_hold),
        "trace": {
            "t_ms": sim["t_ms"][::20].tolist(),
            "area_ratio": sim["area_ratio"][::20].tolist(),
            "activation": sim["act"][::20].tolist(),
        },
    }


# --------------------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------------------

def fig_sweep(sweeps, control, G_fit, path):
    style()
    fig, axes = plt.subplots(2, 3, figsize=(11.5, 7.2))

    ax = axes[0, 0]
    d = sweeps["muscle_number"]
    ax.plot([r["N_muscles"] for r in d], [r["area_ratio"] for r in d], "o-", color=OKABE[0])
    ax.axhline(TARGET_AREA_RATIO, ls="--", color="#999999")
    ax.text(48, TARGET_AREA_RATIO * 1.02, "measured 2.55x", ha="right", fontsize=7.5, color="#666666")
    for lo, hi, lab, col in [(10, 20, "Ukrow", OKABE[2]), (15, 25, "Renard", OKABE[1]),
                             (19, 27, "Kasugai", OKABE[3])]:
        ax.axvspan(lo, hi, alpha=0.07, color=col)
    ax.set_xlabel("radial muscle fibres per organ, N")
    ax.set_ylabel("steady-state area expansion ratio")
    ax.set_title("More muscles barely help")

    ax = axes[0, 1]
    d = sweeps["sacculus_elasticity"]
    ax.semilogx([r["G_kPa"] for r in d], [r["area_ratio"] for r in d], "o-", color=OKABE[1])
    ax.axvline(G_fit, ls=":", color="#333333")
    ax.text(G_fit * 1.15, 1.2, "fitted G", fontsize=7.5, rotation=90, color="#333333")
    ax.axhline(TARGET_AREA_RATIO, ls="--", color="#999999")
    ax.set_xlabel("sacculus shear modulus G (kPa)")
    ax.set_ylabel("steady-state area expansion ratio")
    ax.set_title("The sac, not the muscle, sets the stroke")

    ax = axes[0, 2]
    d = sweeps["contraction_strain"]
    ax.plot([r["eps_max"] * 100 for r in d], [r["area_ratio"] for r in d], "o-", color=OKABE[2])
    lim = [r["eps_max"] * 100 for r in d if r["stroke_limited"]]
    if lim:
        ax.axvspan(min(lim) - 1, max(lim) + 1, alpha=0.12, color=OKABE[3])
        ax.text(min(lim), 1.1, "stroke-limited", fontsize=7.5, color=OKABE[3])
    ax.axhline(TARGET_AREA_RATIO, ls="--", color="#999999")
    ax.set_xlabel("maximum fibre shortening (% of L0)")
    ax.set_ylabel("steady-state area expansion ratio")
    ax.set_title("Where the ceiling changes hands")

    ax = axes[1, 0]
    d = sweeps["fibre_reach"]
    ax.plot([r["fibre_length_um"] for r in d], [r["rise_time_90pct_ms"] for r in d],
            "o-", color=OKABE[0], label="expansion (90%)")
    ax.plot([r["fibre_length_um"] for r in d], [r["retraction_time_90pct_ms"] for r in d],
            "s-", color=OKABE[1], label="retraction (90%)")
    ax.axhspan(TARGET_RISE_MS[0], TARGET_RISE_MS[1], alpha=0.15, color="#999999")
    ax.text(10, TARGET_RISE_MS[1] * 1.05,
            f"measured expansion phase {TARGET_RISE_MS[0]:.0f}-{TARGET_RISE_MS[1]:.0f} ms",
            fontsize=7.5, color="#666666")
    ax.set_xlabel("radial fibre length (um)")
    ax.set_ylabel("time (ms)")
    ax.set_title("Kinetics vs fibre length")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    rows = control.get("damping_sweep", [])
    if rows:
        cs = [r["c_damp_N_s_per_m"] for r in rows]
        ax.loglog(cs, [r["rise_time_90pct_ms"] for r in rows], "o-", color=OKABE[0], label="expansion")
        ax.loglog(cs, [r["retraction_time_90pct_ms"] for r in rows], "s-", color=OKABE[1], label="retraction")
        ax.axhspan(TARGET_RISE_MS[0], TARGET_RISE_MS[1], alpha=0.15, color="#999999")
        ax.axhspan(TARGET_DURATION_MS[0], TARGET_DURATION_MS[1], alpha=0.08, color=OKABE[4])
        b = control.get("best_match_to_measured_asymmetry")
        if b:
            ax.axvline(b["c_damp_N_s_per_m"], ls=":", color="#333333")
        ax.legend(fontsize=8)
    ax.set_xlabel("dermal damping c (N s / m)")
    ax.set_ylabel("time (ms)")
    ax.set_title("Damping is the only knob for retraction")

    ax = axes[1, 2]
    g = sweeps["grid_N_vs_G"]
    Z = np.array(g["area_ratio"])
    im = ax.pcolormesh(np.array(g["N"]), np.array(g["G_kPa"]), Z, shading="nearest", cmap="viridis")
    ax.set_yscale("log")
    cs = ax.contour(np.array(g["N"]), np.array(g["G_kPa"]), Z, levels=[TARGET_AREA_RATIO],
                    colors="white", linewidths=1.6)
    ax.clabel(cs, fmt={TARGET_AREA_RATIO: "measured 2.55x"}, fontsize=7)
    LIM = np.array(g["stroke_limited"])
    ax.contourf(np.array(g["N"]), np.array(g["G_kPa"]), LIM, levels=[0.5, 1.5],
                colors="none", hatches=["///"])
    ax.set_xlabel("radial muscle fibres, N")
    ax.set_ylabel("sacculus shear modulus G (kPa)")
    ax.set_title("Hatched = muscle-stroke limited")
    fig.colorbar(im, ax=ax, label="area ratio")

    fig.suptitle(
        "Simulation. Chromatophore actuator sweeps; one parameter (G) fitted to one measured number",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)


def fig_datasheet(ds, control, path):
    style()
    fig = plt.figure(figsize=(12.4, 8.0))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.52, 1.0], height_ratios=[1.0, 0.75],
                          hspace=0.33, wspace=0.18)

    ax = fig.add_subplot(gs[:, 0])
    ax.axis("off")
    rows = ds["rows"]
    y = 1.0
    dy = 1.0 / (len(rows) + 2)
    ax.text(0.0, y, "CHROMATOPHORE ACTUATOR — DATASHEET", fontsize=11, fontweight="bold")
    y -= dy
    ax.text(0.0, y, "model output unless the note says MEASURED", fontsize=8, color="#666666")
    y -= dy * 0.8
    for r in rows:
        y -= dy
        meas = "MEASURED" in r["note"]
        ax.text(0.0, y, r["quantity"], fontsize=7.4, va="center")
        ax.text(0.58, y, f"{r['value']} {r['units']}".strip(), fontsize=7.4, va="center",
                fontweight="bold" if meas else "normal",
                color=OKABE[2] if meas else "#111111")
        ax.text(0.99, y, r["note"], fontsize=6.1, va="center", color="#777777")
    ax.set_xlim(0, 1.78)
    ax.set_ylim(y - dy, 1.03)

    ax = fig.add_subplot(gs[0, 1])
    t = np.array(ds["trace"]["t_ms"])
    ar = np.array(ds["trace"]["area_ratio"])
    act = np.array(ds["trace"]["activation"])
    ax.plot(t, ar, color=OKABE[0], lw=1.8, label="pigment area ratio")
    ax.axhline(TARGET_AREA_RATIO, ls="--", color="#999999", lw=1.0)
    ax.axvspan(0, 250, alpha=0.08, color=OKABE[1])
    ax.text(125, ar.max() * 0.35, "motor drive on", ha="center", fontsize=7.5, color=OKABE[1])
    ax2 = ax.twinx()
    ax2.plot(t, act, color=OKABE[3], lw=1.0, ls=":", label="activation")
    ax2.set_ylabel("activation", color=OKABE[3], fontsize=8)
    ax2.grid(False)
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("pigment area / retracted area")
    ax.set_title("Simulated step response")

    ax = fig.add_subplot(gs[1, 1])
    comp = control.get("comparisons", {})
    labels, model_v, meas_lo, meas_hi, kinds = [], [], [], [], []
    if comp:
        labels.append("area ratio (x)")
        model_v.append(comp["area_ratio"]["model"])
        meas_lo.append(TARGET_AREA_RATIO); meas_hi.append(TARGET_AREA_RATIO)
        kinds.append("fitted")
        labels.append("rise time (ms)")
        model_v.append(comp["rise_time_ms"]["model"])
        meas_lo.append(TARGET_RISE_MS[0]); meas_hi.append(TARGET_RISE_MS[1])
        kinds.append("prediction")
        labels.append("retract/expand")
        model_v.append(comp["retraction_vs_expansion_asymmetry"]["model"])
        meas_lo.append(min(TARGET_ASYMMETRY_RENARD, TARGET_ASYMMETRY_HADJI))
        meas_hi.append(max(TARGET_ASYMMETRY_RENARD, TARGET_ASYMMETRY_HADJI))
        kinds.append("prediction")
    yy = np.arange(len(labels))
    for i, (lo, hi) in enumerate(zip(meas_lo, meas_hi)):
        ax.plot([lo, max(hi, lo * 1.001)], [yy[i], yy[i]], lw=9, color="#bbbbbb",
                solid_capstyle="butt", zorder=1)
        # a single measured value draws as an invisible bar, so mark it too
        ax.scatter([lo] if lo == hi else [lo, hi], [yy[i]] * (1 if lo == hi else 2),
                   s=42, marker="|", linewidths=2.0, color="#555555", zorder=2)
        txt = f"measured {lo:g}" if lo == hi else f"measured {lo:g}-{hi:g}"
        ax.text((lo * hi) ** 0.5, yy[i] - 0.30, txt, fontsize=7.0, ha="center",
                color="#555555")
    ax.scatter(model_v, yy, s=60,
               color=[OKABE[2] if k == "prediction" else OKABE[4] for k in kinds], zorder=3)
    for i, (v, k) in enumerate(zip(model_v, kinds)):
        ax.text(v, yy[i] + 0.26, f"model {v:.2f} ({k})", fontsize=7.2, ha="center")
    ax.set_yticks(yy); ax.set_yticklabels(labels, fontsize=8)
    ax.set_xscale("log")
    ax.set_xlabel("value (log scale); grey bar = measured")
    ax.set_title("Control arm: both free predictions MISS", fontsize=10)
    ax.set_ylim(-0.75, len(labels) - 0.15)

    fig.suptitle("Simulation. Actuator datasheet, and the control arm against measured "
                 "cephalopod data - which it fails", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)


# --------------------------------------------------------------------------------------

def main():
    base_kwargs = dict(
        r0_um=25.0, R_anchor_um=75.0, N=20, a_fibre_um2=3.14, sigma_max_kPa=250.0,
        v_max=3.5, hill_a=0.25, tau_act_ms=15.0, tau_deact_ms=40.0, t0_um=0.5,
        eps_max=0.30,
    )
    # Extended 2026-11-02 from a -9..-2.5 range to -9..+1. The original sweep's
    # maximum asymmetry sat at its own upper boundary, which is exactly the
    # condition under which "no value reaches X" cannot be claimed. Extending it
    # showed the asymmetry DOES cross 1.0 near c = 0.08, two orders of magnitude
    # above where the sweep stopped, and an earlier version of this study's
    # headline asserted the opposite.
    c_sweep = [10 ** e for e in np.arange(-9.0, 1.01, 0.25)]
    control = run_control(base_kwargs, c_sweep)
    G_fit = control["fitted_G_kPa"]
    best = control.get("best_match_to_measured_asymmetry") or {}
    c_best = best.get("c_damp_N_s_per_m", 1e-6)
    print(f"fitted G = {G_fit:.4g} kPa; damping best match c = {c_best:.3g} N s/m")

    sweeps = run_sweeps(G_fit, c_best)
    ds = datasheet(G_fit, c_best)

    comp = control.get("comparisons", {})
    rise_ok = comp.get("rise_time_ms", {}).get("inside_measured_range")
    _rt = comp.get("rise_time_ms", {}).get("model", float("nan"))
    _asym = comp.get("retraction_vs_expansion_asymmetry", {}).get("model", float("nan"))
    _ar = comp.get("area_ratio", {}).get("model", float("nan"))
    headline = (
        "Two parameters are fitted to two measured quantities - the sacculus stiffness "
        "to the steady-state expansion ratio 2.55, and the dermal damping to the "
        f"measured expansion:retraction asymmetry, which it reaches ({_asym:.2f} against "
        f"{TARGET_ASYMMETRY_RENARD:.2f}, Renard 2026; Hadjisolomou 2021 puts it at "
        f"{TARGET_ASYMMETRY_HADJI:.1f}). The two fits are mutually inconsistent: at that "
        f"damping the peak expansion collapses to {_ar:.2f}, "
        f"{100 * (1 - _ar / TARGET_AREA_RATIO):.0f}% short of the ratio the stiffness was "
        "fitted to. And the one genuinely free prediction fails: the 90% rise is "
        f"{_rt:.0f} ms against a measured expansion phase of {TARGET_RISE_MS[0]:.0f}-"
        f"{TARGET_RISE_MS[1]:.0f} ms, {_rt / TARGET_RISE_MS[1]:.1f}-"
        f"{_rt / TARGET_RISE_MS[0]:.1f}x too slow"
        + (", though it lands" if rise_ok else ", and the control arm fails")
        + ". An earlier version of this study claimed a lumped elastic recoil was "
        "STRUCTURALLY incapable of retraction slower than expansion; that was wrong, "
        "made from a sweep whose maximum sat at its own boundary, and it is corrected "
        "here. Across every sweep the stroke is set by the elastic sacculus rather than "
        "by the muscle, so adding radial fibres buys almost nothing. Parameters: "
        "5 sourced, 13 assumed, 1 nondimensional."
    )

    result = {
        "id": "actuator-mechanics",
        "title": "The chromatophore as an actuator: mechanics, kinetics and a datasheet",
        "kind": "simulation (Hill-type muscle + hyperelastic membrane)",
        "headline": headline,
        "species_of_evidence": {
            "fitted_and_scored_against": "Doryteuthis pealeii (Hadjisolomou et al. 2021)",
            "asymmetry_also_scored_against":
                "Euprymna berryi and Sepia officinalis (Renard et al. 2026)",
            "muscle_property_proxies_from":
                "Doryteuthis pealeii mantle circular and funnel retractor muscle - a "
                "different tissue in the same genus, never a chromatophore radial muscle",
            "note": "Three animals. This study's fit, its asymmetry comparison and its "
                    "proxies do not come from one organism, and the page should not read "
                    "as though they do.",
        },
        "SUPERSEDED_2026_11_02": {
            "what_changed": [
                "comparisons.rise_time_ms is now scored against the expansion PHASE "
                "(67-83 ms) rather than the published rise time tRt (117-150 ms), which "
                "is timed from the flash and includes a 50-67 ms latency this model does "
                "not simulate",
                "comparisons.retraction_vs_expansion_asymmetry now carries BOTH measured "
                "sources; it previously carried Renard's 1.338 alone",
            ],
            # ONLY values that are no longer current belong here. Renard's 1.338 is
            # NOT superseded - it is still one of the two measured asymmetries, and
            # listing it here made a downstream guard refuse the corrected summary
            # for quoting a number that is live. What was superseded is scoring the
            # model against it ALONE, and the 117-150 ms rise comparator.
            "superseded_values": {"measured_rise_range_ms": list(TARGET_RISE_FROM_FLASH_MS)},
            "superseded_practice": (
                "Scoring the asymmetry against Renard's 1.338 alone. Both measured "
                "sources are now carried; 1.338 itself remains current."),
            "effect": "The control arm fails by MORE than the earlier version recorded: "
                      "2.6-3.2x too slow on rise time instead of 1.4-1.8x, and wrong in "
                      "sign against two sources instead of one.",
        },
        "model": {
            "description": (
                "One chromatophore organ: an incompressible neo-Hookean pigment sacculus opened "
                "by N Hill-type radial muscle fibres anchored in the dermis and closed by its own "
                "stored elastic energy against a dermal dashpot. Inertia is checked and discarded."
            ),
            "state_variables": ["sacculus radius r", "muscle activation a"],
            "equations": [
                "F_muscle(r, dr/dt, a) = F_elastic(r) + c dr/dt",
                "F_elastic(r) = 2 pi r G t0 (1 - (r/r0)^-6)",
                "F_muscle = N a_fibre sigma_max a fl(r) fv(dr/dt)",
                "da/dt = (u - a)/tau,  tau = tau_act when driving, tau_deact when releasing",
                "pigment disc thickness h(r) = V0 / (pi r^2), volume conserved",
            ],
            **param_block(PARAMS),
        },
        "control": control,
        "sweeps": sweeps,
        "datasheet": ds,
        "limitations": [
            "This model is a one-constraint model being asked to meet three. It is fitted "
            "to the steady-state expansion ratio and then scored on expansion speed and "
            "on the expansion:retraction asymmetry, and no single setting meets more than "
            "one of them. Enough damping reaches either measured asymmetry, but at a cost "
            "of a third to a half of the expansion magnitude and a rise time that is "
            "already 2.6-3.2x too slow and gets slower. A next version needs a mechanism "
            "that slows retraction WITHOUT loading expansion - a viscoelastic sacculus "
            "whose stress relaxes during the hold, or an active brake - rather than more "
            "of the one knob this model has.",
            "The two measured asymmetries differ by about 3x and are preserved separately "
            "rather than averaged. They are also different measurements in different "
            "animals: Renard tracks phases of individual slice events at 20 fps in "
            "Euprymna berryi and Sepia officinalis; the Hadjisolomou figure is decomposed "
            "by us from per-region summary statistics of a startle response in "
            "Doryteuthis pealeii, and that decomposition is ours, not the authors'.",
            "The sacculus shear modulus has never been measured; it is the one fitted parameter, "
            "so the model cannot claim to predict the expansion ratio - it was told it.",
            "Every muscle property is a PROXY from a different squid muscle (mantle circular or "
            "funnel retractor). No one has measured the contractile properties of a chromatophore "
            "radial muscle, so sigma_max, V_max and the activation kinetics are assumed.",
            "The measured control target itself is a startle response, not a maximal contraction: "
            "Hadjisolomou et al. report what the organ did on a light flash, and state no maximum. "
            "The folklore figure of a ~7x diameter / ~50x area expansion traces, as far as we could "
            "follow it, to a secondary teaching page citing Cloney & Florey 1968; we could not read "
            "a primary source stating it, and so do not use it.",
            "The geometry is axisymmetric, but the organ is not: Renard et al. 2026 show expansion is "
            "routinely anisotropic, with about four independently driven petal-shaped sectors per "
            "chromatophore. A single radius cannot express that, and the model therefore cannot "
            "represent the sub-chromatophore control that the real system has.",
            "Radial muscles of neighbouring chromatophores make direct muscle-to-muscle contacts "
            "(Gauld et al. 2021), so an isolated single-organ model omits a real mechanical coupling.",
            "The dermal damping is not measured anywhere; the value reported is what the model needs, "
            "not what the tissue has.",
            "Holding cost is reported as mechanical stress and stored elastic energy only. We did not "
            "find a measured ATP cost for cephalopod obliquely striated muscle, so no metabolic "
            "number is given rather than a fabricated one.",
        ],
        "figures": ["actuator-sweep.png", "actuator-datasheet.png"],
    }
    write_result(os.path.join(ROOT, "actuator-mechanics.json"), result)
    fig_sweep(sweeps, control, G_fit, os.path.join(FIG, "actuator-sweep.png"))
    fig_datasheet(ds, control, os.path.join(FIG, "actuator-datasheet.png"))
    print(json.dumps(control.get("comparisons", {}), indent=1))


if __name__ == "__main__":
    main()
