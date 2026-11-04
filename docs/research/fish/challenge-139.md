# Challenge 139 — adversarial review of S13-D

**Claim under review (recorded evidence level: `derived`, value `n/a`), source
`harvest:deepen-s13-fin-ray-xfsos0`:**

> "[S13-D] The regime transition out of the folding representation is correct but its
> recorded justification is not: AlphaFold DB v6 puts 27.6% of Actinodin1 (E7F5V5)
> residues above pLDDT 70 and 26.8% for Actinodin2 (A9JRX1), not 0.0%, so the folding
> representation fails not for lack of confidence but because pLDDT is not a modulus and
> the load-bearing object is an assembly; meanwhile the underlying feasibility negative
> survives a factor-of-two attack on its weakest assumption, since relaxing the
> tip-deflection criterion from 10% to 20% of semi-span still leaves a 123–327x
> flexural-rigidity gap and a 123 GPa material requirement against a ~10–30 GPa
> protein-solid ceiling."
> **KEY:** 26.8–27.6% of residues above pLDDT 70 … replacing the recorded 0.0%.
> **VERDICT:** stands

**My outcome: WEAKENED.** The claim's own verdict word ("stands", for the regime
transition) survives. Its KEY number does not survive as stated: the recorded 0.0% is
not a false AlphaFold number, it is a **different predictor's correct number**, and I
found the run. Separately, the claim attacked the second-weakest assumption in the
feasibility leg; the weakest one breaks the 123 GPa figure by two orders of magnitude.

> **Read-level key, on every source:** `full-text` | `abstract` | `listing` |
> `search-summary` | `could-not-access`.
>
> **Nothing in this file is an observation of an organism.** Every number below is
> either retrieved from a database record (a *prediction* where pLDDT is concerned),
> read out of another document in this repository, or arithmetic I ran myself. Each is
> labelled in the sentence that uses it. My script is
> `docs/research/fish/challenge-139-check.py`; `python3 -I` on it reproduces every
> computed number here.

---

## 1. Arithmetic, redone independently from the stated inputs

I did not reuse the author's script. I re-derived the deflection relation symbolically
first, which turns out to matter for §4.

### 1.1 The pLDDT fractions → residue counts

Retrieved by me 2026-11-04, `https://alphafold.ebi.ac.uk/api/prediction/{acc}`, HTTP
200, **read-level `full-text`** (machine-readable record). These are **predictions, not
measurements**:

| | E7F5V5 (And1) | A9JRX1 (And2) |
|---|---|---|
| residues | 570 | 508 |
| `globalMetricValue` | 57.06 | 55.91 |
| veryLow / low / confident / veryHigh | 0.416 / 0.309 / **0.223** / **0.053** | 0.459 / 0.274 / **0.264** / **0.004** |
| `latestVersion`, `modelCreatedDate` | 6, 2025-08-01 | 6, 2025-08-01 |
| `toolUsed` | AlphaFold Monomer v2.0 pipeline | (same record set) |

The claim sums the *rounded* fractions. I instead solved for the integer residue counts
consistent with 3-dp rounding, which is a stronger control because it must partition the
chain exactly (**my computation**):

- E7F5V5: each bin has a **unique** integer solution — 237, 176, **127**, **30** — and
  they sum to exactly 570. Above pLDDT 70 = **157/570 = 27.54%**.
- A9JRX1: unique solutions 233, 139, **134**, **2**, summing to exactly 508. Above
  pLDDT 70 = **136/508 = 26.77%**.

So the claim's "27.6%" is **0.1 pp high** (27.54%, from summing rounded fractions rather
than counts); "26.8%" is right. A trivial correction, recorded for completeness, and it
moves nothing. The exact-partition result is a genuine control the claim did not run,
and it passes: nothing is missing from the four bins.

