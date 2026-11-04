# Challenge 134: adversarial review of S26-D ("S26's 'no' falls")

**Claim under review** (claim 134, source `harvest:deepen-s26-active-stiffening-48xj8q`; the author's
document is `docs/research/fish/S26-deepen.md` and `S26_deepen_calc.py` on
`origin/claude/deepen-s26-active-stiffening-48xj8q`, commit `95578def`, both read in full by me):

> S26's 'no' falls. The 165x gap compares the passive EI of a ≤40 mm bluegill ray (3.8e-6 N m^2) with a
> per-ray requirement for a 120 mm ray (6.3e-4 N m^2). Under isometric L^4 scaling the passive gap shrinks
> to ~2.1x. The single measured ~12x hemitrich-locking factor closes that gap with ~5.7x margin.

**My verdict: WEAKENED.** The diagnosis holds: S26's 165x compares two rays of different sizes, so S26's
"no" does not follow. The **5.7x margin** does not hold. It comes from multiplying a relayed EI whose
base condition is unknown by a locked/unlocked ratio from a different measurement. If both states are
taken from the one primary measurement (Alben 2007), the margin is **~1.6x** (calculated). At that margin,
a ray only ~11% thinner than isometry predicts reverses the result. Nothing in this review was measured by me.

## 1. Arithmetic, redone independently (calculated)

| Quantity | Mine | Author's |
|---|---|---|
| (120 / 40.3)^4 | 78.61 | 78.6 |
| 3.8e-6 × 78.61 | 2.99e-4 N m^2 | 3.0e-4 |
| active factor needed, 6.3e-4 / 2.99e-4 | 2.11x | 2.1x |
| margin of 12x | 5.69x | 5.7x |
| Alben back-calculation: k = 3EI/a^3, k = 1.98 N/m, a = (2/3)(40.3 mm) | EI_clamped = 1.28e-5, one-free = 1.07e-6 N m^2 | same |

The arithmetic is correct. I found no error in it.

## 2. The proxy, and the double-use of the locking factor (the main defect)

The inequality is `F_a × EI_base(120 mm) ≥ EI_req`. For it to mean anything, **EI_base must be the
*unlocked* state that F_a multiplies.** F_a = 12 is Alben et al. 2007's ratio of "both hemitrich bases
clamped" to "one hemitrich free".

- The 3.8e-6 N m^2 is a one-sentence relay in Puri et al. 2018, citing Flammang et al. 2013. The author
  reports that its base condition is **not stated**, and so does Alben's own 1e-6 to 1e-5 range. The
  author's own cross-check puts 3.8e-6 *between* Alben's unlocked (1.07e-6) and locked (1.28e-5) states.
  It is 3.6x above the unlocked value.
- The claim treats 3.8e-6 as the unlocked baseline. That is an **unstated assumption**, and the 5.7x margin
  depends on it.
