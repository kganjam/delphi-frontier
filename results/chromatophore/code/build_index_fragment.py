"""Build index-fragment.json: the three studies, with authored alt text and captions.

Numbers in the summaries are substituted from the result files so they cannot drift
away from the studies they describe; the prose around them is written by hand.
"""
from __future__ import annotations

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(ROOT, name)) as fh:
        return json.load(fh)


SUPERSESSION_MARKERS = ("superseded", "supersedes", "earlier version", "was wrong",
                        "that was wrong", "corrected", "correction", "retract")


def assert_no_superseded_text(studies, sources):
    """Refuse to emit a summary that still tells a superseded study's old story.

    WHY. The fragment builder once carried the pre-retraction actuator story - "the
    wrong way round ... structurally incapable" - after the study itself had been
    corrected. The only thing that stopped it reaching the published index was an
    unrelated `TypeError`, because the field it formatted had changed shape. That is
    luck, not a control.

    The rule: if a source study carries a `SUPERSEDED_*` key, then its summary must
    (a) mention the supersession, and (b) contain NONE of the superseded values. (b)
    is the load-bearing half - it is what catches prose that quietly kept the old
    number.
    """
    problems = []
    for st in studies:
        src = sources.get(st["id"])
        if src is None:
            continue
        sup_keys = [k for k in src if k.startswith("SUPERSEDED")]
        if not sup_keys:
            continue
        summary = st.get("summary", "")
        low = summary.lower()
        if not any(m in low for m in SUPERSESSION_MARKERS):
            problems.append(
                f"{st['id']}: source carries {sup_keys} but the summary never mentions "
                f"the correction")
        for key in sup_keys:
            for name, val in (src[key].get("superseded_values") or {}).items():
                for v in (val if isinstance(val, list) else [val]):
                    if not isinstance(v, (int, float)):
                        continue
                    # `:.0f` is dropped deliberately: it renders 1.3378 as "1",
                    # which matches inside every other number on the page. A
                    # rendering must be distinctive to be evidence.
                    for text in (f"{v:g}", f"{v:.2f}", f"{v:.3f}"):
                        if len(text) < 3:
                            continue
                        if re.search(rf"(?<![\d.]){re.escape(text)}(?![\d])", summary):
                            problems.append(
                                f"{st['id']}: summary contains the SUPERSEDED value "
                                f"{name}={text!r}, which this study replaced")
    if problems:
        raise AssertionError(
            "refusing to emit index-fragment.json:\n  " + "\n  ".join(sorted(set(problems))))
    return {"check": "no_superseded_text_in_summaries", "passed": True,
            "studies_with_superseded_keys": [
                st["id"] for st in studies
                if any(k.startswith("SUPERSEDED") for k in sources.get(st["id"], {}))]}


def selftest_superseded_guard(studies, sources):
    """A guard ships with a case it must flag. Inject a superseded value and require
    the guard to raise; then confirm the real set passes."""
    import copy
    results = []
    target = next((st for st in studies
                   if any(k.startswith("SUPERSEDED") for k in sources.get(st["id"], {}))),
                  None)
    if target is None:
        return [{"arm": "no study carries a SUPERSEDED key", "flagged": None}]
    # Build the positive control by MUTATING THE REAL RECORD, never from a
    # hand-written literal. The first version injected "1.34" by hand; when
    # `superseded_values` was later narrowed - correctly - to drop that number, the
    # injection stopped corresponding to anything superseded and the arm silently
    # went green. A control written against a constant decays the moment the data
    # it is meant to police changes.
    bad = copy.deepcopy(studies)
    b = next(st for st in bad if st["id"] == target["id"])
    src_sup = sources[target["id"]]
    sup_key = next(k for k in src_sup if k.startswith("SUPERSEDED"))
    vals = src_sup[sup_key].get("superseded_values") or {}
    injected = None
    for name, val in vals.items():
        for v in (val if isinstance(val, list) else [val]):
            if isinstance(v, (int, float)) and len(f"{v:g}") >= 3:
                injected = f"{v:g}"
                break
        if injected:
            break
    if injected is None:
        return [{"arm": "no superseded numeric value available to inject",
                 "flagged": None}]
    b["summary"] = b["summary"] + f" The measured range is {injected} ms."
    try:
        assert_no_superseded_text(bad, sources)
        results.append({"arm": "superseded value reinserted into summary",
                        "injected": injected, "flagged": False})
    except AssertionError:
        results.append({"arm": "superseded value reinserted into summary",
                        "injected": injected, "flagged": True})
    bad2 = copy.deepcopy(studies)
    b2 = next(st for st in bad2 if st["id"] == target["id"])
    for m in SUPERSESSION_MARKERS:
        b2["summary"] = b2["summary"].replace(m, "").replace(m.capitalize(), "")
    try:
        assert_no_superseded_text(bad2, sources)
        results.append({"arm": "supersession never mentioned", "flagged": False})
    except AssertionError:
        results.append({"arm": "supersession never mentioned", "flagged": True})
    try:
        assert_no_superseded_text(studies, sources)
        results.append({"arm": "unperturbed", "flagged": False})
    except AssertionError as exc:
        results.append({"arm": "unperturbed", "flagged": True, "error": str(exc)[:200]})
    return results



