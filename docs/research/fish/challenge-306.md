# Challenge 306 — adversarial review

**Claim under review (not mine):** that a ColabFold `pdb70_220313` search over the full 577 aa
ENSDARP00000138218 (zebrafish *slc43a2a*) returned 5 structural homologues with maximum
per-position depth 2, median depth 0, and 474/577 positions at zero coverage, residue 200 and
all of 195–205 among them; and therefore (a) no conservation argument about T200K can be drawn
from PDB70, (b) "any MSA-dependent structure prediction will be weakly supported there", and
(c) low depth is evidence about structural coverage of this transporter family but not about
evolutionary conservation.

**Recorded evidence level:** measured. **Recorded value:** 0 aligned PDB70 hits at residue 200.

**Verdict: WEAKENED.** The headline number survives — and an independent literature check
makes it *more* credible, not less. Two of the three downstream sentences do not survive: the
consequence sentence generalises a template-database measurement to MSA-driven prediction,
which the pipeline's own source code contradicts and which the claim's own scope paragraph
contradicts; and the scope sentence's present-tense statement about the family's structural
coverage is stale by roughly four years. The reported method, read literally, also cannot
produce the reported median.

---

## 0. What I could and could not access

| Source | Read level |
|---|---|
| Zhou et al., "Structures of the neutral amino acid transporter LAT4…", *EMBO J* 2026;45(12):4283–4298, PMC13269557 | full-text (first ~100k of ~128k characters retrieved) |
| Mirdita et al., "ColabFold: making protein folding accessible to all", PMC9184281 | full-text (targeted quotation) |
| ColabFold source, `colabfold/mmseqs/search.py`, `main` branch | full-text |
| ColabFold `README.md`, `main` branch | full-text |
| General search for SLC43A2/LAT4 structures | search-summary |
| ENSDARP00000138218 protein sequence, Ensembl REST | **could-not-access** — `rest.ensembl.org` is not an allowed host in this session's network settings (`connect_rejected` through the egress proxy, and `ENOTFOUND` via the fetch service) |
| The returned a3m, and Nebius operation `op-95b6ef92728e409b` | **could-not-access** — the a3m is not committed anywhere in this repository (searched the full tree for `slc43a2a`, `ENSDARP00000138218`, `pdb70`, `*.a3m`, `msa_search_native`: no hits outside unrelated KCNE1 files), and I have no credentials for that API |

**Consequence of the last two rows, stated plainly:** I did not re-measure anything. Every depth
figure below is the author's, taken as given. I could not independently confirm that
ENSDARP00000138218 is 577 aa or that its residue 200 is T; those rest entirely on the author's
stated positive control. What follows is an audit of internal consistency, of the inference
chain, and of the claim against the published record — not a replication.

## 1. Arithmetic, redone from the stated inputs

Worked from the claim's four numbers only (577 positions, max depth 2, median depth 0, 474
zero-coverage positions). These are *my* derivations, not observations.

**(a) Covered columns.** 577 − 474 = **103** columns carry at least one aligned residue, i.e.
17.85% of the query. Consistent with the claim; the claim does not state this figure, and it is
the more informative one.

**(b) Is median 0 attainable?** For 577 values (odd), the median is the 289th order statistic, so
the median is 0 iff at least 289 columns are 0. 474 ≥ 289. **Consistent.**

**(c) Is max depth 2 attainable with 5 hits?** Total aligned (non-gap) homologue characters
summed over all columns is bounded by (max depth) × (covered columns) = 2 × 103 = **206**. Spread
over 5 hits, the mean aligned length per hit is at most 206/5 = **41.2 columns**, i.e. ≤ 7.1% of
the 577 aa query. **Consistent — but only if all five "structural homologues" are very short
local alignments.** Five full-length family homologues are arithmetically impossible under the
reported statistics. This is not an error, but "5 structural homologues" is a generous label for
≤ ~41-column mean fragments, and a reader who takes "homologue" at face value will overestimate
what was found. Report the per-hit aligned lengths instead.

**(d) The query row — the one real inconsistency.** The stated method is "skipping lowercase
insertion columns and counting non-gap characters per query column." In a ColabFold a3m the first
row *is* the query, and by construction it has a residue in every query column. Counted as
written, every one of the 577 columns would have depth ≥ 1: zero-coverage columns would be **0,
not 474**, the median would be ≥ 1, not 0, and the maximum would be 3, not 2. The four reported
numbers are mutually consistent **only** under query-excluded counting, which the method sentence
does not state. The headline value ("0 aligned PDB70 hits at residue 200") is the
query-excluded reading, so the finding itself is fine — but the method as written does not
reproduce the author's own numbers, and anyone re-running it from that sentence will get 1, 3 and
0 where the claim says 0, 2 and 474. **Fix: say "excluding the query row" in the method.**

