# S44 — protein scale: does ESM-2 masked-marginal scoring rank *slc43a2a* T200K as disruptive?

Project `zebrafish-flight`. Scale: protein. Status: **blocked / refused** — see §4.

---

## 1. The question, restated precisely

*slc43a2a* (= *lat4a*) **T200K** is one of only two demonstrated alleles in the whole
`zebrafish-flight` design. The allele is a **dominant** fin-size **suppressor**. A dominant
suppressor is most consistent with gain- or change-of-function, and a gain-of-function allele
predicts a **moderate** variant-effect score, not the severe score a loss-of-function allele
would give.

The test as specified:

- Score T200K with ESM-2 masked marginals:
  `s = log P(K | x_masked at 200) − log P(T | x_masked at 200)`.
- Report its **rank among the 19** possible non-wild-type substitutions at position 200.
- Report its **percentile against a 120-variant background** of single substitutions.
- State the interpretation as a **prediction fixed before the numbers are read**.

### The numbers that make it hard

Two independent obstacles, both quantified, each sufficient on its own to stop the computation:

| Obstacle | The number |
|---|---|
| The reference protein for *slc43a2a* is **153 aa** long. Position 200 does not exist in it. | **0 of 19** substitutions at position 200 can be constructed against any public reference sequence |
| ESM-2 checkpoint weights are denied by this environment's network policy | **0 of 2** checkpoints (`esm2_t6_8M_UR50D`, `esm2_t33_650M_UR50D`) obtainable |

So the deliverable below is a precise negative, plus the preregistered prediction recorded in
advance so that the test is decisive the moment either obstacle is removed.

---

## 2. What is measured

Every row is someone else's measurement, with read-level. Disagreements are preserved, not averaged.

### 2.1 The allele itself

| Claim | Source | Year | Read-level |
|---|---|---|---|
| A single *nr21* founder was isolated from a small ENU **dominant** screen as having "a dominant, shortened length of all fins compared to wild-type" | Daane, Blum, Lanni, Boldt, Iovine, Higdon, Johnson, Lovejoy, Harris. *Modulation of bioelectric cues in the evolution of flying fishes.* Curr Biol 31(22):5052–5061. PMID 34534441; doi 10.1016/j.cub.2021.08.054 | 2021 | full-text (automated extraction of PMC9172250, first 100,000 of 149,104 characters; **figures and STAR Methods not retrieved**) |
| Authors' words: "identified a nonsynonymous mutation (**T200K**) in a conserved domain of the L-type amino acid transporter, *lat4a*" | same | 2021 | full-text (same caveat) |
| The authors themselves hedge the residue call: the Figure 3C legend refers to "the **predicted** T200K substitution of *nr21*" | same | 2021 | full-text (legend text as extracted; **I did not see the figure**) |
| Mapping by pooled exome sequencing of wild-type siblings vs. short-finned mutants placed the mutation on **chromosome 15** | same | 2021 | full-text (same caveat) |
| Allele is dominant "without an obvious homozygous phenotype" | same, Methods | 2021 | full-text (same caveat) |
| *lat4a nr21/+* "is a medial fin suppressor of *kcnh2a lof/+*"; paired fins remain overgrown in the double mutant; the caudal fin of the double heterozygote is **hypocercal** with an elongated ventral lobe — i.e. not simply wild-type | same | 2021 | full-text (same caveat) |
| Authors' classification: the mutation "results from a **gain-of-function** effect". Basis given: CRISPR frameshifts introduced *in cis* (L106Rfs39) reverted the phenotype to wild-type fin size, and "zebrafish lacking *lat4a* have no fin phenotype" | same | 2021 | full-text (same caveat) |
| *kcnh2a* expression did not change significantly in *nr21* fins, so the suppression acts downstream of the bioelectric signal | same | 2021 | full-text (same caveat) |
| The term "change-of-function" does not appear in the article | same | 2021 | full-text (same caveat) — negative finding, scope: the extracted first 100,000 characters only |

**The authors' claim vs. my inference.** The authors claim gain-of-function. That claim rests on
genetic logic I find sound but did not verify independently: a null has no fin phenotype, and a
frameshift in *cis* on the *nr21* chromosome removes the phenotype — which is hard to explain
unless the *nr21* protein product is doing something a wild-type product does not. **My
inference**, not theirs: this is the strongest available argument that T200K is not a simple
hypomorph, and it is what makes the "moderate score" prediction in §3.3 worth registering.

### 2.2 Gene and sequence records

