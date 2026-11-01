"""R3: underwater drag of the same bodies (fish3d N1/v3a/v3b/v3c and the printed r4 glider, plus the R2 best-feasible fin
variant), fins spread vs pectorals folded, at assumed pre-take-off swimming speeds.

    python -m engineering.organ_sims.r3_underwater_drag

Method (component drag build-up; all simulated, none observed):
  geometry  measured from the committed component STLs (fish3d) or the r4 flight model (glider): wetted areas, body
            length, max width/depth, fin one-side areas and mean chords.
  friction  each component at its OWN Reynolds number; three skin-friction laws give a band, none is claimed:
            laminar Blasius 1.328 Re^-1/2 (lower), Prandtl-Schlichting transitional 0.455 (log Re)^-2.58 - 1700/Re
            (clipped to >= laminar), ITTC-1957 0.075 (log Re - 2)^-2 (fully turbulent, upper). All recalled, standard.
  form      body: Hoerner 1 + 1.5 (d/l)^1.5 + 7 (d/l)^3, d = sqrt(width x depth); fins: 1 + 2 t/c + 60 (t/c)^4.
  folded    pectorals pressed to the body: one face shielded, the other face wetted with form factor 1.
  NOT in the model: wave drag near the surface (taxiing; can be several times the deep-water value), undulatory swimming
            (active drag differs from rigid drag), separation behind the blunt printed tail, scales, appendage
            interference. Deep-water rigid-body drag only.
  cross-check: the same build-up at Re_L = 1000 for N1 against the committed WaterLily GPU runs of N1 (L128/L192 Re 1000,
            Cd on L_ref^2). Those runs carry 'C1 sphere reference gate FAILED' and sub-grid fins, so this is an
            order-of-magnitude consistency check of the build-up, not a validation of either.
"""
import json, math
import numpy as np
from engineering.organ_sims import common as C

RID = "r3-underwater-drag"
RHO_W, NU_W = 998.2, 1.004e-6           # water 20 C (recalled; same values as engineering/cfd3d/vlm.py MEDIA)
SPEEDS = [1.0, 2.0, 5.0, 10.0]          # m/s; 5-10 'assumed, unsourced' in vlm.py SPEEDS; 1-2 cruising, assumed
FISH = {"N1": "fish3d-N1-cypselurus-baseline", "v3a": "fish3d-v3a-fan", "v3b": "fish3d-v3b-glide-pose", "v3c": "fish3d-v3c-daane-length"}
FINS = ("pectoral_L", "pectoral_R", "pelvic_L", "pelvic_R", "dorsal", "anal", "caudal")
FM = "artifacts/glider/r4-daane-printfix/flight_model.json"
CFD = "artifacts/cfd3d/summary-gpu-v1.json"
CFDCASE = "artifacts/cfd3d/gpu-v1/gpu_fish_L192_Re1000/case.json"
T_OVER_C_FISH = 0.6e-3                  # fish3d fin ray thickness 0.60 mm (vlm.py docstring); membrane 0.10 mm
T_GLIDER_FIN = 0.5e-3 + 0.7e-3          # r4 membrane 0.5 mm + ridge height, ASSUMED 0.7 mm


def read_stl(path):
    b = (C.ROOT / path).read_bytes()
    if b[:5] == b"solid" and b"facet" in b[:400]:
        v = [list(map(float, l.split()[1:4])) for l in b.decode().splitlines() if l.strip().startswith("vertex")]
        return np.array(v).reshape(-1, 3, 3)
    n = int(np.frombuffer(b[80:84], "<u4")[0])
    rec = np.frombuffer(b[84:84 + 50 * n], dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]))
    return rec["v"].astype(float)


def tri_area(T):
    return 0.5 * np.linalg.norm(np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]), axis=1).sum()


def cf(Re, law):
    lam = 1.328 / math.sqrt(Re)
    if law == "laminar":
        return lam
    if law == "transitional":
        return max(0.455 / math.log10(Re) ** 2.58 - 1700.0 / Re, lam)
    if law == "turbulent":
        return 0.075 / (math.log10(Re) - 2.0) ** 2
    raise ValueError(law)


