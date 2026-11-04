# Challenge 312: adversarial review of S40-D-D (the ΔE-sensitivity deepening of S40 cell)

Claim under review: S40-D-D, `docs/research/fish/S40-D-deepen.md` on branch
`claude/deepen-s40-sensitive-input-93jzo8`, which I read in full (**full-text**, the repository file), together with
its script `S40-D-sensitivity.py` and the parent `S40-cell.md` (branch `claude/s40-cell-membrane-conductance-oar3jg`,
**full-text**). Date: 2026-11-04. Every number I label **[computed]** comes from my own script,
`docs/research/fish/challenge-312-check.py`. I wrote it from the stated model equations and did not copy the author's
code.

**The claim, as stated.** The S40 verdict is decided almost entirely by the isolated-domain offset ΔE. Below about
10.3 mV, C2 fails whatever the conductance. Above it, no surrogate misses by 2 orders. A 2-fold K⁺ conductance contrast
(the *alf* oocyte figure) bounds ΔE at ≤ 12.0–15.4 mV for D = E_L − E_K = 70–90 mV. That puts the fin in S40's worst
corner. So "C2 not refuted from below" stands on a thin margin, and "G_j is the binding variable" falls.
Recorded evidence level: derived. Verdict: stands.

**My verdict: WEAKENED.** The arithmetic is right. The finding that the decision turns on ΔE is right, and so is the
finding that G_j is not the binding variable. What does not survive is the claim that the fin sits above the threshold,
even on a thin margin. That rests on two choices that the 12–15.4 mV figure hides: the optimum baseline Vm and slab
geometry. Hold the K⁺ contrast at the same 2-fold but let the surround rest at the depolarised fibroblast Vm that the
author themself cites (−16 to −25 mV). ΔE then falls to 2.4–15.0 mV, and most of that range lies below the threshold
**[computed]**. The sign of the margin is therefore unknown, not "thin but positive".

---

## 1. Independent arithmetic [computed]

| Quantity | Author | Mine | Agrees? |
|---|---|---|---|
| S40 slab grid (27 cells, ΔE 15/30/50, w 50/200/1000 µm, G_j 0.2/1/2 nS) | S40 table | identical to 2 s.f. in all 27 cells | yes |
| Worst-corner gap to Hosoi-low (5 µS/cm²) | 9.7× | 9.66× | yes |
| Elasticity of g_m,req with respect to ΔE: worst corner at 15 mV / central case at 30 mV | −3.6 / −2.5 | −3.64 / −2.47 | yes |
| ΔE at which g_m,req = 100× Hosoi-low: worst corner / central case | 10.3 / 10.0 mV | 10.300 / 10.000 mV | yes |
| ΔE_max = D(√f − 1)/(√f + 1) at f = 2 | 15.4 / 12.0 mV (D 90 / 70) | 15.44 / 12.01 mV | yes. I re-derived the optimum r = 1/√f by setting dΔE/dr = 0 |
| f_min table (10/15/30/50 mV at D = 90 and 70) | 1.56/1.96/4.0/12.3 and 1.78/2.39/6.25/36 | same | yes |
| E_K from Nernst at 28 °C, [K⁺]ᵢ 140, [K⁺]ₒ 3–5 mM | −86 to −100 mV | −86.5 to −99.7 mV (RT/F = 25.95 mV) | yes |
| Slab solution V_centre = ΔE(1 − e^(−w/2λ)) | stated | re-derived: inside ΔE + A·cosh(x/λ), outside B·e^(−x/λ), continuity of V and V′ at x = h gives A = −ΔE·e^(−h/λ) | yes |

I found no arithmetic error.

One wording point. "Any ΔE below ~10.3 mV makes C2 fail regardless of conductance" is strictly true only below
10.0 mV, where V_centre < 10 mV for every g_m. Between 10.0 and 10.3 mV, C2 fails because of the 2-order *decision
rule*, not because of physics: a large enough g_m still works there **[computed]**. This is minor, but the sentence
merges a physical impossibility with a rule threshold.

---

## 2. Proxy check: what stands in for what

