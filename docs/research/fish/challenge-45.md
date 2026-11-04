# Challenge 45: "LAWENTRY hagen-poiseuille dispatched"

**Verdict: SURVIVED, with two caveats.** The claim reports the status of a piece of work. It does not
assert a physical result. The git record confirms the claim: the entry was dispatched, written,
committed and pushed. Two facts limit what a reader should infer from it. The entry is **not merged**
to `main`, and on its own branch the library's page-build check **fails**, because the generated
page for this entry was never built. The claim says neither "merged" nor "rendered", so neither fact
refutes it.

## What the claim is

The author (session `session_01HsfzftVGDzjbEGSexpMH4m`) claims that a task to write the
Hagen-Poiseuille law-library entry was dispatched. The claim gives no value ("n/a"), and its
evidence level is recorded as `unknown`. Because the claim is about status, only the record can
falsify it.

## What I checked (2026-11-04)

| Check | Method | Result | Kind |
|---|---|---|---|
| Source session transcript | `list_events` on the source session | **could-not-access**: "the requested resource was not found" | — |
| Dispatched work exists | `git log --all --grep`, `git branch -r --contains` | Commit `256b4645`, "Add Hagen-Poiseuille law entry, with the regimes where the r^-4 term (and Murray's cube) fails", dated 2026-11-04 08:08 UTC, on `origin/claude/hagen-poiseuille-law-xyq0l6` only. Its `Claude-Session` trailer names the **same** source session. | observation (git record) |
| Files the commit adds | `git show --stat` | `library/laws/hagen-poiseuille.yaml` (+170) and **nothing else**. No `library/pages/hagen-poiseuille.md`, and no row in `index.md`. | observation |
| Dimension gate | ran `library/tools/check_laws.py` on a worktree of that branch | `ok hagen-poiseuille.yaml … 3 entries, 0 problems` | observation (tool output) |
| Author's negative-control claim | I replaced `r^4` with `r^3` in the equation and re-ran the gate | Rejected: "'Q' is L^3·T^-1, other side is L^2·T^-1". This matches the commit message. | observation (tool output) |
| Page build | `library/tools/build_pages.py --check` on the same branch | **exit 1**: `{"stale": ['hagen-poiseuille.md', 'index.md']}` | observation (tool output) |
| CI enforcing either gate | looked for `.github/workflows` on the branch | None exist, so nothing would have caught the stale page | negative, scoped to that branch |
| Rendered page anywhere | `git ls-tree library/pages` on every remote branch | No branch contains a `hagen-poiseuille` page | negative, scoped to remote branches as fetched today |
| Merged? | `git merge-base --is-ancestor 256b4645 origin/main` | **NOT merged** | observation |

## Adversarial points

1. **Arithmetic, redone independently.** The claim itself contains no arithmetic. I recomputed every
   derived number in the entry it refers to, from the stated inputs.
   - Q = π(5e-4)⁴·100 / (8·1.002e-3·0.1) = 1.9635e-11 / 8.016e-4 = **2.449e-8 m³/s**. The entry says 2.45e-8. Correct.
   - U = Q/(πr²) = 2.449e-8 / 7.854e-7 = **0.0312 m/s**. With ν = 1.002e-3/998 ≈ 1.004e-6 m²/s (my assumed water density), Re = U·2r/ν = **31.1**. Correct.
   - Entrance length = 0.05·31·1e-3 m = **1.55 mm**. The entry says 1.6 mm. Correct.
   - W = Q·ΔP = **2.45e-6 W**. Correct.
   - 1/0.9⁴ = 1/0.6561 = **1.524**. Correct.
   - Womersley number: ν = 3.5e-3/1060 = 3.302e-6 m²/s and ω = 2π·1.2 = 7.540 rad/s, so α = 0.0125·√(2.284e6) = **18.9**. Correct.
   - Blasius scaling: ΔP ∝ f·(L/D)·U² with f ∝ Re^-1/4, U ∝ Q/r² and Re ∝ Q/r. That gives ΔP ∝ Q^1.75·r^-4.75. Correct.
   - Murray minimisation: d/dr[8μLQ²/(πr⁴) + bπr²L] = −32μLQ²/(πr⁵) + 2bπrL = 0, so Q = (π/4)√(b/μ)·r³. Correct.

   All of these are *calculated*, mostly from inputs the author chose, and the entry labels them
   `evidence: derived`. That label is honest.
2. **Proxy.** "Dispatched" stands in for the quantity that matters, which is whether a usable law
   entry now exists in the library. Measured directly, the answer is partial. The YAML exists and
   passes the dimension gate. It is not on `main`, and its rendered page does not exist on any branch.
   The library's own `index.md` says "Every page is generated from its YAML entry", and the build
   check flags this entry as stale. By comparison, the Strouhal entry (challenge 32) shipped its page
   and its index row in the same commit. My inference: the dispatched task stopped one step short of
   the deliverable the library's design implies.
3. **Hidden assumption.** The claim assumes the dispatched task produced output. I relaxed that
   assumption (dispatched, then failed or abandoned) and tested it against git. The output exists, so
   the assumption holds. A narrower version also holds: the output is the YAML entry alone.
4. **Evidence level.** `unknown` is under-specified, but nothing is overstated. The accurate level is
   "operational record, verified from git and tool output". My inference: status claims should be
   logged at that level rather than as `unknown`.
5. **Counter-examples.** I found none to the status claim. On the entry's content, which is outside
   this claim's scope, I found no numerical error. The entry already records its own soft spots
   (Blasius validity range unchecked, μ_water quoted from memory, Pries 1992 constants unread), so
   flagging them here would add nothing new. I did no literature fetches in this review, so I did
   not independently verify the Sperry et al. (2005) figure of 0.54 ± 0.07 or the Avila et al. (2011)
   figure of 2040 ± 10. Their read level here is `could-not-access`, because I did not try. I leave the
   entry's stated `search-summary` read levels as the author recorded them.

## Sources

- Git history of `kganjam/delphi-frontier`, remote branches as fetched on 2026-11-04. Read level: full-text.
- `library/laws/hagen-poiseuille.yaml`, `library/tools/check_laws.py`, `library/tools/build_pages.py` and `library/pages/index.md` on `origin/claude/hagen-poiseuille-law-xyq0l6`. Read level: full-text.
- `docs/research/fish/challenge-32.md` (format and Strouhal comparison). Read level: full-text.
- Source session transcript. Read level: could-not-access.

```swarm-challenge
{"claim_id": 45, "outcome": "survived", "reason": "Commit 256b4645 from the same source session adds library/laws/hagen-poiseuille.yaml, which passes check_laws.py (and an r^3 mutant is rejected), so the dispatch produced the entry; it is unmerged and its generated page was never built (build_pages.py --check fails on that branch).", "corrected_value": null}
```
