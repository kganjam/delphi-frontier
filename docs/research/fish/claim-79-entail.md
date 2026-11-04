# Claim 79 → protein: what must be true one scale up, and is it?

**Source claim (dna, evidence: measured), in its author's words:**

> The gene symbol `lat4a` used by Daane et al. does not resolve in UniProtKB or NCBI Gene for
> Danio rerio. Four positive controls (kcnh2a, slc43a2a, slc43a2b, kcnk5b) all resolved with the
> same query form, so the zero is a real absence and not a malformed query.

**Result in one line.** All four protein-scale constraints are **satisfied** today. Nothing measured
contradicts the claim from above. There was one new finding along the way. UniProtKB *did* hold a
full-length (571 aa) zebrafish slc43a2a protein, **F1Q5Y9**, from 2011 until it was **deleted on
14 Dec 2022**. So the protein-coverage gap reported in challenge 79 and replication 82 dates from
2022: it did not exist when Daane et al. ran their analysis (Ensembl BioMart, Jan 2020) or published
(2021). F1Q5Y9 never carried `lat4a` in any of its 61 versions, so the claim itself is unaffected.

All live queries below were run by me on **2026-11-04**. A database count is *measured*. A residue
read off a sequence by its index is also *measured*, because the index is trivial. Anything that is
*inference* is labelled as inference in the sentence that states it.

## Why only `existence` and `range`

Claim 79 is a statement about **nomenclature**: a string is absent from two databases. Going up to
protein, that can only entail facts about protein **records**: which ones exist, what they are
called, and what sequence they hold. It entails nothing about rates, length scales, energy or
mass/charge balance. So I have written no `timescale`, `spatial`, `energetic` or `conservation`
constraint. Inventing one would be manufacturing structure the claim does not carry. The one
quantitative constraint the claim supports is a `range` on protein length (C3).

C1 and C2 follow from claim 79 alone. C3 and C4 are **conditional**. They hold only if `lat4a`
refers to a real zebrafish protein, as Daane et al. assert. Claim 79 presupposes that when it
calls the zero an absence *of a symbol* and not of a gene. If that presupposition is dropped,
C3 and C4 lapse; they do not fail.

## The constraints and the checks

### C1 · existence: each control symbol must resolve to at least one *D. rerio* protein record

For the controls to show that "the query form works" at protein scale, each one must hit a protein
entry in UniProtKB with the same query form that gives 0 for `lat4a`.

**Satisfied (measured).** UniProtKB REST, `gene:<sym> AND organism_id:7955`:

| control | hits (first entries) |
|---|---|
| kcnh2a | Q108P2 (1253 aa), A0A8M1N8U2, A0AC58H0R3, A0AC58H0T1, A0AC58H0S7 |
| kcnk5b | Q6PFU3 (448 aa), A0A8M1PBI1 |
| slc43a2a | Q7ZUS0 (153 aa), A0A8N7V006 (153 aa) |
| slc43a2b | Q5PR35 (592 aa), A0A8M1N3P6 (592 aa), A0ACD6B803 (598 aa) |

NCBI Gene, `<sym>[Gene Name] AND "Danio rerio"[Organism]`, gives 563802, 393221, 494042 and 393606,
the same IDs challenge 79 found. Challenge 79 also tested alias-only controls (`lat3a` → F2Z4V7
slc43a1a; `zgc:56271` → 393221), so the query form is known to search synonyms as well. I re-saw
`lat3a` among F2Z4V7's gene names today (read-level: listing).

### C2 · existence (negative): no *D. rerio* protein record may carry `lat4a` as a gene name, synonym, ORF name or protein name

This is the claim's own content seen at protein scale. It must hold in current records. It is
stronger if it also held in the history of the record that actually held the protein.

**Satisfied (measured), with this scope:**

- UniProtKB, current release: `lat4a AND organism_id:7955` → **0**. `protein_name:lat4 AND
  organism_id:7955` → **0**. Unrestricted `lat4a` → 2 entries, both outside the zebrafish:
  Q1ELU5 (*Lachesana tarabaevi*, a spider toxin "M-zodatoxin-Lt4a / Latarcin-4a") and A0A9P6H1T5
  (*Nosema granulosis*, gene `LAT4A`). Neither is a homonym clash within *Danio*.
- NCBI Protein: `lat4a[All Fields] AND "Danio rerio"[Organism]` → **0**. NCBI Gene,
  `lat4a[Gene Name] …` → **0** (re-confirmed).
- UniSave, all 61 archived versions of F1Q5Y9 (the deleted full-length slc43a2a, see C3). Gene-name
  lines over its lifetime: `OTTDARG00000028150`, `Dr.13039`, `slc43a2a`. The only "lat4"
  string anywhere in its history is the InterPro family line `IPR027201; LAT4.` That is a family
  label, not a gene symbol or synonym.
