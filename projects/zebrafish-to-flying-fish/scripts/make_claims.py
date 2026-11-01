#!/usr/bin/env python3
"""Emit the project's proposed Claim and Problem drafts and validate them against frontier/models.py.

The records are *proposals*. Validation means the bytes parse and the field contracts hold; it says
nothing about whether any statement is true, reviewed or reproducible (SPEC-001).

Run from the repo root: python3 scripts/... -> see the Makefile-free invocation in RESULTS.md
  python3 projects/zebrafish-to-flying-fish/scripts/make_claims.py OUT.json
"""
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from frontier.models import Draft  # noqa: E402

NS = "delphi-frontier"
ISSUER = "claude-zf2ff"
GIT = "git:delphi-frontier@claude/zf2ff-20261101"

NOT_REVIEWED = {"status": "none: single operator (claude-zf2ff), not reviewed by anyone"}

EPMC_ACCESS = ("Europe PMC REST search response saved verbatim in this repo; the abstract was read "
               "and nothing deeper. Full text was NOT read, so whether the paper's data support "
               "this abstract sentence is unchecked.")
COMPUTED_ACCESS = ("Files in this repository at the branch named in the locator. The computation was "
                   "run by this project; nobody has re-run it, so it is not independent evidence.")


def epmc_source(name, pmid):
    body = pathlib.Path(__file__).resolve().parent.parent / "data" / name
    tag = f"PMID {pmid}" if pmid else "no PMID in the retrieved record; identified by title and response hash"
    return {
        "uri": f"https://europepmc.org/abstract/MED/{pmid}" if pmid else None,
        "locator": f"git:delphi-frontier@claude/zf2ff-20261101:projects/zebrafish-to-flying-fish/data/{name} ({tag})",
        "source_version": None,
        "content_sha256": hashlib.sha256(body.read_bytes()).hexdigest(),
        "content_available": True,
        "access": EPMC_ACCESS,
        "license": None,
    }


def computed_source(rel):
    body = pathlib.Path(__file__).resolve().parent.parent / rel
    return {
        "uri": None,
        "locator": f"{GIT}:projects/zebrafish-to-flying-fish/{rel}",
        "source_version": GIT,
        "content_sha256": hashlib.sha256(body.read_bytes()).hexdigest(),
        "content_available": True,
        "access": COMPUTED_ACCESS,
        "license": None,
    }


SCOPE = ("Danio rerio and public sequence only. No observation of any Exocoetid fish was made by "
         "this project. Not claimed: that a flying fish can be built, that any zebrafish value "
         "transfers to an Exocoetid, or that any edit below has been performed.")

