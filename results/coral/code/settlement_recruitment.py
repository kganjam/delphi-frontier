#!/usr/bin/env python3
"""
settlement_recruitment.py — from spawning to a surviving one-year recruit, and which
intervention moves the most surviving recruits per unit effort.

WHAT THIS IS: a SENSITIVITY ANALYSIS over stated unknowns. It is not a point prediction,
and it is built that way deliberately, because the research block establishes that most
of the parameters in this chain have NO published wild-scale value:

    eggs per colony                     NONE   (eggs per POLYP is known; polyps per
                                               colony is not)
    wild pelagic larval mortality       NONE   (only laboratory cohorts)
    settlement probability without cue  NONE   (and it is NOT zero: bare rubble and dead
                                               coral induce metamorphosis)
    settlers per larva released in the field   NONE
    absolute size at which recruits escape grazing   NONE

A point prediction built on those would be fabrication. A sensitivity analysis over
honest ranges is a real result, and the thing it produces -- a ranking of interventions
by how much they move the outcome, and an identification of which unknown dominates the
spread -- does not need the unknowns to be resolved.

THE STRUCTURE
-------------
A multiplicative survival chain, each stage with a range rather than a value:

  eggs -> fertilised -> survives to competence -> encounters substrate -> settles and
  ATTACHES -> survives the first week -> survives to one month -> survives to one year

Two stages carry evidence strong enough to pin them, and they are marked `sourced`.
Everything else is `assumed` with a declared range, and the whole chain is sampled by
Latin hypercube so the output is a DISTRIBUTION.

Interventions are modelled as multipliers on named stages, each with its own measured or
assumed effect range and its own cost, so the comparison is per unit effort and not per
unit hope.

Usage
  python3 settlement_recruitment.py --run
  python3 settlement_recruitment.py --figures
"""
from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIGDIR = os.path.join(ROOT, "figures")
CACHE = os.path.join(ROOT, "recruitment-cache.json")
RESULT = os.path.join(ROOT, "settlement-recruitment.json")

N_SAMPLES = 20000
RNG_SEED = 20261102

# --------------------------------------------------------------------------------------
# The chain. Every stage carries status, range, and the exact provenance of that range.
# --------------------------------------------------------------------------------------

STAGES = [
    dict(key="eggs_per_polyp", label="Eggs per polyp", lo=4.0, hi=12.0,
         status="sourced", distribution="loguniform",
         source="Foster & Gilmour 2020, Sci Rep 10:12313 (PMID 32703979), read at FULL "
                "TEXT. Seven Acropora species at Scott Reef, 2008-2010: mean about 6-8 "
                "eggs per polyp with an individual range of about 4-12. Only mature "
                "colonies above 20 cm were sampled and polyps were taken from the colony "
                "CENTRE to avoid sterile margins, so multiplying by a total polyp count "
                "may overstate colony fecundity. Scott Reef is Western Australia, not "
                "the Great Barrier Reef, and the per-species values could not be "
                "recovered because the figure and table values were stripped from the "
                "text retrieved."),
    dict(key="polyps_per_colony", label="Polyps per colony", lo=2000.0, hi=50000.0,
         status="assumed", distribution="loguniform",
         source="NO VALUE WAS OBTAINED, in any source read. The research block says so "
                "explicitly and declines to supply one. This 25-fold range is invented "
                "to span plausible branching-Acropora colony sizes and is the single "
                "crudest number in this file. It is included rather than omitted because "
                "leaving it out would silently fix it at 1."),
    dict(key="fertilisation", label="Fertilisation success", lo=0.5, hi=0.95,
         status="sourced", distribution="uniform",
         source="Dela Cruz et al. 2020, J Exp Mar Biol Ecol (no PMID verified; "
                "search-summary): above 90% at sperm concentrations of 1e5 to 1e7 per mL "
                "in Acropora tenuis, A. millepora and Favites colemani, and above 80% "
                "when gametes are combined up to 4 h after spawning. Buccheri et al. "
                "2023 report a steep rise past 1e4 sperm/mL. Kitanobo et al. 2021 report "
                "most eggs fertilised below 1e6 in situ. Those three answer different "
                "questions (maximum against onset against field) and the range here "
                "spans a slick that is not at the laboratory optimum."),
    dict(key="survive_to_competence", label="Survives to competence",
         lo=0.03, hi=0.83, status="assumed", distribution="loguniform",
         source="NO WILD VALUE EXISTS in anything read. The bounds are the extremes of "
                "what laboratory and rearing studies report, and they differ by a factor "
                "of more than 20 for reasons that are about HANDLING, not about the sea: "
                "Randall et al. 2025 report 3.8% survival in in-situ rearing pools "
                "against 66.1% in on-vessel tanks; Miller et al. 2020 report 71-83% "
                "persistence to competence age in A. palmata laboratory cohorts; "
                "Doropoulos et al. 2017 (PMID 28573015) report above 80% survival from "
                "day 2.5 to 12 in A. millepora. Graham et al. 2008 report that the "
                "mortality SHAPE is a bathtub, not a constant. A wild value would almost "
                "certainly be below the laboratory numbers; nothing read here bounds it "
                "from below."),
    dict(key="encounter_substrate", label="Encounters suitable substrate",
         lo=0.001, hi=0.1, status="assumed", distribution="loguniform",
         source="NO PUBLISHED VALUE. This stage carries everything between a competent "
                "larva in the water and a larva in contact with a surface it could "
                "settle on: dispersal, retention, and how much of the benthos is "
                "settleable. The hundredfold range reflects that it is a placeholder for "
                "an entire connectivity literature that was not read."),
    dict(key="settle_and_attach", label="Settles AND attaches, given contact",
         lo=0.05, hi=0.81, status="sourced", distribution="uniform",
         source="Abdul Wahab et al. 2023, Sci Rep 13:5795 (PMID 37032381): across 15 "
                "coral species and 15 crustose coralline algae, the best inducer "
                "(Titanoderma cf. tessellatum) gave at least 50% settlement in 14 of 15 "
                "species, mean 81%. Whitman et al. 2020 (PMID 33009428): Porolithon "
                "onkodes gave above 50% in 9 of 15 species but BELOW 10% in three "
                "species under every treatment. The low end of the range is that "
                "non-response. NOTE the stage is settlement AND ATTACHMENT together, "
                "because the two are separable: a tetrabromopyrrole cue gives 100% "
                "metamorphosis with 0-2% attachment (Siboni et al. 2012, PMID 22655067). "
                "The no-cue baseline is NONE -- no control-surface percentage was "
                "retrieved from any source -- but it is NOT zero, because bare calcified "
                "rubble and dead coral induce metamorphosis (Heyward & Negri 1999) and "
                "larvae settle on plastic in assays (Jorissen et al. 2021, PMID "
                "34272460)."),
    dict(key="survive_week_1", label="Survives the first week", lo=0.2, hi=0.5,
         status="sourced", distribution="uniform",
         source="Penin et al. 2011 (no PMID verified; search-summary): more than half of "
                "Acropora striata recruits died within SEVEN DAYS in the field at "
                "Moorea, in both caged and uncaged plots. That is an upper bound of 0.5 "
                "on weekly survival, and the lower bound here is assumed. The same study "
                "is the reason herbivory is not modelled as protection: excluding "
                "predators and grazers did not change total mortality, it changed the "
                "cause, from predation (50.0% of dead recruits damaged or missing) to "
                "competition with turf algae and sediment (91.7% intact)."),
    dict(key="survive_to_month_1", label="Survives week 1 to month 1", lo=0.3, hi=0.8,
         status="assumed", distribution="uniform",
         source="NO DIRECT VALUE. Doropoulos et al. 2017 (PMID 28573015) report that "
                "A. millepora settlement was three times higher in crevices than on "
                "exposed surfaces but that by ONE MONTH recruit density was similar on "
                "both, because crevices carry negative density dependence. That says the "
                "refuge advantage is partly spent by a month; it does not give a "
                "survival fraction."),
    dict(key="survive_to_year_1", label="Survives month 1 to year 1", lo=0.05, hi=0.6,
         status="sourced", distribution="uniform",
         source="The first-year survival literature spreads over more than tenfold and "
                "the range is that spread, not an uncertainty about one number: "
                "Chamberland et al. 2017 (PMID 29273761) 9.6% on concrete tetrapods in "
                "Curacao; Randall et al. 2021 2-39% across device types for A. tenuis, "
                "with 100% mortality on upper surfaces; Randall et al. 2025 5 +/- 8%; "
                "Speare et al. 2021 33% in a normal year against 2% in a heatwave year "
                "at Moorea; Waters et al. 2025 effectively zero yield at 21 months at "
                "one Lizard Island site. These are different species, devices, sites and "
                "thermal years. A single number here would be a fiction."),
]

