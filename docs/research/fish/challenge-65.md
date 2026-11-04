# Challenge 65: "LAWENTRY lift-coefficient-lowre dispatched"

- **Claim under attack:** "LAWENTRY lift-coefficient-lowre dispatched"
- **Recorded evidence level:** unknown. **Value:** n/a.
- **Source session:** `session_016kCs8Kcofjr3iZrsTVGKEL`
- **Challenger:** adversarial cloud review, 2026-11-04
- **Verdict: SURVIVED, with three caveats.** The claim reports that a piece of work was dispatched;
  it states no physical result. Git confirms the dispatch and shows that it produced a gated,
  rendered law entry. Every number I could recompute matches, and three primary-source quotes I
  fetched read as the entry says. The caveats: the entry is **not merged**; one dispute the entry
  left open can be settled from the primary source; and the 0.8 anchor value is described as a
  "thin plate" value when it is really a "thin airfoil" value, a small overreach on the entry's
  name and on its "floor" wording.

## 1. Was it dispatched, and did it deliver? (observed, from git and tool output)

| Check | Method | Result |
|---|---|---|
| Work exists | `git log --all --grep` | Commit `b93b6f7e`, "Law library: measured CLmax of thin plates at Re 1e3-1e4, and where it stops transferring", 2026-11-04 08:23:49 UTC. Its `Claude-Session` trailer names the **same** session as the claim's source. |
| Files | `git show --stat` | `library/laws/lift-coefficient-lowre.yaml` (+176), `library/pages/lift-coefficient-lowre.md` (+104), and one row in `library/pages/index.md`. |
| Dimension gate | `check_laws.py --dir library/laws` on a worktree at `b93b6f7e` | `3 entries, 0 problems`. The `--selftest` run passed, including its wrong-Reynolds negative control. |
| Page build | `build_pages.py --check` at the same commit | `{"stale": []}`, exit 0. The page is current. Challenge 45 found the Hagen-Poiseuille page missing; this entry does not have that defect. |
| Branches | `git branch -r --contains b93b6f7e` | Only `origin/claude/lift-coefficient-lowre-mmtlms`. |
| Merged? | `git merge-base --is-ancestor b93b6f7e origin/main` | **NOT merged.** |
| PR? | `gh api search/issues` with `repo:kganjam/delphi-frontier is:pr head:claude/lift-coefficient-lowre-mmtlms` | 0 results. |
| Source session | not queried | I did not open the session transcript. The commit trailer is my only link to the session. |

The claim says "dispatched". It does not say "merged", so the fact that the entry is unmerged
weakens nothing the claim asserts.

## 2. Arithmetic, redone independently (all calculated by me, not observed)

| Entry states | My computation | Match |
|---|---|---|
| L_max = 0.5·1.2·2²·2e-4·0.8 = 3.84e-4 N, "about 39 mg" | 3.840e-4 N. Divided by g = 9.80665 m/s², that is **39.2 mg**. | yes |
| Re of the project wing, 1333 (from reynolds.yaml) | 2·0.01/1.5e-5 = **1333.3** | yes |
| 1.19 = peak of Su et al.'s fit, near α ≈ 40° | I maximised −0.44·e^(−0.47α) + 1.19·sin(1.74α + 20°) numerically: **1.1900 at α = 40.2°**. The exponential term is about 3e-9 there. | yes |
| Dimensions of CL = 2L/(ρU²S) | (M·L·T⁻²)/(M·L⁻³·L²·T⁻²·L²) = 1 | yes |

The entry labels the 1.19 as its own evaluation of the fit, not a number Su et al. state, and it
labels the 39 mg as `derived` and CALCULATED. Both labels are honest.

## 3. Primary-source spot checks (I fetched each one)

- **Cheng & Sun 2016, PMC4863373.** Read level: full-text, through an automated summarising
  fetch. The paper says "at Re = 10⁴ the maximum lift coefficient of a thin airfoil is about 0.8"
  (ref. 9, Okamoto, Yasuda & Azuma 1996). It also says "at Re = 100 … model fruitfly wing is
  about 0.6" (ref. 10, Vogel 1967). The entry quotes both accurately.
- **Su et al., arXiv 2302.09602v2.** Read level: full-text, through an automated summarising
  fetch. The fit (Eq. 10), the peak near 40°, the plate (c = 0.076 m, span 0.456 m, δ = 8 mm,
  AR 6), the Re range of 20,000–50,000, and the line "maximum CL … approximately 45% … smaller"
  than Dickinson et al. (1999) all match the entry.
- **Usherwood 2009, PMC3380271.** Read level: full-text, through an automated summarising
  fetch. The paper reports the tests at "Re ≈ 108,000 and 54,000", with a 3.6 Hz run at
  Re ≈ 49,000. The abstract says "up to 108,000". The 1.64 and 1.44 maxima match.

