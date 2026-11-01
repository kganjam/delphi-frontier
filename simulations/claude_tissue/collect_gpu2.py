"""Collect the edge2d and phasemap Nebius jobs: parse the saved job log (META/RESULT/SNAP/FRAME/DONE lines),
write results JSON, figure (and video for edge2d), and a receipt that records job id, state and script hash.
Usage: collect_gpu2.py edge2d|phasemap <job_id> <saved_log> <state>"""
import json, sys, time, base64, pathlib, subprocess, tempfile, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, sha

kind, job, logp, state = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]).resolve(), sys.argv[4]
meta, rows, snaps, frames, done = None, [], [], [], None
TAGS = ("META ", "RESULT ", "SNAP ", "FRAME ", "DONE ")
def reassemble(lines):
    """Nebius log lines are split at 16384 chars and the continuation can appear before or after its head line
    (same timestamp).  Join each tagged line that does not parse with an adjacent untagged fragment; keep the join
    only if the result parses as JSON."""
    used, out = set(), []
    for i, ln in enumerate(lines):
        if i in used: continue
        tag = next((t for t in TAGS if ln.startswith(t)), None)
        if tag is None: continue
        try:
            json.loads(ln[len(tag):]); out.append(ln); continue
        except ValueError:
            pass
        for j in (i + 1, i - 1, i + 2, i - 2):
            if 0 <= j < len(lines) and j not in used and not any(lines[j].startswith(t) for t in TAGS):
                cand = ln + lines[j]
                try:
                    json.loads(cand[len(tag):]); out.append(cand); used.add(j); break
                except ValueError:
                    continue
        else:
            raise ValueError(f"could not reassemble log line {i} ({tag.strip()})")
    return out
for line in reassemble(logp.read_text().splitlines()):
    for tag in ("META ", "RESULT ", "SNAP ", "FRAME ", "DONE "):
        i = line.find(tag)
        if i == 0 or (i > 0 and line[i-1] == " "):
            obj = json.loads(line[i+len(tag):])
            {"META ": lambda o: None, "RESULT ": rows.append, "SNAP ": snaps.append, "FRAME ": frames.append, "DONE ": lambda o: None}[tag](obj)
            if tag == "META ": meta = obj
            if tag == "DONE ": done = obj
            break
assert meta, "no META line"
def img(s, key="u8"):
    shp = s.get("shape") or [s["n"], s["n"]]; return np.frombuffer(base64.b64decode(s[key]), dtype=np.uint8).reshape(shp)

