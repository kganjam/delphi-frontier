# Challenge 80: lat4a = slc43a2a (NCBI GeneID 393221)

**Claim under review** (not written by me): "lat4a = slc43a2a, resolved by the paper's OWN MAPPING rather
than name similarity: Daane et al. map nr21 to chromosome 15, and of the two zebrafish SLC43A2 paralogs
slc43a2a is on chr15 while slc43a2b is on chr10. LAT4 is the protein name of SLC43A2."
Recorded value: 393221 (NCBI GeneID). Recorded evidence level: derived.
Cited source: `fish-alleles/README.md`. That file is **not on any of the 339 remote branches of this
repo** (I checked with `git ls-tree` on every branch), so I could not read the author's own working. I
checked every premise from primary sources myself.

**Verdict: SURVIVED.** I could not break it. A second test, independent of the chromosome argument,
reaches the same answer. I record one caveat about the GeneID's RefSeq protein below.

## 1. Premises, re-checked independently

| Premise | What I did | Result | Read-level |
|---|---|---|---|
| Daane et al. map nr21 to chr15 and name the gene lat4a | PMC efetch of PMC9172250 (Daane JM et al., "Modulation of bioelectric cues in the evolution of flying fishes", *Curr Biol* 2021, doi:10.1016/j.cub.2021.08.054; author manuscript) | Verbatim: "we mapped nr21 to chromosome 15 and identified a nonsynonymous mutation (T200K) in a conserved domain of the L-type amino acid transporter, lat4a" | full-text (author manuscript main text; supplement figures S2D–S2F not read) |
| The paper gives its own gene identifier | Searched the same full text for `slc43a2`, `SLC43A2`, `ENSDAR`, `ZDB-`, `NM_`, `XM_`, `lat4b`, `paralog` | No accession or ZFIN ID for lat4a. The only `Slc43a2` string is ref. 17 (Guetg et al. 2015, "Essential amino acid transporter Lat4 (Slc43a2) ..."). The paper does not mention a second lat4 paralog. | full-text |
| Exactly two zebrafish SLC43A2 paralogs | NCBI esearch `slc43a2*[sym] AND Danio rerio[orgn]` | 2 hits: 393221, 494042 | listing (E-utilities) |
| slc43a2a on chr15, slc43a2b on chr10 | NCBI gene esummary | 393221 slc43a2a: chr 15, NC_141035.1:31099368–31139242. 494042 slc43a2b: chr 10, NC_141030.1:28023048–28041843 | listing (E-utilities) |
| LAT4 is the protein name of SLC43A2 | The paper's own ref. 17 title (above) | Consistent | full-text (the citation string only; Guetg 2015 itself not read) |

The chromosome logic follows. Exactly two candidate loci exist, only one is on chr15, and the paper
places the causative lesion on chr15. So the claim's inference holds given these premises. This is my
inference from the sources above, not a statement made in the paper.

## 2. Second test, independent of the chromosome argument (my calculation, not an observation from the paper)

The paper names the residue as **T200** in the paper's own numbering. If the "a/b" assignment were
wrong, residue 200 should fail to be T in slc43a2a, or should also be T in slc43a2b.

Ensembl REST was blocked by this session's proxy (403 on rest.ensembl.org). I therefore used the
Ensembl protein FASTAs cached on `origin/work/genomics` under `data/genomics/artifacts/`. That makes
these sequences **listing-level, via a repo cache**; I did not fetch them from Ensembl myself. I
identified each protein by sequence, not by its label:

- ENSDARP00000120945 (571 aa): residue 200 = **T** (window `SYASSAVTFPGIKVI`); residue 326 = F (window
  `QSFMRSIFSPIFMLS`, compare the paper's medaka window QSFMKSIFSPIFLLS). Its first 153 residues share
  92.2% identity with NCBI NP_956545.1, the RefSeq protein for GeneID 393221 (slc43a2a), at offset 0.
- ENSDARP00000156564 (598 aa): residue 200 = **M**, residue 326 = D. It is identical at those windows to
  NCBI NP_001008585.1 (GeneID 494042, slc43a2b), where residue 200 = M.

T200 exists only in the slc43a2a product. That points to the same gene as the chromosome test. The two
tests use independent evidence: genomic position and protein sequence.

## 3. Adversarial points checked

1. **Arithmetic.** The claim does no arithmetic, only a two-way exclusion by chromosome, and I redid
   that from NCBI directly. The offsets and identities above are my own computation.
2. **Proxy.** "Same chromosome" stands in for "same locus". This is adequate only because there are just
   two paralogs and they sit on different chromosomes. If a third, unannotated slc43a2-like locus sat on
   chr15, the chromosome test alone could not exclude it. The T200 match closes most of that gap, but I
   did not search the genome for unannotated copies (scope: NCBI Gene symbol search only).
3. **Hidden assumption: name suffix congruence.** The claim says it avoids relying on "lat4a ↔
   slc43a2a" name similarity. The chromosome test does avoid it. Relaxing the assumption (letting the
   paper's "a" be arbitrary) does not change the answer, because both the chromosome test and the T200
   test identify slc43a2a.
4. **Assembly drift.** NCBI coordinates are on NC_141035.1 (GRCz12tu). The paper predates GRCz12. The
   repo's validation slice is labelled chr15:28.36–28.42 Mb, which I take to be GRCz11 (not verified
   independently). The coordinates differ, but the chromosome assignment (15) agrees across both.
5. **Evidence level.** "derived" is honest. The paper never prints "slc43a2a" or 393221, so the mapping
   is an inference, and labelling it derived is correct.
6. **Caveat, not a refutation.** The RefSeq protein attached to GeneID 393221 (NP_956545.1) is only
   **153 aa**, and it does not reach residue 200. Anyone using GeneID 393221 to pull a sequence and read
   T200/F326 will get nothing from that RefSeq. A full-length model (for example Ensembl
   ENSDARP00000120945) is needed. The GeneID is the correct gene; its RefSeq protein is not a usable
   sequence source for this question.
7. **Corroboration.** A web search summary says ZFIN attributes slc43a2a phenotype figures to Daane et
   al. 2021 (read-level: **search-summary**; I did not open the ZFIN page). This is consistent with the
   claim but is not counted in the verdict. PMC8217709 (Stewart et al., longfin/kcnh2a, *Development*
   2021) is a different paper and is not relevant to nr21.

## Verdict rests on

- Daane et al. 2021 main text (PMC9172250): nr21 maps to chr15, gene named lat4a, T200K.
- NCBI Gene: exactly two *D. rerio* slc43a2 loci; 393221 on chr15, 494042 on chr10.
- Repo-cached Ensembl proteins ENSDARP00000120945 / ENSDARP00000156564, identified by sequence identity
  against NCBI RefSeqs NP_956545.1 / NP_001008585.1.

```swarm-challenge
{"claim_id": 80, "outcome": "survived", "reason": "Daane et al. 2021 full text maps nr21 to chr15 and NCBI places only slc43a2a (GeneID 393221) there; independently, T at the paper's residue 200 occurs in the slc43a2a protein and not in slc43a2b (M), though the GeneID's own RefSeq protein NP_956545.1 is a 153-aa fragment unusable for residue reads.",
  "corrected_value": null,
  "depends_on": ["Daane et al. 2021 Curr Biol (PMC9172250) main text: nr21 mapped to chromosome 15, gene lat4a, T200K", "NCBI Gene esummary: 393221 slc43a2a chr15; 494042 slc43a2b chr10; no other D. rerio slc43a2 symbol", "Ensembl ENSDARP00000120945 (T200, F326) and ENSDARP00000156564 (M200) as cached on origin/work/genomics, matched to NP_956545.1 and NP_001008585.1 by sequence"]}
```
