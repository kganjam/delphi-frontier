# Challenge 69: adversarial review

**Claim under review (not mine):**
> "And1 PDB70 homolog hits = 0; a template-free AlphaFold model exists with 157/570 residues at
> pLDDT>=70 (global 57.06). PDB70 absence does not mean no structure to design against; design
> still unsupported."

- recorded evidence level: `derived`, value: `157 residues pLDDT>=70 of 570`
- recorded source: branch `claude/pdb70-and1-challenge-ne0qg7`, `challenge-12.md`; `AF-E7F5V5-F1` v6

**Verdict: WEAKENED.** The two numbers hold up: 157/570 is the only integer count consistent with
the published bin fractions, and the global pLDDT of 57.06 was re-retrieved from two independent
endpoints. Two of the qualitative words do not hold up. **"template-free"** is not established: the
AlphaFold DB pipeline runs its own PDB70 template search with a deep, MSA-derived profile, and
3D-Beacons gives the "AB-INITIO" label to AlphaFold models that certainly had templates. **"PDB70
homolog hits = 0"** is written as a measured value, but the only recorded input is an MSA depth of
`1` from a single-sequence search, and the author of challenge-12 said themselves that this input
is ambiguous. The bottom line, "design still unsupported", survives.

All work was done on 2026-11-04. Wherever I give my own inference, the sentence says so.

---

## 0. Access log

| Resource | Result | Read-level |
|---|---|---|
| AlphaFold DB API `/api/prediction/E7F5V5` | HTTP 200 | API/JSON (full record) |
| AlphaFold DB `/files/` (v6 per-residue pLDDT, model, PAE, MSA) | HTTP 403 (proxy) | could-not-access |
| GCS `public-datasets-deepmind-alphafold-v4` | `ls` lists `AF-E7F5V5-F1-confidence_v4.json` and `-model_v4.cif`; `get` returns 401 | listing only |
| `alphafold.com`, `ftp.ebi.ac.uk`, `alphafill.eu`, `search.rcsb.org` | CONNECT rejected 403 | could-not-access |
| 3D-Beacons `/uniprot/summary/{acc}.json` (EBI) | HTTP 200 | API/JSON |
| UniProtKB REST `E7F5V5` features | HTTP 200 | API/JSON |
| Tunyasuvunakool et al. 2021, *Nature*, PMC8387240 (AF human proteome) | Methods/Data-availability read through a fetch-and-summarise tool; first ~100k of ~126k chars | full-text (partial, tool-summarised) |
| Varadi et al. 2022, *NAR*, PMC8728224 (AlphaFold DB paper) | read through a fetch-and-summarise tool | full-text (tool-summarised) |
| alphafold.ebi.ac.uk/faq | page renders client-side; no answer text came back | could-not-access |

**I could not obtain per-residue pLDDT from any source.** Every statement below about which
residues are confident is therefore bounded, not counted.

---

## 1. Arithmetic, redone independently

I re-retrieved the inputs rather than copying them from challenge-12. The AlphaFold DB API returns
`globalMetricValue 57.06`, `fractionPlddtVeryLow 0.416`, `Low 0.309`, `Confident 0.223`,
`VeryHigh 0.053`, length 570, `toolUsed "AlphaFold Monomer v2.0 pipeline"`, `latestVersion 6`,
`modelCreatedDate 2025-08-01`. 3D-Beacons independently returns `confidence_avg_local_score 57.06`
for the same model. Both inputs match the claim.

Challenge-12 multiplied 0.276 × 570 = 157.3. I used a different method. Suppose each fraction is
(integer count)/570 rounded to 3 dp. Then each fraction's ±0.0005 rounding window contains exactly
one integer (computed by me):

| bin | fraction | window ×570 | only integer |
|---|---|---|---|
| very low (<50) | 0.416 | 236.83–237.41 | 237 |
| low (50–70) | 0.309 | 175.84–176.41 | 176 |
| confident (70–90) | 0.223 | 126.83–127.39 | 127 |
| very high (>90) | 0.053 | 29.92–30.50 | 30 |

The integers sum to 237 + 176 + 127 + 30 = **570**, which is an internal consistency check that
passes. Residues at pLDDT ≥ 70 = 127 + 30 = **157**. Within that assumption the number is exact,
not ±1. This is still a **calculation from published summary fractions, not a per-residue count**,
and `derived` is the correct label.

There are two residual caveats, both small:
- **Bin boundaries.** AlphaFold DB defines its bins with strict inequalities around 70 and 90.
  Whether a residue at exactly 70.00 falls in "confident" or "low" is `unknown` to me. The claim's
  "≥70" therefore matches the bin sum only up to residues sitting on the boundary.
- **Version.** All figures are for v6. A v4 confidence file exists (GCS listing) but I could not
  read it, so I cannot say whether the v4 and v6 values agree.

**Arithmetic: survives.**

---

## 2. Proxy: "157 residues at pLDDT ≥ 70" standing in for "a structure to design against"

