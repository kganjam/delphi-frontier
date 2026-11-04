# Claim 189 propagated to organ and behaviour: what must be true there, and is it?

**Claim 189 (scale `organism`, evidence `derived`).** "S28 VERDICT NEGATIVE: the best design buildable
from demonstrated alleles is the EXISTING Daane `lat4a^nr21/+; kcnh2a^lof/+` zebrafish, and it cannot
fly, glide, skim, or meaningfully extend its leap."

**Status of this note.** I made no new measurement. Every number without a source beside it is a
**calculation** from `docs/research/fish/claim-189-entail_calc.py` (pure arithmetic, < 1 s,
`python3 -I docs/research/fish/claim-189-entail_calc.py`). Date: 2026-11-04.

**Subject of the claim.** The animal is the **adult zebrafish** (*Danio rerio*), double heterozygote
`lat4a^nr21/+; kcnh2a^lof/+`. Every check below names the animal its number came from. Flying-fish
(Exocoetidae) numbers are not used anywhere in this note. One number comes from the **guppy**
(*Poecilia reticulata*); it is used as a cross-species pointer and never as a refutation.

**A second attempt exists.** Branch `origin/claude/claim-189-entail-mm8coe` holds an earlier
propagation of this same claim. I read it (full-text, repository) after drafting my constraint list.
We agree on C1. **We disagree on C2:** it marks the tail-beat timescale `satisfied` from a larval
value; I mark it `open`, for the reason given in §2. I preserve the disagreement rather than resolve it.

## Sources and read-levels

| Source | Animal | Read-level |
|---|---|---|
| `docs/research/fish/S28-organism.md` @ `origin/claude/s28-organism-design-5z0vjz` (the claim) | zebrafish (model) | full-text (repository) |
| `docs/research/fish/S28-deepen.md` @ `origin/claude/deepen-s28-daane-heterozygote-b7kpn8` | zebrafish | full-text of the lines I grepped (repository) |
| `docs/research/fish/S28-D-D-deepen.md` @ `origin/claude/deepen-s28-sensitive-input-4x2i7x` — figure-read of Daane 2021 bioRxiv Fig 8A/8B | zebrafish double het | full-text (repository). **I did not open the preprint PDF myself**; the figure-read reaches me as a relay |
| Daane JM et al. 2021, *Curr Biol* 31:5052, doi:10.1016/j.cub.2021.08.054 | zebrafish | could-not-access by me this session; relayed via S28-D (which records a full-text read) |
| Miln et al. 2021 (escape peak 1.38 m/s, n = 50) | adult zebrafish | listing (repository relay; S28-D notes challenge 191 could not locate the paper) |
| Demesmay et al. 2025, *PLoS Biol* 23:e3003484 (escape peak 1.57 ± 0.27 m/s) | adult zebrafish | listing (repository relay) |
| Soares D, Bierman HS 2013, "Aerial Jumping in the Trinidadian Guppy (*Poecilia reticulata*)", *PLoS ONE* 8:e61617, PMC3629028 | **guppy** | full-text via automated fetch; I saw the quoted sentences only |
| Perathoner S et al. 2014, "Bioelectric Signaling Regulates Size in Zebrafish Fins", *PLoS Genet* 10:e1004080, PMC3894163 | zebrafish `alf` (kcnk5b) | full-text via automated fetch, first 100 000 characters; figures not seen |
| van Leeuwen JL, Voesenek CJ, Müller UK 2015, *J R Soc Interface* 12:20150479 (larval 95 Hz) | larval zebrafish | **could-not-access** (publisher returned HTTP 403). The 95 Hz figure reaches me only as a relay from the mm8coe branch |
| Web search, "adult zebrafish fast-start escape tail-beat frequency" (standard mode) | — | search-summary. Returned larval/eleutheroembryo work only, incl. a larval "up to 100 Hz" cyclic-swimming statement, and a 2025 eleutheroembryo modelling paper (PMC11930232) stating adult escape studies reported distance, bending and duration — not frequency |
| Web search, "adult zebrafish swim tunnel tail beat frequency Ucrit" (standard mode) | — | search-summary. Ucrit 25–40 cm/s (protocol), no peer-reviewed adult Hz value; a vendor page's 26–33 Hz appears to be demo data and is **not used** |
| Web search, "zebrafish jump out of water leap height" (standard mode) | — | search-summary. Terrestrial jumping (Gibb, Ashley-Ross et al.), guppy aerial jumping, a jump-height scaling model; **no zebrafish water-exit measurement**. `experts.nau.edu` did not resolve from this session and would have to be allowed in the session's network settings to read the Gibb et al. abstract |

