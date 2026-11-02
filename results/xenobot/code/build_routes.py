#!/usr/bin/env python3
"""Build routes.json. Every PMID below was retrieved from PubMed in this session
and its title, journal, volume, pages and DOI read back. read_level is what I
actually read, not what I could have read:
  full-text  -- I retrieved and read the article full text
  abstract   -- I retrieved and read the abstract text
  listing    -- I retrieved the citation record (title/journal/pages/DOI) only
  search-summary / could-not-access -- as labelled
"""
import json, os

S = {}  # source registry


def src(key, cite, pmid=None, doi=None, read="listing"):
    S[key] = {"cite": cite, "read_level": read}
    if pmid:
        S[key]["pmid"] = pmid
    if doi:
        S[key]["doi"] = doi
    return key


# --- verified in this session from PubMed -----------------------------------
src("kriegman20", "Kriegman et al. 2020, Proc Natl Acad Sci U S A 117:1853-1859, 'A scalable pipeline for designing reconfigurable organisms'", "31932426", "10.1073/pnas.1910837117", "full-text")
src("kriegman21", "Kriegman et al. 2021, Proc Natl Acad Sci U S A 118:e2112672118, 'Kinematic self-replication in reconfigurable organisms'", "34845026", "10.1073/pnas.2112672118", "full-text")
src("blackiston21", "Blackiston et al. 2021, Sci Robot 6:eabf1571, 'A cellular platform for the development of synthetic living machines'", "34043553", "10.1126/scirobotics.abf1571", "abstract")
src("gumuskaya23", "Gumuskaya et al. 2023, Adv Sci (Weinh) 11:e2303575, 'Motile Living Biobots Self-Construct from Adult Human Somatic Progenitor Seed Cells'", "38032125", "10.1002/advs.202303575", "abstract")
src("bhattaram25", "Bhattaram et al. 2025, Sci Adv 11:eadx4176, 'AggreBots: Configuring CiliaBots through guided, modular tissue aggregation'", "41004589", "10.1126/sciadv.adx4176", "abstract")
src("bhattaram25pre", "Bhattaram et al. 2025, bioRxiv, 'AggreBots: configuring CiliaBots through guided, modular tissue aggregation' (preprint of the above)", "40060463", "10.1101/2025.02.22.639695", "listing")
src("pai25", "Pai et al. 2025, Commun Biol 8:646, 'Basal Xenobot transcriptomics reveals changes and novel control modality in cells freed from organismal influence'", "40263484", "10.1038/s42003-025-08086-9", "abstract")
src("blackiston23", "Blackiston et al. 2023, Soft Robot 10:674-686, 'Biological Robots: Perspectives on an Emerging Interdisciplinary Field'", "37083430", "10.1089/soro.2022.0142", "abstract")
src("levin20", "Levin, Bongard & Lunshof 2020, Nat Rev Mol Cell Biol 21:655-656, 'Applications and ethics of computer-designed organisms'", "32782340", "10.1038/s41580-020-00284-z", "listing")
src("mitchell07", "Mitchell et al. 2007, Nature 447:97-101, 'A positive feedback mechanism governs the polarity and motion of motile cilia'", "17450123", "10.1038/nature05771", "abstract")
src("mitchell09", "Mitchell et al. 2009, Curr Biol 19:924-929, 'The PCP pathway instructs the planar orientation of ciliated cells in the Xenopus larval skin'", "19427216", "10.1016/j.cub.2009.04.018", "listing")
src("collins20", "Collins et al. 2020, Curr Top Dev Biol 145:3-39, 'Building a ciliated epithelium: Transcriptional regulation and radial intercalation of multiciliated cells'", "34074533", "10.1016/bs.ctdb.2020.08.001", "abstract")
src("kaushik26", "Kaushik et al. 2026, Genes Genomics 48:1131-1143, 'BMP/Ventx1.1 axis modulates the multiciliogenesis in the early Xenopus epidermis'", "42371315", "10.1007/s13258-026-01777-5", "listing")
src("gonzalez09", "Gonzalez-Rodriguez & Lauga 2009, J Phys Condens Matter 21:204103, 'Reciprocal locomotion of dense swimmers in Stokes flow'", "21825512", "10.1088/0953-8984/21/20/204103", "abstract")
src("qiu14", "Qiu et al. 2014, Nat Commun 5:5119, 'Swimming by reciprocal motion at low Reynolds number'", "25369018", "10.1038/ncomms6119", "abstract")
src("hubert21", "Hubert et al. 2021, Phys Rev Lett 126:224501, 'Scallop Theorem and Swimming at the Mesoscale'", "34152187", "10.1103/PhysRevLett.126.224501", "abstract")
src("herschlag11", "Herschlag & Miller 2011, J Theor Biol 285:84-95, 'Reynolds number limits for jet propulsion: a numerical study of simplified jellyfish'", "21669208", "10.1016/j.jtbi.2011.05.035", "abstract")
src("jo16", "Jo et al. 2016, Phys Rev E 94:063116, 'Passive swimming in viscous oscillatory flows'", "28085432", "10.1103/PhysRevE.94.063116", "listing")
src("raman16", "Raman et al. 2016, Proc Natl Acad Sci U S A 113:3497-3502, 'Optogenetic skeletal muscle-powered adaptive biological machines'", "26976577", "10.1073/pnas.1516139113", "listing")
src("williams14", "Williams et al. 2014, Nat Commun 5:3081, 'A self-propelled biohybrid swimmer at low Reynolds number'", "24435099", "10.1038/ncomms4081", "abstract")
src("cvetkovic14", "Cvetkovic et al. 2014, Proc Natl Acad Sci U S A 111:10125-10130, 'Three-dimensionally printed biological machines powered by skeletal muscle'", "24982152", "10.1073/pnas.1401577111", "abstract")
src("guix21", "Guix et al. 2021, Sci Robot 6:eabe7577, 'Biohybrid soft robots with self-stimulating skeletons'", "34043566", "10.1126/scirobotics.abe7577", "abstract")
src("ceron23", "Ceron et al. 2023, Proc Natl Acad Sci U S A 120:e2221913120, 'Programmable self-organization of heterogeneous microrobot collectives'", "37276400", "10.1073/pnas.2221913120", "abstract")
src("ussia24", "Ussia et al. 2024, ACS Nano 18:13171-13183, 'Magnetic Microrobot Swarms with Polymeric Hands Catching Bacteria and Microplastics in Water'", "38717036", "10.1021/acsnano.4c02115", "abstract")
src("peng22", "Peng et al. 2022, ACS Nano 16:7615-7625, 'Shape-Controlled Self-Assembly of Light-Powered Microrobots into Ordered Microchains for Cells Transport and Water Remediation'", "35451832", "10.1021/acsnano.1c11136", "listing")
src("sun24", "Sun et al. 2024, Small 20:e2310769, 'Multiple Magneto-Optical Microrobotic Collectives with Selective Control in Three Dimensions Under Water'", "38263803", "10.1002/smll.202310769", "listing")
src("cheng25", "Cheng et al. 2025, Small 21:e2504289, 'Self-Assembly and Collective Locomotion Behavior of Swarm Microrobot'", "40545868", "10.1002/smll.202504289", "listing")
src("mou19", "Mou et al. 2019, iScience 19:415-424, 'Phototactic Flocking of Photochemical Micromotors'", "31421596", "10.1016/j.isci.2019.07.050", "listing")
src("ghosh20", "Ghosh et al. 2020, Adv Healthc Mater 10:e2000869, 'Magnetic Resonance Guided Navigation of Untethered Microgrippers'", "32691952", "10.1002/adhm.202000869", "listing")
src("yin19", "Yin et al. 2019, Biomed Microdevices 21:82, 'Untethered microgripper-the dexterous hand at microscale' (review)", "31418070", "10.1007/s10544-019-0430-9", "listing")
src("mohanty20", "Mohanty, Khalil & Misra 2020, Proc Math Phys Eng Sci 476:20200621, 'Contactless acoustic micro/nano manipulation: a paradigm for next generation applications in life sciences' (review)", "33363443", "10.1098/rspa.2020.0621", "listing")
src("cao24", "Cao et al. 2024, Micromachines (Basel) 15:186, 'Acoustic Actuators for the Manipulation of Micro/Nanorobots: State-of-the-Art and Future Outlooks' (review)", "38398914", "10.3390/mi15020186", "listing")
src("chen18", "Chen et al. 2018, Adv Mater 30:e1705061, 'Small-Scale Machines Driven by External Power Sources' (review)", "29443430", "10.1002/adma.201705061", "listing")
src("sanchez14", "Sanchez, Soler & Katuri 2014, Angew Chem Int Ed Engl 54:1414-1444, 'Chemically powered micro- and nanomotors' (review)", "25504117", "10.1002/anie.201406096", "listing")
src("xu17", "Xu et al. 2017, ACS Nano 12:327-337, 'Sperm-Hybrid Micromotor for Targeted Drug Delivery'", "29202221", "10.1021/acsnano.7b06398", "listing")
src("singh17", "Singh et al. 2017, ACS Nano 11:9759-9769, 'Microemulsion-Based Soft Bacteria-Driven Microswimmers for Active Cargo Delivery'", "28858477", "10.1021/acsnano.7b02082", "listing")
src("gao13", "Gao et al. 2013, J Am Chem Soc 135:998-1001, 'Organized self-assembly of Janus micromotors with hydrophobic hemispheres'", "23286304", "10.1021/ja311455k", "listing")

