# Replication 15: K+ selectivity-filter motifs in zebrafish kcnk5b (UniProt Q6PFU3)

**Date:** 2026-11-04 · **Type:** independent re-derivation, computed. I ran a regex scan over sequences I downloaded. Nothing here was measured at the bench.

## Claim under test

The zebrafish kcnk5b protein carries exactly two matches to the K+ selectivity-filter regex `[TS].[GAS][YFL]G`, which is the two-pore (K2P) architecture. The prompt gave the claim with the answer removed. The claim text itself names TIGYG at 98–102 and TVGFG at 203–207 and gives "negative controls and1/and2 return 0".

## My value

**2 matches** (computed result, not an observation) in Q6PFU3:

| # | Start–end (1-based) | Motif | Local context (residues 86–115 / 191–220) |
|---|---|---|---|
| 1 | 98–102 | TIGYG | `ENAVIFAATVITT**IGYG**NVAPKTTGGRLFC` → `TT IGYG`; the match is T98-I99-G100-Y101-G102 |
| 2 | 203–207 | TVGFG | `LEGLYFSFTTLT**TVGFG**DYVAGVDPSVNYP` |

**Uncertainty:** on this sequence version the count is exact (0 uncertainty), and it is deterministic. The ways it could be wrong are definitional, not numerical:
- It depends on the regex chosen. The stricter canonical `T.G[YF]G` also gives 2, and so does the bare `G[YF]G` (at 100 and 205). With these three definitions the count does not change.
- It depends on the sequence version: Q6PFU3 SV=1, entry version 124 (02-SEP-2026), 448 aa, CRC64 A5437FAB7930A1B8. The entry is unreviewed TrEMBL. A future sequence revision could move the coordinates.

## Inputs

| Input | Source | Read-level |
|---|---|---|
| kcnk5b sequence, 448 aa | `https://rest.uniprot.org/uniprotkb/Q6PFU3.fasta`. Header: `tr\|Q6PFU3\|Q6PFU3_DANRE Potassium channel, subfamily K, member 5 OS=Danio rerio GN=kcnk5b PE=2 SV=1` | full-text (the whole record was downloaded) |
| Q6PFU3 flat-file annotation | `https://rest.uniprot.org/uniprotkb/Q6PFU3.txt`. TRANSMEM 7–26, 116–137, 158–185, 229–250 (Phobius prediction, ECO:0000256). No INTRAMEM or MOTIF features are annotated. | full-text |
| Negative control and1 | UniProt search `gene_exact:and1 AND organism_id:7955` → E7F5V5 (Actinodin1 precursor, 570 aa) | full-text |
| Negative control and2 | UniProt search `gene_exact:and2 AND organism_id:7955` → A9JRX1 (508 aa) and A0ACM8QEN9 (Actinodin2 precursor, 508 aa) | full-text |
| Positive sanity check (my addition) | Human KCNK5 O95279 (Swiss-Prot, 499 aa) | full-text |

## Method and arithmetic

I counted overlapping matches with a lookahead regex: `re.finditer(r'(?=[TS].[GAS][YFL]G)', seq)`. Coordinates are 1-based, start = index + 1 and end = start + 4.

- Q6PFU3: matches at index 97 and 202 → positions 98–102 (TIGYG) and 203–207 (TVGFG). **Count = 2.**
- E7F5V5 (and1): 0. A9JRX1 (and2): 0. A0ACM8QEN9 (and2): 0.
- Human KCNK5 O95279: 2 matches, at 98–102 (TIGYG) and 203–207 (TIGFG).

**Inference (mine, not a source's claim):** the two filter motifs sit at the same positions in zebrafish and human. In zebrafish, P2 is TVGFG and in human it is TIGFG. Each motif comes just before a predicted TM helix (TM2 at 116, TM4 at 229), which matches the K2P layout M1-P1-M2-M3-P2-M4. UniProt does not annotate the pore loops for Q6PFU3, so I am placing them from the sequence alone.

**Scope of negative searches:** the zero results for and1/and2 apply only to the three UniProt entries listed above. I did not scan other isoforms or Ensembl translations.

## Comparison with the recorded value

I searched the repository for `TIGYG`, `TVGFG` and `kcnk5b`. The only kcnk5b hit is an unrelated line in `findings/gemini-triage-267-problems.json` (line 492, about a regeneration atlas). I found no prior working file. The only record I have is the claim text in my task prompt: exactly two motifs, TIGYG 98–102 and TVGFG 203–207, with and1/and2 returning 0. My count, motifs, coordinates and control results match it exactly.

**Verdict: AGREE.**

One caveat about independence: the prompt that withheld "the answer" also stated the motifs and coordinates. My derivation is independent in method and data, because I downloaded the sequences fresh and wrote my own scan. It was not blind to the expected result.

```swarm-replication
{"claim_id": 15, "my_value": "2 selectivity-filter motifs (TIGYG 98-102, TVGFG 203-207) in Q6PFU3 SV1; 0 in and1 E7F5V5 and and2 A9JRX1/A0ACM8QEN9", "agrees": true,
  "note": "My own regex scan of freshly downloaded UniProt sequences reproduces the count, motifs, coordinates and the zero results for the controls; the same motifs sit at the same positions in human KCNK5 (O95279), but the claim text was visible, so this check was not blind."}
```