Independently corroborated, and I note the agreement rather than claiming it as my own
find: branch `claude/and1-pdb70-challenge-w5uy17`, `docs/research/fish/challenge-69.md`
(**read-level `full-text`**, read by me) reaches the same 157/570 = 127 + 30 by the same
integer route.

Second host, same underlying prediction: PDBe-KB 3D-Beacons
(`www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/E7F5V5.json`, HTTP 200,
**read-level `full-text`**) returns `confidence_avg_local_score: 57.06`,
`confidence_type: pLDDT`, `coverage: 1.0`, provider AlphaFold DB, `created
2025-08-01`. Two endpoints, one prediction — this confirms the record was read
correctly, not that the prediction is correct.

**Must-fail control (mine):** `api/prediction/ZZZZZZ` → HTTP **400** `"Invalid
identifier format"`. The endpoint can refuse, so the 200s are informative.

**One thing I tried and could not do:** I attempted to retrieve an *earlier* AlphaFold DB
version of the E7F5V5 record (`?version=4`, `?version=5`) to test whether the confident
fraction is version-dependent. Both return HTTP 200 but with the **identical v6 payload**
(`latestVersion: 6`, same fractions) — the query parameter is ignored. So "AFDB v6" is
the only AFDB record I can reach; whether an AF2-era v4 record gave different fractions
is **`unknown`**, read-level `could-not-access`. The per-residue array is likewise
unavailable (the author reports 403 on `alphafold.ebi.ac.uk/files/...`; I did not
re-test).

### 1.2 Proline, recomputed

From UniProt FASTAs I fetched myself (`rest.uniprot.org`, HTTP 200, **read-level
`full-text`**), **my computation**: E7F5V5 = 67 P / 570 = **11.75%**; A9JRX1 = 60 P /
508 = **11.81%**. Both round to 11.8%, and glycine is 5.4% and 4.5%. This reproduces the
claim's point that the recorded descriptor does not identify which actinodin was meant.
Corroborated independently at `claude/actinodin-replication-14-fm0uqk`,
`docs/research/fish/replicate-14.md` line 33 (**read-level `full-text`**), which records
67 (11.75%) and 60 (11.81%) from a separate run.

UniProt's own feature table for E7F5V5 (fetched by me, HTTP 200, **read-level
`full-text`**) gives Signal 1–26 and **Disordered 379–400 and 419–570** — i.e. 175 of
570 residues annotated disordered, which is consistent with the 237-residue very-low
band. *That consistency is my inference, not a UniProt statement.*

**Consequence the claim missed:** residues 1–26 are a signal peptide and are cleaved, so
the biologically existing chain is 544 aa. Since I cannot get the per-residue array, the
confident fraction **of the mature chain** is bounded, not pinned: if none of the 157
confident residues lie in the signal peptide, 157/544 = **28.9%**; if all 26 signal
residues are confident, (157−26)/544 = **24.1%**. So the honest mature-chain figure is
**24.1–28.9%**, and the single value 27.6% is a whole-chain number quoted for a chain
that does not exist in the animal. This does not change the direction of anything.

### 1.3 The flexural-rigidity arithmetic

Inputs as stated in the parent document (`claude/s13-protein-fin-ray-e8y8d8`,
`docs/research/fish/S13-protein.md`, **read-level `full-text`**, read by me): m = 0.4 g,
g = 9.81, semi-span b/2 = 0.02 m, cantilever with uniformly distributed load, allowable
tip deflection δ = frac × (b/2).

Rather than copy `δ = w(b/2)⁴/(8EI)`, I reduced it. With w = (W/2)/(b/2) and δ =
frac·(b/2):

**EI_req = W·(b/2)² / (16·frac)**

**My computed values** (all computed, none observed):

| frac | EI_req (N·m²) | vs 4 × 10⁻⁹ | vs 1.5 × 10⁻⁹ | E_req from a 1 GPa baseline |
|---|---|---|---|---|
| 10% | 9.810 × 10⁻⁷ | 245x | 654x | 245 GPa |
| **20%** | **4.905 × 10⁻⁷** | **123x** | **327x** | **123 GPa** |
| 40% | 2.453 × 10⁻⁷ | 61x | 164x | 61 GPa |
| 80% | 1.226 × 10⁻⁷ | 31x | 82x | 31 GPa |

