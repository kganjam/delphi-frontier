# Replication of claim 171 (S10-D-D): improved pectoral-muscle fraction f and the S10-D burst verdict

**What I read and what I avoided.** I read the parent derivation S10-D
(`docs/research/fish/S10-deepen.md` and `S10_deepen_calc.py` on branch
`claude/deepen-s10-flapping-muscle-wr33g7`) to get the model and the old inputs. I did **not** open the
claim's own working (`docs/research/fish/S10-D-deepen.md` and `S10-D-deepen_calc.py` on
`claude/deepen-s10-sensitive-input-k9dp4p`). I only listed that those two files exist.

One caveat on independence: the task prompt itself states the claimed numbers (f 0.014–0.028,
central ~0.016, ×5.4→×4.6, ×2.7, 0.15–0.21 W/kg, 10.1 W/kg, 48–67×, ×2.7–14.5). I could not
avoid reading them. I re-derived each one from primary sources and my own arithmetic.

All requirement numbers below are **calculations** (S10's Rankine–Froude hover model). None of them
is an observation.

---

## 1. Model (taken from S10-D, recomputed by me)

P_body = M · k · √(W³ / (2ρπR²)) / m, with W = m·g, k = 1.2, ρ = 1.2 kg/m³, m = 0.4 g.

The requirement per kg of flight muscle is P_body / f.

| Geometry | P_body, W/kg body (computed) | f at which 134.4 W/kg fast muscle just suffices (computed) |
|---|---|---|
| R = 4 cm, M = 1.5 (generous) | **10.07** | 0.0749 |
| R = 4 cm, M = 2.0 | 13.43 | 0.0999 |
| R = 2 cm, M = 1.5 | 20.14 | 0.1499 |
| R = 2 cm, M = 2.0 (realistic) | 26.86 | 0.1998 |

- **Sensitivity.** P_muscle ∝ M · m^½ / (R · f). Doubling or halving any one of R, M or f moves the requirement by exactly ×2. In S10-D's table the burst verdict did not flip for any of them.
- **The tie.** "Tied for sensitivity" holds for R, M and f, since all enter with exponent ±1. Muscle power is tied with them too, because the verdict is a ratio. Body mass enters as m^½ and is weaker.
- **I agree with the premise** that f is the weakest by evidence. In S10 it was an assumption; in S10-D it became a single proxy species read through a secondary compilation.

## 2. Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| *Abudefduf saxatilis*, sum of four pectoral muscles (abductors and adductors, superficial and profundus) | 0.69 % body mass per fin, so 1.38 % for both fins | Mansuit & Herrel 2021, *Front Ecol Evol* 9:702576, Table 1, as quoted in S10-D | listing (I did not re-read it; I am carrying S10-D's full-text read) |
| Zebrafish adult pectoral fin muscles: **seven** (arrector ventralis, arrector-3, arrector dorsalis, abductor superficialis, abductor profundus, adductor superficialis, adductor profundus). No masses given. | count = 7 | Siomava N & Diogo R (2017/2018) *J Anat*, PMC5770327 | full-text (Table 1, via fetch summary) |
| Bluegill pectoral girdle muscle masses, Table 2 (N = 5, body mass 141.4 ± 12.6 g) | abductor superficialis 0.32 %; abductor profundus 0.19; arrector ventralis 0.15; adductor superficialis (posterior dorsal) 0.13; adductor superficialis (ventral) 0.07; adductor profundus 0.34; arrector dorsalis 0.05; adductor radialis 0.05; **total 1.28 ± 0.08 %** | Jones EA, Lucey KS, Ellerby DJ (2007) *J Exp Biol* 210:3422–3429 | full-text (journals.biologists.com page, via fetch summary; Table 2 reproduced) |
| Bluegill in vitro work-loop power of the two largest muscles at 2.8 Hz | 16.5 ± 2.4 W/kg muscle | Jones et al. 2007 | full-text. A SICB abstract gives 14.9 ± 2.4 W/kg pooled (search-summary). **The two values disagree, and I have not reconciled them.** |
| Bluegill "available" mechanical power during maximal labriform swimming | 0.15–0.21 W/kg body | Jones et al. 2007 | full-text |
| Larval zebrafish fast muscle | 134.4 W/kg | Mead et al. 2020 via S10 | carried over from S10 (not re-read) |

**Bluegill figure: author's claim versus my check.**

- *Author's claim:* 0.21 W/kg body is 16.5 W/kg muscle × 1.28 % (all girdle muscle). 0.15 W/kg body is 16.5 × 0.92 % (the authors' "power-producing" subset).
- *My arithmetic:* 16.5 × 0.0128 = 0.211, and 16.5 × 0.0092 = 0.152. The numbers reproduce.
- *My inference:* "measured" overstates this figure. It is a **calculation** that combines measured in vitro power with measured muscle mass. It is not an in vivo power measurement. It is independent of the *zebrafish* f, but it does depend on the *bluegill* muscle fraction.

