# Challenge 139 — adversarial review of the S13-D claim

**Claim id:** 139 · **Target:** `harvest:deepen-s13-fin-ray-xfsos0`, subproblem S13-D
**Recorded evidence level:** `derived` · **Recorded verdict:** `stands`
**Reviewer:** Claude Code (automated), adversarial role · **Date:** 2026-11-04

> Read-level key, used on every source: `full-text` | `abstract` | `listing` |
> `search-summary` | `could-not-access`.
>
> **Nothing in this file is an observation of an organism.** Every number below is
> either (a) a field retrieved from a database record, (b) the output of a
> structure-prediction pipeline someone else ran, or (c) arithmetic I did. Each is
> labelled in the sentence that uses it. The only *measured* mechanical quantity
> anywhere in this chain is Puri et al. 2018's fin `EI`, which I take at second
> hand from the parent document (`could-not-access` for me directly).

**Outcome: WEAKENED.** The claim has two clauses joined by "meanwhile". The first
clause survives and is in fact *stronger* than the author establishes. The second
clause — that the feasibility negative "survives a factor-of-two attack on its
weakest assumption" — does not survive, because the author attacked the wrong
assumption, and the one they did not vary flips the comparison they rest on.

---

## 1. Arithmetic, redone independently

Recomputed from the claim's stated inputs only, without reading the author's
script until afterwards. Reproduce with
`python3 -I docs/research/fish/challenge139_recompute.py`. **All computed.**

### 1.1 The pLDDT fractions — reproduce exactly

| Quantity | My value | Claim's value | Agrees? |
|---|---|---|---|
| E7F5V5 above pLDDT 70 = 0.223 + 0.053 | 0.276 → **27.6%** | 27.6% | ✅ |
| E7F5V5 residue count = 570 × 0.276 | 157.3 → ≈157 | ≈157 | ✅ |
| A9JRX1 above pLDDT 70 | **0.268 → 26.8%** | 26.8% | ✅ |
| A9JRX1 residue count = 508 × 0.268 | 136.1 | (not stated) | — |
| E7F5V5 band sum (0.416+0.309+0.223+0.053) | 1.001 | 1.001 | ✅ |

The band-sum control is worth keeping: it confirms the four fractions are a
complete partition, so `confident + very-high` is the whole of what lies above 70
and nothing is being dropped.

### 1.2 The beam arithmetic — reproduces, and my first check was wrong, not theirs

My first independent closed form disagreed with the author's script by 50×. The
error was mine: with a uniformly distributed load and the deflection criterion
expressed as a *fraction* of semi-span, `EI_req = w·L⁴/(8·δ)` with `δ = f·L`
collapses to `W·L²/(16·f)`, not `W·L³/(16·f)`. Corrected:

| Allowable tip deflection | `EI_req` (N·m²) | gap vs 4×10⁻⁹ | gap vs 1.5×10⁻⁹ |
|---|---|---|---|
| 10% semi-span | 9.810×10⁻⁷ | 245.2× | 654.0× |
| 20% semi-span | 4.905×10⁻⁷ | **122.6×** | **327.0×** |

The claim's "123–327×" reproduces exactly. **No arithmetic defect found in the
claim.** One presentational note: the claim's "123 GPa" pairs the ratio computed
at the *stiffest* end of the measured `EI` range (4×10⁻⁹) with the 1 GPa
baseline; the parent document used 357× (the 2.75×10⁻⁹ midpoint), which would
give 178 GPa at 20%. The claim's choice is the one least favourable to its own
argument, i.e. conservative in the right direction. Credit, not a fault.

---

## 2. Verifying the first clause against the primary record — it SURVIVES, and is understated

I did not take the author's quoted API fields on trust. Retrieved 2026-11-04 from
`https://alphafold.ebi.ac.uk/api/prediction/{acc}` — **read-level: `full-text`**
(machine-readable record, HTTP 200). These are a *prediction's self-confidence*,
not measurements of a protein.

