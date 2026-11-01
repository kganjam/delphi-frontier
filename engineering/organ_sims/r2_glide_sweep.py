"""R2: wing area / aspect ratio / wing-placement sweep for launch-and-glide range, with mass, CG-window, ballast-bay,
printer-envelope and biological-proportion constraints checked against the r3-daane printed STL masses.

    python -m engineering.organ_sims.r2_glide_sweep

Model (all simulated, none observed):
  aero   CL_alpha from the committed VLM of v3c (CL 0.2511 at 4 deg on S_lattice; vlm.json) scaled to other AR by Helmbold
         (the repo's own hand-NP method); CL_max is an ASSUMED scenario (0.6/0.8/1.0); CD0 from flat-plate laminar skin friction
         (Blasius, recalled) on the measured wetted areas with a 1.3 form factor; Oswald e = 0.8 assumed.
  mass   printed masses from flight_model.json (mesh volume x 1220 kg/m3); fin mass scales with area only (underestimates
         the spar mass of high-AR fins, flagged by R3).
  trim   ballast in the nose bay puts the CG at NP - 8% MAC; NP moves 0.85 x the wing shift (assumed, pectoral lift share).
  flight engineering.simulation.glide.integrate (point mass, fixed CL = min(CLmax, CL at max L/D)), h0 1.35 m, V0 4/6/8 m/s.
"""
import itertools, json, math
import numpy as np
from engineering.simulation import glide
from engineering.simulation.schema import G
from engineering.organ_sims import common as C

RID = "r2-glide-sweep"
FM = "artifacts/glider/r3-daane/flight_model.json"
MAN = "artifacts/glider/r3-daane/manifest.json"
VLM = "artifacts/cfd3d/vlm/fish3d-v3c-daane-length/vlm.json"
CAND = "artifacts/fish3d/fish3d-v3c-daane-length/candidate.json"
RHO, NU = 1.204, 1.516e-5
H0, E_OSW, FF = 1.35, 0.8, 1.3
SM = 0.08                     # static margin, fraction of pectoral MAC (assumed)
NP_FACTOR = 0.85              # NP shift per unit wing shift (assumed)
X_BALLAST = 15.0e-3           # bay centroid, full bay (flight_model fill rows: 14.8-15.2 mm)
H = json.load(open(C.ROOT / FM)); M = json.load(open(C.ROOT / MAN)); V = json.load(open(C.ROOT / VLM)); K = json.load(open(C.ROOT / CAND))

parts = {p["id"]: p for p in H["parts"]}
m_shell = parts["body"]["mass_kg"] + parts["catch_plug-x20-dz+0.0"]["mass_kg"]
cg_shell = (parts["body"]["mass_kg"] * parts["body"]["cg_m"][0] + parts["catch_plug-x20-dz+0.0"]["mass_kg"] * parts["catch_plug-x20-dz+0.0"]["cg_m"][0]) / m_shell
m_pec2 = parts["pectoral_L"]["mass_kg"] + parts["pectoral_R"]["mass_kg"]
m_pel2 = parts["pelvic_L-dec+2"]["mass_kg"] + parts["pelvic_R-dec+2"]["mass_kg"]
cg_pec = parts["pectoral_L"]["cg_m"][0]; cg_pel = parts["pelvic_L-dec+2"]["cg_m"][0]
HNP = M["hand_neutral_point"]
S_PEC0 = 2 * HNP["pectoral"]["area_mm2"] * 1e-6; S_PEL = 2 * HNP["pelvic"]["area_mm2"] * 1e-6
MAC = HNP["pectoral_mac_mm"] * 1e-3
NP0 = float(np.mean(HNP["np_x_mm_bracket"])) * 1e-3
X_ROOT0 = H["lifting_surfaces"][0]["frame_L"]["origin_mm"][0] * 1e-3
Y0 = H["lifting_surfaces"][0]["frame_L"]["origin_mm"][1] * 1e-3
LP0 = HNP["pectoral"]["span_in_plane_mm"] * 1e-3
SL = K["biology"]["standard_length_m"]["value"]
EUY = H["lifting_surfaces"][0]["frame_L"]["e_u"][1]
BALLAST_MAX = H["ballast"]["mass_range_kg"][1]
A4 = 4.0; CL4 = V["cases"]["4"]["CL_paired_fins_on_S_lattice"]; S_LAT = V["lattice"]["S_lattice_m2"]
CLA0 = CL4 / A4                       # per degree, on S_lattice, baseline planform
B0 = 2 * (Y0 + LP0 * EUY); AR0 = B0 ** 2 / (S_PEC0 + S_PEL)
helm = lambda ar: 2 * math.pi * ar / (2 + math.sqrt(4 + ar * ar))   # Helmbold slope per rad
# wetted areas, laminar flat plate + form factor, reference length = standard length, V-dependent Re handled in cd0()
S_WET_BODY = H["body"]["wetted_area_m2"]


