# S13-D — Deepening S13: attacking the weakest input behind the regime transition

**Project:** `zebrafish-flight` · **Scale:** protein · **Subproblem:** S13-D (deepening of S13)
**Date of work:** 2026-11-04 · **Author:** Claude Code (automated research agent)
**Parent artefact:** `docs/research/fish/S13-protein.md` on branch
`claude/s13-protein-fin-ray-e8y8d8`, commit `6b28af1f` (read in full)

> Read-level key, used on every source: `full-text` | `abstract` | `listing` |
> `search-summary` | `could-not-access`.
>
> **Nothing in this file is an observation of an organism.** Every number I
> produce is either (a) retrieved from a database record, (b) the output of a
> structure-prediction pipeline run by someone else, (c) a sequence computation
> I ran, or (d) arithmetic I did. Each is labelled in the sentence that uses it.

---

## 0. What was recorded, and what I am attacking

The S13 answer as recorded in the swarm ledger line I was given:

> *Not answerable in a protein-folding representation: no PDB70 structural
> homolog, 11.8% proline, 0.0% of residues above pLDDT 70. Re-posed as a
> material-assembly question via regime transition
> `R-protein-fold -> R-material-assembly`.*

That conclusion is a **gate**: three folding-diagnostic numbers are used to
declare the protein-folding representation unusable, and the question is then
moved to a different representation. The gate has exactly three inputs. One of
them is not merely uncertain — **it is wrong**, and I show that by recomputing
it from the primary record below.

Note on provenance of the recorded line itself: the three diagnostics
(`PDB70`, `11.8%`, `pLDDT 70`) do **not** appear in the parent S13 document.
`S13-protein.md` reports AlphaFold DB global pLDDT values of 52–57 and a
*confidence-band* breakdown, no PDB70 search, and no 11.8% figure. So the
recorded summary line was produced somewhere I cannot read. **Scope of that
negative:** I read `S13-protein.md` and `s13_arith.py` in full at commit
`6b28af1f`; a cross-branch `git grep` for the strings `11.8`,
`R-material-assembly` and `R-protein-fold` over all 300+ remote branches was
started and abandoned (it exceeded the 120 s tool budget and I did not retry
it). **I therefore cannot attribute the three numbers to a run, and I treat
them as the inputs-as-recorded, not as someone's defended measurement.**

---

## 1. Which input is the answer most sensitive to

There are two separable conclusions in play, and they have different weakest
inputs. I did both.

### 1.1 The gate on representation (what the recorded line actually claims)

Of the three gate inputs, a factor-of-two error matters only for one:

| Gate input | Factor-of-2 test | Does the gate move? |
|---|---|---|
| `11.8% proline` | 5.9% or 23.6% | **No.** 5.9% is near the proteome mean and 23.6% is above human COL1A1 (19.0%, computed, §3.1). Neither value is "high proline" in a way that changes a folding verdict for a non-collagenous chain. Proline fraction is a *descriptor*, not a threshold anyone folds against. |
| `no PDB70 homolog` | not a number; binary | Moves the gate only if a homolog exists (§3.3). |
| **`0.0% of residues above pLDDT 70`** | 0.0% × 2 = **0.0%** | **This is the decisive one, and it is the one input a factor of two cannot rescue.** Zero is the only value of this input for which the gate closes cleanly: "no residue is confidently predicted" is what licenses "not answerable in a folding representation". Any non-zero value — 5%, 27%, 60% — means part of the chain *is* confidently predicted and the representation is partially usable. The input is therefore maximally sensitive *at* zero, which is where it was recorded. |

**So the single most load-bearing input is `0.0% of residues above pLDDT 70`.**
I attacked that one.

### 1.2 The feasibility conclusion underneath (the parent document's own answer)

