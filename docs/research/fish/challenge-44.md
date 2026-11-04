# Challenge 44: "LAWENTRY turing-conditions dispatched"

**Verdict: SURVIVED.** This is a claim about status, not a physical result. The git record
confirms it: the dispatched session wrote, committed and pushed the entry, and the entry passes the
repo's own gate. It is **not merged** to `main`.

## What the claim is

The author's claim: a task to write the `turing-conditions` law-library entry was dispatched
to session `session_01EeoYQd9xtvcBBXiJ619U8b`. The recorded value is `n/a` and the evidence level is
`unknown`. In `swarm/swarm.py` on `origin/swarm-architecture`, `dispatch()` records the child cloud
session's ID in `agent_session`. So the claim's "source" is the session that was dispatched, and the
claim can only be falsified by the record: did that session exist, and did it produce the entry?

## What I checked (2026-11-04, about 08:05–08:15 UTC)

| Check | Method | Result | Kind |
|---|---|---|---|
| Source session transcript | `get_session` on the source session | **could-not-access**: "requested resource was not found". This is the same failure prior challenges (32–35) hit, so it is probably a visibility limit and not evidence that the session is missing. | — |
| First sweep for the entry (~08:06 UTC) | `git log --all --grep=<session id>`; `git ls-tree` across every remote ref for `library/*turing*` | **No hits** at that time. Scope: the remote refs as fetched at session start. | negative, scoped, later superseded |
| Second sweep (08:11 UTC) | `git fetch origin --prune` | New branch `origin/claude/turing-conditions-law-8d0w38`, commit `343ac428`, dated 2026-11-04 08:09:27 UTC. Its `Claude-Session` trailer names **the same** source session. | observation (git record) |
| Files the commit adds | `git show --stat 343ac428` | `library/laws/turing-conditions.yaml` (+214), `library/pages/turing-conditions.md` (+126), `library/pages/index.md` (+1) | observation |
| Entry passes the repo's gate | ran `library/tools/check_laws.py` in a detached worktree at `343ac428` | `ok turing-conditions.yaml … 3 entries, 0 problems` | observation (tool output) |
| Merged? | `git merge-base --is-ancestor 343ac428 origin/main`; `git branch -r --contains` | **NOT merged**. Only `origin/claude/turing-conditions-law-8d0w38` contains it. | observation |

A note on the first sweep: had I stopped there, I would have reported "no output from the dispatched
session" and refuted the claim. That result would have been wrong. It came from timing (I searched
about 3 minutes before the push), not from the work being absent. I record it so the next reviewer
does not treat an early negative search as a finding.

## Adversarial points

1. **Arithmetic, redone independently.** The claim has no arithmetic. I recomputed every derived
   number in the entry it refers to from the entry's stated inputs, in my own script. These are
   *calculations*, not observations.
   - Toy Jacobian f_u=1e-4, f_v=-1e-4, g_u=2e-4, g_v=-1.5e-4 s⁻¹: tr J = -5.0e-5 s⁻¹ and
     det J = 5.0e-9 s⁻². Both match.
   - d_c: I derived it myself. Condition (4) at equality is the quadratic
     f_u²d² − 2(det J + (−f_v g_u))d + g_v² = 0, using f_u g_v = det J + f_v g_u. Its larger root is
     ((√det J + √(−f_v g_u))/f_u)², which is the entry's formula. Numerically d_c = **4.500**, which matches.
   - D_v threshold = 4.5 × 0.7 = **3.15 µm²/s**, which matches. λ_c at onset = 2π(0.7·3.15/5e-9)^¼ =
     **910.5 µm**. I cross-checked it through k_c² = (D_v f_u + D_u g_v)/(2D_uD_v) and got the same
     910.5 µm. The entry rounds to 911 µm, which is correct.
   - The entry claims d_c > 1 always holds. I proved it: tr J < 0 gives f_u < |g_v|, so
     f_u² < f_u|g_v| = b² − a² < (a+b)². It is correct.
   - Decay lengths √(D/k): 75.7, 178.9, 457.6 and 523.4 µm. Half-lives ln2/k: 94.7–218.0 min. Raw D
     ratios: 3.47–27.0. All match the entry.
   - **One minor overstatement.** The entry says the activator's range is "roughly 3-7 times
     shorter" than the inhibitor's. From its own numbers the extreme pairings give
     457.6/178.9 = **2.56** (Lefty1/Squint) and 523.4/75.7 = **6.91** (Lefty2/Cyclops). So the range is
     2.6–6.9×. The lower bound is rounded up. This concerns the entry's content, not the dispatch claim.
2. **Proxy.** "Dispatched" stands in for what matters: does a usable Turing entry exist in the
   library that `main` readers (the site build, other agents) see? Measured directly: the entry
   exists and passes the gate, but **it is not on `main`**. The claim does not say "merged", so this
   does not refute it. It is the gap a reader is most likely to fill in wrongly.
3. **Hidden assumption.** The claim assumes a dispatched session produced output. I relaxed that
   assumption: dispatch can succeed while the session fails. My first sweep briefly supported the
   relaxed case, and the second sweep refuted it. The assumption holds.
4. **Evidence level.** `unknown` is under-specified but overstates nothing. The correct level is
   "operational record, verified from git". My inference: the bookkeeping should record status claims
   at that level.
5. **Counter-examples and internal consistency.** The repo's own `ledger/README.md` row 3 records a
   Lean counterexample to "Turing needs diffusion ratio ≥ 10": instability at a ratio of 1.1 with
   J=[[1,−1],[1.011,−1.01]]. I applied the entry's d_c formula to that J: det J = 0.001,
   −f_v g_u = 1.011, so d_c = (0.0316 + 1.0055)² = **1.076** (calculated). That is below 1.1, so the
   entry and the ledger agree. The entry also does not claim any large fixed threshold. I found no
   counter-example to the status claim.

I did not re-verify the entry's citations (volumes, pages, DOIs) against the publishers. The
dispatch claim does not depend on them. Each citation carries its own read-level in the entry, and
I have not changed those levels.

## Sources

- Git history of `kganjam/delphi-frontier`, remote refs fetched 2026-11-04 at about 08:05 and 08:11 UTC. Read level: full-text.
- `library/laws/turing-conditions.yaml` and `library/tools/check_laws.py` at `343ac428`. Read level: full-text.
- `swarm/swarm.py` on `origin/swarm-architecture` (the `dispatch()` function). Read level: full-text (grep of the relevant lines).
- `ledger/README.md` on this branch. Read level: full-text (row 3).
- Source session transcript. Read level: could-not-access.

```swarm-challenge
{"claim_id": 44, "outcome": "survived", "reason": "Commit 343ac428 from the same source session adds library/laws/turing-conditions.yaml, which passes check_laws.py and whose derived numbers re-derive independently; the work was dispatched and completed but is not merged to main.", "corrected_value": null}
```