**The claim's 123–327x and 123 GPa reproduce exactly.** No arithmetic fault in either
leg of the claim. The faults are elsewhere.

The closed form also shows something the author's numeric script hides: **EI_req is
completely independent of wing area, lift coefficient, air density and flight speed.**
It depends only on weight, semi-span and the deflection fraction. That *strengthens* the
feasibility negative against most of the parent document's self-declared soft spots —
and it identifies semi-span, which no one has attacked, as the only geometric input that
can move it (§4.1).

---

## 2. The break: the recorded 0.0% is a different predictor, not a false number

This is the claim's KEY assertion and the reason it was filed. It does not hold as
stated.

The claim's own §0 and §2 concede that the provenance of the recorded 0.0% could not be
found: a cross-branch `git grep` "was started and abandoned (it exceeded the 120 s tool
budget and I did not retry it)", and the input's read-level is recorded as
`could-not-access` with "unknown provenance". The claim then nonetheless asserts the
number is "**false as recorded**" and that 26.8–27.6% is "**replacing the recorded
0.0%**".

**I found the run.** Scope of my search, stated beside the finding: I listed the 17
remote branches whose names match `s13|fin-ray|actinodin|elastoidin`, plus the two
matching `boltz2|plddt`, fetched them and grepped `docs/` — four fetches, well inside
budget. Two independent documents carry it:

- `claude/challenge-18-boltz2-plddt-kz0kkp`, `docs/research/fish/challenge-18.md`
  (**read-level `full-text`**, read by me). Its title is the recorded claim itself:
  *"Boltz2 reaches 0.0% >pLDDT 70 on and1/and2 and does worse than OpenFold2 because the
  MSA has depth 1."* Its table records, as that document's reading of a swarm run:
  **and1, Boltz2 + PDB70 MSA, 570 aa, global pLDDT 38.1, 0.0% >70, MSA depth 1**; and
  **and2, 508 aa, global 36.1, 0.0% >70, depth 1**. On the OpenFold2 lane the same table
  gives 4.9% for and1.
- `claude/boltz2-kcnk5b-challenge-jhlceq`, `docs/research/fish/challenge-9.md` lines
  180–181 (**read-level `full-text`**) reports the same table from the same run: and1
  38.1 / 0.0% ≥70, and2 36.1 / 0.0% ≥70.

So the three recorded S13 diagnostics are not stray numbers. **"0.0% of residues above
pLDDT 70" is a Boltz2 result obtained with an MSA of depth 1**, and the recorded "no
PDB70 homolog" is the same run's depth-1 input. They are mutually consistent: a depth-1
alignment is *why* that prediction has no confident residues.

The claim therefore compares two different predictors and reports the difference as a
correction:

| | predictor | MSA | global pLDDT | residues >70 |
|---|---|---|---|---|
| recorded S13 input | Boltz2 | depth 1 | 38.1 (and1), 36.1 (and2) | **0.0%** |
| claim's "replacement" | AlphaFold DB v6, AF Monomer v2.0 | AFDB's own deep MSA | 57.06, 55.91 | **27.5%, 26.8%** |

**This disagreement must be preserved, not resolved by substitution.** Both numbers are
correct for their own pipeline; neither is "false". The claim's §2 says exactly the right
thing — the input is "pipeline- and version-dependent… the same chain scores differently
under AlphaFold2 monomer, AF-Multimer, AF3 and ESMFold" — and then its verdict line does
the one thing that insight forbids, treating one pipeline's number as the other's
correction. *That inference is mine; the quoted caveat is the author's own.*

