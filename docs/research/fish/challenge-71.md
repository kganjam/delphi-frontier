# Challenge 71: "and2 max self-identity 0.098 sits at ~89th percentile of shuffles (p=0.106); and1/and2 carry a conserved C-x(6,7)-C repeat module". SURVIVED

**The claim under review** (author: challenger of claim 29,
`docs/research/fish/challenge-29.md` on branch `claude/tandem-repeat-challenge-k6d4ao`,
read-level: full-text):

> and2 max self-identity 0.098 sits at ~89th percentile of composition-preserving shuffles
> (p=0.106), not below null; and1/and2 carry a conserved C-x(6,7)-C repeat module
> (challenger-reported).

Recorded evidence level: *derived*. Value: 0.098 max self-identity.

**Verdict: SURVIVED.** I tried five ways to break it. None did. Two qualifications on scope are
listed in §6. Neither changes the claim as worded.

Everything below is **calculated** from public sequences with my own scripts in
`challenge-71-scripts/`. I did not reuse the challenger's code. Nothing here is a wet-lab
observation, and no structure was used.

---

## Inputs (fetched independently, 2026-11-04, rest.uniprot.org FASTA, read-level: full record)

| protein | accession | length |
|---|---|---|
| kcnk5b | Q6PFU3 | 448 |
| and1 | E7F5V5 (SV=2) | 570 |
| and2 | A9JRX1 | 508 |
| and2 (check) | A0ACM8QEN9 | 508. I checked that it is identical in sequence to A9JRX1. |

Orthologs and paralogs used in §5 are listed there.

## 1. Arithmetic, redone independently (`v.py`)

Statistic: max over offsets k = 1–80 of the fraction of positions i where s[i] = s[i+k]. This is
the original author's definition in `proteins-disorder.md` §3 on `swarm-architecture`
(read-level: full-text). Null: whole-sequence permutation, which preserves composition exactly.
I used **10,000** shuffles with seed 71. The challenger used 2,000 with seed 29.

| | obs (offset) | null mean | null SD | **percentile** | p(null ≥ obs) |
|---|---|---|---|---|---|
| kcnk5b | 0.1101 (k=3) | 0.0880 | 0.0058 | 99.8 | 0.0016 |
| and1 | 0.1157 (k=8) | 0.0930 | 0.0053 | 99.9 | 0.0010 |
| **and2** | **0.0984 (k=61)** | 0.0915 | 0.0054 | **89.3** | **0.107** |

- **Calculated:** 0.098, the ~89th percentile and p ≈ 0.106 all reproduce with an independent
  implementation, a different seed and 5× the draws.
- The challenger's sub-statements also reproduce: and1 and kcnk5b are above chance.
- So "not below null" is correct.

## 2. Proxy check

The quantity that matters is whether the proteins have internally repeated units. Fixed-offset
global identity is a weak proxy for that. The claim does not rely on the proxy for its positive
part. The module half rests on a different quantity: motif counts and flank identity. Its
self-identity half is a statement *about* the proxy, which is the right object when the question
is whether the original "below its null" holds. No substitution defect.

## 3. Hidden assumptions, relaxed

