#!/usr/bin/env python3
"""Parse voxcraft-sim reports + manifest -> per-body CSV and the preregistered endpoint verdicts."""
import sys, os, json, csv, math, statistics as st
import xml.etree.ElementTree as ET

def load_reports(d):
    rows = {}
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".xml") or fn == "output.xml":
            continue
        batch = fn[:-4]
        try:
            root = ET.parse(os.path.join(d, fn)).getroot()
        except Exception as e:
            print("UNPARSEABLE", fn, e); continue
        det = root.find("detail")
        for b in (det if det is not None else []):
            g = lambda p: float(b.find(p).text)
            r = dict(batch=batch, name=b.tag, t=g("currentTime"), n_vox=int(g("num_voxel")),
                     x0=g("initialCenterOfMass/x"), y0=g("initialCenterOfMass/y"), z0=g("initialCenterOfMass/z"),
                     x1=g("currentCenterOfMass/x"), y1=g("currentCenterOfMass/y"), z1=g("currentCenterOfMass/z"))
            r["dx"], r["dy"], r["dz"] = r["x1"]-r["x0"], r["y1"]-r["y0"], r["z1"]-r["z0"]
            rows[(batch, b.tag)] = r
    return rows

def vec(r): return (r["dx"], r["dy"])
def norm(v): return math.hypot(*v)
def sub(a, b): return (a[0]-b[0], a[1]-b[1])
def mean_d(rows, batch, prefix, pat, nrep=3):
    vs = [vec(rows[(batch, f"{prefix}_{pat}_r{i}")]) for i in range(nrep) if (batch, f"{prefix}_{pat}_r{i}") in rows]
    if not vs: return None, None
    m = (st.mean(v[0] for v in vs), st.mean(v[1] for v in vs))
    spread = max(norm(sub(v, m)) for v in vs)
    return m, spread

