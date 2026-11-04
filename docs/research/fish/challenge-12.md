# Challenge 12 — adversarial review

**Claim under review (not mine):**
> "PDB70 returns NO structural homolog for `and1` (only the query itself), so there is no template
> to design a stiffer variant against."

- recorded evidence level: `derived`
- recorded value: `1 sequences`
- recorded source: `msa_search_native` vs PDB70

**Verdict: REFUTED** — the second half does not follow from the first, and is false as written.
A template-free structural model of And1 exists and carries a confidently-modelled core.

**Read this caveat with the verdict:** refuting "there is no template" does **not** make the
stiffer-variant design feasible. Section 2 argues the design target is probably *less* reachable
than the author thinks, for reasons the author did not state. I am refuting the author's
*reasoning*, not manufacturing a green light.

---

## 0. Provenance of the claim, and what I could not access

`and1`, `PDB70` and `msa_search_native` appear **nowhere** in this repository
(`grep -rl` over all tracked files, excluding `.git`, 2026-11-04). There is no raw tool log, no
PDB70 version string, and no record of whether the reported count includes the query. So I could
not re-run the author's search; everything below is independent evidence about the same
underlying question.

Scope of every negative search I ran is stated beside it. Blocked endpoints, honestly:

| Resource | Result | Read-level |
|---|---|---|
| UniProtKB REST | reachable | API/JSON |
| AlphaFold DB `/api/prediction/` | reachable | API/JSON |
| AlphaFold DB `/files/*` (per-residue pLDDT, the model MSA) | **HTTP 403, proxy policy denial** | could-not-access |
| `search.rcsb.org` (PDB full-text search) | **HTTP 000, CONNECT rejected 403 by gateway** | could-not-access |
| PDB70 itself | never accessed; not installed here | could-not-access |
| Zhang et al. 2010, *Nature* 09137 | paywall redirect to `idp.nature.com` | could-not-access (full text) |
| Zhang et al. 2010 — PubMed 20574421 | abstract retrieved | abstract |

Because `search.rcsb.org` was unreachable, **I cannot state how many actinodin structures are in
the PDB.** That number is `unknown`. Per repo rule #8 I ran the query in both directions and both
returned HTTP 000 identically — a result that cannot come back empty *or* full is not a
measurement, and I am not reporting one.

Every protein-level number below is **retrieved**, not remembered. The one thing I remembered —
that And1 is a collagen — turned out to be **wrong**, and section 6 shows the control that killed it.

---

## 1. Arithmetic, redone independently

The recorded value is `1 sequences`. There is no arithmetic to reproduce, but there is an
off-by-query hazard that the record does not resolve:

- If the count **includes** the query, then homologs found = 1 − 1 = **0**, and the parenthetical
  "(only the query itself)" is consistent.
- If the pipeline **excludes** the query, then `1` means **one genuine homolog was found**, and the
  claim contradicts its own evidence.

The claim asserts the first reading in prose but ships a value that is ambiguous without the log.
`unknown` which convention `msa_search_native` uses — the log is not in the repo. As recorded, the
evidence is not independently checkable. That is a defect in the record even if the first reading
is the right one.

**Arithmetic I did run,** on AlphaFold DB's own confidence fractions for And1 (fractions retrieved
from the API; the multiplications are mine, not the author's):

```
fractions: veryLow(<50)=0.416  low(50–70)=0.309  confident(70–90)=0.223  veryHigh(>=90)=0.053
sum = 1.001                                    (rounding check passes)

fraction pLDDT >= 70  = 0.223 + 0.053 = 0.276
residues  pLDDT >= 70 = 0.276 x 570   = 157.3  of 570
residues  pLDDT >= 90 = 0.053 x 570   =  30.2
residues  pLDDT <  70 = 0.724 x 570   = 412.7
```

So ~**157 of 570 residues** are modelled at confident-or-better, ~**30** at very high — with **no
PDB70 hit at all**.

---

## 2. The proxy — named, and the right quantity is worse for the author

**Proxy in use:** `count of PDB70 template hits` standing in for `designability of a stiffer And1`.

That is two substitutions stacked:

1. `PDB70 hit count` → `can a structure be obtained`. This substitution is simply false; see §3.
2. `can a structure be obtained` → `can a stiffer variant be designed`. This one is the deeper
   problem, and it cuts **against** feasibility.

The quantity that actually matters is the **mechanical stiffness of the actinotrichia fibril**, a
supramolecular material property of elastoidin. Zhang et al. 2010 (abstract read-level) describe
actinotrichia as "rigid, unmineralized fibrils" made of elastoidin, and state that elastoidin's
components "apart from collagen, are unknown" before naming And1 and And2 as "essential structural
components."