What survives, restated correctly and, I think, more usefully than the claim's version:
**the recorded gate is real but is an artifact of MSA depth 1, not a property of
actinodin.** Give the same chain a deep MSA and more than a quarter of it is predicted
confidently. That makes the recorded justification *contingent* rather than *false* —
and it is a sharper criticism of the gate, because a gate that flips on an alignment
choice was never load-bearing.

Two further corrections to the claim's framing of the record:

1. `challenge-18.md` already assessed this number and recorded **outcome `weakened`**:
   internally consistent, "**not reproducible from committed artifacts**" (that
   document's §: it searched `operations.jsonl`, `pipeline.py`, `stage2.py` and found
   nothing). So the honest status of the recorded 0.0% was already *unreproducible*, not
   *unknown* and not *false*. The claim re-litigates it without the prior.
2. `challenge-18.md`'s table identifies and2 as **A0ACM8QEN9** (508 aa). The claim's
   comparator for And2 is **A9JRX1** (508 aa). Both are 508-aa Actinodin2 records, but
   they are different accessions, and A0ACM8QEN9 has no AlphaFold model (the claim
   reports HTTP 404; I did not re-test). So for the and2 row the claim's 26.8% is not
   even the AFDB number for the accession the recorded run used — it is the number for a
   sibling record. Noted as a provenance mismatch, not as a numerical fault.

---

## 3. Proxies

The claim is good on the first-order proxy problem and names it correctly: pLDDT is a
confidence estimate standing in for structural knowledge standing in for a mechanical
property no folding model emits. I confirm that and add nothing.

Two proxies it did not name:

**(a) Whole chain for mature chain.** §1.2: the quoted 27.6% is computed over residues
1–570 including a cleaved signal peptide. Right quantity: 24.1–28.9% over the 544-aa
mature chain, unresolvable further without the per-residue array.

**(b) The one that carries the GPa number — a cross-species whole-ray modulus standing
in for zebrafish ray material.** This is §4.2, and it is the bigger of the two.

---

## 4. The hidden assumption that carries the result

The claim nominates the **10%-of-semi-span deflection criterion** as the feasibility
leg's weakest assumption, relaxes it by two, and reports the negative intact. That test
is correctly executed (§1.3 reproduces it). But the criterion is not the weakest
assumption, and relaxing it is not the attack that bites.

### 4.1 Semi-span, which nobody has relaxed

From **EI_req = W·(b/2)²/(16·frac)**, the requirement is quadratic in semi-span and
linear in the deflection fraction. The parent document sets b/2 = 0.02 m = "half body
length" — a 2 cm semi-span on a 4 cm fish, i.e. a wing as long as the animal's half-body,
which the parent itself calls "generous, implies a fin far larger than the real
pectoral". A factor-of-two attack on *that* input is at least as legitimate as one on
the deflection criterion, and it is worth four, not two.

**My computation:** semi-span halved to 0.01 m *and* deflection relaxed to 20% gives
EI_req = 1.226 × 10⁻⁷ N·m², a **31x** gap against 4 × 10⁻⁹ and a **31 GPa**
requirement from the 1 GPa baseline — i.e. two simultaneous factor-of-two relaxations,
both in the direction the parent document's own prose says is more realistic, land the
requirement **at the top edge of the 10–30 GPa protein-solid ceiling** rather than 4x
above it. The claim's "survives a factor-of-two attack, with margin" is true
one-assumption-at-a-time and false for the joint relaxation.

I do not call this a refutation of the feasibility negative: 31 GPa still exceeds every
*measured* protein-solid modulus (the parent's own table gives 3.3 ± 0.4 GPa for an
insulin fibril by AFM, with 10–30 GPa for amyloid being partly **modelling**,
read-level `search-summary` — a disagreement the claim's "~10–30 GPa ceiling" phrasing
flattens by quoting the computational end). It does mean the margin is one more
factor of two, not the comfortable one the claim reports.

### 4.2 The baseline modulus — and here the 123 GPa figure fails