| Accession | Chain | global pLDDT | confident (70–90) | very-high (>90) | **above 70** | band sum |
|---|---|---|---|---|---|---|
| E7F5V5 | Actinodin1, 570 aa | 57.06 | 0.223 | 0.053 | **27.6%** | 1.001 |
| A9JRX1 | Actinodin2, 508 aa | 55.91 | 0.264 | 0.004 | **26.8%** | 1.001 |
| Q6U1J5 | Col1a1a, 1447 aa | 53.44 | 0.062 | 0.144 | **20.6%** | 1.001 |
| L0S5L0 | Col2a1b, 1493 aa | 52.38 | 0.061 | 0.131 | **19.2%** | 1.000 |

**Must-fail controls, run:** `ZZZZZZ` → HTTP **400**, `A0ACM8QEN9` → HTTP **404**.
Both endpoints can come back empty, so the four 200s are informative.

**The strongest attack available on this clause fails.** The obvious way to rescue
the recorded `0.0%` is chain identity: the author shows that `11.8% proline` does
not uniquely name a chain (And1 and And2 are both 11.8%), which opens the
possibility that the recorded line meant some *other* chain whose above-70
fraction really is zero. So I checked **all four** candidate chains the parent
document puts in play, not the two the author checked. **None is at 0.0%; the
range is 19.2–27.6%.** The correction therefore cannot be escaped by reassigning
the chain. That is a materially stronger result than the claim states, and the
author did not claim it.

**Probable provenance of the `0.0%` — my inference, stated as mine.** All four
global pLDDT values (52.38, 53.44, 55.91, 57.06) are below 70. "No chain has a
global pLDDT above 70" is *true*, and equals 0 of 4. My inference is that the
recorded `0.0% of residues above pLDDT 70` is a category slip — a true
chain-level statement transcribed into a per-residue fraction. This does not
rescue the number as written, and does not change the claim's conclusion; it
means the error is a transcription error rather than a fabricated statistic. The
author could not find the provenance (`could-not-access`, scope stated in their
§0) and correctly declined to guess at intent; I am guessing, and labelling it.

**Proxy check on this clause.** `fraction above pLDDT 70` is a proxy twice over —
a prediction's confidence standing in for structural knowledge, which stands in
for designability of a *mechanical* property no folding model emits. The claim
says exactly this, and its replacement reason (pLDDT is not a modulus; the
load-bearing object is an assembly of And1 with Col1a1a/Col2a1b, not a monomer)
is the correct object-level reason and matches the parent's §2.5. **No proxy
substitution defect in clause one.** Minor unflagged detail: the fraction is
computed over the full 570-residue model including the cleaved signal peptide
(UniProt 1–26); excluding it would move the number slightly *up*, so it does not
threaten the claim.

---

## 3. The second clause — the hidden assumption, relaxed. This is where it breaks.

The claim's second clause:

> *"the underlying feasibility negative survives a factor-of-two attack on its
> weakest assumption, since relaxing the tip-deflection criterion from 10% to 20%
> of semi-span still leaves a 123-327x flexural-rigidity gap and a 123 GPa
> material requirement against a ~10-30 GPa protein-solid ceiling."*

### 3.1 The deflection criterion is not the weakest assumption

The claim inherits "weakest assumption = the 10%-of-semi-span deflection
criterion" from the parent document's own §5.4 self-assessment, and tests it at
2×. But the sentence's payload is a **GPa comparison**, and converting the
dimensionless `EI` gap into a required *material modulus* requires a second
input the claim never varies: the **baseline material modulus** of the existing
ray. That input is:

- **unmeasured** — the parent gives it `read-level: search-summary` and names a
  measured `E` for zebrafish lepidotrichia as the single highest-value missing
  measurement in all of S13;
- **wide** — the parent's own cited source gives whole-ray moduli of *mean 1.34
  GPa proximal, range 0.24–3.7 GPa; **distal 0.11–0.67 GPa***, and the parent's
  §3.5 tabulates three different baselines (5 MPa homogenised fin plate, 0.3 GPa
  hydrated collagen fibril, ~1.0 GPa teleost whole-ray) yielding required moduli
  of **1.8 / 107 / 356 GPa** — a factor-of-200 spread;
- **linear in the answer** — required `E` = `ratio × baseline`, so an error here
  passes straight through, undamped.

### 3.2 Relaxed, at the claim's own 20% criterion (all computed)

