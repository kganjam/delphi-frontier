# Challenge 109: adversarial review of S22-D-D-D (the pectoral fold-overgrowth `f`)

**Claim under review** (source `harvest:deepen-s22-d-d-input-vncsjh`, file
`docs/research/fish/S22-D-D-deepen.md` on branch `claude/deepen-s22-d-d-input-vncsjh`). The author says:
S22-D-D's shortfall FF/(p0·f) is equally elastic in all three inputs. Its weakest input, `f` (~1.74–2.05×,
borrowed from `kcnk5b^alf/+`), comes from a mechanistically different allele whose overgrowth grows with body
size. So a `lof/+` `f` ≥ 3.1–3.7× (calculated) is not excluded, and S22-D-D's "most likely falls short by
1.5–2×" **falls** to undetermined. Key number: break-even `f` = 3.1–3.7× (calculated).

**Outcome: WEAKENED.** The core conclusion survives: `f` is an unvalidated proxy, and a match is not
excluded. Two parts do not survive. The key number is quoted too narrowly. The "falls" verdict also rests on
treating direction-free evidence as if it pushed `f` upward.

I ran no experiment. Every number below is either quoted with its read-level or **calculated** by
`challenge-109_calc.py` (this directory) from inputs the author and S22-D-D state. No figure was read.

---

## 1. Arithmetic, redone independently

Inputs as the author states them: FF = 0.65–0.77 SL (search-summary), `p0` = 0.208 SL (S22-D-D figure-read
plus inference, bracket 0.173–0.260 for 60–40 % resection), `f` = 1.74–2.05× (proxy).

- Baseline shortfall 0.65/(0.208·2.05) = 1.52× to 0.77/(0.208·1.74) = 2.13× (calculated). **Matches.**
- Break-even `f` at `p0` = 0.208: 3.13–3.70× (calculated). **Matches.**
- With nr21/+ shortening s = 0.9 or 0.8 at `p0` = 0.208: 3.47–4.11× and 3.91–4.63× (calculated). **Matches**
  the author's "~3.5–4.6×".
- "Equally elastic": S is a pure ratio, so d ln S / d ln x = ±1 for each input. **Correct**, and exact.

