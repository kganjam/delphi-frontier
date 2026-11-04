# Replicate 90 — independent re-derivation for "Correction to claim 82"

Date of all queries: 2026-11-04. Target: the length of NCBI RefSeq protein NP_956545.1
(zebrafish `slc43a2a`), i.e. whether a residue numbered 200 exists in the sequence that
claim 82 proposes numbering a T200K substitution against.

## Independence disclosure

I did not open `docs/research/fish/challenge-82.md` and have not read the prior working.
I did run `git show --stat` on the branch `claude/slc43a2a-t200k-numbering-b2ak09` to locate
that file, and the **commit message** printed in that output stated the prior conclusion
before I had derived mine. So my derivation is not blind: I had seen the recorded number.
I report that rather than claim independence I do not have. The inputs below are nonetheless
fetched directly from NCBI, and the residue count is one I computed myself from the sequence;
none of it is copied from the prior document. Weight the agreement at the end accordingly —
it is a confirmation that the fetch reproduces, not two independent derivations.

## My value

**153 amino acids (exact, no uncertainty).** Therefore position 200 does not exist in
NP_956545.1, and "number T200K against NP_956545.1" has no residue to refer to.

The count is exact rather than estimated: a RefSeq protein record is a fixed string, and the
versioned accession (`.1`) pins the string. The only uncertainty is whether NP_956545.1 is the
right referent at all, not how long it is — see Caveats.

## Inputs, each with source and read-level

| Input | Value | Source | Read-level |
|---|---|---|---|
| `NP_956545.1` sequence | 153-residue string (below) | NCBI E-utilities efetch, `db=protein`, `rettype=fasta` | full-text |
| `NP_956545.1` declared length | `153 aa` on the LOCUS line | NCBI efetch, `rettype=gp` (GenPept) | full-text |
| Protein feature span | `Protein 1..153` | same GenPept record | full-text |
| CDS span on transcript | `/coded_by="NM_200251.2:175..636"` | same GenPept record | full-text |
| Gene identity | `/gene="slc43a2a"`, `db_xref=GeneID:393221`, `db_xref=ZFIN:ZDB-GENE-040426-964` | same GenPept record | full-text |
| Record status | `PROVISIONAL REFSEQ`, derived from `BC047854.1` | same GenPept record, COMMENT block | full-text |
| RefSeq proteins of GeneID 393221 | exactly one protein UID, `41053786` | NCBI elink, `dbfrom=gene&db=protein&linkname=gene_protein_refseq` | full-text (JSON) |
| UID 41053786 identity + length | `NP_956545.1`, `slen=153` | NCBI esummary, `db=protein` | full-text (JSON) |
| Ensembl / ZFIN cross-check | not attempted this session | — | could-not-access (not attempted) |
| UniProt cross-check | not attempted this session | — | could-not-access (not attempted) |

Sequence as retrieved (FASTA body, line breaks as returned):

```
MAPTLATAFSRRWWMAITAVIENLLFSAVLLGWGSLLIMLKSEGFYSYLCREAGNGTGHNVSESENGTMN
ATRLEEEDNLQMNGWPICKEQDEMLNLAFTIGSFLLSAITLPLGIIMDKYGPRKLRLLGSASFAISCILN
SVTRTASVQLYYQ
```

## The arithmetic in full

Line lengths of the FASTA body, counted after stripping the `>` header and newlines:

- line 1: 70
- line 2: 70
- line 3: 13

70 + 70 + 13 = **153**.

Computed, not observed: I ran `len()` on the concatenated, whitespace-stripped string in
Python and got 153, which matches the hand sum above and matches the two numbers NCBI itself
asserts (`153 aa` on the LOCUS line; `slen: 153` in esummary). Three routes, one value.

Positional check for the claim's wild-type residue. Threonine (`T`) occurs at exactly these
1-based positions in NP_956545.1 (computed by enumerating the string):

```
4, 7, 18, 57, 68, 72, 100, 110, 143, 145
```

Ten threonines, the last at 145. 200 > 153, so:

- 200 − 153 = 47 residues past the C-terminus.
- No residue 200 exists, hence no Thr200 exists, hence `T200K` is unnumberable against this
  sequence. This last step is **my inference**, not something NCBI states; what NCBI states is
  the length and the sequence.

Transcript-level consistency check (my inference from the record's own fields, not an
independent observation): the CDS is annotated as `NM_200251.2:175..636`.

- 636 − 175 + 1 = 462 nt of CDS.
- 462 / 3 = 154 codons.
- 154 − 1 stop codon = **153 translated residues.**

So the CDS coordinates and the protein length agree. A protein long enough to carry residue 200
would need at least 200 × 3 + 3 = 603 nt of CDS; the annotated CDS is 462 nt, i.e. 141 nt short.

## Caveats and scope of the negative

The negative finding is: **no residue 200 exists in NP_956545.1.** Its scope is that one
versioned RefSeq accession. Stated precisely, with what is and is not covered:

1. Covered: RefSeq protein NP_956545.1, and the single RefSeq protein that NCBI elink returns
   for GeneID 393221 — which is that same accession. Within RefSeq, GeneID 393221 has no
   second, longer protein isoform that could rescue a position-200 numbering.
2. Not covered: Ensembl, ZFIN, UniProt, and any unannotated or newer longer isoform. I did not
   query them in this session, so I cannot say whether some other database holds a longer
   zebrafish `slc43a2a` product in which a residue 200 exists. Read-level for those:
   could-not-access (not attempted). This is a real gap, not a formality — SLC43A2 orthologues
   in other vertebrates are ~500+ aa, so a 153-aa zebrafish product is short for the family
   and invites the question whether the RefSeq entry is partial.
3. The record itself flags its own provisional status: `PROVISIONAL REFSEQ: This record has not
   yet been subject to final NCBI review`, derived from a single cDNA, `BC047854.1`, with
   `RNAseq introns :: partial sample support`. That is NCBI's statement, quoted. My inference
   from it: the 153-aa length is an annotation that could change in a future version, so the
   finding is properly stated as a fact about `NP_956545.1` specifically rather than about
   zebrafish `slc43a2a` as a biological entity.
4. Disagreement I am preserving rather than resolving: the family-size expectation in (2) and
   the provisional flag in (3) both point the same way — toward the possibility that the true
   protein is longer than this record — while the record's internal evidence (LOCUS, Protein
   feature, CDS coordinates, esummary, elink's single hit) is entirely self-consistent at 153.
   Both things are true at once. The claim's instruction is defeated as written either way,
   because it names a sequence in which position 200 is absent; but "position 200 is absent
   from this accession" and "zebrafish slc43a2a has no residue 200" are not the same statement
   and I am only asserting the first.

## Comparison with the recorded value

As disclosed above, the prior conclusion reached me through the branch's commit message
(read-level: full-text, commit message only): protein is 153 aa, so position 200 does not exist,
and claim 82's prescriptive half is refuted on that basis.

My value: 153 aa; position 200 does not exist.

**AGREE** — on the number and on the consequence for T200K. With the caveat that this is a
re-fetch that reproduces, not a blind second derivation, since I saw the recorded number first.

```swarm-replication
{"claim_id": 90, "my_value": "153 aa (NP_956545.1); position 200 does not exist, so T200K is unnumberable against it", "agrees": true,
  "note": "Re-fetched NP_956545.1 from NCBI and counted 153 residues three ways (hand sum of FASTA lines, Python len, NCBI's own LOCUS/esummary), with CDS 175..636 = 462 nt = 153 codons corroborating; agreement is weakened because the prior conclusion was visible in the branch commit message before I derived mine."}
```