## 4. Adversarial points

1. **Arithmetic.** See §2. I found no error.
2. **Proxy.** "Dispatched" stands in for what actually matters: a correct, usable CLmax entry
   in the library. I checked that directly. The entry exists, passes the gate, has its page built,
   and is not merged. Inside the entry there is a second proxy: a Re 1e4 value standing in for the
   project wing at Re 1333. The author names this proxy, calls the 39 mg an "upper-side number",
   and sets `usability: descriptive` so that it cannot pass or fail a design. I found nothing to
   add.
3. **Hidden assumption: that "about 0.8" is a flat-plate value.** The entry is named "thin
   plates", and where_it_breaks (3) calls "a flat-plate value" a **floor** for cambered sections.
   But Cheng & Sun write "thin **airfoil**". By the author's own reading of the abstract,
   Okamoto et al. (1996) varied camber, thickness and leading-edge shape. If the 0.8 came from a
   cambered section, it is not a flat-plate floor, and a true flat-plate CLmax at Re 1e4 could be
   lower. *My inference:* the constant's own note already says "flat or cambered … UNKNOWN to us",
   and the worked example treats 0.8 as an upper-side figure, which is the conservative direction.
   So this is wording that overreaches in the name and in point (3), not a wrong number. I did not
   read Okamoto et al. (1996) myself (read level: could-not-access, not attempted).
4. **Evidence level.** Recording the claim as `unknown` understates it. The accurate level is
   "operational record, verified from git and tool output". Nothing is overstated. Inside the
   entry, measured-but-secondhand values are labelled MEASURED + SECONDHAND, and calculated values
   are labelled CALCULATED. I found no derived number presented as measured.
5. **Regime, counter-example, or a dispute the author missed.** The entry's third `contested_by`
   item leaves open whether Usherwood (2009) tested at Re 10,800 or at 54,000–108,000. **The
   primary source settles it:** 49,000–108,000. *My inference:* Su et al.'s "up to 10,800" is
   probably a slip by a factor of ten. That is inference; I have no erratum. Either way the test
   lies above 1e4, and the entry already keeps it out of its domain, so no conclusion changes.
   Su et al.'s "45%" also sits uneasily with my recollection that Dickinson et al. (1999) peak
   near CL ≈ 1.8, which would make 1.19 about 34% lower. That 1.8 is from memory, unverified, and
   the fetched page gives no Dickinson maximum. I attribute the tension to Su et al., not to the
   entry, which quotes them faithfully. I found no published steady flat-plate CLmax inside
   Re 1e3–1e4 that contradicts the entry. Scope of that search: the three fetches above only; I ran
   no literature search beyond them.

## Sources

- Git history of `kganjam/delphi-frontier`, remote branches as fetched 2026-11-04. Commit
  `b93b6f7e` and the tool runs at that commit. Read level: full-text.
- Cheng X, Sun M (2016) Sci. Rep. 6:25706, PMC4863373. Read level: full-text (automated summarising fetch).
- Su Y et al., arXiv:2302.09602v2. Read level: full-text (automated summarising fetch).
- Usherwood JR (2009) Exp. Fluids 46:991-1003, PMC3380271. Read level: full-text (automated summarising fetch).
- Okamoto, Yasuda & Azuma (1996). Read level: could-not-access (not attempted).
- Dickinson et al. (1999), CLmax ≈ 1.8. Read level: could-not-access. The figure is from my memory and is unverified.
- Source session transcript. Read level: could-not-access (not attempted).

```swarm-challenge
{"claim_id": 65, "outcome": "survived", "reason": "Commit b93b6f7e from the same source session adds lift-coefficient-lowre.yaml plus its built page, check_laws.py gives 0 problems and build_pages --check gives no stale pages, and every recomputed number (3.84e-4 N / 39 mg, Re 1333, fit peak 1.19 at 40.2 deg) and three fetched source quotes match; it is unmerged, its Usherwood Re dispute is resolvable to 49k-108k, and calling the 0.8 'thin airfoil' value a flat-plate floor overreaches slightly.", "corrected_value": null,
  "depends_on": ["git commit b93b6f7e on origin/claude/lift-coefficient-lowre-mmtlms and its Claude-Session trailer", "check_laws.py and build_pages.py --check output at b93b6f7e", "Cheng & Sun 2016 (PMC4863373) wording 'thin airfoil ... about 0.8' at Re 1e4", "Su et al. arXiv:2302.09602v2 Eq. 10 fit", "Usherwood 2009 (PMC3380271) Re 49,000-108,000", "reynolds.yaml project wing: U=2 m/s, c=0.01 m, nu=1.5e-5 m^2/s"]}
```
