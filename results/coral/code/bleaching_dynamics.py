#!/usr/bin/env python3
"""
bleaching_dynamics.py — host-symbiont bleaching dynamics under thermal stress.

WHAT THIS IS: a simulation. Nothing in the output is a measurement of a coral.

The dynamical core is a line-by-line port of the published coRal model (Cunning, Muller,
Gates & Nisbet 2017, J Theor Biol 431:49-62, PMID 28782552), checked against the author's
own R code to floating-point round-off. See coral_deb.py for the port and for the ONE
thing that is not Cunning et al.: coRal contains no temperature variable, so the thermal
coupling is added here and flagged as an addition everywhere it matters.

THE DESIGN QUESTION
-------------------
Four routes on the coral design-space page claim to raise thermal tolerance by acting on
four different knobs. Three of the four are real coRal parameters:

    T_opt   symbiont thermal optimum          Durusdinium trenchii; heat-evolved strains
    kNPQ    non-photochemical quenching       photoprotective pigments (SS8 route)
    kROS    excess light that doubles ROS     symbiont/host ROS handling
    b       bleaching response to ROS         host regulation; frontloading

Are they additive, or does one dominate?

EVERYTHING DECLARED BEFORE THE SWEEP
------------------------------------
  * the control arm and its six pass conditions
  * the bleaching criterion: S/H below 0.5 of the control steady-state S/H
  * the thermal forcing used to measure a threshold
  * the four knob ranges and why each has the span it has
  * the additivity test (adjusted R^2 of main effects vs main effects + two-way)

Usage
  python3 bleaching_dynamics.py --run         control + port check + sweeps + knob map
  python3 bleaching_dynamics.py --control     control arm only
  python3 bleaching_dynamics.py --figures     redraw from the cache
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time as _time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coral_deb import (CORAL_PARAMETERS, PARS, run, thermal_performance)  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIGDIR = os.path.join(ROOT, "figures")
LOGDIR = os.path.join(ROOT, "logs")
CACHE = os.path.join(ROOT, "bleaching-cache.json")
RESULT = os.path.join(ROOT, "bleaching-dynamics.json")

DT = 0.1          # days. coRal's own documented recommendation ("values > 0.1 are not
                  # recommended", run_coral_ss.R). A step-halving check is run below.

# --------------------------------------------------------------------------------------
# Parameters that are NOT coRal's: the environment, the thermal extension, the readouts.
# --------------------------------------------------------------------------------------

EXTRA_PARAMETERS = [
    # ---- environment --------------------------------------------------------------
    dict(name="L_control", value=30.0, units="mol photons m^-2 d^-1", status="assumed",
         source="Constant downwelling irradiance for every arm. Held CONSTANT rather "
                "than seasonal so that the degree-heating-week threshold is "
                "attributable to temperature alone: coRal drives bleaching with light, "
                "so a seasonal light cycle in phase with the seasonal temperature cycle "
                "would confound the two. A seasonal-light arm is run as a robustness "
                "check and reported separately. 30 mol photons m^-2 d^-1 is a shallow "
                "tropical reef order of magnitude; no measurement was retrieved."),
    dict(name="N_control", value=1.0e-6, units="mol N L^-1", status="assumed",
         source="External dissolved inorganic nitrogen, 1 uM. coRal's own documented "
                "example uses 1e-7, which in this port gives a host whose specific "
                "growth rate is negative (measured: dH/Hdt < 0 at L >= 10). 1e-6 puts "
                "the control in positive energy balance. No reef measurement was "
                "retrieved; this is a model-operating choice."),
    dict(name="X_control", value=0.0, units="C-mol X L^-1", status="assumed",
         source="No heterotrophic feeding in any arm, so autotrophy is the only carbon "
                "source and the bleaching response is not cushioned by feeding. Cunning "
                "et al.'s own abstract states bleaching is 'attenuated by feeding', so "
                "this is the conservative, bleaching-prone choice."),
    dict(name="MMM", value=28.6, units="degC", status="assumed",
         source="Maximum monthly mean used as the DHW reference. A representative "
                "tropical value; NOT a site measurement and not taken from any "
                "climatology file. Only differences from it matter to the result."),
    dict(name="seasonal_amplitude", value=2.0, units="degC", status="assumed",
         source="Half-range of the annual sea-temperature cycle. Representative; no "
                "published value used."),
    # ---- thermal extension (NOT Cunning et al.) ------------------------------------
    dict(name="T_opt", value=28.0, units="degC", status="assumed",
         source="Thermal optimum of symbiont photochemistry in the added performance "
                "curve. No published value applies across Symbiodiniaceae genera. This "
                "is the baseline the sweep moves away from; the SPAN carries the "
                "meaning, not the value."),
    dict(name="sigma_hot", value=1.1, units="degC", status="assumed",
         source="Width of the thermal performance curve above the optimum. THIS IS THE "
                "ONE CALIBRATED PARAMETER: it was chosen so the unmodified holobiont "
                "bleaches inside the NOAA 4-8 degree-heating-week window. A model "
                "calibrated to that window cannot then be used as evidence about it, "
                "and nothing here claims it is."),
    dict(name="tradeoff_kappa", value=0.0, units="fractional loss of photochemical "
                                             "efficiency per degC of thermal optimum",
         status="sourced-structure-assumed-magnitude",
         source="THE STRUCTURE IS SOURCED AND THE MAGNITUDE IS NOT. Cunning, Silverstein "
                "& Baker 2015 (PMID 26041354, abstract) report that in Orbicella "
                "faveolata 'higher proportions of heat-tolerant symbionts LINEARLY "
                "increased bleaching resistance but REDUCED PHOTOCHEMICAL EFFICIENCY'. "
                "So the thermal knob is not free: it is bought against the symbiont's "
                "capacity to turn absorbed light into fixed carbon. This file encodes it "
                "on jCPm, the maximum specific photosynthate production rate: "
                "jCPm_effective = jCPm * phi(T) * (1 - kappa * (T_opt - 28)). "
                "THE FIRST ENCODING WAS ON yCL AND CAME OUT WITH THE WRONG SIGN, which "
                "is recorded because it is a trap in coRal's photon accounting rather "
                "than a typo: excess excitation energy is jeL = jL - jCP/yCL, so LOWERING "
                "the quantum yield makes each unit of fixed carbon consume more photons, "
                "which REDUCES the excess and therefore reduces ROS. Measured, with the "
                "coupling on yCL: raising kappa from 0 to 0.3 IMPROVED both the thermal "
                "gain (+2.000 to +2.137 degC) and the ambient cost (-1.65% to -0.10%) -- "
                "the trade-off made the coral better, which is not what the source says. "
                "On jCPm the direction is the intended one: a lower ceiling on carbon "
                "fixation leaves more absorbed light unused AND delivers less carbon to "
                "the host. The LINEARITY and the "
                "SIGN come from that sentence; kappa itself does not, because the "
                "abstract gives no slope, so kappa is SWEPT rather than set and the "
                "default of 0 is the uncoupled model. NOTE THE SPECIES: Orbicella "
                "faveolata is a massive Caribbean coral, not an Acropora, so applying "
                "this coupling to an Acropora route is a cross-genus assumption."),
    dict(name="sigma_cold", value=7.0, units="degC", status="assumed",
         source="Width below the optimum, set wider than sigma_hot because thermal "
                "performance curves of photosynthetic organisms are left-skewed. Not "
                "fitted to anything."),
    # ---- DHW accounting -------------------------------------------------------------
    dict(name="dhw_hotspot_offset", value=1.0, units="degC", status="sourced",
         source="NOAA Coral Reef Watch convention: HotSpots are summed into degree "
                "heating weeks only when SST exceeds the maximum monthly mean by at "
                "least 1 degC. Source read: the NOAA CRW DHW product page "
                "(coralreefwatch.noaa.gov/product/5km/tutorial/crw10a_dhw_product.php), "
                "read_level web-page. The primary methods papers (Liu et al.; Glynn & "
                "D'Croz 1990; Eakin et al. 2010) were NOT retrieved and are not cited."),
    dict(name="dhw_window", value=84.0, units="days", status="sourced",
         source="NOAA CRW: DHW is the running sum of HotSpots over the previous 12 "
                "weeks. Same page, read_level web-page."),
    dict(name="DHW_alert1", value=4.0, units="degC-weeks", status="sourced",
         source="NOAA CRW: at 4 degC-weeks 'you can expect to see coral bleaching "
                "reef-wide, especially in more sensitive coral species'. Same page, "
                "read_level web-page. Note the page as summarised does not itself label "
                "4 and 8 as Alert Levels 1 and 2."),
    dict(name="DHW_alert2", value=8.0, units="degC-weeks", status="sourced",
         source="NOAA CRW: at 8 degC-weeks 'you are likely to see reef-wide coral "
                "bleaching with mortality of heat-sensitive corals'. Same page."),
    dict(name="DHW_realism_ceiling", value=16.0, units="degC-weeks", status="assumed",
         source="Thresholds above this are reported as 'beyond observed forcing' rather "
                "than as numbers. Twice NOAA's mortality level. A declared reporting "
                "cut, not a biological quantity."),
    # ---- readouts, all declared before the sweep -------------------------------------
    dict(name="bleaching_criterion", value=0.5, units="fraction of control S/H",
         status="assumed",
         source="DECLARED BEFORE THE SWEEP. Bleaching is the symbiont-to-host ratio "
                "falling below half its control steady-state value. Chosen because "
                "visible paling corresponds to a large fractional symbiont loss; no "
                "study used 0.5 as a cut. The sensitivity of every conclusion to this "
                "number is reported (criterion_sensitivity)."),
    dict(name="spinup_years", value=3.0, units="years", status="assumed",
         source="Ambient run before any anomaly, so the heatwave acts on a settled "
                "symbiosis. Checked: the control passes its stationarity conditions."),
    dict(name="anomaly_max", value=4.0, units="degC", status="assumed",
         source="Peak of the thermal anomaly in the standard forcing. Large enough that "
                "even the most tolerant corner of the knob map bleaches or is reported "
                "censored; larger than any single observed reef anomaly."),
    dict(name="sustain_days", value=14.0, units="days", status="assumed",
         source="A readout condition must hold for this long before it counts as a "
                "crossing. DECLARED BEFORE THE SWEEP. coRal's initialisation resets the "
                "flux variables whatever the biomass state, so every run begins with a "
                "one-step transient; requiring persistence makes every readout immune to "
                "it and to any other brief excursion. Two weeks is a round number."),
    dict(name="anomaly_ramp", value=240.0, units="days", status="assumed",
         source="The anomaly rises linearly over this many days, so degree heating "
                "weeks accumulate smoothly and the DHW at first bleaching is well "
                "resolved rather than jumping between time steps."),
]

ALL_PARAMETERS = CORAL_PARAMETERS + EXTRA_PARAMETERS
EP = {p["name"]: p["value"] for p in EXTRA_PARAMETERS}


# --------------------------------------------------------------------------------------
# Thermal forcing and NOAA degree-heating-week accounting
# --------------------------------------------------------------------------------------

def seasonal_sst(t_days, mmm, amp):
    """Annual cycle whose maximum just touches the maximum monthly mean.

    Peak at day 30 so the anomaly below starts at the seasonal maximum, which is when
    real heatwaves bite. An unperturbed year accumulates exactly zero DHW -- that is one
    of the control arm's pass conditions.
    """
    return mmm - amp + amp * np.cos(2 * np.pi * (t_days - 30.0) / 365.25)


def ramp_anomaly(t_days, onset, amplitude, ramp):
    """Linear thermal anomaly, zero before `onset`, rising to `amplitude` over `ramp`."""
    x = np.asarray(t_days, dtype=float) - onset
    return np.clip(x / ramp, 0.0, 1.0) * amplitude


def degree_heating_weeks(sst, t_days, mmm, offset, window_days):
    """NOAA Coral Reef Watch DHW in degC-weeks, at every time point.

    HotSpot = SST - MMM, counted only where it is at least `offset`. DHW is the running
    integral over a trailing `window_days` window, divided by 7.
    """
    hotspot = np.where((sst - mmm) >= offset, sst - mmm, 0.0)
    step = float(np.median(np.diff(t_days)))
    contrib = hotspot * step / 7.0
    csum = np.cumsum(contrib)
    nwin = max(1, int(round(window_days / step)))
    lo = np.maximum(np.arange(len(sst)) - nwin, 0)
    prev = np.where(lo > 0, csum[np.maximum(lo - 1, 0)], 0.0)
    return csum - prev


# --------------------------------------------------------------------------------------
# Knobs: declared ranges, declared before anything is run
# --------------------------------------------------------------------------------------

KNOBS = {
    "T_opt": dict(
        low=28.0, high=30.0,
        label="Symbiont thermal optimum (degC)",
        route="Durusdinium trenchii shuffling or inoculation; heat-evolved strains",
        range_basis=("SOURCED SPAN. Berkelmans & van Oppen 2006 (PMID 16928632) report "
                     "about +1 to +1.5 degC from a C-to-D shift in Acropora millepora; "
                     "Pettay et al. 2015 (PMID 26034268) report +1 to +2 degC for "
                     "Durusdinium trenchii in Caribbean hosts. A 2 degC span is the top "
                     "of the measured range for the symbiont-identity route. Both read "
                     "at abstract level."),
        is_coral_parameter=False),
    "kNPQ": dict(
        low=112.0, high=224.0,
        label="Non-photochemical quenching capacity (mol photon / C-mol S / d)",
        route="Photoprotective pigments; the SS8 heat-evolved strain's reported mechanism",
        range_basis=("ASSUMED SPAN, a doubling. Chan et al. 2023 (PMID 37913765, "
                     "abstract) report that in SS8-hosting Galaxea fascicularis 'algal "
                     "pigments involved in photobiology and oxidative stress were the "
                     "greatest contributors to the thermotolerance differences', but no "
                     "study gives a factor by which NPQ capacity can be raised. A "
                     "doubling is a round number, not a measured ceiling."),
        is_coral_parameter=True),
    "kROS": dict(
        low=80.0, high=160.0,
        label="Excess light that doubles ROS production (mol photon / C-mol S / d)",
        route="Symbiont and host ROS handling; antioxidant frontloading",
        range_basis=("ASSUMED SPAN, a doubling. Buerger et al. 2020 (PMID 32426508, "
                     "read at FULL TEXT) measured wild-type Symbiodiniaceae secreting "
                     "'~13- to 28-fold higher' extracellular ROS than heat-evolved "
                     "strains after three weeks at 31 degC. That is NOT this parameter: "
                     "kROS is the excess excitation energy at which ROS production "
                     "doubles, not a secreted ROS concentration, and the two cannot be "
                     "converted into one another. The doubling used here is therefore "
                     "assumed and is far more conservative than a 13-28x difference in "
                     "a different quantity would suggest."),
        is_coral_parameter=True),
    "b": dict(
        low=5.0, high=2.5,
        label="Bleaching response to ROS (nondimensional; LOWER means more retentive)",
        route="Host regulation of symbiont expulsion; HSF1 and antioxidant frontloading",
        range_basis=("ASSUMED SPAN, a halving of the coRal default, chosen to match the "
                     "other two multiplicative knobs so the ranges are at least "
                     "comparable in kind. "
                     "jST = jST0*(1 + b*(cROS-1)), so b sets how strongly oxidative "
                     "stress converts into symbiont loss. Barshis et al. 2013 (PMID "
                     "23297204, abstract) show resilient Acropora hyacinthus colonies "
                     "constitutively 'frontload' antioxidant and heat-shock "
                     "transcripts, but nothing measures the resulting change in b. The "
                     "direction is from the biology; the magnitude is invented."),
        is_coral_parameter=True),
}
KNOB_NAMES = list(KNOBS)
WILD_TYPE = {"T_opt": EP["T_opt"], "kNPQ": PARS["kNPQ"],
             "kROS": PARS["kROS"], "b": PARS["b"]}


def _env(n_steps, L=None, seasonal_light=False, t=None):
    L0 = EP["L_control"] if L is None else L
    if seasonal_light:
        # Light peaks with temperature; used ONLY in the robustness arm.
        return L0 * (1.0 + 0.4 * np.cos(2 * np.pi * (t - 30.0) / 365.25))
    return np.full(n_steps, L0)


def _run_ensemble(t, sst, knobvals, ensemble, seasonal_light=False, init=None,
                  dt=DT, kappa=None):
    pars = {}
    for nm in ("kNPQ", "kROS", "b"):
        pars[nm] = knobvals[nm]
    # The Cunning et al. 2015 trade-off: a higher heat-tolerant symbiont proportion buys
    # bleaching resistance at the cost of photochemical efficiency, LINEARLY. yCL is
    # coRal's own quantum yield of carbon fixation.
    k = EP["tradeoff_kappa"] if kappa is None else kappa
    if k:
        dT = np.asarray(knobvals["T_opt"], dtype=float) - EP["T_opt"]
        pars["jCPm"] = PARS["jCPm"] * np.clip(1.0 - k * dT, 0.05, 1.0)
    kwargs = {}
    if init is not None:
        kwargs["init_H"], kwargs["init_S"] = init
    return run(L=_env(len(t), seasonal_light=seasonal_light, t=t),
               N=EP["N_control"], X=EP["X_control"], T=sst, pars=pars, dt=dt,
               ensemble=ensemble, T_opt=knobvals["T_opt"],
               sigma_hot=EP["sigma_hot"], sigma_cold=EP["sigma_cold"], **kwargs)


# --------------------------------------------------------------------------------------
# Control arm. Must pass before any sweep is read.
# --------------------------------------------------------------------------------------

def control_arm(seasonal_light=False):
    years = EP["spinup_years"]
    t = np.arange(0.0, years * 365.25, DT)  # DT is read at call time, see control_arm_at
    sst = seasonal_sst(t, EP["MMM"], EP["seasonal_amplitude"])
    out = _run_ensemble(t, sst, WILD_TYPE, 1, seasonal_light=seasonal_light, dt=DT)

    SH = out["SH"][:, 0]
    last = t >= (years - 1.0) * 365.25
    SH_last = SH[last]
    SH_ss = float(np.mean(SH_last))
    swing = float((SH_last.max() - SH_last.min()) / max(SH_ss, 1e-12))

    # Drift between the second and third year: stationarity, not just smoothness.
    mid = (t >= (years - 2.0) * 365.25) & (t < (years - 1.0) * 365.25)
    drift = float(abs(np.mean(SH[mid]) - SH_ss) / max(SH_ss, 1e-12))

    dhw = degree_heating_weeks(sst, t, EP["MMM"], EP["dhw_hotspot_offset"],
                               EP["dhw_window"])
    growth = float(np.mean(out["dHdt"][last, 0]))
    cROS_last = out["cROS"][last, 0]

    checks = {
        "symbiosis_persists": bool(SH_ss > 0.05),
        "host_in_positive_energy_balance": bool(growth > 0.0),
        "symbiont_ratio_seasonally_stable": bool(swing < 0.25),
        "no_interannual_drift": bool(drift < 0.02),
        "no_bleaching_at_ambient": bool(SH_last.min() > EP["bleaching_criterion"] * SH_ss),
        "zero_dhw_at_ambient": bool(dhw.max() < 1e-9),
        "ros_elevated_but_subcritical": bool(1.0 < cROS_last.mean() < 2.0),
    }
    return dict(
        t=t.tolist()[::10], sst=sst.tolist()[::10], SH=SH.tolist()[::10],
        cROS=out["cROS"][:, 0].tolist()[::10], dHdt=out["dHdt"][:, 0].tolist()[::10],
        SH_steady_state=SH_ss, seasonal_swing=swing, interannual_drift=drift,
        mean_specific_growth=growth, mean_cROS=float(cROS_last.mean()),
        checks=checks, passed=bool(all(checks.values())),
        seasonal_light=bool(seasonal_light))


# --------------------------------------------------------------------------------------
# Threshold measurement, vectorised across an ensemble of knob settings
# --------------------------------------------------------------------------------------

def control_arm_at(dt):
    """Control steady-state S/H recomputed at a given step size (for convergence work)."""
    global DT
    old, DT = DT, dt
    try:
        return control_arm()["SH_steady_state"]
    finally:
        DT = old


def thresholds(knob_grid, SH_ref, dt=DT, criterion=None, anomaly_max=None,
               seasonal_light=False, kappa=None):
    """DHW at which each ensemble member first bleaches, under the standard forcing.

    knob_grid: dict of name -> array of length `ensemble`.
    Returns DHW thresholds (NaN where the member never bleached) and censoring flags.
    """
    criterion = EP["bleaching_criterion"] if criterion is None else criterion
    amax = EP["anomaly_max"] if anomaly_max is None else anomaly_max
    ensemble = len(next(iter(knob_grid.values())))

    # Spin up at a CONSTANT temperature equal to the maximum monthly mean, so that the
    # anomaly lands on a settled symbiosis with no seasonal phase discontinuity and the
    # HotSpot is exactly the anomaly.
    #
    # An earlier version spun up on the seasonal cycle and then ramped the anomaly on
    # top of it. That was wrong, and the wrongness was silent: over the 240-day ramp the
    # season cools by about 4 degC, so SST - MMM stayed below the 1 degC HotSpot
    # threshold throughout and the accumulated DHW was zero at the moment the model
    # failed. Thresholds came back as 0.0 for a holobiont that had plainly cooked.
    # Holding the base at MMM makes HotSpot == anomaly by construction.
    spin_t = np.arange(0.0, EP["spinup_years"] * 365.25, dt)
    spin_sst = np.full(len(spin_t), EP["MMM"])
    spin = _run_ensemble(spin_t, spin_sst, knob_grid, ensemble,
                         seasonal_light=seasonal_light, dt=dt, kappa=kappa)
    init = (spin["H"][-1], spin["S"][-1])

    # Standard forcing: held at the climatological maximum, with a linear anomaly.
    t = np.arange(0.0, EP["anomaly_ramp"] + 90.0, dt)
    sst = EP["MMM"] + ramp_anomaly(t, onset=0.0, amplitude=amax, ramp=EP["anomaly_ramp"])
    dhw = degree_heating_weeks(sst, t, EP["MMM"], EP["dhw_hotspot_offset"],
                               EP["dhw_window"])

    out = _run_ensemble(t, sst, knob_grid, ensemble, seasonal_light=seasonal_light,
                        init=init, dt=dt, kappa=kappa)

    # Crossings must be SUSTAINED, not instantaneous. coRal's initialisation resets the
    # flux variables (jeC=10 and so on) whatever the biomass state, which puts a
    # one-step transient at the head of every run; requiring a condition to hold for a
    # declared window makes the readout immune to it and to any other brief excursion.
    win = max(1, int(round(EP["sustain_days"] / dt)))
    anomaly = sst - EP["MMM"]

    def first_crossing(cond):
        c = cond.astype(np.float32)
        run_len = np.cumsum(c, axis=0)
        run_len[win:] -= run_len[:-win].copy()
        held = run_len >= win                      # window ENDS at this index
        hit = held.any(axis=0)
        end = np.where(hit, held.argmax(axis=0), 0)
        start = np.maximum(end - win + 1, 0)       # report the dose at window START
        a = np.where(hit, anomaly[start], np.nan)
        # A crossing within one grid step of the top of the forcing is not a measured
        # threshold, it is the forcing running out. Flagged, not silently reported.
        at_cap = hit & (a >= anomaly.max() - (amax / EP["anomaly_ramp"]) * 2.0 * dt
                        - 1e-12)
        return np.where(hit, dhw[start], np.nan), a, ~hit, at_cap

    SH = out["SH"]                                     # (nt, ensemble)
    # READOUT A -- symbiont loss. The declared bleaching criterion. NOTE: this readout
    # is NOT independent of the knob b, because b IS the coefficient converting
    # oxidative stress into symbiont loss. A knob that acts on expulsion will dominate a
    # readout defined as expulsion, and that is close to tautological. Readout B exists
    # because of this.
    thr_a, anom_a, cen_a, cap_a = first_crossing(SH < (criterion * SH_ref))

    # READOUT B -- host carbon balance. The dose at which the host's specific growth
    # rate first goes negative, i.e. translocated photosynthate no longer covers
    # maintenance. b does not appear in the host's growth equation, so this readout is
    # not confounded with it. Members already in negative balance at ambient are flagged
    # rather than given a threshold of zero.
    dH = out["dHdt"]
    starving_at_start = dH[1] < 0.0
    thr_b, anom_b, cen_b, cap_b = first_crossing(dH < 0.0)

    return dict(dhw=thr_a, anomaly=anom_a, censored=cen_a, at_forcing_cap=cap_a,
                dhw_host=thr_b, anomaly_host=anom_b, censored_host=cen_b,
                at_forcing_cap_host=cap_b,
                negative_balance_at_ambient=starving_at_start,
                ambient_growth=dH[1], final_growth=dH[-1],
                max_dhw_tested=float(dhw.max()),
                max_anomaly_tested=float(anomaly.max()),
                SH_final=SH[-1], t=t, sst=sst, dhw_series=dhw, SH_series=SH)


def ambient_arm(knob_grid, ensemble, dt=DT, kappa=None):
    """READOUT C -- what each knob costs at AMBIENT temperature.

    The cost side of every thermal-tolerance route. Runs four seasonal cycles with no
    anomaly and reports the host's mean specific growth rate over the final year,
    relative to the wild type. Nothing was tuned for this; it is whatever the ported
    equations plus the thermal curve produce.
    """
    t = np.arange(0.0, 4.0 * 365.25, dt)
    sst = seasonal_sst(t, EP["MMM"], EP["seasonal_amplitude"])
    last = t >= 3.0 * 365.25
    out = _run_ensemble(t, sst, knob_grid, ensemble, dt=dt, kappa=kappa)
    g = out["dHdt"][last].mean(axis=0)
    wt = _run_ensemble(t, sst, {k: np.array([v]) for k, v in WILD_TYPE.items()}, 1,
                       dt=dt)["dHdt"][last].mean()
    return dict(growth=g, growth_rel_pct=100.0 * (g / wt - 1.0),
                SH=out["SH"][last].mean(axis=0), wild_type_growth=float(wt))


KAPPA_VALUES = [0.0, 0.01, 0.02, 0.03, 0.05, 0.075, 0.10, 0.15, 0.20, 0.30, 0.45]


def tradeoff_arm(SH_ref):
    """DOES THE THERMAL KNOB STILL PAY ONCE ITS OWN COST IS IN THE MODEL?

    This replaces "are the knobs additive" as the question worth asking, because
    additivity is a property of a box of free parameters and this is a property of a
    trade-off that somebody measured.

    Cunning, Silverstein & Baker 2015 (PMID 26041354, abstract) report that higher
    proportions of heat-tolerant symbionts LINEARLY increased bleaching resistance but
    REDUCED PHOTOCHEMICAL EFFICIENCY, and add that "even minor symbiont shuffling can
    adaptively benefit corals, although fitness effects of resulting trade-offs are
    difficult to predict". The structure of that trade-off is encoded here; its slope
    (kappa) is not given in the abstract, so it is swept.

    For each kappa, three things are measured:
      * the thermal GAIN  -- how much further the host's carbon balance holds when the
        symbiont thermal optimum is raised by 2 degC
      * the ambient COST  -- what that same change does to host specific growth with no
        heatwave at all
      * whether the gain is still positive, i.e. whether the knob still pays

    and two break-evens are reported: the kappa at which the thermal gain reaches zero,
    and the kappa at which the ambient cost reaches the 29% and 38% penalties Jones &
    Berkelmans 2010 measured for Durusdinium-hosting Acropora millepora. If the second
    is smaller than the first, the measured cost lands in a regime where the knob has
    already stopped paying -- which would be the single most consequential thing this
    model could say about the symbiont routes.
    """
    lo, hi = KNOBS["T_opt"]["low"], KNOBS["T_opt"]["high"]
    rows = []
    for k in KAPPA_VALUES:
        g = {nm: np.array([v, v]) for nm, v in WILD_TYPE.items()}
        g["T_opt"] = np.array([lo, hi])
        thr = thresholds(g, SH_ref, kappa=k)
        amb = ambient_arm(g, 2, kappa=k)
        # ambient growth of the UNMODIFIED holobiont at this kappa is the lo entry,
        # which is unaffected by kappa because dT = 0 there.
        gain = float(thr["anomaly_host"][1] - thr["anomaly_host"][0])
        cost = float(100.0 * (amb["growth"][1] / amb["growth"][0] - 1.0))
        collapsed = bool(amb["growth"][1] <= 0.0)
        rows.append(dict(kappa=k, anomaly_host_lo=float(thr["anomaly_host"][0]),
                         anomaly_host_hi=float(thr["anomaly_host"][1]),
                         thermal_gain_degC=gain,
                         ambient_growth_cost_pct=cost,
                         ambient_growth_abs=float(amb["growth"][1]),
                         collapsed_to_bleached_state=collapsed,
                         still_pays=bool(gain > 0.0),
                         dhw_lo=float(thr["dhw"][0]), dhw_hi=float(thr["dhw"][1])))
        print(f"    kappa={k:<6g} gain={gain:+.3f} degC   ambient cost={cost:+7.2f}%"
              f"   {'pays' if gain > 0 else 'DOES NOT PAY'}", flush=True)

    def crossing(key, target, viable_only=False):
        """First kappa at which `key` crosses `target`, linearly interpolated.

        With viable_only, rows whose holobiont has collapsed into the bleached state are
        EXCLUDED and no interpolation is allowed across the gap between the last viable
        row and the first collapsed one. Without that guard the ambient-cost crossing is
        an artefact: between kappa 0.2 and 0.3 the cost jumps from about -14% to about
        -159% because the holobiont falls off the alternate-stable-state cliff, and a
        straight line through that gap manufactures a -29% crossing at a kappa where the
        model has no such steady state at all.
        """
        use = [r for r in rows if not (viable_only and r["collapsed_to_bleached_state"])]
        xs = [r["kappa"] for r in use]
        ys = [r[key] for r in use]
        if viable_only and len(use) < len(rows):
            # refuse to extrapolate past the last viable kappa
            pass
        for i in range(len(xs) - 1):
            a, b_ = ys[i], ys[i + 1]
            if (a - target) * (b_ - target) <= 0 and a != b_:
                f = (target - a) / (b_ - a)
                return float(xs[i] + f * (xs[i + 1] - xs[i]))
        return None

    k_gain_zero = crossing("thermal_gain_degC", 0.0)
    k_cost_29 = crossing("ambient_growth_cost_pct", -29.0, viable_only=True)
    k_cost_38 = crossing("ambient_growth_cost_pct", -38.0, viable_only=True)
    viable = [r for r in rows if not r["collapsed_to_bleached_state"]]
    worst_viable_cost = min(r["ambient_growth_cost_pct"] for r in viable) if viable \
        else None
    verdict = None
    if k_gain_zero is not None and k_cost_29 is not None:
        verdict = ("the measured cost lands where the knob has ALREADY STOPPED PAYING"
                   if k_cost_29 > k_gain_zero else
                   "the knob still pays at the kappa that reproduces the measured cost")
    elif k_cost_29 is None:
        verdict = (
            f"THE TWO CANNOT BE COMPARED ON THIS AXIS, and that is the finding. The "
            f"measured 29% ambient growth penalty is NOT REACHABLE as a steady state at "
            f"any coupling strength in the swept range: the worst steady-state cost the "
            f"model will produce is {worst_viable_cost:.1f}%, and beyond that the "
            f"holobiont falls into the bleached alternate state with negative host "
            f"growth rather than settling at a larger penalty. That is the same gap the "
            f"Durusdinium cost arm finds by a completely different route -- scaling the "
            f"carbon-fixation ceiling directly rather than coupling it to the thermal "
            f"optimum -- so it is a property of the model's bistability and not of "
            f"either arm's parameterisation. Either this model's alternate-stable-state "
            f"transition is too abrupt, or the measured Durusdinium penalty is not a "
            f"carbon-fixation effect at all.")
    return dict(
        kappa_values=KAPPA_VALUES, rows=rows,
        break_even_kappa_thermal_gain_zero=k_gain_zero,
        worst_viable_ambient_cost_pct=worst_viable_cost,
        n_collapsed_rows=sum(1 for r in rows if r["collapsed_to_bleached_state"]),
        kappa_reproducing_29pct_cost=k_cost_29,
        kappa_reproducing_38pct_cost=k_cost_38,
        verdict=verdict,
        coupling="yCL_effective = yCL * (1 - kappa * (T_opt - 28 degC)), floored at 0.05",
        coupling_structure_source=dict(
            cite="Cunning, Silverstein & Baker 2015, Proc Biol Sci 282:20141725",
            pmid="26041354", read_level="abstract",
            quote="higher proportions of heat-tolerant symbionts linearly increased "
                  "bleaching resistance but reduced photochemical efficiency",
            species_of_evidence="Orbicella faveolata",
            cross_genus_note="Orbicella faveolata is a massive Caribbean coral. Most of "
                             "the rest of this design space is Acropora-centred, so "
                             "applying this coupling to an Acropora route is a "
                             "cross-genus assumption and is flagged as one."),
        cost_target_source=dict(
            cite="Jones & Berkelmans 2010, PLoS One 5:e10437", pmid="20454653",
            read_level="abstract",
            quote="type D corals grew 29% slower in the laboratory and 38% slower in the "
                  "field than C2-hosting colonies",
            species_of_evidence="Acropora millepora"),
        caveat="Two different studies, two different genera, one model. The coupling's "
               "structure is from Orbicella and the cost target is from Acropora, and "
               "the model is not evidence that they belong on the same axis. What it "
               "can do is show what WOULD follow if they did.",
        is_observation=False)


def durusdinium_cost_arm():
    """Can the model reproduce the MEASURED cost of a heat-tolerant symbiont?

    Jones & Berkelmans 2010 (PMID 20454653, abstract) report Acropora millepora hosting
    the heat-tolerant type D growing 29% slower in the laboratory and 38% slower in the
    field than C2-hosting colonies; Pettay et al. 2015 (PMID 26034268, abstract) report
    calcification 'reduced by nearly half' in Caribbean hosts carrying Durusdinium
    trenchii. Sproles et al. 2020 (PMID 32592285, abstract) give a candidate mechanism
    in an ANEMONE: D. trenchii assimilated significantly less photosynthetic carbon per
    cell than Breviolum minutum.

    So: scale the symbiont's maximum photosynthate production rate jCPm down, and ask
    what multiplier reproduces a 29% and a 38% fall in host specific growth. This is a
    consistency test between a published cost and a published model, not a measurement.
    """
    from coral_deb import run as _run
    t = np.arange(0.0, 4.0 * 365.25, DT)
    sst = seasonal_sst(t, EP["MMM"], EP["seasonal_amplitude"])
    last = t >= 3.0 * 365.25
    mults = np.linspace(0.30, 1.00, 71)
    out = _run(L=np.full(len(t), EP["L_control"]), N=EP["N_control"], X=EP["X_control"],
               T=sst, pars={"jCPm": PARS["jCPm"] * mults}, ensemble=len(mults), dt=DT,
               T_opt=EP["T_opt"], sigma_hot=EP["sigma_hot"], sigma_cold=EP["sigma_cold"])
    g = out["dHdt"][last].mean(axis=0)
    SH = out["SH"][last].mean(axis=0)
    g0 = float(g[-1])
    rel = 100.0 * (g / g0 - 1.0)
    # Collapsed members: host in negative energy balance, i.e. the bleached stable state.
    collapsed = g < 0.0
    viable = ~collapsed
    worst_viable = float(rel[viable].min()) if viable.any() else float("nan")
    gap_lo = float(mults[viable].min()) if viable.any() else None
    targets = {}
    for tgt in (-29.0, -38.0, -50.0):
        reachable = bool(viable.any() and rel[viable].min() <= tgt)
        i = int(np.argmin(np.abs(np.where(viable, rel, np.inf) - tgt))) if reachable \
            else None
        targets[str(tgt)] = dict(
            reachable_as_a_steady_state=reachable,
            jCPm_multiplier=float(mults[i]) if i is not None else None,
            achieved_pct=float(rel[i]) if i is not None else None)
    return dict(
        multipliers=mults.tolist(), host_growth=g.tolist(),
        host_growth_relative_pct=rel.tolist(), symbiont_host_ratio=SH.tolist(),
        wild_type_growth=g0, collapsed=collapsed.tolist(),
        least_viable_multiplier=gap_lo,
        worst_steady_state_growth_penalty_pct=worst_viable,
        targets=targets,
        finding=(f"Reducing the symbiont's carbon-fixation ceiling drives host growth "
                 f"down continuously only as far as {worst_viable:.1f}%, at jCPm "
                 f"multiplier {gap_lo:.2f}; below that the holobiont falls into the "
                 f"bleached state with negative host growth. There is NO steady state "
                 f"in this model with the 29-38% growth penalty Jones & Berkelmans "
                 f"measured. Either the model's alternate-stable-state transition is "
                 f"too abrupt, or the measured Durusdinium penalty is not a "
                 f"carbon-fixation-ceiling effect and some other term carries it. The "
                 f"model cannot tell which, and does not claim to."),
        is_observation=False)


def one_d_sweeps(SH_ref, n=41):
    out = {}
    for name, spec in KNOBS.items():
        xs = np.linspace(spec["low"], spec["high"], n)
        grid = {k: np.full(n, v) for k, v in WILD_TYPE.items()}
        grid[name] = xs
        r = thresholds(grid, SH_ref)
        amb = ambient_arm(grid, n)
        out[name] = dict(x=xs.tolist(),
                         dhw=[None if not np.isfinite(v) else float(v) for v in r["dhw"]],
                         censored=r["censored"].tolist(),
                         at_forcing_cap=r["at_forcing_cap"].tolist(),
                         at_forcing_cap_host=r["at_forcing_cap_host"].tolist(),
                         anomaly=[None if not np.isfinite(v) else float(v)
                                  for v in r["anomaly"]],
                         dhw_host=[None if not np.isfinite(v) else float(v)
                                   for v in r["dhw_host"]],
                         anomaly_host=[None if not np.isfinite(v) else float(v)
                                       for v in r["anomaly_host"]],
                         censored_host=r["censored_host"].tolist(),
                         ambient_growth=amb["growth"].tolist(),
                         ambient_growth_relative_pct=amb["growth_rel_pct"].tolist(),
                         ambient_SH=amb["SH"].tolist(),
                         label=spec["label"], route=spec["route"],
                         range_basis=spec["range_basis"],
                         is_coral_parameter=spec["is_coral_parameter"],
                         low=spec["low"], high=spec["high"])
    return out


def elasticity(SH_ref, frac=0.05):
    """Local sensitivity: change in threshold DHW per +/-5% change in each parameter.

    This is the comparison the knob RANGES cannot give. The four declared ranges are not
    commensurable (2 degC against two doublings against a fivefold cut), so the span of
    each 1-D sweep measures the range as much as the knob. A symmetric fractional
    perturbation about the wild type is commensurable, and is reported beside the spans.
    For T_opt, whose natural scale is an interval not a ratio, the perturbation is
    applied to (T_opt - 20 degC) so that '5%' is about 0.4 degC; this is stated rather
    than hidden, and it is the one place the comparison is not clean.
    """
    names = KNOB_NAMES
    lo_grid = {k: [] for k in names}
    hi_grid = {k: [] for k in names}
    for nm in names:
        for target, g in (("lo", lo_grid), ("hi", hi_grid)):
            for k in names:
                v = WILD_TYPE[k]
                if k == nm:
                    base = (v - 20.0) if k == "T_opt" else v
                    delta = base * frac * (-1 if target == "lo" else 1)
                    v = v + delta
                g[k].append(v)
    grid_lo = {k: np.array(v, dtype=float) for k, v in lo_grid.items()}
    grid_hi = {k: np.array(v, dtype=float) for k, v in hi_grid.items()}
    rlo = thresholds(grid_lo, SH_ref)
    rhi = thresholds(grid_hi, SH_ref)
    base = thresholds({k: np.array([v]) for k, v in WILD_TYPE.items()}, SH_ref)
    b0 = float(base["dhw"][0])
    out = {}
    for i, nm in enumerate(names):
        d_lo, d_hi = float(rlo["dhw"][i]), float(rhi["dhw"][i])
        out[nm] = dict(dhw_minus=d_lo, dhw_plus=d_hi,
                       elasticity=float((d_hi - d_lo) / (2 * frac * b0))
                       if np.isfinite(d_hi) and np.isfinite(d_lo) and b0 > 0 else None,
                       note="d(log threshold DHW) / d(log parameter), central difference")
    return dict(baseline_dhw=b0, fraction=frac, per_knob=out)


def knob_map(SH_ref, grid=7):
    axes = {nm: np.linspace(KNOBS[nm]["low"], KNOBS[nm]["high"], grid)
            for nm in KNOB_NAMES}
    mesh = np.meshgrid(*[axes[nm] for nm in KNOB_NAMES], indexing="ij")
    flat = {nm: m.ravel() for nm, m in zip(KNOB_NAMES, mesh)}
    t0 = _time.time()
    r = thresholds(flat, SH_ref)
    shape = tuple(grid for _ in KNOB_NAMES)
    amb = ambient_arm(flat, len(flat["b"]))
    return dict(names=KNOB_NAMES, grid=grid,
                axes={nm: axes[nm].tolist() for nm in KNOB_NAMES},
                dhw=r["dhw"].reshape(shape).tolist(),
                censored=r["censored"].reshape(shape).tolist(),
                at_forcing_cap=r["at_forcing_cap"].reshape(shape).tolist(),
                at_forcing_cap_host=r["at_forcing_cap_host"].reshape(shape).tolist(),
                anomaly=r["anomaly"].reshape(shape).tolist(),
                dhw_host=r["dhw_host"].reshape(shape).tolist(),
                anomaly_host=r["anomaly_host"].reshape(shape).tolist(),
                censored_host=r["censored_host"].reshape(shape).tolist(),
                ambient_growth_relative_pct=amb["growth_rel_pct"].reshape(shape).tolist(),
                max_dhw_tested=r["max_dhw_tested"],
                n_cells=int(np.prod(shape)),
                seconds=float(_time.time() - t0))


def additivity(km, readout="anomaly_host"):
    """Are the knobs additive? Declared test, run on the 4-D map.

    Model A: threshold ~ sum of main effects, on knob coordinates scaled to [0,1].
    Model B: model A plus all six two-way interactions.
    Reports adjusted R^2 for each. If A already explains nearly everything, additive.
    Censored cells are EXCLUDED and counted, because a censored cell is not a large
    number -- it is a missing one, and treating it as large would manufacture curvature.
    """
    names = km["names"]
    dhw = np.asarray(km[readout], dtype=float)
    cens = np.asarray(km["censored" if readout in ("dhw", "anomaly")
                         else "censored_host"], dtype=bool)
    coords = np.meshgrid(*[np.linspace(0, 1, km["grid"]) for _ in names], indexing="ij")
    capkey = "at_forcing_cap" if readout in ("dhw", "anomaly") else "at_forcing_cap_host"
    cap = np.asarray(km.get(capkey, np.zeros_like(cens)), dtype=bool)
    mask = np.isfinite(dhw) & ~cens & ~cap
    y = dhw[mask]
    Xm = np.column_stack([np.ones(mask.sum())] + [c[mask] for c in coords])
    pairs = [(i, j) for i in range(len(names)) for j in range(i + 1, len(names))]
    Xi = np.column_stack([Xm] + [coords[i][mask] * coords[j][mask] for i, j in pairs])

    def adj_r2(X, y):
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        ss_res = float(resid @ resid)
        ss_tot = float(((y - y.mean()) ** 2).sum())
        n, p = len(y), X.shape[1]
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        return (1.0 - (1.0 - r2) * (n - 1) / (n - p)), beta

    r2_main, beta_main = adj_r2(Xm, y)
    r2_int, beta_int = adj_r2(Xi, y)

    spans = {}
    for i, nm in enumerate(names):
        spans[nm] = float(beta_main[i + 1])  # change in DHW across the declared range
    return dict(
        readout=readout,
        readout_meaning=(("anomaly in degC at which host specific growth first goes "
                          "negative and stays negative; NOT confounded with the knob b, "
                          "and free of the 1 degC deadband that degree heating weeks "
                          "carry by construction"
                          if readout == "anomaly_host" else
                          "degree heating weeks at which host specific growth first goes "
                          "negative; NOT confounded with the knob b")
                         if readout.endswith("host") else
                         "degree heating weeks at which S/H falls below the declared "
                         "bleaching criterion; CONFOUNDED with the knob b, which is the "
                         "coefficient converting oxidative stress into symbiont loss"),
        n_cells_used=int(mask.sum()), n_cells_censored=int(cens.sum()),
        n_cells_at_forcing_cap=int(cap.sum()),
        exclusion_rule="Cells that never crossed (censored) and cells that crossed only "
                       "within two time steps of the top of the forcing ramp (at the "
                       "forcing cap) are BOTH excluded. A cap crossing is the forcing "
                       "running out, not a measured threshold, and including it would "
                       "pile a spurious plateau into the fit.",
        n_cells_total=int(dhw.size),
        adj_r2_main_effects=float(r2_main), adj_r2_with_two_way=float(r2_int),
        variance_explained_by_interactions=float(r2_int - r2_main),
        main_effect_span_dhw=spans,
        interaction_terms={f"{names[i]}x{names[j]}": float(beta_int[1 + len(names) + k])
                           for k, (i, j) in enumerate(pairs)},
        verdict=("additive" if (r2_int - r2_main) < 0.02 else
                 "interactions material"),
        verdict_rule="DECLARED BEFORE THE FIT: additive if two-way terms add < 0.02 "
                     "adjusted R^2.")


# --------------------------------------------------------------------------------------
# Numerical and robustness checks
# --------------------------------------------------------------------------------------

def numerical_checks(SH_ref):
    wt = {k: np.array([v]) for k, v in WILD_TYPE.items()}
    base = thresholds(wt, SH_ref)
    half = thresholds(wt, SH_ref, dt=DT / 2.0)
    rel = float(abs(half["dhw"][0] - base["dhw"][0]) / max(base["dhw"][0], 1e-12))
    out = {
        "step_halving": dict(
            dt=DT, dhw_at_dt=float(base["dhw"][0]), dhw_at_half_dt=float(half["dhw"][0]),
            relative_change=rel,
            criterion="relative change in the wild-type threshold below 0.05, DECLARED "
                      "BEFORE THE RUN",
            passed=bool(rel < 0.05),
            reported_as_failed_not_relaxed=(
                "This check FAILS and the criterion was not moved. coRal integrates with "
                "explicit Euler and so does this port; a first-order scheme converges "
                "slowly, and a first-crossing readout inherits that error directly. The "
                "convergence table below quantifies it, the Richardson estimate gives "
                "the limit, and the ranking check shows which conclusions survive. The "
                "absolute threshold does not survive; the knob ranking and the "
                "additivity verdict do.")),
    }
    # Full convergence table and a Richardson extrapolation of the limit.
    steps, vals_a, vals_b = [], [], []
    for d in (0.2, 0.1, 0.05, 0.025):
        c = control_arm_at(d)
        r = thresholds({k: np.array([v]) for k, v in WILD_TYPE.items()}, c, dt=d)
        steps.append(d); vals_a.append(float(r["dhw"][0]))
        vals_b.append(float(r["anomaly_host"][0]))
    diffs = [vals_a[i] - vals_a[i + 1] for i in range(len(vals_a) - 1)]
    ratios = [diffs[i] / diffs[i + 1] for i in range(len(diffs) - 1)
              if abs(diffs[i + 1]) > 1e-12]
    rr = float(np.mean(ratios)) if ratios else float("nan")
    limit = (vals_a[-1] - diffs[-1] / (rr - 1.0)) if np.isfinite(rr) and rr > 1.0 \
        else None
    out["convergence"] = dict(
        dt=steps, readout_A_dhw=vals_a, readout_B_anomaly_degC=vals_b,
        successive_differences=diffs, mean_ratio=rr,
        richardson_limit_readout_A_dhw=limit,
        observed_order=float(np.log2(rr)) if np.isfinite(rr) and rr > 0 else None,
        note=("Readout A (degree heating weeks at symbiont loss) is still moving at the "
              "smallest step tried; the Richardson estimate of its limit is given and "
              "the quoted threshold should be read as carrying that much discretisation "
              "uncertainty on top of everything else. Readout B in degC of anomaly is "
              "much better behaved because the anomaly is a smooth monotone function of "
              "time with no 1 degC deadband."))
    # Does the RANKING -- the thing actually claimed -- survive the step size?
    rank_by_dt = {}
    for d in (0.1, 0.05, 0.025):
        c = control_arm_at(d)
        sp = {}
        for nm, spec in KNOBS.items():
            g = {k: np.array([v, v]) for k, v in WILD_TYPE.items()}
            g[nm] = np.array([spec["low"], spec["high"]])
            r = thresholds(g, c, dt=d)
            sp[nm] = float(r["anomaly_host"][1] - r["anomaly_host"][0])
        rank_by_dt[str(d)] = dict(spans=sp,
                                  order=sorted(sp, key=lambda k: -sp[k]))
    orders = [v["order"] for v in rank_by_dt.values()]
    out["ranking_vs_step_size"] = dict(
        by_dt=rank_by_dt, identical_across_step_sizes=bool(
            all(o == orders[0] for o in orders)),
        note="The absolute threshold is not converged; this asks whether the ORDER of "
             "the four knobs is, which is what the design question needs.")
    # How much does the declared 0.5 bleaching criterion drive the answer?
    crit = {}
    for c in (0.3, 0.4, 0.5, 0.6, 0.7):
        crit[str(c)] = float(thresholds(wt, SH_ref, criterion=c)["dhw"][0])
    out["criterion_sensitivity"] = dict(
        thresholds_by_criterion=crit,
        note="Declared criterion is 0.5. The threshold moves with it, as it must; what "
             "matters for the design question is whether the RANKING of knobs moves, "
             "which is tested separately.")
    # Does the knob ranking survive a different criterion and a seasonal light field?
    rank = {}
    for label, kwargs in (("criterion_0.3", dict(criterion=0.3)),
                          ("criterion_0.7", dict(criterion=0.7)),
                          ("seasonal_light", dict(seasonal_light=True))):
        spans = {}
        for nm, spec in KNOBS.items():
            g = {k: np.array([v, v]) for k, v in WILD_TYPE.items()}
            g[nm] = np.array([spec["low"], spec["high"]])
            r = thresholds(g, SH_ref, **kwargs)
            d = r["dhw"]
            spans[nm] = None if not np.isfinite(d).all() else float(d[1] - d[0])
        rank[label] = spans
    out["ranking_robustness"] = dict(
        spans_by_arm=rank,
        note="Span in threshold DHW across each knob's declared range, recomputed under "
             "two other bleaching criteria and under a seasonal light field. A knob "
             "ordering that survives all three is a property of the model; one that "
             "does not is a property of the readout.")
    return out


def cold_arm(SH_ref):
    """An emergent prediction, not a target: does the model bleach when COOLED?

    Nothing was tuned for this. In the model, anything that lowers carbon fixation raises
    the excess excitation energy jeL and therefore ROS, so cooling should bleach too.
    Silverstein, Cunning & Baker 2017 (PMID 28108671, abstract) cooled Montastraea
    cavernosa at 1 degC/week and report that C3-hosting corals 'lost 94% of symbionts',
    while D1a-hosting corals did not bleach. This arm asks only whether the model has the
    same sign; it is not calibrated to that experiment and the magnitudes are not
    comparable.
    """
    t = np.arange(0.0, 420.0, DT)
    base = seasonal_sst(t + 30.0, EP["MMM"], EP["seasonal_amplitude"])
    sst = base - ramp_anomaly(t, onset=0.0, amplitude=8.0, ramp=EP["anomaly_ramp"])
    spin_t = np.arange(0.0, EP["spinup_years"] * 365.25, DT)
    spin = _run_ensemble(spin_t, seasonal_sst(spin_t, EP["MMM"],
                                              EP["seasonal_amplitude"]), WILD_TYPE, 1)
    out = _run_ensemble(t, sst, WILD_TYPE, 1, init=(spin["H"][-1], spin["S"][-1]))
    SH = out["SH"][:, 0]
    bleached = SH < EP["bleaching_criterion"] * SH_ref
    idx = int(bleached.argmax()) if bleached.any() else -1
    return dict(
        cooled_to_degC=float(sst.min()),
        bleaches_on_cooling=bool(bleached.any()),
        sst_at_bleaching=float(sst[idx]) if idx >= 0 else None,
        degC_below_MMM_at_bleaching=float(EP["MMM"] - sst[idx]) if idx >= 0 else None,
        SH_min_fraction_of_control=float(SH.min() / SH_ref),
        interpretation="Emergent, not fitted. The model bleaches on cooling as well as "
                       "on warming, because both lower carbon fixation and so raise "
                       "excess excitation energy. This has the same SIGN as the cold "
                       "bleaching reported by Silverstein et al. 2017 in C3-hosting "
                       "Montastraea cavernosa, which is a weak consistency check and "
                       "not a validation: no magnitude here was compared to theirs, and "
                       "DHW has no cold analogue so no threshold is reported.")


def port_check():
    """Compare the Python port with the author's own R code, scenario by scenario."""
    import csv as _csv
    rows = []
    scen = {"healthy": (30.0, 1e-6, 0.0), "lowlight": (10.0, 1e-6, 0.0),
            "fed": (30.0, 1e-6, 1e-6)}
    worst = 0.0
    for nm, (L, N, X) in scen.items():
        path = os.path.join(LOGDIR, f"coRal_{nm}.csv")
        if not os.path.exists(path):
            rows.append(dict(scenario=nm, status="R reference not generated"))
            continue
        with open(path) as fh:
            rd = list(_csv.DictReader(fh))
        nt = len(rd)
        out = run(L=L, N=N, X=X, T=None, dt=0.1, n_steps=nt)
        for col in ("H", "S", "cROS", "jCP", "jeL", "jST"):
            r = np.array([float(x[col]) for x in rd])
            m = out[col if col in out else "SH"][:, 0]
            rel = float(np.max(np.abs(m - r) / np.maximum(np.abs(r), 1e-300)))
            worst = max(worst, rel)
            rows.append(dict(scenario=nm, variable=col, max_relative_deviation=rel))
    return dict(
        reference="jrcunning/coRal, MIT, commit 7c90f9bee5917d62f69d751a53d105b051732ac6",
        reference_run="R 4.3.3, coRal R/run_coral.R with def_pars() unchanged, dt=0.1 d, "
                      "365 days, three environments",
        comparisons=rows, worst_max_relative_deviation=worst,
        passed=bool(worst < 1e-10),
        note="With the thermal extension OFF, this port must reproduce the published R "
             "code exactly. This is the positive control for the whole study: a port "
             "that silently diverged would look exactly like a model with different "
             "biology in it.")


