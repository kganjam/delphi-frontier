# The law library

*A computable store of biological design laws: what holds, for whom, under what conditions, and
— most importantly — where it breaks.*

---

## 1. What a library entry is, and why it is not a fact

The temptation is to store "Kleiber's law: metabolic rate scales as M^(3/4)". That is a slogan, and
it is actively harmful as an engineering input: the 3/4 exponent is **contested**, the competing 2/3
has serious support, and the law's behaviour at the small end is exactly where a 0.4 g animal lives.

A library entry is therefore a **conditional, contested, bounded claim**. Its mandatory fields:

| Field | Why it is mandatory |
|---|---|
| `equation` | Written symbolically, every symbol defined, **with units** |
| `symbols` | Name, dimension and units for each — this is what makes the entry computable |
| `constants` | Value **and confidence interval**. A bare exponent is a slogan |
| `mechanism` | Why it holds: geometric, hydrodynamic, thermodynamic, network-theoretic |
| `domain_of_validity` | Taxa, size range, conditions where it is *measured* to hold |
| **`where_it_breaks`** | The regime, taxon or scale where it demonstrably fails |
| `worked_examples` | Real named organisms with real numbers |
| `contested_by` | Competing formulations, preserved rather than reconciled |
| `usability` | `constraining` (yields a number a design can be checked against) or `descriptive` |
| `sources` | Each with a read-level |

**`where_it_breaks` is the field that makes the library worth building.** Every textbook gives the
law; almost none gives its failure boundary, and the failure boundary is the only part an engineer
actually needs. A design sits where it sits, and the question is never "is this law true?" but "is
this law true *here*?"

**`usability` is the second-most-valuable field.** Murray's law gives you a number: branch radii must
satisfy r₀³ = Σrᵢ³, and a design either does or does not. D'Arcy Thompson's transformations are
beautiful and constrain nothing. A library that does not separate these wastes the reader's time at
best, and licenses hand-waving at worst.

---

## 2. Where things live: the direction-of-truth rule

The question "git or database?" has a bad answer (pick one) and a good answer (**declare the
direction of truth per table, and never let it be ambiguous**). Two writers disagreeing is the
failure mode, and it is prevented by construction rather than by discipline.

Three classes, and every table belongs to exactly one:

### `git-authoritative` — authored knowledge
Law entries, derivations, prose, curated examples, rubrics, specifications.

Stored as YAML + Markdown under `library/laws/<slug>.yaml`. Git gives review, diff, blame, signing,
and survival independent of any running service. These are **written by people and agents through
pull requests**, and the database never writes them back.

### `derived` — the index
Full-text search, vector embeddings, the hypergraph edge table, numeric ranges for queries like
*"laws valid below 1 g"*.

Built one-way, `git → Postgres`, by a build step. **Entirely rebuildable and therefore disposable.**
If the index disagrees with git, the index is wrong, and the fix is a rebuild rather than an
investigation.

### `db-authoritative` — high-volume machine output
Run records, measurements, agent sessions, grades, comparisons, costs.

These arrive thousands at a time from concurrent agents, and putting them through git would be
absurd. They live in Postgres and are **exported to git periodically as a snapshot** for citability
and backup — a one-way projection in the other direction.

**The rule, stated once:** *authored in git, indexed in Postgres, generated in Postgres and snapshot
to git. No table is written from both sides.* A build that would write a `git-authoritative` file
from the database is a bug, not a feature.

---

## 3. Why it is a hypergraph, and how to store one

The statement the library needs to make is:

> Law **L** holds for taxon **T** at scale **S** under conditions **C** with exponent **b ± e**,
> measured by method **M**, according to source **R**.

That is a **7-ary relation**. An RDF triple store cannot express it without reification, and the
standard workarounds — Wikidata-style qualifiers, RDF-star, named graphs — are all ways of admitting
that triples were the wrong primitive for this.

**Decision: an n-ary relational core in Postgres, with projections out to RDF and nanopublications
for interoperability.** We do not build or adopt a triple store.

The reasoning: every query we actually need is a join with numeric range predicates — *"which
constraining laws have a validity range covering 0.4 g and a Reynolds number near 3×10³?"* —
and that is what a relational engine with indexes is for. A triple store makes that query slow and
awkward in exchange for a flexibility we do not need, since our schema is stable and curated. We
emit RDF so others can consume it, not so we can query it.

The **edge table is the hypergraph**: `law_application` carries the law, the taxon, the scale, the
condition set, the measured constant, the method and the source as columns of one row. Adding an
eighth participant is a column, not a redesign.

---

## 4. Units are not metadata, they are the correctness check

Every quantity carries a unit and a dimension vector (M, L, T, Θ, N, I, J). This is the single
cheapest correctness gate available: **an equation whose dimensions do not balance is wrong, and no
amount of expert review catches it as reliably as the check does.**

This is what makes the library *computable* rather than merely stored, and it is the lesson from
Wolfram's `Quantity` model: a number without its unit is not a value. Concretely, every
`spec_parameter` and every law constant is dimension-checked at build time, and a law whose equation
does not balance **fails the build**. Like every other guard in this repository, it ships with a case
it must flag.

A second, nearly-free gate falls out of the same machinery: **a law applied outside its recorded
`domain_of_validity` raises a warning carrying the entry's own `where_it_breaks` text.** A designer
extrapolating Kleiber to a 0.4 g fish should be told, by the system, at the moment they do it. The
existing fish calculator already does a hand-rolled version of this — it flags a mass outside the
0.003–0.53 kg range Fish (1990) measured — which is evidence the pattern is right and should be
general rather than per-page.

---

