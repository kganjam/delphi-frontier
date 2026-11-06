# Swarm design patterns

*What a team of good scientists and engineers does, written down so a swarm can do it on purpose.*

This is a catalogue, a recommendation of which patterns to adopt first, and a statement of the
resource-routing mechanics that decide where effort goes. It is a companion to
[the design loop](the-design-loop.md), which specifies the single evaluation mechanism all of these
patterns feed.

A note on terminology: one pattern below (**the board**) was requested under the name *moltbook*.
The author's reading of that term is recorded in §2.6; if it meant something else, the pattern is
still worth having under some name.

---

## 1. The organising idea: a blackboard with several frontiers

The classic AI architecture for exactly this problem is the **blackboard**: a shared, structured
workspace that specialists read from and write to opportunistically, with no specialist needing to
know the others exist. It was built for speech understanding (Hearsay-II) and for problems where the
path to a solution is not known in advance — which is this problem.

The `designswarm` database *is* the blackboard. Everything below is a discipline for reading and
writing it.

On top of it sit several **frontiers** running at once. A frontier is a set of open subproblems
sharing a bottleneck:

- the **physics frontier** (can it fly at all)
- the **genetics frontier** (what edits exist)
- the **materials frontier** (will the structure hold)
- the **method frontier** (does the swarm itself work)

Frontiers compete for a finite budget of agent-hours and credit. §3 is how that competition is
resolved, and it is the part most multi-agent systems leave to chance.

---

## 2. The catalogue

### 2.1 Generation

| Pattern | What it is | When it earns its cost |
|---|---|---|
| **Brainstorm** | Divergent generation with criticism *suspended* — quantity first | Early, when the space is unmapped. Criticism during generation is what collapses a search to the obvious. |
| **Quality-diversity (MAP-Elites)** | Keep an archive of the best candidate *in each region* of a behaviour space, not the single best | When a global optimum is likely to be a dead end — which is normal in biology, where the best-scoring design may be unbuildable |
| **Constraint-first synthesis** | Start from the binding constraint and design backwards | When one barrier dominates. For the fish, launch velocity dominates by 10×, so any design not addressing it is decoration |
| **Analogical transfer** | Import a mechanism from another scale, another organism, or another project | Cheap and routinely productive. Exocoetid taxiing is the obvious case |
| **Mutation and recombination** | Perturb or cross existing released parts | Once a parts library exists — it needs stock to work on |

### 2.2 Critique

| Pattern | What it is | Why it is kept separate from generation |
|---|---|---|
| **Adversarial challenge** | An agent whose job is to break a specific claim | *Implemented.* The instruction matters: told to **try**, and to report honestly when the claim survives. An agent rewarded for finding faults manufactures them |
| **Pre-mortem** | "It is a year from now and this failed. Write why." | Elicits objections that direct criticism does not, because it removes the social cost of predicting failure |
| **Steelman then attack** | Strengthen the claim as far as it will go, then attack the strengthened version | Prevents the cheap win of attacking a weak phrasing instead of the idea |
| **Independent replication** | Two agents, same task, no contact, compare afterwards | The cheapest hallucination detector available. Two independent derivations agreeing is evidence; one agent agreeing with itself is not |
| **Red team on the method** | Attack the *process*, not the result — "how would this pipeline produce a confident wrong answer?" | The failure that costs most. Everything else checks outputs |

### 2.3 Deliberation

| Pattern | What it is | Note |
|---|---|---|
| **Structured debate** | Two agents argue opposing positions; a third judges on a frozen rubric | The empirical evidence that debate surfaces truth is **mixed**, including negative results. Adopt it as a *structuring device* with a calibrated judge, not as a truth oracle |
| **Delphi method** | Independent estimates → anonymised feedback → revised estimates, iterated | Designed exactly for quantities nobody can measure directly, which describes most cross-scale junctions. Anonymity is what stops anchoring on the loudest agent |
| **Dialectic** | Thesis, antithesis, explicit synthesis | Forces the synthesis to be *written*, which is where silent contradictions surface |

### 2.4 Aggregation and ranking

| Pattern | Note |
|---|---|
| **Pairwise tournament** | *Implemented.* Bradley-Terry over `comparison`, both orders run, position bias measured |
| **Rubric grading** | *Implemented.* Frozen rubric, calibrated grader |
| **Forecast on claims** | Agents give calibrated probabilities to open questions; Brier-scored once resolved. This scores the *agents*, over time, on something objective |
| **Disagreement preserved** | Not an aggregation but a prohibition: conflicting results stay distinguishable. Averaging two stale copies reads as corroboration |

### 2.5 Coordination

| Pattern | Note |
|---|---|
| **Blackboard** | The organising substrate; see §1 |
| **Priority queue over the frontier** | *Implemented* as dependency-gated readiness; §3 adds the scoring |
| **Contract net** | Tasks are announced, agents bid with a cost and a confidence, the task is awarded. Useful once agents differ enough for bids to mean something |
| **Arena** | Continuous head-to-head competition on a standing task with a leaderboard. Good for *methods* — competing simulators on the same benchmark — rather than for one-off questions |
| **Whiteboard session** | A bounded, shared scratch space for several agents on one problem, with a required written synthesis. The synthesis requirement is the pattern; without it, it is a chat log |

