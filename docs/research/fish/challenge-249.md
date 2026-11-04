# Challenge 249: the harvester's recompute of S25-D's fin-ray EI range

Target: claim 249. This is the harvester's recompute of S25-D, from branch
`claude/deepen-flammang-fin-ray-stiffness-vvpk2v`, file `S25-deepen.md` (read at full text, commit 96cf498).
Recorded value: 1.35e-5 N m², tagged "derived", for a load at L/2.
Date: 2026-11-04.

## Verdict: WEAKENED

The harvester is right that S25-D's 13–105× range is wrong. Its own recorded value is the wrong row, though.

- **Where the harvester is right.** S25-D used the wrong beam model.
- **Where the harvester is wrong.** It recorded the L/2 row. The paper gives the load point as about 2L/3.

At the quoted load point, with deflection measured at the tip, the calculated clamped EI is
**2.24e-5 N m²**. That puts 565e-6 about **25×** above it. It is not 1.35e-5, and it is not 42×.

## 1. Independent arithmetic (calculated, not observed)

Inputs: k = 1.98 N/m and L = 40.3 mm. I used two uniform Euler–Bernoulli cantilever models:

- **Deflection read at the load point a:** EI = k a³ / 3. This is S25-D's model.
- **Deflection read at the tip, with the load at a:** EI = k a² (3L − a) / 6. This is the harvester's model.

| a | EI, load-point model | 565e-6 ÷ EI | EI, tip model | 565e-6 ÷ EI |
|---|---|---|---|---|
| L/3 | 1.60e-6 | 353× | 6.40e-6 | 88× |
| L/2 | 5.40e-6 | 105× | 1.35e-5 | 42× |
| **2L/3 (quoted)** | 1.28e-5 | 44× | **2.24e-5** | **25×** |
| L | 4.32e-5 | 13.1× | 4.32e-5 | 13.1× |

Every number in the claim reproduces under the model it was computed with:

- 4.32e-5 and 13.1× reproduce.
- 1.35e-5, 2.24e-5 and 6.4e-6 reproduce under the tip model.
- S25-D's 5.4e-6 and 1.28e-5 reproduce under the load-point model.

So the disagreement between the two documents is not arithmetic. It is about **which displacement Alben et al.
measured**. The harvester did not diagnose this. It wrote that S25-D's lower end "corresponds to a ~L/3 load". That
is only true when 5.4e-6 is read through the tip model. Under S25-D's own model, 5.4e-6 is exactly the L/2 value.

## 2. Hidden assumption: where the deflection was measured

The harvester had not read the Alben paper, so I went to it.

Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243, PMC2359861. Read-level: **full-text via an automated page
summarizer** (WebFetch of pmc.ncbi.nlm.nih.gov). The Europe PMC fullTextXML endpoint returned HTTP 500 this session.

Quoted, as returned:

- "the force on the probe is measured as a function of **tip deflection** of the ray"
- "a vertical point force is applied at two-thirds of the distance from the ray base to the tip"
- "The ray is clamped horizontally at the base"

**My inference from these quotes:** the tip model at a = 2L/3 is the model the paper describes. Two consequences
follow:

- S25-D's load-point model **underestimates** EI. Its lower end of 5.4e-6 and its midpoint of 1.28e-5 do not
  describe this test.
- Bracketing a over L/2 to L is wider than the text supports. The text gives "about two-thirds".

Caveat: a summarizer produced this quote. I could not verify the words "tip deflection" against the XML or a PDF.

## 3. Proxies and inputs that are still soft

- **L = 40.3 mm is the group's maximum ray length.** Per the summarizer, it is not the length of the tested ray. The
  tested ray is probably ray 4, but its length is **unknown**. EI scales as L³ when a/L is fixed. For example, a
  35 mm ray gives 1.47e-5 N m² at 2L/3 tip (calculated), which is 38× below 565e-6. The multiple only rises for a
  shorter ray. A longer ray than the group maximum is unlikely.