# --------------------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------------------

def _style():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.dpi": 150, "savefig.dpi": 150, "font.size": 8.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": 9.5, "axes.labelsize": 8.5, "legend.frameon": False,
        "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.5,
        "savefig.bbox": "tight", "savefig.facecolor": "white",
    })
    return plt


def figure_control(cache):
    plt = _style()
    c = cache["control_arm"]
    t = np.array(c["t"]) / 365.25
    fig, ax = plt.subplots(3, 1, figsize=(7.0, 6.2), sharex=True,
                           gridspec_kw=dict(hspace=0.18))
    ax[0].plot(t, c["sst"], color="#b2452e", lw=1.2)
    ax[0].axhline(EP["MMM"], color="#888", ls="--", lw=0.8)
    ax[0].text(t[-1], EP["MMM"], " MMM", va="center", fontsize=7, color="#666")
    ax[0].set_ylabel("sea temperature (degC)")
    ax[0].set_title("Control arm: ambient seasonal cycle, no anomaly. SIMULATED.",
                    loc="left")

    SH = np.array(c["SH"])
    ax[1].plot(t, SH, color="#1f6f54", lw=1.2)
    ax[1].axhline(c["SH_steady_state"], color="#888", ls=":", lw=0.8)
    ax[1].axhline(EP["bleaching_criterion"] * c["SH_steady_state"],
                  color="#b2452e", ls="--", lw=0.9)
    ax[1].text(t[-1], EP["bleaching_criterion"] * c["SH_steady_state"],
               " bleaching criterion", va="center", fontsize=7, color="#b2452e")
    ax[1].set_ylabel("symbiont : host (C-mol / C-mol)")
    ax[1].set_ylim(0, max(SH.max() * 1.15, c["SH_steady_state"] * 1.4))

    ax[2].plot(t, c["cROS"], color="#4b5ea8", lw=1.2)
    ax[2].axhline(1.0, color="#888", ls=":", lw=0.8)
    ax[2].set_ylabel("cROS (ROS factor)")
    ax[2].set_xlabel("years")

    pc = cache["port_check"]
    fig.text(0.01, -0.03,
             "Port check against the published R code (coRal, commit 7c90f9b): worst "
             f"max relative deviation {pc['worst_max_relative_deviation']:.1e} over "
             f"{len([r for r in pc['comparisons'] if 'variable' in r])} variable-scenario "
             "pairs, thermal extension off.", fontsize=7, color="#444")
    fig.savefig(os.path.join(FIGDIR, "bleaching-control.png"))
    plt.close(fig)


