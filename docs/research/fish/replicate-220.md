# Replication 220: does the Daane phenocopy "most likely fall short by 1.5–2×"?

**Claim under test (from the S22-D-D line):** the `lat4a^nr21/+; kcnh2a^lof/+` zebrafish "phenocopy" most
likely falls short of flying-fish pectoral fin length / standard length (SL) by about 1.5–2×.
**Recorded outcome (named in the task prompt):** S22-D-D-D deepen says this claim FALLS.

**My result: CANNOT TELL.** The one number that decides the question is the pectoral/SL of the
trans-heterozygote. It exists only in Daane et al. 2021 *Curr Biol* Fig 4B, and I could not get that
figure or the supplementary data from any route I tried (§2). I am not substituting a proxy. A
proxy-based shortfall is the thing being contested, and rebuilding it would only repeat the earlier
derivation, not check it independently.

## 0. Disclosure of exposure

I read lines 1–60 of `docs/research/fish/S22-D-D-deepen.md` on branch `claude/deepen-s22-d-d-input-vncsjh`
to find where the inputs live, and then stopped. In those lines I saw:
- S22-D-D's inputs: `p0` ≈ 0.21 SL (0.17–0.26), the proxy `f` ≈ 1.74–2.05× from `kcnk5b^alf/+`, and FF 0.65–0.77.
- S22-D-D's shortfall of 1.52–2.13×.
- The deepen note's doubling/halving sensitivity table.

I did **not** read the deepen note's verdict section or its calc script. I knew the verdict word
"FALLS" only because the task prompt names it. This replication is therefore not blind to the inputs.
It is blind to the deepen note's reasoning toward its verdict.

## 1. Sources and read-levels

| # | Source | Read-level | What I took |
|---|---|---|---|
| P1 | Daane JM et al. 2021, *Modulation of bioelectric cues in the evolution of flying fishes*, Curr Biol 31:5052, doi:10.1016/j.cub.2021.08.054, PMC9172250 (author manuscript NIHMS1735542) | **full-text** (text and figure legends) via NCBI efetch `db=pmc&id=9172250`, sha256 `a478d83a…85b7`. **Fig 4 image: could-not-access. Data S1 (xlsx): could-not-access** | Author's claims (quoted in §3). Fig 4B legend: "Pectoral fin length … normalized by SL", Tukey's HSD |
| P1-pre | bioRxiv 10.1101/2021.03.05.434157 (Europe PMC record PPR293816) | **listing** (Europe PMC metadata only). PDF and F8 image: HTTP 429 | Nothing numeric |
| ZFIN | ZFIN figure pages for ZDB-PUB-210918-31 (the P1 record, per search listing) | **could-not-access** (zfin.org: TLS chain failure via curl, HTTP 503 via WebFetch. franklin/crick/watson mirrors: connect_rejected by egress proxy) | Nothing |
| C-a | Fishes of Texas species account, *Exocoetus volitans* (citing McEachran & Fechhelm) | **search-summary** | pectoral 73.2–77.1% SL |
| C-b | FAO species guide | **search-summary** | 70–75% SL |
| C-c | FAO identification sheet (Indian Ocean) | **search-summary** | 65–70% SL |
| C-d | Davenport, J Mar Biol Assoc UK (on *E. obtusirostris*, not *E. volitans*) | **search-summary** | upper limit ~78–79% SL (different species, so not used as a target) |

The flying-fish sources disagree (65–70 / 70–75 / 73.2–77.1% SL). I keep the full span 0.65–0.77 SL rather
than averaging. I could not read these sources at full text in this pass, so FF is search-summary
grade. It also matches the FF range I saw S22-D-D use, so it is not independent of their input.

## 2. Access attempts for the decisive number (P_dh = trans-heterozygote pectoral/SL)

