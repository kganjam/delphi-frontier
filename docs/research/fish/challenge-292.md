# Challenge 292: slc43a2a (lat4a) residue 200 and the T200K allele

**Verdict: WEAKENED.** The main claim holds: residue 200 is T in both Ensembl isoforms, and I reproduced that from a different endpoint. One secondary statement in the claim is wrong. The 153 aa UniProt/RefSeq sequences are not "truncated fragments" of the long protein. They match it for residues 1–139 and then end in a different 14-residue C-terminal tail. The claim's practical conclusion still stands: a 153 aa product has no residue 200, so the allele cannot be named against it.

## What I checked (date read: 2026-11-04)

| Source | What I did | Read-level |
|---|---|---|
| Ensembl REST (`rest.ensembl.org`) | The author's own endpoint. **could-not-access**: the session's egress proxy refused it (CONNECT 403). I did not re-run the author's exact query. | could-not-access |
| UniParc `UPI00062E34B4` | Cross-ref `Ensembl ENSDARP00000138218` (active, taxon 7955, gene slc43a2a); 577 aa | full record (sequence) |
| UniParc `UPI000188A62B` | Cross-ref `Ensembl ENSDARP00000120945` (active), also VEGA `OTTDARP00000030624`; 571 aa | full record (sequence) |
| UniProtKB search `gene:slc43a2a AND organism_id:7955` | Returns only Q7ZUS0 and A0A8N7V006, both 153 aa. The `Fragment` field is **empty** for both | listing |
| NCBI protein esearch `slc43a2a[gene] AND txid7955[orgn]` | Returns only `NP_956545.1` (153 aa, from `NM_200251.2` / MGC mRNA `BC047854`). Its GenPept record cites Daane et al. 2021 | listing + GenPept record |
| Daane et al. 2021, Curr Biol 31:5052, PMID 34534441, PMC9172250 | Pulled the full text through NCBI efetch (db=pmc) | full-text |

## 1. Arithmetic redone independently

I indexed the UniParc sequences myself, 1-based (Python `s[199]`):

- ENSDARP00000138218 (577 aa): residues 195–205 are `A S S A V [T] F P G I K`. **Residue 200 is T.**
- ENSDARP00000120945 (571 aa): the same window, `A S S A V [T] F P G I K`. **Residue 200 is T.**
- The two isoforms differ only by a 6-residue deletion at long-isoform positions 367–372 (`EMMEMV`). That is downstream of 200, so both isoforms give the same numbering at residue 200.

The lengths 577 and 571 agree with the claim. These are observations from database records, not calculations.

*Caveat about independence:* UniParc stores the same Ensembl peptide sequences, so this is a second retrieval path for the same gene model. It is not independent biological evidence.

## 2. Proxy check

The quantity that matters is the residue Daane et al. mutated in the nr21 line. The author's proxy is the residue at position 200 of today's Ensembl GRCz11 model. The paper's full text says only "a nonsynonymous mutation (T200K) in a conserved domain of … lat4a". It does not name the transcript or protein accession used for numbering. It refers to the reference genome as "Zv11". So which isoform the paper numbered against is **unknown** from the full text. This only matters for a reference whose N-terminal 200 residues differ from these models. The two current long isoforms agree up to residue 366, so the proxy is adequate for them.

## 3. Hidden assumption, tested relaxed

**Assumption: "T at position 200" validates the numbering convention.** Threonine makes up 35 of 577 residues (6.1%) of the long isoform, so a random position would show T about 6% of the time. A single match is therefore modest evidence on its own. I relaxed it by checking the neighbouring positions: 199 is V and 201 is F. An off-by-one convention (0-based, or counting from a different Met) would not give T. The control does discriminate against ±1 shifts, but not against a different isoform or reference with an unrelated offset. Daane's Fig. 3C shows an alignment of the conserved domain, but I could not see the figure image, so I could not check it residue by residue.

## 4. Evidence level

