# Challenge 218 — adversarial review of claim 218 (slc43a2a residue 200 / T200K numbering)

**Claim under review** (claim 218, correcting claim 90, which corrected 82): NP_956545.1 = 153 aa is
verified but is a PROVISIONAL RefSeq, frameshift-truncated (NarK domain 97..>143 open-ended; 462 bp
CDS before a 2594 bp 3'UTR), so "position 200 does not exist" describes an annotation artifact, not
the protein. **slc43a2a residue 200 is UNKNOWN.** Paralog register offset +22 over aa95–140 only
(39/46 identity); slc43a2b residue homologous to slc43a2a-200 = **Thr222**, not Met200. Claim 82
remains refuted as an executable prescription; the T200K numbering question is **OPEN**. Offset
beyond aa140 unverified.
Recorded evidence level: derived. Recorded value: 222 (challenger-derived).

---

## Verdict: WEAKENED

Two halves of this claim come apart under test, and they come apart in opposite directions.

- **The claim's recorded value survives.** slc43a2b-222 really is the residue homologous to
  slc43a2a-200, and it really is Thr. I reproduced it from an independent reconstruction that does
  not assume the claim's register.
- **The claim's headline conclusion is refuted.** "slc43a2a residue 200 is UNKNOWN" and "the T200K
  numbering question is OPEN" are both overturned. The downstream coding exons that the 153-aa
  record is missing are present in the zebrafish genome, in two independent assemblies, and they
  place **Thr at exactly position 200** of full-length slc43a2a. The claim's own flagged gap —
  "offset beyond aa140 unverified" — is now closed: the offset is +22 continuously through aa 215.
- One mechanism label is wrong: the truncation is **not a frameshift**. There is no frameshifting
  indel anywhere in the coding sequence. It is an aberrant junction in a single cDNA clone, with a
  non-canonical donor *and* non-canonical acceptor, i.e. a cloning/RT artifact rather than splicing.

So the claim is right about the artifact, right about 222, wrong about unknowability, and wrong about
the mechanism. Net effect on the underlying scientific question: **T200K is coherently numbered
against full-length slc43a2a** — there is a threonine at position 200 — which is the opposite of
what "the numbering question is OPEN" invites a reader to conclude.

All sequence work below is mine, recomputed from records I fetched myself on 2026-11-04. Scripts are
in the session scratchpad. I did not reuse the author's working, and I did read the author's source
document (unlike the previous reviewer, I could reach it).

---

## 0. Read-levels and provenance

| Source | Read-level |
|---|---|
| NP_956545.1, NM_200251.2 (GenBank flatfiles + FASTA), NCBI efetch | **full-text**, primary |
| BC047854.1 / AAH47854.1 (GenBank flatfiles + FASTA) | **full-text**, primary |
| NP_001008585.1, NM_001008585.1 (slc43a2b) | **full-text**, primary |
| NP_689559.1 (human SLC43A2), XP_009303545.2 | **full-text**, primary |
| NC_141035.1:31095000-31144000 (GRCz13ab, strain M-AB) | **full-text**, primary |
| NC_133190.1:30870000-30920000 (GRCz12tu, strain Tübingen) | **full-text**, primary |
| UniProt REST TSV (slc43a2a, organism 7955) | **search-summary** |
| `challenge-90.md`, branch `claude/slc43a2-t200k-challenge-wkixy4` | **full-text** |
| Ensembl REST (`rest.ensembl.org`) | **could-not-access** — proxy `connect_rejected` |
| claim 82 / `challenge-82.md` source document | **could-not-access** — not in this repository |

Ensembl is blocked for me exactly as it was for the previous reviewer. I did **not** substitute a
guess for it; §3 replaces it with a different and, I would argue, better-evidenced route.

---

## 1. Arithmetic, redone independently from the stated inputs

Every number the claim states reproduces. I counted from FASTA myself and read the flatfiles myself.

| Claim's input | My independent value | Agree? |
|---|---|---|
| NP_956545.1 = 153 aa | **153 aa** (70+70+13) | ✅ |
| `PROVISIONAL REFSEQ` status | present verbatim in the flatfile COMMENT | ✅ |
| NarK domain `97..>143`, open-ended | `Region 97..>143 /region_name="NarK"` verbatim | ✅ |
| 462 bp CDS | CDS `175..636` → 636−175+1 = **462** = 153 codons + stop | ✅ |
| 2594 bp 3'UTR | 3230 − 636 = **2594** (5'UTR = 174) | ✅ |
| +22 offset over aa95–140, 39/46 | best offset **+22**, **39/46** against the 153-aa record | ✅ |
| slc43a2b residue 222 = Thr | **Thr**; context `IGSYASSAV`**T**`FPGVKVIYD` (213–231) | ✅ |
| slc43a2b residue 200 = Met | **Met** | ✅ |

