# Challenge 34 — "LAWENTRY elastic-similarity dispatched"

**Claim under review (the author's words):** "LAWENTRY elastic-similarity dispatched".
Recorded evidence level: `unknown`. Value: n/a. Source session: `session_01QbcBRYviWiJCPekSe5CNp5`.

**Verdict: SURVIVED.** The dispatch happened, and it produced a deliverable that I could check
against the repository's bytes. The evidence level is recorded too low. Below are three real weaknesses
in the deliverable. None of them refutes the claim that it was dispatched.

## What the claim actually asserts

"Dispatched" is a status claim: a worker was sent to write the `elastic-similarity` law-library entry.
It makes no scientific assertion, so there is no stated arithmetic to redo. That is why I tested
**(a)** whether the dispatch left a trace, and **(b)** whether its output holds up. Point (b) matters
because "dispatched" is only a proxy for what counts, which is a correct entry that has landed.

## (a) Did the dispatch happen? — observed

- `get_session` on `session_01QbcBRYviWiJCPekSe5CNp5` returned **not found**. From here I cannot read
  the session itself. Read-level: could-not-access.
- Remote branch `origin/claude/elastic-similarity-law-dqxwsj` is at commit `9f15ab2c`
  (2026-11-04 08:01:11 UTC). Its message is *"Law library: elastic vs geometric similarity and Greenhill
  buckling bound"*, and its trailer reads `Claude-Session: https://claude.ai/code/session_01QbcBRYviWiJCPekSe5CNp5`.
  It adds one file, `library/laws/elastic-similarity.yaml`, with 177 lines. Read-level: full-text (I read
  the whole file).
- This is **observed**: the source session committed and pushed the entry. So the dispatch both happened
  and completed.

**Evidence level is dishonest by understatement, not overstatement.** `unknown` should be
`observed (commit 9f15ab2c on origin/claude/elastic-similarity-law-dqxwsj)`.

## (b) Does the deliverable hold up?

### Arithmetic, redone independently (calculated, not observed)

I wrote my own power series and bisection for J_ν. I did not use scipy, and I did not reuse the
author's working.

| Quantity | Entry says | My calculation |
|---|---|---|
| first zero of J_{-1/3} | 1.86635 | 1.8663509 |
| Greenhill eigenvalue (3j/2)² | 7.837 | 7.83735 |
| C_G = (7.837/16)^{1/3}, solid circle I/A = d²/16 | 0.788 | 0.78828 |
| l_cr, d = 1 m, E = 10 GPa, ρ = 600 kg/m³ | 94 m | 94.1 m |
| l_cr, d = 0.1 / 0.5 / 3 m | 20 / 59 / 196 m | 20.3 / 59.3 / 195.7 m |
| l_cr, d = 0.1 mm, E = 10 GPa, ρ = 2000 kg/m³ | 0.14 m | 0.136 m |

Every number in the table reproduces. The dimensions balance: E/(ρg) has dimension L, so
L^{1/3}·L^{2/3} = L. The repository's own gate agrees. I ran `library/tools/check_laws.py` at `9f15ab2c`
and it reports `3 entries, 0 problems` (observed). The entry labels every derived number CALCULATED or
DERIVED, and it marks the green-wood E and ρ as ASSUMED. I found no calculated value presented as a
measurement.

### Weaknesses found (none refutes "dispatched")

1. **Proxy gap: dispatched ≠ landed.** `git merge-base --is-ancestor 9f15ab2c origin/main` is false
   (observed, 2026-11-04). The entry exists only on its feature branch. Anyone who reads "dispatched" as
   "in the library" is wrong today.
2. **An in-repo measurement that disagrees went uncited.** The entry gives a tree buckling safety factor
   of about 4 (McMahon 1973, McMahon & Kronauer 1976). The author states this is search-summary level and
   gives no interval. This repository's own `ledger/README.md` ("The one candidate that survived the
   day") reports a **measured** per-tree Greenhill safety factor on Tallo v1.0.0. Its median is
   **1.8 to 2.9** depending on taper, and 0.068%–3.24% of trees exceed the critical height. The two
   sources disagree: about 4 (secondary report of McMahon) against 1.8–2.9 (in-repo measurement, DBH at
   1.3 m, which the ledger says overstates the ratio by about 13%). I am preserving that disagreement,
   not reconciling it. The entry should cite both. *My inference:* the gap probably comes partly from
   McMahon's smaller, older sample and partly from the taper assumption, but I have not tested that.
3. **Prior art that the repo already holds was left out.** `ledger/README.md` lists Mangalam et al. 2024
   (*Sci Rep* 14:19957), a quantile regression on Tallo against the 2/3 exponent with mixed results, and
   Price et al. 2009 (*Ecol Lett* 12:641), which shows that 2/3 cannot discriminate elastic similarity
   from metabolic scaling. Both bear directly on `contested_by`, and neither appears in it. I have only
   listing-level knowledge of these citations, taken from the ledger. I did not open the papers.

Minor: the fin-ray example says l_cr is "roughly two orders of magnitude longer than a millimetre-scale
ray". For a ray several millimetres long the ratio is closer to 30–50×, about 1.5 orders. The
qualitative conclusion, that self-weight buckling does not bind, is unchanged. The entry's own
"water" caveat is stronger anyway: for immersed tissue, (ρ − ρ_water) is close to 0.

### Hidden assumption, relaxed

The Greenhill bound assumes a prismatic, solid, clamped-free column. If taper is allowed, the prefactor
rises. The ledger measured taper as the dominant factor (1.57×). If the section is hollow, I/A rises, and
the entry already says C_G does not apply. Both relaxations **raise** l_cr. The entry flags one of them
(hollow) and omits the other (taper). This changes the bound's prefactor but not the d^{2/3} form.

### Counter-examples / regimes

The entry already records the main ones: mammalian limb bones near geometric similarity (about 0.97),
Niklas 1993 against Norberg 1988 (it keeps them unreconciled, correctly), and falling safety factors in
herbaceous stems and cacti. I found no regime it misses beyond items 2 and 3 above.

## Scope of negative searches

- Repo-wide search for `lawentry` and `elastic` (working tree, `git log --all`, and remote refs): the
  only hits were the branch above and `ledger/README.md`.
- No web search was run. The citations in this file come from the repository only.

```swarm-challenge
{"claim_id": 34, "outcome": "survived", "reason": "Commit 9f15ab2c from the named session exists on origin/claude/elastic-similarity-law-dqxwsj, passes the repo's law gate, and its arithmetic reproduces independently (C_G = 0.7883); it is not yet merged to main, and the evidence level should read observed rather than unknown.", "corrected_value": null}
```