| assumption | relaxed test (calculated) | result |
|---|---|---|
| Offset window k ≤ 80 | k ≤ L/2 (1,000 shuffles) | and2: p = 0.70, so not below null either way. The "89th percentile" number is specific to the k ≤ 80 window; see §6. |
| Whole-sequence shuffle for the motif count (destroys regional Cys clustering) | Block shuffles within 20-aa and 10-aa blocks with random phase, 5,000 each | and1: 8 observed vs block-null mean 1.08 / 1.18, max 5 / 6, p < 2×10⁻⁴. and2: 10 observed vs 1.40 / 1.45, max 6 / 7, p < 2×10⁻⁴. |
| Spacing 6–7 picked after looking (look-elsewhere) | Null statistic = best C-x(k,k+1)-C count over k = 0..29 in each shuffle (2,000) | and1: null mean 2.79, max 6, obs 8. and2: null mean 3.91, max 7, obs 10. p < 5×10⁻⁴ for both. |
| Flank-identity null of random windows (does not control for Cys anchoring) | Cys positions fixed, all other residues shuffled, windows re-taken at the observed module positions (2,000) | and1: 0.132 vs null mean 0.069, max 0.126. and2: 0.157 vs 0.066, max 0.103. p < 5×10⁻⁴ for both. |
| Overlapping regex hits double-count | Listed every hit and used Cys | and1: 16/16 Cys in hits. and2: 20/20 Cys in hits. Hits are disjoint pairs: and1 7× x7 + 1× x6; and2 8× x7 + 2× x6. No double counting. |

Consecutive Cys–Cys spacings (calculated):
- and1: 8 aa ×7, 7 aa ×1, and all other gaps ≥ 17.
- and2: 8 aa ×8, 7 aa ×2, and all other gaps ≥ 19.
- kcnk5b: no 7- or 8-aa gap, so the control is clean.

Every cysteine in both actinodins is in a strict C-x(6,7)-C pair.

## 4. Evidence level

"Derived" is honest. Both numbers are computed statistics and are not presented as measurements.
"(challenger-reported)" correctly attributes the module finding to a single source. I have now
reproduced it independently, so it is still derived, with two sources.

## 5. Regime / taxon counter-example search

**Inference to test:** if the module were a zebrafish quirk or a chance pattern, orthologs would
lack it. Calculated with `o.py`, 2,000 shuffles each, UniProt FASTA read-level: full record:

| gene | accession | species | L | Cys | C-x(6,7)-C | shuffle mean | p |
|---|---|---|---|---|---|---|---|
| and1 | A0A4W4H642 | *Electrophorus electricus* | 570 | 20 | 9 | 1.28 | < 5×10⁻⁴ |
| and1 | A0A6J2UTP2 | *Chanos chanos* | 590 | 16 | 8 | 0.82 | < 5×10⁻⁴ |
| and1 | A0A1S3NHX9 | *Salmo salar* | 774 | 16 | 8 | 0.62 | < 5×10⁻⁴ |
| and1 | A0A3B5K018 | *Takifugu rubripes* | 722 | 16 | 8 | 0.65 | < 5×10⁻⁴ |
| and1 | A0A668TGC6 | *Oreochromis aureus* | 611 | 14 | 7 | 0.60 | < 5×10⁻⁴ |
| and1 | A0A142C693 | *Polyodon spathula* (232 aa entry, likely partial) | 232 | 12 | 6 | 1.07 | < 5×10⁻⁴ |
| and2 | I3KQR1 | *Oreochromis niloticus* | 513 | 20 | 10 | 1.45 | < 5×10⁻⁴ |
| and2 | A0A8C5CWB0 | *Gadus morhua* | 535 | 20 | 10 | 1.42 | < 5×10⁻⁴ |
| and2 | A0A2D0R8N7 | *Ictalurus punctatus* | 470 | 16 | 8 | 0.98 | < 5×10⁻⁴ |
| and2 | A0A6P8F1Q1 | *Clupea harengus* | 506 | 20 | 10 | 1.45 | < 5×10⁻⁴ |
| and2 | A0A6J2VGL5 | *Chanos chanos* | 580 | 23 | 11 | 1.69 | < 5×10⁻⁴ |
| and3 | Q7SZZ6 | *Danio rerio* | 295 | 9 | 5 | 0.46 | < 5×10⁻⁴ |
| and4 | A0AC36IS99 | *Danio rerio* | 306 | 10 | 4 | 0.58 | < 5×10⁻⁴ |

**Result:**
- No counter-example was found.
- In every ortholog tested, almost all Cys are paired at C-x(6,7)-C.
- The ortholog set spans teleosts and a non-teleost actinopterygian (paddlefish).
- The pairing also appears in the zebrafish paralogs and3 and and4.