**Defect 1: the key number drops S22-D-D's own `p0` uncertainty.** The author takes `p0` from S22-D-D, and
S22-D-D gives a bracket of 0.17–0.26, not a point. Over that bracket the break-even `f` is
**2.50–4.44×** (calculated; S22-D-D's own table at lines 137–139 shows the same 2.5–4.4×). The author's key
number, 3.1–3.7×, is the central row only. At the favourable end (`p0` = 0.26) the proxy (2.05×) misses
break-even by only **1.22×** (calculated). With illustrative nr21/+ shortening the full range becomes
2.8–4.9× (s = 0.9) or 3.1–5.5× (s = 0.8) (calculated, s not measured). This error does not hurt the author's
"not excluded" conclusion. It helps it. But a key number that reports one row of a three-row bracket is
overconfident, and later work will copy it.

## 2. Proxy check

The quantity that matters is Rz, the double-mutant (`lat4a^nr21/+; kcnh2a^lof/+`) pectoral length/SL at the
body size Daane et al. measured. `p0·f` stands in for it, and `f` in turn stands in via `alf/+`. The author
names this correctly and correctly says Rz is `unknown` (P1 Fig 4B, preprint Fig 8B and Data S1
could-not-access). I tried again this session. The Fig 4 image at `cdn.ncbi.nlm.nih.gov` was refused by the
proxy (CONNECT 403). Europe PMC `PMC9172250/fullTextXML` returned HTTP 500. **Rz is still `unknown`.** No
proxy problem beyond the one the author already flagged.

## 3. The hidden assumption that carries "falls": the evidence is treated as balanced when it is not

The author's §2 lists three new full-text points, then says "Points 2 and 3 push `f` in opposite directions,
and I cannot net them out." I tested each for **direction**. My inference follows each author's claim.

1. **Different mechanism** (Stewart 2021, full-text: Kcnh2a, unlike Kcnk5b/alf, is not downstream of
   calcineurin. Perathoner 2014, full-text: lof adds segments, alf elongates them). *My inference:* this
   shows the proxy is unvalidated. It says nothing about whether lof/+ overgrows the pectoral **more or
   less** than alf/+. It has no direction.
2. **lof overgrowth grows with size** (Stewart 2021, full-text, caudal regenerates; Iovine & Johnson 2000,
   abstract: positive allometry). *My inference:* this does not push `f` up either. The author's own §2.2
   says alf/+ overgrowth is also allometric (P14: k = 1.88 vs 1.29). So both alleles' `f` rise with SL, and
   the SL of the fish in P1 Fig 4B is `unknown`. If those fish were small, lof/+ `f` would be at the low end
   of its own curve. The point widens the error bar in both directions. It has no direction. It is also not
   new: S22-D-D already labelled its result "size-confounded".
3. **nr21/+ shortens all fins** (Daane 2021 preprint, full-text, author's quote). *My inference:* this is the
   only new point with a direction, and that direction is **toward S22-D-D's shortfall**. The same quoted
   sentence says the double mutant had "wild-type sized medial fins". So in the medial fins nr21/+ fully
   cancelled lof/+ overgrowth. That suggests the nr21/+ effect is not small. Whether it is as large in the
   pectoral is `unknown`, because the paired fins were still "overgrown" (author's claim).

**So the claim misstates the balance.** It is not "two inputs pushing opposite ways". It is two
direction-free widenings plus one push toward the shortfall. Relaxing the author's assumption (that point 2
pushes `f` up) leaves the conclusion like this:

- "Most likely short by **1.5–2×**" does not survive. The proxy cannot fix the *magnitude*, and the
  break-even sits only 1.22–2.6× above the proxy (calculated, full `p0` bracket).
- "Undetermined" is defensible. But the honest wording is that the only directional evidence leans toward
  a shortfall, and that lean is unquantified. It is not that the evidence is symmetric. "Falls" overstates how
  far S22-D-D moved. S22-D-D's own swarm-result already said "calculated on a proxy, size-confounded, not
  observed". What this pass actually added is the mechanism mismatch, which is direction-free.

## 4. Evidence level

- The key number is labelled "calculated". **Honest.** The illustrative s values are labelled illustrative.
  **Honest.**
- The harvest records evidence level `unknown`. The author's own note says full-text (three sources) plus
  abstract (one), with the decisive figure could-not-access. The harvest field under-reports what the author
  had. That is a harvesting defect, not one of the author's.
- Iovine & Johnson 2000. I re-checked: the PMC1461173 article page (HTTP 200) holds only the abstract. The
  PDF link served the same proof-of-work bot gate the author met, and I did not try to defeat it. Europe PMC
  `fullTextXML` returned HTTP 500. **Abstract** is the correct read-level. The author's use of it
  (positive allometry, sof one-half length) matches the abstract text I saw.

## 5. Counter-examples or missed regimes

- **Missed in this review, scope stated:** I found no published numeric pectoral fold-change for
  `kcnh2a^lof/+`. I searched the IJ00 PMC page (abstract only), and S21 and P14 are covered by the author's
  string search, which I did not repeat. I did not search ZFIN, Goldsmith et al. 2003, or later Iovine-lab
  papers. So this is not a negative over the literature. It covers only the sources listed.
- **Regime the author partly missed:** the paired-vs-medial asymmetry of the double mutant. Medial fins are
  wild-type sized, paired fins are overgrown (preprint, author's quote). That means lof/+ and nr21/+
  interact in a fin-specific way. A single multiplicative s applied to an independently borrowed `f` may be
  the wrong model form, because the pectoral outcome is not `p0·f_lof·s` if the two effects interact. *My
  inference.* It does not change the outcome. Rz must be read directly.
- I tried to break "equally elastic" and the arithmetic, and could not. Both hold.

## 6. Verdict

**WEAKENED.** The author is right that S22-D-D's "most likely short by 1.5–2×" cannot stand, because `f` is a
cross-locus proxy with no validated magnitude, and right that the qualitative point (no numerical
cross-species comparison by Daane et al.) stands. Two things are wrong. (a) The key break-even number should
be **2.5–4.4×** over S22-D-D's own `p0` bracket, not 3.1–3.7×. (b) The claim says the new evidence pushes
`f` both ways. In fact the size-dependence and mechanism points have no direction, and the only directional
point (nr21/+ shortening, which fully resets the medial fins) leans toward a shortfall. Correct status of the
S22-D-D headline: the magnitude is undetermined, with an unquantified lean toward a shortfall. Measured
`kcnh2a^lof/+` pectoral fold-change and Rz: **`unknown`**.

```swarm-challenge
{"claim_id": 109, "outcome": "weakened", "reason": "Arithmetic and the 'undetermined' conclusion hold, but the key break-even number omits S22-D-D's own p0 bracket (true range 2.5-4.4x, calculated) and the 'falls' verdict treats direction-free evidence (mechanism mismatch, size-dependence shared by both alleles) as pushing f upward while the only directional new evidence (nr21/+ shortening, medial fins reset to wild type) leans toward the shortfall.", "corrected_value": "break-even kcnh2a lof/+ pectoral fold-overgrowth f = 2.5-4.4x (calculated over p0 0.17-0.26 SL and FF 0.65-0.77 SL; 3.1-3.7x at p0 = 0.208 only; ~2.8-5.5x if nr21/+ shortens the pectoral 10-20%, illustrative); measured lof/+ pectoral fold-change and double-mutant pectoral/SL: unknown", "depends_on": ["S22-D-D: shortfall = FF/(p0*f) (calculated)", "S22-D-D figure-read D18 Fig 1A wt dashed line 0.104 Growth/STL and inferred p0 = 0.104/(resected fraction 0.4-0.6) = 0.17-0.26 SL", "S22-D-D proxy f = 1.74x (alf/+ pectoral, D18) to 2.05x (alf/+ caudal, Perathoner 2014 Fig 1E eye-read)", "Flying-fish target pectoral/SL 0.65-0.77, E. volitans (search-summary, sources disagree)", "Stewart 2021 (full-text, via author): Kcnh2a unlike Kcnk5b/alf not downstream of calcineurin; lof t2/+ regenerates keep growing to 30 dpa", "Iovine & Johnson 2000 (abstract, re-checked this session): lof positive allometric growth", "Perathoner 2014 (full-text, via author): alf/+ caudal allometric k 1.88 vs wt 1.29", "Daane 2021 preprint (full-text, via author): lat4a nr21/+ shortens all fins; double mutant has wild-type sized medial fins and overgrown paired fins", "Double-mutant pectoral/SL Rz unknown (Daane 2021 Fig 4B could-not-access, re-tried this session: CDN proxy 403, Europe PMC 500)", "Fish SL at measurement in Daane 2021 Fig 4B unknown"]}
```
