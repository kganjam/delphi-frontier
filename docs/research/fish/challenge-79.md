# Challenge 79: does `lat4a` really not resolve for *Danio rerio*?

**Verdict: SURVIVED.** I could not break the claim. I reran the author's query and four stricter forms of it. All of them return 0 records for `lat4a` in zebrafish, and alias lookups that should succeed do succeed. One caveat below limits what the zero can be used for later (see "Scope").

## The claim under review (the author's words, not mine)

> "The gene symbol `lat4a` used by Daane et al. does not resolve in UniProtKB or NCBI Gene for Danio rerio. Four positive controls (kcnh2a, slc43a2a, slc43a2b, kcnk5b) all resolved with the same query form, so the zero is a real absence and not a malformed query."
> Evidence level: measured. Value: 0 hits. Source: `fish-alleles/README.md`. Query: `<symbol>[Gene Name] AND "Danio rerio"[Organism]`.

I could not find `fish-alleles/README.md` on any branch of this repository (I listed the tree of every `origin/*` branch). So I am judging the claim as quoted in the challenge, not as it stands in that file. Read-level of the source: **could-not-access**.

## 1. Independent re-run (measured, 2026-11-04)

All rows are live queries I ran myself. NCBI = E-utilities `esearch`, `db=gene`. UniProt = `rest.uniprot.org/uniprotkb/search`.