---

## 1. ENTAIL

Claim 189 is a negative, so what it requires below and beside it are mostly **ceilings**. A ceiling
is checked exactly like a floor: a measured value meets it or contradicts it.

| # | Scale | Kind | Requirement (generic) |
|---|---|---|---|
| **C1** | organ | range | The spread planform area of the paired lifting appendages must lie below the area at which their lift equals body weight at the fastest speed the species is recorded to reach: **< 841 mm²** (calculated at 2.11 m/s, CL 1.07, m 0.25 g). |
| **C2** | organ | timescale | The shortest cycle period of the axial propulsor must be longer than the period needed to drive an airborne skim (132–199 Hz → **5.0–7.6 ms**). |
| **C3** | behaviour | range | The speed at which the animal actually leaves the water must lie below the speed for weight-supporting lift with the existing fin, **< 4.37 m/s** (S28 case C), and — for the "not a meaningful leap extension" half — well below it. |
| **C4** | behaviour | existence | No airborne behaviour may exist that raises fin lift substantially above the quasi-steady spread-fin value S28 already credits (S28 assumes fins held spread at CL 1.07 throughout, itself unobserved). |
| **C5** | organ | spatial | Among alleles with a demonstrated zebrafish fin phenotype, none may lengthen the pectoral fin to within a factor of what weight support needs. Per-fin length for L = W, at the most generous measured speed and the larger figure-read shape factor: **< 1.37 SL** (calculated). Otherwise "the best buildable design is the existing double het" fails. |

None names a molecule. C1 bounds an area, C2 a period, C3 a speed, C4 a class of behaviour, C5 a
length ratio.

---

## 2. CHECK

### C1 — organ, range, planform area < 841 mm² → **satisfied**

Bound (calculation): S = 2W/(ρ V² CL). At 1.38 / 1.57 / 2.11 m/s it is 1965 / 1518 / **841 mm²**. I
use the most generous speed, 2.11 m/s (Demesmay 2025 mean + 2 SD, adult zebrafish, in-water escape).

Meeting it (same animal): the double heterozygote's pectoral fin, figure-read by S28-D-D from the Daane
2021 preprint Fig 8A/8B — length 0.463 SL per fin (median, n = 34), shape factor A/L² 0.13–0.25 per fin
(**one** representative fish), giving 50–96 mm² for the pair. That is **8.8×** below the bound at the
generous speed and 20× below it at 1.38 m/s. S28's own *assumed* AR-5 planform, 202 mm², is still 4.2×
below.

- *Caveats carried, not resolved:* one author-chosen fish; no scale bar; projected area is a lower bound
  on true planform. S28-D-D's estimate for a fully fanned fin (2.1–3.5× the imaged one, ≈ 340 mm²) is
  still 2.5× inside the bound.
- *Disagreement preserved:* S28 case C (202 mm², assumption) vs the figure-read (50–96 mm²). Both inside.
- Read-level: the figure-read is a repository relay; I did not open the PDF.

### C2 — organ, timescale, propulsor period > 5.0–7.6 ms → **open**

Required: a beat period longer than 7.6 ms (frequency < 132 Hz) in the **adult** double het.

