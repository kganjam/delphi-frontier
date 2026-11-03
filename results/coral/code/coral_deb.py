#!/usr/bin/env python3
"""
coral_deb.py — a vectorised Python port of the coRal host-symbiont bioenergetic model,
plus ONE declared thermal extension.

WHAT THIS IS
------------
The dynamical core below is NOT invented here. It is a line-by-line port of

    Cunning R, Muller EB, Gates RD, Nisbet RM (2017)
    "A dynamic bioenergetic model for coral-Symbiodinium symbioses and coral bleaching
     as an alternate stable state." J Theor Biol 431:49-62.   PMID 28782552

as published by its first author in the R package `coRal`
(github.com/jrcunning/coRal, MIT licence, commit 7c90f9bee5917d62f69d751a53d105b051732ac6,
dated 2021-03-23, cloned 2026-11-02). The equations are from `R/run_coral.R` and
`R/synth.R`; every parameter default is from `R/def_pars.R`, including its units and its
comment. Those comments are the provenance for the `sourced` status of 22 parameters:
read_level for the code is full-text (the file was read), read_level for the PAPER is
abstract only (the paper itself was not obtained; see NOTES.md).

WHAT IS NOT CUNNING ET AL.
--------------------------
**coRal has no temperature variable.** Searching the whole cloned repository for
"temp", "thermal", "heat", "degC" and "dhw" returns nothing. In the published model,
bleaching is driven by LIGHT: absorbed light that photochemistry cannot use and that
non-photochemical quenching cannot dissipate drives ROS, and ROS drives symbiont
turnover. Temperature does not appear.

So the thermal coupling here is MY ADDITION and is flagged as such everywhere:

    jCPm_effective(T) = jCPm * phi(T)

with phi an asymmetric thermal performance curve peaking at T_opt. That is, heat lowers
the ceiling on symbiont carbon fixation and nothing else. The excess excitation energy
jeL, the ROS factor cROS and the symbiont turnover jST then all follow through the
PUBLISHED equations without further change.

The mechanistic warrant for routing heat through that one term, and no other, is
Warner, Fitt & Schmidt 1999, PNAS 96:8007-12 (PMID 10393938, read_level abstract):
heat damages the PSII D1 reaction-centre protein faster than it is replaced, and the
authors state that "perturbation of PSII protein turnover rates during photoinhibition
at elevated temperatures underlies the physiological collapse of symbionts in corals
susceptible to heat-induced bleaching". A falling ceiling on photochemistry is what that
is, in this model's accounting. It is a choice, not a measurement, and the limitation is
stated in the result file.

THE STATE THAT EQUILIBRATES IS S/H, NOT S OR H
----------------------------------------------
Measured here by running the unmodified R code over a 4x5 grid of light and DIN: host
and symbiont biomass both grow (or shrink) exponentially without bound, because the model
is biomass-specific and has no size limit. What settles is the symbiont-to-host ratio.
Every readout below is therefore defined on S/H.

THE KNOBS
---------
Four, three of them real coRal parameters with published defaults:

    T_opt   thermal optimum of symbiont photochemistry   MY ADDITION (assumed)
    kNPQ    capacity of non-photochemical quenching      coRal default 112
    kROS    excess light that doubles ROS production     coRal default 80
    b       scaling of the bleaching response to ROS     coRal default 5
"""
from __future__ import annotations

import numpy as np

# --------------------------------------------------------------------------------------
# Parameters, copied from coRal R/def_pars.R with its own comments as the source text.
# --------------------------------------------------------------------------------------

