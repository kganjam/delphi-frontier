# and1 / and2 characterised as sequence, not as structure

No structure prediction is used in this document. Every number is computed from the amino-acid
sequence alone, by `disorder.py`, `disorder2.py` and `tyr_null.py`.

**kcnk5b is carried through every panel as a positive control.** It is a real membrane protein
with a real fold and real K2P homologs, so a method that cannot separate it from the actinodins
is not measuring anything. In two of the four panels below the control is what shows the test works.

---

## 1. The collagen framing is refuted, not merely unsupported

Actinotrichia have historically been called "elastoidin", and 11.8% proline points that way. The
composition refutes it outright:

| | Pro | **Gly** | Ile+Val+Phe |
|---|---|---|---|
| kcnk5b (control) | 4.0% | 6.0% | 20.1% |
| and1 | 11.8% | **5.4%** | 7.4% |
| and2 | 11.8% | **4.5%** | 11.0% |

A collagen Gly-X-Y repeat requires glycine at **every third position, ~33%**. Both actinodins sit
near 5%, i.e. at the ordinary background. **Neither protein can form a collagen triple helix.**
That closes the triple-helix-stability design route as well as the fold route.
*(Glycine point and its consequence contributed by the team lead; recomputed here from
`composition.json` before being written down.)*

## 2. "Disordered" is right for and1 and NOT established for and2

FoldIndex (Prilusky 2005), `FI = 2.785*<H> - |<R>| - 1.151`; `FI < 0` predicts intrinsically
unfolded. It is a **predictor, not a measurement**.

| | FoldIndex | <H> | <R> | % of 51-aa windows with FI<0 |
|---|---|---|---|---|
| kcnk5b (control) | **+0.166** | 0.482 | +0.025 | 38.4% |
| and1 | **−0.056** | 0.402 | −0.025 | **65.1%** |
| and2 | **+0.070** | 0.443 | −0.014 | 40.0% |

**and1 is predicted unfolded; and2 is not.** and2's global FoldIndex is positive and its
disordered-window fraction (40.0%) is indistinguishable from the folded control's (38.4%). So the
sequence evidence does **not** support calling and2 intrinsically disordered, even though it is
11.8% proline and has no PDB70 homolog and folds to 0.0% >pLDDT 70.

Those three facts are consistent with and2 being *something this toolchain cannot model* rather
than with it being disordered. Treating "no fold predicted" and "disordered" as the same statement
would be the error here; they are different claims and only one of them has evidence.

## 3. There are no detectable tandem repeats — in any of the three

Asked directly, and the answer is a clean negative with a null. Maximum self-identity at any
offset 1–80, against 200 composition-preserving shuffles:

| | max observed | chance (Σf²) | shuffled mean-max | shuffled max | verdict |
|---|---|---|---|---|---|
| kcnk5b | 0.110 | 0.060 | 0.088 | 0.109 | at the null |
| and1 | 0.116 | 0.067 | 0.093 | 0.114 | at the null |
| and2 | 0.098 | 0.065 | 0.091 | 0.111 | **below** the null |

Every "peak" sits at or under what the same composition produces by chance, and **no 7-mer recurs
even 3 times** in any sequence. The eye-catching `C…DP…C` motifs (4 in and1, 6 in and2) are real as
motif matches but they are not a periodic repeat array.

## 4. Crosslink-capable residues: the one positive result, stated precisely

Tyr is enriched in both (8.2% and1, 5.7% and2, vs 2.7% control) and Cys modestly so (2.8%, 3.9%
vs 2.0%). Enrichment alone is not organisation, so each was tested against 2,000
composition-preserving shuffles — the fraction of consecutive same-residue gaps ≤4 residues:

| residue | | observed | shuffled | z | p (empirical) |
|---|---|---|---|---|---|
| **Tyr** | kcnk5b | 0.091 | 0.102 | −0.13 | 0.72 |
| | and1 | 0.391 | 0.293 | +1.72 | **0.064** |
| | and2 | 0.393 | 0.211 | +2.74 | **0.011** |
| **Cys** | kcnk5b | 0.000 | 0.076 | −0.84 | 1.00 |
| | and1 | 0.000 | 0.112 | −1.43 | 1.00 |
| | and2 | 0.000 | 0.149 | −2.02 | 1.00 |
| **Lys** | kcnk5b | 0.467 | 0.252 | +3.03 | **0.005** |
| | and1 | 0.200 | 0.172 | +0.40 | 0.44 |
| | and2 | 0.185 | 0.204 | −0.27 | 0.70 |

Read carefully:

- **Tyrosine clustering exceeds composition in and2 (p=0.011). In and1 it does not reach
  significance (p=0.064)** — and1 simply has so much Tyr (47 residues, median gap 7) that most of
  the apparent clustering is already explained by content. Both are worth attention for
  di-tyrosine crosslinking; only and2's *spatial organisation* is established.
- **Cysteines are dispersed, in all three.** Not one pair within 4 residues anywhere, and in and2
  that is significantly *fewer* close pairs than chance (z=−2.02). So there are no CxxC-type
  adjacent motifs: any disulfide architecture would have to be long-range within the chain, or
  between chains. This is a constraint on crosslink design, and it points inter-chain.
- **The Lys row is the positive control.** The test detects real clustering when it exists —
  kcnk5b's lysines are clustered at p=0.005 — and reports none in the actinodins. So the Tyr
  results are not an artifact of a test that calls everything clustered.

## 5. What this licenses, and what it does not

Supported: the actinodins are not collagen-like; they have no tandem-repeat architecture; they are
Tyr- and Cys-enriched with dispersed cysteines; and1 is predicted intrinsically unfolded.
Di-tyrosine crosslinking is the best-supported stiffness lever, and inter-chain rather than
short-range intra-chain disulfide geometry is the better bet.

Not supported: that and2 is disordered. That any of this predicts fibril stiffness — crosslink
density, packing order and mineral fraction are properties of an assembly, and nothing measured
here is a property of an assembly. Sequence composition constrains what chemistry is available;
it does not predict a material.