The claim treats the count of residues at pLDDT ≥ 70 as evidence that a usable design substrate
exists. Two problems with that, both of which inflate it as a measure:

1. **Signal peptide.** UniProt annotates residues **1–26 as a signal peptide** (SignalP, automatic
   annotation, `ECO:0000256`; read-level API/JSON). The mature, secreted And1 that would go into
   actinotrichia is 27–570, 544 residues. A hydrophobic signal sequence
   (`MAHLRGSSIFHVLLLATLILPAFLLA`) is the kind of segment AlphaFold often models as a confident
   helix, though for this model that is my inference and not something I observed. Without
   per-residue data, the number of confident residues in the **mature chain** lies somewhere in
   **131–157**. Where in that range is `unknown`.
2. **pLDDT is local.** It says nothing about whether the confident residues are contiguous, or about
   how confident segments are placed relative to each other, which is what PAE measures. The PAE
   file was 403. UniProt/MobiDB-lite marks residues 379–400 and 419–570 as disordered (174
   residues; prediction, not observation). That is consistent with the confident residues sitting in
   the N-terminal ~380, but it does not show it.

The quantity that matters for a stiffness design is the property of the elastoidin fibril, not
how confidently one monomer is modelled. Challenge-12 §2 already makes that point, and I agree with
it. The claim's final clause, "design still unsupported", already accounts for this, so the proxy
problem weakens the middle sentence ("does not mean no structure to design against") but not the
conclusion.

---

## 3. The hidden assumption: that the AlphaFold model is "template-free"

The claim calls the model template-free. Challenge-12 justifies this in one sentence ("This model
was produced without any PDB70 template — that is what template-free prediction is"). That
reasoning assumes AlphaFold DB models are template-free by construction. **That assumption is
false for the pipeline as published:**

- Tunyasuvunakool et al. 2021 (full-text, partial, tool-summarised) describe the AlphaFold
  proteome-scale pipeline as "MSA construction, **template search**, inference with five models",
  and state that "the template search used **PDB70**". The MSAs were built against UniRef90, MGnify
  and a reduced BFD. That paper covers the human proteome run. Applying it to the 2025 v6 zebrafish
  entry is **my inference**, supported by the API reporting the same "AlphaFold Monomer v2.0
  pipeline".
- In that pipeline the PDB70 search queries an HMM built **from the deep MSA**. A single-sequence
  search that returns MSA depth 1 is far less sensitive. So the original negative, `1 sequences`
  from `msa_search_native`, does not show that AlphaFold's own profile search found nothing. This
  is my inference.
- I tested the obvious counter-argument and it fails. 3D-Beacons labels `AF-E7F5V5-F1` as
  `model_category: "AB-INITIO"`, which looks like support for "template-free". As a control, I
  checked proteins with abundant PDB templates. EGFR (P00533, 415 PDBe entries), haemoglobin α
  (P69905, 361) and COL1A1 (P02452, 18) all have **AlphaFold DB models labelled `AB-INITIO`**. The
  label is applied to every AlphaFold DB model, so it says nothing about whether templates were used.

So whether a PDB70 template went into `AF-E7F5V5-F1` is **`unknown`**. To settle it I would need
the AlphaFold run's template hits, which are not published in the API, or the model MSA (`msaUrl`,
403). I am **not** claiming a template was used. A template-free outcome is plausible, and §4
gives one weak supporting negative. The claim's error is in stating this as established.

What survives the relaxation is that a predicted structure exists, whether templated or not. That
point does not depend on "template-free", so the claim's central refutation of "no structure to
design against" still stands.

---

## 4. "PDB70 homolog hits = 0": is the evidence level honest?

**No. A value derived under an assumption is written as if it were a count.**

- The only recorded input is `1 sequences` from `msa_search_native`. That is an **MSA depth**, not
  a template-hit count. Challenge-12 §1 itself says the include-query/exclude-query convention is
  `unknown` and that the record "is not independently checkable". Its `swarm-challenge` block then
  sets `PDB70 homolog hits = 0` anyway. The claim inherits that number without the caveat.
- No one in this chain has accessed PDB70. Challenge-12 lists it as could-not-access, and so do I.
- Supporting negative (weak), scope stated: the 3D-Beacons registry entry for the exact accession
  `E7F5V5` lists **no PDBe experimental structure and no SWISS-MODEL template-based model**. The
  only entries are the AlphaFold DB model and an AlphaFill entry. AlphaFill is a ligand-transplant
  layer on the AlphaFold model, so I do not read its "TEMPLATE-BASED" label as a protein template.
  That is consistent with there being no close PDB homolog. It is not a PDB70 search: it covers
  only what 3D-Beacons providers have deposited for this one accession, and SWISS-MODEL Repository
  coverage of zebrafish TrEMBL entries is not guaranteed.

The corrected statement is: **"PDB70 template hits: `unknown`. The recorded input is MSA depth 1
from a single-sequence search, which is consistent with 0 hits under the include-query reading."**

---

