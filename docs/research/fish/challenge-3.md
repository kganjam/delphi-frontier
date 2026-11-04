# Challenge 3: "Speed deficit is 10.4× and kinetic-energy deficit is 109× for the 1-BL wing case"

**Claim under attack.** `docs/research/fish/zebrafish-glide-physics.md` (branch
`origin/claude/zebrafish-glide-physics-j176og`), §3 table and §5 verdict. Recorded evidence level
is `derived`, value 10.4 (ratio), source "computed".

**Reviewer's status.** This is a desk review. I ran no experiment. Every number I give below is
**calculated** by me with the script in Appendix A unless I tag it as
a literature value with a read-level. Literature searches were done through a web-search tool;
I opened no full texts this session.

**Verdict: `weakened`.** The arithmetic is correct and the evidence label `derived` is honest.
The failure is in how the number is framed. It is presented as *the* deficit, but it is really an
**upper-bound-style ratio** with two choices built in. (1) The denominator is a sustained speed,
Ucrit, standing in for the burst exit speed the physics actually needs. (2) The wing shape is
fixed at AR = 5 with C_L = 0.6. For the same 1-BL span, relaxing that shape alone moves the
speed ratio from 10.4× down to ≈ 3.6–6.6×. There is also a small internal inconsistency in the
denominator (0.548 vs 0.560 m/s). The qualitative conclusion, that a launch-speed deficit
exists, is **not** refuted.

---

## 1. Arithmetic, redone independently

Inputs as stated by the author: m = 0.4 g, g = 9.81 m/s², ρ_air = 1.2 kg/m³, span b = 1 BL =
0.04 m, AR = 5, C_L = 0.6, level glide L = W.

- W = 4.0e-4 × 9.81 = 3.924e-3 N.
- S = b²/AR = 1.6e-3 / 5 = 3.20e-4 m² (3.20 cm²).
- V = √(2W / (ρ S C_L)) = √(7.848e-3 / (1.2 × 3.20e-4 × 0.6)) = √(7.848e-3 / 2.304e-4)
  = √34.06 = **5.836 m/s** (calc).
- Speed ratio against 0.560 m/s: 5.836 / 0.560 = **10.42×** (calc). KE ratio = 10.42² =
  **108.6×** (calc). The author's 10.4× and 109× **reproduce**.
- Speed ratio against 0.548 m/s: 5.836 / 0.548 = **10.65×**, and KE ratio **113.4×** (calc).

