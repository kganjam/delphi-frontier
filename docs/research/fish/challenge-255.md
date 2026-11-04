# Challenge 255: "the evidence API is valuable only on a narrow subset, and that is the design study's fault, not the tool's"

**Claim under review (author's text):** "So the evidence API is valuable on a NARROW subset: claims
asserting something about biology that someone else might have published. On this project most
claims are computed values specific to this design, which is a property of a design study rather
than a defect in the tool."
Recorded evidence level: derived. Value: n/a. Source: inference from the 39-claim run.

**Verdict: WEAKENED.** The descriptive half mostly holds. The causal half, "rather than a defect in
the tool", does not. The author's own recorded run documents a tool defect, and that defect affects
the very subset the claim calls valuable. The run named as the source is also not recorded anywhere
I could reach.

## Inputs and read-levels

| Input | What it is | Read-level |
|---|---|---|
| commit `699f320d` (branch `swarm-architecture`), `swarm/evidence.py` | the run script and its commit message, which state the two measured limitations | full-text |
| commit `de44fffd` | the controls: 28/0/7, 0/1/34 and 0/0/35 (supports/refutes/neutral) | full-text (commit message only; the raw API responses are not in the repo) |
| `library/pages/project/claims.md` @ `origin/swarm-architecture` (sha256 `a6168e94…4cb83`) | 145 live claims with their recorded evidence level | full-text, but each claim's text is **truncated at roughly 140 characters** in this table |
| the "39-claim run" | the run the claim cites | **could-not-access** |
| the GXL `claims/support` API | the tool itself | not queried by me (the key lives in the author's environment, `~/.config/morphoswarm/paperclip.env`) |

**Negative search, scoped:** I fetched all 646 remote branches of `kganjam/delphi-frontier` and
searched every text file for `39 claims|39-claim|NARROW subset|property of a design study`. I also
searched every commit message for `evidence|paperclip|GXL|39`. Nothing records a 39-claim run. The
committed record shows a **14-claim first run** (3 with support, 8 with more refuting than
supporting passages). It also says the selector "leaves 136 claims the engine can actually judge."
The per-claim results go to a Postgres table (`artifact_signal`, `voter_id='gxl-evidence'`) on the
author's host, which I cannot reach. Where "39" came from is therefore `unknown`.

## 1. Arithmetic, redone independently

The claim contains no number, so there is no arithmetic to reproduce. Its quantitative content is
the word "most", plus the implied claim that the literature-addressable subset is small. I tested
both against the full claim table instead of the unrecorded run, using my own hand classification
(script: `challenge-255-classify.py`; run it with the claims table as its argument):

| Bucket (my classification, made by hand) | n / 145 | % |
|---|---|---|
| A: biology a literature engine could check as stated | 32 | 22.1 |
| D: a value computed here about a natural object (a protein, a wild fish), which someone else could have published | 20 | 13.8 |
| C: about this project's method, tools, scope or audits | 22 | 15.2 |
| B: computed values specific to the flying-zebrafish design | 71 | 49.0 |

These are my **derived** counts from a subjective classification of truncated claim text. They are
not a measurement. Another reader would move a handful of rows, and the B share in particular could
plausibly sit anywhere from about 45% to 55%.

- **"Most claims are computed values"** holds if "computed" includes bucket D: B+D = 91/145 = 62.8%.
  The project's own labels agree: 75 derived + 6 simulated = 81/145 = 55.9%.
- **"Most claims are computed values *specific to this design*"** is about a coin flip (49.0%). It is
  not a clear majority. The recorded label "derived" is not a proxy for "design-specific". Claim 21
  (adult Danio peak fast-start speed, derived from a published Reynolds number) and claim 139
  (AlphaFold DB pLDDT for And1) are computed but are biology. Claim 21's quantity has in fact been
  published directly: the project's own claim 75 cites Miln et al. 2021.
- **"Narrow subset"**: A alone is 22%, and A+D is 36%. A third of the claim set is not obviously
  "narrow". "Narrow" is a judgement word, though, and I do not count this point as a refutation.

## 2. Proxy

The claim measures the tool's value by the **whole-claim verdict**: one `claims/support` query on
the full statement. The quantity that matters is whether the engine can check **the published inputs
a claim rests on**. Those are different things. A design-specific conclusion such as "a tail-driven
skim at the measured 52 Hz maximum reaches only 1.15–1.72 m/s" (claim 193) cannot appear in the
literature. Its binding input, the 52 Hz EMG maximum (Kyriakatos 2011, claims 144/145), can.

At least **42 of the 71** design-specific claims name a measured or published input in their
(truncated) text, by a regex count that is a lower bound. Examples are Ucrit 0.548 m/s, bluegill
ray EI 3.8e-6 N m², CL_max for thin wings at low Re, 5795 W/kg pipefish LaMSA power, and frog
spring-loading work. Checked by input rather than by conclusion, the addressable fraction is
roughly A + D + 42 ≈ 94/145 ≈ 65% (derived, approximate). The low value the claim reports is
partly a result of the unit of query. It is not purely a property of the claims.

## 3. Hidden assumption, relaxed

The assumption carrying "rather than a defect in the tool" is that **every** way the engine fails
on this project comes from claim type. The author's own commit `699f320d` names two measured
limitations:

1. **Limitation two (claim type):** a literature engine has nothing to say about method or scope
   claims. That one really is a property of the project, and it matches bucket C (15%).
2. **Limitation one (semantic):** the engine "scores the claim text AS GIVEN, so a claim containing
   the assertion it DENIES gets that clause scored as refuting it." This is a **defect in the
   tool**. It cannot tell an asserted clause from a denied one. The commit calls it "the
   claiming-versus-quoting failure at the SEMANTIC level." It was measured on claim 14, which went
   from 2 supports / 6 refutes with the concessive clause to 0 / 0 / 35 neutral without it.

Relaxing the assumption: limitation one hits the literature-checkable subset hardest, because
claims about biology in this project are very often negative or bounding claims. **14 of the 32**
bucket-A claims carry a negation in their stated text ("NO TELEOST HAS a locomotor spring",
"gain-of-function stiffening is NOT demonstrated", "Fin AREA was never reported", "No
pectoral-restricted regulatory element … is published"). The script's selector only removes
`despite|although|notwithstanding`. It does not remove plain `NOT`/`NO`. So the tool's semantic
defect bites inside the very subset the claim calls valuable.

Caveat, stated beside the finding: limitation one rests on **one** paired measurement (n = 1). I
have no evidence on whether it misfires on every negation, and I did not query the API. "14 of 32
are in the failure regime" is my inference that they are *exposed*. It is not an observation that
they were mis-scored.

## 4. Evidence level

"Derived" is generous. The claim is an **interpretation** of a run whose output is not in the
repository. It is not a calculation from stated inputs. Read honestly, it is `assumed` (or
`derived` from an unrecorded input, labelled as such). The negative control showed that the engine
discriminates on one known-true claim and one open claim. That establishes the search works. It
does not establish the claim's causal attribution, which nobody tested. No run compared bucket-A
claims phrased positively against the same claims phrased negatively.

## 5. Missed regime

The claim's own dichotomy, "about biology someone else might have published" versus "computed
values specific to this design", leaves out bucket D: computed values about natural objects. These
are exactly where an independent literature check is most useful, because the project re-derived
something that may already exist. Claim 21 versus claim 75 is the worked example. The project
derived 0.84 m/s from a Reynolds number before finding the direct measurement (0.45–1.38 m/s, Miln
et al. 2021, as cited by the project). A literature engine pointed at claim 21 is the tool that
would have caught that earlier. I did not query the API to confirm that it would. That is an
inference.

## Summary

- **Survives:** the engine has nothing to judge on method and scope claims (limitation two), and a
  plurality of claims are design-specific computed values.
- **Weakened:** the attribution "rather than a defect in the tool". The author's own run documents
  a semantic tool defect (limitation one, n = 1) that is exposed in 14 of the 32 claims in the
  "valuable" subset. The "narrow" scope also depends on querying whole conclusions rather than
  their published inputs (≥42 of 71 design-specific claims name one).
- **Unverifiable:** the cited "39-claim run" is recorded nowhere I could reach (all 646 branches,
  all commit messages). The evidence label should say so.

```swarm-challenge
{"claim_id": 255, "outcome": "weakened", "reason": "Design-specific claims are about half (49%, my derived hand classification of 145), not clearly most; the author's own run documents a semantic tool defect (negation scored as refutation, n=1) exposed in 14 of 32 literature-checkable claims, so 'rather than a defect in the tool' is false in part; whole-claim queries understate reach since >=42 of 71 design-specific claims rest on a published input; and the cited 39-claim run is not recorded in any branch.",
  "corrected_value": null,
  "depends_on": ["commit 699f320d message: limitation one measured on claim 14 (2 sup/6 ref vs 0/0/35)", "commit 699f320d message: limitation two (method/scope claims unjudgeable)", "library/pages/project/claims.md @ origin/swarm-architecture sha256 a6168e94de0c8c1fe8ea035e9694f0f5a8af64c60aa697d51982f4142664cb83 (145 live claims, text truncated)", "my hand classification of the 145 claims into A/B/C/D (docs/research/fish/challenge-255-classify.py)", "negative search for the 39-claim run across all 646 remote branches and all commit messages"]}
```
