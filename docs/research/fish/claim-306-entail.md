# Claim 306: what it requires at the DNA and cell scales

**Source claim (protein scale, evidence: measured).** A ColabFold search of `pdb70_220313` over the
577-aa zebrafish slc43a2a product ENSDARP00000138218 returned 5 hits. Maximum per-position depth is 2,
median depth is 0, and 474/577 positions have no coverage, including residue 200 and every position from
195 to 205. As stated, the claim bounds what can be concluded about T200K. It concludes nothing about the
residue itself.

**Subject on every side of this document: zebrafish (*Danio rerio*)**, unless a line says otherwise.
The nearest structural and functional measurements turned out to be **human** (SLC43A2/LAT4), with one
mouse result. No flying-fish source came into this check. Every cross-species number is labelled with
its animal below, and none of them is used as a refutation.

I did not re-run the ColabFold search. This document takes the depth numbers in claim 306 as given and
checks only what they require at the adjacent scales.

---

## Source-scale finding (outside the DNA/cell brief, but it changes the claim's scope)

The claim's SCOPE sentence reads: "Low depth here is evidence about structural coverage of this
transporter family." **That was true of the 2022-03-13 snapshot. It is no longer true of the PDB.**

- InterPro lists **3 PDB structures** in PANTHER family PTHR20766 (LAT4-like): **9jbs** (apo, cryo-EM,
  2.88 Å), **9jbt** (Phe-bound, 3.2 Å) and **9jbu** (digitonin, 3.8 Å). All three are **human** SLC43A2
  (569 aa) expressed in human cells. Read-level: listing (InterPro API, PDBe API).
- PDBe gives a deposition date of 2024-08-27 and a **release date of 2026-03-11** for all three, which is
  after the `pdb70_220313` cut-off. The claim's measured zero is therefore **consistent** with the
  database version it names. This is not a refutation.
- The associated paper: "Structures of the neutral amino acid transporter LAT4 provide insights into
  antitumor effects of its inhibitor tubeimoside-1", *EMBO J* 45(12):4283–4298 (2026),
  doi:10.1038/s44318-026-00786-0, PMID 42082777. It also reports an outward-facing structure of the
  SLC43A3 product ENBT1 (associated entry 9l38). Read-level: abstract (via the PDBe publications
  endpoint).
- Consequence (my inference): a PDB70 build from after March 2026 should align a **human** LAT4 template
  across zebrafish residue 200. In my pairwise alignment, residues 195–205 of the zebrafish sequence are
  11/11 identical to human 188–198. The structural-coverage gap reported in claim 306 belongs to the
  2022 database. It is not a permanent property of this family. Anyone re-running structure prediction
  should use a current template set rather than inherit the "alignment ran out" caveat.

---

## Sequence facts used below (all fetched, none recalled)

| item | value | source (read-level) |
|---|---|---|
| ENSDARP00000138218 sequence | UniParc **UPI00062E34B4**, 577 aa, gene slc43a2a; Ensembl xref first seen 2015-05-15, last seen 2026-03-30 | UniParc REST (full record) |
| residue 200 | **T**; window 195–205 = `ASSAVTFPGIK` | computed from the UniParc FASTA (sha256 of the file I fetched: `6a51728e…2e1f`) |
| UniProtKB full-length entry | A0A0R4IP58, **last seen 2022-12-14** (no longer in UniProtKB) | UniParc cross-reference table (listing) |
| current UniProtKB slc43a2a entries | Q7ZUS0 (PE=2, transcript level) and A0A8N7V006, **153 aa each** | UniProt REST (full record) |
| NCBI gene | GeneID 393221, chr15:31,099,368–31,139,242. Only linked RefSeq protein: **NP_956545.1, 153 aa** | NCBI E-utilities esummary/elink (listing) |
| cDNA behind the 153-aa product | BC047854, "MGC:56271 … complete cds" | NCBI esummary (listing) |
| 153-aa vs 577-aa | identical through residue 139; they **diverge at 140** (`…CILN SVTRTASVQLYYQ` vs `…CILI SYGASDPQNL…`) | computed (my comparison) |
| zebrafish↔human alignment | global, BLOSUM62, gap −11/−1: 563 aligned pairs, 78.5 % identity; **zebrafish T200 ↔ human T193** | computed (Biopython PairwiseAligner) |
| human 9jbs at T193 | observed (ratio 1.0). Chain A observed segments 4–52, **72–230**, 314–389, 415–545. PDBe-assigned helices include 176–189, 190–192, **193–202**, 207–227 | PDBe API (listing of the deposited model) |
| human topology annotation | UniProt Q8N370 TRANSMEM 177–197 and 203–223, evidence **ECO:0000255** (sequence-analysis prediction, not measured) | UniProt REST (full record) |

Ensembl REST (`rest.ensembl.org`), ZFIN and Bgee were **not reachable** from this environment: the
proxy returned 403 or timed out. So I could not read the Ensembl transcript, its CDS, or its transcript
support level. This matters for D1 to D3.

---

## Constraints

### D1 — dna / existence: a gene model must encode the queried 577-aa product with Thr at 200

