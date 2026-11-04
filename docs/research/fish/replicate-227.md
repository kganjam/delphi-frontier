# Replication 227: "Energy per stroke is the binding term" (S29)

**Status:** an independent re-derivation. Every number below is **calculated** from literature inputs. **Nothing here is a new measurement or observation.**

**Target claim:** S29 (`origin/claude/s29-launch-energy-2iuixr`, `docs/research/fish/S29-organism.md`), §5, "The binding term: energy per stroke".

## 0. What I read before deriving (disclosure)

- **Before deriving**, I read only S29's title block (lines 1–6) and §2.1 (lines 80–89). These gave me the inputs m = 0.40 g and V = 4.37 m/s. I **also saw their KE working** there: 3.819 mJ = 9.55 J/kg, the caveat that 5.53 m/s applies at 0.40 g, and the 0.95 J/kg burst.
  - That KE step is therefore **not blind**. It is one line of arithmetic, which I recomputed.
- I did **not** read §0, §1, §2.2–§4 or §5 until my own numbers below were computed. I also did not read `S29_launch_energy.py` or `S29-deepen*`.
- I read §0 and §5 afterwards, for the comparison in §4 only.

## 1. Question, as I framed it

Can a 0.40 g teleost's axial muscle deliver, **in one stroke**, the kinetic energy of a 4.37 m/s launch? If not, by how much is it short?

## 2. Inputs

| # | Input | Value | Source | Read-level |
|---|---|---|---|---|
| 1 | Body mass m | 0.40 g | S29 brief (§2) | full-text (of that section) |
| 2 | Launch speed V | 4.37 m/s | S29 brief, from S28 | full-text (of that section). **Not re-derived by me.** |
| 3 | Myotomal muscle, fraction of body mass f | **0.60** typical; 0.30–0.80 across species | Johnston, Bower & Macqueen 2011, *J Exp Biol* 214:1617: ">60 % in pelagic species". A Springer freshwater-teleost paper gives 30–80 %. | search-summary (both) |
| 3b | Myotomal muscle, fraction of **tail cross-section** in a 5 dpf zebrafish larva | 67.3 ± 0.4 % (fast 61.2 %) | Mead et al. 2020, bioRxiv 10.1101/2020.04.02.010298 | full-text (first 100k characters) |
| 4 | Net work per cycle, fast fish muscle, work loop | **3.5 J/kg** muscle | Johnston et al. 1993, *J Exp Biol* 185:251 (sculpin, optimal strain and phase, 4–8 Hz) | search-summary / abstract |
| 4b | Net work per cycle, larval zebrafish fast muscle | **2.63 ± 0.18 J/kg** at 40 Hz; 0.43 J/kg at 120 Hz | Mead et al. 2020 | full-text (partial) |
| 5 | Peak instantaneous fast-start muscle power | 307 W/kg (C-bend), 222 W/kg (contralateral) | James & Johnston 1998, *J Exp Biol* 201:913 | abstract |
| 6 | Maximum isometric stress σ, fast fibres | 220 kN/m² (sculpin; another snippet gives 125–282 kN/m²) | attributed to Johnston, Franklin & Johnson 1993 | search-summary. **Attribution not confirmed.** |
| 6b | Maximum isometric stress σ, larval zebrafish | 76 ± 3 kN/m² | Mead et al. 2020 | full-text (partial) |
| 7 | Maximum white-fibre strain in a fast start | 24 % anterior, 10 % posterior | fast-start sonomicrometry study, **paper not identified** | search-summary only. Weak. |
| 8 | Muscle density | 1060 kg/m³ | the value Mead et al. 2020 assume | full-text (partial) |

**Not found:** a measured single-contraction work (J/kg muscle) for a **fast-start C-bend** in any fish.
- **Scope of that negative search:** two WebSearch queries, plus the James & Johnston 1998 abstract page. The full text was behind a sign-in.
- **Could-not-access:** cob.silverchair.com, pubmed.ncbi.nlm.nih.gov and ouci.dntb.gov.ua. All three are blocked by this session's network policy.

**Not used:** hydrodynamic (push-off) efficiency. I found no primary source for it. I report η_h = 1, which is the optimistic floor, and show η_h only as a parameter.

## 3. Arithmetic (all calculated)

**Kinetic energy needed:**
- KE = ½ · 0.40×10⁻³ kg · (4.37 m/s)² = ½ · 0.40×10⁻³ · 19.097 = **3.819 mJ = 9.55 J/kg body**.

**Muscle mass:**
- At f = 0.60: m_muscle = 0.24 g.
- One side, for one contraction: 0.12 g. The "one side" split is **my assumption**: a half-stroke is driven by one side of the axis.