def ff_body(d, l):
    r = d / l
    return 1 + 1.5 * r ** 1.5 + 7 * r ** 3


def ff_fin(tc):
    return 1 + 2 * tc + 60 * tc ** 4


def fish_geometry(key):
    d = f"artifacts/fish3d/{FISH[key]}/components"
    T = read_stl(f"{d}/body.stl")
    P = T.reshape(-1, 3)
    ext = P.max(0) - P.min(0)
    g = {"body": {"S_wet_m2": tri_area(T), "length_m": float(ext[0]), "width_m": float(ext[1]), "depth_m": float(ext[2]),
                  "stl": f"{d}/body.stl"}, "fins": {}}
    for f in FINS:
        Tf = read_stl(f"{d}/{f}.stl")
        Pf = Tf.reshape(-1, 3)
        S1 = tri_area(Tf) / 2                                      # thin closed shell: one face ~ half the area
        chord = float(np.ptp(Pf[:, 0]))                            # streamwise extent
        g["fins"][f] = {"S_one_side_m2": S1, "streamwise_extent_m": chord, "mean_chord_m": min(chord, S1 / max(np.ptp(Pf[:, 1:], axis=0).max(), 1e-9)),
                        "stl": f"{d}/{f}.stl"}
    return g


def glider_geometry(pec_scale=1.0):
    H = json.loads((C.ROOT / FM).read_text())
    M = json.loads((C.ROOT / "artifacts/glider/r4-daane-printfix/manifest.json").read_text())["hand_neutral_point"]
    b = H["body"]
    L = 0.15881524292060323          # standard length used by R2 (candidate biology); printed body length measured below
    Tb = read_stl("artifacts/glider/r4-daane-printfix/stl/body.stl")
    Lb = float(np.ptp(Tb.reshape(-1, 3)[:, 0])) * 1e-3          # print STLs are in millimetres (fish3d components in metres)
    mac = M["pectoral_mac_mm"] * 1e-3
    S_pec1 = M["pectoral"]["area_mm2"] * 1e-6 * pec_scale
    S_pel1 = M["pelvic"]["area_mm2"] * 1e-6
    pel_c = S_pel1 / (M["pelvic"].get("span_in_plane_mm", 30.0) * 1e-3)
    g = {"body": {"S_wet_m2": b["wetted_area_m2"], "length_m": Lb, "width_m": b["max_width_m"], "depth_m": b["max_depth_m"],
                  "stl": "artifacts/glider/r4-daane-printfix/stl/body.stl"},
         "fins": {"pectoral_L": {"S_one_side_m2": S_pec1, "mean_chord_m": mac * math.sqrt(pec_scale)},
                  "pectoral_R": {"S_one_side_m2": S_pec1, "mean_chord_m": mac * math.sqrt(pec_scale)},
                  "pelvic_L": {"S_one_side_m2": S_pel1, "mean_chord_m": pel_c}, "pelvic_R": {"S_one_side_m2": S_pel1, "mean_chord_m": pel_c}}}
    return g


def drag(g, U, law, folded=False, nu=NU_W, t_fin=T_OVER_C_FISH):
    """Returns (sum Cf*FF*S [m2], per-component dict).  D = 0.5 rho U^2 x (sum)."""
    b = g["body"]
    comp = {}
    Re_b = U * b["length_m"] / nu
    comp["body"] = cf(Re_b, law) * ff_body(math.sqrt(b["width_m"] * b["depth_m"]), b["length_m"]) * b["S_wet_m2"]
    for f, fg in g["fins"].items():
        c = fg["mean_chord_m"]
        Re = max(U * c / nu, 10.0)
        if folded and f.startswith("pectoral"):
            comp[f] = cf(Re, law) * 1.0 * fg["S_one_side_m2"]
        else:
            comp[f] = cf(Re, law) * ff_fin(t_fin / c) * 2 * fg["S_one_side_m2"]
    return sum(comp.values()), comp