| Query | Hits | Record |
|---|---|---|
| NCBI `lat4a[Gene Name] AND "Danio rerio"[Organism]` (the author's form) | **0** | — |
| NCBI `lat4a[sym] AND "Danio rerio"[Organism]` | 0 | — |
| NCBI `lat4a[Gene/Protein Name] AND "Danio rerio"[Organism]` | 0 | — |
| NCBI `lat4a[All Fields] AND "Danio rerio"[Organism]` | 0 | — |
| NCBI `lat4[All Fields] AND "Danio rerio"[Organism]`, and `lat4b`, `lat4` with `[Gene Name]` | 0 each | — |
| UniProt `gene:lat4a AND organism_id:7955` / `gene_exact:lat4a …` / free text `lat4a …` / `lat4 …` | 0 each | — |
| NCBI controls `kcnh2a`, `kcnk5b`, `slc43a2a`, `slc43a2b` (`[Gene Name]`) | 1 each | 563802, 393606, 393221, 494042 |
| UniProt controls `gene:kcnh2a`, `kcnk5b`, `slc43a2a`, `slc43a2b` | ≥2 each | e.g. Q108P2, Q6PFU3, Q7ZUS0, Q5PR35 |

**The 0 reproduces exactly** (it is a count, so there is no arithmetic to redo). The four positive controls reproduce too.

## 2. Hidden assumption tested: is the query form able to find an alias at all?

The author's four controls are all **official symbols**. They show that the query form finds official symbols. They do not show that it would find `lat4a` if `lat4a` were stored as an *alias*, which is the most likely way a paper-specific name would be recorded. If `[Gene Name]` ignored aliases, the zero would mean nothing. That is the assumption the claim rests on, and the claim does not test it.

I tested it with alias-only controls, using the same query form:

- `lat3a` is **only an alias** of zebrafish `slc43a1a` (NCBI Gene 334395, aliases: `fi47a12, lat3a, slc43a1, wu:fi47a12, zgc:55850`). `lat3a[Gene Name] AND "Danio rerio"[Organism]` gives **1 hit, 334395**. UniProt `gene:lat3a AND organism_id:7955` gives **F2Z4V7 (slc43a1a)**.
- `zgc:56271` is an alias of `slc43a2a`. `zgc:56271[Gene Name] …` gives **1 hit, 393221**.
- Human `LAT4[sym] AND human[orgn]` gives **124935 = SLC43A2** (alias `LAT4`). The alias exists in the human record but not in the zebrafish record.

So the query form *does* search aliases, in both databases. The assumption holds when relaxed, and the zero is a real absence of the string `lat4a` from NCBI Gene and UniProtKB for zebrafish, as symbol and as alias. This makes the claim *stronger* than the author showed. It does not change its value.

## 3. Proxy check: symbol absence is not gene absence

"The symbol does not resolve" is a statement about **nomenclature**, and the claim is correctly limited to that. Downstream use must not read it as "the gene is not in the databases". The gene behind the name is present (my inference, from the sources below):

- Daane et al. 2021, *Curr Biol*, doi:10.1016/j.cub.2021.08.054, PMC9172250. Read-level: **full-text** (PMC HTML). They describe `lat4a` as "the L-type amino acid transporter", mapped as nr21 "to chromosome 15", with "a nonsynonymous mutation (T200K)". Their ref. 17 is titled "Essential amino acid transporter Lat4 (Slc43a2)". The text never writes `slc43a2a`, and I found no zebrafish accession in it (I searched for `slc43`, `ENSDAR`, `ZDB-`).
- NCBI Gene (measured): `slc43a2a` (393221) is on **chr 15**. `slc43a2b` (494042) is on **chr 10**.
- Residue check (my inference; computed by me from a **repo-cached** file, not checked against live Ensembl, because `rest.ensembl.org` did not answer from this container): in `origin/work/genomics:data/genomics/artifacts/ensembl_protein_ENSDARP00000120945.fasta` (571 aa), residue 200 = **T** and residue 326 = **F**. That matches the paper's T200K and the convergent F326 site. The slc43a2b model ENSDARP00000156564 has M at 200 and D at 326. I did not confirm that ENSDARP00000120945 is a translation of slc43a2a's Ensembl gene. Its FASTA header carries no gene id.
- This agrees with the project's own `lat4a_resolution_v3.json` on `work/genomics`. That file reaches slc43a2a (ZDB-GENE-040426-964) through supplement naming plus Ensembl orthology. My chr-15 and residue-200 checks are independent of that chain. The file also says the residue numbering "was not re-derived" because RefSeq NP_956545.1 is 153 aa. The Ensembl model above gives T200 under the paper's numbering (inference, from cached data).

**A related fault worth recording** (it does not break claim 79): UniProtKB's two `slc43a2a` entries (Q7ZUS0, A0A8N7V006) and RefSeq NP_956545.1 are all **153 aa fragments** (measured). So even after `lat4a` is translated to `slc43a2a`, neither UniProt nor RefSeq protein gives a sequence that covers T200 or F326. That is a coverage gap, not a nomenclature gap. Any claim that "slc43a2a resolves in UniProt, therefore its residues can be checked there" would be wrong.

## 4. Evidence level

"Measured, 0 hits" is honest. It is a direct database count, and it reproduces. The only thing that is not measured is the phrase "the zero is a real absence". The author inferred it from controls that could not test aliases. It now has direct support from the alias controls in §2.

## 5. Counter-examples and regimes searched

- **ZFIN**, the authoritative zebrafish nomenclature source, was **not reachable** from this container (HTTP 000 on `zfin.org`). I cannot say whether ZFIN lists `lat4a` as a previous name or alias. Status: `unknown`. The claim names only UniProtKB and NCBI Gene, so this is outside its scope, but nobody should widen the claim to "no database".
- Europe PMC full-text search `lat4a AND (slc43a2a OR slc43a2)` gives 3 papers (listing-level). One is Daane 2021. I did not find a paper that registers `lat4a` as a zebrafish gene symbol.
- Time dependence: these are live databases. The zero holds as of 2026-11-04 and can change.

## Scope of the negative

Databases: NCBI Gene, UniProtKB (Swiss-Prot + TrEMBL). Organism: *Danio rerio* (taxon 7955) only. Strings: `lat4a`, `lat4b`, `lat4`. Fields: `[Gene Name]`, `[sym]`, `[Gene/Protein Name]`, `[All Fields]`, UniProt `gene:`, `gene_exact:`, free text. Not searched: ZFIN (unreachable), Ensembl (unreachable), other taxa (except the human `LAT4` control).

```swarm-challenge
{"claim_id": 79, "outcome": "survived", "reason": "The 0-hit result reproduces in NCBI Gene and UniProtKB under the author's query and four broader forms, and alias-only controls (lat3a->slc43a1a, zgc:56271->slc43a2a) show the query form does search aliases, so the zero is a real nomenclature absence; it is not evidence the gene (slc43a2a, chr15) is missing.",
  "corrected_value": null,
  "depends_on": ["NCBI E-utilities esearch db=gene, 2026-11-04: lat4a 0 hits under [Gene Name], [sym], [Gene/Protein Name], [All Fields] for Danio rerio", "UniProtKB REST search, 2026-11-04: lat4a 0 hits for organism_id:7955 (gene:, gene_exact:, free text)", "alias controls: lat3a[Gene Name] -> NCBI Gene 334395 (slc43a1a) and UniProt F2Z4V7; zgc:56271[Gene Name] -> 393221", "NCBI Gene 393221 slc43a2a chromosome 15; 494042 slc43a2b chromosome 10", "Daane et al. 2021 Curr Biol doi:10.1016/j.cub.2021.08.054 (PMC9172250, full-text): lat4a nr21 mapped to chr15, T200K", "repo-cached origin/work/genomics:data/genomics/artifacts/ensembl_protein_ENSDARP00000120945.fasta residue 200 = T (not live-verified)"]}
```