# --- physics literature not indexed in PubMed; citation details NOT verified here
src("purcell77", "Purcell, E. M. 1977, Am J Phys 45(1):3-11, 'Life at low Reynolds number'", None, "10.1119/1.10903", "search-summary")
src("najafi04", "Najafi & Golestanian 2004, Phys Rev E 69:062901, 'Simple swimmer at low Reynolds number: Three linked spheres'", None, "10.1103/PhysRevE.69.062901", "search-summary")
src("lauga07", "Lauga, E. 2007, Phys Fluids 19:061703, 'Continuous breakdown of Purcell's scallop theorem with inertia'", None, "10.1063/1.2738609", "search-summary")
src("laugapowers09", "Lauga & Powers 2009, Rep Prog Phys 72:096601, 'The hydrodynamics of swimming microorganisms' (review)", None, "10.1088/0034-4885/72/9/096601", "search-summary")

# --- this project's own artifacts -------------------------------------------
src("voxart", "delphi-frontier voxel-actuation artifact, protocol frozen at commit 7b9bd5d, engine Voxelyze @ 4287e365e11416dd108f2f361e9ec4c5a011a16c; artifacts/voxel-actuation/summary.json", None, None, "full-text")
src("voxaudit", "delphi-frontier independent audit of the voxel-actuation artifact, artifacts/audits/xenobot/{manifest,qualifications}.json, 2026-11-01", None, None, "full-text")

print(f"{len(S)} sources registered")
with open("/data/scratch/designspaces/xenobot/data/sources.json", "w") as f:
    json.dump(S, f, indent=2)


def R(id, scale, title, intervention, phenotype, mechanism, strength,
      reversibility, lethality, difficulty, ev, study=None, note=None):
    d = {"id": id, "scale": scale, "title": title, "intervention": intervention,
         "predicted_phenotype": phenotype, "mechanism": mechanism,
         "evidence_strength": strength, "reversibility": reversibility,
         "lethality_risk": lethality, "difficulty": difficulty,
         "evidence": [dict(S[k]) for k in ev]}
    if study:
        d["study"] = study
    if note:
        d["note"] = note
    return d


ROUTES = []
A = ROUTES.append

# ============================================================ molecular ====
A(R("mol-notch-suppress-cilia", "molecular",
    "Suppress multiciliated-cell fate to remove ciliary propulsion",
    "Microinject Notch intracellular domain (Notch ICD) mRNA at the four-cell stage before explanting the animal cap.",
    "A construct that does NOT move itself by cilia. It becomes a passive body whose only motion is whatever an added contractile tissue produces — which is what makes a clean test of a designed gait possible at all.",
    "Notch signalling decides which inner-layer progenitors adopt the multiciliated fate; forcing the intracellular domain suppresses that fate, so the surface develops without motile cilia.",
    "direct_construct_result", "irreversible once injected; a fresh batch is the only undo",
    "low — Kriegman et al. reared and used these embryos routinely",
    "moderate: standard Xenopus microinjection, 370 pg per cell at the four-cell stage",
    ["kriegman20", "collins20"],
    note="Kriegman et al. 2020 state the purpose plainly: with cilia suppressed, 'any displacement results from contractile cardiac muscle tissue that pushes against the surface of the dish'."),
  )
A(R("mol-mcidas-gemc1", "molecular",
    "Raise or lower cilia density through the MCIDAS/GemC1 program",
    "Modulate GemC1 or MCIDAS expression in the animal-cap explant to change how many progenitors enter the multiciliated program.",
    "A construct with a tunable number of propulsive units per unit area — more cilia means more thrust per unit surface, which is the only throttle a cilia-driven biobot has. It still only moves ITSELF unless a shape is imposed that also sweeps material.",
    "GemC1 and MCIDAS initiate the multiciliated transcriptional program and centriole amplification; multiciliated cells carry 100+ motile cilia each.",
    "direct_other_species", "reversible in the sense that it is set per batch",
    "unknown — not reported for xenobot constructs specifically",
    "moderate in Xenopus embryology; untested as a biobot design knob",
    ["collins20", "kaushik26"]),
  )
A(R("mol-pcp-beat-direction", "molecular",
    "Set the direction cilia beat by biasing planar cell polarity",
    "Perturb the PCP pathway, or impose an early directional flow, while the explant is differentiating.",
    "A construct whose surface thrust points in a CHOSEN direction instead of the direction the tissue happens to settle on. This is the closest biological analogue of choosing a gait, and unlike a contractile gait it needs no actuator pattern at all.",
    "Ciliary polarity begins as a bias from tissue patterning and is then refined by the fluid flow the cilia themselves create — a positive feedback loop — with the PCP pathway supplying non-cell-autonomous directional cues.",
    "direct_other_species", "set during differentiation; not adjustable afterwards",
    "low in embryos; unknown in constructs",
    "hard: the feedback is self-reinforcing, so an early bias is amplified and an error is amplified with it",
    ["mitchell07", "mitchell09"],
    note="Both papers study the Xenopus larval skin, the same tissue the constructs are made from, but in the embryo rather than in a construct. Nobody has reported steering a xenobot this way."),
  )
A(R("mol-cardiac-progenitor", "molecular",
    "Add Xenopus cardiac progenitor tissue as a contractile actuator",
    "Excise the presumptive heart field from a tdTomato-labelled stage 23-24 embryo and sandwich it between two Notch-ICD animal caps; heal 1 h at 22 C.",
    "A construct that contracts rhythmically and crawls on the dish floor by pushing against it. This is the only published xenobot actuator that works by BODY DEFORMATION, and therefore the only one the voxel-actuation gait model is even about.",
    "Cardiac progenitors develop into cardiomyocytes and produce contractile waves at the locations where the tissue was placed; coordination emerges spontaneously without enforced signalling.",
    "direct_construct_result", "irreversible: the tissue is grafted",
    "moderate — contractile tissue costs much more metabolic energy, so the build filter caps it at 50% of the body",
    "hard: three-layer microsurgical assembly plus two mRNA injections",
    ["kriegman20"], study="regime-check",
    note="Read from the full text: contraction was modelled in silico as a 2 Hz central pattern generator with RANDOM per-voxel phase offsets, and the geometry was evolved to rectify that randomness. That is the opposite of the voxel-actuation artifact's six hand-chosen deterministic phase fields."),
  )

# ================================================================= cell ====
A(R("cell-xenopus-animal-cap", "cell",
    "Build from Xenopus laevis animal-cap explant (the baseline)",
    "Cut the animal cap from a stage-9/10 blastula with forceps, strip the pigmented outer ectoderm, dissociate the inner layer, pool and reaggregate for 24 h at 14 C.",
    "A ~3,000-cell ciliated spheroid that swims itself along helical trajectories for 10-14 days on maternally provided yolk, with no feeding. It moves itself; it moves external material only as a side effect.",
    "The inner animal-cap layer is pluripotent and differentiates into epidermis including multiciliated cells without further intervention; surface tension makes the default form a sphere.",
    "direct_construct_result", "n/a — this is the substrate",
    "low to the construct; standard amphibian husbandry under IACUC protocol",
    "easy relative to everything else here, and the reason this platform scales",
    ["kriegman21", "blackiston21"]),
  )
A(R("cell-anthrobot-human-airway", "cell",
    "Build from adult human airway epithelial cells (anthrobots)",
    "Culture single adult human lung epithelial cells in extracellular matrix for 2 weeks, then transfer to a minimally viscous habitat.",
    "A 30-500 um ciliated spheroid that self-propels at 5-50 um/s with motility patterns from tight loops to straight lines. It moves itself. Critically for any clinical use it is PATIENT-DERIVED, so it is immunologically self.",
    "Adult somatic cells retain enough plasticity to self-construct a multicellular motile form without genetic editing or manual sculpting; behaviour correlates with the morphology that emerges.",
    "direct_construct_result", "each batch is independent; nothing is edited",
    "low: genetically wild-type autologous cells, no transgene",
    "moderate: a 2-week ECM culture, but no microsurgery and no animal",
    ["gumuskaya23"], study="regime-check",
    note="The commercial argument for this route is immunological, not mechanical: the mechanics are if anything worse than Xenopus (smaller, slower). Its Reynolds number is 1.5e-4 to 2.5e-2, computed in regime-check from these published sizes and speeds."),
  )
