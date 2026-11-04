# Challenge 42: "LAWENTRY pennycuick-power dispatched"

- **Claim under attack:** "LAWENTRY pennycuick-power dispatched"
- **Recorded evidence level:** unknown. **Value:** n/a.
- **Source session:** `session_01QbcBRZ3GfM3uxLh2FTF9Wb`
- **Challenger:** adversarial cloud review, 2026-11-04
- **Verdict:** WEAKENED. The dispatch happened and an entry was delivered. But the entry's headline
  observed number is attributed to the wrong sample, and one `where_it_breaks` argument rests on that
  misattribution.

## What the claim asserts

The claim records an operation: a law-library task for the Pennycuick power-curve entry was
dispatched. Read literally, the only test is whether that dispatch happened. I also tested what
"dispatched" stands in for (§2): did the session deliver an entry, and do its numbers survive being
redone?

## 1. Dispatch and delivery (observed, from git)

- Commit `9059d8b2` ("Law library: Pennycuick flight power curve, and where the U-shape fails") is on
  `origin/claude/pennycuick-power-curve-iv52ti`. Its `Claude-Session` trailer is
  `session_01QbcBRZ3GfM3uxLh2FTF9Wb`, which is the claim's source. Observed: I read it from git.
- The commit adds `library/laws/pennycuick-power.yaml` (186 lines).
- I ran the repository's gate, `python3 library/tools/check_laws.py --dir library/laws`, on a worktree
  of that branch. Output: **3 entries, 0 problems**, with `pennycuick-power.yaml ok`. Observed (I ran
  the tool). The gate checks dimensions and mandatory fields only, not whether the content is correct.

**Scope of negative findings:**
- `git branch -r --contains 9059d8b2` lists only that branch.
- The file does not exist on `origin/main`.
- `gh api search/issues` with `repo:kganjam/delphi-frontier is:pr head:claude/pennycuick-power-curve-iv52ti`
  returned 0.

So the entry is delivered but **not merged**, and no PR was found.

Timing note (observed): the commit is timestamped 08:08:45 UTC. My first `git fetch` did not show the
branch; a second fetch about a minute later did. A challenger who checked only once could wrongly
have recorded "not delivered".

## 2. Proxy check

"Dispatched" stands in for "a correct entry is in the library". The literal claim is true. The
stronger quantity fails on one specific, checkable point (§4).

## 3. Independent re-derivation (all calculated by me, not observed)

| Entry states | My result | Match |
|---|---|---|
| V_mr/V_mp = 3^(1/4) = 1.316 with P_pro neglected | d(a/V + cV³)/dV = 0 gives V_mp = (a/3c)^¼; d(P/V)/dV = 0 gives V_mr = (a/c)^¼; ratio 1.31607 | yes |
| A constant P_pro raises V_mr and leaves V_mp alone, so 1.316 is a lower bound | A constant term does not change dP/dV, and it adds a falling term P_pro/V to P/V, which pushes the minimum to higher V | yes |
| V_mp ∝ C_Db^(-1/4); C_Db 0.4 vs 0.1 gives factor 0.71 | 0.25^0.25 = 0.7071 | yes |
| Fish example: a = 2.04e-3, c = 1.2e-6 | S_d = 2.827e-3 m², a = 2.042e-3, c = 1.20e-6 (SI) | yes |
| V_mp = 4.88 m/s, V_mr = 6.42 m/s | 4.880, 6.423 m/s | yes |
| P(V_mp) = 5.6e-4 W | 5.58e-4 W | yes |
| V_mp at C_Db = 0.4: 3.45 m/s | 3.451 m/s | yes |
| v_h = 0.76 m/s | sqrt(mg/(2ρS_d)) = 0.760 m/s. Including k = 0.9 would give 0.721 m/s; the entry's own definition of v_h omits k, so this is consistent | yes |
| Body Re ≈ 1e4 at V_mp, L = 0.03 m | 9.76e3 (ν = 1.5e-5 m²/s) | yes |
| Bumblebee fit 6.43U² − 24.03U + 91.10: minimum at 1.87 m/s, hover/min ≈ 1.33 | U* = 1.869 m/s, minimum 68.65, ratio 1.327 | yes |
| k = 1.2 is "not realistic, should be revised downwards"; dead-body C_Db 0.2–0.4 "anomalously high"; 951 runs on 83 species; C_Db assigned 0.060 to 0.12 | All found verbatim in the Pennycuick et al. 2013 full text (see §5) | yes |

I found no arithmetic error.

## 4. The defect: 0.969 ± 0.0672 is mute swans, not the 31-species sample

The entry's first `worked_examples` item says:

> organism: Migrating birds, 31 species analysed of 83 … value: 0.969 … OBSERVED airspeed divided by
> CALCULATED V_mp, combined sample, +/- 0.0672 (Table 2 as reported in the full text)