| Claim | Source | Year | Read-level |
|---|---|---|---|
| Gene `slc43a2a`, GeneID **393221**, chromosome **15**, aliases `si:dkey-118k5.2`, `slc43a2`, `zgc:56271`; "Acts upstream of or within fin morphogenesis… Is expressed in dorsal fin and pectoral fin. Orthologous to human SLC43A2" | NCBI Gene 393221 (summary attributed to Alliance of Genome Resources, Jul 2025) | record read 2026-11-04 | full-text (database record) |
| Gene span `NC_141035.1`:31,099,368–31,139,242, **5 annotated exons** | same | same | full-text |
| `NM_200251.2`, 3,230 bp mRNA; **CDS 175..636**; protein `NP_956545.1`, **153 aa**. GenBank record dated 24-AUG-2026. Reference 1 on the record is **Daane et al. 2021** — i.e. this is the transcript record the paper is attached to | NCBI Nucleotide `NM_200251.2` | 2026 | full-text (GenBank flatfile) |
| UniProt `Q7ZUS0` (*slc43a2a*, unreviewed) — **153 aa**; `A0A8N7V006` (*slc43a2a*, unreviewed) — **153 aa** | UniProt REST | retrieved 2026-11-04 | listing (TSV field query) |
| Paralog `slc43a2b`: `Q5PR35` — **592 aa**, "Large neutral amino acids transporter small subunit 4 (L-type amino acid transporter 4)"; also `A0A8M1N3P6` 592 aa, `A0ACD6B803` 598 aa | UniProt REST / FASTA | retrieved 2026-11-04 | full-text (FASTA) + listing |
| Paralog `slc43a2b`, GeneID **494042**, chromosome 10, **15 annotated exons** — against 5 for *slc43a2a* | NCBI Gene 494042 | record read 2026-11-04 | full-text (database record) |

**The disagreement that matters, preserved.** The *slc43a2a* reference protein is annotated at
**153 aa** by RefSeq *and* by UniProt (including the Ensembl-derived TrEMBL entry), while its
paralog *slc43a2b* is annotated at **592 aa**. The paper numbers a residue at **200**. These cannot
all be describing the same molecule. Either the public *slc43a2a* annotation is truncated (far more
likely, given **5** annotated exons for *slc43a2a* against **15** for its same-species paralog
*slc43a2b*), or the paper's residue numbering is anchored to a sequence
that is not in the public reference databases — plausibly the authors' own corrected annotation,
since they generated PacBio data and deposited contigs at Zenodo 10.5281/zenodo.5082978. **I could
not determine which**, and I am not resolving it by assumption.

### 2.3 Nomenclature disagreement — unresolved, read-level search-summary only

| Source | Says |
|---|---|
| Daane et al. 2021 (full-text, as above) | gene *lat4a*, allele ***nr21***; the article "does not use `slc43a2a`" per extraction; `Slc43a2` appears only for mouse Lat4 |
| A ZFIN figure page for Daane et al. 2021 Fig. 4 | gene *slc43a2a*, allele ***dmh26***, genotype written `slc43a2a^dmh26/+` |

Read-level for the ZFIN row: **search-summary only**. `zfin.org` and `www.zfin.org` were both
unreachable from this environment (HTTP 000, see §3.4), so I could not open the record. I report
the two names as a live disagreement about allele designation. I did not verify that `nr21` and
`dmh26` are the same allele, and I have not adopted either as canonical.

A second item surfaced only in search-summary: a review table reportedly lists *nr21* as dominant
with fin phenotype "Short" and mutation type "gain-of-function". **My inference**, flagged as
such: that is reconcilable with Daane et al. rather than contradictory — *nr21/+* alone gives
short fins, and *suppressor* describes its effect in combination with *kcnh2a lof/+*. But I could
not identify or read that review, so I record it as unverified and do not lean on it.

---

## 3. What I computed

All of §3 is **computation and tool-attempt logging performed by me in this session**, not
observation.

### 3.1 Arithmetic on the annotated CDS (computation)

From the `NM_200251.2` GenBank record, CDS = 175..636:

```
coding length      = 636 − 175 + 1      = 462 nt
codons             = 462 / 3            = 154 codons
protein            = 154 − 1 (stop)     = 153 aa          ✓ matches NP_956545.1
```

To reach residue 200 the coding sequence would have to run:

```
nt through codon 200 = 175 + (3 × 200) − 1 = 774
annotated stop codon = 634..636
shortfall            = 774 − 636          = 138 nt (46 codons) past the stop
```

### 3.2 Independent translation check (computation)

I did not take the 153 aa on trust. I translated `NM_200251.2` myself from the annotated start
(mRNA position 175) with the standard genetic code and walked forward to the first in-frame stop:

- mRNA length recovered from the flatfile `ORIGIN` block: **3,230 nt** (matches the LOCUS line)
- **first in-frame stop: mRNA position 634**
- **ORF from the annotated start: 153 aa**
- residue 200 reachable: **False**

So the early termination is a real property of the reference mRNA sequence as deposited, not a
mis-parse of the CDS qualifier. The 3,230 bp transcript carries a long final exon (584..3,214)
that the annotation treats as 3′ UTR.

Coverage arithmetic: `153 / 592 = 25.8%` of the paralog's length.

### 3.3 Naive index transfer to the paralog (computation — and it fails)

If residue numbering were transferable between the paralogs, position 200 of Lat4b would be a
threonine. It is not:

- `Q5PR35` (*slc43a2b*) length **592**
- **residue 200 = M** (methionine)
- context, residues 190–210: `MTFTSLTLPNMFGDLRATFIA`

**My inference:** naive index transfer does not corroborate a threonine at 200, which is expected
once the *slc43a2a* annotation is known to be truncated — the two numbering frames are not
co-linear. This is a negative control on my own shortcut, not evidence against the paper. There
*are* threonines nearby in the paralog frame (`T191`, `T195`), but assigning one of them to the
paper's "T200" would be exactly the kind of invention this project forbids, so I do not.

### 3.4 The preregistered prediction — fixed here, before any score exists

This is registered with **no ESM-2 number having been computed, in this session or elsewhere**.
Nothing below was back-fitted; there is nothing to back-fit to.

**Protocol to be run when unblocked.** Masked-marginal score
`s(i, wt→mt) = log P(mt | x_{masked at i}) − log P(wt | x_{masked at i})`, one forward pass per
masked position, `esm2_t33_650M_UR50D` as primary with `esm2_t30_150M_UR50D` and
`esm2_t36_3B_UR50D` as robustness checks. Site set: all 19 non-wild-type substitutions at position
200. Background: 120 single substitutions drawn uniformly without replacement from
(all positions × 19 alternatives), excluding position 200, under a fixed stated seed. Both the
sequence used and the seed must be recorded in the result.

**Prediction from the dominant-suppressor / gain-of-function argument.** T200K should score
**moderate** — detectably worse than a typical random substitution, but clearly outside the
loss-of-function tail:

| Quantity | Preregistered expectation |
|---|---|
| Rank among the 19 substitutions at position 200 (1 = most negative) | **not in the 3 most negative**; expected mid-range, ranks ~6–15 |
| Percentile in the 120-variant background | **between the 10th and 50th percentile** (more negative than the background median, but not in the bottom decile) |
| Equivalent band | roughly `−1 < z < 0` against the background distribution |

**Registered falsifiers, both directions:**

- T200K **indistinguishable from the background median** (above the 50th percentile) ⇒ ESM-2 sees
  nothing special about the allele, and using it as a designed lever is weakened. This is the
  refutation condition named in the subproblem, and I accept it as stated.
- T200K in the **bottom decile of the background and the 3 most negative at its site** ⇒ ESM-2
  reads it as loss-of-function-like, contradicting the moderate-score expectation.

**Registered in advance, a reason this test may be weakly diagnostic even when it runs** — stated
now so it cannot look like an excuse later. ESM-2 masked marginals estimate evolutionary
likelihood. They track conservation and fitness cost; they are not built to separate gain-of-
function from loss-of-function, and a gain-of-function substitution at a conserved site can score
severely for the same reason a loss-of-function one does. T200K introduces a **positive charge**
in what the authors call a conserved domain of a transmembrane amino-acid transporter. If residue
200 sits in or against a membrane-spanning helix, a severe score is likely **regardless** of the
allele's true mechanism. So the bottom-decile outcome above would not, on its own, refute the
gain-of-function classification — it would more likely reveal a limit of the method. I register
this before seeing numbers because it bears on how much the eventual answer is worth.

### 3.5 Tool attempts and the scope of each negative

Installed and working in this session: **torch 2.15.0+cu132**, **fair-esm 2.0.0**, 4 CPUs, 15 GB
RAM, 31 GB free disk. (`numpy` is absent from the venv and would also be needed; that is trivially
fixable from PyPI, which is reachable.) CPU-only masked-marginal scoring over ~121 masked
positions was estimated as feasible in well under an hour. **The compute was never the problem.**

Real load attempt through the library, not merely a reachability probe:

```
--- attempting esm2_t6_8M_UR50D
Downloading: "https://dl.fbaipublicfiles.com/fair-esm/models/esm2_t6_8M_UR50D.pt"
FAILED esm2_t6_8M_UR50D   URLError <urlopen error Tunnel connection failed: 403 Forbidden>
--- attempting esm2_t33_650M_UR50D
Downloading: "https://dl.fbaipublicfiles.com/fair-esm/models/esm2_t33_650M_UR50D.pt"
FAILED esm2_t33_650M_UR50D URLError <urlopen error Tunnel connection failed: 403 Forbidden>
```

**Scope of the negative searches.** Hosts denied by this environment's network policy (HTTP 000 or
403 at CONNECT): `dl.fbaipublicfiles.com` (fair-esm's weight host), `huggingface.co`, `hf.co`,
`cdn-lfs.huggingface.co`, `hf-mirror.com`, `esmatlas.com`, `api.esmatlas.com`,
`download.pytorch.org`, `rest.ensembl.org`, `ftp.ensembl.org`, `zfin.org`, `www.zfin.org`,
`zenodo.org`, `ftp.ebi.ac.uk`, `blast.ncbi.nlm.nih.gov`, `data.broadinstitute.org`. Reachable:
`pypi.org`, `files.pythonhosted.org`, `eutils.ncbi.nlm.nih.gov`, `rest.uniprot.org`,
`www.uniprot.org`, `www.ebi.ac.uk/proteins/api`, `alphafold.ebi.ac.uk`, `raw.githubusercontent.com`,
`www.rcsb.org`. I did not go looking for unofficial re-uploads of the weights on reachable hosts;
a checkpoint of unverifiable provenance would not support a claim at this project's evidence
standard.

---

## 4. The answer, with its evidence level

**Evidence level: refused (blocked).**

**The answer: unknown — not computed.** I cannot report T200K's rank among the 19 substitutions at
position 200, nor its percentile in a 120-variant background, because the computation was blocked
twice over, independently:

1. **No reference sequence places a residue at position 200.** Every public annotation of
   *slc43a2a* I could reach — RefSeq `NP_956545.1`, UniProt `Q7ZUS0`, UniProt `A0A8N7V006` — gives
   a **153 aa** protein, and my own translation of `NM_200251.2` confirms a genuine in-frame stop
   at mRNA position 634. The 19-substitution site set cannot be constructed, let alone scored.
2. **No ESM-2 weights are obtainable here.** Both checkpoints tried returned 403 at the proxy, and
   every known weight host and mirror is denied (§3.5).

What *is* established, at **literature** level, is the premise the test was built on: T200K is a
real, published, named allele (`lat4a^nr21`, PMID 34534441, 2021), it is dominant, it shortens all
fins on its own, it suppresses *kcnh2a lof/+* medial-fin overgrowth, and **the authors classify it
as gain-of-function** on the strength of a *cis* frameshift reversion and a phenotype-free null.
The project's framing of T200K as a demonstrated allele and a dominant suppressor is **correct and
sourced**. The preregistered prediction and its falsifiers are now on record (§3.4), fixed before
any number exists.

---

## 5. What this does NOT establish

Read this as carefully as §4.

- **It does not establish that T200K is wrong, mis-reported, or does not exist.** The authors
  worked from a *lat4a* sequence; I simply do not have that sequence. The failure here is mine and
  this environment's, not theirs.
- **It does not establish that the 153 aa annotation is correct biology.** A reference protein of
  153 aa with 5 annotated exons, where the same-species paralog *slc43a2b* is 592 aa with 15 exons,
  is far more consistent with a truncated annotation than with a genuinely tiny transporter. I did
  not confirm that, and I did not reconstruct the gene to find out.
- **It does not establish that residue 200 of the true Lat4a is a threonine.** I could not reach a
  sequence in which to check, and naive paralog index transfer gave methionine (§3.3), which
  settles nothing either way.
- **It does not establish anything whatsoever about ESM-2's opinion of T200K** — not its rank among
  the 19, not its background percentile, not its sign or magnitude. No score was produced. Any
  number attached to this subproblem elsewhere did not come from this work.
- **It does not test the suppressor → moderate-score prediction.** That prediction is registered,
  not evaluated. The project should not count it as supported.
- **It does not establish that the gain-of-function classification is right.** That is the authors'
  claim, from genetic evidence I read only as extracted text — I never saw Figure 3C, Figure 4, or
  the STAR Methods, and the authors' own legend calls T200K a *predicted* substitution.
- **It does not establish that the test, once run, will be diagnostic.** This is the most important
  item here. Masked marginals score evolutionary likelihood, which conflates gain- and
  loss-of-function; a charge-introducing substitution in a conserved transmembrane transporter
  domain may score severely whatever its mechanism (§3.4). A severe score would therefore be weak
  evidence against gain-of-function, and the subproblem's stated inference — dominant suppressor ⇒
  moderate score — is **less tightly licensed than its framing suggests**. That is a defect in the
  experimental design, and it is unaffected by whether the compute ever runs.
- **It does not resolve the allele nomenclature.** `lat4a^nr21` (paper, full-text) vs.
  `slc43a2a^dmh26` (ZFIN, search-summary only, record unreadable from here) stands unresolved.
- **It does not establish a 120-variant background.** No background set was ever sampled; the
  seed in §3.4 is a specification, not a record of a draw.
- **It establishes nothing at any other scale.** No claim is made or supported here about fin
  size, fin shape, gliding, lift, or whether any of this helps a 0.4 g fish leave the water.

---

## 6. What would change the answer

In the order that actually unblocks the work.

1. **Allow one weight host.** Adding `huggingface.co` (for `transformers` / `facebook/esm2_*`) or
   `dl.fbaipublicfiles.com` (for `fair-esm`) to the environment's Allowed domains is sufficient on
   the model side. torch and fair-esm are already installed here; only `numpy` would need adding
   from PyPI. The run is then ~121 CPU forward passes. Network access is set in the cloud
   environment's settings (environment menu in the session title bar → Edit → Network access,
   leaving "Allow package managers" ticked): https://code.claude.com/docs/en/cloud-environments#network-access
