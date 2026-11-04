# Challenge 276: adversarial review of S5-D (reachable pectoral-fin planform)

**Date:** 2026-11-04. Desk review. No experiment was run.

**Claim under review** (harvest `deepen-s5-pectoral-fin-ajxurw`). Source file: `docs/research/fish/S5-deepen.md`
on branch `origin/claude/deepen-s5-pectoral-fin-ajxurw`, read in full together with `S5-deepen_calc.py`.

> Genetic enlargement with measured long-fin alleles reaches a per-fin span of ~0.36 SL (0.30–0.45,
> calculated) by dilating the wild-type zebrafish pectoral planform, which leaves aspect ratio
> unchanged, so whether the reachable fin is a flying-fish planform (AR ≥ 3.0, Fish 1990; 9.0–10.7,
> Park & Choi) depends entirely on the wild-type zebrafish pectoral AR, which has not been measured.
> KEY: A0 (span²/area) unknown; reachable AR = A0 under uniform dilation; A0 ≥ 3.0 needed for the Fish
> 1990 envelope, ≥ 9.0 for *Cypselurus*.

**Verdict: WEAKENED.**
- The span arithmetic **survives**.
- Dilation invariance of per-fin AR **survives**.
- "A0 is unknown" **survives**.
- What breaks is the **mapping from A0 to the flying-fish thresholds**. The claim defines A0 as a
  **per-fin** span²/area. It then compares A0 directly with literature ARs whose span convention is
  unverified, and which for *Cypselurus* is more plausibly a tip-to-tip wing AR.
  - Wing-type conventions are ≥ 2× the per-fin value.
  - So the stated cut-offs "A0 ≥ 3.0" and "A0 ≥ 9.0" may be overstated by about 2× or more.
  - By the author's own sensitivity table, a 2× change in the A0 requirement is exactly the change
    that flips the verdict.

All numbers I add are **calculated** in [`challenge-276_check.py`](challenge-276_check.py)
(`python3 -I docs/research/fish/challenge-276_check.py`), unless the sentence says otherwise.

---

## 1. Independent arithmetic

| Quantity | Claim | Mine (calculated) |
|---|---|---|
| span, p0 = 0.173 / 0.208 / 0.260, f = 1.74 | 0.30 / 0.36 / 0.45 SL | 0.301 / 0.362 / 0.452 SL ✓ |
| per-fin AR under L→fL, S→f²S | unchanged | 2.0030 at f = 1, 1.74, 2.05 ✓ (identity, not evidence) |
| equal-ray sector AR = 2/θ; θ for AR 3.0 / 9.0 | 38° / 12.7° | 38.2° / 12.7° ✓ |

The arithmetic is correct. p0 and f are carried-over figure-reads from the S22 chain. I did not
re-derive them and I do not judge them here; Challenge 147 covers p0.

## 2. Proxy check: the threshold is not the same quantity as A0

The claim's A0 is a **single-fin** span²/area, with span measured from the fin base to its tip. The
thresholds come from three sources:

- **Fish 1990** (carried over from `data/research/flying-fish-source-cards.json` on `origin/main`;
  the repo records it as re-read from the PDF; I did not re-read it, so for me it is **listing-level**):
  - p.394 defines AR generically as "wing span squared / wing area", citing Lighthill 1977 and
    Norberg 1985. That is the aerodynamic convention, in which span is tip-to-tip.
  - p.395 applies it to "individual flying fish pectoral fins", range 3.0–16.9.
  - The source card does not say how "span" was taken for one fin. It could be base to tip, or one
    fin's contribution to a tip-to-tip span. **Unknown to me.**
