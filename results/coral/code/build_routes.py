#!/usr/bin/env python3
"""
build_routes.py — assemble and VALIDATE routes.json.

The validation is the point. It refuses to write the file if:
  * any cited PMID is not in the verified set (so a hallucinated identifier cannot ship)
  * any route is missing a required field, or carries an unknown evidence_strength
  * any evidence item lacks a read_level, or uses one outside the declared vocabulary
  * fewer than 30 or more than 45 routes, or fewer than 7 scales
  * any route declares a scale that is not in the scale list
  * any route id is duplicated
  * a route tagged direct_coral_phenotype has no evidence read above 'listing'

The last one is the one that matters: it is the check that stops an evidence level being
asserted on the strength of a title.
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from routes_data import (EVIDENCE_LABELS, OUTCOME_CLASSES, OUTCOME_ORDERING_NOTE,  # noqa
                         RE_VERIFIED, SCALES, VERIFIED)
from routes_table import ROUTES  # noqa: E402
from routes_taxa import TAXA, TRANSFER_LABELS, TRANSFER_ORDER  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "routes.json")

READ_LEVELS = {"full-text", "abstract", "listing", "search-summary", "could-not-access",
               "web-page"}
REQUIRED = ["id", "scale", "title", "intervention", "predicted_phenotype", "mechanism",
            "evidence_strength", "reversibility", "lethality_risk", "difficulty",
            "evidence"]


def validate(routes):  # noqa: C901
    errs = []
    scale_keys = {s["key"] for s in SCALES}
    seen = set()
    for r in routes:
        rid = r.get("id", "<no id>")
        for f in REQUIRED:
            if not r.get(f):
                errs.append(f"{rid}: missing required field {f}")
        if rid in seen:
            errs.append(f"{rid}: duplicate id")
        seen.add(rid)
        if r.get("scale") not in scale_keys:
            errs.append(f"{rid}: unknown scale {r.get('scale')!r}")
        if r.get("evidence_strength") not in EVIDENCE_LABELS:
            errs.append(f"{rid}: unknown evidence_strength {r.get('evidence_strength')!r}")
        best = None
        order = ["could-not-access", "search-summary", "listing", "web-page", "abstract",
                 "full-text"]
        for e in r.get("evidence", []):
            rl = e.get("read_level")
            if rl not in READ_LEVELS:
                errs.append(f"{rid}: bad read_level {rl!r}")
                continue
            if best is None or order.index(rl) > order.index(best):
                best = rl
            pm = e.get("pmid")
            if pm is not None and pm not in VERIFIED:
                errs.append(f"{rid}: UNVERIFIED pmid {pm}")
        if r.get("evidence_strength") in ("direct_coral_phenotype", "direct_other_species"):
            if best not in ("abstract", "full-text"):
                errs.append(f"{rid}: claims {r['evidence_strength']} but best read_level "
                            f"is {best}. Either the tier is overstated or the route "
                            f"should use direct_coral_phenotype_relayed.")
        if r.get("evidence_strength") == "direct_coral_phenotype_relayed":
            if best not in ("search-summary", "web-page", "listing"):
                errs.append(f"{rid}: tagged relayed but its best read_level is {best}; "
                            f"a source read at {best} should carry the full tier")
    ids = {r.get("id") for r in routes}
    for field in ("single_best_route", "best_engineering_route"):
        ref = RECOMMENDATION.get(field)
        if ref and ref not in ids:
            errs.append(f"recommendation.{field} = {ref!r} is not a route id")
    if not (30 <= len(routes) <= 45):
        errs.append(f"route count {len(routes)} outside 30-45")
    scales_used = {r["scale"] for r in routes}
    if len(scales_used) < 7:
        errs.append(f"only {len(scales_used)} scales used, need >= 7")
    return errs


def audit_outcomes(routes):
    """The outcome is DECLARED per route. This only audits it against the patterns.

    See OUTCOME_ORDERING_NOTE: pattern-assignment was tried first and was wrong about ten
    times out of forty-five, always plausibly. The disagreements below are kept because
    they say something about how a route is written, not because the tag is in doubt.
    """
    keys = {oc["key"] for oc in OUTCOME_CLASSES}
    disagreements = []
    for r in routes:
        if r.get("outcome") not in keys:
            raise SystemExit(f"{r['id']}: outcome {r.get('outcome')!r} not a declared class")
        hay = " ".join([r["title"], r["predicted_phenotype"], r["mechanism"]])
        guess = next((oc["key"] for oc in OUTCOME_CLASSES
                      if re.search(oc["match"], hay, re.I)), None)
        if guess != r["outcome"]:
            disagreements.append(dict(route=r["id"], declared=r["outcome"],
                                      first_pattern_match=guess))
    return routes, disagreements


RECOMMENDATION = {
    "single_best_route": "eco-site-prioritisation",
    "best_engineering_route": "sym-shuffle-by-induced-bleaching",
    "why_two_fields": (
        "Because the honest answer to 'what should we do' and the honest answer to "
        "'what should we BUILD' are different routes, and collapsing them into one "
        "field would misrepresent both. The first is siting, which is cheap, reversible "
        "and boring. The second is symbiont shuffling. The two sections below say so in "
        "that order."),
    "If you only get to do one thing": (
        "Pick the reef, not the coral. Mula et al. 2025 found that restoration sites "
        "cluster near human settlements, that outcomes are not predicted by "
        "environmental covariates, and that most restored localities face high or severe "
        "bleaching risk by mid-century with more than half already affected. Nothing "
        "else on this page changes the answer by as much, costs as little, or is as "
        "reversible. It is also the least interesting thing to publish, which is "
        "probably why the siting data look the way they do."),
    "If you have to engineer something": (
        "Symbiont shuffling by controlled sub-lethal bleaching, in colonies already "
        "carrying a background heat-tolerant type. It is the only route on this page "
        "with a causal field-scale coral phenotype attached to a number of degrees "
        "(about +1 to 1.5 degC, Berkelmans & van Oppen 2006), it needs no genetic "
        "modification and therefore probably no GMO regulator, it requires nothing to be "
        "cultured or released, and it is partly reversible. It is chosen over "
        "Durusdinium INOCULATION, which gets the same tolerance, because inoculation "
        "with a non-native lineage is irreversible in open water and the Caribbean shows "
        "what that looks like: a clonal invader associated with calcification reduced by "
        "nearly half.\n\n"
        "The reasons not to do it are stated plainly. You are deliberately bleaching a "
        "living colony; growth falls by more than half for up to 18 months afterwards. "
        "You need a pre-existing reservoir of the tolerant type or there is nothing to "
        "shuffle to. Durability is verified for THREE MONTHS and no longer. And the "
        "direction is conditional: after SEVERE bleaching in a warm recovery environment "
        "the tolerant proportion rises sharply, but after MILD bleaching it tends to "
        "DECREASE — so an intervention that is too gentle does the opposite of what you "
        "wanted."),
    "The single most useful experiment nobody has run": (
        "Cross a symbiont intervention with a host trait in one factorial design and "
        "measure both the thermal threshold AND the growth rate at ambient. Every "
        "thermal route on this page has been tested alone. No study read here crosses "
        "them, so whether two interventions add, interact or cancel is unknown in corals "
        "— our own simulation says additive, and that is a statement about a "
        "four-parameter box in one model, not about a coral.\n\n"
        "The second most useful: a multi-year time course of a shuffled symbiont "
        "community. The three-month persistence result is the longest verified horizon "
        "for shuffling anywhere in the sources read, and a route whose durability is "
        "unknown past one season is being discussed as though it were a decade."),
    "What we would NOT do": (
        "Engineer the animal, for now. CRISPR works in Acropora millepora — that is real "
        "and recent. Counted from the sources read here, SIX genes have been targeted in "
        "a reef-building coral: FGF1a, GFP and RFP (Cleves et al. 2018, chosen to show "
        "the method works), HSF1 (Cleves et al. 2020), SLC4-gamma (Tinoco et al. 2023) "
        "and SLC26A11 (Maruyama et al. 2026, reported in Aiptasia and in a reef-building "
        "coral). Only the last three carry an informative trait phenotype, and every one "
        "of the six is in the INJECTED GENERATION. There is no stable germline coral "
        "line anywhere in this "
        "literature, Acropora takes years to reach reproductive size, spawning is "
        "seasonal, and editing adult colonies has not been shown. The two coral gene "
        "edits with heat or skeleton phenotypes are both LOSS of function: knocking out "
        "HSF1 makes a coral worse, and knocking out SLC4-gamma breaks its skeleton. "
        "Neither tells you how to make one better. The animal-engineering route is where "
        "the science is most exciting and the design leverage is currently lowest.\n\n"
        "We would also not deploy a transgenic symbiont. Not on principle — because no "
        "one has made one. Standard transformation methods failed on the one strain "
        "where the attempt was published, and the PubMed index returns zero for "
        "Symbiodiniaceae CRISPR. And unlike an edited coral, an engineered alga is a "
        "self-replicating microorganism in open water: the one route here whose "
        "irreversibility is categorical rather than practical."),
    "The thing the question gets wrong": (
        "'Could you engineer a coral' treats thermal tolerance as the specification. The "
        "literature says the binding constraint is somewhere else. Adult corals are not "
        "generally what fails first in restoration — recruitment is. First-year survival "
        "of settlers spreads over more than tenfold across sites, devices and thermal "
        "years (9.6% on tetrapods in Curacao; 2 to 39% across device types in one "
        "Acropora tenuis trial; 33% against 2% between a normal and a heatwave year in "
        "Moorea; effectively zero yield at 21 months at one Lizard Island site). In the "
        "best-documented larval seeding experiment, 47 colonies survived from roughly "
        "900,000 larvae. A heat-tolerant coral that cannot recruit is a heat-tolerant "
        "coral you have to keep planting by hand."),
    "The arithmetic nobody puts on the slide": (
        "The median coral restoration project covers 100 square metres (Bostrom-Einarsson "
        "et al. 2020, from a review of the field). The Great Barrier Reef Marine Park is "
        "about 344,400 square kilometres. Covering even one square kilometre at the "
        "median project size takes ten thousand projects. Reef habitat area is far "
        "smaller than Marine Park area, so that ratio overstates the gap — but not by "
        "the four orders of magnitude it would need to close. Reported restoration costs "
        "run about USD 80,000 per hectare at the median in 2010 dollars, with the true "
        "median likely two to four times higher and coral reefs among the most expensive "
        "habitats to restore. Every route on this page should be read against that "
        "denominator."),
    "What would change our mind": (
        "A verified multi-year field time course showing a shuffled or inoculated "
        "symbiont community holding, with growth measured and not just survival, would "
        "move the symbiont route from 'buys a season' to 'buys a decade'. A stable "
        "germline coral line would move the gene scale from a calibration tool to a "
        "design surface. And a single cross-factorial experiment showing that two "
        "interventions combine super-additively would change the recommendation from "
        "'pick one' to 'stack them'."),
}

JUDGE_GENE_CANDIDATES = [
    dict(gene="HSF1 (heat-shock transcription factor 1)",
         key_pmid="33168726",
         species_of_evidence="Acropora millepora, injected-generation larvae",
         what_it_would_actually_produce=(
             "Larvae that die rapidly at 34 degC and are fine at 27 degC. This is the "
             "gene that has a published coral heat phenotype, and the phenotype is "
             "WORSE, not better. Removing it removes the heat-shock response; nothing "
             "shows that adding more of it adds tolerance."),
         distinguishing_question=(
             "Are you describing a loss-of-function result? If the answer is 'they "
             "knocked it out and the coral died in the heat', this is the paper and it "
             "is not a route to a better coral.")),
    dict(gene="SLC4-gamma (bicarbonate transporter)",
         key_pmid="37276409",
         species_of_evidence="Acropora millepora, juvenile polyps",
         what_it_would_actually_produce=(
             "A coral with a defective skeleton, with severity tracking the mutation "
             "frequency. It is a skeleton gene, not a heat gene, and it arose by "
             "duplication at the origin of stony corals."),
         distinguishing_question=(
             "Is the phenotype about the SKELETON or about BLEACHING? If skeleton, it is "
             "almost certainly this one, and almost certainly in the losing direction.")),
    dict(gene="SLC26A11 (symbiosomal bicarbonate/sulfate transporter)",
         key_pmid="42385704",
         species_of_evidence="Exaiptasia and, per the same abstract, a reef-building coral",
         what_it_would_actually_produce=(
             "Reduced symbiosis — the coral loses the alga. The paper's frame is the "
             "evolutionary co-option of lysosomal machinery for photosymbiosis."),
         distinguishing_question=(
             "Does the claimed gene affect the SYMBIOSIS itself rather than the host's "
             "stress response? Then it is this one, and the phenotype is the thing every "
             "other route is trying to prevent.")),
    dict(gene="An unnamed heat-shock co-chaperone under long-term balancing selection",
         key_pmid="32675347",
         species_of_evidence="Acropora millepora, 237 whole genomes across 12 GBR reefs",
         what_it_would_actually_produce=(
             "Nothing, on its own. This is a population-genomic signature, not a "
             "perturbation. NOTE: the gene's NAME was stripped from the PubMed text we "
             "read, so we cannot tell you what it is called, and neither could anyone "
             "working from the abstract alone. Heat tolerance in this species is "
             "polygenic with weak per-locus effects."),
         distinguishing_question=(
             "Did they EDIT it, or did they find it in a genome scan? If the evidence is "
             "'this locus is under selection' or 'this locus came up in a GWAS', there "
             "is no demonstrated phenotype behind it.")),
    dict(gene="FGF1a",
         key_pmid="29695630",
         species_of_evidence="Acropora millepora, injected-generation larvae",
         what_it_would_actually_produce=(
             "It was a METHOD-DEVELOPMENT target, chosen alongside GFP and RFP to show "
             "that Cas9 ribonucleoprotein injection works in coral eggs at about 50% "
             "mutation frequency. No heat or skeleton phenotype is claimed for it."),
         distinguishing_question=(
             "Is the paper from 2018 and about whether CRISPR works in coral at all? "
             "Then the gene is incidental.")),
    dict(gene="Eighteen candidate skeletal-formation genes in Pocillopora acuta",
         key_pmid="28855618",
         species_of_evidence="two sympatric morphs of P. acuta",
         what_it_would_actually_produce=(
             "Unknown. These are candidates from population genomics that distinguish two "
             "morphs differing in skeletal morphology AND bleaching threshold. None has "
             "been functionally tested, and the authors' own reading is that the morphs "
             "may be early cryptic species — so the 'gene for it' may really be 'a "
             "different species'."),
         distinguishing_question=(
             "Does the claim involve colony SHAPE? No gene has ever been shown to change "
             "coral branching versus plating by perturbation, in any species.")),
    dict(gene="Wnt, Notch and BMP pathway members enriched at branch tips",
         key_pmid="25519925",
         species_of_evidence="Acropora cervicornis and A. palmata, tip versus base RNA-seq",
         what_it_would_actually_produce=(
             "Unknown. Differential expression between the tip and the base of a branch, "
             "with the authors suggesting 'a relatively small number of genes' may "
             "separate staghorn from elkhorn form. Correlative, no perturbation, and the "
             "two species differ in everything else as well."),
         distinguishing_question=(
             "Is the evidence an expression difference between two parts of the same "
             "colony? That is a correlate of growth, not a control knob for it.")),
]

WELFARE = {
    "Is a coral a welfare subject?": (
        "Scleractinian corals are cnidarians: a nerve net, no brain, no centralised "
        "nervous system. The usual sentience arguments for vertebrates and cephalopods "
        "do not transfer, and no regulator we could identify treats coral research as "
        "animal research. We are not going to claim a settled answer from a literature "
        "search that did not address the question."),
    "What the real objection is": (
        "It is ecological, not individual. Almost every route here acts on a POPULATION "
        "or an ECOSYSTEM, and several release a self-replicating organism into open "
        "water. A transgenic symbiont, a therapeutic phage and an amoxicillin paste are "
        "not recallable in the way a laboratory animal is, and the harm, if there is "
        "one, lands on an ecosystem that nobody owns."),
    "The one documented harm in this table": (
        "Durusdinium trenchii established in Caribbean hosts, where it is not native, "
        "with low clonal diversity and calcification in affected hosts 'reduced by "
        "nearly half' relative to hosts carrying native symbionts (Pettay et al. 2015). "
        "The authors read the new symbioses as maladapted. That is an inference rather "
        "than a fitness measurement, and it is the clearest instance on this page of a "
        "heat-tolerance gain arriving with an ecosystem-scale cost."),
    "Deliberate harm as a method": (
        "Two routes here work by injuring the coral on purpose. Symbiont shuffling "
        "requires deliberately bleaching a living colony, after which growth falls by "
        "more than half for up to 18 months. Microfragmentation works BECAUSE of "
        "injury-driven edge growth. Both are standard practice and neither is usually "
        "described this way."),
    "Antibiotic release": (
        "Amoxicillin paste is applied directly onto wild reefs, lesion by lesion, for a "
        "disease whose pathogen is unknown. One metagenomic study of 41 colonies found "
        "no effect on beta-lactamase diversity after repeated treatment. That is a "
        "narrow negative — one species, 41 colonies, one gene family — and not a survey "
        "of resistance on the surrounding reef, which nobody read here has done."),
    "The honest asymmetry": (
        "The counterfactual is not an undisturbed reef. It is a reef that in many places "
        "is already losing most of its coral, and a median restoration project that "
        "covers 100 square metres. Precaution about intervention has to be weighed "
        "against a baseline that is itself moving fast, and the people arguing both "
        "sides of that agree on the numbers and disagree about what follows."),
}

LIMITATIONS = [
    "NONE OF THESE ROUTES HAS BEEN ATTEMPTED HERE. This is a reading of a literature, "
    "with two simulations beside it. No coral was touched.",
    "Every PMID cited has been title-matched in PubMed, but READ LEVELS VARY and are "
    "given per source. Most are abstract-level. Three papers were read at full text "
    "(Buerger 2020, Chindapol 2013, Chandler 2024, and parts of Santoro 2021, Rosado "
    "2019 and Madin 2014). An abstract-level claim is not a reading of a paper, and "
    "methods details, sample sizes and effect sizes that live in full texts are mostly "
    "absent here.",
    "Routes carrying evidence with no PMID are marked. Several real and relevant studies "
    "are not indexed in PubMed, or were not found there: Kaandorp 1999, Loya et al. "
    "2001, Doropoulos 2015/2016, Penin et al. 2011, Randall et al. 2021, Chan et al. "
    "2018, Lamb et al. 2024, Page et al. 2018, the cryopreservation papers and the "
    "Fine & Tchernov comment and reply. Their claims are carried at search-summary level "
    "and should not be treated as equal to the PMID-verified rows.",
    "The evidence_strength labels are OURS. They compress a judgement about what a study "
    "shows into one token, and two people could label the same paper differently. The "
    "evidence list under each route is the thing to read.",
    "Reversibility, lethality risk and difficulty are UNQUANTIFIED JUDGEMENTS, not "
    "measurements. No route has a measured probability of anything attached to those "
    "three fields.",
    "This table under-represents what has been tried and failed, because failures are "
    "published less. The one systematic review here notes publication bias toward "
    "success in the restoration-cost literature, and the two deliberate failure cases we "
    "did keep (tetrabromopyrrole, and the Lizard Island device trial) are in because "
    "they happened to be published, not because we searched for failures.",
    "Several of the negatives are scoped to a single PubMed query shape and say so "
    "inline. 'Not found by this search' is not 'does not exist', and preprints, "
    "non-indexed journals, datasets and theses were largely not searched.",
    "Regulatory statements are the weakest content on this page. No primary legal text "
    "was read. The Convention on Biological Diversity and Cartagena Protocol party "
    "statuses were verified by fetching the treaty pages; everything about Australian "
    "gene-technology law, Marine Park permits, the US Endangered Species Act and FDA "
    "jurisdiction is a search summary or an inference, and is labelled as such in the "
    "route.",
    "The outcome classes are regex tags over our own prose, so they describe how we "
    "wrote a route as much as what the route does. The ordering rule is declared with "
    "them because getting it backwards would silently retag most of the table.",
]


def main():
    routes, outcome_disagreements = audit_outcomes([dict(r) for r in ROUTES])
    missing = [r["id"] for r in routes if r["id"] not in TAXA]
    if missing:
        raise SystemExit("routes with no taxon annotation: " + ", ".join(missing))
    for r in routes:
        t = TAXA[r["id"]]
        if t["transfer"] not in TRANSFER_LABELS:
            raise SystemExit(f"{r['id']}: unknown transfer value {t['transfer']!r}")
        r["target_taxon"] = t["target_taxon"]
        r["species_of_evidence"] = t["species_of_evidence"]
        r["evidence_transfer"] = t["transfer"]
        r["evidence_transfer_label"] = TRANSFER_LABELS[t["transfer"]]
        r["evidence_transfer_note"] = t["note"]
    tcounts = {}
    for r in routes:
        tcounts[r["evidence_transfer"]] = tcounts.get(r["evidence_transfer"], 0) + 1
    organism_routes = [r for r in routes if r["evidence_transfer"] != "not_applicable"]
    cross = [r for r in organism_routes
             if r["evidence_transfer"] in ("cross_genus", "cross_growth_form",
                                           "non_reef_coral", "non_coral_cnidarian")]
    errs = validate(routes)
    if errs:
        print("VALIDATION FAILED — routes.json NOT written:")
        for e in errs:
            print("  " + e)
        sys.exit(1)

    # attach re-verified DOIs where we fetched them ourselves this session
    for r in routes:
        for e in r["evidence"]:
            if e.get("pmid") in RE_VERIFIED:
                e["doi"] = RE_VERIFIED[e["pmid"]]
                e["pmid_reverified_here"] = True

    counts = {}
    for r in routes:
        counts[r["evidence_strength"]] = counts.get(r["evidence_strength"], 0) + 1
    read_counts = {}
    for r in routes:
        for e in r["evidence"]:
            read_counts[e["read_level"]] = read_counts.get(e["read_level"], 0) + 1

    out = dict(
        schema="design-space-routes-0.1",
        title="Design a coral: for heat, for shape, or for the reef",
        subtitle=(
            "The question is 'could you engineer a coral' — and the first job is to "
            "refuse it, because it bundles four different animals. A THERMALLY TOLERANT "
            "colony, a colony of a CHOSEN MORPHOLOGY (which decides flow, light capture, "
            "nursery habitat and what a storm breaks), a colony that SETTLES AND "
            "SURVIVES where you put it, and a HOLOBIONT engineered through its symbiont "
            "or microbiome rather than through the animal at all. These are different "
            "scales with different evidence, different costs and different "
            "irreversibility. Nothing below has been attempted here."),
        nothing_attempted="None of these routes has been attempted here.",
        scales=SCALES,
        evidence_labels=EVIDENCE_LABELS,
        outcome_filter_label="Outcome",
        outcome_classes=OUTCOME_CLASSES,
        outcome_classes_note=OUTCOME_ORDERING_NOTE,
        routes=routes,
        recommendation=RECOMMENDATION,
        recommendation_title="If you asked us to actually do it",
        judge_gene_candidates=JUDGE_GENE_CANDIDATES,
        gene_table_title="“They said they found a gene for it” — what that could mean",
        gene_table_note=(
            "Several genes fit that description and they do not produce the same animal. "
            "Six genes have been targeted by CRISPR in a reef-building coral in the "
            "sources read here, and only three of those carry an informative trait "
            "phenotype; the rest were chosen to demonstrate that the method works at "
            "all. Every one is in the injected generation. The last column is the "
            "question that would tell them apart."),
        welfare=WELFARE,
        welfare_title="Welfare, ecological risk and what is actually at stake",
        limitations=LIMITATIONS,
        provenance=dict(
            n_routes=len(routes), n_scales=len(SCALES),
            evidence_strength_counts=counts,
            read_level_counts=read_counts,
            n_evidence_items=sum(len(r["evidence"]) for r in routes),
            n_distinct_pmids=len({e["pmid"] for r in routes for e in r["evidence"]
                                  if e.get("pmid")}),
            n_pmids_reverified_in_session=len(RE_VERIFIED),
            pmid_policy=(
                "Every PMID in this file is in a verified set drawn from the research "
                "blocks, each of which records the identifier as fetched and "
                "title-matched with PubMed's get_article_metadata. build_routes.py "
                "refuses to write the file if any cited PMID falls outside that set, so "
                "an invented identifier cannot reach it. Twelve were additionally "
                "re-fetched directly in this session and their titles re-checked; those "
                "carry pmid_reverified_here and a DOI."),
            evidence_transfer=dict(
                counts=tcounts,
                labels=TRANSFER_LABELS,
                order_weakest_first=TRANSFER_ORDER,
                n_organism_routes=len(organism_routes),
                n_resting_on_cross_genus_or_weaker=len(cross),
                fraction_cross_genus_or_weaker=round(
                    len(cross) / max(len(organism_routes), 1), 3),
                routes_resting_on_a_non_coral=[
                    r["id"] for r in routes
                    if r["evidence_transfer"] in ("non_coral_cnidarian",
                                                  "non_reef_coral")],
                rule="Where a route's evidence spans several taxa, the WEAKEST "
                     "applicable transfer is recorded, because that is the assumption "
                     "the route actually rests on.",
                why_this_exists=(
                    "The symbiont-shuffling route leans on Cunning, Silverstein & Baker "
                    "2015, which is in ORBICELLA FAVEOLATA — a massive Caribbean coral — "
                    "while the CRISPR precedent, the assisted-evolution programme and "
                    "most of the morphology work are Acropora-centred. Transfer between "
                    "them is an assumption, and before this field existed it was "
                    "invisible on the page."),
            ),
            outcome_tagging=dict(
                method="declared per route as a field",
                pattern_audit_disagreements=outcome_disagreements,
                n_disagreements=len(outcome_disagreements),
                note="Where the declared outcome and the first regex match differ, the "
                     "declared one stands. The list is published so the disagreement is "
                     "visible rather than quietly resolved."),
            validation=("validate() in build_routes.py; the binding check is that a route "
                        "claiming a direct phenotype must carry at least one source read "
                        "at abstract level or better, so an evidence tier cannot be "
                        "asserted from a title."),
        ),
    )
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(f"wrote {OUT}: {len(routes)} routes, {len(SCALES)} scales, "
          f"{out['provenance']['n_evidence_items']} evidence items, "
          f"{out['provenance']['n_distinct_pmids']} distinct PMIDs")
    print("  evidence strengths:", counts)
    print("  read levels:", read_counts)
    oc = {}
    for r in routes:
        oc[r["outcome"]] = oc.get(r["outcome"], 0) + 1
    print("  outcomes:", oc)
    print(f"  outcome pattern-audit disagreements: {len(outcome_disagreements)}/"
          f"{len(routes)}")
    print(f"  evidence transfer: {tcounts}")
    print(f"  {len(cross)}/{len(organism_routes)} organism routes rest on cross-genus "
          f"transfer or weaker")


if __name__ == "__main__":
    main()