FF_BODY, FF_FIN = 1.5, 1.5    # assumed: blunt hollow body with slot and no scales; fins with ridges and rim bead


def cf_lam(Re):
    return 1.328 / math.sqrt(Re) if Re < 5e5 else 0.455 / math.log10(Re) ** 2.58


def cd0(V0, S):
    """Skin friction with each surface at its OWN Reynolds number (fin chord Re ~1e4, not body-length Re) plus assumed
    form/ridge factors.  Optimistic: no separation, no interference, no launch-pitch drag."""
    return (cf_lam(V0 * SL / NU) * FF_BODY * S_WET_BODY + cf_lam(V0 * MAC / NU) * FF_FIN * 2 * S) / S


def config(S_pec, ar, dx, cl_max, v0, gam0, cd0_add=0.0):
    """One design point -> dict (constraints + mass + aero inputs)."""
    S = S_pec + S_PEL
    b = math.sqrt(ar * S)
    L_fin = (b / 2 - Y0) / EUY
    k = S_pec / S_PEC0
    m_pec = m_pec2 * k
    x_root = X_ROOT0 + dx
    dry_m = m_shell + m_pec + m_pel2
    cg_dry = (m_shell * cg_shell + m_pec * (cg_pec + dx) + m_pel2 * cg_pel) / dry_m   # pelvics stay put
    np_x = NP0 + NP_FACTOR * dx
    x_t = np_x - SM * MAC
    m_b = max(dry_m * (cg_dry - x_t) / (x_t - X_BALLAST), 0.0)
    m_tot = dry_m + m_b
    cg_final = (dry_m * cg_dry + m_b * X_BALLAST) / m_tot
    # lift slope on S: baseline VLM slope scaled by Helmbold(AR)/Helmbold(AR0), area-normalised on S
    cla = CLA0 * 57.2958 * helm(ar) / helm(AR0)       # informational: not used by the fixed-CL glide
    return {"S_pec_m2": S_pec, "S_m2": S, "AR": ar, "b_m": b, "L_fin_m": L_fin, "dx_m": dx, "x_root_m": x_root,
            "m_dry_kg": dry_m, "m_ballast_kg": m_b, "m_total_kg": m_tot, "cg_final_m": cg_final, "np_m": np_x,
            "wing_loading_N_m2": m_tot * G / S, "CL_alpha_per_rad": cla, "CLmax": cl_max, "V0": v0, "gam0": gam0, "cd0_add": cd0_add}


def constraints(c):
    return {"ballast_fits_bay": c["m_ballast_kg"] <= BALLAST_MAX,
            "cg_in_44_60mm_window": 0.044 <= c["cg_final_m"] <= 0.060,
            "fin_clears_catch_slot_x_root_ge_37mm": c["x_root_m"] >= 0.037,
            "pectoral_print_length_le_115mm": c["L_fin_m"] <= 0.115,
            "pectoral_over_SL_in_0.584_0.77": 0.584 <= c["L_fin_m"] / SL <= 0.77,
            "mass_le_hand_limit_V8_at_CL0.5": c["m_total_kg"] <= 0.5 * RHO * 8 ** 2 * c["S_m2"] * 0.5 / G}


SOFT = "mass_le_hand_limit_V8_at_CL0.5"      # claude-07 rule of thumb for trim speed; reported separately, not a hard limit


