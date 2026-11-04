# Replication 14 — "The actinodins are NOT collagen-like"

Independent re-derivation. I derived my value first, from the UniProt sequences, before
looking for anyone's recorded result. The comparison section was written afterwards.

## What I measured, and how

A collagen triple helix needs Gly at every third position (Gly-X-Y)n. That means about 33 % Gly
and long unbroken runs of Gly-X-Y triplets (in fibrillar collagens, hundreds of triplets).
I used two **computed** (not observed) metrics on the translated sequences:

1. Gly fraction = Gly count / sequence length.
2. Longest run of consecutive Gly-X-Y triplets: the most consecutive positions i, i+3, i+6, …
   that are all Gly, starting from any residue (so every reading frame is covered).

This is sequence arithmetic. It says nothing about post-translational modification
(for example hydroxyproline) or the real fibre structure.

## Inputs

| Input | Source | Read-level |
|---|---|---|
| Actinodin1 (*and1*), *Danio rerio*, 570 aa, SV=2 | UniProt E7F5V5, `rest.uniprot.org/uniprotkb/E7F5V5.fasta`, fetched 2026-11-04 | full-text (full sequence) |
| Actinodin2 (*and2*), *Danio rerio*, 508 aa, SV=1 | UniProt A0ACM8QEN9, `rest.uniprot.org/uniprotkb/A0ACM8QEN9.fasta`, fetched 2026-11-04 | full-text (full sequence) |
| Collagen reference: Gly every 3rd residue, ≈33 % Gly | textbook definition of the Gly-X-Y repeat; not re-fetched | general knowledge, no specific citation |

## Arithmetic (exact counts, computed)

| | And1 (E7F5V5) | And2 (A0ACM8QEN9) | Ideal collagen helix |
|---|---|---|---|
| Length | 570 | 508 | — |
| Gly | 31 → 31/570 = **5.44 %** | 23 → 23/508 = **4.53 %** | ≈33.3 % |
| Pro | 67 (11.75 %) | 60 (11.81 %) | high (X/Y) |
| Tyr | 47 (8.25 %) | 29 (5.71 %) | low |
| Ala | 56 (9.82 %) | 54 (10.63 %) | — |
| Gly-Pro dipeptides | 3 | 2 | very many |
| Longest consecutive Gly-X-Y run | **2 triplets** (res. 35–40, `GDDGSD`) | **2 triplets** (res. 380–385, `GVRGKT`) | hundreds |
| Most abundant residues | P, A, Y, L, D | P, A, L, E, D | G dominant |

Glycine shortfall compared with the ideal: And1 has 5.44/33.3 = 0.16× the needed Gly and And2 has 4.53/33.3 = 0.14×.
Put another way, a 570-residue full-length helix would need about 190 Gly, and And1 has 31.

## My value

**Gly = 5.44 % (And1) and 4.53 % (And2). The longest Gly-X-Y run is 2 consecutive triplets in each.**
Uncertainty: none on the counts, because they are exact for these sequence versions (E7F5V5 SV=2,
A0ACM8QEN9 SV=1). A different isoform or sequence version could change the last digit.

**My inference (not an author's claim):** neither protein has the sequence needed for a collagen
triple helix. The claim "the actinodins are NOT collagen-like" holds at the primary-sequence level.
The old name "elastoidin" for actinotrichia is not explained by collagen-like actinodin sequence.
Note the limit here: actinotrichia also contain real collagens. This analysis covers the actinodins
only, not the whole actinotrichia fibre.

## Comparison with recorded values (done after my derivation)

Searched: local working tree, then `git grep` across every `origin/*` branch for
`actinodin|E7F5V5|A0ACM8QEN9|collagen-like` (the `collagen-like` search was limited to `*.md` files).
The prior working I found:

- `origin/swarm-architecture:docs/research/fish/proteins-disorder.md`: says both actinodins
  "sit near 5%" Gly against about 33 % for collagen and concludes they are "not collagen-like".
  Read-level: listing (grep lines only).
- `origin/claude/s23-actinotrichia-stiffness-protein-wwp5m2:docs/research/fish/S23-protein.md`:
  And1 Gly 31 (5.44 %), And2 Gly 23 (4.53 %), 0 perfect `G..G..G` windows. Read-level: full-text of that table.
  **Disagreement on the input:** that author analysed A9JRX1 ("Zgc:175106", 508 aa) for And2 and
  only mentioned A0ACM8QEN9. I analysed A0ACM8QEN9. Our Gly, Pro, Ala and Tyr counts for And2 are identical
  (23, 60, 54, 29), which suggests the two entries have the same or nearly the same sequence. I did not fetch A9JRX1 to confirm this.
- `origin/claude/s13-protein-fin-ray-e8y8d8:docs/research/fish/S13-protein.md`: longest Gly-X-Y run in
  And1 = 6 aa, 2 triplets. Read-level: full-text of that table. This matches my 2 triplets.
  My "0 `G..G..G` windows" agrees with S23, because a 3-Gly window would be a run of 3 or more.

**Verdict: AGREE.** The counts are identical and the conclusion is the same. Limit on independence: the same public sequences
and the same simple metric. Agreement shows the arithmetic is right. It does not test the
structural interpretation independently.

```swarm-replication
{"claim_id": 14, "my_value": "Gly 5.44% (And1, E7F5V5) and 4.53% (And2, A0ACM8QEN9) vs ~33% for collagen; longest Gly-X-Y run = 2 triplets in each", "agrees": true, "note": "Exact sequence counts (computed, not observed) match the recorded 5.44%/4.53% Gly and 2-triplet maximum, though the prior S23 work used A9JRX1 rather than A0ACM8QEN9 for And2."}
```
