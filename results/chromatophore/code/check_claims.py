"""Check every prose claim that quotes one of our own numbers against the file
that computed it.

WHY THIS EXISTS. Three times in one afternoon a sentence in `routes.json` or
`NOTES.md` quoted a number that one of the result files had since recomputed, and
nothing failed:

  * `org-lamella-pair-count` said 8 -> 9 lamella pairs buys "13%" of gamut; the
    sweep in `optical-gamut.json` says 15%.
  * Two routes compared engineering devices against "117-150 ms" as though it were
    an actuator time, after `actuator-mechanics.json` had established that it is a
    from-flash figure containing 50-67 ms of latency the model does not simulate.
  * `NOTES.md` and `routes.json` both said "about fifteen routes" were downstream
    of the transgene step, where the computed count is ten.

The shape is always the same: **a prose claim about our own data, sitting in a
different file from the data.** Code has callers, a number in a JSON has whatever
recomputed it, but a sentence has nobody. This binds them: each claim names a
literal string that must appear in a file, AND a function that recomputes the value
it asserts. If the prose is edited away, the claim fails as missing. If the model
is rerun and the number moves, the claim fails as stale. Either side drifting is a
failure, which is the point - a one-sided check would let the prose rot quietly.

It is deliberately a small hand-maintained table and not a general number scraper.
A scraper over all numerals in these files flags hundreds of legitimate citations
of other people's measurements, which is the false-positive rate that gets a check
switched off.

Usage:  python3 code/check_claims.py   ->  exit 0 if every claim holds.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_cache: dict[str, object] = {}


def load(name):
    if name not in _cache:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            return None
        if name.endswith(".json"):
            _cache[name] = json.load(open(path))
        else:
            _cache[name] = open(path).read()
    return _cache[name]


def route(rid):
    d = load("routes.json")
    for r in d["routes"]:
        if r["id"] == rid:
            return " ".join(str(r.get(k, "")) for k in
                            ("intervention", "predicted_phenotype", "mechanism",
                             "difficulty", "reversibility", "lethality_risk"))
    raise KeyError(rid)


def close(a, b, tol):
    return abs(a - b) <= tol


def norm(t: str) -> str:
    """Collapse whitespace and strip Markdown emphasis before matching.

    A literal substring test is brittle to re-wrapping: the first run of this
    checker reported "52% of the skin" MISSING from NOTES.md when the file said
    exactly that, with a line break between "of" and "the". That is the same
    failure that cost another agent four numbers to em-dash mismatches today. The
    check still fails if the claim is edited away or its number changed - it just
    does not fail when a paragraph is re-flowed or a phrase is bolded.
    """
    t = t.replace("\u2013", "-").replace("\u2014", "-").replace("\u00d7", "x")
    t = t.replace("**", "").replace("*", "").replace("`", "")
    return re.sub(r"\s+", " ", t)


# Each claim: (id, where the text lives, the literal text, what it should equal)
CLAIMS = []


def claim(cid, where, text, compute, expect, tol, unit=""):
    CLAIMS.append(dict(id=cid, where=where, text=text, compute=compute,
                       expect=expect, tol=tol, unit=unit))


# ---- claims about optical-gamut.json -------------------------------------
def g():
    return load("optical-gamut.json")


claim("lamella-pairs-gain", "routes:org-lamella-pair-count",
      "raises the achievable gamut area by 15%",
      lambda: (lambda rows: rows[9] / rows[8])(
          {r["n_pairs"]: r["hull_area_upvp"] for r in g()["sweeps"]["lamella_pair_count"]}),
      1.15, 0.01, "x")
claim("leucophore-chromaticity", "routes:org-leucophore-backing",
      "gamut area moves by 0%",
      lambda: g()["gamut"]["no_leucophore"]["gamut_relative_to_full"], 1.00, 0.005, "x")
claim("leucophore-luminance", "routes:org-leucophore-backing",
      "peak luminance falls by a factor of five",
      lambda: g()["gamut"]["full"]["Y_max"] / g()["gamut"]["no_leucophore"]["Y_max"],
      5.0, 0.8, "x")
claim("index-contrast", "routes:mol-reflectin-index-engineering",
      "contrast of only 1.048",
      lambda: 1.405 / 1.34, 1.048, 0.001, "")
claim("bragg-frozen-loss", "NOTES.md", "costs 88%",
      lambda: 1 - g()["gamut"]["bragg_fixed_at_live_mean"]["gamut_relative_to_full"],
      0.88, 0.01, "")
claim("retracted-coverage", "NOTES.md", "52% of the skin",
      lambda: g()["derived"]["coverage_retracted"], 0.52, 0.01, "")

# ---- claims about actuator-mechanics.json --------------------------------
def a():
    return load("actuator-mechanics.json")


claim("eight-fibre-ratio", "routes:cell-add-radial-muscles",
      "rises from 1.62 at 8 fibres",
      lambda: a()["sweeps"]["muscle_number"][0]["area_ratio"], 1.62, 0.01, "x")
claim("soft-sacculus-saturates", "routes:org-soften-the-sacculus",
      "saturated at 2.56",
      lambda: a()["sweeps"]["sacculus_elasticity"][0]["area_ratio"], 2.56, 0.01, "x")
claim("soft-sacculus-retraction", "routes:org-soften-the-sacculus",
      "from 295 ms to 543 ms",
      lambda: [r for r in a()["sweeps"]["sacculus_elasticity"]
               if abs(r["G_relative_to_fit"] - 0.5) < 1e-9][0]["retraction_time_90pct_ms"],
      542.65, 1.0, "ms")
claim("stiff-sacculus-tradeoff", "routes:org-soften-the-sacculus",
      "retraction falls to 120 ms and the ratio collapses to 1.32",
      lambda: [r for r in a()["sweeps"]["sacculus_elasticity"]
               if abs(r["G_relative_to_fit"] - 4.0) < 1e-9][0]["retraction_time_90pct_ms"],
      120.2, 1.0, "ms")
claim("rise-miss-factor", "NOTES.md", "2.8-3.5x",
      lambda: a()["control"]["comparisons"]["rise_time_ms"]["model_over_measured"][0],
      2.80, 0.05, "x")
claim("hadji-asymmetry", "NOTES.md", "3.70",
      lambda: a()["control"]["comparisons"]["retraction_vs_expansion_asymmetry"]
      ["measured"]["hadjisolomou_2021_region_matched_phases"], 3.696, 0.01, "")
# NOT a claim about asymmetry_max: that value is window-limited, not physical.
claim("damping-crossing-is-interior", "NOTES.md",
      "crosses 1.0 at **c = 0.1**",
      lambda: a()["control"]["damping_sweep_reach"]["smallest_c_with_asymmetry_above_one"],
      0.1, 0.001, "N.s/m")
claim("unreturned-points-recorded", "NOTES.md", "never returned were never removed",
      lambda: float(a()["control"]["damping_sweep_reach"]
                    ["points_where_the_organ_never_returned_within_the_window"] > 0),
      1.0, 0.0, "")

# ---- claims about routes.json's own validation ---------------------------
claim("downstream-count", "NOTES.md", "other ten are downstream",
      lambda: float(len(load("routes.json")["validation"]
                        ["cephalopod_routes_nobody_can_take"]
                        ["downstream_of_the_transgene_step"])), 10.0, 0.0, "routes")
claim("ceph-scale-count", "NOTES.md", "**30** cephalopod-scale routes",
      lambda: float(load("routes.json")["validation"]
                    ["cephalopod_routes_nobody_can_take"]["cephalopod_scale_routes"]),
      30.0, 0.0, "routes")


# ---- claims about control-channels.json (skipped until it exists) --------
def cc():
    return load("control-channels.json")


if cc() is not None:
    claim("animal-channels-per-actuator", "NOTES.md",
          "754/1829 = 0.412 channels per actuator",
          lambda: cc()["results"]["where_the_real_animal_sits"]["channels_per_actuator"],
          754 / 1829, 1e-9, "")
    claim("animal-past-the-knee", "NOTES.md", "past the knee, by 2.78",
          lambda: cc()["results"]["where_the_real_animal_sits"]["animal_over_knee_range"][0],
          2.78, 0.01, "x")
    claim("knee-grid-neighbours", "NOTES.md",
          "between 306 and 1094, nearest grid point 579",
          lambda: float(cc()["results"]["headline"]["knee95_mean_channels"]),
          579.0, 0.5, "channels")
    claim("coverage-breaks-at-large-units", "NOTES.md", "5.41",
          lambda: cc()["results"]["knee_is_set_by_coverage_not_complexity"]
          ["per_unit_size"]["30"]["ratio_knee_to_K_over_m"], 5.41, 0.01, "x")


def assert_entrypoint_guard_is_last():
    """Fail loudly if anything is defined after the `__main__` guard.

    This file's own `selftest()` was appended AFTER the guard and was therefore
    unreachable when the file was run - the identical mistake that had, an hour
    earlier, thrown away a completed 63-minute sweep in `control_channels.py` by
    appending `run_controls` after that file's guard. Remembering the lesson did
    not prevent the repeat, so it is enforced structurally instead: the guard must
    be the last top-level statement in the file, checked by parsing this file's own
    source. Put the guard last, always, as a layout rule rather than a thing to
    recall.
    """
    import ast as _ast
    tree = _ast.parse(open(os.path.abspath(__file__)).read())
    guards = [i for i, n in enumerate(tree.body)
              if isinstance(n, _ast.If) and _ast.dump(n.test).find("__main__") >= 0]
    if not guards:
        raise AssertionError("no `if __name__ == '__main__'` guard found")
    last_guard = guards[-1]
    trailing = [type(n).__name__ + ":" + getattr(n, "name", "")
                for n in tree.body[last_guard + 1:]]
    if trailing:
        raise AssertionError(
            "these top-level statements come AFTER the __main__ guard and are "
            f"unreachable when this file is run: {trailing}")
    return {"check": "entrypoint_guard_is_last", "passed": True,
            "top_level_statements": len(tree.body),
            "guard_index": last_guard}


# --- the six per-target ceilings -------------------------------------------
# Bound because the PUBLISHED PAGE hand-types three of these figures, and nothing
# downstream of this file recomputes them. Each recomputes from the raw sweep rows
# rather than from control-channels.json, so the check is independent of the
# analysis code that wrote that file.
CEILING_AT_NK = {"edge": 0.9708, "square": 0.9611, "stripes_coarse": 0.9578,
                 "mottle": 0.9503, "gravel_1f": 0.8970, "stripes_fine": 0.6439}
CEILING_EXCLUDED_ROWS = 140


def _ceiling_at_NK(target):
    """Mean r2 at n = K, compact wiring, m = 9, over seeds.

    DEFINED AS THE VALUE AT n = K, not the maximum anywhere in the sweep. The two
    differ by up to 0.0054 (gravel_1f 0.8970 vs 0.9024), enough that a claim bound
    to one and prose written from the other would look like drift.

    Excludes the rows whose r2 is None - the two zero-variance uniform targets,
    140 of 560 at m=9 compact. Not filtering them raises TypeError; coercing them
    silently changes the answer.
    """
    import statistics as _st
    raw = load("control-channels-raw.json")
    vals = [r["r2_blurred"] for r in raw["rows"]
            if r["wiring"] == "compact" and r["m"] == 9
            and r["target"] == target and r["n_chan"] == raw["K"]
            and isinstance(r["r2_blurred"], (int, float))]
    return _st.mean(vals)


def _excluded_row_count():
    raw = load("control-channels-raw.json")
    return float(sum(1 for r in raw["rows"]
                     if r["wiring"] == "compact" and r["m"] == 9
                     and not isinstance(r["r2_blurred"], (int, float))))


if load("control-channels-raw.json") is not None:
    for _t, _v in CEILING_AT_NK.items():
        claim(f"ceiling-{_t.replace('_', '-')}", "NOTES.md", f"| {_t} | {_v:.4f} |",
              (lambda t=_t: _ceiling_at_NK(t)), _v, 5e-5, "")
    claim("ceiling-excluded-rows", "NOTES.md",
          "140 rows are excluded from these means and must be",
          _excluded_row_count, float(CEILING_EXCLUDED_ROWS), 0.0, "rows")


def main():
    text_cache = {}
    rows, bad = [], 0
    for c in CLAIMS:
        where = c["where"]
        if where.startswith("routes:"):
            blob = route(where.split(":", 1)[1])
        else:
            blob = load(where)
        if blob is None:
            rows.append({**{k: c[k] for k in ("id", "where", "text")},
                         "status": "SKIPPED - file absent"})
            continue
        present = norm(c["text"]) in norm(blob)
        try:
            got = float(c["compute"]())
            numeric_ok = close(got, c["expect"], c["tol"])
        except Exception as exc:                            # noqa: BLE001
            got, numeric_ok = None, False
            print(f"  {c['id']}: compute failed: {exc!r}")
        ok = present and numeric_ok
        bad += 0 if ok else 1
        rows.append({"id": c["id"], "where": where, "text": c["text"],
                     "text_present": present, "computed": got,
                     "asserted": c["expect"], "tolerance": c["tol"],
                     "unit": c["unit"], "passed": bool(ok)})
    for r in rows:
        if "passed" not in r:
            print(f"SKIP {r['id']}: {r['status']}")
            continue
        mark = "ok  " if r["passed"] else "FAIL"
        got = "n/a" if r["computed"] is None else f"{r['computed']:.4g}"
        print(f"{mark} {r['id']:30s} {r['where']:42s} "
              f"text={'yes' if r['text_present'] else 'MISSING':7s} "
              f"computed={got:>8s} asserted={r['asserted']:.4g}{r['unit']}")
    print(f"\n{len(rows)} claims, {bad} failing")
    return rows, bad




def selftest():
    """A check whose subject includes the check is not a check. Prove this one
    flags BOTH directions of drift before trusting a clean run."""
    import copy
    results = []

    # (1) the number moves in the result file, prose unchanged -> must FAIL
    saved = copy.deepcopy(CLAIMS)
    target = next(c for c in CLAIMS if c["id"] == "eight-fibre-ratio")
    target["compute"] = lambda: 9.99
    _, bad_a = main()
    results.append(("number drifts in the result file", bad_a > 0))
    CLAIMS[:] = saved

    # (2) the prose is edited away, number unchanged -> must FAIL
    saved = copy.deepcopy(CLAIMS)
    target = next(c for c in CLAIMS if c["id"] == "eight-fibre-ratio")
    target["text"] = "a sentence that is not in any of these files"
    _, bad_b = main()
    results.append(("prose is edited away", bad_b > 0))
    CLAIMS[:] = saved

    # (3) nothing perturbed -> must PASS
    _, bad_c = main()
    results.append(("unperturbed", bad_c == 0))

    print("\n--- self test ---")
    for name, ok in results:
        print(f"{'ok  ' if ok else 'FAIL'} {name}")
    return all(ok for _, ok in results)


def cli():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true",
                    help="perturb a value and then a claim's prose, and require the "
                         "checker to fail in each case before trusting a clean run")
    args = ap.parse_args()
    layout = assert_entrypoint_guard_is_last()
    print(f"layout guard: the __main__ guard is the last of "
          f"{layout['top_level_statements']} top-level statements - ok\n")
    if args.selftest:
        ok = selftest()
        print(f"\nSELFTEST {'PASSED' if ok else 'FAILED'}")
        return 0 if ok else 1
    _, failures = main()
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(cli())