What exists:
- **Larval zebrafish**, 4–5 dpf: 95 Hz (10.5 ms), van Leeuwen et al. 2015 — **could-not-access by me**,
  relayed from the mm8coe branch, which quotes it verbatim. My search summary gives a second larval
  statement of "up to 100 Hz" during cyclic swimming (search-summary).
- **Adult zebrafish:** the project's input of 52 Hz (S28 §1, labelled "measured") has **no primary
  citation attached** in the record I read. I found no peer-reviewed adult escape or maximum tail-beat
  frequency.

Why `open` rather than `satisfied`: the larval numbers are the right species but the wrong life stage,
and the adult number has no traceable source. That adults beat slower than larvae is very likely —
frequency falls with body length across fishes — but that is **my inference**, not a measurement in
the subject animal, and "very likely" is what this structure refuses to count. Note that the larval
value satisfies the bound even if it did transfer (95–100 Hz < 132 Hz, ×1.3–2.1 short), so nothing
here threatens the claim. It is unverified, not doubtful.

- **Disagreement preserved:** the mm8coe propagation marks this `satisfied`, treating the larval ceiling
  as an upper bound on the adult. I do not; both positions are recorded.
- **Scope of the negative:** two standard-mode web searches (adult fast-start / escape tail-beat
  frequency; adult swim-tunnel tail-beat at Ucrit). A 2025 eleutheroembryo paper states that adult
  escape studies reported distance, bending and duration, not frequency. So this is "**nobody has
  published an adult maximum that I could reach**", not "it was measured and found low".

### C3 — behaviour, range, water-exit speed < 4.37 m/s → **open**

The bounded quantity — the speed at which an adult zebrafish leaves the water — **has never been
measured** in the record. Stand-ins, all adult zebrafish, all *in-water* escape peaks: 1.38 m/s (Miln
2021, listing) and 1.57 ± 0.27 m/s (Demesmay 2025, listing). All are 2–3× below 4.37 m/s, so the
**flight / glide half** of the claim is not in danger from them.

The **"not a meaningful leap extension" half is more exposed than S28 says.** S28 assumes exit speed ≤
burst speed and calls this generous. The only measurement I found of the in-water-to-in-air speed
change is in a **different species**:

> Guppy (*Poecilia reticulata*, Soares & Bierman 2013): in-water "maximum velocities (102.36±33.75
> cm/sec) were observed right before" breaking the surface; "The peak velocities in the air were
> slightly higher (123.57±30.0 cm/sec)." (authors' numbers; full-text via automated fetch.)

That is a ratio of 1.21 (calculation). **If** it transferred to zebrafish — which is a hypothesis, not a
finding — the Demesmay +2 SD fish would exit at 2.55 m/s. Fin lift at exit would then be (2.55/4.37)² =
**34 % of weight** (calculation, case C), against the 10 % S28 computes at 1.38 m/s, and S28-D-D's
table already gives an 11 % ascent-deceleration reduction at 2.11 m/s for case C. That is no longer
obviously "not meaningful". Flight would still be ×1.7 short.

- The guppy number is **not** a refutation: different animal, and it bears on an assumption, not on a
  measured zebrafish value. It moves the verdict on the leap-extension half from "robust" to "rests on
  an unmeasured exit speed whose direction is not known".
- My inference about mechanism, stated as such: a fish can still be thrusting with the tail as it
  crosses the surface, which is consistent with the guppy authors' statement that jumping fish
  "continue with whole body thrusts and tail beats, even when out of the water".
- **Scope of the negative:** S28-D's record (Miln, Demesmay: neither filmed a surface exit) plus my
  standard-mode search for zebrafish leaps out of water, which returned terrestrial jumping (a
  different behaviour, on a substrate) and guppy aerial jumping. **Nobody has measured it** — not
  measured and found low.

### C4 — behaviour, existence, no airborne lift augmentation → **unsatisfied (nobody has looked)**

