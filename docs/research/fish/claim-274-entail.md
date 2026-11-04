# Claim 274: what it requires at the organ and behaviour scales

**Source claim (organism scale, evidence: derived).** REOPENING CONDITION, falsifiable: an airborne
zebrafish lobe beating at 1.4–2.2× its best measured burst tail speed (A_pp 12–19 mm at 52 Hz, or
72–117 Hz at burst amplitude), or surface-piercing lobe thrust at Re 1e4 measuring well above the 2-D foil law.

**What this document is.** It lists what the claim needs to be true at the scales next to it, then
checks each requirement against published numbers. No experiment or simulation was run. Every
number below is marked as one of three things: measured (quoted from a source), derived (my own
arithmetic), or assumed.

**Where the claim came from.** Nothing in this repository records the claim or its provenance. A
`grep` for "airborne", "surface-piercing", "lobe thrust" and "52 Hz" found nothing outside `.git`.
So the baseline it implies is reconstructed below from the claim text alone.

## 0. The baseline the claim implies (derived, not observed)

The two ranges in the claim fit together only if the "best measured burst" is about
**A_pp ≈ 8.6 mm at f ≈ 52 Hz**. This is my arithmetic, not a quoted value:

- 12/1.4 = 8.57 mm and 19/2.2 = 8.64 mm.
- 72/1.4 = 51.4 Hz and 117/2.2 = 53.2 Hz.
- The resulting mean tail-tip speed is 2·A_pp·f ≈ 0.89 m s⁻¹.

An 8.6 mm peak-to-peak amplitude is twice the whole body length of a 5 dpf larva (standard length
3.83 ± 0.16 mm; Ravel et al. 2025). So the baseline has to describe a juvenile or adult fish. This
is an inference from size alone.

## 1. Constraints and checks

### C1. behaviour / range: a measured adult burst near 52 Hz with A_pp ≈ 8.6 mm must exist

Status: **unsatisfied**. I could not find the measurement.

- **What I searched:** five web searches (two in extended mode) for adult zebrafish
  fast-start, escape, burst and U_crit tail-beat frequency and amplitude.
- **What I found:** every quantitative hit was larval, a different species, or a flow-tank study
  with no burst maximum:
  - The Mwaffo et al. PeerJ PIV study (flows of 26–52 mm s⁻¹; the search summary gives no year)
    only says bursting fish have larger amplitude and *lower* frequency than cruising fish.
    Read-level: search-summary. peerj.com was blocked by this session's network policy.
  - A vendor protocol page (conductscience.com) gives about 26–33 Hz at U_crit for fish of about
    3 cm. Read-level: search-summary. It is not peer-reviewed and not a burst value.
- **Scope of the negative:** this is "I searched and could not find it". It is not "people
  measured it and found nothing", and it does not rule out a value in papers I could not open.
  - Plaut (2000), J Exp Biol 203:813: only the abstract was seen through a search summary; no
    tail-beat Hz was visible.
  - I did not open full texts of adult fast-start papers.
- **Consequence:** the "best measured" anchor of the reopening condition has no traceable
  citation. The 52 Hz / 8.6 mm baseline should be treated as `unknown` until claim 274's own
  source names it.

### C2. organ / timescale: adult axial fast muscle must fail to cycle at 72–117 Hz at burst strain

**What the requirement is.** At burst amplitude, a half-cycle at 72–117 Hz lasts 4.3–6.9 ms
(derived). For the condition to describe performance beyond the fish's best, adult myotomal
muscle must be unable to complete activation and relaxation at adult burst strain inside that
window.

Status: **unsatisfied**. There is no adult measurement either way, and the larval data push
against the requirement.

**Measured, larval only:**

| Source | Measured value | Read-level |
|---|---|---|
| Voesenek et al. 2020, *PLoS Biol* 18:e3000462 | "the maximum tail-beat frequency observed for zebrafish larvae is 95 Hz"; "maximum muscle contraction frequency of 90–100 Hz" | full-text (first ~100k of ~161k characters) |
| Mead, Kennedy, Palmer, Ebert & Warshaw 2020, *Biophys J*, doi:10.1016/j.bpj.2020.06.036 (bioRxiv 10.1101/2020.04.02.010298) | Larval myotome gives net power of 134 ± 20 W kg⁻¹ at 80 Hz in work loops; peak instantaneous power in 100 Hz work loops comes at 18 ± 2 muscle lengths s⁻¹ | search-summary of the abstract; bioRxiv returned HTTP 429 and par.nsf.gov is blocked |
| van Leeuwen et al. (as relayed by search) | f = 95 Hz with A_tail = 2.4 mm at 4–5 dpf | search-summary |

**What the authors claim:** zebrafish larvae cycle their axial muscle at 80–100 Hz.

**My inference:**

- This does **not** contradict C2. Larval amplitudes (about 2.4 mm) and strains are far below an
  8.6 mm adult burst. The implied larval tip speed of about 0.46 m s⁻¹ (derived, if 2.4 mm is
  peak-to-peak) sits below the 0.89 m s⁻¹ baseline.