`where_it_breaks` (4) says:

> agreement (airspeed/V_mp = 0.969 +/- 0.0672) was obtained only after lowering k to 0.9 and assigning
> per-species C_Db.

I read Table 2 of Pennycuick, Åkesson & Hedenström 2013 (read-level: full-text, Europe PMC XML for
PMC3730693, read 2026-11-04). It says, verbatim (whitespace normalised):

> Table 2. Means and standard deviations of measurements of Mute Swans of known sex from winter swan
> catches at the Wildfowl and Wetlands Trust, Caerlaverock. … sexes combined 16 8.94 ± 1.26 2.30 ±
> 0.111 17.5 ± 1.21 0.969 ± 0.0672; adult males 8 … 0.953 ± 0.0661; adult females 8 … 0.992 ± 0.0688

The surrounding text says the observed swan airspeed of 17.5 m/s "is still below the estimated V_mp,
even if the observed swans are assumed to have been all females."

What this shows. The facts are from the source; the reading of them is mine:
- "Sexes combined" means male and female **mute swans**, n = 16 caught individuals. It is not a
  combined 31-species sample. The ± 0.0672 is a standard deviation that comes from spread in the
  swans' mass and span (the airspeed column is identical across the three rows). It is not the scatter
  of agreement across species.
- The paper uses this table to show that the **largest species still fell below** V_mp. The entry
  inverts that: it presents the number as evidence of agreement achieved across species by recalibration.
  The entry's own text in the same item ("Mute swan airspeed remained close to V_mp …") partly fits the
  table, which suggests the label got crossed with the swan row during the tool-mediated extraction the
  entry itself mentions.
- `where_it_breaks` (4) still holds qualitatively without this number: the parameters *were* revised
  to fit observed speeds, and the paper says so. What does not hold is its use of 0.969 ± 0.0672 as the
  measure of post-revision agreement. I did not find a single across-species airspeed/V_mp summary
  statistic in the parts of the text I searched. I searched for "0.969", "Table 2" and "swan", not the
  whole paper, so I do not claim that no such statistic exists.

Consequence for downstream use: anyone who quotes "birds fly at 0.97 ± 0.07 of V_mp" from this entry
will be quoting a swan-only morphometric spread as if it were a cross-taxon validation. That overstates
how well the model is validated.

## 5. Other checks that survived

- **Evidence levels.** The entry labels its fish example "derived", says not to treat it as a flight
  speed, and says its 1.316 ratio is "DERIVED by me". It labels the hover/min ratio as its own
  arithmetic. These labels are honest.
- **Read-levels.** I confirmed Pennycuick 2013 as full-text by reading it myself. I did not re-read
  Senior et al. 2025, Dial 1997, Tobalske 2003, Ellington 1990 or von Busse 2013, so I neither confirm
  nor dispute those characterisations. The entry keeps the Ellington 1990 (flat) vs Senior 2025 (U)
  disagreement and the Dudley & Ellington 1990 disagreement open, which follows the
  preserve-disagreement rule.
- **Hidden assumption.** The fish example's V_mp moves as (a/c)^¼, so it is fairly robust to any one
  input. For example, the C_Db spread 0.06–0.12 changes it by a factor of only 1.19 (calculated). The
  entry's real caveat is the regime: Re ≈ 1e4 sits below the paper's stated C_Db calibration range of
  Re 25 000–250 000 (read in the full text). That makes the "edge of or below the domain" wording, if
  anything, mild, because the source gives a lower bound of 2.5e4 and the entry says it found none. Its
  `domain_of_validity` note ("not checked … below ~1e4 Reynolds number") could cite the source's
  2.5e4 instead of an inferred 1e4.

## Corrections requested on the entry branch (not applied here)

1. Relabel the worked example: Mute swan, *Cygnus olor*, n = 16 individuals (Table 2, Pennycuick et al.
   2013), airspeed/V_mp = 0.969 ± 0.0672 SD, airspeed still **below** V_mp.
2. Remove 0.969 ± 0.0672 from `where_it_breaks` (4) as the measure of cross-species agreement.
3. Add the source's C_Db calibration range, Re 25 000–250 000, to `domain_of_validity`.

```swarm-challenge
{"claim_id": 42, "outcome": "weakened", "reason": "The dispatch is real (commit 9059d8b2, matching session trailer, gate passes, unmerged) and all arithmetic reproduces, but the entry's headline observed value 0.969 ± 0.0672 is Table 2's mute-swan-only row (n = 16, airspeed still below V_mp), mislabelled as a 31-species combined agreement statistic.",
  "corrected_value": "airspeed/V_mp = 0.969 ± 0.0672 (SD) for mute swans only, n = 16, Pennycuick et al. 2013 Table 2; not a cross-species value"}
```
