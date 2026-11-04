# Claim 30: what it entails at the DNA and cell scales, and what the checks found

**Source claim (protein scale, evidence: derived):** Tyrosine spatial clustering is significant
in and2 (0.393 observed vs 0.211 shuffled, z = 2.74, p = 0.011) but not in and1 (p = 0.064,
where Tyr content alone explains most of it). The kcnk5b control gives p = 0.72.

**Animal:** zebrafish (*Danio rerio*) on the claim side. Every check below names the animal its
number comes from. None of the evidence used here comes from flying fish (Exocoetidae), and no
check depends on an exocoetid number. See §4.

Date: 2026-11-04. All web sources were reached through Europe PMC, UniProt REST or publisher
pages. `ruor.uottawa.ca` (theses) was blocked by this session's network policy, and Nature's
full text needs a login, so both are marked *could-not-access* where they matter.

---

## 0. First, what the claim actually measures (reconstructed, derived)

The claim's analysis code and records are **not in this repository**. I searched both branches
for `tyrosine`, `kcnk5b`, `clustering` and `actinodin` and found nothing relevant. I therefore
rebuilt a statistic that reproduces the reported numbers:

- **Statistic:** of all pairs of consecutive Tyr residues, the fraction whose gap is ≤ 4 residues.
- **Null:** the same full-length precursor sequence, randomly permuted 2,000 times.
- **Input:** UniProt A9JRX1 / A0ACM8QEN9 (and2, 508 aa), E7F5V5 (and1, 570 aa), Q6PFU3 /
  A0A8M1PBI1 (kcnk5b, 448 aa). All are *Danio rerio*. Read level: listing.

| protein | Tyr | observed | shuffled mean | z | p (empirical) |
|---|---|---|---|---|---|
| and2 | 29 | 0.393 | 0.211 | 2.74 | 0.010 |
| and1 | 47 | 0.391 | 0.293 | 1.72 | 0.064 |
| kcnk5b | 12 | 0.091 | 0.102 | −0.13 | 0.717 |

*(my calculation; script: `docs/research/fish/claim-30-tyr-gap-test.py`, seed 1)*

This matches the claim to three decimals, so I am fairly sure this is the metric used. I can't
confirm it is the same pipeline. Three facts from the same calculation set the scope of
everything below:

- 0.393 is 11 of 28 gaps. That is a small count.
- The result depends on the window. With k = 3, p = 0.018. With k = 5, p = 0.054. With k = 1 or
  2 it is not significant. I don't know whether k = 4 was fixed in advance.
- If the signal peptide (residues 1–23, a SignalP prediction in UniProt) is removed, and2 still
  gives p = 0.016. With 20,000 permutations, and2 gives p = 0.0101 and and1 gives p = 0.062.

---

## 1. Entailment: what the claim requires at the adjacent scales

Taken literally, the claim is a statistic about a sequence. It requires something at the DNA
scale directly. It requires something at the cell scale only once you read it the way it is
meant to be used: the clustering matters *because* And2 is a secreted structural protein of the
actinotrichia. I label each constraint **[literal]** or **[functional reading]**.