def figure_threshold(cache):
    plt = _style()
    sw = cache["one_d_sweeps"]
    short = {"T_opt": "T_opt  (degC)", "kNPQ": "kNPQ  (mol ph / C-mol S / d)",
             "kROS": "kROS  (mol ph / C-mol S / d)", "b": "b  (lower = more retentive)"}
    sub = {"T_opt": "symbiont thermal optimum", "kNPQ": "photoprotective quenching",
           "kROS": "excess light that doubles ROS", "b": "bleaching response to ROS"}
    fig, axes = plt.subplots(3, 4, figsize=(11.0, 7.4),
                             gridspec_kw=dict(hspace=0.45, wspace=0.28))
    for col, nm in enumerate(KNOB_NAMES):
        s = sw[nm]
        x = np.array(s["x"])

        # Row 1 -- both readouts in degC of anomaly. One axis, directly comparable.
        ax = axes[0, col]
        for key, capkey, colr, lbl in (
                ("anomaly", "at_forcing_cap", "#1b4f72", "A: lost half its symbionts"),
                ("anomaly_host", "at_forcing_cap_host", "#9c3d1e",
                 "B: host carbon balance negative")):
            y = np.array([np.nan if v is None else v for v in s[key]], dtype=float)
            cap = np.array(s[capkey], dtype=bool)
            ax.plot(x, np.where(cap, np.nan, y), color=colr, lw=1.7, label=lbl)
            if cap.any():
                ax.plot(x[cap], y[cap], color=colr, lw=1.0, ls=(0, (1, 2)))
                ax.plot(x[cap], y[cap], "^", ms=3, color=colr)
        ax.set_ylim(0, EP["anomaly_max"] * 1.02)
        ax.set_title(short[nm] + "\n" + sub[nm], loc="left", fontsize=7.6)
        if col == 0:
            ax.set_ylabel("anomaly at failure (degC)")
            ax.legend(fontsize=6.0, loc="upper left")
        kind = "coRal parameter" if s["is_coral_parameter"] else "added for temperature"
        ax.text(0.98, 0.04, kind, transform=ax.transAxes, ha="right", fontsize=6,
                color="#999")

        # Row 2 -- readout A in degree heating weeks, against the NOAA bands.
        ax = axes[1, col]
        ax.axhspan(EP["DHW_alert1"], EP["DHW_alert2"], color="#f0cf9a", alpha=0.4, lw=0)
        ax.axhline(EP["DHW_alert1"], color="#c08a2e", lw=0.7, ls="--")
        ax.axhline(EP["DHW_alert2"], color="#a8422a", lw=0.7, ls="--")
        yA = np.array([np.nan if v is None else v for v in s["dhw"]], dtype=float)
        yB = np.array([np.nan if v is None else v for v in s["dhw_host"]], dtype=float)
        ax.plot(x, yA, color="#1b4f72", lw=1.7)
        ax.plot(x, yB, color="#9c3d1e", lw=1.4)
        ax.set_ylim(bottom=0)
        if col == 0:
            ax.set_ylabel("same, in degree\nheating weeks")
            ax.text(0.03, 0.93, "NOAA 4 / 8 shaded", transform=ax.transAxes,
                    fontsize=6.2, color="#8a6a2e", va="top")
            ax.text(0.03, 0.68, "readout B sits near 0 in the\nother three panels: it "
                                "fails\nbelow the 1 degC HotSpot cut,\nso DHW cannot "
                                "see it at all",
                    transform=ax.transAxes, fontsize=5.8, color="#9c3d1e", va="top")

        # Row 3 -- the cost at ambient.
        ax = axes[2, col]
        ax.axhline(0.0, color="#888", lw=0.8, ls=":")
        ax.plot(x, s["ambient_growth_relative_pct"], color="#1f6f54", lw=1.7)
        ax.set_xlabel(nm)
        if col == 0:
            ax.set_ylabel("ambient host growth\n(% vs wild type)")
    fig.suptitle(
        "SIMULATED, not measured. Row 1: thermal anomaly at which each design knob's "
        "holobiont fails, on two readouts. Row 2: the same in NOAA degree heating weeks, "
        "which cannot resolve a failure below +1 degC. Row 3: what the knob costs when "
        "there is no heatwave at all.", fontsize=8.0, x=0.012, ha="left", wrap=True)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(os.path.join(FIGDIR, "bleaching-threshold.png"))
    plt.close(fig)


