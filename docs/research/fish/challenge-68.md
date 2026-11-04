# Challenge 68: "LAWENTRY takeoff-stall-speed dispatched"

- **Claim under attack:** "LAWENTRY takeoff-stall-speed dispatched"
- **Recorded evidence level:** unknown. **Value:** n/a.
- **Source session:** `session_01QbcBRbxspfHyvN1ZzaDR6W`
- **Challenger:** adversarial cloud review, 2026-11-04
- **Verdict:** SURVIVED. The task was dispatched. The worker finished and pushed an entry, and that
  entry passes the repo's gate. Every derived number in it that I recomputed matches. I found one
  regulatory paraphrase I could not verify (§5) and a dispatch-base problem (§3). Neither touches
  the dispatch claim itself.

## What the claim says

It records one operation: the law-library task for "stall speed from wing loading" was handed to a
worker. It does **not** say the entry is correct, merged or reviewed. Reading it as "a correct entry
is in the library" would treat a proxy as the target, so I checked that stronger reading separately
(§2).

## Evidence (read-levels stated; all items observed by me unless marked)

1. **Session record** (`get_session`, read-level: full record). Title "Takeoff stall speed".
   Created 2026-11-04T08:14:54Z, status bucket `COMPLETED`, outcome branch
   `claude/takeoff-stall-speed-aiygrv`, source revision `work/frontier-foundation`.
2. **Transcript** (`list_events`, kinds user+result, limit 100). It returned 27 events and I read
   all 27.
   - The first user event (08:14:54Z) is the prompt "Write ONE law-library entry: Stall speed from
     wing loading, and its sensitivity to CL_max". It names the target file
     `library/laws/takeoff-stall-speed.yaml`.
   - The final `result` event (08:19:01Z) has `subtype: success`, `is_error: false`,
     `terminal_reason: completed`, 26 turns.
3. **Commit** `0e202f2f` on `origin/claude/takeoff-stall-speed-aiygrv` (read-level: full text). It
   adds `library/laws/takeoff-stall-speed.yaml` (181 lines), and its `Claude-Session` trailer names
   the source session. `git branch -r --contains 0e202f2f` lists only that branch.
4. **Gate.** I ran `python3 -I library/tools/check_laws.py --dir library/laws` on a clean
   `git archive` of `0e202f2f`. Output: `3 entries, 0 problems`, `ok takeoff-stall-speed.yaml`.
   - The transcript also shows the worker feeding the checker a copy with the square root removed.
     The checker rejected it: "'V_s' is L^1·T^-1, other side is L^2·T^-2". So the gate is live for
     this equation, not a rubber stamp.

**Negative scope:**
- `library/laws/takeoff-stall-speed.yaml` does not exist on `origin/main`.
- `gh api search/issues` with `repo:kganjam/delphi-frontier is:pr head:claude/takeoff-stall-speed-aiygrv`
  returned 0.
- So the entry is delivered, **unmerged, and has no PR**. That is consistent with the session's own
  summary ("no PR opened") and with the claim, which says only "dispatched".

## 1. Arithmetic, redone independently (all CALCULATED by me, not observed)

Inputs are the entry's own: m = 0.4 g, g = 9.80665, S = 3.2e-4 m², ρ = 1.2 kg/m³, Ucrit = 0.548 m/s.

| Entry states | Mine | Match |
|---|---|---|
| W = 3.924e-3 N; W/S = 12.3 N/m² | 3.9227e-3 N; 12.26 N/m² | yes |
| S from span 0.04 m, AR 5 | b²/AR = 3.2e-4 m² | yes |
| V_s at CL_max 0.6 / 0.7 / 0.8 / 1.07 / 1.15 = 5.84 / 5.40 / 5.05 / 4.37 / 4.22 m/s | 5.835 / 5.402 / 5.054 / 4.370 / 4.215 | yes |
| 7.7–10.7 × Ucrit | 7.69–10.65 | yes |
| CL_max range factor 1.92 → V_s factor 1.38 | 1.917; √1.917 = 1.384 | yes |
| +10% CL_max → −4.65% V_s; −10% → +5.41% | −4.654%; +5.409% | yes |
| 1/1.13² = 0.783; 1/1.08² = 0.857 | 0.7831; 0.8573 | yes |
| Halving CL_max → ×1.414 | √2 = 1.4142 | yes |
| 0.6 vs 1.15 moves V_s "up to about 40%" | 38.4% | yes |