SCRIPT_OF = {"edge2d_gamma_fine": "edge2d_gamma"}   # kinds that reuse another kind's GPU script
if kind in ("edge2d", "uniform2d", "edge2d_cases", "uniform2d_y0", "edge2d_gamma", "edge2d_gamma_fine"):
    if kind == "uniform2d_y0":   # group by starting length: reuse the 'b' slot as the grouping key, labelled Y0
        for r in rows + snaps: r["b"] = r.get("y0")
        meta["b"] = None
    if kind in ("edge2d_gamma", "edge2d_gamma_fine"):   # group by rate scale gamma
        for r in rows + snaps: r["b"] = r.get("gamma")
        meta["b"] = None
    OUT = ROOT/f"artifacts/simulations/claude-tissue-{kind.replace('_', '-')}"; OUT.mkdir(parents=True, exist_ok=True); script = f"simulations/claude_tissue/{SCRIPT_OF.get(kind, kind)}_gpu.py"
    summ = {}
    keys = sorted({(r.get("b", meta.get("b")), r["d"], r["speed"]) for r in rows}, key=lambda k: (k[0], k[1], -k[2] if k[2] else 1))
    for bb, d, v in keys:
            rs = [r for r in rows if r.get("b", meta.get("b")) == bb and r["d"] == d and r["speed"] == v]
            kk = {"edge2d_cases": f"b={bb},d={d},v={v}", "uniform2d_y0": f"Y0={bb},d={d},v={v}", "edge2d_gamma": f"gamma={bb},d={d},v={v}", "edge2d_gamma_fine": f"gamma={bb},d={d},v={v}"}.get(kind, f"d={d},v={v}")
            if rs: summ[kk] = dict(b=bb, d=d, speed=v, n=len(rs), orientation_A_mean=float(np.mean([r["orientation_A"] for r in rs])),
                                              orientation_A_sd=float(np.std([r["orientation_A"] for r in rs])), stripes_across_width=[r["stripes_across_width"] for r in rs],
                                              top2_power_fraction_mean=float(np.mean([r["top2_power_fraction"] for r in rs])))
    res = dict(job=job, job_state=state, meta=meta, done=done, n_rows=len(rows), summary=summ, rows=rows,
               reading="orientation_A > 0: stripes running proximo-distally (along growth, ray-like); ~0: isotropic; < 0: stripes parallel to the growing edge.")
    (OUT/f"{kind}.json").write_text(json.dumps(res, indent=1))
    fig = plt.figure(figsize=(16, 8)); ax = fig.add_subplot(2, 1, 1)
    allv = sorted({v["speed"] for v in summ.values()}, key=lambda x: -x if x else 1); pos = {sp: i for i, sp in enumerate(allv)}
    for (bb, d), c in zip(sorted({(v["b"], v["d"]) for v in summ.values()}), ["tab:red", "tab:green", "tab:blue", "tab:purple", "tab:orange"]):
        vs = [v for v in summ.values() if v["b"] == bb and v["d"] == d]
        ax.errorbar([pos[v["speed"]] for v in vs], [v["orientation_A_mean"] for v in vs], [v["orientation_A_sd"] for v in vs], marker="o", color=c, label=(f"start length Y0={bb}, d={d}" if kind == "uniform2d_y0" else (f"gamma={bb}, b=0.9, d={d}" if kind.startswith("edge2d_gamma") else f"b={bb}, d={d}")))
    ax.set_xticks(range(len(allv))); ax.set_xticklabels([("static (all at once)" if sp == 0 else f"{'uniform' if kind.startswith('uniform') else 'edge'} speed {sp}") for sp in allv])
    ax.axhline(0, color="k", lw=0.5); ax.set_ylabel("orientation index A (+1 = proximo-distal stripes)"); ax.legend()
    ax.set_title(f"SIMULATED 2-D { {'edge2d': 'distal-edge growth vs static patterning', 'edge2d_cases': 'distal-edge growth: threshold and other kinetics', 'uniform2d': 'UNIFORM proximo-distal growth (control)', 'uniform2d_y0': 'UNIFORM growth from different starting lengths Y0', 'edge2d_gamma': 'distal-edge growth: threshold vs rate scale gamma', 'edge2d_gamma_fine': 'distal-edge growth: finer speed grid near the threshold'}[kind] } ({len(meta['seeds'])} seeds each); dimensionless")
    sn_sorted = sorted(snaps, key=lambda s: (s.get("b", 0), s["d"], -s["speed"] if s["speed"] else 1))[:13]
    for i, s in enumerate(sn_sorted):
        a2 = fig.add_subplot(2, len(sn_sorted), len(sn_sorted) + 1 + i); a2.imshow(img(s), cmap="magma", origin="lower", aspect="auto"); a2.axis("off")
        a2.set_title(f"{({'uniform2d_y0': 'Y0=', 'edge2d_gamma': 'g=', 'edge2d_gamma_fine': 'g='}.get(kind, 'b='))+str(s['b'])+' ' if s.get('b') is not None else ''}d={s['d']}\n{'static' if s['speed']==0 else 'v='+str(s['speed'])}", fontsize=6)
    fig.text(0.5, 0.02, "panels: final field, seed 1, distal (growing) edge at top", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(OUT/f"{kind}.png", dpi=100); plt.close(fig)
    outs = [OUT/f"{kind}.json", OUT/f"{kind}.png"]
    if frames:
        tmp = tempfile.mkdtemp(prefix="e2v-"); fr = sorted(frames, key=lambda f: f["k"])
        for f in fr:
            fg, a = plt.subplots(figsize=(4, 7)); a.imshow(img(f), cmap="magma", origin="lower"); a.axis("off")
            a.set_title(f"SIMULATED d={f['d']}, edge speed {f['speed']}\nframe {f['k']} (distal edge grows upward)", fontsize=8)
            fg.savefig(f"{tmp}/f{f['k']:03d}.png", dpi=90); plt.close(fg)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-threads", "1", "-framerate", "10", "-i", f"{tmp}/f%03d.png", "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
                        "-pix_fmt", "yuv420p", "-c:v", "libx264", str(OUT/f"{kind}.mp4")], check=True)
        subprocess.run(["cp", f"{tmp}/f{fr[-1]['k']:03d}.png", str(OUT/"poster.png")], check=True); outs += [OUT/f"{kind}.mp4", OUT/"poster.png"]