| Baseline `E` (unmeasured proxy) | source | req. `E` @10% | req. `E` @20% | vs 10–30 GPa ceiling |
|---|---|---|---|---|
| 5 MPa homogenised fin plate | parent §3.4 | 1.2 GPa | **0.6 GPa** | far inside |
| **0.11 GPa whole-ray, distal** | parent §2.2, same source as the ~1 GPa figure | **27.0 GPa** | **13.5 GPa** | **inside, both criteria** |
| 0.3 GPa hydrated collagen fibril | parent §2.4 | 73.6 GPa | **36.8 GPa** | 1.2× above top |
| 1.0 GPa teleost whole-ray | **the claim's choice** | 245.2 GPa | 122.6 GPa | far above |
| 3.7 GPa whole-ray, proximal high | parent §2.2 | 907.4 GPa | 453.7 GPa | far above |

And the threshold, computed: at 20% deflection the requirement **meets the 30 GPa
ceiling top at a baseline of 0.245 GPa**, i.e. after only a **4.1× reduction**
from the claim's 1.0 GPa — and reaches the 10 GPa ceiling floor at 0.082 GPa.
The parent's own cited whole-ray range (0.11–3.7 GPa) *brackets* that crossing
point. The distal row is not a hypothetical: it is the distal end of the very
source the ~1 GPa figure is drawn from, and the distal ray is precisely where a
slender spar's tip lies.

**So the comparison the clause rests on — "123 GPa against a ~10-30 GPa ceiling"
— is not robust.** It is contingent on one unmeasured proxy, and it flips to
*inside the ceiling* at a value within that proxy's own published range, at both
the original and the relaxed deflection criterion. A factor-of-two attack on the
input the author chose leaves the negative standing; a factor-of-four attack on
the input they did not choose does not. **The claim's own framing — "its weakest
assumption" — is the defect: it names the second-weakest.**

### 3.3 What is actually robust, and what still carries the negative

In fairness, and this is the honest residue:

1. **The dimensionless gap survives everything I threw at it.** 123–327× at 20%,
   245–654× at 10%, from measured `EI` plus the beam model. It does not depend on
   the baseline modulus at all. The claim's "123-327x flexural-rigidity gap" is
   sound.
2. **Softening the baseline does not make the redesign easy.** A 0.11 GPa
   baseline puts the *absolute* requirement at 13.5 GPa (inside the protein
   ceiling) but still demands a **~123× increase in the material's own modulus**
   from a sequence change. Inside the ceiling ≠ reachable by mutation.
3. **The parent's second leg is untouched by any of this.** Hydrated collagen
   fibrils (0.2–0.8 GPa) are *softer* than the triple helix they are built from,
   so the tissue is architecture-limited, not molecule-limited, and a sequence
   change pushes a term that is not the bottleneck. That argument is independent
   of every number above and I did not break it.

So the *feasibility negative* survives on legs 1 and 3. What fails is the
claim's specific evidentiary route to it, and its assertion of robustness.

---

## 4. Is the evidence level honest?

**Yes, with one caveat about the key number's framing.** `derived` is the right
label. The claim's document is scrupulous about pLDDT being a prediction rather
than a measurement, says so in the sentences that use it, marks the API read
`full-text`, states the scope of its negative searches, records the four EBI
BLAST job ids rather than inventing outcomes, reports its PDB70 leg as
`could-not-access` rather than implying a search it could not run, and preserves
the parent's internal disagreements instead of averaging them. The must-fail and
positive controls are real and were run. I found **no honesty-floor breach.**

One framing caveat: the key number is phrased "26.8-27.6% of residues above
pLDDT 70", which reads as a property of the actinodins. It is a property of
*AlphaFold DB v6's prediction* of them — which the claim's prose makes clear but
the extracted `key_number` string does not. Anyone reading the ledger line alone
could mistake it for a structural fact. That is a packaging issue, not a defect
in the work.

---

## 5. Regime, taxon and published counter-example search

**The ceiling leg (`~10-30 GPa protein-solid ceiling`) is softer than the claim
implies, but I could not break it.** The parent names its own break condition:
*any measured modulus for a protein-only solid above ~50 GPa*. Searching for one
(**read-level: `search-summary`** throughout; scope: two web searches,
2026-11-04, on stiffest protein/peptide materials):