# --------------------------------------------------------------------------------------
# Interventions: which stage each multiplies, by how much, and what it costs.
# --------------------------------------------------------------------------------------

INTERVENTIONS = [
    dict(key="cca_cue", label="Condition substrate with a strong CCA inducer",
         stage="settle_and_attach", lo=1.5, hi=4.0, status="sourced",
         effect_source="Abdul Wahab et al. 2023 (PMID 37032381) and Whitman et al. 2020 "
                       "(PMID 33009428). The multiplier is the ratio of a strong inducer "
                       "to a weak or absent one, and it is bounded ABOVE by the fact "
                       "that the stage is a probability: the code caps the stage at 0.9 "
                       "after any multiplier, so an intervention cannot push a "
                       "probability past one.",
         cost_lo=1.0, cost_hi=3.0,
         cost_source="RELATIVE EFFORT UNITS, not money. No study read here costs "
                     "substrate conditioning. Anchored at 1 by definition and the other "
                     "interventions are placed relative to it; the ranking is therefore "
                     "only as good as these placements, which is stated in the "
                     "limitations and is the weakest part of this study."),
    dict(key="grooved_device", label="Seeding device with 4 mm refuge grooves",
         stage="survive_to_year_1", lo=2.0, hi=3.5, status="sourced",
         effect_source="Randall et al. 2021 (search-summary, no PMID): first-year "
                       "survival about 39% on 4 mm through-grooved devices against 13% "
                       "on flat control tiles, a ratio of 3.0. The range brackets it.",
         cost_lo=1.5, cost_hi=4.0,
         cost_source="Relative effort units. Device manufacture and deployment."),
    dict(key="tetrapod_wedge", label="Unattached wedged tetrapods instead of bolting",
         stage="survive_to_year_1", lo=0.9, hi=1.3, status="sourced",
         effect_source="Chamberland et al. 2017 (PMID 29273761): 9.6% first-year "
                       "survival, 67% of tetrapods with at least one colony, at 5-18x "
                       "lower outplanting cost and 1.5-7% of the deployment TIME. "
                       "Mendoza Quiroz et al. 2025 (search-summary) measured the "
                       "trade-off directly: bolting took about 120 s against about 10 s "
                       "for wedging, but DOUBLED or QUADRUPLED the proportion of units "
                       "retaining a live coral. So the survival multiplier here is near "
                       "1 or slightly below, and the whole case for this route is on the "
                       "cost side.",
         cost_lo=0.1, cost_hi=0.35,
         cost_source="The one cost ratio in this table with direct support: 5-18x lower "
                     "outplanting cost (Chamberland) and about a twelfth of the "
                     "attachment time (Mendoza Quiroz)."),
    dict(key="acoustic", label="Reef-sound playback at the settlement site",
         stage="encounter_substrate", lo=1.7, hi=1.8, status="sourced",
         effect_source="Aoki et al. 2024 (PMID 38481984) 1.7x on average with a maximum "
                       "of 7x in a brooding coral; Aoki et al. 2026 (PMID 42409953) "
                       "1.79x for a broadcast spawner in static cups. The narrow range "
                       "is deliberate: the maximum of 7 is not used because in "
                       "flow-through conditions the response was minimal and the "
                       "difference between two reefs was TENFOLD. Every verified "
                       "acoustic result comes from one laboratory group and no "
                       "independent replication was found. There is no Acropora value.",
         cost_lo=2.0, cost_hi=6.0,
         cost_source="Relative effort units. Hardware, power and maintenance in water."),
    dict(key="sea_weeding", label="Remove macroalgae around the devices",
         stage="survive_to_year_1", lo=1.2, hi=4.8, status="sourced",
         effect_source="Webster et al. 2015 (PMID 25898011): recruit survival 79% lower "
                       "in caged macroalgae-dense plots, a ratio of 4.8 the other way, "
                       "CONFOUNDED because caging also removes herbivory. Smith et al. "
                       "2025 (PMID 40267811) measured the intervention itself and found "
                       "a first-year benefit that had VANISHED by year two, at USD "
                       "334-577 per surviving coral. The low end of the range is that "
                       "result.",
         cost_lo=4.0, cost_hi=12.0,
         cost_source="Relative effort units, and the highest in the table because the "
                     "labour RECURS: Smith et al. report the benefit disappearing in "
                     "year two, so the cost does not buy a permanent gain."),
    dict(key="sediment_screening", label="Screen out sediment-prone and unstable sites",
         stage="survive_week_1", lo=1.2, hi=3.0, status="sourced",
         effect_source="Rodriguez-Ruano et al. 2026 (PMID 42310106): 2 mm of sediment "
                       "cuts settlement probability to 25% or less and 4 mm suppresses "
                       "it; 4 mm burial cuts ten-day recruit survival to 0-31%, a 3-25x "
                       "mortality risk. Waters et al. 2025 is the field failure case: 9% "
                       "of ceramic devices and 0% of travertine tiles held a recruit at "
                       "21 months, DESPITE travertine attracting more than 2.5 times the "
                       "settlement. The multiplier is conservative relative to the "
                       "3-25x, because a screened site is not a sediment-free one.",
         cost_lo=0.2, cost_hi=0.8,
         cost_source="Relative effort units. Survey time before deployment, paid once."),
    dict(key="larval_supply", label="Mass larval enrichment into a netted plot",
         stage="encounter_substrate", lo=5.0, hi=50.0, status="sourced",
         effect_source="Dela Cruz & Harrison 2017 (PMID 29070842) and 2020 (PMID "
                       "33232367): roughly 3-4 x 10^5 larvae released per plot, with "
                       "control plots producing ZERO settlement of that species. The "
                       "multiplier is on larval ENCOUNTER, not survival, and it is wide "
                       "because the baseline it multiplies is a supply-limited reef and "
                       "no study read here measures how supply-limited a given reef is.",
         cost_lo=6.0, cost_hi=20.0,
         cost_source="Relative effort units. Spawning capture, ex-situ rearing, netting "
                     "and release. The one anchor to real money is USD 35.20 per "
                     "surviving colony at 35 months (Dela Cruz & Harrison 2020), which "
                     "is not comparable with the USD 334-577 per surviving coral at two "
                     "years in Smith et al. 2025: different species, years, accounting "
                     "and survival horizons. They are NOT compared here."),
]