The parent document's negative rests on a different number: `EI_req ≈
9.8 × 10⁻⁷ N·m²`, and §5.4 of that document names its own weakest assumption
honestly — the **10%-of-semi-span allowable tip deflection**, which is an
engineering choice, not a biological measurement. I ran that sensitivity too
(§4.2), because if the gate opens, the feasibility question is what the
protein route would have to answer.

---

## 2. How well is `0.0% above pLDDT 70` established

**Evidence level of the input as recorded: `unknown provenance`.**
**Read-level: `could-not-access`** — I could not find the run that produced it
(scope in §0).

What it *would* be if it came from the obvious source: pLDDT is the output of a
**structure-prediction** pipeline. It is not a measurement of a protein, and it
is not a stiffness. A pLDDT value is the model's own estimate of its agreement
with an (unobserved) experimental structure. So even in the best case this
input is:

- **a proxy, twice over** — a confidence estimate standing in for structural
  knowledge, which in turn stands in for the designability of a *mechanical*
  property that no folding model outputs at all;
- **pipeline- and version-dependent** — the same chain scores differently under
  AlphaFold2 monomer, AF-Multimer, AF3 and ESMFold, and the AlphaFold DB entry
  has been re-run (the current record is model-created 2025-08-01, DB version 6);
- **not a threshold with a mechanical meaning** — pLDDT 70 is a convention for
  "backbone probably right", borrowed from a different purpose.

The parent document makes the same point independently and correctly: *"protein
design tools predict thermodynamic/thermal stability (ΔΔG, Tm), not Young's
modulus"* (`S13-protein.md` §1, author's own claim, read-level full-text).

---

## 3. Going and improving it

### 3.1 The primary record for the pLDDT number

Retrieved 2026-11-04 from the AlphaFold Protein Structure Database REST API,
`https://alphafold.ebi.ac.uk/api/prediction/E7F5V5` — **read-level: `full-text`**
(machine-readable record, HTTP 200). E7F5V5 is *D. rerio* **Actinodin1**, the
non-collagenous actinotrichia protein identified by the parent document as the
one fin-ray structural protein with no stability model, and the only one of the
four candidates whose proline fraction is 11.8% (§3.2) — i.e. it is the chain
the recorded line is about.

Record fields, **as returned by EBI (a prediction, not a measurement):**

| Field | Value |
|---|---|
| `globalMetricValue` (mean pLDDT) | **57.06** |
| `fractionPlddtVeryLow` (<50) | 0.416 |
| `fractionPlddtLow` (50–70) | 0.309 |
| `fractionPlddtConfident` (70–90) | **0.223** |
| `fractionPlddtVeryHigh` (>90) | **0.053** |
| `latestVersion` / `modelCreatedDate` | 6 / 2025-08-01 |
| coverage | residues 1–570, whole chain |

**Band fractions sum to 1.001** (rounding) — control check passed, so the four
numbers are a complete partition of the 570 residues and nothing is missing.

**Computed from those fractions:** fraction above pLDDT 70 =
0.223 + 0.053 = **0.276**, i.e. **27.6% of residues, ≈157 of 570.**

**Independent confirmation of the same prediction from a second host:**
PDBe-KB 3D-Beacons, `https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/E7F5V5.json`
returns `confidence_avg_local_score: 57.06`, `confidence_type: pLDDT`,
`coverage: 1.0` for model `AF-E7F5V5-F1` — **read-level: `full-text`**. Two
endpoints, one underlying prediction; this confirms I read the record right, not
that the prediction is right.

**What I could not get:** the per-residue pLDDT array. Every
`alphafold.ebi.ac.uk/files/...` URL (confidence JSON, PDB, CIF, PAE) returns
**HTTP 403 through this session's egress proxy**, as does `search.rcsb.org` and
`blast.ncbi.nlm.nih.gov`. So I **cannot say which 157 residues** are the
confident ones, and I do not guess. UniProt's own feature table for E7F5V5
(`rest.uniprot.org`, read-level `full-text`) annotates residues **379–400 and
419–570 as `Disordered`** and 1–26 as a signal peptide, which is consistent
with the confident fraction lying in the N-terminal half — **my inference,
stated separately from UniProt's annotation, and not verified residue-by-residue.**

### 3.2 The proline number — recomputed, and it stands

Computed by me from the UniProt FASTA (`rest.uniprot.org/uniprotkb/E7F5V5.fasta`,
HTTP 200, read-level `full-text`), committed beside this file as `E7F5V5.fasta`:

| Chain | Pro count | Length | Pro % |
|---|---|---|---|
| And1 **full chain 1–570** | 67 | 570 | **11.8%** |
| And1 mature chain 27–570 (UniProt signal 1–26) | 66 | 544 | 12.1% |
| *D. rerio* Col1a1a (Q6U1J5) | 234 | 1447 | 16.2% |
| *D. rerio* Col2a1b (L0S5L0) | 248 | 1493 | 16.6% |
| *H. sapiens* COL1A1 (P02452) | 278 | 1464 | 19.0% |

**The recorded 11.8% reproduces exactly, on the full chain.** This input is
`measured` in the only sense available for a sequence statistic — it is a
property of a database record, and I recomputed it from that record. It is also
**not doing any work in the gate** (§1.1).

**But 11.8% does not uniquely identify the chain.** Searching UniProt for
*D. rerio* `and2` (`rest.uniprot.org/uniprotkb/search?query=gene:and2 AND
organism_id:7955`, HTTP 200, read-level `full-text`) returns **A9JRX1** and
**A0ACM8QEN9**, both 508 aa Actinodin2 records. Computed from their FASTAs:
**both are 11.8% proline and 4.5% glycine.** So Actinodin1 (11.8%) and
Actinodin2 (11.8%) are indistinguishable on the recorded descriptor. This does
not rescue the pLDDT input — it makes it worse, because the AlphaFold DB record
for A9JRX1 (HTTP 200, read-level `full-text`) gives global pLDDT **55.91** with
confident + very-high = **0.268**, i.e. **26.8% of residues above pLDDT 70**.
`A0ACM8QEN9` returns HTTP **404** from the AlphaFold API — no model; noted, not
worked around. **Whichever actinodin the recorded line meant, the
above-pLDDT-70 fraction is 26.8–27.6%, not 0.0%.**

Also computed: And1 glycine content is **5.4%**, against 26–28% for the three
collagens. **My inference:** And1 has no Gly-X-Y periodicity, so it is not
triple-helical — which agrees with the parent document's finding (longest
Gly-X-Y run = 6 aa) and is the real reason no collagen stability model applies
to it. That is a *stronger* and *more specific* statement than "11.8% proline".

### 3.3 The PDB70 claim — what I could and could not test

PDB70 is an **HHsearch profile database**. Testing "no PDB70 homolog" properly
needs HHblits/HHsearch against a profile library; I have neither the tool nor
the database here, and `search.rcsb.org` (sequence-similarity service) and
`blast.ncbi.nlm.nih.gov` are both **403 through the proxy**. So I **cannot
replicate the PDB70 search**, and I say so rather than implying I did.

What I submitted, as a weaker sequence-level substitute: **NCBI BLASTP via
the EBI Job Dispatcher REST service** (`www.ebi.ac.uk/Tools/services/rest/ncbiblast`,
reachable, HTTP 200) against the **`pdb`** database, with controls in both
directions as this repo's rule 8 requires.

Four jobs were submitted at 08:20 UTC on 2026-11-04 against `database=pdb`,
`program=blastp`, `matrix=BLOSUM62`, `exp=10` — deliberately permissive, so a
miss is a real miss and not a threshold artefact:

| Job | Query | Role | EBI job id |
|---|---|---|---|
| `POS_HsCOL1A1` | *H. sapiens* COL1A1, P02452, full 1464 aa | **positive control** — must hit collagen entries, or the search is not working | `ncbiblast-R20261104-082034-0107-71207843-p2m` |
| `And1_mature_27_570` | And1 mature chain, 544 aa | the claim under test | `ncbiblast-R20261104-082036-0878-87184913-p2m` |
| `And1_disordered_trim_27_378` | And1 27–378, i.e. with the UniProt-annotated disordered tail removed | a fairer test of the ordered part | `ncbiblast-R20261104-082039-0582-58329231-p2m` |
| `MUSTFAIL_And1_shuffled` | And1 mature chain, residues shuffled (`random.seed(13)`) | **must-fail control** — same composition, no real homolog should survive | `ncbiblast-R20261104-082042-0250-52796950-p2m` |

