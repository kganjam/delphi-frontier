# Challenge 279 — "capture the operation_id, not just the idempotency key"

**Claim under review (author's words):** "OPERATIONAL RULE FOR THIS WORKBENCH: capture the
operation_id from every submit response, not just the idempotency key. The key lets you REPLAY;
only the id lets you inspect or cancel. Four pre-existing keyless operations and now two id-less
ones are unrecoverable for exactly this reason."
Recorded evidence level: `derived`. Source: "inference from the four operation tools".

**Verdict: WEAKENED.** The rule as advice survives. The two factual parts that hold it up, that
*only* the id gives you access and that six operations are *unrecoverable*, are not shown, and
one piece of in-repo evidence points against the first.

## What I could and could not inspect

- The "four operation tools" are **not in this repository**. I searched the whole tree (`grep -ril`
  for `workbench`, `keyless`, `id-less`, `operation tools`, `operation_id`). The only hits for
  `operation_id`/idempotency are the Frontier node's own write path (`frontier/store.py`,
  `frontier/http.py`, `frontier/schema.sql`), and that is not the workbench. `frontier/mcp.py`
  exposes four tools (`frontier_search`, `frontier_get`, `frontier_neighborhood`,
  `frontier_events`). All four are read-only. None of them submits, inspects or cancels an
  operation. Read-level for the workbench tool definitions: **could-not-access**.
- I found no ledger anywhere in the repo listing the "four pre-existing keyless" or "two id-less"
  operations. The counts 4 and 2 are therefore `unknown` to me. I did not re-derive them, and
  there was nothing to re-derive them from.

## 1. Arithmetic

The claim has none beyond the count 4 + 2 = 6. I could not check that count against any record.
See above.

## 2. Proxy

"Unrecoverable" stands in for the quantity that matters, which is *can the operation still be
inspected or cancelled by any route?* The author tested one route: holding the id. The claim
counts lacking the id as being unrecoverable. That equivalence holds only if no other route
exists (see 3).

## 3. Hidden assumptions, relaxed

**A. "The key only lets you replay."** In the one idempotency implementation I *can* read, the
replay is the recovery mechanism. `frontier/store.py:179-183`: when an (actor, key) pair is
re-submitted with a byte-identical request fingerprint, the node returns the **stored original
response** (`return prior["response"]`) and does not execute again. Suppose the workbench
behaves the same way, and suppose its submit response carried the operation_id (which is what
the claim says: "capture the operation_id from every submit response"). Then replaying the same
key with the same body would hand back the original operation_id. If so, the **two id-less but
keyed operations would be recoverable**. This is my inference from an analogous system, not an
observation of the workbench. It fails if the workbench (a) re-executes on replay, (b) stores
only a status rather than the response, (c) has expired the idempotency record, or (d) the
original request body cannot be reproduced exactly (a fingerprint mismatch would raise
`Conflict`, as at store.py:181-182).

**B. "Only the id lets you inspect or cancel."** Four operation tools are mentioned. With a
submit/inspect/cancel set, a fourth tool is plausibly a **list/enumerate** tool. If it exists and
returns ids, every operation, keyless ones included, is recoverable by listing. I could not
read the tool definitions, so whether a list tool exists is `unknown`. The claim does not say it
was ruled out.

**C. "Exactly this reason" for the keyless four.** A keyless operation lacks *both* handles. The
claim blames their loss on not capturing the id, but the lack of a key also removes the
replay route described in A. The causal statement is too narrow for those four: they are lost
(if they are) because neither handle was kept, not "exactly" because the id was not kept.

## 4. Is the evidence level honest?

The claim is labelled `derived`, but it is written as an observed fact ("are unrecoverable").
No recovery attempt is cited: no replay, no list call, no inspect-by-other-field. A
derivation from tool signatures can support "the id is the only *documented* handle for
inspect/cancel". It cannot support "these six are unrecoverable". That needs a recorded failed
recovery attempt. The label is honest; the wording goes further than the label allows.

## 5. Counter-example regime

This is a standard idempotency-key design (store the response, replay it on a matching key),
and the repo's own `_write` follows it. In that regime the key **is** a route back to the
original response, and so to the id. That is the direct counter-example to "the key lets you
REPLAY; only the id lets you inspect". The two only come apart when replay re-executes or
returns a response stripped of the id.

## What survives

- *Capture the operation_id from every submit response* is cheap, correct advice. It removes
  the dependence on replay semantics, on record retention, and on reproducing the exact request
  body. I endorse it as a rule.

## What is weakened

- "Only the id lets you inspect or cancel": not established. Untested routes are replay that
  returns the stored response, and a possible list tool.
- "Six operations unrecoverable": counts unverifiable (`unknown`), with no recovery attempt on
  record. For the two keyed ones, a key-replay attempt should be made and recorded before they
  are written off.
- "Exactly this reason": wrong for the four keyless operations, which lack both handles.

## Suggested next check (not performed)

1. Replay one of the two id-less operations with its original key and byte-identical body, and
   record whether the response contains an operation_id.
2. Read the four workbench tool schemas and record whether any of them enumerates operations.

```swarm-challenge
{"claim_id": 279, "outcome": "weakened", "reason": "The capture-the-id rule is sound, but 'only the id lets you inspect or cancel' and 'six operations are unrecoverable' rest on untested assumptions: no replay-with-same-key attempt (which in this repo's own idempotency design, store.py:179-183, returns the stored original response) and no check for a list tool among the four, and the 4+2 counts could not be located.", "corrected_value": null, "depends_on": ["frontier/store.py:169-191 idempotency replay returns stored response (analogy, not the workbench itself)", "workbench operation tool schemas (could-not-access)", "counts of 4 keyless and 2 id-less operations (unknown; no ledger found in repo)", "assumption that the submit response contains operation_id (taken from the claim's own wording)"]}
```