def main():
    checks, rows = [], []
    geos = {k: fish_geometry(k) for k in FISH}
    H = json.loads((C.ROOT / FM).read_text())
    vol = H["body"]["enclosed_volume_m3"]
    geos["glider_r4"] = glider_geometry(1.0)
    geos["glider_r2best_1.8xpec"] = glider_geometry(1.8)
    # --- controls --------------------------------------------------------------------------------------------
    # (1) flat plate: laminar Blasius at Re 1e5 is 0.0042 (textbook value 1.328/316.2)
    checks.append({"name": "control: Blasius Cf(1e5) = 0.00420", "pass": abs(cf(1e5, "laminar") - 0.0041995) < 1e-6, "detail": cf(1e5, "laminar")})
    # (2) ITTC-57 at Re 1e7 = 0.00301 (tabulated)
    checks.append({"name": "control: ITTC-57 Cf(1e7) = 0.00301 +- 1%", "pass": abs(cf(1e7, "turbulent") / 0.0030125 - 1) < 0.01, "detail": cf(1e7, "turbulent")})
    # (3) STL reader: a unit cube area would be 6; use the committed glider body STL area vs flight_model wetted (outer
    #     loft only) -> shell STL must be LARGER (inner surfaces), never smaller
    Ash = tri_area(read_stl("artifacts/glider/r4-daane-printfix/stl/body.stl"))
    checks.append({"name": "control: glider shell STL area >= flight_model outer wetted area (inner faces present)", "pass": Ash >= H["body"]["wetted_area_m2"], "detail": {"stl_m2": Ash, "wetted_m2": H["body"]["wetted_area_m2"]}})
    # (4) symmetry: L and R fin areas equal within 1% on every fish
    for k in FISH:
        a, b_ = geos[k]["fins"]["pectoral_L"]["S_one_side_m2"], geos[k]["fins"]["pectoral_R"]["S_one_side_m2"]
        checks.append({"name": f"control: {k} pectoral L/R area within 1%", "pass": abs(a / b_ - 1) < 0.01, "detail": [a, b_]})
    # (5) units guard: every body length is 0.05-0.5 m (an earlier draft read the mm print STL as metres: 191 m)
    checks.append({"name": "control: every body length in 0.05-0.5 m (STL unit guard)", "pass": all(0.05 <= g["body"]["length_m"] <= 0.5 for g in geos.values()),
                   "detail": {k: g["body"]["length_m"] for k, g in geos.items()}})
    # --- cross-check against WaterLily N1 Re 1000 ------------------------------------------------------------
    cs = json.loads((C.ROOT / CFDCASE).read_text())
    Lref = cs["nondim"]["L_ref_m"]
    cfd = json.loads((C.ROOT / CFD).read_text())["cases"]
    nu_nd = 1.0 * Lref / 1000.0                       # U = 1, Re_L = 1000 -> nu in m^2/s with L in m
    xs = {law: drag(geos["N1"], 1.0, law, nu=nu_nd)[0] / Lref ** 2 for law in ("laminar",)}
    cross = {"buildup_laminar_Cd_Lref2": xs["laminar"], "cfd_L192": cfd["gpu_fish_L192_Re1000"]["coefficients"]["Cd_total"],
             "cfd_L128": cfd["gpu_fish_L128_Re1000"]["coefficients"]["Cd_total"], "cfd_pressure_part_L192": cfd["gpu_fish_L192_Re1000"]["coefficients"]["Cd_pressure"]}
    cross["ratio_cfd_over_buildup"] = cross["cfd_L192"] / cross["buildup_laminar_Cd_Lref2"]
    # NOTE (argon review #6): Re_L 1000 is ~1600x below the 10 m/s water case and the CFD's sphere gate failed: this
    # comparison has no validation value at the target Reynolds number; it only shows the build-up is not wildly off
    # in the one regime where a 3-D solution of the same family of bodies exists.
    checks.append({"name": "consistency only (no validation value at target Re): CFD/build-up at Re_L 1000 within 0.33-3", "pass": 1 / 3 <= cross["ratio_cfd_over_buildup"] <= 3, "detail": cross})
    # --- sweep -----------------------------------------------------------------------------------------------
    for k, g in geos.items():
        tf = T_GLIDER_FIN if k.startswith("glider") else T_OVER_C_FISH
        for U in SPEEDS:
            for folded in (False, True):
                r = {"body_id": k, "U_m_s": U, "pectorals": "folded" if folded else "spread",
                     "Re_body": U * g["body"]["length_m"] / NU_W}
                for law in ("laminar", "transitional", "turbulent"):
                    s, comp = drag(g, U, law, folded, t_fin=tf)
                    D = 0.5 * RHO_W * U * U * s
                    r[f"D_N_{law}"] = D
                    r[f"P_W_{law}"] = D * U
                    r[f"CdS_m2_{law}"] = s
                    r[f"fin_share_{law}"] = 1 - comp["body"] / s
                rows.append(r)
    # sanity bounds
    checks.append({"name": "every drag finite and laminar <= turbulent", "pass": all(math.isfinite(r["D_N_turbulent"]) and r["D_N_laminar"] <= r["D_N_turbulent"] * 1.0001 for r in rows), "detail": len(rows)})
    checks.append({"name": "folding pectorals never increases drag", "pass": all(
        next(q for q in rows if q["body_id"] == r["body_id"] and q["U_m_s"] == r["U_m_s"] and q["pectorals"] == "folded")["D_N_transitional"] <= r["D_N_transitional"]
        for r in rows if r["pectorals"] == "spread"), "detail": None})
    # volume-based coefficient for the glider body (CD_V = D / (q V^2/3)), bounded to a plausible streamlined-body range
    gl = [r for r in rows if r["body_id"] == "glider_r4" and r["pectorals"] == "folded"]
    for r in gl:
        r["CD_V_transitional"] = r["CdS_m2_transitional"] / vol ** (2 / 3)
    checks.append({"name": "bound: glider CD_V (folded, transitional) in 0.005-0.2 at all speeds", "pass": all(0.005 <= r["CD_V_transitional"] <= 0.2 for r in gl), "detail": [r["CD_V_transitional"] for r in gl]})
    # summary
    summ = {}
    for k in geos:
        for U in (5.0, 10.0):
            sp = next(r for r in rows if r["body_id"] == k and r["U_m_s"] == U and r["pectorals"] == "spread")
            fo = next(r for r in rows if r["body_id"] == k and r["U_m_s"] == U and r["pectorals"] == "folded")
            summ[f"{k}@{U:g}"] = {"D_spread_N_band": [sp["D_N_laminar"], sp["D_N_transitional"], sp["D_N_turbulent"]],
                                  "D_folded_N_band": [fo["D_N_laminar"], fo["D_N_transitional"], fo["D_N_turbulent"]],
                                  "fold_saving_transitional": 1 - fo["D_N_transitional"] / sp["D_N_transitional"],
                                  "fin_share_spread_transitional": sp["fin_share_transitional"], "P_W_spread_transitional": sp["P_W_transitional"]}
    big = summ["glider_r2best_1.8xpec@10"]["D_spread_N_band"][1] / summ["glider_r4@10"]["D_spread_N_band"][1] - 1
    bigf = summ["glider_r2best_1.8xpec@10"]["D_folded_N_band"][1] / summ["glider_r4@10"]["D_folded_N_band"][1] - 1
    # printed spread-fin strength under water (argon review #6): pectoral at a small misalignment alpha_mis, normal force
    # q S CLa alpha at 0.424 span (elliptic-load centroid), root section and UTS from the r4 manifest (R4 routine)
    from engineering.organ_sims.r4_aeroelastic_stiffness import printed_EI
    Mf = json.loads((C.ROOT / "artifacts/glider/r4-daane-printfix/manifest.json").read_text())
    E, UTS = Mf["material"]["flexural_modulus_Pa"], Mf["material"]["ultimate_tensile_strength_Pa"]
    hnp = Mf["hand_neutral_point"]
    _, I_r, zmax = printed_EI(E, hnp["pectoral_mac_mm"] * 1e-3, 14)
    S_p = hnp["pectoral"]["area_mm2"] * 1e-6; span_p = hnp["pectoral"]["span_in_plane_mm"] * 1e-3
    ARp = (2 * span_p) ** 2 / (2 * S_p); cla = 2 * math.pi * ARp / (2 + math.sqrt(4 + ARp ** 2))
    strength = {}
    for a_mis in (1.0, 2.0, 5.0):
        sig = lambda U: 0.5 * RHO_W * U * U * S_p * cla * math.radians(a_mis) * 0.424 * span_p * zmax / I_r
        U_half = math.sqrt((UTS / 2) / sig(1.0))
        strength[f"alpha_mis_{a_mis:g}deg"] = {"root_stress_Pa_at": {f"{U:g}": sig(U) for U in SPEEDS}, "U_max_for_half_UTS_m_s": U_half}
    checks.append({"name": "recorded: printed spread pectoral root stress under water vs UTS (failing speeds are a finding)", "pass": True, "detail": strength})
    figs = fig(rows)
    inputs = [FM, CFD, CFDCASE, "artifacts/glider/r4-daane-printfix/manifest.json", "artifacts/glider/r4-daane-printfix/stl/body.stl"] + \
             [geos[k]["body"]["stl"] for k in FISH] + [geos[k]["fins"][f]["stl"] for k in FISH for f in FINS]
    C.manifest(RID, "Underwater rigid-body drag build-up: fish3d variants and printed glider, fins spread vs folded",
               inputs, {"geometry": {k: {"body": {a: b for a, b in g["body"].items() if a != "stl"},
                                         "fins": {f: {a: b for a, b in fg.items() if a != "stl"} for f, fg in g["fins"].items()}} for k, g in geos.items()},
                        "rows": rows, "summary": summ, "cross_check_re1000": cross,
                        "r2_best_fin_penalty_at_10ms_transitional": {"spread": big, "folded": bigf},
                        "printed_fin_underwater_strength": strength,
                        "assumptions": {"rho_water": RHO_W, "nu_water": NU_W, "speeds": SPEEDS, "fin_t_fish_m": T_OVER_C_FISH, "fin_t_glider_m": T_GLIDER_FIN,
                                        "excluded": ["wave drag near surface", "undulatory swimming", "base separation", "interference"]}},
               checks, {"see": "docs/organ-sims.md"}, seed=None, figures=figs)
    print(json.dumps(summ, indent=1, default=float)); print("cross", cross); print("r2best penalty", big, bigf)
    C.enforce(checks)


