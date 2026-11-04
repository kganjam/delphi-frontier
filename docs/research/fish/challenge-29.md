# Challenge 29: "No tandem repeats in kcnk5b, and1 or and2". REFUTED

**The claim under review** (author: the running agent, `docs/research/fish/proteins-disorder.md` §3 on
branch `swarm-architecture`, read-level: full-text):

> No tandem repeats in any of the three proteins against a null of 200 composition-preserving
> shuffles: and2's max self-identity (0.098) is BELOW its own null (0.111).

Recorded evidence level: *derived*. Value: 0.098 max self-identity.

**Verdict: REFUTED.** The number 0.098 reproduces. Three things built on it do not hold:

1. The decision rule tests against the *maximum* of 200 shuffles, which is a ~99.5th-percentile
   threshold, and calls that "the null".
2. Under the author's own metric, kcnk5b and and1 are significantly **above** chance (p ≈ 0.0015),
   not "at the null".
3. The metric is a proxy that cannot see degenerate repeats with variable spacing. and1 and and2
   both carry an internal **C‑x(6,7)‑C repeat module**: 8 copies in and1 and 10 in and2. Against
   shuffles, no shuffle reached 8 or 10 copies (p < 1/5000), and the module's flanks are
   conserved beyond the cysteines.

Everything below is **calculated** from public sequences with the scripts in
`challenge-29-scripts/`. Nothing here is a wet-lab observation.

---

## Inputs (fetched independently, not taken from the author)

| protein | UniProt | length | read-level |
|---|---|---|---|
| kcnk5b | Q6PFU3 | 448 | full record (FASTA via rest.uniprot.org, 2026-11-04) |
| and1 | E7F5V5 (SV=2) | 570 | full record |
| and2 | A9JRX1 | 508 | full record; identical in sequence to A0ACM8QEN9 (checked) |

The lengths match the author's 448 / 570 / 508. The author's document does not name accessions, so
it is an **inference** that these are the same sequences. The supporting evidence is that every
number in the author's table reproduces to the third decimal (see 1).

## 1. Independent recomputation of the author's statistic

Statistic: the maximum over offsets k = 1–80 of the fraction of positions i where s[i] = s[i+k].
Null: whole-sequence permutation. I drew 2,000 shuffles (seed 29), not 200.

| | max obs (offset) | Σf² | null mean | null SD | max of first 200 | **empirical p** | z |
|---|---|---|---|---|---|---|---|
| kcnk5b | 0.110 (k=3) | 0.060 | 0.088 | 0.0058 | 0.111 | **0.0015** | +3.8 |
| and1 | 0.116 (k=8) | 0.067 | 0.093 | 0.0054 | 0.107 | **0.0015** | +4.2 |
| and2 | **0.098** (k=61) | 0.065 | 0.0915 | 0.0055 | 0.112 | **0.106** | +1.3 |

- **Arithmetic: confirmed.** 0.110, 0.116, 0.098, Σf² and the shuffled means all reproduce the
  author's table.
- **The inference does not follow.** "Shuffled max" is the most extreme of 200 draws, so
  "observed < shuffled max" only says p > ~0.005. That is not "at" or "below" the null.
  - **and2:** 0.098 sits *above* the null mean, at about the 89th percentile (p = 0.106). The
    correct statement is "not significant". **"BELOW its own null" is false.** It is below one
    extreme draw, not below the distribution.
  - **kcnk5b and and1:** in the author's own table, the observed values (0.110, 0.116) *exceed* the
    author's own shuffled maxima (0.109, 0.114). So their p < 1/201, yet they were labelled "at the
    null". With 2,000 shuffles, both have p = 0.0015.
- **Robustness to the hidden assumption.** A whole-sequence shuffle destroys local composition,
  so any regional bias inflates significance. I relaxed it with a block shuffle that permutes only
  within 20- or 40-aa blocks (1,000 draws each):
  - kcnk5b: p = 0.023 / 0.027. Weakened; plausibly TM-segment composition, not repeats.
  - and1: p = 0.002 / 0.010. **Survives.**
  - and2: p = 0.26 / 0.23. Not significant.

So by the author's own metric with a correct null, **and1 is not "at the null"**. The headline
"no repeats in any of the three" already fails on its own test.

## 2. The proxy: global fixed-offset identity is not a tandem-repeat test

The quantity that matters is whether the sequence contains *internally repeated units*,
including degenerate ones with indels. Global identity at a fixed offset measures something
narrower: whether one exact period holds across the *entire* chain. Linkers of variable length
between repeat units scatter the signal across many offsets, so it averages to background.
Dedicated detectors (RADAR, HHrepID, T‑REKS, XSTREAM) exist for this reason. I could not run them
here: none are installed, and I did not fetch them. Their verdicts are **unknown**.

Instead I looked at the feature the author had already flagged as "not a periodic repeat array".

### C‑x(6,7)‑C module: counts versus shuffle (5,000 shuffles, seed 1)

| | observed | shuffle mean | shuffle max | p |
|---|---|---|---|---|
| kcnk5b | 0 | 0.32 | 4 | 1.0 (control: absent) |
| and1 | **8** | 0.82 | 5 | **< 0.0002** |
| and2 | **10** | 1.45 | 6 | **< 0.0002** |

The modules (position of the first C, ±6/+15 aa):

