# Challenge 59: "LAWENTRY hill-muscle dispatched"

- **Claim under attack:** "LAWENTRY hill-muscle dispatched"
- **Recorded evidence level:** unknown. **Value:** n/a.
- **Source session:** `session_01HsfzfrtVetZxKP49B4U4ys`
- **Challenger:** adversarial cloud review, 2026-11-04, about 08:20 to 08:30 UTC
- **Verdict: SURVIVED, with caveats.** The dispatch delivered a law entry, its rendered page and an
  index row. The entry passes the library's dimension gate, and the page build is current. Every
  number I recomputed reproduces. The two primary abstracts I re-fetched (Edman 1988; Rome &
  Sosnicki 1990) match the entry's quoted values. The caveats:
  1. The entry is **not merged**.
  2. The dimension gate checks only the first term on each side. The author says so. I confirmed
     that a wrong second term still passes.
  3. One symbol is ambiguous. The carp curvature is normalised to the *extrapolated* intercept P0*,
     but the entry defines F0 as *measured* isometric force. At 20 °C those two differ by about 1.5×.

  The claim says "dispatched". It does not say "merged" or "verified", so none of these caveats
  refutes it.

## What the claim asserts

The claim records an operation: a task to write a `hill-muscle` law-library entry was sent out. It
contains no number. "Dispatched" is a **proxy**. What matters is whether the library holds a
correct, gated Hill force-velocity entry. I tested the operation and that quantity separately.

## 1. Was it dispatched, and did it deliver? (observed, from git and tool output)

| Check | Method | Result | Kind |
|---|---|---|---|
| Source session transcript | not attempted. Challenges 45 and 53 report that this route returns not-found. | **could-not-access** (not tried) | — |
| Delivering commit | `git log --all` after a fetch of 300 remote branches | Commit **`cc350be3`** (2026-11-04 08:20:06 UTC), "Add Hill force-velocity law entry…", is on `origin/claude/hill-muscle-law-831hag`. Its `Claude-Session` trailer is **the claim's source session**. | observation (git record) |
| Files added | `git show --stat` | `library/laws/hill-muscle.yaml` (+204), `library/pages/hill-muscle.md` (+129), `library/pages/index.md` (+1). Unlike challenge 53, the page **was** built. | observation |
| Dimension gate | `library/tools/check_laws.py --dir library/laws` in a worktree at `cc350be3` | `3 entries, 0 problems`. `--selftest` passes. | observation (tool output) |
| Page build | `library/tools/build_pages.py --check` | `{"stale": []}` | observation (tool output) |
| Negative control, first term | equation changed to `F * v * v + a * v + b * F = b * F0` | **Rejected** (1 problem) | observation (tool output) |
| Negative control, second term | equation changed to `F * v + a * v * v + b * F = b * F0` | **Passes** (0 problems). The gate does not see a wrong non-leading term. The entry's own comment discloses this and says the a·v and b·F terms were checked by hand. I checked them as well: a is a force and b a velocity, so both terms are force × velocity. | observation (tool output) and my check |
| Merged? | `git merge-base --is-ancestor cc350be3 origin/main`; `git branch -r --contains` | **NOT merged**. Only the feature branch contains the commit. | observation |
| This review's own branch | `git ls-remote origin` | `claude/challenge-59-lawentry-hill-muscle-559i0r` was not on GitHub before this push. The local ref pointed at `3272d3e`, which is unrelated base history, so the branch is **not** evidence of the dispatch. Challenges 47 and 53 hit the same trap. | observation |

The only link between the claim and the commit is the commit trailer. I did not open the source
session.

## 2. Arithmetic, redone independently (all CALCULATED by me, not observed)

I solved the power maximum two ways: by a brute-force grid over f in steps of 10⁻⁵, and from the
symmetry of the normalised hyperbola. The normalised form is (f + G)(u + G) = G(1 + G), which is
symmetric in f and u, so F·v peaks at f = u. That gives f = √(G² + G) − G. The two methods agree.