## 2. The proxy — this is the substantive break

**PDB70 depth is standing in for two different quantities, and it is the wrong proxy for one of
them.**

In the ColabFold pipeline, PDB70 is the **template** database and nothing else. The MSA is built
from UniRef30 plus the environmental database. The Nature Methods paper separates the two
explicitly — *"AlphaFold2 searches with HHsearch through a clustered version of the PDB (PDB70)
to find the 20 top ranked…"*, *"we use MMseqs2 to search against the PDB70 cluster
representatives as a prefiltering step"*, *"The accepted templates are given to AlphaFold2 as
input features"* — against *"It searches the sequence(s) with three iterations against the
consensus sequences of the UniRef30"* and *"We use the UniRef30 sequence profile to perform an
iterative search against the BFD/MGnify or ColabFoldDB."*

The source code is blunter still. In `colabfold/mmseqs/search.py` on `main`:

```python
uniref_db: Path = Path("uniref30_2302_db"),
template_db: Path = Path(""),  # Unused by default
metagenomic_db: Path = Path("colabfold_envdb_202108_db"),
...
use_templates: bool = False,
```

and in the argument parser, `# dbs are uniref, templates and environmental` / `# We normally
don't use templates`, with `--use-templates` defaulting to `0`. The paper's own benchmarks say
*"All three ColabFold modes were executed without templates"* and *"For benchmarking, no
templates are given to ColabFold."*

So:

- **The author's claim** is that "any MSA-dependent structure prediction will be weakly supported
  there."
- **My inference from the pipeline source:** that does not follow. A default ColabFold run never
  reads PDB70 at all, and even with templates enabled PDB70 contributes template features, not
  MSA rows. Per-position PDB70 depth therefore places no bound on the MSA that drives the
  Evoformer, and hence none on pLDDT at residue 200. The claim's reassuring corollary — "low
  predicted confidence at residue 200 would mean the alignment ran out, NOT that the region is
  disordered" — is an inference about a *different alignment* than the one measured, and is
  unsupported by this measurement in either direction.

The claim half-knows this: its scope paragraph says "a UniRef or BFD search could still be deep."
That sentence and the consequence sentence cannot both be true. The scope paragraph is the
correct one; the consequence paragraph should be struck.

**The right quantities, named:**

| Question actually at stake | Right measurement |
|---|---|
| Will AF2/ColabFold be confident at residue 200? | per-position depth **and** per-position effective sequence count (Neff) of the UniRef30 + ColabFoldDB a3m — the `final.a3m` the pipeline actually feeds the model |
| Can a conservation argument be made about T200K? | per-position depth and entropy in a UniRef/OrthoDB/vertebrate-orthologue alignment, plus the identity of the aligned column across orthologues |
| Is a structural template available at residue 200? | a search against a **current** PDB / PDB100, not a 2022 snapshot (see §4) |

The claim's final sentence — "This measurement bounds what can be concluded, it does not conclude
anything about the residue" — is the right instinct, and the second and third rows above are
consistent with it. The first row is where the claim overreaches its own stated discipline.

## 3. The hidden assumption, relaxed

**The assumption:** that the returned hit set is an exhaustive census of PDB70 at each position,
so that depth 0 at column 200 means "PDB70 contains nothing alignable there."

**Relaxed, it weakens the measurement in a way the stated controls cannot detect.** The two
positive controls both test *column indexing* (query row byte-identical; residue 200 is T). Both
are good controls for the numbering question, and I accept them for that. Neither is a control on
**search sensitivity**. Nothing in the record shows that this pipeline call *can* return deep
coverage for a query that has deep coverage available. Without that, a 5-hit return is
unidentifiable between three causes:

1. PDB70 genuinely has nothing (what the claim concludes);
2. the search was run at low sensitivity, a strict E-value, or a capped hit count;
3. the returned object was truncated or post-filtered by the wrapping service.

