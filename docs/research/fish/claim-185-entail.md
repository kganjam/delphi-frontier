# Claim 185 — entailment at the adjacent scale (`dna` → `protein`)

**Source claim (scale `dna`, evidence: measured).**
BUILD BLOCKER: every UniProt slc43a2a entry (Q7ZUS0, A0A8N7V006) and RefSeq NP_956545.1 are
153 aa — a truncated gene model that CANNOT carry a residue 200, so the T200K substitution is
unrepresentable in the databases anyone would reach for first. Only Ensembl GRCz11 has the
full-length product.

**Adjacent scale propagated to:** `protein`.

**Date of checks:** 2026-11-04. All database reads below were made on that date against live
endpoints (UniProt REST, NCBI E-utilities). Record contents change; re-read before relying on them.

## Access limitation, stated up front

The claim's own carve-out — "only Ensembl GRCz11 has the full-length product" — is the one
assertion I could **not** verify. `rest.ensembl.org` and `jun2026.archive.ensembl.org` do not
resolve from this session (outside its allowed network domains), and `zfin.org` returned HTTP 503.
Read-level for the Ensembl full-length product: **could-not-access**. Nothing below should be read
as confirming or denying that a full-length Ensembl model exists. To close constraint C2 these hosts
have to be allowed in the session's network settings.

---

## 1. ENTAIL — what claim 185 requires at `protein`

| id | kind | requirement |
|----|------|-------------|
| C1 | range | The product length annotated on the records a reader reaches first must be **< 200 aa**, or the numbered position is representable after all and there is no blocker. |
| C2 | existence | Some record of this gene product, in some database, must be **≥ 200 aa** — otherwise residue 200 has no referent anywhere at protein scale, and the substitution is not merely unrepresentable but undefined. |
| C3 | spatial | Any record offered as the *functional* product must match the length of its 12-TM SLC43/LAT-family orthologues **within a factor ≈1.3** (i.e. ratio in 0.75–1.3), because a facilitator of this family must thread the bilayer ~12 times; a record far below that cannot be the transporter, only a fragment of it. |
| C4 | conservation | Residue numbering must be **convertible** between the short record and the full-length product — the short record must be a colinear prefix (offset 0) of the long one — or "residue 200" cannot be located by any reader holding only the short record. |

C1, C3 and C4 are checkable against measured numbers with no simulation. C2 is an existence
requirement and is the one that needed the blocked host.

---

## 2. CHECK — each constraint

### C1 — range: primary records must be < 200 aa — **satisfied**

Measured, read-level **full-text (primary record, fetched via API)**:

| record | source | length |
|---|---|---|
| Q7ZUS0 (`Q7ZUS0_DANRE`, GN=slc43a2a, PE=2) | UniProt REST `/uniprotkb/Q7ZUS0.fasta` | **153 aa** |
| A0A8N7V006 (`A0A8N7V006_DANRE`, GN=slc43a2a, PE=4) | UniProt REST | **153 aa** |
| NP_956545.1 | NCBI E-utilities efetch, protein db | **153 aa** |

The three sequences are **byte-identical** (string comparison of the fetched sequences; my own
check, trivially reproducible). All begin `MAPTLATAFSRRWWMAITAVIENLLFSAVLLGWGSLLIML…` and end
`…SVTRTASVQLYYQ`.

Corroborating transcript-level measurement, read-level **full-text (GenBank record NM_200251,
LOCUS line dated 24-AUG-2026)**: the mRNA is 3230 bp with `CDS 175..636` — 462 nt = 153 codons plus
stop — inside a final exon `584..3214`. So the annotated coding sequence stops 52 nt into a
2631-nt terminal exon.

A 153-residue sequence cannot carry a residue 200. The claim's core arithmetic holds as stated,
for all three accessions it names.

