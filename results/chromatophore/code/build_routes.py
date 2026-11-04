"""Build routes.json for the programmable-skin design space.

A builder rather than a hand-written file, so that every citation string is
GENERATED from the verified record in lit/library.json, every outcome-class
regex is run against the routes it claims to match, and the evidence tally is
computed rather than asserted. Typing citations by hand produced a wrong one
(PMID 40752587 was written as "Klaassen/Chen tilapia"; it is Liang G et al.
2025, New Biotechnol 89:163-176), which is why nothing here is typed.
"""
from __future__ import annotations

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = json.load(open(os.path.join(ROOT, "lit", "library.json")))


def cite(pmid: str) -> str:
    r = LIB[pmid]
    au = r.get("authors") or []
    who = au[0] if au else "?"
    if len(au) == 2:
        who = f"{au[0]} & {au[1]}"
    elif len(au) > 2:
        who = f"{au[0]} et al."
    jr = r.get("iso_journal") or r.get("journal") or ""
    vol = r.get("volume") or ""
    pg = r.get("pages") or ""
    loc = f"{jr} {vol}:{pg}".strip().rstrip(":")
    return f"{who} {r.get('year')}, {loc}, '{r.get('title')}'"


def ev(*pairs):
    """pairs: (pmid, read_level) or (pmid, read_level, note)."""
    out = []
    for p in pairs:
        pmid, rl = p[0], p[1]
        d = {"cite": cite(pmid), "pmid": pmid, "doi": LIB[pmid].get("doi"),
             "read_level": rl}
        if len(p) > 2:
            d["note"] = p[2]
        out.append(d)
    return out


FT, AB, LS = "full-text", "abstract", "listing"

SCALES = [
    {"key": "molecular", "label": "Molecular - pigment and protein",
     "blurb": "Ommochrome synthesis and the reflectin proteins. This is where the only "
              "two demonstrated cephalopod genetic manipulations live, and both of them "
              "REMOVE pigment rather than control it."},
    {"key": "organelle", "label": "Organelle - the optical stack",
     "blurb": "The Bragg reflector inside an iridophore and the pigment sacculus inside "
              "a chromatophore. The best-measured objects in the whole design space: "
              "layer counts, both refractive indices, both thicknesses and the tuning "
              "range are published numbers from LIVE cells."},
    {"key": "cell", "label": "Cell - the chromatophore as an actuator",
     "blurb": "A pigment sac opened by 15-25 radial muscle fibres under direct "
              "motor-neuron control. Our own mechanics model says the stroke is limited "
              "by the elastic sacculus, not by the muscle, which makes most "
              "muscle-side interventions useless."},
    {"key": "circuit", "label": "Circuit - how many independent channels",
     "blurb": "Motor units, polyneuronal innervation and sub-chromatophore sectors. "
              "Measured in beautiful detail and manipulable almost not at all: every "
              "route here is a recording or a stimulation, not a construction."},
    {"key": "development", "label": "Development - laying out an addressable array",
     "blurb": "A cuttlefish goes from a few thousand chromatophores to a few million "
              "while keeping the light:dark ratio constant and inserting new units far "
              "from old ones. The layout rule is measured; nothing has been intervened on."},
    {"key": "genetic_access", "label": "Genetic access - can you build anything at all",
     "blurb": "The gate on the entire cephalopod half of this design space. Two knockouts "
              "exist. No transgene has been expressed in a cephalopod chromatophore."},
    {"key": "vertebrate", "label": "Vertebrate chromatophores - the tractable substrate",
     "blurb": "Teleost and amphibian chromatophores move pigment on microtubules rather "
              "than by muscle: roughly an order of magnitude slower, and vastly more "
              "genetically tractable. A serious alternative substrate, not a footnote."},
    {"key": "synthetic", "label": "Synthetic and non-living - the honest comparator",
     "blurb": "What a funder will ask about. A 16x16 addressable colour-changing sheet "
              "was built in 2014 and switches in 1-2 s; commercial electrophoretic "
              "panels run at 300 ppi. Any biological route must beat these on some axis."},
]

EVIDENCE_LABELS = {
    "direct_cephalopod_phenotype": "direct cephalopod phenotype",
    "direct_other_species": "direct phenotype, another species",
    "cis_regulatory_inference": "cis-regulatory inference",
    "model_only": "model only (ours or a published model)",
    "proposed": "proposed - nobody has done this",
}

# PATTERNS HERE MUST COMPILE IN A BROWSER AS WELL AS IN PYTHON. They are emitted
# into routes.json and compiled by the renderer with `new RegExp(pattern, "i")`.
# An earlier version began each one with the Python inline flag `(?i)`, which
# JavaScript rejects as a SyntaxError - and the renderer's defensive try/catch
# turned that compile error into an empty outcome tag on every route, which
# removed the filter control, which crashed the page several hundred lines later
# on a missing form field. A three-character prefix presented as a selector
# timeout four layers downstream. Case-insensitivity is supplied by the caller on
# both sides: `re.IGNORECASE` here, the "i" flag there.
# Also avoid: (?P<name>...), (?P=name), \A, \Z, (?#comment), possessive
# quantifiers. `check_js_regex_compatibility` in validate() enforces this.
#
# Every class is run against every route's predicted_phenotype by `validate`,
# which reports both the per-class hit count and any route no class matches.
# The first version left 13 of 46 routes unmatched, which would have shipped a
# filter that silently hides a quarter of the page.
OUTCOME_CLASSES = [
    {"key": "pigment_removed", "label": "Pigment removed or reduced",
     "match": r"(albino|unpigmented|no visible pigment|lose their pigment|loss of pigment|pigmentation (is )?(lost|absent|eliminated|reduced)|colourless|transparent|graded pigmentation|no pigment cells)"},
    {"key": "optics_retuned", "label": "Optics retuned (spectrum, reflectance, gamut)",
     "match": r"(reflectance|reflector|spectral|spectrum|wavelength|nm\b|gamut|refractive index|iridescen|colour shift|absorption edge|hue|luminance|fluorescen|infrared|peak)"},
    {"key": "kinetics_changed", "label": "Speed or timing changed",
     "match": r"(\bms\b|millisecond|rise time|time constant|faster|slower|\bs\b|seconds|per second|latency|relaxation time|frames per second)"},
    {"key": "stroke_changed", "label": "Expansion stroke changed",
     "match": r"(expansion ratio|area ratio|area change|stroke|expands?\b|expand further|retraction|%\s*area|opens? it)"},
    {"key": "addressability_changed", "label": "Addressability or control changed",
     "match": r"(independent(ly)?|channel|motor (unit|neuron)|sector|addressab|on command|on demand|per-cell|drive|stimulat|pattern component|dimension|projector|map\b)"},
    {"key": "array_layout_changed", "label": "Array layout or density changed",
     "match": r"(spacing|density|array|insertion|layout|stripe|spot|pattern (re-?)?forms|Turing|labyrinth|leopard|migrate|texture|3D shape)"},
    {"key": "capability_unlocked", "label": "A capability, not a phenotype yet",
     "match": r"(nothing yet|has not been demonstrated|precondition|a cephalopod in which|candidate promoter|platform|yardstick|unknown, and that is the point|efficient F0)"},
    {"key": "non_living_device", "label": "A device, not an animal",
     "match": r"(film|coating|device|pixel|elastomer|microfluidic|sheet|panel|laminate|in a dish|cell culture|HEK|product page|commercial)"},
]


# A route's EVIDENCE STRENGTH says how well supported it is. It does not say
# whether the route is something you DO or something you WATCH, and conflating
# the two is how a page like this flatters itself: "16 routes with direct
# cephalopod evidence" sounds like 16 things you can do, and it is not.
# Assigned by hand, tallied by `validate`, and cross-tabbed against evidence
# strength so the two cannot be confused.
ROUTE_KIND = {
    "heritable_edit": "a permanent change to the genome, made once",
    "acute_perturbation": "something done to a living or freshly dissected animal that "
                          "changes its state now and wears off",
    "measurement": "a measurement of the unmodified system; nothing is changed",
    "platform": "a capability or a chassis; no phenotype of its own",
    "model": "a prediction from a model, ours or a published one; nothing was done",
    "device": "built from non-living materials",
}
KIND_OF = {
    "mol-tdo-knockout": "heritable_edit",
    "mol-tdo-ido-albino-line": "heritable_edit",
    "mol-timed-crispr-graded-pigment": "heritable_edit",
    "mol-reflectin-index-engineering": "model",
    "org-reflectin-phosphorylation": "measurement",
    "org-neural-iridophore-tuning": "acute_perturbation",
    "org-leucophore-backing": "model",
    "org-soften-the-sacculus": "model",
    "cell-add-radial-muscles": "model",
    "cell-lengthen-fibre-reach": "model",
    "cell-glutamate-drive": "acute_perturbation",
    "cell-serotonergic-brake": "acute_perturbation",
    "circ-count-channels-per-chromatophore": "measurement",
    "circ-single-motoneuron-stimulation": "acute_perturbation",
    "circ-map-motor-units": "acute_perturbation",
    "circ-optic-lobe-microstimulation": "acute_perturbation",
    "circ-low-dimensional-transitions": "measurement",
    "circ-size-the-controller": "model",
    "circ-dermal-photoreception-loop": "measurement",
    "dev-inhibitory-surround": "model",
    "dev-insertion-rate": "measurement",
    "dev-grow-the-array-without-losing-address": "measurement",
    "gen-euprymna-chassis": "platform",
    "gen-doryteuthis-efficiency": "platform",
    "gen-transgene-in-a-chromatophore": "platform",
    "gen-find-the-promoter": "platform",
    "vert-melanopsin-light-actuator": "heritable_edit",
    "vert-dreadd-chemical-drive": "model",
    "vert-optogenetic-scramble": "heritable_edit",
    "vert-ltk-iridophore-dial": "heritable_edit",
    "vert-cx41-8-turing-reprogram": "heritable_edit",
    "vert-transparent-chassis": "heritable_edit",
    "vert-speed-ceiling": "measurement",
    "syn-optoelectronic-sheet": "device",
    "syn-dielectric-elastomer-chromatophore": "device",
    "syn-reflectin-in-human-cells": "device",
    "syn-reflectin-electro-film": "device",
    "syn-adaptive-infrared": "device",
    "syn-texture-not-colour": "device",
    "syn-electrophoretic-benchmark": "device",
    "mol-swap-the-ommochrome": "model",
    "org-lamella-pair-count": "model",
    "cell-muscle-coupling-between-organs": "model",
    "dev-reinnervation-on-colour-change": "measurement",
    "syn-microfluidic-dye": "device",
    "syn-photomechanical-fluorescent-display": "device",
}
# Routes that give SPATIALLY ADDRESSABLE RUNTIME CONTROL - a dial you could use
# in a working programmable skin, addressed to a place, changeable second by
# second. This is the capability the whole design space is named after.
ADDRESSABLE_RUNTIME = {
    "circ-single-motoneuron-stimulation", "circ-map-motor-units",
    "circ-optic-lobe-microstimulation", "vert-melanopsin-light-actuator",
    "vert-optogenetic-scramble", "syn-optoelectronic-sheet",
    "syn-reflectin-electro-film", "syn-adaptive-infrared", "syn-texture-not-colour",
    "syn-electrophoretic-benchmark", "syn-microfluidic-dye",
    "syn-photomechanical-fluorescent-display",
}