Why there are no timescale, energetic or conservation-of-mass constraints: a permutation
statistic on a primary sequence says nothing about rates, power or mass balance. I could not
derive one honestly. Inventing one (for example, "Tyr crosslinking must be faster than fibre
assembly") would turn a guess about mechanism into a requirement, and that is the error this
format exists to prevent.

| # | scale | kind | requirement (stated generically) | basis |
|---|---|---|---|---|
| C1 | dna | existence | The Tyr arrangement must be encoded by the real zebrafish *and2* locus. At least one independently sequenced transcript must give the same product as the analysed model, not just one gene prediction. | literal |
| C2 | dna | range | If the clustering is a heritable sequence feature and not an accident of one sequence, it must recur in *and2* orthologs. Under the same statistic, most teleost *and2* orthologs should have z ≥ 2 (lo = 2). *and1* and the control should not show this as consistently. | literal (the "not a fluke" reading) |
| C3 | cell | existence | A zebrafish cell type must make the protein and send it out of the cell into the subepidermal matrix where actinotrichia form. A Tyr arrangement on a protein that never leaves the cell, or never reaches the fibre, has no structural meaning. | functional reading |
| C4 | cell | existence | If and2's clustered-Tyr region does something that and1 (with unclustered Tyr) cannot, then losing that region of *and2* alone must produce a detectable fin-fold or actinotrichia phenotype at the cell or tissue level, even with *and1* still present. | functional reading |

---

## 2. Checks

### C1 (dna, existence): **satisfied**

- UniProt A9JRX1 is translated from EMBL **BC155829** (protein AAI55830.1), a zebrafish cDNA
  clone (MGC, "zgc:175106"). Its listed evidence is "Evidence at transcript level". The RefSeq
  gene model **NM_001111190.1 / NP_001104660.1** (UniProt A0ACM8QEN9, "Evidence at protein
  level") gives the **identical** 508-aa sequence. I checked this by string comparison. Read
  level: listing (UniProt cross-references).
- **Hanzelova et al. 2026**, *Development* 153:dev204990 (doi 10.1242/dev.204990, PMC13120675;
  read level: full-text, keyword-searched). The authors made a 269-bp CRISPR deletion in
  zebrafish *and2* and confirmed expression by in situ hybridisation. So the locus is real and
  transcribed in fin folds.
- **Caveat:** I didn't confirm that NM_001111190.1 is independent of BC155829. A RefSeq record
  can be built from that same cDNA. The cDNA alone still counts as a measured transcript. I didn't
  compare the cDNA against the GRCz11 genomic sequence, because the Ensembl REST API returned
  HTTP 403 through this session's proxy.
- **Animal:** zebrafish on both sides.

### C2 (dna, range: z ≥ 2 in orthologs): **satisfied for *and2*, with stated limits** (my calculation; teleosts other than zebrafish)

I applied the same statistic (gap ≤ 4, 2,000 shuffles) to every UniProt record named
`and1`, `and2` or `kcnk5b` in Actinopterygii (taxon 7898). Read level: listing. Data were
retrieved 2026-11-04.

| gene | records | p < 0.05 | z > 0 | median z |
|---|---|---|---|---|
| *and2* | 26 (24 species) | 18 (17 species) | 26/26 | 2.46 |
| *and1* | 43 | 6 | 33/43 | 0.88 |
| *kcnk5b* | 14 | 0 | 4/14 | −0.12 |

- The two zebrafish relatives in the set agree with zebrafish *and2*. These are *Sinocyclocheilus
  anshuiensis* (p = 0.008, z = 2.78) and *Carassius auratus* (p = 0.042, z = 2.05; this record is
  371 aa and may be partial).
- The *and2* signal also holds in distant percomorphs, for example *Oryzias latipes* (p = 0.011)
  and *Oreochromis niloticus* (p = 0.018). It is weaker in salmonids, herring, catfish and cod
  (p 0.05–0.20, z still > 0).
- The *and1* versus *and2* contrast in the claim repeats across species. *and1* is rarely
  significant: 6 of 43 records, scattered across Denticeps, Scleropages, Chanos, O. kisutch,
  Salvelinus and Sinocyclocheilus.
- **Limits:**
  - These are other animals, so this result supports the zebrafish claim but cannot prove it.
  - Orthologs are phylogenetically non-independent, so the counts overstate the evidence.
  - Most records are unreviewed gene predictions, and paralog or isoform duplicates are counted
    as separate records.
  - I applied no multiple-testing correction.
  - Window k = 4 was taken from the claim, not chosen in advance.
- **Mechanism (my inference, not tested):** only 3 of the 11 close Tyr pairs in zebrafish *and2*
  fall inside a crude `C[DN]P…` repeat window. Pairs 151/155/158 (`CNPYLDPYCLY`) and 351/354
  (`CDPRYDPYC`) do. Pairs 195–197 (`HYYY`) and 389–395 (`YDCYMFY`) do not. So the clustering is
  not simply produced by the repeat motif. I did not test this further.

### C3 (cell, existence: a cell that makes and secretes And2 into the actinotrichia matrix): **satisfied (literature, zebrafish)**

- **Zhang et al. 2010**, *Nature* 466:234 (doi 10.1038/nature09137). Read level: abstract; full
  text could-not-access (behind a login). The authors state that "And1 and And2 are essential
  structural components of elastoidin", the material actinotrichia are made of.
- **Phan et al. 2019**, *PLoS One* 14:e0216370 (PMC6497306). Read level: full-text, partly read
  via summariser. They report that zebrafish *and1/and2* expression "spatially and temporally
  correlate[s] with actinotrichia formation". It appears first in fin-fold ectoderm, then in
  mesenchyme invading the fold, citing Zhang 2010 and Lalonde 2016. This is a secondary
  statement.
- **Lalonde & Akimenko 2018**, *PLoS One* 13:e0192500 (PMC5805328). Read level: full-text,
  keyword-searched. The authors write: "Fin fold mesenchyme produce and secrete actinodin
  proteins." Ablating that mesenchyme caused actinotrichia defects and fin-fold collapse.
- **Tanimoto et al. 2026**, *iScience* 29:117464 (PMC13573005). Read level: full-text,
  keyword-searched. The authors write: "These derived bECs secrete And proteins and fibrillar
  collagens to the subepidermal space, thereby initiating AT formation". Actinotrichia are
  "approximately 2–3 μm in diameter" and "up to 300 μm in zebrafish".
- UniProt annotates a signal peptide (residues 1–23) on zebrafish And2. This is a SignalP
  **prediction**, not a measurement.
- **Gap:** I found no source, at full-text level, that *directly immunodetects And2 protein* in
  zebrafish actinotrichia. Hanzelova 2026 and Rees 2023 used an anti-And1 antibody. One search
  summary said And1 and And2 colocalise in fibres, but I could not trace it to a paper I read.
  That would be read level search-summary, so I don't rely on it. The "secreted into the fibre"
  part therefore rests on author statements and the knockdown phenotype, not on And2-specific
  localisation.
- **Animal:** zebrafish throughout. Rees et al. 2023 (platyfish, *Xiphophorus maculatus*)
  report all four actinodin genes co-expressed in lateral mesenchyme in regenerating fins. That
  is a different species, so I give it as context only.

### C4 (cell, existence: an *and2*-specific phenotype): **unsatisfied: people looked and found none at gross level**

- **Hanzelova et al. 2026** (PMC13120675; full-text, keyword-searched; zebrafish). The *and2*
  allele is a 269-bp deletion that "leads to a truncation of the protein and removes 8 out of
  10 repeats from the C-terminus". From that wording I infer, but have not checked against their
  Fig. 1A, that the deleted part covers most of the Tyr pairs that make up the clustering signal
  (positions 151–506). The paper reports:
  - "Wild-type sibling and single mutant FFs had actinotrichia, whereas double mutants did not"
    (DIC imaging; n = 3 larvae per single-mutant genotype in Fig. 2A).
  - "Adult single mutants had no observable fin defects" (Fig. S5A; live imaging and Alizarin
    Red).
- **Scope of the negative:** this covers larval fin-fold morphology and actinotrichia presence by
  light microscopy, and adult fin and ray morphology. I found no ultrastructural, mechanical,
  fibre-diameter or regeneration-kinetics measurement of the *and2* single mutant, and no
  measurement of whether *and1* is upregulated in it. Hanzelova reports qPCR only for double
  mutants. Those finer measurements are cases of nobody having looked, as far as my search
  reached: Europe PMC "actinodin OR actinotrichia" (331 hits, first 100 screened by title), plus
  full-text keyword searches of Hanzelova 2026, Tanimoto 2026, Kuroda 2024 (PMC11409509),
  Nakagawa 2023 (PMC10119692), Lalonde 2018 and Miyamoto 2026 (PMC13018208). The Keshinro 2021
  thesis (uOttawa) was could-not-access.
- **Why this is not `unsatisfiable`:**
  - Both sides are zebrafish, so the species objection does not apply.
  - But "no observable defect" is a null observation at gross resolution, not a measured number
    that contradicts a bound.
  - C4 is entailed only by the functional reading, not by the literal statistical claim. The
    literal claim survives this result.
- **What it does show:** in zebrafish, *and1* is enough to build actinotrichia without most of
  *and2*'s repeat region. That limits how much cell-scale function the and2-specific clustering
  can carry. Any claim that the clustering is *required* for actinotrichia now has to point to a
  finer phenotype than anyone has yet measured.

---

## 3. Summary

| # | scale | kind | status | evidence type | animal |
|---|---|---|---|---|---|
| C1 | dna | existence | satisfied | literature (cDNA + RefSeq listing) | zebrafish |
| C2 | dna | range | satisfied (with limits) | derived (my calculation on database sequences) | 24 teleost species incl. zebrafish |
| C3 | cell | existence | satisfied (And2-specific localisation not directly shown) | literature | zebrafish |
| C4 | cell | existence | unsatisfied (gross-level null, finer levels unlooked) | measured (by the cited authors) | zebrafish |

Nothing here refutes claim 30 from below. The strongest new information:

1. The claim's numbers reproduce exactly under a simple statistic. The result depends on the
   window size (p = 0.054 at k = 5).
2. The and2-but-not-and1 pattern recurs across teleost orthologs. This is my calculation, not
   an observation.
3. In zebrafish, an *and2* allele that removes most of the protein's C-terminal repeats leaves
   actinotrichia and adult fins grossly normal. Any functional reading of the clustering has to
   accommodate this measured result.

## 4. Flying fish note

UniProt holds 26 records from exocoetid genera (*Cheilopogon*, *Exocoetus*, *Hirundichthys*,
*Cypselurus*). **None** is an actinodin (query run 2026-11-04). No exocoetid number exists for
any constraint above, so none was used. The closest relative in the C2 set is medaka (*Oryzias
latipes*), which is in the same order (Beloniformes). Its *and2* also shows the clustering
(p = 0.011). That is a cross-species observation, not evidence about zebrafish, and it is not a
measurement of a flying fish.

## Sources

- Hanzelova P, Baird C, Keshinro B, Kadhom R, Lalonde RL, Akimenko MA (2026) An essential role
  for actinotrichia in zebrafish fin patterning and courtship behavior. *Development* 153:dev204990.
  doi:10.1242/dev.204990. **full-text** (Europe PMC XML, keyword-searched).
- Tanimoto R, Miyamoto K, Tamura K, Kondo S, Kuroda J (2026) A collagen orientation switch
  reshapes fin architecture. *iScience* 29:117464. doi:10.1016/j.isci.2026.117464. **full-text**
  (keyword-searched).
- Zhang J et al. (2010) Loss of fish actinotrichia proteins and the fin-to-limb transition.
  *Nature* 466:234–237. doi:10.1038/nature09137. **abstract** (full text could-not-access).
- Phan HE et al. (2019) Differential actinodin1 regulation in embryonic development and adult fin
  regeneration in *Danio rerio*. *PLoS One* 14:e0216370. **full-text** (partial, via summariser).
- Lalonde RL, Akimenko MA (2018) Effects of fin fold mesenchyme ablation on fin development in
  zebrafish. *PLoS One* 13:e0192500. **full-text** (keyword-searched).
- Kuroda J et al. (2020) *Front Cell Dev Biol* 8:580520. **full-text** (partial, via summariser).
  It gives no numeric actinotrichia dimensions.
- Rees L, König D, Jaźwińska A (2023) *Front Cell Dev Biol* 11:1134451 (platyfish). **full-text**
  (partial, via summariser).
- Keshinro B (2021) MSc thesis, University of Ottawa. **could-not-access** (host blocked);
  known only from a search summary.
- UniProt entries A9JRX1, A0ACM8QEN9, E7F5V5, Q6PFU3, A0A8M1PBI1 and all Actinopterygii
  and1/and2/kcnk5b records. **listing**.

```swarm-entail
{"source_claim": 30, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "existence",
      "statement": "The clustered-Tyr arrangement must be encoded by the real zebrafish and2 locus: an independently sequenced transcript must yield the same product as the analysed gene model.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Zebrafish cDNA clone EMBL BC155829 (UniProt A9JRX1, transcript-level evidence) translates to a 508-aa product identical, by string comparison, to RefSeq NP_001104660.1 / NM_001111190.1 (UniProt A0ACM8QEN9); the locus is transcribed in fin folds and was CRISPR-targeted by Hanzelova et al. 2026.",
      "satisfied_evidence": "literature",
      "note": "UniProt cross-references (listing); Hanzelova et al. 2026 Development 153:dev204990 (full-text). Zebrafish on both sides. Not checked: whether the RefSeq model is independent of BC155829, and the cDNA against the GRCz11 genome (Ensembl REST returned 403 via proxy)."},
    {"target_scale": "dna", "kind": "range",
      "statement": "If the clustering is a heritable sequence feature rather than a chance configuration, the same statistic must exceed its shuffled null in and2 orthologs, while and1 and the control should not do so as consistently.",
      "quantity": "z-score of fraction of consecutive Tyr-Tyr gaps <=4 residues vs 2000 sequence shuffles, in teleost and2 orthologs (median)", "lo": 2, "hi": null, "units": "dimensionless (z)",
      "status": "satisfied",
      "satisfied_by": "My calculation on UniProt sequences: and2 median z = 2.46, 18/26 records (17/24 species) p<0.05, 26/26 z>0, including the cyprinids Sinocyclocheilus anshuiensis (p=0.008) and Carassius auratus (p=0.042). and1: median z = 0.88, 6/43 p<0.05. kcnk5b: median z = -0.12, 0/14.",
      "satisfied_evidence": "derived",
      "note": "Calculation, not observation. Animals: 24 teleost species incl. zebrafish, so this supports but cannot prove the zebrafish claim. Limits: orthologs are non-independent, most records are unreviewed predictions, no multiple-testing correction, window k=4 taken from the claim. The zebrafish numbers reproduce the claim exactly (0.393 vs 0.211, z=2.74), but the result depends on the window (k=5 gives p=0.054). Script: docs/research/fish/claim-30-tyr-gap-test.py."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "A cell type must synthesise the protein and send it out of the cell into the subepidermal matrix where the actinotrichia fibres form (functional reading).",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Zebrafish fin-fold basal epidermal cells, and then fin-fold mesenchyme, express and1/and2 and secrete And proteins into the subepidermal space where actinotrichia (about 2-3 um diameter, up to 300 um long) form. And1+And2 knockdown or knockout abolishes actinotrichia. The signal peptide 1-23 is a SignalP prediction only.",
      "satisfied_evidence": "literature",
      "note": "Zhang et al. 2010 Nature 466:234 (abstract; full text could-not-access); Lalonde & Akimenko 2018 PLoS One 13:e0192500 (full-text): 'Fin fold mesenchyme produce and secrete actinodin proteins'; Tanimoto et al. 2026 iScience 29:117464 (full-text); Phan et al. 2019 PLoS One (full-text, partial). All zebrafish. Gap: no full-text source found that immunodetects And2 specifically in actinotrichia (published stains use anti-And1)."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "If and2's clustered-Tyr region does something and1 cannot, loss of that region of and2 alone (with and1 intact) must produce a detectable cell- or tissue-level fin-fold or actinotrichia phenotype (functional reading).",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "None found. Zebrafish and2 single mutants (269-bp deletion; truncated protein lacking 8 of 10 C-terminal repeats) have actinotrichia in larval fin folds and no observable adult fin defects; only and1;and2 double mutants lose actinotrichia.",
      "satisfied_evidence": "measured",
      "note": "Hanzelova et al. 2026 Development 153:dev204990 (full-text, keyword-searched), zebrafish on both sides. The negative covers DIC fin-fold morphology (n=3 per single genotype) and adult live and Alizarin Red fin morphology. Nobody has looked, as far as found, at ultrastructure, fibre mechanics or diameter, regeneration, or and1 compensation in and2 single mutants (search: Europe PMC 'actinodin OR actinotrichia', first 100 of 331 screened, 6 full texts keyword-searched; Keshinro 2021 thesis could-not-access). Not unsatisfiable: this is a gross-level null, not a measured number contradicting a bound, and the literal statistical claim does not require non-redundancy. My inference, not checked against their Fig. 1A, is that the deletion removes most clustered-Tyr positions (151-506)."}
  ]}
```
