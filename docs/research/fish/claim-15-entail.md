# Claim 15: propagation to the DNA and cell scales

**Source claim (protein scale, evidence: derived):** kcnk5b carries EXACTLY TWO K+
selectivity-filter motifs `[TS].[GAS][YFL]G`, TIGYG at 98-102 and TVGFG at 203-207. This is the
defining two-pore K2P architecture.

**Subject animal throughout:** zebrafish (*Danio rerio*), gene `kcnk5b`. I used no flying-fish
(exocoetid) data. Where a number comes from another species or from a heterologous host, I say
so in the sentence that uses it.

Date of checks: 2026-11-04.

---

## 0. First, re-deriving the claim itself (computed, not observed)

- I scanned UniProt **Q6PFU3** (*Danio rerio*, GN=kcnk5b, 448 aa, unreviewed, PE=2) with the
  regex `(?=([TS].[GAS][YFL]G))`. It returns exactly two hits: **98 TIGYG** and **203 TVGFG**.
  This is a computed result that reproduces the claim.
  - Read-level: the full sequence (FASTA) from rest.uniprot.org.
- The other UniProt entry for the gene, A0A8M1PBI1, came back as a 21-residue record, which is
  not a usable sequence, so I did not scan it.
- `GFG` occurs only once in Q6PFU3, at 205-207, which is inside motif 2. `GYG` occurs only once,
  at 100-102, inside motif 1. This matters for constraint C3 below.
- Cross-check against the literature (my inference): Perathoner et al. 2014 name the *alf*
  alleles **W169L** and **F241Y**. Q6PFU3 has W at 169 and F at 241, so the paper and this
  sequence use the same numbering.

---

## 1. Entailed constraints

If kcnk5b really carries two filter motifs at those positions:

| # | Target scale | Kind | Requirement (generic) |
|---|---|---|---|
| C1 | dna | existence | A single protein-coding locus must exist whose mature transcript encodes **both** filter motifs in **one** open reading frame. The two P-domains cannot be split between two genes or carried on mutually exclusive exons. |
| C2 | dna | spatial | In that coding sequence, the codons for the two motifs must lie **in frame, 105 codons = 315 nt apart** (start to start). Any intron that interrupts a motif must preserve the frame. |
| C3 | cell | existence | A cell that expresses the protein must gain a K+ conductance, and that conductance must **depend on the filter motif(s)**: mutating a filter motif must abolish it. |
| C4 | cell | range | The conductance must be K+-selective. The zero-current (reversal) potential must track E_K, with a slope of **50-59 mV per tenfold change in [K+]o** at about 20-25 °C. The upper bound is the Nernst slope, 58.2-59.2 mV. The lower bound of 50 mV is my operating threshold for "highly K+-selective", not a published cutoff. |
| C5 | cell | energetic | For the channel to do anything as a leak channel, the cell must keep a transmembrane K+ gradient so that E_K is more negative than the resting potential. Outward K+ flux must have a driving force, which some pump has to pay for. |

---

## 2. Checks

### C1: dna / existence: **satisfied** (derived from sequenced records)

- **NCBI Gene 393606** (`kcnk5b`, ZFIN ZDB-GENE-040426-1297).
  - It sits on chromosome 20, NC_141040.1 (assembly GRCz13ab, GCF_052040795.2, strain M-AB),
    at 9,371,092-9,386,432, with 5 exons.
  - Read-level: listing (E-utilities esummary and GenBank flat file).
- **RefSeq NM_200633.1** is derived from a sequenced cDNA, EMBL BC057416.
  - Its CDS is 68..1414, which is 1,347 nt.
  - I translated this CDS myself. It is **identical to Q6PFU3 across all 448 residues** and
    contains both motifs (computed).
  - Read-level: full-text (the sequence record).
- I also translated the genomic CDS join on GRCz13ab. Both motifs are present at 98 and 203
  (computed).
  - The genomic translation differs from the RefSeq protein at one residue, **A78V**, which is
    outside both motifs.
  - The genomic record's own annotation says "The RefSeq protein has 1 substitution compared to
    this genomic sequence". The two sources disagree at residue 78. I report the disagreement
    rather than resolve it; it does not bear on the claim.
