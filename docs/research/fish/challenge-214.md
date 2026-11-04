# Challenge 214 — boundary condition behind the 1.98 N/m fin-ray stiffness

**Claim under review (not written by me):**
> COULD NOT VERIFY: the precise boundary condition behind the 1.98 N/m figure -- a challenge
> reports it is at ~2/3 of ray length and base-clamped rather than at the tip. The publisher blocks
> full-text XML from PMC ("does not allow downloading of the full text in XML form") and the OA
> service returns 404. The abstract does not state the load position.

Source: Alben S, Madden PG, Lauder GV (2007) *The mechanics of active fin-shape control in
ray-finned fishes.* J R Soc Interface 4(13):243–256. doi:10.1098/rsif.2006.0181, PMID 17251142,
PMCID PMC2359861.

**Verdict: REFUTED.** The access barrier is real for the two routes tried, but the claim's negative
search was too narrow. The full text is open on the PMC article HTML page, and it states the
boundary condition explicitly.

## What I reproduced (the author's routes)

| Route | Result | Read-level |
|---|---|---|
| NCBI efetch `db=pmc id=2359861` | XML returned with the comment `The publisher of this article does not allow downloading of the full text in XML form.` | could-not-access (front matter only) |
| `https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC2359861` | HTTP 404 page | could-not-access |
| PubMed abstract (efetch `db=pubmed id=17251142`) | Abstract gives no load position and no 1.98 N/m figure | abstract |

The claim describes these three outcomes correctly. One small caveat: the 404 is a 404 for the whole
web page at that legacy URL. It does not say that this article is not open access, so I don't count
it as evidence about the article.

## The route the author missed

| Route | Result | Read-level |
|---|---|---|
| `https://pmc.ncbi.nlm.nih.gov/articles/PMC2359861/` (HTML) | HTTP 200, about 70 k characters of article text, including §2, §5.2, and the captions of figures 6 and 7 | **full-text** |
| Europe PMC `fullTextXML` | HTTP 500 | could-not-access |
| royalsocietypublishing.org `/doi/full/` | HTTP 403 | could-not-access |

The PMC HTML says the following. These are quotations, so they are the authors' statements:

- **Figure 7a caption:** "The ray is clamped horizontally at the base, and a vertical point force is
  applied at two-thirds of the distance from the ray base to the tip, as in figure 6 a. When only one
  of the bases is clamped, the ray deflects much more than when both bases are clamped. In the
  latter case, the force–displacement curve may be fit with a slope of 1.98 N m−1, about 12 times
  the value when one hemitrich is free."
- **§5.2 (Cantilever):** "the two bases of the ray are either clamped, with both clips held fixed at
  the same longitudinal position, or else free to slide axially, with only one of the fin-ray bases
  held by a clip … (i) ϕ0 = 0 or (ii) the free-base boundary condition in equation (3.16)."
- **§5.2:** "a probe pushes down on the fin ray at *approximately* two-thirds of the distance from
  the base to the tip, and the force on the probe is measured as a function of **tip deflection** of
  the ray." Both-bases-fixed gives "an approximately linear relation with an offset".
- **Specimen (§2, figure 2a):** a single fin ray dissected from the pectoral fin of a bluegill
  sunfish (*Lepomis macrochirus*). The fishes had a maximum ray length of 40.3 ± 0.8 mm (mean ±
  s.e., n = 6 fishes). Figure 2a shows ray 4 of 13.

So the precise boundary condition is known:

- The ray is an excised cantilever, clamped horizontally at the base.
- Both hemitrich bases are clamped at the same longitudinal position (ϕ0 = 0), so there is no
  actuation offset.
- A vertical point load is applied at about 2/3 of the base-to-tip length.
- The 1.98 N/m is a linear-fit slope from a single loading curve, and that curve has an offset.

The earlier challenge said "~2/3 of ray length, base-clamped, not at the tip", and it **is correct**
about the load point.

## Arithmetic, redone independently

I calculated these from the paper's stated numbers. None of them are measurements.