CORAL_PARAMETERS = [
    # ---- host -------------------------------------------------------------------
    dict(name="jHT0", value=0.03, units="1/d", status="sourced",
         source="coRal def_pars.R: 'Host specific biomass turnover rate (d^-1)'."),
    dict(name="nNH", value=0.18, units="mol N / C-mol H", status="sourced",
         source="coRal def_pars.R: 'N:C ratio in host biomass (-)'."),
    dict(name="nNX", value=0.2, units="mol N / C-mol X", status="sourced",
         source="coRal def_pars.R: 'N:C ratio in prey biomass (-)'."),
    dict(name="sigmaNH", value=0.9, units="fraction", status="sourced",
         source="coRal def_pars.R: 'Proportion of host nitrogen turnover recycled (-)'."),
    dict(name="sigmaCH", value=0.1, units="fraction", status="sourced",
         source="coRal def_pars.R: 'Proportion of host carbon turnover recycled (-)'."),
    dict(name="jXm", value=0.13, units="mol X / C-mol H / d", status="sourced",
         source="coRal def_pars.R: 'Maximum specific host feeding rate'."),
    dict(name="jNm", value=0.035, units="mol N / C-mol H / d", status="sourced",
         source="coRal def_pars.R: 'Maximum specific host DIN uptake rate'."),
    dict(name="jHGm", value=1.0, units="C-mol H / C-mol H / d", status="sourced",
         source="coRal def_pars.R: 'Maximum specific host growth rate'."),
    dict(name="kCO2", value=10.0, units="mol CO2 / mol C / d", status="sourced",
         source="coRal def_pars.R: 'Rate of host CCM's'."),
    dict(name="KN", value=1.5e-6, units="mol N / L", status="sourced",
         source="coRal def_pars.R: 'Half-saturation constant for host DIN uptake'."),
    dict(name="KX", value=1e-6, units="C-mol X / L", status="sourced",
         source="coRal def_pars.R: 'Half-saturation constant for host feeding'."),
    dict(name="yC", value=0.8, units="fraction", status="sourced",
         source="coRal def_pars.R: declared with no comment; it is the carbon yield of "
                "biomass synthesis, used in both host and symbiont growth."),
    # ---- symbiont ---------------------------------------------------------------
    dict(name="jST0", value=0.03, units="1/d", status="sourced",
         source="coRal def_pars.R: 'Symbiont specific biomass turnover rate (d^-1)'."),
    dict(name="nNS", value=0.13, units="mol N / C-mol S", status="sourced",
         source="coRal def_pars.R: 'N:C ratio in symbiont biomass (-)'."),
    dict(name="yCL", value=0.1, units="mol C / mol photon", status="sourced",
         source="coRal def_pars.R: 'L:C ratio in fixed carbon (=quantum yield)'."),
    dict(name="kNPQ", value=112.0, units="mol photon / C-mol S / d", status="sourced",
         source="coRal def_pars.R: 'capacity of non-photochemical quenching', with the "
                "comment 'calculated as 4x max. photochemical quenching (Gorbunov et al. "
                "2001)'. Gorbunov et al. 2001 was NOT retrieved or read here; the "
                "attribution is coRal's, relayed."),
    dict(name="kROS", value=80.0, units="mol photon / C-mol S / d", status="sourced",
         source="coRal def_pars.R: 'amount of excess light beyond NPQ capacity (e.g., "
                "jeL-jNPQ) that doubles ROS production relative to baseline'."),
    dict(name="k", value=1.0, units="nondimensional", status="sourced",
         source="coRal def_pars.R: 'exponent on ROS production (-)'."),
    dict(name="astar", value=1.34, units="m^2 / C-mol S", status="sourced",
         source="coRal def_pars.R: 'Symbiont specific cross-sectional area'."),
    dict(name="sigmaNS", value=0.9, units="fraction", status="sourced",
         source="coRal def_pars.R: 'Proportion of symbiont nitrogen turnover recycled'."),
    dict(name="sigmaCS", value=0.9, units="fraction", status="sourced",
         source="coRal def_pars.R: 'Proportion of symbiont carbon turnover recycled'."),
    dict(name="jCPm", value=2.8, units="C-mol / C-mol S / d", status="sourced",
         source="coRal def_pars.R: 'Maximum specific photosynthate production rate'. "
                "THIS is the parameter the thermal extension multiplies."),
    dict(name="jSGm", value=0.25, units="C-mol S / C-mol S / d", status="sourced",
         source="coRal def_pars.R: 'Maximum specific symbiont growth rate'."),
    dict(name="b", value=5.0, units="nondimensional", status="sourced",
         source="coRal def_pars.R: 'Scaling parameter for bleaching response'."),
]

# Self-shading coefficients, hard-coded in coRal's run_coral.R rather than in def_pars.R.
SHADE_A, SHADE_B, SHADE_C = 1.256307, 1.385969, 6.479055

PARS = {p["name"]: p["value"] for p in CORAL_PARAMETERS}