**Unresolved ambiguity (my inference).** Jones et al. do not say whether Table 2 covers one side or both. The total, 1.816 g / 141.4 g = 1.28 %, is consistent with either reading. If the table is one side, both sides would come to 2.56 % and the power figure would double to about 0.30–0.42 W/kg body.

## 3. Re-derivation of the improved f

1. The four muscle groups in the Abudefduf proxy correspond in bluegill to abductor superficialis + abductor profundus + adductor superficialis (both parts) + adductor profundus.
   - Their sum is 0.32 + 0.19 + 0.13 + 0.07 + 0.34 = **1.05 %**.
   - The table total is 1.30 % (rows summed); the paper states 1.28 %.
   - So the four-group proxy captures **81 %** of girdle muscle in bluegill (calculation).
2. The two largest bluegill muscles are (0.32 + 0.34) / 1.30 = **51 %** of girdle muscle. This reproduces the claim's "the two largest are half the girdle muscle".
3. Correcting the Abudefduf four-muscle sum by the bluegill composition: 0.0138 / 0.81 = **0.0171**. My **central f is about 0.017**.
4. The bluegill direct value, both-sides reading, is **0.0128**. It is a labriform fish, so it is plausibly generous for zebrafish, which is my inference.
5. The upper bracket depends on assumptions:
   - If bluegill Table 2 is one side only, f = 0.0256.
   - If one assumes, as the claim's upper end seems to, that the four-muscle sum is only half the system, f = 0.0138 / 0.5 = 0.0276. The bluegill table does not support that assumption: the four groups are 81 % there, not 50 %. This is my inference.

**My f: 0.013–0.026, central ~0.017.**

The upper end rests only on the unresolved one-side reading of Jones et al. Zebrafish's own fraction remains `unknown`. I did one search for the seven zebrafish muscles and found no masses. I did not search micro-CT repositories.

## 4. Recomputed burst shortfall (calculation)

The shortfall is (P_body / f) / 134.4 = f_threshold / f.

| f | Generous geometry (threshold 0.0749) | Realistic geometry (threshold 0.1998) | Requirement, W/kg muscle (generous) |
|---|---|---|---|
| 0.0128 (bluegill, both sides) | ×5.85 | ×15.6 | 787 |
| 0.0138 (S10-D) | ×5.43 | ×14.5 | 730 |
| 0.016 | ×4.68 | ×12.5 | 629 |
| **0.0171 (my central)** | **×4.4** | **×11.7** | 590 |
| 0.0256 (one-side reading) | ×2.93 | ×7.8 | 393 |
| 0.028 | ×2.67 | ×7.1 | 360 |

**f-independent hover check (calculation).** Using Jones et al.'s figure, 10.07 / 0.21 = **47.9×** and 10.07 / 0.15 = **67.1×** short. If the one-side reading holds, the gap would be about 24–34×, still far short.

## 5. My value

