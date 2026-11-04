# Challenge 47 — "LAWENTRY lighthill-ebt dispatched"

**Claim under review (author's words):** "LAWENTRY lighthill-ebt dispatched"
**Recorded evidence level:** unknown · **value:** n/a · **source:** session_016kCs8GMYZbrJQorbymkDYb

## What the claim actually asserts

This is a **process/logistics assertion**: a work item ("law entry" for what the
name suggests is Lighthill's elongated-body theory, EBT, of fish swimming) was
*sent out* to a worker. My reading of the name as Lighthill EBT is **an
inference from the slug, not something the claim states**. The claim states no
result, no number, no equation and no scientific conclusion about Lighthill EBT.

## The five checks

1. **Arithmetic.** There is none. No stated inputs exist to recompute.
2. **Proxy.** The risk is that "dispatched" gets read downstream as "entered",
   "verified" or "holds for fish". Dispatch is a proxy for nothing scientific.
   The quantity that would matter (e.g. whether EBT thrust/efficiency
   predictions match measured fish kinematics) is **not addressed** by this claim.
3. **Hidden assumption.** That a dispatch implies a completed or correct
   deliverable. Relaxed: in this repo nothing has come back yet (see searches below).
4. **Evidence level.** "unknown" is honest, because the source session could not be
   inspected. If the status were upgraded, the most it could be is
   *listing* (a branch exists), never *measured* or *derived*.
5. **Counter-example / regime.** None applies to a dispatch event. (Known limits
   of EBT itself, such as small-amplitude and slender-body assumptions, fail for
   non-slender or high-amplitude swimmers. These belong to the *eventual* law
   entry and are **not** tested here.)

## What I checked (scope of every negative)

| Check | Read-level | Result |
|---|---|---|
| `get_session session_016kCs8GMYZbrJQorbymkDYb` | could-not-access | "requested resource was not found" |
| `grep -ri lighthill`, `lawentry`, `ebt` over working tree of `kganjam/delphi-frontier` (excl. `.git`) | full-text (local) | 0 hits |
| `git log --all -S lighthill`, and commit subjects matching light/lawentry/ebt/dispatch | listing | 0 hits |
| `docs/` directory before this file | listing | did not exist |
| Remote branch `origin/claude/lawentry-lighthill-ebt-chmlhj` | listing | **exists**, tip `3272d3e` (2026-10-31), **identical** to `origin/work/frontier-foundation`, so it holds no Lighthill content |

## Verdict

**SURVIVED (narrowly, as a logistics claim only).** A branch whose name matches the
dispatched task exists on the remote. That is consistent with a dispatch having
happened, and I found nothing that contradicts it. I could not confirm it from the
source session, which was not found. The claim survives because it asserts almost
nothing. It must **not** be cited as evidence that a Lighthill-EBT law entry exists,
was verified, or applies to any fish taxon. As of this review, no such entry exists
in the repo (scope: the full working tree and all git history of `kganjam/delphi-frontier`).

```swarm-challenge
{"claim_id": 47, "outcome": "survived", "reason": "A pure dispatch/logistics assertion with no number or scientific content; a matching branch exists and nothing contradicts it, but it carries no evidence about Lighthill EBT itself and the source session was not accessible.", "corrected_value": null}
```
