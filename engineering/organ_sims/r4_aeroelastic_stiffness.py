"""R4: aeroelastic deflection over the SOURCED fin-ray stiffness range (and the printed fin), two-way static coupling.

    python -m engineering.organ_sims.r4_aeroelastic_stiffness

Uses the committed coupled model unchanged (engineering.aeroelastic.run.solve_arm: VLM on the v3a fins + constant-EI
Hermite cantilever per fin, under-relaxed fixed point, linear-beam domain gate tip/span <= 0.1, slope <= 0.2 rad), with
ONE substitution: vlm.lattice is replaced by the consistent-collocation lattice from R1 (the committed lattice puts some
collocation points outside their own panels).  A control records the rigid CL under both lattices.

Stiffness input (the only new physics input):
  ray EI       Alben, Madden & Lauder 2007 (J R Soc Interface 4:243, doi 10.1098/rsif.2006.0181) Sec 3.4: three-point
               bending of bluegill pectoral rays, E ~ 1e8-1e9 Pa, I ~ 1e-6 cm^4 -> EI ~ 1e-6-1e-5 N m^2 (read in
               aeroelastic-sources/alben2007.txt lines 393-433).  Abstract: fish can vary ray stiffness by more than an
               order of magnitude.  Bluegill, ray length ~4 cm; NOT flying fish.
  fin EI       n_rays x ray EI (rays bending in parallel, membrane ignored): an UPPER bound for a fan of splayed rays.
               n_rays from rays.json (pectoral 15, pelvic 6; model geometry, not a sourced count).
  size scaling isometric bluegill->flying-fish ray: I ~ (L_fin/4 cm)^4.  A scenario, not a measurement.
  printed fin  composite section of the r4 pectoral (membrane 0.5 mm, spar 1.6 x 2.0 mm, ridges 0.8 x 1.0 mm) with the
               manufacturer flexural modulus 2.08 GPa (Alpha Grey V1 TDS, as recorded in the r4 manifest).
Speeds 8 (printed launch), 12, 16, 20 m/s (16-20 'relayed from Fish 1990', not read here); alpha 4 deg; rho 1.204.
"""
import json, math, sys, time
from pathlib import Path
import numpy as np
from engineering.cfd3d import vlm
from engineering.aeroelastic import run as AR, model as AM
from engineering.organ_sims import common as C
from engineering.organ_sims import r1_v3b_convergence as R1

RID = "r4-aeroelastic-stiffness"
PROT = "artifacts/aeroelastic/protocol.json"
RAYS = "artifacts/fish3d/fish3d-v3a-fan/rays.json"
R4M = "artifacts/glider/r4-daane-printfix/manifest.json"
SRC = "/data/artifacts/delphi-evolve-rethink/aeroelastic-sources/alben2007.txt"
SPEEDS = [8.0, 12.0, 16.0, 20.0]
EI_GRID = np.logspace(-5.5, -1.5, 17)          # pectoral whole-fin EI, N m^2
RAY_EI = (1e-6, 1e-5)                           # Alben 2007 Sec 3.4
L_BLUEGILL = 0.04
SCR = Path(sys.argv[1]) if len(sys.argv) > 1 else C.OUT / RID / "_arms"


def printed_EI(E, membrane_chord, n_ridges, spar=(1.6e-3, 2.0e-3), ridge=(0.8e-3, 1.0e-3), t_mem=0.5e-3):
    """Composite rectangle section; spar and ridges hang below the membrane (heights are total depth from the membrane's
    upper face, as the r4 manifest states).  Returns EI about the composite neutral axis."""
    rects = [(membrane_chord, t_mem, -t_mem / 2)]
    rects.append((spar[0], spar[1] - t_mem, -t_mem - (spar[1] - t_mem) / 2))
    rects += [(ridge[0], ridge[1] - t_mem, -t_mem - (ridge[1] - t_mem) / 2)] * n_ridges
    A = sum(b * h for b, h, _ in rects)
    zc = sum(b * h * z for b, h, z in rects) / A
    I = sum(b * h ** 3 / 12 + b * h * (z - zc) ** 2 for b, h, z in rects)
    zmax = max(max(abs(z + h / 2 - zc), abs(z - h / 2 - zc)) for b, h, z in rects)
    return E * I, I, zmax


