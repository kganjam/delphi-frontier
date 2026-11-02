#!/usr/bin/env python3
"""convergence: does the voxel-actuation model converge under grid refinement,
and is the flagged non-monotone body-size series a resonance or an artifact?

PREDECLARED (written before the refinement runs were launched; the parity sweep
and the frequency map had already been run and are reported as such):
 Q1 On a PARITY-MATCHED refinement series, does net displacement converge, and
    at what observed order?
 Q2 Is the audit's non-monotone nx series a gait-length resonance or the
    encoding? Declared discriminators, both of which a resonance must pass:
      D1 it must appear in 'travelling' too, whose phase field does not depend
         on grid parity;
      D2 its optimum frequency must move with body length, as f_opt ~ 1/L.
 Q3 Is the ranking of gaits stable under refinement? If it is not, that
    retroactively qualifies the published artifact and must be said.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = "/data/scratch/designspaces/xenobot"
VOX = 0.01


def merged_freq(SW, FO, pat, nx):
    row = {float(k): v for k, v in FO["data"][pat].get(str(nx), {}).items()}
    for f, v in SW["freq_nx_map"][pat].get(str(nx), {}).items():
        row[float(f)] = v["body_lengths"]
    fs = sorted(row)
    return fs, [row[f] for f in fs]


def observed_order(hs, fs):
    """Fit f(h) = f0 + C h^p by least squares over the series (3 parameters).
    Returns f0, C, p and the residual. With only 3 or 4 points this is a
    DESCRIPTION of the series, not a convergence proof."""
    from scipy.optimize import least_squares
    hs, fs = np.asarray(hs, float), np.asarray(fs, float)

    def res(q):
        return q[0] + q[1] * hs ** q[2] - fs

    best = None
    for p0 in (0.5, 1.0, 2.0):
        for f0 in (fs[-1], fs.mean(), 0.0):
            try:
                r = least_squares(res, [f0, (fs[0] - fs[-1]) / hs[0] ** p0, p0],
                                  bounds=([-np.inf, -np.inf, 0.05], [np.inf, np.inf, 6.0]))
            except Exception:
                continue
            if best is None or r.cost < best.cost:
                best = r
    return {"f0_extrapolated": float(best.x[0]), "C": float(best.x[1]),
            "observed_order_p": float(best.x[2]),
            "residual_rms": float(np.sqrt(np.mean(best.fun ** 2))),
            "n_points": len(hs)}


def main():
    SW = json.load(open(f"{ROOT}/data/sweeps.json"))
    FO = json.load(open(f"{ROOT}/data/freqopt.json"))
    RF = json.load(open(f"{ROOT}/data/refine_local.json"))
    R = {"schema": "design-space-study/0.1", "id": "convergence"}
    R["predeclared_questions"] = [
        "Q1 does a parity-matched refinement series converge, and at what observed order",
        "Q2 resonance or encoding; discriminators D1 (must appear in travelling) and D2 (optimum must scale as 1/L)",
        "Q3 is the gait ranking stable under refinement"]

    # ------------------------------------------------------------ Q1 -------
    series = {}
    for name, tags, pat, env in (("A_travelling", ["A1", "A2", "A3", "A4"], "travelling", 0.05),
                                 ("B_longitudinal", ["B1", "B2", "B3", "B4"], "longitudinal", 0.04)):
        rows = [RF[t] for t in tags if t in RF]
        if len(rows) < 3:
            continue
        hs = [r["voxel_m"] for r in rows]
        # the invariant length is the OUTER ENVELOPE, which is identical on every
        # grid here; the centre-to-centre span is NOT and must not be the denominator
        vals = [r["net_disp_m"] / env for r in rows]
        diffs = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
        series[name] = {
            "pattern": pat, "invariant_outer_envelope_m": env,
            "levels": [{"tag": r["tag"], "nx": r["nx"], "ny": r["ny"], "nz": r["nz"],
                        "voxel_m": r["voxel_m"], "voxels": r["voxels"],
                        "net_disp_m": r["net_disp_m"],
                        "normalised_by_outer_envelope": r["net_disp_m"] / env,
                        "dt_s": r["dt_s"], "steps": r["steps"],
                        "diverged": r["diverged"], "wall_s": r["wall_s"]} for r in rows],
            "successive_differences": diffs,
            "successive_difference_ratios": [abs(diffs[i + 1] / diffs[i]) if diffs[i] else None
                                             for i in range(len(diffs) - 1)],
            "monotone": bool(all(d > 0 for d in diffs) or all(d < 0 for d in diffs)),
            "total_spread_rel_to_coarsest": float((max(vals) - min(vals)) / vals[0]),
            "richardson_fit": observed_order(hs, vals)}
    R["refinement_series"] = {
        "design": "the outer envelope and the PHYSICAL actuation field are held fixed while the lattice is refined. Series A uses travelling, whose phase 2*pi*x/nx is a function of fractional position and so is identical on every grid. Series B uses longitudinal with EVEN nx only, so the split at index nx/2 falls at the same physical plane (x = 20 mm) on every grid: 2x10 = 4x5 = 6x3.333 = 8x2.5 mm. The published artifact refined nx 5 -> 10, which moved that plane from 20 to 25 mm and flipped its parity at the same time.",
        "denominator_note": "normalised by the OUTER ENVELOPE nx*voxel, which is invariant across the series. The artifact's stored metric divides by the centre-to-centre span (nx-1)*voxel, which is NOT invariant, and its own audit records that comparing two runs under two different denominators manufactured an agreement that was not in the data.",
        "series": series}

    # ------------------------------------------------------------ Q2 -------
    nxs = list(range(3, 17))
    lo = {n: SW["parity_sweep"]["longitudinal"][str(n)]["body_lengths"] for n in nxs}
    tr = {n: SW["parity_sweep"]["travelling"][str(n)]["body_lengths"] for n in nxs}
    odd = [n for n in nxs if n % 2]
    evn = [n for n in nxs if not n % 2]
    mono = lambda ns, d: all(d[ns[i + 1]] < d[ns[i]] for i in range(len(ns) - 1))

    def alternation(d):
        """mean ratio of each odd nx to the geometric mean of its even neighbours"""
        out = []
        for n in nxs:
            if n % 2 == 0 or n - 1 < nxs[0] or n + 1 > nxs[-1]:
                continue
            out.append(d[n] / np.sqrt(d[n - 1] * d[n + 1]))
        return float(np.median(out)), [float(x) for x in out]

    med_lo, all_lo = alternation(lo)
    med_tr, all_tr = alternation(tr)
    fopt = {}
    for pat in ("longitudinal", "travelling"):
        fopt[pat] = {}
        for nx in (4, 5, 6, 7, 8):
            fs, vs = merged_freq(SW, FO, pat, nx)
            bi = int(np.argmax(vs))
            fopt[pat][str(nx)] = {"L_m": (nx - 1) * VOX, "f_opt_Hz": fs[bi],
                                  "max_body_lengths": vs[bi],
                                  "f_opt_times_L": fs[bi] * (nx - 1) * VOX,
                                  "at_swept_boundary": bi in (0, len(fs) - 1),
                                  "n_frequencies": len(fs),
                                  "freq_range_Hz": [fs[0], fs[-1]],
                                  "total_variation_rel": float((max(vs) - min(vs)) / max(vs))}
    R["parity_vs_resonance"] = {
        "parity_sweep": {"nx": nxs, "longitudinal": lo, "travelling": tr,
                         "fixed": "voxel 10 mm, freq 4 Hz, 5 cycles, same material"},
        "D1_alternation_must_appear_in_travelling_too": {
            "longitudinal_median_odd_over_even_neighbours": med_lo,
            "longitudinal_all": all_lo,
            "travelling_median_odd_over_even_neighbours": med_tr,
            "travelling_all": all_tr,
            "verdict": "FAILS for a resonance: longitudinal alternates by a median factor of "
                       f"{med_lo:.1f}, travelling by {med_tr:.3f}, i.e. not at all."},
        "each_parity_branch_is_monotone": {
            "odd_nx_longitudinal_monotone_decreasing": mono(odd, lo),
            "even_nx_longitudinal_monotone_decreasing": mono(evn, lo),
            "travelling_single_branch_monotone": mono(nxs, tr),
            "reading": "the series the audit called non-monotone is TWO smooth monotone branches interleaved; the four points it flagged (nx 4,5,6,7) are two adjacent points of each branch"},
        "D2_optimum_frequency_must_scale_as_1_over_L": {
            "per_gait": fopt,
            "longitudinal_f_opt_nx4_Hz": fopt["longitudinal"]["4"]["f_opt_Hz"],
            "longitudinal_f_opt_nx8_Hz": fopt["longitudinal"]["8"]["f_opt_Hz"],
            "body_length_ratio_nx8_over_nx4": (8 - 1) / (4 - 1),
            "verdict": "FAILS for a resonance: body length rises by 2.33x from nx=4 to nx=8 and longitudinal's optimum frequency is "
                       f"{fopt['longitudinal']['4']['f_opt_Hz']} Hz at both ends. A length resonance requires f_opt to fall by the same factor.",
            "travelling_caveat": "travelling's optimum runs to the lowest swept frequency for nx>=5, so it is a BOUNDARY not an optimum; its total variation over 0.25-16 Hz is at most "
                                 f"{max(v['total_variation_rel'] for v in fopt['travelling'].values()):.2f}, a broad shallow response rather than a peak."},
        "mechanism_named_at_the_source": {
            "the_line": "(x < c.nx/2) ? 0.0 : kPi",
            "file": "scripts/voxel_actuation/soft_actuation.cpp, phaseFor(), the 'longitudinal' branch (and the identical 'lateral' and 'dorsoventral' branches with y and z)",
            "the_operator": "c.nx/2 is C++ INTEGER division. For even nx it splits the body exactly in half; for odd nx it cannot, and leaves one extra plane of voxels on one side.",
            "split_by_nx": {"4": "2 vs 2, balanced", "5": "2 vs 3, unbalanced",
                            "6": "3 vs 3, balanced", "7": "3 vs 4, unbalanced"},
            "why_it_produces_two_branches": "an unbalanced split leaves a net actuation dipole along the travel axis; a balanced one cancels it to leading order. Net translation needs that broken mirror symmetry, so the odd-nx bodies move roughly an order of magnitude further than their even-nx neighbours at identical resolution, material, amplitude and duration.",
            "why_travelling_is_immune": "its phase is 2*pi*x/nx, a continuous function of fractional position along the body. It never divides by 2 and has no parity to be odd or even, which is why the alternation is absent from it by a median factor of 1.008.",
            "why_no_frequency_removes_it": "the asymmetry is in the spatial actuator LAYOUT, not in the timing, so changing the drive frequency cannot cancel it - and does not, from 0.25 to 16 Hz.",
            "credit": "the integer-division operator was identified by the team lead reading the driver source; this study had established the two-branch structure and its three discriminators without naming the line."},
        "verdict": "ENCODING, not resonance and not a solver artifact. The alternation appears only in the pattern whose phase assignment depends on grid parity; it is absent from the pattern whose phase is a continuous function of position; each parity branch is smooth and monotone over 14 values; and it persists unchanged at every drive frequency from 0.25 to 16 Hz. It is a real mechanical consequence of a real difference in actuator layout, and that difference is an artifact of writing the split as an index comparison."}

    # ------------------------------------------------------------ Q3 -------
    ratios = None
    if "A_travelling" in series and "B_longitudinal" in series:
        a = [l["normalised_by_outer_envelope"] for l in series["A_travelling"]["levels"]]
        bb = [l["normalised_by_outer_envelope"] for l in series["B_longitudinal"]["levels"]]
        n = min(len(a), len(bb))
        ratios = [a[i] / bb[i] for i in range(n)]
    R["headline"] = (
        "On a parity-matched refinement series the model does NOT converge. Across a 4x "
        "refinement (45 to 2880 voxels) the travelling wave spans 41% of its coarsest value "
        "and the longitudinal split 54%, and BOTH series turn over rather than settling. "
        "Separately, the non-monotone body-size series the independent audit flagged is the "
        "actuation encoding, not a gait-length resonance: it is two smooth monotone branches "
        "interleaved by the parity of the actuator split, it is absent from the pattern whose "
        "phase does not depend on parity, and it does not move with drive frequency.")
    R["Q1_verdict"] = {
        "converged": False,
        "statement": "neither series converges. Both are non-monotone across four levels and the successive differences do not fall the way a converging series' do: series A gives ratios 1.44 then 0.83, series B 0.91 then 0.59. A power-law fit f(h) = f0 + C h^p returns p = 0.05 for series A with a residual of 3.4e-2 against values near 0.3, which is not a convergence order but a statement that the series is not a power law.",
        "what_the_audit_said": "the independent audit recorded G_actual_SI_coarse_to_fine_ratio = 7.25 and the status line 'spatial G unresolved'. This study resolves it, as a NEGATIVE: most of that 7.25 was the parity confound, and what remains still does not converge.",
        "consequence_for_the_published_artifact": "any net displacement quoted from the coarse 5x3x3 grid is provisional at best. The artifact itself predicted no convergence for its arm G and said so in advance, so this is a confirmation of its own stated expectation rather than a contradiction of a claim it made."}
    R["ranking_stability"] = {
        "travelling_over_longitudinal_by_level": ratios,
        "reading": "the ORDER is stable - travelling is ahead of longitudinal at every one of the four levels - but the SIZE of the gap is not: it falls from 19.4x to 10.4x across the refinement and is STILL MOVING at the finest grid, with the last step (11.7 to 10.4) no smaller than the one before it relative to the remaining gap. The margin has therefore NOT converged either.",
        "what_is_and_is_not_quotable": "'travelling beats longitudinal' is supported at every level tested. 'travelling beats longitudinal by N times' is NOT quotable at any N, because the margin has not converged and the sequence gives no reason to believe 10.4 is closer to the limit than 19.4 was.",
        "what_can_be_said": "this study refines TWO patterns, not all six, so it cannot report a full ranking at the fine grid. What it establishes is the prior question: whether a single pattern's value is stable enough for any ranking drawn from the coarse grid to mean anything.",
        "per_series": {k: {"total_spread_rel_to_coarsest": v["total_spread_rel_to_coarsest"],
                           "monotone": v["monotone"],
                           "observed_order_p": v["richardson_fit"]["observed_order_p"],
                           "successive_difference_ratios": v["successive_difference_ratios"]}
                       for k, v in series.items()},
        "coarse_grid_gap_between_the_two_patterns": float(
            series["A_travelling"]["levels"][0]["normalised_by_outer_envelope"] /
            series["B_longitudinal"]["levels"][0]["normalised_by_outer_envelope"])
        if "A_travelling" in series and "B_longitudinal" in series else None}

    # ------------------------------------ timestep separation (levels 1-3) --
    DT = f"{ROOT}/data/refine_dt.json"
    if os.path.exists(DT):
        a, bdt = RF, json.load(open(DT))
        ENVM = {"travelling": 0.05, "longitudinal": 0.04}
        nrm = lambda d, t: d[t]["net_disp_m"] / ENVM[d[t]["pattern"]]
        rows = {t: {"voxels": a[t]["voxels"], "pattern": a[t]["pattern"],
                    "dtScale_0.5": nrm(a, t), "dtScale_0.25": nrm(bdt, t),
                    "rel_change_pct": 100 * (nrm(bdt, t) - nrm(a, t)) / nrm(a, t)}
                for t in ("A1", "A2", "A3", "B1", "B2", "B3") if t in bdt}
        per = {}
        for tags, env in ((["A1", "A2", "A3"], "travelling"), (["B1", "B2", "B3"], "longitudinal")):
            if not all(t in bdt for t in tags):
                continue
            v5 = [nrm(a, t) for t in tags]; v25 = [nrm(bdt, t) for t in tags]
            tmax = max(abs(y - x) / x for x, y in zip(v5, v25))
            per[env] = {"spatial_spread_pct_at_dt0.5": 100 * (max(v5) - min(v5)) / v5[0],
                        "spatial_spread_pct_at_dt0.25": 100 * (max(v25) - min(v25)) / v25[0],
                        "max_temporal_change_pct_at_fixed_grid": 100 * tmax,
                        "spatial_over_temporal": ((max(v5) - min(v5)) / v5[0]) / tmax}
        R["timestep_separation_arm"] = {
            "why": "a refinement at fixed dtScale halves dt automatically with the lattice, so spatial and temporal error are confounded. This arm repeats levels 1-3 of both series at HALF the timestep and asks whether the spatial spread survives.",
            "per_level": rows, "per_series": per,
            "verdict": ("For the travelling wave the non-convergence is unambiguously SPATIAL: halving dt changes any level by at most 1.3% while the spread across levels 1-3 is 22% (41% over all four), and that spread is essentially unchanged at the finer dt, 22.4% against 21.8%. "
                        "For the longitudinal split the temporal error is NOT negligible - up to 15.5% at level 2 - but it does not explain the spread either: halving dt moves it only from 54.4% to 48.5%. "
                        "Spatial error dominates by about 17x for travelling and about 3.5x for longitudinal."),
            "relation_to_the_artifacts_own_arm_F": "the pinned artifact's timestep arm found 0.90% spread across a 4x dt range, which does not conflict with the 5.3% we see at B1. Arm F ran longitudinal at nx=5, the ASYMMETRIC split, whose net displacement is large (0.153 body lengths). B1 is nx=4, the SYMMETRIC split, an order of magnitude smaller at 0.015 normalised, so the same absolute numerical error is a much larger relative one. The two measure the same thing on configurations separated by the parity effect this study is about.",
            "caveat": "level 4 was not repeated at the finer timestep."}

    # ------------------------------------------------- conditioning arm ----
    ca, cb = "0.0033333333", "0.0033333333333333335"
    cond = {}
    for pat, tag, env in (("longitudinal", "COND", 0.04), ("travelling", "CONDT", 0.05)):
        fa, fb = f"{ROOT}/data/{tag}-{ca}.json", f"{ROOT}/data/{tag}-{cb}.json"
        if not (os.path.exists(fa) and os.path.exists(fb)):
            continue
        x = json.load(open(fa))["result"]["net_disp_m"]
        y = json.load(open(fb))["result"]["net_disp_m"]
        dv = abs(float(cb) - float(ca)) / float(cb)
        cond[pat] = {"voxel_a": ca, "voxel_b": cb, "net_disp_a_m": x, "net_disp_b_m": y,
                     "input_rel_perturbation": dv, "output_rel_change": abs(y - x) / x,
                     "amplification": (abs(y - x) / x) / dv,
                     "normalised_a": x / env, "normalised_b": y / env}
    if cond:
        R["conditioning_arm"] = {
            "status": "POST-HOC. Found by cross-checking the local refinement against an independent run of the same series on a Nebius L40S node, where two of fourteen runs disagreed.",
            "what_happened": "12 of the 14 runs were bit-identical between an AWS host and a Nebius node, confirming the engine is deterministic across machines as the protocol claims. The two that disagreed were exactly the level-3 grids, where voxel = 1/300 m: the local runs passed the full double-precision value and the remote job passed a 10-digit literal. Re-running locally with the 10-digit value reproduces the remote result EXACTLY, so the engine is not at fault and the difference is entirely the input spelling.",
            "measurement": cond,
            "reading": ("A relative perturbation of 1.0e-8 in the voxel size changes net displacement by 1.2e-2 for the "
                        "SYMMETRIC longitudinal split - an amplification of about 1.2e6 - and by 1.1e-4 for the travelling "
                        "wave, an amplification of about 1.1e4. The quantity being refined is therefore not a well-conditioned "
                        "function of the inputs at these configurations, and the symmetric split is roughly 100x worse than the "
                        "travelling wave. That is a direct explanation for why the refinement series do not converge, and it "
                        "predicts that no amount of further refinement would make them: the spread is not dominated by "
                        "discretisation error that shrinks with h."),
            "caveat": "this is ONE perturbation of ONE parameter at ONE grid level per pattern. It establishes that the configuration is ill-conditioned; it does not measure a condition number, and the amplification figures should not be quoted as one.",
            "consequence_for_the_series": "the series reported here all use the full double-precision 1/300 locally, so they are internally consistent. A reader reproducing them must pass the same value; a 10-digit literal changes level 3 by 1.2% for longitudinal."}

    R["what_this_cannot_establish"] = [
        "that the model converges. It refines two of six patterns on three or four levels each; a converged value is not demonstrated and is not claimed.",
        "a corrected ranking of the six gaits. Only travelling and longitudinal were refined.",
        "anything about a biological construct. This is the same generic soft-voxel model throughout, with the same assumed parameters, and the regime-check study shows it is not the regime a real construct occupies.",
        "that the parity effect is the ONLY cause of the artifact's 8.2x arm-G gap. Varying nx at fixed voxel size changes count, length and mass together, as the independent audit already noted; this study adds that the effect is absent from a parity-free pattern and frequency-independent, which rules out a resonance but does not isolate a single cause."]
    return R


if __name__ == "__main__":
    r = main()
    json.dump(r, open(f"{ROOT}/convergence.raw.json", "w"), indent=2)
    print(json.dumps(r["refinement_series"]["series"], indent=1)[:2200])
    print("D1:", r["parity_vs_resonance"]["D1_alternation_must_appear_in_travelling_too"]["verdict"])
    print("D2:", r["parity_vs_resonance"]["D2_optimum_frequency_must_scale_as_1_over_L"]["verdict"])
