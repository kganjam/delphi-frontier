# Cross-check: claude-evo's flying-fish windows vs this project's miniprot hits

**Scope.** Cross-check of two independent computational placements on the same unannotated assembly: claude-evo's CDS-only GeneWise ortholog windows and this project's miniprot protein-to-genome best hits. Neither is an annotation or an orthology proof, so an agreement means two methods agree, not that a locus is correct.

9 windows checked: **2 agree** (flush to the base), **2 paralog mismatch**, 0 land at a different gene of mine, 1 disagree on scaffold, 4 not comparable because I never queried that gene.

A window anchored upstream of a predicted start codon should sit flush against the CDS it belongs to: ending where the hit starts on the + strand, starting where it ends on the −.

| their symbol | their region | strand | my nearest hit there | gap bp | flush | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| fgf20a | HS2092:897466-899465 | +1 | — | None | None | DISAGREE on scaffold: I queried fgf20a and my hit is on JAGFBZ010000863.1, not on their JAGFBZ010002092.1 |
| shha | HS1012:2185729-2187728 | +1 | shha (round1) | 0 | True | AGREE: flush against my hit for the same gene |
| msx1b | HS2207:4758774-4760773 | -1 | — | None | None | NOT COMPARABLE: I never queried msx1b, so I have no independent placement for it |
| sp7 | HS0074:3788160-3790159 | -1 | — | None | None | NOT COMPARABLE: I never queried sp7, so I have no independent placement for it |
| runx2b | HS2275:410708-412707 | -1 | — | None | None | NOT COMPARABLE: I never queried runx2b, so I have no independent placement for it |
| lef1 | HS0865:1690350-1692349 | +1 | hhip (round2) | 1652899 | False | NOT COMPARABLE: I never queried lef1, so I have no independent placement for it |
| tbx5a | HS1382:1633754-1635753 | +1 | tbx5a (round1) | 0 | True | AGREE: flush against my hit for the same gene |
| fgf10a | HS2193:503910-505909 | -1 | fgf10b (round3) | 325 | False | PARALOG MISMATCH: nearest hit of mine on this scaffold is 'fgf10b' (325 bp away), and my own fgf10a hit is on JAGFBZ010000446.1 |
| kcnk5b | HS0776:65364-67363 | -1 | kcnk5a (round3) | 1 | True | PARALOG MISMATCH: their 'kcnk5b' window is flush against MY 'kcnk5a' hit |

## Their dropped flying-fish `hoxd13a`

- their stated reason: no ortholog hit with a clean 2 kb ACGT-only window
- my hoxd13a best hit: JAGFBZ010000479.1 5214025–5216883 (+), coverage 0.824, identity 0.447
- scaffold length 6138190; 2 kb upstream available: 2000 bp; non-ACGT bases in it: 0

A clean 2 kb ACGT-only window DOES exist immediately upstream of my hoxd13a hit on this strand. Their drop reason was 'no ortholog hit with a clean 2 kb ACGT-only window'; the two halves of that reason are separable, and this result is consistent with the ORTHOLOG-HIT half failing in their GeneWise model rather than the window being unclean. It does not show their model was wrong: my hit is a protein alignment, not an ortholog call, and my hoxd13a hit is the weakest in my table (coverage 0.824, identity 0.447).
