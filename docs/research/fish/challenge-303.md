# Challenge 303: adversarial review of S29-D-D (the spring-release chain efficiency)

**Claim under review** (S29-D-D, branch `claude/deepen-s29-sensitive-input-fyqige`,
`docs/research/fish/S29-D-deepen.md` and `S29-D-deepen_calc.py`, both read in full):

> S29-D's conclusion is most sensitive to the spring-release chain KE_exit/E_stored. A 1.96× error
> restores the all-muscle break-even. Watts 2006 widens the chain to 0.10–0.158 for peak KE. That
> keeps the one-side shortfall at 3.8–6.0× and the all-muscle case 1.24–1.96× short, so S29-D
> stands. But a servo-driven robot (~12 %) removes S29-D's mechanistic reason.
> Recorded evidence level: **measured**.

**Outcome: WEAKENED.** The arithmetic is correct. Three things are not:

1. The recorded evidence level is wrong.
2. The 0.158 upper bound is probably mislabelled. It is likely a best-trial value, not a
   correction from mean speed to peak speed.
3. "S29-D stands" on break-even rests on an unmeasured transfer assumption. At the 0.158 end that
   assumption flips if the robot lost only about 25 % of its stored energy inside its own body.

The servo-robot clause is also overstated.

Everything below marked *calculated* is my own arithmetic. This review measured nothing.

---

## 1. Arithmetic, redone independently

I recomputed from the stated inputs: V = 4.37 m/s, ½V² = 9.548 J/kg, f = 0.30 / 0.60,
w = 32 / 53 / 81 J/kg, and shortfall = ½V² / (f · w · chain). I did not reuse the author's script.

| Quantity | Mine (calculated) | Claim |
|---|---|---|
| Central shortfall at 0.10, f 0.30, w 53 | 6.005 | 6.01 ✓ |
| All-muscle shortfall at 0.10, f 0.60, w 81 | 1.965 | 1.96 ✓ |
| Flip chain for all-muscle break-even | 0.1965 | 0.196 ✓ |
| 0.11 × (0.96/0.80)² | 0.1584 | 0.158 ✓ |
| One-side shortfall at 0.158, w 53 | 3.79 | 3.8 ✓ |
| All-muscle shortfall at 0.158, w 81 | 1.240 | 1.24 ✓ |

No arithmetic error found.

**A wording point on "most sensitive".** The chain is *tied* with w and f, not uniquely the most
sensitive input. All three have elasticity −1. For example, the all-muscle break-even also returns
if w reaches 159 J/kg, the same 1.96× factor. The source document says the three are tied and
gives a judgement for singling out the chain. The one-line claim drops that. This is minor.

## 2. Proxy check: what the 0.96 / 0.80 m/s pair actually is

The claim treats the pair as "peak vs averaged velocity". It builds the 0.158 upper bound on the
reading "if the 11 % used averaged velocity, the peak-KE chain is 0.11 × 1.44".

I re-searched the Watts 2006 thesis record. Read level: **search-summary**. The DSpace record
(1721.1/39203) and the Calhoun record were listed but not opened; the hosts are outside this
session's allowlist. The summary gives the wording as:

> "Peak and averaged maximum velocity was calculated at 0.96 m/s and 0.8 m/s, respectively."

**My inference, not the thesis's statement.** "Averaged *maximum* velocity" most naturally means
the *mean over trials of each trial's maximum*. The 0.96 m/s would then be the best single trial.
On that reading:

- Both figures are **peak** speeds. The 1.44 factor is trial-to-trial scatter, not a difference
  between peak and time-averaged KE.
- 0.158 is then the **best-trial** chain, valid only if E_stored was the same in every trial.
  E_stored per trial is `unknown`.
- It is not a correction toward S29's quantity. The defensible peak-KE value for a *typical*
  release would be 0.11 (or 0.10, Conte).

This does not break the claim's conclusion. 0.158 is still below 0.196 whichever way it is read.
But the claim's label for the upper end ("0.158 for peak KE") likely names the wrong thing. On the
likely reading, the range is 0.10–0.11 typical and ≤ 0.158 best case.

This interpretation is unconfirmed. The thesis full text is `could-not-access`.