def flight(cs):
    """Vectorised point-mass glides for a list of configs."""
    S = np.array([c["S_m2"] for c in cs]); ar = np.array([c["AR"] for c in cs]); m = np.array([c["m_total_kg"] for c in cs])
    v0 = np.array([c["V0"] for c in cs]); clm = np.array([c["CLmax"] for c in cs]); g0 = np.radians([c["gam0"] for c in cs])
    cd = np.array([cd0(c["V0"], c["S_m2"]) + c["cd0_add"] for c in cs])   # cd0_add: low-Re profile-drag penalty scenario (argon review #2)
    cl = glide.cl_command(clm, cd, E_OSW, ar)
    rng, rsn = np.zeros(len(cs)), np.zeros(len(cs), int)
    for g in np.unique(g0):                      # integrate() takes one release angle per call
        i = g0 == g
        out = glide.integrate(m[i], S[i], ar[i], RHO, cl[i], cd[i], E_OSW, H0, v0[i], gam0=float(g), dt=0.002)
        rng[i], rsn[i] = out["range_m"], out["end_reason"]
    ld = cl / glide.drag_coeff(cl, cd, E_OSW, ar)
    return rng, rsn, cl, ld


def main():
    checks = []
    # --- controls ---------------------------------------------------------------------------------------------
    base = config(S_PEC0, AR0, 0.0, 0.8, 6.0, 0.0)
    c0 = config(S_PEC0, AR0, 0.0, 0.8, 6.0, 0.0)
    # control 1: reproduce the repo's hand ballast for CG 52 mm (26.07 g) with its own formula
    dry = m_shell + m_pec2 + m_pel2; cgd = (m_shell * cg_shell + m_pec2 * cg_pec + m_pel2 * cg_pel) / dry
    mb52 = dry * (cgd - 0.052) / (0.052 - X_BALLAST)
    checks.append({"name": "control: ballast model reproduces repo's 26.07 g total at CG 52 mm within 3%",
                   "pass": abs((dry + mb52) / 0.02607182 - 1) < 0.03, "detail": {"mine_g": (dry + mb52) * 1e3, "repo_g": 26.0718, "dry_g": dry * 1e3, "repo_dry_g": 20.3346}})
    checks.append({"name": "control: dry mass equals flight_model assembled_dry within 0.5% (plug included)", "pass": abs(dry / H["assembled_dry"]["mass_kg"] - 1) < 5e-3,
                   "detail": {"sum_g": dry * 1e3, "assembled_g": H["assembled_dry"]["mass_kg"] * 1e3}})
    # control 2: ballistic range with lift and drag off. CL=0.5 only sets the stall floor (lift is off); an earlier
    # draft passed CL=0, which makes V_stall infinite and ended every case at t=0 (control failed, recorded in git history)
    bal = glide.integrate(0.026, 0.0068, 7.5, RHO, 0.5, 0.0, 0.8, H0, np.array([4.0, 6.0, 8.0]), dt=0.002, drag=False, lift=False)["range_m"]
    exact = np.array([4.0, 6.0, 8.0]) * math.sqrt(2 * H0 / G)
    checks.append({"name": "control: ballistic range equals V0 sqrt(2h/g) within 0.3%", "pass": bool(np.all(abs(bal / exact - 1) < 3e-3)), "detail": {"num": bal.tolist(), "exact": exact.tolist()}})
    # control 3: time-step convergence of the glide integrator at the baseline
    def rng_dt(dt):
        cl = glide.cl_command(0.8, cd0(6.0, base["S_m2"]), E_OSW, AR0)
        return float(glide.integrate(base["m_total_kg"], base["S_m2"], AR0, RHO, cl, cd0(6.0, base["S_m2"]), E_OSW, H0, 6.0, dt=dt)["range_m"][0])
    r1, r2 = rng_dt(0.004), rng_dt(0.002)
    checks.append({"name": "control: baseline range dt 0.004 vs 0.002 differs < 0.5%", "pass": abs(r1 / r2 - 1) < 5e-3, "detail": [r1, r2]})
    # --- sweep ------------------------------------------------------------------------------------------------
    S_pecs = np.array([0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]) * S_PEC0
    ars = np.array([0.7, 0.85, 1.0, 1.2, 1.4]) * AR0
    dxs = np.array([-0.004, 0.0, 0.004, 0.008, 0.012, 0.018, 0.024])
    rows = []
    for sp, ar, dx, clm, v0, g0, ca in itertools.product(S_pecs, ars, dxs, (0.6, 0.8, 1.0), (4.0, 6.0, 8.0), (0.0, 10.0), (0.0, 0.02)):
        c = config(sp, ar, dx, clm, v0, g0, ca)
        c["constraints"] = constraints(c)
        rows.append(c)
    rg, er, cl, ld = flight(rows)
    for c, r_, e_, cl_, ld_ in zip(rows, rg, er, cl, ld):
        c.update(range_m=float(r_), end_reason=int(e_), CL_flown=float(cl_), L_over_D=float(ld_), feasible=all(v for k, v in c["constraints"].items() if k != SOFT), meets_hand_mass_limit=c["constraints"][SOFT])
        # energy upper bound on range: (h + V0^2/2g) * L/D_max
        c["range_energy_bound_m"] = float((H0 + c["V0"] ** 2 / (2 * G)) * ld_)
    checks.append({"name": "every sweep range is finite, >= 0 and below the energy bound (h+V0^2/2g)*L/D", "pass": all(math.isfinite(c["range_m"]) and 0 <= c["range_m"] <= c["range_energy_bound_m"] for c in rows),
                   "detail": {"n": len(rows), "worst_ratio": max(c["range_m"] / c["range_energy_bound_m"] for c in rows)}})
    # baseline (r3 geometry, nominal ballast at CG ~NP-8% MAC) reference rows
    def pick(v0, clm, g0, dx=0.0, sp=S_PEC0, ar=AR0):
        return next(c for c in rows if abs(c["S_pec_m2"] - sp) < 1e-12 and abs(c["AR"] - ar) < 1e-9 and abs(c["dx_m"] - dx) < 1e-12 and c["CLmax"] == clm and c["V0"] == v0 and c["gam0"] == g0 and c["cd0_add"] == 0.0)
    summary = {"baseline": {}, "best_feasible": {}, "best_unconstrained": {}}
    for v0 in (4.0, 6.0, 8.0):
        for clm in (0.6, 0.8, 1.0):
            sel = [c for c in rows if c["V0"] == v0 and c["CLmax"] == clm and c["gam0"] == 0.0 and c["cd0_add"] == 0.0]
            bf = max((c for c in sel if c["feasible"]), key=lambda c: c["range_m"], default=None)
            bu = max(sel, key=lambda c: c["range_m"])
            b0 = pick(v0, clm, 0.0)
            key = f"V0={v0:g},CLmax={clm}"
            summary["baseline"][key] = {k: b0[k] for k in ("range_m", "m_total_kg", "m_ballast_kg", "cg_final_m", "CL_flown", "L_over_D", "feasible", "constraints")}
            summary["best_feasible"][key] = bf and {k: bf[k] for k in ("range_m", "S_pec_m2", "AR", "dx_m", "m_total_kg", "m_ballast_kg", "cg_final_m", "L_fin_m")}
            summary["best_unconstrained"][key] = {**{k: bu[k] for k in ("range_m", "S_pec_m2", "AR", "dx_m", "m_total_kg", "m_ballast_kg", "cg_final_m", "L_fin_m")},
                                                   "violates": [k for k, ok in bu["constraints"].items() if not ok]}
    # low-Re penalty scenario: same selection with cd0_add = 0.02 (separation bubbles on thin printed plates at Re_c ~1e4)
    summary["lowRe_penalty_cd0+0.02"] = {}
    for v0 in (4.0, 6.0, 8.0):
        sel = [c for c in rows if c["V0"] == v0 and c["CLmax"] == 0.8 and c["gam0"] == 0.0 and c["cd0_add"] == 0.02]
        bf = max((c for c in sel if c["feasible"]), key=lambda c: c["range_m"])
        b0 = next(c for c in sel if abs(c["S_pec_m2"] - S_PEC0) < 1e-12 and abs(c["AR"] - AR0) < 1e-9 and abs(c["dx_m"]) < 1e-12)
        summary["lowRe_penalty_cd0+0.02"][f"V0={v0:g},CLmax=0.8"] = {"baseline_range_m": b0["range_m"], "best_feasible_range_m": bf["range_m"],
                                                                     "best_feasible": {k: bf[k] for k in ("S_pec_m2", "AR", "dx_m", "L_fin_m")}}
    nfeas = sum(c["feasible"] for c in rows)
    # which constraints bind
    viol = {k: sum(not c["constraints"][k] for c in rows) for k in rows[0]["constraints"]}
    checks.append({"name": "baseline r3 geometry reproduces repo hand verdict: fails hand mass limit (V_trim<=8 m/s at CL 0.5)", "pass": not pick(6.0, 0.8, 0.0)["constraints"]["mass_le_hand_limit_V8_at_CL0.5"], "detail": pick(6.0, 0.8, 0.0)["m_total_kg"]})
    checks.append({"name": "bound: baseline range at V0=8, CLmax 0.8 is within 0.5-25 m (plausible-order guard)", "pass": 0.5 < summary["baseline"]["V0=8,CLmax=0.8"]["range_m"] < 25, "detail": summary["baseline"]["V0=8,CLmax=0.8"]["range_m"]})
    checks.append({"name": "recorded (not gated): number of fully feasible configs", "pass": True, "detail": {"feasible": nfeas, "total": len(rows), "violations_by_constraint": viol}})
    figs = fig(rows)
    C.manifest(RID, "Wing area / AR / placement sweep for launch glide range with printed-mass and constraint checks",
               [FM, MAN, VLM, CAND, "engineering/simulation/glide.py"],
               {"summary": summary, "n_configs": len(rows), "n_feasible_hard": nfeas, "n_meets_hand_mass_limit": sum(c["meets_hand_mass_limit"] for c in rows), "n_feasible_and_hand_limit": sum(c["feasible"] and c["meets_hand_mass_limit"] for c in rows), "violations_by_constraint": viol, "aero_basis": {"CL_alpha_per_deg_v3c_vlm": CLA0, "AR0_whole_wing": AR0, "S_pec0_m2": S_PEC0, "S_pel_m2": S_PEL, "SL_m": SL},
                "assumptions": {"cd0_add_scenarios": [0.0, 0.02], "form_factors_body_fin": [FF_BODY, FF_FIN], "CLmax": [0.6, 0.8, 1.0], "oswald_e": E_OSW, "form_factor": FF, "static_margin_frac_MAC": SM, "np_shift_factor": NP_FACTOR, "h0_m": H0, "rho": RHO},
                "rows_file": f"artifacts/organ-sims/{RID}/rows.json.gz"},
               checks, {"see": "docs/organ-sims.md"}, seed=None, figures=figs)
    import gzip
    with gzip.open(C.OUT / RID / "rows.json.gz", "wt") as fh:
        fh.write(json.dumps(rows, default=float))
    print(json.dumps(summary, indent=1, default=float)[:4000]); print("violations", viol, "feasible", nfeas, "/", len(rows))
    C.enforce(checks)


