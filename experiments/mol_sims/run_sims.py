"""Molecular/cell-scale simulations for the flying-fish project (claude-mol, 2026-11-01).

Deterministic ODE runs of PUBLISHED BioModels SBML with libRoadRunner (cvode, fixed
tolerances), plus a structure-confidence analysis of the OpenFold2 predictions.
No stochastic element, so no seed: the receipt records seed=null and why.
Everything here is SIMULATED or COMPUTED; none of it is observed and none is validated.

Usage: python run_sims.py {s1|s2|s3|s4|all}   (outputs under results/mol-sims/claude-20261101/)
"""
import hashlib, json, math, sys, time
from pathlib import Path

import numpy as np
import roadrunner

ROOT = Path(__file__).resolve().parents[2]
BM = ROOT / "results/bioservices/claude-20261101/biomodels"
OUT = ROOT / "results/mol-sims/claude-20261101"
RTOL, ATOL, T_END = 1e-10, 1e-12, 4000.0


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(model):
    r = roadrunner.RoadRunner(str(BM / f"{model}.xml"))
    r.integrator.relative_tolerance = RTOL
    r.integrator.absolute_tolerance = ATOL
    return r


def settle(r, ids, t_end=T_END):
    """Integrate to t_end; return final values and max |dy/dt| as a steady-state check."""
    r.simulate(0, t_end, 2)
    vals = {i: r.getValue(i) for i in ids}
    resid = float(np.max(np.abs(r.getRatesOfChange())))
    return vals, resid


def write(name, obj):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    p.write_text(json.dumps(obj, indent=1, sort_keys=True))
    return p


def receipt(sim, inputs, outputs, extra):
    return {
        "sim": sim, "command": f".venv-mol/bin/python experiments/mol_sims/run_sims.py {sim}",
        "exit_code": 0, "roadrunner": roadrunner.__version__, "integrator": "cvode",
        "rtol": RTOL, "atol": ATOL,
        "seed": None, "seed_note": "deterministic ODE integration; no random numbers used",
        "input_sha256": {k: sha(v) for k, v in inputs.items()},
        "output_sha256": {k: sha(v) for k, v in outputs.items()},
        "evidence_kind": "simulated",
        "scope": "SIMULATED, not observed. Published-model dynamics, not fit to any fish data; no biological validation.",
        **extra,
    }


def s1():
    """BIOMD0000000275 (Goldbeter, Gonze, Pourquie 2007): RA/FGF mutual-inhibition switch along PSM position x."""
    xs = np.round(np.arange(0.0, 50.01, 1.0), 3)
    perts = {
        "baseline": {},
        "fgf_loss_ks3x0": {"ks3": 0.0},
        "fgf_half_ks3x0.5": {"ks3": 0.5},
        "fgf_over_ks3x2": {"ks3": 2.0},
        "fgf_over_ks3x4": {"ks3": 4.0},
        "cyp26_loss_V0=Vsc=0": {"V0": 0.0, "Vsc": 0.0},
        "ra_synth_x0.5": {"RALDH2_0": 3.55},
        "ra_synth_x2": {"RALDH2_0": 14.2},
    }
    start = {"F_high": {"RA": 0.1, "F": 1.0}, "F_low": {"RA": 5.0, "F": 0.01}}
    res = {}
    for pn, ov in perts.items():
        rows = []
        for x in xs:
            row = {"x": float(x)}
            for sn, ic in start.items():
                r = load("BIOMD0000000275")
                for k, v in ov.items():
                    r[f"init({k})"] = v  # init(): assignment rules read initial values, a plain set is ignored
                r["init(x)"] = float(x)
                for k, v in ic.items():
                    r[f"init([{k}])"] = v
                vals, resid = settle(r, ["F", "RA"])
                row[sn] = {"F": vals["F"], "RA": vals["RA"], "max_abs_rate": resid}
            hi, lo = row["F_high"]["F"], row["F_low"]["F"]
            row["bistable"] = bool(abs(hi - lo) > 0.05 * max(hi, lo, 1e-9))
            rows.append(row)
        bi = [q["x"] for q in rows if q["bistable"]]
        fh = np.array([q["F_high"]["F"] for q in rows])
        fl = np.array([q["F_low"]["F"] for q in rows])

        def cross(a):
            half = (a.max() + a.min()) / 2
            return [float(xs[i]) for i in np.where(np.diff(np.sign(a - half)))[0]]
        res[pn] = {"overrides": ov, "bistable_x_range": [min(bi), max(bi)] if bi else None,
                   "n_bistable_points": len(bi),
                   "F_high_branch_range": [float(fh.min()), float(fh.max())],
                   "F_low_branch_range": [float(fl.min()), float(fl.max())],
                   "half_max_crossing_x_F_high_branch": cross(fh),
                   "half_max_crossing_x_F_low_branch": cross(fl),
                   "max_residual_rate_all_runs": max(max(q["F_high"]["max_abs_rate"], q["F_low"]["max_abs_rate"]) for q in rows),
                   "rows": rows}
        print(pn, res[pn]["bistable_x_range"], res[pn]["half_max_crossing_x_F_high_branch"], res[pn]["half_max_crossing_x_F_low_branch"], res[pn]["max_residual_rate_all_runs"], flush=True)
    p = write("s1_ra_fgf_switch_perturbations.json", {"model": "BIOMD0000000275", "x_units": "model position, L=50 (PSM length, model units); F in model units", "perturbations": res})
    return p, {"sbml": BM / "BIOMD0000000275.xml"}