- What this shows: a sequenced zebrafish mRNA encodes both motifs in one ORF. The existence of a
  cDNA is an observation that the transcript is made. The positions are my computation from it.

### C2: dna / spatial: **satisfied** (derived)

- In NM_200633.1 (computed):
  - TIGYG is at CDS nt **292-306** (`ACT ATA GGT TAT GGT`).
  - TVGFG is at CDS nt **607-621** (`ACT GTC GGT TTT GGT`).
  - The start-to-start distance is **315 nt**, in frame, as required.
- **Additional finding (derived from the NCBI gene model, not stated in any paper I read):**
  - **Motif 1 is split by an intron.** The genomic CDS join is
    `67..252, 4174..4285, 8082..8248, 8340..8508, 13552..14264` (coordinates relative to the
    fetched region).
  - Exon 2 ends `...ACT ATA G`. A **3,796-nt intron** follows. Exon 3 resumes `GT TAT GGT...`.
    So the intron (phase 1) falls inside the first glycine codon of TIGYG.
  - Motif 2 lies entirely inside exon 4.
  - Consequence (my inference): producing TIGYG at the DNA→RNA step requires exact splicing at
    the exon 2/3 junction. The sequenced cDNA BC057416 shows that this splice does occur in vivo
    in at least the source tissue of that clone. I did not look up which tissue that was.

### C3: cell / existence: **satisfied**, for motif 2 only (measured, in a heterologous cell plus in vivo zebrafish)

**Source:** Perathoner S, et al. 2014. "Bioelectric signaling regulates size in zebrafish fins."
*PLoS Genetics* 10(1):e1004080. PMC3894163.
- Read-level: full-text, through a summarising fetch tool. I read about 100k of the 118k
  characters; the remaining 18k were not read.

**What the authors report:**
- Two-electrode voltage clamp in *Xenopus* oocytes, injected with 4 ng of zebrafish `kcnk5b`
  cRNA.
  - Holding potential −80 mV; 0.5 s steps from −100 to +60 mV.
  - n = 5-26 oocytes.
- Wild-type Kcnk5b gives a K+ current. The *alf* mutants (W169L, F241Y) give "an almost two-fold
  increase in K+ conductance".
- They mutated the selectivity-filter **GFG → AAA**. The resulting channel "is unable to conduct
  K+" (Fig. 6J, current normalised to wild type at 60 mV).
- In transgenic **zebrafish** overexpressing this pore-dead construct, "No overgrowth was
  detected" (n = 32).

**My inference:** GFG is unique to residues 205-207 of Q6PFU3. So their AAA mutant hits **motif
2 (TVGFG)**, and the measurement directly ties motif 2 to K+ conduction and to the fin phenotype.

**Animals on each side:**
- The protein is zebrafish Kcnk5b. The host cell for the current measurement is a frog oocyte.
- The phenotype is zebrafish in vivo.
- This is evidence about the zebrafish protein, but it is not a measurement in a native
  zebrafish cell.

**Supporting source:** Yi C, et al. 2021, *eLife* (PMC8110307; DOI 10.7554/eLife.60691) reports
that "Kcnk5b expression increases current density due to K+ leak" in HEK293T cells expressing the
zebrafish protein.
- Read-level: full-text, about 100k of 212k characters. The methods section was not reached.
- No numbers were extracted.

**Scope of the gap:** **motif 1 (TIGYG) has not been mutated** in either paper I read. Whether
motif 1 is functionally required in zebrafish Kcnk5b is unknown: nobody has looked, as far as
these two papers and the searches below show. A K2P channel would be expected to need both
(inference), but that is not a measurement.

### C4: cell / range (50-59 mV/decade): **unsatisfied**, because nobody has measured it, not because a measurement failed

**What exists:**
- Perathoner 2014 (as above) states that the *alf* mutants shift oocyte membrane potential
  "towards −90 to −100 mV", which they call "the equilibrium potential for K+ in Xenopus oocytes".
- This is qualitative support for K+ selectivity, but it does not meet the constraint:
  - no wild-type value is given;
  - no water-injected control value is given;
  - no bath [K+] is stated;
  - there is no ion substitution, and no reversal-vs-[K+]o slope.
- So the 50-59 mV/decade range cannot be checked from it.