- **Improved f:** 0.013–0.026, central ~0.017 (pectoral muscle mass as a fraction of body mass).
- **Generous burst shortfall:** narrows from ×5.4 to **×4.4** at the central f, with a range of ×2.9–×5.9. It does not close.
- **Sustained hover:** the requirement is 10.1 W/kg body, against the bluegill estimate of 0.15–0.21 W/kg body. That is **48–67× short**, or about 24–34× under the one-side reading.
- **Revised enlargement factor:** about **×2.9–15.6** (generous high-f to realistic low-f). S10-D's verdict stands: sustained flapping is not supported, and burst flapping is not supported with present anatomy.

## 6. Comparison with the recorded value (from the task prompt only)

| Quantity | Claim | Mine | Agreement |
|---|---|---|---|
| f | 0.014–0.028, central ~0.016 | 0.013–0.026, central ~0.017 | central and range agree within rounding |
| Generous shortfall at central f | ×4.6 | ×4.4 | agree (difference is from central f) |
| Shortfall at upper bracket | ×2.7 | ×2.9 | agree (difference is from upper f) |
| Hover gap | 48–67× | 47.9–67.1× | agree exactly |
| Enlargement factor | ×2.7–14.5 | ×2.9–15.6 | agree |

On the enlargement factor, the claim keeps S10-D's ×14.5 at the realistic end. That corresponds to f = 0.0138, below the claim's own revised range. Its revised range would give a realistic end of about ×12.5. This is a minor internal inconsistency, not a change of verdict.

Two minor disagreements:

1. The claim's upper f of 0.028 seems to rest on "half the girdle muscle". In bluegill that fraction applies to the *two* largest muscles. The *four*-group sum that the Abudefduf proxy uses is 81 %. On my reading, the defensible upper bracket comes instead from the one-side ambiguity in Jones et al., and it lands at almost the same number.
2. Calling the bluegill 0.15–0.21 W/kg "measured" overstates it. It is calculated from measured in vitro power and measured muscle mass.

**Verdict: AGREE** on the value and on S10-D standing. I flag the basis of the upper bracket and the "measured" wording.

## Sources

- Jones EA, Lucey KS, Ellerby DJ (2007) Efficiency of labriform swimming in the bluegill sunfish (*Lepomis macrochirus*). *J Exp Biol* 210:3422–3429. https://journals.biologists.com/jeb/article/210/19/3422/17090/Efficiency-of-labriform-swimming-in-the-bluegill — **full-text** (via a fetch tool's summary, with Table 2 reproduced; not read by eye)
- Siomava N, Diogo R (2017) Comparative anatomy of zebrafish paired and median fin muscles. *J Anat*. https://pmc.ncbi.nlm.nih.gov/articles/PMC5770327 — **full-text** (via fetch summary)
- Mansuit R, Herrel A (2021) *Front Ecol Evol* 9:702576 — **listing** for me (values taken from S10-D's full-text read)
- SICB abstract, "Mechanical power output of the pectoral fin abductor and adductor muscles of the bluegill sunfish". https://sicb.org/?p=29961 — **search-summary** (14.9 W/kg)
- Mead et al. 2020 (134.4 W/kg) — carried over from S10/S10-D, not re-read
- pubmed.ncbi.nlm.nih.gov — **could-not-access** (host not resolvable from this session)

```swarm-replication
{"claim_id": 171, "my_value": "f = 0.013-0.026 (central ~0.017) of body mass; generous burst shortfall x4.4 (x2.9-5.9); hover 10.07 W/kg body vs 0.15-0.21 W/kg body = 48-67x short; enlargement ~x2.9-15.6", "agrees": true,
  "note": "Independent re-derivation from Jones et al. 2007 Table 2 and Siomava & Diogo 2017 reproduces the central f, the narrowed-but-open burst gap and the 48-67x hover gap; the claim's 0.028 upper bracket is better justified by the unresolved one-side/both-sides ambiguity than by 'half the girdle', and the bluegill power is calculated rather than measured."}
```