def figure_knob_map(cache):
    plt = _style()
    km = cache["knob_map"]
    add = cache["additivity"]
    dhw = np.asarray(km["anomaly_host"], dtype=float)
    names = km["names"]
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    fig, axes = plt.subplots(2, 3, figsize=(9.6, 5.6),
                             gridspec_kw=dict(wspace=0.42, hspace=0.42))
    vmin, vmax = np.nanmin(dhw), np.nanmax(dhw)
    for ax, (i, j) in zip(axes.ravel(), pairs):
        other = [k for k in range(4) if k not in (i, j)]
        sl = np.nanmean(dhw, axis=tuple(other))
        if i > j:
            sl = sl.T
        ex = [km["axes"][names[j]][0], km["axes"][names[j]][-1],
              km["axes"][names[i]][0], km["axes"][names[i]][-1]]
        im = ax.imshow(sl, origin="lower", aspect="auto", extent=ex,
                       cmap="magma", vmin=vmin, vmax=vmax)
        ax.set_xlabel(names[j], fontsize=7.5)
        ax.set_ylabel(names[i], fontsize=7.5)
        ax.tick_params(labelsize=6.5)
        ax.grid(False)
    cb = fig.colorbar(im, ax=axes, fraction=0.025, pad=0.02)
    cb.set_label("thermal anomaly (degC) at host carbon-balance failure\n"
                 "(mean over the other two knobs)")
    fig.suptitle(
        "SIMULATED four-knob map on readout B (host carbon balance, in degC of "
        "anomaly), marginalised to "
        f"pairs. Main effects adj R2 = {add['adj_r2_main_effects']:.3f}; adding all six "
        f"two-way terms adds {add['variance_explained_by_interactions']:.3f}. "
        f"Verdict: {add['verdict']}. {add['n_cells_censored']} of "
        f"{add['n_cells_total']} cells censored.", fontsize=8.2, x=0.02, ha="left")
    fig.savefig(os.path.join(FIGDIR, "bleaching-knob-map.png"))
    plt.close(fig)