**What I searched:**
1. Web search: `zebrafish Kcnk5b electrophysiology reversal potential potassium selectivity HEK
   cells patch clamp`.
2. Web search: `"kcnk5b" zebrafish ion selectivity OR "reversal potential" OR "rubidium" OR
   "sodium permeability"`.
3. The full texts of PMC3894163 and PMC8110307, partially read as noted above.
4. A 2024 *PLoS Biology* fin-bud paper surfaced at search-summary level. It reports that Kcnk5b
   enhances depolarisation **via Na+ channels**. That is a downstream effect, not Na+ permeation
   through Kcnk5b. I did not read it in full, and its methods may contain I-V data I have not seen.

**Finding:** no zebrafish Kcnk5b selectivity slope, permeability ratio (P_Na/P_K, P_Rb/P_K) or
reversal-vs-[K+]o series was found within these searches. This is "nobody has looked", or at
least "nobody has published it where these searches reach". It is **not** "looked and found it
non-selective".

**Cross-species note (not used for the verdict):**
- Human TASK-2 (KCNK5; Reyes et al. 1998, *J Biol Chem* 273:30863) is described as producing
  currents "with activation potential thresholds that closely follow the K+ equilibrium
  potential".
  - Read-level: search-summary of the abstract.
  - That is a different species (human) and a different paralogue context.
  - No mV/decade figure was found.
- So it neither satisfies nor contradicts C4 for zebrafish.

**Unsatisfiable?** No. No measured number contradicts K+ selectivity for this protein in any
species I found.

### C5: cell / energetic (K+ gradient maintained, E_K < V_rest in Kcnk5b-expressing fin cells): **open**

- **Not checked.** I found no paper that measures [K+]i, E_K or resting Vm together in
  Kcnk5b-expressing zebrafish fin mesenchyme.
- The 2024 *PLoS Biology* paper may report membrane-potential (dye) measurements in fin-bud
  cells. I saw it only at search-summary level, so I make no claim from it.
- Oocyte potentials in Perathoner 2014 are about a frog host cell, not a zebrafish fin cell.
  They do not settle this either way.

---

## 3. Summary

| # | Status | Evidence | Animal(s) |
|---|---|---|---|
| C1 dna existence | satisfied | derived from sequenced cDNA plus genome | zebrafish |
| C2 dna spatial 315 nt | satisfied | derived; motif 1 split by a 3,796-nt phase-1 intron | zebrafish |
| C3 cell existence | satisfied for motif 2 only | measured (oocyte TEVC + transgenic fish) | zebrafish protein; frog oocyte host |
| C4 cell range 50-59 mV/dec | unsatisfied (not measured) | unknown | none found for zebrafish |
| C5 cell energetic | open | not checked | none |

**No constraint is unsatisfiable.** Nothing found at the DNA or cell scale contradicts claim 15.
The weakest link is quantitative K+ selectivity (C4): it is the textbook expectation, but there is
no published measurement for the zebrafish channel within the searches above.

### Sources

- UniProt Q6PFU3, https://rest.uniprot.org/uniprotkb/Q6PFU3 (full sequence record)
- NCBI Gene 393606 and RefSeq NM_200633.1; NC_141040.1 region 9371092-9386432 (sequence records,
  through E-utilities)
- Perathoner et al. 2014, *PLoS Genet* 10:e1004080,
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3894163 (full-text, partial read)
- Yi et al. 2021, *eLife* 10:e60691, https://pmc.ncbi.nlm.nih.gov/articles/PMC8110307
  (full-text, partial read; methods not reached)
- Reyes et al. 1998, *J Biol Chem* 273:30863 (search-summary only; human, cross-species note)
- 2024 *PLoS Biology* zebrafish fin-bud Kcnk5b paper (search-summary only; authors and DOI not
  verified, so not cited further)

