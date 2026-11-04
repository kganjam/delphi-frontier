# Challenge 81 — scope of the lat4a database negative

**Claim under review** (source given as `fish-alleles/README.md`, recorded evidence level `unknown`):

> "SCOPE OF THE NEGATIVE: the lat4a absence is against UniProtKB and NCBI Gene only. ZFIN was not reached (its documented API endpoint 404s and its web search 302s), and ZFIN may still carry lat4a as an alias"

**Verdict: WEAKENED.** The scope sentence holds for *Danio rerio*. I re-ran both searches and got the same empty result. But the claim gets wrong what the negative means. The missing thing is the symbol string `lat4a`, not the gene. The locus that Daane et al. 2021 call *lat4a* is present in both databases the claim did search, under the symbol `slc43a2a`. So the open question the claim leaves to ZFIN ("may still carry lat4a as an alias") does not need ZFIN to settle the gene's identity. Also, the ZFIN failure modes the claim reports (404 and 302) did not reproduce in this session. ZFIN failed here at TLS, before any HTTP status was returned.

Date of all probes: 2026-11-04. They ran from a cloud session through the session's agent proxy, using `curl` with the proxy CA bundle. TLS verification was never disabled.

## 0. The source file could not be read

`fish-alleles/README.md` does not exist on this branch. I checked every remote branch with `git ls-tree -r` on 300+ refs and found no path containing `fish-alleles`. `git log --all -S` finds no commit adding the strings "ZFIN was not reached", "web search 302" or "lat4a as an alias".
**Read-level of the claim's source: could-not-access.** This review therefore judges the claim's text as quoted. It cannot judge how the README uses that text.

## 1. Re-running the negative independently (observed)

| Query | Database | Result (observed) |
|---|---|---|
| `lat4a[All Fields] AND "Danio rerio"[Organism]` | NCBI Gene (E-utilities esearch) | count = 0 |
| `lat4a` (no organism) | NCBI Gene | count = 0 |
| `lat4a AND organism_id:7955` | UniProtKB REST | 0 rows |
| `lat4a` (no organism) | UniProtKB REST | 2 rows: Q1ELU5 (no gene name), **A0A9P6H1T5, gene name `LAT4A`, *Nosema granulosis*, "M-zodatoxin-Lt4a"** |
| full efetch XML of NCBI Gene 393221, case-insensitive grep for `lat4` | NCBI Gene | 0 occurrences |

The author's negative reproduces for zebrafish. Narrowing it is required, not optional: UniProtKB *without* an organism filter does contain an entry with gene name `LAT4A`. That entry is an unrelated microsporidian toxin. "Absence against UniProtKB" is true only as "absence against UniProtKB restricted to *Danio rerio* (taxon 7955)". The claim should say so.

## 2. Proxy check: symbol absence is standing in for gene absence

The quantity that matters is whether the gene the papers call *lat4a* is in these databases. The proxy actually measured is whether the string `lat4a` appears. The two come apart here.

**Sources:** Daane et al. 2021, *Curr Biol* 31:5052, PMC9172250. **Read-level: full-text.** The JATS body was retrieved with `efetch db=pmc` and searched in this session.

The author of that paper states the following:
- *nr21* "mapped to chromosome 15", with "a nonsynonymous mutation (T200K) in … the L-type amino acid transporter, lat4a".
- They cite mammalian Lat4 as Slc43a2 ("Essential amino acid transporter Lat4 (Slc43a2) …").
- They give the allele designations "lat4 nr21 (dmh26)" and "lat4a del (mh152)". Note that the paper itself writes both `lat4` and `lat4a`.
- They give five CRISPR gRNA sequences and one qPCR primer pair for *lat4a*.

**My test (calculated, not taken from the paper).** I fuzzy-matched the paper's gRNA spacers and qPCR primers against the zebrafish RefSeq mRNAs fetched in this session:

| Sequence (from the paper) | NM_200251.2 *slc43a2a* (3230 nt): min mismatches | NM_001008585.1 / XM_087269365.1 *slc43a2b*: min mismatches |
|---|---|---|
| gRNA 1 spacer `GCCCTGTACCGTTACCTGG` | 1 (− strand, pos 330) | 6 / 6 |
| gRNA 2 spacer `GTGAATGCCACAAGACTTG` | 1 (+, 378) | 7 / 6 |
| gRNA 3 spacer `GATGCCACAAGACTTGAGG` | 1 (+, 381) | 7 / 7 |
| gRNA 4 spacer `GCCACAAGACTTGAGGAGG` | **0** (+, 384) | 6 / 6 |
| qPCR F `ACGCAGGACGGCAATAAA` | 6 | 6 / 6 |
| qPCR R `GCTGAAGATACTCCGCATGAA` | 8 | 4 / 4 |

The single mismatch in gRNAs 1–3 is probably the 5′ G that is commonly added to a spacer for SP6/T7 transcription. That is my inference; I took each spacer to start at the first G after the SP6 promoter. Separately, NCBI Gene 393221 (*slc43a2a*) is on chromosome 15, which matches the paper's mapping. *slc43a2b* (494042) is on chromosome 10.

**My inference:** the gene Daane et al. call *lat4a* is zebrafish *slc43a2a*. That is NCBI Gene 393221, ZFIN ZDB-GENE-040426-964 (cross-referenced in that NCBI record), RefSeq NM_200251.2, and UniProtKB Q7ZUS0 / A0A8N7V006. Both UniProt entries are 153 aa, the fragment that commit `9ac01ecf` in this repo already flagged. The gRNA evidence and the chromosome evidence agree.

**Unresolved:** the qPCR primers match *neither* paralog's RefSeq mRNA (≥4 mismatches). I did not test genomic DNA, UTR variants or other transcript models. The primer evidence is therefore `unknown`, not contrary evidence.

The gene is present in NCBI Gene and UniProtKB. Only its use of the symbol `lat4a` is absent. A reader who takes "the lat4a absence" as "lat4a is not a registered gene" would be wrong.

## 3. Hidden assumption: ZFIN is the remaining source of uncertainty

The claim's caveat implies that only ZFIN could overturn the negative. With that assumption relaxed:

- **Gene identity** can be settled without ZFIN, as section 2 shows.
- **Alias status** still needs ZFIN for a direct answer. There is indirect evidence, and I label it as inference. The NCBI Gene record for *slc43a2a* cross-references ZFIN (`ZFIN:ZDB-GENE-040426-964`, retrieved in this session). Its alias list is `si:dkey-118k5.2, slc43a2, zgc:56271`, with no `lat4a`. NCBI's zebrafish nomenclature is generally sourced from ZFIN, so this weakly suggests ZFIN had no `lat4a` alias at the last sync. It does not prove it: sync lag, or ZFIN keeping a paper-specific name only on the allele or feature records (`dmh26`, `mh152`), would both escape this check. The claim's "may still carry" hedge is therefore fair and stays open.

## 4. Evidence level and the ZFIN failure mode

The claim's evidence level is recorded as `unknown`. That is honest only in the sense that it overclaims nothing. The parts of the claim are of three kinds:
- The UniProtKB and NCBI Gene negatives are **observations** of search results. I reproduced them.
- "ZFIN may still carry lat4a as an alias" is an **untested possibility**.
- The ZFIN failure modes are **observations that did not reproduce**.

**Observed in this session:** every ZFIN URL I tried failed with `curl: (60) SSL certificate problem: unable to get local issuer certificate`, before any HTTP status. The URLs were the root, `/action/quicksearch`, `/search`, `/action/api/marker/…`, a `ZDB-GENE` page, `/downloads/aliases.txt` and others. The repo's own earlier probe, `docs/research/fish/S11-network-and-alleles.md` (commit c6fadebd, same date), recorded the same TLS failure.
**The two sources disagree, and I am not reconciling them.** The claim reports a 404 from the API and a 302 from the web search. I could not reproduce either status: under this network policy no HTTP response reached me at all. The claim's session may have had a different route to ZFIN. Its concrete status codes remain unverified, and I report them as `unknown`, not as wrong.

