# S25-D-D: deepening S25-D at its weakest input, whether the Flammang ray and the Alben ray are the same size

Project: `zebrafish-flight`. Scale: organ. Date: 2026-11-04.
Parent: S25-D, `docs/research/fish/S25-deepen.md`, commit `96cf4982` (branch
`origin/claude/deepen-flammang-fin-ray-stiffness-vvpk2v`). I read it in full before starting.
Calculations: `docs/research/fish/S25-D-deepen_calc.py` (`python3 -I`). **Every number tagged "calculated"
comes from that script. None of them is an observation.**

## Short answer

S25-D concluded that 565 × 10⁻⁶ N m², the value the Flammang 2013 abstract prints, should not be carried as
the EI of a single bluegill pectoral ray. Its reason: Alben et al. 2007 measured a cantilever stiffness of
1.98 N m⁻¹ on bluegill pectoral rays with a maximum length of 40.3 mm. That stiffness implies EI of about
5.4e-6 to 4.3e-5 N m², which puts 565e-6 13–105× too high (calculated).

**The input that conclusion is most sensitive to is one S25-D listed only as a caveat.** It is the assumption
that Flammang's ray is about the same size as Alben's. EI scales roughly as L⁴ under isometry. If Flammang's ray
were 2× longer, the gap would shrink to 0.8–6.5×, and at the most generous geometry 565e-6 becomes
consistent (calculated, §1). That makes the size match more decisive than k, E, I or the load point. **It is
unmeasured.** Flammang 2013's fish size, ray number and method are still **unknown**, because the body text
could not be reached from this session (§3).

What I could improve:

1. **Alben's test geometry, re-read.** A second full-text read via summarizer, with the exponents written
   out, says the force is applied at 2L/3 but "the force on the probe is measured as a function of **tip
   deflection**." With that geometry the calculated clamped EI is **2.24 × 10⁻⁵ N m²**. 565e-6 is then **25×**
   too high, which narrows S25-D's 13–105× bracket from both ends. 40.3 mm is the fins' *maximum* ray length,
   not the length of each of the 24 tested rays. So this EI is an upper-side estimate, and the gap can only
   widen if the tested rays were shorter.
2. **An independent anchor.** Aiello et al. 2018 tested labrid pectoral rays in three-point bending (abstract)
   and found EI from 10⁻¹⁰ to **1.51 × 10⁻⁶ N m²**. That is a different lab, different species and a
   different test. 565e-6 is 374× their maximum (calculated).
3. **The size needed for reconciliation, made explicit.** For 565e-6 to be a single clamped ray, Flammang's
   ray would have to be about **77–129 mm** long, with **90 mm** at the re-read geometry. That is 1.9–3.2× the
   linear size of Alben's specimens (calculated). Whether Flammang's fish were that large is **unknown**.

**Verdict: STANDS.** It is not "strengthens". The conclusion survives every input I could improve, and it
gains an independent anchor. But its decisive input is still an unverified premise, and §1 shows that premise
can overturn it. The defensible statement is conditional: *if Flammang's ray is within about 2× the length of
Alben's 40 mm rays, 565e-6 is not that ray's EI.*

## 1. Sensitivity of S25-D's conclusion (recomputed, calculated)

I took S25-D's middle case as the baseline: load at 2L/3, gap = 565e-6 / 1.28e-5 = **44×**. I then moved each
input by a factor of 2.

| Input | ×2 effect on EI | Gap after ×2 | Does the conclusion move? |
|---|---|---|---|
| Measured k = 1.98 N m⁻¹ | ×2 | 22× (or 88× for ÷2) | No |
| Alben's E or I, through their own B ≈ 10⁻⁶–10⁻⁵ | ×2 | 565e-6 / 1e-5 = 56× at the top of their bracket | No |
| Lever length in the conversion (L or load point a), EI ∝ a³ | ×8 | 5.5× | Weakened, but still out of range |
| **Flammang ray length relative to Alben's (isometric, EI ∝ L⁴)** | **×16** | **2.8× (2L/3), 0.8× (load at L), 1.6× (re-read geometry), 6.5× (L/2)** | **Yes. At the generous geometries it reconciles.** |