elif kind == "pzone":
    OUT = ROOT/"artifacts/simulations/claude-tissue-pzone"; OUT.mkdir(parents=True, exist_ok=True); script = "simulations/claude_tissue/pzone_gpu.py"
    summ = {}
    for r in rows:
        k = f"lp={r['lp_label']},v={r['speed']}"
        summ.setdefault(k, dict(lp=r["lp"], lp_label=r["lp_label"], speed=r["speed"], A=[], stripes=[], length=r["length"], cells=r["cells"], splits=r["splits"]))
        summ[k]["A"].append(r["orientation_A"]); summ[k]["stripes"].append(r["stripes_across_width"])
    for v in summ.values():
        a = np.array(v["A"]); v.update(n=len(a), orientation_A_mean=float(a.mean()), orientation_A_sd=float(a.std()), orientation_A_sem=float(a.std()/np.sqrt(len(a))),
                                       frac_seeds_A_gt_0_8=float(np.mean(a > 0.8)))
    res = dict(job=job, job_state=state, meta=meta, done=done, n_rows=len(rows), summary=summ, rows=rows,
               reading="lp = width of the distal proliferation zone (small = apical/edge, 'uniform' = whole length); A +1 = proximo-distal stripes")
    (OUT/"pzone.json").write_text(json.dumps(res, indent=1))
    fig = plt.figure(figsize=(16, 8)); ax = fig.add_subplot(2, 1, 1)
    lps = [l for l in meta["lps"]]; cols = ["tab:red", "tab:orange", "tab:green", "tab:blue"]
    for l, c in zip(lps, cols):
        lab = "uniform" if l == 0 else l; vs = [v for v in summ.values() if v["lp_label"] == lab]
        vs.sort(key=lambda v: v["speed"])
        ax.errorbar([v["speed"] for v in vs], [v["orientation_A_mean"] for v in vs], [v["orientation_A_sem"]*1.96 for v in vs], marker="o", color=c, capsize=3,
                    label=f"proliferation zone {'= whole length (uniform)' if l == 0 else str(l) + ' (wavelength ~11)'}")
    st = [v for v in summ.values() if v["lp_label"] == "static"]
    if st: ax.axhline(st[0]["orientation_A_mean"], color="gray", ls=":", label="static (all at once)")
    ax.axhline(0, color="k", lw=0.5); ax.set_xlabel("total elongation speed v"); ax.set_ylabel("orientation A (mean, 95% CI over 12 seeds)")
    ax.set_title(f"SIMULATED continuous growth in a distal proliferation zone, start length {meta['Y0']} -> {meta['Y1']}, d={meta['d']}"); ax.legend(fontsize=8)
    sn = sorted(snaps, key=lambda s: (s["lp"] if s["lp"] > 0 else (1e3 if s["lp"] == 0 else 1e4), s["speed"]))
    for i, s_ in enumerate(sn[:13]):
        a2 = fig.add_subplot(2, len(sn[:13]), len(sn[:13]) + 1 + i); a2.imshow(img(s_), cmap="magma", origin="lower", aspect="auto"); a2.axis("off")
        a2.set_title(f"{'static' if s_['lp'] < 0 else ('unif' if s_['lp'] == 0 else 'Lp=' + str(s_['lp']))}\nv={s_['speed']}", fontsize=6)
    fig.tight_layout(); fig.savefig(OUT/"pzone.png", dpi=100); plt.close(fig)
    outs = [OUT/"pzone.json", OUT/"pzone.png"]