A(R("cell-cilia-vs-contractile", "cell",
    "Choose ciliary propulsion over engineered contraction",
    "Leave cilia intact (no Notch ICD) and add no cardiac tissue.",
    "A construct that moves itself with no engineered actuator at all, by surface cilia that arise from normal tissue patterning. It is far easier to make and it has NO gait to design — which also means no gait to optimise for pushing.",
    "Cilia arise through normal tissue patterning, needing no scaffold, microprinting or genomic editing, which is what makes high-throughput production possible.",
    "direct_construct_result", "fully reversible at the design stage",
    "low", "easy",
    ["blackiston21", "kriegman21"],
    note="This is the fork in the road for the whole design space. A ciliary construct is a surface-thrust machine; a cardiac construct is a body-deformation machine. Only the second has anything a gait model can describe, and almost all the published constructs are the first."),
  )
A(R("cell-ciliabot-building-blocks", "cell",
    "Use cilia-inactive modules to place thrust where you want it",
    "Aggregate human airway spheroids into a target shape, substituting CCDC39-mutated (cilia-inactive) spheroids at chosen positions.",
    "A construct whose ACTIVE SURFACE is patterned by construction: thrust where you put working modules, none where you put mutant ones. This is gait design done with tissue rather than with timing, and it needs no actuator control at all.",
    "Ciliary thrust is a surface property, so where the working cilia sit determines the net force and torque on the body.",
    "direct_construct_result", "fixed once aggregated",
    "unknown for the mutant modules; the wild-type aggregation is reported as tolerated",
    "moderate: guided modular aggregation, reported 2025",
    ["bhattaram25", "bhattaram25pre"],
    note="This is the strongest published answer to 'how do you actually choose a gait in a living construct', and it sidesteps the actuation-phase question entirely."),
  )
A(R("cell-transcriptome-drift", "cell",
    "Accept that cells freed from the embryo change what they express",
    "None — this is a property of the substrate you must design around.",
    "A construct whose cells are NOT simply epidermis: at least 537 non-epidermal transcripts are upregulated relative to age-matched embryos, and inter-individual variability is significantly larger. Any mechanical parameter measured on embryonic tissue is therefore a guess about construct tissue.",
    "Removing cells from instructive embryonic signals releases them to explore transcriptional space.",
    "direct_construct_result", "n/a", "n/a",
    "n/a — this is a constraint, not an intervention",
    ["pai25"],
    note="This is the reason every mechanical parameter in every xenobot simulation, including ours, is ASSUMED rather than measured. There is no measured modulus for this tissue in this state."),
  )

# =============================================================== tissue ====
A(R("tis-microcautery-sculpt", "tissue",
    "Impose a shape by microsurgery and cautery",
    "Compress the 24-h spheroid at 2.62 mg/mm for 3 h to a disk, culture 24 h more, then subtract tissue with a 13 um wire cautery electrode and sharpened forceps; allow 1 h to heal.",
    "A construct with an arbitrary non-spherical body plan that is stable for the rest of its life. This is the ONLY published way to put a designed geometry into a xenobot, and geometry is what the whole design pipeline optimises.",
    "The tissue heals over about an hour and the imposed morphology then becomes stable; compression first flattens the disk so it does not rotate out of plane during shaping.",
    "direct_construct_result", "irreversible — tissue is removed",
    "moderate: shaping is subtractive surgery on a living construct",
    "hard and manual; Kriegman et al. call out that some steps 'still require manual intervention'",
    ["kriegman21", "kriegman20"]),
  )
A(R("tis-concavity-limit", "tissue",
    "Respect the 100 um minimum concavity, or the shape closes",
    "When designing, forbid any concave feature narrower than 100 um (about 12% of body length).",
    "A construct whose designed features SURVIVE. Below that width, aggregating stem cells close the gap by tissue contraction and the feature you designed simply is not there in the built object.",
    "Developing stem-cell aggregates tend to close small gaps in their collective geometry; the threshold was found by building progressively smaller deformations and seeing which persisted.",
    "direct_construct_result", "n/a — a design constraint",
    "n/a", "easy to apply, and it is already a filter in the published pipeline",
    ["kriegman20"],
    note="A hard, measured manufacturing limit. Any body plan this design space proposes has to clear it."),
  )
A(R("tis-modular-aggregation", "tissue",
    "Build the shape by aggregating spheroids instead of cutting one",
    "Guide multiple human airway spheroids into contact so they fuse into rod, triangle or diamond shapes.",
    "A construct with a chosen geometry built ADDITIVELY, keeping surface cilia density and inter-module boundary fidelity. Multi-module constructs were reported to move more than single ones.",
    "Spheroids fuse at their contacts while retaining their own surface; the assembled outline is set by where you put them.",
    "direct_construct_result", "fixed once fused",
    "low — no cutting, no cautery",
    "moderate, and far more scalable than microsurgery",
    ["bhattaram25"],
    note="Additive assembly is the obvious route to manufacturability. It is also the only published shape method that does not destroy tissue."),
  )
A(R("tis-self-repair", "tissue",
    "Rely on self-repair rather than on redundancy",
    "None — lacerate a construct and leave it.",
    "A construct that closes its own lacerations and resumes moving. A machine that repairs itself does not need the design margin a synthetic microrobot needs, which is a genuine advantage over every comparator on this page.",
    "The cells retain embryonic wound-healing competence even in a novel configuration.",
    "direct_construct_result", "n/a", "the damage itself is the risk",
    "n/a — it is a property, not a step",
    ["kriegman20", "blackiston21"]),
  )

# ================================================================= body ====
A(R("body-semitorus-mouth", "body",
    "Give the body a C-shaped mouth that captures loose material",
    "Sculpt progenitors into an asymmetric semitorus with a single narrow mouth instead of leaving them spherical.",
    "A construct that GATHERS external particles rather than merely bumping them: dissociated cells are captured, transported and aggregated in the mouth. Offspring diameter rose 149% and replication rounds rose 250% (mean 1.2+-0.4 to 3+-0.8, max 2 to max 4) against spherical progenitors.",
    "A concave mouth converts the construct's own motion into a sweeping volume that collects material, instead of scattering it.",
    "direct_construct_result", "irreversible: sculpted",
    "moderate: microsurgery",
    "hard to build, but it is the single best published geometry for doing work on something else",
    ["kriegman21"], study="cargo-work",
    note="This is the most directly relevant published result on this whole page. The shape was found by evolutionary search in silico and then built and confirmed in vivo, and the measured quantity is EXTERNAL MATERIAL MOVED, not self-locomotion."),
  )
A(R("body-pouch-transport", "body",
    "Exapt a drag-reducing hole into a cargo pouch",
    "Evolve for displacement, keep the designs that develop a hole through the transverse plane, then re-evolve with the pouch as an explicit constraint and the objective changed to carried-object distance.",
    "In SIMULATION, a construct that carries a discrete object. The pouch topology was realised in vivo, but that built organism was never layered with contractile tissue, so no physical xenobot has ever carried a defined cargo.",
    "A hole reduces hydrodynamic drag; the same void can hold an object, so a feature selected for one purpose is reused for another.",
    "model_only", "n/a — design-stage",
    "unknown: never built as a motile cargo carrier",
    "hard — the gap here is manufacturing, not search",
    ["kriegman20"], study="cargo-work",
    note="Read from the full text and worth stating precisely: object TRANSPORT in Kriegman et al. 2020 is in silico only. Object MANIPULATION (debris aggregation) is in vivo. The page must not blur the two."),
  )
A(R("body-travelling-wave", "body",
    "Drive a contractile body with a travelling phase wave rather than a split",
    "Set each actuated voxel's phase to 2*pi*x/L along the travel axis instead of assigning two phases 0 and pi to a front and a back half.",
    "A construct that moves itself AND, uniquely among the six published patterns, keeps moving in the viscous regime a real construct lives in. In our dry-friction reproduction it is the best self-mover (0.364 body lengths in 5 cycles) and the best pusher (transport ratio 0.95 of its own path transferred to the cargo).",
    "A continuous phase gradient makes the stroke non-reciprocal: the shape trajectory encloses area in shape space, so time-reversal symmetry is broken and net motion survives even when inertia does not.",
    "model_only", "n/a — an actuation choice",
    "n/a",
    "the biology is the hard part: no published construct has per-region phase control",
    ["voxart", "purcell77"], study="regime-check",
    note="Our own result. Of the six published patterns this is the only non-reciprocal one; the other five are exactly dead at low Reynolds number."),
  )
