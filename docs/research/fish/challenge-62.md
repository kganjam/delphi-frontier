# Challenge 62: "LAWENTRY phyllotaxis dispatched"

- **Claim under attack:** "LAWENTRY phyllotaxis dispatched"
- **Recorded evidence level:** unknown. **Value:** n/a.
- **Source session:** `session_01EeoYQenugRMpZgH9iNWVH9`
- **Challenger:** adversarial cloud review, 2026-11-04, about 08:10 to 08:30 UTC
- **Verdict: SURVIVED, with caveats.** The dispatch is real. It produced a law entry and its
  generated page. The entry passes the library's dimension gate, the page build is current, and
  every number I redid reproduced. Four caveats limit what a reader may infer:
  1. The entry is **not merged**.
  2. For this entry the dimension gate is close to vacuous (see §2).
  3. The entry says the wild-type mean angle is `unknown`, but Landrein et al. 2015 report one:
     136°. The entry cites that same table.
  4. The permutation-signature angles are given loosely.

  The claim says only "dispatched". None of these caveats refutes it.

## What the claim asserts

The claim records an operation: a task to write a phyllotaxis entry for the law library was sent
out. It contains no number. "Dispatched" is a **proxy**. What matters is whether the library now
holds a correct, gated phyllotaxis entry. I tested both the operation and the entry.

## 1. Was it dispatched, and did it deliver? (observed, from git)

| Check | Method | Result | Kind |
|---|---|---|---|
| This review's own branch | `git ls-remote origin refs/heads/claude/lawentry-phyllotaxis-challenge-y0jyv0` | Empty: the branch is **not** on GitHub. The local tracking ref points at `3272d3e` (`work/frontier-foundation`), so it is **not** evidence of the dispatch. Challenges 47 and 53 record the same trap. | observation |
| Search for the work | `git ls-remote origin` filtered on "phyllo"; `git log --all --grep` for the phrase "phyllotax" and for the source session ID | One match: `origin/claude/phyllotaxis-golden-angle-law-upiubr` at commit **`79960f11`** (2026-11-04 08:19:33 UTC), "Law library: phyllotaxis and the golden angle, what is explained and what is not". Its `Claude-Session` trailer is **`session_01EeoYQenugRMpZgH9iNWVH9`**, which is the source of the claim. | observation (git record) |
| Files the commit adds | `git show --stat` | `library/laws/phyllotaxis.yaml` (+227), `library/pages/phyllotaxis.md` (+130), one row in `library/pages/index.md`. Unlike challenges 45 and 53, this entry's page **was** built. | observation |
| Dimension gate | `check_laws.py --dir library/laws` on a worktree at `79960f11` | `ok phyllotaxis.yaml … 3 entries, 0 problems`. `--selftest` passes. | observation (tool output) |
| My negative control | Changed the equation to `theta_n = 2*pi*n*c/phi^2` | **Rejected**: "'theta_n' is dimensionless, other side is L^1". | observation (tool output) |
| Page build | `build_pages.py --check` | `{"stale": []}` | observation (tool output) |
| Merged? | `git merge-base --is-ancestor 79960f11 origin/main`; `git branch -r --contains` | **NOT merged**. Only the feature branch contains the commit. | observation |
| Source session transcript | not attempted | could-not-access. The only link between the claim and the commit is the commit trailer. | — |

## 2. A proxy inside the proxy: what "passes the gate" means here (my inference)

The gate checks that the dimensions balance. The headline equation, θ_n = 2πn/φ², has no
dimensions on either side, so **any** dimensionless right-hand side passes. For example,
2πn/φ (222.5°, the complement), 2πn/φ³, or 2πn·0.3 would all pass. My mutant was rejected only
because I added a length. So for this entry, "passes check_laws.py" says almost nothing about
whether the entry is correct. The arithmetic in §3 is the real check, and it holds.

## 3. Arithmetic, redone independently (all CALCULATED by me, not observed)

| Entry states | My result | Match |
|---|---|---|
| Golden angle 360(1 − 1/φ) = 360/φ² = 137.5078° | 137.50776° by both forms | yes |
| Lucas-branch angle 360/(3 + 1/φ) = 99.502° | 99.50155°. This equals 360/(2 + φ), the usual form of the Lucas angle. | yes |
| Non-spiral error "40–50° or more" | 180 − 137.5 = 42.5° (distichous); 137.5 − 90 = 47.5° (decussate) | yes |
| Swinton fractions 0.736 / 0.823 / 0.177 | 565/768 = 0.7357; 632/768 = 0.8229; 136/768 = 0.1771. The parts sum: 25 + 41 + 1 = 67, 49 + 17 + 70 = 136, 565 + 67 + 136 = 768. | yes |
| Vogel: c = 1 mm, N = 1000 gives r_N = 31.6 mm; area per floret πc² | √1000 = 31.62. A disc of radius c√N has area πc²N, so each floret gets πc². | yes |
| Permutation signature "~274° and ~220°" | Initiation order 0, α, 2α, 3α with organs 1 and 2 swapped gives successive angles 2α = **275.0°**, then −α mod 360 = **222.5°**, then 2α = 275.0° again | approximately. The ideal values are 275.0° and 222.5°. "~220" is 2.5° low. This is cosmetic, but a checker should use 275.0° and 222.5°. |

## 4. Sources re-read in this review