# Which ANIMAL each route's evidence actually comes from. Recorded because this page
# otherwise silently merges a cuttlefish, a bobtail squid, two different loliginid
# squid and an octopus into one organism: the actuator fit is Doryteuthis pealeii,
# the asymmetry comparison adds Euprymna berryi and Sepia officinalis, the optics are
# Doryteuthis opalescens, and the control-layer anchor is Euprymna berryi and Sepia.
# Only species named in a title or abstract we read are given; "squid (species not
# read)" is used rather than a guess.
CEPH = "cephalopod"
SPECIES = {
    "mol-tdo-knockout": ["Doryteuthis pealeii"],
    "mol-tdo-ido-albino-line": ["Euprymna berryi"],
    "mol-timed-crispr-graded-pigment": ["Doryteuthis pealeii"],
    "mol-reflectin-index-engineering": ["Doryteuthis opalescens", "recombinant protein, no animal"],
    "mol-swap-the-ommochrome": ["Sepia officinalis", "squid (species not read)"],
    "org-lamella-pair-count": ["Doryteuthis opalescens"],
    "org-reflectin-phosphorylation": ["Doryteuthis pealeii", "loliginid squid (species not read)"],
    "org-neural-iridophore-tuning": ["Doryteuthis pealeii"],
    "org-leucophore-backing": ["Doryteuthis opalescens"],
    "org-soften-the-sacculus": ["Doryteuthis pealeii"],
    "cell-add-radial-muscles": ["Euprymna berryi", "Sepia officinalis", "Sepioteuthis lessoniana"],
    "cell-lengthen-fibre-reach": ["squid (species not read)"],
    "cell-glutamate-drive": ["Sepia officinalis", "squid (species not read)"],
    "cell-serotonergic-brake": ["Ommastrephidae and Loliginidae (species not read)",
                                "Sepioteuthis lessoniana"],
    "cell-muscle-coupling-between-organs": ["squid (species not read)"],
    "circ-count-channels-per-chromatophore": ["Euprymna berryi", "Sepia officinalis"],
    "circ-single-motoneuron-stimulation": ["Euprymna berryi", "Sepia officinalis"],
    "circ-map-motor-units": ["Sepia officinalis"],
    "circ-optic-lobe-microstimulation": ["squid (species not read)"],
    "circ-low-dimensional-transitions": ["Sepia officinalis"],
    "circ-size-the-controller": ["model; anchored in Sepia officinalis, Euprymna berryi "
                                 "and Doryteuthis pealeii, which is three animals"],
    "circ-dermal-photoreception-loop": ["Doryteuthis pealeii"],
    "dev-inhibitory-surround": ["Sepia officinalis"],
    "dev-insertion-rate": ["Sepia officinalis"],
    "dev-reinnervation-on-colour-change": ["Sepia officinalis"],
    "dev-grow-the-array-without-losing-address": ["Sepia officinalis"],
    "gen-euprymna-chassis": ["Euprymna berryi", "bobtail squid (species not read)"],
    "gen-doryteuthis-efficiency": ["Doryteuthis pealeii"],
    "gen-transgene-in-a-chromatophore": ["none - this has not been done in any cephalopod"],
    "gen-find-the-promoter": ["Loligo vulgaris", "bobtail squid (species not read)",
                              "Octopus bimaculoides"],
    "vert-melanopsin-light-actuator": ["Xenopus laevis", "Danio rerio", "zebrafish/Xenopus mix"],
    "vert-dreadd-chemical-drive": ["Oreochromis mossambicus"],
    "vert-optogenetic-scramble": ["Danio rerio"],
    "vert-ltk-iridophore-dial": ["Danio rerio"],
    "vert-cx41-8-turing-reprogram": ["Danio rerio"],
    "vert-transparent-chassis": ["tilapia (Oreochromis, species not read)"],
    "vert-speed-ceiling": ["Epinephelus striatus", "Oreochromis niloticus",
                           "Paracheirodon innesi", "Doryteuthis pealeii"],
    "syn-optoelectronic-sheet": ["not an animal"],
    "syn-microfluidic-dye": ["not an animal"],
    "syn-dielectric-elastomer-chromatophore": ["not an animal"],
    "syn-reflectin-in-human-cells": ["Homo sapiens cell line (HEK293)"],
    "syn-reflectin-electro-film": ["not an animal"],
    "syn-adaptive-infrared": ["not an animal"],
    "syn-texture-not-colour": ["not an animal"],
    "syn-photomechanical-fluorescent-display": ["not an animal"],
    "syn-electrophoretic-benchmark": ["not an animal"],
}

R = []


# Six routes were written, cut to bring the page inside the 25-40 range it was
# specified at, and then RESTORED when that range turned out to be a floor rather
# than a cap. The set is kept as a record of the judgement and its reversal, and
# the reasons each one was nearly cut are in NOTES.md.
NEARLY_CUT = {"cell-muscle-coupling-between-organs", "mol-swap-the-ommochrome",
              "syn-photomechanical-fluorescent-display", "org-lamella-pair-count",
              "dev-reinnervation-on-colour-change", "syn-microfluidic-dye"}
CUT = set()


def route(**kw):
    if kw["id"] in CUT:
        return
    kw["route_kind"] = KIND_OF[kw["id"]]
    kw["addressable_runtime_control"] = kw["id"] in ADDRESSABLE_RUNTIME
    kw["species_of_evidence"] = SPECIES.get(kw["id"], ["not stated"])
    if kw["id"] in NEARLY_CUT:
        kw["editorial_note"] = ("Written, cut to meet a route-count range, then restored "
                                "when that range turned out to be a floor. See NOTES.md "
                                "for the reason it was nearly cut.")
    R.append(kw)


# ======================= molecular =========================================
route(
    id="mol-tdo-knockout", scale="molecular",
    title="Knock out tryptophan 2,3-dioxygenase to delete ommochrome pigment",
    intervention="CRISPR-Cas9 ribonucleoprotein against tdo, injected into early "
                 "Doryteuthis pealeii embryos.",
    predicted_phenotype="Eyes and chromatophores lose their pigment: an unpigmented "
                        "animal whose chromatophore organs are still present and still "
                        "innervated, but have nothing to show. Knockout efficiency "
                        "routinely above 90%.",
    mechanism="TDO catalyses the first committed step of ommochrome synthesis from "
              "tryptophan; without it the pigment granules are never filled.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="None. A germline or early-embryo edit is permanent.",
    lethality_risk="Low for the edit itself in D. pealeii embryos; the species cannot "
                   "currently be cultured through its life cycle, which is the real limit.",
    difficulty="Demonstrated. This is the precedent the whole field rests on.",
    evidence=ev(("32735817", AB)),
)
route(
    id="mol-tdo-ido-albino-line", scale="molecular",
    title="Double knockout of tdo and ido to get a heritable albino line",
    intervention="CRISPR-Cas9 against both tdo and ido in Euprymna berryi, bred to "
                 "homozygosity over generations.",
    predicted_phenotype="A true albino squid line that breeds true, used for two-photon "
                        "calcium imaging of brain activity through the unpigmented tissue.",
    mechanism="E. berryi carries an indoleamine 2,3-dioxygenase that catalyses the same "
              "reaction as TDO, so single tdo knockouts stayed pigmented; removing both "
              "closes the pathway.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="None.",
    lethality_risk="Low: the line is viable and fertile through multiple generations.",
    difficulty="Demonstrated, and it took an unexpected second gene to work. The surprise "
               "is the lesson: cephalopod biochemistry is not annotated well enough to "
               "predict which single gene is sufficient.",
    evidence=ev(("37343558", AB)),
)
route(
    id="mol-timed-crispr-graded-pigment", scale="molecular",
    title="Time the CRISPR injection to set the degree of pigmentation",
    intervention="Deliver the tdo ribonucleoprotein at chosen points in early development "
                 "rather than at the earliest possible stage.",
    predicted_phenotype="Graded pigmentation between wild type and unpigmented, set by "
                        "how late the edit arrives relative to the lineage's divisions.",
    mechanism="Later delivery leaves more already-committed cells unedited, so the mosaic "
              "fraction is a function of injection time.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="None, but the SETTING is chosen before the animal exists.",
    lethality_risk="As for the knockout.",
    difficulty="Demonstrated. Worth flagging because it is the only analogue control knob "
               "anyone has over a cephalopod chromatophore property, and it is a one-shot "
               "developmental dial, not a runtime one.",
    evidence=ev(("32735817", AB)),
)
route(
    id="mol-reflectin-index-engineering", scale="molecular",
    title="Engineer reflectin for a higher condensed-state refractive index",
    intervention="Alter reflectin's conserved RLDQSY/RMDQSH-type motif composition to "
                 "raise the refractive index of the condensed protein phase, then express "
                 "it in iridophores or in a film.",
    predicted_phenotype="Higher peak reflectance and a wider reachable gamut at the same "
                        "layer count and the same tuning range.",
    mechanism="Live-cell lamellae sit at n = 1.405 +/- 0.012 against an inter-lamellar "
              "space at 1.34, a contrast of only 1.048. Reflectance of a Bragg stack is "
              "set by that ratio raised to the power of twice the pair count.",
    evidence_strength="model_only",
    reversibility="n/a - a protein design change, not a runtime dial.",
    lethality_risk="Unknown in vivo; reflectin assembly is tied to osmotic water expulsion, "
                   "so a variant that condenses harder may not cycle.",
    difficulty="High. No one has shown a designed reflectin variant with a raised "
               "condensed-phase index in a living cell.",
    study="optical-gamut",
    evidence=ev(("23740489", FT), ("24694894", AB), ("28889973", AB),
                ("34272457", FT, "recombinant reflectin multilayers, in a film, not a cell")),
)
route(
    id="mol-swap-the-ommochrome", scale="molecular",
    title="Change which ommochrome fills the sacculus",
    intervention="Perturb the ommochrome branch downstream of TDO to shift the pigment "
                 "a chromatophore makes between the yellow, red and brown species.",
    predicted_phenotype="A chromatophore whose absorption edge moves, changing the hue it "
                        "contributes at the same expansion state.",
    mechanism="Squid chromatophores of different colours carry distinguishable metabolite "
              "fingerprints, and xanthommatin is localised to the light class in "
              "cuttlefish, so pigment identity and colour class covary.",
    evidence_strength="proposed",
    reversibility="Unknown; chromatophores darken irreversibly with age in the wild type.",
    lethality_risk="Unknown.",
    difficulty="High, and badly under-specified: no measured absorption spectrum for any "
               "cephalopod ommochrome was found, so the target hues cannot be stated.",
    evidence=ev(("42186259", AB), ("30333578", FT)),
)