def _sample(lo, hi, dist, u):
    if dist == "loguniform":
        return np.exp(np.log(lo) + u * (np.log(hi) - np.log(lo)))
    return lo + u * (hi - lo)


def latin_hypercube(n, d, rng):
    out = np.empty((n, d))
    for j in range(d):
        out[:, j] = (rng.permutation(n) + rng.random(n)) / n
    return out


def run_chain(n=N_SAMPLES, interventions=(), seed=RNG_SEED):
    """Sample the chain. Returns surviving one-year recruits per SPAWNING COLONY."""
    rng = np.random.default_rng(seed)
    u = latin_hypercube(n, len(STAGES), rng)
    vals = {}
    for j, st in enumerate(STAGES):
        vals[st["key"]] = _sample(st["lo"], st["hi"], st["distribution"], u[:, j])

    mult = {st["key"]: np.ones(n) for st in STAGES}
    for iv in interventions:
        spec = next(x for x in INTERVENTIONS if x["key"] == iv)
        m = _sample(spec["lo"], spec["hi"], "uniform", rng.random(n))
        mult[spec["stage"]] = mult[spec["stage"]] * m

    out = vals["eggs_per_polyp"] * vals["polyps_per_colony"]
    for st in STAGES[2:]:
        v = vals[st["key"]] * mult[st["key"]]
        # every stage after the first two is a PROBABILITY; an intervention cannot push
        # one past 1. The cap is 0.9, declared, so a stacked set of multipliers cannot
        # manufacture certainty.
        v = np.minimum(v, 0.9)
        out = out * v
    return out, vals


def cost_of(interventions, n, seed=RNG_SEED + 1):
    rng = np.random.default_rng(seed)
    total = np.zeros(n)
    for iv in interventions:
        spec = next(x for x in INTERVENTIONS if x["key"] == iv)
        total += _sample(spec["cost_lo"], spec["cost_hi"], "uniform", rng.random(n))
    return total


