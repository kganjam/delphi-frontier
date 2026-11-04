# Challenge 46: "LAWENTRY froude-efficiency dispatched"

**Verdict: SURVIVED, with a provenance caveat. I also found one defect in the entry itself, which
lies outside the claim.** The claim describes the status of a piece of work. The git record shows
that a `froude-efficiency` law entry was written, committed, pushed, and passes the repository's
gate. What I could **not** do is tie that entry to the source session named in the claim. My
sibling challenges 32 and 33 could make that link; this one cannot.

## What the claim is

Source session `session_01QbcBRaWeyX3u1KWMzbVYmN` claims that a task to write the Froude-efficiency
law-library entry was dispatched. The recorded value is "n/a" and the recorded evidence level is
`unknown`. Because this is a status claim, the record is the only thing that can falsify it: does
the dispatched work exist?

## What I checked (2026-11-04)

| Check | Method | Result | Kind |
|---|---|---|---|
| Source session | `get_session` on the source session | **could-not-access**: "the requested resource was not found" | — |
| Entry exists | `git grep -il froude` on every remote branch | `library/laws/froude-efficiency.yaml` exists on `origin/swarm-architecture` only | observation (git record) |
| Commit that adds it | `git log -- library/laws/froude-efficiency.yaml` | `aebc0736`, 2026-11-04 00:07 −0800, author "SciDEX Bot", subject "Four law entries…". The message says the entries were "written by cloud sessions" | observation |
| Link to the source session | `git log --all` bodies grepped for `QbcBRaWeyX3u1KWMzbVYmN`; `git grep` of the same string on all remote branches | **No hits.** Commit `aebc0736` has no `Claude-Session` trailer. Scope: all refs fetched on 2026-11-04 | negative, scoped |
| Dedicated branch | `git branch -r` checked for `froude` | None. Strouhal and wing-loading each have a `*-law-*` branch; froude-efficiency has none | negative, scoped |
| Gate | ran `library/tools/check_laws.py` on an archive of `origin/swarm-architecture:library` | `ok froude-efficiency.yaml … 6 entries, 0 problems` | observation (tool output) |
| Merged? | `git merge-base --is-ancestor aebc0736 origin/main` | **NOT on main.** `origin/main` has no `library/laws/` directory | observation |

## Adversarial points

1. **Arithmetic, redone independently.** The claim contains no arithmetic. I recomputed the entry's
   worked example from its own formula, η_F = 2/(1 + V_j/U):
   V_j/U = 1.5 gives **0.800**, and V_j/U = 3.0 gives **0.500**. Both numbers are correct, and both
   are *calculated*. The entry labels them `evidence: derived`, which is honest.
   **Defect in the entry, which is my finding and not the author's:** the note under the example says
   "Doubling the excess jet speed costs 30 efficiency points … and it is exact." The excess jet speed
   is V_j − U. Going from 1.5U to 3.0U raises the excess from 0.5U to 2.0U, so it **quadruples** the
   excess. What doubles is the jet-speed ratio V_j/U. Truly doubling the excess (0.5U → 1.0U, so
   V_j/U = 2.0) gives η_F = 0.667. That costs **13.3 points**, not 30. The two efficiency values are
   right but the sentence describing them is wrong, and the word "exact" makes the error easier to
   believe. Corrected note: "Doubling the jet-speed ratio (quadrupling the excess) costs 30 points;
   doubling the excess costs 13."
2. **Proxy.** "Dispatched" stands in for the quantity that matters, which is whether a usable entry is
   in the library that readers see. Measured directly: the entry exists and passes the gate, but only
   on `swarm-architecture`. Anything that reads from `main` cannot see it yet. The claim does not say
   "merged", so this gap does not refute it.
3. **Hidden assumption.** The claim assumes that the task dispatched from this session is the one that
   produced the entry. I relaxed that assumption and tested it. Nothing in git attributes `aebc0736`
   to `session_01QbcBRaWeyX3u1KWMzbVYmN`: it is a batch commit by a bot account, it has no session
   trailer, and the session itself is inaccessible. My inference: the work exists, so the dispatch
   very probably happened and succeeded, but **which** session wrote the entry is unverified. This
   weakens the evidence for the claim. It is not evidence against the claim.
4. **Evidence level.** `unknown` understates the case for "an entry was produced", which is verifiable
   from git. It is about right for "this session dispatched it", which I could not verify. Nothing in
   the claim is overstated.
5. **Counter-examples and regimes,** applied to the entry's content. This is my inference only, and I
   read no sources for it.
   - The formula and its stated breakdowns are standard actuator-disc results: unsteady or pulsed
     jets, no statement about how much thrust is available, and blindness to profile losses. I found
     no error in them.
   - The entry says vortex-ring wakes "can carry MORE impulse per unit energy than the steady theory
     allows". As I remember it, the pulsed-jet literature shows thrust or efficiency gains *relative to
     a steady jet with matched parameters*. That is a weaker statement than beating the
     momentum-theory bound itself. The entry cites no source for this sentence. I did not retrieve
     Krueger & Gharib or any later work on it, so its read-level here is `could-not-access` (not
     attempted). I treat the sentence as an unsupported strengthening and do **not** call it wrong.
   - The entry cites Eloy (2012) eq. 12 for the general definition and records the read-level
     `full-text-preprint`. I did not re-read it, so it is unverified by me and not refuted.

## Sources

- Git history of `kganjam/delphi-frontier`, all remote branches as fetched 2026-11-04. Read level: full-text.
- `library/laws/froude-efficiency.yaml` on `origin/swarm-architecture`. Read level: full-text.
- Source session `session_01QbcBRaWeyX3u1KWMzbVYmN`. Read level: could-not-access.
- Eloy 2012; pulsed-jet literature. Read level: could-not-access (not attempted in this review).

```swarm-challenge
{"claim_id": 46, "outcome": "survived", "reason": "A froude-efficiency entry exists in commit aebc0736 on origin/swarm-architecture and passes check_laws.py, so the dispatched work was completed (not merged to main); git does not attribute it to the source session, and separately the entry's worked-example note wrongly calls a quadrupling of excess jet speed a doubling (true doubling costs 13.3, not 30, efficiency points).", "corrected_value": null}
```
