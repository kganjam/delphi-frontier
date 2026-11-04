# Challenge 53: "LAWENTRY reynolds-stokes dispatched"

- **Claim under attack:** "LAWENTRY reynolds-stokes dispatched"
- **Recorded evidence level:** unknown. **Value:** n/a.
- **Source session:** `session_01HsfzfsQvViw99BJpFggTVU`
- **Challenger:** adversarial cloud review, 2026-11-04, about 08:15 to 08:25 UTC
- **Verdict: SURVIVED, with caveats.** The dispatch is real. It produced a law entry, and that
  entry passes the library's dimension gate. Every number in the entry reproduced when I redid it.
  Three things limit what a reader may infer:
  1. The entry is **not merged**.
  2. Its generated page was **never built**.
  3. One worked example applies the steady Stokes law to an unsteady problem, which is the failure
     mode (7) that the entry itself names. Its order-of-magnitude conclusion still holds.

  The claim says "dispatched". It does not say "merged", "rendered" or "verified", so none of these
  refutes it.

## What the claim asserts

The claim records an operation: a task to write a "reynolds-stokes" law-library entry was sent out.
It contains no number and no physics. "Dispatched" is a **proxy**. What matters is whether the
library now holds a correct, gated entry for the Stokes (creeping-flow) regime. I tested both the
operation and that quantity.

## 1. Was it dispatched, and did it deliver? (observed, from git)

| Check | Method | Result | Kind |
|---|---|---|---|
| Source session transcript | `list_events` on the source session | **could-not-access**: "the requested resource was not found" | — |
| First sweep (about 08:15 UTC) | `git grep`/`git log -S` for `reynolds`, `stokes` and `LAWENTRY` over the working tree, all history and 276 fetched remote branches | No reynolds-stokes entry. The only Reynolds entry, `library/laws/reynolds.yaml`, was added by `343e8f15` on 2026-11-03, before the dispatch, and has no Stokes-regime content. | negative, scoped to those refs at that time |
| This review's own branch | `git ls-remote origin` | `claude/challenge-53-reynolds-stokes-upfryp` was **not** on GitHub. The local tracking ref pointed at `work/frontier-foundation` (`3272d3e`), so it is **not** evidence of the dispatch. Challenge 47 records the same trap. | observation |
| Re-fetch every 30 s | background `git fetch` loop | At 08:18:21 UTC `origin/claude/reynolds-stokes-law-ar3x7v` appeared, holding commit **`44fa61f7`** (2026-11-04 08:17:54 UTC): "Add Stokes-regime law entry: what changes below Re ~1, and where the linear drag law fails". Its `Claude-Session` trailer names **the same session as the claim's source**. The work landed while this review was running. | observation (git record) |
| Files the commit adds | `git show --stat` | Only `library/laws/reynolds-stokes.yaml` (+209). There is no `library/pages/reynolds-stokes.md` and no index row. | observation |
| Dimension gate | `library/tools/check_laws.py --dir library/laws` on a worktree at `44fa61f7` | `ok reynolds-stokes.yaml … 3 entries, 0 problems`. `--selftest` passes, including its wrong-Reynolds negative control. | observation (tool output) |
| My own negative control | Changed the equation to `F_D = 3*pi*mu*U*d^2` and re-ran the gate | **Rejected**: "'F_D' is M^1·L^1·T^-2, other side is M^1·L^2·T^-2". The gate does bite on this entry. | observation (tool output) |
| Page build | `library/tools/build_pages.py --check` | `{"stale": ['reynolds-stokes.md', 'index.md']}`. The rendered page was never generated. | observation (tool output) |
| Merged? | `git merge-base --is-ancestor 44fa61f7 origin/main`, `git branch -r --contains` | **NOT merged**. Only the feature branch contains the commit. `origin/main` has no `library/laws/` directory at all. | observation |

The link between the claim and the commit is the commit trailer only. I could not open the source
session.

## 2. Arithmetic, redone independently (all CALCULATED by me, not observed)

| Entry states | My result | Match |
|---|---|---|
| Oseen correction (3/16)·Re_d at Re_d = 0.1, 0.5, 1 | 1.875 %, 9.375 %, 18.75 % | yes |
| Schiller–Naumann 0.15·Re_d^0.687 at Re_d = 0.1, 0.5, 1, 100 | 3.08 %, 9.32 %, 15.0 %, 354.9 % | yes |
| Factor of ~1.6 between the two corrections at Re_d = 0.1 | 1.64 | yes |
| Factor 4.55 at Re_d = 100 | 4.549 | yes |
| τ = 2ρa²/(9μ), with a = 1 µm | 2.22×10⁻⁷ s (from m/(6πμa) with m = (4/3)πa³ρ) | yes |
| Coasting distance U·τ, with U = 30 µm/s | 6.67×10⁻¹² m | yes, as quasi-steady arithmetic (see §3) |
| Settling v = Δρ g d²/(18μ), with d = 10 µm and Δρ = 50 kg/m³ | 2.725×10⁻⁶ m/s, and Re_d = 2.7×10⁻⁵ | yes |
| Cilium Re = 10⁻³·10⁻⁵/10⁻⁶ | 0.01 | yes |
| Cunningham Cc at d = 1 µm and 0.1 µm (λ = 0.066 µm) | 1.166 and 2.89, using Cc = 1 + Kn(1.257 + 0.4 e^(−1.1/Kn)) with Kn = 2λ/d | yes. The constants are Davies-type values that I quote **from memory**. |
| Tritton's 2 % at container/sphere ratio 100, and Lindgren's 4 % at 50 | 2.1 % and 4.4 %, from the first-order centreline wall correction 1/(1 − 2.104·d/D) | consistent. The coefficient 2.104 is from memory (Faxén/Haberman). I did not verify it against a source in this review. |
| Split of 3π into 2π viscous shear plus π pressure | 4πμUa + 2πμUa in radius form, so the ratio is 2:1 | yes |
| Dimensions of F_D = 3πμUd | M L T⁻², confirmed by the gate and by my mutant | yes |

