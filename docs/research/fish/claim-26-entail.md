# Claim 26 — entailment to adjacent scales (dna, cell)

**Source claim (scale `protein`, evidence `derived`):**
> An MSA-dependent model's confidence tracks ALIGNMENT DEPTH, not disorder: PDB70 depth falls to
> 0.0 from residue 326 because crystallised K2P constructs are truncated, and Boltz2 reads 41.4
> there while MSA-independent ESMFold2 reads 76.4.

Date of check: 2026-11-04. All web and API lookups were made from this session. Read-levels are given per source.

## 0. What the claim is about, and what I could not pin down

- **Which protein? Unknown.** The claim says "K2P" and gives residue 326. It does not name the gene,
  the species, or the numbering. Claim 26's source is not in this repository: I grepped the working
  tree and all 30 commits on all branches for `PDB70`, `Boltz`, `ESMFold`, `K2P`, `41.4`, `76.4` and
  `claim 26` and found nothing. Below I test the claim against the TREK subfamily (KCNK2/TREK-1,
  KCNK10/TREK-2, KCNK4/TRAAK), because those are the K2Ps with many truncated crystal structures. I
  check zebrafish (*Danio rerio*) sequences where they exist, because this project's claims are
  mostly about zebrafish. **Every species is named where a number is used.**
- **I did not reproduce the claim's numbers** (41.4, 76.4, or the depth profile). I also did not
  confirm that a model called "ESMFold2" exists under that name. Those are protein-scale facts and
  outside this task.
- **One ambiguity in the claim itself.** PDB70 is a *template* database (structures). An "MSA" is a
  *sequence* alignment, built from UniRef or genome-derived databases. The claim uses the
  template-depth collapse as its evidence but names the mechanism "MSA-dependent". Constraint D3
  below separates the two. This is my reading of the claim, not something it states.

## 1. Constraints

### D1 — dna / `range`: the native coding sequence must extend well past residue 326
*Statement:* If residues ≥326 exist for a model to score, the native open reading frame must encode
a protein longer than the crystallised construct. So the full-length protein length must be ≥ 327
aa. If the gene ended near 326, there would be nothing to score and the claim would be empty.

*Check (UniProt REST, queried 2026-11-04, read-level: listing; entries are computationally
annotated unless marked reviewed):*

| species | gene | accession | length (aa) | status |
|---|---|---|---|---|
| *D. rerio* | kcnk2a | F1QAI2, A0ACM8QMU7 / A0AB32T9G3 | 426 / 413 | unreviewed |
| *D. rerio* | kcnk2b | A0AB32TCH9 / Q32LX0, A0ACM8Q8Y4 / A0AC58I4H9 | 425 / 384 / 231 | unreviewed |
| *D. rerio* | kcnk10a | A3QJX1, A0A8M1P283 | 569 | unreviewed |
| *D. rerio* | kcnk4a | A0AB32T5S6 / A0AB32T7K4 / A0AC58H9G9 | 542 / 425 / 357 | unreviewed |
| *H. sapiens* | KCNK2 | O95069 | 426 | reviewed |
| *M. musculus* | Kcnk2 | P97438 | 426 | reviewed |
| *H. sapiens* | KCNK10 | P57789 | 538 | reviewed |
| *H. sapiens* | KCNK4 | Q9NYG8 | 393 | reviewed |

**Verdict: satisfied**, for both zebrafish TREK-1 paralogs and for the human and mouse proteins.
Each has at least one predicted product of 384–426 aa, so 58–100 residues lie beyond 326.
Caveats:
1. Zebrafish entries are unreviewed gene-model predictions, not measured proteins.
2. Zebrafish kcnk2b also has a 231-aa entry (A0AC58I4H9). I did not check whether that is a real
   short isoform or a fragment.
3. Human KCNK2 has a reviewed isoform 4 in which residues 233–426 are replaced (UniProt
   "Alternative sequence 233–426", citing PMID 24196565; read-level: listing). So a CTD-less
   product exists in human. That is a human fact. It is not evidence about zebrafish either way.