**Defect (minor, internal consistency).** The §3 table divides by 0.560 m/s. That is the
*secondary* Plaut value [author's S9, `search-summary`]. The §5 verdict says: "The only measured
adult swimming speed retrieved is Ucrit, **0.548 m/s**. That is a **10.4×** speed deficit and a
**109×** kinetic-energy deficit." Those two numbers do not follow from 0.548. With 0.548 they
would be 10.65× and 113×. The difference is ~2 % in speed and ~4 % in energy, so it changes
nothing qualitatively. But the sentence pairs a denominator with a ratio that was not computed
from it.

The KE ratio is just (V_req/V_exit)², because mass cancels. It is a ratio of exit kinetic
energies, **not** a ratio of muscle work. The author does not claim otherwise, but the label
"kinetic-energy deficit" may be read as an energy-budget gap. The real work needed to reach a
given exit speed in water also includes added-mass acceleration, hydrodynamic drag on the run-up,
and water-exit losses. All of these are omitted. *Inference (mine):* the muscle-work ratio would
therefore be **larger** than the KE ratio at fixed speeds. Its magnitude is unknown, and I did
not compute it.

## 2. Input data: a proxy quantity is doing the work

The denominator is **Ucrit**, a stepped-velocity test minutes long [author's S7/S9,
`search-summary`]. What the claim needs is the **burst (fast-start) speed at water exit**. The
author discloses this in the §5 caveat. The headline number is still computed against the proxy.

What I found on the correct quantity:
- **Adult zebrafish fast-start peak velocity: `unknown`.** Scope of my negative search: two web
  searches ("adult zebrafish fast-start escape peak velocity m/s high-speed video"; "zebrafish
  Danio rerio adult burst swimming speed BL s-1 / cm s-1 C-start maximum velocity", extended
  mode). Neither returned a measured adult value. This agrees with the author's three negative
  searches. The results surfaced larval values (3.6 mm larvae, mean size-specific maximum
  velocity 50–66 BL/s; Transactions of the American Fisheries Society 115:143, 1986, "Burst-swimming
  performance of larval zebra danios", `search-summary`). They also surfaced a cross-species
  statement that maximum burst speed is "10 L s⁻¹ on average" across 27 species (Frontiers in
  Physiology 2012, doi:10.3389/fphys.2012.00035, `search-summary`; the species set and sizes were
  not retrieved). That is not a zebrafish value, and it is *below* the measured zebrafish Ucrit of
  18 SL/s. So it cannot be used as a zebrafish burst estimate, and I do not use it.
- The direction of the bias is not in doubt: burst speed exceeds Ucrit. This is general fish
  physiology (*inference*, though a standard one). So **10.4× is an over-estimate of the
  speed deficit against the quantity that matters**, by the unknown factor burst/Ucrit.
- Illustration only, with **assumed** burst speeds, not measured (calc): at 0.8 / 1.0 / 1.2 m/s
  (20 / 25 / 30 BL/s) the 1-BL, AR 5, C_L 0.6 ratios become 7.3× / 5.8× / 4.9× in speed and
  53× / 34× / 24× in KE.

## 3. Hidden assumption: "1-BL wing" silently fixes AR = 5 and C_L = 0.6

"The 1-BL wing case" names only the **span**. The required speed depends on **area**, and the
area is S = b²/AR. Fixing AR at 5 gives a 1-BL wing a chord of only 0.8 cm. A low-aspect-ratio
fin, which is closer to what an enlarged pectoral fin is likely to be (*inference*), has much
more area at the same span. Low-AR plates also tend to delay stall through tip-vortex lift
(qualitative, from search-summary listings of oscillating/static low-AR wing studies; no C_L
numbers at Re 1e3–1e4 were retrieved).

Sensitivity at fixed 1-BL span (all calc; denominator 0.560 m/s, with 0.548 in brackets):

| AR | S (cm²) | C_L | V_req (m/s) | speed ratio | KE ratio |
|---|---|---|---|---|---|
| 5 | 3.20 | 0.6 | 5.84 | **10.4×** (10.7×) | **109×** (113×) |
| 5 | 3.20 | 1.0 | 4.52 | 8.1× (8.3×) | 65× (68×) |
| 3 | 5.33 | 0.6 | 4.52 | 8.1× (8.3×) | 65× (68×) |
| 2 | 8.00 | 0.6 | 3.69 | 6.6× (6.7×) | 43× (45×) |
| 2 | 8.00 | 1.0 | 2.86 | 5.1× (5.2×) | 26× (27×) |
| 1 | 16.0 | 0.6 | 2.61 | 4.7× (4.8×) | 22× (23×) |
| 1 | 16.0 | 1.0 | 2.02 | 3.6× (3.7×) | 13× (14×) |

So the "1-BL" headline spans **3.6×–10.7× in speed and 13×–113× in KE**, depending on two design
choices that the label hides. The author's case is the **worst corner** of this grid. Whether
C_L = 1.0 is attainable at Re ≈ 2e3–4e3 is `unknown`. I searched for steady-translating low-AR
flat-plate C_L,max at Re 1e3–1e4 and found qualitative statements only. Taira & Colonius 2009
(JFM, Re 300/500) was listed but no values were retrieved (`listing`). The arXiv study of swept
low-AR wings at Re 400 (arXiv:2011.12336, `abstract`) gives no numbers in its abstract. The
C_L = 1.0 rows are therefore sensitivity cases, not claims. The AR rows need no aerodynamic
assumption beyond the author's own C_L = 0.6. They only reflect that a lower-AR wing of the same
span has more area.

Note also that lowering AR raises the chord and so raises Re. At AR 1, c = 4 cm and V = 2.6 m/s,
which gives Re ≈ 6,900 (calc). The author's §1 Re argument (Re pinned at 1.9e3–4.0e3) assumed
AR 3–8, so this lever slightly helps the C_L assumption rather than hurting it.

Other assumptions I tested and found **not** to matter much:
- **Level glide (L = W).** In a steady glide at angle γ, L = W cos γ, so V_req scales as √cos γ.
  At γ = 10° / 20° / 30° the reduction is 0.8 % / 3 % / 7 % (calc). This is negligible unless the
  glide is very steep.
- **Air density, g.** These are standard values, with no material effect.

## 4. Mechanisms or counter-examples missed

- **Freshwater hatchetfishes (Gasteropelecidae)** are small (a few cm) characiforms that leave the
  water using enlarged pectoral girdles and elongate pectoral fin rays. Wiest (1995, J. Zool.
  236:571–592) is cited as showing by high-speed video that their jumps are **ballistic, not
  powered flight** (FishBase family summary and a J. Exp. Biol. jumping-kinematics paper citing
  Wiest; both `search-summary`; Wiest's take-off velocities were **not retrieved**). This is the
  nearest-size natural counter-example. It **supports** the author's conclusion rather than
  breaking it: a fish of this size has evolved water exit, not gliding. It is a published
  comparison the author did not use. Wiest's take-off speed would be the best available empirical
  upper bracket on exit speed for a ~cm-scale fish. Its value is `unknown` to me.
- **Surface taxiing** (keeping the tail in the water to keep accelerating after the wings are
  out) is listed by the author as a design lever, so it is not missed. It would change the
  denominator from "exit speed from a C-start" to "speed reached during a taxi run". No zebrafish
  number exists for that.
- **Body lift.** The fish body's own planform (~4 cm × <1 cm) adds lifting area that the S = b²/AR
  model omits. Its contribution is `unknown`, and I would expect it to be small at these
  incidences (*inference*). It would reduce V_req slightly.

## 5. Is the evidence level honest?

Yes, with one qualification. `derived` / "computed" is correct: the ratio is arithmetic on a
`search-summary`-level literature value (Ucrit) and on assumed design parameters (AR 5, C_L 0.6).
Nothing is presented as observed. The qualification is about how the numbers are presented. The
§5 verdict states "a **10.4×** speed deficit" as a property of the fish. It is a property of
*one chosen wing geometry* measured against *a sustained-speed proxy*. The ledger value should
carry those two conditions in the claim text, or it will be quoted as the deficit.

## 6. What survives

- The arithmetic (10.42×, 108.6× against 0.560 m/s) is correct.
- A large launch-speed deficit exists across the whole grid in §3 when measured against Ucrit
  (≥ 3.6× in speed, ≥ 13× in KE, calc). It persists against assumed 20–30 BL/s bursts for the
  author's geometry. The qualitative verdict, "launch speed is the hardest barrier", is not
  challenged here.

## 7. Recommended restatement

> "For a 1-BL-span wing at AR 5 and C_L 0.6, the required glide speed (5.84 m/s, calc) is
> 10.4× the secondary Ucrit value of 0.560 m/s (10.7× against 0.548 m/s), i.e. 109–113× in exit
> kinetic energy (derived). Ucrit is a sustained-speed proxy; adult burst speed is unknown, so
> this overstates the burst deficit by an unknown factor. At the same span, AR 1–2 gives
> 3.6–6.6×."

## Sources

| Source | Read-level | Used for |
|---|---|---|
| Author's report and `zebrafish_glide_calc.py` (branch `claude/zebrafish-glide-physics-j176og`) | full-text | claim, inputs |
| Ucrit 0.548 ± 0.007 m/s = 18.0 BL/s, adult zebrafish (PLoS ONE "Establishing zebrafish as a novel exercise model", surfaced in search) | search-summary | denominator check |
| PMC7842627, Ucrit protocol for adult zebrafish | listing | context only |
| Larval zebra danio burst swimming, Trans. Am. Fish. Soc. 115:143 (1986) | search-summary | larval 50–66 BL/s, not used numerically |
| Frontiers in Physiology 2012, doi:10.3389/fphys.2012.00035 ("10 L s⁻¹ on average", 27 species) | search-summary | shown to be inapplicable |
| Wiest, F.C. (1995) J. Zool. 236:571–592, hatchetfish locomotory apparatus | search-summary (via FishBase family page and seriouslyfish.com); paper **could-not-access** | counter-example class |
| Taira & Colonius (2009) JFM, low-AR flat plates at Re 300/500 | listing | C_L values not retrieved |
| arXiv:2011.12336, low-AR swept wings at Re 400 | abstract | no numbers in abstract |

## Appendix A: reviewer's script (calc)

```python
import math
W=0.4e-3*9.81; rho=1.2; b=0.04
for U in (0.548,0.560):
  for AR in (5,3,2,1):
    for CL in (0.6,1.0):
      S=b*b/AR; V=math.sqrt(2*W/(rho*S*CL))
      print(U, AR, CL, S*1e4, V, V/U, (V/U)**2)
for g in (10,20,30,45): print(g, math.sqrt(math.cos(math.radians(g))))
V=math.sqrt(2*W/(rho*(b*b/5)*0.6))
for Ub in (0.8,1.0,1.2): print("assumed burst", Ub, V/Ub, (V/Ub)**2)
```

```swarm-challenge
{"claim_id": 3, "outcome": "weakened", "reason": "Arithmetic reproduces (5.836/0.560 = 10.42x, 108.6x KE), but the ratio is computed against a sustained-speed proxy (Ucrit) instead of the unknown burst exit speed, the verdict pairs it with the 0.548 m/s value it was not computed from (that gives 10.65x / 113x), and the unstated AR = 5, C_L = 0.6 choice puts it at the worst corner of a 3.6x-10.7x range for the same 1-BL span.", "corrected_value": "10.4x (vs 0.560 m/s) or 10.7x (vs 0.548 m/s) speed and 109-113x KE, conditional on AR 5 and C_L 0.6 and on Ucrit as the denominator; an upper bound on the burst-speed deficit; 3.6-6.6x speed (13-43x KE) at AR 1-2 for the same span"}
```
