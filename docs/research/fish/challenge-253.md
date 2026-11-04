# Challenge 253: adversarial review of "LIMITATION TWO: the engine is mismatched to claim TYPE"

**Claim under review** (the author's wording, not mine):
> "SECOND LIMITATION: the engine is mismatched to claim TYPE. Many of our claims are about our own method or search scope ("the no-homolog result is scoped to PDB70") rather than about the world. A literature engine cannot support or refute a statement about what we searched, so its verdict on those is meaningless and must not be aggregated."

Recorded evidence level: `derived`. Value: n/a. Source: "inspection of claims 2 and 19".

**Verdict: WEAKENED.** The narrow logical point holds: a statement whose only content is "we searched X" or "we could not read Y" is about our own process, and no outside corpus can confirm or deny it. But the claim goes further than that, in three ways that matter:
- Both claims it cites as examples are **hybrids**. Each contains a proposition about the world.
- For one of those two (claim 19), the world proposition has **already been shown wrong** by challenge 19. That is exactly the kind of error an outside literature check could plausibly catch.
- The fix the claim justifies ("must not be aggregated", implemented as a keyword filter) **excludes by wording, not by type**. On the claims table it misses scope claims and catches world claims.

## What I worked with

| Source | What it is | Read-level |
|---|---|---|
| Commit `699f320d` (`origin/swarm-architecture`), message + `swarm/evidence.py` | The claim's origin and how it was implemented | full-text |
| `library/pages/project/claims.md` on `origin/swarm-architecture` (commit `b65a9c4b` lineage) | Wiki export of 145 live claims. **Statements are cut off at about 150 characters** | listing |
| `docs/research/fish/challenge-19.md` (commit `91206219`) | Earlier adversarial review of claim 19 | full-text |
| Claims database (`designswarm` Postgres, `claim` table) | Full statement text, and any GXL engine output on claims 2 and 19 | could-not-access (local DB on the author's host, not reachable from this session) |
| GXL `claims/support` API | Would let me re-run the engine on claims 2 and 19 | could-not-access (no API key in this session; I did not try to obtain one) |

Search scope for the negatives below: I searched `git log --all` for the claim text and for "scoped to PDB70", and searched the tree of `origin/swarm-architecture`. I found **no recorded engine output** (support/refute/neutral counts) for claims 2 or 19 anywhere in the repo.

## 1. Arithmetic

The claim itself contains no arithmetic. The commit that goes with it states that "Both exclusions ... leave 136 claims the engine can actually judge". I tried to recompute this myself:

- claims.md lists **145** live claims (observed: I counted the table rows).
- I applied the selector's two regexes from `evidence.py` to the cut-off statements in claims.md (a calculation on truncated text, not on the DB). 4 statements match the scope regex (claims 19, 22, 223, 232) and 1 matches the concessive regex. That gives 145 − 5 = **140**, if the two sets don't overlap.
- I cannot reproduce 136. The DB's full statements may match more patterns, the selector also has a `length between 40 and 1200` filter, and the DB snapshot may differ from the wiki snapshot. **Recomputed value: unknown.** 140 is only an upper-bound estimate from truncated text.

## 2. Proxy: the selector uses wording as a stand-in for claim type

The quantity that matters is: *does this claim contain a proposition about the world that literature could bear on?* The implementation instead uses **phrases that suggest provenance or scope**: `scoped to|could not|we searched|this project|recomputed here|verified here|SCOPE:|LIMITATION`. I ran this regex against claims.md (truncated text, so this is a calculation and a lower bound on misclassification):

- **False negatives (scope or method claims that are NOT excluded):**
  - Claim 2, which the claim itself cites as evidence ("The only retrieved adult Danio swimming speed is Ucrit = 0.548 m/s ..."), does **not** match the regex in its visible text. Whether its full DB text matches is unknown.
  - Claim 4 ("no retrieved fish measurement of any species approaches 5.8 m/s") is a negative bounded by search scope, and it also is not excluded.
- **False positives (world claims excluded by wording):**
  - Claim 232 ("... S7-D could not reach is now derived from measur...") reports a derived result about the girdle section. It is excluded only because the phrase "could not" appears in it.
  - `recomputed here` / `verified here` are provenance phrases, not scope phrases. If they appear in a claim's statement, they exclude world claims. An example would be claim 15's proposition (kcnk5b has two K+ selectivity-filter motifs), which is a fact about a protein that the literature on two-pore K+ channels speaks to. In the exported table that phrase sits in claim 15's source column, not its statement, so whether claim 15 itself is excluded is unknown.

So the claim's conclusion ("must not be aggregated") rests on a classifier the claim never validated. This is my inference from the regex and the table.

## 3. Hidden assumption: a claim is EITHER about our search OR about the world

The claim treats type as all-or-nothing. Its own two exemplars break this assumption:

- **Claim 19** has three parts:
  - (a) "the no-homolog result is scoped to PDB70". This is about our process, and literature cannot judge it.
  - (b) "PDB70, a STRUCTURE database". This is a **world fact about a public resource**.
  - (c) "this workbench exposes no sequence-database search". This is about our tooling.

  Challenge 19 found **(b) is wrong**: PDB70 is an HH-suite library of sequence-profile HMMs of PDB chains, searched by profile–profile comparison. Challenge 19's read-level for that was the author's background knowledge of the HH-suite docs. I did not re-fetch them either. Part (b) is the kind of statement a literature engine *can* bear on. If the engine had returned refuting passages for claim 19, that verdict would not have been "meaningless". It would have pointed at a real error. This is my inference: I have no record of what the engine actually returned for claim 19.
- **Claim 2** contains "adult Danio Ucrit = 0.548 m/s, a SUSTAINED speed, not a burst". Literature can support or refute this directly: it is a measured value, and Ucrit is by definition a prolonged-swimming metric. Only the "only retrieved" qualifier is about our search.

Now relax the assumption and allow hybrid claims. The defensible rule becomes **asymmetric**, and I offer it as my inference, not the author's:
- *Support* from literature for a scope claim tells you nothing about the scope part.
- *Refutation* of an embedded world clause is informative, and so is a passage that reports what our search said it did not find (for example, a fish measured above 5.8 m/s against claim 4). It means the claim is wrong, or our search missed something.

Excluding these claims wholesale throws away the very signal that can catch search gaps. Search gaps are the main way a scope-bounded negative goes wrong.

## 4. Evidence level

- `derived` is generous. Nothing was computed. The claim is an argument from inspecting two claims, with no engine output recorded for either. The honest label is closer to *argued / inspection*. It is not a defect of inflation exactly, since no number is claimed. But the commit title says the engine's "two limitations" were **measured**. Limitation one was measured (claim 14: 2 supports / 6 refutes vs 0 / 0 / 35 rephrased). **Limitation two was not measured**: the repo contains no counts for any scope claim. The title presents an inference as a measurement.
- "Many of our claims": in the visible text of claims.md, only 4 of 145 statements match the scope regex. That is a calculation on truncated text. Hybrid claims like 2 and 4 would raise the count, but nobody has counted them. "Many" is unquantified.

## 5. Counter-example the author missed

Claim 19 itself is the counter-example. It is the exemplar the claim quotes, and an independent review found that its world-facing clause was wrong. Claims about our *search scope* often depend on a world fact about the *resource searched*: what PDB70 contains, what Ucrit measures, which hosts serve a paper. Those facts are literature-checkable. "About our method" therefore does not imply "outside the literature's reach".

## Corrected statement

> "A literature engine cannot judge the purely self-referential part of a claim ('we searched X', 'we could not read Y'). Support it returns for such claims carries no weight. But most of our scope claims also contain world propositions (what a database contains, what a metric measures, whether a value exists). Refutation of those, or passages reporting what our search said was absent, is informative and should be kept, flagged as bearing on the world clause only. The current keyword selector is a stand-in for claim type and was not validated. On the exported claims table it misses scope claims 2 and 4 and excludes world claim 232. No engine output on any scope claim has been recorded, so this limitation is argued, not measured."

```swarm-challenge
{"claim_id": 253, "outcome": "weakened", "reason": "The purely self-referential part of a scope claim is indeed beyond a literature engine, but both cited exemplars (claims 2 and 19) embed world propositions, claim 19's ('PDB70 is a structure database') was already shown wrong by challenge 19, the keyword selector implementing the exclusion misclassifies claims in both directions, and the limitation was argued from inspection rather than measured, so 'meaningless, must not be aggregated' overreaches: refutations of embedded world clauses carry signal.", "corrected_value": null, "depends_on": ["commit 699f320d message and swarm/evidence.py selector regex (full-text)", "library/pages/project/claims.md on origin/swarm-architecture, truncated statements of claims 2, 4, 19, 22, 223, 232 (listing)", "challenge-19 verdict that PDB70 is a sequence-profile HMM library, not a structure database (commit 91206219; its own read-level: background knowledge of HH-suite docs)", "absence of any recorded GXL engine output for claims 2 or 19 in the repo (scope: git log --all and origin/swarm-architecture tree)"]}
```
