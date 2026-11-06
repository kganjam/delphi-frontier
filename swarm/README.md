# Running this swarm on another project

Everything here is project-agnostic through one environment variable. Nothing else needs editing.

```sh
export SWARM_PROJECT=your-project-id      # must exist as a row in `project`
```

Four scripts read it (`swarm.py`, `generate.py`, `harvest.py`, `check_specs.py`); the rest operate
on whatever those produce. If you find a hardcoded `zebrafish-flight` anywhere, that is a bug —
one was found in `harvest.py` on 2026-11-04, where it sat in three SQL inserts and would have
filed a second project's claims under the first **without erroring**.

---

## The loop

```
generate.py N   →  dispatch up to N agents: challenge, replicate, deepen, entail
   (agents work in cloud sessions, committing to claude/* branches)
harvest.py      →  pull their result blocks into the graph
progress.py     →  is anything progressing, and will the credit be spent?
```

`monitor.sh` runs that loop on a deadline. It is the only piece that assumes Claude cloud sessions;
swap `swarm.py`'s `dispatch()` to use a different harness.

## The four generators, and what each is for

| generator | what it does | why |
|---|---|---|
| **challenge** | an adversary attacks each unchallenged claim | an unchallenged assertion is worth little |
| **replicate** | an agent re-derives a number **without seeing the original** | the cheapest hallucination detector available |
| **deepen** | attacks an answered subproblem's weakest input | an answered question is not a finished one |
| **entail** | propagates a claim to neighbouring scales and **checks** what it requires there | the only arm that can refute a claim from below, using a measurement rather than a simulation |

**Depth is capped at 2** on evidence, not intuition: depth 3 produced nothing of value, depth 2
twice reached an assumption buried under an answer.

## The checkers — run these, they find real things

| script | what it answers |
|---|---|
| `check_specs.py` | do the specs' own acceptance criteria hold? Prints **UNCHECKED beside PASS and FAIL** |
| `check_vacuity.py` | which mechanisms have **no rows**, so any rule over them is vacuously true? |
| `check_interval_collapse.py` | which summary ranges are **narrower** than their source's? |

## What this cost us, so you do not pay it again

Four bugs of one shape, all found in a single day, all in `harvest.py`:

- **`depends_on` was parsed by nobody** — 636 entries discarded. Worse, the column is an FK to
  `claim.id` and **0 %** of what agents write is a claim id, because they compose the block before
  the id exists. Resolve subproblem ids through `claim.subproblem_id` instead.
- **`answer_kind` and `answer`** were parsed and written to the *claim*, never to the *subproblem*.
  68 of 81 `answered` rows had no answer text.
- **An entire block type was discarded.** The regex matched four kinds; the dispatch had three
  branches. 134 replication results — including 17 disagreements, two of which were right about
  the project's headline numbers — were counted in the "blocks found" total and dropped.

**The check that would have caught the last one is three lines:** assert every kind the regex
matches has a branch. It is now in the file.

## The failure mode worth internalising

A mechanism that works, operating over an empty set, is **indistinguishable from one that is
correct**. The query succeeds, the count is a number, and `0` is the number a passing check wants.
See [the empty set](../docs/architecture/the-empty-set.md): **11 of 21 mechanisms here hold no rows
at all**, so eleven classes of rule are vacuously true.

Every checker in this directory therefore ships with **a case it must flag**, and says so in its
own output. A checker that has never failed cannot be distinguished from one that cannot fail.
