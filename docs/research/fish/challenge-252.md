# Challenge 252: "a retrieval engine cannot tell a clause being asserted from one being denied"

**Verdict: WEAKENED.** The data shows that rewording claim 14 changed the engine's output. It does not
show *why*. The claim names a mechanism (the engine can't tell assertion from denial) and a remedy
(strip concessive clauses). The one measured pair can't tell that mechanism apart from at least two
others. The concessive clause is also the clause most clearly *asserted*, not denied. And the remedy
as written ("stripped") is not what the code does (it excludes the claim).

## What the claim rests on

Source: commit `699f320d` ("Run every claim past the GXL evidence API…"), commit message and
`swarm/evidence.py`. Read-level: **full-text** (git object in this repo). The measured pair, as the
author recorded it:

| Phrasing of claim 14 | supports | refutes | neutral |
|---|---|---|---|
| "the actinodins are NOT collagen-like DESPITE actinotrichia being historically termed elastoidin" | 2 | 6 | **not recorded** |
| "the identical finding phrased as a clean chemical statement" (exact text **not recorded**) | 0 | 0 | 35 |

I could not see the passages the engine returned. The GXL/Paperclip API and the `designswarm`
Postgres instance are not reachable from this sandbox (`could-not-access`). So I can't re-query, and
I can't read the 6 "refuting" passages.

## 1. Arithmetic, redone

Nothing much to compute. I redid it from the recorded counts. Net signal (supports − refutes) goes
from 2 − 6 = **−4** to 0 − 0 = **0**. The refute count drops by 6. Supports also drop, from 2 to 0.
That second point matters: **the clean phrasing is not supported by the engine either.** All 35
passages came back neutral. The rewording moved the claim from "net refuted" to "no stance". It did
not move it to "supported". The author's sentence "returned 0 refutes and 35 neutral" is accurate.
But readers could easily take "the spurious signal is retracted" to mean the clean claim was
confirmed, and it wasn't. The with-clause neutral count is missing, so the size of the retrieved
pool can't be compared between the two runs. That leaves open whether the rewording changed
*retrieval* (which passages came back) or *stance scoring* (how the same passages were judged).

## 2. Proxy: where the effect comes from

The claim attributes the change to the **concessive clause**. The two phrasings differ in at least
three ways at once:

1. the concessive clause ("despite … termed elastoidin") was removed;
2. the matrix negation ("NOT collagen-like") was removed or reworded. A "clean chemical
   statement" about glycine periodicity would not normally contain "NOT";
3. the topic changed. The words *actinotrichia*, *elastoidin* and *collagen* probably dropped out,
   which changes what gets retrieved (see the missing neutral count above).

The quantity that matters is how much of the change comes from the concessive clause on its own.
The pair can't separate the three. A 2×2 test would: {with/without concessive} × {with/without
"NOT"}, with the topic words held fixed, and the neutral count recorded each time. This is my
inference about the experimental design. It is not a measurement.

## 3. Hidden assumption: that the 6 refutes are spurious

The whole claim assumes the engine got the claim wrong. Relax that and see what follows.

- What the literature says about what actinotrichia are made of: Durán et al. 2011, *Dev. Biol.*
  354:160–172, "Actinotrichia collagens and their role in fin formation". It reports actinotrichia
  are built from collagen I plus a fish-specific collagen II (col2a1b). Read-level:
  **search-summary/abstract** (via portaldelainvestigacion.uma.es and the search result; full text
  not read). Zhang et al. 2010, *Nature* 466:234–237, identifies actinodin 1/2 as the *non-collagen*
  structural parts of elastoidin. Read-level: **listing/search-summary**.
- The claim sentence uses "actinodins" and "actinotrichia" close together. A reader, or a stance
  model, could take it as "actinotrichia/elastoidin is not collagen-like". Durán 2011 does refute
  that reading.