## 5. The design palette: what the swarm can actually reach

A library of laws is inert without tools to apply them. The honest inventory, as of now:

| Capability | Status | Note |
|---|---|---|
| Literature retrieval | **have** | PubMed/E-utilities, bioRxiv, Consensus. PMC serves a CAPTCHA to agents; E-utilities is the working route |
| Sequence and annotation | **have** | UniProt REST verified working |
| Protein structure prediction | **partial** | Nebius ESMFold/Boltz/Protenix reachable; AlphaFold3 blocked by licence (`af3-params` not granted) |
| Protein design | **reachable, unused** | RFdiffusion, ProteinMPNN, Proteina on the workbench |
| Molecular dynamics | **reachable, unused** | GROMACS is the one model qualified as `isolated-pilot`; AMBER/NAMD/OpenMM/LAMMPS are source-adapter only |
| Variant effect prediction | **blocked** | ESM-2 650M is paused for maintenance upstream |
| **Low-Reynolds CFD** | **MISSING** | The single most important gap. S2 is answered from published polars, not from our own solve |
| **Structural FEA** | **MISSING** | S6 (can a fin ray carry lift?) needs beam/shell analysis |
| **Multibody locomotion** | **MISSING** | No MuJoCo or equivalent for launch and glide dynamics |
| Reaction-diffusion / morphogenesis | **partial** | Coral work has a bespoke solver; nothing general, and none of ScienceClaw's 336 skills covers morphogenesis |
| Dimensional analysis / units | **MISSING** | §4 above; cheap and high value |
| Allometric scaling calculators | **MISSING** | Trivial once the law library exists — it is the library made executable |
| Phylogenetic comparative methods | **MISSING** | Needed to say "this trait evolved N times independently", which is how you tell a constraint from an accident |
| Uncertainty propagation | **MISSING** | We multiply numbers with confidence intervals and report point values |
| Geometry and meshing | **have** | Printable STL pipeline exists from the coral and insect work |

:::{danger} This inventory was wrong, and the way it was wrong matters
**Corrected 2026-11-04, after `morphoswarm-34` checked it against the repository.** The table above
was written from what this session had personally *probed* — the Nebius workbench and our scratch
directories — and presented as the inventory. `origin/main` already carries a large `engineering/`
tree: `fin_mechanics` (an Euler-Bernoulli beam), `cfd3d/vlm.py` (a thin-surface vortex-lattice
method), `aeroelastic`, `coupled_mechanics`, `windtunnel`, `glider`, `launch_glider`, `fish3d`,
`bioelectric` and more. So "almost no mechanical tooling" was false.

This is the same error as reading `list_scientific_models` (26 models) as the workbench's capability
list when `tools/list` returns 69 — **an enumeration whose domain excludes the answer looks exactly
like a finding.** It happened twice in one night, in two different systems, which is why it is
recorded here rather than quietly fixed.

**What is genuinely missing, after checking:** a *viscous* low-Reynolds membrane solver validated
against measured polars — `vlm.py` cannot supply it and says so in its own header, *"Inviscid,
attached flow, small angle of attack; Reynolds-number independent"* — and a units/dimensional
library, which `grep` finds nowhere on `main`.

**And S6 may already be answered.** Whether `fin_mechanics` bounds tip deflection and buckling for a
real ray geometry is now a review question, not a build one.
:::

**The three to build first**, judged by what currently blocks the fish:

1. **Dimensional analysis and units.** Cheapest, and it gates the correctness of everything else.
2. **Low-Reynolds aerodynamics.** The project's headline number rests on published polars for
   *other* geometries. Without our own solver we cannot evaluate a *designed* wing at all — only
   look one up.
3. **Beam/shell FEA for fin rays.** S6 is a make-or-break structural question currently unanswered.

Note what this inventory exposes: the swarm has excellent *molecular* tooling and almost no
*mechanical* tooling, while the fish project is blocked almost entirely on mechanics. That mismatch
was not visible until the palette was written down, which is the argument for writing it down.

---

## 6. Seeding, and the standard for an entry

The library starts with the laws the fish project actually needs, because a library built
speculatively is a library nobody checks. First entries, each of which is already load-bearing:

- **Reynolds number and regime boundaries** — pins S2 and determines attainable CL_max
- **Strouhal number**, with the measured 0.2–0.4 cruising band for swimming and flying animals
- **Wing loading vs mass** scaling, and the measured ceiling on powered flight
- **Elastic vs geometric similarity** (McMahon) — governs whether an enlarged fin ray holds
- **Second moment of area** for a spar — S6's core
- **Murray's law** — the clearest `constraining` example, and a good template
- **Kleiber**, entered *with its controversy intact*, as the worked example of a contested law

An entry is admissible when it has an equation that dimension-balances, at least one measured
constant with an interval, a stated `domain_of_validity`, a non-empty `where_it_breaks`, one worked
example with arithmetic shown, and sources with read-levels. **An entry missing `where_it_breaks` is
rejected by the build**, because that field is the difference between a library and a poster.

---

## 7. What this does not establish

- No entry exists yet. The schema and the standard are specified; the content is being gathered by
  two research sessions now running, and nothing here is validated against real entries.
- The dimension checker is described and not written.
- The claim that a relational core beats a triple store for our queries is reasoned from the query
  shapes we expect, not measured against a triple store we built.
- The capability inventory in §5 reflects what has been probed. Several models are marked
  "reachable, unused", which means a submit path exists and no job has returned results — that is
  weaker than "working".
- Whether agents will actually *consult* the library when designing is an open behavioural question,
  and is more likely to decide the library's value than any schema choice here.