What the fins of a leaping zebrafish do in the air has **never been observed** in any source I reached.
S28 assumes fins held spread at CL 1.07 throughout the leap and labels this "generous and unobserved".

Nothing known meets the constraint in the subject animal. Cross-species pointers, which point in
**opposite directions** and are not averaged:
- Guppy (Soares & Bierman 2013): fish jumped "with adducted pectoral fins" — i.e. folded, producing
  *less* lift than S28 credits. If that transferred, S28's leap-extension figure is an over-estimate and
  the claim is conservative.
- Same guppy paper: fish "continue with whole body thrusts and tail beats, even when out of the water"
  — an airborne behaviour does exist in a small teleost. A tail beat in air moves fluid of density
  ρ_air/ρ_water ≈ 1/815 of water's (calculation from standard densities), so I expect its momentum
  contribution to be small — an inference, not a measurement.

**Scope:** one standard-mode web search for zebrafish aerial jumping and the repository record (S28,
S28-D, S28-D-D) — all of which list in-air fin posture as unobserved. This is "**nobody has looked**",
which is distinct from "looked and found no augmentation". One high-speed film of the existing animals
leaping would settle C3 and C4 together.

### C5 — organ, spatial, no demonstrated allele within reach of 1.37 SL per fin → **open**

Bound (calculation): per-fin length for L = W at fixed shape, L = √(S / 2k). At 2.11 m/s and k = 0.25
(the larger figure-read shape factor), **1.37 SL**; at 1.38 m/s, 2.09 SL (k = 0.25) to 2.90 SL (k = 0.13).
Even with S28's assumed AR-5 shape (k = 0.523) at 2.11 m/s, 0.94 SL.

Measured in zebrafish (figure-reads relayed via S28-D-D, Daane preprint Fig 8B): `kcnh2a^lof/+` median
0.463 SL (isolated points up to 0.545); double het median 0.463 SL (up to 0.534). These are **3.0× short**
of 1.37 SL, and 2.0× short of even the AR-5 0.94 SL. The authors mark `lof/+` vs double het "n.s." for
pectoral length — so the double het's advantage is suppressed *median* fins, not longer pectorals.

Why `open`: the constraint ranges over all demonstrated fin-overgrowth alleles, and I could not check
them all.
- `alf` (kcnk5b gain-of-function, Perathoner 2014, zebrafish): heterozygotes show "positive allometric
  growth" with "an allometric coefficient *k* near 2" vs 1.29 in wild type, and "Homozygous mutants have a
  stronger phenotype" — **caudal fin only**. No pectoral length found in the 100 000 characters I read;
  the values are in figures I did not see. **Pectoral fin length in `alf`: unknown.**
- Homozygous `lof`, other overgrowth alleles, and combinations (e.g. `alf; lof`): **not searched**.
- The repository also relays a "swimming-impairing ceiling" of 0.79 SL per fin (Davenport, search-summary
  via challenge 189); I did not check it. Even it is 1.7× short of 1.37 SL.

So every *measured* value satisfies the bound with ≥ 1.7× margin, but the claim's phrase "the best
design buildable from demonstrated alleles" is only checked for `lof` and `nr21`. That is a gap in
scope, not a counter-example.

---

## 3. Result

- **No `unsatisfiable`.** No measured zebrafish number contradicts any constraint. I looked specifically
  for a fin area, exit speed, beat frequency or fin length that would break a ceiling.
- **Satisfied: C1** (planform area, ≥ 4.2× margin, same animal, figure-read relay).
- **Open: C2, C3, C5.** C2 and C5 are open on scope (no adult frequency; untested alleles), and every
  value that does exist meets them. C3 is open because the bounded quantity has never been measured.