Cause 2 is not hypothetical for this database. ColabFold's own PDB70 step runs with `-e 0.1` and
is explicitly a *prefilter*, after which only *"the top 20 target templates according to E-value
are then aligned by HHsearch."* A hit ceiling of 20 and a 0.1 E-value cutoff make "per-position
PDB70 depth" a capped, thresholded statistic by construction, not a census. Note also that
ColabFold's PDB70 step emits a tabular `.m8` file, while the MSA path emits the a3m; a service
that returns an a3m for a pdb70 search is doing something adjacent to, not identical with,
ColabFold's template step, which is one more reason not to treat the returned object as a
complete enumeration.

**What would fix it, cheaply:** one run of the identical call on a query with a known close PDB
relative, reported beside the negative result. If that control returns depth in the tens, cause 1
is isolated and the claim strengthens considerably. I could not run it — no API access.

## 4. The counter-example the author missed: the snapshot is four years stale

`pdb70_220313` is a **2022-03-13** snapshot. That date is load-bearing and the claim never
mentions it.

Structures of the direct human orthologue now exist. Zhou et al., *The EMBO Journal*
2026;45(12):4283–4298 (received 2025-08-18, revised 2026-03-16, accepted 2026-03-27, published
2026-05-04; PMID 42082777, PMCID PMC13269557) report cryo-EM structures of human LAT4/SLC43A2 —
**PDB 9JBS** (apo, 2.9 Å), **9JBT** (phenylalanine-bound, 3.2 Å), **9JBU** (digitonin, 3.8 Å),
EMDB EMD-61324/61325/61326 — and of the family member human ENBT1/SLC43A3, **PDB 9L38**
(EMD-62783). A database frozen in March 2022 cannot contain structures from a study accepted in
March 2026.

This cuts both ways, and I want both halves on the record because they disagree in tone:

- **It corroborates the measurement.** The paper's introduction frames the work as addressing
  *"the lack of detailed structural insights into the LAT4 transport mechanism"* and states *"Here,
  we report a series of SLC43 family transporter structures determined by cryo-electron
  microscopy"* — language consistent with no SLC43 family structure having been solved before.
  (The paper does not state this as an explicit negative, so this is my reading of its framing,
  not its assertion.) If so, a 2022 PDB70 genuinely had no SLC43 member, and five short
  fragmentary hits with median depth 0 is exactly the expected result. The author's number looks
  right, for the stated reason.
- **It refutes the scope sentence as written.** "Low depth here is evidence about structural
  coverage of this transporter family" is true only in the past tense: it is evidence about the
  family's structural coverage **as of 2022-03-13**. Present-day structural coverage of SLC43 is
  not zero, and the practical corollary the claim draws — that template-dependent work on this
  transporter is unsupported — is now false. A current PDB/PDB100 search, or an explicit
  alignment of zebrafish *slc43a2a* to human SLC43A2 over 9JBS, is the available and much more
  informative measurement. Whether residue 200 falls in a modelled region of 9JBS, and what the
  aligned human residue is, I did not determine — zebrafish-to-human alignment needs the
  zebrafish sequence, which I could not retrieve (§0). That is the obvious next experiment, and it
  is cheap.

I am deliberately not asserting a zebrafish/human identity figure or an aligned human residue for
position 200. Both are **unknown** to me, and inventing either would be worse than leaving the gap.

## 5. Is the evidence level honest?

Mostly, with one imprecision worth correcting.

- "0 aligned PDB70 hits at residue 200" as **measured** is defensible: it is a direct read of one
  column of a returned file, backed by an operation id and a named database build.
- The distribution statistics — max 2, median 0, 474 zero columns — are **derived** from that file
  by the author's own counting script. Labelling the whole bundle "measured" blurs a deterministic
  read (fine) with a script output whose one stated implementation detail does not reproduce its
  own numbers (§1d). The honest label is "measured (search, op-95b6ef92728e409b) + derived
  (per-position depth statistics, query row excluded)."

This is a labelling fix, not a fabrication, and I am not scoring it as a violation. The claim is
unusually careful about scope elsewhere — the final sentence in particular — and its failure is
over-generalisation in one paragraph, not dishonesty.

## 6. Scope of my negative searches

- Repository: full tree search (excluding `.git`) for `slc43a2a`, `ENSDARP00000138218`, `pdb70`,
  `msa_search_native`, `colabfold`, `nebius`, `challenge-*`, `*.a3m`. The only hits were unrelated
  KCNE1 preregistration/result files. No prior record of claim 306, and no copy of the a3m.