def s2():
    """BIOMD0000000395 (Sivakumar 2011, Drosophila Hedgehog): dose-response and perturbations; output target gene s75."""
    ids = ["s75", "s70"]

    def run(ov):
        r = load("BIOMD0000000395")
        for k, v in ov.items():
            r[f"init([{k}])"] = v
        return settle(r, ids, 2000.0)
    out = {"dose_response": [], "perturbations": {}}
    for d in [0.0] + list(np.logspace(-7, 2, 37)):
        v, rs = run({"s7": float(d)})
        out["dose_response"].append({"Hh_s7": float(d), "target_s75": v["s75"], "Ci_s70": v["s70"], "max_abs_rate": rs})
    out["ptc_titration_at_Hh5"] = []
    for pv in [0.0] + list(np.logspace(-7, 1, 33)):
        v, rs = run({"s1": float(pv)})
        out["ptc_titration_at_Hh5"].append({"Ptc_s1": float(pv), "target_s75": v["s75"], "max_abs_rate": rs})
    pert = {"baseline": {}, "ptc_loss_s1=0": {"s1": 0.0}, "ptc_half": {"s1": 2.5}, "ptc_over_x2": {"s1": 10.0},
            "smo_loss_s148=0": {"s148": 0.0}, "smo_over_x2": {"s148": 6.0},
            "sufu_complex_loss_s128=0": {"s128": 0.0}, "sufu_over_x2": {"s128": 5.0}, "hh_loss_s7=0": {"s7": 0.0}}
    for n, ov in pert.items():
        v, rs = run(ov)
        out["perturbations"][n] = {"overrides": ov, "target_s75": v["s75"], "Ci_s70": v["s70"], "max_abs_rate": rs}
        print(n, v["s75"], rs, flush=True)
    out["species_note"] = {"s7": "Hedgehog", "s1": "Patched", "s148": "smoothened", "s128": "Ci-repressor/Su(fu) complex",
                           "s75": "Hedgehog target gene",
                           "organism": "Drosophila model; zebrafish shha/ptch/smo orthology is by name only and is not mapped"}
    p = write("s2_hedgehog_dose_response_perturbations.json", {"model": "BIOMD0000000395", **out})
    return p, {"sbml": BM / "BIOMD0000000395.xml"}


def s2b():
    """Review fix for s2: the s2 perturbations ran at the model's default Hh (s7=5), which saturates the target
    (dose-response plateau from ~5e-3), so Ptc/Smo/Sufu changes could not show. Re-run every perturbation at the
    interpolated EC50 and EC10/EC90 Hh doses taken from the s2 dose-response (log-linear interpolation)."""
    s2p = OUT / "s2_hedgehog_dose_response_perturbations.json"
    dr = json.loads(s2p.read_text())["dose_response"]
    d = np.array([q["Hh_s7"] for q in dr[1:]]); y = np.array([q["target_s75"] for q in dr[1:]])
    lo, hi = dr[0]["target_s75"], y.max()

    def ec(frac):
        tgt = lo + frac * (hi - lo)
        i = int(np.where(y >= tgt)[0][0])
        return float(10 ** np.interp(tgt, [y[i - 1], y[i]], [np.log10(d[i - 1]), np.log10(d[i])]))
    doses = {"EC10": ec(0.1), "EC50": ec(0.5), "EC90": ec(0.9)}
    pert = {"baseline": {}, "ptc_loss_s1=0": {"s1": 0.0}, "ptc_half": {"s1": 2.5}, "ptc_over_x2": {"s1": 10.0},
            "smo_loss_s148=0": {"s148": 0.0}, "smo_half": {"s148": 1.5}, "smo_over_x2": {"s148": 6.0},
            "sufu_complex_loss_s128=0": {"s128": 0.0}, "sufu_over_x2": {"s128": 5.0}}
    out = {"doses_s7": doses, "target_range": [lo, float(hi)], "perturbations": {}}
    for dn, dv in doses.items():
        out["perturbations"][dn] = {}
        for n, ov in pert.items():
            r = load("BIOMD0000000395")
            r["init([s7])"] = dv
            for k, v in ov.items():
                r[f"init([{k}])"] = v
            v, rs = settle(r, ["s75", "s70"], 2000.0)
            out["perturbations"][dn][n] = {"overrides": ov, "target_s75": v["s75"], "Ci_s70": v["s70"], "max_abs_rate": rs,
                                           "fraction_of_dynamic_range": (v["s75"] - lo) / (hi - lo)}
            print(dn, n, round(v["s75"], 4), "%.1e" % rs, flush=True)
    p = write("s2b_hedgehog_perturbations_at_ec.json", {"model": "BIOMD0000000395", **out})
    return p, {"sbml": BM / "BIOMD0000000395.xml", "s2_result": s2p}


