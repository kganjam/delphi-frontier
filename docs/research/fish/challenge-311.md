# Challenge 311: "the entailment generator does not check that the refuting measurement concerns the same subject"

**Verdict: WEAKENED.** The core, the part that is an actual observation, survives every check I could run.
Constraint rows from claims 268 and 269 are S32 zebrafish claims. Both were refuted with exocoetid data, and
both refutations go away when the right animal is used. Two parts of the claim go further than its evidence.
The first is the sentence "the error has a SYSTEMATIC DIRECTION rather than being random", which is filed under
evidence level `measured`. It rests on two rows from one parent subproblem, which is effectively one independent
case. The second is the proposed mechanism ("the nearest measurement is usually about the wrong animal"). The
branches themselves point to a more specific and checkable cause: the subject was lost before any literature
search began. Separately, the claim **understates** the defect. The same mistake also produced `satisfied`
verdicts that should not have been given.

Date of checks: 2026-11-04. No new measurement was made. Everything below is either a reading of repository
records or arithmetic on them, and each sentence says which.

---

## What I read (read-levels)

| Source | Read-level |
|---|---|
| `docs/research/fish/S32-organism.md` + `S32_taxi.py`, branch `claude/s32-multi-stroke-launch-qpq9g2` (c1b761eb) | full-text. I ran the script myself (§3) |
| `docs/research/fish/claim-268-entail.md`, branch `claude/claim-268-entail-awpse5` (ba80d5ac) | full-text |
| `docs/research/fish/claim-269-entail.md`, branch `claude/claim-269-entail-r026ky` (61531940) | full-text |
| `claim-234-entail.md` (w70nz4), `claim-185-entail.md` (7lju9n), `claim-192-entail.md` (2ctr6q) | full-text of the unsatisfiable rows and headers |
| All 42 remote branches whose name contains `entail` | listing + grep for `"status": "unsatisfiable"` in each branch's own diff |
| The constraint table with row ids 43, 53, 93, 125 | **could-not-access**. It is not in this repository (searched `main` and all entail branches). Row ids are therefore unverified |
| `docs/FINDINGS.md` | **could-not-access**. It does not exist on `main` (7b5ba52c) or on the entail branches |
| The entailment generator's source code | **could-not-access**. Not in this repository (searched `main` for `swarm-entail` and `entail` outside generated site data and captures) |
| Franzisket 1965, Fish 1990 | not read by me. I use them only as the two entail docs relay them |

---

## 1. Are claims 268 and 269 really about zebrafish? Yes (record reading)

- S32's title: *"Can an airborne-body taxi take the **designed zebrafish** from exit speed to glide speed?"* The
  inputs are a 0.25–0.40 g body, the 1.38 m/s *Danio* burst, the 52 Hz Kyriakatos maximum and the S28
  designed wing.
- Claim 268's text (as the entail doc quotes it: "816x … 4.6 mN to 8 uN … 1.1–3.4 mN … doubling in ~10
  strokes at 52 Hz") is S32 §0 item 1, word for word in substance.
- Claim 269's text ("stalls at 2.19–2.88 m/s, 50–65% of the 4.41 m/s glide speed, ~30–38 strokes over
  1.5–2 m") is S32 §0 item 2.
- Neither entail doc contains the string "zebrafish" or "Danio" (grep, 0 hits each). Doc 268 says outright:
  "The claim is about the flying-fish (Exocoetidae) taxi." Doc 269 says: "I read this as being about flying
  fish."

The author's identification of the subject is correct.

## 2. Were the two refutations made with exocoetid data, and do they fail on the right subject?

**Claim 269, B1** (`unsatisfiable`, evidence `measured`). The contradicting value is Franzisket 1965 via
Deng et al.: 400 m in 30 s. My own arithmetic: 400 / 30 = **13.3 m/s**. That matches the doc. The quantity
that matters is the terminal taxi speed of the *designed 0.25 g zebrafish with a 192 mm² wing*. **That
organism does not exist**, so no measurement of it can exist. My inference: the right status for B1 is
`open` (unmeasurable until the organism is built), not `unsatisfiable`. A flying-fish field speed is a proxy
for an animal 760× heavier (191 g / 0.25 g) whose lobe Reynolds number is 10–40× higher. S32 identifies
that Reynolds number as the very term that separates the two animals.

**Claim 268, C4** (`unsatisfiable`). I redid this from the stated inputs and did not copy the doc's working.
- The doc's own arithmetic is internally correct. Smallest Fish 1990 specimen: 0.003 kg × 8.7 m/s² =
  26 mN, 7.7× the 3.4 mN ceiling. Impulse ceiling: 3.4 mN × 0.19 s = 6.5×10⁻⁴ kg·m/s, which at 10 m/s means
  m ≤ 65 mg. 3 g / 65 mg = 46. All calculated, all agree.
