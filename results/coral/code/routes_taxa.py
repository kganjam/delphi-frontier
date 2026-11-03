#!/usr/bin/env python3
"""
routes_taxa.py — what organism each route's evidence actually comes from.

Added after the team lead noticed that Cunning, Silverstein & Baker 2015 — the
symbiont-shuffling reconciliation paper the whole shuffling route leans on — is in
ORBICELLA FAVEOLATA, a massive Caribbean coral, while most of the rest of this design
space is Acropora-centred: the CRISPR precedent, the assisted-evolution programme and
most of the morphology work. A route's evidence transferring to its target is therefore
an ASSUMPTION in a large fraction of this table, and it was invisible before this file
existed.

`transfer` is one of, from weakest assumption to strongest:

  none                  evidence and target are the same species
  within_genus          different species, same genus (usually within Acropora)
  cross_genus           a different reef-building coral genus
  cross_growth_form     a different coral genus AND a different growth form (branching
                        against massive), which matters because growth form covaries
                        with bleaching susceptibility, fecundity and mechanics
  non_reef_coral        a stony coral that does not build reefs (Astrangia, the
                        Mediterranean species in the decalcification work)
  non_coral_cnidarian   an anemone (Exaiptasia) or Nematostella
  not_applicable        the route is not about an organism (siting, permits, portfolio)

Where a route's evidence spans several, the WEAKEST applicable value is recorded, because
that is the assumption the route actually rests on.
"""

