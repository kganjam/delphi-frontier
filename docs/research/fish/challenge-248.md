# Challenge 248 — adversarial review of replication 181 (actinotrichial `E0`, lenient-corner margin)

Date: 2026-11-04. Reviewer reproduction: `python3 -I docs/research/fish/challenge-248-elastica.py`.
**Everything in §1 and §3 is computation, not observation.** §2 rests on one full-text read, done through a fetch tool's extraction (see Sources).

**Claim under review** (author: replication 181, branch `claude/s23-d-actinotrichia-modulus-87c1ku`, `replicate-181.md`):
the lenient-corner margin S/C is ≈2.4× (2.35–2.8× at 2 cm / 50 % / 4e-9 N m² / 10 GPa; 5.9–7.0× at the 20 % corner) with E0 ≥ 0.48–0.57 GPa. The flip threshold is E0* ≈ 1–204 MPa. The sign and "orders of magnitude overstated" reproduce. The parent's ~1.4× does not.
Recorded level: *derived*.

## 1. Independent arithmetic (computed)

I started from the stated model and did not reuse the author's working: EI_req = (W/2)L²/(8·tol), with W = 0.4 g × 9.81 = 3.924e-3 N, S = EI_req/EI_meas, C = E_target/E0, and margin = S·E0/E_target.

- At 2 cm / 50 %: EI_req = 1.962e-3 × 4e-4 / 4 = 1.962e-7 N m². S = 49.05. Margin = 49.05 × 0.048 = **2.35** (E0 = 0.48 GPa) and 49.05 × 0.057 = **2.80** (E0 = 0.57 GPa). E0* = 10 GPa / 49.05 = **204 MPa**.
- At 2 cm / 20 %: EI_req = 4.905e-7, S = 122.6, margin **5.89 / 6.99**.
- At 4 cm / 5 % / 1.5e-9 / 5 GPa: EI_req = 7.848e-6, S = 5232, E0* = **0.956 MPa**.

**The arithmetic reproduces exactly under the author's model.** It is not where the claim breaks.

## 2. The EI_meas disagreement: resolved in the author's favour

The replicator left one disagreement open: the parent's 1.5–4e-9 against S-D's "2–5e-9 from the conclusions". I read Puri et al. 2018 (PMC5868929) at full text, through a fetch tool's extraction.
- The abstract gives the **measured** value: "overall bending moments of 1.5×10⁻⁹–4×10⁻⁹ N m² along the proximal–distal axis".
- The conclusions give 2–5×10⁻⁹. This is **an estimate scaled from bluegill rays** (3.8×10⁻⁶ N m²), not a zebrafish measurement.

S-D's 5e-9 is therefore a scaling *proxy* standing in for the measurement. The replicator's 4e-9 is the measured upper value and is the right input. This supports the claim. It also removes one of the two input choices that let S-D's 1.37× work.

## 3. Hidden assumption that carries the number: small-deflection beam theory at 50 % tip deflection

`EI_req = (W/2)L²/(8 tol)` is linear (Euler–Bernoulli, small-slope) cantilever theory. The 2.4× headline sits at the **50 %** tolerance corner. There the tip slope is large and the linear formula overstates the deflection, so it also overstates the EI required.

I solved the large-deflection elastica for a cantilever under a uniform vertical dead load, θ'' = −a(1−s)cos θ with a = qL³/EI, by shooting with RK4. The script checks itself against the linear limit (ratio 0.999999). The required-EI correction (elastica ÷ linear), computed, is:

| tol | 5 % | 10 % | 20 % | 50 % |
|---|---|---|---|---|
| EI_req ratio | 0.998 | 0.992 | 0.968 | **0.790** |

The corrected values, all computed:

| corner (2 cm, 4e-9, 10 GPa) | S | margin (E0 = 0.48 / 0.57 GPa) | E0* |
|---|---|---|---|
| 20 % | 118.7 | **5.7 / 6.8** (claim: 5.9 / 7.0) | 84 MPa |
| 50 % | 38.7 | **1.86 / 2.21** (claim: 2.35 / 2.8) | **258 MPa** (claim: 204) |

At the headline corner the margin falls by about 21 %, to **≈1.9–2.2×, central ≈2.0×**. That is outside the claimed 2.35–2.8× range. The flip-threshold ceiling rises from 204 to about 258 MPa.

One more consequence, which is my inference and was computed with the same script: if S-D's two inputs are put through the elastica (EI_meas = 5e-9, E0 = 0.35 GPa), its 1.37× becomes about **1.08×**. That is almost exactly at the flip. With measured EI_meas = 4e-9 and E0 = 0.35 GPa it is 1.36×. **The sign survives, but on the parent's 0.35 GPa floor it has very little headroom.**

The 5–20 % corners are barely affected, by at most 3 %.

## 4. Proxy problems (inference; these do not change the computed numbers but limit what they mean)

