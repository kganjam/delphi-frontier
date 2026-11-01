#!/usr/bin/env python3
"""Build the voxcraft GPU results page (single HTML, inline SVG) from committed result JSON/XML."""
import json, math, sys, os, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A
ART = "artifacts/voxcraft-gpu"
ep = json.load(open(f"{ART}/sweep-l40s-s1-unmodified/endpoints.json"))
ci = json.load(open(f"{ART}/cilia-l40s-e2-unmodified/cilia_endpoints.json"))
pop = json.load(open(sys.argv[1])); out = sys.argv[2]
W, H, PL, PB, PT, PR = 640, 300, 64, 44, 16, 16

def logscale(v, lo, hi, a, b):
    return a + (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (b - a)

# Chart 1: mirror error relative (log) per pair, contraction (base dt) vs cilia (dt090, F=0.01 and 0.02)
pairs = [("wave_px~wave_mx", "Wave, x-mirror"), ("split_px~split_mx", "Half-split, x-mirror"),
         ("wave_py~wave_my", "Short-axis wave, y-mirror"), ("diag_pxpy~diag_pxmy", "Diagonal wave, y-mirror")]
con = [(lbl, ep["E3_mirror"][f"{k}@endpoints_dt090"]["rel"]) for k, lbl in pairs]
cil = []
for k, lbl in (("F020_px~mx", "Thrust +x/−x, 0.02 N"), ("F020_py~my", "Thrust +y/−y, 0.02 N"), ("F020_dpp~dpm", "Thrust diagonal, 0.02 N"),
               ("F010_px~mx", "Thrust +x/−x, 0.01 N"), ("F010_py~my", "Thrust +y/−y, 0.01 N (threshold)")):
    v = ci["C3_mirror"][f"{k}@cilia_dt090"]; cil.append((lbl, max(v["e"] / v["d"], 1e-7)))
rows = [("c", l, v) for l, v in con] + [("k", l, v) for l, v in cil]
lo, hi = 1e-7, 10
bh, gap = 22, 8; H1 = PT + len(rows) * (bh + gap) + PB; LX = 230
s = [f'<svg viewBox="0 0 {W} {H1}" role="img" aria-label="Relative mirror error per pattern pair, log scale">']
for t in range(-7, 2):
    x = logscale(10 ** t, lo, hi, LX, W - PR)
    s.append(f'<line x1="{x:.1f}" y1="{PT}" x2="{x:.1f}" y2="{H1-PB}" class="grid"/><text x="{x:.1f}" y="{H1-PB+16}" class="tick" text-anchor="middle">1e{t}</text>')
x1 = logscale(0.01, lo, hi, LX, W - PR)
s.append(f'<line x1="{x1:.1f}" y1="{PT-4}" x2="{x1:.1f}" y2="{H1-PB}" class="bound"/><text x="{x1+4:.1f}" y="{PT+6}" class="tick">1% preregistered bound</text>')
for i, (kind, lbl, v) in enumerate(rows):
    y = PT + i * (bh + gap); w = logscale(max(v, lo), lo, hi, LX, W - PR) - LX
    s.append(f'<g class="hov"><title>{html.escape(lbl)}: mirror error {v*100:.3g}% of |d|</title><text x="{LX-8}" y="{y+bh/2+4}" class="lab" text-anchor="end">{html.escape(lbl)}</text>'
             f'<rect x="{LX}" y="{y}" width="{max(w,2):.1f}" height="{bh}" rx="4" class="{"s1" if kind=="c" else "s2"}"/>'
             f'<text x="{LX+max(w,2)+6:.1f}" y="{y+bh/2+4}" class="val">{v*100:.2g}%</text></g>')
s.append(f'<text x="{(LX+W)/2:.0f}" y="{H1-6}" class="tick" text-anchor="middle">mirror error ÷ |displacement| (log)</text></svg>')
chart1 = "".join(s)

# Chart 2: population scatter, |d_act| vs |d_passive| (log-log)
pts = pop["points"]; lo2, hi2 = 1e-9, 1e-1
s = [f'<svg viewBox="0 0 {W} {H+40}" role="img" aria-label="Population: active displacement vs passive control displacement">']
for t in range(-9, 0):
    x = logscale(10 ** t, lo2, hi2, PL, W - PR); y = logscale(10 ** t, lo2, hi2, H + 40 - PB, PT)
    s.append(f'<line x1="{x:.1f}" y1="{PT}" x2="{x:.1f}" y2="{H+40-PB}" class="grid"/><line x1="{PL}" y1="{y:.1f}" x2="{W-PR}" y2="{y:.1f}" class="grid"/>')
    s.append(f'<text x="{x:.1f}" y="{H+40-PB+16}" class="tick" text-anchor="middle">1e{t}</text><text x="{PL-6}" y="{y+4:.1f}" class="tick" text-anchor="end">1e{t}</text>')
xa, ya = logscale(lo2, lo2, hi2, PL, W - PR), logscale(lo2, lo2, hi2, H + 40 - PB, PT); xb, yb = logscale(hi2, lo2, hi2, PL, W - PR), logscale(hi2, lo2, hi2, H + 40 - PB, PT)
s.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" class="bound"/>')
xt = logscale(1e-5, lo2, hi2, PL, W - PR)
s.append(f'<line x1="{xt:.1f}" y1="{PT}" x2="{xt:.1f}" y2="{H+40-PB}" class="bound2"/><text x="{xt+4:.1f}" y="{PT+10}" class="tick">passive tolerance 10 µm</text>')
for name, a, p, e, n in pts:
    x = logscale(min(max(p, lo2), hi2), lo2, hi2, PL, W - PR); y = logscale(min(max(a, lo2), hi2), lo2, hi2, H + 40 - PB, PT)
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" class="dot"><title>{name}: active {a*1e3:.3f} mm, passive {p*1e6:.3g} µm, mirror error {e*1e3:.3f} mm, {n} voxels</title></circle>')
s.append(f'<text x="{(PL+W)/2:.0f}" y="{H+40-8}" class="tick" text-anchor="middle">passive-control displacement |d| (m, log)</text>'
         f'<text x="14" y="{(H+40)/2:.0f}" class="tick" transform="rotate(-90 14 {(H+40)/2:.0f})" text-anchor="middle">actuated |d| (m, log)</text></svg>')
chart2 = "".join(s)

# Chart 3: cilia displacement vs per-voxel force (dt090, +x)
fv = [(0.005, ci["disp_vs_F_dt090"]["F005_px"][0]), (0.010, ci["disp_vs_F_dt090"]["F010_px"][0]), (0.020, ci["disp_vs_F_dt090"]["F020_px"][0])]
mx = 800
s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Cilia thrust: displacement vs per-voxel force">']
for t in range(0, 801, 200):
    y = H - PB - t / mx * (H - PB - PT)
    s.append(f'<line x1="{PL}" y1="{y:.1f}" x2="{W-PR}" y2="{y:.1f}" class="grid"/><text x="{PL-6}" y="{y+4:.1f}" class="tick" text-anchor="end">{t}</text>')
bw = 90
for i, (F, d) in enumerate(fv):
    x = PL + 60 + i * 170; h = abs(d) * 1e3 / mx * (H - PB - PT)
    s.append(f'<g><title>{F} N per surface voxel: {d*1e3:.1f} mm in 5 s</title><rect x="{x}" y="{H-PB-max(h,1):.1f}" width="{bw}" height="{max(h,1):.1f}" rx="4" class="s2"/>'
             f'<text x="{x+bw/2}" y="{H-PB-max(h,1)-6:.1f}" class="val" text-anchor="middle">{d*1e3:.1f} mm</text>'
             f'<text x="{x+bw/2}" y="{H-PB+16}" class="tick" text-anchor="middle">{F} N / voxel</text></g>')
s.append(f'<text x="14" y="{H/2:.0f}" class="tick" transform="rotate(-90 14 {H/2:.0f})" text-anchor="middle">displacement in 5 s (mm)</text></svg>')
chart3 = "".join(s)

P = pop
doc = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "page_template.html")).read()
rep = {"CHART1": chart1, "CHART2": chart2, "CHART3": chart3,
       "POP_N": str(P["n_candidates"]), "POP_BODIES": str(P["n_bodies"]), "POP_OVERLAP": str(P["cross_engine_overlap"]),
       "POP_DISAGREE": str(P["cross_engine_disagreements"]), "POP_PAS": str(P["passive_ge_10um"]),
       "POP_PASFRAC": f'{100*P["passive_ge_10um"]/P["n_candidates"]:.0f}', "POP_CLEAN": str(P["clean_n"]),
       "POP_ACTP50": f'{P["clean_act_p50"]*1e3:.2f}', "POP_RELP50": f'{100*P["clean_rel_mirror_p50"]:.0f}',
       "POP_RELP90": f'{100*P["clean_rel_mirror_p90"]:.0f}', "POP_RELN": str(P["clean_rel_mirror_n"]),
       "POP_REL1": f'{100*P["clean_rel_mirror_frac_lt_1pct"]:.1f}', "POP_DUP": str(P["duplicates_exact"]),
       "VALID_N": str(33 + P["cross_engine_overlap"]) if P["cross_engine_disagreements"] == 0 else "MISMATCH", "POP_ENGINES": ", ".join(f"{v} on {k}" for k, v in P["bodies_by_engine"].items())}
for k, v in rep.items(): doc = doc.replace("{{" + k + "}}", v)
assert "{{" not in doc
open(out, "w").write(doc); print("wrote", out, len(doc))