# ======================= organelle =========================================
route(
    id="org-lamella-pair-count", scale="organelle",
    title="Change the number of lamella pairs in the iridophore Bragg stack",
    intervention="Alter the number of reflectin-filled lamellae per stack from the eight "
                 "or nine that contribute in live cells.",
    predicted_phenotype="Peak reflectance rises steeply with pair count while the peak "
                        "wavelength is unchanged. In our transfer-matrix model, going "
                        "from eight to nine pairs - the whole range a live cell shows - "
                        "raises the achievable gamut area by 15%, and peak reflectance "
                        "at 550 nm climbs from 0.002 at one pair to 0.187 at ten.",
    mechanism="A quarter-wave stack's admittance scales as (n_H/n_L) raised to twice the "
              "pair count, so at this very low index contrast more pairs is the cheapest "
              "way to brighten the reflector.",
    evidence_strength="model_only",
    reversibility="n/a.",
    lethality_risk="Unknown.",
    difficulty="High: nobody has manipulated lamella number. The pair count is MEASURED "
               "(eight or nine live, six or seven after chemical fixation); only the "
               "intervention is hypothetical.",
    study="optical-gamut",
    evidence=ev(("23740489", FT)),
)
route(
    id="org-reflectin-phosphorylation", scale="organelle",
    title="Phosphorylate reflectin to condense it and switch the reflector on",
    intervention="Drive the native acetylcholine-triggered phosphorylation cascade in "
                 "iridophores, or phosphorylate recombinant reflectin in vitro.",
    predicted_phenotype="The lamellae condense, expel water, thin, and the stack's "
                        "refractive index contrast rises: reflectance appears and the peak "
                        "moves to shorter wavelengths.",
    mechanism="Phosphorylation neutralises reflectin's net charge, allowing hierarchical "
              "assembly and osmotic water expulsion from the lamellae.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="Reversible in the animal; this is the native switching mechanism.",
    lethality_risk="None - it is physiology.",
    difficulty="Demonstrated as a natural mechanism. Driving it ON COMMAND in a chosen "
               "cell is not demonstrated.",
    evidence=ev(("19776150", AB), ("25918159", AB), ("22896651", AB)),
)
route(
    id="org-neural-iridophore-tuning", scale="organelle",
    title="Stimulate skin nerves to tune iridophore colour and brightness",
    intervention="Electrical stimulation of neurons in isolated Doryteuthis pealeii skin, "
                 "with acetylcholine released within the iridophore layer.",
    predicted_phenotype="The reflected peak shifts by more than 145 nm to shorter "
                        "wavelengths and peak reflectance rises by more than 245%. "
                        "Critically, the colour shift takes 17 s and the brightness change "
                        "32 s - two orders of magnitude slower than a chromatophore.",
    mechanism="Two distinct mechanisms: reflectin condensation accounts for the "
              "reflectance change, while the faster colour shift is unexplained by it and "
              "the authors say so.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="Reversible.",
    lethality_risk="n/a - an isolated skin preparation.",
    difficulty="Demonstrated. The design consequence is severe and usually glossed over: "
               "the optical stack and the pigment actuator cannot be used together for a "
               "fast pattern, because one of them needs half a minute.",
    study="optical-gamut",
    evidence=ev(("22896651", AB)),
)
route(
    id="org-leucophore-backing", scale="organelle",
    title="Switch the leucophore backing under the stack",
    intervention="Add, remove or tune the broadband-scattering leucophore layer beneath "
                 "the iridophores.",
    predicted_phenotype="Chromaticity is essentially unchanged - in our model the gamut "
                        "area moves by 0% - while peak luminance falls by a factor of five "
                        "when the backing is removed. It is a brightness layer, not a "
                        "colour layer.",
    mechanism="A diffuse white backing returns the light the partially-reflecting Bragg "
              "stack transmits, raising Y without changing the spectral shape much.",
    evidence_strength="model_only",
    reversibility="n/a.",
    lethality_risk="Unknown.",
    difficulty="High as an intervention. Tunable leucophores are measured in female "
               "Doryteuthis opalescens, so the cell type is real and known to be dynamic.",
    study="optical-gamut",
    evidence=ev(("24006348", AB), ("23740489", FT)),
)
route(
    id="org-soften-the-sacculus", scale="organelle",
    title="Soften the pigment sacculus so the same muscle opens it further",
    intervention="Reduce the elastic sacculus's shear modulus - genetically, by altering "
                 "its structural protein, or pharmacologically.",
    predicted_phenotype="Not more stroke, and much slower return. In our sweep the "
                        "steady-state ratio is already saturated at 2.56 at and below the "
                        "fitted stiffness, so softening buys nothing there - but it costs "
                        "retraction steeply: halving the fitted modulus raises the 90% "
                        "retraction from 295 ms to 543 ms, and at a twentieth of it the "
                        "organ does not return 90% of the way within six seconds. "
                        "Stiffening trades the other way: at four times the fitted "
                        "modulus retraction falls to 120 ms and the ratio collapses to "
                        "1.32.",
    mechanism="Expansion is a balance between active radial-muscle force and the "
              "sacculus's elastic restoring force; retraction is driven by that same "
              "elasticity alone against the dermal drag, so stiffness sets return speed "
              "directly. Above the fitted value it also starts to cost stroke.",
    evidence_strength="model_only",
    reversibility="Depends on the intervention.",
    lethality_risk="Unknown.",
    difficulty="High. The sacculus shear modulus has never been measured in any paper we "
               "read; it is the one FITTED parameter in our mechanics model, so this route "
               "is a prediction about a quantity nobody has a number for.",
    study="actuator-mechanics",
    evidence=ev(("34220538", FT), ("5700268", LS,
                "the classic ultrastructure paper; cited from its PubMed record, not read")),
)