"123 GPa requirement" is `123 × E_baseline`. The entire GPa comparison rests on
`E_baseline ≈ 1 GPa`, a **teleost whole-ray proxy from other species at read-level
`search-summary`** in the parent document — the weakest-evidenced input anywhere in the
chain, and the only one that converts a dimensionless gap into a number comparable with
a protein ceiling.

The parent document's *own measured* inputs disagree with that proxy by two orders of
magnitude. It computes `E_eff = EI / I_eff` from Puri et al. 2018's measured EI
(1.5–4 × 10⁻⁹ N·m²) and I_eff (3–7 × 10⁻¹⁶ m⁴) and gets **2–13 MPa**, then sets it
aside as a "plate modulus… not the ray material's modulus, and I do not use it as one".

**I tested that dismissal, and it does not hold.** Using the parent's own stated ray
geometry (16–18 rays, 0.1–0.2 mm diameter), **my computation** of the rays' summed
second moment, Σ πd⁴/64:

| rays × diameter | Σ I (m⁴) | implied E from EI 1.5–4 × 10⁻⁹ |
|---|---|---|
| 16–18 × 0.10 mm | 7.9–8.8 × 10⁻¹⁷ | 17–51 MPa |
| 16–18 × **0.15 mm** | **4.0–4.5 × 10⁻¹⁶** | **3.4–10.1 MPa** |
| 16–18 × 0.20 mm | 1.3–1.4 × 10⁻¹⁵ | 1.1–3.2 MPa |

At the mid geometry the rays' own summed second moment (4.0–4.5 × 10⁻¹⁶ m⁴) **lands
inside Puri's measured I_eff range of 3–7 × 10⁻¹⁶ m⁴**. *My inference, stated separately
from the parent's claim:* if I_eff is essentially the rays' second moment, then
`EI/I_eff` = 2–13 MPa is not a dilute membrane-plus-rays plate modulus at all — it is
approximately **the ray material's modulus**, and the parent's reason for discarding it
is unsound. My independent geometry route agrees with it (3.4–10.1 MPa at 0.15 mm).

So the baseline is not 1 GPa. Required ray modulus at the claim's own 20% relaxation
(**my computation**):

| baseline E, and its provenance | required E at 123x |
|---|---|
| ~1 GPa, other teleosts, read-level `search-summary` | 123 GPa — **above any protein solid** |
| 10 MPa, the parent's own named alternative | **1.23 GPa** — inside silk (1–10 GPa) |
| 3.4–10.1 MPa, my calc from Puri's measured EI + parent's ray geometry | **0.42–1.24 GPa** — inside silk |

The parent document says this itself, in its "what would settle it" section: if the ray
modulus "is ~10 MPa rather than ~1 GPa… the required post-redesign modulus lands near
3.6 GPa and a protein route becomes live." The claim read that document in full,
reproduced its deflection sensitivity, and did not run the baseline sensitivity that the
document flags as its highest-value open measurement.

**So: "a 123 GPa material requirement against a ~10–30 GPa protein-solid ceiling" is not
a robust statement.** It is robust to a factor of two on the deflection criterion, and it
collapses by a factor of ~100 under the baseline input that the parent document names as
unmeasured in zebrafish and most worth buying. On the measurement-internal baseline the
requirement at 20% deflection is ~0.4–1.2 GPa, which is *inside* the protein range, not
above the ceiling.

**What I am not claiming.** I am not claiming the protein route is feasible. The
dimensionless gap (123–654x in EI) is untouched by any of this and rests on Puri's
*measured* EI; and at the parent's own 10% criterion the measurement-internal baseline
still demands 245 × 3.4–10.1 MPa = **0.8–2.5 GPa**, i.e. a hydrated structural protein
solid stiffer than hydrated collagen fibril (0.2–0.8 GPa) by 1–10x — hard, unproven,
but not off the chart. The honest status of the feasibility negative is **"gap robust,
GPa framing not"**, and the deciding quantity is a mechanical measurement nobody has:
hydrated nanoindentation on isolated adult zebrafish lepidotrichia. That is also, I note,
an argument *for* the regime transition the claim upholds.