The author labelled this "measured". It is a direct read-out of a database record. Nothing in it was derived or simulated, so it is not mislabelled as calculated. Strictly, though, the record is a *computational gene model* (Ensembl annotation), not a measured protein sequence. I count this as a minor labelling looseness, not a defect.

## 5. Counter-evidence the author missed: the "truncated fragments" characterisation

The author claims the 153 aa entries are "truncated fragments". This is my own comparison, observed directly from the sequences:

- Residues 1–139 of the 153 aa sequence (Q7ZUS0 = A0A8N7V006 = NP_956545.1) match the long isoforms exactly.
- After residue 139 they diverge:
  - short, 131–153: `ASFAISCILNSVTRTASVQLYYQ*`
  - long, 131–160: `ASFAISCILISYGASDPQNLSILIFFALAL…`
- A truncated fragment would be a prefix of the long protein. This sequence is not one: its residues 140–153 are absent from the long protein at that position.
- UniProt does **not** flag either 153 aa entry as a fragment (empty `Fragment` field). NCBI's curated RefSeq protein for this gene (NP_956545.1) is the same 153 aa product, translated from a full-length MGC cDNA.

My inference, which I have not verified: the 153 aa product most likely comes from an alternative or intron-retaining transcript with its own stop codon. It is a complete CDS from a real cDNA, not an incomplete entry. The claim's main point is unaffected: the allele must be numbered against the long product, because the short one has no residue 200.

Two more points the claim does not mention:

- The long-isoform UniProt entries do exist, but are inactive/obsolete in UniParc: A0A0R4IP58 (↔ ENSDARP00000138218) and F1Q5Y9 (↔ ENSDARP00000120945).
- NCBI's only RefSeq protein for this gene is also the short one. Scope of that search: NCBI protein esearch, `slc43a2a[gene] AND txid7955[orgn]`, and a name search for "solute carrier family 43 member 2a" in txid7955. Both returned only NP_956545.1.

So the *reference* NCBI product for this gene is the short isoform. Anyone using RefSeq coordinates would hit the same "no residue 200" problem. The claim's warning should cover RefSeq as well as UniProt.

## Bottom line

- **Survives:** residue 200 is T in ENSDARP00000138218 (577 aa) and in ENSDARP00000120945 (571 aa). This is consistent with the wild-type residue in T200K (Daane et al. 2021, full text), and ±1 positions do not give T.
- **Wrong:** "truncated fragments". The 153 aa sequences are a complete alternative product that shares residues 1–139 and has a distinct C-terminal tail. They are not flagged as fragments, and the same product is the current RefSeq NP_956545.1.
- **Unknown:** which accession Daane et al. numbered against. The text does not state it, and I did not see Fig. 3C.

```swarm-challenge
{"claim_id": 292, "outcome": "weakened", "reason": "Residue 200 is T in both Ensembl isoforms (reproduced via UniParc; neighbours V199/F201), but the 153 aa entries are not truncated fragments: they share residues 1-139 then carry a distinct 14-aa C-terminal tail, are unflagged as fragments in UniProt, and equal the current RefSeq NP_956545.1.", "corrected_value": "Residue 200 = T (unchanged); the 153 aa sequences (Q7ZUS0, A0A8N7V006, NP_956545.1) are an alternative short product diverging after residue 139, not truncated fragments", "depends_on": ["UniParc UPI00062E34B4 sequence (xref Ensembl ENSDARP00000138218, 577 aa), read 2026-11-04", "UniParc UPI000188A62B sequence (xref Ensembl ENSDARP00000120945, 571 aa), read 2026-11-04", "UniProtKB Q7ZUS0 / A0A8N7V006 sequences and empty Fragment field, read 2026-11-04", "NCBI RefSeq NP_956545.1 (153 aa, from NM_200251.2), read 2026-11-04", "Daane et al. 2021 Curr Biol 31:5052 (PMC9172250) full text: nr21 = T200K in lat4a, no reference accession stated"]}
```
