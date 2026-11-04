# Replication of claim 284 (S18-D): the required/available frequency ratio for active attitude control

**Status:** independent re-derivation of the required/available frequency ratio R = f_req / f_avail.
**Date:** 2026-11-04.

## Contamination disclosure (read this first)

The inputs live on `origin/claude/deepen-s18-zebrafish-air-3u64z4`, in the file `docs/research/fish/S18-deepen.md`. I ran a keyword `grep` over that file to find the *required* frequency and S18's reference-design parameters. That grep printed two lines that contain the recorded result: line 122 (the R values) and line 179 (the answer string). **I saw the recorded value before deriving mine.** After that I stopped reading the file's conclusions. I took from it only:

- S18's quoted pitch-frequency statement;
- the reference-design parameters, read from its script listing;
- the citations it gives for the larval gain figures.

I re-sourced f_avail myself from the toadfish primary literature, and I recomputed f_req with my own script. Take this as a partly blinded replication, not a fully blinded one.

## What R means

R = f_req / f_avail.

- **f_req** is the frequency the controller must track. Here that is the pitch short-period frequency of S18's reference 0.4 g glider. It is **calculated** on a made-up design, not observed.
- **f_avail** is the frequency up to which the vestibular sensor is known to respond.

If R < 1, the sensor bandwidth alone does not rule out active control.

## Inputs