elif kind in ("fan", "fan_video"):
    OUT = ROOT/f"artifacts/simulations/claude-tissue-{kind.replace('_', '-')}"; OUT.mkdir(parents=True, exist_ok=True); script = f"simulations/claude_tissue/{kind}_gpu.py"
    summ = {}
    for d in meta["ds"]:
        for v in meta["speeds"]:
            rs = [r for r in rows if r["d"] == d and r["speed"] == v]
            if not rs: continue
            cnt = np.array([r["peaks_along_arc"] for r in rs]); exp = np.array(rs[0]["expected_r_theta_over_lambda"])
            summ[f"d={d},v={v}"] = dict(d=d, speed=v, radii=rs[0]["radii"], peaks_mean=cnt.mean(0).tolist(), peaks_by_seed=cnt.tolist(),
                                        expected=exp.tolist(), inner_to_outer_increase=float(cnt[:, -1].mean() - cnt[:, 0].mean()),
                                        expected_increase=float(exp[-1] - exp[0]),
                                        radial_orientation_A=float(np.mean([r["radial_orientation_A"] for r in rs])))
    res = dict(job=job, job_state=state, meta=meta, done=done, n_rows=len(rows), summary=summ, rows=rows,
               reading="If stripes run radially and keep their spacing, the count along the arc rises with radius as r*THETA/lambda (stripes inserted or branched); a flat count means stripes fan out and widen instead.")
    (OUT/f"{kind}.json").write_text(json.dumps(res, indent=1))
    fig = plt.figure(figsize=(15, 5)); ax = fig.add_subplot(1, 4, 1)
    for (k, v), c in zip(summ.items(), ["tab:red", "tab:blue", "tab:gray", "tab:green"]):
        ax.plot(v["radii"], v["peaks_mean"], "o-", color=c, label=("static" if v["speed"] == 0 else f"edge speed {v['speed']}") + f", d={v['d']}")
    v0 = next(iter(summ.values())); ax.plot(v0["radii"], v0["expected"], "k--", label="r*THETA/lambda*")
    ax.set_xlabel("radius r"); ax.set_ylabel("stripes counted along the arc"); ax.legend(fontsize=7); ax.set_title("SIMULATED fan: stripe count vs radius", fontsize=9)
    for i, sn in enumerate(sorted(snaps, key=lambda s: -s["speed"] if s["speed"] else 1)[:3]):
        a2 = fig.add_subplot(1, 4, 2 + i); a2.imshow(img(sn), cmap="magma", origin="lower"); a2.axis("off")
        a2.set_title(f"d={sn['d']}, {'static' if sn['speed']==0 else 'edge speed '+str(sn['speed'])} (base at bottom)", fontsize=8)
    fig.tight_layout(); fig.savefig(OUT/f"{kind}.png", dpi=100); plt.close(fig)
    outs = [OUT/f"{kind}.json", OUT/f"{kind}.png"]
    if frames:
        tmp = tempfile.mkdtemp(prefix="fanv-"); fr = sorted(frames, key=lambda f: f["k"])
        for f in fr:
            fg, a = plt.subplots(figsize=(5, 5)); a.imshow(img(f), cmap="magma", origin="lower"); a.axis("off")
            a.set_title(f"SIMULATED Turing pattern on a fan growing at its distal arc\nd={f['d']}, edge speed {f['speed']}, t={f['t']:.0f} (dimensionless)", fontsize=8)
            fg.savefig(f"{tmp}/f{f['k']:03d}.png", dpi=90); plt.close(fg)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-threads", "1", "-framerate", "12", "-i", f"{tmp}/f%03d.png", "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
                        "-pix_fmt", "yuv420p", "-c:v", "libx264", str(OUT/f"{kind}.mp4")], check=True)
        subprocess.run(["cp", f"{tmp}/f{fr[-1]['k']:03d}.png", str(OUT/"poster.png")], check=True); outs += [OUT/f"{kind}.mp4", OUT/"poster.png"]