So on the author's own founding source, elastoidin is a **composite**: collagen *plus* actinodins.
Stiffness is a property of that composite. A monomer structure of And1 — PDB70 template or
AlphaFold model or a crystal structure — does not yield a fibril modulus. The honest statement is
that *no single-chain structural resource of any kind*, template or otherwise, licenses a stiffness
design. The author reached a defensible bottom line through an indefensible route, and the route is
what was recorded as evidence.

---

## 3. The hidden assumption, relaxed

**Assumption:** that a design template must be a PDB70 hit — i.e. that PDB70 emptiness implies no
structure is available.

Relaxed, the assumption fails on retrieved data. AlphaFold DB has a model:

| field | value |
|---|---|
| entryId | `AF-E7F5V5-F1` |
| uniprotAccession | `E7F5V5` (`E7F5V5_DANRE`, "Actinodin1 precursor", `and1`, *Danio rerio*, 570 aa, **unreviewed/TrEMBL**) |
| toolUsed | `AlphaFold Monomer v2.0 pipeline` |
| latestVersion | 6 (`allVersions` 1–6) |
| modelCreatedDate | `2025-08-01` |
| globalMetricValue (mean pLDDT) | **57.06** |

Controls on this endpoint, both directions (rule #8): known protein `P00533` → HTTP 200;
impossible accession `E0E0E0` → HTTP 404. The endpoint can come back empty, so the hit is a
measurement.

This model was produced **without any PDB70 template** — that is what template-free prediction is.
So "there is no template to design against" is false: there is a structural model, covering
residues 1–570, with a ~157-residue confident core. Designing on predicted structures is routine
practice, not a workaround.

Second relaxation: **PDB70 cannot answer the homolog question in principle.** The hh-suite
documentation describes PDB70 as profile HMMs for representative sequences **from the PDB**
(search-summary read-level). No actinodin protein structure needs to exist for PDB70 to be empty —
PDB70 contains only solved structures. An empty PDB70 result for a fin-specific fish protein is the
*expected* output and carries almost no information about whether homologs exist. Querying PDB70 for
MSA depth is a category error: MSA depth comes from sequence databases (UniRef/BFD), templates come
from PDB70. A depth-1 MSA from a template database is the correct, uninformative answer. Note that
the AlphaFold entry exposes an `msaUrl` — an MSA *was* built for this protein — though that file is
403-blocked here, so its depth is `unknown`.

---

## 4. Is the evidence level honest?

**No — mislabelled in both directions at once, which is the interesting part.**

- `1 sequences` is a **measured tool output**. Labelling it `derived` understates it.
- "there is **no** structural homolog" is an **inference** from that output, and a weak one, because
  the database searched cannot contain actinodins.
- "so there is **no template**" is a **second** inference, and it is false (§3).

The record collapses a measurement and two inferences into one row at one evidence level. Per repo
rule #6 these are different columns. The defect stands independently of whether `1` is the right
number — and by rule #9, note the direction: this detail *closes* a line of work, so nothing
downstream would have questioned it. A claim that ends an investigation gets as little scrutiny as
one that improves a result.

---

## 5. Regime and published counter-example the author missed

**Counter-example, from the claim's own founding paper** (Zhang et al. 2010, PMID 20574421,
abstract read-level):

> "The presence of actinodin sequences in several teleost fishes and in the elephant shark
> (*Callorhinchus milii*, which occupies a basal phylogenetic position), but not in tetrapods..."

Actinodin homologs are published across teleosts and in a chondrichthyan. And within zebrafish
itself, retrieved from UniProtKB (scope: `organism_id:7955`, gene-name query, 2026-11-04):

| gene | accessions | length | name |
|---|---|---|---|
| `and1` | `E7F5V5` | 570 | Actinodin1 precursor |
| `and2` | `A9JRX1`, `A0ACM8QEN9` | 508 | Actinodin2 precursor |
| `and3` | `Q7SZZ6`, `A0A8M3BCX9` | 295 / 292 | Actinodin3 precursor / isoform X1 |

