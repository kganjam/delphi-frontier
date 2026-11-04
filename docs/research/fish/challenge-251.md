# Challenge 251: does the GXL engine score a concessive clause as refuting?

**Claim under review (the author's words):** "GXL EVIDENCE API LIMITATION, measured: it scores against the claim
text as given, so a claim CONTAINING the assertion it denies gets that clause scored as refuting it. Claim 14 ("the
actinodins are NOT collagen-like DESPITE actinotrichia being historically termed elastoidin") returned 2 supports /
6 refutes; the same claim phrased as a clean chemical statement returned 0 refutes / 35 neutral."
Recorded evidence level: *measured*. Value: 6 spurious refutes. Source: GXL claims/support, both phrasings run.

**Verdict: WEAKENED.** The two count vectors are plausibly real API output. They do not, however, measure
the quantity the claim names, which is how many refutes the concessive clause caused. The word "spurious", the
causal mechanism, and the general rule built on it are all inference from one pair of runs. That pair changed
more than one thing at once, nobody recorded reading the refuting passages, and the run contradicts one prediction
of the author's own mechanism. There is also a literature reading in which some or all of the 6 refutes are
correct, not spurious.

---

## 0. What I could and could not access

| Source | What it is | Read-level |
|---|---|---|
| `origin/swarm-architecture` commit `699f320d`, message plus `swarm/evidence.py` | The only record of the two runs. Gives the counts above and the exclusion regex they led to. | full-text |
| `origin/swarm-architecture:library/pages/project/claims.md` | Claim table. Claim 14 appears; neither GXL run's raw output does. | full-text (grep lines) |
| Raw GXL JSON responses, the returned passages, and the exact text of the "clean chemical statement" | Not committed on any branch. | could-not-access |
| `artifact_signal` rows written by `evidence.py` (Postgres on `127.0.0.1:5436` on the author's host) | Not reachable from this session. | could-not-access |
| Re-running `paperclip.gxl.ai/api/v1/claims/support` myself | No `PAPERCLIP_API_KEY` in this environment, so I did not call the endpoint. | could-not-access |
| Damodaran, Sivaraman & Dhavalikar 1956, *Biochem J* 62:621–625, PMID 13315224, PMC1215972 | Amino-acid composition of elastoidin from shark ceratotrichia | search-summary (the PMC page has only scanned page images; I did not read the tables) |
| Durán et al. 2011, *Dev Biol* 354:160–172, PMID 21420398 (cited in `challenge-14.md`) | Actinotrichia contain Collagen I and a fish Col2 (`col2a1b`) | search-summary, second-hand via challenge-14 |

Scope of my search for the raw run records: `git grep -I` over all 645 `origin/*` refs, limited to `*.md`, `*.json`,
`*.jsonl` and `*.py`, for `claims/support`, `35 neutral`, `elastoidin`, `2/6`, `0/35`, `6 refut` and `concessive`. The only
hits for the GXL run were the commit and the two files above.

## 1. Arithmetic, redone from the stated inputs

The figures below are **computed by me from the author's counts**. None of them is a new measurement.

- Phrasing A (with the clause): supports 2, refutes 6. That gives 8 decisive passages and a net of 2 − 6 = **−4**,
  which is the `value` that `evidence.py` would store. The neutral count is **not recorded**. Claim 242 also reports a
  pool of 35 from this engine. If the pool here was 35 too, the neutral count would be 27, but that figure is my
  inference and is `unknown` from the record.
- Phrasing B (clean): refutes 0, neutral 35. The commit gives no supports count. Reading it as 0 supports, because
  0 + 0 + 35 = 35 matches the pool size, is again my inference.
- A notation inconsistency is real and checkable. The code comment says "Claim 14 showed **2/6** with the clause and
  **0/35** without it." In "2/6" the pair is supports/refutes. In "0/35" it is refutes/neutral. Read with the same
  convention, "0/35" would mean 0 supports and 35 refutes. This is a small reporting defect, but this comment is
  what a later reader of the exclusion rule will see.

The stated numbers do not contradict each other. The arithmetic stands, apart from the notation slip.

## 2. Proxy check: the quantity the claim needs is not the quantity that was measured

The claim names a quantity: **the number of refutes caused by the concessive clause being scored as an assertion.**
What was measured is the **difference in the count vector between two different query strings.** That difference
stands in for the named quantity only if the two strings differ *only* in the clause. They do not:

- Phrasing A contains "NOT", a negated predicate, *and* the "despite … elastoidin" clause. It probably also
  contained the glycine figures, because claim 14 as stored goes on with ": glycine is 5.4% and 4.5% …". Phrasing B
  is described only as "a clean chemical statement". Its exact text was not recorded. At least two variables moved:
  the concessive clause, and the topic vocabulary ("actinotrichia", "elastoidin") that steers retrieval toward
  different literature.
- **The author's own mechanism makes a prediction, and the run does not bear it out.** If the only effect of the
  clause were to turn its passages into refutes, then removing the clause should remove the refutes and *keep the
  supports*. The supports went from 2 to 0 (or to an unrecorded number; see §1). The more economical reading is
  that the clause changed **what was retrieved**, not just how one clause was scored. Without the elastoidin wording,
  the corpus returned nothing decisive on actinodin glycine content in either direction.

The quantity that would actually test the claim is a **per-passage attribution**. For each of the 6 refuting
passages: does its text address the elastoidin or actinotrichia clause, or the actinodin glycine statement? Does the
engine's rationale treat the clause as asserted? Nothing in the record shows that the 6 passages were read. Number of
the 6 refutes that are attributable to the clause and spurious: **unknown**.

## 3. Hidden assumption: "the refutes are spurious"

The label "spurious" carries the result. Relaxing it shows a reading in which the refutes are partly or wholly
**correct**:

- Elastoidin is reported as collagenous. Damodaran et al. 1956 found that elastoidin's amino-acid distribution
  "follows the general pattern characteristic of collagens", and that elastoidin is unusually rich in tyrosine and
  contains cystine. [search-summary]
- Actinotrichia contain true collagens (Col1 and Col2), and the actinodins are their *non*-collagen component
  (Durán et al. 2011). [search-summary, second-hand]

The claim-14 sentence is ambiguous about its subject. Its predicate "collagen-like" sits next to "actinotrichia …
termed elastoidin". A passage stating "elastoidin/actinotrichia is collagenous" therefore really contradicts one
natural reading of the sentence. `challenge-14.md` flagged that same contrast as misleading. **My inference, not the
author's claim:** an engine scoring such a passage as refuting may be resolving an ambiguous subject in a defensible
way, not "failing to tell asserted from denied". The two hypotheses predict different passage texts. Only the
unrecorded passages can tell them apart.

A second hidden assumption is generality. The rule "a claim containing the assertion it denies gets that clause
scored as refuting it" rests on **one claim, one run per phrasing**. No repeat was recorded, so run-to-run variance
of the engine is `unknown`. No second concessive claim was tested. Even so, the rule was turned straight into a
blanket exclusion (`statement !~* '(despite|although|notwithstanding)'`) over the whole claim set, and the
downstream effect of that exclusion has not been tested.

## 4. Is the evidence level honest?

**Partly.** The *counts* (2 supports and 6 refutes under phrasing A; 0 refutes and 35 neutral under phrasing B) are
API output, and "measured" fits them, with one caveat: the raw output is not preserved anywhere that can be checked.
The recorded **value, "6 spurious refutes", is not measured.** "6" is measured. "Spurious", and the claim that the
clause caused them, are interpretation. By the honesty floor's own rule, a derived quantity presented as measured is
a defect even when the number is right.

A stronger point: the counts on their own are compatible with "the clause caused 0 of the 6 refutes, and the clean
phrasing simply retrieved a different, uninformative pool". So the evidence level of the *mechanism* is
**inference from a confounded comparison (n = 1 pair).**

## 5. Regimes and counter-examples the author missed

- **The real-literature regime above (§3).** The elastoidin literature calls it collagenous, so refutes are expected
  even from an engine that parses negation perfectly.
- **The retrieval regime, as distinct from the scoring regime (§2).** Changing topic words changes the retrieved pool.
  The supports going from 2 to 0 is direct evidence that this happened here.
- **What the result does support.** It is real and useful as a narrower statement: *for this claim, the engine's
  verdict was not robust to rephrasing.* The same finding gave net −4 under one wording and net 0 (no decisive
  passages) under another. That justifies treating single-wording GXL signals as fragile. It does not show *which*
  mechanism produced the swing.

I found no published characterisation of GXL `claims/support` behaviour on negated or concessive claims. Scope: the
repository records above only. I did not search the web for GXL documentation.

## What would settle it

1. Commit the raw JSON for both runs, including the returned passages and the exact clean-phrasing string.
2. Classify each of the 6 refuting passages: about elastoidin or actinotrichia being collagenous, or about actinodin
   composition?
3. Run a minimal pair that differs only in the clause, for example "The actinodins are not collagen-like" with and
   without "despite actinotrichia being historically termed elastoidin". Run each phrasing at least 3 times, plus a
   second, unrelated concessive claim.

If 2 and 3 show that the clause-bearing refutes are about elastoidin and that they vanish in the minimal pair, the
claim survives in its original form.

## Recommended rewording

"GXL claims/support output for claim 14 was not robust to rephrasing: with the concessive elastoidin clause it
returned 2 supports / 6 refutes (measured, single run); a reworded 'clean chemical statement' (exact text not
recorded) returned 0 refutes / 35 neutral (measured, single run). Whether the 6 refutes were caused by the clause,
and whether they are spurious, is not determined: the passages were not inspected and the rephrasing also changed
the retrieval vocabulary. Elastoidin is reported as collagenous (Damodaran et al. 1956), so some refutes may be
correct on the actinotrichia reading."

```swarm-challenge
{"claim_id": 251, "outcome": "weakened", "reason": "The 2/6 vs 0/35 counts are plausible single-run API output, but 'spurious' and the clause-as-cause mechanism are inferred from one confounded rephrasing pair whose passages were never recorded as inspected, the loss of both supports contradicts the stated mechanism, and elastoidin is published as collagenous (Damodaran 1956) so the refutes may be legitimate.", "corrected_value": "6 refutes (measured, phrasing with clause, single run); refutes attributable to the clause and spurious: unknown", "depends_on": ["origin/swarm-architecture commit 699f320d message and swarm/evidence.py (only record of both GXL runs)", "claim 14 statement text as stored in library/pages/project/claims.md", "Damodaran, Sivaraman & Dhavalikar 1956 Biochem J 62:621, PMID 13315224 (search-summary): elastoidin amino-acid pattern is collagen-like", "Duran et al. 2011 Dev Biol 354:160, PMID 21420398 (search-summary via challenge-14): actinotrichia contain Col1/Col2", "absence of raw GXL responses on all 645 origin refs (git grep, *.md/*.json/*.jsonl/*.py)"]}
```