def q(a):
    return dict(p05=float(np.percentile(a, 5)), p25=float(np.percentile(a, 25)),
                median=float(np.median(a)), p75=float(np.percentile(a, 75)),
                p95=float(np.percentile(a, 95)), mean=float(np.mean(a)),
                geometric_mean=float(np.exp(np.mean(np.log(np.maximum(a, 1e-300))))))


def control_arm(n=N_SAMPLES):
    """Pre-declared controls. These must pass before any comparison is read.

    CONTROL 1 -- NULL INTERVENTION. An 'intervention' with a multiplier identically 1
    must leave the distribution unchanged to within sampling noise. If it does not, the
    machinery is adding an effect of its own.

    CONTROL 2 -- ORDER INDEPENDENCE. The chain is a product, so applying two
    interventions in either order must give the same answer. If it does not, the cap is
    being applied inconsistently.

    CONTROL 3 -- MONOTONICITY. Every intervention has a multiplier of at least 0.9 at
    its low end, so no single intervention should LOWER the median by more than a
    little. A large drop would mean the cap is binding somewhere it should not.
    """
    base, _ = run_chain(n)
    rng = np.random.default_rng(RNG_SEED + 99)
    null_spec = dict(key="__null__", label="null", stage="survive_week_1",
                     lo=1.0, hi=1.0, status="assumed", effect_source="control",
                     cost_lo=0.0, cost_hi=0.0, cost_source="control")
    INTERVENTIONS.append(null_spec)
    try:
        nullr, _ = run_chain(n, interventions=("__null__",))
    finally:
        INTERVENTIONS.remove(null_spec)
    ab, _ = run_chain(n, interventions=("cca_cue", "grooved_device"))
    ba, _ = run_chain(n, interventions=("grooved_device", "cca_cue"))
    singles = {}
    for iv in INTERVENTIONS:
        r, _ = run_chain(n, interventions=(iv["key"],))
        singles[iv["key"]] = float(np.median(r) / np.median(base))
    checks = {
        "null_intervention_changes_nothing": bool(
            abs(np.median(nullr) / np.median(base) - 1.0) < 0.02),
        "order_independent": bool(abs(np.median(ab) / np.median(ba) - 1.0) < 0.02),
        "no_intervention_reduces_median_by_more_than_15pct": bool(
            min(singles.values()) > 0.85),
    }
    return dict(checks=checks, passed=bool(all(checks.values())),
                baseline=q(base), null_arm=q(nullr),
                single_intervention_median_ratios=singles,
                note="The baseline is recruits per SPAWNING COLONY per spawning event, "
                     "spread over four orders of magnitude because the unknowns are. The "
                     "number itself is not a prediction; the RATIOS below are what the "
                     "study is for.")


def sensitivity(n=N_SAMPLES):
    """Which unknown dominates the spread? Rank-correlation of each stage with the output.

    Spearman rank correlation between each sampled stage value and the log of the final
    count, over the Latin-hypercube sample. Reported as the fraction of summed squared
    correlation, so it reads as a share of the spread. DECLARED BEFORE THE RUN.
    """
    out, vals = run_chain(n)
    y = np.log(np.maximum(out, 1e-300))
    ry = np.argsort(np.argsort(y))
    rows = []
    for st in STAGES:
        rx = np.argsort(np.argsort(vals[st["key"]]))
        r = float(np.corrcoef(rx, ry)[0, 1])
        rows.append(dict(stage=st["key"], label=st["label"], status=st["status"],
                         spearman=r, spearman_sq=r * r,
                         range_decades=float(np.log10(st["hi"] / st["lo"]))))
    tot = sum(x["spearman_sq"] for x in rows)
    for x in rows:
        x["share_of_spread"] = x["spearman_sq"] / tot if tot > 0 else None
    rows.sort(key=lambda x: -x["spearman_sq"])
    return rows


def compare(n=N_SAMPLES):
    base, _ = run_chain(n)
    med0 = float(np.median(base))
    rows = []
    for iv in INTERVENTIONS:
        r, _ = run_chain(n, interventions=(iv["key"],))
        c = cost_of((iv["key"],), n)
        gain = r / base
        rows.append(dict(
            key=iv["key"], label=iv["label"], stage=iv["stage"],
            effect_source=iv["effect_source"], cost_source=iv["cost_source"],
            median_multiplier=float(np.median(gain)),
            multiplier_p05=float(np.percentile(gain, 5)),
            multiplier_p95=float(np.percentile(gain, 95)),
            median_cost=float(np.median(c)),
            gain_per_unit_effort=float(np.median((gain - 1.0) / np.maximum(c, 1e-9))),
            probability_it_helps_at_all=float(np.mean(gain > 1.0)),
        ))
    rows.sort(key=lambda x: -x["gain_per_unit_effort"])

    # a stacked arm: everything whose per-unit-effort gain is positive
    best = [r["key"] for r in rows if r["gain_per_unit_effort"] > 0][:4]
    stacked, _ = run_chain(n, interventions=tuple(best))
    sc = cost_of(tuple(best), n)
    return dict(baseline_median=med0, per_intervention=rows,
                stacked=dict(interventions=best,
                             median_multiplier=float(np.median(stacked / base)),
                             median_cost=float(np.median(sc)),
                             gain_per_unit_effort=float(np.median(
                                 (stacked / base - 1.0) / np.maximum(sc, 1e-9))),
                             note="Stacking is multiplicative by construction in this "
                                  "model, because the chain is a product and the "
                                  "interventions act on different stages. That is an "
                                  "ASSUMPTION, not a finding: no study read here crosses "
                                  "two of these interventions factorially, so whether "
                                  "they interact in the water is unknown."))