TAXA = {
    # ---- molecular ----------------------------------------------------------------
    "mol-coral-atac-first": dict(
        target_taxon="reef-building corals (Acropora, Stylophora)",
        species_of_evidence=["Nematostella vectensis"],
        transfer="non_coral_cnidarian",
        note="The only validated cnidarian enhancer map is in Nematostella, which is not "
             "a coral and does not calcify. The scoped negative that motivates the route "
             "is about Acropora, so the route is a proposal to REMOVE this transfer gap, "
             "not to rely on it."),
    "mol-methylation-priming": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Stylophora pistillata", "unnamed reef-building coral"],
        transfer="cross_genus",
        note="Liew et al. is Stylophora; Abbott et al.'s abstract names no species. The "
             "two also disagree, so the route rests on cross-genus transfer of a "
             "disputed effect."),
    # ---- gene ----------------------------------------------------------------------
    "gene-hsf1-knockout": dict(
        target_taxon="Acropora millepora",
        species_of_evidence=["Acropora millepora"],
        transfer="none",
        note="Target and evidence are the same species. One of only a handful of routes "
             "in this table for which that is true."),
    "gene-hsf1-pathway-frontloading": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Acropora hyacinthus", "Acropora millepora"],
        transfer="within_genus",
        note="The frontloading correlation is in A. hyacinthus; the only causal edit is "
             "in A. millepora. Same genus, different species, and the two results are "
             "different KINDS of evidence."),
    "gene-slc26a11-symbiosis": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Exaiptasia", "unnamed reef-building coral"],
        transfer="non_coral_cnidarian",
        note="The abstract reports the requirement 'in Aiptasia and a reef-building "
             "coral' but does not name the coral, so the coral half cannot be placed."),
    "gene-knockdown-toolkit-astrangia": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Astrangia poculata"],
        transfer="non_reef_coral",
        note="Astrangia is a temperate, facultatively symbiotic, non-reef-building stony "
             "coral. That is exactly why it is tractable and exactly why the transfer is "
             "not guaranteed. The route is about MOVING the toolkit, so the gap is the "
             "point."),
    # ---- cell ----------------------------------------------------------------------
    "cell-slc4g-knockout": dict(
        target_taxon="Acropora millepora",
        species_of_evidence=["Acropora millepora", "Stylophora pistillata"],
        transfer="none",
        note="The CRISPR phenotype is in the target species; the Stylophora work is "
             "supporting expression and localisation only."),
    "cell-untested-calcification-pathway": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Stylophora pistillata", "Acropora millepora",
                             "cold-water azooxanthellate corals"],
        transfer="cross_growth_form",
        note="The calcium-ATPase inference comes from COLD-WATER, azooxanthellate corals "
             "— a different ocean, a different depth and no symbionts. That is the "
             "weakest link and it carries the pH-up-regulation mechanism."),
    "cell-ecm-ph-readout": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Stylophora pistillata", "Acropora yongei",
                             "Pocillopora damicornis"],
        transfer="cross_genus",
        note="Three genera, three methods, and the methods disagree on absolute values. "
             "The route is the measurement, so the transfer question is about whether "
             "the TECHNIQUE moves, not the number."),
    "cell-soft-body-refuge": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["two Mediterranean scleractinians (species not verified)"],
        transfer="non_reef_coral",
        note="This is the published objection, not ours: the commenter's criticism is "
             "precisely that the two slow-calcifying Mediterranean species 'may not be "
             "representative' of zooxanthellate reef-builders, and the authors concede "
             "they chose slow calcifiers."),
    # ---- symbiont -------------------------------------------------------------------
    "sym-durusdinium-inoculation": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Acropora millepora", "Montastraea cavernosa",
                             "unnamed Caribbean hosts", "Exaiptasia pallida"],
        transfer="non_coral_cnidarian",
        note="The thermal gain and the growth penalty are both from Acropora millepora; "
             "the calcification figure is from unnamed Caribbean hosts; the MECHANISM "
             "(reduced carbon assimilation per cell) is from an ANEMONE. Three different "
             "levels of transfer in one route."),
    "sym-shuffle-by-induced-bleaching": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Montastraea cavernosa", "Orbicella faveolata",
                             "Acropora millepora"],
        transfer="cross_growth_form",
        note="THE ONE THE LEAD CAUGHT. The reconciliation result that makes this route's "
             "severity-dependence statement possible — Cunning, Silverstein & Baker 2015 "
             "— is in ORBICELLA FAVEOLATA, a massive Caribbean coral. The persistence "
             "result is in Montastraea cavernosa, also massive and Caribbean. The "
             "degrees-of-tolerance figure is in Acropora millepora, branching and "
             "Indo-Pacific. Applying the severity rule to an Acropora route crosses both "
             "genus and growth form and an ocean, and nothing read here tests that."),
    "sym-heat-evolved-ss8": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Galaxea fascicularis", "Exaiptasia diaphana"],
        transfer="non_coral_cnidarian",
        note="The adult-coral result is in Galaxea fascicularis, which is neither "
             "Acropora nor a massive Caribbean coral; the strain-panel comparison that "
             "shows heat evolution does NOT reliably help is in an anemone."),
    "sym-heat-evolved-library-screen": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["coral larvae, host species not printed in the text read"],
        transfer="cross_genus",
        note="The PMC text export strips italicised species names, so the host species "
             "of the Buerger larvae cannot be stated from what was read. Marked "
             "cross_genus because it cannot be shown to match any target."),
    "sym-host-matched-switching": dict(
        target_taxon="Acropora",
        species_of_evidence=["Acropora tenuis", "Acropora millepora"],
        transfer="within_genus",
        note="This is the one route whose POINT is that transfer fails: the ranking of "
             "symbiont types reverses between two Acropora species."),
    "sym-transgenic-symbiont": dict(
        target_taxon="Symbiodiniaceae",
        species_of_evidence=["Symbiodinium microadriaticum CCMP2467", "dinoflagellates"],
        transfer="none",
        note="Target and evidence are both the alga. The transfer question here is to "
             "OTHER STRAINS, not to another host."),
    "sym-feed-the-host-to-pay-for-the-symbiont": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Exaiptasia pallida", "diverse coral taxa (Kemp)",
                             "model only (Cunning)"],
        transfer="non_coral_cnidarian",
        note="The carbon deficit this route compensates was measured in an anemone, and "
             "the counter-evidence says the deficit may not exist in corals at all."),
    "sym-do-not-move-the-symbiont": dict(
        target_taxon="Caribbean reef corals",
        species_of_evidence=["unnamed Caribbean hosts"],
        transfer="none",
        note="The harm and the target are the same system."),
    # ---- microbiome -----------------------------------------------------------------
    "micro-bmc-consortium": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Pocillopora damicornis",
                             "a Brazilian Atlantic coral (genus not stated)",
                             "Pocillopora cf. verrucosa", "Acropora hemprichii"],
        transfer="cross_genus",
        note="The 40% survival result's host species was stripped from the extracted "
             "text and is not stated. Four studies, at least three genera, two oceans."),
    "micro-postbiotic-heatkilled": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Acropora cf. valida"],
        transfer="within_genus",
        note="The only in-water trial, and it is in an Acropora — which makes it the "
             "best-matched microbiome route for an Acropora-centred page."),
    "micro-homogenate-transplant": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Pocillopora sp.", "Porites sp."],
        transfer="cross_genus",
        note="Two genera, both conspecific donor-to-recipient within the study, so the "
             "transfer question is to a THIRD genus."),
    "micro-amoxicillin-sctld": dict(
        target_taxon="Caribbean and Florida reef corals",
        species_of_evidence=["Montastraea cavernosa", "four further species (unnamed)",
                             "Orbicella faveolata"],
        transfer="none",
        note="Disease, treatment and target are the same system, which is why this is "
             "the one microbial route with a real field record."),
    "micro-phage-prophylaxis": dict(
        target_taxon="reef corals",
        species_of_evidence=["coral species not stated in the abstract"],
        transfer="cross_genus",
        note="Neither the coral species nor the replicate number is in the abstract, and "
             "the pathogen is one named bacterium that is NOT the stony coral tissue "
             "loss disease agent."),
    # ---- colony ----------------------------------------------------------------------
    "colony-flow-regime-plasticity": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Pocillopora verrucosa", "Pocillopora damicornis",
                             "three Pocillopora morphospecies"],
        transfer="cross_genus",
        note="Every flow result here is Pocillopora. Applying it to Acropora, whose "
             "branching architecture is different, is untested."),
    "colony-light-plate-induction": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Montipora capitata"],
        transfer="cross_genus",
        note="One genus, one experiment, and it is a PREPRINT. The strongest direct "
             "light-to-plate evidence in this table is also the least peer-reviewed."),
    "colony-compact-for-storms": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["11 species at Lizard Island across five growth forms",
                             "Sesoko Island community survey"],
        transfer="within_genus",
        note="Unusually broad taxonomic coverage for this table — the mechanical result "
             "is explicitly ACROSS growth forms, which is what makes it transferable."),
    "colony-branching-for-habitat": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Pocillopora", "Acropora", "Porites", "Seriatopora",
                             "Stylophora", "Montipora"],
        transfer="within_genus",
        note="Six genera measured by the same photogrammetry method, which is what makes "
             "the scaling exponents comparable across growth forms."),
    "colony-model-guided-placement": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Pocillopora verrucosa"],
        transfer="cross_genus",
        note="The one calibrated member of this model class was validated against five "
             "Pocillopora verrucosa colonies. Nothing validates it for any other genus."),
    "colony-lineage-selection": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Pocillopora acuta", "Acropora cervicornis",
                             "Acropora palmata"],
        transfer="cross_genus",
        note="The morph-with-different-bleaching-threshold result is Pocillopora; the "
             "tip-versus-base expression work is Caribbean Acropora."),
    # ---- population -------------------------------------------------------------------
    "pop-selective-breeding": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Acropora (species not named in the abstracts read)",
                             "19 species in the meta-analysis"],
        transfer="within_genus",
        note="The directly measured heritabilities are Acropora; the meta-analysis spans "
             "19 species and disagrees with them, which is itself a transfer problem."),
    "pop-assisted-gene-flow": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Acropora (Dixon, species not in abstract)",
                             "two species at Ningaloo"],
        transfer="within_genus",
        note="Larval results only. No juvenile or adult field survival in any of them."),
    "pop-interspecific-hybrids": dict(
        target_taxon="Acropora",
        species_of_evidence=["Acropora kenti", "Acropora loripes",
                             "two further GBR Acropora pairs"],
        transfer="within_genus",
        note="Within Acropora by construction — the route IS an interspecific cross. The "
             "two studies disagree, and they used different species pairs, which may be "
             "the whole explanation."),
    "pop-thermal-preconditioning": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Great Barrier Reef corals, broadly",
                             "Acropora hyacinthus"],
        transfer="within_genus",
        note="The natural protective-trajectory analysis is reef-wide and satellite-based "
             "rather than species-specific, which is unusually broad support."),
    "pop-cryobank": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Diploria labyrinthiformis", "Mussismilia harttii"],
        transfer="cross_growth_form",
        note="Both are massive corals, one Caribbean and one Brazilian. The two give "
             "DIFFERENT answers on whether frozen sperm matches fresh, and no Acropora "
             "figure was retrieved."),
    # ---- larval ------------------------------------------------------------------------
    "larval-cca-cue-substrate": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["15 Great Barrier Reef coral species",
                             "Acropora cytherea"],
        transfer="within_genus",
        note="The 15-by-15 design is the broadest taxonomic coverage of any route here, "
             "and its finding is that the pairing MATTERS — three species settled below "
             "10% under every treatment."),
    "larval-tbp-negative-control": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Acropora millepora"],
        transfer="within_genus",
        note="A negative control, so transfer matters less: the point is that an assay "
             "scoring metamorphosis alone will call this a success in any species."),
    "larval-grooved-refuge-device": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Acropora tenuis", "Acropora millepora"],
        transfer="within_genus",
        note="One reef, one genus, and the device geometry is probably more transferable "
             "than the survival percentage."),
    "larval-tetrapod-seeding": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Caribbean corals (Curacao)",
                             "Diploria labyrinthiformis", "Acropora palmata"],
        transfer="cross_growth_form",
        note="Caribbean, and the attachment trade-off was measured on one massive and "
             "one branching species with different answers (doubled against quadrupled)."),
    "larval-mass-enrichment": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Acropora loripes", "Acropora tenuis"],
        transfer="within_genus",
        note="Two Acropora species, one site, two trials by the same group. The 2020 "
             "paper's own abstract says only one earlier experiment had demonstrated "
             "long-term success."),
    "larval-acoustic-enrichment": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["Favia fragum", "Diploria labyrinthiformis"],
        transfer="cross_growth_form",
        note="A brooding Caribbean coral and a massive Caribbean broadcast spawner. "
             "THERE IS NO ACROPORA VALUE AT ALL, and every verified result comes from "
             "one laboratory group with no independent replication found."),
    "larval-site-screen-sediment": dict(
        target_taxon="reef-building corals",
        species_of_evidence=["six Caribbean species", "wild larval assemblage",
                             "Ningaloo corals", "Acropora striata"],
        transfer="within_genus",
        note="Four studies across two oceans agreeing on direction, which is why this is "
             "the best-supported route in the recruitment group."),
    "larval-microfragment-bypass": dict(
        target_taxon="massive reef-building corals",
        species_of_evidence=["Orbicella faveolata", "Montastraea cavernosa"],
        transfer="none",
        note="Target and evidence are both massive Caribbean corals. The route is "
             "explicitly FOR slow-growing massive corals, so this is well matched — and "
             "it is a reason not to read it across to branching taxa."),
    # ---- ecological ---------------------------------------------------------------------
    "eco-site-prioritisation": dict(
        target_taxon="restoration sites, not an organism",
        species_of_evidence=["global restoration-site analysis"],
        transfer="not_applicable", note="A siting decision, not a biological claim."),
    "eco-regulated-pilot": dict(
        target_taxon="not an organism",
        species_of_evidence=["programme pages and treaty texts"],
        transfer="not_applicable",
        note="Regulatory and programmatic; no organism-level evidence."),
    "eco-portfolio-with-mitigation": dict(
        target_taxon="reefs, not an organism",
        species_of_evidence=["global reviews and genomic models"],
        transfer="not_applicable",
        note="Programme-level. The underlying models are Acropora-parameterised, which "
             "is noted inside the route."),
}

# Ordered weakest-assumption-first; a route's value is the weakest that applies.
TRANSFER_ORDER = ["non_coral_cnidarian", "non_reef_coral", "cross_growth_form",
                  "cross_genus", "within_genus", "none", "not_applicable"]

TRANSFER_LABELS = {
    "none": "same species",
    "within_genus": "same genus, different species",
    "cross_genus": "different coral genus",
    "cross_growth_form": "different genus AND growth form",
    "non_reef_coral": "a stony coral that does not build reefs",
    "non_coral_cnidarian": "an anemone or Nematostella, not a coral",
    "not_applicable": "not an organism-level claim",
}
