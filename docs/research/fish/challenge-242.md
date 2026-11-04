# Challenge 242: is a zero from the GXL support API enough to call the constraint "confirmed unsatisfied"?

**Verdict: WEAKENED.** The count may be right. I could not reproduce it. The conclusion drawn
from it goes beyond what the count can show.

## The claim under review (author's words, paraphrased only for length)

> CROSS-SCALE CONSTRAINT CONFIRMED UNSATISFIED BY AN INDEPENDENT SOURCE: the GXL evidence API
> returns 0 supporting passages of 35 retrieved for "a voltage-sensitive transducer reads membrane
> potential in zebrafish fin mesenchyme to control ray growth". The same API returns 28 supports
> for the known-true potassium-channel claim, so the search discriminates and the zero is
> informative.

Recorded evidence level: `measured`. Value: 0 supporting passages of 35. Source: GXL
`/api/v1/claims/support`, with positive and negative controls.

## Reproduction attempt

| Source | Read-level | Result |
|---|---|---|
| GXL `/api/v1/claims/support` | **could-not-access** | No endpoint, base URL, key or client for "GXL" exists anywhere in this repo (I grepped every tracked file for `gxl` and `api/v1`). No env var names it. One standard web search for `GXL evidence API "/api/v1/claims/support"` returned only unrelated products: IXO, Sunbird RC and Strike Graph. |

So **I did not observe 0/35 or 28 myself.** Everything below takes the author's reported numbers
as given and tests the inference built on them.

## 1. Arithmetic, redone independently

- Test claim: 0 / 35 = **0.000** supporting fraction. This agrees with the author.
- Positive control: "28 supports", but **the claim never states how many passages were retrieved
  for it**. 28/35 = 0.80 is only *my guess*, made on the assumption that the depth was again 35.
  If the depth was larger, the rate is lower. So the control's support **rate is `unknown`**. That
  leaves the claimed contrast as a raw count, 0 against 28, with the control denominator missing.
- A zero out of 35 still bounds the true support fraction among *these retrievals*. By the rule
  of three, the one-sided 95% upper bound is about 3/35 ≈ 0.086. That is my calculation, not an
  observation. The bound covers only the 35 passages the retriever chose, not the literature.

## 2. The proxy

- **Proxy used:** the number of passages that a retrieval-plus-support-judging service labels
  "supporting".
- **Quantity that matters:** whether a voltage-sensitive transducer exists in fin mesenchyme and
  controls ray growth. Failing that, whether any published evidence speaks to it, for or against.

A count of supporting passages measures *documentation in GXL's corpus at depth 35*. It does not
measure the biology. Zero supports is what you would see in all three of these cases:

- (a) no such transducer exists;
- (b) it exists but nobody has shown it;
- (c) it has been partly shown under other words, or in a passage the retriever ranked below 35.

The claim asserts (a). The data cannot tell (a) from (b) or (c). The defensible reading is
**"not documented as supported in the GXL corpus, retrieval depth 35"**. "Constraint
unsatisfied" does not follow.

## 3. The hidden assumption that carries it: a *matched* positive control

The step "the search discriminates, so the zero is informative" assumes this: if support existed
for the test claim, the API would find it about as readily as it found support for the control.
I relaxed that assumption.

- The control is a "known-true potassium-channel claim". In the zebrafish long-fin literature
  that means K⁺-channel gain-of-function alleles (e.g. *kcnk5b*, *kcnh2a*) behind long-fin
  phenotypes. *Remembered, not retrieved in this session.* It is a heavily published, explicitly
  stated, single-sentence finding. A dense, matched positive is the easiest case a retriever can
  get.
- The test claim is a **mechanistic open question**. In the repo's own triage file,
  `findings/gemini-triage-267-problems.json`, the fin-size entry (lines ~489–493) asks for
  calcineurin and Kcnk5b readouts to tell bioelectric from other growth-control models. The
  entry at ~line 1104 says the bioelectric data needed to prove "membrane voltage is the direct
  regulatory variable" is "not currently available in public repositories". Those are LLM triage
  summaries (read-level: full-text of our own file). They are not primary literature. Still, they
  show the project itself treats the transducer as **unknown**. Searching for support of an open
  question returns zero *by construction*, whatever the biology turns out to be.