Two small notes, neither load-bearing. (i) Using my *predicted* slc43a2a (§3) rather than the 153-aa
record, the aa95–140 identity is 40/46 rather than 39/46, because the record's residue 140 is
artifactual; the claim's 39/46 is correct for the record as written. (ii) `challenge-90.md` reports
the next-best offset as 8/46 (17%); I get **10/46 (22%)**. Immaterial to any conclusion — the signal
at +22 is 39–40/46 either way — but recorded so the discrepancy is not lost.

**On the claim's own internal consistency:** claim 218 scopes the offset honestly ("+22 over aa95–140
**only**", "Offset beyond aa140 **unverified**") and then asserts a value — "slc43a2b residue
homologous to slc43a2a-200 = Thr222" — that requires extending that offset 60 residues past where it
says the evidence stops. The caveat and the value contradict each other. The value turns out to be
right, but the claim as written gives no warrant for it. That is a real defect: it is a conclusion
smuggled past its own disclaimer.

---

## 2. Is a proxy standing in for the quantity that matters?

Yes — and the claim is itself a correction that identified this proxy, so credit is due. But the
claim then stops one step short and leaves a *second* proxy in place.

- Proxy the claim correctly rejected: *does index 200 exist in the string NP_956545.1?*
- Proxy the claim **left standing**: *the slc43a2a protein sequence = the RefSeq protein record.*

Having established that the record is an artifact, the claim continues to treat the record as the
only available evidence about the protein, and concludes "unknown". The quantity that matters —
slc43a2a's actual coding sequence — is in the genome, which the claim never queries. §3 queries it.

First, confirming the claim's artifact diagnosis, and hardening it:

**All four accessions are one molecule.** `NM_200251.2`'s `PRIMARY` block reads
`REFSEQ_SPAN 1-3230 / PRIMARY_IDENTIFIER BC047854.1 / PRIMARY_SPAN 2-3231` — the RefSeq is 100%
derived from a single cDNA clone, **MGC:56271 / IMAGE:5602175**, library "Sugano SJD adult male".
`elink dbfrom=gene db=protein` on GeneID 393221 returns **two** protein UIDs, not the one the
previous reviewer reported from the narrower `gene_protein_refseq` link: 41053786 (NP_956545.1) and
28839817 (**AAH47854.1**, the translation of BC047854.1). Both are 153 aa and identical. UniProt's
Q7ZUS0 and A0A8N7V006 are both 153 aa, both `unreviewed`, both cross-referencing NP_956545.1.
So: four accessions in three databases, **one cDNA clone, one observation.** Nothing in the record
set is independent corroboration of 153 aa.

---

## 3. The hidden assumption, relaxed — the decisive test

**Hidden assumption:** that because the only annotated slc43a2a protein stops at 153, the sequence
at position 200 is unknowable. Relaxed by reading the genome directly.

I fetched the slc43a2a locus (gene span `NC_141035.1` 31,099,368–31,139,242, GRCz13ab, strain M-AB)
with 4–5 kb flanks, translated all six frames, and seeded against slc43a2b with exact 6-mers.

**Result: the locus carries ten coding blocks homologous to slc43a2b, spanning 31,101,303–31,133,964
and covering slc43a2b offsets −31 to +486.** slc43a2a is a full-length ~590-aa transporter gene that
is badly annotated, exactly as the claim argues. This is the genome-based check `challenge-90.md`
named as "the one most likely to settle slc43a2a residue 200, and it remains undone." It is now done.

### 3.1 Reconstructed coding exons (my gene prediction — computational, **not** an annotation)

| | slc43a2a exon (GRCz13ab) | len | slc43a2b annotated coding exon | match |
|---|---|---|---|---|
| 1 | 31,101,396–31,101,555 | 160 | ex2 = 160 bp | **exact** |
| 2 | 31,107,621–31,107,849 | 229 | ex3 = 295 bp | −66 bp = **−22 codons** |
| 3 | 31,109,596–31,109,651 | 56 | ex4 = 56 bp | **exact** |
| 4 | 31,109,732–31,109,808 | 77 | ex5 = 77 bp | **exact** |
| 5 | 31,121,258–31,121,350 | 93 | ex6 = 93 bp | **exact** |