A(R("body-two-phase-split", "body",
    "Split the body into two antiphase halves (the published longitudinal gait)",
    "Assign phase 0 to voxels with x < nx/2 and phase pi to the rest.",
    "On a dry floor, a construct that crawls: 0.153 body lengths in 5 cycles, second of six. In water at the scale a real construct occupies, EXACTLY NOTHING. Do not build this.",
    "Two phases 0 and pi mean every voxel's actuation is +/- one scalar in time, so the body's shape sequence retraces itself and the stroke is time-reciprocal. Purcell's scallop theorem then forbids net displacement in Stokes flow.",
    "model_only", "n/a", "n/a",
    "easy to specify, which is exactly why it is a trap",
    ["voxart", "purcell77", "gonzalez09"], study="regime-check",
    note="Our regime-check computes this directly: the control matrix has rank 1 and the enclosed area in shape space is 1.9e-16, machine zero. Four other published patterns (lateral, dorsoventral, checker, uniform) fail in the same way."),
  )
A(R("body-parity-of-the-split", "body",
    "If you do split the body, make the split asymmetric",
    "Choose an odd voxel count along the travel axis so the two actuated halves are unequal (2|3 rather than 2|2).",
    "On a dry floor, 7.6x to 66x more net displacement than an adjacent symmetric split at the same resolution, material, amplitude and duration (median 23x over the 13 adjacent pairs in a sweep of nx = 3 to 16). In the viscous regime, still exactly nothing — asymmetry of LAYOUT does not make a stroke non-reciprocal.",
    "Net translation needs a broken mirror symmetry about the travel axis; an unequal split supplies one, an equal split does not.",
    "model_only", "n/a", "n/a",
    "trivial to specify and easy to get accidentally",
    ["voxart", "voxaudit"], study="convergence",
    note="Our convergence study swept nx = 3..16 and found two smooth monotone branches interleaved by parity, and the mechanism is a single operator: the split is written (x < c.nx/2), and c.nx/2 is C++ INTEGER division, so an even nx splits the body exactly in half and an odd nx cannot. The audit's own three adjacent-pair ratios (7.65, 17.81, 9.25) sit at the low end of the 13 pairs this wider sweep measures. This is the explanation for the 'non-monotone ten-fold swing' the independent audit flagged, and it is an artifact of how the gait was encoded, not a property of the mechanics. The audit's own three adjacent-pair ratios (7.65, 17.81, 9.25) sit at the low end of the 13 pairs this wider sweep measures."),
  )
A(R("body-evolved-geometry-random-actuation", "body",
    "Evolve the geometry to rectify actuation you cannot control",
    "Give contractile cells random fixed phase offsets from a 2 Hz central pattern generator and let evolutionary search change only which voxels exist and which are contractile.",
    "A construct that moves reliably even though its actuator timing is uncontrolled: shape and tissue placement collectively derandomise the motion. Built and verified in vivo — inverting the design 180 degrees significantly reduced displacement both in silico (p<0.001) and in vivo (p<0.0001).",
    "If you cannot impose a phase pattern on living tissue, you can instead select a geometry whose response to ANY phase pattern has a consistent direction.",
    "direct_construct_result", "n/a — design-stage",
    "low", "the search is cheap; the build is the bottleneck",
    ["kriegman20"], study="regime-check",
    note="This is the published approach, and it is a different design problem from the one the voxel-actuation artifact poses. The artifact optimises the phase field with the geometry fixed; Kriegman et al. optimise the geometry with the phase field random."),
  )
A(R("body-size-and-speed", "body",
    "Accept that making it bigger does not make it faster in body lengths",
    "Scale the construct up at fixed lattice spacing and fixed drive frequency.",
    "A construct whose displacement per cycle in body lengths falls smoothly as it gets longer — in our sweep the travelling wave peaks near a 5 cm model body and declines by a factor of three by 15 cm. There is no body length at which it suddenly does better.",
    "The actuation wave carries a fixed number of wavelengths per body, so a longer body moves more mass for the same strain while the drag it must overcome grows faster than the thrust.",
    "model_only", "n/a", "n/a", "n/a",
    ["voxart"], study="convergence",
    note="Our sweep also tested, and rejected, the hypothesis that this is a resonance: the optimum frequency does not scale as 1/L. Longitudinal's optimum sits at 12 Hz for both nx=4 and nx=8, with body length doubling in between."),
  )

# ================================================================ fluid ====
A(R("fluid-reynolds-regime", "fluid",
    "Compute the Reynolds number before trusting any gait model",
    "Take the construct's own size and speed and evaluate Re = rho*U*L/mu in water.",
    "A number that decides which physics applies. For every published construct it is well below 1: anthrobots at 1.5e-4 to 2.5e-2 from their own reported 30-500 um and 5-50 um/s, a nominal 1 mm xenobot at 0.1 mm/s at Re = 0.0996. Inertia is irrelevant; viscosity is everything.",
    "Re is the ratio of inertial to viscous stress. Below 1 the Navier-Stokes nonlinearity drops out and the flow is time-reversible.",
    "direct_construct_result", "n/a — a measurement",
    "n/a", "trivial, and routinely skipped",
    ["gumuskaya23", "purcell77"], study="regime-check",
    note="The voxel-actuation artifact's own body, at its own simulated 50 mm and 12.9 mm/s, would sit at Re = 643 in water. That is 3.8 orders of magnitude from the 1 mm construct. The artifact has no fluid at all, so this is a scale comparison and is labelled as one."),
  )
A(R("fluid-scallop-theorem", "fluid",
    "Make the stroke non-reciprocal, or get exactly zero",
    "Check whether the actuation sequence retraces itself under time reversal. Concretely: write the per-unit drive as sin(wt)*cos(phi) + cos(wt)*sin(phi) and take the rank of that 2xN matrix. Rank 1 means reciprocal.",
    "A pass/fail gate on any proposed gait, before any simulation. A reciprocal stroke produces ZERO net displacement at low Reynolds number no matter how strong, how fast or how clever it is.",
    "In Stokes flow the equations have no time derivative, so reversing the stroke exactly reverses the motion. A stroke that is its own time-reverse must therefore undo whatever it did.",
    "model_only", "n/a — an analysis", "n/a",
    "trivial to apply and it eliminates most candidate gaits immediately",
    ["purcell77", "gonzalez09", "voxart"], study="regime-check",
    note="Applied to the six published patterns this kills five of them. It is the cheapest filter on this page and nothing in the published pipeline applies it."),
  )
A(R("fluid-escape-non-newtonian", "fluid",
    "Escape the scallop theorem by working in a non-Newtonian fluid",
    "Operate the construct in a shear-thickening or shear-thinning medium (mucus, biofilm, a polymer solution) rather than in saline.",
    "A construct whose RECIPROCAL stroke does produce net motion, because the theorem's assumptions no longer hold. Demonstrated with a synthetic single-hinge 'micro-scallop' with measurement, numerics and analysis in agreement.",
    "Net propulsion arises from modulation of the fluid viscosity with shear rate, which breaks the time-reversal symmetry that the theorem needs.",
    "direct_other_species", "fully reversible: it is the medium, not the construct",
    "unknown for living constructs in such media",
    "moderate, and it reframes the whole problem: pick the fluid, not the gait",
    ["qiu14"],
    note="Important caveat on relevance: most biomedically interesting fluids ARE non-Newtonian, so a reciprocal gait is not universally dead. It is dead in the saline the published constructs actually swim in."),
  )
A(R("fluid-escape-body-inertia", "fluid",
    "Escape it instead through the swimmer's own inertia",
    "Make the construct dense relative to the fluid, or give its parts different coasting times.",
    "A construct that swims on a reciprocal stroke even with NO fluid inertia, driven by the inertia of the swimmer itself. Shown theoretically, in simulation and in experiment for a dumbbell with asymmetric coasting times.",
    "Body inertia supplies a second degree of freedom, so the configuration sequence in the combined body-plus-flow state is no longer reciprocal even when the shape sequence is.",
    "direct_other_species", "reversible at design time",
    "unknown for cells, which are close to neutrally buoyant",
    "hard for a living construct: tissue is near the density of water, which is exactly the wrong end of this lever",
    ["gonzalez09", "hubert21"]),
  )
A(R("fluid-intermediate-re", "fluid",
    "Push the construct into the intermediate-Re band where reciprocal strokes start to work",
    "Increase size or beat frequency until the relevant Reynolds number is of order 1 to 10.",
    "A construct for which a simple squeeze-and-release stroke begins to produce measurable net motion. The literature puts the practical floor for jet propulsion around Re = 5: almost all animals using it swim at Re of about 5 or more, and in 2D simulation forward velocity decays rapidly below Re = 10.",
    "With finite inertia the flow no longer reverses exactly when the body does, so the forward and return strokes stop cancelling.",
    "direct_other_species", "reversible: it is an operating point",
    "unknown",
    "very hard here: reaching Re ~ 5 from Re ~ 0.1 means roughly 50x more speed or 7x more size at constant speed",
    ["herschlag11", "lauga07", "jo16"],
    note="The breakdown is continuous rather than a threshold, so there is no single Re at which reciprocal motion switches on. These numbers are where it becomes practically useful, not where it becomes nonzero."),
  )
