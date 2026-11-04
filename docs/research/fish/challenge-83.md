# Challenge 83: the kcnk5b PDB70 a3m has 76 sequences

**Claim under review (the author's words, not mine):** "PDB70 search on kcnk5b a3m holds 76 sequences (query + 75 PDB70 hit chains, 73 distinct entries); top hits are K2P structures. HARVESTER-VERIFIED: 76 `>` records in kcnk5b_core.a3m, sha256 d65d3773... matches receipt a3m_sha256 and a3m_n_seqs=76." Recorded evidence level: derived. Value: 76 sequences.

**Verdict: SURVIVED.** I redid every count from the raw file and each one came out the same. The two limits I found (below) narrow what "verified" means. Neither one changes the number.

## Inputs and read-levels

| Input | Source | Read-level |
|---|---|---|
| `kcnk5b_core.a3m` (152 lines, 20,906 bytes) | `origin/claude/mol-sims-20261101`, `results/mol-sims/claude-20261101/structures/msa/kcnk5b_core.a3m` | full-text |
| `kcnk5b_core_receipt.json` | same branch, same directory | full-text |
| PDB entry titles for 8 hits (6WLV, 4XDK, 6W88, 4WFE, 3UKM, 6RV3, 7SK1, 6ND0) | PDBe REST `/api/pdb/entry/summary/<id>`, queried 2026-11-04 | listing (titles only) |
| UniProt Q6PFU3 gene name, organism and sequence | `rest.uniprot.org/uniprotkb/Q6PFU3`, queried 2026-11-04 | listing (TSV fields) |
| Author's working | `origin/claude/pdb70-kcnk5b-search-s7699q`, `docs/research/fish/replicate-11.md` | full-text. I read it for the claim only and wrote my own parser. |

## 1. Arithmetic, redone independently (observations on the archived file)

- `sha256sum` of the file gives `d65d377353a647de904d8ca4b3e7c611f88888ab8d39ad80b32754c2df160b01`. This **equals** the receipt's `a3m_sha256`.
- `grep -c '^>'` gives **76**. The receipt's `a3m_n_seqs` is 76. The file has 152 lines, exactly 2 per record, so no record is split across lines and none is missing a header.
- Record 1 is `>query`. Its sequence is 265 aa, and it is byte-identical to the receipt's `sequence` field, whose sha256 matches `sequence_sha256`. So there are 76 − 1 = **75** hit records, with 0 duplicate headers.
- Distinct 4-character PDB IDs: **73**. 6UWM and 7T4X each contribute two chains, so 75 − 2 = 73.
- After dropping lowercase insertions, every hit row has length 265, so the a3m is well-formed against the query.
- The receipt also embeds the alignment (`result_summary.result.alignments.pdb70_220313.a3m.alignment`). It is byte-identical to the file.

## 2. Top hits (my calculation from the a3m, plus a PDBe title listing)

Identity is computed over the query-aligned columns where neither the query nor the hit has a gap. I got these values with my own code:

| # | Hit | Aligned cols / 265 | Identity | PDBe title (listing) |
|---|---|---|---|---|
| 1 | 6WLV_A | 263 | 64.3% | TASK2 in MSP1D1 lipid nanodisc at pH 6.5 |
| 3 | 4XDK_D | 245 | 40.4% | human TREK2 (K2P10.1) |
| 6 | 6W88_B | 228 | 38.2% | K2P2.1 (TREK-1):ML335 |
| 7 | 4WFE_B | 231 | 40.7% | human TRAAK |
| 11 | 3UKM_D | 220 | 34.1% | human K2P1 (TWIK-1) |
| 12 | 7SK1_B | 220 | 34.1% | TWIK1 in nanodisc |
| 13 | 6RV3_D | 184 | 41.3% | human TASK-1 (K2P3.1) |
| 14 | 6ND0_D | 57 | 36.8% | human BK channel (not K2P) |

For hits 14–75, the aligned columns range from 19 to 64. These rows match the author's table. I checked titles for 8 of the 75 hits, not all of them. Hits 2, 4, 5, 8, 9 and 10 have the same alignment profiles as their family neighbours, but I did not look up their titles.

**Query identity:** UniProt Q6PFU3 is `kcnk5b` from *Danio rerio*. The receipt's 265-aa sequence equals UniProt residues 1–265 of the 448-aa entry. So the label "kcnk5b, residues 1–265" is correct. That is an observation from a UniProt listing.

## 3. Attempts to break it

**Proxy.** "Sequences in the a3m" stands in for "PDB70 hits for kcnk5b". These are not the same quantity. The search ran with `search_type: colabfold` against `pdb70_220313`. How many hits it returns depends on that service's E-value, coverage and max-hit settings, and the receipt does not record them. A different PDB70 release or a different cutoff would give a different N. The claim is worded as "the a3m holds", which scopes it to this file, so the proxy is declared rather than hidden. Under the claim's wording this is not a defect. It does mean that "76" should not be quoted as the number of PDB structures homologous to Kcnk5b.

**Hidden assumption: what "harvester-verified" means.** The hash match shows that the file equals what the pipeline wrote into its own receipt, and the embedded alignment matches as well. This is an **internal-consistency check inside a single pipeline**. It does not check the file against the service's own output. The raw service response (`result_summary.response.sha256` `8e10078c…`, 21,167 bytes) is not archived in this repository. A `git grep` for that hash on `origin/claude/mol-sims-20261101` finds only the receipt, and no file path contains `op-71484e57`. The customer-storage bucket is redacted. So I could not check the a3m against the upstream bytes. Suppose I drop the assumption that the receipt was written straight from the service response. The count of 76 is still an exact count of the archived file. What can't be checked is whether the file is the service's complete, untruncated output. I found no sign that it is truncated: the record structure is clean, the last record is complete, and its length is consistent with the 21,167-byte JSON wrapper around a 20,906-byte a3m. That size argument is an inference, not a proof.

**Evidence level.** The label is "derived". The count itself is a direct observation of an archived file. The file is a computed search output, and the receipt says `evidence_kind: computed`. Calling it "derived" is therefore conservative and does not overstate anything. It is not a measured number presented as something stronger. No defect.

**Counter-regime.** If K2P structures deposited after 2022-03-13 (the PDB70 snapshot date) were included, the count would change and might add hits such as other TASK or THIK structures. I did not search for those. This search covers only the receipt's database field, `pdb70_220313`, and the claim makes no statement outside that snapshot.

## Scope of negative searches

- Raw response artifact: I ran `git grep 8e10078c1b4d` and searched path names for `op-71484e57` on `origin/claude/mol-sims-20261101` only. The only match was the receipt itself.
- I did not re-run HHsearch or the ColabFold search, because there is no PDB70 database or HH-suite in this container.
- PDBe titles were checked for 8 of the 73 entries only.

```swarm-challenge
{"claim_id": 83, "outcome": "survived", "reason": "Independent recount of the archived kcnk5b_core.a3m gives 76 records (query + 75 hits, 73 distinct PDB IDs), sha256 and embedded alignment match the receipt, query equals UniProt Q6PFU3 1-265, and top hits are K2P structures by PDBe titles; the only caveat is that the hash check is pipeline self-consistency, since the raw service response is not archived.",
  "corrected_value": null,
  "depends_on": ["origin/claude/mol-sims-20261101:results/mol-sims/claude-20261101/structures/msa/kcnk5b_core.a3m (sha256 d65d377353a6...)", "origin/claude/mol-sims-20261101:results/mol-sims/claude-20261101/structures/msa/kcnk5b_core_receipt.json", "PDBe entry summaries for 6WLV, 4XDK, 6W88, 4WFE, 3UKM, 6RV3, 7SK1, 6ND0 (queried 2026-11-04)", "UniProt Q6PFU3 (queried 2026-11-04)"]}
```