# ======================= cell ==============================================
route(
    id="cell-add-radial-muscles", scale="cell",
    title="Add radial muscle fibres to the chromatophore rosette",
    intervention="Increase the number of radial muscle fibres per organ beyond the "
                 "measured 15-25.",
    predicted_phenotype="Almost nothing. In our model the expansion ratio rises from 1.62 "
                        "at 8 fibres to its plateau well before the wild-type count, "
                        "because the stroke is set by the sacculus's elasticity and not by "
                        "available force. This is a NEGATIVE design result and the most "
                        "useful thing our mechanics model says.",
    mechanism="Across every sweep the organ is elastic-limited rather than "
              "stroke-limited at the baseline geometry, so extra parallel force actuators "
              "buy stroke only until the elastic load is overcome.",
    evidence_strength="model_only",
    reversibility="n/a.",
    lethality_risk="Unknown.",
    difficulty="High, and our own model says not worth doing.",
    study="actuator-mechanics",
    evidence=ev(("42418335", FT, "15-25 radial fibres per chromatophore"),
                ("40719173", FT, "10-20 in the abstract; ~10-15 in the same paper's histology"),
                ("21483763", AB, "19-27 in Sepioteuthis lessoniana")),
)
route(
    id="cell-lengthen-fibre-reach", scale="cell",
    title="Lengthen the radial fibres' reach to the dermal anchor",
    intervention="Increase the anchor radius, so each fibre's contraction sweeps the "
                 "sacculus rim further.",
    predicted_phenotype="A larger stroke: in our sweep the area ratio rises monotonically "
                        "with anchor radius, and the organ passes out of the "
                        "stroke-limited regime.",
    mechanism="A Hill-type fibre's absolute shortening is a fixed fraction of its length, "
              "so a longer fibre moves the rim further for the same strain.",
    evidence_strength="model_only",
    reversibility="n/a.",
    lethality_risk="Unknown.",
    difficulty="High. The anchor radius is one of our ASSUMED parameters: the source "
               "describes 'an extremely elongated distal end' with no number.",
    study="actuator-mechanics",
    evidence=ev(("33998033", AB)),
)
route(
    id="cell-glutamate-drive", scale="cell",
    title="Expand a chromatophore on command with glutamate",
    intervention="Local application of L-glutamate to skin, or agonists at the "
                 "AMPA/kainate and NMDA-like receptors of the chromatophore neuromuscular "
                 "junction.",
    predicted_phenotype="The chromatophore expands, and its transmission spectrum shifts "
                        "towards lighter colours as the granule layer thins.",
    mechanism="Motor neurons make excitatory glutamatergic synapses onto the radial "
              "muscles; nitric oxide mediates part of the glutamate-dependent pathway in "
              "Sepia.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="Reversible on washout.",
    lethality_risk="n/a in an isolated preparation; systemic glutamate agonists in a live "
                   "animal are a different question and we did not find one addressed.",
    difficulty="Demonstrated. It is a bath, not an address: it drives every chromatophore "
               "it reaches, so it is a chemistry control and not a spatial one.",
    evidence=ev(("30333578", FT), ("12581168", AB), ("20516065", AB)),
)
route(
    id="cell-serotonergic-brake", scale="cell",
    title="Use the myogenic rhythm and its serotonergic brake as a second channel",
    intervention="Apply serotonin, or block it, in skin showing spontaneous myogenic "
                 "chromatophore activity.",
    predicted_phenotype="Spontaneous chromatophore oscillation is suppressed or released, "
                        "independently of the motor-neuron drive.",
    mechanism="Squid chromatophore networks show myogenic activity under serotonergic "
              "inhibition - a slow modulatory channel layered on top of the fast "
              "glutamatergic one.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="Reversible.",
    lethality_risk="Unknown systemically.",
    difficulty="Demonstrated in preparation. Interesting for a designer because it is a "
               "SECOND, chemically distinct control channel over the same actuator.",
    evidence=ev(("29061686", AB), ("21483763", AB,
                "miniature oscillations contributing to natural pattern expression")),
)
route(
    id="cell-muscle-coupling-between-organs", scale="cell",
    title="Cut or add the muscle-to-muscle links between neighbouring chromatophores",
    intervention="Sever, or engineer, the direct radial-muscle contacts between adjacent "
                 "chromatophore organs.",
    predicted_phenotype="Changed spatial correlation between neighbouring units at "
                        "unchanged neural drive: a mechanically blurrier or sharper skin.",
    mechanism="Radial muscles of neighbouring chromatophores make direct contacts, so the "
              "array has mechanical coupling the wiring diagram does not show.",
    evidence_strength="proposed",
    reversibility="n/a.",
    lethality_risk="Unknown.",
    difficulty="High. The anatomy is described; the functional consequence is the authors' "
               "own suggestion ('could influence') and has not been tested.",
    evidence=ev(("33998033", AB)),
)

# ======================= circuit ===========================================
route(
    id="circ-count-channels-per-chromatophore", scale="circuit",
    title="Measure how many independent channels drive ONE chromatophore",
    intervention="Divide each chromatophore into 36 polar slices, track slice areas at "
                 "20 fps, and separate the sources by PCA followed by ICA.",
    predicted_phenotype="Each chromatophore is driven by 3.715 +/- 1.211 independent "
                        "sources (1829 cells, sedated), each innervating a contiguous "
                        "petal-shaped domain of 3 to 16 of the 36 slices. Sedation does "
                        "not change it (3.683 +/- 1.224 unsedated, p = 0.83).",
    mechanism="Polyneuronal innervation with non-overlapping angular territories, so a "
              "single chromatophore is roughly four independent actuators and not one.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="n/a - a measurement.",
    lethality_risk="Animals were head-fixed, sedated or not; this is terminal or "
                   "near-terminal work.",
    difficulty="Demonstrated. This is the single most important number in the design "
               "space for anyone building an addressable skin: the pixel is not the cell.",
    study="control-channels",
    evidence=ev(("42418335", FT)),
)
route(
    id="circ-single-motoneuron-stimulation", scale="circuit",
    title="Fire one motor neuron and watch its field expand",
    intervention="Intracellular stimulation of a single chromatophore-lobe motor neuron "
                 "with simultaneous high-speed video of the skin.",
    predicted_phenotype="About five nearby chromatophores each expand partially and "
                        "directionally, in petals pointing at a common virtual centre - "
                        "not whole cells switching on. Some units instead expand "
                        "isotropically, and the authors report that too.",
    mechanism="One motor neuron's terminals reach contiguous angular sectors of several "
              "adjacent chromatophores, forming a 'virtual chromatophore'.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="n/a.",
    lethality_risk="Terminal preparation.",
    difficulty="Demonstrated, and technically hard.",
    study="control-channels",
    evidence=ev(("42418335", FT)),
)
route(
    id="circ-map-motor-units", scale="circuit",
    title="Map motor units by minimal stimulation of distal nerve branchlets",
    intervention="Threshold electrical stimulation of nerve branchlets in freshly "
                 "dissected dorsal mantle skin, scoring which chromatophores expand.",
    predicted_phenotype="Small monochromatic units of 2-10 chromatophores, usually "
                        "clustered, with a median radius of 2.5 chromatophores or 247 um. "
                        "Light units are harder to stimulate in isolation than dark ones, "
                        "suggesting smaller axons.",
    mechanism="Each motor neuron innervates a small, colour-pure, spatially clustered set.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="n/a.",
    lethality_risk="Terminal preparation.",
    difficulty="Demonstrated.",
    study="control-channels",
    evidence=ev(("30333578", FT)),
)
route(
    id="circ-optic-lobe-microstimulation", scale="circuit",
    title="Microstimulate the optic lobe to call up body-pattern components",
    intervention="Focal electrical stimulation at sites across the squid optic lobe.",
    predicted_phenotype="Discrete, repeatable body-pattern components appear, organised "
                        "mosaically rather than somatotopically across the lobe.",
    mechanism="The optic lobe holds a mosaic map of pattern components, not of skin "
              "position, so the addressing above the motoneurons is by PATTERN, not by place.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="Reversible within a session.",
    lethality_risk="Invasive brain work; terminal.",
    difficulty="Demonstrated. For a designer, this says the natural control hierarchy "
               "compresses the skin into a pattern vocabulary - which is also what the "
               "9-dimensional transition manifold below says.",
    evidence=ev(("28123014", AB)),
)
route(
    id="circ-low-dimensional-transitions", scale="circuit",
    title="Exploit the low dimensionality of real pattern transitions",
    intervention="Track 17,305 chromatophores at 60 frames per second through repeated "
                 "dark-to-light startle transitions and project into principal components.",
    predicted_phenotype="The animal moves through very similar intermediate states every "
                        "time, with 85% of the variance in 9 dimensions - from a "
                        "17,305-dimensional actuator array.",
    mechanism="Neural constraints, not mechanical ones, restrict the paths pattern "
              "transitions can take; nothing physical forbids a direct route.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="n/a.",
    lethality_risk="None - freely behaving animals.",
    difficulty="Demonstrated. This is the strongest empirical argument that a programmable "
               "skin needs far fewer channels than it has actuators, and it is a measured "
               "number rather than our model's.",
    study="control-channels",
    evidence=ev(("30333578", FT)),
)
route(
    id="circ-size-the-controller", scale="circuit",
    title="Size the controller: how many channels, at what motor-unit size",
    intervention="Sweep the number of independent control channels and the motor-unit "
                 "size against pre-declared target patterns in a model array at the "
                 "measured chromatophore density, and find the knee.",
    predicted_phenotype="See the control-channels study for the measured knee and its "
                        "spread across seeds. The headline is a channel count per unit "
                        "skin area, which is the spec sheet anyone building this needs.",
    mechanism="Below the knee the skin cannot cover the target; above it, extra channels "
              "address actuators that are already driven by a neighbour.",
    evidence_strength="model_only",
    reversibility="n/a.",
    lethality_risk="n/a.",
    difficulty="Our own study. Every structural input is measured (array density, "
               "motor-unit sizes, expansion ratio); the observer's acuity is assumed.",
    study="control-channels",
    evidence=ev(("30333578", FT), ("42418335", FT), ("34220538", FT)),
)
route(
    id="circ-dermal-photoreception-loop", scale="circuit",
    title="Close the loop in the skin itself with dermal photoreception",
    intervention="Use the opsin and phototransduction machinery already present in "
                 "chromatophores to make the skin respond to local light without the brain.",
    predicted_phenotype="Local, brain-independent modulation of chromatophore state by "
                        "the light falling on that patch of skin.",
    mechanism="Rhodopsin, retinochrome and the phototransduction cascade are expressed in "
              "and around cephalopod chromatophores, and the longfin squid carries an "
              "unexpected diversity of photoreceptor classes.",
    evidence_strength="cis_regulatory_inference",
    reversibility="n/a.",
    lethality_risk="n/a.",
    difficulty="The MACHINERY is demonstrated by expression and localisation. That the "
               "skin uses it to drive chromatophores is an inference the authors state as "
               "a suggestion ('suggest dermal photoreception'), not a measured behaviour.",
    evidence=ev(("25994635", AB), ("26351853", AB)),
)

