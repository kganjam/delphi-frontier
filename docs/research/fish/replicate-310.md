# Replicate 310: [S43] pectoral fin area protocol, an independent re-derivation

**Verdict: DISAGREE, in part.** The headline sample size reproduces *if* you accept its
assumption. The "about four-fold" reduction from measuring area does not hold under the same
geometric assumption that produces "10.25 %". The cost figure is CANNOT TELL.

## 0. Procedure and contamination statement

- I derived everything in §1–§3 before opening the harvest branch
  `claude/zebrafish-fin-area-protocol-xy8ijv`. I opened it only for §4. The working branch
  had no S43 material on it: I ran a grep for `kcnh2a`, `fin area` and `310` over `*.md`,
  `*.json` and `*.jsonl` and got no hits.
- The question text is itself the claim, so I knew the claimed numbers ("10.25 %", "four-fold",
  "n = 30", "$12,200–$18,000", "32 weeks") from the start. I did not know which one was the
  recorded key number, or what assumptions sat behind it, until §4.
- Everything numeric below is **calculation**. None of it is observation. I made no
  measurements.

## 1. Inputs

| input | value | source | read-level |
|---|---|---|---|
| Genotypes exist; nr21 is a *lat4a* short-fin allele (Lat4a T200K); *lof* is a *prrx1a*→*kcnh2a* regulatory inversion; nr21/+ × lof/+ crosses were made | — | Daane et al. 2021, *Curr Biol*, "Modulation of bioelectric cues in the evolution of flying fishes". Figure legends as surfaced on ZFIN (ZDB-FIG-221222-34, -35) | **search-summary**. I did not read the full text or the figure pages themselves |
| Residual CV of adult pectoral fin area, or of length, among sibling genotypes | **unknown** | One web search (lat4a nr21 / kcnh2a longfin fin length) returned only the ZFIN figure listings. I did no other CV search | could-not-access (not found in the scope above) |
| z quantiles | z₀.₉₇₅ = 1.960, z₀.₈ = 0.842, z₁₋₀.₀₁₆₇/₂ = 2.394, z₀.₉ = 1.282 | Python `statistics.NormalDist` | computed |
| Mendelian ratio of a double-het × wild-type cross (nr21/+ × lof/+) | ¼ in each of 4 classes | Mendel; both alleles carried singly by different parents | standard |
| Unit costs (per diem, genotyping, labour) | **unknown** | Not sourced. No search done | — |

## 2. Arithmetic

**2a. Length → area effect (isotropic scaling, A ∝ L²).**
1.05² = 1.1025, so a 5 % length effect is a **10.25 % area effect**. AGREE.

**2b. Does measuring area cut *n* four-fold?**
Per-group *n* for a two-sample comparison ≈ k·(CV/δ)², with k = 2(z_{α/2}+z_β)².

- Naively, (10.25/5)² = **4.20**, and that is where "four-fold" comes from. It holds only if CV_area = CV_length.
- The isotropic assumption that gives 10.25 % also gives log A = 2 log L + c. Any biological
  variation in length therefore doubles in log-area: SD(log A) = 2·SD(log L), so
  CV_area ≈ 2·CV_length. The effect on the log scale is ln 1.1025 = 2·ln 1.05. The
  standardized effect, δ/SD, is **identical** for area and length, so the *n* ratio is
  **1.00, not 4**.
- Numerical check (α = 0.05 two-sided, power 0.80, k = 15.70):

  | CV_length | n, length (5 %) | n, area if CV_area = CV_length | n, area if CV_area = 2·CV_length |
  |---|---|---|---|
  | 0.05 | 15.7 | 3.7 | 14.9 |
  | 0.08 | 40.2 | 9.6 | 38.2 |
  | 0.10 | 62.8 | 14.9 | 59.8 |

  On the exact log scale the length and area columns are equal (16.5 / 42.2 / 65.9 each). The
  small gap in the last column is a linearization artefact.