- The zebrafish myotome lineage therefore *can* run at 72–117 Hz at small strain. C2 holds only
  if adult fibre kinetics or strain scaling bring the ceiling below about 72 Hz.
- I found no measured adult zebrafish twitch or work-loop frequency ceiling. So this is
  `unsatisfied`, not `satisfied`, and not `unsatisfiable`.

**Disagreement kept:** the 72–117 Hz band that the claim treats as "beyond best" overlaps the
95 Hz larval maximum. The two are compatible only because they are at different amplitudes.

### C3. behaviour / existence: a behaviour must exist in which a zebrafish lobe beats while airborne

Status: **unsatisfied**.

**Measured:** Gibb, Ashley-Ross, Pace & Long (2011), *J Exp Zool A*, "Fish out of water:
terrestrial jumping by fully aquatic fishes". Read-level: listing plus search-summary.
- The authors report that *Danio rerio* makes tail-flip jumps on land.
- The jumps are a modified fast-start with a prolonged stage one.
- They are launched by pushing against a substrate.

**My inference:** this shows zebrafish do have airborne ballistic phases. It does not show a lobe
**beating** in air during flight, and no tail-beat frequency in air was reported in anything I
read.

**Scope of the negative:** one search on terrestrial jumping. I did not search for zebrafish
leaping out of water or behaviour at the air-water surface. So "beating while airborne" is
"not found in a narrow search", not "looked for and absent".

### C4. organ / range: the fish must operate at Re near 1e4 (the surface-piercing branch)

Status: **satisfied**, but by **derivation**, not by a direct measurement of Re.

**Measured:**
- Adult wild-type U_crit is reported as 25–90 cm s⁻¹ across studies. The ranges listed are 25–40,
  70–90, 40–80, 50–65, 55, 25–30 and 35–45 cm s⁻¹ (Wakamatsu, Kashima & Hirata 2020,
  *Bio-protocol* 10:e3712, Table 1, read via PMC7842627).
- The authors attribute the spread to differences between swim-mill equipment. **This
  disagreement is kept, not averaged.**
- Read-level: full-text, but the table text was garbled, so the ranges could not be matched to
  individual studies.

**Assumed:** body length L ≈ 3 cm (no length is given in that source) and ν ≈ 0.87×10⁻⁶ m² s⁻¹
at 26–28 °C.

**Derived:**

| | Re at 25 cm s⁻¹ | Re at 90 cm s⁻¹ |
|---|---|---|
| Based on body length (3 cm) | 8.6×10³ | 3.1×10⁴ |
| Based on an assumed 9 mm fin chord | 2.6×10³ | 9.3×10³ |

So Re of about 1e4 sits inside the adult range when based on body length, and at the upper edge
when based on fin chord.

**Note:** whether thrust follows "the 2-D foil law" is a separate question. I did not check it,
and C4 does not test it.

### C5. organ / energetic: available muscle power must be compared with the power needed to support weight in air

Status: **open**.

- **Available power:** the only zebrafish number I found is larval and measured in vitro:
  134 W kg⁻¹ muscle at 80 Hz (Mead et al. 2020, read through search-summary). Read-level is the
  same as in C2.
- **Required power:** this needs lobe area, stroke geometry and body mass for an airborne fish.
  Claim 274 does not state them, and I did not compute them.
- So no comparison was made, and the constraint is not checked.

## 2. Summary

| # | Scale | Kind | Status | Evidence |
|---|---|---|---|---|
| C1 | behaviour | range | unsatisfied | could not find the 52 Hz / 8.6 mm baseline |
| C2 | organ | timescale | unsatisfied | adult data missing; larval measurements reach 95 Hz at small amplitude |
| C3 | behaviour | existence | unsatisfied | airborne tail-flip exists; lobe beating in air not reported |
| C4 | organ | range | satisfied | derived from measured U_crit and an assumed body length |
| C5 | organ | energetic | open | not checked |

**None are `unsatisfiable`.** No measured value I found contradicts the claim.

**Weakest point:** C1. The reopening condition is scaled to a "best measured burst" whose
measurement I could not trace.

## Sources (with read-level)

- Ravel G et al. 2025, *iScience* 28:112056 (PMC11930232). Read-level: full-text, first 100k
  characters.
- Voesenek CJ, Li G, Muijres FT, van Leeuwen JL 2020, *PLoS Biol* 18:e3000462 (PMC7481021).
  Read-level: full-text, partial.
- Mead AF, Kennedy GG, Palmer BM, Ebert AM, Warshaw DM 2020, *Biophys J*,
  doi:10.1016/j.bpj.2020.06.036. Read-level: search-summary; the full text could not be reached.
- Voesenek CJ, Muijres FT, van Leeuwen JL 2018, *J Exp Biol* 221:jeb149583. Read-level:
  full-text, partial.
  - It describes a 5 dpf larva at about 85 Hz with A ≈ 0.44 body lengths.
  - It gives no adult zebrafish frequency and no zebrafish Re apart from a CFD Re of 340.