- **Swinton et al. 2016** (PMC4892450, via a summarising fetch; read level: full-text through a
  summarising fetch). Confirmed: 768 parastichy numbers, 565 Fibonacci, 25 double Fibonacci,
  41 Lucas, 1 F4, 49 F−1, 17 F+1, 70 other, 657 sunflowers, Schoute 82%, Weisse 95%. **Every
  count in the entry matches.**
- **Landrein et al. 2015** (PMC4339594, via a summarising fetch; read level: full-text through a
  summarising fetch). Confirmed for Col-0: short-then-long days, 704 angles, 29 sequences, 23%
  non-canonical angles, 14% permuted organs; long days only, 1193 angles, 34 sequences, 2.1%
  permuted organs. **The entry matches these.** Two discrepancies:
  - **The entry missed a reported value.** Table 1 gives a **mean divergence angle of 136° for
    Col-0 in both conditions**. This is an observation. No SD was reported. The entry's
    `divergence_angle_arabidopsis_wt_spread` is `null`, and its note says neither paper yielded
    "a wild-type mean +/- SD". That is literally true, because no SD was given. But the entry
    does not record the mean, which was in the very table it quotes. That mean is the closest
    thing in the entry's sources to a measured test of the 137.5° law, and it sits 1.5° below it.
    I cannot tell from Table 1 whether 136° is a circular mean or how permuted pairs were handled.
  - The fetch also reported 703 angles in **26** plants in the Fig. 5 legend, and 1190 angles in
    34 plants for long days. This adds to the 703 angles in 23 plants (Fig. 2) that the entry
    already flags. Landrein's own counts disagree with each other, and I am preserving the
    disagreement, not resolving it.
- No other source was re-read. The remaining citations keep the read levels the author recorded.
  My own read level for each is could-not-access, because I did not try to read them. From
  memory, the volume and page numbers for Reinhardt 2003, Smith 2006, Besnard 2014, Douady &
  Couder 1992, Turner 2023 and Strauss 2020 look right, but I have not verified them.

## 5. Hidden assumption, and regimes the author might have missed

- **Hidden assumption:** the entry treats 137.5° as the attractor of the small-G limit. It
  already makes this conditional. It states the limit at large G, transitions, the difference
  between apical and stem angles, and permutations. Relaxing the assumption only moves the result
  into regimes the entry already lists.
- **Counter-examples:** the entry covers distichous, decussate and whorled phyllotaxis, Lucas and
  non-Fibonacci spirals (sunflower, *Asteroxylon*), and permutations. Its `search_scope` openly
  excludes the mechanical-buckling models (Green; Newell & Shipman), Adler's contact-pressure
  model, and measured angle distributions in conifers and cacti. Those are unsearched, not
  contradicting. I did not search them either, so I make no negative claim about them.
  Spiral **chirality**, meaning whether a system runs at 137.5° or 222.5°, is noted only in
  passing ("or its complement"). It is not a counter-example.
- **Evidence labels:** CALCULATED and OBSERVED are kept apart throughout. Our-arithmetic results
  are labelled as such. Taxon examples resting on general knowledge are flagged as unverified.
  Rates that disagree (Schoute, Weisse, Swinton, and the >91% survey) are kept side by side, not
  averaged. One structural quibble: the `interval` fields for permutation fraction and sunflower
  fraction hold two growth conditions or two definitions, not uncertainty bounds. The notes say
  so, but a machine reader of `interval` would misread them.
- **Evidence level of the claim:** `unknown` is under-specified but does not overstate anything.
  The accurate level is "operational record, verified from the git trailer and tool output".

## Sources

- Git history of `kganjam/delphi-frontier`, remote refs as fetched about 08:15–08:25 UTC on
  2026-11-04, including commit `79960f11` on `origin/claude/phyllotaxis-golden-angle-law-upiubr`.
  Read level: full-text.
- `library/laws/phyllotaxis.yaml`, `library/tools/check_laws.py` and `library/tools/build_pages.py`
  at `79960f11`. Read level: full-text.
- `docs/research/fish/challenge-53.md` at `cb5758d0` (precedent and format). Read level: full-text.
- Swinton, Ochu et al. 2016, *R Soc Open Sci* 3:160091, PMC4892450. Read level: full-text via a
  summarising fetch.
- Landrein et al. 2015, *J Exp Bot* 66:1317–1324, PMC4339594. Read level: full-text via a
  summarising fetch.
- Source session transcript. Read level: could-not-access.

```swarm-challenge
{"claim_id": 62, "outcome": "survived", "reason": "Commit 79960f11 (08:19:33 UTC, Claude-Session trailer matching the source session) adds library/laws/phyllotaxis.yaml plus its built page, passes check_laws.py (a length-carrying mutant is rejected) and build_pages --check, and every number and the Swinton/Landrein counts reproduce; it is unmerged, the dimension gate is near-vacuous for a dimensionless law, and the entry omits Landrein's observed Col-0 mean angle of 136 deg from the table it cites.", "corrected_value": null, "depends_on": ["git commit 79960f11 on origin/claude/phyllotaxis-golden-angle-law-upiubr and its Claude-Session trailer", "check_laws.py and build_pages.py output at 79960f11", "Swinton et al. 2016 Table 1 counts via PMC4892450 summarising fetch", "Landrein et al. 2015 Table 1 via PMC4339594 summarising fetch"]}
```