- **Inference (mine, not a source's):** area beats length only if the noise in area grows
  less than in proportion to length². Two ways that could happen: measurement error dominates
  and is relatively smaller for area, or width varies partly independently of length while the
  genotype effect hits both. If width varies independently and the genotype affects only length,
  area is *worse* than length. Which case applies is an empirical question for the pilot. As a
  general rule, "four-fold" is unsupported, and the expected gain under the claim's own
  geometry is about 1×.

**2c. Sample size at a stated area CV.**
I used α = 0.05/3 = 0.0167 Bonferroni (three contrasts against wild-type siblings; I chose
this independently as the natural design for 4 classes), power 0.90, k = 27.01.

- CV_area = 0.10, δ = 10.25 % (linear): n = 27.01·(0.10/0.1025)² = **25.7**.
- CV_area = 0.10, δ = ln 1.1025 = 0.0976 (log scale): n = **28.4** → about 29–30 per genotype.
- CV_area = 0.20 (which is what CV_length = 0.10 implies under 2b): n = **113.5**.

So n = 30/genotype is adequate if CV of *area* ≤ about 0.10, which means CV of length ≤ about
0.05 under isotropy. That CV is **unknown** (§1).

**2d. Yield of the cross.**
200 F1 → 50 expected per class. P(one class ≥ 30) = 0.99979 (exact binomial). P(all four
≥ 30) ≈ 0.9992 (independence approximation). So n = 30 per class from 200 genotyped siblings
is reliably achievable. AGREE.

**2e. Cost ($12,200–$18,000) and duration (32 weeks).**
I did not source unit prices, so I cannot re-derive this. **CANNOT TELL.**

## 3. My value

- Area effect: **10.25 %** (exact, given isotropy).
- Fold reduction in *n* from measuring area instead of length: **≈ 1× (no reduction)** under
  the isotropy that defines 10.25 %. It is 4.2× only if CV_area = CV_length, which isotropy
  argues against. Uncertainty: plausibly between about 0.5× and 4× depending on the
  unmeasured variance structure. This is calculation, not observation.
- n per genotype (90 % power, Bonferroni α = 0.0167, CV_area = 0.10): **26–29**, so n = 30 is
  adequate. At CV_area = 0.20: **~103–114**.
- Cost: **unknown**.

## 4. Comparison with the recorded value (read after §1–§3)

The harvest file `docs/research/fish/S43-organ.md` (branch `…-xy8ijv`; read-level: full-text
for the sections quoted) records the key number as *"n = 30 fish per genotype … for 90 % power
at Bonferroni-corrected alpha=0.0167 against a 10.25 % area effect, assuming residual
CV = 0.10"*. Its table gives 28 at CV 0.10 / 10.25 % / power 0.90 on log-area, with a Guenther
correction.

- **n = 30 | CV = 0.10: AGREE.** My 28.4 (log scale, no small-sample correction) matches its 28.
  The recorded document states openly that the CV is unsourced and provides a pilot with a
  pre-specified escalation rule (CV > 0.10 → n = 60, CV > 0.15 → …). I agree with that design.
- **"Cuts the required n about four-fold": DISAGREE.** The recorded text says four-fold "at the
  same CV". Its caveat is only that the *measurement* CV of area might be larger because of
  flattening. It does not address the fact that, under the isotropy it uses to get 10.25 %,
  *biological* CV of area is about 2× that of length. That cancels the gain exactly. The
  author's claim is a 4× reduction; my inference is about 1× unless the pilot shows otherwise.
- **The CV of 0.10 needs a label.** It is a CV of *area*. If someone carries over a length CV
  of 0.10 from a length study, the correct area figure is about 0.20, and n ≈ 105–114 per
  genotype, not 30.
- **Cost / 32 weeks: CANNOT TELL.** The recorded document itself notes an 11-fold disagreement
  between institutional per-diem sources. I did not resolve it.

## 5. Scope of negative searches

- Fin-area CV: one web search (above). I did not search ZFIN phenotype data, theses, or the
  Daane 2021 supplement. The CV is **unknown**, not shown to be absent from the literature.
- Unit costs: not searched.

```swarm-replication
{"claim_id": 310, "my_value": "10.25% area effect (agree); n≈28/genotype at CV_area=0.10, 90% power, alpha=0.0167 (agree); fold reduction in n from area vs length ≈1x not 4x under isotropy; cost unknown", "agrees": false,
  "note": "The n=30 arithmetic reproduces, but the four-fold reduction does not: the isotropy that turns a 5% length effect into 10.25% area also doubles CV_area, so the standardized effect, and hence n, is unchanged."}
```