A(R("fluid-crawling-not-swimming", "fluid",
    "Crawl on a substrate instead of swimming, and the theorem no longer applies",
    "Keep the construct negatively buoyant so its ventral surface stays in contact with the dish.",
    "A construct whose contact friction with the surface can rectify even a reciprocal stroke, because surface friction is not Stokes drag and is outside the theorem's assumptions. This is the regime the published xenobots are actually in: the deciliated organisms 'always kept part of their ventral surfaces in contact with the surface of the dish due to negative buoyancy'.",
    "An anisotropic or load-dependent contact force breaks time-reversal symmetry independently of the fluid.",
    "direct_construct_result", "reversible: adjust buoyancy",
    "low",
    "easy — it is the default, which is why it is easy to forget that it is a choice",
    ["kriegman20", "voxart"], study="regime-check",
    note="This is the strongest limit on our own headline. The scallop-theorem verdict applies cleanly to a free swimmer. A surface crawler is a different problem and the dry-friction model may be qualitatively right about its MECHANISM even though its magnitudes come from an object at Re = 643."),
  )

# ========================================================== design-loop ====
A(R("loop-noise-robustness-filter", "design-loop",
    "Filter designs by robustness to actuation noise before building any of them",
    "Perturb every voxel's phase offset by a normal draw with SD 0.4*pi and keep only designs whose performance survives.",
    "A shortlist of designs that actually work when built. Noise resistance in simulation has been shown to predict whether a design keeps its behaviour in vivo.",
    "A design that depends on precisely timed excitation will not survive contact with tissue whose timing nobody controls; a design robust to scrambled phase is one whose behaviour comes from its mechanics.",
    "direct_construct_result", "n/a — a filter", "n/a",
    "easy and cheap; it is pure extra simulation",
    ["kriegman20"],
    note="Together with the build filter this is the published pipeline's answer to sim-to-real, and it is a behavioural filter rather than a physics fix."),
  )
A(R("loop-hydrodynamics-in-the-sim", "design-loop",
    "Put buoyancy and drag in the simulator, or it will invent gaits that cannot exist",
    "Replace a ground model that lacks buoyancy and drag with an infinite plane submerged in water: reduce effective gravity for buoyancy and apply a drag force to every surface voxel face.",
    "A design pipeline whose outputs are buildable. Kriegman et al.'s first pass, in their words, 'simulated designs on land' and 'resulted in highly performant but nontransferable designs', with 'timeframes (on average, 47% of the gait cycle) in which no part of the in silico design was in contact' with the simulated ground plane. After 'incorporating first-order hydrodynamics', contact with the simulated ground plane rose from 52.7% to 93.3% of the evaluation period.",
    "Without buoyancy and drag the simulated body is far heavier relative to its actuation than the real one, and search exploits ballistic flight that the real construct cannot perform.",
    "direct_construct_result", "n/a — a modelling choice",
    "n/a", "easy, and already done once in the published work",
    ["kriegman20"], study="regime-check",
    note="The single most important source finding on this page, and it is THEIRS rather than ours: the original authors already hit the sim-to-real failure our regime analysis predicts, diagnosed it, and fixed it by moving toward the viscous regime. SEPARATE THEIR CLAIM FROM OUR INFERENCE. They say only that the first pass 'simulated designs on land'; they do not characterise its contact model. What they state is the FIX: 'decreasing the coefficient of gravitational acceleration (increasing buoyancy)' and 'applying a drag force to each voxel face on the design's surface'. That the first pass therefore lacked buoyancy and per-face drag is OUR inference from what was added, not their wording. Also keep two things apart that are easy to merge into one false sentence: the 52.7% -> 93.3% pair is contact with the SIMULATED GROUND PLANE over the evaluation period, while 'the deciliated organisms always kept part of their ventral surfaces in contact with the surface of the dish due to negative buoyancy' is a separate qualitative observation about the REAL organisms, with no percentage attached. The voxel-actuation artifact we re-examined uses full gravity, dry Coulomb friction and no fluid."),
  )
A(R("loop-cilia-as-surface-impulse", "design-loop",
    "Model cilia as a surface impulse, not as a volumetric gait",
    "Apply an impulse force to each SURFACE voxel in the horizontal plane, standing in for the aggregate metachronal wave, and lock vertical moments in plane.",
    "A simulation that matches what cilia-driven constructs actually do. This is how the self-replication work modelled its organisms, and it means the whole six-gait volumetric-actuation question does not describe a cilia-driven xenobot at all.",
    "Cilia act at the surface and produce thrust directly; they do not deform the body, so a bulk strain field is the wrong abstraction for them.",
    "direct_construct_result", "n/a — a modelling choice", "n/a",
    "easy, and it is what the field already does",
    ["kriegman21"], study="regime-check",
    note="Read from Kriegman et al. 2021's Materials and Methods. Combined with the previous route this means the voxel-actuation gait comparison is about the 2020 cardiac-driven constructs, not the 2021 cilia-driven ones, and the page should say which."),
  )
A(R("loop-tuned-for-stability-not-measured", "design-loop",
    "Know that the material parameters in these simulations are tuned, not measured",
    "None — read the methods.",
    "A calibrated expectation of how much any of these numbers mean. Kriegman et al. 2021 state that voxels were 'simulated with material properties manually tuned to allow for the largest stable time step of numerical integration'.",
    "Explicit integrators are stable only below a timestep set by the stiffest element, so there is pressure to choose stiffness for numerical reasons rather than physical ones.",
    "direct_construct_result", "n/a", "n/a", "n/a",
    ["kriegman21", "pai25"], study="regime-check",
    note="Our own model inherits exactly this problem and says so: every mechanical parameter in regime-check, convergence and cargo-work is marked assumed, not sourced."),
  )
A(R("loop-grid-convergence", "design-loop",
    "Refine the grid on a parity-matched series, or you measure your own encoding",
    "Hold the outer envelope and the PHYSICAL actuation field fixed while halving the lattice spacing, instead of refining a split defined by voxel index.",
    "A refinement series that measures discretisation error rather than a change of design. The published artifact refined nx 5 -> 10, which moved the actuation split from 20 mm to 25 mm and flipped its parity at the same time, and reported an 8.2x change.",
    "An actuation field defined on lattice indices is a different physical field on a different lattice, so refining the grid silently changes the experiment.",
    "model_only", "n/a — a methodological fix", "n/a",
    "easy once seen, and it was invisible to two review rounds",
    ["voxart", "voxaudit"], study="convergence"),
  )

# =========================================================== collective ====
A(R("coll-kinematic-self-replication", "collective",
    "Let a swarm build its own successors out of loose cells",
    "Place 12 mature ciliated spheroids in a 60 mm dish among ~60,000 dissociated stem cells at 25-150 cells/mm2 and leave them 20 h at 20 C.",
    "A swarm that pushes loose cells into piles; piles of at least 50 cells mature into new motile spheroids. This is the published system doing mechanical work on external material, and the material happens to be more of itself.",
    "Collective motion compresses dissociated cells into aggregates that then adhere, compact and differentiate on their own over about 5 days.",
    "direct_construct_result", "the organisms are discarded; the behaviour is not installed",
    "the system halts on its own: 4 of 5 trials gave one generation, 1 gave two, and offspring shrink until they cannot mature",
    "moderate for one round; the limit is contamination and feedstock, not difficulty",
    ["kriegman21"], study="cargo-work",
    note="The negative control is reported and matters: with no progenitor organisms present, no offspring self-assembled at any cell concentration tested. The piling is done by the swarm, not by fluid dynamics or self-assembly."),
  )
A(R("coll-swarm-size", "collective",
    "Add more constructs and ask what actually scales",
    "Place N constructs in a fixed field of loose particles and vary N.",
    "In our model, a swarm that moves MORE total material as N rises but does not aggregate it: the particle field's radius of gyration increases at every swarm size and every random seed we ran. A uniform swarm with no sensing and no differentiated roles sweeps; it does not corral.",
    "Every construct runs the same gait and travels the same way, so their effects add as a common drift rather than converging on a point. Corralling needs either a concave body that traps material or constructs that move differently from one another.",
    "model_only", "n/a", "n/a", "n/a",
    ["voxart", "kriegman21"], study="cargo-work",
    note="An honest negative from our own work. It is also the mechanistic reason the semitorus matters: the mouth, not the swarm, is what turns sweeping into gathering."),
  )
