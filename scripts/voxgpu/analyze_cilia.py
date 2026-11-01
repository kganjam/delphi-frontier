#!/usr/bin/env python3
"""Evaluate PREREGISTRATION.md Addendum A (cilia arm) from cilia_dt090.xml / cilia_dt045.xml."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A
d = sys.argv[1]; rows = A.load_reports(d); out = {}
def m(b, F, k):
    vs = [A.vec(rows[(b, "cil_F%03d_%s_r%d" % (F, k, r))]) for r in range(3) if (b, "cil_F%03d_%s_r%d" % (F, k, r)) in rows]
    if not vs: return None, None
    mu = (sum(v[0] for v in vs)/len(vs), sum(v[1] for v in vs)/len(vs)); return mu, max(A.norm(A.sub(v, mu)) for v in vs)
B9, B4 = "cilia_dt090", "cilia_dt045"
off = [A.norm(A.vec(r)) for (b, n), r in rows.items() if "_off_" in n]
out["C1_passive"] = dict(max_abs_d=max(off), n=len(off), verdict="PASS" if len(off) == 6 and max(off) < 1e-5 else ("FAIL" if len(off) == 6 else "INCOMPLETE"))
px9, _ = m(B9, 20, "px"); sw9, _ = m(B9, 20, "swirl"); px4, _ = m(B4, 20, "px"); sw4, _ = m(B4, 20, "swirl")
delta = A.norm(A.sub(px9, sw9)); R = max(A.norm(A.sub(px4, px9)), A.norm(A.sub(sw4, sw9)))
out["C2_pattern_dependence_F020"] = dict(delta=delta, R=R, verdict="PASS" if delta > R else "FAIL")
Mx = lambda v: (-v[0], v[1]); My = lambda v: (v[0], -v[1]); c3 = {}; allok = True
for F in (5, 10, 20):
    for a_, c_, M in (("px", "mx", Mx), ("py", "my", My), ("dpp", "dpm", My), ("rand", "randmy", My)):
        for b in (B9, B4):
            da, _ = m(b, F, a_); dc, _ = m(b, F, c_)
            e = A.norm(A.sub(dc, M(da))); thr = max(1e-5, 0.01 * A.norm(da)); ok = e < thr
            if b == B9: allok &= ok
            c3[f"F{F:03d}_{a_}~{c_}@{b}"] = dict(e=e, d=A.norm(da), thr=thr, ok=ok)
out["C3_mirror"] = c3; out["C3_primary"] = "PASS" if allok else "FAIL"
out["disp_vs_F_dt090"] = {f"F{F:03d}_{k}": (lambda v: None if v is None else [v[0], v[1]])(m(B9, F, k)[0]) for F in (5, 10, 20) for k in ("px", "py", "dpp", "swirl", "rand")}
out["replicate_spread_max"] = max((m(b, F, k)[1] or 0) for b in (B9, B4) for F in (5, 10, 20) for k in ("px", "mx", "py", "my", "dpp", "dpm", "swirl", "rand", "randmy"))
json.dump(out, open(os.path.join(d, "cilia_endpoints.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "C3_mirror"}, indent=1))
print("worst C3 rel err at dt090:", max((v["e"] / v["d"]) for k, v in c3.items() if k.endswith(B9) and v["d"] > 1e-5))