def main():
    t0 = time.time()
    P = json.loads((C.ROOT / PROT).read_text())
    EIin = P["parameters"]["EI_inputs"]
    pel_ratio = EIin["pelvic_L"]["EI_Nm2_by_compliance"]["0.2"] / EIin["pectoral_L"]["EI_Nm2_by_compliance"]["0.2"]
    ei02 = EIin["pectoral_L"]["EI_Nm2_by_compliance"]["0.2"]
    rays = json.loads((C.ROOT / RAYS).read_text())["fins"]
    n_pec, n_pel = rays["pectoral_L"]["n_rays"], rays["pelvic_L"]["n_rays"]
    L_pec = EIin["pectoral_L"]["length_m"]
    scale_iso = (L_pec / L_BLUEGILL) ** 4
    bands = {"sourced_bluegill_x_nrays": [n_pec * RAY_EI[0], n_pec * RAY_EI[1]],
             "sourced_x10_active_stiffening": [n_pec * RAY_EI[0], 10 * n_pec * RAY_EI[1]],
             "isometric_size_scaled": [n_pec * RAY_EI[0] * scale_iso, n_pec * RAY_EI[1] * scale_iso],
             "committed_assay_design_values": sorted(EIin["pectoral_L"]["EI_Nm2_by_compliance"].values())}
    M = json.loads((C.ROOT / R4M).read_text())
    E = M["material"]["flexural_modulus_Pa"]; UTS = M["material"]["ultimate_tensile_strength_Pa"]
    mac = M["hand_neutral_point"]["pectoral_mac_mm"] * 1e-3
    EI_print, I_print, zmax = printed_EI(E, mac, n_pec - 1)
    EI_print_tip, _, _ = printed_EI(E, mac * 0.6, n_pec - 1, spar=(1.6e-3, 1.2e-3))
    bands["printed_r4_root_section"] = EI_print
    bands["printed_r4_tip_section"] = EI_print_tip
    checks = []
    # control A: printed section reproduces a membrane-only plate exactly when spar/ridges are removed
    eim, _, _ = printed_EI(E, 0.03, 0, spar=(1e-9, 0.5e-3 + 1e-12))
    checks.append({"name": "control: section routine gives E b t^3/12 for a bare membrane (1e-6 rel)", "pass": abs(eim / (E * 0.03 * 0.5e-3 ** 3 / 12) - 1) < 1e-6, "detail": eim})
    # control B: source text lines contain the EI numbers used
    src = Path(SRC).read_text(errors="ignore") if Path(SRC).exists() else ""
    checks.append({"name": "control: source text contains the measured EI statement (10^-6-10^-5 J m)", "pass": "measured B" in src.replace("\n", " ") and "10K6" in src, "detail": SRC})
    rows = []
    SCR.mkdir(parents=True, exist_ok=True)
    # lattice control: rigid CL committed vs consistent lattice at 20 m/s
    AM.setup.cache_clear()
    r_orig = AR.solve_arm("0.2", 20.0, "fine", "rigid", SCR / "ctrl-orig", time.monotonic() + 600)
    vlm.lattice = R1.lattice_consistent
    AM.setup.cache_clear()
    r_cons = AR.solve_arm("0.2", 20.0, "fine", "rigid", SCR / "ctrl-cons", time.monotonic() + 600)
    lat_ctrl = {"CL_rigid_committed_lattice": r_orig["iterations"][-1]["CL_on_fixed_source_area"], "CL_rigid_consistent_lattice": r_cons["iterations"][-1]["CL_on_fixed_source_area"]}
    lat_ctrl["rel_diff"] = abs(lat_ctrl["CL_rigid_consistent_lattice"] / lat_ctrl["CL_rigid_committed_lattice"] - 1)
    checks.append({"name": "control: rigid CL changes < 3% between committed and consistent lattice (fine 24x6)", "pass": lat_ctrl["rel_diff"] < 0.03, "detail": lat_ctrl})
    # control C: stiff limit -> two-way equals rigid
    stiff = AR.solve_arm("0.2", 20.0, "fine", "two-way-static-feedback", SCR / "ctrl-stiff", time.monotonic() + 600, scenario={"EI_scale": 1e6})
    checks.append({"name": "control: EI x1e6 two-way CL equals rigid within 1e-6", "pass": abs(stiff["iterations"][-1]["CL_on_fixed_source_area"] - lat_ctrl["CL_rigid_consistent_lattice"]) < 1e-6,
                   "detail": [stiff["status"], stiff["iterations"][-1]["CL_on_fixed_source_area"]]})
    rigid = {}
    for U in SPEEDS:
        rr = AR.solve_arm("0.2", U, "fine", "rigid", SCR / f"rigid-u{U:g}", time.monotonic() + 600)
        rigid[U] = rr["iterations"][-1]["CL_on_fixed_source_area"]
    for U in SPEEDS:
        for ei in EI_GRID:
            d = SCR / f"u{U:g}-ei{ei:.3e}"
            r = AR.solve_arm("0.2", U, "fine", "two-way-static-feedback", d, time.monotonic() + 600, scenario={"EI_scale": float(ei / ei02)})
            last = r["iterations"][-1]
            tip = max(v["max_sampled_deflection_over_span"] for v in last["shape_validity"].values())
            prop = last.get("rejected_proposed_shape")
            tip_prop = max(v["max_sampled_deflection_over_span"] for v in prop.values()) if prop else None
            rows.append({"U_m_s": U, "EI_pectoral_Nm2": float(ei), "EI_pelvic_Nm2": float(ei * pel_ratio), "status": r["status"],
                         "valid": r["valid_for_declared_transfer"], "iterations": len(r["iterations"]),
                         "CL": last["CL_on_fixed_source_area"], "CL_rigid": rigid[U], "dCL_rel": last["CL_on_fixed_source_area"] / rigid[U] - 1,
                         "tip_over_span_last_accepted": tip, "tip_over_span_rejected_proposal": tip_prop,
                         "lift_N": float(np.dot(last["total_force_N"], [-math.sin(math.radians(4)), 0, math.cos(math.radians(4))])),
                         "range_m_protocol_descent": (r["flight"] or {}).get("main", {}).get("range_m")})
            print(json.dumps({k: rows[-1][k] for k in ("U_m_s", "EI_pectoral_Nm2", "status", "CL", "tip_over_span_last_accepted")}), flush=True)
    # critical EI per speed: smallest grid EI giving a converged valid state
    crit = {}
    for U in SPEEDS:
        ok = [r["EI_pectoral_Nm2"] for r in rows if r["U_m_s"] == U and r["valid"]]
        crit[U] = min(ok) if ok else None
    # analytic cross-check of tip/span with the rigid load as a uniform load: w/L = F L^2 / (8 EI)
    F20 = EIin["pectoral_L"]["reference_normal_force_N"]
    ana = {U: F20 * (U / 20) ** 2 * L_pec ** 2 / (8 * 0.1) for U in SPEEDS}   # EI at which uniform-load tip/span = 0.1
    checks.append({"name": "cross-check: grid critical EI within x4 of uniform-load estimate F L^2/(8*0.1) at every speed", "pass": all(crit[U] is not None and 0.25 <= crit[U] / ana[U] <= 4 for U in SPEEDS),
                   "detail": {"grid": crit, "uniform_load_estimate": ana}})
    # monotonic: tip deflection decreases with EI among valid rows at each speed
    mono = all(all(a["tip_over_span_last_accepted"] >= b["tip_over_span_last_accepted"] - 1e-12 for a, b in zip(rs, rs[1:]))
               for U in SPEEDS for rs in [[r for r in rows if r["U_m_s"] == U and r["valid"]]])
    checks.append({"name": "valid states: tip deflection non-increasing with EI", "pass": mono, "detail": None})
    # printed fin root stress at 8 and 20 m/s (rigid load as uniform: M = F L/2)
    stress = {U: (F20 * (U / 20) ** 2 * L_pec / 2) * zmax / I_print for U in SPEEDS}
    frac = {k: {U: (b[0] >= crit[U] if isinstance(b, list) else b >= crit[U]) if crit[U] else False for U in SPEEDS} for k, b in bands.items() if k != "committed_assay_design_values"}
    figs = fig(rows, bands, crit)
    C.manifest(RID, "Aeroelastic deflection over the sourced fin-ray stiffness range (two-way static VLM+beam)",
               [PROT, RAYS, R4M, "engineering/aeroelastic/run.py", "engineering/aeroelastic/model.py", "engineering/cfd3d/vlm.py", "engineering/organ_sims/r1_v3b_convergence.py"],
               {"rows": rows, "bands_EI_pectoral_Nm2": bands, "critical_EI_linear_domain_by_speed": crit, "uniform_load_estimate": ana,
                "printed_root_stress_Pa_uniform_load": stress, "UTS_Pa": UTS, "lattice_control": lat_ctrl,
                "band_lower_edge_inside_linear_domain": frac, "n_rays": {"pectoral": n_pec, "pelvic": n_pel}, "isometric_scale_I": scale_iso,
                "source": {"citation": "Alben, Madden & Lauder 2007, J R Soc Interface 4:243-256, doi 10.1098/rsif.2006.0181, Sec 3.4", "file": SRC},
                "wall_s": time.time() - t0},
               checks, {"see": "docs/organ-sims.md"}, seed=None, figures=figs,
               extra={"source_text_sha256": C.sha(SRC) if Path(SRC).exists() else None})
    print(json.dumps({"crit": crit, "bands": bands, "stress": stress, "lat": lat_ctrl}, indent=1, default=float))
    C.enforce(checks)


