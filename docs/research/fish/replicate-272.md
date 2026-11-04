# Replication of claim 272: the lobe drag coefficient (C_D) gap between zebrafish and exocoetids

**Status:** independent re-derivation, partial. The size argument cannot be turned into a single number from the sources I could access. It gives one of two answers depending on which drag regime governs the lobe. I did not choose between them.

## What I was asked

Zebrafish and exocoetids (flying fish) are said to share f·A_pp/V_to ≈ 0.09–0.10, a Strouhal-type ratio: tail-beat frequency × peak-to-peak amplitude / take-off speed. They are said to differ only in the drag coefficient of the caudal lobe at their own Reynolds numbers. My task was to derive that difference.

## Provenance check (where the inputs were meant to live)

- The brief says the inputs live in `S32-organism.md`. **That file does not exist in this repository.**
  - Search scope: `find . -name "S32*"`, plus `git ls-files` filtered on S32/organism/fish, on branch `claude/replicate-272-fish-size-qg3d5j`.
  - Only two branches exist, this one and `work/frontier-foundation`. The repository has 30 commits.
- `grep -ril` for `zebrafish|exocoet|flying fish|A_pp|V_to` found only two files: `findings/gemini-*.json`. Both are unrelated triage text about zebrafish fin regeneration and ZFIN. Neither holds working for this claim.
- **I did not see the original derivation or its recorded value.** So I cannot use the 0.09–0.10 ratio's own inputs (f, A_pp, V_to). I take the ratio as given in the brief, not as something I reproduced.

## Inputs

| # | Quantity | Value used | Source | Read-level | Nature |
|---|---|---|---|---|---|
| 1 | Exocoetid body length | 0.25 m (mass 0.191 kg) | Deng J, Wang S, Zhang L, Mao X (2019), "Why does a flying fish taxi on sea surface before take-off? A hydrodynamic interpretation", bioRxiv 10.1101/765560 (Europe PMC PPR91964) | abstract | A **model** fish in a CFD study, not a measured animal |
| 2 | Exocoetid taxiing / take-off speed | 10 m/s | Same, abstract: "the fish is assumed to swim at a constant speed of 10 m s⁻¹" | abstract | **Assumed** CFD input |
| 3 | Exocoetid taxiing tail-beat frequency | 50 Hz (minimum-power case); the literature quoted in search snippets gives 50–70 Hz | Deng et al., abstract; snippet of the same preprint | abstract; search-summary | **Simulated** optimum. One APS 2024 abstract snippet reports 13.5 Hz instead. That is unresolved disagreement and I have not averaged it away. |
| 4 | Exocoetid hypocaudal lobe chord | `unknown`; I bracket it at 0.02–0.05 m (8–20 % of body length) | Not found. Tried web search; the full PDF was rate-limited/blocked (HTTP 429, Cloudflare 1015) | could-not-access | **My assumption** |
| 5 | Zebrafish take-off / burst speed | `unknown`; I bracket it at 0.3–1 m/s | Not found. Web search turned up larval data only; the one sourced length is 4.2 mm at 5 dpf | search-summary | **My assumption** |
| 6 | Zebrafish caudal lobe chord | `unknown`; I bracket it at 3–8 mm | Not found | — | **My assumption** |
| 7 | Kinematic viscosity of water | 1.0×10⁻⁶ m²/s | Textbook value for water at about 20–25 °C | — | Standard constant |
| 8 | Laminar flat-plate friction | C_f = 1.328/√Re | Blasius solution (textbook) | — | Standard formula |
| 9 | Turbulent flat-plate friction | C_f = 0.074·Re^(−0.2) | Prandtl 1/5-power law (textbook) | — | Standard formula |
| 10 | Bluff-plate pressure drag | C_D ≈ 1.2–2, roughly independent of Re above about 10³ | Hoerner, *Fluid-Dynamic Drag* (from memory, not re-read) | could-not-access (recalled) | Standard result |

## Arithmetic (all calculated, none observed)

Reynolds number of the lobe is Re = U·c/ν.

- **Zebrafish:**
  - Low end: 0.3 × 0.003 / 1e-6 = 900.
  - High end: 1.0 × 0.008 / 1e-6 = 8,000.
  - Central value: about 3,000.
- **Exocoetid:**
  - Low end: 10 × 0.02 / 1e-6 = 2×10⁵.
  - High end: 10 × 0.05 / 1e-6 = 5×10⁵.
  - Central value: about 4×10⁵.

So the two Reynolds numbers are about two orders of magnitude apart (a factor of about 25–550). That conclusion holds across every bracket I tried.

**Regime A: friction-dominated lobe** (lobe moving roughly edgewise).

| Re_zf | C_f,zf (laminar) | Re_ex | C_f,ex (laminar) | C_f,ex (turbulent) | Ratio, laminar/laminar | Ratio, laminar/turbulent |
|---|---|---|---|---|---|---|
| 900 | 0.0443 | 2e5 | 0.00297 | 0.00644 | 14.9 | 6.9 |
| 3000 | 0.0242 | 4e5 | 0.00210 | 0.00561 | **11.6** | **4.3** |
| 8000 | 0.0148 | 5e5 | 0.00188 | 0.00536 | 7.9 | 2.8 |

The full grid (3×3 Re pairs) runs from 2.3 to 23.6. The script output is in the session log; the rows above are a subset of it.

**Regime B: pressure-dominated lobe** (lobe moving broadside, as in lateral tail beating).

C_D,zf / C_D,ex ≈ 1.2–2 / 1.2–2 ≈ **1** (somewhere between 0.6 and 1.7). Both Reynolds numbers sit above about 10³, where bluff-plate drag barely depends on Re.

## My value

- **Calculated, not observed:** zebrafish lobe C_D / exocoetid lobe C_D ≈ **4–12 (central about 5–10; full bracket 2.3–24)** if the lobe's drag is mainly skin friction.
- It is ≈ **1 (0.6–1.7)** if the drag is mainly pressure (form) drag.
- The ratio of Reynolds numbers, about 10², is the robust part.
- Whether the Re gap turns into a C_D gap depends on the drag regime. That is a modelling choice I could not settle from primary data.

**My inference, not a sourced claim:** a taxiing exocoetid beats its lower lobe laterally through the water at 50–70 Hz. That kinematics suggests mainly pressure/added-mass loading, which is Regime B. On that view the claim that the two fish "differ only in lobe C_D" would explain little. Only if friction or the viscous boundary layer dominates does a "size argument" with a large factor (about 4–12) follow.

## Comparison with the recorded value

I could not find the recorded value. `S32-organism.md` is absent from the repository, and no other file in it carries this claim. Verdict: **CANNOT TELL.**

```swarm-replication
{"claim_id": 272, "my_value": "lobe C_D ratio zebrafish/exocoetid ~4-12 (bracket 2.3-24) if friction-dominated, ~1 (0.6-1.7) if pressure-dominated; Re_zf ~1e3-8e3 vs Re_ex ~2e5-5e5 (calculated, dimensionless)", "agrees": null, "note": "S32-organism.md and the recorded value are absent from the repo, and the zebrafish speed and both lobe chords are unsourced assumptions, so this brackets the claim rather than confirms it."}
```