- Gibb AC, Ashley-Ross MA, Pace CM, Long JH 2011, *J Exp Zool A*. Read-level: listing plus
  search-summary.
- Wakamatsu Y, Kashima M, Hirata H 2020, *Bio-protocol* 10:e3712. Read-level: full-text.
- Plaut I 2000, *J Exp Biol* 203:813. Read-level: search-summary.
- Mwaffo et al., *PeerJ* article 4041 (year not seen). Read-level: search-summary; access was
  blocked by network policy.

```swarm-entail
{"source_claim": 274, "source_scale": "organism",
  "constraints": [
    {"target_scale": "behaviour", "kind": "range",
      "statement": "A measured best burst of adult/juvenile zebrafish must exist with tail-beat frequency near 52 Hz at peak-to-peak tail amplitude near 8.6 mm (the baseline implied by the claim's 1.4-2.2x bands)",
      "quantity": "burst tail-beat frequency at A_pp ~8.6 mm", "lo": 51.4, "hi": 53.2, "units": "Hz",
      "status": "unsatisfied",
      "satisfied_by": "Not found. Searched adult zebrafish fast-start/escape/burst/Ucrit tail-beat frequency and amplitude (5 web searches); hits were larval, other species, or flow-tank data without a burst maximum.",
      "satisfied_evidence": "unknown",
      "note": "Baseline bounds derived by me from claim text (72/1.4, 117/2.2; 12/1.4, 19/2.2). Mwaffo et al. PeerJ 4041 (search-summary, access blocked): bursting fish have lower TBF than cruising; conductscience vendor page (search-summary, unverified) ~26-33 Hz at Ucrit. Scope: could-not-find, not measured-absent; full texts of adult fast-start papers and Plaut 2000 not read."},
    {"target_scale": "organ", "kind": "timescale",
      "statement": "Adult axial fast muscle must be unable to complete an activation-relaxation cycle at burst strain within a 4.3-6.9 ms half-cycle (72-117 Hz), so that the band lies beyond best performance",
      "quantity": "maximum cyclic contraction frequency of adult myotome at burst strain", "lo": null, "hi": 72, "units": "Hz",
      "status": "unsatisfied",
      "satisfied_by": "No adult zebrafish twitch/work-loop frequency ceiling found. Larval myotome is measured to cycle at 80-100 Hz at small amplitude, which does not contradict the adult-strain requirement but shows the tissue lineage can reach the band.",
      "satisfied_evidence": "unknown",
      "note": "Voesenek et al. 2020 PLoS Biol e3000462 (full-text, partial): larval max TBF 95 Hz, max muscle contraction frequency 90-100 Hz. Mead et al. 2020 Biophys J doi:10.1016/j.bpj.2020.06.036 (search-summary of abstract): 134+/-20 W/kg at 80 Hz. Larval A_tail ~2.4 mm (search-summary) << 8.6 mm, so not unsatisfiable. Scope: adult muscle mechanics not found in searches of zebrafish muscle work-loop/twitch kinetics."},
    {"target_scale": "behaviour", "kind": "existence",
      "statement": "A behaviour must exist in which a zebrafish propulsive lobe beats cyclically while the animal is airborne",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "Zebrafish make substrate-launched terrestrial tail-flip jumps with ballistic airborne phases (Gibb et al. 2011), but no report of lobe beating during flight was found.",
      "satisfied_evidence": "literature",
      "note": "Gibb, Ashley-Ross, Pace & Long 2011 J Exp Zool A (listing + search-summary). Scope: one search on terrestrial jumping; leaping from water and surface behaviour not searched, so this is not-found-in-narrow-search."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The fish/lobe must operate at Reynolds number near 1e4 for the surface-piercing foil comparison to apply",
      "quantity": "Reynolds number (body-length based)", "lo": 3000, "hi": 30000, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Derived from measured adult Ucrit 25-90 cm/s with assumed L=3 cm, nu=0.87e-6 m2/s: Re_L 8.6e3-3.1e4; chord-based (assumed 9 mm) 2.6e3-9.3e3.",
      "satisfied_evidence": "derived",
      "note": "Wakamatsu, Kashima & Hirata 2020 Bio-protocol 10:e3712 Table 1 (full-text, table garbled): Ucrit ranges 25-90 cm/s vary by swim-mill equipment; disagreement preserved. Body length assumed, not sourced. 2-D foil-law conformity not checked."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "Mass-specific muscle power available must be compared against the power needed for airborne lobe weight support",
      "quantity": "available minus required mass-specific power", "lo": null, "hi": null, "units": "W/kg",
      "status": "open",
      "satisfied_by": "Not checked: required power needs lobe area, stroke geometry and mass not stated in the claim; only available-power figure found is larval in vitro 134 W/kg at 80 Hz.",
      "satisfied_evidence": "unknown",
      "note": "Mead et al. 2020 Biophys J (search-summary). No calculation performed."}
  ]}
```