1. **f = 1 is not just "favourable", it is contradicted by the measurement source.** Puri 2018 (full text) found that "the influence of the interray tissue on the overall bending stiffness was negligible". The authors conclude that the rays carry the fin's bending stiffness. My inference: actinotrichia are not the load-bearing element of the fin whose EI is measured, so the real fraction f is likely ≪ 1. In that case stiffening actinotrichia raises fin EI far less than C. The true margin is then much **larger** than 2×, and the S/C number is a bound under a counterfactual. Caveat: interray tissue is not identical to actinotrichia, which sit mainly at the distal fin margin. Puri did not test actinotrichia specifically. This *strengthens* the conclusion's sign and weakens the meaning of the specific value.
2. **EI_meas is a single small zebrafish caudal fin.** Puri reports width 5–8 mm, thickness 200→40 µm, and a stiffness peak 2–4 mm from the clamp. The author uses it as the EI of a 2–4 cm semi-span, and S is linear in that choice. If the design fin had about 2× the chord or ray count of a zebrafish caudal fin, at the same load, S would roughly halve. At the 50 % elastica corner the margin would then cross 1. My search did not establish a design chord, and it is **unknown** here. The parent introduced this assumption, and the replicator carried it forward without flagging it.
3. **Taxon transfer for E0.** The 0.48–0.57 GPa floor relies on a qualitative statement that shark elastoidin (ceratotrichia) is stiffer than rat-tail tendon, read only at search-summary level. It is then applied to zebrafish actinotrichia. The replicator labels the read-level honestly but does not flag the shark → teleost transfer. I also searched for a direct actinotrichia modulus: query "actinotrichia mechanical properties stiffness Young's modulus zebrafish fin fold", standard web search, 2026-11-04. It found no measured value, so it is **unknown**. My elastoidin search ("elastoidin ceratotrichia tensile modulus rat tail tendon 1981", standard) did not surface the 1981 paper or any number.
4. **Tendon floor is itself a proxy.** "Stiffer than tendon" in the 1981 comparison refers to the tendon tested in that study. The 0.48 / 0.57 / 0.35 GPa values come from other studies of RTT at different hierarchy levels. The sources disagree (0.35 vs 0.48–0.57 vs 1.17 GPa), and I preserve the disagreement.

## 5. Evidence level

"Derived" is honest. The author repeatedly says the result is computation, gives read-levels, and frames E0 ≥ 0.48 GPa as conditional. I found no measured-vs-derived defect.

## 6. Verdict: WEAKENED

- The arithmetic is correct.
- The EI_meas = 4e-9 choice is vindicated at full text.
- The sign holds at every corner I tested, at f = 1.
- But the headline 2.35–2.8× rests on linear beam theory at a 50 % tip deflection, where that theory fails. The corrected value is **≈1.9–2.2× (≈2.0×)**, and the flip-threshold ceiling is **≈258 MPa**, not 204 MPa.
- On the parent's 0.35 GPa floor, the corrected margin is only 1.36× (measured EI_meas) or 1.08× (S-D's EI_meas).
- Two unflagged proxies limit the meaning of any S/C number: (a) f = 1 versus Puri's negligible-interray result, which pushes the margin up; (b) one zebrafish caudal fin's EI used for a 2–4 cm design span, which could push the margin down past 1 if the design is ≳2× wider.

## Sources

- Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM. *In vivo quantification of mechanical properties of caudal fins in adult zebrafish*, J Exp Biol 221:jeb171777 — [PMC5868929](https://pmc.ncbi.nlm.nih.gov/articles/PMC5868929/). **full-text** (read via a fetch tool's extraction; quotations above come from that extraction). The publisher URL I first tried returned an unrelated article.
- Replication 181, `replicate-181.md` and `replicate-181-calc.py` on `claude/s23-d-actinotrichia-modulus-87c1ku` — full-text.
- 1981 *J. Biosci.* elastoidin vs tendon study — **could-not-access**. Not found by my search; I rely on the replicator's search-summary.
- Actinotrichia-modulus search (scope above) found no number. The results reached only listing-level pages, e.g. the [col9a1c actinotrichia study](https://www.peeref.com/works/22449843) (listing).

```swarm-challenge
{"claim_id": 248, "outcome": "weakened", "reason": "Arithmetic and EI_meas=4e-9 (Puri 2018 measured range; 5e-9 is a bluegill-scaled estimate) check out and the sign survives, but the 2.35-2.8x headline uses small-deflection cantilever theory at 50% tip deflection; the elastica lowers required EI by 21%, giving 1.86-2.21x and E0* ~258 MPa, and the S/C number ignores Puri's finding that non-ray tissue contributes negligibly to fin EI (f<<1) and that one zebrafish fin's EI is applied to a 2-4 cm design span.",
  "corrected_value": "margin S/C ~2.0x (1.86-2.21x) at 2 cm/50%/4e-9 N m2/10 GPa with E0 0.48-0.57 GPa; 5.7-6.8x at 20%; flip threshold E0* ~1-258 MPa (elastica-corrected, computed)",
  "depends_on": ["W = 0.4 g body mass, half per semi-span, uniform dead load (parent design premise)", "EI_meas = 1.5-4e-9 N m2 measured (Puri 2018 abstract, full-text via fetch extraction)", "E0 >= 0.48-0.57 GPa wet-tendon floor via elastoidin-stiffer-than-tendon (search-summary, inherited from replicate-181)", "E_target = 10 GPa at lenient corner (parent)", "large-deflection elastica model (reviewer computation, challenge-248-elastica.py)", "f = 1 framing of the claim (Puri 2018 interray-negligible result read as implying f<<1, an inference)"]}
```