- **An internally consistent version (my calculation, from the author's own inputs).** Take both states from
  the single Alben 2007 measurement, then scale isometrically to 120 mm:

| Bluegill source ray length | locked EI at 120 mm | locked / EI_req | unlocked EI at 120 mm | factor needed |
|---|---|---|---|---|
| 40.3 mm (assumed, group max) | 1.01e-3 N m^2 | **1.60x** | 8.4e-5 | 7.5x |
| 30 mm | 1.35e-3 | 2.15x | 1.1e-4 | 5.6x |
| 20 mm | 2.03e-3 | 3.22x | 1.7e-4 | 3.7x |

  At the author's own chosen length (40.3 mm), the margin is **1.6x, not 5.7x**.
- **My inference:** the author's 5.7x carries a ~3.6x boost. It comes from the relayed 3.8e-6 sitting above
  Alben's unlocked state while being multiplied by the full 12x. If 3.8e-6 was itself measured with the base
  clamped (the usual mounting for an excised-ray bending test), the remaining active factor is ~1, and the
  scaled gap of 2.1x stays open. I cannot rule this reading out. Flammang's methods are inaccessible (see §5).

## 3. The hidden assumption that carries the result: isometry, tested relaxed

EI ∝ E·d^4. "L^4" is only a stand-in for d^4 under isometry. What matters is the **ray's cross-section
(d)**, not its length. A margin M in EI therefore tolerates a diameter shortfall of only M^(1/4) (calculated):

- Author's basis (M = 5.69): the result flips if the 120 mm ray is thinner than **65%** of the isometric
  diameter.
- Alben-consistent basis (M = 1.60): it flips below **89%** of isometric diameter. That is an ~11% slenderness
  excess.

Flying-fish pectoral rays are long relative to body size. The author says so, and gives the direction of
the allometry as unknown. An ~11% departure from isometry in diameter is small compared with ordinary
interspecific allometric variation. That last statement is my judgement, not a sourced number. **No
exocoetid ray diameter or EI was found** (scope: the author's searches and S6-D's 35-hit Europe PMC search;
I ran no new ray-diameter search). So the conclusion rests on an untested ratio, and on the Alben-consistent
basis that ratio has little room.

Other robustness checks on the Alben-consistent basis (40.3 mm, locked, calculated):
- tip-heavy load (EI_req × 1.47): 1.09x, which barely passes;
- the replication's upper corner (EI_req = 3.1e-3): **0.32x, fail**. The author reports a pass here
  ("needs 10.4x"), but only on the 3.8e-6 basis;
- halving the locking factor to 6x: on the unlocked basis it needs 7.5x, so **fail**.

## 4. Evidence level

The ledger records this claim as **"measured"**. **That is a defect.** The author's own `swarm-result` says
"derived: calculation on a cross-taxon proxy… size-corrected under an isometric-scaling assumption". The key
number (3.0e-4 N m^2) is calculated from a relayed value times an assumed scaling law. The only measured
inputs are Alben's 1.98 N/m and the 12x ratio (n = 1 as reported), and the 40.3 mm ray length. The author
labels each one honestly in the text. The ledger label should be **calculated / derived**, not measured.

## 5. Sources and counter-evidence

| Source | What I used | Read-level |
|---|---|---|
| Author's S26-deepen.md + calc script | all inputs and working | full-text |
| Flammang, Alben, Madden & Lauder 2013, *J Morphol* 274:1044, doi:10.1002/jmor.20161 | abstract: EI "calculated to be 565 × 10^-6 Nm2", in an **in vivo** vortex-jet perturbation; no specimen length or base condition in the abstract | abstract (Europe PMC REST, fetched by me) |
| Alben et al. 2007; Puri et al. 2018 | the values as relayed by the author | listing (via the author's document; I did not re-read them) |

- **The disagreement is preserved, not averaged.** Flammang's abstract value (565e-6 N m^2, in vivo) is ~150x
  the relay (3.8e-6). If the in-vivo value is the right baseline, the size-corrected passive ray is already
  ~70x over the requirement: 565e-6 × 78.6 ≈ 4.4e-2 N m^2, calculated. Active stiffening would then be
  unnecessary, not "sufficient with margin". On the excised-ray basis, the margin is ~1.6x. These two readings
  lead to different answers, and **neither is resolved here.**
- I found no second measured locked/unlocked ratio in any taxon. Scope: I did not search for one. I rely on
  the author's two web searches and Das et al. 2024, as reported by the author.

## 6. What survives

- S26's 165x is a size-mismatched comparison. Its "no" does not follow from it. **This part of the claim
  survives.**
- "Active stiffening can carry the load with ~5.7x margin" **does not survive** as stated. A defensible
  restatement (calculated):

  > On internally consistent excised-ray data (Alben 2007), an isometric 120 mm bluegill-proportioned ray
  > meets the per-ray requirement when fully locked, with ~1.6x margin. The margin fails at the replication's
  > upper EI_req corner. It also fails if ray diameter falls more than ~11% below isometry. It further
  > depends on n = 1 for the locking ratio, and on muscles reaching full clamping in vivo. The in-vivo
  > Flammang value (unresolved) would make the question moot.

```swarm-challenge
{"claim_id": 134, "outcome": "weakened", "reason": "The 165x size-mismatch diagnosis holds, but the 5.7x margin multiplies a relayed EI of unknown base condition (3.8e-6, which sits 3.6x above Alben's own unlocked state) by Alben's full 12x locking ratio; taking both states from Alben's single measurement gives ~1.6x margin. That margin is lost with an ~11% sub-isometric ray diameter or at the replication's upper EI_req corner, and the ledger's 'measured' label is wrong for a calculated value.", "corrected_value": "locked isometric 120 mm ray EI ~1.0e-3 N m^2 vs required 6.3e-4 N m^2: margin ~1.6x (calculated), not 5.7x", "depends_on": ["Alben, Madden & Lauder 2007: clamped point-load stiffness 1.98 N/m at a=2/3 L, ~12x vs one-hemitrich-free, n=1 as reported (as relayed in S26-deepen.md)", "Alben et al. 2007: bluegill max pectoral ray length 40.3 mm, used as tested-ray length (author's assumption, retained)", "S6-D required EI 6.3e-4 N m^2 per ray for L=0.12 m (calculated upstream)", "replicate-72 EI_req upper corner 3.1e-3 N m^2", "challenge-72 tip-heavy load factor x1.47", "Puri et al. 2018 relay of 3.8e-6 N m^2 with unstated base condition", "Flammang et al. 2013 abstract: 565e-6 N m^2 in vivo (read by me, abstract level; disagreement unresolved)", "assumption: uniform Euler-Bernoulli cantilever for back-calculating EI from 1.98 N/m", "assumption: EI scales as d^4 with diameter; isometry d~L tested relaxed"]}
```
