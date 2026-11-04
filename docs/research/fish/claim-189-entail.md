# Claim 189 propagated to its neighbouring scales: what must be true at organ and behaviour

**Claim under propagation (189, scale `organism`, evidence `derived`).**
"S28 VERDICT NEGATIVE: the best design buildable from demonstrated alleles is the EXISTING Daane
`lat4a^nr21/+ ; kcnh2a^lof/+` zebrafish, and it cannot fly, glide, skim, or meaningfully extend its leap."

**Status of this note.** No new measurement was made. Every number without a source beside it is a
**calculation** from `docs/research/fish/claim-189-entail_calc.py` (run time < 1 s). Where I report a
value from the literature I give its read-level. Date: 2026-11-04.

**What I read.**

| Source | Read-level |
|---|---|
| `docs/research/fish/S28-organism.md` @ `origin/claude/s28-organism-design-5z0vjz` (the claim itself) | full-text (repository) |
| `docs/research/fish/S28-deepen.md` @ `origin/claude/deepen-s28-daane-heterozygote-b7kpn8` (S28-D) | full-text of §§1–6 via `git show` and grep; I did not run its script |
| `docs/research/fish/S28-D-D-deepen.md` @ `origin/claude/deepen-s28-sensitive-input-4x2i7x` (the figure-read of the fin) | full-text (repository) |
| `docs/research/fish/replicate-189.md` @ `origin/claude/replicate-claim-189-lyc37e` | full-text (repository) |
| `docs/research/fish/challenge-262.md` @ `origin/claude/challenge-s28-fin-length-w7k0zz` | full-text (repository) |
| van Leeuwen JL, Voesenek CJ, Müller UK 2015, *J R Soc Interface* 12:20150479, doi:10.1098/rsif.2015.0479 | full-text via automated fetch; I read only the quoted sentence |
| Gibb AC, Ashley-Ross MA, Pace CM, Long JH 2011, *J Exp Zool A* 315A:649–653 (PMID 21972177) | search-summary (title/abstract gist only; no full text) |
| SICB meeting abstract, terrestrial movements of *Danio rerio* and *Gambusia affinis* | search-summary. **`sicb.org` does not resolve from this session** — it has to be allowed in the session's network settings before the abstract itself can be read |
| Brewer JM et al. — in-air kinematics of jumping *Poecilia reticulata*, PMC3629028 | search-summary |
| Mansuit R, Herrel A 2021 review of appendicular muscle mass across the fin-to-limb transition | listing (surfaced by search; not opened) |
| Daane et al. 2021 *Curr Biol* 31:5052, doi:10.1016/j.cub.2021.08.054 | **not read by me this session.** Its full text, and the bioRxiv Fig 8B/8A figure-reads, reach me only as the repository relay above |
| Miln et al. 2021 burst 1.38 m/s; Demesmay et al. 2025 escape peak 1.57 ± 0.27 m/s | listing, relayed through the repository. Neither primary was opened by me |

**Inputs I inherit, with their levels.** m = 0.25 g and SL = 3.0 cm (**assumed**, S28 back-solve);
CL_max = 1.07 (**project-derived**); pectoral fin length 0.463 SL per fin, IQR 0.449–0.488, n = 34
(**figure-read** of the bioRxiv Fig 8B, via S28-D-D); planform shape factor A/L² = 0.13–0.25 per fin
(**figure-read** of Fig 8A, one representative fish, via S28-D-D) against 0.52 for S28's AR-5 case C
(**assumption**); in-water escape peaks 0.95–2.11 m/s (**literature, listing**); skim requirement
132–199 Hz (**project-derived**).

---

## 1. ENTAIL — what claim 189 requires at the adjacent scales

Claim 189 is a negative, so its entailments are mostly **ceilings**: for the organism to be unable to
fly, glide, skim or meaningfully extend its leap, certain organ-level and behavioural quantities must
lie *below* stated values. A ceiling is as checkable as a floor, and the same measured number either
meets it or contradicts it.

