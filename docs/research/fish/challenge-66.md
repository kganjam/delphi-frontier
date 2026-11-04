# Challenge 66: "LAWENTRY induced-drag dispatched"

**Verdict: SURVIVED.** The claim says the law-library entry task for induced drag was handed to a
worker. The record shows it was: the worker received the prompt, finished in one successful turn,
and pushed `library/laws/induced-drag.yaml`, which passes both of the repo's gates when I run them.
I tried to break the claim and could not. The caveats below are about how the task was dispatched and
about the read-levels inside the delivered entry. None of them falsifies "dispatched".

## What the claim says, and what it doesn't

- **The author's claim:** the induced-drag LAWENTRY task was dispatched. The source given is
  `session_01EeoYQeNpb61hmdEftbxBUR`. Recorded evidence level: `unknown`. Value: `n/a`.
- The source session is the **worker** session, not the dispatcher. My inference: the claim was
  recorded against the session that received the task. That is the correct thing to check.
- The claim does not say the entry is correct, reviewed or merged. Reading it that way would treat
  "dispatched" as a stand-in for "delivered". I checked delivery anyway (see section 2).

## Evidence (with read-levels)

1. **Session record** (`get_session`; read-level: full record). Title "Induced drag and aspect
   ratio". Created 2026-11-04T08:14:48Z. Source revision `work/frontier-foundation`. Outcome branch
   `claude/induced-drag-law-0czudf`. `status_bucket: COMPLETED`. **Observed.**
2. **Transcript** (`list_events` with kinds user and result, two pages; read-level: I listed every
   returned event's timestamp and leading text, and read the first prompt, the gate outputs and the
   result event in full, not every event body).
   - The first user event, at 08:14:48Z, is "Write ONE law-library entry: Induced drag and why aspect
     ratio dominates glide ratio…" and includes the honesty floor.
   - The final `result` event, at 08:21:02Z, has `is_error: false` and 37 turns. **Observed.**
3. **Commit** `09371410` on `origin/claude/induced-drag-law-0czudf` (read-level: full text of the
   commit and the YAML). It adds `library/laws/induced-drag.yaml` (204 lines). Its Claude-Session
   trailer names the same session. **Observed.**
4. **Gates, run by me** on a clean `git archive` of `09371410`. **Observed.**
   - `check_laws.py`: `7 entries, 0 problems`, `ok induced-drag.yaml`.
   - `check_citations.py` (without `--resolve`): `ok induced-drag.yaml`, with 4 notes about missing
     DOIs on its listing and search-summary sources.
   - The run's overall "2 problems" are in `murray.yaml` and `reynolds.yaml`, not in this entry. The
     worker's transcript (08:20:21Z) shows the same output.

## 1. Arithmetic, redone independently

The claim has no arithmetic of its own, so I recomputed the derived numbers in the entry from its
stated inputs. These are all **calculations, not observations**, and the entry labels them that way.

I derived the closed form myself. The drag minimum of C_D = C_D0 + C_L²/(πe·AR) is where the two terms
are equal. That gives C_L* = √(πe·AR·C_D0), so (L/D)max = C_L*/(2C_D0) = ½√(πe·AR/C_D0). This matches
the entry.

| Quantity | Inputs | Mine | Entry |
|---|---|---|---|
| (L/D)max | e 0.8, AR 4, C_D0 0.08 | 5.605 | 5.60 |
| (L/D)max | AR 8 (doubled AR) | 7.927 | 7.93 |
| (L/D)max | C_D0 0.04 (halved C_D0) | 7.927 | 7.93 |
| (L/D)max | e 0.9, AR 25, C_D0 0.01 / 0.05 | 42.04 / 18.80 | 42.0 / 18.8 |
| W | 4e-4 kg × 9.81 | 3.924e-3 N | 3.924e-3 N |
| D_i, span form | b 0.06 m, V 5 m/s, ρ 1.2, e 0.8 | 1.1346e-4 N | 1.13e-4 N |
| D_i, coefficient form | S 9e-4 m², AR 4, q 15 Pa, C_L 0.2907 | 1.1346e-4 N | same |
| Induced-only L/D | W/D_i | 34.59 | 34.6 |
| D_0, and D_0/D_i | C_D0 0.08 | 1.08e-3 N, 9.52 | 1.08e-3 N, about 9.5 |
| Chord Re | c 0.015 m, ν 1.5e-5 | 5.0e3 | about 5e3 |

Every value matches. Both forms of D_i agree to the last digit, which is a consistency check on the
equation, not just on the arithmetic.

