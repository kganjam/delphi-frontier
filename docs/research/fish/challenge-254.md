# Challenge 254 — GXL tool-fit finding ("0 supports on every method claim, over 39 claims")

**Claim under review (author's words):** "TOOL-FIT FINDING, measured over 39 claims: the GXL evidence
API returned 0 supporting passages for EVERY claim about our own method, search or computation. There
is no literature to support 'no measurement was found' or 'the a3m holds 76 sequences', so those zeros
are not evidence of anything and must not be allowed to accumulate as if they were."
Recorded level: **measured**. Value: 0 supports on method claims. Source: GXL claims/support over 39 claims.

**Verdict: WEAKENED.** The policy conclusion (do not aggregate GXL zeros on method/scope claims) holds,
but it holds as a reasoning argument, not as a measurement. The "measured over 39 claims" part cannot
be reproduced from anything in this repository, the code that is committed cannot have produced it,
and the claim's own worked example is contradicted by the committed file.

## What I could access (read-levels)

| Source | Read-level |
|---|---|
| `swarm/evidence.py` at commit `699f320d` (branch `origin/swarm-architecture`, identical at branch tip) | full-text |
| Commit messages `699f320d`, `de44fffd` | full-text |
| `library/pages/project/claims.md` and `corrections.md` on `origin/swarm-architecture` | full-text (table rows truncated by the page generator) |
| `results/fish-proteins/structures/kcnk5b_pdb70.a3m` on `origin/swarm-architecture` | full-text |
| The `artifact_signal` rows (Postgres at 127.0.0.1:5436, `designswarm`) holding the per-claim GXL counts | could-not-access (private host, not in this container) |
| GXL endpoint `https://paperclip.gxl.ai/api/v1/claims/support` | could-not-access (outbound proxy returned 403 on CONNECT; no API key available here) |

Negative-search scope: `git grep` for `GXL`, `claims/support`, `tool-fit`, `39 claims` across all
remote branches of `kganjam/delphi-frontier` fetched on 2026-11-04, plus `git log --all --grep`.
Only two commits (`de44fffd`, `699f320d`) and one script mention GXL. No artifact records a 39-claim run.

## 1. Arithmetic, redone independently

There is no arithmetic in the claim beyond a count (39) and a value (0). Neither can be recomputed:
the per-claim counts live only in the inaccessible `artifact_signal` table. The one run the repository
does document is the commit message of `699f320d`: **"FIRST RUN: 14 claims, 3 with supporting
literature, 8 where refuting evidence outweighed supporting."** That is n = 14, not 39, and it does
not break out how many of the 14 were method claims or what each returned. The count of 39 is
therefore `unknown` from the record; I did not invent a substitute.

## 2. Proxy

The quantity that matters is: *does the engine discriminate when applied to method/scope claims?*
The proxy used is: *method claims returned 0 supports.* That proxy cannot separate the two
explanations the claim needs separated:

- (a) **tool mismatch** — the claim type has no literature, so any answer is meaningless; vs
- (b) **ordinary narrowness** — the claim is more specific than any passage, which the project
  elsewhere treats as an *informative* zero (claim 242, S31: "0 supporting passages of 35" recorded
  as **measured** evidence that a constraint is unsatisfied).

Both produce 0 supports. The right measurement is a positive control *of the same claim type*: a
method-shaped statement that does have literature behind it (e.g. "PDB70 contains TRAAK K2P channel
structures"). If that also returns 0, the mismatch is shown; if it returns supports, the zeros on our
own method claims are just the narrowness case. No such control was run (inference from the absence
of any record; the only control in `evidence.py` is a biology claim, floor 5 supports).

My inference, not the author's: the "0" is predicted a priori by the author's own argument ("there is
no literature to support..."). A result that is guaranteed by the definition of the category does not
measure a tool property; it restates the category.

## 3. Hidden assumption, relaxed

The assumption carrying "EVERY method claim" is that method claims are cleanly literature-free. Relax
it and it fails on the claim's own example: claim 83 reads "PDB70 search on kcnk5b a3m holds 76
sequences ...; **top hits are K2P structures**." The second clause is a literature-checkable assertion
(K2P structures such as TRAAK are published). A method claim can carry scientific content, so a zero on
it is not automatically meaningless, and a non-zero is possible. "EVERY" is unverified (scope: the
39 rows were not readable).

A second, structural problem: the committed selector in `evidence.py` **excludes** method/scope claims
before querying (`statement !~* '(scoped to|could not|we searched|this project|recomputed here|verified
here|SCOPE:|LIMITATION)'`). The only committed code cannot have produced a measurement over method
claims; the 39-claim result must come from an uncommitted or earlier run. That is a reproducibility
gap of exactly the kind recorded for claim 210.

## 4. Evidence level

The claim bundles three things under one "measured" label:

| Part | Honest level |
|---|---|
| "GXL returned 0 supports for these claims" | measured (API output), **but unverifiable here**; n stated as 39, only n = 14 is documented |
| "there is no literature to support method claims" | reasoned/derived, not measured; and contradicted in part (§3) |
| "zeros must not accumulate" | a policy recommendation; correct, but not an observation |

Presenting the bundle as **measured** is a defect even though the policy is right. Recommended
level: **derived** (argument + an undocumented API observation).

## 5. Counter-example the author missed

The worked example is factually inconsistent with the committed data. The claim cites "the a3m holds
76 sequences". I counted header lines (`^>`) in the committed
`results/fish-proteins/structures/kcnk5b_pdb70.a3m`: **72** (query + 71 hits) — this is a count I
made, an observation of the file. Sources disagree and I preserve the disagreement:

- claim 83 (🟡 derived, from branch `claude/pdb70-kcnk5b-search-s7699q` replicate-1): 76 sequences;
- claim 211 (🟢 measured, recomputed from the committed file): 72 sequences;
- correction #11 records 72 → superseded by #83's 76.

This does not change the tool-fit argument, but it shows the illustrative "method claim" is itself a
disputed number, which is the opposite of the clean literature-free case the claim relies on.

Also, by the same logic the author applies, claim 242's "0 supports" on a novel mechanistic claim is
exposed to the narrowness explanation (§2). That claim is out of scope here; I flag it, I do not judge it.

## What survives

The policy — exclude self-referential method/scope claims from GXL aggregation, record them as
`not-applicable` rather than as 0-support signals — is sound and is already implemented in the selector.
What does not survive: "measured", "39", and "EVERY".

```swarm-challenge
{"claim_id": 254, "outcome": "weakened", "reason": "The do-not-aggregate policy is sound reasoning, but the 39-claim measurement is unreproducible (only a 14-claim run is documented and the committed selector excludes method claims), 'no literature exists' is derived not measured and fails for method claims carrying checkable content, and the cited a3m holds 72 sequences in the committed file, not 76.", "corrected_value": null, "depends_on": ["swarm/evidence.py @ 699f320d (selector regex excluding method/scope claims)", "commit message 699f320d: first run 14 claims, 3 supported, 8 refute>support", "results/fish-proteins/structures/kcnk5b_pdb70.a3m on origin/swarm-architecture: 72 header lines (counted here)", "claims.md claim 83 (76 sequences, top hits K2P) and claim 211 (72 sequences)", "claims.md claim 242 (0 of 35 supports recorded as measured)", "artifact_signal table with the 39 per-claim GXL counts: could-not-access"]}
```
