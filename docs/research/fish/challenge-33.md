# Challenge 33: "LAWENTRY wing-loading dispatched"

Reviewer: adversarial review of a claim recorded from session `session_01HsfzfufBJiUuuzDCjQ1e9K`.
Recorded evidence level: unknown. Recorded value: n/a.

## 0. What the claim is

The claim states a process fact, not a quantity: a law-library entry for wing loading was
produced and sent out. I could not read the source session (`list_events` returned "resource not
found"). I found the work product by searching git history on every remote branch. It is commit
`0e8f5c61` ("Law library: wing loading vs body mass, and the contested ceiling on powered
flight"). The commit carries that session's `Claude-Session` trailer and adds
`library/laws/wing-loading.yaml` (165 lines) on branch `origin/claude/wing-loading-law-m65wyw`.

My inference, not the author's statement: "dispatched" means the entry was written, committed and
pushed. On that reading the claim is true. Checked facts:

- The commit exists and is pushed to `origin/claude/wing-loading-law-m65wyw` (observed, `git branch -r --contains`).
- It is **not** on `origin/main` (observed, `git merge-base --is-ancestor` returned false). "Dispatched" must not be read as "merged".
- The repository's own checker passes. Running `library/tools/check_laws.py` on that branch's `library/` tree printed `3 entries, 0 problems` (observed by me, this session), which matches the commit message.

The recorded evidence level is "unknown". That is honest but understated: the claim can be
checked directly from the repository, and I have checked it. It has no number, so there is no
measured-versus-derived defect to find.

Because the claim is thin, I went on to attack the substance of the dispatched entry.

## 1. Arithmetic, redone independently

All of the following are my own recalculations from the entry's stated inputs (python, this session):

| Item | Inputs | My result | Entry |
|---|---|---|---|
| Argentavis Q | 70 kg × 9.81 / 8.11 m² | 84.67 N/m² | 84.7 (paper 84.6) |
| Quetzalcoatlus Q, Chatterjee & Templin | 70 × 9.81 / 9.55 | 71.91 N/m² | 71.91 |
| Quetzalcoatlus Q, Witton | 259 × 9.81 / 11.36 | 223.66 N/m² | 223.66 |
| Ratio of the two | — | 3.11 | 3.1 |
| Danio design check Q | 4e-4 × 9.81 / 2e-3 | 1.962 N/m² | 1.96 |
| Danio stall speed | sqrt(2 × 1.962 / (1.2 × 1.0)) | 1.808 m/s | 1.81 |
| Seabird Q exponent | 1 − 0.58, CI 1 − [0.62, 0.53] | 0.42 [0.38, 0.47] | same |
| Hummingbird Q exponent | 1 − [1.1, 1.3] | −0.1 to −0.3 | same |
| Power-margin exponent | 2/3 − 7/6 | −1/2 | same |
| Dimension of k | [Q]/M^(1/3) | M^(2/3) L⁻¹ T⁻² | same |

No arithmetic error.

## 2. Source checks (read-levels)

- **Sato et al. 2009, PLoS ONE, PMC2670537.** Read-level: full-text, via a tool-mediated extraction.
  It confirms WA = 0.15·M^0.58 (exponent CI 0.53–0.62) from 22 birds of 4 species. It confirms the
  take-off exponent −0.30 and the cruising exponent −0.18, and 41 kg (bootstrap CI 26–75 kg) at a
  5.1 m span. The paper frames 41 kg as a limit on *soaring animals*, derived from their flapping
  capacity. The entry's label "Sato, soaring" matches the authors' framing, and its mechanism text
  correctly says the limit is kinematic. Not a defect.
- **Witton & Habib 2010, PMC2981443.** Read-level: full-text, first 100k of 175k characters, the
  same partial read the author had. It confirms the methods text "180–250 kg for *Q. northropi*"
  and the Table 1 rows (70.00 kg / 9.55 m² / 71.91; 259.06 kg / 11.36 m² / 223.66). The abstract
  says "200–250 kg". The entry uses 180–250 in `where_it_breaks` and 200–250 in `contested_by`.
  Both figures are in the source, so I preserve the difference rather than call it an error. The
  Witton row (259 kg) sits slightly above the paper's own preferred range. The entry does not
  remark on this, but it does not misreport it either.
- **Skandalis et al. 2017, Nat. Commun.** Read-level: search-summary, the same level the author
  recorded. The summary confirms the 1.1–1.3 range and ~0.7 for other birds. A secondary source
  in the same search attributes the 1.1–1.3 range to **Greenwalt 1962**, which Skandalis cites.
  The entry presents the range as "reported by Skandalis". My inference: that is a citation-chain
  imprecision, not a wrong number. The exponent is against body *weight*, which gives the same
  exponent as against mass.
- I did not re-read Chatterjee 2007 or Ksepka 2014 (scope limit). Their values (70 kg, 8.11 m²,
  170 W vs ≥600 W; *P. sandersi* 21.9–40.1 kg; 12–16 kg) are unverified by me. They are not refuted.

## 3. Proxy, hidden assumption, counter-examples

- **Proxy.** The entry itself says that Q is a proxy for flight capability and that it fails as
  one: the 3.1× spread from mass/area reconstruction swamps the scaling effect. No proxy is
  passed off as the target quantity.
- **Hidden assumption: the "within-clade" seabird exponent.** The 0.58 exponent pools 22
  individuals from 4 species, so intraspecific and interspecific variation are mixed together. My
  inference: "steeper than isometric within this clade" rests on effectively 4 species clusters.
  The CI excludes 2/3, so the direction holds as fitted, but how it would generalise to all
  Procellariiformes is untested. The entry flags this as "my inference". Relaxing the assumption
  weakens the generality but does not reverse the sign.
- **Unsourced attribution (a real but minor defect).** Item (5) of `where_it_breaks` says "the
  theory's own authors attribute this to a reliance on burst/anaerobic take-off". No source is
  attached, and the theory's originating source (Pennycuick 2008) is listed as could-not-access.
  This sentence should either cite where the attribution was read or be marked as the author's
  inference. The bustard masses (18–21 kg) are marked search-summary, which is acceptable.
- **Counter-examples the author missed.** Insects and bats are not covered, and the entry already
  records that as a stated gap in its negative searches. I found nothing the entry asserts that a
  published counter-example contradicts. My scope: the three source fetches/searches above, on
  2026-11-04. I did no separate literature search for bat or insect scaling.

## Verdict: SURVIVED

The claim as stated, that the wing-loading law entry was dispatched, is true. The commit exists,
is pushed, and passes the repository's checker. It is not merged to main. Every number in the
entry that I recalculated reproduces. Every source value I re-read matches. The defects I found
are minor wording and attribution issues inside the entry: the unsourced "theory's own authors"
sentence, and the Skandalis versus Greenwalt citation chain. Neither changes any value, so I do
not record them as weakening the claim.

```swarm-challenge
{"claim_id": 33, "outcome": "survived", "reason": "Commit 0e8f5c61 (library/laws/wing-loading.yaml) exists on origin/claude/wing-loading-law-m65wyw, not main, and passes check_laws.py (3 entries, 0 problems); all arithmetic and the re-read Sato/Witton-Habib/Skandalis values reproduce, leaving only minor attribution wording issues.", "corrected_value": null}
```