### D2 — dna / `spatial`: the depth collapse must sit at a construct boundary, not a gene feature
*Statement:* The claim gives a cause: depth falls to 0 because crystallised constructs are
*truncated*. That cause requires the C-terminal end of deposited structures, set by the
cloning-construct design, to coincide with the depth-collapse position (≈326). The match needs to be
within a few percent of length, not a factor of 2. If the deposited structures instead ran well past
326, or stopped far before it, the stated cause would be wrong. Bound: last modelled residue of
deposited TREK-subfamily structures in [300, 350] in their own UniProt numbering.

*Check (PDBe SIFTS `best_structures` API, queried 2026-11-04, read-level: listing; these are
**observed/modelled** residue ranges mapped to UniProt, not the construct boundaries):*
- human TREK-1 (O95069): 4TWK, residues 41–315 (one X-ray entry mapped).
- mouse TREK-1 (P97438): 25 X-ray entries (6CQ6/8/9, 6V36/37/3C/3I, 6W7B–6W8F, 8UE2/9/C, 8UF6).
  They end at residue 336–339. 8UE* entries start at 50, the rest at 35–36.
- human TREK-2 (P57789, 538 aa): 4BW5, 4XDJ/K/L, 8QZ1–4, residues 62/70–335.
- human TRAAK (Q9NYG8, 393 aa): 12 entries ending at 264 or 274.
- No cryo-EM entry was returned for any of the four by this API. I could not run an independent
  RCSB search: search.rcsb.org was refused by this session's egress proxy. **So "no full-length
  structure exists" is not established here.**

**Verdict: satisfied, with a numbering caveat.** Every TREK-1 and TREK-2 X-ray structure mapped by
SIFTS ends between residue 315 and 339 of proteins that are 426–538 aa long. All of them are
C-terminally truncated, which matches the claim's mechanism. The claim's 326 sits inside the
315–339 spread. I cannot say which structure or numbering produced *exactly* 326, because the
claim does not name its query sequence (§0). The match is therefore to within ~4% of position,
derived from listings. It is not an exact reproduction.

### D3 — dna / `conservation` (sequence supply): homologous sequence depth must NOT collapse at 326
*Statement:* This constraint splits the two readings of "alignment depth". The claim contrasts an
MSA-dependent model with an MSA-independent language model that still scores 76.4 beyond 326. A
language model trained on UniRef can only have learned the CTD if many genome-derived sequences
cover it. So homologous coding sequences that span the post-326 region must exist in sequence
databases in quantity. If they do, the *sequence* MSA beyond 326 is not empty, and the "depth" that
falls to 0 is template depth (PDB70) only. In that case the claim's mechanism holds only in its
template sense. This is my inference about what the claim needs.

*Check (UniProt REST counts, `gene:kcnk2 AND taxonomy_id:7742` [Vertebrata], queried 2026-11-04,
read-level: listing):* 762 entries in total. 609 have length 400–600 aa, 150 have length < 400 aa.
Ray-finned fish (`gene:kcnk2a AND taxonomy_id:7898`) gave 25 entries; I did not split those by
length.

**Verdict: satisfied** for existence: hundreds of vertebrate KCNK2 sequences are long enough to
contain the CTD. **Not checked:** whether those CTDs actually *align* to the query. The distal CTD
is likely less conserved than the pore domains. I did not build an MSA or compute per-column depth.
The 609 count is a database listing, not an alignment depth.
**Consequence for the claim (my inference, not tested):** If a real sequence MSA stays deep past
326, then Boltz2's low score there cannot be explained by *MSA* depth. It must come from template
absence, or something else. The claim's wording ("MSA-dependent … PDB70 depth") should be narrowed
to template depth unless a per-column MSA depth is shown to fall as well.

### C1 — cell / `existence`: the post-326 region must be present and functional in the cell
*Statement:* The region scored beyond 326 must be part of the mature channel in the cell, and must
do something there. If it were spliced or cleaved away before use, its predicted confidence would be
biologically moot.