- **On the right subject** (calculated): m·U₀ = 0.25×10⁻³ kg × 1.38 m/s = **3.45×10⁻⁴ kg·m/s ≤
  6.5×10⁻⁴**. Doubling 1.38 m/s in 0.19 s needs a mean acceleration of 7.26 m/s², so a mean net force of
  0.25 g × 7.26 = **1.8 mN**. That lies inside the claim's 1.1–3.4 mN. For the 0.40 g variant the force
  is 2.9 mN, still ≤ 3.4 mN. The momentum budget **closes** for the zebrafish.
- S32's own integration (which I re-ran, §3) gives U = 2.64 m/s at stroke 10 (1.91×). So "doubling in ~10
  strokes" is what the model actually outputs, and C4 is satisfied by construction for the claim's subject.

The author's statement that both rows were refuted with exocoetid measurements, and that the refutations do
not transfer, is confirmed.

## 3. "Self-refuting: S32's equations reproduce the exocoetid taxi to 15 m/s". Confirmed, with two qualifications

I ran `S32_taxi.py` (python3 -I, from my scratchpad; simulated output, not observation):

| Exocoetid case (S32 equations) | U_eq (m/s) |
|---|---|
| 191 g, A_pp 2.6 cm, C_D scaled | 15.6, reaches glide speed |
| 191 g, A_pp 3.1 cm, C_D scaled | 20.5, reaches glide speed |
| 191 g, **A_pp 2.0 cm**, C_D scaled | **11.1** |
| 191 g, A_pp 2.0–3.1 cm, C_D const | 5.0–8.4 |

Zebrafish: generous 2.88 m/s, central 2.19 m/s, matching S32 and claim 269.

1. **Amplitude dependence.** S32's own stated range for exocoetid A_pp is 2.0–3.1 cm (assumed). At the low
   end the model gives an 11.1 m/s ceiling, which is *below* Franzisket's 13.3 m/s mean. "What the model
   predicts" therefore holds for A_pp ≥ 2.6 cm (the rows S32 chose to tabulate), not over S32's whole stated
   range. The 2.0 cm row is printed by the script but not shown in S32 §4.2.
2. **Partial circularity.** S32 picked the scaled-C_D branch *because* flying fish are reported to taxi to
   15–20 m/s (§4.2: "the constant-C_D branch is therefore contradicted"). The exocoetid speed is closer to
   an input to S32's model selection than to an independent prediction.

Neither qualification rescues the refutation. A flying-fish speed cannot contradict a zebrafish claim
whatever S32 predicts for flying fish. But "self-refuting" is sharper than the evidence: the more accurate
statement is "consistent with S32 by construction, for A_pp ≥ 2.6 cm".

## 4. "Both agents partly noticed". Confirmed

- Row from 269: the note field reads verbatim "Conditional: if claim 269 models a small or tank-confined fish,
  this becomes open." The status was still `unsatisfiable`.
- Row from 268: caveat 3 reads "claim 268's model fish runs at a far lower speed or mass than real taxiing
  fish". C4 was still `unsatisfiable`.

## 5. Where the claim goes beyond its evidence

### 5a. "Systematic direction" is an inference, filed as `measured`

- The observation is 2 wrong-subject rows out of 4. Both come from one parent subproblem, S32, and the same
  generator run produced both entail docs 11 s apart (commit times 10:11:28 and 10:11:39). They share one
  context deficit, so they are one independent case, not two.
- Two cases cannot tell a systematic error from a random one. The author's argument for "systematic" is that
  the literature is mostly about flying fish. That is a plausible mechanism, not a measurement. Under rule 4 of
  this review, presenting it inside a `measured` claim is a labelling defect. The count is measured. The
  direction is a hypothesis.