# ======================= development =======================================
route(
    id="dev-inhibitory-surround", scale="development",
    title="Change the inhibitory surround that spaces new chromatophores",
    intervention="Alter the size, or the age-dependence of the size, of the hypothetical "
                 "inhibitory field each chromatophore projects around itself.",
    predicted_phenotype="A different array layout at the same density: varying the "
                        "surround in the published simulation generates other known "
                        "cephalopod distributions, including the clustered units seen in "
                        "some squid species.",
    mechanism="New chromatophores are inserted far from existing ones; a sigmoidal "
              "inhibitory surround whose size changes with age reproduces the measured "
              "spacing of new versus old units.",
    evidence_strength="model_only",
    reversibility="n/a - developmental.",
    lethality_risk="Unknown.",
    difficulty="High. The surround is HYPOTHETICAL: it is a term in a simulation fitted "
               "to spacing measurements, with no molecule attached to it.",
    study="control-channels",
    evidence=ev(("30333578", FT)),
)
route(
    id="dev-insertion-rate", scale="development",
    title="Change the insertion rate and watch the colour ratio defend itself",
    intervention="Alter skin growth rate or the fraction of existing chromatophores that "
                 "seeds new ones per day.",
    predicted_phenotype="The light-to-dark ratio should move - and in the wild type it "
                        "does not: it stays at 1.06 +/- 0.19 to 1 across animals from 8 to "
                        "252 days old, while insertion falls from 4.1%/day at 7 days to "
                        "0.6%/day at 105 days and the light-state lifetime rises from "
                        "about 19 to about 97 days.",
    mechanism="Insertion rate and light-state lifetime are balanced along a curve the "
              "authors derive analytically, and the measured pairs fall on it.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="n/a.",
    lethality_risk="None - longitudinal imaging of behaving animals.",
    difficulty="The MEASUREMENT is done and is excellent. The INTERVENTION is proposed: "
               "nobody has perturbed either quantity.",
    evidence=ev(("30333578", FT), ("21957106", AB)),
)
route(
    id="dev-reinnervation-on-colour-change", scale="development",
    title="Re-innervate chromatophores as they change colour class",
    intervention="Test whether a chromatophore's motor neuron is swapped when the cell "
                 "transitions from the light to the dark class at about 19 days.",
    predicted_phenotype="Motor units stay monochromatic across the animal's life without "
                        "the animal having to track each unit's age.",
    mechanism="If new motor neurons innervated only newly born light chromatophores, the "
              "animal would need to know each unit's age to keep units colour-pure. "
              "Re-innervation removes that requirement.",
    evidence_strength="proposed",
    reversibility="n/a.",
    lethality_risk="Unknown.",
    difficulty="Open. The supporting observation is indirect - red (transitioning) "
               "chromatophores have smaller mean diameter and smaller size variance than "
               "light or dark ones - and the authors present it as a hypothesis.",
    evidence=ev(("30333578", FT)),
)
route(
    id="dev-grow-the-array-without-losing-address", scale="development",
    title="Grow the array a hundredfold while keeping it addressable",
    intervention="The developmental problem itself: go from a few thousand chromatophores "
                 "in a hatchling to a few millions before death, with new units inserted "
                 "daily into a stretching sheet, without the control map going stale.",
    predicted_phenotype="An addressable array whose addresses survive an order-of-"
                        "magnitude change in element count. No engineered display has this "
                        "property and none needs it.",
    mechanism="Local insertion rules plus (hypothesised) re-innervation, with no global "
              "coordinate system anywhere in the account.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="n/a.",
    lethality_risk="None.",
    difficulty="This is the part of the design space with the least engineering competition "
               "and, we think, the most transferable idea in it.",
    evidence=ev(("30333578", FT), ("21957106", AB)),
)

# ======================= genetic access ====================================
route(
    id="gen-euprymna-chassis", scale="genetic_access",
    title="Use Euprymna berryi as the transgenic chassis",
    intervention="Adopt E. berryi: large embryo numbers, culturable through the whole life "
                 "cycle, sequenced genome, and an existing germline knockout line.",
    predicted_phenotype="A cephalopod in which edits can be made, bred and recovered - the "
                        "precondition for everything else on the cephalopod side.",
    mechanism="n/a - a platform choice.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="n/a.",
    lethality_risk="Low; lines are viable.",
    difficulty="Demonstrated for knockout. Not demonstrated for anything that ADDS a "
               "function.",
    evidence=ev(("37343558", AB),
                ("40481147", AB, "a bobtail squid (Euprymna) atlas; the other published "
                                 "cephalopod cell-type atlas is Loligo vulgaris, a "
                                 "different animal, and is cited only under "
                                 "gen-find-the-promoter")),
)
route(
    id="gen-doryteuthis-efficiency", scale="genetic_access",
    title="Use Doryteuthis pealeii for high-efficiency embryo editing",
    intervention="CRISPR-Cas9 in D. pealeii embryos, where knockout efficiency routinely "
                 "exceeds 90%.",
    predicted_phenotype="Efficient F0 knockouts, in the species with the best-characterised "
                        "chromatophore physiology and the largest axons.",
    mechanism="n/a.",
    evidence_strength="direct_cephalopod_phenotype",
    reversibility="n/a.",
    lethality_risk="Low for the edit.",
    difficulty="Demonstrated for F0. The species is not closed-life-cycle in culture, so "
               "there is no germline route in it - a real split from E. berryi.",
    evidence=ev(("32735817", AB)),
)
route(
    id="gen-transgene-in-a-chromatophore", scale="genetic_access",
    title="Express ANY transgene in a cephalopod chromatophore",
    intervention="Deliver a chromatophore-specific promoter driving any protein - a "
                 "fluorophore, a channelrhodopsin, a designer receptor - into a cephalopod "
                 "and show it is expressed in the right cell.",
    predicted_phenotype="Nothing yet. This has not been demonstrated.",
    mechanism="n/a.",
    evidence_strength="proposed",
    reversibility="n/a.",
    lethality_risk="Unknown.",
    difficulty="This is the gate. Every cephalopod route that ADDS a controllable element "
               "- optogenetic drive, a designer receptor, an engineered reflectin, a "
               "reporter of motor-unit identity - is downstream of this one step, and the "
               "step has no published precedent we found. Both demonstrated cephalopod "
               "manipulations delete a gene; neither expresses one.",
    evidence=ev(("32735817", AB), ("37343558", AB), ("36594460", AB)),
)
route(
    id="gen-find-the-promoter", scale="genetic_access",
    title="Mine single-cell atlases for a chromatophore-specific promoter",
    intervention="Mine the published cephalopod single-cell atlases - cell types in "
                 "Loligo vulgaris, and a bobtail squid visual and nervous system atlas - "
                 "for genes expressed in chromatophore muscle or pigment cells and "
                 "nowhere else, then test their regulatory regions.",
    predicted_phenotype="A candidate promoter that drives expression in chromatophores "
                        "specifically - the missing reagent for the route above.",
    mechanism="Cell-type-resolved transcriptomes give candidate marker genes; their "
              "upstream regions are candidate drivers.",
    evidence_strength="cis_regulatory_inference",
    reversibility="n/a.",
    lethality_risk="n/a.",
    difficulty="Feasible now and, as far as we found, not yet done. Two cautions. The "
               "inference from 'expressed specifically' to 'its promoter drives "
               "specifically' is exactly the inference that fails often enough to need "
               "testing. And neither atlas is in the species with the germline route: "
               "the cell-type atlas is Loligo vulgaris and the nervous-system atlas is a "
               "bobtail squid, while the only heritable knockout line is Euprymna "
               "berryi, so a promoter found in one animal has to be shown to work in "
               "another.",
    evidence=ev(("36594460", AB), ("40481147", AB), ("26268193", AB)),
)