*Check:*
- **Mouse TREK-1 (heterologous expression):** Honoré, Maingret, Lazdunski & Patel 2002, *EMBO J*
  21:2968–2976, PMC126047 (read-level: full-text via automated summary). Deleting "the last 100
  amino acids in the C-terminal region" (Δ100) "almost completely abolished TREK-1
  mechano-sensitivity". Arachidonic acid "failed to affect" Δ100. FCCP-induced acidosis did not
  stimulate Δ100. The authors state the construct was mouse TREK-1. The species of Δ100 is implied,
  not stated.
- **Disagreement between sources, preserved:** a WUSTL abstract (read-level: search-summary; title
  "…analyses of gating thermodynamics and effects of deletions in the…", profiles.wustl.edu) reports
  that a further distal deletion (Δ334–411) removed voltage dependency but otherwise had no
  additional effect. Read together, the sources suggest the function-critical part is proximal
  (≈ residues 290–333, including E306 and the PKA site S333/S348). Residues far past ~340 appear
  more dispensable. That is my synthesis of the two sources, not a statement from either.
- **Zebrafish:** Nasr et al. 2018, *Sci Rep*, PMC6192994 (read-level: full-text via automated
  summary). They expressed zebrafish Kcnk2a and Kcnk2b in HEK-293 cells. Both were activated by
  stretch (inside-out, −80 mmHg: Kcnk2a 4064.6 ± 1239.4 pA; Kcnk2b 366.1 ± 59 pA), by intracellular
  acidification (Kcnk2a 79.1 → 428.8 pA, pH 7.2 → 5.2), and by 10 µM arachidonic acid (Kcnk2a 42.35
  → 304.70 pA/pF). Both are expressed in larval brain (ISH, 4 dpf). Kcnk2-like currents were seen in
  adult zebrafish cardiomyocytes. The paper gives **no construct lengths and no CTD analysis**.

**Verdict: open** for zebrafish, **satisfied** for mouse.
- *Mouse:* the CTD is present and required for stretch, AA and acid gating (Honoré 2002).
- *Zebrafish:* the channels show the same three responses. In mouse those responses depend on the
  CTD, so it is *plausible* the zebrafish CTD is functional. But that is a cross-species inference
  (mouse mechanism → zebrafish phenotype), and nobody I found has truncated a zebrafish Kcnk2 CTD.
  Scope of the negative: the Nasr 2018 full text, plus one web search for zebrafish kcnk2a/kcnk2b
  C-terminal constructs. That search returned Nasr 2018, Park et al. 2024 *Dev Dyn* (expression
  only; read-level: search-summary) and plasmid listings.
- Even in mouse, it is unresolved whether residues *beyond* ~326–340 matter for the claim. The
  function-critical segment overlaps the region that *does* have templates (D2).

### C2 — cell / `existence`: the region beyond 326 must be ordered in its native context
*Statement:* The claim says low Boltz2 confidence there reflects missing alignments "not disorder",
and it treats ESMFold2's 76.4 as the better reading. That requires the post-326 segment to be at
least partly ordered in the cell, for example as a membrane-associated helix or a partner-bound
segment. A measurement showing the native CTD to be intrinsically disordered would contradict the
"not disorder" half.

*Check:*
- Honoré 2002 (above): "the proximal C-terminal domain is likely to be composed of long stretches of
  α-helices". This is a **sequence prediction** (DNA Star), drawn as a helical wheel for G293–F310,
  i.e. *before* 326. It is not a measurement.
- UniProt P97438 (mouse) lists a "Helix 285–333" feature, and O95069 (human) lists "Helix 287–315".
  These come from deposited crystal structures (read-level: listing). They reach at most residue
  333, so the helix overlaps the first ~7 residues past 326 in mouse numbering. Nothing beyond 339 is
  structurally observed in any entry found in D2.
