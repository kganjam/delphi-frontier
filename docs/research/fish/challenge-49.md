# Challenge 49: "LAWENTRY wolff dispatched"

**Verdict: SURVIVED.** This claim reports the status of a piece of work. It is not a physical
result. The git record confirms it, and the record goes further than the claim: the Wolff's-law
entry was dispatched, written, committed and pushed by the same source session, and it passes the
repo's dimension gate. It is **not merged** to `main`.

## What the claim is

The swarm's dispatcher (`swarm/swarm.py` on `origin/swarm-architecture`, read in full) records a
claim each time it starts a cloud session. This claim says a session was started to write the
`wolff` law-library entry. It gives no value ("n/a"), and its evidence level is recorded as
`unknown`. A status claim can only be falsified by the record, so the test is whether the
dispatched work exists and came from the named session.

## What I checked (2026-11-04, about 08:10 UTC)

| Check | Method | Result | Kind |
|---|---|---|---|
| Source session transcript | `get_session` / `list_events` on `session_01Hsfzfu6LNA42PvQDBk5S9N` | **could-not-access**: "requested resource was not found" | — |
| Dispatched work exists | `git fetch`, `git branch -r`, `git log --all` | My first fetch found **no** wolff branch. A second fetch about a minute later found `origin/claude/wolff-law-bone-remodelling-01vcyd`, commit `0112ddf6`, dated 2026-11-04 08:09:16 UTC: "Add Wolff's law entry…" | observation (git record) |
| Same session? | the commit's `Claude-Session` trailer | `session_01Hsfzfu6LNA42PvQDBk5S9N`, an **exact** match. (A session-ID prefix close to this one, `01Hsfzfuf…`, belongs to the wing-loading branch. I compared the full string.) | observation |
| What the commit adds | `git show --stat 0112ddf6` | `library/laws/wolff.yaml` (+248). It adds no `pages/` file, which the Strouhal entry had. | observation |
| Gate | ran `library/tools/check_laws.py` (with `python3 -I`) on a worktree at `0112ddf6` | `ok wolff.yaml … 3 entries, 0 problems` | observation (tool output) |
| Merged? | `git merge-base --is-ancestor 0112ddf6 origin/main`; `git branch -r --contains` | **NOT merged**. Only that one branch contains it. | observation |

Negative-search scope: the "no wolff branch" result from my first fetch covered only the remote refs
as fetched at about 08:09 UTC. A refetch reversed it, so the first result was a timing artefact and
not a finding.

## Adversarial points

1. **Arithmetic, redone independently.** The claim itself contains no arithmetic. I redid the
   numbers in the entry it refers to, without copying the author's working:
   - 0.2066 % = 0.002066 = **2066 µε**, and 0.0192 % = **192 µε**. The ratio is 2066/192 = **10.76**.
     The entry gives 10.8 (and "~11" in `where_it_breaks`), which is consistent. This is a
     calculated value from observed strains (Hillam et al. 2015, n = 1). The entry labels it
     `evidence: derived`, which is correct.
   - Dimensions of the SED rule. B·S/ρ = (M T L⁻⁵)(M L⁻¹ T⁻²)/(M L⁻³) = M L⁻³ T⁻¹. B·k =
     (M T L⁻⁵)(L² T⁻²) = M L⁻³ T⁻¹. Both match dρ/dt. S/ρ = J/kg = L² T⁻², the same as k.
     The equation is dimensionally consistent.
2. **Proxy.** "Dispatched" stands in for the quantity that matters: whether a usable entry is in the
   library. Measured directly: it exists and passes the gate, but it is **not on `main`**, so the
   site build and agents that read `main` do not see it. The claim does not say "merged", so this is
   not a refutation. It is the gap a reader is most likely to fill in wrongly.
   A second point, which is my inference: the gate's `eval_side` (`check_laws.py`, lines 140–148)
   keeps only the **first `+`-separated term** of each side. So for this entry the gate checked
   dρ/dt against B·S/ρ and never looked at B·k. The author says this in `equation_note` ("B*k was
   checked by hand"), and my hand check above agrees. "Passes the gate" is therefore a partial
   check here, and the entry discloses that honestly.
3. **Hidden assumption.** The claim assumes the dispatch produced output. I relaxed that assumption
   (dispatched, then failed or stalled), and my first fetch briefly seemed to support the relaxed
   version. The refetch showed the output exists. The assumption holds.
4. **Evidence level.** `unknown` is under-specified, but nothing is overstated. The right label is
   "operational record, verified from git". My inference: status claims should be recorded at that
   level and not as `unknown`.
5. **Counter-examples and regime.** I found no counter-example to the status claim. One point about
   the entry's *content* is outside this claim's scope, and it is my inference only. The entry sets
   `usability: descriptive` and records no zebrafish fin-ray set point. Its negative search is
   scoped to "the searches listed under sources, Nov 2026". It also cites Weigele & Franz-Odendaal
   (2016) for cellular zebrafish lepidotrichia against earlier acellular reports, and it keeps that
   disagreement instead of resolving it. That is consistent with the honesty floor. I did not
   re-read any of the cited papers (I made no fetches), so for this review every citation in the
   entry has read level `could-not-access`. I report no values from them beyond what the entry states.

## Sources

- Git history of `kganjam/delphi-frontier`, remote branches as fetched 2026-11-04 about 08:10 UTC. Read level: full-text.
- `library/laws/wolff.yaml` and `library/tools/check_laws.py` at commit `0112ddf6`. Read level: full-text.
- `swarm/swarm.py` on `origin/swarm-architecture`. Read level: full-text.
- Source session transcript `session_01Hsfzfu6LNA42PvQDBk5S9N`. Read level: could-not-access.

```swarm-challenge
{"claim_id": 49, "outcome": "survived", "reason": "Commit 0112ddf6 on origin/claude/wolff-law-bone-remodelling-01vcyd, carrying the same source session trailer, adds library/laws/wolff.yaml which passes check_laws.py; the work was dispatched and completed, though it is not merged to main.", "corrected_value": null}
```