## 3. The hidden assumption that carries "S29-D stands": transfer from robot to zebrafish spring

Every number in the claim's range is a **whole-device** ratio. It includes loss inside the robot's
own body: hysteresis in the urethane rubber body and in the beam. S29 needs the chain for a
zebrafish axial spring. S29 itself takes tendon return to be 0.93 (Ker 1981, via S29).

The claim's `depends_on` lists, as an ASSUMPTION, that neither robot's efficiency is dominated by
material loss. Neither source separates material loss from hydrodynamic loss: `unknown`, as the
author also records.

**Relaxing the assumption** (calculated). Suppose the robot lost a fraction x of its stored energy
internally, and the zebrafish spring loses only 7 %. Then the zebrafish chain is
c · 0.93 / (1 − x), and the all-muscle break-even (≥ 0.1965) returns when:

| Robot chain c | Robot internal loss x that restores the break-even |
|---|---|
| 0.10 (Conte) | ≥ 53 % |
| 0.11 (Watts, as reported) | ≥ 48 % |
| 0.158 (Watts, the claim's upper end) | **≥ 25 %** |

- **At the claim's own upper bound, a 25 % internal loss in a urethane-bodied robot is enough to
  undo "break-even gone".** That loss is unmeasured, and I have no measured hysteresis figure for
  this urethane. I am not supplying one.
- At the central 0.10 the loss would need to be about half, which is less likely but not excluded.
- S29-D-D's own §6 is calculated. It shows that S29's 0.323 would need 54–71 % internal loss, so
  the author knew this axis existed. The headline, however, presents "nothing found reaches 0.196"
  as closing the question. **It closes it only for whole-device ratios, not for the
  tendon-spring quantity S29 needs.**

The author's sentence "nothing found reaches 0.196" is literally true. My inference is that it does
not support the verdict "break-even gone" without the material-loss assumption. That assumption has
no evidence either way.

## 4. Evidence level

- **The ledger records the claim as "measured".** That is a defect. The S29-D-D document correctly
  labels itself "derived".
- Every shortfall, flip point and the 0.158 figure are **calculated** by S29-D-D.
- The 0.10 is itself "calculated" by Conte et al. from measured acceleration (abstract). S29-D-D
  correctly caught and corrected S29-D's "MEASURED" label for it.
- Watts 11 % and Feng ~12 % are at **search-summary** read level.
- **The correct evidence level is "derived"**, from literature values at abstract and
  search-summary level.

## 5. The servo-robot clause: a counter-quantity, not a counter-example

The claim says the Feng 2011 servo robot "removes S29-D's mechanistic reason". My re-search
(search-summary only; DSpace, core.ac.uk and meetings.aps.org could-not-access) found:

- **The 12 % may not be from the paper itself.** It appears to come from a related 2011 APS DFD
  abstract (Modarres-Sadeghi, Feng, Bonafilia, Costain), which calls it a **"hydrodynamic
  efficiency"**. The search did not surface an efficiency number from the IMECE paper's own
  abstract.
- **The two sources disagree on acceleration:** 2.0 m/s² (DSpace abstract) versus about 4 m/s²
  (APS abstract). I am keeping both.
- **The regime is different.** Peak speed was 0.09 m/s and acceleration 2–4 m/s². That is 10–20×
  below Conte's 40 m/s², and roughly 100× lower in KE per unit mass. It is not a fast start in the
  sense S29 needs.
- **The denominator is `unknown`.** If it is electrical or servo input, the ratio from mechanical
  work to KE is *higher* than 12 %, because motor losses sit in the denominator. That would make
  active drive *better* than the spring devices, which is S29-D's mechanism, not a refutation of
  it. If it is a Froude-type hydrodynamic efficiency, it is a different quantity from
  KE_exit/E_stored altogether.

The S29-D-D document itself calls this "a weak inference" that moves no number. The one-line claim
upgrades it to "removes". **Correct wording:** the Feng value *does not support* S29-D's mechanism
and does not refute it either. S29-D's passive-release explanation remains untested.

## 6. Counter-examples searched

- 2 standard web searches in this pass, covering the Watts 2006 record and the Feng 2011 record.
- 3 fetch attempts, all could-not-access (host not allowlisted): core.ac.uk, meetings.aps.org,
  absimage.aps.org.
- Not found: any spring-released or latch-released body with KE_exit/E_stored ≥ 0.196, or any
  in-air material-loss measurement for the Conte/Watts device. Both are `unknown`. The scope is
  limited to these searches plus the author's documented scope.

## 7. Verdict

| Part of claim | Status |
|---|---|
| Arithmetic (6.01, 1.96, 0.196, 0.158, 3.79, 1.24) | **Survives**, recomputed independently |
| "Most sensitive" | Tied with w and f, not unique (minor) |
| Upper end 0.158 is "peak KE" | **Likely mislabelled.** It is probably the best-trial value, conditional; the typical value is 0.10–0.11 |
| "S29-D stands" (break-even gone) | **Conditional.** It holds for whole-device ratios. It flips if robot internal loss is ≥ 25 % (at 0.158) or ≥ 53 % (at 0.10), which is unmeasured |
| Servo robot "removes" S29-D's mechanism | **Overstated.** Different regime, different or unknown quantity. It neither supports nor refutes |
| Recorded evidence level "measured" | **Wrong.** It should be derived |

## Sources

| Source | Read level | Used for |
|---|---|---|
| S29-D-D doc and script (`claude/deepen-s29-sensitive-input-fyqige`) | full-text | the claim and its inputs |
| S29-D doc (`claude/s29-deepen-launch-energy-0r1gju`) | full-text (passages on mechanism) | S29-D's passive-release argument |
| Watts 2006 MIT/WHOI thesis, DSpace 1721.1/39203 | search-summary | "peak and averaged maximum velocity 0.96 / 0.8 m/s"; 11 % |
| Feng et al. 2011, IMECE2011-65035, DSpace 1721.1/120737 | search-summary | servo drive; 2.0 m/s², 0.09 m/s |
| Modarres-Sadeghi, Feng, Bonafilia, Costain, APS DFD 2011 abstract | search-summary | "hydrodynamic efficiencies around 12 %"; about 4 m/s² |
| Conte et al. 2010, *Bioinspir. Biomim.* 5:035004 | search-summary (this pass); abstract per author | about 10 %, 40 m/s², 1.2 m/s |

```swarm-challenge
{"claim_id": 303, "outcome": "weakened", "reason": "Arithmetic reproduces exactly, but the recorded evidence level 'measured' should be 'derived'; the 0.158 upper bound is more likely a best-trial value (Watts's 0.8 m/s is an 'averaged maximum', i.e. trial-mean of peaks) than a peak-vs-mean KE correction; 'break-even gone' holds only for whole-device robot ratios and flips if the robot lost >=25% (at 0.158) or >=53% (at 0.10) of stored energy internally, which is unmeasured; and the ~12% servo robot (0.09 m/s, 2-4 m/s^2, 'hydrodynamic efficiency', denominator unknown) neither removes nor supports S29-D's passive-release mechanism.", "corrected_value": "spring-release chain KE_exit/E_stored 0.10-0.11 typical, <=0.158 best-trial (derived from abstract/search-summary literature values, not measured); break-even flip 0.196, reachable if robot internal material loss >=25-53% (unknown)", "depends_on": ["S29-D-D shortfall formula 0.5*V^2/(f*w*chain) and inputs V 4.37 m/s, f 0.30/0.60, w 32/53/81 J/kg (via S29)", "Watts2006 thesis 'peak and averaged maximum velocity 0.96 and 0.8 m/s', efficiency 11% (search-summary)", "Conte2010 KE_final/E_stored ~0.10, 'calculated' (abstract via author; search-summary here)", "Ker1981 tendon return 0.93 (via S29) for the material-loss transfer calculation", "ASSUMPTION (mine): 'averaged maximum' means trial-mean of per-trial peaks", "ASSUMPTION (S29-D-D, relaxed here): robot internal material loss is small; actual value unknown", "Feng2011 IMECE / Modarres-Sadeghi 2011 APS abstract: servo-driven, 0.09 m/s, 2.0 vs ~4 m/s^2, 'hydrodynamic efficiency ~12%', denominator unknown (search-summary)"]}
```