A(R("coll-emergent-entanglement", "collective",
    "Expect constructs to stick to each other, especially if ciliated",
    "Put several constructs in one dish.",
    "A swarm whose members collide, form temporary mechanical bonds and orbit each other before separating tangentially; with cilia intact they frequently become entangled and swap partners. Predicted in silico and observed in vivo.",
    "Surface cilia and tissue adhesion give unintended attractive interactions that no design specified.",
    "direct_construct_result", "n/a", "low",
    "n/a — it happens whether you want it or not",
    ["kriegman20", "blackiston21"]),
  )
A(R("coll-evolve-the-terrain", "collective",
    "Design the arena instead of the organism",
    "Evolve the placement of walls on the dish floor, leaving the progenitors as wild-type spheroids.",
    "In SIMULATION, wild-type spheroids achieving significantly more replication rounds than on a flat surface (p<0.0001), and in a cluttered environment the search found shapes that lift the organism above the clutter.",
    "Walls constrain otherwise stochastic trajectories into more predictable paths, which concentrates the material the swarm sweeps.",
    "model_only", "fully reversible — it is the container",
    "none to the construct",
    "easy compared with sculpting tissue, and it is the cheapest unexploited lever here",
    ["kriegman21"],
    note="Not demonstrated in vivo. But of everything on this page it is the intervention with the best ratio of expected effect to manufacturing difficulty."),
  )

# ========================================================== application ====
A(R("app-debris-aggregation", "application",
    "Clear particulate matter from a surface",
    "Strew the environment with particulate matter and release motile constructs for 24 h.",
    "Constructs that spontaneously aggregate external objects, shown both in silico and in vivo, individually and in groups. This is the one application on the ladder that is OBSERVED rather than simulated.",
    "A moving body sweeps a volume; adhesive or settled particles are pushed along and accumulate where trajectories converge.",
    "direct_construct_result", "n/a", "low",
    "easy — it is emergent and needs no extra design",
    ["kriegman20", "kriegman21"], study="cargo-work",
    note="Note the honest limit: aggregation here is a SIDE EFFECT of locomotion, the authors' own phrasing. Nothing published targets a particular pile location or a particular particle."),
  )
A(R("app-directed-push", "application",
    "Push a defined object in a chosen direction",
    "Place a discrete cargo in the construct's path and let it drive into it.",
    "In our model, real transport: the travelling-wave construct transfers 95% of its own path length to an 8 g cargo and does 3.3% of its actuation energy as useful work against floor friction. The two-phase gaits transfer 51% and 26%. No published physical xenobot has done this.",
    "A construct in sustained contact with a sliding object does work against the object's friction; how much depends on how steadily the gait maintains contact force.",
    "model_only", "n/a", "n/a",
    "hard: it needs both a controllable gait and a placement method, neither of which exists in vivo",
    ["voxart", "kriegman20"], study="cargo-work",
    note="Our predeclared expectation was that the best self-mover would NOT be the best pusher. It was wrong: travelling wins on cargo displacement, on transport ratio and on efficiency. We report that as a failed prediction."),
  )
A(R("app-heavy-cargo-efficiency", "application",
    "Carry the heaviest load that still moves, not the lightest",
    "Increase cargo mass at fixed volume and watch efficiency rather than speed.",
    "In our model, a construct whose ENERGY efficiency rises with cargo mass — 0.8% at 2 g to 8.2% at 32 g, while cargo displacement falls only from 107 mm to 78 mm, and then stalls: at 64 g transport collapses 17-fold to 4.6 mm. The intuition that a lighter payload is better is backwards for useful work.",
    "Friction work scales with mass while the construct's displacement is set by its gait, so until the cargo stalls the construct it is nearly free to make the load heavier.",
    "model_only", "n/a", "n/a", "n/a",
    ["voxart"], study="cargo-work",
    note="All three contacting gaits stall between 32 g and 64 g, so the threshold is a property of the actuation strength rather than of the gait. Caution on the metric: our declared efficiency uses the cargo's PATH length, so past the stall it RISES spuriously - 13.4% at 256 g while the cargo moves 0.1 mm. The net-displacement version falls to 0.08% there, which is the honest number."),
  )
A(R("app-exponential-utility", "application",
    "Let replication multiply the work, not just the machines",
    "Deploy self-replicating progenitors into an environment containing both feedstock cells and the objects to be worked on.",
    "In SIMULATION, utility rising quadratically with time: a swarm closing microcircuits as a side effect of movement, fitted as 2.7x^2 - 43x + 182.4 with R^2 = 0.9988 over 50 simulation bifurcations and 5,024 light emitters switched on.",
    "If replicators perform useful work while replicating, and feedstock is available, utility compounds from a small initial investment.",
    "model_only", "n/a",
    "this is the route where containment matters most",
    "very hard: it needs self-replication, a task, and feedstock all at once, and replication currently halts after 2-4 rounds",
    ["kriegman21"],
    note="The authors are explicit that this is a forecast from a computational model and 'may not be achievable'. It is on this page as the commercial argument, labelled as a simulation."),
  )
A(R("app-neural-sheet-repair", "application",
    "Use the construct's traversal itself as the therapy",
    "Place anthrobots on a scratched sheet of cultured human neurons.",
    "Constructs that traverse the scratch and induce rapid repair of it in vitro. The useful work is done by being there and moving, not by carrying anything.",
    "Reported as a capability of the construct; the mechanism is not established in the source.",
    "direct_construct_result", "n/a",
    "autologous cells, so the immunological risk is low by construction",
    "moderate in vitro; everything about in vivo delivery is unaddressed",
    ["gumuskaya23"],
    note="This is the only route on the page with a stated biomedical endpoint and a patient-derived construct. It is in vitro."),
  )

# ============================================================ lifecycle ====
A(R("life-yolk-limited-lifespan", "lifecycle",
    "Rely on the yolk running out as the off switch",
    "None — build the construct and deploy it.",
    "A construct that moves for 10-14 days on maternally provided energy stores and then sheds cells and deteriorates. Containment is a property of the material rather than a system you have to build.",
    "The explant carries only the yolk it was made with and has no feeding apparatus, so it cannot persist.",
    "direct_construct_result", "n/a — it is the default",
    "this IS the safety feature; the risk is that it is also the operating limit",
    "n/a",
    ["kriegman21", "kriegman20"]),
  )
A(R("life-replication-halts", "lifecycle",
    "Count on replication halting on its own, and know how many rounds you get",
    "None — observe the generations.",
    "A self-replicating swarm that stops: spheroid progenitors managed a mean of 1.2+-0.4 generations and semitoroids 3+-0.8, maximum 4, with offspring shrinking each round until they are too small to mature. Replication can also be stopped deliberately by withholding dissociated cells.",
    "Each generation gathers less material than the last, so offspring size falls below the ~50-cell threshold needed to become motile.",
    "direct_construct_result", "n/a",
    "low: the authors note the design is intended to be maximally controllable",
    "n/a",
    ["kriegman21", "levin20"],
    note="The AI-designed shape that makes the system work better also makes it halt later. Capability and containment are the same knob here, turned in opposite directions."),
  )
A(R("life-no-genomic-edit", "lifecycle",
    "Keep the genome wild-type so there is nothing heritable to escape",
    "Build by reconfiguration and sculpting rather than by transgene or refactored genome.",
    "A construct with no engineered genetic material at all. Whatever it does is a property of its arrangement, which does not propagate into any organism it meets.",
    "Morphological reconfiguration redirects self-organising processes without genomic editing or transgenes.",
    "direct_construct_result", "n/a", "low — this is the containment argument",
    "easy: it is the platform's default and a deliberate design commitment",
    ["kriegman21", "blackiston23", "levin20"],
    note="The Notch ICD and tdTomato routes DO use injected mRNA, so a construct built for a designed contractile gait is not wild-type in the sense this route claims. The two are in tension and the page should say so."),
  )

# =========================================================== comparator ====
A(R("cmp-magnetic-microrobot", "comparator",
    "Use an externally driven magnetic microrobot instead",
    "Fabricate a magnetic micro-structure and drive it with an external rotating or oscillating field.",
    "A machine you can steer, that needs no feeding, that works in any fluid you can put a field around, and that stops when you turn the field off. For most mechanical tasks at this scale this wins today, and a funder will ask why it does not.",
    "External field supply means the energy and the control both come from outside, so the device itself can be simple and does not need to live.",
    "direct_other_species", "fully reversible: switch the field off",
    "not biodegradable; retrieval is the problem instead",
    "mature as a research field; a large literature of reviews and devices",
    ["chen18", "ghosh20", "yin19"],
    note="This is the honest alternative. The living construct's advantages are narrow and specific: self-repair, biodegradation, patient-derived immunological self, and self-replication. Not steering, not force, not speed, not reliability."),
  )