| # | Scale | Kind | Requirement |
|---|---|---|---|
| **C1** | organ | range | The **spread paired-pectoral planform area** must lie below the area at which fin lift equals body weight at the fastest conspecific speed on record. Bound: **< 841 mm²** (calculated at 2.11 m/s, CL 1.07, m 0.25 g). If the organ exceeds it, a weight-supporting glide exists and the claim fails. |
| **C2** | organ | timescale | The **oscillation period of the axial propulsor** must be *slow* relative to the period required to drive an airborne skim. Required: 132–199 Hz, i.e. a **5.0–7.6 ms** cycle. The organ's ceiling must lie above (slower than) that period. |
| **C3** | organ | energetic | The **mass fraction of the fin-driving musculature** must lie below what weight-supporting flapping needs: **< 7.5 %** of body mass (the low end of S28 §5 row 6). Above it, powered flight is not excluded on power grounds. |
| **C4** | behaviour | range | The **water-exit speed actually achieved in a leap** must lie below **4.32 m/s** (calculated V_to at the generous case-C area) for the no-flight / no-glide verdict, and below **2.39 m/s** for the "no 3× leap" verdict. |
| **C5** | behaviour | existence | **No in-air behaviour may exist** that supplies lift beyond the quasi-steady value of a fully abducted fin — no unsteady or flapping augmentation large enough to turn a +1.5–3 % range gain into a meaningful extension. |

Each is generic: C1 bounds an area, not a particular fin ray; C2 bounds a period, not a muscle fibre
type; C3 bounds a mass fraction, not a named muscle; C5 forbids a class of behaviour, not a gait.

---

## 2. CHECK — each constraint against the record

### C1 (organ, range): spread paired-fin planform area < 841 mm² — **SATISFIED**

The required area is a calculation: S = 2W/(ρ_air V² CL). My script gives

| Exit speed used | S for L = W | ratio to the figure-read fin (96 mm²) | ratio to case C (201 mm²) |
|---|---|---|---|
| 0.95 m/s | 4146 mm² | ×43.0 | ×20.7 |
| 1.38 m/s | 1965 mm² | ×20.4 | ×9.8 |
| 1.57 m/s | 1518 mm² | ×15.7 | ×7.6 |
| **2.11 m/s** (most generous) | **841 mm²** | **×8.7** | ×4.2 |

The organ-level number that meets this is the **figure-read spread planform of the double
heterozygote's pectoral fins**: A/L² = 0.13–0.25 per fin at a fin length of 0.463 SL gives **50–96 mm²
for the pair** (my recomputation of S28-D-D's digitisation; it reproduces that document's 52–96 mm²).
That is 8.7× to 43× below the bound. Even S28's unsupported AR-5 planform (201 mm²) is 4.2× below it.
With the heavier isometric body (0.43 g) the required area at 2.11 m/s rises to 1446 mm², ×15.0.

- **Named mechanism satisfying it:** the *longfin* (`kcnh2a^lof`) elongation is **length-dominated**,
  not area-dominated — A/L² ≈ 0.13–0.25 against 0.52 for an AR-5 wing. The ray elongation adds span
  without webbing proportional area.
- **Caveats carried forward, not resolved:** the planform is a figure-read of **one representative
  fish** chosen by the authors, from an image with no scale bar, measured as projected area (hence a
  *lower* bound on true planform). A deliberately fanned fin could exceed it; S28-D-D estimates a fully
  webbed 60° sector would be 2.1–3.5× the partly spread image. **Even ×3.5 leaves the pair at ~340 mm²,
  still 2.5× below the 841 mm² bound.** So the margin survives the caveat.
- **Disagreement preserved:** S28 case C (201 mm², assumption) vs the figure-read 50–96 mm². Challenge
  262 argues separately that a *lower* aspect ratio at fixed length would raise the area; it tested
  AR 2.5, which raises its effect figures by ~1.5×. That too stays inside the bound.