So the conclusion is most sensitive to **whether the two papers measured rays of the same size**, which is
the same physical quantity S25-D needed. S25-D listed this in its caveats ("if they used much larger
bluegill … both can be right"), but its `depends_on` recorded it only as an assumption. It did not test it as
the decisive input.

## 2. How well established is that input?

| Input | Source | Read-level | Status |
|---|---|---|---|
| Flammang 2013 fish size, ray identity, ray length | Flammang et al. 2013, *J Morphol* 274:1044–1059 | abstract only (Crossref JATS abstract and PubMed efetch, both re-read this session). Body: **could-not-access** | **Unknown.** The abstract gives no size, ray number or method. |
| Alben ray length 40.3 ± 0.8 mm | Alben, Madden & Lauder 2007, PMC2359861 | full-text via automated summarizer | **Measured**, but it is the fins' *maximum* ray length, not the length of each tested ray |
| Equivalence of the two (S25-D's implicit premise) | none | n/a | **Assumption.** It was repeated in S25-D's recomputation as if established. |

Evidence level of the decisive input: **assumption.** Nothing measured links Flammang's ray to Alben's.

## 3. Attempts to improve it

**Flammang 2013 body text (would settle it): could-not-access.**

- Wiley `onlinelibrary.wiley.com/doi/full/10.1002/jmor.20161`: HTTP 403 (WebFetch) and 403 (curl).
- A web search (search-summary) located a lab PDF at `sites.harvard.edu/glauder/files/2022/03/Flammang.etal_.2013.JMorph_finrays.pdf`
  and a Deep Blue record at `deepblue.lib.umich.edu`. Neither host resolves in this session
  (`ENOTFOUND`, network policy).
- Unpaywall and scholar.archive.org: CONNECT 403. Crossref (200) returns the abstract only.
- The search summary said the Harvard PDF snippet "shows the same figure" (565×10⁻⁶). That is
  **search-summary** read-level, and the summary itself called the text "garbled". I do not treat it as a
  body-text confirmation.

These are network-policy failures. They say nothing about the paper.

**Alben 2007 geometry, re-read** (WebFetch of `pmc.ncbi.nlm.nih.gov/articles/PMC2359861/`, full-text via
summarizer, exponents written out explicitly on request; Europe PMC fullTextXML still HTTP 500; curl to PMC hits
a reCAPTCHA page). Quoted, as returned:

- "a point force is applied (aluminium triangle in the photograph) at two-thirds the distance from the base to the tip"
- "the force on the probe is measured as a function of tip deflection of the ray"
- "Six fishes with fins of similar size (maximum ray length =40.3±0.8 mm, mean±s.e.)"; "24 separate rays";
  "ray 4 out of 13"
- "the force–displacement curve may be fit with a slope of 1.98 N m−1"
- "the measured B=EI≈10−6–10−5 J m", which the summarizer wrote out as 10^-6–10^-5 J m
- "L=4 cm for the length of a typical bluegill fin ray"

My inference: the "tip deflection" sentence appears in the same figure description as the 2L/3 load. If the
deflection was read at the tip, the cantilever relation is δ_tip = F a²(3L − a)/(6EI) with a = 2L/3. That gives
EI = 0.173 k L³ = **2.24e-5 N m²** (calculated). Another "probe … near the tip" sentence describes holding the
deflection at zero, which may belong to the actuation experiment. So the geometry is not fully pinned down. I
keep S25-D's bracket of 5.4e-6 to 4.3e-5 and add 2.24e-5 as the most text-consistent point inside it.

**Independent measurement, different lab.** Aiello BR et al. 2018, *J Exp Biol* 221:jeb163360, PMID 29162638
(abstract, PubMed efetch): "Pectoral fin ray flexural stiffness ranged from 0.0001 to 1.5109 µN m2". That is
1e-10 to 1.51e-6 N m², from three-point bending of *Gomphosus varius* and *Halichoeres bivittatus*. Caveats, my
inference: three-point bending gives a *local* EI, and the authors report that it decays exponentially along
the ray, so it is not the same quantity as a whole-ray clamped cantilever EI. Fish sizes are **unknown** at
abstract read-level. This anchor therefore argues about order of magnitude only. It does not reach 10⁻⁵, let
alone 5.65 × 10⁻⁴.

**Abstract-internal check (calculated, weak).** Suppose the abstract's 67 mN impact force acted at the tip of a
40 mm linear cantilever. With EI = 565e-6 the maximum curvature would be 0.0048 mm⁻¹. That is below the
abstract's own *normal-swimming* ceilings of 0.029 and 0.065 mm⁻¹. With 3.8e-6 it would be 0.71 mm⁻¹. The
abstract reports 9.38 mm⁻¹ with local buckling, which is outside linear beam theory, so this check is **not
diagnostic** and I give it no weight in the verdict. It is only mildly suggestive, and that is my inference:
at 565e-6 a 67 mN impact would bend the ray less than ordinary swimming does, which sits poorly with the
abstract's report of buckling.

Other searches and their scope:

- Europe PMC citations of PMID 23720195: 31 hits. Only PMC5454310 (Nguyen et al. 2017) was open full text. I
  grepped it for "Flammang", "565", "flexural", "rigidity" and "bluegill". It contains no Flammang stiffness
  value and no bluegill ray size.
- The other likely mechanics citers had no Europe PMC full text, so I read only their abstracts: 29693259,
  29885081, 37364788, 34380757 and 28082612. None restates 565e-6 or gives Flammang's fish size.

## 4. Recompute with the improved inputs

| Case | EI (calculated) | 565e-6 ÷ EI | 3.8e-6 ÷ EI |
|---|---|---|---|
| S25-D bracket, load and read at L/2 to L | 5.4e-6 to 4.3e-5 | 105× to 13× | 0.70 to 0.09 |
| **Re-read geometry: load 2L/3, read at tip** | **2.24e-5** | **25×** | **0.17** |
| Aiello 2018 labrid maximum (local, independent) | 1.51e-6 | 374× | 2.5 |
| Ray length needed for 565e-6 (isometric) | n/a | 77 to 129 mm (90 mm at re-read geometry) | n/a |

- **S25-D's part 1** (565e-6 is the abstract's printed value, and the ratio of 149 is not a unit slip):
  **stands**. Its sensitivity was already shown by S25-D, and nothing here touches it.
- **S25-D's part 2** (565e-6 is not a single bluegill ray's EI, and 3.8e-6 is consistent with measured rays):
  **stands, conditionally**. The independent labrid data and the re-read geometry both point the same way.
  But it holds only if Flammang's ray is within about 2× the length of Alben's 40 mm rays. A ray of 77–129 mm,
  or a different quantity such as a whole fin, a different ray or per-unit-width EI, would reconcile 565e-6
  with Alben. Those possibilities are not excluded. This is a narrowing of scope, not a strengthening.

