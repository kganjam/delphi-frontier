# Challenge 224: adversarial review of the S29 stored-spring-energy figure

**Claim under review (the author's, not mine):** "A 0.4 g body at 4.37 m/s needs 3.82 mJ (9.55 J/kg). With 6.5 % in-water drag, the best measured C-start hydromechanical efficiency 0.37 and 0.93 tendon return, the spring must store 11.8 mJ (29.6 J/kg). Both figures reproduced here."
**Recorded evidence level:** derived. **Value:** 11.8 mJ stored.
**Source read:** `docs/research/fish/S29-organism.md` on branch `origin/claude/s29-launch-energy-2iuixr`. Read level: full-text (the whole file). I did not run the author's script `S29_launch_energy.py`. Every check below is my own recomputation.

**Verdict: WEAKENED.** The arithmetic is exact. However, "must store 11.8 mJ" is the optimistic end of the author's own inputs, stated as a requirement. It is a lower-bound central case, not a requirement.

---

## 1. Independent arithmetic (calculated by me, not observed)

I used only the stated inputs: m = 0.40 g, V = 4.37 m/s, ρ = 1000 kg m⁻³, Cd = 0.2, A = 24 mm², stroke s = 1.09 cm, η_h = 0.37, spring return r = 0.93.

| Quantity | My result | Author | Match |
|---|---|---|---|
| KE = ½mV² | 3.8194 mJ = 9.548 J/kg | 3.82 mJ, 9.55 J/kg | yes |
| Drag work ½ρCdAV²·s/2 | 0.2498 mJ = 6.54 % of KE | 0.250 mJ, 6.5 % | yes |
| (KE + W_d)/η_h/r | 11.826 mJ = 29.56 J/kg | 11.8 mJ, 29.6 J/kg | yes |

**The arithmetic survives.** The ½ factor in the drag integral is correct: under constant acceleration, v² is linear in x, so the mean of v² over the stroke is V²/2.

## 2. Proxy check: is η_h the efficiency that matters?

The quantity the claim needs is **spring-stored energy → centre-of-mass kinetic energy at exit**. The number used is a **hydromechanical efficiency of a pike C-start**. As the author describes it (ABSTRACT read level, via a UBC record), this is useful power over the mechanical power output of the fast-start.

**My inference, not the author's:** these are not the same quantity, for three reasons.

- **The spring path has losses that η_h does not contain.** These include internal tissue damping as the body is bent and unbent, energy left in lateral and rotational segment motion, and latch losses. Each of these would *raise* the required store. So 11.8 mJ is a **lower bound on its own inputs, not "must store"**.
- **η_h is a whole-manoeuvre average over a turning C-start**, which is not a straight push-off toward the surface. Which way this biases the result is unknown.
- **The author double-counts drag work.** It is added explicitly and may also sit inside η_h. The author flags this, at about 6 %, conservative. I agree with that assessment.

I tried to read the primary pike source to see how it defines efficiency. Search found the record as H. R. Frith, *Energetics of fast-starts in northern pike, Esox lucius*, UBC thesis, 1990 (read level: search-summary). The search extract gives "average hydrodynamic efficiency of 0.37" but is truncated. Fetching `open.library.ubc.ca` failed: the host is not in this session's network allowlist. The author's attribution to "Frith & Blake" is not confirmed by what I could read. The co-author is `unknown` to me.

## 3. Hidden assumption, relaxed: the 0.93 return

The 0.93 return comes from **sheep** tendon (Ker 1981, which the author read at ABSTRACT level). But the same S29 document cites Shadwick (ABSTRACT) for **tuna axial tendon at 7–25 % dissipation**, a return of 0.75–0.93. It uses that tuna source for the spring *volume* (E and strain) and then switches to the mammalian figure for the *return*. Because the hypothetical organism is a teleost, the fish range is the consistent input.

Here are the author's own stated ranges, run through the same formula. All values are calculated, not measured.

| Drag fraction | η_h | r | Stored (mJ) | J/kg body |
|---|---|---|---|---|
| 3 % | 0.39 | 0.93 | 10.85 | 27.1 |
| **6.5 %** | **0.37** | **0.93** | **11.83** | **29.6** (the claim) |
| 6.5 % | 0.37 | 0.75 | 14.66 | 36.6 |
| 27 % | 0.37 | 0.93 | 14.10 | 35.2 |
| 27 % | 0.34 | 0.75 | 19.02 | 47.6 |

So the claim's 11.8 mJ sits near the **bottom** of a 10.9–19.0 mJ range built only from inputs the author already cites. The direction matters for S29's verdict. A higher stored-energy requirement widens S29's 1.86× energy shortfall. It does not close it. So S29's NEGATIVE conclusion is *strengthened*, not overturned. What is weakened is the claim as a stand-alone requirement.

## 4. Is the evidence level honest?

Mostly, yes. The claim is labelled "derived" and is derived; nothing is presented as measured. Two small defects:

- **"Best measured" is unverified.** The author's own range is 0.34–0.39. If 0.37 is the mean, then 0.39 is the best, which would give 11.2 mJ. The word "best" is also unverified against any systematic survey (see §5).
- **"Must store" overstates certainty.** On the claim's own inputs this is a central, optimistic estimate, as argued in §2.

## 5. Regime and taxon counter-examples

- **A cyprinid source exists that the author did not use.** Wakeling, Kemp & Johnston 1999, J. Exp. Biol. 202:3057 (read level: search-summary), studied carp (*Cyprinus carpio*), a cyprinid like zebrafish, from 7 mm larvae to 80 mm juveniles. They define hydrodynamic efficiency as inertial power in the direction of travel over muscle power, and report it **did not change significantly across size**. That supports transferring an efficiency across size, which the author assumed without support. I could not get their numbers: fetching `discovery-pp.ucl.ac.uk` failed under the network policy, so the values are `unknown`.
- **Temperature dependence.** A follow-up study (Wakeling, Cole, Kemp & Johnston 2000; read level: search-summary) reports carp fast-start hydrodynamic efficiency rising from **0.19 to 0.38** over acute temperatures of 10–20 °C.
  - The upper end matches pike at 0.37, so I find **no counter-example above 0.37–0.39**. "Best measured ≈ 0.37–0.38" survives within my search scope.
  - The efficiency is strongly temperature-dependent. At 0.19 the store would be 23.0 mJ (calculated). A zebrafish kept at ~28 °C lies outside the measured 10–20 °C range, so no value for it is available: `unknown`.
- **Mechanical-fish models** report about 11–12 % efficiency (MIT pike and chain-pickerel robots; read level: search-summary). These are robots, not organisms, and not directly comparable. I note them only as evidence that 0.37 is not a floor.

**Scope of negative searches.** I ran three web searches (standard mode) on pike and carp fast-start hydrodynamic efficiency. I made two fetch attempts, and both were blocked by the network allowlist. I did no systematic survey of fast-start efficiency across taxa. "No value above ~0.39 found" holds only within that scope.

## 6. Summary

- **Arithmetic:** reproduced exactly (11.83 mJ, 29.56 J/kg).
- **Defect:** the figure is presented as what the spring "must store". It is really the optimistic end of the author's own cited inputs, for two reasons:
  - It uses mammalian tendon return (0.93) where the document's own fish-tendon source gives 0.75–0.93.
  - It uses a whole-C-start hydromechanical efficiency as a stand-in for spring-to-centre-of-mass efficiency, which omits internal and latch losses.
- **Corrected statement (mine):** a stored energy of **≥ 11.8 mJ (≥ 29.6 J/kg)**, with about **11–19 mJ (27–48 J/kg)** across the author's own stated input ranges. All of these are calculated, not measured.
- **Effect on S29:** the error runs in the direction that makes S29's NEGATIVE verdict *more* secure.

### Sources
- `docs/research/fish/S29-organism.md` (origin/claude/s29-launch-energy-2iuixr): full-text.
- Frith 1990, UBC thesis, *Energetics of fast-starts in northern pike* — https://open.library.ubc.ca/collections/831/items/1.0100459: search-summary (fetch blocked).
- Wakeling, Kemp & Johnston 1999, J. Exp. Biol. 202:3057 — https://research-portal.st-andrews.ac.uk/en/publications/the-biomechanics-of-fast-starts-during-ontogeny-in-the-common-car/ : search-summary (PDF at discovery-pp.ucl.ac.uk could not be accessed).
- Wakeling, Cole, Kemp & Johnston 2000, thermal acclimation in carp — https://researchers.mq.edu.au/en/publications/the-biomechanics-and-evolutionary-significance-of-thermal-acclima/ : search-summary.
- MIT mechanical pike — https://dspace.mit.edu/handle/1721.1/39203 : search-summary.
- Ker 1981 and Shadwick (tuna tendon): not read by me. Values are taken as S29 reports them (S29 read them at ABSTRACT level).

```swarm-challenge
{"claim_id": 224, "outcome": "weakened", "reason": "The arithmetic reproduces exactly (11.83 mJ, 29.56 J/kg), but 'must store' is the optimistic end of the author's own inputs: mammalian 0.93 return where S29's own fish-tendon source gives 0.75-0.93, and a whole-C-start hydromechanical efficiency standing in for spring-to-COM efficiency, which omits internal and latch losses; the honest statement is a lower bound with a range of about 11-19 mJ.", "corrected_value": ">= 11.8 mJ (>= 29.6 J/kg); about 10.9-19.0 mJ (27-48 J/kg) across S29's stated drag 3-27%, eta_h 0.34-0.39, return 0.75-0.93", "depends_on": ["S28 4.37 m/s target and 24 mm^2 frontal area", "S29 Cd 0.1-0.3 and stroke 1-3 cm drag range", "Frith 1990 pike C-start eta_h 0.34-0.39 (search-summary; S29 ABSTRACT)", "Shadwick tuna tendon dissipation 7-25% (as reported in S29, ABSTRACT)", "Ker 1981 tendon return 0.93 (as reported in S29, ABSTRACT)", "Wakeling et al. 1999/2000 carp hydrodynamic efficiency 0.19-0.38 and size-invariance (search-summary)"]}
```