else:
    OUT = ROOT/"artifacts/simulations/claude-tissue-phase-map"; OUT.mkdir(parents=True, exist_ok=True); script = "simulations/claude_tissue/phase_map_gpu.py"
    grid = {}
    for b in meta["bs"]:
        for d in meta["ds"]:
            rs = [r for r in rows if r["b"] == b and r["d"] == d]
            if not rs: continue
            if not rs[0].get("simulated"):
                grid[f"{b},{d}"] = dict(b=b, d=d, turing_unstable=False); continue
            dens = [r.get("component_density") for r in rs if r.get("component_density") is not None]
            grid[f"{b},{d}"] = dict(b=b, d=d, turing_unstable=True, component_density_mean=float(np.mean(dens)) if dens else None,
                                    labels=[r.get("label") for r in rs], wavelength_mean=float(np.mean([r["wavelength"] for r in rs])),
                                    amplitude_mean=float(np.mean([r["amplitude"] for r in rs])))
    res = dict(job=job, job_state=state, meta=meta, done=done, n_rows=len(rows), grid=grid, rows=rows,
               classifier="component density = n_components(u>mean)*lambda^2/area; > 0.6 spots, else stripes/labyrinth (synthetic check: stripes 0.25, hexagonal spots 1.0)")
    (OUT/"phase-map.json").write_text(json.dumps(res, indent=1))
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))
    M = np.full((len(meta["bs"]), len(meta["ds"])), np.nan)
    for i, b in enumerate(meta["bs"]):
        for j, d in enumerate(meta["ds"]):
            gcell = grid.get(f"{b},{d}")
            if gcell and gcell["turing_unstable"] and gcell["component_density_mean"] is not None: M[i, j] = gcell["component_density_mean"]
    im = ax[0].imshow(M, origin="lower", cmap="coolwarm", vmin=0, vmax=1.4, aspect="auto")
    ax[0].set_xticks(range(len(meta["ds"]))); ax[0].set_xticklabels(meta["ds"]); ax[0].set_yticks(range(len(meta["bs"]))); ax[0].set_yticklabels(meta["bs"])
    ax[0].set_xlabel("diffusion ratio d"); ax[0].set_ylabel("kinetic parameter b"); fig.colorbar(im, ax=ax[0], label="component density (blue: stripes, red: spots); blank = no Turing pattern")
    ax[0].set_title("SIMULATED Schnakenberg stripe/spot phase map (a=0.1, 3 seeds)")
    sn = {(s["b"], s["d"]): s for s in snaps}; nb, nd = len(meta["bs"]), len(meta["ds"])
    tsz = next(iter(sn.values()))["n"] if sn else 64; P = tsz + 2
    canvas = np.full((nb*P, nd*P), 255, np.uint8)
    for i, b in enumerate(meta["bs"]):
        for j, d in enumerate(meta["ds"]):
            if (b, d) in sn: canvas[i*P:i*P+tsz, j*P:j*P+tsz] = img(sn[(b, d)])
    ax[1].imshow(canvas, cmap="magma", origin="lower"); ax[1].set_xticks([j*P + tsz//2 for j in range(nd)]); ax[1].set_xticklabels(meta["ds"])
    ax[1].set_yticks([i*P + tsz//2 for i in range(nb)]); ax[1].set_yticklabels(meta["bs"]); ax[1].set_xlabel("d"); ax[1].set_ylabel("b"); ax[1].set_title("final fields (seed 11, 64x64 downsample)")
    fig.tight_layout(); fig.savefig(OUT/"phase-map.png", dpi=100); plt.close(fig)
    outs = [OUT/"phase-map.json", OUT/"phase-map.png"]
ok = state == "COMPLETED" and done is not None
rec = dict(name=f"claude-tissue-{kind.replace('_', '-')}", command=f"python3 /work/{ {'edge2d': 'edge2d', 'uniform2d': 'uniform2d', 'phasemap': 'phasemap', 'edge2d_cases': 'edge2dc', 'uniform2d_y0': 'uniform2dy0', 'fan': 'fan', 'edge2d_gamma': 'edge2dg', 'fan_video': 'fanv', 'edge2d_gamma_fine': 'edge2dg', 'pzone': 'pzone'}[kind] }.py (args in META)", job=job, job_state=state,
           exit_code=0 if ok else 1, seed=meta.get("seeds"), wall_s=(done or {}).get("wall_s"),
           compute=f"Nebius {job} ({meta.get('gpu')}), image nvcr.io/nvidia/pytorch@sha256:11e99763...",
           code_sha256={script: meta["script_sha256"]}, code_matches_repo=bool(meta["script_sha256"] == sha(ROOT/script)),
           collector_sha256={"simulations/claude_tissue/collect_gpu2.py": sha(ROOT/"simulations/claude_tissue/collect_gpu2.py")},
           input_sha256={}, output_sha256={str(p.relative_to(ROOT)): sha(p) for p in outs + [logp]},
           evidence_kind="simulated; not observed", collected_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
(OUT/f"receipt-claude-tissue-{kind.replace('_', '-')}.json").write_text(json.dumps(rec, indent=1, sort_keys=True))
print(json.dumps(dict(kind=kind, rows=len(rows), snaps=len(snaps), frames=len(frames), done=done, code_matches_repo=rec["code_matches_repo"])))
