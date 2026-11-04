# Challenge 35: "LAWENTRY second-moment dispatched"

- **Claim under attack:** "LAWENTRY second-moment dispatched"
- **Recorded evidence level:** unknown. **Value:** n/a.
- **Source session:** `session_016kCs8K3uFEsD7z4PsNYtMf`
- **Challenger:** adversarial cloud review, 2026-11-04
- **Verdict:** SURVIVED. Scope caveats are below.

## What the claim actually asserts

This claim records an operation, not a scientific quantity. It says that a law-library task for the
second-moment entry was dispatched. Read literally, the only test is whether that dispatch happened.
I applied two harder tests, because "dispatched" stands in for what actually matters (see §2):

1. Did the dispatched session deliver an entry?
2. Does that entry hold up when its numbers are redone?

## 1. Was it dispatched, and did it deliver? (observed, from git)

- Commit `c3979a35` ("Law library: second moment of area and span scaling of spar stiffness") is on
  `origin/claude/second-moment-law-atubah`. Its `Claude-Session` trailer is
  `session_016kCs8K3uFEsD7z4PsNYtMf`, which is the claim's source. This is observed: I read it from git.
- It adds `library/laws/second-moment.yaml` (145 lines), `library/pages/second-moment.md`, and index
  and MyST wiring.
- I ran the repository's own gate on an extracted copy of that branch:
  `python3 library/tools/check_laws.py --dir library/laws` gave **3 entries, 0 problems**, including
  `second-moment.yaml`. `--selftest` passed, including the negative control that must be rejected.
  This is observed (I ran the tool), but it checks dimensions and mandatory fields only, not correctness.

**Scope of negative findings:**
- `git branch -r --contains c3979a35` lists only `origin/claude/second-moment-law-atubah`.
- `library/laws/second-moment.yaml` does not exist on `origin/main`.
- `gh api search/issues` with `repo:kganjam/delphi-frontier is:pr head:claude/second-moment-law-atubah`
  returned no PR.

So the work is dispatched and delivered to a branch. It is **not merged**, and no PR was found.

## 2. Proxy check

"Dispatched" is a proxy for "a correct, gated entry is in the library". Dispatch is necessary but
not sufficient. I tested the stronger quantity directly (§1 for delivery, §3 for correctness), and it
also holds, apart from the merge status. The claim as worded does not overstate: it says
"dispatched", not "merged" or "verified". So I do not count the proxy as a defect of this claim. It
would become one if a downstream record read this claim as "the law library contains second-moment".

## 3. Independent re-derivation of the entry's numbers

All of these are calculated by me, not observed. My script was a hand-written RK4 integrator with
bisection shooting, because scipy is not installed here. It is kept in the scratchpad and not committed.

| Entry states | My independent result | Match |
|---|---|---|
| Timoshenko shear/bending ratio = 0.3 (E/G)(h/L)², rectangular section, κ = 5/6 | δ_s/δ_b = E h²/(4κ G L²) = 0.300 (E/G)(h/L)² | yes |
| Isotropic (E/G = 2.6): 0.8 % at L/h=10, 3.1 % at 5, 8.7 % at 3 | 0.78 %, 3.12 %, 8.67 % | yes |
| E/G = 20: 6 % at L/h=10, 24 % at 5 | 6.0 %, 24.0 % | yes |
| Elastica: linear formula over-predicts δ by 1 % / 5 % / 10 % at FL²/EI = 0.30 / 0.68 / 0.98 | 1.02 % / 5.06 % / 10.09 %; true δ/L = 0.099 / 0.216 / 0.297 | yes |
| Elastica check value δ/L = 0.3017 at FL²/EI = 1 | 0.3017 | yes |
| Bonded vs sliding two-layer section: factor 4 | (2h)³ / (2·h³) = 8/2 = 4 | yes |
| UDL vs tip-load case: "factor-of-2.7" | (1/3)/(1/8) = 2.67 | yes |
| Span doubled, fixed section: k₂/k₁ = 0.125 | (1/2)³ = 0.125 | yes |
| Isometric doubling: k₂/k₁ = 2, self-weight δ/L doubles | 2⁴/2³ = 2; δ/L ∝ ρgA L³/EI ∝ L | yes |
| Aerodynamic load at fixed q: δ/L size-independent | w ∝ qc ∝ L, so δ/L ∝ L·L³/L⁴ = const | yes |
| Zebrafish k = 0.036 to 0.096 N/m at assumed L = 5 mm | 3·1.5e-9/1.25e-7 = 0.036; 3·4e-9/1.25e-7 = 0.096 N/m | yes |

