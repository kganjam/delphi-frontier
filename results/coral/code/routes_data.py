#!/usr/bin/env python3
"""
routes_data.py — the route table for "Design a coral", as data.

Every `pmid` here appears in VERIFIED, which is the set of PubMed IDs that the research
blocks in raw/ record as having been fetched and title-matched with
get_article_metadata. build_routes.py refuses to emit the file if any route cites a PMID
outside that set, so a hallucinated identifier cannot reach routes.json.

Twelve of them were additionally re-verified directly in this session (see RE_VERIFIED).

read_level is per source and per route: a paper read at abstract level supports an
abstract-level claim and no more.
"""

# PMIDs the research blocks record as fetched and title-matched.
VERIFIED = {
    # symbiont.md
    "30100341", "16928632", "20454653", "15178799", "18577506", "26034268", "32592285",
    "32585772", "37727091", "32518247", "25099991", "32426508", "37913765", "39838803",
    "42010874", "37752965", "30779749", "28713348", "41592424", "29459692", "29365068",
    "42960469", "15306799", "26041354", "28108671", "10393938", "28782552", "32268445",
    "19603078", "41877353", "42519509", "25136339", "35539007", "35276225", "39207106",
    # assisted-evolution.md
    "25646461", "28247459", "26113720", "34482591", "32453867", "39402025", "41999765",
    "41027478", "27081069", "31999709", "27509748", "40200110", "29672529", "29109975",
    "41131223", "41241951", "40442326",
    # genome-cell.md
    "21785439", "29242500", "32675347", "39567907", "39964876", "40212849", "23297204",
    "24762535", "33168726", "24642862", "31693674", "34299075", "29881778", "38390378",
    "41275842", "39027686", "28817121", "20018670", "42478180", "42431872", "39776154",
    "42385704", "40916562", "29695630", "37276409", "41772232", "40380248", "21637757",
    "30746460", "29062113", "26040894", "18617510", "23765379", "25139990", "27253604",
    "27122561", "33622149", "40990046", "23504739", "17395821",
    # morphology.md
    "24894390", "17122855", "12927523", "15178203", "11312588", "23326222", "10061916",
    "25044878", "25519925", "28855618", "18979594", "39232103", "25556295", "38170717",
    # settlement.md
    "37032381", "33009428", "34272460", "21559509", "22655067", "39431916", "38481984",
    "42409953", "41288555", "41363886", "42362633", "25898011", "42310106", "28573015",
    "29273761", "40267811", "23185875", "33232367", "29070842", "32703979", "27912010",
    "36882893", "21302829", "30991454",
    # microbiome.md
    "28326066", "33321044", "30518818", "34389536", "33957989", "40151579", "42692023",
    "42910909", "40230573", "38914624", "27557714", "18923867", "17107548", "26636661",
    "27034285", "32551200", "33883581", "37646698", "42909972", "33175886",
}

# Re-fetched directly in this session with get_article_metadata; titles matched the
# research blocks exactly. DOIs as returned by that tool.
RE_VERIFIED = {
    "28782552": "10.1016/j.jtbi.2017.08.003",
    "33168726": "10.1073/pnas.1920779117",
    "37276409": "10.1073/pnas.2216144120",
    "16928632": "10.1098/rspb.2006.3567",
    "32426508": "10.1126/sciadv.aba2498",
    "37913765": "10.1111/gcb.16987",
    "34389536": "10.1126/sciadv.abg3088",
    "32551200": "10.7717/peerj.9289",
    "23326222": "10.1371/journal.pcbi.1002849",
    "24894390": "10.1111/ele.12306",
    "33232367": "10.1371/journal.pone.0242847",
    "32703979": "10.1038/s41598-020-68289-4",
}