---

## 5. Is the evidence level honest?

**Mostly yes, and better than most.** The claim is recorded `derived`, and that is the
right word: the pLDDT fractions are retrieved database fields describing someone else's
prediction, and the fractions-to-percent step is the author's arithmetic. The document
repeatedly and correctly refuses to call pLDDT a measurement, labels the sensitivity
table "all computed, not observed", and records its own blocked services and abandoned
searches. The honesty floor is not breached: I found no invented number, accession or
citation, and every number I could re-derive, re-derived.

Three defects at this level, in descending order:

1. **An input recorded `could-not-access` / "unknown provenance" is nonetheless called
   "false as recorded" and "numerically false", and its replacement is asserted.** A
   number whose source you have not read cannot be declared false; it can only be
   declared inconsistent with a number you *did* read, which is what §2 shows it to
   be. The abandoned search was the load-bearing step, and it was recoverable in four
   fetches.
2. **"27.6%"** is a sum of rounded fractions; the exact count-based value is **27.54%**
   (§1.1). Small, but the claim presents it as the KEY number.
3. **"~10–30 GPa protein-solid ceiling"** quotes the computational end of a range whose
   measured end, in the parent's own table, is 3.3 ± 0.4 GPa. Preserving that
   disagreement makes the negative *stronger*, so the flattening is not
   self-serving — but it is a flattening.

---

## 6. Regime, taxon or counter-example missed

- **The predictor regime (§2).** The recorded 0.0% and the claimed 27.5% are the same
  chain in two prediction regimes separated by MSA depth. `challenge-18.md` names the
  mechanism; the claim's verdict does not.
- **The species regime behind the 1 GPa proxy (§4.2).** It is a whole-ray value for
  larger teleosts, applied to a 4 cm zebrafish whose own measured EI and I_eff imply
  2–13 MPa. A 100x cross-species disagreement sitting under the headline GPa figure.
- **Taxon scope of the actinodin identification.** The claim notes And1 and And2 are both
  11.8% proline. I add that the ambiguity is three-way at the record level: UniProt
  carries both **A9JRX1** and **A0ACM8QEN9** as 508-aa And2, and the recorded Boltz2 run
  used the latter while the claim scored the former (§2).
- **No counter-example found against the regime transition itself.** Scope of that
  negative: I read `S13-protein.md`, `S13-deepen.md`, `challenge-18.md`, `challenge-9.md`
  (lines 169–185), `challenge-69.md` and `replicate-14.md` in full, and grepped the
  19 remote branches matching `s13|fin-ray|actinodin|elastoidin|boltz2|plddt` for the
  relevant strings. I did not grep all ~300 remote branches. The claim's §4.2(a)
  reasoning — pLDDT is not a modulus; the load-bearing object is an And1 + Col1a1a +
  Col2a1b assembly, not a monomer; this is true at pLDDT 57 and at pLDDT 95 — I tried to
  break and could not. **That part SURVIVED**, and it is the claim's best contribution.

---

## 7. Verdict

**WEAKENED.**

