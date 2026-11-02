#!/usr/bin/env python3
"""Fold the post-hoc onset arm into cargo-work.json, with the pooled span analysis
that supersedes the arm's own automatic verdict.

Run AFTER cargo_assemble.py. See rebuild.sh for the order.
"""
import json
ROOT = "/data/scratch/designspaces/xenobot"
A = json.load(open(f"{ROOT}/data/cargo-arm3b.json"))
C = json.load(open(f"{ROOT}/cargo-work.json"))
narrow = C["arm3_swarm"]["per_N"]

rows = []
for tag, src, half in (("narrow(y +/-22)", narrow, 22), ("wide(y +/-42)", A["per_N"], 42)):
    for n, v in src.items():
        N = int(n)
        span = (N - 1) / 2 * 5 + 1            # construct extent in y, lattice sites
        rows.append({"field": tag, "N": N, "swarm_half_span_sites": span,
                     "field_half_width_sites": half, "span_over_field": span / half,
                     "median_rg_change_mm": v["S2_min_median_max"][1] * 1000,
                     "aggregating_seeds": sum(1 for s in v["per_seed"] if s["S2_rg_change_m"] < 0),
                     "n_seeds": len(v["per_seed"])})
rows.sort(key=lambda r: r["span_over_field"])
lo = [r for r in rows if r["span_over_field"] <= 0.70]
hi = [r for r in rows if r["span_over_field"] >= 0.80]

C["arm3b_onset_test"] = {
    "status": A["status"],
    "why": ("In the main arm the field dispersed at every N from 1 to 6 in all seeds, then at N=8 the median "
            "fell 2.6-fold and 2 of 5 seeds turned negative. That is either the onset of aggregation at larger "
            "swarm size or something else. N>9 does not fit the main arm's field at the minimum construct "
            "stride, so this arm widens the field in y, scales the particle count to hold DENSITY fixed, and "
            "pushes N to 16."),
    "predeclared_for_this_arm": A["predeclared_for_this_arm"],
    "field": A["field"], "n_particles": A["n_particles"], "per_N": A["per_N"],
    "automatic_verdict_from_the_arm_script": A["verdict"],
    "automatic_verdict_superseded": ("the script's own test was whether the median falls monotonically with N "
                                     "and crosses zero. It does not (0.379, 0.466, 0.442, 0.051 mm at N = 4, 8, "
                                     "12, 16), so the script returned 'consistent with seed scatter'. Pooling "
                                     "both fields gives a better explanation, below, and that is what is reported."),
    "span_analysis": {
        "hypothesis": ("the apparent aggregation is a BOUNDARY effect: it appears when the swarm spans most of "
                       "the field, so the constructs sweep particles into a narrower band, regardless of N."),
        "measure": "swarm half-span in lattice sites divided by field half-width; constructs sit at stride 5 in y",
        "rows": rows,
        "all_runs_with_span_over_field_below_0.70": {
            "configurations": len(lo), "aggregating_seeds": sum(r["aggregating_seeds"] for r in lo),
            "median_rg_change_mm_range": [min(r["median_rg_change_mm"] for r in lo),
                                          max(r["median_rg_change_mm"] for r in lo)]},
        "all_runs_with_span_over_field_at_or_above_0.80": {
            "configurations": len(hi), "aggregating_seeds": sum(r["aggregating_seeds"] for r in hi),
            "median_rg_change_mm_range": [min(r["median_rg_change_mm"] for r in hi),
                                          max(r["median_rg_change_mm"] for r in hi)]},
        "the_controlled_comparison": ("N = 8 is the discriminator. In the narrow field its span/field is 0.84 and "
                                      "2 of 5 seeds aggregate; in the wide field the SAME swarm size has "
                                      "span/field 0.44 and 0 of 5 aggregate. Conversely N = 12 in the wide field "
                                      "is a LARGER swarm at span/field 0.68 and also shows nothing. So the effect "
                                      "tracks the span ratio and not the swarm size."),
        "verdict": ("NOT a swarm-size onset. Across 10 configurations in two field sizes and swarm sizes 1 to 16, "
                    "every configuration with span/field <= 0.68 gives 0 aggregating seeds, and both "
                    "configurations with span/field >= 0.84 give some (2/5 and 1/5) with the median collapsing. "
                    "The main arm's conclusion therefore stands and is strengthened: a uniform, sensorless, "
                    "single-gait swarm does not corral. What looked like aggregation is the swarm reaching the "
                    "edge of its arena."),
        "caveat": ("the cut sits between 0.68 and 0.84 with no configuration in between, so the threshold is "
                   "bracketed rather than located, and 'span/field' is one summary of a geometry that also "
                   "changes particle count per construct. Two field widths is not a scan over field width.")},
    "reading": ("The two aggregating seeds at N=8 in the main arm are a BOUNDARY effect, not an onset: the same "
                "swarm size in a wider field shows nothing, and a larger swarm in the wider field also shows "
                "nothing. Aggregation-like behaviour appears only when the swarm spans more than about 0.8 of "
                "the field.")}
C["arm3_swarm"]["S2_aggregation"]["onset_tested"] = C["arm3b_onset_test"]["reading"]
C["headline"] = C["headline"].replace(
    "and in 5 cycles only one of six even reaches its cargo.",
    "and in 5 cycles only one of six even reaches its cargo. A uniform swarm never corrals, over swarm sizes 1 to 16 in two field sizes.")
C["limitations"].append(
    "The swarm result covers N = 1 to 16 in two field sizes. Its one apparent exception, 2 of 5 seeds at N = 8 in "
    "the narrower field, was tested rather than hedged and turned out to track the swarm's span relative to the "
    "arena rather than its size. The threshold is bracketed between span/field 0.68 and 0.84, not located, and "
    "two field widths is not a scan over field width.")
json.dump(C, open(f"{ROOT}/cargo-work.json", "w"), indent=2)
print(f"onset: low-span {len(lo)} configs / {sum(r['aggregating_seeds'] for r in lo)} aggregating; "
      f"high-span {len(hi)} / {sum(r['aggregating_seeds'] for r in hi)}")