SCALES = [
    dict(key="molecular", label="Molecular · sequence and regulation",
         blurb="Enhancers, methylation and polygenic scores. The level at which coral "
               "is furthest behind: no coral enhancer has ever been validated, and the "
               "PubMed search for Acropora ATAC-seq returns zero against five for "
               "Nematostella run the same way."),
    dict(key="gene", label="Gene · targeted edits in the animal",
         blurb="CRISPR/Cas9 in Acropora millepora works, in the injected generation, "
               "and has produced exactly four published coral phenotypes. There is no "
               "stable transgenic or germline-edited coral line anywhere in the "
               "literature read here."),
    dict(key="cell", label="Cell and tissue · calcification",
         blurb="The calicoblastic epithelium raises pH and concentrates bicarbonate "
               "under the skeleton. One gene in that pathway has a loss-of-function "
               "coral phenotype; everything else is localisation, expression and "
               "inhibitor work."),
    dict(key="symbiont", label="Symbiont · Symbiodiniaceae",
         blurb="Change the alga, not the animal. The best-evidenced thermal route and "
               "the one with the clearest measured cost. Seven genera, a shuffling "
               "literature that disagrees with itself in a way that has been partly "
               "reconciled, and no genome-edited symbiont."),
    dict(key="microbiome", label="Microbiome · bacteria, phage, antibiotics",
         blurb="Beneficial Microorganisms for Corals. Striking tank results, one "
               "in-water heatwave trial, and inoculants that in every study read here "
               "disappear within weeks. The one microbial intervention with a real "
               "field record is an antibiotic for a disease whose pathogen is unknown."),
    dict(key="colony", label="Colony · growth form and mechanics",
         blurb="Branching, plating, massive. Decides flow, light capture, what a storm "
               "breaks and what fish live in it. Substantially plastic, steerable by "
               "environment without touching a gene, and the one scale with a published "
               "runnable model class."),
    dict(key="population", label="Population · breeding and gene flow",
         blurb="Selective breeding, assisted gene flow, hybrids, cryobanking. The only "
               "family of routes with anything like a deployment programme behind it, "
               "and still no located instance of a bred coral on the Great Barrier Reef."),
    dict(key="larval", label="Larval · settlement and recruitment",
         blurb="Where restoration actually fails. Adults survive; recruits do not. "
               "Cues, devices, substrate, grazing and sediment, with first-year survival "
               "spread over more than tenfold across sites and thermal years."),
    dict(key="ecological", label="Ecological and regulatory · the reef, the law",
         blurb="Siting, permits, scale and what the whole portfolio is for. A median "
               "restoration project covers 100 square metres. The arithmetic that "
               "follows from that is the honest frame for everything above."),
]

EVIDENCE_LABELS = {
    "direct_coral_phenotype": "direct coral phenotype",
    "direct_coral_phenotype_relayed": "direct coral phenotype, source unverified",
    "direct_other_species": "direct, another species",
    "cis_regulatory_inference": "cis-regulatory inference",
    "model_only": "model only",
    "proposed": "proposed",
}

OUTCOME_CLASSES = [
    dict(key="thermal", label="Thermal tolerance",
         match=r"bleach|thermal|thermotoleran|heat|degree heating|DHW|temperature"),
    dict(key="morphology", label="A chosen colony shape",
         match=r"branch|plat|morpholog|colony form|growth form|compact|"
               r"structural complexit|dislodg"),
    dict(key="recruitment", label="Settles and survives where you put it",
         match=r"settl|recruit|spat|metamorph|outplant|seed"),
    dict(key="holobiont", label="Engineered holobiont, not animal",
         match=r"symbion|Symbiodin|Durusdinium|Cladocopium|microbiom|probiotic|"
               r"consortium|holobiont"),
    dict(key="skeleton", label="Skeleton and calcification",
         match=r"skelet|calcif|aragonit|corallit|biominerali|bicarbonate"),
    dict(key="disease", label="Disease resistance",
         match=r"disease|lesion|SCTLD|pathogen|phage|antibiotic|white plague"),
    dict(key="enabling", label="Enabling work, not a coral",
         match=r"infrastructur|protocol|readout|toolkit|map|bank|permit|portfolio"),
]

OUTCOME_ORDERING_NOTE = (
    "THE OUTCOME IS DECLARED PER ROUTE, as a field, not inferred from the text. An "
    "earlier version assigned it by running these regexes over each route's own prose "
    "and taking the first match, and it was wrong in about ten of forty-five cases in "
    "ways that all looked plausible: the HSF1 knockout came out as 'recruitment' "
    "because its phenotype is in larvae, the Durusdinium route came out as 'skeleton' "
    "because the cost it pays is calcification, and the flow-plasticity route came out "
    "as 'skeleton' because the sentence explaining it mentions skeleton already laid "
    "down. A pattern run over prose classifies the prose. The regexes are KEPT, but "
    "only as an audit: build_routes.py records where the declared outcome and the "
    "pattern disagree, and those disagreements are data about the writing, not "
    "corrections to the tag."
)