- **Park & Choi 2010** (*J Exp Biol* 213:3269, doi:10.1242/jeb.046052):
  - The full text was **could-not-access**: the journal page returned a Cloudflare challenge, and
    Europe PMC lists no PMCID.
  - The abstract (**abstract** read-level, Europe PMC REST) gives no AR convention. It does compare
    the fish's glide polar with **bird wings** (hawk, petrel, wood duck), whose ARs are tip-to-tip.
    That is suggestive, not proof.
  - The repo card labels 9.0–10.7 "pectoral fin only, not whole wing".
  - Challenge 131 (`origin/claude/challenge-131-wing-aspect-ratio-1n9y9w`, §2) inferred that a
    per-fin AR of about 9.5 would need a leading edge about 9.5 mean chords long, which is implausibly
    slender for a broad flying-fish pectoral. On that basis it judged the tip-to-tip reading more
    plausible.
  - **Disagreement preserved:** the repo card says per-fin; Challenge 131 says probably tip-to-tip.
    Neither re-read the paper's methods.
- **Walker et al. 2013** (*PLoS ONE* 8:e75422; quoted by Challenge 131 at **full-text**):
  - The per-fin length²/area "is doubled to conform to the definition of AR for wings in the
    aerodynamics literature".
  - So at least one fish-fin literature convention is **2 × (per-fin L²/S)**.

**What the A0 requirement becomes under each convention** (calculated, §4 of the script). β is half
the body width as a fraction of fin length; β = 0.1 is assumed, for illustration.

| Literature AR T | if T is per-fin L²/S | if T is doubled per-fin | if T is tip-to-tip (β = 0.1, no body area) |
|---|---|---|---|
| 3.0 (Fish 1990, low end) | A0 ≥ 3.00 | A0 ≥ 1.50 | A0 ≥ 1.24 |
| 9.0 (Park & Choi, low) | A0 ≥ 9.00 | A0 ≥ 4.50 | A0 ≥ 3.72 |
| 10.7 (Park & Choi, high) | A0 ≥ 10.7 | A0 ≥ 5.35 | A0 ≥ 4.42 |

The claim's KEY states only the left-hand column, as if the conventions were identical.

- The author's own §1 table shows "A0 × 2 → flips". A 2× shift in the threshold is the same size.
- The cleanest falsifiable statement is the band: the per-fin A0 needed for *Cypselurus* lies
  **between about 3.7 and 9.0, depending on a convention not yet read**. The claim's single value of
  9.0 is the top of that band.
- **My inference:** this does not make a flying-fish planform more likely in fact, because A0 is
  still unknown. It does mean a future measurement of A0 cannot be scored against the claim's
  thresholds as written.

## 3. Hidden assumption relaxed: "AR unchanged" holds only for the per-fin convention

Suppose the threshold is a tip-to-tip wing AR, with body width and the intervening body strip in the
wing. Fish 1990's wing area for wing loading includes "pectoral + pelvic + intervening body", per
the repo card. Then the comparable reachable AR is

`AR_w(f) = 2·A0·(1 + β/f)² / (1 + γ/f²)`, with β = b/(2L) and γ = S_body/(2S).

Body width and body strip area are set by the body, **not dilated by f**. That is my assumption, and
it holds for fin-specific alleles if the body is not enlarged.

| β, γ (assumed, illustrative) | AR_w at f = 1 | AR_w at f = 1.74 | ratio |
|---|---|---|---|
| 0.10, 0.05 | 4.61 | 4.40 | 0.955 |
| 0.24, 0.12 | 5.49 | 4.98 | 0.907 |

(Calculated, with A0 = 2 assumed only for illustration; the ratio does not depend on A0.)

So under the wing convention, enlargement **lowers** the comparable AR by about 5–10%, towards the
asymptote 2·A0. It does not leave it unchanged. This is a small effect next to the 2× convention gap,
but it contradicts the word "unchanged" outside the per-fin convention.

The claim's "depends **entirely** on A0" is also stronger than the author's own note. That note
(§1–§3) shows that the answer depends on:
- α, the area exponent;
- the fin-spread convention (AR = 2/θ for a fan);
- differential ray growth (the `g` factor).

The KEY's "under uniform dilation" qualifier partly covers α. "Entirely" does not survive.

## 4. Evidence level

- Recorded level: `unknown`.
- The source's own evidence line reads "calculated … on carried-over figure-reads … decisive input
  unknown".