If no gene model translates to this sequence, "residue 200" and "T200K" refer to nothing.

**Status: satisfied, at the level of an annotation record.** UniParc UPI00062E34B4 is 577 aa, residue 200
is T, and it is cross-referenced to ENSDARP00000138218, still active in 2026. This shows that a gene
**model** exists. It does not show that the model is correct. See D2.

### D2 — dna / existence: an expressed transcript must exist that spans the codon for residue 200

The claim treats a 577-aa protein as the object being described. For that object to be a protein the
fish makes, some transcript evidence must cover the exons around codon 200.

**Status: unsatisfied, with a precisely bounded scope.**
- **Searched and found nothing:** NCBI Gene 393221 (the only linked RefSeq protein is the 153-aa
  NP_956545.1; no 577-aa XP model is linked) and UniProtKB (only 153-aa entries remain; the 577-aa TrEMBL
  entry A0A0R4IP58 was dropped after 2022-12-14). The one full-length cDNA, BC047854, encodes a product
  that diverges from the 577-aa sequence at residue 140 and stops at 153. **It does not reach residue
  200.**
- **Could not look:** Ensembl transcript support level and exon structure, and ZFIN/Bgee expression.
  All were blocked by network policy. Ensembl may hold RNA-seq support that would satisfy this
  constraint. "Not found where I could look" is the finding. "Looked everywhere and found nothing" would
  overstate it.
- **Not unsatisfiable:** BC047854 is a measured transcript, but a 153-aa isoform does not contradict a
  second, longer isoform. My inference is that the divergence at 140 looks like alternative splicing or
  intron retention, but I have not seen the exon structure.
- **The sources disagree, and I am keeping both positions:** Ensembl annotates a 577-aa product, while
  NCBI RefSeq and current UniProtKB annotate only 153 aa.

### D3 — dna / range: the CDS of the 577-aa model must be exactly 1734 nt

This is (577 × 3) + 3 for the stop codon, assuming no selenocysteine or frameshift annotation. It is
derived arithmetic, not a measurement. The upper bound against genomic span is trivially met: the NCBI
gene span is 39,875 nt.

**Status: open.** This needs the Ensembl transcript's CDS, which I could not fetch. I did not check it.

### C1 — cell / spatial: the 195–205 window must sit in the ordered, membrane-embedded transporter core

The claim's own caution only makes sense if this region is ordered. Low predicted confidence there
should then mean "the alignment ran out", not "disordered". At the cell scale, ordered transporter
cores lie within the bilayer, so the window should fall in a helical segment comparable to the
membrane's hydrophobic thickness. I take that thickness as ~3 nm, which is ~20 residues of α-helix at
0.15 nm/residue. That figure is a textbook approximation that I am **assuming**; I did not measure or
cite it here.

**Status: open.**
- **Supporting measurement, from human:** in cryo-EM structure 9jbs, human T193 (aligned to zebrafish
  T200) is observed, and residues 72–230 form a continuous observed stretch. The PDBe-assigned helix runs
  193–202, preceded by 176–189. The window is ordered **in the human protein**.
- **Inference to zebrafish:** the 11-residue window is identical between the two species and overall
  identity is 78.5 %. That makes the same fold likely, but it is an inference across species, not a
  zebrafish measurement.
- **Not checked:** membrane depth. I did not read a membrane placement (OPM/PDBTM) for 9jbs. The UniProt
  TM boundaries are predictions (ECO:0000255). They put human 193 near the end of predicted TM5 at
  177–197, and the deposited model has a helix break at 189/190. Whether residue 200 is mid-bilayer or at
  the interface is **unknown**.

### C2 — cell / existence: a membrane amino-acid transport function must exist for this gene product

The claim's scope frames the protein as a member of "this transporter family". That framing requires
the product to act as a transporter at the cell membrane.

**Status: open.**
- **Human, measured:** plasma-membrane localisation (UniProt Q8N370, ECO:0000269 citing PubMed 30379325).
  Na⁺-, Cl⁻- and pH-independent uniport of L-Phe, L-Met and branched-chain amino acids (PubMed 15659399,
  26305885). Read-level: listing (UniProt function and location comments). I did not read the papers.
- **Mouse:** basolateral low-affinity symmetric uniporter in absorptive epithelia, needed for early
  development. Source: scicrunch record for PMID 25480797. Read-level: search-summary.
- **Zebrafish:** a web search ("zebrafish slc43a2a expression LAT4 amino acid transporter", standard
  mode) found **no study of zebrafish slc43a2a function or expression**. The only zebrafish SLC43 work in
  the results concerned LAT3 (SLC43A1) knockdown in podocytes, cited in a review (Fujita Health University
  record, read-level: search-summary). That is a different paralog and tells us nothing here. ZFIN and
  Bgee were not reachable. As far as I could search, nobody has looked at this function in zebrafish; I
  found no study that looked and saw nothing.

### Kinds I could not support

I wrote no `timescale`, `energetic` or `conservation` constraint. An alignment-depth claim makes no
statement about rates, energy budgets or balances at the DNA or cell scale. Inventing one to fill the
kinds would be the failure this exercise is meant to catch.

