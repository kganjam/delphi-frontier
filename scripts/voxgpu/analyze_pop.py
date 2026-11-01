#!/usr/bin/env python3
"""Merge lite population reports (unmodified L40S + fork H100; identical inputs) and summarise.
Usage: analyze_pop.py <out.json> <dir>[:engine] ...   Bodies present in both engines must agree bitwise (checked)."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A
out_path = sys.argv[1]; src = {}; disagree = 0; both = 0
for spec in sys.argv[2:]:
    d, eng = spec.split(":")
    for (b, n), r in A.load_reports(d).items():
        if not b.startswith("pop"): continue
        if n in src:
            both += 1
            if A.vec(src[n][0]) != A.vec(r): disagree += 1
            continue
        src[n] = (r, eng)
c = {}
for n, (r, eng) in src.items():
    cand, arm = n.split("_"); c.setdefault(cand, {})[arm] = (r, eng)
full = {k: v for k, v in c.items() if len(v) == 4}
q = lambda xs, p: sorted(xs)[min(len(xs) - 1, int(p * (len(xs) - 1)))]
N = lambda r: A.norm(A.vec(r))
pas = [N(v["pas"][0]) for v in full.values()]; act = [N(v["act"][0]) for v in full.values()]
emir = [A.norm(A.sub(A.vec(v["mir"][0]), (-v["act"][0]["dx"], v["act"][0]["dy"]))) for v in full.values()]
erep = [A.norm(A.sub(A.vec(v["rep"][0]), A.vec(v["act"][0]))) for v in full.values()]
ratio = [a / max(p, 1e-9) for a, p in zip(act, pas)]
clean = [k for k, v in full.items() if N(v["pas"][0]) < 1e-5]          # passive control holds (E1 criterion)
act_clean = [N(full[k]["act"][0]) for k in clean]
emir_clean = [A.norm(A.sub(A.vec(full[k]["mir"][0]), (-full[k]["act"][0]["dx"], full[k]["act"][0]["dy"]))) for k in clean]
rel_clean = [e / a for e, a in zip(emir_clean, act_clean) if a > 1e-3]
engines = {}
for v in full.values():
    for arm in v.values(): engines[arm[1]] = engines.get(arm[1], 0) + 1
out = dict(n_candidates=len(full), n_bodies=4 * len(full), bodies_by_engine=engines, cross_engine_overlap=both, cross_engine_disagreements=disagree,
           invalid_rejected=len(A.INVALID), duplicates_exact=sum(1 for e in erep if e == 0), duplicate_err_max=max(erep),
           passive_ge_10um=sum(1 for p in pas if p >= 1e-5), passive_p50=q(pas, .5), passive_p95=q(pas, .95), passive_max=max(pas),
           act_p50=q(act, .5), act_p90=q(act, .9), act_max=max(act),
           frac_act_gt_10x_passive=sum(1 for x in ratio if x > 10) / len(ratio),
           clean_n=len(clean), clean_act_p50=q(act_clean, .5) if clean else None, clean_act_p90=q(act_clean, .9) if clean else None,
           clean_act_max=max(act_clean) if clean else None,
           clean_mirror_err_p50=q(emir_clean, .5) if clean else None, clean_mirror_err_p95=q(emir_clean, .95) if clean else None,
           clean_rel_mirror_n=len(rel_clean), clean_rel_mirror_p50=q(rel_clean, .5) if rel_clean else None,
           clean_rel_mirror_p90=q(rel_clean, .9) if rel_clean else None,
           clean_rel_mirror_frac_lt_1pct=(sum(1 for x in rel_clean if x < .01) / len(rel_clean)) if rel_clean else None)
top = sorted(clean, key=lambda k: -N(full[k]["act"][0]))[:10]
out["top10_clean"] = [dict(cand=k, d_mm=round(N(full[k]["act"][0]) * 1e3, 3), dx_mm=round(full[k]["act"][0]["dx"] * 1e3, 3),
                           dy_mm=round(full[k]["act"][0]["dy"] * 1e3, 3), passive_um=round(N(full[k]["pas"][0]) * 1e6, 3),
                           mirror_err_mm=round(A.norm(A.sub(A.vec(full[k]["mir"][0]), (-full[k]["act"][0]["dx"], full[k]["act"][0]["dy"]))) * 1e3, 3),
                           n_vox=full[k]["act"][0]["n_vox"]) for k in top]
out["points"] = [[k, N(v["act"][0]), N(v["pas"][0]), A.norm(A.sub(A.vec(v["mir"][0]), (-v["act"][0]["dx"], v["act"][0]["dy"]))), v["act"][0]["n_vox"]] for k, v in sorted(full.items())]
json.dump(out, open(out_path, "w"))
print(json.dumps({k: v for k, v in out.items() if k != "points"}, indent=1))