- That is honest. No calculated number is presented as measured.
- The span is correctly marked calculated.
- The thresholds 3.0 and 9.0–10.7 are measured values in their sources. What makes them comparable
  with A0 is an **unstated assumption**, and the claim does not flag it.
- Read-levels for the thresholds: carried over and "not re-read" for both, which the source does
  disclose.

## 5. Counter-examples and missed regimes

- **Convention gap** (§2): this is the main finding.
- **AR alone does not mark a flying fish.** Challenge 131 reports non-flying labrids at per-fin AR
  0.91–2.08, possibly on the undoubled convention (Fulton et al. 2016, full-text in Challenge 131).
  - If the doubled convention applies, those labrids sit at about 1.8–4.2, inside Fish 1990's 3.0+
    envelope.
  - So "AR ≥ 3.0 ⇒ flying-fish planform" is a test of membership in an envelope, not a test of
    function. That is my inference.
  - The source note treats it as an envelope (S5-deepen §1), but the claim's phrase "is a
    flying-fish planform" reads as more than that.
- **Allele scope:** "measured long-fin alleles … ~0.36 SL" is the value for `kcnk5b^alf/+` only.
  - Homozygous or other alleles (`kcnh2a` lof, double mutants) have no pectoral fold-change in any
    source the author or I opened.
  - So 0.36 SL is the value for one measured allele, not an established ceiling.
  - The source note says this (§4, falsifier check). The one-line claim does not.

**Negative-search scope for this review:**
- Park & Choi 2010: publisher page (Cloudflare challenge, could-not-access) and Europe PMC REST
  (abstract only, no PMCID).
- I did not search for Fish 1990 (I relied on the repo card) or for a zebrafish A0 value. The author
  documented that search, and I did not extend it.
- No measured zebrafish pectoral AR is known to me from any source I opened.

## 6. What would settle it

1. Read the Fish 1990 Methods and the Park & Choi 2010 Methods for how "span" was measured on a
   single fin.
2. Measure A0 using the **same** span convention, together with the spread protocol the author
   proposes (S5-deepen §3a).

Until step 1 is done, the A0 requirement for *Cypselurus* is a band, **about 3.7–9.0 per-fin**
(calculated, β = 0.1 assumed), not 9.0.

```swarm-challenge
{"claim_id": 276, "outcome": "weakened", "reason": "Span arithmetic and per-fin dilation invariance hold, but the claim compares a per-fin A0 (base-to-tip span^2/area) against flying-fish ARs whose span convention is unverified and plausibly tip-to-tip or doubled (Walker 2013 doubles per-fin AR; Challenge 131 infers Park & Choi is wing AR), so the A0 cut-offs 3.0/9.0 may be overstated ~2x or more - the very factor the author shows flips the verdict - and under a wing convention enlargement lowers AR ~5-10% rather than leaving it unchanged.", "corrected_value": "span 0.36 SL (0.30-0.45) unchanged; per-fin A0 required: Fish 1990 low end 1.2-3.0, Cypselurus 3.7-9.0 (calculated; convention-dependent, beta=0.1 assumed); A0 itself unknown", "depends_on": ["S5-deepen.md and S5-deepen_calc.py on origin/claude/deepen-s5-pectoral-fin-ajxurw (full-text)", "carried-over p0 = 0.208 (0.173-0.260) and f = 1.74 from S22-D-D (not re-derived)", "Fish 1990 AR definition span^2/area citing Lighthill/Norberg and 'individual pectoral fins' 3.0-16.9, via repo source card (listing-level for me, not re-read)", "Park & Choi 2010 AR 9.0-10.7: full text could-not-access; abstract compares glide polar with bird wings", "repo card claim that Park & Choi AR is pectoral-only vs Challenge 131 inference that it is tip-to-tip (disagreement unresolved)", "Walker et al. 2013 PLoS ONE: per-fin AR doubled to match wing convention (quoted full-text in Challenge 131)", "Fulton et al. 2016 labrid AR 0.91-2.08 (quoted full-text in Challenge 131)", "assumption: body half-width beta = 0.1 fin length and body area not dilated by f (illustrative)", "unknown: wild-type zebrafish pectoral A0 and spread convention"]}
```
