# Challenge 222: the grader calibration (claim 222)

**Verdict: WEAKENED.** The count of 7/7 holds up and is fairly labelled `measured`. Two parts of the
claim don't hold:

- **"trusted"**, because the defect class of every item was named in the prompt.
- **"the 166 recorded challenge verdicts now come from an instrument that has been tested"**, because
  the benchmark tests a different task. That task is cued, binary and short, while a challenge is an
  open-ended adversarial review. Some of the 166 verdicts may also come from a different model, and
  the benchmark barely tests the property that matters for those verdicts, which is how often the
  grader fires on a claim that is actually correct.

## Sources and read levels

| source | what it is | read level |
|---|---|---|
| commit `e889e72a` (`origin/swarm-architecture`) | the calibration commit: `db/designswarm/0012_calibration_data.sql` (7 `benchmark_item` rows, 1 `grader_calibration` row) and the claims and index pages | full-text |
| session `session_01QbcBRXmj1D5f1cmzW25ocp` transcript | the grader's exact prompt, its two tool calls and its output, read with `list_events` | full-text |
| commit `619a6b1d`, `docs/specs/SPEC-evaluation-kernel.md` | §3, §4 and §8: the source of "166" and of the calibration requirement | full-text |
| `Co-Authored-By` trailers on challenge commits, all branches | which model signed the challenge commits | listing (trailers are self-declared and were not checked against session records) |

## 1. Arithmetic, redone independently

These are my own calculations, done in Python, not observations:

- 1.38² / 9.81 = **0.1941 m**. Item 1 (19.4 cm) is correct and item 4 (1.94 m) is 10× too large. R = v²/g
  is the right formula for a 45° launch. ✔
- (120 / 40.3)⁴ = **78.6**. Using the rounded 40 mm in the item text gives 3⁴ = 81. Both are
  legitimate, because the item says "40 mm" and the answer key uses 40.3 mm.
- 6.3e-4 / 3.8e-6 = **165.8×** unscaled. Scaled, it is **2.11×** with 78.6 or 2.05× with 81. ✔
- Score: 3/3 known-good marked correct and 4/4 known-bad marked defective, which is **7/7**. The
  grader's output in the transcript matches the `grader_calibration` row. ✔

The arithmetic does not break the claim.

## 2. Is a proxy standing in for the quantity that matters? Yes.

**The quantity that matters** is whether the challenge verdicts are reliable: whether a challenger
calls a fault where none exists, and misses one where it does. The spec this claim answers (§4)
raises exactly this worry. The survival rate is 17%, which "looks exactly like manufactured faults".
The open question was therefore **specificity under pressure to find faults**.

**The proxy measured** is binary correct/defective verdicts on seven one-line claims, given to a
grader that was told which axis to check. The grader prompt (full text in the transcript) attaches a
hint to every item:

> `ITEM 6: ... (the quantity at issue: scaling)`
> `ITEM 5: ... (the quantity at issue: regime validity)`
> `ITEM 7: ... (claimed evidence level: measured)`
> `ITEM 4: ... (the quantity at issue: v^2/g)`

The prompt also lists the four defect classes that count as "defective", which are the same four
the benchmark seeds. So the run tested whether the grader can confirm a defect along an axis it was
pointed at. It did not test whether the grader finds the defect without help. The claim calls the
run "blind", and it was blind only to the number of defective items. It was not blind to where the
defects were.

Three more things set the proxy apart from the target:

- **Pairing gives item 4 away.** Items 1 and 4 have the same wording and differ only in the value,
  19.4 cm against 1.94 m. A grader can spot the odd one out without doing any arithmetic. (This one
  did the arithmetic anyway.)
- **The pressure runs the other way.** The grader was told not to assume a balance. A challenger is
  told to "try hard to break it". The base-rate worry concerns the challenger setting, and the
  benchmark does not reproduce it.
- **Specificity rests on three items.** Two of them barely test anything:
  - "Reynolds number is dimensionless" is textbook.
  - Item 3 (kcnk5b MSA depth) is covered under §3.

## 3. Hidden assumption: a "correct" mark on a known-good item shows the grader rejects nothing true. Relaxed, it does not.

The transcript shows the grader grepped the repository for `0\.842|kcnk5b|burst`. The only file
returned was `findings/gemini-triage-267-problems.json`, a hit on the word "burst". **The pattern
`kcnk5b` matched no file in its checkout, so the committed `kcnk5b_pdb70.a3m` was not there.** (In
this repository the a3m was added in commit `8bf7ee39` on `origin/swarm-architecture`, and it is not
in the tree I have checked out.) The grader still returned item 3 as `correct`, and its output gives
no basis for that mark.

My inference from this: item 3 shows that the grader **accepts a claim it cannot check**. It does
not show that the grader can recognise a correct claim. If you relax the assumption that "marked
correct" means "verified correct", the known-good evidence drops from 3 items to at most 2, and both
of those are trivial.

The item 7 match is also more generous than the claim allows. The answer key says 0.842 m/s was
"DERIVED from a measured Reynolds number". The grader's stated reasons were different:

- it found no provenance in the repository;
- the value has "three significant figures [and] looks derived or modeled";
- it conflicts with the 1.38 m/s used in items 1 and 4.

So the grader got the class right, but by cue and heuristic, not by finding the actual derivation.
The commit describes this as "the correct defect named each time". The 1.38 against 0.842 "conflict"
is the grader's inference, not an error the benchmark seeded. Two burst speeds from different studies
or fish can differ without either one being wrong, so this should not be counted as extra skill.

