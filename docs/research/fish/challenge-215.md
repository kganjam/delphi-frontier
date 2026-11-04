# Challenge 215: adversarial review of the S26 scope statement

**Claim under review** (a scope statement; recorded evidence level `unknown`, value `n/a`):

> SCOPE OF WHAT S26 RESTS ON: the ORDER OF MAGNITUDE of active stiffening is confirmed by the paper's own
> abstract (>10x). The exact 12x factor, and therefore the exact 5.7x margin, depend on a boundary condition
> that could not be checked.

I could not find this sentence in any branch of this repository. I searched every `origin/*` ref under
`docs/` for "order of magnitude of active stiffening" and "boundary condition that could not", and got no
hits. So I judge the sentence as written, against its upstream chain:

- `S26-deepen.md` and `S26_deepen_calc.py` on `origin/claude/deepen-s26-active-stiffening-48xj8q`, the source
  of the 5.7x. Read in full.
- `challenge-92.md`, `replicate-92.md` and `challenge-159.md` on their own branches. Read in full.

**Verdict: WEAKENED.** Three parts of the claim do not hold:

- The abstract is not an independent confirmation of the 12x.
- What the abstract confirms is not *active* stiffening in the sense S26 needs.
- The boundary condition behind the 12x *can* be checked, and I checked it. It is not what carries the
  5.7x. The input that carries the 5.7x is the baseline the 12x is multiplied onto. That input moves the margin
  from 5.7x to 1.6x, while moving the factor itself from 12x to 10x only moves the margin from 5.7x to 4.7x.

All numbers below are **calculated** by me with `python3 -I`, unless they are tagged as a source value. I
measured nothing.

## Source read this session

Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243, PMC2359861 (doi 10.1098/rsif.2006.0181).

- **Read-level: full-text.** I fetched the PMC HTML with curl and stripped the tags myself, with no summarizer
  in between.
- I also read the abstract separately through the Europe PMC REST API (read-level: **abstract**).

Verbatim fragments:

- Abstract: "a variation in ray stiffness over more than an order of magnitude depending on actuation at the
  bases of the fin rays". It is preceded by "The model agrees well with the experiment; both show ...".
- Methods: "Experiments were also done comparing the stiffness (force per unit deflection) of the fin ray when
  both hemitrich bases are fixed to prevent sliding to the stiffness when one hemitrich base is fixed and the
  second is free to slide (see §5.2). The cantilevered ray was deflected by applying a point force about
  two-thirds of the way along the ray."
- Methods: the fish "were euthanized with tricaine methanesulphonate (MS-222)". The tests were "performed with
  the rays submersed in water within 48 h". The base offset was reproduced with "small clips". The paper says
  "Experiments to measure mechanical properties were done on 24 separate rays."
- Fig. 7a caption: "The ray is clamped horizontally at the base, and a vertical point force is applied at
  two-thirds of the distance from the ray base to the tip ... a slope of 1.98 N m−1, about 12 times the value
  when one hemitrich is free."
- Fig. 7b caption: the model's clamped/one-free ratio "transitions from 3 to 100". The text of §5.2 says "a
  factor of 4 (for G = 3) to 100 (for G > 10^5)". **Preserved:** the paper disagrees with itself on the lower
  end, 3 versus 4.
- Tip condition: the CT scans "find that the two hemitrichia appear to be fused there". The paper also says "it
  is unclear whether the hemitrichia tips are always fused".

## 1. Independent arithmetic

Inputs:

- EI_req = 6.3e-4 N m^2 (S6-D, calculated upstream).
- Isometric scale factor (120/40.3)^4 = **78.6**.
- Two baselines:
  - the relay, 3.8e-6 N m^2;
  - the primary-derived one-hemitrich-free value, 1.07e-6 N m^2. This is 1.98 N/m treated as a cantilever with
    k = 3EI/a^3, a = (2/3)(40.3 mm), divided by 12. I re-derived it and got the same value.

