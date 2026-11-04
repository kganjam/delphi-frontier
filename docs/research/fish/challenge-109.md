# Challenge 109: adversarial review of S22-D-D-D (the pectoral fold-overgrowth `f`)

**Claim under review (S22-D-D-D, branch `claude/deepen-s22-d-d-input-vncsjh`,
`docs/research/fish/S22-D-D-deepen.md`):** S22-D-D's shortfall FF/(p0·f) is equally elastic in all three
inputs. Its weakest input, `f` (~1.74–2.05×, a proxy borrowed from `kcnk5b^alf/+`), comes from a
mechanistically different allele whose overgrowth, like lof's, grows with body size. So a needed lof/+ `f`
of ≥3.1–3.7× (calculated) is not excluded, and "most likely falls short by 1.5–2×" falls to undetermined.
Key number: break-even `f` = 3.1–3.7× (calculated), ~3.5–4.6× if nr21/+ shortens the pectoral 10–20%
(illustrative).

**My verdict: WEAKENED.** The headline verdict (S22-D-D's quantitative "most likely short" falls to
undetermined) survives, and my correction makes it stronger. The **key number** is defective. It was computed
at S22-D-D's *central* `p0` only, which hides the `p0` uncertainty that the parent itself reported. Everything
below is either quoted with a read-level or labelled **calculated** (by me, independently, from the stated
inputs). I ran no experiment.

---

## 1. Independent arithmetic (calculated)

Inputs as stated by the claim and its parent S22-D-D (branch `claude/s22-d-sensitive-input-pwechp`, read
in this repo): `p0` = 0.208 SL (range 0.173–0.260, S22-D-D figure-read plus resection-fraction inference),
`f` = 1.74–2.05× (proxy), FF = 0.65–0.77 SL (search-summary, carried over).

| Quantity | Claim | My recomputation (calculated) |
|---|---|---|
| Baseline shortfall FF/(p0·f), central p0 | 1.52–2.13× | 1.524–2.128× ✔ |
| Break-even `f` = FF/p0, central p0 | 3.1–3.7× | 3.125–3.702× ✔ |
| Break-even with s = 0.9 / 0.8, central p0 | 3.5–4.1 / 3.9–4.6× | 3.47–4.11 / 3.91–4.63× ✔ |
| Elasticity of S w.r.t. each input | equal | ∂lnS/∂ln(FF) = +1, ∂lnS/∂ln(p0) = ∂lnS/∂ln(f) = −1 ✔ |

The arithmetic is correct for the inputs the author chose to use.

## 2. The defect: the key number drops the `p0` range (calculated)

S22-D-D (read in this repo, its §3b table) bracketed `p0` at **0.17–0.26** for 60%–40% resection. Its own
required-fold column was **2.5× – 4.4×**. S22-D-D-D's `S22-D-D-deepen_calc.py` hard-codes `P0 = 0.208` and
reports break-even `f` as 3.1–3.7×. That narrows the interval by about 2× without justification. Over the full
`p0` range (calculated by me):

| s (nr21/+ pectoral factor, illustrative) | Break-even `f`, central p0 (claim) | Break-even `f`, p0 0.173–0.260 (mine) |
|---|---|---|
| 1.0 | 3.13–3.70× | **2.50–4.45×** |
| 0.9 | 3.47–4.11× | **2.78–4.95×** |
| 0.8 | 3.91–4.63× | **3.13–5.56×** |

Shortfall over the full `p0` range: **1.22–2.56×** (calculated), against the claim's 1.52–2.13×.

What this changes:
- At its low end the break-even (2.50×) sits only **1.22×** above the proxy's top value (2.05×) (calculated).
  The claim says a value ≥3.1× "is not excluded". The honest statement is weaker in one way and stronger in
  another. The parent's shortfall was never far from parity even *on the proxy*, because a 40%-resection
  reading of D18 Fig 1A plus the caudal alf/+ value already gives a 1.22× shortfall.
- So the verdict "falls to undetermined" **survives, and is reinforced**. The defect is in the precision of
  the reported key number, not in the direction of the verdict. A reader who takes "3.1–3.7×" at face value
  would think the proxy has to be wrong by at least 1.5×, when 1.2× is enough.

## 3. Proxy check: is `f` the right quantity?

- The decision quantity is **Rz = double-mutant pectoral/SL** (`lat4a^nr21/+; kcnh2a^lof/+`), as the claim
  itself says. `f` is a factorisation of Rz, not a measurement of it. Agreed.
- **Small inconsistency in the answer sentence.** It says "the needed **lof/+** `f` of ≥3.1–3.7×". That is
  only the lof/+ requirement if s = 1 (nr21/+ does not shorten the pectoral). The claim's own §2.3 says nr21/+
  shortens all fins alone. So the lof/+ single-mutant requirement is break-even/s, which is higher. The 3.1–3.7×
  figure is the **double-mutant** requirement. This is wording, not arithmetic, but it conflates the two genotypes.

## 4. Hidden assumption: does "grows with body size" point anywhere?

The claim's key causal sentence is that the alf proxy comes from an allele "whose overgrowth (like lof's) grows
with body size". *My inference:* this argument is **symmetric**. If both alleles show positive allometry
(P14 alf/+ k = 1.88 vs wt 1.29, via S22-D-D; IJ00 abstract for lof), size-dependence makes the proxy
unreliable but gives **no direction**. It does not make a larger lof/+ `f` more likely than a smaller one.
The mechanistic difference (Stewart 2021: Kcnh2a is not downstream of calcineurin, unlike Kcnk5b/alf) is also
directionless. The claim's conclusion is "undetermined", not "probably reaches parity", so it does not
overreach on this point. I relaxed the assumption (treated size-dependence as directionless) and the verdict
"undetermined" still holds. With the full `p0` range it holds more easily (§2).