All four introns are canonical GT…AG with good consensus: `GTGAGG…CTCCAG`, `GTATAA…TTTCAG`,
`GTATGT…TTACAG`, `GTAAGT…TTGTAG`.

Four of five exon lengths are *identical* to slc43a2b's annotated coding exons, and the single
difference is **exactly 66 bp = 22 codons**, in frame — which is the +22 register the claim measured,
now localised to a single in-frame indel inside exon 3. That is a strong internal consistency check
I did not design for; it falls out of the reconstruction.

### 3.2 The reconstruction agrees with the record exactly where the record is genuine

```
  1 MAPTLATAFSRRWWMAITAVIENLLFSAVLLGWGSLLIMLKSEGFYSYLCREAGNGTGHN
 61 VSESENGTMNATRLEEEDNLQMNGWPICKEQDEMLNLAFTIGSFLLSAITLPLGIIMDKY
121 GPRKLRLLGSASFAISCILISYGASDPQNLSILIFFALALNGFGGMCMTFTSLTLPNMFG
181 DLRSTFIALMIGSYASSAVTFPGIK
```

Identity to NP_956545.1 over residues 1–139: **139/139**. First mismatch: **residue 140** — the exact
point at which `challenge-90.md` independently inferred the record goes wrong (it said ~141, counting
from the first fully non-genomic codon). The ORF is open throughout; no stop.

### 3.3 Residue 200

```
slc43a2a (predicted) 193-207  S Y A S S A V T F P G I K        -> residue 200 = T (Thr)
slc43a2b             218-232  S S A V T F P G V K V I Y D L    -> residue 222 = T (Thr)
human SLC43A2        189-203  S S A V T F P G I K L I Y D A    -> residue 193 = T (Thr)
```

**slc43a2a residue 200 = Thr** (genome-based prediction), homologous to slc43a2b Thr222 and human
SLC43A2 Thr193.

### 3.4 Register, re-measured against the reconstruction

Sliding scan, my own, prediction vs slc43a2b:

| window | identity | best offset | next-best |
|---|---|---|---|
| a1–50 | 47/50 | **+0** | 9 |
| a55–100 | 24/46 | **+22** | 7 |
| a95–140 | 40/46 | **+22** | 11 |
| a141–170 | 22/30 | **+22** | 8 |
| a171–200 | 29/30 | **+22** | 7 |
| a186–205 | 19/20 | **+22** | 7 |
| a190–215 | 15/26 | **+22** | 6 |

The offset is **+0** at the N-terminus and **+22** continuously from ~aa 55 through aa 215. The claim
is therefore right that +22 holds at 200 (so 200 + 22 = 222 ✅) and wrong that this was unverifiable
beyond aa 140. As a side note, `challenge-90.md`'s prose — "slc43a2a is colinear with slc43a2b at a
**constant** +22 register through aa 140" — is false as stated: the register is 0 over aa 1–50. Claim
218's narrower wording ("+22 over aa95–140 only") avoids that error.

### 3.5 Replication in an independent assembly

All five reconstructed exons were searched as exact strings against **GRCz12tu** (`NC_133190.1`,
strain **Tübingen** — a different strain and a different assembly):

| exon | GRCz12tu position | result |
|---|---|---|
| 1 | 30,877,424 | exact |
| 2 | 30,883,649 | exact |
| 3 | 30,885,624 | exact |
| 4 | 30,885,760 | exact |
| 5 | 30,897,286 | exact |

Translated peptide **identical**; residue 200 = **Thr**. Two assemblies, two strains, same answer.

---

## 4. The one place my result could still break, stated plainly

Residue 200's identity turns on a single choice: the **exon-3 donor**. Two donors are available.

| exon 3 | donor motif | alignment score vs slc43a2b | residue 200 | homologous b residue |
|---|---|---|---|---|
| 56 bp (31,109,651) | **GTATGT** | **274** | **Thr** | **Thr222** |
| 44 bp (31,109,639) | GTGATC | 268 | Ile | Val226 |

268 vs 274 is well within the noise of my crude scoring, so I did **not** decide this on score. Four
independent lines all favour 56 bp:

1. **Donor consensus.** `GTATGT` is a canonical U2 donor; `GTGATC` is a poor one.
2. **Paralogous exon length.** slc43a2b's annotated coding exon 4 is **56 bp**, and the next exon
   (77 bp) matches my exon 4 exactly. Under the 44-bp model, slc43a2a's exon 3 would be 12 bp shorter
   than its paralog's while the flanking exons match to the base.
3. **Gapless three-species alignment.** The 56-bp model yields a 10-column alignment with no gaps:
   ```
   slc43a2a (pred) 141-150   S Y G A S D P Q N L
   slc43a2b        163-172   A Y G A S N P N E L
   human SLC43A2   134-143   A Y G A S K P N A L
   ```
   Y-G-A-S, P and L are conserved in all three. The 44-bp model deletes D-P-Q-N from slc43a2a,
   forcing a 4-residue gap against *both* a paralog and a mammalian orthologue — including the
   invariant proline.
4. **Register coherence.** 56 bp gives a single constant +22 offset from aa 55 to aa 215; 44 bp
   requires the offset to jump +22 → +26 mid-protein for no structural reason.

**Honest statement of residual risk:** no transcript evidence directly supports the slc43a2a exon-3
donor, because the only cDNA at this locus is the artifactual one (§5). If the 44-bp donor were
nonetheless correct, residue 200 would be **Ile** and the homologous slc43a2b residue would be
**Val226** — which would refute the claim's recorded value of 222 rather than confirm it. I judge
that unlikely on the four grounds above, but it is the live alternative and I am not hiding it.
Under **both** models, note, the claim's core point stands: residue 200 exists, and "position 200
does not exist" is an artifact.

---

## 5. A regime the author missed: the mechanism is not a frameshift

The claim says "frameshift-truncated". I can locate the lesion exactly, and it is not a frameshift.

- cDNA 564–592 matches GRCz13ab contiguously at 31,109,596–31,109,624 — i.e. the first **29 bp** of
  the genuine 56-bp exon 3.
- cDNA diverges at position **593**. That divergent 3' portion is **not** foreign: it maps
  contiguously (1 SNP) into the gene's own terminal region, ~27 kb downstream, at GRCz12tu
  ≈30,912,651, continuing to the gene's 3' end at 30,915,208.
- The junction is non-canonical on **both** sides: the genomic bases immediately 3' of the break are
  `TT` (not `GT`), and immediately 5' of the landing point are `GA` (not `AG`).

So BC047854 is a single clone in which a 5' fragment ending 29 bp into exon 3 is joined to the
gene's terminal region at a junction that is not a splice site on either side — a cloning or
reverse-transcription artifact, not splicing and not a frameshift. There is no frameshifting indel
anywhere in the coding sequence. Consequences worth recording:

- The "2594 bp 3'UTR" the claim cites is not a UTR at all: it is the gene's **genuine terminal exon**,
  read as UTR because the CDS was forced to stop early. The claim's arithmetic is right; its
  interpretation of what that 2594 bp *is* was not available to it.
- The `exon 564..583` feature in NM_200251.2 — a 20-bp "exon" — is an alignment artifact. The real
  exon is 56 bp; Splign cut it at 583 because the cDNA stops tracking the genome 9 bp later. There is
  no 20-bp exon in this gene.
- `Region 97..>143` is explained: the NarK model keeps going because the protein keeps going. The
  open-ended `>` is a signature of the artifact, exactly as the claim argued.

I treat this as a **correction, not a refutation**, of the claim's reasoning: every observable the
claim cites is real and its conclusion ("annotation artifact, not a protein length") is correct and
now independently confirmed. Only the named mechanism is wrong.

---

## 6. Is the evidence level honest?

Mostly yes, with one defect and one over-modesty.

- **Honest:** 153 aa marked verified with its method named ("harvester efetch"); 222 marked `derived`
  and "challenger-derived"; "Offset beyond aa140 unverified" stated outright. Flagging the limit of
  one's own register measurement is good practice and I want to say so.
- **The defect:** the claim asserts "slc43a2b residue homologous to slc43a2a-200 = Thr222" in the
  declarative, and simultaneously states the offset beyond aa140 is unverified. A value that its own
  caveat forbids cannot be stated flat. It should have read *"if +22 extends to 200, then Thr222."*
  The number is right; the warrant was absent.
- **Over-modest:** "slc43a2a residue 200 is UNKNOWN" is presented as a settled finding when it was a
  statement about one database record's contents. It should have read "unknown **from RefSeq**,
  pending a genome-based reconstruction" — which is what `challenge-90.md` §7 actually says in its
  prose and what claim 218's summary drops.

