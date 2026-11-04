# Challenge 295 — adversarial review of [S40] fin-mesenchyme membrane conductance

Target claim (claim_id 295), recorded evidence level **derived**, source `harvest:s40-cell-membrane-conductance-oar3jg`
(reviewed at commit `f7cddad`, file `docs/research/fish/S40-cell.md`, read at **full-text** — the whole document).

> "A syncytial length-constant model requires fin-mesenchyme membrane conductance of roughly 1e-9 to 4.8e-5 S/cm2
> (central case ~2e-7) to hold >=10 mV; the two measured mesenchymal surrogates (5-15 uS/cm2 mouse L-cell
> fibroblasts; ~1-3.3e-4 S/cm2 cardiac fibroblasts in situ) lie above this except in the narrow-domain/strong-coupling
> corner where one sits ~1 order below, so C2 is not refuted from below, but no fin-mesenchyme conductance or
> gap-junction conductance has been found, so C2 is not settled."
> KEY: 4.8e-5 S/cm2 (worst-case required g_m; dE=15 mV, w=50 um, Gj=2 nS, a=10 um, A=800 um2)

**Verdict: WEAKENED.** The claim's two-part conclusion ("not refuted from below, not settled") survives, and I
cannot refute C2 either. Three things do not survive: (1) the headline range's upper end, **4.8e-5 S/cm2, is not a
bound** — it is the maximum over an arbitrary input grid, and the requirement is unbounded above; (2) the two
"measured surrogates" are **not two independent measurements of membrane conductance**, and the higher one is not a
membrane conductance at all; (3) the claim as recorded presents a value the author **computed** as **measured**.

Labels used below, in the sentence where each applies: **[computed]** = arithmetic I did here;
**[measured]** = a number cited authors report observing; **[inference]** = my reading, not a source's claim.
I separate the author's claim from my inference throughout.

---

## 1. Arithmetic, redone independently — it all reproduces

I re-derived the model from the stated inputs without reading the author's working, then compared.

**The cable solution is correct.** Solving the matched steady-state problem from scratch: inside the domain
(|x| < h, h = w/2) `V_in = ΔE + A·cosh(x/λ)`; outside `V_out = B·e^(-(x-h)/λ)`. Continuity of V and of axial current
at x = h gives `B = -A·sinh(h/λ)` and hence `A = -ΔE·e^(-h/λ)`, so

  **V_centre − V_far = ΔE·(1 − e^(−w/2λ))**

which is exactly the author's expression. **[computed]** I also checked the step the author states without
showing: for a cubic lattice with a gradient along one axis only, the four transverse neighbours contribute nothing
(no transverse gradient), so the discrete balance `G_j(V_{i+1} + V_{i-1} − 2V_i) = G_m(V − E)` does give
`λ = a·√(G_j/G_m)`. That is right, and it is not a trivial step.

**All 27 grid cells reproduce.** **[computed]** Required `w/2λ = −ln(1 − 10/ΔE)` gives λ_max/w = 0.4551 / 1.2332 /
2.2407 for ΔE = 15 / 30 / 50 mV, matching the author's 0.455 / 1.233 / 2.241. Every entry in the g_m,req table
reproduces to the quoted precision, including the headline 4.8e-5 (ΔE 15, w 50 µm, G_j 2 nS) and the central
2.1e-7 (ΔE 30, w 200 µm, G_j 1 nS). Both inverse `G_j,max` tables reproduce (0.21 nS, 24 nS, 2.0 µS for Hosoi-low;
14 nS, 1.6 µS, 1.3e5 nS for Kohl-high). The implied λ range (2.8–70.7 µm) and τ_m (3–200 ms) reproduce.

**One trivial inaccuracy.** **[computed]** The grid minimum is 5.0e-10 S/cm2 (ΔE 50, w 1000 µm, G_j 0.2 nS), not
1e-9. The claim's "roughly" covers this; I note it only for completeness and do not count it as a fault.

