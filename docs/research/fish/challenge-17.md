# Challenge 17 — adversarial review of the PDB70 / Kcnk5 template claim

**Claim under review (author's words):** "PDB70 hits include 6WLV/6WM0, TASK-2, RCSB gene name
Kcnk5 -- the direct ortholog is present in the MSA. The hit set is the K+ superfamily, not
uniformly K2P."
Recorded evidence level: `literature`. Source: `msa_search_native`; 10 of 69 hits verified against
RCSB by the running agent.

**Verdict: WEAKENED.** The identity of the two entries holds up when checked against the primary
records. Four other parts of the claim do not hold as worded: the evidence label, "in the MSA",
"direct ortholog", and the count of 69 hits. Details follow.

## What I could and could not access

| Source | What I used it for | Read-level |
|---|---|---|
| `files.rcsb.org/header/6WLV.pdb`, `6WM0.pdb` | title, organism, gene, DBREF, citation | full-text (header records) |
| PDBe API `entry/molecules/6wlv` | gene name, organism, synonym | full-text (JSON record) |
| PDBe Solr search, `gene_name:KCNK*` (Kcnk, kcnk too) | count of K2P structures in the PDB | listing |
| UniProt FASTA: Q9JK62, Q32PR9, Q6PFU3, O95279, O14649, Q9NPC2, Q9H427, P57789, O95069, Q9NYG8, Q9HB14 | sequences for the identity calculation | full-text (sequence) |
| PubMed esearch "kcnk5b zebrafish fin" | why kcnk5b is the fish gene of interest | search-summary (titles only) |
| `data.rcsb.org` REST API | — | could-not-access (proxy refused, 403) |
| The `msa_search_native` run: its hit table, its MSA, and the 10 hits the agent checked | — | could-not-access. Nothing in this repo or on `origin/work/frontier-foundation` (`git grep` for pdb70, msa_search, kcnk5) |

Because I could not see the run's outputs, every statement below about the 69 hits is an inference
from public records. None of it comes from the run itself.

## 1. Facts checked against the primary records (OBSERVED in database records)

- **6WLV**: "TASK2 in MSP1D1 lipid nanodisc at pH 6.5". *Mus musculus*, GENE KCNK5, DBREF
  UniProt **Q9JK62** residues 1–335, SEQRES 343 aa.
- **6WM0**: "TASK2 in MSP1D1 lipid nanodisc at pH 8.5". Same organism, same gene, same DBREF
  (Q9JK62 1–335), SEQRES 344 aa.
- Both entries share one citation: Li, Rietmeijer & Brohawn, *Nature* 586:457 (2020), PMID 32999458,
  DOI 10.1038/s41586-020-2770-2.
- PDBe lists gene_name `Kcnk5` and synonym "Potassium channel TASK2" for 6WLV.

The author's identification ("6WLV/6WM0, TASK-2, gene Kcnk5") is **correct**. The author left out
the source species: these are **mouse** structures, not fish.

## 2. Arithmetic redone independently (CALCULATED by me, not measured)

These are Smith–Waterman local alignments with BLOSUM62 and gap penalties −11/−1. The script is
`docs/research/fish/challenge-17-aln.py`. Identity = identities / alignment columns, gaps included.
Treat these as rough figures. They are not a curated orthology call.

| Query (zebrafish) | Target | Identity (calculated) |
|---|---|---|
| kcnk5b (Q6PFU3, 448 aa) | mouse Kcnk5 1–335 (the 6WLV/6WM0 construct) | 181/311 = **58.2 %**, query span 1–311 |
| kcnk5a (Q32PR9, 513 aa) | mouse Kcnk5 1–335 | 218/311 = **70.1 %**, query span 1–309 |
| kcnk5b | human KCNK5 (O95279) | 212/456 = 46.5 % |
| kcnk5b | zebrafish kcnk5a | 233/447 = 52.1 % |
| kcnk5b | human TASK-1 / TASK-3 / TASK-5 / TREK-1 / TREK-2 / TRAAK / THIK-1 | 27–39 % |

So by sequence, Kcnk5 is clearly the closest K2P subfamily to either fish paralog. That supports
the author's orthology direction.

## 3. Defects

### D1 — The evidence level is mislabeled (honesty-floor defect)
`literature` is the wrong label. The claim is a **computed search result** (HHsearch-style hits
against a template database), plus a **database lookup** of 10 hits. No paper was read to
establish it. The correct label is computed/database-listing. A computed hit list presented as
literature is a defect even though the identification is right.

### D2 — Proxy: "present in the MSA" is backed by template hits
PDB70 is a **template** database. A PDB70 hit shows that the query profile aligns to that
structure. It does not show that the mouse Kcnk5 sequence is a **row in the query MSA**, which in
the usual pipeline is built separately (e.g. UniRef/BFD). The quantity that matters for "the
ortholog is present in the MSA" is MSA membership. That should be checked by finding a
Kcnk5-family sequence (Q9JK62 or another Kcnk5 co-ortholog) among the MSA rows and reporting its
coverage. I could not reach the MSA, so whether the MSA contains it is **unknown**. My inference:
it very likely does, because Kcnk5 orthologs are abundant in UniProt. But the stated evidence
(a PDB70 hit) does not establish it.

### D3 — "The direct ortholog" overstates the relationship
- Zebrafish has **two** Kcnk5 paralogs, kcnk5a and kcnk5b (UniProt listing). A single mouse gene is
  therefore at best a **co-ortholog** (1:2) of each. It is not "the direct ortholog" of either.
- If the query is kcnk5b, the gene in the fin-size literature (e.g. PMID 33830014, eLife 2021, and
  PMID 29991812, Sci Rep 2018; titles only), my calculated figures show the mouse template is
  **closer to kcnk5a (70 %) than to kcnk5b (58 %)**. kcnk5b is the more diverged paralog.
- The template construct covers mouse residues 1–335. It aligns to kcnk5b only over query residues
  ~1–311, so **about 137 C-terminal residues of kcnk5b (312–448) have no template coverage** from
  this hit (calculated from the alignment span).

### D4 — The hit list is internally inconsistent with the database name
6WLV and 6WM0 have the **same sequence** (the same Q9JK62 1–335 construct; SEQRES lengths differ
by 1). PDB70 clusters chains at 70 % identity and keeps one representative per cluster, so a
genuine PDB70 search should return **one** of these two, not both. There are two possible
explanations. (a) The database was not standard PDB70, for example an unclustered pdb_seqres. (b)
The hit table expands cluster members. Either way, **"69 hits" overstates how many independent
templates there are**, by an amount I cannot determine without the run.

### D5 — "Not uniformly K2P" rests on 10 of 69 hits
The superfamily statement is supported only by the 10 hits that were checked against RCSB. **The
other 59 (86 %) were not checked.**
- PDBe listing, my count: **117 PDB entries** carry a KCNK* gene name. They span KCNK1, 2 (human,
  mouse, zebrafish kcnk2a), 3, 4, 5, 6, 9, 10 and 13.
- In a truly 70 %-clustered PDB70, these collapse to roughly 10–15 representatives. That is my
  estimate; I did not run the clustering. Under that assumption, a 69-hit list *must* contain
  non-K2P hits, and the second sentence of the claim is true by counting alone.
- **If you relax that assumption**, which D4 suggests you should (the database looks unclustered),
  117 K2P entries are enough to fill 69 hits with K2P alone. "Not uniformly K2P" then holds only if
  at least one of the 10 checked hits was non-K2P. That is plausible (KcsA, Kir, Kv and MthK pore
  domains commonly appear), but I could not see which 10 were checked. **Not refuted, not
  independently confirmed.**

## 4. Things the author may have missed

- **Newer Kcnk5 templates exist.** PDBe lists five more mouse TASK-2 cryo-EM entries released
  October 2026: 10OY ("TASK-2 at pH 6.5"), 10PB ("TASK-2 L127N at pH 6.5"), 10PC, 10PD and 10PF
  (listing; I read titles for 10OY and 10PB only). A PDB70 build older than October 2026 would not
  contain them. 6WLV/6WM0 are no longer the only Kcnk5 templates. They are still mouse.
- **No fish Kcnk5 structure.** No *Danio rerio* KCNK5 entry exists. Scope of that negative: PDBe
  Solr, gene_name KCNK*/Kcnk*/kcnk*, searched 2026-11-04. The only zebrafish K2P structure found
  was kcnk2a (TREK-1): 8DE7, 8DE8, 8DE9, 9DBR.
- **pH state matters for a template.** 6WLV (pH 6.5) and 6WM0 (pH 8.5) were solved at different
  pH. Per the cited paper's title (pH gating of TASK2), they represent different gating states. The
  claim treats them as one hit, but a downstream structural use has to choose between them.

## 5. Corrected statement

> Template search (computed; database name and clustering unconfirmed) returned mouse Kcnk5/TASK-2
> structures 6WLV (pH 6.5) and 6WM0 (pH 8.5). Both are the same construct (UniProt Q9JK62 1–335,
> Li et al. 2020 Nature). Mouse Kcnk5 is a 1:2 co-ortholog of zebrafish kcnk5a/kcnk5b. Calculated
> local identity is ~58 % to kcnk5b (query 1–311) and ~70 % to kcnk5a. Whether a Kcnk5 sequence is
> in the query MSA is unverified. Superfamily composition beyond the 10 RCSB-checked hits is
> unverified.

The identification survives. "Direct ortholog", "in the MSA", the 69-hit count and the
`literature` label do not survive as written.

```swarm-challenge
{"claim_id": 17, "outcome": "weakened", "reason": "6WLV/6WM0 are confirmed mouse Kcnk5/TASK-2 (Q9JK62 1-335), but the evidence level is computed not literature, a PDB70 template hit is used as a proxy for MSA membership, mouse Kcnk5 is a 1:2 co-ortholog only ~58% identical (calculated) to zebrafish kcnk5b over residues 1-311, the duplicate 6WLV/6WM0 hits are inconsistent with a 70%-clustered PDB70, and the superfamily claim rests on 10 of 69 checked hits.", "corrected_value": "co-ortholog template, ~58% calculated local identity to kcnk5b over query residues 1-311 (~70% to kcnk5a); MSA membership unknown"}
```