## 5. What would settle it

1. **Read Flammang 2013's Methods.** This costs nothing beyond network access. Allow `sites.harvard.edu`
   or `deepblue.lib.umich.edu` in this environment's network settings. Read off the fish SL, which ray was
   used, its length, and the equation behind "calculated". If the ray is about 40 mm, part 2 is
   **confirmed**. If it is 75 mm or longer, or the quantity is not a single-ray EI, part 2 **falls** back to
   "the two values may describe different things".
2. **Measure it.** A clamped cantilever test plus a µCT section of pectoral ray 4 from bluegill at two sizes,
   for example 40 mm and 90 mm rays. That would test L⁴ scaling directly. Cost: **unknown**, and I have no
   sourced figure.

## Sources

| Source | Read-level |
|---|---|
| Flammang BE, Alben S, Madden PGA, Lauder GV 2013, *J Morphol* 274:1044–1059, doi:10.1002/jmor.20161, PMID 23720195 | abstract (Crossref and PubMed, this session); body **could-not-access** (Wiley 403; Harvard and UMich hosts not resolvable) |
| Harvard lab PDF of the above, as described by web search | search-summary |
| Alben S, Madden PG, Lauder GV 2007, *J R Soc Interface* 4:243–256, doi:10.1098/rsif.2006.0181, PMC2359861 | full-text via automated summarizer (this session; exponents requested explicitly); PMC efetch front matter and abstract (direct) |
| Aiello BR et al. 2018, *J Exp Biol* 221:jeb163360, PMID 29162638 | abstract |
| Aiello BR et al. 2018, *J Morphol* 279:1031–1044, PMID 29693259 | abstract |
| Taft NK et al. 2018, *J Morphol* 279:1045–1057, PMID 29885081 | abstract |
| Nguyen K et al. 2017, *J R Soc Interface*, PMC5454310 | full-text (Europe PMC XML, keyword-grepped) |
| Europe PMC citation listing for PMID 23720195 (31 hits) | listing |
| Parent S25-D (`S25-deepen.md`, commit 96cf4982) and its quotes of Puri et al. 2018 (PMC5868929) | full-text (repository); Puri not re-read this session |