| # | Input | Value | Source | Read-level |
|---|---|---|---|---|
| I1 | Pitch frequency model | f_n = (1/2π)·√(½ρV²·S_t·l_t·a_t / I_y) | S18's formula, as reproduced in `S18-deepen.md` | listing (secondhand: I did not find S18's own document on this branch or on `work/frontier-foundation`) |
| I2 | Reference-design parameters | m = 0.4 g, L = 0.04 m, I_y = mL²/12 = 5.33×10⁻⁸ kg m², S_t = 1×10⁻⁴ m², l_t = 0.02 m, a_t = 1.6 rad⁻¹, ρ = 1.2 kg m⁻³ | same listing; these are S18's **made-up** design values | listing |
| I3 | S18's original f_avail | 0.5 Hz, "highest measured zebrafish vestibular-reflex test frequency" | S18, as quoted in `S18-deepen.md` | listing (secondhand) |
| I4 | Toadfish horizontal-canal afferents (*Opsanus tau*): sinusoidal rotation **0.001–10 Hz**, 5–100 °/s, 66 afferents; high-gain afferents "show a high-frequency gain enhancement and phase advance" | test range 10 Hz | Boyle R, Highstein SM (1990) *J Neurosci* 10(5):1557–1569, PMC6570080 | abstract (I could not fetch the full-text PDF: www.jneurosci.org is outside this session's network allowlist) |
| I5 | Toadfish canal afferents: sinusoidal stimuli **0.1–20 Hz**, with sweeps "limited to <20 Hz"; rapidly adapting afferents show a 90° phase lead and frequency-dependent gain; no afferent upper corner is reported | test range 20 Hz | Rabbitt RD, Boyle R, Holstein GR, Highstein SM (2004/2005) "Hair-cell versus afferent adaptation in the semicircular canals", *J Neurophysiol* 93:424–436, PMC3000937 | full-text, first 100k of about 131k characters, via fetch-tool summary |
| I6 | Toadfish afferent transfer functions over about 0.02–30 Hz | — | Highstein et al. (1996) *J Neurophysiol* | search-summary only. **Not used for any number.** |
| I7 | Endolymph kinematic viscosity | ν ≈ 1×10⁻⁶ m² s⁻¹ (water) | **assumption** | — |
| I8 | Reflex gains: larval pitch correction 0.29 / 0.44; adult AVOR 0.20 | — | Hamling et al., bioRxiv 2023.12.06.570482; D1 in the deepen file | **not re-read by me.** They are cited from the deepen file and do not enter R. |

### What the toadfish sources do and do not establish

- **What the authors state.** Both toadfish studies tested up to 10 Hz (I4) or 20 Hz (I5). Their models describe high-frequency gain *enhancement* and phase *advance* (I4, I5). Neither text I could read reports an upper corner frequency or a high-frequency roll-off.
- **My inference.** The afferents were still responding at the top of the tested band. Gain enhancement rather than a roll-off means 10 Hz and 20 Hz are **lower bounds** on the bandwidth, not measured bandwidths.
- **This is the same kind of limit as S18's 0.5 Hz.** It is a test-protocol ceiling. The difference is direction: these ceilings sit above f_req, so they still bound R from above.
- **Caveat.** I did not see a 10 Hz gain value in any text I read. The abstract (I4) does not say what the response was at exactly 10 Hz.

## Arithmetic (calculated, not observed)

Here k scales S_t·l_t/I_y over ×0.25 to ×4, which moves f_req by ×0.5 to ×2. That is the geometry sensitivity.

ω = √(½·1.2·V²·1e-4·0.02·1.6 / 5.333e-8) = √(36·V²) = 6.0·V rad s⁻¹, so f_req = 6.0V / 2π = **0.955·V Hz**.

| V (m s⁻¹) | f_req, reference (Hz) | f_req, geometry ×0.5 to ×2 (Hz) |
|---|---|---|
| 1 | 0.955 | 0.48 – 1.91 |
| 2 | 1.910 | 0.95 – 3.82 |
| 3 | 2.865 | 1.43 – 5.73 |

The ratio R at each candidate f_avail, for the reference geometry at 1 / 2 / 3 m s⁻¹:

| f_avail | Basis | R at 1 / 2 / 3 m s⁻¹ |
|---|---|---|
| 0.5 Hz | S18, larval test ceiling | 1.91 / 3.82 / 5.73 |
| ≥ 10 Hz | toadfish, I4 | **0.095 / 0.191 / 0.286** (upper bounds) |
| ≥ 20 Hz | toadfish, I5 | 0.048 / 0.095 / 0.143 (upper bounds) |

Adding the geometry range: at f_avail ≥ 10 Hz, R spans 0.048 to 0.57 across 1–3 m s⁻¹. At f_avail ≥ 20 Hz it spans 0.024 to 0.29.

**Steinhausen cross-check** (calculated, using assumption I7). The canal's upper corner is f_u = 1/(2π·τ_s), with τ_s = r²/(8ν). So f_u ≥ 10 Hz needs a duct radius r ≤ 0.36 mm, and f_u ≥ 20 Hz needs r ≤ 0.25 mm. I did not find a measured duct radius for either toadfish or zebrafish (scope: none of the sources above). So this check stays open; it does not confirm anything.

## My value

**R ≈ 0.1–0.3** at 1–3 m s⁻¹ on S18's reference geometry, with f_avail ≥ 10 Hz.

- R is an upper bound, because 10 Hz is itself a test ceiling.
- If 20 Hz is used instead, R ≈ 0.05–0.14.
- If the geometry varies ×0.5 to ×2, R can reach 0.57. That is still below 1.

On the same inputs, S18's version was R ≈ 1.9–5.7. So I find R < 1 across every case I computed.

**Uncertainty, and what limits the conclusion.**

1. **f_req is calculated on an invented airframe.** It is not observed.
2. **f_avail is cross-species.** It comes from toadfish, not adult zebrafish. Adult zebrafish canal bandwidth is `unknown`: I found no adult *D. rerio* canal-afferent frequency sweep in the searches I ran (two web searches for toadfish canal-afferent frequency response, plus the papers above).
3. **The toadfish full text was only partly read** (I4 abstract only; I5 the first 100k of about 131k characters).
4. **Peripheral bandwidth is not closed-loop bandwidth.** Central processing, the gain (I8) and the latency still limit the loop. Adult latency is `unknown`. All of this means the bandwidth argument *against* active control falls, but it does not follow that active control is feasible.

## Comparison with the recorded value

**Recorded value**, which I saw early through the grep (see the disclosure above): R = 0.10 / 0.19 / 0.29 at 1 / 2 / 3 m s⁻¹, "0.1–0.3 instead of 2–6".

**Mine:** 0.095 / 0.191 / 0.286 at f_avail = 10 Hz. **I AGREE** on the number and on the qualitative conclusion (R < 1, so the bandwidth argument falls).

Where my reading adds to the recorded claim:

- **(a)** 10 Hz and 20 Hz are also test ceilings, not measured bandwidths. That makes R an upper bound, which strengthens "falls". But the claim's wording, that the afferents "respond across 0.1–10/20 Hz", rests on test ranges plus model descriptions, not on a 10 Hz gain value I could read.
- **(b)** The geometry range widens R to as much as 0.57.
- **(c)** The agreement is partly weakened as evidence. I computed f_req from the same reference parameters, and I saw the result before my own derivation.

```swarm-replication
{"claim_id": 284, "my_value": "R = f_req/f_avail ≈ 0.10-0.29 (dimensionless; 1-3 m/s, f_avail ≥10 Hz toadfish test ceiling, so an upper bound; up to 0.57 with ×0.5–×2 geometry; 0.05-0.14 if f_avail ≥20 Hz)", "agrees": true,
  "note": "My f_avail came independently from the toadfish primary sources (Boyle & Highstein 1990 abstract; Rabbitt et al. 2004 partial full text), and my recomputed f_req reproduces R≈0.1-0.3, though I saw the recorded value through a grep before deriving mine and the toadfish 10/20 Hz figures are themselves test ceilings, not measured corners."}
```