Controls on this endpoint (rule #8): `collagen AND organism_id:7955` → 782 results (positive);
`zzqqxxnotagene AND organism_id:7955` → 0 results with HTTP 200 (must-fail passes, so the endpoint
can genuinely return empty). Note the free-text term `actinodin` as a *protein name* returned 0 rows
— the hits above came from gene-name queries. Worth recording: a naive name search here *does*
return nothing, which is one plausible way a pipeline reports "no homolog" for a protein that has
two paralogs.

**Regime the author missed:** And1 is proline-rich and compositionally skewed — P 11.8% (67/570),
A 9.8% (56), Y 8.2% (47), L 7.7% (44), D 6.8% (39), S/E 6.7% (38 each), R 6.5% (37) — and 72.4% of
its residues model below pLDDT 70. Profile-HMM search against a structure database is known to be
at its weakest for exactly this class of low-complexity, largely-disordered structural proteins.
An empty result in this regime is uninformative by construction, not evidence of absence.

**Database-vintage scope, which the claim does not state:** PDB70 is frozen. ColabFold replaced it
with PDB100 (built with Foldseek) in June 2023; hh-suite maintainers declined to rebuild PDB70
partly because UniClust30 was also unupdated; ColabFold 1.5.2 defaulted to `pdb70_2203`, i.e. a
March 2022 snapshot (search-summary read-level). A negative against PDB70 is a negative against a
~2022 clustered snapshot of the PDB — roughly three and a half years stale as of today, and
superseded. The AlphaFold model that refutes the claim is dated **2025-08-01**, after that snapshot.
"State the scope of every negative search": the author did not, and the scope is materially narrower
than "no structural homolog exists."

---

## 6. What I tried that FAILED to break the claim

I expected the strongest refutation to be: And1 is a collagen-like Gly-X-Y repeat protein, the PDB
is full of collagen triple-helix peptides, therefore an obvious template exists and imino-acid
content is the classic stiffness lever. **That hypothesis is wrong, and my own test killed it.**

Computed by me from the retrieved E7F5V5 sequence, against human COL1A1 (`P02452`) as a positive
control:

| metric | And1 (E7F5V5) | COL1A1 (P02452, control) |
|---|---|---|
| length | 570 | 1464 |
| Gly content | 31 (5.4%) | 391 (26.7%) |
| Gly-first triplets, best frame | 6.3% (vs 5.4% expected by chance) | — |
| `GPP` motifs | **0** | 47 |
| longest run of Gly-every-3rd | **2 triplets** | **338 triplets** |

The control shows the test works and would have detected a collagen. And1 is not one: no GPP, Gly
not even among its eight most frequent residues, no periodicity above chance. This agrees
independently with the Zhang 2010 abstract, which lists collagen as a *separate* elastoidin
component from the actinodins.

So the "use a collagen template" refutation is dead, and I am recording it as dead rather than
shipping it. It would have been the more impressive-looking finding.

---

## 7. What survives of the original claim

- That PDB70 returns no actinodin structural homolog: **probably true, and I could not reproduce
  it** (no PDB70 access, no RCSB access). I am not disputing it.
- That this implies no template: **false.** `AF-E7F5V5-F1` v6 exists, template-free, global pLDDT
  57.06, ~157/570 residues at pLDDT >= 70.
- That a stiffer-variant design is unsupported: **likely still true**, but for the §2 reason
  (fibril-level composite property, 72.4% of the chain below pLDDT 70), not for the stated reason.
  A low-confidence monomer model is a poor design substrate, and that is the honest objection — it
  is an argument about model quality and about what stiffness *is*, not about template absence.

The useful correction is not "the design is feasible." It is: **this line was closed on evidence
that could not have spoken to the question, and if it is to stay closed it needs the real reason
written down.**

---

## Sources

| Source | Read-level |
|---|---|
| UniProtKB REST, `E7F5V5` / `A9JRX1` / `A0ACM8QEN9` / `Q7SZZ6` / `A0A8M3BCX9` / `P02452`, retrieved 2026-11-04 | API/JSON + FASTA (full sequence) |
| AlphaFold DB API, `https://alphafold.ebi.ac.uk/api/prediction/E7F5V5`, retrieved 2026-11-04 | API/JSON |
| AlphaFold DB `/files/` (per-residue pLDDT, model MSA) | could-not-access (HTTP 403, proxy policy) |
| Zhang et al., "Loss of fish actinotrichia proteins and the fin-to-limb transition", *Nature* 2010, PMID 20574421 | abstract (full text paywalled) |
| hh-suite wiki / ColabFold PDB70→PDB100 migration | search-summary |
| RCSB PDB structure search | could-not-access (CONNECT rejected) |
| PDB70 database itself | could-not-access |

Disagreement preserved: the hh-suite/ColabFold material is a search-summary and the exact PDB70
retirement date is not confirmed by it; the sources agree PDB100 superseded PDB70 in ColabFold in
June 2023 but do not establish that PDB70 was formally withdrawn, and one source notes PDB70 is
still installed on some HPC systems. I have not reconciled that, and it does not change §5's point
that the snapshot is stale.

```swarm-challenge
{"claim_id": 12, "outcome": "refuted", "reason": "PDB70 contains only solved PDB structures so it cannot evidence homolog absence for a fin-specific fish protein, and a template-free AlphaFold model of And1 (AF-E7F5V5-F1 v6, global pLDDT 57.06) exists with ~157/570 residues at pLDDT>=70, so 'no template to design against' is false as written -- though the design remains unsupported for the different reason that fibril stiffness is a composite material property and 72.4% of the chain models below pLDDT 70.",
  "corrected_value": "157 of 570 residues (27.6%) at pLDDT >= 70; global pLDDT 57.06 (AF-E7F5V5-F1 v6); PDB70 homolog hits = 0, not '1 sequence'"}
```
