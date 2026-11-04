# Challenge 225: "SPRING VOLUME PASSES"

**Claim under review (the S29 author's claim, not mine):** "SPRING VOLUME PASSES: 1–4 % of body volume as mammal-grade tendon, 13–24 % at measured fish-tendon strains." Recorded evidence level: *derived*. Recorded value: 4 percent body volume.
**Source:** `docs/research/fish/S29-organism.md` §2.4 and §6, on branch `claude/s29-launch-energy-2iuixr` (commit 44ed219). **Read level: full-text**, including the script `S29_launch_energy.py`.
**My working:** `docs/research/fish/challenge_225.py`. Every number below is printed by it. **Everything in this note is calculated. None of it is a measurement.**

## Verdict: WEAKENED

The arithmetic is correct. The claim still overstates the pass, for three reasons:

1. **The low end sits at tendon fracture stress.** The 1 % figure is not a working-stress figure.
2. **The fish-tendon rows mix inputs.** They use a fish modulus with a mammalian energy return.
3. **Volume is a proxy.** On the anatomy S29 itself specifies, a spring of the right volume cannot be given the right shape.

At the mass-consistent target speed, the fish-tendon case reaches 21–47 % of body volume. At that size "it fits" is no longer self-evident.

## 1. Independent arithmetic

I took S29's inputs as stated and recomputed from them:
- stored energy 11.83 mJ (central case)
- body 0.40 g at 1050 kg m⁻³, so body volume 381.0 mm³
- E = 1.65 GPa
- tuna tendon E 0.65–1.2 GPa at 2 % strain

The energy densities u = σ²/2E and u = ½Eε² reproduce S29 exactly: 3.9 mm³ (1.0 %), 15.6 mm³ (4.1 %), 49.3 mm³ (12.9 %) and 91.0 mm³ (23.9 %). **I found no arithmetic error.**

There is one small internal inconsistency. S29 §0 says "0.8–4 %", while §2.4 and §6 say "1–4 %". The 0.8 % matches none of the table's central-case rows (its 0.78 % is the resilin failure-toughness row).

## 2. Hidden assumptions, tested relaxed

### 2a. The 100 MPa row is a fracture stress, not a working stress

| Source | What it says | Read level |
|---|---|---|
| Ker, Alexander & Bennett 1988, "Why are mammalian tendons so thick?" | Tendon fracture stress is about **100 MPa**. Typical limb-tendon stress in use is about **13 MPa**. | search-summary |
| Ker 1981, J. Exp. Biol. 93:283 | Estimated peak stress in the sheep plantaris during fast locomotion is about **75 MN m⁻²**. | search-summary of the abstract and text |

S29 attributes "50–100 MPa working stress" to Ker as a figure for a galloping antelope. **I could not confirm the antelope figure.** The 75 MPa value above is the one my search returned. I am recording this as a disagreement between sources, not resolving it.

Applying that stress range (my inference):
- **Working-stress band, 50–75 MPa:** 1.8–4.1 % of body volume. The "1 %" end needs the spring to be loaded to roughly its failure stress on every launch.
- **Typical tendon stress, 13 MPa:** 61 %. This is not the right comparison for a dedicated spring tendon, since spring tendons are thin precisely so they run at high stress. I include it only to show how sensitive the result is to the chosen stress.

### 2b. The fish-tendon rows use a mammalian return

The rows at 13–24 % use the tuna modulus and the tuna burst strain. They keep the **0.93** return taken from sheep tendon. S29 itself quotes the same Shadwick abstract as giving **7–25 % dissipation** for tuna tendon (S29's read level: abstract; I did not re-read it).

Using the fish's own dissipation consistently gives a return of 0.75 at the low end:
- stored energy rises to 14.67 mJ
- spring volume becomes **13–30 %** (the 0.65 GPa row moves from 23.9 % to 29.6 %)

### 2c. The target speed

S29 flags this optimism in its own text, but leaves it out of the claim. At the mass-consistent 5.53 m/s, kinetic energy rises ×1.60. I scaled the drag term by the same factor, which is an approximation. The spring volume becomes:
- **2.9–6.6 %** for mammal tendon at working stress
- **21–47 %** for fish tendon

At 21–47 % the claim needs re-checking against the rest of S29's own budget. S29 §5 reaches break-even only when about 60 % of body mass is muscle loading the spring. Then 60 % muscle plus 21–47 % tendon leaves 0 to about 20 % of the body for skeleton, viscera, swim bladder, the latch and everything else.

That comparison mixes mass and volume fractions, which are close at near-equal densities. It is my inference, not S29's. **"Either way it fits" is not supported for the fish-tendon case.**

### 2d. Is measured strain the same as strain capacity?

This point works in the claim's favour. The 2 % is the strain tuna tendon *reaches* at burst, not a material limit. Fish collagen could likely be strained further. On this point the 13–24 % is pessimistic, and I do not count it against the claim.

## 3. Proxy: volume stands in for packaging

The real requirement is that a tendon of length L and area A can be:
- stretched by the muscle to the stored energy
- fitted inside a body 3.0 cm long (S29's stroke table: 1.5 cm = ½ BL)

Volume alone cannot show this. For a linear spring loaded to force F, the stretch is δ = 2W/F, and the length is L = δ/ε.

**Force inputs:**
- Frontal area: 24 mm² (S29/S28).
- Fast-muscle isometric stress: 186 kPa. This is my conversion of 18.65 N cm⁻² for cod fast skinned fibres (Altringham & Johnston 1982, J. Physiol.; read level: search-summary). Zebrafish was not found.

**Results for a direct series tendon (no lever)**, which is S29 §4 item 1: "a series elastic element loaded by the axial muscle of one side".

| Muscle cross-section pulling | F | Stretch needed | Tendon L at 75 MPa | at 50 MPa | at fish 2 % |
|---|---|---|---|---|---|
| ~30 % of frontal area (one side, ASSUMED) | 1.34 N | 17.7 mm (59 % BL) | 389 mm = **13 BL** | 19 BL | 29 BL |
| 100 % of frontal area (upper bound, impossible) | 4.46 N | 5.3 mm (18 % BL) | 117 mm = **3.9 BL** | 5.8 BL | 8.8 BL |

Even with the entire cross-section treated as muscle, the tendon has the right volume but is **4–9 body lengths long and 0.06–0.09 mm² thick**.

**A lever could fix the shape, but not the excursion.** A lever of gain G shortens the tendon by a factor of G. That means G ≥ 4 to 13 just to reach one body length, which is a further skeletal invention beyond the latch. The muscle must still shorten 5–18 mm at full force. That requirement is the energy-per-stroke wall S29 already identifies as binding. It is not a separate fault, but it shows that the volume "pass" and the energy "fail" are the same constraint seen twice. The volume test passes only because it ignores force and excursion.

## 4. Is the evidence level honest?

Yes. S29 labels the number *derived* and says so in the same sentence. The 0.93 return and the 50–100 MPa stress are presented as inputs, and the 100 MPa is not marked as a near-failure value. That is a labelling weakness, not a measured-versus-derived defect.

## 5. Scope of my searches

I ran three web searches (standard mode) on:
- Ker 1981
- Bennett et al. 1986 and tendon tensile strength
- fish fast-muscle isometric stress

I read none of these papers in full; every source above is search-summary.

Not found: a measured working stress, fracture stress or hysteresis for **any teleost tendon or myoseptum**, and an isometric stress for zebrafish muscle. Both are **unknown** here. I found no published teleost counter-example in which a locomotor tendon stores launch-scale energy, which is consistent with S29's own negative search.

## Corrected statement

The calculation gives 1.8–4.1 % of body volume as mammal-grade tendon at a 50–75 MPa working stress (1 % only at ~100 MPa, i.e. fracture). For fish tendon at 2 % strain with fish-measured 7–25 % dissipation, it gives 13–30 %. All of these are ×1.6 at the mass-consistent 5.53 m/s.

The volume is necessary but not sufficient: a directly loaded series tendon of that volume would be 4–29 body lengths long. "Spring volume passes" holds for mammal-grade tendon as a material-volume bound only. It is not shown for fish-grade tendon, and packaging is not shown at all.

## Sources

- [Ker 1981, J. Exp. Biol. 93:283](https://cob.silverchair.com/jeb/article/93/1/283/23085/Dynamic-tensile-properties-of-the-plantaris-tendon) (search-summary)
- [Ker, Alexander & Bennett 1988, "Why are mammalian tendons so thick?"](https://scilit.com/publications/947184a0fabd160c17d11a667bed1e6a) (search-summary)
- [Bennett et al. 1986, J. Zool. 209:537](https://scilit.net/publications/79ad668b20bca34e7d69988121ba05f5) (listing only; no abstract available, so no number taken from it)
- [Altringham & Johnston 1982, J. Physiol.](https://openpolar.no/Record/crwiley:10.1113%2Fjphysiol.1982.sp014462) (search-summary)

```swarm-challenge
{"claim_id": 225, "outcome": "weakened", "reason": "Arithmetic reproduces exactly, but the 1% end uses ~fracture stress (100 MPa), the fish-tendon rows assume mammalian 0.93 return despite the cited 7-25% fish dissipation, and volume is a proxy: a directly loaded series tendon of that volume would be 4-29 body lengths long.", "corrected_value": "1.8-4.1 % body volume (mammal tendon at 50-75 MPa working stress); 13-30 % (fish tendon, 2% strain, 0.75-0.93 return); x1.6 at the mass-consistent 5.53 m/s target", "depends_on": ["S29 stored energy 11.83 mJ (central case)", "S29 body 0.40 g at 1050 kg/m3", "Ker 1981 E 1.65 GPa and ~75 MPa peak locomotor stress (search-summary)", "Ker Alexander Bennett 1988 tendon fracture ~100 MPa, typical ~13 MPa (search-summary)", "Shadwick tuna tendon E 0.65-1.2 GPa, 2% burst strain, 7-25% dissipation (via S29, abstract)", "Altringham & Johnston 1982 cod fast fibre 186 kPa isometric stress (search-summary)", "S28 frontal area 24 mm2 and body length 3.0 cm", "S28 mass-consistent target 5.53 m/s"]}
```
