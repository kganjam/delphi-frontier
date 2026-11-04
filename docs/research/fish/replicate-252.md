# Replicate 252: an independent re-derivation from the measured pair

**Claim 252, as given to me with the answer removed:** "This is the claiming-versus-quoting failure
at the SEMANTIC level." Where the inputs live: "inference from the measured pair."

**My value (calculated from recorded counts, not observed by me):** rewording claim 14 to remove the
concessive clause moved the GXL engine's net signal (supports − refutes) from **−4 to 0 passages**,
a shift of **+4**. That shift is made of **−6 refutes and −2 supports**. The clean phrasing is
**not supported** either (0 supports). It is *no stance* (35 neutral), not *confirmed*.
**Uncertainty:** n = 1 pair, no replicate queries, engine run-to-run variability unknown, and the
neutral count for the with-clause run is not recorded. So the shift has no error bar. Its
attribution to the concessive clause specifically is an inference, not a measurement (see §4).

## 1. How I found the inputs (and what I avoided)

- The branch for this task held nothing on claim 252. A `git grep` over every remote branch except
  `challenge-claim-252-*` for `concessive|claiming-versus-quoting|claiming vs quoting` found two
  files: `origin/swarm-architecture:swarm/evidence.py` and `challenge-253.md`. I didn't open
  `challenge-253.md`.
- I traced `swarm/evidence.py` to commit `699f320d` (2026-11-04). Its commit message contains the
  question's sentence word for word: "This is the claiming-versus-quoting failure at the SEMANTIC
  level: a retrieval engine cannot tell a clause being asserted from one being denied …". That
  places claim 252 as a derived generalisation drawn from the claim 14 pair.
- I did **not** read `docs/research/fish/challenge-252.md` (branch `challenge-claim-252-h22o2b`)
  until after §2–§4 below were done. I saw its commit title ("concessive-clause retrieval claim
  weakened") in a branch log before deriving. That's how I found the term "concessive". It also
  told me that a challenge existed and what its verdict was.

## 2. Inputs

| # | Input | Value | Source | Read-level |
|---|---|---|---|---|
| 1 | Claim 14 with concessive clause ("the actinodins are NOT collagen-like DESPITE actinotrichia being historically termed elastoidin") | 2 supports, 6 refutes, neutral **unknown** | commit `699f320d` message | full-text (git object) |
| 2 | Claim 14 as a "clean chemical statement" (exact text **unknown**, not recorded) | 0 refutes, 35 neutral; supports not stated, implied 0 by "0/35" | commit `699f320d` message + `swarm/evidence.py` comment | full-text (git object) |
| 3 | Same pair, code-comment form | "Claim 14 showed 2/6 with the clause and 0/35 without it" | `swarm/evidence.py` lines 78–80 on `origin/swarm-architecture` | full-text |
| 4 | Engine control | 28 supports for the control claim (floor 5) | commit `699f320d` message | full-text |
| 5 | The raw GXL responses / `artifact_signal` rows | **could-not-access** | `paperclip.gxl.ai` refused by this sandbox's egress proxy (HTTP CONNECT 403). The `designswarm` Postgres is on 127.0.0.1:5436 of another host. | could-not-access |

**Disagreement between sources, kept as found:** the commit message says "2 supports and 6
refutes". The code comment says "2/6". Read on its own, "2/6" looks like 2 of 6, which would be
4 refutes, not 6. I take the commit message as the fuller statement, so the inputs are 2 sup /
6 ref. I flag that the comment's shorthand is ambiguous and could be misquoted downstream. Also,
`evidence.py` calls the engine with `top_n=10`, yet the clean run returns 35 passages. The counts
must therefore cover a pool larger than `top_n`. I can't check how the pool is defined (`unknown`).

## 3. Arithmetic (calculated)

The signal the script writes is `value = sup − ref`, with `weight = sup + ref + neu`
(`evidence.py`, insert statement).

- With clause: value = 2 − 6 = **−4**. Weight = 8 + neu_with, where neu_with is unknown.
- Without clause: value = 0 − 0 = **0**. Weight = 0 + 0 + 35 = **35**.
- Δvalue = 0 − (−4) = **+4**. Δrefutes = −6. Δsupports = −2.
- Refute share among stance-bearing passages: with clause 6/(2+6) = **75%**. Without: 0/0, undefined
  (no stance-bearing passages).

Is 6 refutes vs 0 more than chance? (One-sided Fisher exact on refutes vs non-refutes. This is my
inference and needs neu_with, which is unknown, so I give the two ends of the range.)

- If neu_with = 0 (pool 8): table [[6, 2], [0, 35]], P = **4.6 × 10⁻⁶**.
- If neu_with = 27 (pool 35, same size as the clean run): table [[6, 29], [0, 35]], P = **0.012**.

Either way the drop is unlikely under "rewording does nothing", **if** passages are independent
draws. They aren't independent draws: the two phrasings retrieve different pools. So the P-value
only says the outputs differ. It doesn't say why.

## 4. What the pair does and does not support (my inference, separated from the author's claim)

- **Author's claim:** the engine "cannot tell a clause being asserted from one being denied". This
  is the same failure as a forbidden-string check that can't tell claiming from quoting.
- **My inference:** the pair shows that **phrasing changed the engine's output** (−4 → 0). It can't
  show the mechanism. The two phrasings differ in several ways at once: the concessive clause, the
  "NOT" negation, and probably the topic words (elastoidin/actinotrichia). The pair can't separate
  these. It also can't rule out that the 6 refutes were *correct* readings of an ambiguous subject.
  I didn't check the literature on actinotrichia composition here. That is out of scope for an
  arithmetic re-derivation, so I make no claim about it.
- Also, a concessive clause ("despite X being termed elastoidin") is *conceded*, i.e. asserted. The
  clause that is *denied* is "collagen-like", under "NOT". So the claiming-vs-quoting analogy fits
  negation better than concession. This is my reading. It isn't measured.
- Scope of negative searches: the git trees of all remote branches for the strings above, and one
  attempted HTTPS connection to the GXL API (refused). I didn't do a literature search.

## 5. Comparison with the recorded value (done after the derivation)

- I looked for claim 252's own row in `origin/swarm-architecture:library/pages/project/claims.md`.
  That table ends at claim 243, so there's **no recorded value field for 252** that I could find.
  Claim 252 is qualitative. As far as I can tell its only numbers are the pair in input rows 1–2.
- I then read `challenge-252.md` (another agent's challenge, not the recorded value). It redoes the
  same arithmetic and gets **−4 → 0**, with supports also dropping 2 → 0, and the neutral count
  unrecorded. That **matches** my figures. The challenge also reaches the same confound concerns
  (§4) that I reached. I wrote §4 before reading it, but after seeing its commit title.
- Verdict: **AGREE** on the arithmetic (Δnet = +4, −6 refutes, −2 supports) with the commit's
  counts and with the challenge's redo. **CANNOT TELL** for claim 252's recorded value, because I
  found none. I record `agrees: null` for that reason. The agreement with the challenge isn't fully
  independent: we both read the same single commit, and nobody re-queried the engine.

```swarm-replication
{"claim_id": 252, "my_value": "net GXL signal -4 -> 0 passages (+4; -6 refutes, -2 supports; clean phrasing 0 sup/0 ref/35 neu), n=1 pair, attribution to the concessive clause not separable from negation/topic change", "agrees": null, "note": "No numeric recorded value for claim 252 was found (claims table ends at 243); my arithmetic matches commit 699f320d's counts and the challenge-252 redo, but both rest on one unreplicated pair whose with-clause neutral count is unrecorded."}
```