- **Unsatisfied: C4** — nobody has filmed what zebrafish fins do in the air.
- **The asymmetry is the finding.** "Cannot fly, glide or skim" survives every check with margins of
  ×1.3–9. "Cannot *meaningfully extend its leap*" rests on two unmeasured behavioural quantities
  (exit speed, in-air fin posture), and the one cross-species measurement of the exit-speed change
  (guppy, +21 % in air) points **against** the claim's "generous" assumption, while the same paper's
  fin-posture observation (adducted pectorals) points **for** it. Neither is about zebrafish.
- **Cheapest decisive measurement:** ≥ 500 fps video of the existing double het and wild-type siblings
  leaping from water, giving exit speed (C3) and fin posture (C4) in one session.

```swarm-entail
{"source_claim": 189, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The spread planform area of the paired lifting appendages must lie below the area at which their lift equals body weight at the fastest speed the species is recorded to reach.",
      "quantity": "paired pectoral fin spread planform area", "lo": null,
      "hi": 841, "units": "mm^2",
      "status": "satisfied",
      "satisfied_by": "Figure-read planform of the Daane double heterozygote (adult zebrafish): per-fin length 0.463 SL (median, n=34), shape factor A/L^2 0.13-0.25 per fin (one fish), giving 50-96 mm^2 for the pair, 8.8x below the bound; S28's assumed AR-5 planform (202 mm^2) is 4.2x below. Bound is a calculation S=2W/(rho V^2 CL) at 2.11 m/s (Demesmay 2025 mean+2SD, adult zebrafish in-water escape), CL 1.07, m 0.25 g (assumed).",
      "satisfied_evidence": "literature",
      "note": "Figure-read of Daane et al. bioRxiv 10.1101/2021.03.05.434157 Fig 8A/8B (= Curr Biol 31:5052 Fig 4B), digitised in docs/research/fish/S28-D-D-deepen.md @ origin/claude/deepen-s28-sensitive-input-4x2i7x; read-level for me: repository full-text relay, PDF not opened. Caveats: one author-chosen fish, no scale bar, projected area is a lower bound; a fully fanned fin (~340 mm^2, S28-D-D estimate) is still 2.5x inside. Same animal on both sides."},
    {"target_scale": "organ", "kind": "timescale",
      "statement": "The shortest cycle period of the axial propulsor must be longer than the period needed to drive an airborne skim (132-199 Hz, 5.0-7.6 ms).",
      "quantity": "maximum tail-beat frequency of the adult", "lo": null,
      "hi": 132, "units": "Hz",
      "status": "open",
      "satisfied_by": "No adult zebrafish maximum tail-beat frequency with a traceable primary source was found. Larval zebrafish (4-5 dpf) 95 Hz (van Leeuwen et al. 2015, could-not-access by me, relayed) and a larval 'up to 100 Hz' cyclic-swimming statement (search-summary) both lie below 132 Hz, but are the wrong life stage; the project's 52 Hz adult input has no primary citation in the record. Adults beating slower than larvae is my inference, not a measurement.",
      "satisfied_evidence": "unknown",
      "note": "Disagreement preserved: origin/claude/claim-189-entail-mm8coe marks this satisfied from the larval value. Negative-search scope: two standard-mode web searches (adult fast-start/escape tail-beat frequency; adult swim-tunnel tail-beat at Ucrit) returned larval/eleutheroembryo data, an eleutheroembryo paper (PMC11930232) stating adult escape studies reported distance, bending and duration rather than frequency, and an unverifiable vendor table (not used). Finding: nobody has published an adult maximum I could reach - not measured-and-found-low. Every value that exists meets the bound."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The speed at which the animal actually leaves the water must lie below the takeoff speed for weight-supporting lift with the existing fin, and well below it for the leap-extension half of the claim.",
      "quantity": "water-exit speed of a leaping adult", "lo": null,
      "hi": 4.37, "units": "m/s",
      "status": "open",
      "satisfied_by": "Never measured in zebrafish. Stand-ins are adult zebrafish IN-WATER escape peaks: 1.38 m/s (Miln 2021) and 1.57 +/- 0.27 m/s (Demesmay 2025), 2-3x below the bound. The only measured in-water-to-in-air speed change found is in the GUPPY (Poecilia reticulata): in-air peak 123.57 vs in-water 102.36 cm/s (ratio 1.21). If it transferred (hypothesis only) a zebrafish at 2.11 m/s would exit at 2.55 m/s and its fin would carry ~34% of weight at exit (calculation), weakening the 'not a meaningful leap extension' half; flight would still be 1.7x short.",
      "satisfied_evidence": "literature",
      "note": "Miln 2021 and Demesmay 2025 (PLoS Biol 23:e3003484): read-level listing via repository relay. Soares & Bierman 2013 PLoS ONE 8:e61617 (PMC3629028): full-text via automated fetch, quoted sentences only. Cross-species: the guppy number is a pointer against S28's 'exit <= burst is generous' assumption, NOT a refutation. Negative-search scope: S28-D record (neither zebrafish study filmed a surface exit) plus one standard-mode search for zebrafish leaping out of water, which returned only terrestrial jumping and guppy work. Nobody has measured it. Bound 4.37 m/s is S28's derived case-C takeoff speed; S28's 3x-range speed is 2.39 m/s."},
    {"target_scale": "behaviour", "kind": "existence",
      "statement": "No airborne behaviour may exist that raises fin lift substantially above the quasi-steady spread-fin value the claim already credits.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "Nothing known meets it in zebrafish: in-air fin posture and in-air propulsive behaviour of leaping zebrafish have never been observed in any source reached; S28 itself labels its spread-fin assumption 'generous and unobserved'. Cross-species pointers disagree and are not averaged: guppies jump 'with adducted pectoral fins' (less lift than S28 credits, supporting the claim) yet 'continue with whole body thrusts and tail beats, even when out of the water' (an airborne behaviour exists in a small teleost). Air density is ~1/815 of water's, so I infer airborne tail beats contribute little momentum - inference, not measurement.",
      "satisfied_evidence": "unknown",
      "note": "Soares & Bierman 2013 PLoS ONE 8:e61617 (guppy), full-text via automated fetch, quoted sentences only. Negative-search scope: one standard-mode web search for zebrafish aerial jumping plus the repository record (S28, S28-D, S28-D-D), all listing in-air fin posture as unobserved. This is 'nobody has looked', not 'looked and found none'. A single high-speed film of the existing animals leaping would settle this and C3 together."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "Among alleles with a demonstrated fin phenotype in the species, none may lengthen the pectoral fin to within a factor of the per-fin length that weight support requires.",
      "quantity": "per-fin pectoral length / standard length required for lift = weight", "lo": null,
      "hi": 1.37, "units": "SL",
      "status": "open",
      "satisfied_by": "Measured (figure-read, adult zebrafish, Daane preprint Fig 8B via S28-D-D): kcnh2a lof/+ median 0.463 SL (points to 0.545), double het median 0.463 SL (points to 0.534), 3.0x short of 1.37 SL and 2.0x short of the AR-5 value 0.94 SL. Bound is a calculation L=sqrt(S/2k) at 2.11 m/s, k=0.25; at 1.38 m/s it is 2.09-2.90 SL. NOT checked: pectoral length in alf (kcnk5b) - Perathoner 2014 reports caudal allometric k near 2 in heterozygotes and a stronger homozygous phenotype but no pectoral value in the text I read; homozygous lof and allele combinations not searched.",
      "satisfied_evidence": "literature",
      "note": "Perathoner S et al. 2014 PLoS Genet 10:e1004080 (PMC3894163), full-text via automated fetch of first 100,000 characters, figures not seen: alf pectoral length unknown. Davenport 0.79 SL 'swimming-impairing ceiling' is a repository relay at search-summary, unchecked; even it is 1.7x short. Every measured value meets the bound; the constraint stays open because 'best design from demonstrated alleles' has been checked only for lof and nr21."}
  ]}
```