- **Uniform beam.** Real rays taper, so they are stiffer near the base. A tapered ray gives a smaller apparent EI
  than a uniform beam would for the same k. I did not quantify this.
- **Base compliance.** Compliance at the base would lower k, which means EI could be higher than calculated. Its
  size is unknown. Neither document measured it.

## 4. Counter-evidence and tension inside the source

- Alben 2007's three-point-bending result is EI ≈ 10⁻⁶–10⁻⁵ N m² (quoted, summarizer). The cantilever-derived
  2.24e-5 sits **above** that range. This is a disagreement between two methods in the same paper, and I leave it
  unresolved.
- On either reading, 565e-6 is still 25–56× above both methods. The S25-D conclusion that 565e-6 should not be
  carried as a single ray's EI **survives**.
- How 3.8e-6 fits is now subtler (calculated):
  - It sits below the clamped tip-model value at 2L/3 (2.24e-5, a ratio of 0.17).
  - It sits above the one-hemitrich-free value (2.24e-5 ÷ 12 = 1.87e-6, a ratio of 2.0).
  - So it lies between the two clamping states and within an order of magnitude of both. That is consistent, but it
    is not "inside the envelope" in S25-D's sense.

## 5. Evidence level

"Derived" is honest. The value is a calculation from a measured slope, and no one presents it as measured. The
**label** is the problem. Calling 1.35e-5 the "mid" of the range, and saying it is "within 5%" of S25-D's 1.28e-5,
compares a tip-model L/2 value with a load-point-model 2L/3 value. The 5% agreement is a coincidence of two errors
roughly cancelling.

## Corrected statement

The cantilever EI of a bluegill pectoral ray, calculated from Alben 2007's k = 1.98 N/m (both hemitrichs clamped),
is about **2.2e-5 N m²**. This takes:

- the load at the quoted 2L/3;
- the deflection at the tip, as the paper describes it;
- L = 40.3 mm, which is the group maximum, so the EI is an upper estimate for a shorter ray.

The clamped range for the load point anywhere from L/2 to L is 1.35e-5 to 4.3e-5 N m². That makes 565e-6 about
**25×** too stiff, within a range of 13–42×. The harvester's range is right. Its recorded point value is not.

Flammang 2013's own method is still **unknown** (body text not read, here or upstream).

## Sources

| Source | Read-level |
|---|---|
| S25-deepen.md, branch `claude/deepen-flammang-fin-ray-stiffness-vvpk2v` | full-text |
| Alben, Madden & Lauder 2007, PMC2359861 | full-text via automated summarizer; Europe PMC XML HTTP 500 |
| Flammang et al. 2013 | not accessed this session |

```swarm-challenge
{"claim_id": 249, "outcome": "weakened", "reason": "Alben 2007 measured tip deflection with the load at ~2L/3, so the harvester's tip-deflection model and its 13-42x range are right, but its recorded value takes the L/2 row; at the quoted load point the calculated clamped EI is 2.24e-5 N m^2 (565e-6 is ~25x higher), and its 'mid within 5%' match to S25-D's 1.28e-5 is a coincidence of two different models.", "corrected_value": "2.24e-5 N m^2 (calculated; clamped, load at 2L/3, tip deflection, L = 40.3 mm)",
  "depends_on": ["Alben, Madden & Lauder 2007 PMC2359861 (full-text via summarizer): k = 1.98 N/m both hemitrichs clamped, load ~2/3 along the ray, force measured vs tip deflection", "Alben 2007: L = 40.3 mm is the group maximum ray length; tested ray length unknown", "Uniform Euler-Bernoulli cantilever, tip deflection under load at a: EI = k a^2 (3L - a)/6", "Base compliance assumed negligible (unmeasured)", "Flammang 2013 abstract value 565e-6 N m^2 (abstract read-level, upstream)", "Alben 2007 three-point bending EI ~1e-6 to 1e-5 N m^2 (summarizer; exponents reconstructed)"]}
```
