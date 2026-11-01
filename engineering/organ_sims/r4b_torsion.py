"""R4b: add finite fin TORSION to R4's two-way static aeroelastic loop (argon review #1: the committed model is
torsion-rigid, while its own constraint torsion is ~29% of root bending).

    python -m engineering.organ_sims.r4b_torsion [workers]

Model: R4's loop (v3a fins, consistent-collocation VLM, constant-EI Hermite cantilever per fin, under-relaxation 0.5,
fixed point on CL and shape) plus a uniform-GJ torsion rod per fin about an elastic axis at chord fraction f_ea:
  torque per panel tau_i = F_n,i (w_ea - w_i)            (w downstream; force aft of the axis twists the leading edge DOWN)
  theta(s) = (1/GJ) sum_i tau_i min(s, s_i)                (clamped root, point torques at the bound-vortex stations)
  point (s, w) moves by theta(s) (w_ea - w) along the fin normal; normals tilt by theta toward +w.
Gates: R4's linear-beam domain (tip/span <= 0.1, slope <= 0.2 rad) plus |theta| <= 0.2 rad (small-angle twist).
Inputs: EI grid {printed r4 root 7.35e-3, 3.16e-3, 1.78e-3} N m^2 (the last two are R4 grid points near the isometric-upper
and sourced-x10 bands, so the GJ = inf arms must reproduce R4);
GJ/EI {0.03, 0.1, 0.3, 1, inf}; f_ea {0.05 (spar on the leading ray, assumed), 0.25, 0.40}; U {8, 12, 16, 20} m/s.
Printed-fin GJ estimate (open thin section, G = E/2.7 with nu 0.35 ASSUMED): recorded, ~0.3 EI.  Simulated only.
"""
import json, math, sys, time
import numpy as np
from engineering.cfd3d import vlm
from engineering.aeroelastic import model as AM, run as AR
from engineering.organ_sims import common as C
from engineering.organ_sims import r1_v3b_convergence as R1
from engineering.organ_sims import r4_aeroelastic_stiffness as R4

RID = "r4b-torsion"
EIS = (7.35e-3, 10 ** -2.5, 10 ** -2.75)   # printed root; R4 grid points nearest the isometric-upper and sourced-x10 bands
RATIOS = (0.03, 0.1, 0.3, 1.0, math.inf)
FEA = (0.05, 0.25, 0.40)
SPEEDS = (8.0, 12.0, 16.0, 20.0)
MESHES = ((24, 6), (48, 12))
RHO, ALPHA = 1.204, 4.0
import os
if os.environ.get("R4B_SMOKE"):          # pipeline smoke test only
    EIS, RATIOS, FEA, SPEEDS, MESHES = (10 ** -2.5,), (0.3, math.inf), (0.05,), (20.0,), ((24, 6),)


def setup(ns=24, nc=6):
    vlm.lattice = R1.lattice_consistent
    fins = AM.setup(ns, nc)
    for f in fins.values():
        lat, geo = f["lattice"], f["geometry"]
        mid = (lat["A"] + lat["B"]) / 2
        f["s_i"] = AM.span(f, mid)
        f["w_i"] = (mid - geo["O"]) @ geo["ew"]
        u_i = (mid - geo["O"]) @ geo["eu"]
        ch = [vlm.chord_at(geo["poly"], u) for u in u_i]
        f["le_i"] = np.array([c[0] for c in ch]); f["c_i"] = np.array([c[1] - c[0] for c in ch])
    return fins