- **Diphenylalanine (FF) peptide nanotubes: ~19 GPa** (Kol et al., *Nano Lett*
  5(7):1343-6, 2005 — AFM point stiffness 160 N/m converted to a modulus by
  finite-element analysis, so model-derived, not a direct measurement), and
  **27 ± 4 GPa** from a later AFM bending-beam study. Both sit **inside** the
  10–30 GPa ceiling, so they do not break it. A first-principles calculation for
  the bulk gives **~8.8 GPa**, *below* the AFM values — disagreement preserved,
  not averaged.
- **Candidates above 50 GPa exist but I could not verify any of them.**
  Pro-Phe-Phe ~44 GPa and Hyp-Phe-Phe ~102 GPa appear only in a **USPTO patent
  document** (12185635); a ~275 GPa figure for dipeptide nanospheres appears only
  in a **press-style secondary page** (Foresight Institute). A peer-reviewed
  title that plausibly underlies the latter exists — *"Diphenylalanine-Derivative
  Peptide Assemblies with Increased Aromaticity Exhibit Metal-like Rigidity and
  High Piezoelectricity"*, ACS Nano 14(6):7025 — but **I could not read it or any
  abstract of it**: `pubs.acs.org` and `pubmed.ncbi.nlm.nih.gov` both fail DNS
  resolution in this session (outside its allowed network domains), so per this
  session's guidance I stopped rather than trying further hosts. **I do not quote
  44, 102 or 275 GPa as established, and I do not treat the ceiling as broken.**
- **Scope of that negative:** two web searches only, no full-text access to any
  primary mechanical-testing paper. Absence here means "not verified within that
  scope", not "does not exist".

Two further points on the ceiling, both mine:

- Even if the >50 GPa values hold, they are **dipeptide crystals and nanotubes** —
  highly ordered small-molecule-like assemblies. They are not a route for a
  570-aa actinodin, so they would break the *ceiling leg as the parent phrased
  it* without reopening the actual design question.
- No taxon counter-example found for the S13 geometry. I did not find a published
  teleost with fin-ray `EI` near 10⁻⁶ N·m² at this body scale, but I did not
  search systematically for one — **scope: none, not attempted.**

---

## 6. What I could not test

1. **Per-residue pLDDT.** Not retrieved; I used only the four band fractions. So
   like the author, I cannot say *which* ~157 residues are confident, and I make
   no claim about whether they form a domain.
2. **The PDB70 negative.** Unchanged and untested by me; the author's
   `could-not-access` stands, and their caveat that a BLASTP miss is weaker than
   an HHsearch miss is correct.
3. **The four EBI BLAST jobs.** I did not poll or resubmit them.
4. **Puri et al. 2018's measured `EI`.** `could-not-access` for me; taken at
   second hand from the parent's full-text read. **My verdict depends on it.** If
   that `EI` is wrong, both the 123–327× gap and my §3.2 table move.
5. **The 11.8% proline recomputation.** I did not redo it; it is not load-bearing
   in either clause and the author's reproduction of it is internally consistent.

---

## 7. Verdict

**WEAKENED.**

- **Clause 1 (the pLDDT correction) — SURVIVED, and strengthened.** Verified
  independently against the primary record: 27.6% (E7F5V5) and 26.8% (A9JRX1)
  reproduce exactly, and I extended the check to the other two candidate chains
  (20.6%, 19.2%), closing the chain-identity escape route the author left open.
  The recorded `0.0%` is false as written for every chain in play. The
  replacement reason for the regime transition — pLDDT is not a modulus, the
  load-bearing object is an assembly — is correct.
- **Clause 2 (the robustness assertion) — FAILS as stated.** The deflection
  criterion is not the weakest assumption. The baseline material modulus is: it
  is unmeasured, spans a factor of ~200 across the parent's own tabulated
  candidates, enters the answer linearly, and at the distal whole-ray value from
  the very source the claim's ~1 GPa figure comes from (0.11 GPa) the requirement
  is **13.5 GPa at 20% deflection and 27.0 GPa at 10% — inside the quoted
  10–30 GPa ceiling at both.** The "123 GPa against a ~10-30 GPa ceiling"
  comparison is not robust and should not be offered as evidence of survival.