This is my **calculated** addition. It *strengthens* "conserved", which the challenger supported
only with within-protein flank identity and and1/and2 paralog correspondence. I did not do a
phylogenetic alignment. Whether the individual units are orthologous one-to-one across species is
**unknown**.

**Scope of the negative search:**
- 13 sequences, chosen from UniProt searches `gene:and1`–`gene:and4` (first 25 hits each).
- No chondrichthyan or sarcopterygian actinodin was tested. An elephant-shark sequence is
  mentioned in the Zhang 2010 abstract, but I did not locate an accession.

**Literature:**
- Zhang et al. 2010, *Nature* 466:234, PMID 20574421. Read-level: **abstract** (Europe PMC). The
  abstract does not mention repeats or a cysteine motif.
- Europe PMC title search for "actinotrichia OR actinodin": 20 hits, read-level: **listing**. No
  title mentions a repeat or cysteine module.
- Whether published work already describes this module: **unknown**. No full texts were read.

## 6. Qualifications that do not break the claim

1. **The window dependence of "89th percentile".** That percentile is for the k ≤ 80 statistic.
   With k ≤ L/2, and2's percentile falls to ~30. "Not below null" holds in both cases. The number
   itself is window-specific.
2. **The "module" core is ~9 aa, not 22.** Per-column identity across the aligned units is high
   only inside the C…C core. In and2, the columns at C+2 (P), C+5 (D) and the second C each reach
   0.62. Columns outside the core are 0.02–0.24, near background. The challenger's 22-aa windows
   are display context. The conserved module is approximately **C-[DN]-P-x-x-D-P-x-C**, which is
   the challenger's own stated consensus. "Conserved repeat module" is accurate for the core and
   overstated for the full 22-aa windows.

## Reproduce

```
python3 -I challenge-71-scripts/v.py <dir with Q6PFU3.fa E7F5V5.fa A9JRX1.fa A0ACM8QEN9.fa>
python3 -I challenge-71-scripts/o.py <dir with ortholog FASTAs> and1:A0A4W4H642 and1:A0A6J2UTP2 \
  and1:A0A1S3NHX9 and1:A0A3B5K018 and1:A0A668TGC6 and1:A0A142C693 and2:I3KQR1 and2:A0A8C5CWB0 \
  and2:A0A2D0R8N7 and2:A0A6P8F1Q1 and2:A0A6J2VGL5 and3:Q7SZZ6 and4:A0AC36IS99
```

```swarm-challenge
{"claim_id": 71, "outcome": "survived", "reason": "Independent recomputation (10,000 shuffles) gives and2 0.0984 at the 89.3th percentile (p=0.107), and the C-x(6,7)-C module survives block-shuffle, look-elsewhere and Cys-fixed flank nulls and recurs in all 11 actinodin orthologs and both zebrafish paralogs tested; the only caveats are that the percentile is specific to the k<=80 window and the conserved core is ~9 aa (C-[DN]-P-x-x-D-P-x-C), not the 22-aa display window.",
  "corrected_value": null,
  "depends_on": ["UniProt A9JRX1 (and2) sequence, 508 aa", "UniProt E7F5V5 SV=2 (and1) sequence, 570 aa", "UniProt Q6PFU3 (kcnk5b) sequence, 448 aa", "statistic definition: max fixed-offset identity over k=1..80 (proteins-disorder.md §3, swarm-architecture)", "whole-sequence permutation as the composition-preserving null", "UniProt ortholog/paralog sequences A0A4W4H642, A0A6J2UTP2, A0A1S3NHX9, A0A3B5K018, A0A668TGC6, A0A142C693, I3KQR1, A0A8C5CWB0, A0A2D0R8N7, A0A6P8F1Q1, A0A6J2VGL5, Q7SZZ6, A0AC36IS99"]}
```