```
and1                           and2
 121 GDIYKSCAESDDPNCVSSYTNR     114 SQIYKTCANSDDPDCIAESTSK
 152 PAPVKSCDPYRDPYCLYSKGYS     148 QATVAVCNPYLDPYCLYAIRPK
 228 AELLRICDAEDVECLQYHLRAA     217 AELLRICNPSDTECLQYHLRAA
 261 SYAHLGCDPKTDPQCVPHLVQK     250 SYSHLGCDPTKDPYCQPKLVAR
 288 YLRYPNCDPRVDPYCAYAAALA     277 YHLYPSCNPATDPLCVANVVAP
 313 NPESPPCNPLYEDNCNPLTATR     308 APKDKLCNPLFDEGCNPLTAAK
   —                            347 APLNLACDPRYDPYCLIGGSAA
 406 TKEGYECFVGYDKECIPLSSQN     391 TKEGYDCYMFYDKDCTPVENQD
   —                            418 ASSKPDCHPFDPNCGRFAAQPS
 458 IEPDPDCDPEYDRNCRLRRYEP     453 IEPHPDCDPEIDYNCRLRRSES
```

Recurring consensus: **C‑[DN]‑P‑x‑x‑D‑P‑x‑C**.

**The flanks are conserved, not just the cysteines.** I scored mean pairwise identity across the
22-aa windows, with the cysteine columns excluded. The null is 2,000 sets of random windows of the
same size from the same protein:

| | flank identity | null mean | null max | p |
|---|---|---|---|---|
| and1 | 0.132 | 0.066 | 0.126 | < 0.0005 |
| and2 | 0.157 | 0.064 | 0.113 | < 0.0005 |

This underestimates the conservation, because C‑x6‑C and C‑x7‑C windows are compared without a
gap.

**Spacing.** In and2 the modules start at 114, 148, 217, 250, 277, 308, 347, 391, 418 and 453.
That gives spacings of 34, 69, 33, 27, 31, 39, 44, 27 and 35 aa, a median of ~34. My
**inference**: this is a degenerate array of ~30–35-aa units spanning residues ~110–475, with one
unit missing or diverged around 160–215. The same structure holds in and1 (8 units, 121–480).
The and1 and and2 modules also correspond one-to-one and in order (`AELLRIC…ECLQYHLRAA`,
`IEP.PDCDPE.D..CRLRR`). The two paralogs have kept the same unit order, which is further evidence
that this is a real module and not a chance pattern.

**Why the author's tests missed it.**
- **Global offset test:** the spacing varies (27–69 aa), so no single offset collects the matches.
- **"≤ 4-residue Cys gap" test (§4 of the source):** its window ends just short of the
  7–8-residue intra-module spacing. "Cysteines are dispersed … no CxxC" is literally true, but
  the cysteines are in fact strictly paired at C‑x(6,7)‑C.
- **"No 7-mer recurs 3×":** I confirmed that is true, but exact 7-mer recurrence is a very weak
  test for degenerate repeats.

Whether these units should be called "tandem repeats" in the strict sense is a definitional
point. They are tandemly arranged, internally repeated, degenerate units. **"No tandem repeats …
no repeat architecture" is not a defensible summary** of sequences that carry 8–10 copies of a
conserved module at p < 0.0002.

## 3. Evidence level

"Derived" is the right label for 0.098. It is a computed statistic, and the author did not
present it as measured. What is wrong is the **interpretation**: "BELOW its own null". That
misstates a p ≈ 0.11 result as evidence of absence, and the claim generalises it to all three
proteins when two are significant by the same test.

## 4. Literature and counter-examples (scope stated)

- Zhang et al. 2010, *Nature* 466:234–237, "Loss of fish actinotrichia proteins and the
  fin-to-limb transition". **could-not-access** (paywall redirect from nature.com).
  - The search summary says Figure 1 schematically compares zebrafish and elephant-shark
    actinodins (read-level: **search-summary**).
  - I do **not** know whether the paper describes these repeats. I did not find that statement,
    and I am not asserting it.
- Search scope: one web search ("actinodin and1 and2 zebrafish protein repeats sequence Zhang 2010
  Nature actinotrichia") and one fetch attempt of the Nature article. I made no PubMed or
  Europe PMC full-text search. Prior literature on the repeat is therefore **unknown**, not absent.
- The counter-example is in the sequences themselves (§2). It does not depend on literature.

## 5. What this changes downstream

- The source's §5 line "they have no tandem-repeat architecture" should be withdrawn.
- §4's "cysteines are dispersed … any disulfide architecture would have to be long-range or
  inter-chain" needs revision.
  - The cysteines are strictly paired at i, i+7/8 inside a repeated module.
  - That geometry is compatible with **intra-module** disulfides. This is my **inference**,
    untested; no structure was used.
  - It reopens the short-range intra-chain option that the source closed.
- **Unchanged:** I did not touch the collagen refutation (Gly ~5%) or the Tyr-clustering result.

## Reproduce

```
python3 -I challenge-29-scripts/tr.py  <dir with Q6PFU3.fa E7F5V5.fa A9JRX1.fa> 2000   # §1 table
python3 -I challenge-29-scripts/tr2.py <dir>     # block-shuffle null, offset profiles, Cys/DP positions
python3 -I challenge-29-scripts/tr3.py <dir>     # C-x(6,7)-C counts vs 5,000 shuffles
python3 -I challenge-29-scripts/tr4.py <dir>     # module flank identity vs random windows
```

```swarm-challenge
{"claim_id": 29, "outcome": "refuted", "reason": "0.098 reproduces but is at the ~89th percentile of the shuffle null (p=0.106), not below it; by the same metric and1 and kcnk5b are above chance (p=0.0015), and and1/and2 carry 8 and 10 copies of a conserved ~30-35-aa C-x(6,7)-C repeat module (shuffle p<0.0002) that a fixed-offset identity test cannot detect.", "corrected_value": "and2 max self-identity 0.098 = 89th percentile of 2,000 composition-preserving shuffles (null mean 0.0915, p=0.106); and2 contains 10 C-x(6,7)-C repeat units (shuffle mean 1.45, p<0.0002)"}
```
