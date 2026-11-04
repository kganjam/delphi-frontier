# Challenge 15 — kcnk5b selectivity-filter motif count

**Claim under review (author's):** "kcnk5b carries EXACTLY TWO K+ selectivity-filter motifs
`[TS].[GAS][YFL]G` — TIGYG at 98-102 and TVGFG at 203-207 — the defining two-pore K2P architecture."
Recorded evidence level: *derived*; value: 2 motifs.

**Verdict: SURVIVED** (with scope notes below; no correction to the value).

## Sources (with read-level)

| Source | What | Read-level |
|---|---|---|
| UniProt Q6PFU3 (Q6PFU3_DANRE, unreviewed, 448 aa, GN=kcnk5b, ZFIN ZDB-GENE-040426-1297) | FASTA + flat file (TRANSMEM features) | full-text (entry downloaded via rest.uniprot.org) |
| UniProt A0A8M1PBI1 (unreviewed, 448 aa, "Potassium channel subfamily K member 5b") | FASTA | full-text |
| UniProt O95279 (KCNK5_HUMAN, reviewed) | FASTA, ortholog comparator | full-text |
| UniProt E7F5V5 (Actinodin1, *and1*) and A9JRX1 (returned by `gene:and2 AND organism_id:7955`; protein name "Zgc:175106") | negative controls | full-text |

No literature was consulted; everything below is computed from these sequences.

## 1. Independent re-computation (calculated, not observed)

Own Python regex scan (overlapping lookahead) of Q6PFU3, written independently of the author's script:

- `[TS].[GAS][YFL]G` → **2 hits: TIGYG 98–102, TVGFG 203–207.** Matches the claim exactly.
- A0A8M1PBI1 (the second UniProt kcnk5b record) is residue-for-residue identical to Q6PFU3 (0 differences / 448) → same 2 hits. The result does not depend on which zebrafish record is picked.
- Negative controls: E7F5V5 (and1) 0 hits, A9JRX1 (and2 query result) 0 hits — reproduces the author's controls.

## 2. Proxy check

A regex hit is a proxy for "a P-loop selectivity filter". I tested whether the hits sit where a K2P pore loop must sit, using UniProt's predicted TRANSMEM features (themselves computational predictions, not structures):
TM1 7–26, TM2 116–137, TM3 158–185, TM4 229–250.
- Hit 1 (98–102) lies between TM1 and TM2 → P1 position.
- Hit 2 (203–207) lies between TM3 and TM4 → P2 position.

This is the M1-P1-M2-M3-P2-M4 topology of a K2P subunit, so the proxy and the structural quantity agree here (inference from predicted topology, not from a solved structure). The human ortholog O95279 shows the same layout (TIGYG 98–102, TIGFG 203–207; P2 differs from fish only at I→V), consistent with the claim.

## 3. Hidden assumptions, relaxed

- **Pattern stringency.** Relaxed `G[YFL]G` still gives exactly 2 in kcnk5b (100–102, 205–207) but gives 2 spurious hits in the and1 control (GYG 532–534, 549–551) and 1 extra in human KCNK5 (GLG 326–328, C-terminal, outside the pore). So the T/S anchor is what keeps the controls clean; the kcnk5b count is robust to relaxation, the controls are not. Tightened `[TS][IVL]G[YFLHM]G` also gives exactly 2.
- **Chance-hit rate.** Using kcnk5b's own amino-acid composition, the per-site probability of the 5-mer pattern is ≈3.0×10⁻⁴, giving ≈0.13 expected random hits over 448 aa (calculated). Two hits at the two predicted P-loop positions are not plausibly chance.
- **"Exactly two" vs. all forms.** Only the UniProt protein products were scanned. I did not scan Ensembl/RefSeq alternative transcripts; an isoform lacking exon(s) could carry fewer motifs. Scope of the negative (no third motif): the two 448-aa UniProt kcnk5b records only.

## 4. Evidence level

"Derived" is honest: the count is a computational regex result on a database sequence (UniProt record itself is PE=2, transcript-level evidence, unreviewed). Nothing is presented as measured. One wording caveat: "the defining two-pore K2P architecture" is an interpretation; the regex establishes two motifs, while the two-pore architecture is supported here only by predicted topology and orthology, not by structure or electrophysiology of the zebrafish protein.

## 5. Counter-examples sought

- K2P filters are known to deviate from GYG in P2 (GFG/GLG are common), which is why the author's `[YFL]` class was needed; the claim already accommodates this. A K2P member with a non-T/S first position or a non-[YFL] aromatic at P2 would be missed by this regex, but kcnk5b is not such a case (both hits found).
- No evidence found of a third P-loop or of a filter loss in kcnk5b; search scope = regex variants above on Q6PFU3/A0A8M1PBI1 only.

## Conclusion

The arithmetic (2 motifs, at 98–102 and 203–207) reproduces independently; positions match predicted P1/P2 loops; controls are clean; chance expectation is ≈0.13. Residual caveats (isoforms not scanned; architecture inferred, not observed) narrow scope but do not change the value.

```swarm-challenge
{"claim_id": 15, "outcome": "survived", "reason": "Independent regex scan of Q6PFU3 (and identical A0A8M1PBI1) gives exactly TIGYG 98-102 and TVGFG 203-207, both in predicted P1/P2 loops, with clean controls and ~0.13 expected chance hits; only isoform scope is untested.", "corrected_value": null}
```