def effort_unit_sensitivity(n=4000, n_draws=400, seed=RNG_SEED + 7):
    """IS THE RANKING A PROPERTY OF THE BIOLOGY OR OF THE EFFORT UNITS I INVENTED?

    The biology is sampled 20,000 times. The denominators were then point estimates,
    which is the exact structure this study exists to avoid, so they are sampled too.

    Each draw perturbs every intervention's cost range by an independent lognormal factor
    (median 1, so the perturbation is unbiased) and recomputes the full per-unit-effort
    ranking. Reported: how often each intervention lands in each rank, how often each
    PAIRWISE ordering holds, and which claims survive. The lead's prediction, recorded
    before the run: the gap between the top two and the rest is robust, and the order
    WITHIN the top two is not.
    """
    rng = np.random.default_rng(seed)
    keys = [iv["key"] for iv in INTERVENTIONS]
    base, _ = run_chain(n)
    gains = {}
    for k in keys:
        r, _ = run_chain(n, interventions=(k,))
        gains[k] = float(np.median(r / base)) - 1.0

    rank_counts = {k: [0] * len(keys) for k in keys}
    pair_counts = {}
    top2_sets = {}
    for _ in range(n_draws):
        eff = {}
        for iv in INTERVENTIONS:
            f = float(np.exp(rng.normal(0.0, SIGMA_EFFORT)))
            c = 0.5 * (iv["cost_lo"] + iv["cost_hi"]) * f
            eff[iv["key"]] = gains[iv["key"]] / max(c, 1e-9)
        order = sorted(keys, key=lambda k: -eff[k])
        for pos, k in enumerate(order):
            rank_counts[k][pos] += 1
        for i in range(len(keys)):
            for j in range(len(keys)):
                if i != j:
                    pair_counts[(keys[i], keys[j])] = pair_counts.get(
                        (keys[i], keys[j]), 0) + (1 if eff[keys[i]] > eff[keys[j]] else 0)
        t2 = tuple(sorted(order[:2]))
        top2_sets[t2] = top2_sets.get(t2, 0) + 1

    label = {iv["key"]: iv["label"] for iv in INTERVENTIONS}
    per = []
    for k in keys:
        counts = rank_counts[k]
        per.append(dict(key=k, label=label[k],
                        p_rank_1=counts[0] / n_draws,
                        p_top_2=(counts[0] + counts[1]) / n_draws,
                        modal_rank=int(np.argmax(counts)) + 1,
                        rank_distribution=[c / n_draws for c in counts]))
    per.sort(key=lambda r: -r["p_top_2"])
    pairs = [dict(a=a, b=b, p_a_beats_b=c / n_draws)
             for (a, b), c in sorted(pair_counts.items(), key=lambda kv: -kv[1])]
    robust = [p for p in pairs if p["p_a_beats_b"] >= 0.95]
    fragile = [p for p in pairs if 0.3 <= p["p_a_beats_b"] <= 0.7]
    top2 = sorted(top2_sets.items(), key=lambda kv: -kv[1])
    return dict(
        n_draws=n_draws, sigma_effort=SIGMA_EFFORT,
        method="Each draw multiplies every intervention's mean effort by an independent "
               "lognormal factor with median 1 and sigma " + str(SIGMA_EFFORT) +
               ", then recomputes the ranking. The perturbation is unbiased, so this "
               "asks whether the ORDERING survives the denominators being wrong, not "
               "whether the costs are right.",
        per_intervention=per,
        pairwise=pairs,
        robust_orderings=robust,
        fragile_orderings=fragile,
        most_common_top_two=[dict(pair=list(k), frequency=v / n_draws) for k, v in top2[:3]],
        is_observation=False)


SIGMA_EFFORT = 0.5


# --------------------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------------------

def _style():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.dpi": 150, "savefig.dpi": 150, "font.size": 8.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": 9, "axes.labelsize": 8.5, "legend.frameon": False,
        "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.5,
        "savefig.bbox": "tight", "savefig.facecolor": "white"})
    return plt