def twist_lattice(fin, lat, theta_fn, f_ea):
    geo = fin["geometry"]; src = fin["lattice"]
    out = dict(lat)
    for key in ("A", "B", "C"):
        X = src[key]
        s = AM.span(fin, X); w = (X - geo["O"]) @ geo["ew"]; u = (X - geo["O"]) @ geo["eu"]
        ch = [vlm.chord_at(geo["poly"], float(np.clip(uu, geo["poly"][:, 0].min() + 1e-9, geo["poly"][:, 0].max() - 1e-9))) for uu in u]
        wea = np.array([c[0] + f_ea * (c[1] - c[0]) if c else ww for c, ww in zip(ch, w)])
        out[key] = lat[key] + (theta_fn(s) * (wea - w))[:, None] * geo["n_up"]
    th = theta_fn(AM.span(fin, src["C"]))
    N = lat["N"] + th[:, None] * geo["ew"]
    out["N"] = N / np.linalg.norm(N, axis=1)[:, None]
    return out


def arm(args):
    EI, ratio, f_ea, U, (ns, nc) = args
    fins = setup(ns, nc)
    P = AM.protocol()
    pel = P["parameters"]["EI_inputs"]["pelvic_L"]["EI_Nm2_by_compliance"]["0.2"] / P["parameters"]["EI_inputs"]["pectoral_L"]["EI_Nm2_by_compliance"]["0.2"]
    EIf = {n: EI * (pel if n.startswith("pelvic") else 1.0) for n in fins}
    GJf = {n: EIf[n] * ratio for n in fins}
    cur = {n: np.zeros(len(f["lattice"]["area"])) for n, f in fins.items()}
    tq = {n: np.zeros(len(f["lattice"]["area"])) for n, f in fins.items()}
    area = float(sum(f["source"]["area_flat_m2"] for f in fins.values()))
    ld = np.array([-math.sin(math.radians(ALPHA)), 0, math.cos(math.radians(ALPHA))])
    prev, status, hist = None, "unconverged: iteration budget", []
    theta_tip = {n: 0.0 for n in fins}
    for it in range(80):
        val = {n: AR.validity(f, cur[n], EIf[n]) for n, f in fins.items()}
        if not all(v["valid"] for v in val.values()):
            status = "model-domain exit: linear beam"; break
        thf = {}
        for n, f in fins.items():
            g = GJf[n]
            if math.isinf(g):
                thf[n] = lambda s: np.zeros_like(np.asarray(s, float))
            else:
                si, ti = f["s_i"], tq[n]
                thf[n] = (lambda si, ti, g: (lambda s: (ti[None, :] * np.minimum(np.asarray(s, float)[:, None], si[None, :])).sum(1) / g))(si, ti, g)
            theta_tip[n] = float(thf[n](np.array([f["length"]]))[0])
        if max(abs(v) for v in theta_tip.values()) > 0.2:
            status = "model-domain exit: twist > 0.2 rad"; break
        lats = {n: twist_lattice(f, AM.deform(f, cur[n], EIf[n]), thf[n], f_ea) for n, f in fins.items()}
        comb = vlm.combine(lats)
        _, unitF, _, _ = vlm.solve(comb, ALPHA)
        phys = unitF * RHO * U ** 2
        CL = float(phys.sum(0) @ ld / (0.5 * RHO * U ** 2 * area))
        off, new_b, new_t, res = 0, {}, {}, 0.0
        for n, f in fins.items():
            k = len(f["lattice"]["area"]); F = phys[off:off + k]; off += k
            nrm, _ = AM.transfer(f, lats[n], F)
            new_b[n] = nrm
            wea = f["le_i"] + f_ea * f["c_i"]
            new_t[n] = nrm * (wea - f["w_i"])
            res = max(res, float(np.max(np.abs(new_b[n] - cur[n]))) / max(float(np.max(np.abs(new_b[n]))), 1e-12))
        d = None if prev is None else abs(CL - prev)
        hist.append({"it": it, "CL": CL, "theta_tip_rad": dict(theta_tip)})
        if d is not None and d <= 1e-6 and res <= 1e-5:
            status = "converged"; break
        for n in fins:
            cur[n] = 0.5 * cur[n] + 0.5 * new_b[n]
            tq[n] = 0.5 * tq[n] + 0.5 * new_t[n]
        prev = CL
    tip = max(v["max_sampled_deflection_over_span"] for v in val.values())
    return {"mesh": [ns, nc], "EI_pectoral_Nm2": EI, "GJ_over_EI": None if math.isinf(ratio) else ratio, "f_ea": f_ea, "U_m_s": U, "status": status,
            "valid": status == "converged", "iterations": len(hist), "CL": hist[-1]["CL"] if hist else None,
            "theta_tip_pectoral_deg": math.degrees(theta_tip["pectoral_L"]), "theta_tip_pelvic_deg": math.degrees(theta_tip["pelvic_L"]),
            "tip_over_span": tip}


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    t0 = time.time()
    from concurrent.futures import ProcessPoolExecutor
    grid = [(EI, r, f, U, ms) for ms in MESHES for EI in EIS for r in RATIOS for f in (FEA if not math.isinf(r) else (FEA[0],)) for U in SPEEDS]
    rigid = [(1e3, math.inf, FEA[0], U, ms) for ms in MESHES for U in SPEEDS]
    with ProcessPoolExecutor(workers) as ex:
        rows = list(ex.map(arm, grid + rigid))
    rgm = {(tuple(r["mesh"]), r["U_m_s"]): r["CL"] for r in rows[len(grid):]}
    rg = {r["U_m_s"]: r["CL"] for r in rows[len(grid):] if tuple(r["mesh"]) == MESHES[0]}
    rows = rows[:len(grid)]
    for r in rows:
        c0 = rgm[(tuple(r["mesh"]), r["U_m_s"])]
        r["CL_rigid"] = c0; r["dCL_rel"] = None if r["CL"] is None or not r["valid"] else r["CL"] / c0 - 1
    checks = []
    # control: GJ = inf reproduces R4 bending-only CL at the same EI/U where R4 has that grid point (1e-5 abs)
    r4 = json.loads((C.ROOT / "artifacts/organ-sims/r4-aeroelastic-stiffness/manifest.json").read_text())["results"]["rows"]
    pairs = []
    for r in rows:
        if r["GJ_over_EI"] is None and r["valid"] and tuple(r["mesh"]) == (24, 6):
            m = [x for x in r4 if x["U_m_s"] == r["U_m_s"] and abs(x["EI_pectoral_Nm2"] / r["EI_pectoral_Nm2"] - 1) < 0.02 and x["valid"]]
            if m:
                pairs.append((r["U_m_s"], r["EI_pectoral_Nm2"], r["CL"], m[0]["CL"]))
    checks.append({"name": "control: rigid-torsion arms reproduce R4 bending-only CL where EI matches within 2% (|dCL| <= 2e-3, EI grids differ slightly)", "pass": bool(pairs) and all(abs(a - b) <= 2e-3 for _, _, a, b in pairs),
                   "detail": {"pairs": pairs, "note": "no pair -> recorded as vacuous" if not pairs else None}})
    checks.append({"name": "control: rigid (EI 1e3, GJ inf) CL equals R4's consistent-lattice rigid CL at 24x6 (1e-6)", "pass": all(abs(v - 0.2516508331140743) < 1e-6 for v in rg.values()), "detail": rg})
    mono = []
    for EI in EIS:
        for f in FEA:
            for U in SPEEDS:
                s = [r for r in rows if r["EI_pectoral_Nm2"] == EI and r["f_ea"] == f and r["U_m_s"] == U and r["valid"] and r["GJ_over_EI"] is not None and tuple(r["mesh"]) == MESHES[0]]
                s.sort(key=lambda r: r["GJ_over_EI"])
                mono.append(all(abs(a["theta_tip_pectoral_deg"]) >= abs(b["theta_tip_pectoral_deg"]) - 1e-9 for a, b in zip(s, s[1:])))
    checks.append({"name": "valid arms: tip twist magnitude non-increasing with GJ", "pass": all(mono), "detail": sum(mono)})
    # printed-fin GJ estimate
    M = json.loads((C.ROOT / "artifacts/glider/r4-daane-printfix/manifest.json").read_text())
    E = M["material"]["flexural_modulus_Pa"]; Gm = E / (2 * 1.35)
    mac = M["hand_neutral_point"]["pectoral_mac_mm"] * 1e-3
    J = mac * 0.5e-3 ** 3 / 3 + 0.229 * 2.0e-3 * 1.6e-3 ** 3 + 14 * 0.141 * 1.0e-3 * 0.8e-3 ** 3   # thin strip + rectangles (beta ~0.23, 0.14)
    EIp, _, _ = R4.printed_EI(E, mac, 14)
    printed = {"G_Pa_assumed_nu0.35": Gm, "J_m4": J, "GJ_Nm2": Gm * J, "EI_root_Nm2": EIp, "GJ_over_EI": Gm * J / EIp}
    # lattice sensitivity of the torsion effect (recorded): dCL_rel fine minus main for matching valid arms
    lat = []
    if len(MESHES) > 1:
        for r in rows:
            if tuple(r["mesh"]) == MESHES[0] and r["valid"]:
                q = [x for x in rows if tuple(x["mesh"]) == MESHES[1] and x["valid"] and all(x[k] == r[k] for k in ("EI_pectoral_Nm2", "GJ_over_EI", "f_ea", "U_m_s"))]
                if q:
                    lat.append(q[0]["dCL_rel"] - r["dCL_rel"])
    checks.append({"name": "recorded: lattice sensitivity of dCL_rel (48x12 minus 24x6), max abs", "pass": True, "detail": {"n": len(lat), "max_abs": max(map(abs, lat)) if lat else None}})
    figs = fig([r for r in rows if tuple(r["mesh"]) == MESHES[0]])
    C.manifest(RID, "Fin torsion added to the two-way static aeroelastic loop (VLM + bending + twist)",
               ["artifacts/aeroelastic/protocol.json", "artifacts/fish3d/fish3d-v3a-fan/panels.json", "artifacts/glider/r4-daane-printfix/manifest.json",
                "artifacts/organ-sims/r4-aeroelastic-stiffness/manifest.json"],
               {"rows": rows, "rigid_CL_by_speed": rg, "rigid_CL_by_mesh_speed": {f"{k[0][0]}x{k[0][1]}@{k[1]:g}": v for k, v in rgm.items()}, "printed_fin_torsion_estimate": printed, "wall_s": time.time() - t0, "workers": workers},
               checks, {"see": "docs/organ-sims.md"}, seed=None, figures=figs)
    print(json.dumps({"printed": printed, "n": len(rows)}, indent=1))
    C.enforce(checks)