CLAIMS = [
    dict(
        id="zf2ff-claim-one-exocoetid-assembly",
        title="Exactly one Exocoetidae genome assembly is public, and it is unannotated",
        statement=(
            "As retrieved on 2026-11-01, NCBI Datasets lists one assembly for the family Exocoetidae: "
            "Hirundichthys speculiger GCA_018398805.1, at scaffold level with no annotation. Ensembl "
            "lists no Exocoetidae species; medaka (Oryzias latipes) is the nearest Beloniformes in the "
            "Ensembl species list and can only be used as a labelled proxy. The assembly FASTA "
            "downloaded by this project has sha256 "
            "6f312a972a382295873cf1170771b0ef952f5f7772ce3b7bd19e3b49603c1052."),
        context=("A constraint on what comparative genomics is possible for a flying-fish project at all. "
                 + SCOPE),
        assumptions=["The NCBI Datasets and Ensembl listings read on 2026-11-01 are current.",
                     "Listing contents were read; assembly quality and completeness were not assessed."],
        limitations=["A listing is not an assessment of assembly quality.",
                     "Not claimed: that no other Exocoetid assembly exists privately or unlisted.",
                     "The published genome paper (PMID 34306036) was retrieved at title level only; its abstract was not in the saved response."],
        source=computed_source("data/round2/mapping_summary_round2.json"),
        origin="source_statement",
    ),
    dict(
        id="zf2ff-claim-candidate-loci-detectable",
        title="All 27 candidate fin-development proteins align somewhere in the Hirundichthys speculiger assembly, with controls passing, but two cannot be assigned to a paralog",
        statement=(
            "miniprot 0.18-r281 (-t4 -N5 --outs=0.6, applied per assembly chunk) aligned 27 distinct "
            "Danio rerio candidate proteins to GCA_018398805.1 across three runs; every one has a "
            "best-aligning region. Best-hit amino-acid identity (PAF residue matches over alignment "
            "block length) ranges 0.447 (hoxd13a) to 0.989 (the actb1 positive control). Controls "
            "behaved: actb1 aligned at coverage 1.00 and identity 0.989, and three independently "
            "shuffled negative controls (fgf10a-, kcnh2a- and eda-shuffled, seed 12345) produced no hit "
            "at all. msxb, mapped in two runs on separately re-chunked copies of the assembly, returned "
            "the identical interval JAGFBZ010000863.1:508027-509355. Paralog controls added after review "
            "show that kcnh2a and kcnh2b best-hit the same region of JAGFBZ010001591.1 from the identical "
            "start coordinate 1301510 with the b query scoring HIGHER (identity 0.762 vs 0.610), so the "
            "detected region cannot be assigned to kcnh2a; tbx5b, fgf10b and kcnk5a resolve to scaffolds "
            "different from their a paralogs."),
        context=("Protein-to-genome alignment only. An alignment is not an annotation, an orthology "
                 "assignment, a copy-number statement, or evidence that the locus is transcribed or does "
                 "anything in Hirundichthys. " + SCOPE),
        assumptions=["miniprot's PAF NM/blocklen is taken as the identity measure.",
                     "The assembly was split into five chunks of whole scaffolds to stay inside a 6 GB memory cap; because no scaffold was split, a best alignment lies wholly inside one chunk, which is why best hits are taken as chunk-independent while secondary-hit sets are not."],
        limitations=["No orthology test was run (no reciprocal best hit, no synteny, no phylogeny), so no row names a paralog.",
                     "shha and shhb/twhh best-hit the same region of JAGFBZ010001012.1 (overlap 6364 bp) and cannot be assigned to distinct loci by this method.",
                     "The kcnh2a row must NOT be read as 'the kcnh2a ortholog is detectable': the kcnh2b query aligns to the same region at higher identity. kcnh2a is this project's primary candidate locus, so this is a limitation on the plan, not only on the table.",
                     "A span audit (scripts/audit_long_spans.py) shows the kcnh2a (278 kb), kcnh2b (239 kb) and cacna1g (298 kb) best hits each contain one intron-like gap of about 0.1 Mb and carry 2-4 frameshifts, with zero assembly-gap (N) content; whether these are large-intron genes or chaining artefacts was not determined. Treat them as 'something channel-like is present', not as located genes.",
                     "cacna1g best-hit coverage is 0.640, so its alignment is partial.",
                     "Alternative-hit counts per query are artefacts of applying -N5 and --outs=0.6 per chunk and must not be read as copy number.",
                     "No non-coding or regulatory sequence was examined.",
                     "The round-1 run was produced by a predecessor process and reviewed here, not re-run."],
        source=computed_source("data/loci_merged.json"),
        origin="derived",
    ),
    dict(
        id="zf2ff-claim-longfin-is-cis-kcnh2a",
        title="Source statement: longfin(t2) is a cis-regulatory kcnh2a allele that lengthens fins by prolonging outgrowth",
        statement=(
            "The abstract of PMID 34061172 (Development, 2021) states that the zebrafish mutant "
            "longfin(t2) overexpresses the ether-a-go-go-related K+ channel kcnh2a from chromosome 2; "
            "that disrupting kcnh2a in cis rescues the mutant, making longfin(t2) a regulatory kcnh2a "
            "allele; that the overgrowth comes from prolonged outgrowth periods rather than altered "
            "positional information or cell-level growth potency; that it acts tissue-autonomously "
            "within the intra-ray mesenchymal lineage; and that Kcnh2a appears to inhibit calcineurin "
            "output to supersede growth-cessation signals."),
        context=("The load-bearing source for treating fin size as a controllable outgrowth *duration* "
                 "in a specific cell lineage, and for preferring a regulatory edit over a coding one. "
                 + SCOPE),
        assumptions=["The abstract text as returned by Europe PMC is what the authors wrote."],
        limitations=["Abstract-level read only; the paper's figures were not examined.",
                     "Danio rerio only. Not claimed: that this mechanism operates in any Exocoetid.",
                     "Not claimed: that the lesion's coordinates are known here. They are not."],
        source=epmc_source("epmc2/longfin_kcnh2a_gof.json", 34061172),
        origin="source_statement",
    ),
    dict(
        id="zf2ff-claim-kcnh2a-lat4a-phenocopy",
        title="Source statement: a kcnh2a x lat4a interaction in zebrafish phenocopies flying-fish fin proportions",
        statement=(
            "The abstract of PMID 34534441 (Current Biology, 2021) states that a phylogenomic analysis of "
            "genome-wide variation in 35 species of flying fishes and relatives identified signatures in "
            "both coding and regulatory regions underlying convergent evolution of increased paired fin "
            "size and aerial gliding behaviours; that intersecting those signatures with distantly related "
            "zebrafish fin-size mutants implicated an L-type amino acid transporter, lat4a, and the "
            "potassium channel kcnh2a in fin proportion; and that the interaction between these loci in "
            "zebrafish closely phenocopies the observed fin proportions of flying fishes."),
        context=("The strongest published bridge this project found from zebrafish genetics to "
                 "flying-fish morphology. " + SCOPE),
        assumptions=["The abstract text as returned by Europe PMC is what the authors wrote."],
        limitations=["Abstract-level read only; no figure, effect size, sample size or statistic was read.",
                     "'Closely phenocopies' is the authors' wording for fin proportion only; it says nothing about ray material properties, caudal asymmetry, launch muscle or gliding behaviour.",
                     "Which UniProt zebrafish entry the paper's 'lat4a' denotes is unresolved here (slc43a2a Q7ZUS0 is a 153 aa fragment; slc43a2b Q5PR35 is the 592 aa L-type amino acid transporter 4).",
                     "The 35-species variation data behind the analysis is not public to this project, so the convergence scan cannot be reproduced here."],
        source=epmc_source("epmc2/flyingfish_bioelectric.json", 34534441),
        origin="source_statement",
    ),
    dict(
        id="zf2ff-claim-ra-rcan2-kcnk5b-bud-scaling",
        title="Source statement: retinoic acid scales the zebrafish pectoral fin bud through rcan2, Kcnk5b, Ca2+ and shha",
        statement=(
            "The abstract of PMID 38527087 (PLoS Biology, 2024) states that intracellular K+ levels fall "
            "in a coordinated way during zebrafish pectoral fin bud growth; that overexpressing K+-leak "
            "channels coordinately increases bud proportions; that retinoic acid decreases K+ in bud "
            "tissues and up-regulates rcan2; that rcan2 overexpression increases bud growth and decreases "
            "K+ while CRISPR-Cas9 targeting of rcan2 does the reverse; that Rcan2-mediated growth depends "
            "on Kcnk5b; that Kcnk5b enhances depolarization via Na+ channels and this is required for its "
            "growth effect; and that Kcnk5b-induced shha transcription and bud growth require "
            "IP3R-mediated Ca2+ release and CaMKK activity."),
        context=("One of the few reads that places the K+/Ca2+ size-scaling mechanism in the *embryonic* "
                 "fin bud rather than in adult regeneration, which matters because a wing must be built "
                 "during development. " + SCOPE),
        assumptions=["The abstract text as returned by Europe PMC is what the authors wrote."],
        limitations=["Abstract-level read only.",
                     "Danio rerio only.",
                     "A chain of named dependencies in an abstract is not a quantitative model; no rate constant in this chain is known to this project."],
        source=epmc_source("epmc2/pecfin_bud_scale_K.json", 38527087),
        origin="source_statement",
    ),
    dict(
        id="zf2ff-claim-size-and-segment-are-separable",
        title="Source statement: cell-type-specific bioelectric manipulation separates fin size from fin-ray segment length",
        statement=(
            "The abstract of the 2024 Development paper 'Cell-type-dependent bioelectric regulation of fin "
            "size and fin-ray segment length in zebrafish' states that expressing the hyperactive "
            "potassium channel mutant kcnk5b(W169L) or the dominant-negative connexin mutant Cx43(T154A) "
            "under cell-type-specific promoters had different effects by cell type: manipulation in "
            "keratinocytes primarily affected fin size, while manipulation in osteoblasts preferentially "
            "altered fin-ray segment length; that combining them produced enlarged fins with short "
            "segments or small fins with long segments; and that optogenetic manipulation showed membrane "
            "potential itself can regulate both."),
        context=("Establishes two separately addressable design knobs — overall appendage size and "
                 "skeletal element length — which is what a wing design needs, since a long fin with "
                 "wrong ray segmentation is not a wing. " + SCOPE),
        assumptions=["The abstract text as returned by Europe PMC is what the authors wrote.",
                     "The retrieved record carried no PMID field; it is identified by title and the saved response hash."],
        limitations=["Abstract-level read only.",
                     "Danio rerio only; promoter specificity and leak were not assessed here.",
                     "Not claimed: that either manipulation produces a mechanically adequate fin."],
        source=epmc_source("epmc/bioelectric_fin_size.json", 0),
        origin="source_statement",
    ),
    dict(
        id="zf2ff-claim-timing-edit-hypothesis",
        title="Hypothesis: the flying-fish pectoral wing is reachable by extending outgrowth duration in ray mesenchyme alone",
        statement=(
            "HYPOTHESIS, with no evidence of any kind offered for it here. If the Exocoetid pectoral fin "
            "is enlarged by the same mechanism that enlarges the longfin(t2) zebrafish fin, then the "
            "minimal edit that increases fin length is one that extends the outgrowth period in the "
            "intra-ray mesenchymal lineage and nowhere else, rather than one that increases growth rate, "
            "cell number or positional values. The prediction that makes it falsifiable: an edit "
            "restricted to that lineage should change fin length without changing ray segment count per "
            "unit length, and an edit restricted to osteoblasts should do the opposite."),
        context=("Written down so it can be attacked. It is the design assumption behind perturbation "
                 "rows P1 and P4 in PLAN.md. " + SCOPE),
        assumptions=["ASSUMED, not shown: that the Exocoetid wing and the zebrafish longfin phenotype share a mechanism. Nothing read or run here tests this.",
                     "ASSUMED, not shown: that fin proportion is the binding constraint on gliding, rather than ray stiffness or muscle power."],
        limitations=["This is a hypothesis. It is not evidence, it has not been tested, and no experiment in PLAN.md has been performed.",
                     "No Exocoetid expression, timing or cell-lineage data exists in this project.",
                     "Even if true, it addresses trait T1 only and leaves T3, T5, T6 and T8 (caudal asymmetry, ray material, launch muscle, behaviour) entirely unaddressed."],
        source=computed_source("PLAN.md"),
        origin="hypothesis",
    ),
    dict(
        id="zf2ff-claim-pleiotropy-conflicts",
        title="Two candidate edits for flying-fish traits destroy other required traits in the same organism",
        statement=(
            "Reading the abstracts together exposes two conflicts that any flying-fish design has to "
            "resolve. First: triple hoxa13a/hoxa13b/hoxd13a mutant rays become shorter and thicker and "
            "lose joints, bifurcations and actinotrichia, resembling acanthomorph spiny rays (PMID "
            "41739864) — so the edit that moves rays toward a stiffer, spine-like character also shrinks "
            "the fin and deletes the collagen fibres, opposing the enlarged-wing trait. Second: eda "
            "knockout zebrafish lack scales, fin rays, pharyngeal teeth and gill rakers (PMID 41344457) "
            "— so a scale or keel edit through eda is not separable from the fin-ray programme. Neither "
            "conflict was resolvable from what was read."),
        context=("A derived reading of two source abstracts, not a new experiment. Its value is that it "
                 "rules out two otherwise attractive edit routes before any bench cost is incurred. "
                 + SCOPE),
        assumptions=["The two abstracts' phenotype descriptions are taken at face value.",
                     "ASSUMED: that these zebrafish pleiotropies would also hold in an Exocoetid. Untested."],
        limitations=["Abstract-level reads on both sides; no dosage series, conditional or cell-type-restricted version of either edit was examined, and either could dissolve the conflict.",
                     "Danio rerio only.",
                     "This is a conflict between published phenotypes, not a demonstration that no design can satisfy both."],
        source=computed_source("PLAN.md"),
        origin="derived",
    ),
]

