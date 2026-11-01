# The full text changes three things, and lets one prediction be tested

Europe PMC's `fullTextXML` endpoint returned HTTP 500 for both target papers, but both are in PMC
with free full text. `PMC9172250` (PMID 34534441, Daane et al., *Current Biology* 2021 — the
flying-fish phylogenomics this project's plan rests on) was retrieved from
`https://pmc.ncbi.nlm.nih.gov/articles/PMC9172250/`, saved as `data/fulltext/PMC9172250.html`
(sha256 begins `d4ef7558fe93e48065a7`) with the extracted text in `PMC9172250.txt` (96,979
characters).

**This is the first full text this project has read.** Everything else in `PLAN.md` remains
abstract-level.

## 1. The flying-fish genomic signal is in `lat4a`. `kcnh2a` is zebrafish-side only.

The abstract says the study identifies "a role for an L-type amino acid transporter, `lat4a`, and
the potassium channel, `kcnh2a`, in the regulation of fin proportion", without saying where each
came from. The full text separates them:

- **`lat4a`** carries the comparative signal: elevated relative evolutionary rate in gliding
  beloniforms, phyloP acceleration **p = 0.008** on the common ancestral node of flying fishes, and
  a convergent amino-acid substitution shared across gliding lineages.
- **`kcnh2a`** enters only through **zebrafish** genetics. Revertant alleles of the zebrafish
  `longfin^dt2` (`lof`) mutant map to loss-of-function mutations in `kcnh2a`, and `lof` itself is a
  **chromosomal inversion on chromosome 2** whose breakpoints lie upstream of the `prrx1a`
  transcription start site (~23.174 Mb, Zv11) and **between `kcc4a` and `kcnh2a`** (~24.075 Mb),
  without affecting either coding region.

**What that does to this project's earlier framing.** Several commits said the published flying-fish
`kcnh2a` signal "needs re-reading". That was based on the abstract and was the wrong worry: the paper
never claims an Exocoetid `kcnh2a` signal. This project's finding that Beloniformes lack `kcnh2a`
therefore **does not contradict the paper at all**. It does still bite on the engineering plan — the
`lof` route is a zebrafish tool and cannot be transferred to a clade lacking the gene — but the
earlier wording implied a tension that does not exist, and it is corrected.

**An incidental cross-check.** The paper's `lof` breakpoint sits "between `kcc4a` and `kcnh2a`
(~24.075 Mb)". `kcc4a` is SLC12A7. This project's independent synteny run
(`data/synteny/synteny.json`) placed zebrafish `slc12a7a` at 24,027,744–24,069,434 and `kcnh2a` at
24,080,694 — the paper's breakpoint falls in the gap between them. Two independent routes to the same
interval.

## 2. `lat4a` is SLC43A2, from the paper's own citation

The paper cites Guetg et al. 2015, "Essential amino acid transporter **Lat4 (Slc43a2)** is required
for mouse development". That ties "lat4a" to the SLC43A2 family this project had already mapped, and
is the answer the open Problem `zf2ff-problem-lat4a-identifier` was looking for on the family level.

## 3. The substitution is named: **F326L**

> "we detected a shared amino acid substitution in `lat4a` that is found across multiple lineages
> having enlarged pectoral fins (**F326L**)"

It is present in **both** flying-halfbeak lineages (*Oxyporhamphus*, *Euleptorhamphus*) and in **all**
sequenced flying fishes **except** the sailfin flying fish *Parexocoetus brachypterus*, which has an
elongated dorsal fin instead and whose `lat4a` is separately highly accelerated. The paper also
reports a zebrafish `lat4a` allele `nr21` with a predicted **T200K** substitution.

44 convergent substitutions were found in all three gliding lineages against 14–28 in control
comparisons, and `lat4a` emerged from intersecting those with genes from zebrafish fin-proportion
screens.

## 4. The testable prediction, and the test

*Hirundichthys speculiger* is an Exocoetid and is not *P. brachypterus*, so the paper predicts **L**
at the F326 position in its LAT4. `scripts/check_lat4a_f326l.py` tests that against the two SLC43A2
loci this project predicted from `GCA_018398805.1`. Result (`data/census_slc43/lat4a_f326l_check.json`):

| numbering reference | residue at 326 | `slc43locus01` | `slc43locus02` |
| --- | --- | --- | --- |
| zebrafish `slc43a2a` (Ensembl, 577 aa) | **F** | S | **L** |
| zebrafish `slc43a2b` (UniProt, 592 aa) | D | D | D |

Three things line up:

1. **Position 326 of zebrafish `slc43a2a` is `F`** — which is what "F326L" requires. The same
   position in `slc43a2b` is `D`. So the paper's numbering is on the **`a` paralog**, which this
   project had to infer because the text read does not say.
2. **`slc43locus02` carries `L`** at the aligned column, in conserved flanking context:
   zebrafish `SFMRSI`**F**`SPIFML` vs flying fish `SFMKSI`**L**`SPIFLL`.
3. **`slc43locus01` — the locus confidently assigned to `slc43a2b` — carries `S`**, so the signal is
   not in the `b` paralog.

**This independently reproduces the published substitution in a different Exocoetid species, from a
public draft assembly, by a different route than the paper used.** It also resolves the identifier
question: the paper's `lat4a` is the **`a`** paralog of `slc43a2`, and the corresponding flying-fish
locus is this project's `slc43locus02` on **JAGFBZ010001224.1** — the locus three gene trees had
tentatively placed on the `a` side at sub-threshold support (36.2/65, then 66.7/78). The residue
evidence and the tree evidence now point the same way by independent means.

## Limitations, stated

- The flying-fish residue comes from a **miniprot prediction** on an unannotated draft assembly, not
  a sequenced transcript. A prediction error at that codon is possible; the conserved flanking
  context argues against it but does not exclude it.
- That the paper's F326 numbering is on zebrafish `slc43a2a` is **this project's inference** from the
  residue matching, not a statement read from the paper.
- `slc43locus05` and `slc43locus06` also show `L` at the aligned column, but their flanking context is
  **non-homologous** (`SFRSCVLSWFFLW`, `TFLECLLSRFFVC` against `SFMRSIFSPIFML`). They are
  `slc43a3`-family loci and those matches are coincidental; only `slc43locus02`'s is in context.
- Nothing here measures transport activity, expression or any phenotype. The paper reports in vivo
  zebrafish work for that; this project has read it, not reproduced it.
- One operator, not independently reviewed.