- **The underlying answer to S13 is unchanged** — the `R-protein-fold →
  R-material-assembly` transition is right, and the feasibility negative still
  holds on the dimensionless 123–327× gap and the independent
  architecture-limited argument. I am not manufacturing feasibility: a protein
  sequence route still has to supply ~123× in material modulus even on the most
  favourable baseline.
- **Recommended ledger edit:** keep the corrected key number; replace the
  robustness clause with the dimensionless gap alone, and record that the
  required-modulus-versus-ceiling comparison is contingent on an unmeasured
  baseline that the parent itself flags as S13's highest-value missing
  measurement.

---

## Provenance

- **Reachable** (HTTP 200): `alphafold.ebi.ac.uk/api/prediction/...` for E7F5V5,
  A9JRX1, Q6U1J5, L0S5L0.
- **Controls run:** `ZZZZZZ` → 400, `A0ACM8QEN9` → 404 (must-fail, both
  informative).
- **Unreachable** (DNS not resolved — outside this session's allowed domains):
  `pubs.acs.org`, `pubmed.ncbi.nlm.nih.gov`. These need to be allowed in the
  session's network settings for the ceiling counter-example to be raised above
  `search-summary`.
- **Read in full:** the S13-D claim document (`S13-deepen.md`) and its
  `s13d_sensitivity.py`, and the parent `S13-protein.md`, both at the commits
  named in §0 of the claim.
- Recompute script: `docs/research/fish/challenge139_recompute.py`.
- No number, citation, gene symbol, allele or accession in this file was invented.
  Unavailable values are marked `unknown` or `could-not-access`.

```swarm-challenge
{"claim_id": 139, "outcome": "weakened",
  "reason": "The pLDDT correction verifies exactly against the primary record and is stronger than claimed (all four candidate chains are 19.2-27.6% above pLDDT 70, closing the chain-identity escape), but the second clause misidentifies the weakest assumption: the required-modulus-versus-ceiling comparison is linear in an unmeasured baseline ray modulus spanning a factor of ~200 in the parent's own table, and at the distal whole-ray value from the same source as the claim's ~1 GPa figure (0.11 GPa) the requirement is 13.5 GPa at 20% deflection and 27.0 GPa at 10%, i.e. inside the quoted 10-30 GPa protein ceiling at both criteria.",
  "corrected_value": "pLDDT clause confirmed: 27.6% (E7F5V5, 0.223+0.053 of 570), 26.8% (A9JRX1, 0.264+0.004 of 508), plus 20.6% (Q6U1J5) and 19.2% (L0S5L0), AlphaFold DB v6 retrieved 2026-11-04. Robustness clause corrected: the robust quantity is the dimensionless 123-327x EI gap at 20% semi-span deflection; the required material modulus is 0.6-454 GPa across the parent's own baseline range, not 123 GPa, and falls inside the 10-30 GPa protein ceiling for baselines at or below 0.245 GPa.",
  "depends_on": [
    "AlphaFold DB v6 band fractions for E7F5V5 (fractionPlddtConfident 0.223, fractionPlddtVeryHigh 0.053, 570 aa), retrieved 2026-11-04, read-level full-text",
    "AlphaFold DB v6 band fractions for A9JRX1 (0.264, 0.004, 508 aa), retrieved 2026-11-04, read-level full-text",
    "AlphaFold DB v6 band fractions for Q6U1J5 (0.062, 0.144) and L0S5L0 (0.061, 0.131), retrieved 2026-11-04, read-level full-text",
    "Puri et al. 2018 measured zebrafish fin EI = 1.5-4e-9 N m^2, taken at second hand from S13-protein.md (could-not-access for me directly)",
    "S13 glider spec: body mass 0.4 g, semi-span 0.02 m, uniformly loaded cantilever model delta = wL^4/(8EI)",
    "S13-protein.md baseline moduli: 5 MPa homogenised fin plate, 0.3 GPa hydrated collagen fibril, ~1.0 GPa teleost whole-ray with cited range 0.24-3.7 GPa proximal and 0.11-0.67 GPa distal (read-level search-summary)",
    "S13-protein.md 10-30 GPa amyloid-fibril ceiling for protein solids (read-level search-summary, partly computational in origin)",
    "S13-protein.md architecture-limited argument: hydrated collagen fibril 0.2-0.8 GPa is softer than the triple helix it is built from"
  ]}
```