PROBLEMS = [
    dict(
        id="zf2ff-problem-lat4a-identifier",
        title="Which zebrafish UniProt entry is the 'lat4a' of the flying-fish convergence papers?",
        known_state=(
            "Two independent papers name lat4a as a fin-size locus with a convergent signature in flying "
            "fishes (PMID 34534441) and a convergent amino-acid change shared with syngnathids, reported "
            "as confirmed in vitro (PMID 40689752). UniProt's zebrafish entries are slc43a2a (Q7ZUS0, "
            "153 aa, a fragment) and slc43a2b (Q5PR35, 592 aa, annotated 'L-type amino acid transporter "
            "4'). This project mapped both to GCA_018398805.1 and they best-hit different scaffolds "
            "(JAGFBZ010001224.1 and JAGFBZ010000485.1), so two distinct LAT4-like regions are detectable."),
        question=("Which gene — and therefore which Exocoetid scaffold region — do the two papers mean by "
                  "lat4a, and which codon carries the reported convergent change?"),
        problem_kind="project_gap",
        novelty_status="Not a field open problem; it is a gap in this project's reading. Resolvable by one full-text read.",
        data_access=("Both papers are indexed in Europe PMC; PMID 34534441 is Current Biology (access not "
                     "checked), PMID 40689752 is Integrative Zoology (access not checked). The assembly and "
                     "both alignments are already on disk in this repository."),
        completeness="actionable",
        acceptance_criteria=["A full-text read of PMID 34534441 and PMID 40689752 names the gene identifier or accession used, and the residue position of the convergent change.",
                             "The named identifier is matched to one of the two mapped scaffold regions, with the amino-acid position located in that alignment."],
        falsifiers=["The papers use a gene identifier that corresponds to neither slc43a2a nor slc43a2b, in which case the candidate locus in this project is wrong.",
                    "The convergent change is reported only in Exocoetid species other than H. speculiger and is absent from the H. speculiger assembly."],
        next_action=("Read the two full texts for the gene identifier and residue position, then extract the "
                     "corresponding codon from the aligned region of GCA_018398805.1 recorded in "
                     "data/round2/mapping_summary_round2.json."),
        required_capabilities=["full-text literature access", "sequence extraction from a local FASTA"],
        cost_stop_bounds=("Two full-text reads and one short sequence-extraction script; under an hour. Stop "
                          "if neither paper states a usable identifier, and record that as the finding."),
        downstream_uses=["Unblocks analysis G4 in PLAN.md section 3.",
                         "Unblocks perturbation row P2 (single-codon knock-in), which cannot be designed against an unknown paralog."],
        source=computed_source("data/round2/mapping_summary_round2.json"),
        approach="literature_gap",
        scales=["molecular", "evolutionary"],
        context_tags=["flying fish", "lat4a", "identifier resolution"],
    ),
    dict(
        id="zf2ff-problem-no-candidate-for-caudal-asymmetry",
        title="No candidate gene is known to this project for the hypocercal caudal fin of flying fishes",
        known_state=(
            "Exocoetid caudal fins have an enlarged lower lobe used at the water surface. Zebrafish caudal "
            "fin symmetry is patterned by a central and two peripheral organizers (PMID 35403297, abstract "
            "level) and caudal fin shape imprinted in late embryogenesis is re-patterned by Shh signalling "
            "(PMID 40853969, title level). A targeted Europe PMC query for Exocoetid or Beloniform caudal "
            "and hypural asymmetry returned 34 hits, none of which was an Exocoetid caudal morphology or "
            "genetics paper with an abstract in the response."),
        question=("What genetic or developmental difference makes the Exocoetid caudal fin hypocercal, and "
                  "is any of it shared with the zebrafish caudal symmetry organizers?"),
        problem_kind="project_gap",
        novelty_status="Whether the field has addressed this was not established; the queries run here found nothing, which is weak evidence of absence.",
        data_access=("No Exocoetid caudal morphometry, expression or sequence data specific to the trait was "
                     "found. The only Exocoetid assembly is unannotated and there is no Exocoetid "
                     "transcriptome in anything retrieved."),
        completeness="recorded",
        required_capabilities=["comparative morphology literature access", "Exocoetid specimens or published morphometry"],
        downstream_uses=["Marks perturbation row P11 in PLAN.md as having no designable edit, which prevents an invented one."],
        source=computed_source("SOURCES.md"),
        approach="literature_gap",
        scales=["organ", "tissue", "developmental"],
        context_tags=["flying fish", "caudal fin", "hypocercal", "unknown"],
    ),
    dict(
        id="zf2ff-problem-no-exocoetid-husbandry",
        title="Nothing retrieved establishes Exocoetid husbandry, spawning, embryo access or transgenesis",
        known_state=(
            "Every engineering method in PLAN.md section 5 that is rated feasible is feasible *in zebrafish*. "
            "Across 45 Europe PMC queries, no record retrieved described captive Exocoetid breeding, embryo "
            "collection, microinjection or transgenesis. Cytogenetic work on three species used chromosome "
            "preparations, not living embryos (PMID 42325591)."),
        question=("Can Exocoetid embryos be obtained and injected at all, and by whom, or is every 'edit a "
                  "flying fish' route closed at the husbandry step regardless of the genetics?"),
        problem_kind="project_gap",
        novelty_status="This is a gap in this project's knowledge, not a claim that the field has never done it.",
        data_access="No source read addresses it. Marine station and fisheries literature was not searched.",
        completeness="recorded",
        required_capabilities=["marine fish husbandry literature", "contact with a pelagic-fish facility"],
        downstream_uses=["Bounds the whole project: it separates 'a zebrafish with flying-fish fin proportions', which is scoped, from 'a flying fish', which is not."],
        source=computed_source("SOURCES.md"),
        approach="measurement",
        scales=["organism", "developmental"],
        context_tags=["flying fish", "husbandry", "feasibility hard stop"],
    ),
]