| Entry states | My result | Match |
|---|---|---|
| G = 0.25: f_opt 0.309, P_max 0.0955·F0·v_max | 0.30902 (grid), 0.0955 | yes |
| G = 0.066: 0.199, 0.0397 | 0.19925, 0.0397 | yes |
| G = 0.49: 0.364, 0.1328 | 0.36446, 0.1328 | yes |
| "dimensionless peak power changes 3.3-fold" | 0.1328 / 0.0397 = 3.35 | yes |
| f_opt = v_opt/v_max for every G | u at the optimum equals f (0.309, 0.1992, 0.3645, 0.3216). This follows from the symmetry above. | yes |
| Carp at 20 °C: f_opt 0.322, v_opt 1.84 L0/s, P_max 0.1035 | 0.3216; 0.3216 × 5.71 = 1.836; 0.1035 | yes |
| v_max in carp "rose 61 %" from 10 to 20 °C | 5.71 / 3.55 = 1.608 | yes. The abstract's mean Q10 of 1.63 ± 0.07 is a mean of per-preparation ratios, so a small difference is expected. |
| Power Q10 of 1.58 | 94.3 / 59.7 = 1.580 | yes |
| Edman: break at 78.4 % F0, which equals 10.9 % v_max | If one hyperbola runs through (0.784, 0.109) with the fitted intercept equal to measured P0, the implied G is 0.80. That curvature is implausibly flat for frog. If the intercept is 1.17 P0, the entry's quoted 17 % overestimate, the implied G is 0.33. | consistent only if F0_fit is about 1.17 P0, as the entry's break (1) states. My inference: these numbers cohere. |

**Cross-check the author did not make (my calculation).** The Hill fit's predicted 10→20 °C ratio of
peak power can be compared with the measured power ratio of 1.58. The prediction depends on which
F0 the curvature and power are scaled to:

- Scaled to measured P0, using the entry's isometric-tension Q10 of 1.13 (I did not re-verify that
  figure): (0.1035 × 5.71 × 1.13) / (0.1328 × 3.55) = **1.42**.
- Scaled to the extrapolated P0*, which is 1.19 at 10 °C and 1.51 at 20 °C: 1.42 × 1.51 / 1.19 =
  **1.80**.

The measured 1.58 lies between the two. So the choice of F0 moves the Hill prediction by about 25 %,
which is a scale-matters result. That leads to the hidden assumption in §3.

## 3. Hidden assumption, relaxed: "F0 in the hyperbola is measured isometric force"

The entry defines `F0` as the "maximum isometric force at the same length and activation", which
is a measured quantity. The Rome & Sosnicki abstract, which I fetched for this review, says the
curvature is **a/P0\***, "where P0\* is the extrapolated load at zero velocity". It gives P0\* as
1.19 ± 0.04 at 10 °C and 1.51 ± 0.20 at 20 °C.

- The entry's carp G values (0.49 and 0.29) are therefore normalised to the **fitted intercept**,
  not to measured F0.
- The carp worked example writes P_max = 0.1035·F0·v_max. That is correct only if F0 is read as
  P0\*. Read with the entry's own symbol definition (measured F0), it understates the Hill-fit peak
  power by a factor of 1.51 at 20 °C.

I did not independently confirm that 1.19 and 1.51 are multiples of measured P0. My fetch's summary
asserted it, but the quoted abstract text does not state it. The author also flagged this as their
own reading. I checked only the carp source, so this point is confirmed for carp alone. Whether the
Bottinelli rat G values are a/F0 or a/F0\* is **unknown** to me; I did not re-fetch that source.

**Effect (my inference).** The entry already warns, in break (1), that a fitted F0 must not be
used as holding force. The defect is that the symbol table and the carp example do not carry that
warning through. A reader who multiplies 0.1035 by a measured isometric stress gets a Hill peak
power about 1.5× too low at 20 °C. This is a notation caveat inside the entry. It is not a fault
in the dispatch claim.

## 4. Evidence level

`unknown` is under-specified but overstates nothing. The accurate level is "operational record,
verified from the git trailer and tool output".

Inside the entry, the labels are honest:

- Both worked examples are tagged `evidence: derived` and say they are not observed.
- G = 0.25 is marked illustrative and is explicitly not entered as a measurement.
- Intervals are labelled as the author's own mean ± SEM construction.
- The zebrafish curvature is `unknown`, and the scope of that negative search is stated: one web
  search.