```swarm-entail
{"source_claim": 15, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "existence",
      "statement": "A single protein-coding locus must exist whose mature transcript encodes both K+ selectivity-filter motifs in one open reading frame",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "NCBI Gene 393606 (kcnk5b, chr20 NC_141040.1 GRCz13ab 9,371,092-9,386,432, 5 exons); RefSeq NM_200633.1 from sequenced cDNA BC057416, CDS 68..1414 translates identically to UniProt Q6PFU3 incl. TIGYG98 and TVGFG203 (computed)",
      "satisfied_evidence": "derived",
      "note": "Zebrafish. Translation done by me from the sequence records (read-level: full sequence). Genomic CDS differs from RefSeq protein at A78V, outside both motifs; the records disagree and I left the disagreement unresolved."},
    {"target_scale": "dna", "kind": "spatial",
      "statement": "The codons for the two filter motifs must lie in frame, 105 codons apart in the coding sequence; any intron interrupting a motif must preserve frame",
      "quantity": "start-to-start CDS distance between the two filter-motif codon runs", "lo": 315, "hi": 315, "units": "nt",
      "status": "satisfied",
      "satisfied_by": "NM_200633.1 CDS nt 292-306 (TIGYG) and 607-621 (TVGFG): 315 nt, in frame. Motif 1 is split by a 3,796-nt phase-1 intron between exons 2 and 3; motif 2 lies within exon 4.",
      "satisfied_evidence": "derived",
      "note": "Zebrafish. Computed by me from the RefSeq mRNA and the NCBI GRCz13ab gene model; the intron split is not stated in any paper I read. The existence of cDNA BC057416 shows the splice occurs in vivo in at least the tissue that clone came from."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "Cells expressing the protein must gain a K+ conductance that depends on the filter motif, so that mutating the motif abolishes it",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Perathoner et al. 2014 PLoS Genet 10:e1004080: zebrafish kcnk5b cRNA gives K+ current in Xenopus oocytes (TEVC); GFG->AAA filter mutant 'unable to conduct K+' (Fig 6J) and gives no fin overgrowth in transgenic zebrafish (n=32). GFG is unique to residues 205-207, so the mutation is in motif 2 (my inference). Yi et al. 2021 eLife: zebrafish Kcnk5b raises K+ leak current density in HEK293T.",
      "satisfied_evidence": "measured",
      "note": "Read-level: full-text, partial (PMC3894163 ~100k/118k chars; PMC8110307 ~100k/212k chars). Animals: zebrafish protein in a frog-oocyte host plus zebrafish in vivo. Only motif 2 has been tested; motif 1 (TIGYG) has never been mutated in either paper, so its necessity is not looked at, not refuted."},
    {"target_scale": "cell", "kind": "range",
      "statement": "The channel's conductance must be K+-selective: the reversal potential must shift with external K+ at close to the Nernst slope",
      "quantity": "slope of reversal potential vs log10[K+]o", "lo": 50, "hi": 59, "units": "mV per decade",
      "status": "unsatisfied",
      "satisfied_by": "No reversal-vs-[K+]o series, permeability ratio or ion-substitution data found for zebrafish Kcnk5b. Perathoner 2014 gives only a qualitative statement that alf mutants push oocyte Vm to -90 to -100 mV 'near E_K', with no wild-type value, no control and no bath [K+].",
      "satisfied_evidence": "unknown",
      "note": "This is 'nobody has measured it', not 'measured and failed'. Scope: two web searches (kcnk5b + reversal potential/selectivity/rubidium/sodium permeability), plus partial full-text reads of PMC3894163 and PMC8110307; a 2024 PLoS Biol fin-bud paper was seen at search-summary level only. Human TASK-2 (Reyes 1998, search-summary) has thresholds that 'follow E_K'; that is cross-species and not used. The lower bound of 50 mV is my threshold, not a published one. Nothing contradicts the constraint, so it is not unsatisfiable."},
    {"target_scale": "cell", "kind": "energetic",
      "statement": "Cells using the channel as a K+ leak must maintain a K+ gradient such that E_K is more negative than resting Vm, so that outward K+ flux has a driving force",
      "quantity": "E_K minus V_rest in kcnk5b-expressing fin cells", "lo": null, "hi": 0, "units": "mV",
      "status": "open",
      "satisfied_by": "Not checked: found no paired [K+]i/E_K/Vm measurement in zebrafish fin mesenchyme.",
      "satisfied_evidence": "unknown",
      "note": "Oocyte potentials (Perathoner 2014) are for a frog host cell and are not used. The 2024 PLoS Biol fin-bud paper may contain Vm-dye data but was not read beyond a search summary."}
  ]}
```