## 5. Regimes and counter-examples

- **Paralogs within the same genome.** As challenge-12 §5 records, zebrafish has `and2`/`and3`.
  If any actinodin paralog or orthologue had an experimental structure, that would be a template.
  I could not run an RCSB search (CONNECT rejected), so this is `unknown`. 3D-Beacons for the exact
  accession shows none (scope as in §4).
- **No published counter-example found.** I found no source reporting an experimental structure of
  any actinodin. That is a negative, scoped to the searches above. It is not a literature survey.

---

## 6. What I tried that failed to break the claim

- **I expected the 157 to be wrong by rounding.** The integer-consistency test pins it to exactly
  157, assuming the fractions are count/570 rounded to 3 dp, so it is not off by rounding.
- **I expected 57.06 might be stale or a different version.** Two independent endpoints return
  57.06 for the v6 model today.
- **I expected "design still unsupported" to be over-cautious.** It is not. Nothing I found
  supplies a fibril-level stiffness model, and a model that is 72% below pLDDT 70 (412/570 by the
  integer counts above) is a poor design substrate.

---

## 7. Summary

| part of claim | status |
|---|---|
| 157/570 residues at pLDDT ≥ 70 | **survives** (derived from bin fractions; exactly 157 under the integer constraint). Up to 26 may be in the signal peptide, so 131–157 in the mature chain |
| global pLDDT 57.06 | **survives** (re-retrieved, 2 endpoints) |
| "template-free" | **unsupported.** The AlphaFold DB pipeline searches PDB70 with an MSA profile, and the "AB-INITIO" label is uninformative (controls in §3). Template use is `unknown` |
| "PDB70 homolog hits = 0" | **overstated.** It is derived from an ambiguous MSA-depth input and presented as a count. `unknown`; consistent with 0 |
| "PDB70 absence ≠ no structure to design against" | **survives.** A predicted structure exists whether or not it was templated |
| "design still unsupported" | **survives** |

## Sources

| Source | Read-level |
|---|---|
| AlphaFold DB API, `https://alphafold.ebi.ac.uk/api/prediction/E7F5V5`, 2026-11-04 | API/JSON |
| 3D-Beacons summary API (EBI) for E7F5V5, P00533, P69905, P02452, 2026-11-04 | API/JSON |
| UniProtKB REST `E7F5V5` (signal, disorder features), 2026-11-04 | API/JSON |
| GCS `public-datasets-deepmind-alphafold-v4` object listing for AF-E7F5V5-F1 | listing |
| Tunyasuvunakool et al. 2021, *Nature*, "Highly accurate protein structure prediction for the human proteome", PMC8387240 | full-text (partial, tool-summarised) |
| Varadi et al. 2022, *NAR*, AlphaFold Protein Structure Database, PMC8728224 | full-text (tool-summarised); no template statement found |
| `claude/pdb70-and1-challenge-ne0qg7:docs/research/fish/challenge-12.md` | full-text |
| AlphaFold DB per-residue/PAE/MSA files, alphafold.com, alphafill.eu, RCSB search, PDB70 | could-not-access |

I have kept one disagreement between sources as it stands. 3D-Beacons labels the model `AB-INITIO`,
while the published pipeline includes a PDB70 template search. I resolve that only as far as the
controls allow: the label is uninformative. I do not resolve it to "a template was used".

```swarm-challenge
{"claim_id": 69, "outcome": "weakened", "reason": "The numbers survive (157/570 is the unique integer solution to AlphaFold DB's bin fractions and 57.06 re-retrieves from two endpoints), but 'template-free' is unestablished because the AlphaFold DB pipeline runs its own MSA-profile PDB70 template search and the 3D-Beacons AB-INITIO label also tags templated models like EGFR, and 'PDB70 homolog hits = 0' is written as a count when it rests on an ambiguous MSA-depth-1 input with PDB70 never accessed.",
  "corrected_value": "157 of 570 residues at pLDDT>=70 (derived from bin fractions, 127 confident + 30 very high; 131-157 in the mature chain after the 1-26 signal peptide); global pLDDT 57.06; PDB70 template hits unknown (consistent with 0); template use in AF-E7F5V5-F1 unknown",
  "depends_on": ["AlphaFold DB API record for AF-E7F5V5-F1 v6 (fractions 0.416/0.309/0.223/0.053, globalMetricValue 57.06, retrieved 2026-11-04)", "assumption that AFDB bin fractions are count/570 rounded to 3 dp", "3D-Beacons summary API for E7F5V5, P00533, P69905, P02452 (AB-INITIO label control; no PDBe/SWISS-MODEL entries for E7F5V5)", "Tunyasuvunakool et al. 2021 PMC8387240 statement that the AlphaFold proteome pipeline includes PDB70 template search, extrapolated to the v6 entry", "UniProtKB E7F5V5 signal peptide 1-26 (SignalP automatic annotation)", "challenge-12.md record that the original input was msa_search_native '1 sequences' with unknown query-inclusion convention"]}
```