def s3():
    """Local log-sensitivity (+-10 %, central) of outputs to every nonzero parameter and initial amount."""
    out = {}
    for model, outs, t, skip in [("BIOMD0000000275", ["F", "RA"], 4000.0, {"vs1", "rho", "alpha1", "alpha2", "RALDH2_0_unused"}),
                                 ("BIOMD0000000395", ["s75"], 2000.0, set())]:
        r0 = load(model)
        names = [f"init({p})" for p in r0.model.getGlobalParameterIds() if p not in skip and r0.getValue(p) != 0.0]
        names += [f"init([{s}])" for s in r0.model.getFloatingSpeciesIds() if r0.getValue(f"init([{s}])") > 0]
        if model == "BIOMD0000000275":
            names = [n for n in names if n not in ("init([M_F])",)]
        base, _ = settle(load(model), outs, t)
        sens = {}
        for p in names:
            vals = {}
            for sign in (+1, -1):
                r = load(model)
                r[p] = r[p] * (1 + 0.1 * sign)
                vals[sign], _ = settle(r, outs, t)
            sens[p] = {}
            for o in outs:
                a, b = vals[+1][o], vals[-1][o]
                sens[p][o] = (math.log(a / b) / math.log(1.1 / 0.9)) if a > 0 and b > 0 else None
        out[model] = {"baseline": base, "n_parameters": len(names), "log_sensitivity": sens,
                      "top_by_abs": {o: sorted(((p, s[o]) for p, s in sens.items() if s[o] is not None), key=lambda z: -abs(z[1]))[:8] for o in outs}}
        print(model, {o: [(p, round(v, 3)) for p, v in out[model]["top_by_abs"][o][:4]] for o in outs}, flush=True)
    p = write("s3_local_sensitivity.json", out)
    return p, {"sbml_275": BM / "BIOMD0000000275.xml", "sbml_395": BM / "BIOMD0000000395.xml"}


def s4():
    """Per-residue pLDDT (PDB B-factor column) of the four OpenFold2 monomers vs UniProt feature ranges."""
    base = ROOT / "results/bioservices/claude-20261101"
    acc = {"fgf10a": "Q8AY90", "hoxd13a": "Q90472", "shha": "Q92008", "kcnk5b": "Q6PFU3"}
    out, ins = {}, {}
    for g, a in acc.items():
        pdb = base / f"openfold2/{g}_{a}_rank1.pdb"
        ins[g] = pdb
        pl = np.array([float(l[60:66]) for l in pdb.read_text().splitlines() if l.startswith("ATOM") and l[12:16].strip() == "CA"])
        uni = json.loads((base / f"uniprot/{g}.json").read_text())
        ent = next((e for e in uni["results"] if e["primaryAccession"] == a), None)
        feats = []
        if ent:
            ins[g + "_uniprot"] = base / f"uniprot/{g}.json"
            for f in ent.get("features", []):
                if f["type"] in ("Domain", "DNA binding", "Region", "Signal", "Transmembrane", "Propeptide", "Motif", "Intramembrane", "Chain"):
                    s, e = f["location"]["start"]["value"], f["location"]["end"]["value"]
                    if s and e:
                        seg = pl[s - 1:e]
                        feats.append({"type": f["type"], "desc": f.get("description", ""), "start": s, "end": e,
                                      "mean_plddt": float(seg.mean()), "frac_ge70": float((seg >= 70).mean())})

        def longest(th):
            best = cur = 0
            for v in pl:
                cur = cur + 1 if v >= th else 0
                best = max(best, cur)
            return best
        out[g] = {"accession": a, "n": int(len(pl)), "mean_plddt": float(pl.mean()), "frac_ge70": float((pl >= 70).mean()),
                  "frac_ge50": float((pl >= 50).mean()), "longest_run_ge70": longest(70), "longest_run_ge50": longest(50),
                  "uniprot_entry_found": bool(ent), "uniprot_features": feats,
                  "md_decision": ("not run: no stretch of >=30 consecutive residues with pLDDT>=70 to define a prepared MD start"
                                  if longest(70) < 30 else "has a confident stretch; MD could be considered on that segment only")}
        print(g, round(out[g]["mean_plddt"], 1), out[g]["frac_ge70"], out[g]["longest_run_ge70"], len(feats), flush=True)
    p = write("s4_structure_confidence_vs_domains.json", out)
    return p, ins


def main():
    which = sys.argv[1]
    for name, fn in [("s1", s1), ("s2", s2), ("s2b", s2b), ("s3", s3), ("s4", s4)]:
        if which in (name, "all"):
            t0 = time.time()
            p, ins = fn()
            write(f"{name}_receipt.json", receipt(name, ins, {"result": p}, {"wall_seconds": round(time.time() - t0, 1)}))


if __name__ == "__main__":
    main()