**Proxy 1. The *alf* "almost two-fold increase in K⁺ conductance" stands in for the wild-type regional contrast f in
the cell's total dominant K⁺ conductance.** The claim already flags this, but it is three steps removed from f:

1. It compares a mutant channel with the wild-type channel, each expressed alone in *Xenopus* oocytes
   (**[measured]** per Perathoner et al. 2014, PLoS Genet 10:e1004080). I did not re-read the paper and rely on S40's
   quotation. S40 reports its read-level as full-text.
2. It is the fold-change of one channel's conductance. f in the ΔE_max formula is the fold-change of the cell's whole
   g_K. Kcnk5b is one of several K⁺ conductances (S40 itself names *kcnh2a*). **[inference]** If Kcnk5b carries only a
   fraction of g_K, doubling it gives f < 2. So as a guide to f, the proxy errs on the high side.
3. Nothing about a mutant fold-change bounds wild-type regional contrast in either direction. Regional channel
   expression can differ by more than 2-fold, and nothing found shows that it does in fin. **[inference]** Calling
   12–15.4 mV an "upper bound" is valid only conditional on f = 2. It is not an upper bound on the fin's ΔE.

**Proxy 2 (not flagged by the author). ΔE_max stands in for ΔE.** ΔE_max is the maximum over the baseline ratio
r = g_K/g_L, reached at r = 1/√f. That optimum forces a specific surround Vm **[computed]**:

| E_L, E_K | Surround Vm at the optimum (f = 2) |
|---|---|
| 0, −86 mV | −35.6 mV |
| 0, −100 mV | −41.4 mV |
| −20, −86 mV | −47.3 mV |
| −20, −100 mV | −53.1 mV |

So 12–15.4 mV assumes the surround rests at about −36 to −53 mV. No fin Vm is measured (S40 §2a; S40-D-D §2). The
author's own cited fibroblast range is −25 to −16 mV (Silic & Zhang 2023, as read by S40-D-D). Kohl & Gourdie report
isolated cardiac fibroblasts at −10 to −20 mV (via S40). Both are more depolarised than the optimum.

---

## 3. Hidden assumptions, tested relaxed [computed]

### 3a. Baseline Vm: pin it to a measured value instead of optimising it

I fixed the surround Vm, which fixes r for given E_L and E_K. I then gave the domain f = 2 times more g_K ("up") or
2 times less ("down"):

| Surround Vm | E_L 0, E_K −86 | E_L 0, E_K −100 | E_L −10, E_K −86 | E_L −10, E_K −100 | E_L −20, E_K −86 | E_L −20, E_K −100 |
|---|---|---|---|---|---|---|
| −16 mV | 11.0 / 7.2 | 11.6 / 7.3 | 5.1 / 2.9 | 5.2 / 2.9 | n/a | n/a |
| −20 mV | 12.5 / 8.7 | 13.3 / 8.9 | 7.7 / 4.6 | 8.0 / 4.7 | n/a | n/a |
| −25 mV | 13.7 / 10.4 | 15.0 / 10.7 | 10.1 / 6.7 | 10.7 / 6.8 | 4.3 / 2.4 | 4.4 / 2.4 |
| −35 mV | 14.8 / 13.0 | 16.9 / 13.8 | 12.6 / 10.0 | 14.1 / 10.5 | 9.4 / 6.5 | 10.3 / 6.7 |
| −50 mV | 13.2 / 14.8 | 16.7 / 16.7 | 12.4 / 12.9 | 15.4 / 14.3 | 11.3 / 10.6 | 13.6 / 11.5 |

Each cell gives ΔE (mV) for the up / down direction. n/a means Vm ≥ E_L, which is impossible in a two-conductance
cell. (This table is a subset of my script output. The −60 and −75 mV rows are in the script.)