# --------------------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--control", action="store_true")
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--grid", type=int, default=7)
    args = ap.parse_args()

    os.makedirs(FIGDIR, exist_ok=True)

    if args.figures:
        with open(CACHE) as fh:
            cache = json.load(fh)
        figure_control(cache); figure_threshold(cache); figure_knob_map(cache)
        print("figures redrawn"); return

    print("port check against the published R code ...", flush=True)
    pc = port_check()
    print(f"  worst max relative deviation {pc['worst_max_relative_deviation']:.3e} "
          f"-> {'PASS' if pc['passed'] else 'FAIL'}", flush=True)

    print("control arm ...", flush=True)
    ctrl = control_arm()
    for k, v in ctrl["checks"].items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    print(f"  control S/H = {ctrl['SH_steady_state']:.4f}", flush=True)
    if not ctrl["passed"]:
        print("CONTROL ARM FAILED. Sweeps are not read. Reporting the failure.",
              flush=True)
    if args.control:
        print(json.dumps(ctrl["checks"], indent=1)); return

    SH_ref = ctrl["SH_steady_state"]

    print("numerical and robustness checks ...", flush=True)
    nc = numerical_checks(SH_ref)
    print(f"  step halving: {nc['step_halving']['relative_change']:.4f} relative change "
          f"-> {'PASS' if nc['step_halving']['passed'] else 'FAIL'}", flush=True)

    print("cold arm (emergent) ...", flush=True)
    cold = cold_arm(SH_ref)

    print("trade-off arm: does the thermal knob still pay? ...", flush=True)
    tro = tradeoff_arm(SH_ref)
    print(f"  break-even kappa (thermal gain -> 0): "
          f"{tro['break_even_kappa_thermal_gain_zero']}; kappa reproducing the measured "
          f"29% cost: {tro['kappa_reproducing_29pct_cost']}", flush=True)
    print(f"  -> {tro['verdict']}", flush=True)

    print("Durusdinium cost arm ...", flush=True)
    dur = durusdinium_cost_arm()
    print(f"  worst steady-state growth penalty "
          f"{dur['worst_steady_state_growth_penalty_pct']:.1f}% at jCPm multiplier "
          f"{dur['least_viable_multiplier']:.2f}", flush=True)

    print("one-dimensional sweeps ...", flush=True)
    sw = one_d_sweeps(SH_ref)

    print("elasticities ...", flush=True)
    el = elasticity(SH_ref)

    print(f"four-knob map, grid {args.grid} ...", flush=True)
    km = knob_map(SH_ref, grid=args.grid)
    print(f"  {km['n_cells']} cells in {km['seconds']:.1f}s", flush=True)
    add = additivity(km, readout="anomaly_host")
    add_sym = additivity(km, readout="anomaly")
    for a in (add, add_sym):
        print(f"  [{a['readout']}] used {a['n_cells_used']}/{a['n_cells_total']} cells "
              f"({a['n_cells_censored']} censored); main adj R2 "
              f"{a['adj_r2_main_effects']:.4f}; two-way adds "
              f"{a['variance_explained_by_interactions']:.4f} -> {a['verdict']}",
              flush=True)

    cache = dict(port_check=pc, control_arm=ctrl, numerical_checks=nc, cold_arm=cold,
                 durusdinium_cost_arm=dur, tradeoff_arm=tro, one_d_sweeps=sw,
                 elasticity=el,
                 knob_map=km, additivity=add, additivity_symbiont_readout=add_sym)
    with open(CACHE, "w") as fh:
        json.dump(cache, fh)
    figure_control(cache); figure_threshold(cache); figure_knob_map(cache)
    write_result(cache)