A(R("cmp-microrobot-swarm-capture", "comparator",
    "Use a synthetic swarm that actually captures and aggregates",
    "Self-assemble magnetic beads into rotating planes under an external field and drive them through the medium.",
    "A swarm that actively captures free-swimming bacteria and dispersed microplastics on the fly and can be collected afterwards. This is the corral-and-aggregate application, delivered, with a retrieval story.",
    "The assembled rotating plane both generates propulsion and presents a sequestering surface; plane size modulates propulsion speed.",
    "direct_other_species", "reversible: the assembly is field-dependent",
    "n/a", "demonstrated 2024",
    ["ussia24", "ceron23"], study="cargo-work",
    note="Directly comparable to this page's swarm study and ahead of it. Ceron et al. additionally show heterogeneous collectives caging or expelling passive objects, which is the corralling behaviour our uniform swarm does not produce."),
  )
A(R("cmp-acoustic-manipulation", "comparator",
    "Move the particles directly with sound and skip the robot",
    "Use acoustic radiation forces to trap and translate the target particles.",
    "Contactless manipulation of the objects themselves. If the task is only to move particles from A to B in a container you control, a machine may not be needed at all.",
    "Acoustic radiation force acts on any object with an impedance mismatch, with no onboard actuator.",
    "direct_other_species", "fully reversible", "n/a",
    "mature; reviewed extensively",
    ["mohanty20", "cao24"],
    note="The sharpest framing question for the whole design space: for a task in a controllable container, a field beats a robot. The living construct's case has to rest on environments you cannot put a transducer around."),
  )
A(R("cmp-muscle-biohybrid", "comparator",
    "Use an engineered muscle actuator on a printed skeleton",
    "Culture an engineered skeletal-muscle strip on a 3D-printed hydrogel skeleton with an asymmetric design, or on a serpentine spring that self-stimulates during maturation.",
    "A biohybrid machine with a DESIGNED, controllable actuator: optogenetic skeletal muscle giving up to 300 uN of active tension and 310 um/s of locomotion, or a cardiomyocyte-driven filament swimmer at 5-10 um/s, 81 um/s with two tails.",
    "A synthetic skeleton supplies the geometry and the restoring force while living muscle supplies the actuation, so each part does what it is good at.",
    "direct_other_species", "the construct is built, not edited",
    "requires mammalian cell culture and a scaffold",
    "hard, but the actuator is genuinely controllable, which no xenobot's is",
    ["cvetkovic14", "raman16", "guix21", "williams14"],
    note="This is the closest comparator to a designed-gait xenobot, and it is ahead on exactly the axis this design space cares about: you can command the actuator. Williams et al. 2014 is explicitly a low-Reynolds-number swimmer with a slender-body model, so it is also the right physics."),
  )
A(R("cmp-bacteria-sperm-propelled", "comparator",
    "Bolt a cargo onto something that already swims well",
    "Attach a drug-loaded particle or droplet to motile bacteria or to a single sperm cell.",
    "A cargo carrier that inherits a propulsion system already optimised by evolution for exactly this Reynolds number, with no gait to design at all.",
    "Flagellar propulsion is non-reciprocal by construction, so the scallop theorem is satisfied without any engineering.",
    "direct_other_species", "n/a",
    "a live motile organism as a vehicle raises its own containment questions",
    "moderate; several demonstrated systems",
    ["xu17", "singh17"],
    note="Worth stating plainly: this comparator solves the problem this page spends its first study on, by never creating it."),
  )
A(R("cmp-catalytic-micromotor", "comparator",
    "Let chemistry do the propulsion",
    "Use a catalytic Janus particle or tubular micromotor that converts a dissolved fuel into motion.",
    "A self-propelled carrier with no external field and no living tissue, able to assemble into chains that pick up and transport microscale objects including yeast cells.",
    "Asymmetric catalysis produces a local gradient that drives the particle, continuously and non-reciprocally.",
    "direct_other_species", "stops when the fuel runs out",
    "the fuel is usually peroxide, which is not biocompatible",
    "mature chemistry; biocompatibility is the open problem",
    ["sanchez14", "peng22", "gao13", "mou19"]),
  )

# ------------------------------------------------------------- assemble ---
SCALES = [
    {"key": "molecular", "label": "Molecular · adhesion, cilia and contractility",
     "blurb": "What the cells are told to become. At this scale you choose whether the construct will have a propulsion system at all, and which one."},
    {"key": "cell", "label": "Cell · sourcing and power source",
     "blurb": "Which cells, from which organism, driven by what. The fork between ciliary surface thrust and contractile body deformation is made here, and it decides whether a gait model is even the right abstraction."},
    {"key": "tissue", "label": "Tissue · shape imposition and self-assembly",
     "blurb": "How a designed geometry gets into a living object. Every shape on this page has to survive a 100 um minimum feature size and an hour of healing."},
    {"key": "body", "label": "Body plan · geometry and actuation pattern",
     "blurb": "The design variables the published optimisation loop actually searches. This is where our three studies push hardest."},
    {"key": "fluid", "label": "Fluid · the regime the construct actually lives in",
     "blurb": "A millimetre-scale construct in water sits at Reynolds number well below 1. That single number decides which gaits can work at all, and it is the scale most of this literature's simulations are not in."},
    {"key": "design-loop", "label": "Design loop · search and sim-to-real transfer",
     "blurb": "The pipeline that turns a goal into a built organism — and the place where this page's own subject, the gap between the simulator and the dish, lives."},
    {"key": "collective", "label": "Collective · swarms and self-replication",
     "blurb": "What changes when there is more than one. Including the one published result where constructs demonstrably rearrange their environment."},
    {"key": "application", "label": "Application · work on an external object",
     "blurb": "The ladder this page is about: corral loose particles, then transport a defined cargo, then aggregate a dispersed field with a swarm."},
    {"key": "lifecycle", "label": "Lifecycle · lifetime, degradation and containment",
     "blurb": "These constructs stop on their own. That is both the safety case and the operating limit, and they are the same property."},
    {"key": "comparator", "label": "Comparator · synthetic microrobots",
     "blurb": "The alternative a funder will raise. For most tasks at this scale it wins today, and the living construct's case has to be made on the narrow axes where it does not."},
]

OUTCOME_CLASSES = [
        {"key": "moves-itself", "label": "Moves itself only",
         "match": "moves itself|self-propel|locomot|crawl|swim|motil|propulsion|thrust|net motion|net displacement|displacement"},
        {"key": "moves-something", "label": "Moves something else",
         "match": "push|carri|cargo|transport|corral|aggregat|manipulat|debris|particle|pile|sweep|captur|gather|repair|traverse|work on"},
        {"key": "changes-form", "label": "Changes its own form",
         "match": "shape|morpholog|geometr|sculpt|topolog|assembl|fuse|body plan|concav"},
        {"key": "enables", "label": "Makes the others possible",
         "match": "filter|predict|calibrat|design|search|shortlist|simulat|number that decides|pass/fail|expectation|rectif|transcript|calibrated|is a guess|constraint|survive"},
        {"key": "bounds-risk", "label": "Bounds the risk",
         "match": "lifespan|lifetime|degrad|contain|halt|stops|off switch|wild-type|generations|genetic material|genome|deteriorat"}]

