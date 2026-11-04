# Challenge 256 — "Nebius concurrency is server-side per key and cannot be raised from the client"

**Verdict: WEAKENED.** The measured part (4 parallel submits, 4 × HTTP 429 `ADMISSION_LIMIT_REACHED`,
`admission: "not-submitted"`) is not disputed. Four other things are folded into the sentence and
were inferred, not measured: the mechanism ("concurrency"), its scope ("per key"), that it "cannot
be raised", and that a 429 "creates NO operation". The result itself, 0 of 4 admitted, argues
*against* the simplest reading of "per-key concurrency limit".

## What I could and could not access

- Raw logs of the concurrency test (request bodies, response headers, timestamps, the state of the
  key just before): **could-not-access**. They are not in this repository. I searched for
  `ADMISSION_LIMIT`, `admission`, `429`, `concurren`, `infer_openfold2` and `nebius` across all
  tracked files on `claude/nebius-concurrency-challenge-gwas4p` and in the commit messages of every
  branch. The only admission record I found is in `results/2026-10-31-kcne1-binding-ddg-STOPPED.md` §6
  (read-level: full-text), and it is a different refusal: HTTP 503 `MODEL_MAINTENANCE` from
  `submit_stab_ddg`.
- The live endpoint `https://89.169.99.188/mcp`: **could-not-access**. From this container a single
  `initialize` POST got no HTTP response (curl code `000`, 15 s timeout, tried 2026-11-04), and I have
  no credentials. **I did not reproduce the test.** Everything below is reasoning from the claim
  as stated, not a new measurement.

## 1. Arithmetic

I checked it myself: 4 submits, 4 refusals, so 0/4 = 0 % admitted. The count is right. Nothing in
the claim is computed beyond that count.

## 2. Proxy problem: the measured outcome does not fit the stated mechanism

The quantity the claim is about is **the number of jobs the server lets this key run at once (k)**.
What was measured is **how many of 4 simultaneous submits were admitted, from an unknown starting
state**.

Suppose a per-key concurrency cap k ≥ 1 and the key has nothing in flight. A burst of 4 should then
admit min(k, 4) ≥ 1 and refuse the rest. **The test got 0.** That leaves three possibilities, and
the test cannot tell them apart:

1. The key already had ≥ k operations in flight, so the cap was already used up. (In the STOPPED
   record, the same team left a 60 s retry probe running against this server. Whether anything was
   in flight at test time is `unknown`.)
2. The limit is not per key. It could be per App, per org, or global admission capacity shared
   with other tenants, and it was full at that moment. "Per key" would then be wrong.
3. Effective k was 0 for this key: no quota, or a quota that had expired.

So "server-side" is well supported. A 429 from the server with a server-generated code is not a
client-side throttle, and I accept that part. **"Per key" is an inference that the data does not
reach.** The control needed is a **single** submit with a verified empty in-flight list
(`list_*operations` or similar), then a burst of k+1.

## 3. Hidden assumptions, relaxed

- **"Cannot be raised from the client."** This is a negative claim, and no attempt was reported to
  look for a request field, header or tool that changes the limit. No quota-increase request was
  reported either. All the test shows is that sending 4 at once does not get 4 admitted. If
  "client" means "this MCP client with no account changes", the claim may well hold, but it was
  **not tested**. If "client" includes the account owner asking the provider for more quota, the
  sentence is unsupported. The error name `ADMISSION_LIMIT_REACHED` suggests a configured limit,
  and configured limits are usually adjustable *by someone*. That last point is my inference, not
  evidence.
- **"A 429 creates NO operation."** The source for this is the server's own `admission:
  "not-submitted"` field. That counts as a measurement of what the server *reports*. It is not an
  independent check that no operation row, artifact reservation or billing record exists. The
  claim does not say an operations listing was checked afterwards. If one was, that should be
  cited. If not, the evidence level for this clause is **server-reported**, not measured. The
  STOPPED record shows `not-submitted` is a generic admission-stage label: it also appears on a 503
  maintenance refusal. That fits "nothing was created", but it is the same self-report again.
- **"Retrying is free."** "No GPU consumed" may follow if the previous clause is right. "Free" goes
  further. Retries may count toward a request-rate limit, and a 429 normally means "slow down".
  Retrying in parallel without backoff while the limit is held can also starve the team's own
  queue position, if there is a queue (`unknown`). No `Retry-After` header was reported.
  **Unmeasured.**
- **"Back-pressure, not an error."** This is a reading of what the response means. It is
  reasonable, but it is a classification, not an observation.

## 4. Is "measured" honest?

**Only for the 0/4 count.** The recorded level "measured" is attached to a sentence that is mostly
derived. Split by clause:

| Clause | Honest level |
|---|---|
| 4/4 returned 429 `ADMISSION_LIMIT_REACHED`, `admission=not-submitted` | measured (by the author; raw logs could-not-access by me) |
| limit is server-side | well-supported inference |
| limit is **per key** | inference, and the 0/4 result does not discriminate it from per-App or global |
| **cannot be raised** from the client | untested |
| 429 creates **no operation** | server-reported, not independently verified (as far as the claim states) |
| retrying is **free** | untested |

Putting a "measured" label on the whole sentence is the defect, even where individual clauses
turn out to be true.

## 5. Missed regime

The burst-of-4 design only tells you something if the starting state is known. The STOPPED record
shows the same team was running background probes against this server in the same period. With
the starting in-flight count unknown, the observation "0 of 4" fits every value of k. As stated,
the test cannot measure k at all.

## Corrected statement

> Four parallel `infer_openfold2_native` submits all returned HTTP 429 `ADMISSION_LIMIT_REACHED`
> with `admission: "not-submitted"` (measured, 0/4 admitted). The limit is enforced server-side.
> Its scope (per key vs per App/org/global), the value of k, whether it can be raised, and whether
> retries are cost-free were not measured. That no operation is created rests on the server's own
> `not-submitted` report.

```swarm-challenge
{"claim_id": 256, "outcome": "weakened", "reason": "The 0-of-4 count is measured, but 'per key', 'cannot be raised', 'no operation' and 'retrying is free' are inferred or server-self-reported, and a 0/4 burst from an unknown in-flight state cannot distinguish a per-key cap from an already-saturated or shared (per-App/global) limit.", "corrected_value": "0 of 4 submits admitted (measured); per-key concurrency limit k = unknown; raisability = untested", "depends_on": ["claim 256 statement as given: 4 parallel infer_openfold2_native submits, 4x HTTP 429 ADMISSION_LIMIT_REACHED, admission=not-submitted", "absence of raw concurrency-test logs and any operations-listing check in this repository (searched all tracked files and commit messages)", "results/2026-10-31-kcne1-binding-ddg-STOPPED.md section 6 (not-submitted label also used on 503 MODEL_MAINTENANCE; concurrent 60 s retry probe running)", "endpoint https://89.169.99.188/mcp unreachable from this container on 2026-11-04 (no reproduction)"]}
```
