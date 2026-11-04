# Challenge 54: "LAWENTRY mcmahon-elastic dispatched"

**Claim under review (the author's words):** "LAWENTRY mcmahon-elastic dispatched".
Recorded evidence level: `unknown`. Value: n/a. Source session: `session_01EeoYQgcbcm2cFsHrzqhCRS`.

**Verdict: SURVIVED.** The dispatch happened. I could read the session, its prompt and the commit it
pushed. The deliverable passes the repo's law gate, and every number in it reproduced when I worked
it out myself. Two defects are real but neither refutes "dispatched": (1) the evidence level is
recorded *lower* than it should be, and (2) "dispatched" stands in for "landed", which has not
happened yet.

## What the claim asserts

"Dispatched" is a status claim. It says a worker session was sent to write the `mcmahon-elastic`
law-library entry. The claim itself contains no arithmetic. So I tested **(a)** whether the dispatch
left an observable trace, and **(b)** whether what it produced holds up. That matters because
"dispatched" is only a proxy (see below).

## (a) Did the dispatch happen? Observed

| Check | Result | Read-level |
|---|---|---|
| `get_session session_01EeoYQgcbcm2cFsHrzqhCRS` | exists. Title "McMahon elastic similarity law". Created 2026-11-04T08:14:09Z. Status bucket COMPLETED. Source `work/frontier-foundation`. Outcome branch `claude/mcmahon-elastic-law-bcc9q2` | full-text (session record) |
| First user event of that session, 08:14:09Z | *"Write ONE law-library entry: McMahon elastic similarity for limb and spar proportions … Write `library/laws/mcmahon-elastic.yaml` … commit it on a new branch."* | I read only part of the transcript. I located the dispatch prompt and searched the rest for keywords. I did **not** read all ~210k characters of it |
| `git ls-remote origin` | `refs/heads/claude/mcmahon-elastic-law-bcc9q2` → `210177a0` | observed |
| Commit `210177a0` (2026-11-04 08:18:04Z) | Adds one file, `library/laws/mcmahon-elastic.yaml`, +195 lines. Its trailer is `Claude-Session: …session_01EeoYQgcbcm2cFsHrzqhCRS` | full-text (I read the whole file) |

The dispatch prompt, the session, the branch and the commit all agree. The worker was sent and it
finished its task, in about 4 minutes.

**The evidence level is wrong, and wrong in the low direction.** It is recorded as `unknown`. It should be
`observed (commit 210177a0 on origin/claude/mcmahon-elastic-law-bcc9q2, from the named session)`.

## (b) Does the deliverable hold up?

### Gate (observed)

I checked out `210177a0` in a scratch worktree and ran `python3 library/tools/check_laws.py`. Output:
`ok mcmahon-elastic.yaml … 3 entries, 0 problems`.

### Arithmetic, redone independently (calculated, not observed)

I derived the result myself rather than reading the author's working. For a uniform cantilever under
load q, δ = q l⁴ / (8 E I), with q = ρ g A. For a solid circle, I/A = (πd⁴/64)/(πd²/4) = d²/16. So
δ/l = 2 ρ g l³ / (E d²), which gives **C_s = 2**.

| Quantity | Entry says | My calculation |
|---|---|---|
| C_s, solid circle | 2 | 2.000 |
| Branch δ/l, l = 5 m, d = 0.2 m, ρ = 600 kg/m³, E = 10 GPa | 3.7e-3 | 3.679e-3 |
| Same branch at 2× length, geometric scaling (d = 0.4 m) | 7.4e-3 | 7.358e-3 |
| Same branch at 2× length, elastic scaling (d = 0.2·2^1.5) | d = 0.566 m, 3.7e-3 | d = 0.5657 m, 3.679e-3 |
| Diameter factor / area factor for 2× length | 2.83× / 8× | 2.828× / 8× |
| Fin-ray rod δ/l, l = 10 mm, d = 0.1 mm, ρ = 2000 kg/m³, E = 10 GPa | 3.9e-4 | 3.924e-4 |
| Dynamic pressure, ½·C_L·ρ_air·v² with C_L = 0.5, ρ_air = 1.2 kg/m³, v = 5 m/s | 7.5 Pa | 7.5 Pa |
| Load ratio, aerodynamic (1 mm strip) / self-weight | ≈ 49 | 48.7 (7.5e-3 / 1.541e-4 N/m) |
| Mass exponents from d ∝ l^1.5 and M ∝ l d² | l ∝ M^¼, d ∝ M^⅜ | 0.25, 0.375 |
| Measured interval for the length-vs-diameter exponent | [0.52, 0.97] | min/max of the four values listed (0.52, 0.67, 0.83, 0.97) |

Every number reproduces. The dimensions balance: ρ g l³ / (E d²) has units
(M L⁻² T⁻²·L³)/(M L⁻¹ T⁻²·L²) = 1. The hollow-section caveat is also correct. For a tube,
I/A = (d_o² + d_i²)/16 > d_o²/16, so C_s < 2 when measured against the outer diameter.

### Is a proxy standing in for the quantity that matters?

Yes. The status word "dispatched" stands in for what actually matters, which is **a correct entry
present in the library**. I checked with `git merge-base --is-ancestor 210177a0` against
`origin/main` and against `origin/work/frontier-foundation`. It is **not an ancestor of either**
(observed, 2026-11-04). The entry exists only on its feature branch. Its sibling,
`elastic-similarity` (`9f15ab2c`), is in the same unmerged state, as Challenge 34 recorded. Anyone
who reads "dispatched" as "in the library" is wrong today.

### Hidden assumption: test it with the assumption relaxed

The entry's design content is that "geometric scaling makes a spar relatively floppier". That rests
on self-weight being the governing load. The author does not hide this assumption. They label the
entry `usability: descriptive` instead of `constraining`, and their own fin-ray calculation drops it
(aerodynamic load ≈ 49× self-weight). The proportion rule fails as a description of mammal limbs
(0.97 across orders), cetaceans and bird humeri, and the entry lists all of these under
`where_it_breaks`. The assumption is stated and already relaxed by the author. I found nothing new
here.

### Evidence-level honesty inside the deliverable

The author's labelling:

- Every derived number is labelled CALCULATED or DERIVED.
- The green-wood and fin-ray values for E and ρ are labelled ASSUMED.
- Every literature exponent carries a read-level, and none is above search-summary or listing.
- The author says they opened no primary paper.
- The cetacean and bird-wing citations say "authors not verified" rather than inventing names.
- The Bovidae match is set against Price et al. 2009, and the two are not reconciled. The
  disagreement is kept, not averaged away.

I found **no calculated value presented as an observation**.

### Weaknesses (none refutes "dispatched")

1. **Wrong evidence level on the claim:** `unknown` should be `observed`. This is an understatement,
   not an overstatement.
2. **Not landed:** the commit is on a feature branch only (see the proxy section above).
3. **The literature layer is thin. This is my inference, not a fault the author missed.** All four
   contested-by mammal exponents, the bird humerus exponent (M^0.44) and the Biewener postural
   exponents rest on search summaries or second-hand reports. If any of them is wrong, the
   `where_it_breaks` narrative weakens. The beam law and its arithmetic would not. I did not
   re-verify these values. Scope of that gap: I made no literature searches in this review. The
   author already discloses it.
4. **A small internal tension.** `domain_of_validity.taxa` lists Bovidae limb bones as in-domain.
   But `where_it_breaks` (1) says self-weight is the wrong load for limbs. The author covers this
   with "mechanism there is uncertain", and Price et al. 2009 says a 2/3 match cannot pick out the
   mechanism. A reader could still take the Bovidae listing as support for the mechanism. This is
   a wording issue, not an error.

### Counter-examples or regimes the author missed?

The author already covers these regimes: mammals across orders, carnivoran families, cetaceans, bird
wings, millimetre spars in air and water, and hollow or tapered sections. My scope was to compare the
entry against the counter-examples in this repo's `ledger/README.md` (McMahon 1973, Mangalam et al.
2024, Price et al. 2009). Searching beyond the repo was out of scope. I found no regime they missed.
Mangalam et al. 2024 is about tree height-vs-diameter on Tallo and falls under the sibling Greenhill
entry. It is not a counter-example to the bending entry.

