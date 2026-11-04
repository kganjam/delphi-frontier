# Replication 255: independent re-derivation of "the evidence API is valuable on a NARROW subset"

**Question as given to me (answer removed):** "So the evidence API is valuable on a NARROW subset ..."
Context: "inference from the 39-claim run".

**My value: `unknown`.** I could not derive the size or makeup of the "narrow subset" from primary
sources. The per-claim output of the 39-claim run is not in the repository. The engine that produced
it cannot be reached from this session.

**Comparison: CANNOT TELL.** I found no recorded value to compare against, and I have no value of my own.

## What the derivation would need

The quantity is a fraction: of the claims checked in the 39-claim run, how many got a signal that
means something. That means supports > 0 or refutes > 0 on a claim about the world. The derivation
needs:

1. The list of claim ids in the 39-claim run, with their full statements.
2. The GXL `claims/support` counts (supports / refutes / neutral) returned for each claim.
3. A classification of each claim: about the world, about our own method or search scope, or a hybrid.

The arithmetic would be: n_informative / 39, with a binomial interval. All three inputs are missing.
So the arithmetic cannot be done, and I have not substituted any numbers.

## Inputs, sources, read-levels

| Input | Source | Read-level | What it gives |
|---|---|---|---|
| How the run worked | `swarm/evidence.py` on `origin/swarm-architecture` (commit `699f320d`, unchanged at branch tip `2ef23dc2`) | full-text | It selects live `zebrafish-flight` claims with no existing `gxl-evidence` signal. It excludes scope phrasing (`scoped to\|could not\|we searched\|...`) and concessive phrasing (`despite\|although\|notwithstanding`). It writes each result to the Postgres table `artifact_signal` and prints it to stdout. **Nothing is written to a file in git.** |
| Per-claim counts for the 39-claim run | `artifact_signal` table, Postgres `designswarm` at 127.0.0.1:5436 | could-not-access | This lives on the author's host. There is no DB in this container and no `~/.config/morphoswarm/` credentials. |
| Re-running the engine | `https://paperclip.gxl.ai/api/v1/claims/support` | could-not-access | I sent one unauthenticated POST with the public control claim. The outbound proxy returned `CONNECT tunnel failed, response 403`. There is also no API key in this session. |
| Claim statements | `library/pages/project/claims.md` on `origin/swarm-architecture` | listing | 145 claims, with statements cut off at about 150 characters. The highest row ids are 242 and 243, so the export predates claim 255 and possibly part of the 39-claim run. |
| The only documented GXL run | commit message `699f320d` | full-text | Author's claim: "FIRST RUN: 14 claims, 3 with supporting literature, 8 where refuting evidence outweighed supporting", which the author attributes mostly to the concessive-clause artifact. Also: control claim = 28 supports, and "136 claims the engine can actually judge" after the exclusions. **That run is n = 14, not 39.** |

### Negative-search scope
- I ran `git grep -il paperclip` over the trees of all 667 remote branches of `kganjam/delphi-frontier`
  (fetched 2026-11-04), excluding `site/`. Matches: `frontier/store.py` (a licence note, on 666
  branches), `swarm/evidence.py`, `docs/research/fish/challenge-252.md` and
  `docs/research/fish/challenge-254.md`.
- `git log --all` messages grepped for `gxl|paperclip`: the only run records are in `de44fffd` and
  `699f320d`. Neither describes a 39-claim run.
- I also grepped the `origin/swarm-architecture` tree for `GXL claims/support:`, `literature-support`,
  `external-evidence` and `claims/support`. The only hit outside the script is claim 242's row in
  claims.md, a single-claim result (0 supports), not a run summary.
- Not searched: anything outside this repository (the author's DB, logs and terminal output).

## Arithmetic

None was possible. Every value needed is `unknown`:
- n (claims in the run) = 39, according to the question's own wording. I could not confirm it from
  any record.
- n_informative = unknown
- fraction = unknown / 39

## What I can say, labelled

- **Calculation, from code (not an observation of output):** the selector's regex exclusions mean the
  39 claims had already been filtered to remove scope phrasing. So if most of them still came back
  uninformative, a "narrow subset" reading would be stronger than the run alone shows: the subset
  would be narrow *even after* the obvious non-literature claims were removed. This is my inference
  from `evidence.py`. Whether it holds depends on the per-claim counts I could not read.
- **Author's claim, not verified by me:** on the 14-claim first run, 3/14 (21%) had supporting
  literature. The author says most of the 8 "refuting" results were artifacts. I cannot re-check
  either count.
- **On the same 39-claim run, a different claim:** a separate challenge (challenge 254) reached the
  same access wall. It also found that the 39-claim measurement cannot be reproduced from the repo. I
  read only its summary, sources table and arithmetic sections. That agreement is about access, not
  about the value of claim 255.

## Contamination disclosure

I did not find claim 255's own working anywhere in the repository. Claim 255 is not in the exported
claims table. I did not open `challenge-252.md`, because it might contain the claim-255 framing. I
read the `699f320d` commit message only after concluding that I could not derive a value.

```swarm-replication
{"claim_id": 255, "my_value": "unknown (fraction of the 39 claims with an informative GXL signal; the per-claim counts are only in an inaccessible Postgres table and the API is blocked by the proxy)", "agrees": null,
  "note": "I could not re-derive it: the 39-claim run left no record in git (I searched all 667 branches), the artifact_signal DB is on the author's host, and paperclip.gxl.ai returns 403 through the proxy, so I CANNOT TELL."}
```