def main(d):
    rows = load_reports(d)
    out = {"n_bodies_reported": len(rows)}
    with open(os.path.join(d, "bodies.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(next(iter(rows.values())).keys()) if rows else ["batch"])
        w.writeheader(); [w.writerow(r) for r in rows.values()]
    REF = {"endpoints_dt090": "ref", "endpoints_dt045": "ref", "endpoints_dt0225": "ref", "endpoints_mesh": "fine"}
    pats = ["passive_cte0","sync","wave_px","wave_mx","wave_py","wave_my","checker","split_px","split_mx","diag_pxpy","diag_pxmy"]
    tab = {}
    for b, p in REF.items():
        for pat in pats:
            m, s = mean_d(rows, b, p, pat)
            if m is not None:
                tab[(b, pat)] = (m, s)
    out["table"] = {f"{b}|{pat}": dict(dx=v[0][0], dy=v[0][1], norm=norm(v[0]), rep_spread=v[1]) for (b, pat), v in tab.items()}
    base = "endpoints_dt090"; refs = ["endpoints_dt045", "endpoints_dt0225", "endpoints_mesh"]
    # E1
    pv = [norm(vec(r)) for (b, n), r in rows.items() if b in REF and "passive_cte0" in n]
    out["E1_passive"] = dict(max_abs_d=max(pv) if pv else None, n=len(pv), tol=1e-5,
                             verdict=("PASS" if pv and max(pv) < 1e-5 else "FAIL") if len(pv) == 12 else "INCOMPLETE")
    # E2
    def e2(a, c):
        if (base, a) not in tab or (base, c) not in tab: return dict(verdict="INCOMPLETE")
        delta = norm(sub(tab[(base, a)][0], tab[(base, c)][0]))
        ch = {f"{P}@{r}": norm(sub(tab[(r, P)][0], tab[(base, P)][0])) for P in (a, c) for r in refs if (r, P) in tab}
        R = max(ch.values()) if ch else None
        return dict(delta=delta, R=R, changes=ch, verdict=("PASS" if delta > R else "FAIL") if len(ch) == 6 else "INCOMPLETE")
    out["E2_pattern_dependence"] = {f"{a}~{c}": e2(a, c) for a, c in (("wave_px","sync"),("wave_px","checker"),("split_px","sync"))}
    out["E2_primary"] = out["E2_pattern_dependence"]["wave_px~sync"]["verdict"]
    # E3
    M = {"x": lambda v: (-v[0], v[1]), "y": lambda v: (v[0], -v[1])}
    e3 = {}
    for a, c, ax in (("wave_px","wave_mx","x"),("split_px","split_mx","x"),("wave_py","wave_my","y"),("diag_pxpy","diag_pxmy","y")):
        for b in [base] + refs:
            if (b, a) in tab and (b, c) in tab:
                da, dc = tab[(b, a)][0], tab[(b, c)][0]
                e = norm(sub(dc, M[ax](da))); thr = max(1e-5, 0.01*norm(da))
                e3[f"{a}~{c}@{b}"] = dict(e=e, d_orig=norm(da), thr=thr, rel=e/norm(da) if norm(da) else None, ok=e < thr)
    out["E3_mirror"] = e3
    bp = [v for k, v in e3.items() if k.endswith("@"+base)]
    out["E3_primary"] = ("PASS" if all(v["ok"] for v in bp) else "FAIL") if len(bp) == 4 else "INCOMPLETE"
    # Population
    pop = {}
    for (b, n), r in rows.items():
        if b.startswith("pop_"):
            c, arm = n.split("_"); pop.setdefault(c, {})[arm] = r
    full = {c: v for c, v in pop.items() if len(v) == 4}
    if full:
        pas = sorted(norm(vec(v["pas"])) for v in full.values())
        p95 = pas[int(0.95*(len(pas)-1))]
        act = [norm(vec(v["act"])) for v in full.values()]
        emir = [norm(sub(vec(v["mir"]), (-v["act"]["dx"], v["act"]["dy"]))) for v in full.values()]
        erep = [norm(sub(vec(v["rep"]), vec(v["act"]))) for v in full.values()]
        mask = [norm(vec(v["act"])) > 10*max(p95, 1e-12) for v in full.values()]
        rel = [e/a for e, a, m in zip(emir, act, mask) if m]
        q = lambda xs, p: sorted(xs)[int(p*(len(xs)-1))] if xs else None
        out["population"] = dict(n_candidates_complete=len(full), n_candidates_partial=len(pop)-len(full),
            passive_frac_ge_tol=sum(1 for x in pas if x >= 1e-5)/len(pas), passive_p50=q(pas,.5), passive_p95=p95, passive_max=pas[-1],
            act_p50=q(act,.5), act_p90=q(act,.9), act_max=max(act),
            mirror_err_p50=q(emir,.5), mirror_err_p95=q(emir,.95), rep_err_p50=q(erep,.5), rep_err_max=max(erep),
            frac_rep_exact=sum(1 for x in erep if x == 0)/len(erep),
            n_rel_eligible=len(rel), mirror_rel_p50=q(rel,.5), mirror_rel_p90=q(rel,.9), frac_mirror_rel_lt_1pct=(sum(1 for x in rel if x < .01)/len(rel)) if rel else None)
        top = sorted(full.items(), key=lambda kv: -norm(vec(kv[1]["act"])))[:10]
        out["population_top10"] = [dict(cand=c, d_act=norm(vec(v["act"])), dx=v["act"]["dx"], dy=v["act"]["dy"], d_pas=norm(vec(v["pas"])),
                                         mirror_err=norm(sub(vec(v["mir"]), (-v["act"]["dx"], v["act"]["dy"]))), n_vox=v["act"]["n_vox"]) for c, v in top]
    json.dump(out, open(os.path.join(d, "endpoints.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ("table", "E3_mirror")}, indent=1))

if __name__ == "__main__":
    main(sys.argv[1])