def synth(x, y, m):
    """Parallel complementary synthesising unit (Kooijman 2010 p.105, via coRal synth.R).

    1 / (1/m + 1/x + 1/y - 1/(x+y)). Returns 0 where either substrate flux is <= 0,
    which is the limit of the expression and avoids a division by zero.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ok = (x > 0) & (y > 0)
    out = np.zeros(np.broadcast(x, y, np.asarray(m, dtype=float)).shape, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        val = 1.0 / (1.0 / m + 1.0 / np.where(ok, x, 1.0) + 1.0 / np.where(ok, y, 1.0)
                     - 1.0 / np.where(ok, x + y, 1.0))
    return np.where(ok, val, out)


def thermal_performance(T, T_opt, sigma_hot, sigma_cold):
    """Asymmetric thermal performance curve in [0, 1], peaking at T_opt.

    NOT from Cunning et al. This is the thermal extension. Left-skewed (sigma_cold >
    sigma_hot) because thermal performance curves of photosynthetic organisms fall away
    faster above the optimum than below it.
    """
    d = np.asarray(T, dtype=float) - np.asarray(T_opt, dtype=float)
    sig = np.where(d >= 0.0, sigma_hot, sigma_cold)
    return np.exp(-0.5 * (d / sig) ** 2)


def run(L, N, X, T=None, pars=None, dt=0.1, n_steps=None, ensemble=1,
        T_opt=28.0, sigma_hot=2.6, sigma_cold=7.0, init_H=1.0, init_S=1.0,
        record=("SH", "cROS", "jCP", "jeL", "jST", "jSG", "dHdt", "H", "S", "jHG")):
    """Integrate the model forward, vectorised over an ensemble of parameter sets.

    L, N, X : environmental forcing. Each is either a scalar (constant) or an array of
              length n_steps (time series). Units as in coRal: L mol photons m^-2 d^-1,
              N mol N L^-1, X C-mol X L^-1.
    T       : sea temperature in degC, scalar or length-n_steps array. If None, the
              thermal extension is OFF and the model is exactly coRal.
    pars    : dict overriding any of PARS. A value may be an array of length `ensemble`,
              in which case that parameter varies across the ensemble.
    ensemble: number of parameter sets integrated simultaneously.

    Returns a dict of arrays shaped (n_steps, ensemble) for each recorded quantity.

    Integration is explicit Euler on the specific rates, exactly as coRal's run_coral.R
    does it; dt=0.1 d is coRal's own documented recommendation ("Values > 0.1 are not
    recommended", run_coral_ss.R). A step-halving check is in bleaching_dynamics.py.
    """
    p = dict(PARS)
    if pars:
        p.update(pars)

    def arr(v):
        return np.broadcast_to(np.asarray(v, dtype=float), (ensemble,)).astype(float)

    # Parameters, broadcast across the ensemble.
    (jHT0, nNH, nNX, sigmaNH, sigmaCH, jXm, jNm, jHGm, kCO2, KN, KX, yC,
     jST0, nNS, yCL, kNPQ, kROS, kexp, astar, sigmaNS, sigmaCS, jCPm, jSGm, bb) = (
        arr(p[nm]) for nm in
        ("jHT0", "nNH", "nNX", "sigmaNH", "sigmaCH", "jXm", "jNm", "jHGm", "kCO2",
         "KN", "KX", "yC", "jST0", "nNS", "yCL", "kNPQ", "kROS", "k", "astar",
         "sigmaNS", "sigmaCS", "jCPm", "jSGm", "b"))
    T_opt_a = arr(T_opt)

    # Forcing as time series. The length is n_steps if given, else the length of
    # whichever forcing was supplied as an array.
    given = [np.asarray(v, dtype=float) for v in (L, N, X, T) if v is not None]
    lengths = {len(v) for v in given if np.asarray(v).ndim > 0}
    if n_steps is None:
        if len(lengths) != 1:
            raise ValueError(
                f"cannot infer n_steps: array forcings have lengths {sorted(lengths)}")
        n_steps = lengths.pop()
    elif lengths and lengths != {n_steps}:
        raise ValueError(f"forcing lengths {sorted(lengths)} disagree with n_steps")

    def series(v):
        v = np.asarray(v, dtype=float)
        return np.full(n_steps, float(v)) if v.ndim == 0 else v

    Lt, Nt, Xt = series(L), series(N), series(X)
    nt = len(Lt)
    if T is None:
        Tt = None
    else:
        Tt = series(T)
        if len(Tt) != nt:
            raise ValueError("T must match the forcing length")

    # Constant host input fluxes (coRal computes these outside the loop).
    jX = jXm * Xt[:, None] / (Xt[:, None] + KX)          # (nt, ens)
    jN = jNm * Nt[:, None] / (Nt[:, None] + KN)
    rNH = jHT0 * nNH * sigmaNH
    rNS = jST0 * nNS * sigmaNS

    # Initial values, exactly coRal's.
    H = np.broadcast_to(np.asarray(init_H, dtype=float), (ensemble,)).astype(float)
    S = np.broadcast_to(np.asarray(init_S, dtype=float), (ensemble,)).astype(float)
    rhoN = jN[0].copy()
    jeC = np.full(ensemble, 10.0)
    jCO2 = kCO2 * jeC
    jHG = np.full(ensemble, 0.25)
    rCH = jHT0 * sigmaCH
    jL = Lt[0] * astar
    jCPm0 = jCPm * (thermal_performance(Tt[0], T_opt_a, sigma_hot, sigma_cold)
                    if Tt is not None else 1.0)
    jCP = np.maximum(0.0, synth(jL * yCL, jCO2 * H / S, jCPm0))
    jeL = np.maximum(jL - jCP / yCL, 0.0)
    jSG = jSGm / 10.0
    jST = jST0.copy()
    cROS = np.ones(ensemble)

    out = {kk: np.zeros((nt, ensemble)) for kk in record}

    def stash(i, **kw):
        for kk in out:
            if kk in kw:
                out[kk][i] = kw[kk]

    stash(0, SH=S / H, cROS=cROS, jCP=jCP, jeL=jeL, jST=jST, jSG=jSG,
          dHdt=jHG - jHT0, H=H, S=S, jHG=jHG)

    for i in range(1, nt):
        Hp, Sp = H, S
        # --- symbiont -------------------------------------------------------------
        jL = (SHADE_A + SHADE_B * np.exp(-SHADE_C * (Sp / Hp))) * Lt[i] * astar
        rCS = sigmaCS * (jST0 + (1.0 - yC) * jSG / yC)
        jCPm_eff = jCPm * (thermal_performance(Tt[i], T_opt_a, sigma_hot, sigma_cold)
                           if Tt is not None else 1.0)
        jCP = synth(jL * yCL, (jCO2 + rCH) * Hp / Sp + rCS, jCPm_eff) / cROS
        jeL = np.maximum(jL - jCP / yCL, 0.0)
        with np.errstate(divide="ignore"):
            jNPQ = np.where(jeL > 0, 1.0 / (1.0 / kNPQ + 1.0 / np.where(jeL > 0, jeL, 1.0)),
                            0.0)
        cROS = 1.0 + (np.maximum(jeL - jNPQ, 0.0) / kROS) ** kexp
        jSG = synth(yC * jCP, (rhoN * Hp / Sp + rNS) / nNS, jSGm)
        rhoC = np.maximum(jCP - jSG / yC, 0.0)
        jST = jST0 * (1.0 + bb * (cROS - 1.0))
        dSdt = jSG - jST
        S = np.maximum(Sp + dSdt * Sp * dt, 1e-30)
        # --- host -----------------------------------------------------------------
        rhoC_t = rhoC * Sp
        jHG = synth(yC * (rhoC_t / Hp + jX[i]),
                    (jN[i] + nNX * jX[i] + rNH) / nNH, jHGm)
        rhoN = np.maximum(jN[i] + nNX * jX[i] + rNH - nNH * jHG, 0.0)
        jeC = np.maximum(jX[i] + rhoC_t / Hp - jHG / yC, 0.0)
        rCH = sigmaCH * (jHT0 + (1.0 - yC) * jHG / yC)
        jCO2 = kCO2 * jeC
        dHdt = jHG - jHT0
        H = np.maximum(Hp + dHdt * Hp * dt, 1e-30)

        stash(i, SH=S / H, cROS=cROS, jCP=jCP, jeL=jeL, jST=jST, jSG=jSG,
              dHdt=dHdt, H=H, S=S, jHG=jHG)

    return out