# ======================= vertebrate ========================================
route(
    id="vert-melanopsin-light-actuator", scale="vertebrate",
    title="Put melanopsin in a melanophore and command it with light",
    intervention="Express Opn4x under a melanophore promoter in zebrafish and project "
                 "patterned blue light.",
    predicted_phenotype="Cell-autonomous pigment dispersion (darkening) of individual "
                        "melanophores under blue light, reversible in the dark, with the "
                        "spatial pattern set by the projector.",
    mechanism="Melanopsin drives dispersion in Xenopus melanophores through "
              "phospholipase C and calcium; zebrafish melanophores carry the same "
              "dynein/kinesin melanosome transport machinery.",
    evidence_strength="direct_other_species",
    reversibility="Fully reversible - light off.",
    lethality_risk="Low.",
    difficulty="Each half is demonstrated in a different animal; the combination is not. "
               "Note the authors' own complication: in Xenopus the IN VITRO response is "
               "direct and dispersing, while the IN VIVO embryo response needs the eye "
               "and pituitary alpha-MSH and goes the other way. We keep both readings.",
    evidence=ev(("26108966", AB), ("26095528", AB,
                "the in vivo route disagrees with the in vitro one; both kept"),
                ("25143402", AB), ("30911050", AB)),
)
route(
    id="vert-dreadd-chemical-drive", scale="vertebrate",
    title="Drive melanophores with a designer receptor and a designer ligand",
    intervention="Express a Gi-coupled DREADD in melanophores and dose the animal with "
                 "its ligand.",
    predicted_phenotype="Ligand-dependent, dose-graded melanosome aggregation - a pale "
                        "animal on command.",
    mechanism="Alpha-2 adrenoceptors, which are Gi-coupled, predominantly mediate "
              "aggregation in tilapia melanophores; a designer Gi receptor should enter "
              "the same pathway.",
    evidence_strength="model_only",
    reversibility="Reversible on clearance.",
    lethality_risk="Low.",
    difficulty="The inference from 'alpha-2 aggregates' to 'any Gi receptor aggregates' "
               "is the weak link, and it is OUR inference, not the source's. The field "
               "also disagrees about cAMP's sign: PACAP raises cAMP and AGGREGATES "
               "tilapia melanophores, which the authors themselves call paradoxical, "
               "while in zebrafish cAMP/PKA disperses.",
    evidence=ev(("18072544", AB)),
)
route(
    id="vert-optogenetic-scramble", scale="vertebrate",
    title="Scramble and re-form a pigment pattern with channelrhodopsin",
    intervention="Blue light on transgenic zebrafish melanophores expressing a ChR2 "
                 "variant.",
    predicted_phenotype="Melanophores depolarise and MIGRATE at random, disarranging "
                        "xanthophores and iridophores too; the pattern re-forms when the "
                        "light goes off. Works in young and adult fish but not at about "
                        "5 weeks post-fertilisation.",
    mechanism="Depolarisation drives cell migration. It is a cell-MOVEMENT tool, not a "
              "colour-change tool, and the paper reports no melanosome transport readout.",
    evidence_strength="direct_other_species",
    reversibility="Reversible - the pattern re-forms.",
    lethality_risk="None reported; the light is not harmful to the cells.",
    difficulty="Demonstrated. Included because it is the ONLY published optogenetic "
               "chromatophore experiment we found, and it is important that what it "
               "controls is position, not colour.",
    evidence=ev(("30578760", AB)),
)
route(
    id="vert-ltk-iridophore-dial", scale="vertebrate",
    title="Dial iridophore number up or down with one receptor gene",
    intervention="Use shady (ltk loss of function) or the dominant moonstone allele "
                 "ltk-mne, or an inducible ltk transgene.",
    predicted_phenotype="Loss: no silvery iridophores and an abnormal stripe pattern. "
                        "Gain: ectopic iridophores and silvery patches.",
    mechanism="Ltk controls iridophore establishment, proliferation and survival "
              "cell-autonomously, with evidence for homotypic competition.",
    evidence_strength="direct_other_species",
    reversibility="None for an allele; an inducible transgene would be.",
    lethality_risk="Low - the mutants are viable.",
    difficulty="Demonstrated both ways. The closest thing in any animal to a single-gene "
               "dial on a structural-colour cell type.",
    evidence=ev(("18369445", AB), ("26801003", AB)),
)
route(
    id="vert-cx41-8-turing-reprogram", scale="vertebrate",
    title="Reprogram the skin pattern itself with connexin41.8 variants",
    intervention="Transgenic expression of Cx41.8 or its mutants under the mitfa promoter.",
    predicted_phenotype="Narrow stripes with wide interstripes, narrow stripes with "
                        "narrow interstripes, a labyrinth, or a leopard (donut-ring) "
                        "pattern - the last predicted in advance by a Turing model.",
    mechanism="Gap-junction coupling between pigment cells sets the wavelength of a "
              "reaction-diffusion-like pigment-cell network.",
    evidence_strength="direct_other_species",
    reversibility="None.",
    lethality_risk="Low.",
    difficulty="Demonstrated, and it is the only route in this whole design space where a "
               "quantitative model PREDICTED a pattern before it was made. It changes the "
               "standing layout, not the runtime state, so it is a development route in a "
               "vertebrate body.",
    evidence=ev(("22313791", AB)),
)
route(
    id="vert-transparent-chassis", scale="vertebrate",
    title="Start from a transparent fish so your actuator is the only thing visible",
    intervention="Use tyrb;csf1ra;pnp4a ('amber') or tyrb;csf1ra;tfec ('ruby') triple "
                 "mutant tilapia, or a zebrafish nacre/csf1ra background.",
    predicted_phenotype="A medium-sized fish with no visible pigment cells, so any "
                        "introduced colour element is unambiguous. Note the honest "
                        "caveat in the source: amber stops being transparent at 60 dpf as "
                        "iridophores recover, and ruby at 120 dpf as the body wall thickens.",
    mechanism="Sequential removal of xanthophores, erythrophores, pigmented melanophores "
              "and reflective platelets by multi-gene CRISPR mutation and crossing.",
    evidence_strength="direct_other_species",
    reversibility="None.",
    lethality_risk="Low - lines are viable and used for in vivo imaging.",
    difficulty="Demonstrated. The time-limited transparency is a real constraint on any "
               "experiment that needs an adult.",
    evidence=ev(("40752587", AB)),
)
route(
    id="vert-speed-ceiling", scale="vertebrate",
    title="Find out how fast a vertebrate chromatophore can actually be driven",
    intervention="Measure single-cell melanosome aggregation and dispersion time "
                 "constants under neural and hormonal drive, which we could not find "
                 "reported.",
    predicted_phenotype="Unknown, and that is the point. The fastest vertebrate figure we "
                        "found is whole-body: Nassau groupers change pattern in 4.44 s "
                        "mean (range 0.97-9.87 s), with the fastest contrast changes under "
                        "1 s, which the authors read as direct neural control. Compare a "
                        "cephalopod chromatophore: peak expansion 117-150 ms after a "
                        "startle flash, of which only 67-83 ms is the actuator itself and "
                        "50-67 ms is sensory and neural latency.",
    mechanism="Microtubule motor transport of melanosomes, rather than muscle, sets the "
              "vertebrate timescale.",
    evidence_strength="proposed",
    reversibility="n/a - a measurement.",
    lethality_risk="Low.",
    difficulty="Cheap and apparently not done. SCOPE OF THE NEGATIVE: no melanosome-level "
               "time constant appeared in any ABSTRACT we read, across PubMed searches "
               "for tilapia melanophore aggregation, melanosome aggregation kinetics and "
               "Xenopus melanophore dispersion. No full texts were fetched, and older "
               "physiology literature was not searched. The positive control is that the "
               "same searches returned relevant papers.",
    evidence=ev(("25263436", AB), ("34220538", FT), ("23940562", AB), ("20554565", AB)),
)

# ======================= synthetic =========================================
route(
    id="syn-optoelectronic-sheet", scale="synthetic",
    title="Build the sheet out of silicon and thermochromic dye instead",
    intervention="A 1.4 cm, 16x16 pixel flexible sheet with multiplexed photodetectors "
                 "and silicon diode heaters under a thermochromic dye layer.",
    predicted_phenotype="Autonomous black-to-white pattern matching to the surroundings, "
                        "switching in 1-2 s at 10.5-11.5 V, with distributed sensing and "
                        "actuation in one laminate.",
    mechanism="Diode heating crosses the dye's 47 C threshold; photodetectors in the same "
              "laminate close the loop.",
    evidence_strength="direct_other_species",
    reversibility="Fully reversible, indefinitely.",
    lethality_risk="n/a.",
    difficulty="Built in 2014. This is the comparator every biological route has to beat, "
               "and on 'changes appearance on command' it already wins.",
    evidence=ev(("25136094", AB)),
)
route(
    id="syn-microfluidic-dye", scale="synthetic",
    title="Pump coloured fluid through channels in a silicone skin",
    intervention="Microfluidic networks moulded into a soft elastomer body, perfused with "
                 "dyed or temperature-controlled fluids.",
    predicted_phenotype="Colour, contrast, pattern, apparent shape, luminescence and "
                        "surface temperature all changed - and changed SIMULTANEOUSLY in "
                        "the visible and the infrared, which the authors note no organism "
                        "can do.",
    mechanism="Bulk transport of a coloured fluid, rather than any local actuator.",
    evidence_strength="direct_other_species",
    reversibility="Fully reversible.",
    lethality_risk="n/a.",
    difficulty="Built in 2012. Tethered to pumps, and the response time was not reported "
               "in the abstract we read.",
    evidence=ev(("22904008", AB)),
)
route(
    id="syn-dielectric-elastomer-chromatophore", scale="synthetic",
    title="Make an artificial chromatophore from a dielectric elastomer",
    intervention="A pigmented dielectric elastomer actuator that expands a coloured area "
                 "under high voltage.",
    predicted_phenotype="33-42% area change in the published modelling, needing about "
                        "5.6 kV, with a viscoelastic relaxation time around 3 s. Compare "
                        "a real chromatophore: +155% area, reached 117-150 ms after a "
                        "startle flash, of which the actuator's own expansion phase is "
                        "67-83 ms.",
    mechanism="Maxwell stress thins and stretches the elastomer, spreading the pigment.",
    evidence_strength="model_only",
    reversibility="Reversible.",
    lethality_risk="n/a.",
    difficulty="The honest comparison is unflattering to the mimic: it is four times "
               "smaller in stroke and twenty times slower than the biological actuator, "
               "and it wants kilovolts. These numbers come from a MODEL; we did not obtain "
               "measured values from the experimental paper's abstract.",
    evidence=ev(("26063823", AB), ("22549047", AB)),
)
route(
    id="syn-reflectin-in-human-cells", scale="synthetic",
    title="Express reflectin in a human cell and make it optically dynamic",
    intervention="Reflectin A1 in HEK293 cells, reconfigured with 100 mM NaCl and imaged "
                 "by quantitative phase microscopy.",
    predicted_phenotype="Reflectin particles grow from about 400 to about 800 nm over an "
                        "hour and their refractive index moves within 1.41-1.52. It is a "
                        "change in refractive index and particle size, NOT a demonstrated "
                        "colour change, and the paper does not claim one.",
    mechanism="Salt screens reflectin's charge, driving the same condensation that "
              "phosphorylation drives in a squid iridophore.",
    evidence_strength="direct_other_species",
    reversibility="Partially; cycling was not the focus.",
    lethality_risk="n/a - cell culture.",
    difficulty="Demonstrated. The gap between 'the protein assembles in a human cell' and "
               "'the cell changes colour' is the whole remaining problem.",
    evidence=ev(("37519901", FT)),
)
route(
    id="syn-reflectin-electro-film", scale="synthetic",
    title="Switch a reflectin film with a voltage instead of a kinase",
    intervention="Apply -0.55 to -0.8 V to a hydrated recombinant reflectin thin film.",
    predicted_phenotype="The film shrinks by 8-15 nm and its refractive index rises by "
                        "0.022-0.045, over 30 cycles. That is a real but small tuning: "
                        "the best protein-film spectral shift anyone has reported is about "
                        "11 nm, against the 250 nm range a live iridophore covers.",
    mechanism="Electrochemical reduction of histidine residues substitutes for "
              "phosphorylation in neutralising charge and driving assembly.",
    evidence_strength="direct_other_species",
    reversibility="Cyclable, 30 cycles shown.",
    lethality_risk="n/a.",
    difficulty="Demonstrated in vitro. The films (45-91 nm) are far thinner than a Bragg "
               "stack, so this is a materials result, not yet a reflector.",
    evidence=ev(("39961049", FT), ("33259748", AB), ("34272457", FT)),
)
route(
    id="syn-adaptive-infrared", scale="synthetic",
    title="Give up on visible colour and modulate the infrared instead",
    intervention="A mechanically actuated squid-skin-inspired composite, strained 0-50%.",
    predicted_phenotype="Infrared transmittance switches on/off by a factor of about 25 "
                        "(1% to 25%), regulating about 36 W/m2 of heat flux for about "
                        "3 W/m2 of mechanical input, stable over 1000 cycles.",
    mechanism="Strain opens gaps in a reflective metal layer on an elastomer.",
    evidence_strength="direct_other_species",
    reversibility="Fully reversible, 1000 cycles.",
    lethality_risk="n/a.",
    difficulty="Built, and already in a wearable demonstrator. It is the most commercially "
               "advanced thing in this list, and it works precisely because it abandoned "
               "the hard problem (visible colour) for an easier one.",
    evidence=ev(("29599237", AB), ("31036806", FT), ("23897625", AB)),
)
route(
    id="syn-texture-not-colour", scale="synthetic",
    title="Change the texture rather than the colour",
    intervention="Elastomeric membranes with embedded inextensible textile mesh, inflated "
                 "pneumatically, after the papilla musculature of cuttlefish.",
    predicted_phenotype="Flat sheets transform into programmed 3D shapes within 10% of "
                        "their targets, imitating stones and plants.",
    mechanism="A fibre-reinforced membrane's inflated shape is set by the mesh pattern, "
              "so the target shape can be designed backwards.",
    evidence_strength="direct_other_species",
    reversibility="Fully reversible.",
    lethality_risk="n/a.",
    difficulty="Demonstrated. Included because cuttlefish papillae are a SEPARATE "
               "actuator system from chromatophores, neurally controlled and capable of "
               "holding a shape for an hour without continuous input, and the engineering "
               "mimic got there first.",
    evidence=ev(("29026040", AB), ("30058000", AB)),
)
route(
    id="syn-photomechanical-fluorescent-display", scale="synthetic",
    title="Pattern a fluorescent skin with light rather than electricity",
    intervention="Photomechanically modulated display layers that pattern fluorescence "
                 "on demand.",
    predicted_phenotype="Arbitrary fluorescent patterns written optically into a soft "
                        "sheet, with no per-pixel wiring at all.",
    mechanism="A photomechanical layer changes the geometry that gates the fluorophore's "
              "emission.",
    evidence_strength="direct_other_species",
    reversibility="Reported as on-demand patterning; cycling limits not read.",
    lethality_risk="n/a.",
    difficulty="Demonstrated. Relevant to the control-channel question from the other "
               "side: optical addressing removes the wiring problem entirely, which is the "
               "problem every biological route spends its effort on.",
    evidence=ev(("34695246", AB), ("25225837", AB), ("33390008", AB)),
)
route(
    id="syn-electrophoretic-benchmark", scale="synthetic",
    title="Benchmark against a commercial electrophoretic panel",
    intervention="None - this is the yardstick.",
    predicted_phenotype="A commercial reflective panel at 300 pixels per inch, i.e. about "
                        "85 um pitch, which is comparable to a cuttlefish chromatophore's "
                        "15-100 um diameter. Update time, contrast and power are not on "
                        "the public product page, so we do not state them.",
    mechanism="Electrophoretic migration of charged pigment particles in a microcapsule.",
    evidence_strength="direct_other_species",
    reversibility="Fully reversible, bistable.",
    lethality_risk="n/a.",
    difficulty="On sale. The design-space consequence is blunt: on spatial resolution the "
               "engineered article already matches the animal, so a biological programmable "
               "skin has to justify itself on something else - self-repair, self-assembly, "
               "growth, or power.",
    evidence=[{"cite": "E Ink ED060KHE 6-inch Carta 1300 product page",
               "url": "https://www.eink.com/product/detail/ED060KHE",
               "read_level": "full-text",
               "note": "Only the resolution and pixel density were on the page; the pitch "
                       "is our arithmetic from 300 ppi, and is labelled as such."}],
)