- Counter-evidence within the same set: claim 192 (S28, the same designed zebrafish) was refuted with
  zebrafish data (Demesmay et al. 2025, adult *Danio* escape speed), the correct subject. That doc named its
  source branch. Claim 234 (S29) used exocoetid data but stated its scope ("Refutes applying single-stroke
  supply to exocoetids, not the inequality beta > alpha itself"), and S29's claim itself uses exocoetid β.
  So among zebrafish-design claims, a nearby flying-fish paper did **not** always win.

### 5b. A more specific mechanism, visible in the branches (record reading + my inference)

- Both 268 and 269 entail branches are cut from `3272d3e`, a commit on which `docs/research/fish/` does not
  exist. S32 lived only on `claude/s32-multi-stroke-launch-qpq9g2`. Doc 269 records this directly: "The
  repository has no earlier fish documents … so I don't know the body size, species or model."
- The claim text handed to the agents is an excerpt of S32's `answer` field with the subject removed. The
  word "zebrafish" appears only in S32's title and further into its answer, not in either excerpt.
- My inference: the defect is first a **context-propagation** failure (subject and source document never
  reached the agent), and only second a failure to check subject. A subject check cannot run when the subject
  was never passed in. The claim's framing ("does not check") is right but incomplete. The fix should be to
  carry `subject` (taxon, body mass, designed-vs-natural) and the source branch into every entailment row,
  then refuse `unsatisfiable` when the measurement's taxon differs from it.
- I could not read the generator code (could-not-access), so I can't say whether it drops the subject or
  never had one.

### 5c. The defect is larger than "2 false refutations": it also produces false `satisfied`

Reading the same two docs, these verdicts rest on exocoetid data applied to the zebrafish:
- 268 **C1 `satisfied`**: "elongated hypocaudal lobe, 63.1% of caudal fin, six exocoetid genera". S32 §1
  states that "the zebrafish lobe has no hypocercal cant". This is a false positive by the same defect.
- 268 C3 `satisfied`, using Hubbs's 9 m exocoetid taxi. 269 B2 `satisfied`, using Hertel/Davenport ~50 Hz
  flying fish. 269 O3 `satisfied`, using Wardle's contraction time for L = 0.3 m. 269 O1 stride ratios
  computed for L = 0.25–0.30 m. Each of these comes out satisfied or plausible for the zebrafish *for other
  reasons* (S32's own inputs), but the cited evidence is for the wrong animal.

So auditing only `unsatisfiable` rows underestimates the defect. False `satisfied` rows are more dangerous,
because nobody re-reads them.

## 6. Unverified parts of the claim (stated, not refuted)

- **Row ids 93, 125, 43, 53 and "the first 4".** The constraint table was not accessible (could-not-access),
  so the ids could not be checked. What I could check: across all 42 `entail` branches, exactly 5 contain an
  `unsatisfiable` status. By commit time they are 268 (10:11:28), 269 (10:11:39), 234 (10:12:41), 185
  (10:12:43) and 192 (10:15:42). The first four by commit time are 268, 269, 234 and 185. That fits the
  claim, if rows 43 and 53 are 234 and 185. Their notes do each "state explicitly what it does and does not
  refute", which matches the author's description. The ordering of row ids (43 and 53 below 93 and 125)
  doesn't follow commit order, so the mapping is unconfirmed. Scope of that negative: these 42 remote
  branches only, not the swarm's database.
- I judge 234 sound but borderline. It applies exocoetid stroke counts to a claim about a zebrafish design,
  but it explicitly limits itself to the exocoetid half of that claim's argument.

## 7. Corrected statement

> Two of the first four `unsatisfiable` entailment verdicts (from S32 zebrafish claims 268 and 269, row ids
> per the host's table) were made with exocoetid data and do not hold for the claim's subject. On the
> 0.25 g zebrafish, 268's momentum budget closes (1.8 mN needed vs ≤ 3.4 mN; calculated), and 269's taxi
> speed is unmeasurable because the organism does not exist, so the row should be `open`. Both come from
> one parent and one context failure. Entailment ran on a base without S32, on claim text stripped of its
> subject. The same failure also produced false `satisfied` verdicts (268 C1 hypocaudal lobe). Whether the
> error is systematic toward flying-fish literature is a hypothesis with one independent case behind it.

```swarm-challenge
{"claim_id": 311, "outcome": "weakened", "reason": "The two wrong-subject refutations are confirmed (zebrafish claims 268/269 refuted with exocoetid data; 268's momentum budget closes on the 0.25 g zebrafish at 1.8 mN needed vs <=3.4 mN), but 'systematic direction' rests on one independent case (both rows from S32, generated 11 s apart from a base lacking S32) and is an inference filed as measured, the better-evidenced mechanism is lost context rather than literature abundance, and the same defect also produced false 'satisfied' verdicts the claim does not count.", "corrected_value": null,
  "depends_on": ["S32-organism.md (claude/s32-multi-stroke-launch-qpq9g2, c1b761eb): subject is a designed 0.25-0.40 g zebrafish", "S32_taxi.py re-run: zebrafish U_eq 2.19-2.88 m/s; exocoetid 191 g U_eq 11.1 (A_pp 2.0 cm) / 15.6 (2.6 cm) / 20.5 (3.1 cm) scaled C_D", "claim-268-entail.md (ba80d5ac) C4 and C1 rows", "claim-269-entail.md (61531940) B1 row and note", "claim-234/185/192 entail docs: scoping and subject of the other unsatisfiable rows", "Franzisket 1965 400 m in 30 s as relayed by Deng et al. 2019 (not read by me)", "Fish 1990 specimen masses 0.003-0.53 kg as relayed by claim-268-entail (not read by me)", "entail branches based on 3272d3e, which lacks docs/research/fish/", "constraint-table row ids 43/53/93/125: could-not-access, unverified"]}
```