| Component of the claim | My outcome |
|---|---|
| Regime transition `R-protein-fold → R-material-assembly` is correct | **survives** (§6) — and the claim's reason for it is the right reason |
| The AFDB numbers themselves (27.5% / 26.8% above pLDDT 70) | **survive**, with an exactness correction: 157/570 = 27.54%, 136/508 = 26.77%, and both are whole-chain; mature-chain And1 is 24.1–28.9% |
| "…not 0.0%", "replacing the recorded 0.0%" | **refuted** (§2). The recorded 0.0% is a Boltz2 depth-1-MSA result, correct for its pipeline, already recorded as `weakened`/unreproducible at `challenge-18.md`. The right statement is that the gate is an MSA-depth artifact, not that it is false |
| "fails not for lack of confidence but because pLDDT is not a modulus" | **survives on the mechanism, overstated on the contrast** — under the pipeline the swarm actually ran, there genuinely was no confident prediction |
| "survives a factor-of-two attack on its weakest assumption" | **weakened** (§4). Correct for the deflection criterion; the weakest assumption is the ~1 GPa baseline modulus, and a joint factor-of-two on semi-span and deflection reaches 31 GPa |
| "123–327x flexural-rigidity gap" | **survives**, reproduced exactly from an independently derived closed form |
| "123 GPa requirement vs ~10–30 GPa ceiling" | **refuted as framed** (§4.2). On a baseline internal to the same measured dataset the requirement is ~0.4–1.2 GPa at 20% deflection and ~0.8–2.5 GPa at 10%, inside the protein range. The dimensionless gap stands; the GPa comparison does not |

The claim is careful, reproducible work whose two headline sentences both overreach: it
calls a rival pipeline's number false, and it reports a robustness it tested on the
second-weakest input. Its durable contributions are the integer-exact AFDB fractions and
the assembly argument for the regime transition.

---

## 8. What would settle what remains

1. **The Boltz2 run's artifacts** (`operations.jsonl` and the stage scripts
   `challenge-18.md` searched for and did not find). Cost: zero if committed somewhere I
   did not look; otherwise one re-run. This is what would turn §2 from "two pipelines
   disagree" into "the depth-1 lane is the error".
2. **Per-residue pLDDT for E7F5V5** (`alphafold.ebi.ac.uk/files/...`, 403 here), to
   close the 24.1–28.9% mature-chain bound and say whether the 157 confident residues
   form one domain. Cost: one unblocked host.
3. **Hydrated nanoindentation or microbeam bending on isolated adult zebrafish
   lepidotrichia.** Cost: one AFM session on a handful of adult fish. This is the
   measurement §4.2 turns on, it decides the GPa framing by two orders of magnitude, and
   both the parent document and I independently rank it the highest-value buy in S13.
4. **Puri et al. 2018 Fig. S5C** (the lepidotrichia modulus) and **Puri's definition of
   I_eff**, which would confirm or kill my §4.2 inference directly. Cost: one
   supplementary-file access; recorded `could-not-access` by the parent and not re-tried
   by me.

---

## Provenance

- **Reachable from this session** (HTTP 200, verified by me):
  `alphafold.ebi.ac.uk/api/...`, `rest.uniprot.org`,
  `www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/...`.
- **Must-fail control run by me:** `alphafold.ebi.ac.uk/api/prediction/ZZZZZZ` → HTTP
  **400**, so the endpoint can refuse and the 200s above are informative.
- **Negative control that failed to be a control:** `?version=4` / `?version=5` on the
  E7F5V5 prediction endpoint return 200 with the v6 payload — the parameter is ignored,
  so version-sensitivity is `unknown`, not "unchanged".
- **Not re-tested by me**, taken from the reviewed document: 403s on
  `alphafold.ebi.ac.uk/files/...`, `search.rcsb.org`, `blast.ncbi.nlm.nih.gov`; the four
  queued EBI BLAST jobs; all compute-tool blocks.
- **Repository reads, all `full-text`:** `S13-deepen.md` and `s13d_sensitivity.py`
  (`claude/deepen-s13-fin-ray-xfsos0`), `S13-protein.md`
  (`claude/s13-protein-fin-ray-e8y8d8`), `challenge-18.md`
  (`claude/challenge-18-boltz2-plddt-kz0kkp`), `challenge-9.md`
  (`claude/boltz2-kcnk5b-challenge-jhlceq`), `challenge-69.md`
  (`claude/and1-pdb70-challenge-w5uy17`), `replicate-14.md`
  (`claude/actinodin-replication-14-fm0uqk`).