def build(kind, payloads):
    out = []
    for p in payloads:
        rid = p.pop("id")
        draft = {"namespace": NS, "kind": kind, "id": rid, "issuer": ISSUER,
                 "source_uri": f"urn:frontier:project:zebrafish-to-flying-fish:{rid}",
                 "visibility": "public", "predecessor": None,
                 "payload": dict(p, prior_review=NOT_REVIEWED) if kind == "Claim" else dict(p)}
        Draft.model_validate(draft)
        out.append(draft)
    return out


drafts = build("Claim", CLAIMS) + build("Problem", PROBLEMS)
doc = {
    "schema": "frontier-record-0.1 drafts (not submitted, not reviewed)",
    "project": "projects/zebrafish-to-flying-fish",
    "issuer": ISSUER,
    "note": ("These are proposed drafts validated against frontier/models.py. SPEC-001: a record being "
             "schema-valid is not a scientific claim of any kind. None of these has been submitted to a "
             "store, assessed, or reviewed by a second party."),
    "counts": {"Claim": len(CLAIMS), "Problem": len(PROBLEMS)},
    "validated_against": "frontier.models.Draft",
    "drafts": drafts,
}
out = pathlib.Path(sys.argv[1])
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(doc, indent=1) + "\n")
print(f"validated {len(drafts)} drafts: {doc['counts']}")
for d in drafts:
    print(" ", d["kind"], d["id"], "origin=" + d["payload"].get("origin", d["payload"].get("completeness", "-")))