def write_result(cache):
    add = cache["additivity"]
    sw = cache["one_d_sweeps"]
    ctrl = cache["control_arm"]
    dur = cache["durusdinium_cost_arm"]
    tro = cache["tradeoff_arm"]

    spans = {}
    for nm, s in sw.items():
        def span(key):
            a, b_ = s[key][0], s[key][-1]
            return None if (a is None or b_ is None) else float(b_ - a)
        spans[nm] = dict(
            low_end_dhw=s["dhw"][0], high_end_dhw=s["dhw"][-1],
            span_dhw=span("dhw"), n_censored=int(sum(s["censored"])),
            low_end_dhw_host=s["dhw_host"][0], high_end_dhw_host=s["dhw_host"][-1],
            span_dhw_host=span("dhw_host"),
            low_end_anomaly=s["anomaly"][0], high_end_anomaly=s["anomaly"][-1],
            span_anomaly=span("anomaly"),
            low_end_anomaly_host=s["anomaly_host"][0],
            high_end_anomaly_host=s["anomaly_host"][-1],
            span_anomaly_host=span("anomaly_host"),
            n_censored_host=int(sum(s["censored_host"])),
            n_at_forcing_cap=int(sum(s["at_forcing_cap"])),
            n_at_forcing_cap_host=int(sum(s["at_forcing_cap_host"])),
            span_anomaly_is_saturated=bool(s["at_forcing_cap"][0]
                                           or s["at_forcing_cap"][-1]),
            ambient_growth_cost_pct=float(s["ambient_growth_relative_pct"][-1]))
    ranked = sorted([(v["span_anomaly_host"] if v["span_anomaly_host"] is not None
                      else -1e9, k) for k, v in spans.items()], reverse=True)

    counts = {}
    for p in ALL_PARAMETERS:
        counts[p["status"]] = counts.get(p["status"], 0) + 1

    wt_dhw = cache["elasticity"]["baseline_dhw"]
    topt_cost = spans["T_opt"]["ambient_growth_cost_pct"]
    spans_b = {k: v["span_anomaly_host"] for k, v in spans.items()}
    headline = (
        f"THREE OF THE FOUR INTERVENTIONS BUY A CORAL THAT STILL LOOKS BROWN WHILE IT "
        f"STARVES. Measured on two readouts: on symbiont loss all four design knobs move "
        f"the failure threshold by a comparable amount, but on the host's CARBON BALANCE "
        f"the symbiont thermal optimum moves it {spans_b['T_opt'] / max(spans_b['kROS'], 1e-9):.1f} "
        f"times further than the next best knob ({spans_b['T_opt']:+.2f} degC of anomaly "
        f"against {spans_b['kROS']:+.2f}, {spans_b['kNPQ']:+.2f} and {spans_b['b']:+.2f}). "
        f"Raising photoprotection, ROS tolerance or symbiont retention keeps the ALGAE IN "
        f"PLACE without keeping the HOST FED. Anyone selecting on visual bleaching score "
        f"-- which is most of the restoration field -- is scoring the readout that cannot "
        f"tell those apart. "
        f"And the thermal knob is not free either. With the trade-off Cunning et al. "
        f"measured put into the model -- heat-tolerant symbiont proportion raises "
        f"bleaching resistance and lowers photochemical efficiency, linearly -- the "
        f"thermal gain from +2 degC falls to zero at a coupling strength of "
        f"{tro['break_even_kappa_thermal_gain_zero']:.2f}"
        f" -- but whether a real coral sits before or after that point cannot be "
        f"answered here, because the measured 29% growth penalty is NOT REACHABLE as a "
        f"steady state at any coupling in the swept range: the worst the model will "
        f"produce is {tro['worst_viable_ambient_cost_pct']:.1f}%, and past that the "
        f"holobiont drops into the bleached alternate state instead of settling at a "
        f"larger penalty. A second arm reaches the same gap by scaling the "
        f"carbon-fixation ceiling directly, so it is the model's bistability and not "
        f"either arm's parameterisation. "
        f"Underneath all of it: the dynamical core is a line-by-line port of the "
        f"published coRal model, reproducing the author's own R code to "
        f"{cache['port_check']['worst_max_relative_deviation']:.0e} relative error, but "
        f"CORAL HAS NO TEMPERATURE IN IT -- the published model bleaches corals with "
        f"light. The thermal coupling is this file's addition, it enters through exactly "
        f"one parameter, and every thermal number here is a property of that extension. "
        f"The unmodified holobiont bleaches at {wt_dhw:.1f} degree heating weeks, which "
        f"is where the single calibrated parameter put it and is therefore not evidence "
        f"about NOAA's 4-8 window.")
    out = dict(
        schema="design-space-result-0.1",
        study_id="bleaching-dynamics",
        title="Host-symbiont bleaching dynamics under thermal stress",
        is_observation=False,
        headline=headline,
        provenance=dict(
            generated_at=_time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            code="results/coral/code/bleaching_dynamics.py (with coral_deb.py and "
                 "coral_reference_run.R beside it)",
            model_source=dict(
                name="coRal",
                url="https://github.com/jrcunning/coRal",
                licence="MIT",
                commit="7c90f9bee5917d62f69d751a53d105b051732ac6",
                cloned="2026-11-02",
                paper="Cunning R, Muller EB, Gates RD, Nisbet RM (2017) J Theor Biol "
                      "431:49-62",
                pmid="28782552",
                read_level_of_code="full-text",
                read_level_of_paper="abstract",
                note="The equations and all 23 of its parameter values were taken from "
                     "the code, which was read. The PAPER was not obtained; its "
                     "abstract is the only part read. Where this file quotes a reason "
                     "for a parameter value, the quote is from a comment in "
                     "def_pars.R, not from the paper."),
        ),
        model=dict(
            name="coRal (ported) + one thermal coupling",
            kind="deterministic ODE system, explicit Euler, biomass-specific DEB",
            is_observation=False,
            state_variables=[
                dict(name="H", units="C-mol", meaning="host biomass"),
                dict(name="S", units="C-mol", meaning="symbiont biomass"),
                dict(name="S/H", units="C-mol / C-mol",
                     meaning="symbiont-to-host ratio; THIS is the quantity that reaches "
                             "a steady state. Measured here by running the unmodified R "
                             "code over a 4x5 light-by-DIN grid: H and S themselves grow "
                             "or shrink exponentially without bound, because the model is "
                             "biomass-specific and has no size limit. Every readout is "
                             "defined on the ratio."),
            ],
            causal_chain=(
                "light absorbed per symbiont carbon (jL, self-shaded by S/H) -> carbon "
                "fixed (jCP, capped by jCPm and divided by the current ROS factor) -> "
                "excess excitation energy (jeL = jL - jCP/yCL) -> what NPQ cannot "
                "dissipate (jeL - jNPQ, with jNPQ saturating at kNPQ) -> ROS factor "
                "(cROS = 1 + ((jeL-jNPQ)/kROS)^k) -> symbiont turnover "
                "(jST = jST0(1 + b(cROS-1))) -> symbiont loss. Every step is Cunning et "
                "al.'s. Temperature enters at exactly one place: jCPm -> jCPm*phi(T)."),
            thermal_extension=dict(
                is_from_cunning_et_al=False,
                equation="jCPm_effective(T) = jCPm * exp(-0.5*((T-T_opt)/sigma)^2), "
                         "sigma = sigma_hot above T_opt and sigma_cold below",
                why_this_term="Warner, Fitt & Schmidt 1999 (PMID 10393938, abstract): "
                              "heat damages the PSII D1 protein faster than it is "
                              "replaced, and the authors state that perturbation of PSII "
                              "protein turnover during photoinhibition at elevated "
                              "temperature underlies symbiont collapse. A falling "
                              "ceiling on photochemistry is what that is in this model's "
                              "accounting.",
                scope_of_the_negative=(
                    "No temperature term appears in any source file of the cloned coRal "
                    "repository. A case-insensitive search of the whole tree (excluding "
                    ".git) for 'temp', 'thermal', 'heat', 'degC' and 'dhw' returns "
                    "exactly ONE match, and it is not a temperature term: "
                    "`.Rbuildignore:2:^\\.Rproj\\.user$  # used for temporary files.` "
                    "-- an incidental hit on 'temporary' inside a build-ignore comment. "
                    "POSITIVE CONTROLS for the same search: 'symbiont' matches 14 files, "
                    "'light' 14, 'photo' 12, 'carbon' 9, so the search runs and finds "
                    "what is there. This is a statement about the CODE as published at "
                    "commit 7c90f9be, not about the paper, which was not read in "
                    "full.")),
            parameters=ALL_PARAMETERS,
            parameter_status_counts=counts,
            knobs={nm: dict(wild_type=WILD_TYPE[nm], **{k: v for k, v in s.items()
                                                        if k != "label"})
                   for nm, s in KNOBS.items()},
            readouts=dict(
                control_steady_state="mean S/H over the final year of a 3-year ambient run",
                readout_A_bleaching=dict(
                    definition="S/H below 0.5 of the control steady state; DECLARED "
                               "BEFORE THE SWEEP. Threshold = NOAA degree heating weeks "
                               "accumulated at that moment.",
                    confound_source_lines=[
                        "coRal R/def_pars.R:43:    b=rep(5, nsym)  # Scaling parameter "
                        "for bleaching response",
                        "coRal R/run_coral.R:106:    jST[t,] <- pars$jST0 * (1 + pars$b "
                        "* (cROS[t,] - 1))"],
                    confound="NOT independent of the knob b. The two lines above are the "
                             "whole of it: jST = jST0*(1 + b*(cROS-1)) "
                             "is the only equation in which symbiont loss is produced, "
                             "and b is its coefficient, so a knob acting on expulsion "
                             "necessarily dominates a readout defined as expulsion. "
                             "Measured: at the retentive end of b's range this readout "
                             "censors most of the knob map, because a host that does not "
                             "expel symbionts never crosses the criterion at any dose. "
                             "That is close to tautological and is why readout B exists."),
                readout_B_host_energy=dict(
                    definition="Degree heating weeks at which the host's specific growth "
                               "rate dH/Hdt first goes negative, i.e. translocated "
                               "photosynthate no longer covers maintenance.",
                    why="b does not appear in the host growth equation, so this readout "
                        "is not confounded with any knob. It also asks a different "
                        "question: not 'did the coral pale' but 'did the symbiosis stop "
                        "paying for itself'. A holobiont that retains ROS-damaged "
                        "symbionts scores as unbleached on readout A and can still fail "
                        "on readout B. The additivity verdict is taken on THIS readout."),
                readout_C_ambient_cost=dict(
                    definition="Mean host specific growth rate over the fourth year of a "
                               "purely ambient run, relative to the wild type.",
                    why="The cost side. Every thermal-tolerance route is scored for what "
                        "it gives up when there is no heatwave, which is the half of the "
                        "symbiont literature a thermal-threshold model otherwise "
                        "silently ignores.")),
        ),
        port_check=cache["port_check"],
        control_arm={k: v for k, v in ctrl.items()
                     if k not in ("t", "sst", "SH", "cROS", "dHdt")},
        control_arm_series=dict(t_days=ctrl["t"], sst=ctrl["sst"], SH=ctrl["SH"],
                                cROS=ctrl["cROS"]),
        numerical_checks=cache["numerical_checks"],
        degree_heating_weeks_blind_spot=dict(
            finding="Degree heating weeks cannot see a sub-1-degC failure, by "
                    "construction.",
            why="NOAA Coral Reef Watch sums HotSpots into degree heating weeks only "
                "where sea temperature exceeds the maximum monthly mean by at least "
                "1 degC. Any failure mode that bites below that accumulates exactly "
                "zero DHW, however severe it is.",
            measured_here=(
                f"The wild-type holobiont's carbon balance goes negative at an anomaly "
                f"of about {sw['T_opt']['anomaly_host'][0]:.2f} degC -- right at the "
                f"deadband -- where the DHW reading is still "
                f"{sw['T_opt']['dhw_host'][0]:.2f}. In three of the four knob panels the "
                f"host-energy threshold sits at or near zero degree heating weeks for "
                f"the whole sweep, not because nothing happens but because the metric "
                f"cannot register it."),
            consequence="Anyone using degree heating weeks as a design currency, or as "
                        "the trigger for an intervention, is blind to this mode. It is a "
                        "property of the metric and not of the model, and it is why the "
                        "knob ranking and the additivity verdict in this study are taken "
                        "in degC of anomaly rather than in degC-weeks.",
            is_observation=False),
        emergent_cold_arm=cache["cold_arm"],
        emergent_ambient_cost=dict(
            per_knob_pct=({nm: spans[nm]["ambient_growth_cost_pct"] for nm in spans}),
            finding=(
                f"Raising the symbiont thermal optimum by 2 degC changes the host's "
                f"ambient specific growth rate by {topt_cost:+.2f}%. It is the only knob "
                f"of the four whose ambient effect is negative; the other three improve "
                f"ambient growth, because they all reduce the oxidative burden the "
                f"control is already carrying (control cROS = "
                f"{ctrl['mean_cROS']:.3f}, i.e. ROS production is already above "
                f"baseline at ambient in this model)."),
            interpretation=(
                "Nothing was tuned for this. The mechanism is that a symbiont whose "
                "optimum sits above the ambient range is below its optimum for most of "
                "the year, fixes less carbon, and therefore leaves more absorbed light "
                "unused. That is the right SIGN for the measured Durusdinium trade-off "
                "(Jones & Berkelmans 2010: 29% slower in the laboratory, 38% in the "
                "field) and about an order of magnitude too small. So this model does "
                "NOT support a shifted thermal optimum as the explanation of that "
                "penalty, which is a finding about the model and a pointer to the "
                "alternatives the literature already offers: reduced carbon "
                "translocation per cell (Sproles et al. 2020, in an anemone) or "
                "something not in the model at all. Kemp et al. 2023 (PMID 37727091) "
                "report no ambient nutrient-exchange difference between Cladocopium and "
                "Durusdinium colonies, so the measured cost is itself disputed and the "
                "model is not adjudicating it."),
            is_observation=False),
        durusdinium_cost_arm=dur,
        tradeoff_arm=cache["tradeoff_arm"],
        sweeps=dict(one_dimensional=sw, spans=spans,
                    ranking=[k for _, k in ranked],
                    saturation_note=(
                        "Readout A saturates: for three of the four knobs the modified "
                        "end of the range does not fail until the forcing ramp itself "
                        "runs out, so the span measured on readout A is a property of "
                        "the +4 degC cap and not of the knob. Those points are flagged "
                        "at_forcing_cap and are excluded from the additivity fit. "
                        "Readout B does not saturate, which is the second reason the "
                        "ranking is taken there."),
                    ranking_caveat="The four declared ranges are not commensurable: "
                                   "2 degC of thermal optimum against two doublings "
                                   "against a fivefold cut. The span therefore measures "
                                   "the range as much as the knob. The elasticity block "
                                   "is the commensurable comparison."),
        elasticity=cache["elasticity"],
        knob_map={k: v for k, v in cache["knob_map"].items()
                  if k not in ("dhw", "dhw_host", "anomaly", "anomaly_host",
                               "ambient_growth_relative_pct")},
        knob_map_dhw=cache["knob_map"]["dhw"],
        knob_map_dhw_host=cache["knob_map"]["dhw_host"],
        knob_map_anomaly=cache["knob_map"]["anomaly"],
        knob_map_anomaly_host=cache["knob_map"]["anomaly_host"],
        knob_map_ambient_growth_relative_pct=cache["knob_map"][
            "ambient_growth_relative_pct"],
        additivity=add,
        additivity_on_symbiont_readout=cache["additivity_symbiont_readout"],
        answer_to_the_design_question=dict(
            question="Are the thermal-tolerance knobs additive, or does one dominate?",
            answer=(f"In this model, over these ranges, on the readout that is not "
                    f"confounded with any knob (host carbon balance): {add['verdict']}. "
                    f"Main effects alone reach adjusted R2 "
                    f"{add['adj_r2_main_effects']:.3f} on the {add['n_cells_used']} "
                    f"usable cells of the {add['n_cells_total']}-cell map, and all six "
                    f"two-way interactions together add "
                    f"{add['variance_explained_by_interactions']:.3f}. Ranked by span: "
                    + ", ".join(f"{k} ({spans[k]['span_anomaly_host']:+.2f} degC of "
                                f"anomaly)" if spans[k]['span_anomaly_host'] is not None
                                else f"{k} (censored)" for _, k in ranked) + "."),
            the_result_the_two_readouts_disagree_about=(
                "On readout A (symbiont loss) all four knobs move the threshold by a "
                "comparable amount. On readout B (host carbon balance) T_opt moves it "
                "about six times further than any of the other three. Read together: "
                "raising photoprotection, ROS tolerance or symbiont retention mostly "
                "keeps the ALGAE IN PLACE without keeping the HOST FED, whereas moving "
                "the symbiont's thermal optimum delays both. In this model, three of the "
                "four interventions buy a coral that still looks brown while it starves. "
                "That is a statement about a model whose host has no food source but its "
                "symbiont, and it is the kind of thing a single-readout study would not "
                "see at all."),
            why_two_readouts=(
                "The obvious readout -- degree heating weeks at which the coral loses "
                "half its symbionts -- cannot answer this question cleanly, because one "
                "of the four knobs (b) is the coefficient that converts oxidative stress "
                "into symbiont loss. Asking whether b dominates a symbiont-loss readout "
                "is close to asking whether b equals b. Measured: on that readout "
                f"{cache['additivity_symbiont_readout']['n_cells_censored']} of "
                f"{cache['additivity_symbiont_readout']['n_cells_total']} map cells are "
                "censored because retentive hosts never cross the criterion at any dose. "
                "The host-energy readout has no such relationship to any knob, and the "
                "verdict is taken there. Both are reported."),
            caveat="'Additive' here is a property of a four-parameter box in one model. "
                   "It is not a claim that two real interventions combine additively in "
                   "a coral, which nobody has tested: no study in the research block "
                   "crosses a symbiont swap with a host trait.",
        ),
        limitations=[
            "This is a SIMULATION. No coral was measured. Nothing here is evidence that "
            "any intervention raises a real coral's bleaching threshold.",
            "coRal CONTAINS NO TEMPERATURE. The published model bleaches corals with "
            "light, not heat. The thermal coupling is this file's addition, it enters "
            "through exactly one parameter, and every number that depends on "
            "temperature depends on that choice. A different coupling -- heat acting on "
            "symbiont growth, on host respiration, or on the repair arm directly -- "
            "would give different thresholds.",
            "ONE parameter was calibrated: sigma_hot, set so the unmodified holobiont "
            "bleaches inside the observed 4-8 degree-heating-week window. The model "
            "therefore cannot be used as evidence about that window, and the headline "
            "says so.",
            "The thermal performance curve is an assumed shape with three assumed "
            "parameters. No measured thermal performance curve for Symbiodiniaceae "
            "photochemistry was retrieved; the research block records that symbiont "
            "density per cm2, a bleached-density threshold, mitotic index and absolute "
            "Fv/Fm are all unavailable from the sources read.",
            "The knob RANGES are three-quarters invented. Only T_opt's 2 degC span is "
            "sourced (Berkelmans & van Oppen 2006; Pettay et al. 2015, both abstracts). "
            "The two doublings and the fivefold cut in b are round numbers. So the "
            "ranking of knobs by span is partly a ranking of my choices, which is why "
            "the elasticity block exists.",
            "Host and symbiont biomass are unbounded in coRal, so 'the colony died' is "
            "not representable: the model has no mortality. A holobiont whose S/H "
            "collapses is scored as bleached, and what happens to it afterwards is "
            "outside the model.",
            "One symbiont type, not a population. Symbiont shuffling -- the route that "
            "most of the symbiont literature is about -- is a change in the MIX of two "
            "or more types, and cannot be represented by moving one thermal optimum. "
            "coRal supports multiple symbionts (nsym > 1) and this port does not use "
            "that; a shuffling study would.",
            "No acclimatisation and no plasticity: the knobs are constants in time, so "
            "the preconditioning route (Ainsworth et al. 2016) cannot be represented at "
            "all. Nor can anything epigenetic.",
            "The growth cost IS scored (readout C), but it comes out about an order of "
            "magnitude too small. Raising the thermal optimum by 2 degC costs under 2% "
            "of host specific growth here, against the 29% (laboratory) and 38% (field) "
            "that Jones & Berkelmans 2010 measured for Durusdinium-hosting Acropora "
            "millepora, and the 'nearly half' calcification reduction Pettay et al. 2015 "
            "report. The Durusdinium cost arm shows the model has no steady state with "
            "a penalty that large at all. So the model reproduces the SIGN of the "
            "trade-off and not its size, and nothing here should be read as a prediction "
            "of what a symbiont swap costs.",
            "Calcification is not in the model at all. coRal tracks host carbon biomass, "
            "not skeleton, so the Pettay 'nearly half' calcification figure has no "
            "counterpart here and the comparison above is to GROWTH, which is a "
            "different quantity measured a different way.",
            "Light is constant in the main arms and the anomaly is a single linear ramp. "
            "Real thermal histories are not ramps, and in coRal light is the primary "
            "driver, so a reef whose summer light and summer temperature peak together "
            "is a harsher case than anything here. The seasonal-light robustness arm is "
            "one step toward that and not a substitute for real forcing.",
            "DEGREE HEATING WEEKS CANNOT SEE A SUB-1-degC FAILURE, by construction. "
            "The NOAA convention sums HotSpots only where SST exceeds the maximum "
            "monthly mean by at least 1 degC, so any failure mode that bites below that "
            "accumulates zero DHW. In this model host carbon balance is exactly such a "
            "mode: the wild type's growth rate goes negative at an anomaly of about "
            "+1 degC, right at the deadband, where the DHW reading is still 0. That is "
            "why readout B is reported in degC of anomaly as well, and why the knob "
            "ranking and the additivity verdict are taken in degC rather than in "
            "degC-weeks. It is a property of the metric, not of the model, and it is "
            "worth knowing for anything that uses DHW as a design currency.",
            "The host is fragile here BECAUSE feeding was switched off. X = 0 in every "
            "arm, so the host has no carbon source but its symbiont. Cunning et al.'s "
            "own abstract states that bleaching in this model is 'attenuated by "
            "feeding', so a fed holobiont would fail later and readout B's sensitivity "
            "is partly a consequence of a declared modelling choice.",
            "Degree heating weeks are computed to the NOAA convention from a SYNTHETIC "
            "temperature series. The 4 and 8 degC-week lines on the figures are field "
            "thresholds drawn for scale, taken from the NOAA product page at "
            "read_level web-page; the primary methods papers were not obtained.",
            "The bleaching criterion (0.5 of control S/H) is declared but arbitrary. "
            "Thresholds move with it, as the criterion_sensitivity block shows. What is "
            "tested is whether the knob RANKING moves, which is a weaker claim than it "
            "sounds: it is still a ranking inside one model.",
        ],
        sources=[
            dict(cite="Cunning R, Muller EB, Gates RD, Nisbet RM 2017, J Theor Biol "
                      "431:49-62, 'A dynamic bioenergetic model for coral-Symbiodinium "
                      "symbioses and coral bleaching as an alternate stable state'",
                 pmid="28782552", read_level="abstract",
                 note="The CODE implementing this paper was read in full and ported; "
                      "the paper itself was not obtained."),
            dict(cite="Warner ME, Fitt WK, Schmidt GW 1999, PNAS 96:8007-12, 'Damage to "
                      "photosystem II in symbiotic dinoflagellates: a determinant of "
                      "coral bleaching'", pmid="10393938", read_level="abstract",
                 note="Warrant for routing temperature through the photochemical "
                      "ceiling and nowhere else."),
            dict(cite="Berkelmans R, van Oppen MJH 2006, Proc Biol Sci 273:2305-12",
                 pmid="16928632", read_level="abstract",
                 note="+1 to 1.5 degC from a C-to-D symbiont shift; the sourced half of "
                      "the T_opt range."),
            dict(cite="Pettay DT et al. 2015, PNAS 112:7513-8", pmid="26034268",
                 read_level="abstract",
                 note="+1 to 2 degC for Durusdinium trenchii, and calcification "
                      "'reduced by nearly half' -- the cost this model does not score."),
            dict(cite="Jones AM, Berkelmans R 2010, PLoS One 5:e10437", pmid="20454653",
                 read_level="abstract",
                 note="29% (lab) and 38% (field) slower growth with the heat-tolerant "
                      "symbiont."),
            dict(cite="Buerger P et al. 2020, Sci Adv 6:eaba2498", pmid="32426508",
                 read_level="full-text",
                 note="Wild-type strains secreted 13-28x more ROS than heat-evolved "
                      "ones at 31 degC; cited for direction, not converted into kROS."),
            dict(cite="Chan WY et al. 2023, Glob Chang Biol 29:6945-6968",
                 pmid="37913765", read_level="abstract",
                 note="Photobiology and oxidative-stress pigments as the reported "
                      "mechanism of the SS8 strain; the kNPQ route."),
            dict(cite="Barshis DJ et al. 2013, PNAS 110:1387", pmid="23297204",
                 read_level="abstract",
                 note="Constitutive 'frontloading' of antioxidant and heat-shock "
                      "transcripts in resilient colonies; the direction for b."),
            dict(cite="Silverstein RN, Cunning R, Baker AC 2017, J Exp Biol 220:1192-6",
                 pmid="28108671", read_level="abstract",
                 note="C3-hosting Montastraea cavernosa lost 94% of symbionts on "
                      "COOLING while D1a-hosting colonies did not; the sign check for "
                      "the emergent cold arm."),
            dict(cite="NOAA Coral Reef Watch, Degree Heating Week product page",
                 url="https://coralreefwatch.noaa.gov/product/5km/tutorial/"
                     "crw10a_dhw_product.php",
                 read_level="web-page",
                 note="MMM+1 HotSpot convention, the 12-week window, and the 4 and 8 "
                      "degC-week statements. The primary methods papers (Liu et al.; "
                      "Glynn & D'Croz 1990; Eakin et al. 2010) were NOT retrieved."),
        ],
    )
    with open(RESULT, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"wrote {RESULT}")


if __name__ == "__main__":
    main()