- Second-hand figures are flagged with "as reported by" (Devrome & MacIntosh, Katz, Huxley, Edman
  1976, Ranatunga).

The one soft spot is the Askew & Marsh observation, at search-summary level. It is labelled
`evidence: literature`, and its muscle ("soleus") is attributed to citing papers. The author
discloses this. I did not upgrade or verify it.

## 5. Regimes or counter-examples the author missed

- **Status claim:** none. The dispatch produced the entry and its page.
- **Entry content:** the entry lists seven boundaries: high force, very low force, lengthening,
  history, cyclic work loops, multi-joint human tasks, and non-transfer across temperature and fibre
  type. It also keeps the temperature-direction disagreement between carp/icefish and rat sources,
  instead of averaging it away. Beyond the F0/P0\* notation point in §3, I found no missing regime I
  could support with a source.
- **Unverified idea, not raised as a fault:** partial activation (submaximal recruitment) is not
  listed as a boundary. The regime field does restrict the entry to "full, constant activation", so
  the scope already covers it.
- **Not verified by me:** I re-fetched only Edman (1988) and Rome & Sosnicki (1990). For every other
  source, including Bottinelli et al. 1991, Seow 2013, Alcazar et al. 2019, Hill 1938/1964, Askew &
  Marsh 1998 and Johnston & Altringham 1985, my read level is could-not-access, because I did not
  try. The author's recorded read levels stand unchecked.

## Sources

- Git history of `kganjam/delphi-frontier`, 300 remote branches as fetched about 08:20 UTC on
  2026-11-04, including commit `cc350be3` on `origin/claude/hill-muscle-law-831hag`. Read level:
  full-text.
- `library/laws/hill-muscle.yaml`, `library/tools/check_laws.py` and `library/tools/build_pages.py`
  at `cc350be3`. Read level: full-text.
- Edman KA (1988) J Physiol 404:301-321, PMC1190827. Read level: abstract, through an automated
  summarising fetch. It confirms 78.4 ± 0.4 % P0 (n = 12), 10.9 ± 0.4 % Vmax, 1-3 °C, 2.10 µm, a
  negative branch to 1.6-1.8 P0, and 1.8 ± 0.3 % Vmax across 0.90-1.20 P0.
- Rome LC, Sosnicki AA (1990) J Physiol 427:151-169, PMC1189924. Read level: abstract, through an
  automated summarising fetch. It confirms a/P0\* 0.49 ± 0.06 and 0.29 ± 0.06, P0\* 1.19 ± 0.04 and
  1.51 ± 0.20, Vmax 3.55 ± 0.26 and 5.71 ± 0.29 ML/s, Q10 of Vmax 1.63 ± 0.07, and power 59.7 ± 2.3
  and 94.3 ± 3.2 W/kg. The isometric-tension Q10 of 1.13 was not in the excerpt returned.
- `docs/research/fish/challenge-53.md` (format precedent). Read level: full-text.
- Source session transcript. Read level: could-not-access (not attempted).

```swarm-challenge
{"claim_id": 59, "outcome": "survived", "reason": "Commit cc350be3 (Claude-Session trailer matching the source session) adds library/laws/hill-muscle.yaml plus its built page and index row, passes check_laws.py (a first-term mutant is rejected, though a wrong second term passes as the entry itself discloses), and every derived number and the re-fetched Edman 1988 and Rome & Sosnicki 1990 values reproduce; it is unmerged, and the carp curvature is a/P0* (extrapolated intercept, 1.51x measured at 20 C) while the entry defines F0 as measured isometric force.", "corrected_value": null,
  "depends_on": ["git commit cc350be3 on origin/claude/hill-muscle-law-831hag and its Claude-Session trailer", "check_laws.py and build_pages.py output at cc350be3", "Edman 1988 abstract (PMC1190827, abstract read-level)", "Rome & Sosnicki 1990 abstract (PMC1189924, abstract read-level)", "origin/main as fetched 2026-11-04 ~08:20 UTC (merge status)"]}
```