**Evidence level: literature (figure-read of a primary source, relayed through the repository) against a
calculated bound.** Read-level for the figure itself: I did not open the bioRxiv PDF this session; the
digitisation reaches me at repository full-text.

### C2 (organ, timescale): propulsor period slower than 5.0–7.6 ms — **SATISFIED**

The requirement is a calculation from the project's own skim condition (132–199 Hz).

| Measured / inherited ceiling | Period | Short of the skim requirement by |
|---|---|---|
| **95 Hz**, larval zebrafish 4–5 dpf cyclic swimming | 10.5 ms | ×1.4–2.1 |
| 52 Hz, project input (S28 §1, level "measured", primary not identified in the record) | 19.2 ms | ×2.5–3.8 |
| ~21 Hz, intact adult short high-frequency swimming | 47.6 ms | ×6.3–9.5 |

- The 95 Hz value is the strongest thing I verified myself: van Leeuwen, Voesenek & Müller 2015 state
  "Larvae at 4–5 dpf reach higher f (95 Hz) and A_tail (2.4 mm) than at 2 dpf (80 Hz, 1.8 mm)"
  (**author's statement**; read-level full-text via automated fetch, quoted sentence only). *My
  inference:* larvae are the fastest-beating life stage, so a larval ceiling bounds the adult from
  above — the same paper remarks that adult fish use "narrower, lower frequency body waves" with no
  number attached.
- The ~21 Hz adult figure is attributed to Kyriakatos et al. 2011 by a secondary article surfaced in my
  search. **Read-level: search-summary. I did not open either the quoting article or the primary, so I
  do not rely on it** — it is listed because it points the same way, not because it is checked.
- **Disagreement preserved, and it matters:** the claim's own input is 52 Hz, between the verified
  larval 95 Hz and the relayed adult ~21 Hz. The three numbers are not averaged. The constraint is
  satisfied under all three, and the *weakest* case for the claim (larval 95 Hz) still leaves the skim
  1.4–2.1× out of reach.
- **Scope of what is still missing:** no adult zebrafish *escape* tail-beat maximum was found. Searches:
  two web searches (standard mode) for adult escape/fast-start tail-beat frequency, plus one fetch of
  the article that had been quoted. All returned larval values or adult sustained-swimming values.
  "Nobody has published an adult escape maximum that I could reach" — not "people looked and found none".

### C3 (organ, energetic): fin-muscle mass fraction < 7.5 % of body mass — **OPEN**

I did not establish this and will not mark it satisfied.

- **What the record offers:** S28 §5 row 6 states ~1.4 % for teleost pectoral musculature against a
  7.5–20 % requirement, labelled "measured (teleost, not zebrafish)". That reaches me as a repository
  relay with **no primary citation attached**, so I cannot give it a read-level above `listing`, and I
  cannot name the species it was measured in.
- **What I searched:** one web search (standard mode) for zebrafish pectoral fin muscle mass as a
  percentage of body mass. It returned zebrafish fin *myology and development* (Patterson & Devoto
  2008; ZFIN figure records) and a comparative review (Mansuit & Herrel 2021, read-level listing, not
  opened) that reports appendicular muscle mass *increasing* across the fin-to-limb transition without,
  in the material I saw, a zebrafish figure. **No zebrafish pectoral muscle mass fraction was found.**
- *My inference, stated as such:* for C3 to fail, the zebrafish fin musculature would have to be ≥ 5×
  the relayed teleost fraction. That is implausible to me, and implausible is exactly the word that
  does not license `satisfied`. **Status `open`.** Cheapest closure: dissect and weigh paired-fin
  musculature in the existing animals — hours of work, and it is S28 §4's own lowest-ranked candidate.

### C4 (behaviour, range): exit speed < 4.32 m/s (and < 2.39 m/s) — **OPEN**

The bounded quantity has **never been measured** in adult zebrafish. This is the load-bearing gap in
claim 189, and it was already recorded as such by S28-D ("Neither study measured a surface exit. No
adult zebrafish exit speed is known in the record.").

What exists, all of it a proxy or a different behaviour:

| Stand-in | Value | Level / read-level | Inside the 4.32 m/s bound? |
|---|---|---|---|
| In-water escape peak (Miln et al. 2021, n = 50, 120 fps) | 1.38 m/s per-fish max | literature; **listing**, repository relay | yes, by ×3.1 |
| In-water escape peak (Demesmay et al. 2025, 240 fps) | 1.57 ± 0.27 m/s, +2 SD = 2.11 | literature; **listing**, repository relay | yes, by ×2.0 at +2 SD |
| **Terrestrial** jump distance, *Danio rerio* | mean ≈ 0.10 m, max ≈ 0.27 m | **search-summary** of a conference abstract; `sicb.org` unreachable from this session | implies 0.99 / **1.63 m/s** at a 45° vacuum launch (my calculation) — yes, by ×2.7 |

Three independent stand-ins land at 1.4–2.1 m/s and none approaches 4.32 m/s. *My inference:* the
no-flight verdict is not in danger from this constraint. But the second bound is closer: **2.39 m/s**
for a 3× leap is only ×1.13 above Demesmay's +2 SD, and ×1.47 above the jump-implied 1.63 m/s.

Two cautions I am not allowed to smooth over:

1. The terrestrial jump figures are a **different behaviour** (a stranded fish on a substrate, tail-flip
   driven, reported takeoff near 90° for *Danio*), and the reported ~0.27 m maximum sits oddly against
   an arena reported as ~0.1 m across. Read-level search-summary, from an abstract I could not open. I
   record it as a pointer, not as a bound. If it survives reading, it is a *measured* leap distance
   exceeding the claim's 19.4 cm ballistic baseline — which would raise the inferred exit speed toward,
   not away from, the 2.39 m/s figure. That is a reason to read it, not a refutation.
2. Marking C4 `satisfied` would mean treating in-water escape peaks as surface-exit speeds. S28 itself
   calls that assumption "generous"; breaking the surface costs speed. The assumption is probably
   conservative *for the claim*, but it is an assumption about the very quantity the constraint bounds,
   so the constraint is **`open`**, not satisfied.

**Scope of the negative:** no adult zebrafish water-exit speed in the record, per S28-D's access record
(Miln, Demesmay) plus my two searches above for zebrafish leap/aerial kinematics. Searches returned
terrestrial jumping (Gibb et al. 2011 and its SICB abstract), guppy aerial jumping (PMC3629028) and a
cross-taxon H/L ∼ Fr² scaling result — **no zebrafish surface-exit measurement**. This is "nobody has
measured it", not "it was measured and is low".

### C5 (behaviour, existence): no in-air lift augmentation beyond a spread fin — **UNSATISFIED**

Nothing known meets this, because **nobody has filmed what the fins do in the air.**

- S28's own trajectory model assumes "the fish holds the fins spread at CL 1.07 throughout the leap",
  and labels it "generous and unobserved". S28-D records in-air abduction as the open question behind
  its detectability clause. So the claim's bound is computed under an unobserved behaviour, in the
  direction generous to itself.
- **What is measured, in other species, and points the other way:** the guppy aerial-jump study
  (PMC3629028, **read-level search-summary**) reports that jumping fish "continue with whole body
  thrusts and tail beats, even when out of the water" — so in-air propulsive behaviour *does* exist in
  a small teleost. Archerfish accounts describe raising the pectoral and pelvic fins before takeoff and
  then an unpowered glide. I did not find any study that measures pectoral fin spread during the
  airborne phase of any fish (scope: one web search, standard mode, for in-air fin abduction kinematics).
- **Why the claim nevertheless does not collapse here, as a calculation and not an observation:** an
  airborne tail beat at matched kinematics transfers momentum in proportion to fluid density, and
  ρ_air/ρ_water = 1.23e-3, i.e. **1/815** of its in-water value. For the lift route, the effect scales
  with S·CL; doubling CL by some unsteady mechanism is equivalent to doubling the area, which in
  S28-D-D's own table moves the ascent-deceleration reduction from 1.4–2.6 % to about 2.6–5.1 % — still
  not a meaningful leap extension, and still ×2 or more short in speed for flight.
- So C5 is `unsatisfied` in the strict sense — **no mechanism is known to meet it, and the quantity has
  never been observed** — while the magnitude of the gap it could open is bounded above by the two
  calculations just given. I am flagging it rather than discharging it: it is the one constraint where a
  single afternoon with a 1000 fps camera could change the status in either direction.

---

## 3. What this propagation did and did not do

- **It found no `unsatisfiable`.** No measured number contradicts any of the five constraints. I
  looked specifically for one: a fin area, an exit speed, or a beat frequency large enough to break a
  ceiling. The largest measured stand-in anywhere in the record (2.11 m/s, Demesmay +2 SD) is ×2.0
  inside C4's flight bound, and the figure-read fin is ×8.7 inside C1's.
- **The claim's weight rests on C1 and C2**, the two constraints that are checked against numbers
  (one a figure-read, one a published measurement I verified myself). Both are satisfied with margins
  of 1.4× to 43×.
- **Its exposure is C4 and C5**, both behavioural, both unmeasured. Neither can rescue flight — C4's
  stand-ins are ×2–3 short and C5's augmentation is bounded above — but C4's secondary bound (2.39 m/s
  for a 3× leap) is only ×1.13 above a measured in-water escape peak + 2 SD. **The "cannot fly" half of
  claim 189 is far better supported than the "cannot meaningfully extend its leap" half.** That
  asymmetry is the finding of this note.
- **C3 is open on a technicality that is cheap to close**, and closing it is worth less than closing
  C4 or C5.

Ranked next measurements, by how much they would move these statuses: (1) high-speed surface-leap video
of the double het and wild-type siblings, which closes C4 and C5 together; (2) a calibrated photograph
of a maximally fanned pectoral fin, which replaces C1's single-fish figure-read with a measurement;
(3) the SICB abstract and Gibb et al. 2011 full text, which is a reading task, not an experiment, and
needs `sicb.org` allowed in this session's network settings.

```swarm-entail
{"source_claim": 189, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The spread paired-pectoral planform area must lie below the area at which fin lift equals body weight at the fastest conspecific speed on record; above it a weight-supporting glide exists and the claim fails.",
      "quantity": "spread paired-fin planform area", "lo": 0,
      "hi": 841, "units": "mm^2",
      "status": "satisfied",
      "satisfied_by": "Figure-read spread planform of the double heterozygote's pectoral fins: A/L^2 = 0.13-0.25 per fin at a figure-read fin length of 0.463 SL gives 50-96 mm^2 for the pair, which is 8.7x to 43x below the bound; the longfin elongation is length-dominated (A/L^2 0.13-0.25) rather than area-dominated (0.52 for an AR-5 wing). Bound itself is my calculation S = 2W/(rho V^2 CL) at 2.11 m/s, CL 1.07, m 0.25 g (assumed mass).",
      "satisfied_evidence": "literature",
      "note": "Figure-read of bioRxiv preprint 10.1101/2021.03.05.434157 Fig 8A/8B (published as Daane et al. 2021 Curr Biol 31:5052, doi:10.1016/j.cub.2021.08.054 Fig 4B), digitised in docs/research/fish/S28-D-D-deepen.md @ origin/claude/deepen-s28-sensitive-input-4x2i7x; read-level for me: repository full-text, I did not open the PDF this session. Caveats carried, not resolved: one author-chosen fish, no scale bar, projected area is a lower bound on true planform. A fully fanned fin at S28-D-D's estimated 2.1-3.5x the imaged planform reaches ~340 mm^2, still 2.5x inside the bound. Disagreement preserved: S28's assumed AR-5 case C gives 201 mm^2, and challenge 262's AR-2.5 relaxation raises area further; both stay inside the bound."},
    {"target_scale": "organ", "kind": "timescale",
      "statement": "The oscillation period of the axial propulsor must be slow relative to the period required to drive an airborne skim (132-199 Hz, i.e. a 5.0-7.6 ms cycle).",
      "quantity": "maximum tail-beat frequency", "lo": null,
      "hi": 132, "units": "Hz",
      "status": "satisfied",
      "satisfied_by": "Measured zebrafish tail-beat ceiling: 95 Hz in larvae at 4-5 dpf (the fastest-beating life stage), period 10.5 ms, which is 1.4-2.1x slower than the skim requirement. The project's own 52 Hz input is 2.5-3.8x short and a relayed adult value of ~21 Hz is 6.3-9.5x short.",
      "satisfied_evidence": "measured",
      "note": "van Leeuwen JL, Voesenek CJ, Muller UK 2015, J R Soc Interface 12:20150479, doi:10.1098/rsif.2015.0479, author's statement quoted verbatim: 'Larvae at 4-5 dpf reach higher f (95 Hz) and A_tail (2.4 mm) than at 2 dpf (80 Hz, 1.8 mm)'; read-level full-text via automated fetch, quoted sentence only. Same paper says adults use 'narrower, lower frequency body waves' with no number, so my inference is that the larval value bounds the adult from above. The ~21 Hz adult figure is attributed to Kyriakatos et al. 2011 by a secondary article in my search results; read-level search-summary, neither opened, so it is listed but not relied on. Three numbers (95/52/21 Hz) are not averaged; the constraint holds under all three. Negative-search scope: two standard-mode web searches for an adult zebrafish escape/fast-start tail-beat maximum plus one article fetch returned only larval or adult sustained-swimming values - nobody has published an adult escape maximum I could reach, which is not the same as people having looked and found none."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "The mass fraction of the fin-driving musculature must lie below what weight-supporting flapping flight requires; above it, powered flight is not excluded on power grounds.",
      "quantity": "paired-fin muscle mass as a fraction of body mass", "lo": 0,
      "hi": 7.5, "units": "% of body mass",
      "status": "open",
      "satisfied_by": "NOT ESTABLISHED. The repository relays ~1.4% for teleost pectoral musculature against a 7.5-20% requirement (S28 section 5 row 6, labelled 'measured, teleost, not zebrafish') but attaches no primary citation, so I cannot give it a read-level above listing or name the species. My search for a zebrafish value found fin myology and development (Patterson & Devoto 2008; ZFIN figure records) and a comparative review (Mansuit & Herrel 2021, listing, not opened) but no mass fraction. For the constraint to fail the zebrafish fin musculature would have to be 5x the relayed teleost fraction, which I find implausible - and implausible does not license 'satisfied'.",
      "satisfied_evidence": "unknown",
      "note": "Negative-search scope: one standard-mode web search for zebrafish pectoral fin muscle mass as a percentage of body mass. No zebrafish figure found; the teleost ~1.4% reaches me only as an uncited repository relay. Cheapest closure: weigh paired-fin musculature in the existing animals (hours), which is S28 section 4's own lowest-ranked candidate."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The water-exit speed actually achieved in a leap must lie below the takeoff speed for weight-supporting flight (and below the speed that would treble the ballistic leap).",
      "quantity": "water-exit speed of a leaping adult", "lo": 0,
      "hi": 4.32, "units": "m/s",
      "status": "open",
      "satisfied_by": "THE BOUNDED QUANTITY HAS NEVER BEEN MEASURED in adult zebrafish. Only stand-ins exist, all inside the bound: in-water escape peaks of 1.38 m/s per-fish max (Miln et al. 2021, n=50, 120 fps) and 1.57 +/- 0.27 m/s (Demesmay et al. 2025, 240 fps, +2 SD = 2.11 m/s), both read-level listing via repository relay; and reported TERRESTRIAL jump distances for Danio rerio of mean ~0.10 m and max ~0.27 m, which imply 0.99 and 1.63 m/s at a 45-degree vacuum launch (my calculation). Treating an in-water escape peak as a surface-exit speed is an assumption about the very quantity bounded - S28 calls it 'generous' because breaking the surface costs speed - so this is open, not satisfied.",
      "satisfied_evidence": "literature",
      "note": "Bound 4.32 m/s is my calculation of V_to at S28's generous case-C area (201 mm^2, CL 1.07, m 0.25 g assumed); with the figure-read area it rises to 6.23-8.64 m/s. The secondary bound for a 3x leap is 2.39 m/s = sqrt(3) x 1.38, only x1.13 above Demesmay +2 SD and x1.47 above the jump-implied 1.63 m/s. Terrestrial-jump figures are a DIFFERENT behaviour (stranded fish, tail-flip driven, Danio takeoff reported near 90 degrees) from a conference abstract I could not open: sicb.org does not resolve from this session and must be allowed in the session's network settings; read-level search-summary, and the ~0.27 m maximum sits oddly against an arena reported as ~0.1 m across, so I record it as a pointer, not a bound. Negative-search scope: S28-D's access record for Miln and Demesmay plus two standard-mode web searches of mine for zebrafish leap/aerial kinematics, which returned terrestrial jumping (Gibb et al. 2011, J Exp Zool A 315A:649-653, PMID 21972177, search-summary), guppy aerial jumping (PMC3629028, search-summary) and a cross-taxon H/L ~ Fr^2 scaling result. No zebrafish surface-exit measurement exists in anything I reached: nobody has measured it, as distinct from it having been measured and found low."},
    {"target_scale": "behaviour", "kind": "existence",
      "statement": "No in-air behaviour may exist that supplies lift beyond the quasi-steady value of a fully abducted fin - no unsteady or flapping augmentation large enough to turn a +1.5-3% range gain into a meaningful leap extension.",
      "quantity": "in-air lift augmentation over the quasi-steady spread-fin value", "lo": null,
      "hi": 2, "units": "x (multiple of quasi-steady CL)",
      "status": "unsatisfied",
      "satisfied_by": "NOTHING KNOWN MEETS IT: what zebrafish fins do during the airborne phase has never been observed. S28's own model assumes the fins are held spread at CL 1.07 throughout the leap and labels that 'generous and unobserved'. Measured behaviour in other small teleosts points the other way: jumping Poecilia reticulata 'continue with whole body thrusts and tail beats, even when out of the water' (PMC3629028, read-level search-summary), and archerfish accounts describe raising the pectoral and pelvic fins before takeoff. Two calculations bound how much this could matter: an airborne tail beat at matched kinematics transfers momentum in proportion to fluid density, rho_air/rho_water = 1.23e-3 (1/815); and on the lift route, doubling CL is equivalent to doubling area, which in S28-D-D's own table moves the ascent-deceleration reduction only from 1.4-2.6% to about 2.6-5.1%, still not a meaningful extension and still x2 or more short in speed for flight.",
      "satisfied_evidence": "unknown",
      "note": "Negative-search scope: one standard-mode web search for in-air pectoral fin abduction kinematics in any fish, which found no study measuring fin spread during the airborne phase; plus the repository record (S28, S28-D, challenge 262) which independently lists in-air abduction as unobserved. The density ratio and the CL-doubling figures are my calculations (docs/research/fish/claim-189-entail_calc.py and S28-D-D's table), not observations. This is the one constraint whose status a single session with a >=1000 fps camera could change in either direction."}
  ]}
```