- Literature: one search for SLC43A2/LAT4 structural work (search-summary), followed by full-text
  retrieval of the single directly relevant paper. I did **not** systematically search for
  pre-2022 structures of more distant relatives that might share the fold, so "PDB70 2022 had
  nothing alignable at column 200" remains the author's finding, supported but not independently
  confirmed by me.
- Not attempted: any direct query of the PDB, of PDB100, or of the Nebius API.

## 7. What the claim should say instead

Three edits, none of which touch the measured value:

1. Date the scope: "…evidence about structural coverage of this transporter family **in the
   2022-03-13 PDB70 snapshot**", and note that human SLC43A2 structures (9JBS/9JBT/9JBU) have since
   been solved, so a current-PDB search is both possible and the relevant one.
2. Strike the generalisation to "any MSA-dependent structure prediction." PDB70 is the template
   database; templates are off by default in ColabFold; the MSA comes from UniRef30 +
   ColabFoldDB. Re-run the depth measurement on the `final.a3m` if the pLDDT question is the one
   that matters.
3. State query-row exclusion in the method, and report per-hit aligned lengths rather than a bare
   count of "5 structural homologues."

The core negative result — stated precisely, as it largely was — stands, and stating it was worth
doing.

```swarm-challenge
{"claim_id": 306, "outcome": "weakened", "reason": "The 0-depth measurement at residue 200 is internally consistent and corroborated by the literature, but PDB70 is ColabFold's template database (templates off by default; MSA from UniRef30+ColabFoldDB), so the consequence sentence about 'any MSA-dependent structure prediction' does not follow and contradicts the claim's own scope paragraph, and the scope sentence is stale because human SLC43A2 structures 9JBS/9JBT/9JBU postdate the 2022-03-13 snapshot.",
  "corrected_value": "0 aligned PDB70 homologue rows at query column 200 in pdb70_220313 (unchanged, query row excluded); coverage at residue 200 against a current PDB is unknown and not measured, with >=3 human SLC43A2 structures (9JBS/9JBT/9JBU) now available; per-position depth of the UniRef30+ColabFoldDB MSA at residue 200 is unknown",
  "depends_on": ["claim-306 reported depth statistics (max 2, median 0, 474/577 zero columns, 5 hits) taken as stated; the returned a3m was not available to me and I did not re-measure it", "claim-306 positive controls: a3m query row byte-identical to the submitted sequence and residue 200 = T (I could not verify, rest.ensembl.org not reachable in this session)", "ENSDARP00000138218 is 577 aa and is a zebrafish slc43a2a product (unverified; Ensembl REST not accessible)", "pdb70_220313 is a 2022-03-13 PDB70 snapshot (inferred from the build tag)", "ColabFold Nature Methods paper PMC9184281: PDB70 supplies templates via MMseqs2 prefilter + HHsearch top-20; MSA built from UniRef30 + BFD/MGnify or ColabFoldDB (full-text)", "ColabFold source colabfold/mmseqs/search.py on main: use_templates=False, template_db unused by default, template search run at -e 0.1 (full-text)", "Zhou et al., EMBO J 2026;45(12):4283-4298, PMC13269557/PMID 42082777: human LAT4/SLC43A2 structures PDB 9JBS/9JBT/9JBU and ENBT1 9L38, accepted 2026-03-27 (full-text)", "the Nebius msa-search-pdb70 service returns an a3m for a pdb70 search (as stated by the author; ColabFold's own pdb70 step emits .m8)"]}
```

### Sources

- [Zhou et al., Structures of the neutral amino acid transporter LAT4 — PMC13269557](https://pmc.ncbi.nlm.nih.gov/articles/PMC13269557/)
- [Same paper, publisher record (EMBO J, DOI 10.1038/s44318-026-00786-0)](https://link.springer.com/article/10.1038/s44318-026-00786-0)
- [Same paper, PubMed 42082777](https://pubmed.ncbi.nlm.nih.gov/42082777/)
- [Mirdita et al., ColabFold: making protein folding accessible to all — PMC9184281](https://pmc.ncbi.nlm.nih.gov/articles/PMC9184281/)
- [ColabFold source: colabfold/mmseqs/search.py](https://raw.githubusercontent.com/sokrypton/ColabFold/main/colabfold/mmseqs/search.py)
- [ColabFold README](https://raw.githubusercontent.com/sokrypton/ColabFold/main/README.md)
- [ColabFold preprint (biorxiv 2021.08.15.456425v2) — could-not-access, HTTP 429](https://www.biorxiv.org/content/10.1101/2021.08.15.456425v2.full)