Also untested by either party: equal resection fraction across genotypes in D18 Fig 1A. If alf/+ fins were
resected at a different fraction, the 1.74× ratio moves too. The magnitude is **unknown**.

## 5. Evidence level

- The key number is correctly labelled **calculated**. The s values are correctly labelled **illustrative**.
  "Measured lof/+ pectoral fold-change: unknown" is honest. I found no case of a derived number presented as
  measured.
- The recorded evidence level for the claim is "unknown". The claim's own note says full-text text reads plus
  an abstract, with the decisive figure could-not-access. That fits a **text-only/inference** grade. It should
  not be upgraded.
- **I could not re-verify the author's full-text quotes in this pass.** pmc.ncbi.nlm.nih.gov served a
  reCAPTCHA/bot page (≈21 kB HTML) for PMC8217709 (Stewart 2021) and PMC9172250 (Daane 2021). bioRxiv
  returned HTTP 429. So the Stewart 2021 and preprint quotes rest on the author's read, not on mine.

## 6. Counter-example / missed source search (scope stated)

I tried to find any measured `kcnh2a^lof/+` (or double-mutant) pectoral/SL value that would settle the question:

| Route | Read-level | Result |
|---|---|---|
| Iovine & Johnson 2000, PMC1461173 article page | **abstract** (HTML 200, sha256 `a938b458…bb8e`, text is front matter + abstract only) | No number |
| Same, PDF `/articles/instance/1461173/pdf/10880491.pdf` | **could-not-access** (reCAPTCHA page). Not defeated | — |
| Europe PMC REST fullTextXML, PMC1461173 and PMC9172250 | **could-not-access** (HTTP 500) | — |
| bioRxiv 10.1101/2021.03.05.434157v1.full | **could-not-access** (HTTP 429) | — |
| WebSearch (standard), one query on kcnh2a lof/+ pectoral length/SL, Daane 2021 Fig 4 | **search-summary** | Found ZFIN record ZDB-FIG-221222-35 (Daane 2021 Fig 4). Per the search summary: panel B = pectoral length normalised by SL, panel D = fold change relative to lof/+ (expression). **No numerical values** |
| zfin.org/ZDB-FIG-221222-35 direct | **could-not-access** (TLS chain failure through the proxy, even with the session CA bundle; same failure S22-D recorded) | — |

Negative result, scoped to the above: **no measured value of `f` or Rz found**. I did not find a published
counter-example that bounds lof/+ pectoral overgrowth either above or below 3×. Not searched: Goldsmith et al.
2003, later Iovine-lab and Harris-lab papers, and any thesis data.

## 7. Verdict

**WEAKENED.** The claim's arithmetic is correct at central `p0`, and its labels are honest. Its qualitative
verdict (S22-D-D's "most likely short by 1.5–2×" is undetermined; the qualitative "no numerical cross-species
comparison" point stands) **survives**. The **key number is overstated in precision**. With the `p0` range S22-D-D itself
reported (0.173–0.260), break-even double-mutant `f` is **2.5–4.5×** (calculated), not 3.1–3.7×. It is
2.8–5.0× / 3.1–5.6× if nr21/+ shortens the pectoral by 10% / 20% (illustrative). The low end is only 1.22×
above the proxy, which makes "undetermined" *more* secure than the claim shows. Two smaller defects: the
answer mislabels the double-mutant requirement as a "lof/+" requirement, and the "grows with body size"
argument is directionless (harmless only because the claim concludes "undetermined").

```swarm-challenge
{"claim_id": 109, "outcome": "weakened", "reason": "Arithmetic and the 'undetermined' verdict hold, but the key break-even f of 3.1-3.7x uses only the central p0 (0.208) and drops the parent's own p0 range 0.173-0.260, which gives 2.5-4.5x (calculated), only 1.22x above the proxy at the low end; the answer also calls the double-mutant requirement a lof/+ requirement.", "corrected_value": "break-even double-mutant pectoral fold-overgrowth f = 2.5-4.5x (calculated over p0 0.173-0.260 SL, FF 0.65-0.77 SL, s=1); 2.8-5.0x (s=0.9) and 3.1-5.6x (s=0.8), s illustrative; shortfall on alf proxy 1.22-2.56x (calculated); measured value unknown", "depends_on": ["S22-D-D p0 range 0.173-0.260 SL (figure-read of Daane 2018 Fig 1A wt 0.104 Growth/STL plus inferred 40-60% resection, branch claude/s22-d-sensitive-input-pwechp)", "S22-D-D proxy f 1.74-2.05x (kcnk5b alf/+, D18 Fig 1A pectoral figure-read and Perathoner 2014 Fig 1E caudal eye-read)", "Flying-fish target pectoral/SL 0.65-0.77 (search-summary, sources disagree)", "Shortfall model S = FF/(p0*f) (S22-D-D)", "Assumption: equal resection fraction across genotypes in D18 Fig 1A", "nr21/+ pectoral shortening factor s unknown (author's illustrative 0.8-1.0)", "Author's full-text quotes from Stewart 2021 and Daane 2021 preprint (not re-verified by me; PMC/bioRxiv gated this session)", "Iovine & Johnson 2000 abstract: lof positive allometric growth", "Negative search for measured kcnh2a lof/+ or double-mutant pectoral/SL (scope in section 6)"]}
```