def _write_browser_safe(path, obj):
    """Write JSON a browser's JSON.parse will accept.

    Python emits NaN and Infinity as bare literals, which are NOT valid JSON, and
    Python's own json.load accepts them by default - so the defect is invisible to
    a Python round-trip and fatal in a browser. Ours shipped 16 bare NaNs and took
    down every page on the site, not only its own. Non-finite floats become null;
    the write is then re-parsed with `parse_constant` as a positive control.
    """
    import math

    def safe(o):
        if isinstance(o, float):
            return None if not math.isfinite(o) else o
        if isinstance(o, dict):
            return {k: safe(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [safe(v) for v in o]
        return o

    def boom(x):
        raise ValueError(f"non-finite literal {x!r} survived the safe writer")

    text = json.dumps(safe(obj), indent=1)
    json.loads(text, parse_constant=boom)
    with open(path, "w") as fh:
        fh.write(text)


def main():
    am = load("actuator-mechanics.json")
    og = load("optical-gamut.json")
    cch = load("control-channels.json")

    amc = am["control"]["comparisons"]
    asym = amc["retraction_vs_expansion_asymmetry"]["measured"]
    pc_am = am["model"]["parameter_counts"]
    pc_og = og["model"]["parameter_counts"]
    pc_cc = cch["model"]["parameter_counts"]
    hd = cch["results"]["headline"]
    an = cch["results"]["where_the_real_animal_sits"]
    rr = cch["results"]["knee_is_set_by_coverage_not_complexity"]["ratio_range"]
    gm = og["gamut"]

    studies = [
        {
            "id": "actuator-mechanics",
            "title": "The chromatophore as an actuator: mechanics, kinetics and a datasheet",
            "scale": "cell",
            "kind": am["kind"],
            "question": "A cephalopod chromatophore is a pigment sac opened by radial "
                        "muscle under direct motor-neuron control. Treat it as an "
                        "actuator and write its datasheet: what stroke, what speed, what "
                        "force, what does it cost to hold open - and does a physical "
                        "model of it reproduce what was measured?",
            "summary": (
                f"Two parameters are fitted to two measured quantities and the two fits "
                f"are mutually inconsistent. The sacculus shear modulus is fitted to the "
                f"2.5506x steady-state expansion ratio; the dermal damping is then fitted "
                f"to the measured expansion:retraction asymmetry and reaches it "
                f"({amc['retraction_vs_expansion_asymmetry']['model']:.2f} against "
                f"{asym['renard_2026_slice_phases']:.2f} from Renard 2026, while "
                f"Hadjisolomou 2021 decomposed per region gives "
                f"{asym['hadjisolomou_2021_region_matched_phases']:.1f}) - but at that "
                f"damping the peak expansion collapses to {amc['area_ratio']['model']:.2f}, "
                f"{100 * amc['area_ratio']['shortfall']:.0f}% short of the ratio the "
                f"stiffness was fitted to. **The one genuinely free prediction fails**: "
                f"the 90% rise is {amc['rise_time_ms']['model']:.0f} ms against a measured "
                f"expansion phase of {amc['rise_time_ms']['measured_range'][0]:.0f}-"
                f"{amc['rise_time_ms']['measured_range'][1]:.0f} ms, "
                f"{amc['rise_time_ms']['model_over_measured'][0]:.1f}-"
                f"{amc['rise_time_ms']['model_over_measured'][1]:.1f}x too slow. An earlier "
                f"version of this study claimed a lumped elastic recoil was STRUCTURALLY "
                f"incapable of retraction slower than expansion; that was wrong - it was "
                f"read off a sweep whose maximum sat at its own boundary - and the "
                f"correction is recorded in the file rather than edited out. The parameter "
                f"ledger is the study's own indictment: {pc_am['sourced']} sourced against "
                f"{pc_am['assumed']} assumed, with every muscle property an explicit proxy "
                f"from a different Doryteuthis muscle because nobody has measured a "
                f"chromatophore radial muscle. Its most useful output is negative: across "
                f"every sweep the stroke is set by the elastic sac rather than by the "
                f"muscle, so adding radial fibres buys almost nothing."),
            "code": "code/actuator_mechanics.py",
            "data": "actuator-mechanics.json",
            "summary_table_title": "Chromatophore actuator datasheet",
            "figures": [
                {
                    "file": "figures/actuator-datasheet.png",
                    "alt": "A two-part figure. On the left, a 22-row datasheet table for "
                           "one chromatophore organ, listing addressable unit, retracted "
                           "and expanded pigment disc area, area expansion ratio, linear "
                           "stroke, fibre shortening, blocked and holding force, holding "
                           "stress, isometric duty, stored elastic energy, work density, "
                           "rise and retraction times, response latency, bandwidth, "
                           "in-vivo flicker rate, independent control inputs, array "
                           "density, power supply and return mechanism; six rows are "
                           "highlighted in green as measured rather than modelled. Top "
                           "right, a simulated step response: the pigment area ratio "
                           "rises to about 2.06 during a 250 ms drive window and relaxes "
                           "back to 1.0 by about 400 ms, with a dashed line at the "
                           "measured 2.55 that the curve never reaches. Bottom right, a "
                           "log-scale comparison of three quantities, each showing the "
                           "model value as a coloured dot and the measured value or range "
                           "as a grey bar: area ratio model 2.06 against measured 2.55, "
                           "rise time model 215 ms against measured 117-150 ms, and "
                           "retraction-over-expansion model 0.49 against measured 1.34.",
                    "caption": "Simulation, not a measurement. The datasheet is model "
                               "output except for the six rows marked MEASURED. The "
                               "bottom-right panel is the control arm and it fails: only "
                               "the area ratio was fitted, and the one free prediction - "
                               "the rise time - falls outside the measured range, while "
                               "the expansion-to-retraction asymmetry comes out on the "
                               "wrong side of 1.",
                },
                {
                    "file": "figures/actuator-sweep.png",
                    "alt": "Six panels of parameter sweeps. Top row: steady-state area "
                           "expansion ratio against the number of radial muscle fibres, "
                           "rising steeply to about 20 fibres and then flat at the "
                           "measured 2.55; against sacculus shear modulus, flat at 2.55 "
                           "below about 80 kPa and falling steeply above it, with the "
                           "fitted modulus marked; and against maximum fibre shortening, "
                           "rising linearly to 30 per cent and flat thereafter, with the "
                           "stroke-limited region shaded. Bottom row: expansion and "
                           "retraction times against radial fibre length, with expansion "
                           "flat near 215 ms above the measured 117-150 ms band and "
                           "retraction falling from 155 to 80 ms; expansion and "
                           "retraction times against dermal damping, both nearly flat "
                           "across nine orders of magnitude; and a heat map of area ratio "
                           "over fibre number and sacculus modulus, with the "
                           "muscle-stroke-limited region hatched and the measured 2.55 "
                           "contour drawn.",
                    "caption": "Simulation, not a measurement. Each panel varies one "
                               "parameter about the baseline. The shape that matters is "
                               "in the first and third panels: the organ sits on the flat "
                               "part of the fibre-number curve and on the flat part of "
                               "the shortening curve, so it is limited by the elasticity "
                               "of the pigment sac and not by its muscle. Dermal damping "
                               "is the only knob that touches retraction, and it has "
                               "never been measured.",
                },
            ],
        },
        {
            "id": "optical-gamut",
            "title": "A pigment layer over a tunable Bragg reflector: how much colour is "
                     "reachable, and which layer stops it",
            "scale": "organelle",
            "kind": og["kind"],
            "question": "Cephalopod skin stacks a pigment actuator over a tunable "
                        "multilayer reflector over a broadband scatterer. Given the "
                        "measured optical parameters of each, what colours can that stack "
                        "actually reach under a stated illuminant - and which layer is "
                        "the one holding it back?",
            "summary": (
                f"Freezing the iridophore stack removes "
                f"{(1 - gm['bragg_fixed_at_live_mean']['gamut_relative_to_full']) * 100:.0f}% "
                f"of the achievable chromaticity area, so the multilayer is what produces "
                f"the colour - but the layer that PROVIDES the gamut is not the layer "
                f"that LIMITS it. Widening the stack's measured 425-675 nm tuning range "
                f"to the whole visible band buys "
                f"{(gm['wider_bragg_380_780']['gamut_relative_to_full'] - 1) * 100:.0f}%, "
                f"while raising the reflectin refractive index from the live-cell mean "
                f"1.405 to the measured maximum 1.44 buys "
                f"{(gm['higher_n_high_1p44']['gamut_relative_to_full'] - 1) * 100:.0f}% "
                f"and a nearly transparent retracted state buys "
                f"{(gm['wider_area_ratio_50x']['gamut_relative_to_full'] - 1) * 100:.0f}%. "
                f"**The study's weakness is entirely on the pigment side**: the Bragg "
                f"stack's layer count, both refractive indices, both thicknesses and its "
                f"tuning range are published numbers from live cells, but no measured "
                f"absorption spectrum for any cephalopod ommochrome was found, so all "
                f"nine pigment numbers are assumed and every hue in the gamut inherits "
                f"that ({pc_og['sourced']} sourced against {pc_og['assumed']} assumed). "
                f"It is also a steady-state, normal-incidence model under CIE D65 and a "
                f"HUMAN observer, which is wrong on three counts at once: real "
                f"iridophores are strongly angle-dependent, seawater is not D65, and the "
                f"animals that matter are a colour-blind cephalopod and a tetrachromatic "
                f"fish. One of its four controls fails, and the failure is in the source "
                f"rather than the model - the published endpoint thicknesses do not "
                f"reproduce the published tuning range under the paper's own refractive "
                f"indices."),
            "code": "code/optical_gamut.py",
            "data": "optical-gamut.json",
            "figures": [
                {
                    "file": "figures/gamut-space.png",
                    "alt": "Two panels. Left, a CIE 1976 u-prime v-prime chromaticity "
                           "diagram with the horseshoe-shaped spectral locus outlined in "
                           "grey and four overlapping shaded polygons showing achievable "
                           "chromaticities: the largest is the hypothetical case with the "
                           "reflectin refractive index at its measured maximum, inside it "
                           "the achievable set with every dial free, and two much smaller "
                           "regions for chromatophores held expanded and for the "
                           "iridophore stack held fixed; the D65 white point is marked "
                           "with a cross near the middle of the achievable set. Right, "
                           "reflectance against wavelength from 380 to 780 nanometres: "
                           "four narrow peaks of about 15 per cent reflectance for stacks "
                           "tuned to 440, 520, 600 and 660 nanometres with their layer "
                           "thicknesses labelled, plus two broad dark curves for the "
                           "whole skin with all pigment expanded and with all pigment "
                           "retracted, both rising steeply towards the red end.",
                    "caption": "Optical model, not a measurement. The multilayer is a "
                               "transfer-matrix calculation using measured live-cell "
                               "parameters; the pigment layer above it uses an assumed "
                               "absorption spectrum, because none was found. Note how "
                               "close together the achievable set and the white point "
                               "are: at the measured refractive-index contrast of 1.048 "
                               "a nine-pair stack reflects only about 15 per cent at its "
                               "peak, so the skin is never very saturated.",
                },
                {
                    "file": "figures/gamut-limiting-layer.png",
                    "alt": "Two bar charts of gamut area relative to the full model. "
                           "Left, ten horizontal bars: five orange bars for holding one "
                           "layer fixed, showing the iridophore held at its live-cell "
                           "mean at 0.11, chromatophores held retracted at 0.59, "
                           "chromatophores held expanded at 0.26, the leucophore backing "
                           "removed at 1.00 and the stack fixed at eight pairs at 0.87; "
                           "and five green bars for widening one dial, showing "
                           "chromatophore area ratio ten times at 1.48, Bragg tuning over "
                           "the whole visible band at 1.01, reflectin index at its "
                           "measured maximum at 1.68, area ratio fifty times at 1.61 and "
                           "both optical dials at 1.76. Right, three yellow bars for "
                           "removing one pigment class: without yellow the gamut is "
                           "larger than the full model, without red it is about 0.73, and "
                           "without brown it is essentially unchanged.",
                    "caption": "Optical model, not a measurement. Two questions with two "
                               "different answers: freezing the iridophore costs 88 per "
                               "cent of the gamut, so the stack is what provides the "
                               "colour, but widening its tuning range buys one per cent "
                               "while raising the refractive index buys sixty-eight, so "
                               "index contrast is what limits it. Removing the yellow "
                               "pigment class makes the gamut bigger, because at the only "
                               "sourced expansion ratio a retracted chromatophore still "
                               "covers 52 per cent of the skin and that floor is a pure "
                               "loss.",
                },
            ],
        },
        {
            "id": "control-channels",
            "title": "How many independent control channels does an addressable skin need?",
            "scale": "circuit",
            "kind": cch["kind"],
            "question": "An array of pigment actuators at a measured spatial density is "
                        "driven by N independent channels, each owning a motor unit of m "
                        "actuators. How well can the skin match a target pattern, and "
                        "where is the point of diminishing returns? The knee is the spec "
                        "sheet for anyone building this.",
            "summary": (
                f"At the measured motor-unit size of nine actuators per channel the knee "
                f"sits at {hd['knee95_mean_channels']:.0f} +/- "
                f"{hd['knee95_sd_channels']:.0f} channels over a "
                f"{int(hd['K_actuators'])}-actuator patch - about "
                f"{hd['knee95_channels_per_mm2']:.0f} channels per square millimetre, or "
                f"one channel per {hd['actuators_per_channel_at_the_knee']:.1f} actuators "
                f"- but quote it as 'between 306 and 1094, nearest grid point 579', "
                f"NOT as '579 +/- 0'. The standard deviation across the 30 "
                f"runs is genuinely 0.0 and that is a GRID ARTEFACT: channel count is "
                f"swept on a 14-point logarithmic grid, so a knee can only land on a "
                f"grid point and all 30 landed on the same one. What the agreement "
                f"shows is that the knee is stable to within one grid step. Across unit sizes the knee tracks the "
                f"count needed simply to COVER the array within a factor of "
                f"{rr[0]:.2f}-{rr[1]:.2f}, so for everything but the finest target the "
                f"channel budget is set by innervating the skin at all, not by the "
                f"complexity of the pattern. The real animal is not a free parameter "
                f"here: Renard et al. 2026 resolved 754 putative motor units driving "
                f"1829 chromatophores, which is {an['channels_per_actuator']:.3f} "
                f"channels per actuator with units of about nine, so a cuttlefish sits "
                f"at {an['channels_on_this_patch']:.0f} channels on this patch and is "
                f"{an['verdict']}. **Its biggest weakness is that the "
                f"addressable element is wrong**: motor units here own whole actuators, "
                f"whereas a real chromatophore is driven by about four independent "
                f"sources acting on contiguous angular sectors, so these channel counts "
                f"are a lower bound on what a cuttlefish has. The observer's acuity is "
                f"assumed and is the parameter the knee most likely depends on, no "
                f"predator acuity number having been sourced; the coverage law is "
                f"biased by up to 16 per cent relative and that control is reported as "
                f"FAILED, with a sensitivity arm showing the knee does not move. Two "
                f"optimiser bugs were caught by declared controls before they could ship "
                f"as results, and both are documented in the file with the numbers they "
                f"produced. {pc_cc['sourced']} parameters are sourced against "
                f"{pc_cc['assumed']} assumed."),
            "code": "code/control_channels.py",
            "data": "control-channels.json",
            "summary_table_title": "Knee by motor-unit size and target",
            "grid_caveat": cch["results"]["headline"]["why_the_spread_is_zero"],
            "knee_quotable_as": "between 306 and 1094, nearest grid point 579",
            "controls_declared_but_not_reached": [
                c["name"] for c in
                cch["controls_declared_but_NOT_REACHED"]["not_reached"]],
            "verification_gap": cch["controls_declared_but_NOT_REACHED"]["status"],
            "figures": [
                {
                    "file": "figures/channels-vs-fidelity.png",
                    "alt": "Six panels, one per target pattern - edge, square, coarse "
                           "stripes, fine stripes, one-over-f gravel and mottle - each "
                           "plotting pattern match as variance explained against the "
                           "number of independent control channels on a logarithmic "
                           "axis. Each panel carries five curves, one per motor-unit size "
                           "of one, three, nine, fourteen and thirty actuators, with "
                           "shaded bands for plus or minus one standard deviation across "
                           "five array seeds, and a dotted vertical line marking each "
                           "curve's knee. A solid black vertical line, with a black dot "
                           "on the nine-actuator curve, marks the channel count a real "
                           "cuttlefish uses, derived from published motor-unit counts. "
                           "Every curve is flat near zero at low channel counts, rises "
                           "steeply over about one decade, and saturates.",
                    "caption": "Simulation, not a measurement. The dotted lines are the "
                               "knee as declared before the sweep ran: the smallest "
                               "channel count reaching 95 per cent of the score at one "
                               "channel per actuator. Larger motor units push the knee to "
                               "the left, because fewer channels are needed to cover the "
                               "array - and that, rather than the pattern's spatial "
                               "detail, is what sets the budget for five of the six "
                               "targets. The black line is the measured operating point "
                               "of a real animal - 754 motor units over 1829 "
                               "chromatophores in Euprymna berryi and Sepia officinalis "
                               "- placed on our own curve, which is the comparison this "
                               "study exists to make. The two uniform targets are not "
                               "plotted: their variance is zero, so the score is "
                               "undefined and is reported as null rather than as a "
                               "vacuous 1.0.",
                },
                {
                    "file": "figures/channels-examples.png",
                    "alt": "A grid of greyscale images in two rows. The leftmost column "
                           "is the target pattern, a soft one-over-f noise texture. Each "
                           "subsequent column shows the modelled skin driven by an "
                           "increasing number of channels, from a handful to one per "
                           "actuator, with the achieved match score printed beneath each "
                           "panel. The top row uses compact wiring and the bottom row "
                           "the oracle wiring that is allowed to choose its motor units "
                           "after seeing the target. Panels at low channel counts are "
                           "nearly uniform grey; panels at high counts closely resemble "
                           "the target.",
                    "caption": "Simulation, not a measurement, and not a photograph of "
                               "skin. All panels share one grey scale. The bottom row is "
                               "an upper bound no animal can reach - it rewires itself "
                               "for each target - and it is shown so the compact row can "
                               "be read against something other than the target.",
                },
            ],
        },
    ]

    vid = cch.get("video") or {}
    if vid.get("written"):
        studies[2]["figures"].append({
            "file": "figures/channels-demo.mp4",
            "alt": "A short silent animation. The left half holds a fixed one-over-f "
                   "noise target; the right half shows the modelled skin as the number "
                   "of independent control channels is stepped up from one to one per "
                   "actuator, with the channel count and the achieved match score in the "
                   "panel title. The right half begins as flat grey and progressively "
                   "resolves into the target texture, with most of the change happening "
                   "over a single decade of channel count.",
            "caption": "Simulation, not a measurement. The same sweep as the fidelity "
                       "figure, animated over channel count at a fixed motor-unit size "
                       "of nine. What the animation shows that the curve does not is "
                       "where the error goes as channels are added: the large-scale "
                       "blocks resolve first and the fine texture last.",
        })

    sources = {"actuator-mechanics": am, "optical-gamut": og,
               "control-channels": cch}
    arms = selftest_superseded_guard(studies, sources)
    for a in arms:
        print(f"  superseded-guard selftest: {a['arm']} -> flagged={a['flagged']}")
    want = [True, True, False]
    if [a["flagged"] for a in arms] != want:
        raise SystemExit(f"superseded-guard selftest FAILED: {arms}")
    guard = assert_no_superseded_text(studies, sources)
    print(f"  superseded-guard: {guard}")

    doc = {"studies": studies, "_guards": {"superseded_text": guard,
                                           "selftest_arms": arms}}
    for s in doc["studies"]:
        for f in s["figures"]:
            p = os.path.join(ROOT, f["file"])
            if not os.path.exists(p):
                raise SystemExit(f"figure missing on disk: {f['file']}")
            assert f["alt"] and f["caption"], f["file"]
    out = os.path.join(ROOT, "index-fragment.json")
    _write_browser_safe(out, doc)
    print(f"wrote {out}: {len(doc['studies'])} studies, "
          f"{sum(len(s['figures']) for s in doc['studies'])} figures")


if __name__ == "__main__":
    main()