Using the entry's own ISA ρ = 1.225 instead of 1.2 moves V_s(0.6) from 5.84 to 5.78 m/s (calculated,
−1%). The 1.2 value is inherited from challenge-23's inputs, so this is not an error. I found no
arithmetic fault.

## 2. Proxy

"Dispatched" stands in for "a usable entry exists". I checked that stronger quantity directly
(evidence 3–4 and §1). The entry exists, passes the gate, and its numbers are right. It is not
merged, and the claim does not say it is. The proxy and the target agree, up to merge status.

## 3. Hidden assumption, relaxed

The dispatch assumed the worker's checkout contained the template and the checker. **It did not.**
- The worker's first command (08:15:02Z) returned `ls: cannot access 'library/laws': No such file or directory`.
  The source revision was `work/frontier-foundation`.
- The worker recovered by basing its branch on `699500a7`, the first commit that carries `library/`.
  The commit message says so.
- As a result:
  - `git rev-list --count origin/work/frontier-foundation..0e202f2f` = **1384**.
  - `git log origin/main..0e202f2f` = **8 commits**. They include unrelated protein, MyST and
    skill-vendoring work, not just the one-file entry.
- The same defect is recorded for the euler-buckling dispatch (challenge 55).

The worker's first push was also rejected three times with "stale info" (08:18:33Z). A retry at
08:18:41Z created the branch.

With the assumption relaxed, the dispatch still happened and still delivered. My inference, not
stated by the source: had the worker not gone looking for `library/`, no gated entry would exist,
and "dispatched" would then have been true but empty.

## 4. Evidence level

`unknown` understates it. The dispatch and its completion are **observed** in the session record,
the transcript and git. The claim presents no derived number as measured.

Inside the entry, I checked the labelling:
- The worked examples are tagged `evidence: derived` and say "CALCULATED".
- The external sources are honestly labelled `search-summary`.
- The hawk 1.6 is marked as a lower bound, not a confidence interval.
- The 1.8 bird value and the clean-wing ~1.5 were left out as unverifiable. They were not invented.

I found no mislabelling.

## 5. Counter-examples, and one unverified concern

There is no physical regime against which to test a dispatch. I looked for the operational
counter-examples and found none:
- an errored turn
- a missing branch
- a gate failure
- an overwritten file

**Scope of that negative:** this one session's 27 user/result events and this one branch. I did not
survey other sessions for a duplicate takeoff-stall-speed dispatch.

**Unverified concern, for whoever challenges the entry itself (not this claim).** The entry
paraphrases 14 CFR 25.107(b)'s 1.08 V_SR arm as applying to "four-engine airplanes on which applying
power significantly reduces stall speed". My recollection, from memory and **not retrieved**, is
that the rule lists two separate cases:
- turbopropeller and reciprocating-engine airplanes with more than three engines; or
- turbojet airplanes with provisions for a significant power-on stall-speed reduction.

On that reading, the entry merges the two cases into one. I tried to fetch
`www.law.cornell.edu/cfr/text/14/25.107`, and it failed DNS resolution, as `www.ecfr.gov` did for
the worker. **So this is unknown, not a finding.** It does not affect the 1.13 factor or the
0.783 / 0.857 arithmetic. To verify it, `www.law.cornell.edu` or `www.ecfr.gov` has to be added to
the session's allowed network domains.

```swarm-challenge
{"claim_id": 68, "outcome": "survived", "reason": "Session session_01QbcBRbxspfHyvN1ZzaDR6W received the takeoff-stall-speed law-entry prompt at 08:14:54Z, ended with result subtype success, and pushed commit 0e202f2f adding library/laws/takeoff-stall-speed.yaml, which passes check_laws.py (3 entries, 0 problems) and whose derived numbers all reproduce; the only faults are that the dispatch base lacked library/ (worker rebased onto 699500a7) and the entry is unmerged with no PR, neither of which contradicts 'dispatched'.",
  "corrected_value": null,
  "depends_on": ["get_session record for session_01QbcBRbxspfHyvN1ZzaDR6W (status bucket COMPLETED, outcome branch claude/takeoff-stall-speed-aiygrv)", "list_events transcript of that session (27 user/result events; first prompt 08:14:54Z; result subtype success 08:19:01Z)", "origin/claude/takeoff-stall-speed-aiygrv commit 0e202f2f", "library/tools/check_laws.py at 0e202f2f (3 entries, 0 problems)", "work/frontier-foundation lacking library/ (dispatch-base caveat; branch based on 699500a7)", "challenge-23 inputs (m 0.4 g, S 3.2e-4 m^2, rho 1.2, Ucrit 0.548 m/s) used in the arithmetic recheck"]}
```
