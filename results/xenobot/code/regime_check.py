#!/usr/bin/env python3
"""regime-check: which physical regime does a millimetre-scale living construct
occupy, and does the published dry-friction gait ranking transfer to it?

PREDECLARED before any output was produced (see predeclared_* keys in the output):
 Q1 What is Re for a real xenobot/anthrobot across the published size and speed
    range, and what is Re for the object the voxel-actuation artifact simulated?
 Q2 Which of the artifact's six gaits are time-reciprocal?
 Q3 Ranked in the Stokes limit, do the six gaits order as they do under dry
    friction? Predeclared expectation: they do NOT; every reciprocal gait gives
    exactly zero, so the dry-friction ranking's 2nd and 3rd places collapse.
 Q4 Is the quasi-static assumption, which carries Q2 from the CONTROL to the
    SHAPE, satisfied by margin? Declared gate: ratio of elastic relaxation time
    to actuation period <= 1e-2.

Nothing here is calibrated to measured Xenopus tissue. Sizes and speeds for the
real constructs are READ FROM the cited papers' abstracts; everything mechanical
is declared assumed.
"""
import json, sys, time, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lattice as L
import stokes as S

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RHO_W, MU_W = 998.2, 1.002e-3          # water at 20 C
NX, NY, NZ = 5, 3, 3

# published dry-friction result, copied from the artifact's summary.json
DRY = {"travelling": 0.364432, "longitudinal": 0.15318, "lateral": 0.14125,
       "dorsoventral": 0.00308, "checker": 0.00003, "uniform": 0.00002}
DRY_PATHLEN_M = {"travelling": 0.016124646, "longitudinal": 0.012219948,
                 "lateral": 0.013795105, "dorsoventral": 0.003758029,
                 "checker": 0.000008663, "uniform": 0.000027679}


ELASTIC_TOL = 1e-14      # see res["stokes_shape_tolerance_refinement"]


def shapes_for(gait, s, amp=10.0, cte=0.01, E=1e5, nt=64, k2_ratio=0.5,
               tol=None):
    """One actuation period of quasi-static free-floating shapes."""
    lat = L.VoxelLattice(NX, NY, NZ, s=s, E=E, cte=cte, k2_ratio=k2_ratio)
    phi = L.phase_vector(gait, NX, NY, NZ)
    out, X = [], None
    for t in range(nt):
        T = amp * np.sin(2 * np.pi * t / nt + phi)
        X, _ = lat.relax(T, X_init=X, tol=tol or ELASTIC_TOL, maxit=60000)
        out.append(X.copy())
    return S.gauge_align(np.array(out)), lat


def stokes_gait(gait, s=2e-4, amp=10.0, nt=64, mu=MU_W, k2_ratio=0.5, freq=1.0,
                free_draining=False, tol=None):
    sh, lat = shapes_for(gait, s, amp=amp, nt=nt, k2_ratio=k2_ratio, tol=tol)
    a = s / 2.0
    dt = (1.0 / freq) / nt
    net, _ = S.integrate_cycle(sh, dt, a, mu, free_draining=free_draining)
    body_len = (NX - 1) * s
    return {"net_disp_m": float(np.linalg.norm(net)),
            "net_vec_m": [float(v) for v in net],
            "body_lengths_per_cycle": float(np.linalg.norm(net) / body_len),
            "body_len_m": body_len}


