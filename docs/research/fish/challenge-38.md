# Challenge 38 — Daane et al. 2021 flying-fish fin proportions in zebrafish

**Claim under review (author: not me; source cited as `S22-dna.md`):**
"Daane et al. 2021 (Curr Biol 31:5052-5061.e8, doi:10.1016/j.cub.2021.08.054) phenocopied
flying-fish fin PROPORTIONS in zebrafish by crossing two dominant alleles, lat4a^nr21/+ (T200K)
and the longfin allele kcnh2a^lof/+." Recorded evidence level: literature. Value: n/a.

**Verdict: SURVIVED**, with one scope note on the word "phenocopied" (see §4).

## Sources and read-levels

| Source | Read-level | Notes |
|---|---|---|
| Daane et al. 2021, PMC9172250 (author manuscript) | full-text, partial: characters 0–100,000 of ~149,000 read through a fetch tool that summarises. Quotes below come from that tool's output, not from reading the page myself | main evidence |
| ZFIN figure pages ZDB-FIG-221222-34 / -35 (Daane et al. 2021 Figs. 3–4) | search-summary (direct fetch returned HTTP 503 / DNS failure) | legend text agrees with PMC |
| ZFIN publication record ZDB-PUB-210918-31, NOAA repository record, X-MOL listing | search-summary / could-not-access (503 or host blocked) | citation metadata only |
| PubMed 34534441 | could-not-access (host not in the session's network allowlist) | — |
| `S22-dna.md` (the claim's own source) | could-not-access: no file of that name exists anywhere in this repository (searched the whole working tree, excluding .git) | I could not check the author's working |

## 1. Arithmetic

None. The claim contains no number to recompute. Citation metadata (Curr Biol 31, 5052–5061.e8, 2021,
doi 10.1016/j.cub.2021.08.054) matches the search listings, and the ScienceDirect PII S0960982221011908 matches the doi.

## 2. Each element checked against the paper (quotes from the PMC full text)

- **nr21 is dominant, in lat4a, T200K:** "We identified a dominant mutant, *nr21*, as having small adult
  fins"; "a nonsynonymous mutation (T200K) in a conserved domain of the L-type amino acid transporter";
  cis-frameshift revertants restore wild-type fins, "indicating that the mutation in *lat4a^nr21* results
  from a gain-of-function effect." — **confirmed.**
- **longfin is a dominant kcnh2a allele, notated kcnh2a^lof:** "The dominant *longfin* mutant (*lof^dt2*)";
  the paper itself writes *kcnh2a^lof*/+. Loss-of-function *kcnh2a* mutations in cis revert it. The lesion
  is a chromosome-2 inversion that upregulates *kcnh2a* in fins: a cis-regulatory gain of function, not a
  coding change. — **confirmed.** The notation matches the paper. ZFIN's formal allele name is `dt2`.
- **The cross is the double heterozygote:** "double mutants between *kcnh2a^lof*/+ and *lat4a^nr21*/+ are
  viable … the *lat4a^nr21*/+;*kcnh2a^lof*/+ fish show wild-type-sized medial fins, while the paired fins are
  overgrown"; Fig. 4 legend: "*nr21/lof* trans-heterozygotes exhibit elongated paired fins and a hypocercal
  caudal fin." — **confirmed.** The legend says "trans-heterozygote", but the two alleles sit in different
  genes, so this is a double heterozygote, as the main text says. Both terms describe the same fish.
- **"Proportions", not size:** this is the right quantity. The paper's point is that the effect is
  non-additive and differs between fins. lof/+ alone lengthens *all* fins and nr21/+ alone shortens
  *all* fins. Only the combination changes proportion: paired fins long, medial fins wild type. The
  claim's capitalised PROPORTIONS matches the paper.

## 3. Proxy / hidden assumption

- **Proxy:** in the paper, "flying-fish proportions" means a qualitative fin layout: long paired fins,
  medial fins not enlarged, and a hypocercal caudal fin. In the paper's figures, zebrafish fin length is
  normalised to standard length (Fig. 4B–C). The part of the main text I read gives **no numerical
  comparison** to flying-fish ratios, such as pectoral length / SL in *Exocoetidae*. The quoted
  conclusion is the authors' own judgement: "remarkably similar to that of flying fishes."
- **Assumption relaxed:** if "phenocopied" meant quantitative agreement, with zebrafish ratios inside the
  flying-fish range, the paper as read does not support it. That match is `unknown`. I did not read
  the last ~49k characters of the PMC text or the supplementary tables, and I have not invented
  any magnitude. Read qualitatively, as the authors use it, the claim holds.

## 4. Evidence level

"literature" with value n/a is honest: the claim restates a published result and presents no derived
number. Scope note: "phenocopied" repeats the authors' qualitative framing ("sufficient to reproduce the
flying fish fin bauplan"). Downstream users should not read it as a measured match of ratios.
This is a caveat about how far the claim reaches. It is not an error in the claim, so I do not
downgrade to "weakened."

## 5. Counter-examples / regimes

- Not every flying fish has the convergent lat4a change. Search summaries of the paper report that the
  sailfin flying fish lacks the convergent lat4a allele (search-summary level, not verified in the full
  text). This bears on the evolutionary inference. It does not bear on the zebrafish phenocopy claim.
- The zebrafish nr21 T200K allele came from a zebrafish mutant collection (how it was induced: `unknown`, not checked). The claim does not say it is the same substitution
  as the flying-fish variants, and it should not be read that way. Whether the residues match is
  `unknown` from what I read.
- I found no published paper that fails to reproduce this result. Scope of that search: two web searches
  plus the paper's own text. No citation-tracking search was done.

## Conclusion

Every factual element checks against the full text: the paper, both alleles, the dominance of each,
T200K, the double-heterozygote cross, and the result being about proportion. The only soft spot is that
the phenocopy is qualitative and judged by the authors.

```swarm-challenge
{"claim_id": 38, "outcome": "survived", "reason": "PMC full text confirms dominant lat4a^nr21 (T200K, gain-of-function) and dominant cis-regulatory kcnh2a^lof, and that lat4a^nr21/+;kcnh2a^lof/+ double heterozygotes have overgrown paired fins with wild-type medial fins and a hypocercal caudal fin, which the authors call remarkably similar to flying fishes; the phenocopy is qualitative, with no numeric ratio match in the text read.",
  "corrected_value": null}
```
