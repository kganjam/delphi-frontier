# Challenge 90 — adversarial review of claim 82's correction (slc43a2a T200K numbering)

**Claim under review** (claim 89's correction to claim 82): GeneID 393221 (slc43a2a) has a single
RefSeq protein NP_956545.1 of 153 aa, so position 200 does not exist and T200K cannot be numbered
against it. The full-length zebrafish SLC43A2 paralog is slc43a2b (GeneID 494042, NP_001008585.1,
592 aa, residue 200 = Met). Thr200 absent in 0 of 32 SLC43A2-family RefSeq proteins checked
(challenger-reported). Recorded evidence level: derived; value 153 aa.

**Verdict: REFUTED** — not on its numbers, which I reproduced exactly, but on the inference those
numbers are made to carry. Position 200 is absent from *a provisional, frameshift-truncated RefSeq
record*, which is not the same thing as absent from the slc43a2a protein. And the author's
reassurance that "residue 200 = Met" compares position 200 across two paralogs that are out of
register by 22 residues; the position in slc43a2b actually homologous to slc43a2a-200 is **Thr222**.
The claim's own supporting datum, read in register, points the opposite way.

All sequence work below is mine, recomputed from FASTA I fetched myself. I did not reuse the
author's working.

---

## 1. Arithmetic, redone independently

Fetched via NCBI E-utilities `efetch` (read-level: **full-text**, primary record) and counted
residues myself from the FASTA:

| Accession | Length (my count) | Residue 200 (my count) | Claim says | Agree? |
|---|---|---|---|---|
| NP_956545.1 (slc43a2a) | **153 aa** | does not exist | 153 aa | ✅ |
| NP_001008585.1 (slc43a2b) | **592 aa** | **M** (Met) | 592 aa, Met | ✅ |

The two numbers the claim rests on are correct. I also checked the "single RefSeq protein"
assertion, which the claim does not itself evidence: `elink` `gene_protein_refseq` returns exactly
**one** protein UID for GeneID 393221 (41053786 = NP_956545.1) and **five** for GeneID 494042.
So "a single RefSeq protein" holds for 393221 as stated.

Extending the Met200 check to all five of GeneID 494042's RefSeq proteins — which the claim did not
do — residue 200 is Met in every one (NP_001008585.1 592 aa; XP_087125491.1, XP_087125490.1,
XP_087077278.1, XP_009303545.2 all 598 aa). The claim is not cherry-picking an isoform. Credit
where due.

**Note on a wording defect that inverts the claim's own argument:** "Thr200 absent in 0 of 32" states
that Thr200 failed to be absent in any of the 32 proteins — i.e. that Thr200 is *present in all 32*,
which would demolish the claim rather than support it. The intended sense is evidently "present in
0 of 32." As written the key supporting statistic says the opposite of what it is used for. This is
flagged as a defect in the record, not treated as the author's position.

## 2. Is a proxy standing in for the quantity that matters?

Yes, and this is the central fault.

- **Proxy used:** does index 200 exist within the string NP_956545.1?
- **Quantity that matters:** does residue 200 exist in the slc43a2a *protein*, and what is it?

These come apart when the RefSeq record is incomplete. Four independent signals from the record
itself say it is (read-level: **full-text**, GenBank flatfile `NP_956545.1` / `NM_200251.2`):

1. `PROVISIONAL REFSEQ: This record has not yet been subject to final review.`
2. `Region 97..>143 /region_name="NarK"` — the `>` is NCBI's notation for a domain that **runs off
   the end of the record**. The transporter domain is cut mid-domain by the record's terminus. A
   genuinely 153-aa protein does not end mid-NarK.
3. `RNAseq introns :: partial sample support`.
4. **The transcript arithmetic.** NM_200251.2 is 3230 bp; its CDS is `175..636`. I computed:
   462 bp CDS = 153 codons + stop, 5'UTR = 174 bp, 3'UTR = **2594 bp**. A 153-codon CDS sitting in
   front of a 2.6 kb "3'UTR," for a gene whose paralog encodes 592 aa, is the signature of a CDS
   annotation that terminates early inside real coding sequence.

I then located the termination mechanism directly. Sliding slc43a2a aa95–140 against slc43a2b gives
an unambiguous single optimum at **offset +22** (39/46 = 85% identity; next-best offset 8/46 = 17%):

```
slc43a2a  95-140  LNLAFTIGSFLLSAITLPLGIIMDKYGPRKLRLLGSASFAISCILN
slc43a2b 117-162  LNLAFTVGSFLLSAITLPLGIVMDKYGPRKLRLLGSACFALSCLMI
```

So slc43a2a is colinear with slc43a2b through ~aa 140 at a constant +22 register. But slc43a2a's
final 13 residues, `SVTRTASVQLYYQ`, match **nothing** in slc43a2b (best 13-mer anywhere = 4/13,
i.e. noise). A record that tracks its paralog at 85% for 46 residues and then emits 13 residues of
non-homologous sequence and stops has gone out of frame. The 153 aa is a frameshift artifact
terminating a provisional annotation — it is not a protein length.

**Conclusion on the proxy:** "position 200 does not exist" is a true statement about a database
string and a false statement about slc43a2a. The claim does not distinguish them, and its
operative recommendation — retarget T200K onto slc43a2b — follows only from the conflation.

## 3. The hidden assumption, relaxed

The claim's reassurance rests on an unstated premise: **that position 200 means the same thing in
slc43a2a and slc43a2b.** Relaxed, it fails. The register offset I measured is +22. Therefore:

- slc43a2a residue 200 aligns to slc43a2b residue **222**, not 200.
- slc43a2b residue 222 = **Thr**. Context (my count): `IGSYASSAV`**T**`FPGVKVIYD` (aa 213–231).
- Conversely, slc43a2b's Met200 aligns to slc43a2a ~178, a position irrelevant to T200K.

So the single datum the claim offers against a Thr at 200 — "residue 200 = Met" — is measured at the
wrong position. Read in register, the paralogous residue for slc43a2a-200 is a threonine, which is
consistent with, not contrary to, a T200K numbered against full-length slc43a2a.

**Stated as my inference, separately from the measurement:** the measurements are that the offset is
+22 over aa95–140 and that slc43a2b-222 is Thr. My inference is that slc43a2a-200 is therefore
*plausibly* Thr. I cannot assert it. **The +22 register is verified only to aa 140, because the
slc43a2a record ends at 153.** Any indel in slc43a2b between aa 162 and 222 would shift the
correspondence, and I have no slc43a2a sequence with which to exclude one. slc43a2a residue 200 is
**unknown**. What I have shown is that the claim's grounds for calling it not-Thr are invalid, not
that it is Thr.

## 4. Is the evidence level honest?

Partly, with one real misassignment.

- `153 aa` is recorded as **derived**. It is in fact read directly off a primary record — closer to
  measured. Understating is the safe direction and I do not count it a defect.
- "challenger-reported" on the 32-protein survey is honest labelling of unverified input. Good.
- **The defect:** "position 200 does not exist" and "the full-length zebrafish SLC43A2 paralog is
  slc43a2b" are *inferences* presented with the flat declarative authority of the verified 153.
  The second in particular converts an annotation artifact into a biological designation —
  slc43a2a is not a short paralog; it is a badly annotated one. Nothing in the claim's evidence
  level discloses that the key conclusion is an interpretation of a record flagged
  `PROVISIONAL` on its own face.

## 5. Counter-examples and taxon check

I tested whether Thr200 is excluded family-wide, as the claim's survey implies.

Human SLC43A2 (GeneID 124935), all 11 RefSeq proteins, my own residue count (read-level:
**full-text**): residue 200 is **Ile** (NP_689559.1 569 aa; NP_001271427.1, NP_001308293.1,
NP_001308294.1 573 aa; XP_054171015.1, XP_047291288.1 393 aa), **Lys** (XP_054171014.1,
XP_047291287.1 411 aa), **Pro** (XP_054171013.1, XP_016879668.1 536 aa), **Arg**
(NP_001271428.1 432 aa). No Thr200 in any.

**Scope of this negative search, stated precisely:** 16 proteins carrying a position 200
(5 zebrafish slc43a2b + 11 human SLC43A2), plus NP_956545.1 which has none — 17 records total, two
species, RefSeq only, queried 2026-11-04. Thr at position 200: **0 of 16**. I did **not** verify the
challenger's 32-protein set and cannot reproduce its membership; my 17 may overlap it. This is
consistent with the claim's *intended* statistic.

But it does not rescue the claim, for two reasons. First, a literal position-200 census across
paralogs and species is the same register error as in §3 — these proteins range 393–598 aa and are
not mutually in frame, so "position 200" indexes different structural positions in each.
Note that the 411-aa human isoforms carry **Lys200** — the very residue T200K produces — which
illustrates how little an unaligned position-200 census constrains anything. Second, the relevant
question was never whether Thr sits at index 200 of arbitrary family members, but what the T200K
source numbered against. In slc43a2b, Thr residues sit at 191, 193, 196, 207, **222** and 235 — a
Thr is available within a few residues of 200 under several plausible numbering conventions, so even
a modest offset in the source's reference would place a Thr at "200."

## 6. What survives

- Claim 80 (lat4a = slc43a2a by chr15 mapping) is untouched by anything here. The claim's own
  statement that it is not disturbed is correct — I did not re-test it, and nothing above bears
  on it. Read-level for claim 80: **could-not-access** (not examined).
- NP_956545.1 = 153 aa: **verified**, mine independently.
- NP_001008585.1 = 592 aa, residue 200 = Met: **verified**, mine independently, and extended to all
  five GeneID 494042 RefSeq proteins.
- GeneID 393221 has exactly one RefSeq protein: **verified**, mine independently.
- "The T200K source numbering is unknown and must be re-examined": **agreed, and strengthened.**
  This is the claim's one durable conclusion. My work raises its priority rather than settling it.

## 7. Disagreement preserved

UniProt reports slc43a2a as 153 aa (Q7ZUS0, A0A8N7V006; read-level: **search-summary** via REST
TSV). This looks like independent corroboration and is not: both entries are `unreviewed` and both
cross-reference NP_956545.1 as their source. One record, two databases. I record the agreement and
decline to count it as a second observation.

I could not reach Ensembl (`rest.ensembl.org` refused by this session's egress proxy, 403;
read-level: **could-not-access**). Ensembl annotates from the genome independently of RefSeq and is
the obvious place to recover a full-length slc43a2a. **That check is the one most likely to settle
slc43a2a residue 200, and it remains undone.** Someone with Ensembl or genomic-BLAST access should
run it before claim 82 or claim 89 is treated as resolved. I did not substitute a guess for it.

## 8. Provenance limitation

The cited source — branch `claude/slc43a2a-t200k-numbering-b2ak09`, file `challenge-82.md` — is not
present in this repository, and `docs/research/fish/` did not exist before this file. I reviewed the
claim **as quoted in the task**, against primary NCBI records. I could not read the author's own
document. Read-level for `challenge-82.md`: **could-not-access**. If its reasoning differs from the
quoted summary, §2–§5 should be re-checked against the original.

## 9. What the corrected record should say

> NP_956545.1 (slc43a2a, GeneID 393221) is 153 aa, but it is a `PROVISIONAL` RefSeq whose NarK
> domain runs off the end of the record (`97..>143`) and whose 462 bp CDS sits in front of a 2594 bp
> 3'UTR in a 3230 bp transcript; its last 13 residues are non-homologous to slc43a2b, indicating a
> frameshift-truncated annotation. The 153 aa is therefore an annotation artifact and does not show
> that slc43a2a lacks a residue 200. slc43a2a is colinear with slc43a2b at a +22 register through
> aa 140, so the position homologous to slc43a2a-200 is slc43a2b-**222 = Thr**, not slc43a2b-200
> = Met. slc43a2a residue 200 is **unknown** pending a genome-based annotation. T200K cannot be
> excluded on these grounds, and the source numbering remains the open question.

---

```swarm-challenge
{"claim_id": 90, "outcome": "refuted", "reason": "The 153 aa length is correct but comes from a PROVISIONAL, frameshift-truncated RefSeq (NarK domain runs off the end at 97..>143; 462 bp CDS in front of a 2594 bp 3'UTR; final 13 aa non-homologous to slc43a2b), so 'position 200 does not exist' describes an annotation artifact rather than the protein; and the claim's reassuring Met200 is measured out of register, since slc43a2a is colinear with slc43a2b at +22 through aa 140, making the residue homologous to slc43a2a-200 be slc43a2b-Thr222.", "corrected_value": "NP_956545.1 = 153 aa (verified) but truncated/provisional, not a protein length; slc43a2a residue 200 = unknown; paralog register offset = +22 aa (85% identity over aa95-140); slc43a2b residue homologous to slc43a2a-200 = Thr222 (not Met200)", "depends_on": ["NP_956545.1 length = 153 aa (NCBI efetch, verified independently)", "NP_956545.1 GenBank annotation: PROVISIONAL REFSEQ status and Region 97..>143 NarK domain with open-ended terminus", "NM_200251.2 = 3230 bp with CDS 175..636 (yields 462 bp CDS, 2594 bp 3'UTR)", "NP_001008585.1 = 592 aa with residue 200 = Met and residue 222 = Thr (NCBI efetch, verified independently)", "slc43a2a/slc43a2b register offset = +22 aa, measured over slc43a2a aa95-140 only (39/46 identity); UNVERIFIED beyond aa 140 because the slc43a2a record terminates at 153", "elink gene_protein_refseq: GeneID 393221 -> exactly 1 protein UID; GeneID 494042 -> 5 protein UIDs", "human SLC43A2 GeneID 124935, 11 RefSeq proteins, residue 200 in {Ile, Lys, Pro, Arg}, no Thr", "challenger-reported 32-protein Thr200 survey (NOT verified by me; wording 'absent in 0 of 32' is inverted as written)", "Ensembl slc43a2a full-length annotation = could-not-access (proxy 403); claim 82 source document = could-not-access"]}
```