So there's a second explanation the data can't rule out. The engine may have read the **denial**
correctly ("NOT collagen-like") and then found literature that contradicts that denial for a
closely related subject (actinotrichia). If so, it *can* tell asserted from denied, and the 6
refutes reflect a claim whose subject is ambiguous. They wouldn't be a semantic blind spot. I can't
decide between the two explanations without the passages, so it's **unknown**. The author's
universal "cannot tell" is therefore not established by this evidence.

## 4. Is the analogy right, and is the evidence level honest?

- **The analogy points at the wrong clause.** A forbidden-string check fails on use versus mention:
  a quoted string isn't being asserted. A concessive clause is the reverse. "Despite actinotrichia
  being historically termed elastoidin" *concedes the clause is true*. The author asserts it. The
  only clause in claim 14 that is *denied* is "collagen-like", under "NOT". So "cannot tell a clause
  being asserted from one being denied" fits the **negation**, not the concessive. The remedy goes
  after the concessive. Known weaknesses of NLI/stance models are about negation and scope more than
  concession. I recall this from the literature generally. I didn't fetch a source in this session,
  so I cite none.
- **The remedy as stated doesn't match the code.** The claim says statements "must be stripped of
  concessive clauses". `swarm/evidence.py` instead **excludes** any claim matching
  `(despite|although|notwithstanding)`. Stripping would change what the claim says. Excluding
  creates a selection bias: claims with concessions never get an external check. The regex also
  misses "NOT", "but", "unlike", "rather than", "contrary to", "while", "even though" (it matches
  "although" but not "though"), and it doesn't catch negation at all. That's the more likely culprit
  from §2–3.
- **Evidence level "derived" from "the measured pair".** The label isn't false, since the
  generalisation is inferred and doesn't claim to be measured. But the support is **n = 1**,
  confounded, with one of the six counts missing. The commit calls it "LIMITATION ONE, MEASURED BOTH
  WAYS", which reads as more than it is. Honest label: *hypothesis suggested by one confounded
  pair*.

## 5. Counter-regimes the author missed

- Claims with **no concessive** that negate ("X does NOT do Y") go through the current filter
  unchanged. If negation is the real mechanism, those claims are still at risk, and the filter gives
  false confidence.
- Concessive claims whose concession is **true and well supported** (as in claim 14) could add
  *supports* rather than refutes. Stripping them throws away correct context. A concession is not
  always noise.
- Scope of my negative search: I searched the git history of this repo (`git log --all -S`) for
  "concessive", "gxl", "elastoidin" and "claims/support". The only GXL commits are `de44fffd` and
  `699f320d`. Neither records more pairs, the clean phrasing's text, or the neutral count for the
  with-clause run. I ran one web search (standard mode, 2026-11-04) on actinotrichia composition.

## What survives

Rewording claim 14 to drop the concession, the negation and the elastoidin framing changed the net
signal from −4 to 0. Putting several propositions into one claim can make the engine's
support/refute counts uninterpretable. **Supportable rewording:** "Claim statements sent to a
stance engine should each make one proposition, with no negation or concession. The claim 14 pair
(2/6 → 0/0/35) shows the phrasing changes the result but does not tell us which clause caused it."

```swarm-challenge
{"claim_id": 252, "outcome": "weakened", "reason": "The single measured pair changed the concessive clause, the matrix negation and the topic words at once, so it cannot attribute the effect to concession; the concessive clause is the asserted (not denied) one, the 6 refutes may be genuine (Durán 2011: actinotrichia contain collagen I/II), and the code excludes rather than strips such claims while missing plain negation.", "corrected_value": null, "depends_on": ["commit 699f320d: claim 14 counts 2 sup / 6 ref (neutral unrecorded) with clause vs 0 sup / 0 ref / 35 neu clean", "clean rephrasing text of claim 14 (unrecorded; assumed to drop NOT and elastoidin wording)", "swarm/evidence.py exclusion regex (despite|although|notwithstanding)", "Durán et al. 2011 Dev Biol 354:160-172 abstract-level: actinotrichia comprise collagen I and col2a1b", "Zhang et al. 2010 Nature 466:234-237 listing-level: actinodins are non-collagen elastoidin components"]}
```
