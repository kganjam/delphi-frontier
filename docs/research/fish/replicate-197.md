# Replicate 197 — S13: can a stiffer structural-protein variant stiffen the fin ray?

**Type:** independent re-derivation (calculation, not observation) · **Date:** 2026-11-04
**Author:** Claude Code (automated research agent)

## 0. Disclosure of what I saw of the other derivation

- The question was handed to me as `[S13] No` with the answer removed. To find out what S13 asks,
  I read **only the first 20 lines** of `docs/research/fish/S13-protein.md` on branch
  `claude/s13-protein-fin-ray-e8y8d8`. That gave me its title, *"Can a stiffer structural protein
  variant be designed for the fin ray?"*, and the start of its §1. I stopped there and did not read
  its §2–§3, its numbers or `s13_arith.py`.
- **Contamination I could not avoid:** `git log` printed that branch's commit subject, *"S13: fin-ray
  protein stiffness — derived negative on the materials route"*. So I knew its **direction**
  (negative) before I started. I did not know any of its numbers. The question stem `No` points the
  same way. Weigh any agreement on direction with that in mind.
- I found no project definition of S13 or of a target stiffness. I searched `seeds/`, `specs/` and
  `findings/` on this branch, and `git grep` on `work/fin-ray-constitutive`. Because of that, **I
  defined the quantity myself** (§1). The recorded derivation may have answered a different
  quantity.

## 1. The quantity I derived

**F_max:** the largest fold-increase in fin-ray flexural stiffness EI that a change of material
(through the structural protein) can deliver at fixed ray geometry. Because EI = E·I and I is held
fixed, F_max = E_new / E_native.

I bound it in two ways:
- **(A) Empirical ceiling.** The stiffest vertebrate mineralised-collagen tissue on record, divided
  by the native fin-ray modulus. This is an upper bound for *any* material change in bone, and most
  of it comes from mineral, not from protein.
- **(B) Protein-only ceiling.** Raise the collagen modulus while the mineral fraction stays fixed.
  Voigt (iso-strain) and Reuss (iso-stress) composite bounds bracket the result.

## 2. Inputs (all quoted from sources unless marked ASSUMPTION)