**An assumption that cancels — credit where due.** **[inference]** The `A_cell = 800 µm²` placeholder looks load-
bearing but is not, *for the Kohl comparison*: the requirement divides by A_cell, and the author's Kohl surrogate is
itself computed as (1/R) ÷ (C/1 µF·cm⁻²) with the same area convention, so the area cancels and that comparison is
really G_m versus G_m (40–120 pS against 0.8–2.7 nS). The author does not point this out, but it makes the comparison
robust to the A_cell guess. **The cell pitch `a` does not cancel**: g_m,req ∝ a². At a = 30 µm — plausible if
intra-ray mesenchyme is sparse rather than confluent — the headline case rises 9× to **4.3e-4 S/cm2** [computed].

So: the model is sound and the arithmetic is clean. The breaks are elsewhere.

---

## 2. Break 1 — the stated upper bound is an artifact of the G_j ceiling, and the fin gene is *cx43*

The headline 4.8e-5 is the maximum over a grid whose G_j ceiling is **2 nS**, taken from cultured cardiac-fibroblast
pairs (Rook 1992) and a channel-count estimate (Kohl's "10–30 channels" × 21 pS). But the zebrafish fin size
phenotype the whole argument is about runs through **cx43** (*short fin*). I searched for measured Cx43 junctional
conductances, which the author did not:

| Preparation | G_j **[measured]** | Read-level |
|---|---|---|
| Engineered neonatal ventricular pairs, G_j vs Cx43 immunosignal | **8–50 nS** | search-summary (PMC3339855) |
| Neuro2a cells expressing Cx43, WT pairs | **~40.8 nS** (n = 10) | search-summary (PMC3848784, table) |
| WT neonatal ventricular pairs | **~80 nS** | search-summary (PMC3307380) |
| Control ventricular pairs, cardiac-restricted Cx43-KO study | **~558–588 nS** | search-summary |
| **Cx43-knockout** pairs, same study | **~4–11 nS** (21% uncoupled) | search-summary |
| Cx43-KO atrial pairs | **~24 nS** | search-summary (PMC3307380) |

**[inference]** The author's G_j ceiling of 2 nS sits below *every* measured Cx43 pair conductance I found —
including the **knockouts**. Recomputing the requirement with these values **[computed]**:

| G_j | ΔE15 / w50 | ΔE15 / w200 | ΔE30 / w200 |
|---|---|---|---|
| 2 nS (author's ceiling) | 4.8e-5 | 3.0e-6 | 4.1e-7 |
| 8 nS | 1.9e-4 | 1.2e-5 | 1.6e-6 |
| 24 nS | 5.8e-4 | 3.6e-5 | 4.9e-6 |
| 40 nS | **9.7e-4** | 6.0e-5 | 8.2e-6 |
| 80 nS | 1.9e-3 | 1.2e-4 | 1.6e-5 |

At G_j = 40 nS the requirement is **1.3 orders of magnitude above the claim's stated maximum**.

**Disagreement preserved, and a limit on this break.** A KIT project page states that because fibroblast gap-junction
channels are of low conductance, electrical coupling between fibroblasts, and between fibroblasts and myocytes,
"appears to be of lesser degree than in-between myocytes" (search-summary). The high values above are from myocytes
and expression systems, not fibroblasts. **I therefore do not assert that fin mesenchymal G_j is ~40 nS** — it is
unmeasured, exactly as the author says. My narrower point stands on its own: **2 nS is not a defensible ceiling** on
the plausible range, so a maximum computed at that ceiling is not a worst case.

**This contradicts the document's own caveat.** §5.4 of S40-cell.md says "Cx43-rich tissues can couple far more
strongly... If fin G_j is ≥10–100 nS, the narrow-domain cases fail even with the higher surrogate g_m." The author
saw this and still published a range whose top is computed at 2 nS. The caveat and the headline number are
inconsistent, and the headline number is what got recorded as the claim.

---

## 3. Break 2 — the requirement diverges as ΔE → 10 mV, so there is no finite upper end

The grid's ΔE floor of 15 mV is equally arbitrary, and here the consequence is sharper. The target is "**hold ≥10
mV**", and ΔE is unmeasured (the author says so). The requirement `w/2λ ≥ −ln(1 − 10/ΔE)` **diverges as ΔE → 10⁺**.
Any ΔE in (10, 15) mV is admissible under the claim's own framing **[computed]**:

| ΔE (w = 50 µm, G_j = 2 nS) | required g_m |
|---|---|
| 15 mV (author's floor) | 4.8e-5 |
| 13 mV | 8.6e-5 |
| 12 mV | 1.3e-4 |
| 11 mV | 2.3e-4 |
| 10.5 mV | 3.7e-4 |

**[computed]** Relaxing both inputs modestly and simultaneously — ΔE = 12 mV, G_j = 20 nS (still below most measured
Cx43 pairs), w = 50 µm — gives **1.3e-3 S/cm2**, about **1.4 orders above the claim's stated maximum**.

**[inference]** So "roughly 1e-9 to 4.8e-5 S/cm2" is not a range of required conductance. It is a range of *what this
grid happened to contain*. The true requirement has no finite upper end without a measured ΔE and a measured G_j,
neither of which exists. A reader who takes 4.8e-5 as "the worst case" — which is how the KEY field reads — is
misled about the size of the unmeasured space.

---

## 4. Break 3 — the proxy. The "two surrogates" are ~one, and the high one is not a membrane conductance

This is the substantive methodological break, and it uses the author's own model against the author's own inputs.

**The misplaced proxy, named.** Kohl & Gourdie's 0.5–1 GΩ is explicitly an ***in situ*** fibroblast resistance — a
cell sitting in tissue, coupled to its neighbours. The author divides 1/R by an *isolated*-cell capacitance and
calls the result a specific **membrane** conductance. But the input resistance of a coupled cell is not its membrane
resistance: it includes the junctional path into the syncytium. **The quantity that matters is G_m; the number used
is G_in, which contains G_m *plus the very coupling the model is about*.** That is circular — the leak term is being
smuggled into the insulation term.

**Quantified, on the author's own lattice.** For one cell in an infinite cubic syncytium (each cell: G_m to its own
reversal potential, G_j to each of 6 neighbours), the input conductance follows from the lattice Green's function:

  `G_in = 1 / [ (2π)⁻³ ∫_BZ d³k / (G_m + 2G_j(3 − cos k_x − cos k_y − cos k_z)) ]`

I evaluated this numerically **[computed]** (uniform Brillouin-zone grid; converged — identical to 4 decimal places
at n = 100, 150 and 250 per axis):

| Hosoi g_m | G_m | G_j | predicted *in-situ* R_in |
|---|---|---|---|
| 5 µS/cm² | 40 pS | 0.2 nS | **1.08 GΩ** |
| 15 µS/cm² | 120 pS | 0.2 nS | **0.94 GΩ** |
| 5 µS/cm² | 40 pS | 1 nS | 0.24 GΩ |
| 5 µS/cm² | 40 pS | 2 nS | 0.12 GΩ |

Kohl & Gourdie's **measured** in-situ value is **0.5–1.0 GΩ**.

**[inference] Two consequences.**

**(a) The preserved "disagreement" is largely not a disagreement.** Hosoi's isolated-cell membrane conductance
(5–15 µS/cm²), once the cell is embedded and coupled at G_j = 0.2 nS, predicts an in-situ input resistance of
0.94–1.08 GΩ — landing on Kohl's measured 0.5–1.0 GΩ. The author carefully refuses to average the two surrogates
and offers four hypotheses for the 1–2 order gap. The arithmetic says much of the gap needs no hypothesis: it is
gap-junctional loading, with **no difference in membrane conductance required at all**. Inverting properly at
G_j = 0.2 nS, Kohl's R_in implies g_m = **1.0e-5 to 1.15e-4 S/cm2** (against the author's naive 1.3e-4 to 2.5e-4),
whose low end coincides with Hosoi. The author's own instinct — that Kohl's remark about isolated cells having ~10×
higher resistance "pushes toward Hosoi's value" — was correct, and understated.

**(b) An internal contradiction in the author's input set.** At the author's own G_j = 1 or 2 nS, the junctional load
**alone** is 3.97 or 7.94 nS, capping R_in at **0.25 or 0.13 GΩ** *for any g_m ≥ 0*. A measured in-situ 0.5–1.0 GΩ is
then **arithmetically impossible**. The document simultaneously asserts G_j ∈ {0.2, 1, 2} nS and reads an in-situ
0.5–1 GΩ as a membrane resistance. For G_j ≥ 1 nS those are mutually exclusive — and G_j ≥ 1 nS is exactly the
corner that produces the headline 4.8e-5.

**Relaxing my own hidden assumption.** This calculation inherits the author's cubic 6-neighbour lattice with uniform
G_j. If in-situ cardiac fibroblasts couple to ~2 neighbours rather than 6, the junctional floor falls ~3× and
G_j ≈ 0.2–0.6 nS becomes consistent with the measured R_in. So result (b) is specific to 6-neighbour coupling at
G_j ≥ 1 nS; result (a) weakens but survives, because any coupling at all inflates G_in above G_m. I searched for a
measured coupled-neighbour count for cardiac fibroblasts in situ and **found none** (scope: 2 web searches, US index,
2026-11-04); a KIT page states that direct measurement of fibroblast coupling in situ is difficult (search-summary).

**Read-level, stated plainly.** I did **not** read Kohl et al. 1994 or Kamkin et al. 2002, the primary sources for the
0.5–1 GΩ; I take that value as the author reports it from the Kohl & Gourdie review. I did independently confirm via
**search-summary** that a Kamkin review reports rat atrial fibroblasts at ≈0.5 GΩ with resting Vm ≈ −22 mV, which is
consistent with what the author reported.

**What this does to the claim.** The claim's reassurance is "the two measured surrogates lie above this". After this
correction there is effectively **one** independent surrogate for mesenchymal membrane conductance (~5–15 µS/cm², and
Kohl's number is consistent with it rather than an order above it), and that one is **itself an upper bound**: Hosoi
& Slayman's own caveat is that their membrane resistance was "in the same range as the seal resistance" (10–50 GΩ),
so seal leak inflates it and the true g_m may be lower. The claim compares an upper-bound estimate against a
lower-bound requirement and reads "above, therefore not refuted" — the weak direction of a one-sided comparison.

---

## 5. Evidence level — one defect in the claim as recorded

The claim sentence calls `~1-3.3e-4 S/cm2 cardiac fibroblasts in situ` one of "the **two measured** mesenchymal
surrogates". It is not measured. It is **computed by the author**, by dividing a resistance from one preparation
(*in situ*, via Kohl 1994 / Kamkin 2002) by a capacitance from a *different* preparation (isolated cells, via Chilton
2005 / Dawson 2012), both cited secondhand through a review.

**Credit to the document:** S40-cell.md labels it **[computed]**, flags the mixed provenance in §2b, and names the
mixing as a possible cause of the disagreement. The document is honest. **The recorded claim is not** — it loses the
label and the provenance and presents the number as an observation. Per the honesty floor, a derived number presented
as measured is a defect even when the number is right; here it is also the number §4 argues is misinterpreted. The
first surrogate (5–15 µS/cm², Hosoi & Slayman) *is* measured and specific-conductivity-reported, read at **abstract**
level by the author and not re-read by me.

The overall evidence level **derived** is honest for the requirement itself.

---

## 6. Regime / taxon check, and what survives

**My own negative search, with scope.** I searched independently for zebrafish fin mesenchyme electrophysiology
(membrane potential, input resistance, patch clamp, intra-ray fibroblasts). **Nothing.** Every hit concerned
neurons, hair cells or neuromuscular junctions. Scope: 1 extended + 3 standard web searches, US index, 2026-11-04;
I did not reach PubMed, Google Scholar or Web of Science, and did not check lab supplements or theses. **The author's
central negative result is independently confirmed within this scope**, and stated precisely it is a successful
deliverable: no fin-mesenchyme membrane conductance, junctional conductance or calibrated ΔVmem is on record.

**Regimes the author flagged and I did not break:** anisotropy along vs across rays, the epidermal/transepithelial
path, extracellular resistance, transjunctional gating, voltage-dependence of g_m (Kcnh2a), heterogeneity. All
correctly listed as omitted.

**One regime worth adding.** **[inference]** The author treats the equal-λ case (same g_m inside and outside the
domain). If the domain is created by *raising* g_m inside — the natural reading of regional *kcnk5b* expression —
then λ_in < λ_out, and solving the mismatched problem gives
`V_c = ΔE·[1 − 1/(cosh(h/λ_in) + (λ_out/λ_in)·sinh(h/λ_in))]`, which is **larger** than the equal-λ result. So the
author's equal-λ assumption is *conservative* in the direction that matters, and this one cuts in the claim's favour.

**Credit, explicitly.** Sound and worth keeping: the cable derivation; the direction of the inequality (higher g_m
shortens λ and insulates, so the requirement is a genuine lower bound on g_m); the refusal to convert Heubach's
+70 mV hMSC current density into a resting conductance (§5.6 — correct, and a trap avoided); the τ_m argument that
hours-long patterns are steady-state; the sensitivity notes on A_cell and a; and the nine-item §5 list, which
anticipates several attacks including the two I pressed in §2 and §3.

---

## 7. Net effect on the verdict

| Component of the claim | Status |
|---|---|
| Cable model and all arithmetic | **Survives** — fully reproduced, independently re-derived |
| Range upper end "4.8e-5" as a worst case | **Broken** — artifact of G_j ≤ 2 nS and ΔE ≥ 15 mV; unbounded above |
| "Two measured mesenchymal surrogates" | **Broken** — ~one independent surrogate; high leg is G_in, not G_m, and is computed not measured |
| "lie above this except in [one] corner" | **Weakened** — margin thinner, and the corner widens |
| "C2 is not refuted from below" | **Survives**, but for weaker reasons than stated |
| "C2 is not settled" | **Survives** — independently confirmed negative |

**My corrections push toward refutation risk, not away from it** — which I note because it is the opposite of a
convenient finding. Raising the requirement's ceiling while the only defensible surrogate is an *upper* bound means
the comparison is tighter than the claim says, and it inverts: **[computed]** at G_j ≳ 24 nS with ΔE = 15 mV and
w = 50 µm, Hosoi's 5 µS/cm² sits **≥2.1 orders below** the requirement, which trips the refutation rule the author
states for S40 ("two or more orders below refutes"). At ΔE = 12 mV and G_j = 20 nS it is 2.4 orders below.

I still do **not** call C2 refuted, for a reason I want to be explicit about rather than hide: that corner is one
region of an input space in which **ΔE, G_j, w and a are all unmeasured**. Refuting a claim on a corner chosen after
the fact would be the same error as settling it on one, which is precisely the error §2 and §3 identify in the
original. The honest position is the author's own two-part conclusion — **not refuted, not settled** — reached with
a requirement that has no upper bound and one surrogate rather than two. The claim's *verdict* is right; its
*number* and its *margin* are not.

**The binding variable is confirmed to be G_j, more strongly than the claim says.** The author concludes this in §4.
My Cx43 numbers sharpen it: measured Cx43 pair conductances (8–588 nS) sit **above** the entire `G_j,max` column the
author computes for 50 µm domains (0.21–14 nS), and above it for 200 µm domains at the Hosoi surrogate (24–73 nS).
Whether fin mesenchyme couples like a fibroblast (weakly) or like a Cx43-rich tissue (strongly) is the whole
question, and it is unmeasured.

---

## 8. What would change *this* verdict

* A measured in-situ **coupled-neighbour count** and **G_j** for fibroblast–fibroblast pairs: this is what §4(b)'s
  impossibility result hinges on, and it is the input I could not find.
* Reading **Kohl et al. 1994** and **Kamkin et al. 2002** at full text, to confirm the 0.5–1 GΩ provenance and
  whether those authors corrected for coupling. If they did, §4 weakens substantially.
* **Perforated-patch R_in + C_m of zebrafish intra-ray mesenchyme** — the measurement the author correctly names as
  decisive. It settles the claim in either direction.
* A **measured ΔE** in fin (calibrated GEVI or dye-plus-electrode). If ΔE ≫ 15 mV, §3 collapses and the requirement
  regains a finite, low ceiling.

### Sources consulted for this review (with read-level)
* `docs/research/fish/S40-cell.md` @ `f7cddad`, the claim under review. **Full-text.**
* Cx43 pair conductances: PMC3307380, PMC3339855, PMC3848784 (table), and a cardiac-restricted Cx43-KO study
  surfaced via synapsesocial records. **Search-summary** (all four; I did not open the primary full texts).
* Kamkin review, rat atrial fibroblast ≈0.5 GΩ / Vm ≈ −22 mV; KIT/IBT project pages on in-situ fibroblast coupling
  difficulty and fibroblast:myocyte ratios. **Search-summary.**
* Kohl et al. 1994; Kamkin et al. 2002; Chilton 2005; Dawson 2012 (primaries behind the Kohl & Gourdie figures).
  **Could-not-access** — taken as the author reports them.
* Hosoi & Slayman 1985; Rook et al. 1992. **Not re-read** — taken as the author reports them (author read-level:
  abstract).
* Zebrafish fin mesenchyme electrophysiology. **Could-not-access / does not appear to exist** within the scope in §6.

```swarm-challenge
{"claim_id": 295, "outcome": "weakened", "reason": "Arithmetic and cable model reproduce exactly, but the stated upper bound 4.8e-5 S/cm2 is an artifact of an indefensible G_j ceiling of 2 nS (measured Cx43 pair conductances are 8-588 nS, and even Cx43-knockout pairs are 4-24 nS) and of an arbitrary 15 mV floor on an unmeasured dE that makes the requirement diverge as dE->10 mV, while the second 'measured' surrogate is a coupled-cell input conductance the author computed, not a measured membrane conductance, so the claim's verdict of 'not refuted, not settled' survives on one upper-bound surrogate rather than two and with no finite upper bound on the requirement.",
  "corrected_value": "worst-case required g_m is unbounded above, not 4.8e-5 S/cm2; ~1e-3 S/cm2 at dE=12 mV, Gj=20 nS, w=50 um, a=10 um, A=800 um2 (computed, and itself not a bound). Kohl cardiac-fibroblast surrogate corrected from ~1-3.3e-4 to ~1.0e-5-1.15e-4 S/cm2 once gap-junctional loading is removed at Gj=0.2 nS (computed).",
  "depends_on": ["S40 syncytial length-constant model (lambda = a*sqrt(Gj/Gm)) and its equal-lambda, isopotential-extracellular, cubic-lattice assumptions", "a = 10 um cell pitch (placeholder; g_m,req scales as a^2)", "A_cell = 800 um2 from 6-10 pF at 1 uF/cm2 (cancels in the Kohl comparison, not in the absolute requirement)", "cubic 6-neighbour lattice coordination number (carries my section 4(b) impossibility result)", "Hosoi & Slayman 1985 slope conductivity 5-15 uS/cm2, mouse L-cell fibroblasts (abstract; author-reported, seal-resistance-limited upper bound)", "Kohl & Gourdie 2014 in-situ fibroblast R_in 0.5-1 GOhm and isolated-cell C_m 6-10 pF (review full-text partial; primaries Kohl 1994 / Kamkin 2002 could-not-access)", "measured Cx43 junctional conductances 8-588 nS and Cx43-knockout 4-24 nS (search-summary, PMC3307380 / PMC3339855 / PMC3848784)", "report that fibroblast-fibroblast coupling is weaker than myocyte-myocyte coupling (search-summary, KIT/IBT) - limits how far the Cx43 values transfer", "the >=10 mV target threshold for C2, which is what makes the requirement diverge as dE -> 10 mV", "the S40 refutation rule that >=2 orders below the requirement refutes", "the negative result that no fin-mesenchyme g_m, G_j or calibrated dVmem exists in the searched literature (scope in section 6)", "absence of a measured in-situ coupled-neighbour count for cardiac fibroblasts (negative, scope in section 4)"]}
```
