# Challenge 55 — "LAWENTRY euler-buckling dispatched"

**Verdict: SURVIVED.** The claim is a fleet status claim: that the law-library entry task for
Euler buckling was handed to a worker. The session record shows that it was handed over, the worker
finished, and the output passes the repo's own checker. I tried to find a fault and did not find one
in the claim. The caveats below are about the dispatch, not the claim.

## What the claim says, and what it doesn't

- Author's claim: the task was *dispatched* to `session_01HsfzfvgK3Y13TvPG5Pbmki`. That's all.
  Evidence level recorded: `unknown`. Value: `n/a`.
- It does **not** say the entry is correct, merged or reviewed. Reading it that way would mean
  treating "dispatched" as a stand-in for "delivered". So I checked both.

## Evidence (read-levels stated)

1. **Session record** (`get_session`, read-level: full record). Title "Euler buckling law",
   created 2026-11-04T08:14:12Z, status bucket `COMPLETED`, outcome branch
   `claude/euler-buckling-law-sajrle`. **Observed.**
2. **Transcript** (`list_events`, user/assistant/result kinds, newest 100 events; read-level: I
   searched the whole saved output by keyword and read the first and last parts in full, not
   every event). The first user event (08:14:12Z) is the "Write ONE law-library entry: Euler
   buckling…" prompt. The final `result` event is `subtype: success`, `terminal_reason:
   completed`. **Observed.**
3. **Branch** `origin/claude/euler-buckling-law-sajrle` (read-level: full-text of the commit).
   Commit `2322e3fe` adds `library/laws/euler-buckling.yaml` (176 lines), with a
   Claude-Session trailer naming this same session. **Observed.**
4. **Build gate.** I ran `library/tools/check_laws.py` on a clean `git archive` of that commit:
   `3 entries, 0 problems`, `ok euler-buckling.yaml`. **Observed (I ran it myself).**

## 1. Arithmetic, redone independently

The claim itself has no arithmetic. I recomputed the entry's derived numbers from its stated inputs.
These are **calculations, not measurements**, as they are in the entry:

| Quantity | Inputs | Mine | Entry |
|---|---|---|---|
| λ_y = π√(E/σ_y) | 200 GPa, 250 MPa | 88.86 | 88.9 |
| AISC 4.71√(E/F_y) | same | 133.22 | 133.2 |
| Johnson C_c = √(2π²E/σ_y) | same | 125.66 | 125.7 |
| bone λ_y | 18 GPa, 190 MPa | 30.58 | 30.6 |
| EC3 χ at λ̄=1, curves a0/b/d | α=0.13/0.34/0.76 | 0.725/0.597/0.467 | same |
| EC3 χ/(1/λ̄²) at λ̄=2, a0/d | | 0.929/0.707 | 0.93/0.71 |
| rod P_cr (d=0.1 mm, L=5 mm, E=10 GPa) | | 0.01938 N, λ=200, 2.47 MPa | same |
| AISC F_e/F_y at transition | | 0.445 | "0.44" |

Every value matches.

## 2. Proxy

"Dispatched" could be standing in for "the entry exists and passes the gate", which is what
matters. I checked that directly (evidence 3–4) and it holds. The proxy and the real target
agree here.

## 3. Hidden assumption, relaxed

The dispatch assumed the worker's checkout held the template (`library/laws/reynolds.yaml`,
`murray.yaml`) and the checker (`library/tools/check_laws.py`). **It didn't.** The worker
started on `work/frontier-foundation`. Its first command failed with `ls: cannot access
'library/laws': No such file or directory` (transcript, 08:14:21Z). The worker found the library
on another branch and built on top of it. As a result, the delivered branch is `work/frontier-foundation`
plus **1,384 commits** (`git rev-list --count`), not just the one-file commit. Someone merging it
will pull in all of that unrelated history.

- This is a defect in how the task was dispatched, not a falsification of "dispatched". With this
  assumption relaxed, the dispatch still happened and the work still completed. It is also why the
  `depends_on` below includes the base branch. My inference, not something the source states: a
  worker that had not gone looking for the library would have produced an entry the gate never
  checked.

## 4. Evidence level

`unknown` understates it. The dispatch and its completion are **observed** in the session record.
No derived number is being presented as measured.

Separate from the claim: inside the entry, Taylor & Dirks 2012 has `read_level: full-text`, but its
own note says it was read "through a fetch tool that returned a model-generated summary… Treat as
between abstract and full-text." By this repo's honesty floor the label should be a lower level.
That is a flaw in the delivered entry, and it doesn't touch the dispatch claim. Flagged for
whoever challenges the entry itself.

## 5. Counter-example / missed regime

There's no physical regime to test against a dispatch claim. I looked for the obvious operational
counter-examples and found none: a failed or errored turn, a missing outcome branch, the gate rejecting
the entry, or a second dispatch overwriting the first. Scope of that negative: only this one
session's record, its newest 100 transcript events, and the one branch. I did not survey other
sessions for duplicate euler-buckling dispatches.

```swarm-challenge
{"claim_id": 55, "outcome": "survived", "reason": "Session session_01HsfzfvgK3Y13TvPG5Pbmki received the euler-buckling law-entry prompt at 08:14:12Z, completed successfully, and committed library/laws/euler-buckling.yaml (2322e3fe), which passes check_laws.py; the only fault found is that the dispatch base lacked the library template, which the worker recovered from.",
  "corrected_value": null,
  "depends_on": ["get_session record for session_01HsfzfvgK3Y13TvPG5Pbmki (status COMPLETED)", "list_events transcript of that session (first user prompt 08:14:12Z, result subtype success)", "origin/claude/euler-buckling-law-sajrle commit 2322e3fe", "library/tools/check_laws.py at 2322e3fe (3 entries, 0 problems)", "work/frontier-foundation lacking library/ (dispatch-base caveat)"]}
```