def fig(rows):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, len(FEA), figsize=(5 * len(FEA), 4), sharey=True, squeeze=False)
    for a, f in zip(ax[0], FEA):
        for i, EI in enumerate(EIS):
            for U, ls in ((8.0, ":"), (20.0, "-")):
                s = sorted([r for r in rows if r["EI_pectoral_Nm2"] == EI and r["f_ea"] == f and r["U_m_s"] == U and r["valid"] and r["GJ_over_EI"]], key=lambda r: r["GJ_over_EI"])
                if s:
                    a.plot([r["GJ_over_EI"] for r in s], [100 * r["dCL_rel"] for r in s], "o" + ls, color=f"C{i}", label=f"EI {EI:.1e}, {U:g} m/s")
        a.set_xscale("log"); a.set_xlabel("GJ / EI"); a.set_title(f"elastic axis at {f:.2f} chord (simulated)")
    ax[0][0].set_ylabel("CL change vs rigid, % (valid states)"); ax[0][0].legend(fontsize=6)
    fig.tight_layout(); fp = C.OUT / RID / "torsion.png"; (C.OUT / RID).mkdir(parents=True, exist_ok=True); fig.savefig(fp, dpi=110)
    return [f"artifacts/organ-sims/{RID}/torsion.png"]


if __name__ == "__main__":
    main()