## Inputs this verdict rests on

- The session record and dispatch prompt of `session_01EeoYQgcbcm2cFsHrzqhCRS`. I read the prompt
  only, not the whole transcript.
- Commit `210177a0` on `origin/claude/mcmahon-elastic-law-bcc9q2` (`library/laws/mcmahon-elastic.yaml`).
- `library/tools/check_laws.py` output at `210177a0`.
- My own Euler–Bernoulli derivation of C_s = 2 and the recomputed worked examples (calculated).
- The ancestry check against `origin/main` and `origin/work/frontier-foundation`, as of 2026-11-04.

```swarm-challenge
{"claim_id": 54, "outcome": "survived", "reason": "The dispatch is observed: session 01EeoYQgcbcm2cFsHrzqhCRS received the prompt at 08:14Z and pushed commit 210177a0 with library/laws/mcmahon-elastic.yaml. The entry passes check_laws.py and every number reproduces independently. The only defects are that the recorded evidence level (unknown) should be observed and that the entry is not yet merged.", "corrected_value": null,
  "depends_on": ["session_01EeoYQgcbcm2cFsHrzqhCRS record and dispatch prompt (2026-11-04T08:14:09Z)", "commit 210177a0 on origin/claude/mcmahon-elastic-law-bcc9q2 (library/laws/mcmahon-elastic.yaml)", "library/tools/check_laws.py output at 210177a0: 3 entries, 0 problems", "independent Euler-Bernoulli derivation C_s = 2 and recomputed worked examples (calculated)", "merge-base check: 210177a0 not in origin/main or origin/work/frontier-foundation as of 2026-11-04"]}
```