On item 5, the grader gave CL_max of about 0.6–1.0 and the answer key gives 0.9–1.15. The ranges
overlap but are not the same. "Gave the right low-Re CL_max range unprompted" overstates the match a
little, and the verdict is still correct.

## 4. Is the evidence level honest? Partly.

- **"7 of 7 items" as `measured`: honest.** It is an observed count from one recorded run, and I
  re-read it from the transcript.
- **"TRUSTED", and "the 166 recorded challenge verdicts now come from an instrument that has been
  tested against known answers": not measured.** That half of the sentence is an inference that
  carries a seven-item result over to a different task. Labelling the whole sentence 🟢 measured
  inflates the evidence level, which is one of the four defect classes this benchmark itself seeds.
  Claim 223, the recorder's own scope row ("one grader, seven items, one run"), is the honest
  version. It should qualify claim 222, not sit beside it.
- **Uncertainty is missing.** These bounds are my calculation (exact binomial), not an observation:
  - 7/7 accuracy: 95% two-sided lower bound **59%**, one-sided **65%**.
  - 4/4 sensitivity: lower bound **40%**.
  - 3/3 specificity: lower bound **29%**, and lower still if item 3 is excluded as unverified.

  A claim of "trusted" with a 95% interval that cannot rule out 29% specificity needs that interval
  printed next to it.

## 5. What the author missed: the "166 verdicts" are not from this instrument

- **Task mismatch.** The `grader_calibration` row names `cloud:claude-opus-5-5`, one session, and a
  one-shot binary prompt. The challenge verdicts were written by separate challenger sessions doing
  long agentic reviews with a three-way outcome (survived, weakened, refuted). Spec §3 defines
  calibration for a *grader* whose grades are aggregated, so it is not clear the challenger is that
  grader at all.
- **Possible model mismatch.** I counted `Co-Authored-By` trailers on commits whose subject matches
  "Challenge N" (read level: listing):
  - 182 say "Claude Opus 5.5";
  - **18 say "Claude Opus 5"**;
  - 200 commits have no trailer.

  Trailers are self-declared, so whether any of the 166 verdicts came from a different model is
  `unknown`. It cannot be assumed that they did not.
- **The count is stale.** The same commit `e889e72a` changes `library/pages/project/index.md` so that
  "Challenges resolved" reads **223**, not 166. The claim's "166" comes from the spec's earlier
  count. Which number of verdicts the calibration is supposed to cover is `unknown`, because I did not
  query the database. This repository holds only the dump, not the challenge table.
- **One run, no repeats.** Run-to-run variance at temperature is not measured, so "the instrument"
  is one sample of a stochastic instrument.

Negative search scope: I looked for any second calibration run, a calibration of challenger sessions,
or an uncued variant of the benchmark. I searched commit messages on all branches for
"grader|calibrat" and read the full diff of `e889e72a`, and found none of the three.

## What survives

The grader catches all four seeded defect classes when it is cued to the axis. Its arithmetic and
L⁴ reasoning are sound, and it did not overcorrect the scaling item. That is a real, narrow, positive
result.

What does not survive:

- the claim that the challenge verdicts are now backed by a tested instrument;
- the 🟢 label on that half of the sentence.

**Corrected statement:** "On a 7-item benchmark that named each item's defect axis in the prompt, one
`claude-opus-5-5` grader run scored 7/7 (95% lower bound 59%; 4/4 sensitivity, lower bound 40%; 3/3
specificity, lower bound 29%, with one of the three marked correct without the data needed to check
it). Whether this transfers to the challenge verdicts is unknown."

## How to repair the benchmark (my suggestions, not results)

1. Remove the `(the quantity at issue: …)` hints.
2. Split paired items such as 1 and 4 across separate runs.
3. Add known-good items that look suspicious, such as a correct value with three significant figures,
   a correct regime edge case, and a correctly scaled comparison. These test false-positive rate
   under the challenger's "try to break it" prompt, which is the failure §4 was worried about.
4. Make sure every known-good item can be checked from what the grader is given.
5. Run the actual challenger prompt on the benchmark items, rather than a separate grader prompt.
6. Repeat the run at least 3 times.

```swarm-challenge
{"claim_id": 222, "outcome": "weakened", "reason": "The 7/7 count reproduces and is honestly measured, but every item named its defect axis in the prompt, one of the three known-good passes was accepted without the a3m the grader could not find, specificity rests on 3 items (95% lower bound 29%), and the transfer to the challenge verdicts (a different, uncued, adversarial task, partly signed by a different model, and counted as 223 not 166 in the same commit) is an inference labelled measured.", "corrected_value": "7 of 7 items on a cued binary benchmark (95% CI lower bound 59%; sensitivity 4/4, lower bound 40%; specificity 3/3, lower bound 29%); calibration of the challenge verdicts: unknown", "depends_on": ["e889e72a:db/designswarm/0012_calibration_data.sql benchmark_item rows 1-7 and grader_calibration row 1", "session_01QbcBRXmj1D5f1cmzW25ocp transcript: grader prompt text with per-item 'quantity at issue' hints, and its Grep for kcnk5b returning no kcnk5b file", "619a6b1d:docs/specs/SPEC-evaluation-kernel.md sections 3, 4, 8 (166 count; base-rate worry about manufactured faults)", "e889e72a:library/pages/project/index.md 'Challenges resolved 223'", "Co-Authored-By trailers on challenge commits (listing level; self-declared)", "exact binomial (Clopper-Pearson) bounds computed here"]}
```