def fig(rows, bands, crit):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.3))
    for i, U in enumerate(SPEEDS):
        rs = sorted([r for r in rows if r["U_m_s"] == U], key=lambda r: r["EI_pectoral_Nm2"])
        v = [r for r in rs if r["valid"]]
        ax[0].plot([r["EI_pectoral_Nm2"] for r in v], [r["tip_over_span_last_accepted"] for r in v], "o-", color=f"C{i}", label=f"{U:g} m/s")
        x = [r for r in rs if not r["valid"]]
        ax[0].plot([r["EI_pectoral_Nm2"] for r in x], [0.1] * len(x), "x", color=f"C{i}")
        ax[1].plot([r["EI_pectoral_Nm2"] for r in v], [100 * r["dCL_rel"] for r in v], "o-", color=f"C{i}", label=f"{U:g} m/s")
    for a in ax:
        a.axvspan(*bands["sourced_bluegill_x_nrays"], color="0.5", alpha=0.25, label="Alben 2007 ray EI x 15 rays")
        a.axvspan(*bands["isometric_size_scaled"], color="C4", alpha=0.12, label="isometric size-scaled (scenario)")
        a.axvline(bands["printed_r4_root_section"], color="k", ls="--", label="printed r4 root section")
        a.axvline(bands["printed_r4_tip_section"], color="k", ls=":", label="printed r4 tip section")
        a.set_xscale("log"); a.set_xlabel("pectoral whole-fin EI, N m^2")
    ax[0].set_yscale("log"); ax[0].axhline(0.1, color="r", lw=0.8); ax[0].set_ylabel("max deflection / span (x = linear-beam domain exit)")
    ax[0].legend(fontsize=6); ax[0].set_title("two-way static aeroelastic (simulated)")
    ax[1].set_ylabel("CL change vs rigid, %"); ax[1].set_title("lift loss from bending (valid states only)")
    fig.tight_layout(); fp = C.OUT / RID / "stiffness.png"; (C.OUT / RID).mkdir(parents=True, exist_ok=True); fig.savefig(fp, dpi=110)
    return [f"artifacts/organ-sims/{RID}/stiffness.png"]


if __name__ == "__main__":
    main()
