# SPEC — The artifact graph, against the ASK Activation Test

**Status:** normative. Where this spec and the code disagree, say which is wrong; do not paper over it.

**Source.** Mehmet Fırat, *Active Scientific Knowledge: A Conceptual Model for Machine-Actionable and
Versioned Science*, DOI [10.2139/ssrn.7416579](https://doi.org/10.2139/ssrn.7416579). Read at
**full-text** (local copy in `morphoswarm:papers/10.2139%2Fssrn.7416579/paper.pdf`,
sha256 `cc709a91…`). The reference list and Figure 1's artwork were not read.

---

## 1. Scope

Every artifact this system produces — a claim, a law entry, a predicted structure, a simulation run,
a part revision, a dataset, a Lean proof — is a node in one graph and carries the metadata that makes
the six ASK dimensions answerable **about that node**.

The paper's scoring rule is adopted verbatim as our acceptance bar:

> "Full activation does not require computational execution where execution is methodologically
> inapplicable. It requires **every applicable dimension to be represented and every non-applicable
> dimension to be justified**. Partial activation remains useful, but **missing capacities must
> remain visible**."

That last clause is the whole reason this spec is cheap to satisfy honestly and impossible to fake:
a gap shown as a gap **scores**; a gap filled in to look complete does not.

---

## 2. The six dimensions, and what each REQUIRES of an artifact

The paper names the six capacities three different ways in its own text. **These are the Activation
Test's names**, which are the ones attached to the questions, and they are quoted exactly.

### D1 — Addressability
> *"Can its scientific entities be uniquely identified and semantically interpreted by humans and machines?"*

**REQUIRED on every artifact:** a stable assigned `id`; a `kind` from a closed vocabulary; a
`content_sha256` where the artifact has bytes. Assigned id and content hash are both required and
neither substitutes for the other — a hash cannot express "the same part, revision B", and an
assigned id cannot prove integrity.

**INVALID:** an artifact whose only identity is a file path.

### D2 — Evidential traceability
> *"Can every claim and transformation be traced to supporting **and contradicting** evidence,
> responsible agents, dates, decisions, and versions?"*

**REQUIRED on every claim:** `evidence` from the closed vocabulary (`measured`, `simulated`,
`derived`, `literature`, `assumed`, `refused`, `unknown`); `read_level` on every literature source;
the producing `run_id` or `artifact_id` where one exists; `created_at`; the agent that produced it.

**REQUIRED, and this is the half usually missing:** *contradicting* evidence is first-class. Every
`challenge` row — including `outcome = survived` — is part of the record. A claim with no challenge
is not thereby stronger; it is **untested**, and the graph must be able to say so.

**INVALID:** a number whose evidence level is absent, or a `measured` level on a value nobody measured.

### D3 — Conditional executability
> *"Can repeatable analyses or procedures be rerun under a specified environment with expected
> outputs, **or is non-executability explicitly justified by the method**?"*

**REQUIRED where executable:** `command`, `code_sha`, `params`, `exit_code`, and the environment.
**REQUIRED where not executable:** an explicit `not_executable_because` naming the methodological
reason. A field-observed value and a published measurement are legitimately non-executable; silence
is not.

**INVALID:** a run record with no `code_sha`, or an artifact that is neither executable nor justified.

### D4 — Version responsiveness
> *"Can new evidence alter epistemic status or scope **without overwriting earlier states**?"*

**REQUIRED:** supersession, never mutation. A corrected claim gets a new row and the old row gets
`superseded_by`. A released `part_revision` is immutable. A retracted result moves to `retraction`
with its reason, and is not deleted.

**INVALID:** a `UPDATE` that changes a recorded value in place. Correcting a value by editing it is
the defect this dimension exists to prevent.

### D5 — Context-preserving transferability
> *"Can another project import and use the entity **without severing its provenance, scope
> conditions, dependencies, or restrictions**?"*

**REQUIRED:** every quantity carries its `units` and its `conditions` — a modulus at an unstated
temperature is a number, not a parameter. Every law entry carries `domain_of_validity` and
`where_it_breaks`. Every export carries these with the value, in the same record.

**INVALID:** exporting a value without the conditions under which it holds. This is the dimension
most easily lost at an API boundary, and the one that causes the most downstream damage, because
the receiving project cannot see what it is missing.

### D6 — Contestable federation
> *"Can alternative interpretations, ontologies, and judgments be represented, attributed, exchanged,
> and audited across interoperable nodes?"*

**REQUIRED:** conflicting claims remain distinguishable and attributed; graders and challengers are
**named, never pooled**; disagreement is preserved rather than averaged.

**PARTIAL, and declared as partial:** exchange across *interoperable nodes* — §5.

---

## 3. Conformance of the current implementation

Honest, per dimension. `designswarm` has 27 tables; this is what they actually deliver today.

| Dimension | Status | What exists | What is missing, stated as a gap |
|---|---|---|---|
| **D1 Addressability** | **partial** | `part.id` assigned, `part_revision.content_sha256`, `artifact.sha256`, closed `kind` vocabulary | Ids are not **resolvable** — nothing dereferences them. No semantic type beyond `kind` |
| **D2 Evidential traceability** | **strong** | `claim.evidence` + `read_level` + `run_id` + `artifact_id` + `created_at`; `challenge` carries contradicting evidence incl. `survived`; `check_citations.py` resolves DOIs at doi.org | Agent identity is a free-text string, not a resolvable actor id |
| **D3 Conditional executability** | **partial** *(was weak)* | `run` has `command`, `code_sha`, `params`, `exit_code` — **13 rows now exist, none missing a `code_sha`**, where the table was empty when this row was written. **And `results/compute/` holds 19 committed GPU/CPU run families**, one of which (`evo2zf`) carries full environment capture *and* a shuffled control | **No environment capture *in the graph*** — the one run that has it (`entry.json`: torch build, H100, flash-attn version) is a committed file linked to nothing. **1 of 19** run families has it; 14 have only a `job.log`; at least one failed. ~~Still no `not_executable_because` field~~ — **added 2026-11-04** as `run.not_executable_because`, with §4 item 1's reasoning carried in a column comment. Until then the distinction was carried by the literal string `not_executable` inside free-text `notes`, where a typo would silently convert a documented non-executable run into an undocumented one. **The checker was also blind to it**: rule 3 tested `code_sha is null`, and run 17 holds the empty STRING, so the rule returned 0 violations while a run had neither a sha nor a reason — a gate reporting PASS over a real violation. Fixed with `btrim()`; the must-flag control is run 17 with its reason removed, which the new query returns 1 for and the old one 0. Still only 18 of 295 claims carry a `run_id`, and **environment capture is still absent from the graph** |
| **D4 Version responsiveness** | **strong** | `claim.superseded_by`, immutable `part_revision`, `retraction` table, `regime_transition` for representation change — **and automatic propagation now works** | ~~No automatic propagation~~ — **corrected 2026-11-04**: the `trg_claim_superseded` trigger was always correct; it had been walking a `claim_depends` holding **6 edges across 330 claims**. After a backfill to **236 edges** it fired unprompted, raising 22 flags. **The gap was never the propagation, it was the empty graph** |
| **D5 Context-preserving transferability** | **partial** | `spec_parameter.conditions` + `units` mandatory; `domain_of_validity` and `where_it_breaks` mandatory on law entries and gate-enforced | No export format that carries them. A consumer reading the DB directly can drop `conditions` without noticing |
| **D6 Contestable federation** | **partial** | Challengers and graders named; disagreement preserved; both sides of a supersession readable | **No federation.** One node, no exchange protocol, no cross-node audit |

**Two dimensions are weak and one is honestly absent.** Under the paper's own rule that is a
legitimate partial activation *provided the gaps stay visible* — which is what this table is for.

---

## 4. Required work, derived from §3

1. **`run.environment`** (D3). ~~and `run.not_executable_because`~~ — **the second field was added
   2026-11-04 and this item is half discharged.** The reasoning is kept rather than deleted because it
   is the reusable part: without that field a legitimately non-executable artifact is
   indistinguishable from an undocumented one, and the paper requires the distinction explicitly.
   `run.environment` remains missing, and **1 of 19 committed GPU run families has environment
   capture at all** — in a file linked to nothing.
2. **Dependency propagation** (D4). The source video states the capability directly — *"New findings
   update claims and **flag dependent designs**."* Superseding a claim must mark every claim, part
   revision and subproblem that consumed it as `needs-review`. This is the single highest-value
   missing piece, because without it a refuted input silently keeps supporting its conclusions.
3. **A transfer record** (D5): a serialisation in which a value cannot be separated from its units,
   conditions and scope. See §5.
4. **Resolvable ids** (D1).

---

## 5. Nanopublications: what they give us, and where we must go beyond

Nanopubs are the right **publication and federation** layer for the subset of our graph that is
assertional. They are the wrong **storage model** for the graph as a whole. Both halves matter.

**What a nanopub supplies, and we should use:** a trusty URI that is content-derived and therefore
self-verifying (D1); the assertion/provenance/publication-info split, which is D2's shape already;
cryptographic signing and attribution; immutability with `npx:supersedes`, which is D4 done properly;
and a real federated network with independent servers — the only off-the-shelf answer to D6 we have.

**Where they do not reach, and this is not a criticism of nanopubs but of using them for everything:**

1. **Most of our artifacts are not assertions.** A predicted structure, a 300 KB mmCIF, a mesh, a
   parameter sweep, a Lean proof object, a simulation run. A nanopub can *point at* these; it cannot
   *be* them.
2. **No operating envelope.** D5 needs value + units + conditions + validity domain + failure
   boundary as one inseparable unit. RDF can express it; the nanopub template vocabulary has no
   standard shape for it, so every publisher would invent their own and transferability would be
   lost exactly where it matters.
3. **No executability binding.** D3 wants environment, command and expected output attached to the
   claim. Nothing in the nanopub model carries this.
4. **The supersession chain is key-bound.** `npx:supersedes` only works when signed with the same key
   as the original (recorded in `morphoswarm:docs/decisions/ADR-0005`). An automated swarm whose
   agents come and go cannot rely on one key surviving, and a correction that cannot be signed is a
   correction that cannot be published.
5. **Granularity.** One assertion per nanopub is right for a published finding and wrong for a
   10,000-row parameter sweep.

**The architecture that follows:**

- **Postgres is the working graph.** It holds everything, including the non-assertional artifacts,
  and is where the six dimensions are enforced.
- **Nanopubs are the export surface for claims that clear a bar** — a claim that is not superseded,
  carries a resolved citation or a run id, and has survived at least one challenge. Publishing is
  irreversible, so the bar is a gate, not a default.
- **The gap between them is ours to fill,** and it is an *extension*, not a replacement: an
  `ask-transfer/v1` record that carries value, units, conditions, validity domain, failure boundary,
  evidence level, provenance chain and open challenges as one object. It embeds a nanopub for the
  assertional core when one exists, and it is the thing another project imports. D5 is only
  satisfiable with something of this shape, whether or not we call it this.

**What we must not do:** claim nanopub conformance as ASK conformance. They answer D1, D4 and D6
well, D2 partially, and D3 and D5 not at all.

---

## 6. Acceptance

A record in this graph conforms when:

1. Every artifact has an assigned id, a `kind`, and a content hash where it has bytes.
2. Every claim has an `evidence` level, and a `read_level` on each literature source.
3. Every run has a `code_sha`, **or** a `not_executable_because`.
4. No recorded value is ever changed in place; corrections supersede.
5. Every quantity carries units and conditions.
6. Every challenge outcome is recorded, including `survived`.
7. **Every dimension this record does not satisfy is named in the record**, with the reason.

Rule 7 is the one that makes the other six honest, and it is the paper's own standard rather than
ours: *missing capacities must remain visible*.

---

## 7. What this spec does not establish

- Conformance is specified, **not measured**. No checker enforces §6 yet; `check_citations.py` and
  `check_laws.py` cover parts of D2 and D5 only.
- D6 federation has no implementation and no second node to federate with.
- The `ask-transfer/v1` record in §5 is designed, not built.
- The paper was read at full text by another session in this organisation on 2026-10-29; the
  quotations here are taken from that reading's record, not re-extracted from the PDF.