# ======================= assembly ==========================================
RECOMMENDATION = {
    "single_best_route": "gen-transgene-in-a-chromatophore",
    "Why this one": (
        "Not because it is the most interesting result, but because it is the only "
        "route that unblocks the others. Exactly two genetic manipulations have been "
        "demonstrated in any cephalopod chromatophore system, and both DELETE a "
        "pigment gene: tdo knockout in Doryteuthis pealeii (2020) and tdo+ido double "
        "knockout giving a heritable albino Euprymna berryi line (2023). You cannot "
        "build an addressable skin by deleting things. Every cephalopod route in this "
        "space that ADDS a controllable element - an optogenetic drive on a radial "
        "muscle, a designer receptor, an engineered reflectin, a reporter that labels "
        "one motor unit - requires expressing a transgene in a chromatophore, and we "
        "found no published instance of a transgene being expressed in a cephalopod at "
        "all. Counted rather than guessed, and the count is computed in "
        "`validation.cephalopod_routes_nobody_can_take` rather than asserted here: of "
        "the 30 cephalopod-scale routes on this page, twelve are ones nobody can "
        "currently take. One of those twelve is this step itself and one is our own "
        "controller-sizing study, which needs no animal. The other TEN are downstream "
        "of expressing a transgene - as is every future route of that kind. "
        "The reagents now exist to try: a germline-competent species with a closed life "
        "cycle, published single-cell atlases to mine for a chromatophore-specific "
        "promoter, and a working delivery route. Until this lands, the cephalopod half "
        "of this page is a reading list."),
    "What we would fund second": (
        "circ-size-the-controller and the measurement that feeds it. The control layer "
        "is the part of this system that is genuinely novel as engineering - a "
        "chromatophore is about four independent actuators, not one, and real pattern "
        "transitions live on a 9-dimensional manifold out of 17,305 - and it is "
        "measurable today with video and no genetics at all."),
    "The route we would NOT fund": (
        "Anything whose goal is a wider tunable range in the reflector. Our own optical "
        "model says the measured 425-675 nm range already spans the useful band and "
        "widening it buys 1% of gamut, while refractive-index contrast buys 68%."),
    "If the goal is a product rather than a result": (
        "Buy the non-living route. A 16x16 autonomously colour-matching optoelectronic "
        "sheet was built in 2014 and switches in 1-2 s; commercial electrophoretic "
        "panels run at 300 ppi, a pitch comparable to a real chromatophore's. On "
        "'skin that changes appearance on command', the engineered article already "
        "wins. The biology's contribution right now is the design brief - what to aim "
        "for, and which axes are hard - not the substrate."),
    "What would change our mind": (
        "A single published transgene expressed in a cephalopod chromatophore. That one "
        "result moves the ten routes counted above from unreachable to attemptable, "
        "opens the class of routes that cannot be written down yet because nobody can "
        "try them, and nothing else on the horizon does."),
}

WELFARE = {
    "status": (
        "Cephalopods are the invertebrates most often brought inside research-animal "
        "regulation, and the literature treats them that way: papers on this list "
        "include dedicated anaesthesia studies framed explicitly as welfare "
        "contributions. We did not read any legal instrument and make no claim about "
        "what any particular jurisdiction requires."),
    "anaesthesia": (
        "Magnesium chloride and ethanol have been assessed in Euprymna berryi embryos; "
        "isoflurane has been assessed dose-dependently in Octopus vulgaris and "
        "described by its authors as a contribution to cephalopod welfare. Both are "
        "pilot or dose-finding studies, not settled protocols."),
    "what the routes here actually cost": (
        "Most circuit-scale routes on this page are terminal or near-terminal: motor-unit "
        "mapping is done on freshly dissected skin, single-motoneuron stimulation needs "
        "an opened animal, and optic-lobe microstimulation is invasive brain work. The "
        "developmental and behavioural routes are not - Reiter et al. tracked 17,305 "
        "chromatophores in freely behaving animals with nothing more invasive than a "
        "camera, which is worth noting because it produced the single most useful "
        "control-layer number on this page."),
    "the sedation question": (
        "Renard et al. checked whether sedation changed their result and it did not "
        "(3.715 +/- 1.211 independent components per chromatophore sedated versus "
        "3.683 +/- 1.224 head-fixed and unsedated, p = 0.83). That control is worth "
        "copying: it is the difference between a welfare measure and a confound."),
    "vertebrate alternative": (
        "If the goal is a demonstration rather than cephalopod biology specifically, "
        "zebrafish and tilapia routes reach a comparable result in an animal with "
        "established husbandry, established welfare frameworks and reversible, "
        "non-invasive actuation (light on, light off)."),
    "non-living alternative": (
        "Several routes here involve no animal at all and reach the headline capability "
        "faster. That is an uncomfortable thing for a biology page to say and we think "
        "it should be said first, not last."),
}

LIMITATIONS = [
    "A count of routes with direct cephalopod evidence flatters this page, and the "
    "`validation` block is built to stop it doing that. Every route carries a "
    "`route_kind` as well as an evidence strength, and the cross-tab is computed. The "
    "number that matters is `addressable_runtime_control`: how many routes give a "
    "dial you could actually use in a working skin - addressed to a place, changeable "
    "second by second. Read that field before anything else on this page. In a "
    "cephalopod the only entries are electrode stimulations of a dissected or opened "
    "preparation, which is not a programmable skin; it is a way of finding out how one "
    "would work.",
    "Cephalopod causal genetics rests on two papers. Crawford et al. 2020 and Ahuja et "
    "al. 2023 are the entire demonstrated repertoire, both knockouts of the same "
    "pigment pathway. Treating this as a 'literature' would be wrong.",
    "We read the full text of six sources and the abstract of most of the rest. An "
    "abstract-level read is recorded as such on every evidence item. Several numbers "
    "quoted here - the tilapia transparency timings, the Gorodetsky IR figures, the "
    "DEA area changes - come from abstracts, and an abstract's numbers are the ones "
    "the authors chose to headline.",
    "The two engineering sources with no PubMed record in the earlier survey (the "
    "Rogers optoelectronic sheet, the Whitesides microfluidic skin) do in fact have "
    "PMIDs, 25136094 and 22904008, which we found and verified. Much of the remaining "
    "cephalopod optics and soft-robotics literature genuinely sits in physics and "
    "materials journals; where a source has no PMID the field is simply absent and a "
    "DOI or URL carries the citation instead. See NOTES.md.",
    "Three routes on this page are ours rather than anyone's: the sacculus-softening "
    "route, the add-radial-muscles route and the controller-sizing route come out of "
    "our own models, and the first two depend on a sacculus stiffness that has never "
    "been measured and which our model FITS. They are labelled model_only for that "
    "reason and should not be read as predictions with evidence behind them.",
    "We did not survey the octopus papilla literature, the deep-sea bioluminescent "
    "signalling literature, or the behavioural camouflage literature in any depth, "
    "although sources from each are in the library. The page is about the actuator, "
    "the optics and the control layer.",
    "No route here has been costed, and several 'difficulty' fields are judgements "
    "rather than measurements. Where a difficulty claim rests on an absence ('nobody "
    "has done this'), the scope of the search that found nothing is stated in NOTES.md "
    "rather than in the route.",
]


