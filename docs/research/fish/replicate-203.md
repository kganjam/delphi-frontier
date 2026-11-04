# Replicate 203: "[S10] Sustained flapping is not supported"

**Method:** an independent re-derivation from primary sources, made without seeing the recorded answer. I read the recorded value (via `challenge-203.md` on branch `claude/fish-flapping-power-challenge-bquvmd`) only **after** §1–§3 below were finished. I did not read the harvest file `S10-tissue.md`.

## 0. A scope mismatch, found only after the derivation

The question I was given was the bare sentence "Sustained flapping is not supported". I took the subject to be **real flying fish (Exocoetidae)**. The recorded claim turned out to concern a **hypothetical 0.4 g flapping fish** (the zebrafish design in S10), in **hover**, with results expressed **per kg of flight muscle**. My derivation is therefore a test of the same physiological proposition on a different system:

> Can teleost pectoral muscle sustain the power that flapping flight needs?

It is **not** a re-computation of the recorded number. Once I had read the recorded inputs, I did not redo the 0.4 g case, because that would no longer be independent.

## 1. Inputs

| # | Input | Value | Source | Read-level |
|---|---|---|---|---|
| 1 | Maximum lift-to-drag ratio of a gliding flying fish (*Cypselurus hiraii*) | ~4.4 (wind-tunnel models, model 3) | Park & Choi, IUTAM 2007 conference paper (the precursor to Park & Choi 2010 *J Exp Biol* 213:3269, PMID 20833919) | **search-summary** (I could not fetch the PDF because the host was blocked). The 2010 abstract was read in full (**abstract**). It gives no number, but it does say that L/D peaks near 0° attack, that gliding performance is "comparable to hawk, petrel, wood duck", and that ground effect raises L/D. |
| 2 | Maximum L/D, CFD model of *C. hiraii* | 4.7 | Deng et al. 2019 *Bioinspir Biomim* 14:046009, PMID 31117061 | **abstract** |
| 3 | Flight speed of flying fish | 10–20 m/s ("in the region of") | A *J Exp Biol* paper that cites Hertel 1966, Fish 1990 and Davenport 1994 together | **search-summary** |
| 3b | Conflicting speed figure | ~8 m/s (30 km/h, the record 45 s glide) | Live Science, citing Guinness | **search-summary**. This figure disagrees with row 3, so I kept both and used 8 m/s as a generous lower bound. |
| 4 | Maximum mechanical power from pectoral muscle during maximal labriform swimming, bluegill | **0.15–0.21 W/kg body mass** | Jones, Lucey & Ellerby 2007 *J Exp Biol* 210:3422, PMID 17872996 | **abstract**. The authors estimated it from in-vitro measurements of maximal muscle power output. It is a measured-then-scaled estimate, not an in-vivo observation. |
| 5 | Flying fish: red axial muscle is "no more than" that of mackerel cruisers; acceleration to take-off "probably" uses anaerobic white muscle | qualitative | Davenport 1992 *J Mar Biol Assoc UK*, doi 10.1017/s0025315400048761 | **abstract** (via the Crossref record) |
| 6 | Flying fish get their in-air thrust by taxiing with the tail in the water, at up to 50 beats/s | qualitative | Davenport 1994 *Rev Fish Biol Fish*, doi 10.1007/BF00044128 | **search-summary** (I could not reach the abstract) |
| 7 | Pectoral muscle "up to a quarter of body weight" in flying fish | 0.25 | fishkeeper.co.uk popular article | **search-summary**. This is not peer-reviewed. I list it but **do not rely on it**. |
| 8 | Pectoral muscle mass fraction of flying fish, from a primary source | `unknown` | I tried PubMed ("flying fish pectoral muscle"), Crossref, and web search. Davenport 1994 says the girdle is "considerably enlarged" but gives no number that I could reach. | — |
| 9 | g | 9.81 m/s² | constant | — |

**Disagreement between sources, kept rather than averaged:**
- Speed: 8 m/s (row 3b) against 10–20 m/s (row 3).
- L/D: 4.4 measured (row 1) against 4.7 from CFD (row 2).
- Anatomy: Brousseau 1976 (*J Morphol*, PMID 1246081, **abstract**) describes the freshwater hatchetfish (*Gasteropelecus*) as specialised for "self-propelled, aerial flight", with massive ventral flight muscles. That is an anatomical claim of powered flapping in a fish. It is not a power measurement, and it says nothing about whether flapping is *sustained*. I did not test it here.

## 2. Arithmetic (all calculated, nothing observed)

For steady level flight, the minimum aerodynamic power per kg of body mass is bounded by the glide polar:

P/m ≥ g · U / (L/D)

This is a **lower bound** for flapping flight. A flapping wing pays extra profile power, and a propulsor is less than 100% efficient, so the muscle must deliver more than this.

| U (m/s) | L/D | P/m (W/kg body) | ÷ 0.21 | ÷ 0.15 |
|---|---|---|---|---|
| 8 | 4.7 | 16.7 | 80× | 111× |
| 10 | 4.7 | 20.9 | 99× | 139× |
| 10 | 4.4 | 22.3 | 106× | 149× |
| 15 | 4.7 | 31.3 | 149× | 209× |
| 20 | 4.4 | 44.6 | 212× | 297× |
| 8 | 10 *(stress case: L/D ≈ 10 with ground effect, which is my assumption, not a measurement)* | 7.8 | 37× | 52× |

Two worked examples: 9.81 × 10 / 4.7 = 20.87 W/kg, and 20.87 / 0.21 = 99.4.

**Second framing (calculated).** Here I drop the bluegill proxy and ask what specific power the muscle itself would need. If pectoral muscle were 25% of body mass (row 7, which is unreliable and generous), it would have to deliver 7.8/0.25 = **31** to 44.6/0.25 = **178 W/kg muscle**, continuously, in aerobic operation. I have no primary-source value for aerobic fish muscle power that I could cite (`unknown` from my searches; PubMed "fish red muscle power output sustained" returned nothing). So I make no claim about how this compares with fish muscle.

## 3. My value

**Calculated:** the power needed for level flapping flight of a flying fish is ≥ **~17–45 W/kg body mass** (generous stress case ~8 W/kg). The maximum measured-and-scaled pectoral power of a teleost (bluegill) is **0.15–0.21 W/kg body**. That is a shortfall of **~100×**, with a range of **~40–300×**.

**My inference** (separate from what the authors claim): a teleost-type pectoral system cannot sustain flapping flight. This fits the authors' own claims that in-air thrust comes from tail-taxiing in water (row 6) and that take-off uses anaerobic muscle (row 5).

The uncertainty is dominated by the proxy. A bluegill is not a flier, and a fish with an enlarged girdle could have several times more pectoral muscle (fraction `unknown`). Even so, a 40–300× gap would need two orders of magnitude to close.

**Scope of negative searches:** PubMed E-utilities (5 queries), Crossref (4 queries), and about 6 web searches. Full texts at journals.biologists.com, Springer, Cambridge, Wiley, ResearchGate, typeset.io, phys.org and monash.edu could not be accessed (hosts blocked or returned 403 in this session).

## 4. Comparison with the recorded value (read only after §1–§3)

Recorded claim, as quoted in `challenge-203.md`: sustained flapping is not supported, because fish red/slow muscle gives **5–10 W/kg** (measured), below the computed **hover** requirement of **≥ ~34 W/kg flight muscle** for a 0.4 g fish.

- **Direction: agrees.** Both derivations conclude that fish muscle cannot sustain flapping flight. They use different inputs: bluegill pectoral power plus flying-fish aerodynamics here, against red-muscle work-loop values plus 0.4 g hover theory in the record. This is the useful part: it is independent evidence, not one agent agreeing with itself.
- **Magnitude: cannot be compared.** The organism (wild flying fish of about 100 g against a hypothetical 0.4 g fish), the flight regime (fast forward flight against hover) and the normalisation (per kg body against per kg muscle) all differ. As an illustration only, my 17–45 W/kg body at a hypothetical f = 0.3 converts to 56–149 W/kg muscle. That is higher than 34, as expected for flight at 10–20 m/s, but it is not the same quantity.
- I did **not** independently test the recorded claim's weakest point, which the challenger identified: whether forward flight at minimum-power speed (rather than hover) brings the 0.4 g requirement down into the 5–10 W/kg band. My result says nothing about a 0.4 g animal at about 2 m/s.

**Verdict: CANNOT TELL** on the recorded number. The qualitative conclusion agrees.

```swarm-replication
{"claim_id": 203, "my_value": "flying-fish flapping requirement >=~17-45 W/kg body (calculated, glide-polar lower bound) vs 0.15-0.21 W/kg body max teleost pectoral power (bluegill, measured-scaled) = ~100x shortfall (range ~40-300x)", "agrees": null,
  "note": "Independently reached the same qualitative verdict (sustained fish flapping is unsupported) but for wild Exocoetidae in forward flight per kg body, not the recorded 0.4 g hover case per kg flight muscle, so the ~34 W/kg figure itself could not be checked."}
```