- One-hemitrich-free slope: 1.98 / 12 ≈ **0.165 N/m**. The paper gives this only as the ratio "12×".
- Model ratio range: the paper says the clamped/free ratio "transitions from 3 to 100" as G passes
  through 1. The experimental 12 sits inside that range at G ≈ 10², which is consistent with the
  paper.
- A rough check using a classical cantilever, 3B/a³:
  - Inputs: a = (2/3)(40.3 mm) ≈ 26.9 mm, and the paper's measured B ≈ 10⁻⁶ to 10⁻⁵ J m.
  - Result: k ≈ 0.15 to 1.5 N/m. The one-free value (0.165 N/m) is in that range, and the
    both-clamped value (1.98 N/m) is above it. This fits the paper's account that shear coupling
    adds stiffness. It is an order-of-magnitude check only.

## Proxy problem the claim and its upstream both miss

The figure is not a load-point stiffness. Per §5.2, the deflection axis is **tip deflection**, while
the force is applied at 2/3 L. So 1.98 N/m is (force at 2/3 L) / (tip displacement), a
transfer compliance. The figure 7a caption just says "deflection of the ray", which is ambiguous. I
take the §5.2 main text as the more specific statement, but I flag the disagreement between the
caption and the text rather than resolving it.

- For a uniform Euler–Bernoulli cantilever loaded at a = 2L/3, tip deflection / load-point
  deflection = (3L − a)/(2a) = 1.75. If pure bending applied, the load-point stiffness would then be
  about 1.98 × 1.75 ≈ 3.5 N/m. This is my calculation, not a reported value.
- That correction holds only when G ≪ 1. The paper places the real ray at G ≈ 10², where shear
  dominates and the deflection shape differs. So 1.75 is not a valid conversion factor for this ray,
  and **the load-point stiffness is `unknown`** from what the paper reports.
- Any downstream use that treats 1.98 N/m as a "tip stiffness" or a load-point spring constant uses
  the wrong quantity. Don't use it as either without saying so.

## Other scope limits on the figure

These come from the paper's text; I did not reanalyse its data.

- The ray was excised and isolated. Fin membrane, neighbouring rays, and the fish's own muscle
  tone are all absent, so this is not an in-vivo fin stiffness.
- The figure is for one taxon (bluegill), one fin (pectoral), and evidently one ray per curve.
  I found no replicate count or error bar for the 1.98 slope in the text I read.
- The both-clamped curve is "linear with an offset" and the ray has nonlinear (stiffening) intraray
  collagen, so the slope depends on the force range fitted.
- I did not look for counter-examples in other taxa. That search was not attempted, so its scope is
  zero.

## Evidence level

The claim records its level as "unknown". The 1.98 N/m number is a **measured** linear fit of
experimental force–displacement data (figure 7a, the experiment panel, not the model panel 7b). It is
not derived. Its boundary condition is now known from full text.

```swarm-challenge
{"claim_id": 214, "outcome": "refuted", "reason": "The full text is openly readable at pmc.ncbi.nlm.nih.gov/articles/PMC2359861/ and states the condition: an excised bluegill pectoral ray clamped horizontally at the base with both hemitrich bases fixed (phi0=0), a vertical point force at ~2/3 base-to-tip, and the 1.98 N/m slope fitted against tip deflection (per section 5.2), so it is a transfer stiffness, not a load-point or tip stiffness.", "corrected_value": "1.98 N/m (measured linear-fit slope; force applied at ~2/3 L, displacement measured at the tip; both hemitrich bases clamped; one-base-free about 0.165 N/m by the paper's 12x ratio)", "depends_on": ["Alben, Madden & Lauder 2007 J R Soc Interface 4:243-256, PMC2359861, full-text HTML at pmc.ncbi.nlm.nih.gov, Figure 7a caption", "same source, section 5.2 statement that force is measured as a function of tip deflection", "same source, section 2 specimen description (Lepomis macrochirus pectoral ray, max ray length 40.3 +/- 0.8 mm)", "same source, Figure 7a caption ratio of 12 between both-clamped and one-free slopes"]}
```