def validate(doc):
    """Run every outcome-class regex, check every pmid, compute every tally."""
    routes = doc["routes"]
    report = {"n_routes": len(routes), "n_scales": len(doc["scales"])}

    seen_scales = {r["scale"] for r in routes}
    declared = {s["key"] for s in doc["scales"]}
    report["scales_with_no_routes"] = sorted(declared - seen_scales)
    report["routes_in_undeclared_scale"] = sorted(seen_scales - declared)
    report["routes_per_scale"] = {k: sum(1 for r in routes if r["scale"] == k)
                                  for k in sorted(declared)}

    tally = {}
    for r in routes:
        tally[r["evidence_strength"]] = tally.get(r["evidence_strength"], 0) + 1
    report["evidence_tally"] = dict(sorted(tally.items(), key=lambda kv: -kv[1]))
    bad = [r["id"] for r in routes if r["evidence_strength"] not in doc["evidence_labels"]]
    report["routes_with_undeclared_evidence_label"] = bad

    # Every pattern must compile in a BROWSER, not only in Python. Checked here
    # rather than trusted, because the renderer swallows compile errors in a
    # try/catch and returns an empty tag - so a broken pattern produces a silently
    # wrong answer, never an error. Shipped with a must-flag case below.
    JS_HOSTILE = [(r"\(\?[imsxaLu]\)", "inline flag such as (?i) - JS throws SyntaxError"),
                  (r"\(\?P<", "Python named group (?P<name>...)"),
                  (r"\(\?P=", "Python named backreference (?P=name)"),
                  (r"\\A|\\Z", r"\A / \Z anchors - JS has ^ and $"),
                  (r"\(\?#", "Python comment group (?#...)"),
                  (r"[*+?}]\+", "possessive quantifier")]

    def js_problems(pattern):
        return [why for rx, why in JS_HOSTILE if re.search(rx, pattern)]

    report["js_incompatible_outcome_patterns"] = [
        {"key": oc["key"], "problems": js_problems(oc["match"])}
        for oc in doc["outcome_classes"] if js_problems(oc["match"])]
    must_flag = "(?i)(albino|unpigmented)"
    report["js_compat_check_positive_control"] = {
        "pattern": must_flag,
        "flagged": bool(js_problems(must_flag)),
        "note": "A checker that never flags anything is not a checker. This is the "
                "exact prefix that took the page down; the check must catch it."}
    if not js_problems(must_flag):
        raise AssertionError("js-compat positive control did not fire")
    if report["js_incompatible_outcome_patterns"]:
        raise AssertionError(
            "outcome_classes contain patterns a browser cannot compile: "
            f"{report['js_incompatible_outcome_patterns']}")

    hits = {}
    for oc in doc["outcome_classes"]:
        rx = re.compile(oc["match"], re.IGNORECASE)
        m = [r["id"] for r in routes if rx.search(r["predicted_phenotype"])]
        hits[oc["key"]] = len(m)
    report["outcome_class_hits"] = hits
    report["outcome_classes_matching_nothing"] = [k for k, v in hits.items() if v == 0]
    uncovered = [r["id"] for r in routes
                 if not any(re.search(oc["match"], r["predicted_phenotype"],
                                      re.IGNORECASE)
                            for oc in doc["outcome_classes"])]
    report["routes_matched_by_no_outcome_class"] = uncovered

    pmids, missing, no_pmid = set(), [], []
    for r in routes:
        for e in r["evidence"]:
            p = e.get("pmid")
            if p is None:
                no_pmid.append({"route": r["id"], "cite": e["cite"][:70]})
            elif p not in LIB:
                missing.append(p)
            else:
                pmids.add(p)
    report["distinct_pmids_cited"] = len(pmids)
    report["pmids_not_in_verified_library"] = sorted(set(missing))
    report["evidence_items_without_a_pmid"] = no_pmid
    rl = {}
    for r in routes:
        for e in r["evidence"]:
            rl[e["read_level"]] = rl.get(e["read_level"], 0) + 1
    report["read_levels"] = dict(sorted(rl.items(), key=lambda kv: -kv[1]))

    required = ["id", "scale", "title", "intervention", "predicted_phenotype", "mechanism",
                "evidence_strength", "reversibility", "lethality_risk", "difficulty",
                "evidence", "species_of_evidence"]
    report["routes_without_species_of_evidence"] = [
        r["id"] for r in routes if not r.get("species_of_evidence")]
    report["distinct_species_cited"] = sorted({sp for r in routes
                                               for sp in r.get("species_of_evidence", [])
                                               if "not an animal" not in sp
                                               and "none" not in sp and "model;" not in sp})
    report["restored_after_being_cut"] = sorted(NEARLY_CUT)
    ceph_scales = {"molecular", "organelle", "cell", "circuit", "development",
                   "genetic_access"}
    ceph = [r for r in routes if r["scale"] in ceph_scales]
    blocked = [r for r in ceph if r["route_kind"] == "model"
               or r["evidence_strength"] == "proposed"]
    report["cephalopod_routes_nobody_can_take"] = {
        "cephalopod_scale_routes": len(ceph),
        "not_currently_takeable": sorted(r["id"] for r in blocked),
        "count": len(blocked),
        "note": "Of these, gen-transgene-in-a-chromatophore IS the blocking step and "
                "circ-size-the-controller is our own modelling study, which needs no "
                "animal. The rest are downstream of expressing a transgene.",
        "downstream_of_the_transgene_step": sorted(
            r["id"] for r in blocked if r["id"] not in
            ("gen-transgene-in-a-chromatophore", "circ-size-the-controller")),
    }
    report["routes_missing_a_required_field"] = [
        {"id": r.get("id"), "missing": [k for k in required if k not in r]}
        for r in routes if any(k not in r for k in required)]
    ids = [r["id"] for r in routes]
    report["duplicate_route_ids"] = sorted({i for i in ids if ids.count(i) > 1})
    studies = {r["study"] for r in routes if "study" in r}
    report["studies_referenced"] = sorted(studies)

    kinds = {}
    for r in routes:
        kinds[r["route_kind"]] = kinds.get(r["route_kind"], 0) + 1
    report["route_kind_tally"] = dict(sorted(kinds.items(), key=lambda kv: -kv[1]))
    xt = {}
    for r in routes:
        xt.setdefault(r["evidence_strength"], {})
        k = r["route_kind"]
        xt[r["evidence_strength"]][k] = xt[r["evidence_strength"]].get(k, 0) + 1
    report["evidence_strength_by_route_kind"] = xt

    ceph = [r for r in routes if r["evidence_strength"] == "direct_cephalopod_phenotype"]
    report["cephalopod_direct_routes"] = {
        "total": len(ceph),
        "by_kind": {k: sum(1 for r in ceph if r["route_kind"] == k)
                    for k in sorted({r["route_kind"] for r in ceph})},
    }
    addr = [r for r in routes if r["addressable_runtime_control"]]
    report["addressable_runtime_control"] = {
        "total": len(addr),
        "cephalopod": sorted(r["id"] for r in addr if r["scale"] in
                             ("molecular", "organelle", "cell", "circuit",
                              "development", "genetic_access")),
        "vertebrate": sorted(r["id"] for r in addr if r["scale"] == "vertebrate"),
        "synthetic": sorted(r["id"] for r in addr if r["scale"] == "synthetic"),
        "read_this_first": (
            "Ten routes on this page offer spatially addressable runtime control. Five "
            "are non-living devices. Two are vertebrate, and one of those "
            "(vert-melanopsin-light-actuator) is a combination of two results from two "
            "different animals that nobody has yet put together, while the other "
            "(vert-optogenetic-scramble) controls where a pigment cell GOES, not what "
            "colour it is. The three cephalopod entries are all electrode stimulation "
            "of dissected or opened preparations. So: in a cephalopod, the state of the "
            "art in addressing a chromatophore is a wire on a nerve in a dish. That is "
            "the honest answer to 'could you build skin that changes appearance on "
            "command', and it is why the recommended route is a reagent and not an "
            "experiment."),
    }
    return report



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
    doc = {
        "schema": "design-space-routes-0.1",
        "title": "Programmable skin: a cellular actuator you can address",
        "question": (
            "Could you build skin that changes appearance on command, and what is the "
            "actual engineering object? A cephalopod chromatophore is a real actuator "
            "with a real datasheet - a pigment sac opened by radial muscle under direct "
            "motor-neuron control, expanding in about a tenth of a second - sitting on "
            "an optical stack that works by a different mechanism and runs a hundred "
            "times slower. This page lays out the routes into that system at eight "
            "scales, and is deliberately blunt about how few of them anyone can "
            "currently take."),
        "scales": SCALES,
        "evidence_labels": EVIDENCE_LABELS,
        "outcome_filter_label": "What changes",
        "outcome_classes": OUTCOME_CLASSES,
        "routes": R,
        "recommendation": RECOMMENDATION,
        "welfare": WELFARE,
        "limitations": LIMITATIONS,
    }
    doc["validation"] = validate(doc)
    out = os.path.join(ROOT, "routes.json")
    _write_browser_safe(out, doc)
    print(json.dumps(doc["validation"], indent=1))
    print("wrote", out)


if __name__ == "__main__":
    main()