**Required muscle-specific work, at η_h = 1:**
- Both sides: 3.819 mJ / 0.24 g = **15.9 J/kg muscle**.
- One side: 3.819 mJ / 0.12 g = **31.8 J/kg muscle**.
- With η_h < 1, divide by η_h. For example, at η_h = 0.37 (S29's value, not sourced by me), one side needs 86 J/kg.

**(A) Supply per stroke at measured cyclic work-loop rates.** This is the measured basis.

| f | w (J/kg muscle) | Both sides (mJ) | One side (mJ) | Shortfall, both | Shortfall, one side |
|---|---|---|---|---|---|
| 0.60 | 3.5 | 0.84 | 0.42 | 4.5× | 9.1× |
| 0.60 | 2.63 | 0.63 | 0.32 | 6.1× | 12.1× |
| 0.30 | 2.63–3.5 | 0.32–0.42 | 0.16–0.21 | 9–12× | 18–24× |
| 0.80 | 2.63–3.5 | 0.84–1.12 | 0.42–0.56 | 3.4–4.5× | 6.8–9.1× |

**(B) Single-contraction physical ceiling.**
- The ceiling is w_max = σ · ε / ρ. It assumes a rectangular loop: peak isometric force held through the whole shortening. Force–velocity makes that unreachable, so this is an **upper bound**, not an estimate.

| σ (kN/m²) | ε | w_max (J/kg) | Both sides at f = 0.6 (mJ) | One side (mJ) |
|---|---|---|---|---|
| 76 | 0.10 | 7.2 | 1.72 | 0.86 |
| 76 | 0.24 | 17.2 | 4.13 | 2.06 |
| 220 | 0.10 | 20.8 | 4.98 | 2.49 |
| 220 | 0.24 | 49.8 | 11.95 | 5.98 |
| 282 | 0.24 | 63.8 | 15.32 | 7.66 |

### My value

**Measured basis.** Per stroke, the axial muscle of a 0.40 g fish delivers **≈ 0.3–0.8 mJ**. The launch needs 3.82 mJ, so it is **short by ~4.5–12×**, even at η_h = 1. This is a calculation from cyclic work-loop data.
- The one-side / f = 0.6 central case is **0.32–0.42 mJ, short by 9–12×**.

**Ceiling basis.** Only the rectangular-loop bound, with adult-fish σ and the largest reported strain, reaches the requirement. One side gives 6 mJ against 3.8 mJ needed, at η_h = 1. **Any η_h below ~0.6 defeats even that bound.**

So my inference is that per-stroke energy is a real deficit, for a direct muscle stroke. That is my inference, not an author's claim.

**Uncertainty is large.**
- Cyclic work-loop values underestimate single fast-start contractions. Larger strain and a single activation both raise work. I could not find a measured fast-start J/kg.
- I did **not** evaluate the spring (LaMSA) route's loading work, which S29's headline rests on.

## 4. Comparison with the recorded value (read only after §3)

**S29 §5 claims**, as author's claims:
- Spring-loaded, one side (f = 0.30), w = 53–81 J/kg (frog; Mendoza & Azizi 2021), η_spring 0.93, η_h 0.37 → **54–82 % of the 10.17 J/kg need, short by 1.2–1.9×**.
- Required one-side muscle work is **98.5 J/kg**, which is **11.5×** the 8.6 J/kg they back-calculate for today's direct stroke.

**Where we agree:**
- KE is the same: 3.819 mJ, 9.55 J/kg. (I saw theirs first; see §0.)
- My one-side requirement, 31.8 J/kg at η_h = 1, becomes 31.8 / 0.37 / 0.93 · (10.17 / 9.55) = **98.4 J/kg**. That reproduces their 98.5 J/kg from my own chain.
- Direction: both derivations find the muscle cannot supply the launch energy in one stroke.

**Where we differ:**
- **Direct-stroke muscle work.** They back-calculate 8.6 J/kg from the observed 1.38 m/s burst, assuming η_h = 0.37. Measured cyclic work loops give 2.6–3.5 J/kg. These are different quantities: an in-vivo inference versus in-vitro cyclic data. I keep both; I do not average them.
- **Size of the direct-stroke gap.** My measured-basis gap is 9–12× at η_h = 1, against their 11.5× with η_h = 0.37. The magnitudes coincide only because the two differences offset each other.

**What I cannot check:**
- I could not read the frog w = 32–81 J/kg values (could-not-access). A search-summary of the same paper reports a ~2.5× range in mass-specific stored energy between species. That is consistent with 81/32 = 2.5, but I did not see the absolute values.
- I did not verify η_h = 0.37 or η_spring = 0.93.

**Verdict:**
- **AGREE** that energy per stroke is a binding deficit: the muscle cannot deliver 3.82 mJ in one stroke on measured values.
- **CANNOT TELL** for the specific spring-loaded shortfall of 1.2–1.9×. Its key inputs (frog w, η_h) were outside what I could read.

## Sources

- [Mead et al. 2020, bioRxiv](https://www.biorxiv.org/content/10.1101/2020.04.02.010298.full): full-text, first 100k characters.
- [James & Johnston 1998, J Exp Biol 201:913](https://journals.biologists.com/jeb/article-abstract/201/7/913/7903/Scaling-of-Muscle-Performance-During-Escape?redirectedFrom=fulltext): abstract.
- [Johnston et al. 1993, J Exp Biol 185:251](https://next.sciencegate.app/document/10.1242/jeb.185.1.251): search-summary.
- [Johnston, Bower & Macqueen 2011, J Exp Biol 214:1617](https://cob.silverchair.com/jeb/article-split/214/10/1617/10212/Growth-and-the-regulation-of-myotomal-muscle-mass): search-summary (host blocked).
- [Wakeling & Johnston 1998, J Exp Biol 201:1505](https://www.sciencegate.app/document/10.1242/jeb.201.10.1505): search-summary. Not used in the arithmetic.
- [Mendoza & Azizi 2021, J Exp Biol 224](https://escholarship.org/uc/item/3xg7f10h): search-summary. Used only for the comparison.

```swarm-replication
{"claim_id": 227, "my_value": "0.3-0.8 mJ muscle work per stroke vs 3.82 mJ needed (short 4.5-12x at eta_h=1, measured work-loop basis); rectangular sigma*epsilon ceiling 2-12 mJ", "agrees": true,
  "note": "Independently confirm a per-stroke energy deficit and reproduce the 98.5 J/kg one-side requirement, but cannot verify the spring-loaded 1.2-1.9x shortfall because the frog loading-work and eta_h inputs were not readable."}
```