I found no arithmetic error.

## 4. Hidden assumptions, relaxed

- **Zebrafish k depends on an assumed L = 5 mm.** The entry says this itself and labels the k range
  "derived". Because k ∝ L⁻³, L = 4 mm gives k = 0.070 to 0.19 N/m, and L = 6 mm gives 0.021 to
  0.056 N/m (calculated). The entry's range carries no more confidence than it claims. This is not a defect.
- **"Under 1 % while δ/L < 0.1".** At true δ/L = 0.099 my error is 1.02 %, so the boundary sits right
  at 1 %. This rounds honestly.
- **Shear coefficient κ = 5/6** is the standard rectangular value. Using a different section (circular,
  κ ≈ 0.9) would change the 0.3 prefactor. The entry correctly states the result is for a rectangle.

## 5. Evidence levels and sources, checked against what I could read

- **Puri et al. 2018, J Exp Biol 221:jeb171777.** I read the abstract via Europe PMC (read-level:
  abstract). It confirms the range of 1.5×10⁻⁹ to 4×10⁻⁹ N m², the non-monotonic proximal-distal
  pattern, in-vivo micro-Newton loading, and adult zebrafish caudal fin. Two things the entry did not record:
  - The abstract calls these values "bending moments" while giving them in N m². Those are
    flexural-rigidity (EI) units, so I infer the entry's reading of them as EI is correct and the
    source's wording is loose. The entry should keep using N m².
  - The abstract reports that surgically disrupting the interray tissue caused **no significant change**
    in overall bending stiffness, so stiffness "predominantly relies on ... the rays". The entry's caveat
    that "whole-fin EI already lumps rays and interray tissue" is still literally true. But this source
    says the interray share is small. My inference: caveat (4) is softer for this fin than the entry
    suggests, at least for the interray component. It does not address the hemitrich-sliding factor.
  - The entry's read-level of "search-summary" for this source can be upgraded to "abstract". The EI
    = FL³/3y method statement is not in the abstract, so I could not verify it. It stays search-summary.
- **Combes & Daniel 2003, J Exp Biol 206(17):2979–2987, DOI 10.1242/jeb.00523.** I read the abstract
  via Europe PMC (read-level: abstract). It confirms:
  - 16 species from six orders
  - spanwise EI ∝ span³ and chordwise EI ∝ chord²
  - wing size accounting for over 95 % of variance

  The entry's citation, its exponents, and the "> 95 %" figure all match. The confidence interval on
  the exponent is not in the abstract and is still `unknown`.
- **Own scratch computations labelled read_level "full-text".** The label is odd for an uncommitted
  script. The numbers reproduce (§3), so I treat this as a labelling quibble, not a defect.
- **The claim's own evidence level, "unknown".** For a dispatch event, the honest level would be
  "observed" (the commit is in git). "unknown" understates the evidence rather than overclaiming it,
  so it does not invalidate the claim.

## 6. Counter-examples and regimes

- The entry already preserves the interspecific (span³, Combes & Daniel) vs intraspecific (chord⁴,
  Ribak et al. 2025, summary-level) disagreement without averaging it. I did not re-read Ribak
  (read-level for me: could-not-access, not attempted). I am not adding or removing anything there.
- I found no published counter-example to the cantilever result k = 3EI/L³ within its stated domain.
  The listed failure regimes (shear, large deflection, Brazier ovalisation, composite or sliding
  sections, non-isometric biological scaling) cover the cases I would have raised.

## Verdict

**SURVIVED.** The dispatch happened and delivered. The delivered entry passes the repository gate, and
every number I redid independently reproduces. The residual issues are scope notes, not refutations:

- The entry is only on a feature branch (no PR found, not on `main`).
- The Puri abstract weakens the interray part of caveat (4).
- The Puri read-level can be upgraded to "abstract".

```swarm-challenge
{"claim_id": 35, "outcome": "survived", "reason": "Session 016kCs8K3uFEsD7z4PsNYtMf delivered commit c3979a35 with a second-moment entry that passes check_laws.py and whose shear, elastica, layered-section and zebrafish-k arithmetic all reproduce independently; it is unmerged (branch only, no PR found), which the word 'dispatched' does not contradict.", "corrected_value": null}
```
