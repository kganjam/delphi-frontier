# Challenge 48: "LAWENTRY von-bertalanffy dispatched"

**Verdict: SURVIVED.** This is a claim about the status of the work, not a physical result. The git
record confirms it. The work was dispatched, written, committed and pushed, and it passes the
library's dimension gate. It is **not merged** to `main`. Separately, the entry has one wording
defect in its content (the "no inflection point" sentence, see point 5). That defect sits outside the
status claim, so it does not refute the claim.

## What the claim is

The author (session `session_01EeoYQgFGUL4fRtHwVYzBT6`) claims that a task to write the von
Bertalanffy growth entry for the law library was dispatched. The claim states no value, and its
evidence level is recorded as `unknown`. The only thing that can falsify a status claim is the
record, so I tested whether the dispatched work exists.

## What I checked (2026-11-04)

| Check | Method | Result | Kind |
|---|---|---|---|
| Dispatched work exists | `git branch -r`; searched commit trailers for the source session id | Branch `origin/claude/von-bertalanffy-law-mu4ij5`, commit `d898ddc3` "Add von Bertalanffy growth entry…", 2026-11-04 08:10 UTC. Its `Claude-Session` trailer names the **same** source session. | observation (git record) |
| Files added | `git show --stat d898ddc3` | `library/laws/von-bertalanffy.yaml` (+174), `library/pages/von-bertalanffy.md` (+112), `library/pages/index.md` (+1) | observation |
| Passes the repo's gate | ran `library/tools/check_laws.py` on a worktree of that branch | `ok von-bertalanffy.yaml … 3 entries, 0 problems` | observation (tool output) |
| Merged? | `git merge-base --is-ancestor d898ddc3 origin/main` | **NOT merged**. Only that one branch contains the commit. | observation |
| Source session transcript | not attempted | not read | could-not-access (not tried) |

## Adversarial points

1. **Arithmetic, redone independently.**
   - Length form from the mass form: dm/dt = p·m^(2/3) − q·m with m = c·L³ gives
     3cL²·dL/dt = p·c^(2/3)·L² − q·c·L³. Dividing through gives dL/dt = q/3·(p/(q·c^(1/3)) − L).
     So K = q/3 and L_inf = p/(q·c^(1/3)). The entry's linear ODE follows exactly from the 2/3
     assumption, as it says. (My derivation, calculated.)
   - Worked example: ln(20) = 2.9957, and 2.9957 / 0.5 yr⁻¹ = **5.99 yr**. The entry gives 6.0 yr,
     which is correct to the stated precision. Both the entry and I calculate this from an assumed
     K, and the entry labels it `evidence: derived`, which is accurate.
2. **Proxy.** "Dispatched" stands in for the quantity that matters: whether a usable entry exists in
   the library. Measured directly, the entry exists and passes the gate, but it is not on `main`.
   Anything that reads from `main` does not see it yet. The claim does not say "merged", so this
   does not refute it. It is the gap a reader is most likely to fill in wrongly.
3. **Hidden assumption.** The claim assumes the dispatched task produced output. I relaxed that
   assumption (the task might have been dispatched and then failed or produced nothing) and tested it
   against git. The output exists, so the assumption holds.
4. **Evidence level.** `unknown` is under-specified, but nothing is overstated. The correct level is
   "operational record, verified from git". I also spot-checked the entry's most load-bearing
   literature numbers against Renner-Martin et al. (2018), PMC5756614, read-level **full-text
   (automated summarising fetch; the final ~14.6k of ~114.6k characters were not read)**. All of them
   match:
   - the search grid was a = 0, 0.01, …, 0.99;
   - 24 of the 60 data sets had their optimum at 0.99;
   - 11 problem-free data sets had a_opt between 0.14 and 0.94;
   - zebrafish #36 (Gomez-Requeni 2010, time-weight, male, 7 points) had a = 0.99 with interval 0.66–0.99;
   - zebrafish #37 (Kaushik et al. 2011, larvae, time-length, 7 points) had a = 0.99 with interval 0.57–0.99.

   The entry labels these as fitted (calculated from observations), not as observations, which is
   honest. I did not check the other cited sources.
5. **Counter-example in the content, outside the scope of this claim.**
   - **What the entry says.** `where_it_breaks` (2) says "VB has no inflection point. The curve is
     concave from t_0 onward, so it cannot represent an initial accelerating … phase."
   - **Where that holds.** It is true of the **length** form.
   - **Where it fails, by my calculation.** It is false for the **mass** form of the same model.
     Under isometry, m(t) = m_inf·(1 − e^(−K(t−t₀)))³, which is sigmoid with an inflection at
     m/m_inf = (2/3)³ = 8/27 ≈ 0.296. I confirmed 0.2963 numerically.
   - **The generalized model.** For m' = p·m^a − q·m, the inflection is at m/m_inf = a^(1/(1−a)).
     That is ≈ 0.366 at a = 0.99, the zebrafish optimum.
   - **Why it matters here.** The entry's own zebrafish examples are fitted in mass (series #36 is
     time-weight, and #37 takes mass as length³). A reader could therefore conclude that VB in
     weight cannot show early acceleration, and that conclusion is wrong.
   - **Recommended wording (my inference).** "VB in *length* has no inflection point; VB in *mass*
     has one at a fixed fraction (8/27 for a = 2/3) of asymptotic mass, so its early phase is
     constrained in shape rather than absent."
   - **Effect on the larval point.** The Zweifel & Lasker point may still stand, because a
     one-parameter-fixed inflection is less flexible than Gompertz. I did not read that paper,
     read-level could-not-access (not tried).

## Sources

- Git history of `kganjam/delphi-frontier`, as fetched 2026-11-04. Read level: full-text.
- `library/laws/von-bertalanffy.yaml` and `library/pages/von-bertalanffy.md` on
  `origin/claude/von-bertalanffy-law-mu4ij5`. Read level: full-text.
- Renner-Martin K et al. (2018) PeerJ 6:e4205, PMC5756614. Read level: full-text (summarising
  fetch, last ~13% unread).
- Source session transcript. Read level: could-not-access (not attempted).

```swarm-challenge
{"claim_id": 48, "outcome": "survived", "reason": "Commit d898ddc3 from the same source session adds library/laws/von-bertalanffy.yaml, which passes check_laws.py and whose Renner-Martin 2018 numbers check out against the paper; the work was dispatched and completed, though it is unmerged and its 'VB has no inflection point' line holds only for the length form.", "corrected_value": null}
```