def fig(rows):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fp = C.OUT / RID / "range_maps.png"; (C.OUT / RID).mkdir(parents=True, exist_ok=True)
    fig, axs = plt.subplots(1, 3, figsize=(14, 4))
    for ax, v0 in zip(axs, (4.0, 6.0, 8.0)):
        sel = [c for c in rows if c["V0"] == v0 and c["CLmax"] == 0.8 and c["gam0"] == 0.0 and abs(c["dx_m"]) < 1e-9 and c["cd0_add"] == 0.0]
        S = sorted({c["S_pec_m2"] for c in sel}); A = sorted({c["AR"] for c in sel})
        Z = np.array([[next(c["range_m"] for c in sel if c["S_pec_m2"] == s and c["AR"] == a) for s in S] for a in A])
        F = np.array([[next(c["feasible"] for c in sel if c["S_pec_m2"] == s and c["AR"] == a) for s in S] for a in A])
        im = ax.pcolormesh(np.array(S) * 1e4, A, Z, shading="nearest"); fig.colorbar(im, ax=ax, label="range m")
        ax.contour(np.array(S) * 1e4, A, F.astype(float), [0.5], colors="w")
        ax.scatter([S_PEC0 * 1e4], [AR0], c="r", marker="*"); ax.set_title(f"V0={v0:g} m/s, CLmax 0.8, dx 0 (white: hard constraints ok)", fontsize=7)
        ax.set_xlabel("pectoral pair area, cm2"); ax.set_ylabel("whole-wing AR")
    fig.tight_layout(); fig.savefig(fp, dpi=110)
    return [f"artifacts/organ-sims/{RID}/range_maps.png"]


if __name__ == "__main__":
    main()