**Minor notational point (my inference).** The entry says the coefficient 24 (diameter Re) "equals
6π/R" in Veysey & Goldenfeld's radius convention. Under the area normalisation the entry itself
defines, C_D = F/(½ρU²·πd²/4), 24/Re_d equals **12/R**. The 6π/R form holds only if C_D is
normalised as F/(ρU²a²), which the entry does not state. The ratio of the correction terms,
(3/8)R = (3/16)Re_d, is unaffected, and so is every number in the entry.

## 3. Hidden assumption, relaxed: "the steady Stokes drag governs a coasting body"

The first worked example computes a coasting distance from the steady drag, which is a
quasi-steady assumption. In break (7) the entry itself states that the steady law omits added-mass
and Basset history forces, and that it does not record when they matter. The example does not check
that. Here is the check, which is my inference from a scaling argument and not a solved problem:

- The particle relaxation time is τ_p = 2.2×10⁻⁷ s. The vorticity diffusion time is
  a²/ν = 10⁻⁶ s. So τ_p/(a²/ν) = (2/9)(ρ_p/ρ_f) ≈ 0.22. The body would stop faster than the
  surrounding flow can adjust. The quasi-steady assumption is therefore **not** self-consistent
  here, and the unsteady forces are leading order, not corrections.
- Added mass alone, for a neutrally buoyant sphere (m_eff = (ρ_p + ρ_f/2)V), raises τ by 1.5× to
  3.3×10⁻⁷ s (calculated). The history force adds a slow algebraic velocity tail. Dimensional
  reasoning puts the resulting displacement on the order of U·a²/ν = 3×10⁻¹¹ m (calculated scale,
  not a solution). That is about 4.5× the entry's 6.7×10⁻¹² m.
- The fluid around a towed sphere also carries momentum of its own, so "propulsion stops" is not
  the same initial condition as "sphere released with speed U". I did not resolve which initial
  condition applies.

**Effect.** The number 6.7×10⁻¹² m is the right *quasi-steady* arithmetic but not a defensible
physical coasting distance. The conclusion the entry draws from it ("no coasting", sub-ångström to
ångström scale) survives even with a correction of about 5×. This is a caveat on one worked
example, not a refutation, and it is outside what the claim asserts. I have no exact value, so the
corrected value is reported as null.

## 4. Evidence level

`unknown` is under-specified but overstates nothing. The accurate level is "operational record,
verified from the git trailer and tool output". Inside the entry, the labels are honest. Every
derived number is tagged CALCULATED or `evidence: derived`, with assumed inputs stated. Read levels
are given per source, for example Veysey & Goldenfeld as full-text, Purcell as search-summary
(host blocked), and Schiller & Naumann as could-not-access. Disputes are kept rather than averaged:
Faxén against Oseen/Illingworth on the 3R/8 term, the Pruppacher data, and Oseen against
Schiller–Naumann. I found no derived number presented as measured.

## 5. Regimes or counter-examples the author missed

- **Status claim:** none. The dispatch produced the entry.
- **Entry content:** the unsteady caveat in §3 is the only gap I found. The entry lists seven
  failure boundaries (finite Re, 2D bodies/Stokes paradox, far field, walls, rarefied gas,
  non-Newtonian fluids, unsteady motion) and records that no zebrafish swimming stage reaches
  Re < 1. I checked whether zebrafish **sperm** contradicts that statement. It does not, because the
  entry lists sperm among the bodies the law *does* apply to, and a gamete is not a swimming life
  stage of the fish.
- **Not verified by me:** I made no literature fetches in this review. Veysey & Goldenfeld's
  quotes, the Faxén dispute, the Tritton and Lindgren wall figures, the larval Re range of 60–1400
  (van Leeuwen et al. 2015, held only at listing level in this entry) and the McHenry & Lauder
  (2005) figure all keep the read levels the author recorded. My own read level for each is
  could-not-access, because I did not try. The bibliographic details (volumes and pages) are not
  checked here.

## Sources

- Git history of `kganjam/delphi-frontier`, remote branches as fetched 08:15–08:19 UTC on
  2026-11-04, including commit `44fa61f7` on `origin/claude/reynolds-stokes-law-ar3x7v`. Read level:
  full-text.
- `library/laws/reynolds-stokes.yaml`, `library/laws/reynolds.yaml`, `library/tools/check_laws.py`
  and `library/tools/build_pages.py` at `44fa61f7`. Read level: full-text.
- `docs/research/fish/challenge-45.md`, `challenge-47.md` and `challenge-51.md` on their branches
  (precedent and format). Read level: full-text.
- Source session transcript. Read level: could-not-access.

```swarm-challenge
{"claim_id": 53, "outcome": "survived", "reason": "Commit 44fa61f7 (08:17:54 UTC, Claude-Session trailer matching the source session) adds library/laws/reynolds-stokes.yaml, which passes check_laws.py (a d^2 mutant is rejected) and whose numbers all reproduce; it is unmerged, its page was never built, and its coasting example applies steady Stokes drag where tau_p < a^2/nu, so unsteady forces (its own break 7) are leading order, though the no-coasting conclusion survives.", "corrected_value": null}
```