At the depolarised fibroblast Vm the author cites (−16 to −25 mV), f = 2 gives ΔE from 2.4 to 15.0 mV. Of those 28
feasible values, 9 clear 10.3 mV: the four E_L = 0 "up" values at −16 and −20 mV, all four E_L = 0 values at −25 mV,
and one E_L = −10 value at −25 mV (10.7 mV). The other 19 do not. Once E_L ≤ −10 mV, every value is at or below
10.7 mV. **[inference]** At a 2-fold contrast, the fin is as likely to sit in the region where C2 fails whatever the
conductance as in S40's worst corner. The claim's "puts the fin in S40's worst corner" needs a baseline Vm of roughly
−35 to −55 mV, which is unmeasured.

### 3b. D = E_L − E_K

At f = 2, ΔE_max ≥ 10 mV needs D ≥ 58.3 mV, and ΔE_max ≥ 10.3 mV needs D ≥ 60.0 mV **[computed]**. The claim uses
D = 70–90 mV. That rests on the assumed E_L of 0 to −20 mV. A Cl⁻-dominated leak would push E_L more negative and
shrink D. The fin E_L is **unknown**, and I did not search for a fin E_Cl. **[inference]** The margin on D is about
10 mV at the low end of the author's range.

### 3c. Geometry: slab versus disk versus sphere

S40 uses a 1-D slab. Fin mesenchyme between hemirays is closer to a sheet (2-D). A compact patch is closer to a sphere.
For the same isotropic lattice λ = a√(G_j/G_m), I re-derived the centre potential:

* 2-D disk: V₀ = ΔE·(1 − ρK₁(ρ)), with ρ = R/λ. This uses the Wronskian I₀K₁ + I₁K₀ = 1/ρ.
* 3-D sphere: V₀ = ΔE·(1 − (1 + ρ)e^(−ρ)).

| Geometry | Refutation ΔE, worst corner (w 50 µm, G_j 2 nS) | Gap at ΔE 12.0 | Gap at ΔE 15.44 |
|---|---|---|---|
| slab (S40) | 10.30 mV | 26× | 8.7× |
| disk | 10.82 mV | 55× | 23× |
| sphere | 11.52 mV | 84× | 39× |

The central case (200 µm, 1 nS) refutes at 10.0 mV in all three geometries. **[computed]**

A wider domain loses less to its surround than a narrower one, so the slab is the most optimistic case. Relaxing the
slab moves the threshold from 10.3 up to 10.8–11.5 mV. In a spherical patch at ΔE = 12 mV, the gap comes within a
factor of 1.2 of the 2-order rule. The claim's "~10.3 mV" holds only for the slab. None of the three geometries
flips the verdict at ΔE ≥ 12 mV, so this weakens the margin but does not refute.

### 3d. Assumptions I did not test

* The isopotential extracellular space, already flagged by the author through Liu et al. 2026 (search-summary there).
* Voltage dependence of Kcnh2a.
* Unequal g_m inside and outside the domain. At the optimum, the domain's g_m is about 1.4× the surround's
  **[computed: (1+√2)/(1+1/√2)]**. Untested.

---

## 4. Evidence level

The recorded level is "derived", and that is honest. The key number is computed, and the document labels it
**[computed]** in place. The verdict word "stands", however, carries a premise that the label hides. The claim says
the fin sits *above* threshold, but that position comes from an optimised baseline (§3a), not from a measured fin Vm
or a measured f. It is not mislabelled as measured, but it overstates how firmly the realistic case has been located.

---

## 5. Counter-examples and regimes missed

* **Regime missed: a depolarised resting tissue (§3a).** This is the author's own cited fibroblast range, so it is
  internal to the evidence base, not new literature.
* **Regime missed: non-slab domains (§3c).**
* **Published counter-example: none found.** I ran no new literature searches in this review, so this is not a
  search result. It means no source was added beyond the documents named above. No calibrated fin Vm or regional fin
  K⁺ conductance is known to me from those documents. Their own negative-search scopes apply: S40 ran about 10 web
  searches and S40-D-D ran 5. PubMed was unreachable in both.

---

## 6. What survives

* The arithmetic (§1).
* ΔE, not G_j, decides the answer. g_m,req diverges as ΔE → 10 mV, while G_j enters linearly. I confirmed this, and
  it holds in all three geometries.