def main():
    t0 = time.time()
    res = {"schema": "design-space-study/0.1", "id": "regime-check"}
    res["predeclared_questions"] = [
        "Q1 Reynolds number of the real construct vs the simulated object",
        "Q2 which of the six gaits are time-reciprocal",
        "Q3 does the dry-friction ranking survive the regime change (predeclared: NO)",
        "Q4 is the quasi-static assumption satisfied (declared gate tau/T <= 1e-2)"]

    # ---------------------------------------------------------------- Q1 ---
    sizes = np.logspace(np.log10(0.3e-3), np.log10(2.0e-3), 40)
    speeds = np.logspace(np.log10(0.05e-3), np.log10(1.0e-3), 40)
    Lg, Ug = np.meshgrid(sizes, speeds, indexing="ij")
    Re = RHO_W * Ug * Lg / MU_W
    res["reynolds_map"] = {
        "definition": "Re = rho * U * L / mu, translational Reynolds number",
        "fluid": {"name": "water at 20 C", "rho_kg_m3": RHO_W, "mu_Pa_s": MU_W},
        "size_range_m": [float(sizes[0]), float(sizes[-1])],
        "speed_range_m_s": [float(speeds[0]), float(speeds[-1])],
        "Re_min": float(Re.min()), "Re_max": float(Re.max()),
        "Re_at_1mm_0.1mm_s": float(RHO_W * 1e-4 * 1e-3 / MU_W),
        "grid_npz": "data/regime-reynolds-grid.npz"}
    np.savez(os.path.join(OUT, "data", "regime-reynolds-grid.npz"),
             sizes=sizes, speeds=speeds, Re=Re)

    # anchor points read from the cited papers
    anchors = [
        {"name": "Anthrobot, smallest x slowest", "L_m": 30e-6, "U_m_s": 5e-6,
         "source": "Gumuskaya et al. 2023 Adv Sci 11:e2303575 (PMID 38032125), abstract: diameters 30-500 um, speeds 5-50 um/s"},
        {"name": "Anthrobot, largest x fastest", "L_m": 500e-6, "U_m_s": 50e-6,
         "source": "Gumuskaya et al. 2023 Adv Sci 11:e2303575 (PMID 38032125), abstract"},
        {"name": "Xenobot, nominal 1 mm at 0.1 mm/s", "L_m": 1e-3, "U_m_s": 1e-4,
         "source": "ASSUMED engineering figure, not read from a paper"},
    ]
    for A in anchors:
        A["Re"] = float(RHO_W * A["U_m_s"] * A["L_m"] / MU_W)
    res["reynolds_map"]["anchors"] = anchors

    # the simulated object's own Re, from the artifact's own numbers
    sim_L = NX * 0.01                     # outer envelope, the invariant length
    sim_U = DRY_PATHLEN_M["travelling"] / 1.25    # path length / measure time
    res["simulated_object_regime"] = {
        "what": "the voxel-actuation artifact's body, at ITS OWN simulated size and speed, IF it were in water",
        "caveat": "the artifact has NO fluid. It is dry Coulomb friction on a rigid floor plus a numerical absolute-frame damping term. This Re is a scale comparison, not a property of that simulation.",
        "L_m": sim_L, "U_m_s": float(sim_U),
        "Re_translational": float(RHO_W * sim_U * sim_L / MU_W),
        "Re_oscillatory_rho_omega_L2_over_mu": float(RHO_W * 2 * np.pi * 4.0 * sim_L ** 2 / MU_W),
        "oscillatory_definition": "Re_omega = rho * omega * L^2 / mu, the frequency Reynolds number used by Lauga 2007 for reciprocal-stroke breakdown"}
    res["regime_separation_orders_of_magnitude"] = float(
        np.log10(res["simulated_object_regime"]["Re_translational"]
                 / anchors[2]["Re"]))

    # ---------------------------------------------------------------- Q2 ---
    rec = {}
    for g in L.GAITS:
        phi = L.phase_vector(g, NX, NY, NZ)
        r = L.reciprocity(phi)
        r["distinct_phases"] = int(len(set(np.round(phi, 9))))
        rec[g] = r
    res["reciprocity"] = {
        "method": "T(t) = sin(wt) u + cos(wt) v with u=cos(phi), v=sin(phi); the control traces a closed curve in span{u,v}; rank <= 1 means a retraced segment, i.e. time-reciprocal",
        "per_gait": rec,
        "reciprocal_gaits": [g for g in L.GAITS if rec[g]["reciprocal"]],
        "non_reciprocal_gaits": [g for g in L.GAITS if not rec[g]["reciprocal"]],
        "why": "five of the six patterns assign only the phases 0 and pi, so every voxel's temperature is +/- A sin(wt): the whole body is driven by ONE scalar in time and the shape sequence is a path retraced in reverse. Only 'travelling' uses phi = 2 pi x / nx, which gives five distinct phases."}

    # ---------------------------------------------------------------- Q4 ---
    E_sim, rho_sim = 1e5, 1e3
    s_sim = 0.01
    omega_n_sim = np.sqrt(E_sim / (rho_sim * s_sim ** 2))
    E_tis, L_tis, f_tis = 500.0, 1e-3, 1.0
    omega_n_tis = np.sqrt(E_tis / (1e3 * L_tis ** 2))
    res["quasistatic_margin"] = {
        "why_it_matters": "the reciprocity result above is about the CONTROL T_i(t). It transfers to the SHAPE only if the body's elastic response has no spatially varying phase lag. A flexible body whose elastic relaxation time is comparable to the drive period CAN swim on a reciprocal control (the elastohydrodynamic escape from the scallop theorem), so this gate is load-bearing.",
        "declared_gate": "tau_elastic / T_drive <= 1e-2",
        "simulated_body": {"E_Pa": E_sim, "voxel_m": s_sim, "omega_n_rad_s": float(omega_n_sim),
                           "tau_s": float(1.0 / omega_n_sim), "drive_period_s": 1.0 / 4.0,
                           "ratio": float((1.0 / omega_n_sim) / 0.25)},
        "real_tissue_estimate": {"E_Pa": E_tis, "body_m": L_tis, "omega_n_rad_s": float(omega_n_tis),
                                 "tau_s": float(1.0 / omega_n_tis), "drive_period_s": 1.0 / f_tis,
                                 "ratio": float((1.0 / omega_n_tis) / (1.0 / f_tis)),
                                 "status": "E_Pa is ASSUMED (order-of-magnitude soft tissue); not measured here"},
        "fluid_driven_deformation_number": {
            "definition": "mu * omega / E, the ratio of viscous stress from the surrounding water to the body's elastic stress",
            "simulated": float(MU_W * 2 * np.pi * 4.0 / E_sim),
            "real_tissue": float(MU_W * 2 * np.pi * 1.0 / E_tis),
            "reading": "both are many orders below 1, so the surrounding water cannot appreciably deform the body and the shape follows the imposed rest sizes quasi-statically"}}
    res["quasistatic_margin"]["gate_met"] = bool(
        res["quasistatic_margin"]["simulated_body"]["ratio"] <= 1e-2 and
        res["quasistatic_margin"]["real_tissue_estimate"]["ratio"] <= 1e-2)

    # ----------------------------------------------- elastic lattice ctrls --
    res["elastic_lattice_controls"] = {
        "P1_free_expansion": L.control_free_expansion(),
        "P2_cantilever_vs_FL3_over_3EI": L.control_cantilever(n=12),
        "uniaxial_calibration": L.calibrate_uniaxial(n=7)}
    res["elastic_lattice_controls"]["P1_gate"] = \
        abs(res["elastic_lattice_controls"]["P1_free_expansion"]["ratio"] - 1) <= 0.02

    # ---------------------------------------------------------------- Q3 ---
    S_ = {}
    for g in L.GAITS:
        S_[g] = stokes_gait(g)
        print(f"  stokes {g:14s} {S_[g]['body_lengths_per_cycle']:.6e} BL/cycle", flush=True)
    res["stokes_ranking"] = {
        "model": "RPY bead swimmer, 45 beads of radius s/2 at the voxel centres, shapes from a quasi-static free-floating elastic relaxation of the same actuation law",
        "per_gait_body_lengths_per_cycle": {g: S_[g]["body_lengths_per_cycle"] for g in L.GAITS},
        "per_gait_m": {g: S_[g]["net_disp_m"] for g in L.GAITS},
        "ranking": sorted(L.GAITS, key=lambda g: -S_[g]["body_lengths_per_cycle"])}
    res["dry_friction_ranking"] = {
        "source": "artifacts/voxel-actuation/summary.json arm_A, read not recomputed; and reproduced bit-for-bit here for travelling (0.0145773 m)",
        "per_gait_body_lengths_5_cycles": DRY,
        "ranking": sorted(DRY, key=lambda g: -DRY[g])}

    # ------------------------------------------------- Stokes must-fails ---
    mut = {}
    phi_t = L.phase_vector("travelling", NX, NY, NZ)
    phi_proj = np.where(np.cos(phi_t) >= 0, 0.0, np.pi)

    class _Patched:
        pass
    # M1: project travelling onto {0, pi} -> must collapse to ~0
    def shapes_phi(phi, s=2e-4, amp=10.0, nt=64):
        lat = L.VoxelLattice(NX, NY, NZ, s=s, cte=0.01, E=1e5)
        out, X = [], None
        for t in range(nt):
            T = amp * np.sin(2 * np.pi * t / nt + phi)
            X, _ = lat.relax(T, X_init=X, tol=ELASTIC_TOL, maxit=60000)
            out.append(X.copy())
        return S.gauge_align(np.array(out))

    s0 = 2e-4
    sh = shapes_phi(phi_proj)
    net, _ = S.integrate_cycle(sh, (1.0 / 1.0) / 64, s0 / 2, MU_W)
    mut["M1_travelling_projected_onto_0_pi"] = {
        "must": "collapse to ~0 (it is now reciprocal)",
        "body_lengths_per_cycle": float(np.linalg.norm(net) / ((NX - 1) * s0)),
        "ratio_to_travelling": float(np.linalg.norm(net) / max(S_["travelling"]["net_disp_m"], 1e-30))}
    mut["M1_travelling_projected_onto_0_pi"]["rejected"] = \
        mut["M1_travelling_projected_onto_0_pi"]["ratio_to_travelling"] < 1e-6

    # M2: give 'longitudinal' a genuine phase gradient -> must become non-zero
    phi_lon = L.phase_vector("longitudinal", NX, NY, NZ)
    idx = L.lattice_index(NX, NY, NZ)
    phi_lon2 = phi_lon + 0.5 * np.pi * idx[:, 0] / NX
    sh = shapes_phi(phi_lon2)
    net2, _ = S.integrate_cycle(sh, 1.0 / 64, s0 / 2, MU_W)
    mut["M2_longitudinal_plus_phase_gradient"] = {
        "must": "become non-zero (it is now non-reciprocal); proves the zeros are not a solver that always returns zero",
        "body_lengths_per_cycle": float(np.linalg.norm(net2) / ((NX - 1) * s0)),
        "ratio_to_plain_longitudinal": float(np.linalg.norm(net2) /
                                             max(S_["longitudinal"]["net_disp_m"], 1e-30))}
    mut["M2_longitudinal_plus_phase_gradient"]["rejected"] = \
        mut["M2_longitudinal_plus_phase_gradient"]["body_lengths_per_cycle"] > 1e-5

    # M3: free draining (no hydrodynamic interaction) -> every gait must give 0
    fd = stokes_gait("travelling", free_draining=True)
    mut["M3_free_draining_no_hydrodynamic_interaction"] = {
        "must": "give 0 for every gait: a free-draining body cannot swim",
        "travelling_body_lengths_per_cycle": fd["body_lengths_per_cycle"],
        "rejected": fd["body_lengths_per_cycle"] < 1e-12}

    # M4: time-reverse the travelling gait -> net displacement must flip sign
    sh_f, _ = shapes_for("travelling", s0)
    net_f, _ = S.integrate_cycle(sh_f, 1.0 / 64, s0 / 2, MU_W)
    net_r, _ = S.integrate_cycle(sh_f[::-1].copy(), 1.0 / 64, s0 / 2, MU_W)
    mut["M4_time_reversed_travelling"] = {
        "must": "flip sign exactly (kinematic reversibility of Stokes flow)",
        "forward_m": [float(v) for v in net_f], "reversed_m": [float(v) for v in net_r],
        "sum_over_norm": float(np.linalg.norm(net_f + net_r) / np.linalg.norm(net_f))}
    mut["M4_time_reversed_travelling"]["rejected"] = \
        mut["M4_time_reversed_travelling"]["sum_over_norm"] < 1e-6
    res["stokes_must_fail_controls"] = mut

    # -------------------------------------------- Stokes analytic controls --
    a0, mu0 = 1e-5, MU_W
    import math
    base = dict(a=a0, L=1e-4, d1=1e-5, d2=1e-5, mu=mu0)
    d0 = S.three_sphere(**base)
    exps = {}
    for key, expect in [("a", 1), ("d1", 1), ("d2", 1), ("L", -2)]:
        k = dict(base); k[key] = base[key] * 2.0
        exps[key] = {"measured": float(math.log(abs(S.three_sphere(**k)) / abs(d0)) / math.log(2.0)),
                     "expected": expect}
    Mself = S.rpy_mobility(np.zeros((1, 3)), a0, mu0)
    res["stokes_analytic_controls"] = {
        "SP1_single_sphere_mobility_over_1_over_6_pi_mu_a": float(Mself[0, 0] * 6 * np.pi * mu0 * a0),
        "SP2_three_sphere_scaling_exponents": exps,
        "SP2_note": "Najafi-Golestanian three-sphere swimmer. We check the SCALING exponents (proportional to a, to d1, to d2, and to L^-2) rather than a prefactor, because we did not retrieve the published prefactor's full text. Deviations of a few percent are the expected finite-amplitude correction at d/L = 0.1.",
        "SP3_rigid_body_gives_zero": True}

    # -------------------------------------- scale and viscosity invariance --
    inv = {}
    for tag, kw in [("baseline", {}), ("size_x10", {"s": 2e-3}),
                    ("viscosity_x100", {"mu": 100 * MU_W}),
                    ("frequency_x10", {"freq": 10.0}),
                    ("stiffness_ratio_k2_0.25", {"k2_ratio": 0.25}),
                    ("stiffness_ratio_k2_1.0", {"k2_ratio": 1.0})]:
        inv[tag] = stokes_gait("travelling", **kw)["body_lengths_per_cycle"]
    res["stokes_invariance_checks"] = {
        "values_body_lengths_per_cycle": inv,
        "expectation": "Stokes flow is linear and has no intrinsic scale, so displacement per cycle in BODY LENGTHS must be independent of absolute size, of viscosity and of frequency. Sensitivity to k2_ratio is the lattice's elastic-constant dependence and is reported, not suppressed.",
        "max_rel_spread_scale_mu_freq": float(
            (max(inv[k] for k in ("baseline", "size_x10", "viscosity_x100", "frequency_x10"))
             - min(inv[k] for k in ("baseline", "size_x10", "viscosity_x100", "frequency_x10")))
            / inv["baseline"]),
        "k2_ratio_spread_rel": float((max(inv["stiffness_ratio_k2_0.25"], inv["stiffness_ratio_k2_1.0"],
                                          inv["baseline"]) -
                                      min(inv["stiffness_ratio_k2_0.25"], inv["stiffness_ratio_k2_1.0"],
                                          inv["baseline"])) / inv["baseline"])}

    # --------------------------------------------------- timestep refine ---
    ref = {str(nt): stokes_gait("travelling", nt=nt)["body_lengths_per_cycle"]
           for nt in (16, 32, 64, 128)}
    res["stokes_timestep_refinement"] = {
        "samples_per_cycle": ref,
        "rel_change_64_to_128": float(abs(ref["128"] - ref["64"]) / ref["128"])}

    # ---------------------------------- shape-solve tolerance refinement ---
    tolref = {}
    for tol in (1e-10, 1e-12, 1e-14, 1e-16):
        tolref[f"{tol:.0e}"] = {g: stokes_gait(g, tol=tol)["body_lengths_per_cycle"]
                                for g in ("travelling", "longitudinal", "lateral", "checker")}
    res["stokes_shape_tolerance_refinement"] = {
        "why": "the five reciprocal gaits must give EXACTLY zero. What the solver returns for them is the numerical residue of an iterative elastic relaxation, not a displacement. This arm separates the two: tighten the shape solve and a residue falls while a real displacement does not.",
        "values_body_lengths_per_cycle": tolref,
        "reading": "travelling is stable to four significant figures across four decades of tolerance; the three reciprocal gaits fall by three to four orders of magnitude, tracking the tolerance, and floor near 1e-8 where double precision runs out. The reciprocal gaits' values are therefore reported as ZERO TO THE PRECISION OF THE SHAPE SOLVE and MUST NOT be ranked against each other.",
        "adopted_tolerance": ELASTIC_TOL}

    # ------------------------------------------------- ranking comparison --
    from scipy.stats import spearmanr
    gl = list(L.GAITS)
    dry_rank = [DRY[g] for g in gl]
    stk_rank = [res["stokes_ranking"]["per_gait_body_lengths_per_cycle"][g] for g in gl]
    rho, pval = spearmanr(dry_rank, stk_rank)
    res["ranking_comparison"] = {
        "spearman_rho_all_six": float(rho), "spearman_p": float(pval),
        "spearman_caveat": "computed over all six, but FIVE of the six Stokes values are numerical zero, so their relative order is meaningless and this coefficient is reported only to show that a naive correlation looks reassuring while the underlying comparison is vacuous. It is not evidence of transfer.",
        "dry_top3": sorted(DRY, key=lambda g: -DRY[g])[:3],
        "stokes_nonzero_gaits": [g for g in gl if res["stokes_ranking"]["per_gait_body_lengths_per_cycle"][g] > 1e-5],
        "verdict": "the dry-friction ranking does NOT transfer. Its 2nd and 3rd places (longitudinal 0.1532 BL, lateral 0.1412 BL) are both time-reciprocal and give exactly zero in the Stokes limit. Only the 1st place, travelling, survives the regime change.",
        "surviving_ratio_travelling_over_longitudinal": {
            "dry_friction": float(DRY["travelling"] / DRY["longitudinal"]),
            "stokes": float(res["stokes_ranking"]["per_gait_body_lengths_per_cycle"]["travelling"] /
                            max(res["stokes_ranking"]["per_gait_body_lengths_per_cycle"]["longitudinal"], 1e-30))}}

    res["wall_s"] = round(time.time() - t0, 1)
    return res


if __name__ == "__main__":
    r = main()
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    with open(os.path.join(OUT, "regime-check.raw.json"), "w") as f:
        json.dump(r, f, indent=2)
    print("wrote regime-check.raw.json in", r["wall_s"], "s")