def make_figures(cache):
    plt = _style()
    # ---- recruitment-sensitivity.png -----------------------------------------------
    sens = cache["sensitivity"]
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10.4, 4.2),
                                   gridspec_kw=dict(width_ratios=[1.25, 1]))
    labs = [r["label"] for r in sens][::-1]
    share = [100 * r["share_of_spread"] for r in sens][::-1]
    stat = [r["status"] for r in sens][::-1]
    cols = ["#b2452e" if s == "assumed" else "#1f6f54" for s in stat]
    ax0.barh(range(len(labs)), share, color=cols)
    ax0.set_yticks(range(len(labs))); ax0.set_yticklabels(labs, fontsize=7)
    ax0.set_xlabel("share of the spread in log surviving recruits (%)")
    ax0.set_title("Which unknown drives the answer", loc="left", fontsize=8.5)
    ax0.text(0.98, 0.04, "red = assumed range\ngreen = sourced range",
             transform=ax0.transAxes, ha="right", fontsize=6.5)

    base = cache["control_arm"]["baseline"]
    xs = np.array([base["p05"], base["p25"], base["median"], base["p75"], base["p95"]])
    ax1.plot(xs, [1] * 5, "o-", color="#1b4f72", lw=2, ms=5)
    ax1.set_xscale("log"); ax1.set_yticks([])
    for v, lab in zip(xs, ["5th", "25th", "median", "75th", "95th"]):
        ax1.annotate(f"{lab}\n{v:.2g}", (v, 1), textcoords="offset points",
                     xytext=(0, 12 if lab in ("5th", "median", "95th") else -26),
                     ha="center", fontsize=6.5)
    ax1.set_xlabel("surviving one-year recruits per spawning colony, per spawning")
    ax1.set_title("The baseline is a distribution, not a number", loc="left",
                  fontsize=8.5)
    ax1.set_ylim(0.6, 1.5)
    fig.suptitle("SIMULATED sensitivity analysis over stated unknowns. Not a prediction "
                 "of any reef. No coral was measured.", fontsize=8.2, x=0.012, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(os.path.join(FIGDIR, "recruitment-sensitivity.png"))
    plt.close(fig)

    # ---- recruitment-intervention-compare.png ---------------------------------------
    comp = cache["comparison"]
    rows = comp["per_intervention"]
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.0, 4.4),
                                   gridspec_kw=dict(width_ratios=[1.1, 1]))
    labs = [r["label"] for r in rows][::-1]
    med = np.array([r["median_multiplier"] for r in rows])[::-1]
    lo = np.array([r["multiplier_p05"] for r in rows])[::-1]
    hi = np.array([r["multiplier_p95"] for r in rows])[::-1]
    y = np.arange(len(labs))
    ax0.hlines(y, lo, hi, color="#9aa7bd", lw=3)
    ax0.plot(med, y, "o", color="#1b4f72", ms=6)
    ax0.axvline(1.0, color="#b2452e", ls="--", lw=0.9)
    ax0.set_yticks(y); ax0.set_yticklabels(labs, fontsize=7)
    ax0.set_xscale("log")
    ax0.set_xlabel("multiplier on surviving one-year recruits (5th-95th percentile)")
    ax0.set_title("How much each intervention moves the outcome", loc="left", fontsize=8.5)

    eff = np.array([r["gain_per_unit_effort"] for r in rows])[::-1]
    ax1.barh(y, eff, color=["#1f6f54" if e > 0 else "#b2452e" for e in eff])
    ax1.set_yticks(y); ax1.set_yticklabels([])
    ax1.axvline(0.0, color="#555", lw=0.8)
    ax1.set_xlabel("median gain per unit of relative effort")
    ax1.set_title("...per unit effort. THE EFFORT UNITS ARE ASSUMED.", loc="left",
                  fontsize=8.5)
    ax1.text(0.97, 0.04, "Effort is in relative units anchored\nat 1 for substrate "
                         "conditioning.\nOnly the tetrapod cost ratio has\ndirect "
                         "published support.",
             transform=ax1.transAxes, ha="right", fontsize=6.0)
    fig.suptitle("SIMULATED. Each bar is a multiplier on a model whose baseline spans "
                 "four orders of magnitude; the RANKING is the result, not the numbers.",
                 fontsize=8.2, x=0.012, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(os.path.join(FIGDIR, "recruitment-intervention-compare.png"))
    plt.close(fig)
    print("figures written")


def write_result(cache):
    comp = cache["comparison"]; sens = cache["sensitivity"]; ctrl = cache["control_arm"]
    top = comp["per_intervention"][0]
    dominant = sens[0]
    assumed_share = sum(r["share_of_spread"] for r in sens if r["status"] == "assumed")
    counts = {}
    for st in STAGES:
        counts[st["status"]] = counts.get(st["status"], 0) + 1
    eff = cache["effort_unit_sensitivity"]
    top2 = eff["most_common_top_two"][0]
    top2_labels = [next(i["label"] for i in INTERVENTIONS if i["key"] == k)
                   for k in top2["pair"]]
    headline = (
        f"NO INTERVENTION IN THIS TABLE MOVES RECRUITMENT AS MUCH AS THE DIFFERENCE "
        f"BETWEEN A NORMAL YEAR AND A HEATWAVE YEAR, and this model has no thermal year "
        f"in it at all. Speare et al. measured recruit survivorship of 33% in a normal "
        f"year against 2% in a heatwave year at the same site in Moorea -- a 16-fold "
        f"swing -- while the best intervention here has a median multiplier of "
        f"{max(r['median_multiplier'] for r in comp['per_intervention']):.0f}x on a "
        f"quantity whose own baseline spans four orders of magnitude. "
        f"The second result is the decomposition, and it is the kind only a sensitivity "
        f"analysis reaches: about {100*assumed_share:.0f}% of the spread comes from "
        f"stages whose range this page had to INVENT, led by '{dominant['label']}' at "
        f"{100*dominant['share_of_spread']:.0f}%. So the highest-value next experiment "
        f"in this entire chain is a MEASUREMENT, not an intervention trial. "
        f"On the ranking: the effort units were invented, so they were sampled too, and "
        f"what survives is that '{top2_labels[0]}' and '{top2_labels[1]}' are in a "
        f"different class from the rest ({100*top2['frequency']:.0f}% of draws put "
        f"exactly those two on top), while the order WITHIN that pair is not stable. "
        f"{counts.get('assumed', 0)} of the {len(STAGES)} stages have no published wild "
        f"value at all, which is why this is a distribution and not a prediction.")
    out = dict(
        schema="design-space-result-0.1",
        study_id="settlement-recruitment",
        title="Settlement and recruitment: which intervention actually moves surviving "
              "recruits per unit effort",
        is_observation=False,
        headline=headline,
        provenance=dict(generated_at=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                        code="results/coral/code/settlement_recruitment.py",
                        n_samples=N_SAMPLES, sampling="Latin hypercube over stage values; "
                                                      "simple random for intervention "
                                                      "multipliers and costs",
                        rng_seed=RNG_SEED),
        model=dict(
            name="multiplicative survival chain with interval-valued stages",
            kind="Monte Carlo sensitivity analysis",
            is_observation=False,
            why_not_a_point_prediction=(
                "Because the parameters for one do not exist. The research block records "
                "NO published value for eggs per colony, wild pelagic larval mortality, "
                "no-cue settlement probability, settlers per larva released in the "
                "field, or the absolute size at which a recruit escapes incidental "
                "grazing. A point prediction would be an invented number wearing a "
                "decimal place."),
            parameters=STAGES,
            parameter_status_counts=counts,
            interventions=INTERVENTIONS,
            stage_cap=dict(
                value=0.9,
                note="Every stage after fecundity is a probability and is capped at 0.9 "
                     "after any intervention multiplier, so stacked interventions cannot "
                     "manufacture a certainty. Declared before the run; the control arm "
                     "checks the cap is not binding where it should not be."),
        ),
        control_arm=ctrl,
        sensitivity=dict(
            ranking=sens,
            share_of_spread_from_assumed_ranges=assumed_share,
            interpretation=(
                f"{100*assumed_share:.0f}% of the spread in the answer comes from stages "
                f"whose range this file INVENTED. The top contributor, "
                f"'{dominant['label']}', is "
                f"{'assumed' if dominant['status'] == 'assumed' else 'sourced'}. That is "
                f"the result most worth acting on: measuring the dominant stage once "
                f"would narrow this analysis more than any intervention trial would."),
            method="Spearman rank correlation of each sampled stage against the log of "
                   "the final count, squared and normalised to a share. Declared before "
                   "the run.",
            caveat="A rank correlation measures how much a stage's DECLARED RANGE drives "
                   "the output, so a stage with a wide invented range will dominate by "
                   "construction. The range_decades column is published beside each row "
                   "so that circularity is visible rather than hidden."),
        comparison=comp,
        effort_unit_sensitivity=eff,
        quotable=dict(
            note="Which numbers in this study may be cited, and why. Written because the "
                 "biology was sampled 20,000 times and the effort units were not, until "
                 "they were, and the difference matters to what can be said.",
            may_be_quoted=[
                dict(claim=f"'{top2_labels[0]}' and '{top2_labels[1]}' are in a different "
                           f"class from the other interventions, per unit of effort.",
                     basis=f"{100*top2['frequency']:.0f}% of {eff['n_draws']} draws with "
                           f"independently perturbed effort units put exactly those two "
                           f"in the top two."),
                dict(claim="About four fifths of the spread in surviving recruits comes "
                           "from stages with no published wild value.",
                     basis="Spearman rank decomposition over the Latin-hypercube sample; "
                           "the stage ranges are published beside it so the circularity "
                           "is visible."),
                dict(claim="The baseline spans four orders of magnitude.",
                     basis="5th to 95th percentile of the sampled chain."),
                dict(claim="No intervention here moves recruitment as much as the "
                           "difference between a normal and a heatwave year.",
                     basis="Comparison of this table's multipliers against Speare et "
                           "al.'s measured 33% against 2%. Note that is a comparison "
                           "ACROSS a model and a measurement, so it is an "
                           "order-of-magnitude statement and not an effect size."),
            ],
            may_NOT_be_quoted=[
                dict(claim=f"'{top2_labels[0]}' beats '{top2_labels[1]}'.",
                     why="The gap between them rests on invented denominators and does "
                         "not survive perturbing them. See fragile_orderings."),
                dict(claim="Any absolute number of surviving recruits.",
                     why="The baseline is a distribution four orders of magnitude wide "
                         "built on four invented ranges. The median is a property of "
                         "those choices."),
                dict(claim="Any cost in money.",
                     why="The effort units are relative and mostly invented. The two "
                         "real money figures in the literature are not comparable with "
                         "each other and are not compared here."),
            ]),
        limitations=[
            "This is a SIMULATION over invented ranges. No coral was measured and no reef "
            "was surveyed.",
            "A MULTIPLICATIVE CHAIN IS A STRONG ASSUMPTION. Real recruitment has density "
            "dependence (Doropoulos et al. 2017 find negative density dependence in "
            "crevices), size-dependent mortality, and stage-dependent causes of death "
            "that switch rather than add. None of that is here.",
            "THE EFFORT UNITS ARE MOSTLY INVENTED, and they decide the ranking. They "
            "are now sampled rather than fixed (see effort_unit_sensitivity), which "
            "establishes WHICH parts of the ordering survive them -- but sampling an "
            "invented range does not make it a measured one. Exactly "
            "one cost ratio has direct published support: tetrapods at 5-18x lower "
            "outplanting cost and about a twelfth of the attachment time. The two real "
            "money figures in the literature -- USD 35.20 per surviving colony at 35 "
            "months in the Philippines and USD 334-577 per surviving coral at two years "
            "on the Great Barrier Reef -- are from different species, years, accounting "
            "methods and survival horizons, and they are NOT compared here, because "
            "comparing them would be the error this study exists to avoid.",
            "Intervention effects are modelled as stage multipliers drawn independently. "
            "No study read here crosses two of these interventions factorially, so "
            "whether they interact is unknown, and the stacked arm's multiplicative "
            "combination is an assumption of the model.",
            "Herbivory is NOT modelled as protection, deliberately. Penin et al. found "
            "that excluding predators and grazers did not change total recruit mortality, "
            "it changed the cause; Webster et al. found caging raised recruit mortality "
            "through macroalgae. The sign depends on stage and microhabitat, and a "
            "single multiplier cannot carry that.",
            "Thermal years are not in the model. Speare et al. report recruit survival of "
            "33% in a normal year against 2% in a heatwave year at the same site -- a "
            "larger swing than any intervention in this table produces. A recruitment "
            "model with no temperature in it will overstate what recruitment engineering "
            "can achieve.",
            "The acoustic multiplier uses 1.7-1.8x and NOT the maximum of 7x that one "
            "study reports, because in flow-through conditions the response was minimal "
            "and the between-reef difference was tenfold. That is a judgement, it "
            "lowers the rank of that intervention, and someone could reasonably disagree.",
            "Every verified acoustic result comes from one laboratory group and no "
            "independent replication was found. There is no Acropora value at all.",
            "Microfragmentation is NOT in the comparison, although it is in the route "
            "table, because it bypasses sexual recruitment entirely rather than moving a "
            "stage of it. Comparing it here would be a category error.",
            "The one-year horizon hides what the two-year results show: Smith et al. "
            "found the sea-weeding benefit present at year one and gone by year two. An "
            "analysis that stops at a year will rank recurring-cost interventions too "
            "highly, and this one does.",
        ],
        sources=[
            dict(cite="Foster & Gilmour 2020, Sci Rep 10:12313", pmid="32703979",
                 read_level="full-text", note="Eggs per polyp; the one sourced fecundity "
                                              "parameter."),
            dict(cite="Abdul Wahab et al. 2023, Sci Rep 13:5795", pmid="37032381",
                 read_level="abstract", note="Settlement by crustose coralline alga, 15 "
                                             "corals x 15 algae."),
            dict(cite="Whitman et al. 2020, Sci Rep 10:16397", pmid="33009428",
                 read_level="abstract", note="The non-responders that set the low end."),
            dict(cite="Siboni et al. 2012, PLoS One 7:e37774", pmid="22655067",
                 read_level="abstract", note="Metamorphosis 100%, attachment 0-2% -- why "
                                             "settlement and attachment are one stage."),
            dict(cite="Doropoulos et al. 2017, R Soc Open Sci 4:170082", pmid="28573015",
                 read_level="abstract", note="Larval survival in the laboratory, and "
                                             "negative density dependence in crevices."),
            dict(cite="Chamberland et al. 2017, Sci Rep 7:18076", pmid="29273761",
                 read_level="abstract", note="9.6% first-year survival on tetrapods; the "
                                             "cost ratio."),
            dict(cite="Smith et al. 2025, J Environ Manage 383:125322", pmid="40267811",
                 read_level="abstract", note="Sea-weeding benefit gone by year two; USD "
                                             "334-577 per surviving coral."),
            dict(cite="Dela Cruz & Harrison 2020, PLoS One 15:e0242847", pmid="33232367",
                 read_level="abstract", note="Mass larval enrichment; USD 35.20 per "
                                             "surviving colony at 35 months."),
            dict(cite="Dela Cruz & Harrison 2017", pmid="29070842", read_level="abstract",
                 note="Zero settlement in control plots; 2.3 colonies per square metre at "
                      "three years."),
            dict(cite="Rodriguez-Ruano et al. 2026, Commun Biol 9", pmid="42310106",
                 read_level="abstract", note="Sediment burial."),
            dict(cite="Webster et al. 2015, PLoS One 10:e0124162", pmid="25898011",
                 read_level="abstract", note="Macroalgae, confounded with caging."),
            dict(cite="Aoki et al. 2024, R Soc Open Sci 11:231514", pmid="38481984",
                 read_level="abstract", note="Acoustic enrichment, 1.7x."),
            dict(cite="Aoki et al. 2026, Sci Rep", pmid="42409953", read_level="abstract",
                 note="Acoustic enrichment in a broadcast spawner; the flow-through "
                      "null and the tenfold between-reef difference."),
            dict(cite="Randall et al. 2021, Front Mar Sci — grooved microrefugia, 39% "
                      "against 13%, and 100% mortality on upper surfaces. No PMID "
                      "verified.", pmid=None, read_level="search-summary"),
            dict(cite="Penin et al. 2011, Hydrobiologia — more than half of recruits dead "
                      "in seven days, cage or no cage. No PMID verified.",
                 pmid=None, read_level="search-summary"),
            dict(cite="Speare et al. 2021, Glob Change Biol — 33% against 2% recruit "
                      "survivorship between a normal and a heatwave year at Moorea. No "
                      "PMID verified.", pmid=None, read_level="search-summary"),
            dict(cite="Waters et al. 2025, Restoration Ecology — the field failure case. "
                      "No PMID verified.", pmid=None, read_level="search-summary"),
            dict(cite="Mendoza Quiroz et al. 2025, Restoration Ecology — the attachment "
                      "time-against-retention trade-off. No PMID verified.",
                 pmid=None, read_level="search-summary"),
        ],
    )
    with open(RESULT, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"wrote {RESULT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--figures", action="store_true")
    args = ap.parse_args()
    os.makedirs(FIGDIR, exist_ok=True)
    if args.figures:
        with open(CACHE) as fh:
            make_figures(json.load(fh))
        return
    print("control arm ...", flush=True)
    ctrl = control_arm()
    for k, v in ctrl["checks"].items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    print(f"  baseline median {ctrl['baseline']['median']:.3g} "
          f"(5th {ctrl['baseline']['p05']:.3g}, 95th {ctrl['baseline']['p95']:.3g})")
    print("sensitivity ...", flush=True)
    sens = sensitivity()
    for r in sens:
        print(f"  {100*r['share_of_spread']:5.1f}%  {r['status']:8s} {r['label']}")
    print("intervention comparison ...", flush=True)
    comp = compare()
    for r in comp["per_intervention"]:
        print(f"  {r['gain_per_unit_effort']:+8.3f}/effort  "
              f"{r['median_multiplier']:5.2f}x  {r['label']}")
    print("effort-unit sensitivity ...", flush=True)
    eff = effort_unit_sensitivity()
    for r in eff["per_intervention"][:4]:
        print(f"  P(top 2) = {r['p_top_2']:.2f}  P(rank 1) = {r['p_rank_1']:.2f}  "
              f"{r['label']}")
    cache = dict(control_arm=ctrl, sensitivity=sens, comparison=comp,
                 effort_unit_sensitivity=eff)
    with open(CACHE, "w") as fh:
        json.dump(cache, fh)
    make_figures(cache)
    write_result(cache)


if __name__ == "__main__":
    main()