def fig(rows):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    ids = sorted({r["body_id"] for r in rows})
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
    for i, k in enumerate(ids):
        for j, (p, ls) in enumerate((("spread", "-"), ("folded", "--"))):
            rs = sorted([r for r in rows if r["body_id"] == k and r["pectorals"] == p], key=lambda r: r["U_m_s"])
            U = [r["U_m_s"] for r in rs]
            ax[0].plot(U, [r["D_N_transitional"] for r in rs], ls, color=f"C{i}", label=f"{k} {p}")
            if p == "spread":
                ax[0].fill_between(U, [r["D_N_laminar"] for r in rs], [r["D_N_turbulent"] for r in rs], color=f"C{i}", alpha=0.12)
    ax[0].set_xscale("log"); ax[0].set_yscale("log"); ax[0].set_xlabel("speed in water, m/s"); ax[0].set_ylabel("rigid drag, N (band: laminar..turbulent)")
    ax[0].legend(fontsize=6); ax[0].set_title("underwater drag build-up (simulated, deep water, rigid)")
    r10 = [r for r in rows if r["U_m_s"] == 10.0]
    x = np.arange(len(ids))
    ax[1].bar(x - 0.2, [next(r["D_N_transitional"] for r in r10 if r["body_id"] == k and r["pectorals"] == "spread") for k in ids], 0.4, label="spread")
    ax[1].bar(x + 0.2, [next(r["D_N_transitional"] for r in r10 if r["body_id"] == k and r["pectorals"] == "folded") for k in ids], 0.4, label="folded")
    ax[1].set_xticks(x); ax[1].set_xticklabels(ids, rotation=20, fontsize=7); ax[1].set_ylabel("drag at 10 m/s, N (transitional law)"); ax[1].legend()
    fig.tight_layout(); fp = C.OUT / RID / "drag.png"; (C.OUT / RID).mkdir(parents=True, exist_ok=True); fig.savefig(fp, dpi=110)
    return [f"artifacts/organ-sims/{RID}/drag.png"]


if __name__ == "__main__":
    main()
