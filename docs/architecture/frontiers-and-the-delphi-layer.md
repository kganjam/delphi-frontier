# Frontiers, and the Delphi layer

*Many frontiers at once, and how one project's work becomes another's starting point.*

---

## 1. A frontier is a bottleneck, not a level

The first instinct is to make "frontier" a level in a hierarchy — project frontier, subproblem
frontier, and so on. That is the wrong primitive, because the thing that makes a set of questions
*one frontier* is not a shared parent. It is a **shared binding constraint**: resolve the constraint
and the whole set moves; leave it and no amount of work on the others helps.

So a frontier is a **view**, defined by its bottleneck, and the same question can belong to two.

Four kinds are live right now, and they are genuinely different in character:

| Frontier | Bottleneck | Example from tonight |
|---|---|---|
| **Project** | the top-level design question | Can a zebrafish fly? 19 subproblems, 5 open |
| **Subproblem** | one answered question's weakest input | S6 fell and spawned **S25** (which relaying of Flammang 2013 is right?) and **S26** (can active stiffening close the gap?) |
| **Artifact** | an unresolved value inside a library entry | strouhal.yaml's cruising band has no confidence interval in its source |
| **Method** | whether the system itself works | Does adversarial debate beat independent replication at equal cost? Nobody has run the control |

**The promotion rule, and it fired for real tonight:** a subproblem becomes a frontier when it
spawns two or more children. S6 did exactly that at 00:22. Nothing had to be decided by a human;
the structure followed from the work.

**The method frontier is the one most systems never create**, and it is the one that decides whether
the others are trustworthy. It belongs in the same queue, competing for the same budget, scored the
same way.

---

## 2. Many frontiers, one budget

Frontiers compete. The allocation policy is specified in
[allocation-as-experiment.md](allocation-as-experiment.md) and the essential point here is that
**scoring is global, not per-frontier** — otherwise each frontier gets a fixed share and the whole
mechanism degenerates into round-robin with extra steps.

What this changes in practice: tonight S21 (a literature lookup, one session) outscored every
structural question in the project, because it could have overturned the headline and cost almost
nothing. A per-frontier split would have spent equally on five frontiers and found it hours later.

The one guard against starvation is a floor, not a share: no frontier drops to zero, because a
frontier that goes quiet is sometimes the one that is hard rather than the one that is finished.

---

## 3. The Delphi layer: publishing for reuse

The question is not "how do we store artifacts" — that is §1 of
[the law library](the-law-library.md). It is: **how does a project that does not exist yet find this
work and adapt it without breaking it?**

### 3.1 What gets published, and the bar

Not everything. Publishing is irreversible and a published artifact that is wrong is worse than an
unpublished one that is right, because it travels.

A `claim` is publishable when it is **not superseded**, carries a **resolved citation or a run id**,
and has **survived at least one challenge**. A `part_revision` is publishable when **released**, with
every load-bearing `spec_parameter` at evidence level `measured`, `simulated` or `literature` — never
`assumed`. A `law entry` is publishable when it passes both gates: dimensional balance and citation
resolution.

### 3.2 Discovery is by capability, not by name

A new project does not know our part numbers and should not have to. It knows what it needs: *"I
need something that bears bending load at Reynolds 1e3–1e4"*, or *"I need a way to enlarge a
paired appendage"*.

So the index is over **(scale, function, the law it instantiates, the conditions it holds under)**,
and the query is a *requirement*, not a keyword. The match is a join with range predicates — which is
exactly why the store is relational and not a triple store.

### 3.3 Negative results are the most reusable artifacts, and this is the main argument for the layer

The most valuable thing the fish project can hand another project is not a design. It is:

> *A lepidotrichial fin ray, as a passive cantilever, cannot carry glide lift. Required EI ≈ 6.3e-4
> N·m²; reported ray stiffness ≤3.8e-6. The passive route is closed. The open question is active
> stiffening.*

A project reaching for fin rays as a lightweight structural spar learns in one query that the
obvious route fails, what the number was, and where the live uncertainty sits. That saves an
investigation, which is worth more than any positive result we could hand them — and conventional
publication systematically loses it.

**So the Delphi layer indexes refutations as first-class, equal to findings.** A `claim` with
`evidence = refused`, a `subproblem` with `status = refuted`, a `challenge` with `outcome = refuted`
and a `regime_transition` are all *products*, not failures.

### 3.4 Adaptation preserves provenance, and that is a schema constraint

ASK dimension 5 is the hard requirement: *"Can another project import and use the entity without
severing its provenance, scope conditions, dependencies, or restrictions?"*

An import is a `derivation` edge, not a copy:

```
derivation(
  source_artifact, source_project, source_revision,
  importing_project, adapted_how, what_changed,
  conditions_carried  -- the scope under which the original holds
)
```

**The rule that makes it work: an import carries the `conditions` or it is refused.** A value
separated from the conditions it holds under is not reusable, it is a trap — and it is the specific
failure that destroyed the Strouhal calculation in S24, where a cruising band was applied to a
Reynolds regime it does not cover. That happened *inside one project*, with the conditions one field
away. Across a project boundary, with nobody who remembers, it is the default outcome.

### 3.5 Cross-project propagation is the same mechanism, extended

Here is the part worth building and the reason the pieces already fit: **reuse across projects is
within-project dependency with a boundary crossed.**

`claim_depends` already records what a claim rests on, and a trigger on `claim.superseded_by` walks
those edges to flag every dependent claim and subproblem. A `derivation` edge is the same edge with
a different project on one end. So when the fish project resolves S25 and supersedes one of the two
conflicting Flammang values, **every downstream project that imported the fin-ray stiffness gets
flagged automatically**.

That is the capability the source video states — *"New findings update claims and flag dependent
designs"* — reaching across projects rather than stopping at the project boundary. It needs no new
machinery, only the edge.

---

## 4. What is built, and what is not

| Piece | Status |
|---|---|
| Frontier as a view over open work, with dependency gating | **built** (`subproblem`, `subproblem_dep`, `ready_subproblems()`) |
| Promotion of a subproblem to a frontier on spawning children | **happens, not formalised** — S6 did it; no code recognises it |
| Global rather than per-frontier scoring | **specified, not measured** — six policies, `random` as control, none run |
| Method frontier | **named here, empty** — no method question is in the queue |
| Publication bar (§3.1) | **specified, not enforced** — no checker applies it |
| Capability index (§3.2) | **not built** |
| Negative results as first-class products | **built in the schema** (`refused`, `refuted`, `regime_transition`), **not indexed for discovery** |
| `derivation` edge and conditions-carrying import | **not built** |
| Cross-project propagation | **one edge away** — the walker and trigger exist and are tested |

---

## 5. What this does not establish

- No second project exists. Every claim about cross-project reuse is a design argument, and the
  mechanism has never carried an artifact across a boundary.
- The promotion rule in §1 is stated from a single instance (S6). One case is an example, not a rule.
- §3.3's claim that negative results are the most reusable artifacts is an argument, not a
  measurement; nobody has reused one.
- The publication bar is a judgement about what is safe to publish, and it has not been tested
  against a case where it would wrongly refuse something valuable.