```swarm-result
{"subproblem": "S25-D-D", "evidence": "literature", "answer": "S25-D's conclusion is most sensitive to an unmeasured premise: that Flammang 2013's ray is the same size as Alben 2007's 40.3 mm rays. A 2x longer ray (isometric EI ~ L^4) shrinks the 565e-6 gap from 13-105x to 0.8-6.5x. Flammang's body text could not be accessed. Re-reading Alben's geometry (load at 2L/3, deflection at tip) gives a calculated clamped EI of 2.24e-5 N m^2, putting 565e-6 25x too high, and Aiello 2018's independent labrid maximum of 1.5e-6 N m^2 points the same way. So the conclusion stands, but only conditionally: it holds if Flammang's ray is within about 2x of 40 mm (565e-6 would need a 77-129 mm ray).", "key_number": "bluegill pectoral ray clamped EI 2.24e-5 N m^2 (calculated, load 2L/3, tip deflection, k = 1.98 N/m, L = 40.3 mm), so 565e-6 is 25x too high; reconciliation would need a Flammang ray of 77-129 mm (unknown)", "verdict": "stands", "depends_on": ["Flammang et al. 2013 abstract, PMID 23720195 (abstract read-level): EI 565 x 10^-6 Nm2 'calculated'; impact force 67 mN; curvatures 0.029/0.065/9.38 mm^-1", "Flammang et al. 2013 body text: could-not-access; fish size, ray identity, ray length and EI method unknown", "Premise (unverified, decisive): Flammang 2013 ray length within ~2x of Alben 2007's 40.3 mm rays and the 565e-6 refers to a single-ray EI", "Alben, Madden & Lauder 2007, PMC2359861 (full-text via summarizer): k = 1.98 N/m both hemitrichs clamped; max ray length 40.3 +/- 0.8 mm; load at 2L/3; force vs tip deflection; B = EI ~ 1e-6 to 1e-5 N m^2; 24 rays, ray 4 of 13", "Interpretation that Alben's deflection was read at the tip (inference from the figure description; alternative load-point readings kept as bracket 5.4e-6 to 4.3e-5)", "Euler-Bernoulli uniform cantilever model, small deflection", "Isometric scaling EI ~ L^4 (used for the size sensitivity and the 77-129 mm requirement)", "Assumption: cantilever base compliance does not inflate the gap by >13x (unmeasured)", "Aiello et al. 2018 J Exp Biol PMID 29162638 (abstract): labrid pectoral ray EI 1e-10 to 1.51e-6 N m^2, three-point bending, local EI", "Puri et al. 2018 PMC5868929 (via S25-D, full-text): 3.8e-6 N m^2 relay attributed to Flammang 2013", "S25-D (commit 96cf4982) conclusion and its bracket 5.4e-6 to 4.3e-5 N m^2", "S25 part 1: ratio 148.7 is not a power-of-ten unit slip"]}
```