| # | Input | Value | Source | Read-level |
|---|---|---|---|---|
| 1 | Zebrafish fin-ray reduced modulus (indentation, regenerated rays). Alendronate group stated to have "recovered to the pre-amputation condition" | 8.68 ± 8.74 GPa (alendronate); 5.60 ± 5.04 GPa (prednisolone) | Study of prednisolone/alendronate on regenerating zebrafish fin bone, via the [NTHU ETD record](https://etd.lib.nthu.edu.tw/detail/bbd7d08bf7afa861826c148917ae41f8) and the web-search summary. I could not confirm which record holds these numbers | search-summary |
| 2 | Fin-ray modulus in a non-zebrafish fish, three-point bending, proximal region | mean 1.34 GPa (range 0.24–3.7) | [Drexel record](https://researchdiscovery.drexel.edu/esploro/outputs/journalArticle/Bioinspiration-from-fish-for-smart-material/991019168076204721) | search-summary |
| 3 | Whole caudal-fin bending stiffness, in vivo, adult zebrafish | 1.5×10⁻⁹ – 4×10⁻⁹ N·m². Authors: flexibility "predominantly relies on the mechanical properties of the rays"; removing interray tissue did not observably change stiffness | Puri et al., *J Exp Biol* 221 (2018), [PMC5868929](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5868929/) | search-summary. The full text at cob.silverchair.com and ikarus.physik.uzh.ch is **could-not-access** (host not allowed by the network policy) |
| 4 | Stiffest bone on record: fin-whale tympanic bulla, 86.4 % mineral | E = 31.3 GPa (range quoted 14–31 GPa) | Currey (2006), as tabulated in [PMC9119617 table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC9119617/table/joa13615-tbl-0001) and a 2020 Appl Phys A paper ([link](https://link.springer.com/content/pdf/10.1007/s00339-020-03913-8.pdf)). I did not read Currey's primary paper | search-summary |
| 5 | Collagen fibril modulus | hydrated ≈ 0.3 GPa at small strain, ≈ 1.2 GPa at large strain; dry 0.9–11.5 GPa; single molecules ≈ 4.8 ± 2 GPa | Review in [PMC8999528](https://pmc.ncbi.nlm.nih.gov/articles/PMC8999528); Buehler *Nano Lett* 2011 ([pdf](https://web.mit.edu/mbuehler/www/papers/nl103943u_2011.pdf)) | search-summary |
| 6 | Hydroxyapatite modulus | 114 GPa as commonly cited (source ambiguous); 112 GPa dense ceramic; 143–150 GPa single-crystal nanoindentation | [Langmuir 2012](https://web.mit.edu/mbuehler/www/papers/Langmuir_2012.pdf); [Snyders 2007](https://orbi.umons.ac.be/bitstream/20.500.12907/12966/1/Snyders-2007-2-Journal.pdf) | search-summary |
| 7 | Mineral volume fraction of fin-ray bone | φ = 0.40 | **ASSUMPTION** (typical bone value from my background knowledge, not measured for fin rays) | n/a |

Disagreement between sources, kept as found: the zebrafish indentation value (8.7 GPa) and the
other species' bending value (1.34 GPa) differ by about 6×. Indentation reduced modulus and beam
modulus are different measurements, so I do not average them.

## 3. Arithmetic (all computed by me; nothing here is observed)

**(A) Empirical ceiling, F_A = 31.3 / E_native**

| E_native (GPa) | F_A = EI gain | Equivalent radius gain for a solid ray, F^(1/4) |
|---|---|---|
| 8.68 (zebrafish, input 1) | 31.3/8.68 = **3.61×** | 1.378× |
| 5.60 (input 1, prednisolone group) | 5.59× | 1.538× |
| 3.7 (top of input 2) | 8.46× | 1.705× |
| 1.34 (input 2 mean, other species) | 23.4× | 2.198× |

F_A is the gain for turning fin-ray bone into the most-mineralised bone known (86.4 % mineral). The
sources attribute that modulus to mineralisation, not to a protein sequence. So F_A over-estimates
what a protein variant can do. Currey's data also tie higher modulus to lower strain to failure, and
the bulla is described as "very weak in bending".

**(B) Protein-only ceiling (φ = 0.40, E_mineral = 114 GPa)**

Reuss: 1/E = φ/E_m + (1−φ)/E_c. Voigt: E = φ·E_m + (1−φ)·E_c.

| Change in collagen modulus E_c | Reuss composite | Reuss gain | Voigt composite | Voigt gain |
|---|---|---|---|---|
| 1 → 2 GPa (2×) | 1.657 → 3.295 GPa | 1.99× | 46.2 → 46.8 GPa | 1.013× |
| 1 → 5 GPa (5×, about the dry or single-molecule maximum) | 1.657 → 8.097 GPa | 4.89× | 46.2 → 48.6 GPa | 1.052× |
| 0.3 → 5 GPa (16.7×, an extreme case) | 0.499 → 8.097 GPa | 16.2× | 45.78 → 48.6 GPa | 1.062× |

Real bone sits between these bounds. Native fin-ray moduli (1–9 GPa) lie far below the Voigt values
(about 46 GPa). That is the regime where collagen compliance matters, so the Reuss column is not
dismissible on this evidence alone. But a 5× stiffer *hydrated* collagen is not supported by any
source I found: input 5 reaches ≈ 5 GPa only for dry fibrils or isolated molecules.

## 4. Result

**My value (calculated):** a material or protein route raises fin-ray EI by **≈ 3.6×** at most
(central estimate, zebrafish E_native = 8.7 GPa against the 31.3 GPa bone ceiling).

- Uncertainty band for F_A: 2–23×. The spread comes almost entirely from E_native, which is poorly
  pinned down (±100 % SD in input 1; a different species and method in input 2).
- The part attributable to *protein* alone, with mineral fixed: **1.01×–~2×** for a plausible
  2× stiffer hydrated collagen, and ≤ 5× only under the iso-stress bound with dry-state collagen
  stiffness.
- For comparison, the central 3.6× equals only a ~1.38× increase in solid-ray radius.

**Answer to S13 as I framed it:** no published or derivable evidence shows that a stiffer
structural-protein variant can raise fin-ray EI by more than a small multiple. The material ceiling
is set by mineral, not protein, and a modest geometric change matches it. Whether "a small multiple"
is enough depends on a required-EI target. I could not find one in the repository, so I cannot
turn this into a hard feasibility verdict.

**Scope of negative searches:**
- I did **not** search for engineered or designed collagen (col1a1/col1a2) or actinodin variants
  with measured stiffness. "None found" therefore applies only to the five web searches listed here
  plus the repository searches in §0.
- I did not read any primary paper in full text. Every number above is at search-summary read-level.

## 5. Comparison with the recorded value

I did not read the recorded derivation's numbers. The only things I know about it are its commit
subject ("derived negative on the materials route") and the stem `[S13] No`. My result is also
negative on the materials route, but I learned that direction before deriving, so the agreement on
direction is contaminated. On the number I **CANNOT TELL**.

```swarm-replication
{"claim_id": 197, "my_value": "max fin-ray EI gain via material/protein route ≈ 3.6x (range 2–23x, protein-only 1.01–~2x; calculated, not observed)", "agrees": null,
  "note": "Independently negative on the materials route, but I saw the recorded derivation's commit subject ('derived negative') before deriving and never saw its number, so agreement cannot be judged."}
```