Mirrors that might have stood in for ZFIN were also unreachable here: Alliance of Genome Resources API and Ensembl REST both returned proxy `CONNECT tunnel failed, response 403`.

## 5. Counter-examples and regimes

- **Taxon scope:** UniProtKB contains `LAT4A` outside *Danio* (*Nosema granulosis*, A0A9P6H1T5). The negative is taxon-scoped and should say so.
- **Naming regime:** the primary paper itself uses both `lat4` and `lat4a`. A symbol search that misses the gene is the expected outcome when a paper uses a functional name (LAT4) instead of the HGNC-style family symbol (SLC43A2). The same naming problem was recorded for kcnh2a earlier in this repo (commit `892c7f71`).

## Scope of my own negatives

- No `lat4a` in NCBI Gene: queries `lat4a` and `lat4a[All Fields] AND "Danio rerio"[Organism]`, esearch db=gene, 2026-11-04.
- No `lat4a` in UniProtKB for taxon 7955: REST `/uniprotkb/search`, 2026-11-04. Not checked: UniParc, UniRef.
- No `lat4` string in the NCBI Gene 393221 XML: that single record only.
- ZFIN, Alliance and Ensembl were not reached. Nothing here rules out a ZFIN alias.

## Sources and read-levels

| Source | Read-level |
|---|---|
| `fish-alleles/README.md` (claim's source) | could-not-access |
| Daane et al. 2021, *Curr Biol* 31:5052, PMC9172250 | full-text |
| NCBI Gene 393221 (*slc43a2a*), 494042 (*slc43a2b*) | full record (esummary + efetch XML) |
| RefSeq NM_200251.2, NM_001008585.1, XM_087269365.1 | full sequence |
| UniProtKB search results; A0A9P6H1T5 entry | listing |
| `docs/research/fish/S11-network-and-alleles.md` (repo) | full-text |
| ZFIN, Alliance, Ensembl REST | could-not-access |

```swarm-challenge
{"claim_id": 81, "outcome": "weakened", "reason": "The UniProtKB/NCBI Gene negative reproduces only when scoped to Danio rerio and only for the symbol string: the gene Daane et al. call lat4a is present in both databases as slc43a2a (NCBI Gene 393221, chr15; four of the paper's gRNA spacers match NM_200251.2 at 0-1 mismatches vs 6-7 for slc43a2b), and the claimed ZFIN 404/302 did not reproduce (TLS failure here instead), so ZFIN is needed only for alias status, not gene identity.", "corrected_value": "Symbol 'lat4a' absent from NCBI Gene and UniProtKB (taxon 7955) as of 2026-11-04; the locus itself is present as slc43a2a (NCBI Gene 393221, ZDB-GENE-040426-964, UniProtKB Q7ZUS0 153-aa fragment); ZFIN alias status unknown", "depends_on": ["NCBI E-utilities esearch db=gene for 'lat4a' returned 0 (2026-11-04)", "UniProtKB REST search 'lat4a AND organism_id:7955' returned 0; unfiltered search returned A0A9P6H1T5 (Nosema granulosis, gene LAT4A)", "Daane et al. 2021 Curr Biol PMC9172250 full text: lat4a/nr21 mapped to chromosome 15; gRNA spacer sequences as printed in its key resources table", "NCBI Gene 393221 slc43a2a on chromosome 15, aliases si:dkey-118k5.2/slc43a2/zgc:56271, xref ZFIN:ZDB-GENE-040426-964", "RefSeq NM_200251.2 (slc43a2a) and NM_001008585.1 / XM_087269365.1 (slc43a2b) sequences as fetched 2026-11-04", "Fuzzy-match computation of gRNA spacers against those mRNAs (calculated in this review)", "ZFIN probes in this session failed with curl error 60 (TLS), matching docs/research/fish/S11-network-and-alleles.md"]}
```
