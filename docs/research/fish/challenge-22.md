# Challenge 22: Danos & Lauder 2012, Table 1, peak COM velocity

**Claim under review (from the agent that ran the work; evidence level unknown, value n/a):**
"The direct peak COM velocity in Table 1 of Danos & Lauder 2012 could not be read: the table is
image-only and the full-PDF hosts are outside the session network policy."

**Paper:** Danos N., Lauder G.V. (2012). Challenging zebrafish escape responses by increasing water
viscosity. *J. Exp. Biol.* 215:1854–1862. doi:10.1242/jeb.068957

**Verdict: WEAKENED.** The main point holds: I also could not read a direct peak COM velocity
in this session. But two of the reasons it gives are wrong or incomplete, and it is aimed at the
wrong table.

## Sources and read-levels

| Source | Route | Read-level |
|---|---|---|
| Crossref record, 10.1242/jeb.068957 | api.crossref.org | abstract |
| Europe PMC record (PMID 22573764) | ebi.ac.uk REST | listing (`isOpenAccess: N`, `inPMC: N`, `hasPDF: N`) |
| Publisher HTML, journals.biologists.com/jeb/article/215/11/1854/10837/ | WebFetch, characters 0–120,936 | full-text, except the table and figure images. A summarising model read the page; I quote only what it returned verbatim. |
| Publisher PDF, journals.biologists.com/jeb/article-pdf/... | curl | could-not-access (HTTP 403 Cloudflare "Just a moment..." challenge) |
| sites.harvard.edu/glauder/files/2022/03/Danos.Lauder.2012.pdf | curl and WebFetch | could-not-access (proxy CONNECT 403; WebFetch ENOTFOUND, i.e. the host is outside the session's allowed domains) |
| dash.harvard.edu, api.unpaywall.org, api.semanticscholar.org, api.openalex.org, core.ac.uk, researchgate.net, scholar.archive.org | curl | could-not-access (proxy CONNECT 403, policy denial) |
| zendy.io PDF viewer (found by web search) | not tried | could-not-access |
| PMC11930232 (2025 paper that cites Danos & Lauder as ref. 13) | Europe PMC fullTextXML | full-text. It cites the paper only qualitatively and gives no COM velocity values from it. |

## Point by point

### 1. "the table is image-only": CONFIRMED

On the publisher page, Table 1 appears only as an image (`m_table016.jpeg`). The page text has no
table rows (WebFetch read). Table 2 is also an image (`m_table017.jpeg`).

### 2. "the full-PDF hosts are outside the session network policy": WRONG for the primary host

- **journals.biologists.com is inside the policy.** The proxy let the curl request through and the
  site itself answered with a Cloudflare bot challenge (HTTP 403). The proxy's status page lists no
  relay failure for this host. WebFetch also retrieved the full article HTML from this host. So the
  publisher is blocked by a bot challenge, not by network policy, and its HTML is readable.
- **The other hosts are outside the policy, as claimed.** sites.harvard.edu (the Lauder-lab PDF),
  dash.harvard.edu and the open-access aggregators are refused by the proxy.
- The negative result still stands, because the HTML route only exposes the table as an image.
  But the stated mechanism is inaccurate, and the claim misses a working full-text route.

### 3. Proxy and target problem: Table 1 is probably the wrong place to look

Captions as returned by WebFetch:

- **Table 1:** "Univariate ANOVA results for 25 kinematic variables during zebrafish C-starts"
- **Fig. 3:** "Selected kinematic variables (means + s.e.m.) at each viscosity treatment … G–I show
  duration, linear displacement and velocity of C-starts. See Table 1 for statistical results."

My inference (not observed): Table 1 most likely holds test statistics (F, P), not velocity values.
The paper puts the per-treatment mean velocities in Fig. 3 G–I. So a "direct peak COM velocity in
Table 1" may not exist. Even with the table image in hand, the measured value would have to be read
off Fig. 3 bars or found in the PDF. I could not see either table image, so I cannot rule out that
Table 1 also lists means. That part is unknown.

### 4. A derived value can be recovered from the text. The claim did not mention it.

The Results give, verbatim: "The mean maximum Reynolds number in 1 mPa s water was 27,800 (±2140
s.e.m.) … compared with 2350 (±160 s.e.m.) and 820 (±60 s.e.m.) in 10 and 20 mPa s fluid,
respectively." Re was computed "using fish length, maximum linear velocity per sequence" and "the
appropriate viscosity for each treatment". Methods: "Fish (mean total length 33.0±1.3 mm)".

I inverted U = Re·μ/(ρ·L) myself, from these inputs alone. Assumptions: ρ = 1000 kg m⁻³ (the paper
gives no density, only that "the differences in fluid density were negligible") and L = 33.0 mm
total length.

| μ (mPa s) | Re (mean ± s.e.m.) | **Derived** U_max (m s⁻¹) | ± from Re s.e.m. | Range for L = 31.7–34.3 mm | BL s⁻¹ |
|---|---|---|---|---|---|
| 1 | 27,800 ± 2140 | 0.84 | ±0.065 | 0.81–0.88 | 25.5 |
| 10 | 2350 ± 160 | 0.71 | ±0.048 | 0.69–0.74 | 21.6 |
| 20 | 820 ± 60 | 0.50 | ±0.036 | 0.48–0.52 | 15.1 |

**These numbers are calculated, not measured.** The paper never states them. Here is what they
depend on:

- **Which velocity went into Re.** The text says "maximum linear velocity per sequence". The
  abstract says "maximum velocity of the center of mass". That these are the same quantity is my
  inference. If Re used a different point, such as the snout, the derived value is not COM velocity.
- **Which length.** If they used standard length (about 0.8 of total length for adult zebrafish; my
  approximation) instead of total length, every derived U rises by about 25%.
- **Mean of products.** Mean Re equals ρ·mean(U·L)/μ, not ρ·mean(U)·mean(L)/μ. With length varying
  only ~4% (s.d. 1.3 of 33 mm), the error from this is small.
- **Fluid density.** Dextran solutions are slightly denser than water. A 1–3% higher ρ would lower U
  by the same fraction, which is negligible next to the s.e.m.

The derived values fall in the expected direction and match the abstract (peak COM velocity
decreases with viscosity). That is a consistency check, not verification.

### 5. Counter-examples and regimes

I did not search for other published values. This is not a test of the claim. Any comparison to
other studies of adult zebrafish C-starts would need its own sourced read.

## What would close this

Either read the Fig. 3 G–I bars (for example by digitising the publisher image `m_jeb068957f3.jpeg`)
or get the PDF. Getting the PDF needs sites.harvard.edu or dash.harvard.edu added to the session's
allowed network domains, or a browser session that passes the Cloudflare challenge on
journals.biologists.com. Until then the direct measured value is `unknown`.

```swarm-challenge
{"claim_id": 22, "outcome": "weakened", "reason": "No direct value could be read, as claimed, but the publisher host is inside the network policy (the article HTML is readable via WebFetch and only a Cloudflare challenge blocks curl), Table 1 is an ANOVA-statistics table while mean velocities are in Fig. 3 G-I, and peak COM velocity can be derived from the stated Re values (about 0.84, 0.71 and 0.50 m/s at 1, 10 and 20 mPa s; calculated, not measured).",
  "corrected_value": null}
```