**Outcome: `could-not-access`.** All four jobs were still `QUEUED` in the EBI
Job Dispatcher ~15 minutes after submission and returned no results within this
session's budget. Job ids are recorded above so the run can be retrieved or
repeated rather than re-invented. **I therefore report no BLAST hits, no
BLAST misses, and no control outcome** — the controls are the reason this
cannot be read as a negative result. The parameters and ids are the
deliverable here, not a finding.

**Standing caveat whatever the result:** a BLASTP miss against PDB seqres is
*weaker* evidence than an HHsearch miss against PDB70 — profile methods find
remote homologs that pairwise BLAST misses. A BLAST miss is therefore
**consistent with** the recorded "no PDB70 homolog" but does not establish it.
Read-level for the PDB70 claim itself remains **`could-not-access`**.

---

## 4. Recomputing the conclusion

### 4.1 The gate, with the improved input

Script: `docs/research/fish/s13d_sensitivity.py`
(`python3 -I docs/research/fish/s13d_sensitivity.py` from the repo root
reproduces every number in this section). **All computed, none observed.**

| Gate input | As recorded | Improved (primary record, 2026-11-04) | Effect |
|---|---|---|---|
| residues above pLDDT 70, And1 | **0.0%** | **27.6%** (≈157/570 residues); **26.8%** if the chain meant was And2/A9JRX1 | **gate input falls either way** |
| proline fraction, And1 | 11.8% | 11.8% (reproduced exactly; And2 is also 11.8%, so the descriptor does not identify the chain) | unchanged, and non-load-bearing |
| PDB70 homolog | none | not replicable here; BLASTP substitute in §3.3 | unchanged, read-level `could-not-access` |

A factor-of-two error in the pLDDT input was never the risk. **The input is off
by a categorical margin: the recorded value is zero and the record says more
than a quarter of the chain is in the confident band or better.** On the
recorded input, "no residue is confidently predicted" licenses "not answerable
in a folding representation". On the improved input that licence is withdrawn:
≈157 residues of And1 are predicted at pLDDT > 70 by AlphaFold DB v6, and
AlphaFold's global score of 57.06 is a *whole-chain mean dragged down by the
41.6% very-low fraction*, which UniProt independently annotates as disordered
region (§3.1).

**So the stated reason for the regime transition does not hold.** I state that
plainly, because it is the finding.

### 4.2 Does the conclusion itself survive the gate failing?

Two separate questions, and the honest answer differs between them.

**(a) "Is the folding representation unusable?" — the recorded reason FALLS, and
a better reason replaces it.** The representation is not unusable because the
model is unconfident; it is unusable because **pLDDT is not a modulus and no
folding model outputs one.** That is true at pLDDT 57 and it would be equally
true at pLDDT 95. A confidently-folded And1 monomer still tells you nothing
about the axial stiffness of an elastoidin fibre, because the load-bearing
object is an **assembly** of And1 with Collagen I and Col2a1b, not a monomer.
The parent document reached the same place by a cleaner route (`S13-protein.md`
§2.5: the prediction is of a *monomer* while collagen's load-bearing unit is a
triple helix). **The regime transition to `R-material-assembly` is therefore
correct — but the three diagnostics recorded as its justification are the wrong
justification, and one of them is numerically false.**

**(b) "Could a stiffer protein variant close the fin-ray stiffness gap?" — the
parent negative STANDS, and I tested it against its own weakest assumption.**
Recomputed (all computed, not observed; `EI` baseline 1.5–4 × 10⁻⁹ N·m² is
*measured* by Puri et al. 2018, read-level `full-text` per the parent document):