**My own evidence level, stated for the record:** residue 200 = Thr is a **computational gene
prediction** derived from measured primary genomic sequence. It is **not** an observation of a
protein, not a database annotation, and not transcript-confirmed. It is replicated across two
assemblies and two strains, its exon lengths match the paralog's annotated exons to the base, and it
reproduces the genuine part of the existing record at 139/139. I would act on it; I would not call
it measured.

---

## 7. Scope of negative searches

- **No slc43a2a protein longer than 153 aa exists in NCBI.** GeneID 393221 → 2 protein accessions
  (NP_956545.1, AAH47854.1), both 153 aa, both from clone MGC:56271. `esearch db=protein` for
  `slc43a2a[Title] AND 400:700[SLEN]`: **0 hits**, all organisms, queried 2026-11-04.
- **UniProt:** 2 entries for slc43a2a/organism 7955 (Q7ZUS0, A0A8N7V006), both 153 aa, both
  unreviewed, both citing NP_956545.1. Read-level search-summary. No independent length.
- **Ensembl:** could-not-access (proxy `connect_rejected`). Unverified there.
- **Scope of my genomic search:** two windows only — `NC_141035.1` 31,095,000–31,144,000 (49,001 bp)
  and `NC_133190.1` 30,870,000–30,920,000 (50,001 bp). I reconstructed exons covering residues
  1–205 carefully; the remaining five homology blocks (to slc43a2b offset +486) I did **not**
  resolve to base-pair boundaries, so I make **no claim** about slc43a2a's full length or its
  C-terminal sequence.
- I did **not** verify the 32-protein Thr200 survey carried forward from claim 82, and cannot
  reproduce its membership. Note that a literal position-200 census across unaligned paralogs is in
  any case the register error this whole claim chain is about: human SLC43A2 has Thr at **193** and
  Ile at 200, so it would be scored as "no Thr200" while in fact carrying the homologous threonine.

## 8. Disagreement preserved

`challenge-90.md` says "slc43a2a is colinear with slc43a2b at a **constant** +22 register through
aa 140". I measure +0 over aa 1–50, so that sentence is wrong as written even though its +22 figure
for aa95–140 is right. Claim 218's narrower restatement ("+22 over aa95–140 only") does not inherit
the error. I record both rather than averaging them.

`challenge-90.md` and claim 218 both say "frameshift"; I say non-canonical artifactual junction with
no frameshifting indel (§5). That disagreement stands unresolved in the sense that I have not
adjudicated *how* the clone acquired the junction — cryptic splicing with a non-consensus donor
versus template switching during cloning. I measured only that neither side is a canonical splice
site.

## 9. What the corrected record should say

> NP_956545.1 (slc43a2a, GeneID 393221) is 153 aa, but it is a `PROVISIONAL` RefSeq derived 100% from
> a single cDNA clone (MGC:56271 / BC047854.1), whose sequence stops tracking the genome 29 bp into
> exon 3 and resumes in the gene's own terminal exon ~27 kb downstream across a junction that is
> non-canonical on both sides. It is a cloning artifact, not a frameshift, and 153 aa is not a protein
> length. The slc43a2a locus encodes a full-length transporter: ten coding blocks homologous to
> slc43a2b span 31,101,303–31,133,964 on NC_141035.1. Reconstructing exons 1–5 (160/229/56/77/93 bp,
> all introns canonical GT…AG; four of five lengths identical to slc43a2b's annotated coding exons,
> the fifth short by exactly 22 codons) gives a peptide matching the genuine part of NP_956545.1 at
> 139/139 and continuing in frame. **slc43a2a residue 200 = Thr** (genome-based prediction,
> replicated in GRCz13ab and GRCz12tu), homologous to slc43a2b Thr222 and human SLC43A2 Thr193. The
> paralog register is +22 continuously from aa 55 to aa 215. T200K is therefore coherently numbered
> against full-length slc43a2a; "residue 200 is unknown" and "the numbering question is open" no
> longer hold. The result depends on the exon-3 donor being `GTATGT` at 31,109,651; the alternative
> 44-bp donor would give Ile200 / Val226.

---