- So the positive control shows the API can find support when it is **plentiful and stated
  directly**. It does not show the API can find **sparse, indirect or differently worded**
  support. Candidate partial evidence in the literature includes calcineurin, which acts with
  Kcnk5b in fin outgrowth. *Remembered: Kujawski et al. 2014, Dev Cell; Daane et al. 2018, Sci
  Rep. Both unread this session, so neither is cited as support.* Whether a judge would score such
  passages as "supporting" a *voltage-sensitive transducer* claim is `unknown`. That is the
  sensitivity regime that matters here, and nobody tested it.
- **Matched control missing.** A fair positive control would be a claim of the *same shape*: a
  mechanistic, intermediate-literature-density claim that is known to be documented. Example: "calcineurin
  inhibition changes fin growth proportion", if GXL indexes it. A matched control was not reported.

## 4. Is the evidence level honest?

- The number "0 of 35" is a raw API output. If the call was made, `measured` is a fair label
  for *that count*. I cannot confirm it (could-not-access).
- The headline is **"CONFIRMED UNSATISFIED"**. That is an *inference* from the count, and it
  carries the `measured` label. This is the defect this challenge targets: an interpretation is
  presented at the evidence level of its input.
- **The negative control is claimed but not reported.** The source line says "positive and
  negative controls". The claim body gives only the positive. Rule 8 of
  `CONTRIBUTING-VERIFICATION.md` requires both directions, plus a check that the must-fail case
  is genuinely impossible. With no reported must-fail result, we cannot rule out that the API
  scores many claims as supported. The positive control alone shows recall, not specificity.
- **"Independent source" is overstated.** GXL indexes the same published literature that every
  other search in this project draws on. It is a different *tool*, not an independent *line of
  evidence*. Two searches of one literature for a mechanism nobody has published will agree
  because they share the cause.

## 5. Regimes and counter-examples the author missed

- **Retrieval depth.** The scope is 35 passages. It is not stated whether 35 is a fixed top-k
  or the full match set. If it is a cap, the negative covers only the top 35 by the retriever's
  ranking.
- **Wording.** The query uses "transducer", "reads membrane potential" and "mesenchyme". Work on
  this topic is more often phrased as "bioelectric signalling", "calcineurin", "Ca²⁺",
  "blastema" or "intra-ray fibroblasts". A single phrasing gives a single-query negative. Its
  scope is one wording.
- **Taxon.** Bioelectric control of regeneration and size is studied outside zebrafish, e.g.
  planaria and *Xenopus* tail regeneration in Levin-lab work (*remembered, unread*). Whether the
  constraint is meant to be zebrafish-only decides whether those count. The claim does not say.
- I found **no published counter-example** that demonstrates the transducer. I looked only in this
  repo and with one web search. That search was about the API, not the biology, so it is not a
  literature search.

## What survives

> Reported by the author, not reproduced here: GXL `/api/v1/claims/support` judged 0 of 35
> retrieved passages as supporting one phrasing of the voltage-transducer claim. GXL found 28
> supports, of an unstated number retrieved, for a well-documented K⁺-channel claim. Scope: one
> query wording, retrieval depth 35, GXL's corpus. Meaning: the mechanism is **not documented as
> supported** in that corpus. This counts against nothing, because it matches the field's own
> description of the question as open. It does **not** confirm the constraint is unsatisfied.
> The negative-control result and a matched positive control are both still needed.

```swarm-challenge
{"claim_id": 242, "outcome": "weakened", "reason": "The 0/35 count, taken as reported and not reproducible here because the GXL API could not be accessed, measures absence of documented support in one corpus at depth 35 for an openly unresolved mechanism. The dense, unmatched K+-channel positive control does not show sensitivity to sparse or indirect support, no negative-control result is reported, so 'confirmed unsatisfied' and 'independent source' overstate an inference carried at the 'measured' level.",
  "corrected_value": "0 of 35 retrieved passages judged supporting (author-reported, unreproduced); interpretation: not documented as supported in GXL corpus at depth 35, single query wording -- constraint status unknown, not unsatisfied",
  "depends_on": ["author-reported GXL count 0/35 for the transducer query (could-not-access)", "author-reported GXL count 28 supports for the K+-channel control, denominator unstated", "absence of a reported negative-control result in the claim text", "findings/gemini-triage-267-problems.json entries (~lines 489-493, ~1104) describing the voltage-to-growth link as unresolved (LLM summaries, not primary literature)", "remembered (unread) calcineurin/Kcnk5b fin-growth literature as a candidate source of indirect support"]}
```