* "C2 is not refuted from below by any data found" is still formally true, because no measurement of ΔE, f or fin Vm
  exists to refute it.

## 7. What does not survive

* "ΔE ≤ 12–15.4 mV ... puts the fin in S40's worst corner." At f = 2 the realistic ΔE is **2.4–16.9 mV across the
  tested baselines** (−16 to −50 mV, E_L 0 to −20 mV), and **2.4–15.0 mV at the cited depolarised fibroblast Vm**
  **[computed]**. Much of that range is below the 10.0–11.5 mV threshold, where C2 fails whatever the conductance.
  The margin's *sign* is undetermined. It is not established as thin and positive.
* "~10.3 mV" as the threshold. It is 10.3–11.5 mV depending on domain geometry **[computed]**.

**Correct statement.** With a 2-fold K⁺ contrast, C2 is undecided. ΔE is 12–15.4 mV only at the optimal baseline
Vm of −36 to −53 mV. At the depolarised fibroblast Vm the author cites, it is 2.4–15.0 mV. The refutation threshold is
10.3 mV (slab) to 11.5 mV (sphere). Settling it needs a calibrated fin resting Vm as well as f. Calibrated ASAP1
imaging, S40-D-D's proposed decisive test, would give both.

### Sources (read-level)
* S40-D-D, `S40-D-deepen.md` and `S40-D-sensitivity.py` (branch `claude/deepen-s40-sensitive-input-93jzo8`):
  **full-text**.
* S40-cell.md (branch `claude/s40-cell-membrane-conductance-oar3jg`): **full-text** (sections 1–3 read).
* Perathoner et al. 2014, PLoS Genet 10:e1004080: **could-not-access** in this review. I did not attempt to fetch it.
  Its values are used only as quoted in S40, which gives its read-level as full-text.
* Silic & Zhang 2023, Cells 12:1148: **could-not-access** in this review (not fetched). The fibroblast range of −25 to
  −16 mV is used only as quoted in S40-D-D.
* Kohl & Gourdie 2014: **could-not-access** in this review (not fetched). Values are taken via S40.

```swarm-challenge
{"claim_id": 312, "outcome": "weakened", "reason": "Arithmetic and the dE-not-Gj sensitivity finding reproduce, but dE 12-15.4 mV holds only at an optimised surround Vm of -36 to -53 mV; at the author's own cited depolarised fibroblast Vm (-16 to -25 mV) a 2-fold K+ contrast gives dE 2.4-15.0 mV, mostly below a threshold that is itself 10.3-11.5 mV depending on slab/disk/sphere geometry, so the sign of the C2 margin is undetermined rather than thin-but-positive.", "corrected_value": "dE at f=2: 12.0-15.4 mV only at optimal baseline; 2.4-15.0 mV at surround Vm -16 to -25 mV; refutation threshold 10.3 mV (slab) to 11.5 mV (sphere)", "depends_on": ["S40 syncytial model lambda = a*sqrt(Gj/Gm) with isopotential extracellular space", "computed: slab/disk/sphere centre-potential solutions (challenge-312-check.py)", "assumption: two-conductance cell V = (gK*EK + gL*EL)/(gK + gL)", "measured (via S40, not re-read): alf kcnk5b ~2-fold K+ conductance in Xenopus oocytes (Perathoner 2014) as proxy f=2", "measured (via S40-D-D, not re-read): generic vertebrate fibroblast Vm -25 to -16 mV (Silic & Zhang 2023) as surround baseline", "assumption: EL 0 to -20 mV, EK -86 to -100 mV (Nernst, assumed [K+])", "S40 surrogates: Hosoi & Slayman 1985 5-15 uS/cm2; Kohl & Gourdie 2014 100-330 uS/cm2 (computed)", "S40 placeholders: a = 10 um, A_cell = 800 um2, Gj 0.2-2 nS, w 50-1000 um", "S40 refutation rule: >=2 orders below requirement", "negative: no fin resting Vm, fin EL, or regional fin K+ contrast in S40/S40-D-D search scope; no new searches run in this review"]}
```
