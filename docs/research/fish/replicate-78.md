# Replicate 78: how much would zebrafish pectoral muscle have to grow for flapping?

**Claim under test:** "Flapping requires a 5–15x enlargement of the pectoral musculature. No
zebrafish pectoral-muscle mass measurement was found in the sources searched."

**Repository check:** The brief says the inputs are in `S10-deepen.md`. That file does not exist in
this checkout, on any branch or in any commit, and no file mentions "pectoral" or "flapping". So I
did not see the other derivation. Everything below comes from outside sources.

## Result

**My value: `unknown`.** The enlargement factor cannot be calculated from observations, because its
denominator, the zebrafish pectoral-muscle mass as a fraction of body mass, has no measurement I
could find. What I *can* derive is a conditional formula:

    enlargement factor = F_required / f_zebrafish

with F_required ≈ 0.115–0.25 (see inputs) and f_zebrafish unknown.

This formula is my own calculation, not an observation. Any factor such as "5–15x" depends on an
assumed value of f_zebrafish.

## Inputs

| # | Input | Value | Source | Read-level |
|---|-------|-------|--------|-----------|
| 1 | Lowest flight-muscle ratio (flight muscle mass / body mass) among flying animals able to take off, measured across species | 0.115 (range 0.115–0.560) | Marden 1987, *J Exp Biol* 130:235–258, "Maximum lift production during takeoff in flying animals" | search-summary (the full text on cob.silverchair.com is blocked by this session's network policy) |
| 2 | Lift per unit flight muscle mass, similar across taxa | 54–63 N/kg | Marden 1987 (as above) | search-summary |
| 3 | Freshwater hatchetfish (Gasteropelecidae) pectoral muscle | "up to one-quarter" of body weight (~0.25) | Wikipedia (Gasteropelecidae); Animal Diversity Web (*Gasteropelecus sternicla*); hobbyist sites | search-summary. These are secondary or popular sources, and I found no primary measurement. |
| 4 | Zebrafish adult pectoral-muscle mass | **unknown** | Searched: the web for "zebrafish pectoral fin muscle mass adult abductor adductor weight". Hits: Thorsen & Hale 2005 (anatomy); Patterson, Mook & Devoto 2008 (fibre growth, hyperplasia/hypertrophy); a PMC paper stating "little information is available about the adult musculature" of zebrafish fins; Nord et al. 2021 (fibre counts at 5 dpf). None reports mass. | search-summary |
| 5 | Pectoral-muscle mass fraction in other non-flying teleosts (possible substitute for #4) | **unknown** | Stickleback "pectoral muscle index" (Hoffmann & Borg 2006, *J Fish Biol* 68:1451) is defined, but no values were visible. Thorsen & Westneat 2005 (12 labriform reef fishes) reports masses that were not visible. Foster & Higham 2010 (ratfish, dogfish) could not be accessed (biomechanics.ucr.edu is blocked). | listing / could-not-access |

**Scope of the negative searches (#4, #5):** I ran about six web searches in a single session on
2026-11-04. I could not open the JEB or UCR PDFs because those hosts are outside this session's
allowed network. I did not search PubMed or ZFIN directly for full texts. "Not found" means not found
within that scope. It does not mean no measurement exists.

## Arithmetic

Required fraction, F_required:
- Minimum observed in flying animals (Marden): 0.115.
- The only fish credited with powered aerial pectoral use (hatchetfish, from popular sources): ~0.25.
- I use 0.115–0.25 as the bracket. I am **not averaging** these: one is a taxon-wide minimum for
  powered take-off, the other a single-family maximum from popular sources.

Enlargement factor = F_required / f_zebrafish, for illustrative values of f_zebrafish (assumed, not
measured):

| f_zebrafish (assumed) | factor at F = 0.115 | factor at F = 0.25 |
|---|---|---|
| 0.5 % | 23x | 50x |
| 1 % | 11.5x | 25x |
| 2 % | 5.75x | 12.5x |
| 3 % | 3.8x | 8.3x |
| 5 % | 2.3x | 5x |

Working backwards (my inference): a factor that lands somewhere in 5–15x needs
0.115/15 ≤ f ≤ 0.25/5, so **0.77 % ≤ f_zebrafish ≤ 5 %**. A factor of 5–15x across the whole range
of F_required needs f_zebrafish ≈ 1.7–2.3 %, a band too narrow to defend without a measurement.

## Caveats

- Mass ratio is necessary but not sufficient. Marden's threshold is for animals that already have
  wings, flight-adapted fibre types and air-adapted wing loading. A fin in air would also need area,
  stiffness and enough flapping frequency. So "enlargement of musculature" alone underestimates
  what flapping requires. This is my inference, not something a source claims.
- Whether hatchetfish truly flap in powered flight is itself a published question that I did not
  re-check here. I use input #3 only as an upper bracket.

## Comparison with the recorded value

The question text gives the claim as 5–15x, and I found no recorded derivation in the repository.
My derivation reproduces the *form* of the claim: a ~10x-scale factor follows if zebrafish pectoral
muscle is about 1–3 % of body mass. But the input that decides the factor is unmeasured, so the
factor itself is an assumption, not a derived result.

**Verdict: CANNOT TELL.** I neither confirm nor refute 5–15x. Both derivations, if they agree, would
be agreeing on an assumed denominator.

```swarm-replication
{"claim_id": 78, "my_value": "unknown (conditional: factor = 0.115-0.25 / f_zebrafish; 5-15x implies an assumed, unmeasured f_zebrafish of ~0.8-5% body mass)", "agrees": null,
  "note": "The flight-muscle requirement (Marden 1987, >=0.115 of body mass) is sourced, but no zebrafish or comparable teleost pectoral-muscle mass fraction was found, so 5-15x cannot be derived from observations."}
```
