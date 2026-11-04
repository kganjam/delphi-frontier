# Allocating agentic attention is an experiment, not a setting

*How the swarm decides where to spend effort — and how it finds out whether that decision was any good.*

---

## 1. The mistake this document exists to avoid

ScienceClaw ships a deterministic **pressure score** for plannerless coordination
([B5](../sources/BIBLIOGRAPHY.md#b5-morphoswarmdocsprior-artscienceclaw-infinitemd), verbatim from
`artifacts/pressure.py:194`):

```python
pressure = 2.0*novelty + 1.0*centrality + 0.5*depth + 0.2*age_term
```

It is a good design. It is deterministic, auditable, has no LLM in the loop, and its `age_term`
exists specifically to prevent starvation — a failure mode that is easy to miss until a frontier
goes silent.

**But adopting it because it is published would be the same error this project forbids everywhere
else: accepting a claim at the level of "someone credible asserts it".** Nobody has shown those four
coefficients are right for *our* problem, and the paper reporting the system gives qualitative
outcomes only, with no quantitative metrics or benchmark numbers ([B1](../sources/BIBLIOGRAPHY.md)).
The weights `2.0 / 1.0 / 0.5 / 0.2` are a reasonable prior, not a result.

So: **allocation policy is a treatment under test, not a configuration value.**

---

## 2. Policies are versioned artifacts

Every policy is a row in `allocation_policy` with an id, a frozen specification, and a rationale. A
policy is a pure function from the current blackboard state to a ranked list of work items, so it can
be replayed against a recorded state and audited.

The arms currently specified:

| Policy | Specification | Why it is in the experiment |
|---|---|---|
| **`random`** | Uniform over ready subproblems | **The control.** Without it, no claim about any other policy means anything |
| **`round-robin`** | Cycle frontiers evenly | The naive baseline most systems actually use |
| **`pressure-sc`** | ScienceClaw's formula, coefficients unchanged | The published prior art, tested rather than assumed |
| **`voi`** | `decisiveness × uncertainty × unblocking / cost` | Our proposal: spend where the top-level answer moves most |
| **`pressure-voi`** | Pressure plus a decisiveness term | The semantic merge of the two, which is the point of running both |
| **`thompson`** | Bandit over frontiers on realised information gain | Learns the allocation instead of specifying it |

`random` is not a joke arm. It is the only thing that converts "our policy produced results" into
"our policy produced more results than not having one". A great many allocation heuristics beat
nothing and lose to uniform sampling, and that is only ever discovered by running uniform sampling.

---

## 3. Open-research methodology, applied to ourselves

The system is doing science; its own operation should meet the standard it applies to its subject
matter. Concretely:

### 3.1 Pre-registration

Before an allocation experiment runs, an `experiment` row is frozen containing: the hypothesis, the
arms, the primary metric, the secondary metrics, the stopping rule, and the minimum effect size worth
acting on. `frozen_at` is recorded. **Analysis decisions made after seeing results are a different
kind of claim** and are recorded as exploratory, never promoted into the primary result.

This is the same principle as the frozen rubric in [the design loop](the-design-loop.md): the
defence is not against dishonesty, it is against the ordinary human and model tendency to find the
analysis that agrees with you.

### 3.2 A primary metric chosen to resist Goodhart

The obvious metric — *subproblems answered per dollar* — is a trap. Optimising it produces many
cheap, trivial answers. The primary metric is instead:

> **Decisiveness-weighted claims surviving adversarial challenge, per dollar.**

Three defences are built into that sentence:

1. **Surviving adversarial challenge**, so an unchallenged assertion scores nothing.
2. **Decisiveness-weighted**, so resolving a question that changes no decision scores near zero.
3. **The challenger and the decisiveness judge are held out** from the allocator — the thing being
   optimised against cannot be visible to the optimiser.

Secondary metrics, recorded but not optimised: wall-clock to first decisive result, frontier
starvation (max time any frontier went unserved), cost per surviving claim, and the rate at which
claims are later *retracted* — which is the one that catches a policy producing confident rubbish.

### 3.3 Everything tried is documented, including what failed

A `policy_trial` row is written for every arm that runs, whether or not it worked, whether or not the
experiment completed, and whether or not the result was embarrassing. The negative-results registry
is not a courtesy; a system that records only its successful configurations will re-try the failures
forever, and will overstate its own competence in exactly the way this project exists to avoid.

### 3.4 Replication before belief

A policy that wins once has won once. Promotion to default requires the result to hold on a second,
independently-seeded run, on a different frontier mix. Single-run superiority is recorded as a lead.

### 3.5 Blinding where it is cheap

The adversarial challenger is not told which policy produced the claim it is attacking. This costs
nothing and removes a bias that would otherwise be invisible.

---

## 4. What makes this measurable at all

An allocation experiment needs the outcome of a choice to be attributable to the choice. That
requires three things the schema now provides:

- **`subproblem_dep`** makes *unblocking* a graph query rather than an opinion.
- **`challenge.outcome`** makes *survival* an observed event with a date.
- **`agent_session.cost_usd`** makes the denominator real money rather than an estimate.

Where a factor cannot be measured it is recorded as unmeasured rather than estimated. Two of the four
VOI factors are currently judgements: `decisiveness` and `uncertainty` are assigned by an agent, not
derived. That is a known weakness of the `voi` arm and is written into the experiment's own
limitations, because a policy whose inputs are opinions can win by having agreeable opinions.

---

## 5. Honest status

**Nothing in this document has been run.** No allocation experiment has executed, no policy has been
compared to the `random` control, and no metric has been collected. The current live behaviour is
simple dependency-gated readiness with round-robin over accounts — which is approximately the
`round-robin` arm, chosen for being obvious rather than for being good.

The first experiment to run should be the cheapest meaningful one: `round-robin` versus `voi` on the
fish frontier, with `random` as control, primary metric as in §3.2, pre-registered before the first
dispatch. Until that has run twice, any statement that this system allocates attention *well* is
unsupported, and should be written as what it is — a design intention.

---

## 6. What this does not establish

- The six policies are specified; only two have ever executed, neither as a controlled arm.
- The primary metric is argued for, not validated. It may have Goodhart paths nobody has spotted;
  the retraction-rate secondary metric exists to catch some of them, and will not catch all.
- `decisiveness` and `uncertainty` are agent judgements (§4), which weakens the `voi` arm in a way
  that cannot be fixed by running it more.
- The ScienceClaw coefficients are reproduced faithfully but have not been re-derived; whether they
  were tuned, chosen, or inherited is not something the source states.