---

## Verdict summary

- **No constraint is unsatisfiable.** Nothing measured contradicts claim 306.
- The most consequential result sits at the **source scale**. Human LAT4 structures, released in March
  2026, cover the residue-200 window with an identical 11-residue sequence. The claim's measurement
  stands for `pdb70_220313`, but its "structural coverage of this family" scope is out of date.
- The weakest point sits at the **DNA scale**. The 577-aa product is an Ensembl-only model. NCBI RefSeq and
  UniProtKB carry only a 153-aa product, which diverges at residue 140, and its cDNA does not reach
  residue 200. Before any T200K argument, confirm in Ensembl or by RT-PCR that a transcript covering
  codon 200 is expressed.

```swarm-entail
{"source_claim": 306, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "existence",
      "statement": "A protein-coding gene model must exist whose CDS translates to the queried 577-aa sequence with Thr at position 200",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "UniParc UPI00062E34B4 (577 aa, slc43a2a, Danio rerio) cross-referenced to Ensembl ENSDARP00000138218, active to 2026-03-30; residue 200 = T, window 195-205 = ASSAVTFPGIK",
      "satisfied_evidence": "literature",
      "note": "UniParc REST record, read-level full-text. Shows an annotation exists, not that it is correct; see the next constraint. Zebrafish on both sides."},
    {"target_scale": "dna", "kind": "existence",
      "statement": "An expressed transcript must exist whose exons span the codon for residue 200 of the 577-aa product",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "Searched NCBI Gene 393221 (only RefSeq protein NP_956545.1, 153 aa) and UniProtKB (only 153-aa entries Q7ZUS0, A0A8N7V006; 577-aa A0A0R4IP58 last seen 2022-12-14). The only full-length cDNA, BC047854, encodes a product that diverges at residue 140 and ends at 153, so it does not reach codon 200",
      "satisfied_evidence": "unknown",
      "note": "NCBI E-utilities and UniProt REST, read-level listing. SCOPE: Ensembl transcript support level, ZFIN and Bgee could not be accessed (proxy 403/timeout), so this is not-found-where-searchable, not people-looked-and-found-nothing. Not unsatisfiable: a 153-aa isoform does not contradict a longer one. Sources disagree: Ensembl 577 aa vs RefSeq/UniProtKB 153 aa. Zebrafish on both sides."},
    {"target_scale": "dna", "kind": "range",
      "statement": "The coding sequence of the transcript encoding the 577-aa product must have length 3 x 577 + 3 (stop)",
      "quantity": "CDS length", "lo": 1734, "hi": 1734, "units": "nt",
      "status": "open",
      "satisfied_by": "Not checked: requires the Ensembl transcript CDS, which could not be fetched (rest.ensembl.org blocked by proxy)",
      "satisfied_evidence": "derived",
      "note": "Bound is derived arithmetic, assuming no frameshift or selenocysteine annotation. Upper bound trivially below the NCBI genomic span of 39,875 nt (chr15:31099368-31139242, GeneID 393221, listing)."},
    {"target_scale": "cell", "kind": "spatial",
      "statement": "The residue 195-205 window must lie in the ordered, membrane-embedded transporter core: a helical segment whose length is comparable to bilayer hydrophobic thickness, rather than a disordered loop",
      "quantity": "hydrophobic thickness spanned by the helical segment containing residue 200", "lo": 2.5, "hi": 3.5, "units": "nm",
      "status": "open",
      "satisfied_by": "HUMAN cryo-EM 9jbs (2.88 A): human T193, aligned to zebrafish T200 with the 195-205 window 11/11 identical, is observed in continuous segment 72-230 and in PDBe-assigned helix 193-202 (preceded by 176-189). Membrane depth of residue 193 not determined",
      "satisfied_evidence": "measured",
      "note": "The measurement is in HUMAN SLC43A2 (expressed in human cells); the claim is about ZEBRAFISH, so this is cross-species support, not satisfaction. PDBe API listing; paper doi:10.1038/s44318-026-00786-0 read at abstract level. The 2.5-3.5 nm bilayer thickness is an assumed textbook range, not measured here. UniProt Q8N370 TM 177-197/203-223 are predictions (ECO:0000255). No OPM/PDBTM membrane placement read."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "The gene product must act as a membrane amino-acid transporter in the cell, consistent with the claim's framing of a 'transporter family'",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "HUMAN SLC43A2: plasma-membrane localisation (PMID 30379325) and Na+/Cl-/pH-independent uniport of L-Phe, L-Met and BCAAs (PMID 15659399, 26305885). MOUSE: basolateral low-affinity uniporter (PMID 25480797). ZEBRAFISH slc43a2a: no functional or expression study found",
      "satisfied_evidence": "literature",
      "note": "Human data via UniProt Q8N370 comments (listing; papers not read). Mouse via scicrunch (search-summary). Zebrafish negative scope: one standard web search 'zebrafish slc43a2a expression LAT4 amino acid transporter'; ZFIN/Bgee unreachable. Read as nobody-has-looked, not looked-and-found-nothing. Species differ, so not satisfied for zebrafish."}
  ]}
```