| Allowable tip deflection | `EI_req` (N·m²) | Gap vs 4 × 10⁻⁹ | Gap vs 1.5 × 10⁻⁹ | Required ray `E` from the ~1 GPa whole-ray proxy |
|---|---|---|---|---|
| 5% semi-span | 1.96 × 10⁻⁶ | 490× | 1308× | 490 GPa |
| **10% (parent's choice)** | 9.81 × 10⁻⁷ | 245× | 654× | **245 GPa** |
| 20% | 4.91 × 10⁻⁷ | 123× | 327× | 123 GPa |
| 40% | 2.45 × 10⁻⁷ | 61× | 164× | 61 GPa |
| 80% (absurd for a spar) | 1.23 × 10⁻⁷ | 31× | 82× | **31 GPa** |

The deflection criterion has to be relaxed to **80% of semi-span** — a wing
whose tip droops nearly as far as it spans — before the required material
modulus falls to ~31 GPa, i.e. merely *touches* the 10–30 GPa ceiling the
parent document reports for the stiffest known protein solid (amyloid fibril,
read-level `search-summary`, partly computational in origin). A factor of two
on the criterion (10% → 20%) leaves a 123–327× gap and a 123 GPa requirement.
**The feasibility negative is not sensitive at the factor-of-two level.**

And the parent document's second leg is untouched by any of this: every source
it cites agrees the hydrated collagen fibril (0.2–0.8 GPa) is **softer** than
the triple helix it is built from, so the tissue is architecture-limited, and a
sequence change pushes on a term that is not the bottleneck.

### 4.3 Verdict

**The conclusion STANDS. Its stated reason FALLS.**

- The regime transition `R-protein-fold → R-material-assembly` is the right
  move, for the reason in §4.2(a) and not for the reason recorded.
- `0.0% of residues above pLDDT 70` is **false as recorded**: the AlphaFold DB
  v6 record for E7F5V5 (Actinodin1) gives **27.6%**, and for A9JRX1
  (Actinodin2) **26.8%**. That number should be corrected in the ledger
  whatever is done with the rest.
- `11.8% proline` reproduces exactly — and holds for *both* actinodins, so it
  does not even name the chain under discussion. It is doing no work.
- `no PDB70 homolog` is neither confirmed nor refuted here — the tool and both
  fallback services are blocked by this session's proxy.
- The underlying feasibility negative (a protein-sequence route cannot supply
  245–654× in `EI`) survives a factor-of-two attack on its own weakest
  assumption, with margin.

Recorded as one verdict for the swarm: **stands** — because the question's
answer (no, re-pose as material assembly) is unchanged. A reader who only
reads the verdict will miss the more useful half, which is that a false input
was carried in the justification.

---

## 5. What this does NOT establish

1. **It does not establish that And1 folds.** 27.6% of residues above pLDDT 70
   is a *prediction's confidence*, from a pipeline I did not run. I could not
   retrieve the per-residue array (403), so I cannot say the confident residues
   form a single domain, and I did not look at the structure at all.
2. **It does not establish the PDB70 negative.** §3.3. HHsearch against PDB70
   was not run by me and cannot be from this container.
3. **It does not re-measure anything biological.** No experiment, no organism,
   no tissue. The only measured quantities anywhere in this chain are Puri
   et al. 2018's fin `EI` and `I_eff`, quoted at second hand from the parent
   document's full-text read.
4. **It does not resolve the parent document's open discrepancies** — the ~150×
   Flammang-derived bluegill stiffness disagreement, and the missing
   lepidotrichia Young's modulus (Puri Fig. S5C, `could-not-access`). Those
   remain the two numbers most worth buying.
5. **It does not run a design tool.** Same blocks as the parent: no GPU, and
   `huggingface.co`, `dl.fbaipublicfiles.com`, `api.esmatlas.com` and
   `collagen.princeton.edu` unreachable. I ran no stability prediction and
   report none.
6. **The 80%-deflection row in §4.2 is not an endorsement.** I computed it to
   find where the negative *would* break, not because any wing works that way.
7. **Negative-search scope.** For the provenance of the three recorded
   diagnostics: parent branch read in full; a cross-branch `git grep` over all
   remote branches was started and abandoned on a 120 s timeout and not
   retried. Absence means "not found in `S13-protein.md` or `s13_arith.py`",
   not "nowhere in the repository".

---

## 6. What would settle the remaining unknowns, and what it would cost

1. **Per-residue pLDDT for E7F5V5, and an AF-Multimer/AF3 run on an
   And1 + Col1a1a + Col2a1b assembly.** Cost: one unblocked host
   (`alphafold.ebi.ac.uk/files`) for the first — free; one GPU-hour or an
   AF3/Boltz server run for the second. This is what would turn §3.1's
   inference about *which* residues are confident into a statement.
2. **An HHsearch run against PDB70** (or any profile method) on the And1
   mature chain, to actually test the recorded claim. Cost: ~50 GB for the
   PDB70/UniRef30 profile databases and a few CPU-hours — cheap, but needs
   egress this session does not have.
3. **The measurement that would reopen the materials route: hydrated
   nanoindentation or microbeam bending on isolated adult zebrafish
   lepidotrichia**, giving the ray material's `E` directly. Per the parent
   document, if that modulus is ~10 MPa rather than ~1 GPa the required
   post-redesign modulus lands near 3.6 GPa and a protein route becomes live.
   Cost: one AFM/nanoindenter session on fins from a handful of adult fish —
   small-animal dissection plus instrument time, days not months. **This is
   still the single highest-value measurement in S13, and it is a mechanical
   measurement, not a protein one — which is itself an argument for the regime
   transition.**
4. **Flammang et al. 2013 full text**, to resolve 565 × 10⁻⁶ vs 3.8 × 10⁻⁶ N·m².
   Cost: one interlibrary request.

---

## Provenance

- **Reachable from this session** (HTTP 200): `rest.uniprot.org`,
  `alphafold.ebi.ac.uk/api/...`, `www.ebi.ac.uk` (3D-Beacons, InterPro,
  Job Dispatcher BLAST REST), `files.rcsb.org`, `www.rcsb.org`.
- **Refused** (403 via egress proxy): `alphafold.ebi.ac.uk/files/...` (all
  model/confidence/PAE files), `search.rcsb.org`, `blast.ncbi.nlm.nih.gov`.
  Unreachable per the parent document and not re-tested here:
  `collagen.princeton.edu`, `huggingface.co`, `dl.fbaipublicfiles.com`,
  `api.esmatlas.com`, `sites.harvard.edu`; `journals.biologists.com` → 403.
- **Must-fail controls run:** `rest.uniprot.org/uniprotkb/ZZZZZZ.fasta` → HTTP
  **400** and `alphafold.ebi.ac.uk/api/prediction/ZZZZZZ` → HTTP **400**, i.e.
  both endpoints *can* come back empty, so the four 200s in §3.1–3.2 are
  informative. Per this repo's rule 8, the must-fail accession was chosen to be
  impossible (`ZZZZZZ` is not a valid UniProt accession format), not merely
  unfamiliar.
- **Positive control run:** `files.rcsb.org/download/1CAG.pdb` and
  `www.rcsb.org/fasta/entry/1CAG` → 200 with the expected collagen-like
  `(PPG)n` peptide sequence, confirming the RCSB file host is live even though
  its search service is blocked.
- Compute: 4 CPU, 15 GB RAM, no GPU. No structure prediction and no stability
  prediction was run by me.
- No number, citation, gene symbol, allele or accession in this file was
  invented. Unavailable values are marked `unknown` or `could-not-access`.

```swarm-result
{"subproblem": "S13-D", "evidence": "derived",
  "answer": "The regime transition out of the folding representation is correct but its recorded justification is not: AlphaFold DB v6 puts 27.6% of Actinodin1 (E7F5V5) residues above pLDDT 70 and 26.8% for Actinodin2 (A9JRX1), not 0.0%, so the folding representation fails not for lack of confidence but because pLDDT is not a modulus and the load-bearing object is an assembly; meanwhile the underlying feasibility negative survives a factor-of-two attack on its weakest assumption, since relaxing the tip-deflection criterion from 10% to 20% of semi-span still leaves a 123-327x flexural-rigidity gap and a 123 GPa material requirement against a ~10-30 GPa protein-solid ceiling.",
  "key_number": "26.8-27.6% of residues above pLDDT 70 (E7F5V5: 0.223 confident + 0.053 very-high of 570 residues; A9JRX1: 0.268 of 508; AlphaFold DB v6 records retrieved 2026-11-04) - replacing the recorded 0.0%",
  "verdict": "stands"}
```