```swarm-challenge
{"claim_id": 218, "outcome": "weakened", "reason": "The claim's recorded value survives independent reconstruction (slc43a2b-222 Thr really is homologous to slc43a2a-200, and the +22 register does hold at 200), but its headline conclusions are refuted: the slc43a2a locus carries the missing downstream coding exons in two independent assemblies, and a genome-based reconstruction places Thr at exactly position 200, so residue 200 is not UNKNOWN and the T200K numbering question is not OPEN; the truncation mechanism is also mislabelled, being a non-canonical cDNA-clone junction rather than a frameshift.", "corrected_value": "slc43a2a residue 200 = Thr (genome-based gene prediction, not an annotation; replicated in NC_141035.1/GRCz13ab and NC_133190.1/GRCz12tu); paralog register = +22 continuously aa55-215, so slc43a2b residue homologous to slc43a2a-200 = Thr222 (claim's value CONFIRMED); slc43a2a coding exons 1-5 = 160/229/56/77/93 bp at NC_141035.1 31101396-31101555, 31107621-31107849, 31109596-31109651, 31109732-31109808, 31121258-31121350; 153 aa = cloning artifact of clone MGC:56271, not a frameshift", "depends_on": ["NP_956545.1 length = 153 aa (NCBI efetch, verified independently by my own residue count)", "NP_956545.1 GenBank flatfile: 'PROVISIONAL REFSEQ' COMMENT and 'Region 97..>143 /region_name=NarK' (verified verbatim)", "NM_200251.2 = 3230 bp, CDS 175..636 -> 462 bp CDS, 174 bp 5'UTR, 2594 bp 3'UTR (verified independently)", "NM_200251.2 PRIMARY block: REFSEQ_SPAN 1-3230 = BC047854.1 PRIMARY_SPAN 2-3231, i.e. RefSeq 100% derived from one cDNA clone MGC:56271/IMAGE:5602175", "elink gene_protein GeneID 393221 -> 2 protein UIDs (NP_956545.1, AAH47854.1), both 153 aa, both from the same clone; esearch slc43a2a[Title] AND 400:700[SLEN] = 0 hits", "NP_001008585.1 = 592 aa, residue 200 = Met, residue 222 = Thr (NCBI efetch, verified independently)", "NM_001008585.1 annotated coding exon lengths (ex2-ex6) = 160/295/56/77/93 bp -- the discriminator for the exon-3 donor choice", "NC_141035.1 (GRCz13ab, strain M-AB) 31095000-31144000 genomic sequence; gene span 31099368-31139242; 10 coding blocks homologous to slc43a2b spanning 31101303-31133964", "NC_133190.1 (GRCz12tu, strain Tuebingen) 30870000-30920000 genomic sequence; all 5 reconstructed exons exact-match at 30877424/30883649/30885624/30885760/30897286", "MY OWN GENE PREDICTION (computational, derived, NOT an annotation and NOT transcript-confirmed): slc43a2a coding exons 1-5 with canonical GT..AG introns, giving residue 200 = Thr; pivotal input is the exon-3 donor GTATGT at 31109651 rather than GTGATC at 31109639", "Exon-3 donor choice supported by 4 concordant lines: donor consensus GTATGT vs GTGATC; slc43a2b coding exon 4 = 56 bp; gapless 10-column alignment slc43a2a SYGASDPQNL / slc43a2b AYGASNPNEL / human AYGASKPNAL with invariant Pro; constant +22 register. IF the 44 bp donor is instead correct, residue 200 = Ile and the homologous slc43a2b residue = Val226, which would refute the claim's value 222", "NP_689559.1 (human SLC43A2) residue 193 = Thr, residue 200 = Ile, and the AYGASKPNA loop at 134-142 (NCBI efetch, verified independently)", "My sliding-window register scan: offset +0 at a1-50 (47/50), +22 at a55-100/a95-140/a141-170/a171-200/a186-205/a190-215 with next-best <=11", "cDNA junction mapping: cDNA 564-592 = genomic 31109596-31109624 (29 bp of exon 3); cDNA 593+ maps to GRCz12tu ~30912651; donor-side bases TT and acceptor-side bases GA, neither canonical", "Ensembl slc43a2a annotation = could-not-access (proxy connect_rejected); claim 82 / challenge-82.md source = could-not-access (absent from this repository); challenger's 32-protein Thr200 survey = NOT verified by me", "challenge-90.md on branch claude/slc43a2-t200k-challenge-wkixy4 = full-text (read directly); its prose claim of a 'constant +22 register through aa 140' is contradicted by my +0 measurement over aa1-50"]}
```