OUT = {
    "schema": "design-space-routes-0.1",
    "title": "A biological machine that does work on something other than itself",
    "subtitle": "What body plan and actuation pattern lets a millimetre-scale living construct push, carry, corral or aggregate an external object?",
    "scales": SCALES,
    "evidence_labels": {
        "direct_construct_result": "direct xenobot / anthrobot result",
        "direct_other_species": "direct result, another system",
        "model_only": "model or simulation only",
        "proposed": "proposed — no source bears on it"},
    "outcome_filter_label": "What it would do",
    "outcome_classes": [
        {"key": "moves-itself", "label": "Moves itself only",
         "match": "moves itself|self-propel|locomot|crawl|swim|motil|propulsion|thrust|net motion|net displacement|displacement"},
        {"key": "moves-something", "label": "Moves something else",
         "match": "push|carri|cargo|transport|corral|aggregat|manipulat|debris|particle|pile|sweep|captur|gather|repair|traverse|work on"},
        {"key": "changes-form", "label": "Changes its own form",
         "match": "shape|morpholog|geometr|sculpt|topolog|assembl|fuse|body plan|concav"},
        {"key": "enables", "label": "Makes the others possible",
         "match": "filter|predict|calibrat|design|search|shortlist|simulat|number that decides|pass/fail|expectation|rectif|transcript|calibrated|is a guess|constraint|survive"},
        {"key": "bounds-risk", "label": "Bounds the risk",
         "match": "lifespan|lifetime|degrad|contain|halt|stops|off switch|wild-type|generations|genetic material|genome|deteriorat"}],
    "routes": ROUTES,
    "recommendation": {
        "single_best_route": "body-semitorus-mouth",
        "Why this one": "It is the only body plan in this whole space that has been computationally designed, physically built, and then MEASURED on external material moved rather than on self-locomotion. Sculpting progenitors into an asymmetric semitorus with a narrow mouth raised offspring diameter by 149% and replication rounds by 250% over spherical progenitors, because the mouth captures, transports and aggregates loose cells. It is also cilia-driven, so it never has to solve the actuation problem that kills most of this page's alternatives.",
        "What it buys you that a gait does not": "A concave mouth converts locomotion into gathering through GEOMETRY. It needs no per-region phase control, no actuator timing, and no contractile tissue graft \u2014 none of which exist in a controllable form in any living construct today. The construct just has to move; the shape does the work.",
        "The gait question is the wrong question, and that is this page's main finding": "The published six-gait comparison asks which spatial actuation phase pattern moves a soft body furthest. In the regime a real millimetre-scale construct occupies \u2014 Reynolds number below 0.1 \u2014 five of those six patterns produce EXACTLY ZERO net displacement, because they assign only the phases 0 and pi and so retrace their own stroke. The live design question is not 'which gait ranks highest' but 'is this gait non-reciprocal at all', which is a yes/no test you can run on paper in a minute.",
        "What to build next, in order": "1. Replicate the semitorus and measure particle clearance with a declared metric, not as a side effect. 2. Apply the rank test to any proposed actuation pattern before simulating it. 3. If you simulate, put buoyancy and drag in \u2014 Kriegman et al. already found and fixed this failure once, and the artifact we re-examined uses the physics they abandoned. 4. Evolve the ARENA (coll-evolve-the-terrain): it is the cheapest unexploited lever here and needs no new biology.",
        "The honest commercial position": "For most mechanical tasks at this scale a magnetically or acoustically driven synthetic device wins today on steering, force, speed and reliability, and a synthetic swarm has already been shown capturing bacteria and microplastics on the fly with a retrieval story. The living construct's case rests on four narrow axes and should be argued only on those: self-repair, biodegradation and a yolk-limited lifespan as built-in containment, patient-derived immunological self (anthrobots), and kinematic self-replication. Nothing else on the comparator scale offers any of them.",
        "Runner-up": "cell-ciliabot-building-blocks \u2014 placing cilia-inactive modules to pattern thrust by construction is gait design done with tissue instead of with timing, and it is the most manufacturable idea on this page."},
    "welfare": {
        "Animal use": "The Xenopus routes require fertilised Xenopus laevis eggs and embryos harvested at blastula stage. The source papers record institutional approval: Kriegman et al. 2020 under Tufts IACUC protocol M2017-53, Kriegman et al. 2021 under M2020-35. Shaping is subtractive surgery \u2014 microcautery with a 13 um wire electrode \u2014 performed on tissue explanted before a nervous system exists.",
        "The anthrobot route avoids animals entirely": "Anthrobots are built from adult human lung epithelial cells and need no animal, no embryo and no genetic editing. If a programme can be run on that substrate, the animal-use question largely disappears. This is a substantive welfare argument for the human route and not only a commercial one.",
        "Moral status of the constructs themselves": "These constructs have no nervous system and are not sentient on any account we are aware of. They are nonetheless novel self-organising entities with behaviours absent from the donor organism, and the field itself has raised the question rather than dismissed it. We flag it and do not resolve it.",
        "Containment": "Lifespan is bounded by maternally provided yolk at 10\u201314 days with no feeding, replication halts after 2\u20134 rounds on its own, and the genome is unmodified in the baseline routes \u2014 so there is no heritable engineered material to escape. Two caveats we will not paper over: the contractile-gait route DOES inject mRNA (Notch ICD and a lineage tracer), so a designed-gait construct is not wild-type in the sense the containment argument assumes; and the AI-designed shape that makes replication useful is the same knob that makes it halt later.",
        "What this page does not address": "Any in vivo deployment. Every route here is a dish, a culture or a simulation. Delivery, biodistribution, immune response in a real body and environmental release are all out of scope and none of our studies bear on them."},
    "limitations": [
        "Our three studies are SIMULATIONS. No organism, tissue or cell was measured for this page. Every mechanical parameter in them is marked assumed, not sourced, and the same is true of the published simulations they re-examine \u2014 Kriegman et al. 2021 state their voxel material properties were 'manually tuned to allow for the largest stable time step of numerical integration'.",
        "The scallop-theorem result applies cleanly to a FREE SWIMMER. A xenobot crawling on a dish bottom, negatively buoyant with its ventral surface in contact, is not one: contact friction is not Stokes drag and is outside the theorem's assumptions, so a reciprocal gait can rectify against a surface. The defensible claim is that the published ranking is void for a free or near-neutrally-buoyant construct, and that for a crawler its magnitudes come from an object 3.8 orders of magnitude away in Reynolds number.",
        "Cilia-driven propulsion is not body-deformation swimming, and most published constructs are cilia-driven. The scallop theorem still constrains the cilium's own stroke, but a surface-thrust machine has no body gait for our analysis to rank. Our regime result therefore bears directly on the 2020 cardiac-driven constructs and only indirectly on the 2021 cilia-driven ones.",
        "Our Stokes swimmer is a Rotne-Prager-Yamakawa bead model over shapes from a quasi-static central-force spring lattice. That lattice obeys the Cauchy relations, so its Poisson ratio is a property of the spring topology rather than an input: we measure 0.20 against the artifact's 0.35, and its axial and bending effective moduli differ by about a factor of two. We use it only to generate a shape, and we report that the Stokes ranking shifts by under 1% across a 4x change in its stiffness ratio.",
        "The five reciprocal gaits do not come back as literally zero but as 1e-7 to 1e-8 body lengths per cycle, which is the numerical residue of an iterative shape solve. We establish that by refinement rather than assertion \u2014 tightening the solve drops those values by four orders while the travelling wave holds to four significant figures \u2014 and their relative order must not be read as a ranking.",
        "The cargo and swarm studies are in the dry-friction regime, matching the artifact they extend, NOT the viscous regime our own first study says the real object occupies. They answer 'does the best self-mover also push best' within that model and nowhere else.",
        "Our swarm has no sensing, no communication and no differentiated roles, and every member runs the same gait. Its failure to aggregate is a statement about that swarm, not about swarms.",
        "Read-levels are stated per source and most are 'listing' \u2014 citation record retrieved and verified from PubMed, abstract not read by us. Only Kriegman et al. 2020 and 2021 were read in full text. Four physics citations (Purcell 1977, Najafi & Golestanian 2004, Lauga 2007, Lauga & Powers 2009) are not indexed in PubMed and are labelled search-summary: their volume, page and DOI details were NOT independently verified by us.",
        "Scope of the negative on the application question: searching PubMed and Consensus for a xenobot or anthrobot deliberately transporting a defined external cargo found nothing. What exists is debris and particle AGGREGATION as a reported side effect of locomotion, plus object transport in silico only. bioRxiv was not searched by keyword.",
        "voxcraft-sim, the GPU engine this literature actually uses, does NOT build at its pin against a modern toolkit. We ran the probe on an NVIDIA L40S in nvidia/cuda:12.4.1-devel-ubuntu22.04: both arms configured cleanly and both failed to compile, because the code calls cudaDeviceSynchronize() from __device__ functions (removed in CUDA 12, seven sites) and because nvcc cannot compile Boost.Asio's trait machinery reached through boost::process. No cross-engine comparison is offered anywhere here. We tested one toolkit on one platform; the pinned CUDA 10.2 route was not attempted. Receipt: data/voxcraft-probe.json."],
}

# The brief requires every route to carry a verified PMID or DOI, or to state
# explicitly that no source bears on it. Four routes rest only on this page's own
# simulation, which has neither by nature. Mark them rather than leave it implied.
for _r in ROUTES:
    if not any(("pmid" in _e or "doi" in _e) for _e in _r["evidence"]):
        _r["external_source"] = ("NONE. This route rests only on this page's own simulation and on "
                                 "the delphi-frontier artifact it re-examines. No published source "
                                 "bears on it, and it carries no PMID or DOI for that reason.")

import re as _re2
_un = [r["id"] for r in ROUTES
       if not any(_re2.search(oc["match"], r["predicted_phenotype"], _re2.I)
                  for oc in OUTCOME_CLASSES)]
assert not _un, ("routes invisible to the outcome filter", _un)

print(f"{len(ROUTES)} routes across {len({r['scale'] for r in ROUTES})} scales")
print("routes resting only on our own work:",
      [r["id"] for r in ROUTES if "external_source" in r])
from collections import Counter
print(Counter(r["scale"] for r in ROUTES))
print(Counter(r["evidence_strength"] for r in ROUTES))
missing = [r["id"] for r in ROUTES if not r["evidence"]]
assert not missing, missing
declared = {s["key"] for s in SCALES}
bad = {r["scale"] for r in ROUTES} - declared
assert not bad, bad
with open("/data/scratch/designspaces/xenobot/routes.json", "w") as f:
    json.dump(OUT, f, indent=2)
print("wrote routes.json")