| Baseline | Active factor needed | Margin at 12x | at 10x (the abstract's floor) | at 4x / 3x (model lower end) |
|---|---|---|---|---|
| relay 3.8e-6 | 2.11x | **5.69x** | 4.74x | 1.90x / 1.42x |
| primary one-free 1.07e-6 | 7.49x | **1.60x** | 1.33x | 0.53x / 0.40x (fail) |

The 5.7x reproduces. **There is no arithmetic fault.**

## 2. "Confirmed by the paper's own abstract": a restatement, not a confirmation

The abstract and the Fig. 7 caption are the **same paper, the same experiment and the same authors**. The
abstract says model and experiment "both show" the >10x. The only experimental number behind it is the one
~12x comparison in Fig. 7a. The paper says 24 rays were tested overall, but no n or spread is given for this
comparison. The model only says the ratio could be anywhere from 3 (or 4) to 100, depending on G.

So the abstract is a lower read-level summary of the 12x. It cannot corroborate the 12x. Calling it
confirmation counts one source twice. **The order of magnitude rests on effectively n = 1, exactly as the exact
12x does.** That is my inference from the text above.

## 3. Proxy: what the abstract measures is not the active gain S26 needs

The ratio is **both hemitrich bases fixed by clips** against **one base free to slide**. It was measured on dead,
excised rays (MS-222, tested within 48 h). The authors call this "actively vary fin-ray stiffness". That wording
is **the authors' interpretation**; no muscle was activated.

S26 needs a different ratio: **the stiffness of a living ray with its muscles contracted, divided by the same
ray with its muscles relaxed.** In an intact fin, both hemitrich bases stay attached to tendons and soft
tissue. So the relaxed baseline is very probably *stiffer* than "one base free to slide". That makes the
realisable active gain **≤ 12x**, by an amount that is `unknown`. Challenge-159 §5 made the same point.

No measurement of that ratio exists within my search scope (see §6). On the relay baseline, the yes still
holds down to a factor of 2.1x. On the primary baseline, it fails below 7.5x. So whether the true in-vivo gain
is above or below 7.5x matters, and it is not established.

## 4. "A boundary condition that could not be checked": it can be checked

The full text is open access and states the conditions:

- a cantilever clamped horizontally at the base;
- a point load at about 2/3 of the length;
- both bases fixed, compared with one base free to slide;
- natural tips, which appear fused on CT.

I read this directly this session. So the boundary condition of the **12x** is checkable, and it has been
checked.

What remains unchecked about the 12x:

- n and spread for this comparison (not reported);
- whether the tested ray's tip was fused. The model's ratio depends on the tip condition, and the authors say
  fusion is not certain.

Neither of these is "a boundary condition that could not be checked" in the sense the claim gives.

There **is** an unchecked boundary condition that carries the result, but it belongs to the **baseline**, not to
the 12x. The base condition of the relayed 3.8e-6 N m^2 is unknown:

- I did not access Flammang 2013 or Puri 2018 this session.
- Upstream reports Flammang's full text as could-not-access and Puri's as read full-text.

The 12x is a ratio over a one-base-free state. Multiplying it onto a baseline that is not one-base-free
mismatches the boundary conditions. The relay sits **3.55x** above the primary-derived one-free value.

## 5. Hidden assumption: the claim points to the wrong input

The phrase "the exact 12x ... and therefore the exact 5.7x margin" implies that uncertainty in the factor is
what limits the margin. Relaxing each input in turn (calculated, §1):

- Factor 12x → 10x, the abstract's floor: margin 5.7x → **4.7x**.
- Baseline relay → primary one-free: margin 5.7x → **1.6x**.
- Isometric scaling relaxed: challenge-92 and replicate-92 show the margin falls to below 1 under whole-fish
  isometry or a diameter exponent b < 0.89 on the primary baseline. I did not re-run these; this is relayed.
- EI_req at the replicate-72 upper corner of 3.1e-3: the primary path fails (needs 37x). This is from
  challenge-92; I checked it as 3.1e-3/(1.07e-6 × 78.6) = 36.9x.

So the exactness of the 12x is the **least** influential input. A scope statement that names it as the
dependency of the 5.7x leaves out the inputs that can flip the sign of the result.

## 6. Regime, taxon and counter-examples

**Search.** One standard web search ("fin ray hemitrich bilaminar stiffness clamped versus free ratio
measurement trout OR zebrafish OR synthetic"). It found:

- no second clamped-versus-free ratio in any species (only Alben 2007's sunfish ~12x, restated);
- no zebrafish measurement;
- a rainbow-trout micromechanics programme (Barthelat lab), whose clamped/free ratio I did not find. I read
  search-summary only; I did not open the PDFs.

An APS DFD 2021 abstract titled "Active Control of Caudal Fin-Ray Stiffness and Propulsion" appeared in the
results. I did not read it, so I make no claim about its content.

Scope: that one search plus the single full-text fetch. Google Scholar, Web of Science and ZFIN were not
searched.

**Unresolved disagreement, preserved.** The Flammang 2013 abstract gives 565e-6 N m^2. Upstream read it at
abstract level; I did not re-read it. That is ~149x the relay value for the same species. If both describe the
same ray in different states, the in-vivo stiffness range would exceed 10x by far. If they do not, it says
nothing about the factor. I cannot tell which, and I do not average the two.

## 7. Evidence level

`unknown` / `n/a` is not honest for a statement that asserts a confirmation.

- The ">10x" is an **authors' summary claim**, read at abstract and full-text level. It comes from one
  experimental comparison plus a model.
- The 5.7x is **calculated**, and it is conditional on a relayed baseline and an isometric-scaling assumption.

The claim should carry those labels. It presents nothing as measured that is not, so this is a labelling gap,
not a fabrication.

## 8. What survives

- The ">10x" wording is accurately quoted from the abstract.
- The 12x is reported in the full text.
- The 5.7x arithmetic is correct.
- The 12x is a single comparison with no spread reported.

What does not survive:

- "confirmed": it is the same source restated;
- "active": it is clip-imposed on dead, excised rays;
- "could not be checked": the 12x boundary condition is stated in an open-access full text;
- the implication that the margin depends mainly on the 12x: it depends mainly on the baseline, which gives a
  margin of 5.7x to 1.6x, and on scaling.

**Corrected scope statement (my wording):**

> The ~12x is one clip-clamped, both-bases-fixed versus one-base-free comparison on an excised bluegill ray
> (Alben 2007, full-text). The abstract's ">10x" restates it together with a model range of 3–100x, and does
> not independently confirm it. The in-vivo active gain is unmeasured and probably ≤12x. The 5.7x margin
> depends chiefly on multiplying that ratio onto the relayed 3.8e-6 baseline, whose base condition is
> unknown. On the primary-derived one-free baseline the margin is 1.6x, and it fails below a 7.5x factor.

```swarm-challenge
{"claim_id": 215, "outcome": "weakened", "reason": "The abstract's '>10x' restates the same single clip-clamped vs one-base-free comparison on dead excised bluegill rays (plus a 3-100x model range) rather than independently confirming active stiffening, the 12x boundary condition is stated in the open-access full text and so is checkable, and the 5.7x margin depends chiefly on the baseline the ratio multiplies (relay 3.8e-6 gives 5.7x; primary-derived one-free 1.07e-6 gives 1.6x) not on the exactness of 12x (12x->10x only moves 5.7x->4.7x).", "corrected_value": "margin of the measured ~12x: 5.7x (relay baseline) to 1.6x (primary-derived one-free baseline); 4.7x to 1.3x at the abstract's 10x floor; fails on the primary baseline for any in-vivo gain below 7.5x (calculated)", "depends_on": ["Alben, Madden & Lauder 2007 PMC2359861 full-text (read directly this session): both bases fixed vs one free to slide, cantilever, point load at ~2/3 L, 1.98 N/m, ~12x, euthanized excised rays with clips, 24 rays tested overall with no n for this comparison", "Alben et al. 2007 abstract: stiffness variation over more than an order of magnitude, model and experiment 'both show'", "Alben et al. 2007 model clamped/one-free ratio 3 (caption) or 4 (text) to 100 depending on G", "S26-D: EI_req 6.3e-4 N m^2 per ray (S6-D calculated) and isometric (120/40.3)^4 = 78.6 scaling (assumption)", "Puri 2018 relay of bluegill ray EI 3.8e-6 N m^2 citing Flammang 2013, base condition unknown (not read by me)", "S26-D cantilever back-calculation: one-free EI 1.07e-6 N m^2 from 1.98 N/m at L = 40.3 mm (assumption: tested ray = group max length)", "challenge-92 / replicate-92: margin falls below 1 under whole-fish isometry or sub-isometric ray diameter on primary baseline (relayed, not re-run)", "Flammang 2013 abstract 565e-6 N m^2, ~149x the relay, unresolved (relayed)"]}
```