- **Not searched:** ZFIN (TLS to zfin.org failed through this container's proxy: curl exit 60), and
  Ensembl (`rest.ensembl.org` refused by the egress proxy, `connect_rejected`). So whether ZFIN
  lists `lat4a` as a previous name is still **unknown**, as challenge 79 also found. This is a
  "nobody here could look" gap. It is not a "looked and found nothing" result.

### C3 · range: the protein the paper calls Lat4a must be at least 326 residues long

Daane et al. number a substitution F326L in Lat4a (and T200K). Any protein their numbering refers to
must therefore be ≥ 326 aa. I set no upper bound: the claim does not imply one, and I will not
invent one. For orientation only (these are not bounds), related lengths are: human LAT4 Q8N370
569 aa (from replicate-82), and zebrafish slc43a2b 592/598 aa (measured above).

**Satisfied (measured), with a disagreement between databases recorded below.**

- **Ensembl ENSDARP00000120945** (gene slc43a2a, ENSDARG00000036848) is **571 aa**. I submitted the
  sequence cached in this repo (`origin/work/genomics:data/genomics/artifacts/ensembl_protein_ENSDARP00000120945.fasta`)
  to UniParc's exact-sequence lookup. It returned **UPI000188A62B**, with the Ensembl cross-reference
  ENSDARP00000120945 marked `active: true`, `lastUpdated 2026-03-30`, `geneName slc43a2a`.
  So the cached sequence is confirmed live as the current Ensembl protein, by a route that does not
  need rest.ensembl.org. Read-level: full-text (record).
- The same UniParc entry lists **UniProtKB/TrEMBL F1Q5Y9**, `active: false`. UniProtKB gives the
  reason: `inactiveReasonType: DELETED`, "Deleted from sequence source (ENSEMBL)". UniSave shows it
  was integrated on 03-May-2011, held a 571-aa sequence (CRC64 C3433781EF6CD87C) in every version,
  and was last released as v61 on 14-Dec-2022. Versions 52–57 span 11-Dec-2019 to 29-Sep-2021,
  so it was live through the paper's BioMart date and its publication. Read-level: full-text (records).
- **Disagreement, preserved.** The *current* UniProtKB (Q7ZUS0, A0A8N7V006) and RefSeq
  (NP_956545.1, the only NCBI Protein hit for `slc43a2a[Gene Name]` in *D. rerio*; esummary says
  `slen 153`, updated 2026/08/24) all give **153 aa**. My comparison of Q7ZUS0 with
  ENSDARP00000120945 shows they are identical over residues 1–139 and diverge from residue 140.
  That matches replicate-82's comparison against its own miniprot model.
- Why this does **not** make C3 unsatisfiable: a 153-aa record is a measured *record length*. It is
  not a measurement that the protein *is* 153 aa. NP_956545.1 is flagged PROVISIONAL (replicate-82).
  The full-length model is supported by a live Ensembl record and independently by replicate-82's
  computed miniprot reconstruction (572 aa). Two other points are database curation facts, not
  biology: UniProt says F1Q5Y9 was deleted *because Ensembl dropped it*, yet UniParc shows the same
  Ensembl protein ID active today. **Those two statements conflict, and I cannot resolve that from
  here.** Possible explanations (my inference, untested): the protein was removed from Ensembl and
  later restored, or UniProt's Ensembl import excluded it on grounds other than its existence.

### C4 · existence: the referent protein must carry the paper's wild-type residues at its numbered positions (T at 200, F at 326)

If `lat4a` is a real but non-standard name, the only route from the paper to a protein record is by
sequence and position, not by symbol. That route must land on a protein whose residue 200 is T and
whose residue 326 is F.

**Satisfied (measured on the record), by ENSDARP00000120945 / UPI000188A62B:** residue 200 = **T**,
residue 326 = **F** (1-based, read directly off the 571-aa sequence). The paralogue slc43a2b
(Q5PR35) has M200 / D326 (replicate-82, measured), so the residues tell the two paralogues apart.
None of the *current* UniProtKB or RefSeq slc43a2a records can host either position (153 < 200).
So C4 is satisfied **only** via Ensembl/UniParc and the deleted F1Q5Y9. My inference, not the
authors' statement: the paper does not cite a protein accession (replicate-82, full-text negative),
so I cannot confirm that ENSDARP00000120945 is the exact record Daane et al. numbered against. It
is the only public record I found that fits both positions.

## Scope of negatives, collected

- `lat4a` absence: UniProtKB (current, Swiss-Prot + TrEMBL), NCBI Gene, NCBI Protein, UniSave history
  of F1Q5Y9. *D. rerio* only, apart from the unrestricted UniProt query noted in C2.
- Not reachable: ZFIN, Ensembl REST. Status for both: **unknown**.
- Live databases change. Everything here holds as of 2026-11-04. The F1Q5Y9 deletion shows the
  facts can move.

## Sources and read-levels

| source | used for | read-level |
|---|---|---|
| UniProtKB REST search (2026-11-04) | C1, C2, C3 | full-text (records/listings) |
| UniParc `/uniparc/sequence` for the 571-aa sequence → UPI000188A62B | C3, C4 | full-text (record) |
| UniProtKB F1Q5Y9 (inactive entry) and UniSave v1–v61 | C2, C3 | full-text (records) |
| NCBI E-utilities esearch/esummary (gene, protein) | C1, C2, C3 | full-text (records) |
| `docs/research/fish/challenge-79.md` (commit e9747f72) | alias controls, prior ZFIN/Ensembl failure | full-text |
| `docs/research/fish/replicate-82.md` (commit 8ad18d0f) | human LAT4 length, slc43a2b residues, miniprot model, PROVISIONAL flag, paper has no accession | full-text |
| Daane et al. 2021, *Curr Biol*, doi:10.1016/j.cub.2021.08.054 | T200K, F326L numbering (as quoted in challenge-79 and replicate-82) | not re-read by me; inherited from those two documents, which read it full-text |
| ZFIN | — | could-not-access |
| Ensembl REST | — | could-not-access |

```swarm-entail
{"source_claim": 79, "source_scale": "dna",
  "constraints": [
    {"target_scale": "protein", "kind": "existence",
      "statement": "Each positive-control symbol must resolve, under the same query form that returns zero for lat4a, to at least one Danio rerio protein record",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "UniProtKB gene:<sym> AND organism_id:7955 returns kcnh2a->Q108P2, kcnk5b->Q6PFU3, slc43a2a->Q7ZUS0/A0A8N7V006, slc43a2b->Q5PR35/A0A8M1N3P6/A0ACD6B803; NCBI Gene IDs 563802, 393606, 393221, 494042",
      "satisfied_evidence": "measured",
      "note": "Live UniProtKB REST and NCBI E-utilities, 2026-11-04. Alias-only controls (lat3a->F2Z4V7, zgc:56271->393221) from challenge-79.md show the query form searches synonyms."},
    {"target_scale": "protein", "kind": "existence",
      "statement": "No Danio rerio protein record, current or archived for the locus, may carry the string as a gene name, synonym, ORF name or protein name",
      "quantity": "number of D. rerio protein records naming lat4a", "lo": 0, "hi": 0, "units": "records",
      "status": "satisfied",
      "satisfied_by": "0 hits: UniProtKB lat4a AND organism_id:7955; UniProtKB protein_name:lat4 AND organism_id:7955; NCBI Protein lat4a[All Fields] AND Danio rerio; NCBI Gene lat4a[Gene Name]. All 61 UniSave versions of F1Q5Y9 have gene names only OTTDARG00000028150, Dr.13039, slc43a2a; the only 'LAT4' string is the InterPro family line IPR027201",
      "satisfied_evidence": "measured",
      "note": "Scope: UniProtKB current + UniSave history of F1Q5Y9, NCBI Gene, NCBI Protein; D. rerio. Unrestricted UniProt lat4a hits only Q1ELU5 (Lachesana tarabaevi) and A0A9P6H1T5 (Nosema granulosis). ZFIN and Ensembl not reachable from this container: unknown, not negative."},
    {"target_scale": "protein", "kind": "range",
      "statement": "Conditional on lat4a naming a real zebrafish gene: the protein the paper numbers (F326L, T200K) must be at least as long as its highest numbered residue",
      "quantity": "length of the referent protein", "lo": 326, "hi": null, "units": "amino acids",
      "status": "satisfied",
      "satisfied_by": "Ensembl ENSDARP00000120945 (slc43a2a), 571 aa, confirmed live via UniParc UPI000188A62B (Ensembl xref active, lastUpdated 2026-03-30); same sequence was UniProtKB F1Q5Y9 from 2011-05-03 until deleted 2022-12-14 ('Deleted from sequence source (ENSEMBL)')",
      "satisfied_evidence": "measured",
      "note": "Disagreement preserved: current UniProtKB Q7ZUS0/A0A8N7V006 and RefSeq NP_956545.1 (PROVISIONAL) are 153 aa, identical to the 571-aa protein over residues 1-139, then divergent. A truncated record length does not measure the protein's length, so this is not a contradiction. UniProt's deletion reason conflicts with UniParc's 'active' Ensembl xref; unresolved. Independent computed support: replicate-82 miniprot model, 572 aa."},
    {"target_scale": "protein", "kind": "existence",
      "statement": "Conditional on lat4a naming a real zebrafish gene: a public protein record reachable without the symbol must carry the paper's wild-type residues at the paper's positions (T at 200, F at 326)",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "ENSDARP00000120945 / UPI000188A62B residue 200 = T, residue 326 = F; paralogue slc43a2b Q5PR35 has M200/D326; no current UniProtKB or RefSeq slc43a2a record can host either position (153 aa)",
      "satisfied_evidence": "measured",
      "note": "Residues read directly off the UniParc-confirmed sequence. Daane et al. 2021 (doi:10.1016/j.cub.2021.08.054) give no protein accession (replicate-82, full-text negative), so it is inference, not author statement, that this is the record they numbered against."}
  ]}
```
