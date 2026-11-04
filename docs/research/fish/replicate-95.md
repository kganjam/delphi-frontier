# Replicate 95: S26 "scale error found", the (120/40.3)^4 size-correction factor

**Status:** re-derivation from sources. I measured nothing. Every number below is labelled *measured (by the
cited authors)*, *calculated (by me)* or *assumption*.

## 0. The blind was broken, and how

The brief said the inputs live in `S26-deepen.md`. That file is not on this branch or on the default branch.
I found it at `origin/claude/deepen-s26-active-stiffening-48xj8q:docs/research/fish/S26-deepen.md`.
I read it in full and only then saw that it **is the working that produced the recorded value**: its §3 table
gives 78.6. The brief also quoted the expression `(120/40.3)^4 = 78.6`.

**So this is not a blind derivation.** I knew the expression and its result before I started. To make up for
that, I checked each input against the source it came from, and I recomputed the arithmetic myself. The
agreement reported in §4 covers the **inputs and the arithmetic**. It is not evidence from someone who
reached the expression independently.

## 1. Inputs, with source and read-level

| Input | Value | Kind | Source | Read-level |
|---|---|---|---|---|
| Bluegill maximum pectoral ray length | **40.3 ± 0.8 mm** (mean ± s.e., 6 fish) | measured (Alben et al.) | Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243, doi:10.1098/rsif.2006.0181, PMC2359861, §2: "Six fishes with fins of similar size (maximum ray length = 40.3±0.8 mm, mean±s.e.)" | full-text via an automated page summarizer (WebFetch of pmc.ncbi.nlm.nih.gov). Direct downloads failed: Europe PMC fullTextXML gave HTTP 500, NCBI efetch gave "publisher does not allow downloading", the PMC HTML returned a reCAPTCHA page, and the Royal Society and Europe PMC PDFs gave 403. The abstract was read directly through the Europe PMC REST API and does not contain the length |
| Length of the ray the requirement is written for | **120 mm** (L = 0.12 m) | **assumption** (by S6-D) | `origin/claude/deepen-fin-ray-s6-cj2i2x:docs/research/fish/S6-deepen.md` line 41: "effective ray span L = 0.12 m, assumption". It is bounded only by Davenport 1992 (abstract, as S6-D relays it) | listing: I grepped the parameter table and did not read the whole file |
| Scaling exponent | **4** | assumption + standard beam theory | EI = E·I. For a solid or thin-walled section of fixed shape, I ∝ d^4. Under isometry d ∝ L. At constant E, EI ∝ L^4 | textbook (Euler–Bernoulli); no source fetched |
| The EI being scaled | 3.8e-6 N m^2 | measured by Flammang et al. 2013 per a relay; **specimen length unknown** | Puri et al. 2018, *J Exp Biol* 221:jeb171777, relaying Flammang et al. 2013 | **listing.** I only saw this second-hand, in S6-deepen and S26-deepen. I did not re-read Puri |

**A mismatch in the inputs (my inference, not any author's claim).** The value being scaled (3.8e-6) comes from
**Flammang et al. 2013**. The source length (40.3 mm) is from **Alben et al. 2007**, which studied a different
set of bluegill. Both papers come from the Lauder lab and study the same species, but the length of Flammang's
specimen is `unknown`. I did not try Flammang's full text. S26-deepen reports that it could not access it
(sites.harvard.edu failed DNS). Alben also says the group's lengths are a *maximum*, and that the ray
behind the 12x comparison is not identified.

## 2. Arithmetic (calculated, `python3 -I`)

- 120 / 40.3 = 2.977667
- 2.977667^2 = 8.8665
- 8.8665^2 = **78.615**

The s.e. bracket on L_src (my calculation; the s.e. is a spread across 6 fish, not an uncertainty for the
specimen that was tested):

- L_src = 39.5 mm: (120/39.5)^4 = 85.18
- L_src = 41.1 mm: (120/41.1)^4 = 72.67

A shorter source ray gives a much larger factor, because 40.3 mm is a maximum length:

- 30 mm: 256
- 20 mm: 1296

Consequence (calculated): 3.8e-6 × 78.615 = **2.99e-4 N m^2** passive EI at 120 mm. Under the same
assumptions, a 12x locking factor meets an EI_req of 6.3e-4 whenever L_src < 62.2 mm.

## 3. My value

**Size-correction factor = 78.6 (calculated), with a range of about 73–85 from the s.e. on the group-maximum
ray length.** The factor is ≥ 78.6 if the tested ray was shorter than the group maximum.

The value is conditional on three assumptions: (a) isometric bluegill-to-120 mm scaling at constant E;
(b) the requirement's L = 0.12 m, itself an assumption; (c) the Flammang ray having had Alben's group-maximum
length, which has no source. The arithmetic is exact. The real uncertainty sits in (a) and (c), and neither can be
quantified from what I could read.

The qualitative claim, that S26's 165x compares a ~40 mm ray's EI against a 120 mm ray's requirement
without size correction, is supported. Both lengths are as stated in their sources: Alben, read full-text via
the summarizer, and S6-D's assumption table.

## 4. Comparison with the recorded value

Recorded (S26-deepen.md §3, and the brief): (120/40.3)^4 = 78.6. Mine: 78.615.

**AGREE** on the arithmetic and on the provenance of both lengths. The caveat from §0 stands: I saw the recorded
value before deriving it, so this agreement checks the inputs and the arithmetic only. One gap is unresolved,
and the recorded working also names it ("Flammang's specimen sizes are `unknown`"): nobody has shown that the
40.3 mm length belongs to the ray behind 3.8e-6.

Negative-search scope: one WebFetch of PMC2359861, plus direct attempts on the Europe PMC XML/PDF, NCBI efetch,
the PMC HTML and the Royal Society PDF. No search for Flammang 2013 specimen lengths was made in this session.

```swarm-replication
{"claim_id": 95, "my_value": "78.6 (dimensionless EI scale factor; ~73-85 over the s.e. of the 40.3 +/- 0.8 mm group-maximum ray length; larger if the tested ray was shorter)", "agrees": true,
  "note": "Arithmetic and both input lengths check out against Alben 2007 (full-text via summarizer) and S6-D's L=0.12 m assumption, but I saw the recorded 78.6 before deriving it, and the 3.8e-6 being scaled is Flammang 2013's ray, whose length is unknown, so the factor rests on isometry plus an unsourced length match."}
```