*Derived (my computation, not an observation):* translating NM_200251 from the annotated start
codon through the stop gives a genuine in-frame stop at codon 154; and in the three frames
downstream of position 636 the longest stop-free stretch is 184 aa (frame +2), 86 aa (+0) and
85 aa (+1). None is long enough to append the ~420 residues that would bring the product to
orthologue length. **Inference (mine, not NCBI's):** the truncation in this RefSeq entry is not a
mis-called start/stop that could be rescued by re-reading NM_200251 in another frame; closing the
gap requires a *different transcript model*, not a different CDS call on this one.

### C2 — existence: some ≥ 200 aa record must exist — **open**

What I searched, and the scope of each negative:

- **UniProtKB**, query `gene:slc43a2a AND organism_id:7955`, all entries, reviewed and unreviewed:
  **2 hits, both 153 aa** (Q7ZUS0, A0A8N7V006). Widening to `gene:slc43a2*` returns the paralog
  slc43a2b at 592 aa (Q5PR35, A0A8M1N3P6) and 598 aa (A0ACD6B803) — full-length, but a *different
  gene*, not a record of slc43a2a. Read-level: full-text (API result set).
- **NCBI Protein**, query `slc43a2a[Gene Name] AND "Danio rerio"[Organism]`: **Count = 1**,
  NP_956545 (153 aa). No `XP_` predicted protein of any length. Read-level: full-text (esearch +
  esummary).
- **NCBI Gene 393221** (`slc43a2a`, chromosome 15): the record lists exactly one RefSeq protein
  (NP_956545) and one RefSeq mRNA (NM_200251) while being annotated on four assemblies —
  **GRCz11, GRCz12ab, GRCz12tu, GRCz13ab**. So the 153-aa model is not a GRCz11-era leftover that
  newer assemblies fixed; it is the current NCBI product across all four. Read-level: full-text
  (gene XML).
- **Ensembl**: **could-not-access** (DNS refusal on `rest.ensembl.org` and
  `jun2026.archive.ensembl.org`; `zfin.org` 503).

So: *people have looked and found nothing ≥ 200 aa in UniProt or NCBI* — a positive negative with a
stated scope. That is different from the Ensembl question, where **nobody here has been able to
look at all**.

One weak, non-primary signal, read-level **search-summary** (a web-search engine's summary of a
ZFIN page I could not open myself, so it may be wrong and is not a record read): ZFIN is said to
list Ensembl transcripts `slc43a2a-201` at 2011 nt and `slc43a2a-202` at 2101 nt. **Inference
(mine, not ZFIN's):** a 2011-nt transcript is long enough *in principle* to carry a ~570-aa CDS
(1710 nt), so the claim's carve-out is not arithmetically impossible — but transcript length is not
protein length, and this does not establish that a ≥ 200-aa translation is annotated. C2 stays
`open`. Marking it `satisfied` on this basis is exactly the move this structure exists to catch.

### C3 — spatial: functional product must be within ~1.3× of orthologue length — **unsatisfiable for the primary records**

Measured, read-level **full-text (UniProt records and their feature tables)**:

| record | length | annotated transmembrane helices | ratio to orthologue (569–592 aa) |
|---|---|---|---|
| SLC43A2 human, Q8N370 (`LAT4_HUMAN`) | 569 aa | **12** | 1.00 (reference) |
| slc43a2b zebrafish, Q5PR35 | 592 aa | **12** | 1.04 |
| slc43a2b zebrafish, A0A8M1N3P6 | 592 aa | **12** | 1.04 |
| **slc43a2a zebrafish, Q7ZUS0** | **153 aa** | **2** (12–39, 94–115) | **0.27** |

Measured 153 aa against a required window of roughly 427–770 aa (0.75–1.3 × 569–592) contradicts
the constraint: 0.27× is outside it by a wide margin, and 2 annotated TM helices out of 12 says the
same thing independently of any length arithmetic. The 153-aa record is therefore **refuted as the
functional transporter** from below, with no simulation.

Direction of this result: it **refutes the records, not the claim**. Claim 185 predicts precisely
this — a truncated gene model — and C3 is the measurement that converts "153 aa" from a number into
a diagnosis. If instead the 153-aa record had come in near orthologue length, claim 185 would have
been in trouble.

### C4 — conservation: numbering must be convertible between the records — **unsatisfied**

Measured, read-level **full-text (UniProt feature tables)**: TM1 is annotated at **12–39** in both
Q7ZUS0 and slc43a2b — identical coordinates, so the two are in register at the N-terminus. But TM2
is annotated at **94–115** in Q7ZUS0 versus **116–137** in slc43a2b: a ~22-residue displacement
already present *within* the 153 residues the short record does cover.

**Inference (mine; UniProt asserts the coordinates, not this conclusion):** the short model's
numbering is not a simple colinear prefix of a full-length SLC43 numbering even over its own
length, so a reader holding only the 153-aa record cannot locate "residue 200" by extrapolating or
offsetting. The position is defined only inside whichever full-length model is used, and that model
must be named whenever T200K is written down.

Scope of the negative: I found no mapping, alias table, or isoform cross-reference from the 153-aa
numbering to any ≥ 200-residue numbering in UniProt's cross-references for Q7ZUS0 (which list only
RefSeq NP_956545.1 / NM_200251.2 and ZFIN ZDB-GENE-040426-964 — no Ensembl protein xref, no
`Non-terminal residue` feature, and **no `CAUTION` comment flagging the truncation**). Whether
Ensembl's model supplies such a mapping is unchecked — see the access limitation.

---

## Net effect on claim 185

The checkable part of the claim is **confirmed by measurement**: three primary records, all
153 aa, all byte-identical, with a transcript model (NM_200251) whose annotated CDS stops at
codon 154 and which no reframing can extend to a residue 200; and a family-length/topology
comparison that marks the 153-aa product as a fragment carrying 2 of 12 TM helices. A further
measured finding the claim does not mention, and which strengthens it: the 153-aa product is
NCBI's current annotation on **GRCz12ab, GRCz12tu and GRCz13ab as well as GRCz11**, so this is not
a stale-assembly artifact. Two findings that weaken the record set rather than the claim: UniProt
carries **no** `CAUTION` or `Non-terminal residue` flag warning a user that the entry is truncated.

The claim's exclusivity clause ("only Ensembl GRCz11 has the full-length product") remains
**unverified in both directions** here. Any downstream use of T200K must name the model and the
numbering it is relative to; it is not safe to write "slc43a2a T200K" unqualified.

```swarm-entail
{"source_claim": 185, "source_scale": "dna",
  "constraints": [
    {"target_scale": "protein", "kind": "range",
      "statement": "The product length annotated on the protein records a reader reaches first must be below the numbered residue position, or the substitution is representable and there is no blocker.",
      "quantity": "annotated product length", "lo": 1,
      "hi": 199, "units": "aa",
      "status": "satisfied",
      "satisfied_by": "UniProt Q7ZUS0 = 153 aa, UniProt A0A8N7V006 = 153 aa, RefSeq NP_956545.1 = 153 aa; all three sequences byte-identical. RefSeq mRNA NM_200251 is 3230 bp with CDS 175..636 = 153 codons.",
      "satisfied_evidence": "measured",
      "note": "UniProt REST /uniprotkb/{acc}.fasta and NCBI E-utilities efetch (protein, nuccore), read 2026-11-04, read-level full-text (primary records). NM_200251 LOCUS line dated 24-AUG-2026. Separate DERIVED result, my own translation and not an observation: the CDS ends at a genuine in-frame stop at codon 154, and the longest stop-free stretch downstream of position 636 is 184 aa (frame +2), 86 aa (+0), 85 aa (+1) -- none long enough to extend the product to orthologue length, so the truncation cannot be rescued by re-calling the CDS on this transcript."},

    {"target_scale": "protein", "kind": "existence",
      "statement": "A protein record of the same gene product must exist in some database with length at least the numbered residue position, or that residue has no referent at protein scale anywhere.",
      "quantity": "length of the longest available record of this gene product", "lo": 200,
      "hi": null, "units": "aa",
      "status": "open",
      "satisfied_by": "Not found in the two databases I could reach, and the database the claim credits could not be reached. UniProtKB query 'gene:slc43a2a AND organism_id:7955' returns 2 entries, both 153 aa. NCBI Protein 'slc43a2a[Gene Name] AND Danio rerio[Organism]' returns Count=1 (NP_956545, 153 aa), no XP_ model. NCBI Gene 393221 lists one RefSeq protein across GRCz11, GRCz12ab, GRCz12tu and GRCz13ab. Ensembl GRCz11, the claim's named exception, was unreachable.",
      "satisfied_evidence": "unknown",
      "note": "Searched 2026-11-04. Negative scope: UniProtKB (all entries, reviewed+unreviewed, gene-name query) and NCBI Protein/Gene (gene-name-indexed) -- people have looked and found nothing >=200 aa for slc43a2a; the zebrafish paralog slc43a2b is full length (Q5PR35 592 aa, A0ACD6B803 598 aa) but is a different gene. Nobody has been able to look at Ensembl from here: rest.ensembl.org and jun2026.archive.ensembl.org do not resolve (outside this session's allowed network domains) and zfin.org returned HTTP 503 -- read-level could-not-access; those hosts must be allowed to close this. Weak non-primary signal at read-level search-summary (a search engine's summary of a ZFIN page I could not open): ZFIN reportedly lists Ensembl transcripts slc43a2a-201 at 2011 nt and slc43a2a-202 at 2101 nt. MY INFERENCE, not ZFIN's: 2011 nt could in principle carry a ~570 aa CDS (1710 nt), so the carve-out is not arithmetically impossible -- but transcript length is not protein length and this does not establish an annotated >=200 aa translation, so the constraint stays open rather than satisfied."},

    {"target_scale": "protein", "kind": "spatial",
      "statement": "Any record offered as the functional member of this 12-transmembrane transporter family must match its orthologues' length within a factor of about 1.3, since the fold must thread the bilayer roughly twelve times; a record far below that is a fragment, not the transporter.",
      "quantity": "ratio of record length to 12-TM orthologue length (569-592 aa)", "lo": 0.75,
      "hi": 1.3, "units": "dimensionless",
      "status": "unsatisfiable",
      "satisfied_by": "Measured contradiction: Q7ZUS0 is 153 aa with 2 annotated transmembrane helices (12-39, 94-115), i.e. ratio 0.27 against human SLC43A2 Q8N370 (569 aa, 12 TM helices) and zebrafish paralog slc43a2b Q5PR35 / A0A8M1N3P6 (592 aa, 12 TM helices). 0.27 lies far outside 0.75-1.3, and 2 of 12 helices contradicts the topology requirement independently of length arithmetic.",
      "satisfied_evidence": "measured",
      "note": "UniProt REST, fields length and ft_transmem, read 2026-11-04, read-level full-text (primary records and their feature tables). This refutes the 153-aa RECORDS as the functional protein, not claim 185 -- the claim predicts exactly this truncation, and the measurement is what turns '153 aa' into the diagnosis 'fragment'. Reported as unsatisfiable because a measured number contradicts the stated window, as required; if the record had come in near 569-592 aa the claim would instead have been in trouble."},

    {"target_scale": "protein", "kind": "conservation",
      "statement": "Residue numbering must be convertible between the truncated record and the full-length product -- the short record must be a colinear prefix of the long one -- or the numbered residue cannot be located by a reader holding only the short record.",
      "quantity": "numbering offset between truncated and full-length product", "lo": 0,
      "hi": 0, "units": "residues",
      "status": "unsatisfied",
      "satisfied_by": "No mapping found. Measured: UniProt annotates TM1 at 12-39 in BOTH Q7ZUS0 and slc43a2b (in register at the N-terminus), but TM2 at 94-115 in Q7ZUS0 versus 116-137 in slc43a2b -- a ~22-residue displacement arising within the 153 residues the short record covers. MY INFERENCE (UniProt asserts the coordinates, not this conclusion): the short model's numbering is not a colinear prefix of a full-length SLC43 numbering even over its own length, so residue 200 cannot be reached by offsetting from the truncated record and is defined only inside whichever full-length model is named.",
      "satisfied_evidence": "measured",
      "note": "UniProt REST ft_transmem and cross-references for Q7ZUS0, read 2026-11-04, read-level full-text. Negative scope: Q7ZUS0's cross-references list only RefSeq NP_956545.1 / NM_200251.2 and ZFIN ZDB-GENE-040426-964 -- no Ensembl protein cross-reference, no 'Non-terminal residue' feature, and no CAUTION comment warning that the entry is truncated, so nothing in the entry supplies or points to a numbering map. Whether Ensembl's model supplies one is unchecked: see the could-not-access note on constraint 2."}
  ]}
```