- **Compute:** 4 CPU, no GPU. I ran **no** structure prediction and **no** stability
  prediction, and report none. Every GPa, MPa, N·m² and percentage I introduce is
  arithmetic, labelled as such at the point of use.
- No number, citation, gene symbol, allele or accession in this file was invented.
  Unavailable values are marked `unknown` or `could-not-access`.

```swarm-challenge
{"claim_id": 139, "outcome": "weakened", "reason": "The regime transition and the AFDB fractions survive (157/570 = 27.54%, 136/508 = 26.77%, by exact integer partition), but the recorded 0.0% is not false - it is a Boltz2 depth-1-MSA result recorded at challenge-18, so the KEY 'replacing the recorded 0.0%' is a cross-predictor substitution rather than a correction; and the feasibility leg's 123 GPa figure rests on a search-summary ~1 GPa cross-species baseline that the same measured dataset puts at 2-13 MPa, which drops the requirement to ~0.4-1.2 GPa, inside the protein range, while the dimensionless 123-654x gap stands.",
  "corrected_value": "Residues above pLDDT 70: AlphaFold DB v6 gives 157/570 = 27.54% (E7F5V5, whole chain; 24.1-28.9% for the 544-aa mature chain) and 136/508 = 26.77% (A9JRX1) - NOT a replacement for the recorded 0.0%, which is Boltz2 with MSA depth 1 (global pLDDT 38.1 and1, 36.1 and2) and correct for that pipeline; the two disagree by predictor, not by error. Feasibility: EI_req = W(b/2)^2/(16*frac), so 4.905e-7 N m^2 and a 123-327x gap at 20% semi-span confirmed, but required ray modulus is 123 GPa only on the ~1 GPa cross-species proxy; on the measurement-internal 2-13 MPa baseline it is 0.42-1.24 GPa at 20% and 0.8-2.5 GPa at 10%. Joint factor-of-two on semi-span and deflection gives 31x and 31 GPa.",
  "depends_on": ["AlphaFold DB API record AF-E7F5V5-F1 v6 (fractions 0.416/0.309/0.223/0.053, globalMetricValue 57.06, AlphaFold Monomer v2.0, retrieved by me 2026-11-04)", "AlphaFold DB API record AF-A9JRX1-F1 v6 (fractions 0.459/0.274/0.264/0.004, globalMetricValue 55.91, retrieved by me 2026-11-04)", "assumption that AFDB bin fractions are residue count / chain length rounded to 3 dp (controlled: unique integer solutions partition both chains exactly)", "UniProt E7F5V5 and A9JRX1 FASTA and feature table (570 aa, 508 aa; Signal 1-26; Disordered 379-400, 419-570), retrieved by me 2026-11-04", "challenge-18.md on branch claude/challenge-18-boltz2-plddt-kz0kkp: Boltz2 + depth-1 MSA gives and1 global 38.1 / 0.0% >pLDDT 70 and and2 36.1 / 0.0%, recorded there as internally consistent but not reproducible from committed artifacts", "challenge-9.md on branch claude/boltz2-kcnk5b-challenge-jhlceq lines 180-181, same Boltz2 table", "Puri et al. 2018 measured whole-caudal-fin EI = 1.5-4e-9 N m^2 and I_eff = 3-7e-16 m^4, quoted at second hand from S13-protein.md (I did not read Puri)", "parent S13-protein.md ray geometry: 16-18 rays of 0.1-0.2 mm diameter", "parent S13-protein.md ~1 GPa teleost whole-ray modulus proxy, read-level search-summary (the input my §4.2 attack targets)", "parent S13-protein.md glider assumptions: m = 0.4 g, semi-span 0.02 m, cantilever with uniformly distributed load, 10% allowable tip deflection", "protein-solid stiffness ceiling as tabulated in S13-protein.md: amyloid 10-30 GPa (partly modelling), insulin fibril 3.3 +/- 0.4 GPa (AFM), silk 1-10 GPa, hydrated collagen fibril 0.2-0.8 GPa"]}
```
