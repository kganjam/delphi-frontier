#!/usr/bin/env python3
"""
build_index.py — assemble index-fragment.json.

Every figure listed here must exist on disk and must carry an authored alt text and an
authored caption; the builder refuses to write the file otherwise. A study listed here
and missing from the tree is reported as declared-and-absent rather than dropped, so the
page cannot quietly shrink.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "index-fragment.json")

STUDIES = [
    dict(
        id="bleaching-dynamics",
        title="What a heatwave does to the partnership, and which knob actually moves it",
        scale="symbiont",
        kind="host-symbiont bioenergetic model under thermal stress",
        question=(
            "Four routes on this page claim to raise thermal tolerance by acting on four "
            "different things: the symbiont's thermal optimum, its photoprotective "
            "capacity, how much oxidative stress it takes to do damage, and how readily "
            "the host expels symbionts under that stress. Are they additive, or does one "
            "dominate? And what does each cost when there is no heatwave?"),
        summary=(
            "The dynamical core is not invented here: it is a line-by-line port of the "
            "published coRal model, checked against the author's own R code to 5e-15 "
            "relative error across three environments. That matters because coRal "
            "contains NO temperature variable at all -- in the published model bleaching "
            "is driven by light -- so the thermal coupling is this page's addition and "
            "enters through exactly one parameter. The study's weakness is that single "
            "calibration: one parameter was tuned so the unmodified holobiont bleaches "
            "inside NOAA's 4-8 degree-heating-week window, which means the model cannot "
            "then be used as evidence about that window. A second weakness is numerical "
            "and is reported as a failure rather than smoothed over: the step-halving "
            "check fails at 9%, because coRal integrates with explicit Euler and a "
            "first-crossing readout inherits that slow convergence. The absolute "
            "threshold is therefore not converged; the knob ranking, which is what the "
            "study claims, is identical at three step sizes."),
        code="results/coral/code/bleaching_dynamics.py "
             "(with coral_deb.py and coral_reference_run.R beside it)",
        data="results/coral/bleaching-dynamics.json",
        summary_table_title="Four knobs, two readouts, and what each costs at ambient",
        figures=[
            dict(file="bleaching-control.png",
                 alt="Three stacked time series over three years of an ambient seasonal "
                     "cycle: sea temperature oscillating below a dashed maximum-monthly-"
                     "mean line, the symbiont-to-host ratio settling to a steady value "
                     "well above a dashed bleaching-criterion line, and the ROS factor "
                     "sitting steadily above one.",
                 caption="Simulation, control arm. The ambient seasonal cycle with no "
                         "anomaly, which has to hold before any sweep is read. All seven "
                         "pre-declared checks pass, including that an unperturbed year "
                         "accumulates exactly zero degree heating weeks. The footnote "
                         "records the port check against the published R code."),
            dict(file="bleaching-threshold.png",
                 alt="A three-row, four-column grid, one column per design knob. The top "
                     "row plots the thermal anomaly at failure on two readouts; the "
                     "middle row plots the same thresholds in degree heating weeks "
                     "against shaded NOAA bands, where the host-energy readout sits near "
                     "zero in three of four panels; the bottom row plots the percentage "
                     "change in ambient host growth, which is positive for three knobs "
                     "and negative only for the symbiont thermal optimum.",
                 caption="Simulation, not measurement. The bottom row is the point: "
                         "raising the symbiont's thermal optimum is the only one of the "
                         "four knobs that costs anything when there is no heatwave. The "
                         "middle row shows why the study needed two readouts at all -- "
                         "degree heating weeks are summed only above a 1 degC HotSpot "
                         "threshold, so a failure mode that bites below that reads as "
                         "zero."),
            dict(file="bleaching-knob-map.png",
                 alt="Six heatmap panels, one for each pair of the four knobs, each "
                     "marginalised over the other two, with a shared colour scale for "
                     "the thermal anomaly at which the host's carbon balance fails.",
                 caption="Simulation. The full four-knob map, marginalised to pairs. Main "
                         "effects alone explain 0.999 of the variance and all six "
                         "two-way interactions together add 0.001, so within this box "
                         "the knobs are additive. That is a property of a four-parameter "
                         "model, not a claim that two real interventions combine "
                         "additively in a coral -- which nobody has tested."),
        ]),
    dict(
        id="colony-morphology",
        title="Branching, plating, massive: a growth-geometry problem, and where the "
              "model runs out",
        scale="colony",
        kind="accretive growth on a diffusive resource field",
        question=(
            "Colony shape decides flow, light capture, nursery habitat and what a storm "
            "breaks. Can a single dimensionless parameter -- the ratio of uptake rate to "
            "transport rate that Merks and colleagues identify -- take a colony from "
            "massive through to branching? Is the transition sharp or graded, and which "
            "metric sees it?"),
        summary=(
            "The model class is published and runnable; this implementation is in that "
            "family and is not a port of any member of it. Both pre-declared controls "
            "pass and the Damkohler sweep moves surface-to-volume, fractal dimension and "
            "bounding-box fill smoothly and substantially. The honest result is a "
            "failure as well as a finding: the model spans compact mound to open lobed "
            "mound and DOES NOT REACH either true branching or plating, so the "
            "three-form span this study was built to produce is not achieved. Getting "
            "there took three rewrites of the growth rule, and the reason is worth more "
            "than the sweep: two earlier voxel versions were dominated by the lattice "
            "rather than the physics -- six-connected growth produced octahedra, "
            "twenty-six-connected growth produced cubes -- and none of the four declared "
            "metrics revealed it. They all varied smoothly and plausibly with the "
            "control parameter while the shapes being measured were artefacts. Only "
            "looking at the projections showed it."),
        code="results/coral/code/colony_morphology.py",
        data="results/coral/colony-morphology.json",
        summary_table_title="What the control parameter moves, and what it does not",
        figures=[
            dict(file="morphology-forms.png",
                 alt="A two-row gallery of simulated colonies, side views above and plan "
                     "views below, running from a smooth compact hemispherical mound at "
                     "low Damkohler number to progressively rougher and more open lobed "
                     "mounds at high Damkohler number, with flow-biased and "
                     "light-weighted variants at the right.",
                 caption="Simulated colonies, one random seed each. These are "
                         "occupied-voxel silhouettes, not renderings. The gallery is "
                         "also the evidence for this study's main negative: the "
                         "high-Damkohler forms are rough open mounds, not separated "
                         "branches, and no setting tried produced a branching or a "
                         "plating colony."),
            dict(file="morphology-growth.mp4",
                 alt="A short animation of two simulated colonies growing side by side, "
                     "side and plan views, one at low Damkohler number staying a smooth "
                     "compact mound and one at high Damkohler number roughening into an "
                     "open lobed form, with generation count and voxel volume shown.",
                 caption="Simulated accretive growth, 65 generations at twelve frames a "
                         "second. Occupied-voxel silhouettes, not renderings; no coral "
                         "was filmed. The two arms are the ends of the control "
                         "parameter, so the comparison is the point rather than the "
                         "motion — and the right-hand arm is also the clearest view of "
                         "this study's negative, since what it grows into is a rough "
                         "mound rather than a branching colony."),
            dict(file="morphology-transition.png",
                 alt="Four panels against a logarithmic Damkohler axis: branch count, "
                     "surface-to-volume ratio, box-counting dimension and the "
                     "area-diameter exponent, each with a shaded band of plus and minus "
                     "one standard deviation across random seeds, and with the "
                     "measured exponent ranges for real branching and massive colonies "
                     "shaded on the last panel.",
                 caption="Simulation. The band is the spread across independent random "
                         "seeds, not a confidence interval. Only the rightmost panel can "
                         "be compared with a measurement: the area-diameter exponent is "
                         "dimensionless, and Chandler and colleagues measured it on real "
                         "colonies by photogrammetry. The transition verdict uses a cut "
                         "declared before the sweep was run."),
        ]),
    dict(
        id="settlement-recruitment",
        title="The bottleneck nobody engineers: which intervention actually moves "
              "surviving recruits",
        scale="larval",
        kind="Monte Carlo sensitivity analysis over stated unknowns",
        question=(
            "Restoration does not usually fail because adult corals die. It fails at "
            "recruitment. Given larval supply, a settlement cue, and early "
            "post-settlement mortality, which intervention moves the most surviving "
            "recruits per unit of effort?"),
        summary=(
            "This is deliberately a sensitivity analysis and not a point prediction, "
            "because the parameters for a prediction do not exist: there is no published "
            "value for eggs per colony, wild pelagic larval mortality, no-cue settlement "
            "probability, settlers per larva released in the field, or the size at which "
            "a recruit escapes incidental grazing. The baseline therefore spans four "
            "orders of magnitude, and that is the honest answer rather than a defect. "
            "Its own weakness is the cost model: the interventions are ranked per unit "
            "of effort and the effort units are mostly invented, with exactly one cost "
            "ratio carrying direct published support. The most useful output is not the "
            "ranking but the sensitivity decomposition, which shows that about four "
            "fifths of the spread comes from stages whose range this page had to invent "
            "-- so the highest-value next experiment in this whole chain is a "
            "measurement, not a trial."),
        code="results/coral/code/settlement_recruitment.py",
        data="results/coral/settlement-recruitment.json",
        summary_table_title="Interventions ranked by gain per unit of effort",
        figures=[
            dict(file="recruitment-sensitivity.png",
                 alt="A horizontal bar chart of each life-history stage's share of the "
                     "spread in the final recruit count, coloured by whether that "
                     "stage's range is sourced or assumed, beside a logarithmic "
                     "percentile strip showing the baseline spanning four orders of "
                     "magnitude.",
                 caption="Simulation over stated unknowns, not a prediction of any reef. "
                         "The red bars are stages whose range this page invented because "
                         "no published value was found, and they dominate. The strip at "
                         "the right is the point of the whole study: the baseline is a "
                         "distribution four orders of magnitude wide, and anyone quoting "
                         "a single number for it is quoting a choice."),
            dict(file="recruitment-intervention-compare.png",
                 alt="Two panels: at the left, each intervention's median multiplier on "
                     "surviving one-year recruits with a 5th-to-95th-percentile bar on a "
                     "logarithmic axis; at the right, the same interventions ranked by "
                     "median gain per unit of relative effort.",
                 caption="Simulation. The left panel's multipliers come from measured "
                         "effect sizes where those exist; the right panel's ranking "
                         "additionally depends on effort units that are mostly assumed, "
                         "which is stated on the figure because it is the weakest link "
                         "in the comparison. Mass larval enrichment moves the outcome "
                         "most in absolute terms and site screening wins per unit of "
                         "effort, and the gap between those two statements is the whole "
                         "argument about how to spend a restoration budget."),
        ]),
]


def main():
    errs = []
    figdir = os.path.join(ROOT, "figures")
    for st in STUDIES:
        data = os.path.join(ROOT, os.path.basename(st["data"]))
        st["data_present"] = os.path.exists(data)
        if not st["data_present"]:
            errs.append(f"{st['id']}: declared data file missing: {data}")
        n_sent = len([s for s in st["summary"].split(". ") if s.strip()])
        if not (3 <= n_sent <= 8):
            errs.append(f"{st['id']}: summary has {n_sent} sentences, want 3-6ish")
        for f in st["figures"]:
            path = os.path.join(figdir, f["file"])
            f["present"] = os.path.exists(path)
            if not f["present"]:
                errs.append(f"{st['id']}: figure missing on disk: {f['file']}")
            if not f.get("alt") or len(f["alt"]) < 40:
                errs.append(f"{st['id']}/{f['file']}: alt text missing or too short")
            if not f.get("caption") or len(f["caption"]) < 40:
                errs.append(f"{st['id']}/{f['file']}: caption missing or too short")
            low = f["caption"].lower()
            if not any(w in low for w in ("simulat", "model")):
                errs.append(f"{st['id']}/{f['file']}: caption does not open by saying "
                            f"what the figure IS")
    if errs:
        print("VALIDATION FAILED — index-fragment.json NOT written:")
        for e in errs:
            print("  " + e)
        sys.exit(1)

    out = dict(
        schema="design-space-index-0.1",
        note=("The index the site build reads. A study listed here and missing from the "
              "tree is reported as declared-and-absent rather than dropped, so the page "
              "cannot quietly shrink. Captions and alt text are authored here, so no "
              "figure can appear without them, and build_index.py refuses to write this "
              "file if a caption does not open by saying what the figure is."),
        routes=dict(
            title="Design a coral: for heat, for shape, or for the reef",
            data="results/coral/routes.json",
            note=("Forty-five published perturbations and bounded proposals across nine "
                  "scales, each with its own evidence level and the read level of every "
                  "source behind it. None has been attempted here."),
            nothing_attempted="None of them has been attempted here."),
        studies=STUDIES,
    )
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    nfig = sum(len(s["figures"]) for s in STUDIES)
    print(f"wrote {OUT}: {len(STUDIES)} studies, {nfig} figures, all present on disk")


if __name__ == "__main__":
    main()