2. **Obtain a sequence in which residue 200 exists.** Any one of: the authors' *lat4a* annotation
   from Zenodo `10.5281/zenodo.5082978`; the Ensembl *slc43a2a* transcript via `rest.ensembl.org`;
   the ZFIN allele record for `nr21`/`dmh26`; or a direct request to the corresponding author for
   the numbering reference. Each requires a host currently denied (§3.5), except the last.
3. **Failing that, reconstruct the CDS — and label it a reconstruction.** The gene occupies
   `NC_141035.1`:31,099,368–31,139,242, a span of **39,874 bp**, and genomic sequence is reachable
   via NCBI E-utilities. Exons could be called by homology to Lat4b (`Q5PR35`, 592 aa) and to human
   *SLC43A2*. This would produce a *derived* sequence, and every score computed on it would inherit
   that evidence level — it could not be reported as `measured`, and residue 200 would have to be
   checked for a threonine as the first sanity test. If it is not T, the reconstruction is wrong or
   the paper's frame is different, and scoring must stop.
4. **The design change that would most improve the answer's worth.** Because masked marginals
   cannot separate gain- from loss-of-function, pair the ESM-2 run with a method that can carry
   directional information: compare T200K against the other 18 substitutions at the same site
   grouped by physicochemical class (does ESM-2 penalise *any* positive charge at 200, or lysine
   specifically?), and against the authors' own `L106Rfs39` frameshift as an internal
   loss-of-function anchor. A site-specific, charge-specific penalty profile is a far more
   informative readout than a single rank, and it is obtainable from exactly the same forward
   passes.
5. **The measurement that would settle the biology regardless of any model.** Transporter activity
   of Lat4a^T200K versus wild-type Lat4a in a heterologous uptake assay. Elevated or altered
   L-leucine transport would support gain- or change-of-function directly, and would make the
   ESM-2 question a calibration exercise rather than the primary evidence. No language-model score
   substitutes for it.

---

```swarm-result
{"subproblem": "S44", "evidence": "refused",
  "answer": "Not computed: ESM-2 masked-marginal scoring of slc43a2a T200K was blocked twice independently — every public slc43a2a reference protein (RefSeq NP_956545.1, UniProt Q7ZUS0/A0A8N7V006) is only 153 aa so position 200 does not exist and the 19-substitution site set cannot be built, and all ESM-2 weight hosts are denied by this environment's network policy; the allele itself is confirmed real, dominant and classified gain-of-function by Daane et al. 2021 (PMID 34534441), and the moderate-score prediction plus its falsifiers are registered here before any number exists.",
  "key_number": "153 aa (slc43a2a reference protein length; residue 200 lies 46 codons past the in-frame stop at mRNA position 634 of NM_200251.2)",
  "blocked_on": "ESM-2 checkpoint weights (dl.fbaipublicfiles.com and huggingface.co both denied, 403 at proxy CONNECT) and a full-length lat4a sequence in which residue 200 exists (rest.ensembl.org, zfin.org and zenodo.org all unreachable)"}
```