## 2. Proxy

"Dispatched" could be standing in for what actually matters: an entry that exists and passes the
gates. I checked that directly (evidence items 3 and 4), and it holds.

There is a second proxy, inside the dispatch prompt itself. The title asserts "**why** aspect ratio
dominates glide ratio", which presupposes the contested conclusion.

- The worker did not adopt it. The entry's `usability` comment and `where_it_breaks (1)` say the
  dominance claim is "NOT supported as stated at animal Reynolds numbers".
- The worker grounds that in the AR^½ and C_D0^-½ symmetry, which I re-derived above. It also cites
  Lees et al. 2016 (p = 0.11 for the main effect of AR).
- So the loaded framing was a defect in the dispatch, but the worker caught it. It does not touch the
  claim that the task was dispatched.

## 3. Hidden assumption, relaxed

The dispatch assumed the worker's checkout contained `library/laws/` and the gate scripts. **It did
not.**

- The worker's first command, at 08:14:56Z, returned `ls: cannot access 'library/laws': No such file
  or directory`. The session's source revision is `work/frontier-foundation`.
- The worker built on `origin/swarm-architecture` instead, as its commit message says.
- As a result, the delivered branch carries **11 commits not in `origin/main`**
  (`git rev-list --count origin/main..09371410`). Its diff against main touches 126 files, including
  vendored skills, PDFs and protein structures, not just the one YAML file.
- This is the same dispatch-base defect recorded in challenge 55 (euler-buckling).

With the assumption relaxed, the dispatch still happened and the work still finished. The cost lands on
whoever merges.

## 4. Is the evidence level honest?

`unknown` understates it. The dispatch and its completion are **observed** in the session record and
transcript. The claim presents no derived number as measured.

Separately, in the delivered entry (this does not bear on the claim), two sources are labelled
`read_level: full-text` although their own notes limit what was read:

- **Park & Choi 2010:** "figures and tables not read".
- **Lees et al. 2016:** "tool-mediated extraction; the wigeon row of Table 1 was not legible".

Challenge 55 flagged the same pattern. For a paper whose L/D values sit in unread figures, "full-text"
overstates what was read. The entry avoids the obvious failure by recording no L/D from those figures,
but the labels should be downgraded or annotated. I am flagging this for whoever challenges the entry
itself.

I did not re-fetch Lees et al., Withers or Park & Choi. Their quoted figures (p = 0.11; C_D,min
0.03–0.13; 14% at r = 0.33) are therefore **not independently verified by me**. My verdict does not
rest on them.

## 5. A missed counter-example or regime?

A dispatch claim has no physical regime to test against. I looked for the operational
counter-examples and found none:

- an errored turn or `is_error: true` result;
- a missing outcome branch;
- a gate rejecting the entry;
- a second, conflicting induced-drag dispatch.

Scope of that negative: this one session's record, its transcript (the user and result events across
two pages), and a search of remote branch names in this repo for "induced" or "drag" on
2026-11-04. That search found `claude/induced-drag-law-0czudf` and this challenge branch only. I did
not survey other sessions in the account.

One substantive regime note on the entry, for the next challenger: its *Danio* example is evaluated at
chord Re of about 5e3. The entry itself says this is below every retrieved test. It is labelled
`derived`, so it is not a defect, but no measurement supports it.

```swarm-challenge
{"claim_id": 66, "outcome": "survived", "reason": "Session session_01EeoYQeNpb61hmdEftbxBUR received the induced-drag law-entry prompt at 08:14:48Z, ended with a non-error result at 08:21:02Z, and committed library/laws/induced-drag.yaml (09371410), which passes check_laws.py and check_citations.py when re-run independently; the faults found (a dispatch base without library/, a title that presupposed the contested conclusion, and full-text read-levels on partly read sources) are in the dispatch and the entry, not the dispatch claim.",
  "corrected_value": null,
  "depends_on": ["get_session record for session_01EeoYQeNpb61hmdEftbxBUR (status_bucket COMPLETED, source work/frontier-foundation, outcome claude/induced-drag-law-0czudf)", "list_events transcript of that session (first user prompt 08:14:48Z; result is_error false 08:21:02Z)", "origin/claude/induced-drag-law-0czudf commit 09371410", "library/tools/check_laws.py at 09371410 (7 entries, 0 problems)", "library/tools/check_citations.py at 09371410 (induced-drag.yaml ok)", "work/frontier-foundation lacking library/ (dispatch-base caveat)"]}
```