- Searched: "TREK-1 C-terminal domain intrinsically disordered NMR circular dichroism" (standard),
  and `"TREK-1" "C-terminal" "intrinsically disordered" K2P channel` (extended). Neither returned an
  NMR, CD, SAXS, HDX or cryo-EM measurement of the distal TREK-1/TREK-2 CTD in any species. The
  extended search did return reviews stating that no TREK-1 crystal structure resolves this part of
  the CTD, and that the CTD is a polymodal sensor (PIP2, pH, PLD2 binding). Those are read-level
  search-summary. Natale et al. 2021 *JMB* (K2P structure review) was listed but not opened. A
  2024 *Nat Commun* paper on coupling between the cytosolic sensor domain and the filter in TREK
  channels (s41467-024-48823-y) was **could-not-access** (publisher login redirect).
- MobiDB (disorder consensus) was refused by this session's egress proxy, so no disorder annotation
  was retrieved.

**Verdict: unsatisfied — as far as this search reaches, nobody has measured it.** I found no
measurement that the TREK distal CTD is ordered, and none that it is disordered. This is a
"nobody-has-looked (within my scope)" negative, **not** a "looked-and-found-nothing" negative. The
scope is two web searches, the UniProt feature tables for O95069 and P97438, and the Honoré 2002
full text. It is **not unsatisfiable**: no measured number contradicts order. Note one point
against reading crystal-structure absence as evidence of disorder: in these structures the residues
are absent because the *construct* was truncated (D2). Missing density therefore says nothing about
order here. That supports the claim's logic, but it is not evidence for order either.

## 2. Summary

| id | scale | kind | verdict | carries weight because |
|---|---|---|---|---|
| D1 | dna | range | satisfied (zebrafish predicted, human/mouse reviewed) | there is a CTD to score |
| D2 | dna | spatial | satisfied (to ~4%, numbering unknown) | structures end at 315–339 of 426–538 aa |
| D3 | dna | conservation | satisfied (existence only) | narrows the claim: "depth" must mean template depth unless MSA depth also falls |
| C1 | cell | existence | open (zebrafish) / satisfied (mouse) | function-critical CTD is mostly *proximal*, overlapping templated residues |
| C2 | cell | existence | unsatisfied (unmeasured) | "not disorder" has no direct measurement behind it |

No constraint is `unsatisfiable`. Nothing measured contradicts the claim from below. The most useful
result is D3: the claim's own evidence (PDB70) is template depth, but it names an MSA mechanism. The
claim should either show a per-column *sequence* MSA depth profile, or be reworded to "template
coverage".

## 3. Sources