### 2.6 The board

A persistent, append-only space where agents post findings, and others react, cite, extend or dispute
them asynchronously — a feed, not a conversation. The distinguishing property is that **the audience
is not addressed**: a post is written for whoever later needs it, including agents that do not exist
yet.

Why it is worth having separately from the claim tables: a claim is a finished assertion, whereas
most of what a working scientist produces is a *lead* — "this number looks wrong", "this paper might
settle S21". Leads have no home in a claim graph and are lost. A board gives them one, cheaply, with
a timestamp and an author.

The real risk is that it becomes a performance: agents posting to look productive, and other agents
reacting to look engaged. The defence is that a post costs nothing and earns nothing — **the board
confers no status and feeds no ranking**. Anything that matters must graduate into a claim, a
subproblem or a part.

### 2.7 Memory

| Pattern | Note |
|---|---|
| **Claim graph / nanopublications** | Machine-actionable assertions with provenance |
| **Negative-results registry** | Deliberate and load-bearing. The fish project's first real finding is a 109× energy deficit — a negative result, and the most valuable thing produced so far. Systems that record only successes re-run failures forever |
| **Lessons registry** | Failures *of method*, which are otherwise rediscovered every session |

### 2.8 Self-modification

The swarm may propose changes to its own rubrics, patterns, schema and prompts — through the same
design loop, with the artifact under evaluation being a piece of the system. The meta-level uses the
identical machinery, which is the point: no separate privileged path.

**What is not self-modifiable**, and this list is itself not self-modifiable:

1. The honesty floor — evidence levels, read-levels, the prohibition on presenting simulated as
   observed.
2. The requirement that a grader be calibrated before it is trusted.
3. The requirement that a rubric be frozen before scoring.
4. The prohibition on a scorer being a function of anything but the thing scored.

A system that can relax its own standards will, because relaxing them always makes the next number
look better.

---

## 3. Where effort goes: routing

Several frontiers are live and the budget is finite. Effort is allocated by **expected value of
information per unit cost** — not by how interesting a question is, and not round-robin.

A subproblem's priority has four factors:

```
  priority  =  decisiveness  ×  uncertainty  ×  unblocking  /  cost
```

- **Decisiveness** — how much the project's top-level answer moves if this resolves either way. A
  question whose two answers lead to the same decision is worth nothing however interesting it is.
- **Uncertainty** — how unresolved it currently is. A question already answered has no value left.
- **Unblocking** — how many other subproblems become ready when it resolves. This is a graph query
  over `subproblem_dep`, not a judgement.
- **Cost** — agent-hours, credit, and whether it needs a scarce resource such as a GPU grant.

**The worked example.** Subproblem **S21** — the measured peak velocity of an adult zebrafish
fast-start — scores highest in the whole project right now, and it is worth seeing why, because it is
not the most interesting question:

- *Decisiveness:* very high. The headline verdict rests on Ucrit = 0.548 m/s, a **sustained** speed
  used as a proxy because the burst number could not be retrieved. Burst speed in fishes is several
  times Ucrit. The entire 10.4× deficit could move substantially.
- *Uncertainty:* total. It is recorded `unknown`.
- *Unblocking:* S24 (surface taxiing) depends on it.
- *Cost:* one literature session.

A question that could overturn the project's headline, costs one session, and is currently a guess
dressed as a measurement — that is what the routing is for. Interest is not an input.

**Rebalancing.** Frontiers that stop returning information lose budget to those that are returning
it — a bandit allocation over frontiers, not a fixed split. The guard against starvation is a floor:
no frontier drops to zero, because a frontier that goes quiet is sometimes the one that is hard
rather than the one that is finished.

---

## 4. What to adopt first, and why these five

Patterns are cheap to list and expensive to run. In order:

1. **Independent replication** — highest value per unit cost by a wide margin. Two agents, same
   question, no contact. It directly attacks the failure mode that matters most here, which is
   confident fabrication.
2. **Value-of-information routing** (§3) — without it, parallelism just spreads effort evenly over
   questions of wildly different worth. Already partly built.
3. **Negative-results registry** — the project's best finding so far is a negative one. Build the
   place to put it before producing more.
4. **Pre-mortem on the design** — cheap, and it is the pattern most likely to surface the barrier
   nobody has thought of. For the fish, run it before committing to any edit stack.
5. **The board** (§2.6) — leads currently have nowhere to live and are being lost between sessions.

Deliberately **not** first: arenas, contract-net bidding and prediction markets. All three need a
population of agents that differ measurably, and a standing benchmark to differ *on*. Without that,
a leaderboard ranks noise. Revisit once grader calibration data exists.

---

## 5. What this does not establish

- No pattern here has been measured *in this system*. The claims about which are cheap and which are
  valuable are reasoned, and are marked as reasoning rather than as results.
- The priority formula in §3 is a stated policy, not a validated model. Its four factors are not
  independent, and the product form is a choice, not a derivation.
- Debate is included despite mixed empirical support, as a structuring device. If our own use of it
  does not beat independent replication at equal cost, it should be dropped.
- The board has a known failure mode (performance) and only a structural defence (no status, no
  ranking). Whether that defence holds is untested.
