# What the runs actually establish (and what they do not)

**Every structure here is a prediction.** pLDDT and pTM are each model's confidence in its own
output — not accuracy, not a measurement. No experimental structure of kcnk5b, and1 or and2 was
used or compared against. Nothing below is evidence that any of these proteins behaves as
described in a fish.

---

## 1. kcnk5b — the MSA is what made the difference, and it matters at the functional site

| | OpenFold2 (single-seq) | Boltz2 + PDB70 MSA |
|---|---|---|
| mean pLDDT | 56.1 | **62.0** |
| pTM | 0.258 | **0.479** |
| residues >70 | 14.7% | **38.8%** |
| longest stretch >70 | 17 aa | **55 aa** (160–214) |
| mean pLDDT, residues 1–250 | — | **77.5** (69.6% >70) |

**The selectivity filters are the check that makes this interpretable.** Potassium channels carry
a T-x-G-Y/F-G signature at the pore. Scanning the kcnk5b sequence for `[TS].[GAS][YFL]G` returns
**exactly two** matches — which is the defining architecture of a two-pore-domain (K2P) channel:

| motif | residues | context | OpenFold2 pLDDT | Boltz2 pLDDT |
|---|---|---|---|---|
| `TIGYG` | 98–102 | `AATVITTIGYGNVAPKT` | 40.1 | **80.2** |
| `TVGFG` | 203–207 | `SFTTLTTVGFGDYVAGV` | 41.4 | **82.6** |

So the single-sequence model left both functionally central sites unmodelled (~40), and the
MSA-conditioned model resolved both (~80–83). For a channel whose job is selective K+ conduction,
that is the difference between a structure that can be reasoned about and one that cannot.

**The confident block is residues ~1–250 and the poor region is ~260–448.** That split is what a
K2P channel plus a long cytoplasmic C-terminal tail would look like. **This mapping is my
inference** from the fold and the alignment, *not* a cited annotation: Q6PFU3 is an unreviewed
TrEMBL entry with **no curated FUNCTION comment and no topology** (checked against UniProtKB
release 2026_03, 2026-11-03). A low pLDDT in a tail is also consistent with genuine disorder,
which is a prediction about flexibility, not a failure — the two cannot be told apart from pLDDT
alone.

**What the alignment contains.** 71 hits over 69 PDB entries. Ten identities were checked against
RCSB rather than recalled (`msa_kcnk5b/HITS.md`); the other 59 were not. The relevant one:
**6WLV / 6WM0 are TASK-2, RCSB gene name `Kcnk5`** — the direct ortholog, in two pH states. The
hit set is *not* uniformly K2P (2R9R, 1ORQ, 6U9Z, 7T4X are Kv, prokaryotic and plant channels),
so it is the potassium-channel superfamily with K2P members and the ortholog inside it.

---

## 2. and1 / and2 — a real negative, from three independent directions

Published work on actinodins shows loss of function; whether they can be *stiffened* was the open
design question. The honest answer from this workbench is that **there is nothing to design
against yet**:

1. **No structural homolog exists.** `msa_search_native` against PDB70 returned **1 sequence —
   the query alone** — for both and1 and and2. (Positive control: the same search on kcnk5b
   returned 72. The search works; the absence is real for this database.)
2. **Neither model folds them.** Both are **0.0% of residues above pLDDT 70** under Boltz2, and
   1.0–4.9% under OpenFold2. and1 Boltz2 pTM 0.219, and2 0.184. Boltz2 was *worse* than OpenFold2
   for both, which is what an MSA-dependent model does when handed an MSA of depth 1.
3. **The composition is non-globular.** Measured from the sequences:

   | | length | Pro | Tyr | Ser | Ile | Val | Phe | `C…DP…C` motifs |
   |---|---|---|---|---|---|---|---|---|
   | kcnk5b | 448 | 4.0% | 2.7% | 5.1% | 5.8% | 8.3% | 6.0% | 0 |
   | and1 | 570 | **11.8%** | 8.2% | 9.8% | 2.1% | 3.9% | 1.4% | 4 |
   | and2 | 508 | **11.8%** | 5.7% | 10.6% | 3.1% | 4.7% | 3.1% | 6 |

   11.8% proline with depleted Ile/Val/Phe is an extended, repetitive, non-globular composition —
   the opposite of a packable hydrophobic core. kcnk5b's Leu/Val-rich profile is a membrane protein.

**Scope.** This is a negative against **PDB70 only** — a structure database. It says no *solved
structure* resembles them. It is not a statement about sequence homologs in UniProt, and this
workbench exposes no sequence-database search to test that. A deeper MSA (UniRef/BFD) is the
obvious next step and is not available here.

---

## 3. Substitution scoring — blocked as specified, and the substitute has a caveat

`esm2-650m`, `esm2-3b` and `stab-ddg` all return
`MODEL_MAINTENANCE: This App is temporarily paused for maintenance; the request was not submitted.`
So variant scoring and ddG as specified could not be run. (Note the catalogue lists esm2-3b and
stab-ddg as `availability: "available"` — that field is not a runtime claim.)

ProteinMPNN is live and was run as the nearest substitute. **It answers a different question**:
which residues a backbone tolerates — a design prior conditioned on geometry — not ESM's
"how surprising is this substitution", and not a ddG in kcal/mol.

**Its first run was a false start, and the second is its own control:**

| backbone | mean pLDDT | seq recovery | score (lower better) |
|---|---|---|---|
| OpenFold2 full (448 aa) | 56.1 | 0.127–0.152 | 1.437–1.555 |
| **Boltz2 core (1–250)** | **77.5** | **0.292–0.324** | **0.962–1.069** |

The first run returned near-poly-leucine at ~14% recovery. That is what ProteinMPNN does on a bad
backbone, not a property of kcnk5b; recovery roughly doubled and the score improved by ~0.45 on
the better backbone. **Even 0.32 is modest**, so the per-position distributions
(`mpnn_core/result_*.json`, `probs`, 250×21) are a weak prior and should not be read as
substitution effects. They are not a substitute for ESM scoring, and the ESM result is simply
missing.

---

## 4. What would move this forward

- A deeper MSA than PDB70 (UniRef/BFD) — the single biggest lever, and not available on this
  workbench. kcnk5b went 0.258 → 0.479 pTM on 72 PDB sequences alone.
- The TASK-2 structures (6WLV/6WM0) as explicit templates, rather than only as MSA rows.
- ESM-2 / stab-ddg once maintenance ends, for the substitution question as actually posed.
- For and1/and2: a disorder/coiled-coil analysis is the appropriate tool, not a folding model.
  Asking a structure predictor to fold a 11.8%-proline repeat protein and reporting the low score
  as a result would be measuring the wrong thing.