- UniProt REST (rest.uniprot.org), entries and counts listed above — listing.
- PDBe SIFTS best_structures API for O95069, P97438, P57789, Q9NYG8 — listing.
- Honoré E, Maingret F, Lazdunski M, Patel AJ (2002) *EMBO J* 21:2968–2976, [PMC126047](https://pmc.ncbi.nlm.nih.gov/articles/PMC126047) — full-text (automated summary).
- Nasr N et al. (2018) *Sci Rep*, "Identification and characterization of two zebrafish Twik related potassium channels, Kcnk2a and Kcnk2b", [PMC6192994](https://pmc.ncbi.nlm.nih.gov/articles/PMC6192994/) — full-text (automated summary).
- WUSTL abstract on TREK-1 gating thermodynamics and C-terminal deletions, [profiles.wustl.edu](https://profiles.wustl.edu/en/publications/analyses-of-gating-thermodynamics-and-effects-of-deletions-in-the/) — search-summary.
- Park et al. (2024) *Dev Dyn*, TREK-family expression in zebrafish, [ZFIN](https://zfin.org/action/publication/ZDB-PUB-240126-2/all-figures) — search-summary.
- Natale et al. (2021) *JMB*, K2P structural review, [PDF](https://scvrb-core.ucsf.edu/~dminor/pdf/Natale_etal_JMB2021.pdf) — listing (not opened).
- *Nat Commun* (2024) s41467-024-48823-y — could-not-access.
- MobiDB, search.rcsb.org — could-not-access (egress proxy refused).

```swarm-entail
{"source_claim": 26, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "range",
      "statement": "The native coding sequence must encode a full-length protein that extends well beyond the last crystallised residue, so that a post-326 region exists to be scored",
      "quantity": "full-length protein length encoded by the native ORF", "lo": 327, "hi": null, "units": "amino acids",
      "status": "satisfied",
      "satisfied_by": "UniProt gene models: zebrafish kcnk2a 426/413 aa (F1QAI2, A0AB32T9G3), kcnk2b 425/384 aa (A0AB32TCH9, Q32LX0); human KCNK2 O95069 and mouse Kcnk2 P97438 426 aa (reviewed)",
      "satisfied_evidence": "literature",
      "note": "UniProt REST listing 2026-11-04. Zebrafish entries are unreviewed predictions; a 231-aa kcnk2b entry (A0AC58I4H9) not investigated; human isoform 4 replaces 233-426 (PMID 24196565, listing) - human only. Claim does not name its gene/species."},
    {"target_scale": "dna", "kind": "spatial",
      "statement": "The C-terminal end of deposited structures, set by truncated expression constructs, must coincide with the position where template depth collapses",
      "quantity": "last modelled residue of deposited TREK-subfamily structures (own UniProt numbering)", "lo": 300, "hi": 350, "units": "residue index",
      "status": "satisfied",
      "satisfied_by": "PDBe SIFTS: human TREK-1 4TWK ends 315; 25 mouse TREK-1 X-ray entries end 336-339; human TREK-2 entries end 335; all of 426-538-aa proteins",
      "satisfied_evidence": "literature",
      "note": "PDBe best_structures API listing; observed-residue ranges, not construct boundaries. Exact 326 not reproduced because the claim's query sequence/numbering is unknown. RCSB search refused by proxy, so absence of a full-length cryo-EM structure is not established."},
    {"target_scale": "dna", "kind": "conservation",
      "statement": "Homologous genome-derived sequences covering the post-326 region must exist in quantity (sequence supply does not collapse), so that the depth that falls to zero is template depth, not sequence depth",
      "quantity": "vertebrate KCNK2 UniProt entries long enough to contain the CTD", "lo": 1, "hi": null, "units": "sequences",
      "status": "satisfied",
      "satisfied_by": "UniProt: 609 of 762 vertebrate (taxon 7742) gene:kcnk2 entries are 400-600 aa",
      "satisfied_evidence": "literature",
      "note": "Database count (listing), not an alignment: per-column MSA depth and CTD alignability not computed. Implication (inference): if sequence MSA stays deep past 326, Boltz2's low score cannot be attributed to MSA depth; the claim should say template coverage."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "The region beyond the crystallised boundary must be present in the mature channel in the cell and contribute to its function",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "Mouse TREK-1: Delta100 C-terminal deletion almost abolishes stretch, arachidonic-acid and acidosis gating (Honore et al. 2002). Zebrafish Kcnk2a/b respond to stretch, pH and AA in HEK-293 (Nasr et al. 2018) but no zebrafish CTD truncation found.",
      "satisfied_evidence": "literature",
      "note": "Honore 2002 EMBO J PMC126047 (full-text) - MOUSE. Nasr 2018 Sci Rep PMC6192994 (full-text) - ZEBRAFISH, no construct lengths or CTD analysis. Satisfied for mouse; open for zebrafish (cross-species inference only). WUSTL abstract (search-summary) reports distal Delta334-411 affects only voltage dependence - function-critical CTD may be proximal, overlapping templated residues. Negative scope: Nasr full text + one web search for zebrafish kcnk2 C-terminal constructs."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "The post-326 segment must be at least partly ordered (e.g. membrane- or partner-associated secondary structure) in its native context, as the 'not disorder' reading requires",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "No measurement found either way. Only a sequence-based helix prediction for G293-F310 (Honore 2002) and crystallographic helix annotations ending at residue 333 (mouse P97438) / 315 (human O95069).",
      "satisfied_evidence": "unknown",
      "note": "Nobody-has-looked within scope, not looked-and-found-nothing. Scope: two web searches for TREK-1 CTD disorder/NMR/CD (standard + extended), UniProt feature tables O95069/P97438, Honore 2002 full text. Nat Commun 2024 s41467-024-48823-y could-not-access; MobiDB refused by proxy. Not unsatisfiable: no measured value contradicts order."}
  ]}
```