All of these were tried in this session, 2026-11-04:
- Europe PMC `PMC9172250/fullTextXML`: HTTP 500.
- NCBI efetch PMC XML: **200**, text only. The graphics are `nihms-1735542-f0004.jpg` (Fig 4), with no image payload.
- `pmc.ncbi.nlm.nih.gov/articles/PMC9172250/`: reCAPTCHA challenge page.
- `/bin/nihms-1735542-f0004.jpg` on europepmc.org: 403. On www.ncbi / pmc.ncbi: 404.
- PMC open-data S3 bucket (`pmc-oa-opendata`, prefix `PMC9172250.1/`): only `.json`, `.txt` and `.xml`, no figures.
- Europe PMC `supplementaryFiles`: "Article with id PMC9172250 is not open access one".
- PMC `/bin/NIHMS1735542-supplement-2.xlsx`: 403 / 404 / an HTML stub.
- bioRxiv full PDF and `F8.large.jpg`: HTTP 429 (retried once after a pause).
- ZFIN: see the table above.
- Web search for the numeric trans-heterozygote pectoral/SL (one standard query): no value found.

Scope of the negative: these routes, these hosts, this date. The value very likely exists in Fig 4B
and Data S1. I could not read it. **P_dh = unknown.**

## 3. Author claims (P1, full-text), kept separate from my inference

- Author's claim: "the lat4a nr21/+; kcnh2a lof/+ fish show wild-type-sized medial fins, while the paired fins
  are overgrown (Figure 4)."
- Author's claim: "The overall fin phenotype … is thus remarkably similar to that of flying fishes,
  suggesting the interaction between these two genes is sufficient to phenocopy this key innovation."
- Author's claim (Fig 4 title): "…is sufficient to phenocopy the evolved flying fish fin allometry."
- Author's claim: flying-fish pectoral fins scale with strong positive allometry against SL (Fig 1B,
  Data S1A).

My inference: "remarkably similar" and "phenocopy" are qualitative. The text gives no pectoral/SL value
for the mutant and does not compare it numerically with a flying fish. The author claims therefore
neither confirm nor refute a 1.5–2× shortfall. The positive-allometry claim means a size-matched FF
target would be lower than the adult *E. volitans* 0.65–0.77. I have no size-matched number, so the
right target itself is **unknown**.

## 4. Arithmetic (calculated, not observed)

Shortfall S = FF / P_dh.

What P_dh would make the claim "S ≈ 1.5–2×" true (calculated):
- P_dh = FF / S, giving the range FF_min/2 to FF_max/1.5.
- 0.65 / 2 = 0.325. 0.77 / 2 = 0.385. 0.65 / 1.5 = 0.433. 0.77 / 1.5 = 0.513.
- So the claim holds if P_dh lies in about **0.33–0.51 SL**. That holds only when FF is an adult
  *E. volitans* value from 0.65 to 0.77.
- No shortfall (S ≤ 1) needs P_dh ≥ 0.65–0.77 SL against the adult target. A size-matched target would
  need a smaller P_dh, but that P_dh is unknown (§3).
- S > 2 needs P_dh < 0.325–0.385 SL.

P_dh is unknown, so **S is unknown.** I cannot put a calculated value or interval on it without the
Fig 4B readout.

## 5. Comparison with the recorded outcome

The recorded outcome is that the claim FALLS. I can neither reproduce nor contradict that. My
independent route stops at an unreadable figure. The break-even band in §4 (P_dh ≈ 0.33–0.51 SL for a
1.5–2× shortfall) is what anyone who can read Fig 4B or Data S1 should check P_dh against.

**Verdict: CANNOT TELL.**

What would settle it: a readout of P1 Fig 4B (trans-heterozygote and wild-type pectoral/SL, with n) or
the Data S1 zebrafish sheet, if one exists. A size-matched flying-fish pectoral/SL from P1 Data S1A
would also help.

```swarm-replication
{"claim_id": 220, "my_value": "unknown (shortfall S = FF/P_dh; P_dh, the trans-heterozygote pectoral/SL, is only in Daane 2021 Fig 4B / Data S1, both could-not-access; the claim needs P_dh ~0.33-0.51 SL against FF 0.65-0.77 SL)", "agrees": null,
  "note": "Could not access Fig 4B or Data S1 by any route tried (PMC, Europe PMC, PMC S3, bioRxiv, ZFIN), so I can neither confirm nor refute that the 1.5-2x shortfall claim falls; the author's own claim of a phenocopy is qualitative only."}
```
