"""Read-only gallery adapter for the neural-scale models (engineering.neuro). The site owner supplies tracked reads and media copying.

Usage in build_site.engineering_cards:
    cards += neuro_site.build_cards(ins.read, lambda rid, name, sha: _vid(ins, out, "neuro-" + rid, "artifacts/neuro/" + rid, name, sha))

A card is built only for a run whose run_receipt.json says exit_code 0 and whose manifest digest matches that receipt.
No simulator import, model run or network access happens here. Numbers come from the manifests; the authored text is in cards.json.
"""
from __future__ import annotations
from hashlib import sha256
import json

RIDS = ("m1-fast-start", "m2-caudal-cpg", "m3-glide-stabilizer", "j1-m1-sobol", "j2-m3-atlas", "j3-m5-mcell", "j4-m3-sobol")


def _f(x, nd=2):
    return "n/a" if x is None else (f"{x:.{nd}f}" if isinstance(x, (int, float)) else str(x))


def _q(d, unit=""):
    return f"median {_f(d.get('q50'))}{unit} (5-95%: {_f(d.get('q5'))}-{_f(d.get('q95'))}{unit}, n {d.get('n')})" if d and d.get("n") else "none"


def findings(rid, m):
    s = m.get("summary") or m.get("headline") or {}
    if rid == "m1-fast-start":
        tp, to = s["taxi_pes"], s["taxi_opt"]
        return [{"name": "emergence speed", "result": _q(s["U_emerge_ms"], " m/s") + "; Fish 1990 implies about 10 m/s at the start of the taxi"},
                {"name": "emergence path angle", "result": _q(s["gamma_emerge_deg"], " deg")},
                {"name": "looming onset to Mauthner command", "result": _q({k: (v * 1e3 if k != "n" else v) for k, v in s["t_go_s"].items()}, " ms") + " (Preuss 2006 goldfish means: 142-716 ms)"},
                {"name": "outcome fractions", "result": f"respond {_f(s['P_respond'])}, caught {_f(s['P_caught'])}, emerge {_f(s['P_emerge'])} (pursuit predator is an assumption)"},
                {"name": "take-off after taxi | emerged", "result": f"pessimistic start {_f(tp['P_takeoff_given_emerge'])}, optimistic start {_f(to['P_takeoff_given_emerge'])}"},
                {"name": "glide range after take-off (h0 0.1 m)", "result": _q(tp["glide_range_m_h0_0.1"], " m") + "; fixed V0 12 m/s, h0 1 m baseline: 25.1 m"},
                {"name": "power to hold 10 m/s underwater", "result": ", ".join(f"{k}: {v:.0f} W/kg muscle" for k, v in s["power_to_hold_10ms_submerged_W_per_kg_muscle"].items())}]
    if rid == "m2-caudal-cpg":
        return [{"name": "submerged speed at muscle-power cap", "result": ", ".join(f"{k} W/kg: {v:.2f} m/s" for k, v in s["submerged_U_at_power_cap_W_per_kg"].items())},
                {"name": "sweep maximum (no power cap)", "result": f"{_f(s['sweep_max_U_ms'])} m/s ({_f(s['sweep_max_U_BL_s'], 0)} body lengths/s)"},
                {"name": "taxi top speed, f50 Hz, muscle corner 70 Hz", "result": json.dumps(s["taxi_V_max_ms_capped_by_power_and_wet_fraction"].get("f50_fm70"))}]
    if rid == "m3-glide-stabilizer":
        return [{"name": "trim (25 g print)", "result": f"V {_f(s['trim_25g']['V'])} m/s, NP {_f(s['trim_25g']['x_np'] * 1e3, 1)} mm, CG {_f(s['trim_25g']['x_cg'] * 1e3, 1)} mm"},
                {"name": "pitch: critical vision delay (canal 10 ms, nominal gain)", "result": json.dumps(s["pitch_crit_vision_delay_s_tc0.01_nominal_gain"])},
                {"name": "pitch: critical common vestibular delay (otolith + canal)", "result": json.dumps(s["pitch_crit_common_delay_s_otolith_nominal_gain"])},
                {"name": "passively pitch-stable static margins", "result": f"{_f(s['passive_pitch_stable_sm_range'][0] * 100, 0)} to {_f(s['passive_pitch_stable_sm_range'][1] * 100, 0)} % MAC (swept -10 to 30)"},
                {"name": "roll, 25 g, dihedral 7, k_v 0.15", "result": f"critical vision delay {s['roll_crit_vision_delay_s_tc0.01'].get('25g_G7_kv0.15')} s; otolith-only loop stable: {s['roll_otolith_stable_tc0.01'].get('25g_G7_kv0.15')}; open loop unstable: {s['roll_openloop_unstable'].get('25g_G7_kv0.15')}"}]
    if rid in ("j1-m1-sobol", "j4-m3-sobol"):
        return [{"name": k, "result": f"mean {_f(v['mean'], 3)}; largest total indices: " + ", ".join(f"{n} {st:.2f} [{lo:.2f}-{hi:.2f}]" for n, st, (lo, hi), _ in v["top_ST"][:4])}
                for k, v in s.items() if isinstance(v, dict) and "top_ST" in v]
    if rid in ("j2-m3-atlas", "j3-m5-mcell"):
        return [{"name": k, "result": json.dumps(v)[:400]} for k, v in s.items() if isinstance(v, dict)]
    return []


def build_cards(read, publish_media):
    text = json.loads(read("engineering/neuro/cards.json"))
    src = json.loads(read("engineering/neuro/sources.json"))["sources"]
    cards = []
    for rid in RIDS:
        d = f"artifacts/neuro/{rid}"
        try:
            rr = json.loads(read(f"{d}/run_receipt.json")); raw = read(f"{d}/manifest.json")
        except (FileNotFoundError, OSError, KeyError):
            continue
        if rr.get("exit_code") != 0 or sha256(raw).hexdigest() != rr.get("manifest_sha256"):
            continue
        m = json.loads(raw); t = text[rid]
        st, ph = publish_media(rid, "figure.png", m["outputs"].get("figure.png"))
        cards.append({"id": "neuro-" + rid, "title": m["title"], "scales": [m["project_scale"]] + m.get("also_scales", []), "evidence_kind": m["evidence_kind"],
                      "model": {"name": t["model_name"], "context": t["context"]},
                      "time": {"units": t["time_units"], "note": f"seed {m['seed']}; ran {m['ran']['utc']}; {m['elapsed_s']:.0f} s CPU wall; command {rr['command']} (exit {rr['exit_code']})"},
                      "video": {"file": None, "sha256": None, "note": ""}, "video_state": "none", "poster_href": ph, "poster_is_figure": True,
                      "numerical_checks": [{"name": c["name"], "result": "passed" if c["pass"] else "FAILED"} for c in m["checks"]] + findings(rid, m),
                      "parameter_unknowns": t["parameter_unknowns"], "open_questions": t["open_questions"], "equations": t["equations"],
                      "sources": [{"label": k, "locator": f"{src[k]['cite']}; {src[k].get('doi', '')}; read level {src[k]['level']}"} for k in t["sources"] if k in src],
                      "perturbation_sweep": t["perturbation_sweep"], "experiment_design": t["experiment_design"], "does_not_establish": t["does_not_establish"],
                      "limitations": t["does_not_establish"], "couplings": t.get("couplings", []), "manifest": f"{d}/manifest.json", "native": True})
    return cards
