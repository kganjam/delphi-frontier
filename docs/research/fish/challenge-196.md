# Challenge 196: adversarial review of claim [S24], surface taxiing and the launch gap

**Claim under review (the author's words, not mine):** "Surface taxiing cannot close the 1-BL (5.84 m/s) launch gap and does not demonstrably close the 3-BL (1.95 m/s) gap. The binding limit is tail-beat frequency, not thrust force, because keeping a caudal lobe producing thrust at 1.95 m/s needs ~49-73 Hz (St 0.2-0.3, A 0.2 TL; calc), against measured adult zebrafish maxima of 21 Hz sustained and 52 Hz transient escape. At sustained frequencies the calculated taxi ceiling (~0.56 m/s) is Ucrit itself. KEY: ~73 Hz needed (range 29-98 Hz) vs 52 Hz measured."

Recorded evidence level: `derived`. Source: `harvest:s24-surface-taxiing-launch-tsepbn`. That harvest document is **not in this repository** (I searched the working tree for "taxi" and found no match). I therefore checked the claim from its stated inputs only.

**Verdict: WEAKENED.** The arithmetic is right. The headline framing is selective, though, and the conclusion depends on one assumption: that taxiing has to run at the Strouhal number of steady, fully submerged cruising. A published measurement on flying fish (read only as a search summary) contradicts that assumption.

---

## 1. Independent arithmetic (calculated, not observed)

I used St = f·A/U, so f = St·U/A. A = 0.2 TL. The stated 49-73 Hz only comes out with TL = 0.04 m (4 cm), so I take that as the author's implicit body length.

| St | A (TL) | f needed at 1.95 m/s | f needed at 5.84 m/s | Ceiling at 21 Hz |
|---|---|---|---|---|
| 0.30 | 0.20 | 73.1 Hz | 219 Hz | 0.56 m/s |
| 0.25 | 0.20 | 60.9 Hz | 183 Hz | 0.67 m/s |
| 0.20 | 0.20 | 48.8 Hz | 146 Hz | 0.84 m/s |
| 0.20 | 0.30 | 32.5 Hz | 97 Hz | 1.26 m/s |
| 0.10 | 0.25 | 19.5 Hz | 58 Hz | 2.10 m/s |
| 0.08 | 0.20 | 19.5 Hz | 58 Hz | 2.10 m/s |
| 0.08 | 0.30 | 13.0 Hz | 39 Hz | 3.15 m/s |

All values in this table are calculated. The author's 49-73 Hz and 0.56 m/s reproduce exactly.

**Defect 1: selective headline (framing).** The KEY puts "~73 Hz vs 52 Hz" side by side. But 73 Hz is the *top* of the author's own St band. The bottom of that same band (St 0.2) gives **48.8 Hz, which is below the 52 Hz escape maximum** the author cites. The 0.56 m/s "ceiling" is also the most pessimistic end (St 0.3). At St 0.2 the ceiling is 0.84 m/s. So the claim's own inputs leave the 3-BL speed within transient frequency range at St 0.2. The headline hides that.

## 2. Proxy check

The **proxy** is the Strouhal band for efficient steady cruising (St 0.2-0.3), measured on fully submerged fish. It stands in for **the minimum St at which a partly submerged tail lobe makes enough net thrust to balance the much lower drag of a mostly airborne body.** These are different quantities. St 0.2-0.4 marks peak *propulsive efficiency*, not the onset of thrust. When the body is lifted out of the water, the thrust needed falls, so a lower St may be enough. This is my inference, not something a source states.

## 3. Hidden assumption, relaxed

The result rests on St ≥ 0.2 during taxiing.

- **Counter-evidence (preserved disagreement):**
  - A 2024 APS March Meeting abstract, "Flying fish taxiing on the water's surface" (https://meetings-archive.aps.org/mar/2024/s27/13; **read-level: search-summary**), reportedly gives a measured taxiing tail-beat frequency of **13.5 Hz**, with ~2 N minimum tail force for a 200 g flying fish.
  - A bioRxiv preprint, "Why does a flying fish taxi on sea surface before take-off?" (https://www.biorxiv.org/content/10.1101/765560.full.pdf; **read-level: search-summary**), cites **50-70 strokes/s** from older literature and gets ~42-50 Hz from its own model at 10 m/s.
  - These two sources disagree by a factor of about 4. I have not resolved which is right.
- **My inference, not in either source:** suppose the 13.5 Hz figure applies at a taxi speed of about 10 m/s (that speed comes from the preprint's model, not from the abstract), with A ≈ 0.2 TL for a fish of roughly 0.3 m. The implied taxiing St is then about 0.08. Carried over to a 4 cm zebrafish, St 0.08 means **~13-20 Hz at 1.95 m/s. That is at or below the 21 Hz sustained maximum.** The 1-BL speed would need ~39-58 Hz, which overlaps the 52 Hz transient figure.
- **Consequences under the relaxed assumption:**
  - The 3-BL statement "does not demonstrably close" is still literally true. Nothing shows that a zebrafish *can* taxi.
  - The supporting statement that frequency is *the* binding limit is not established.
  - "Ceiling = Ucrit" is not established either. The ceiling ranges from 0.56 to 3.15 m/s across plausible St and A.
  - The categorical "cannot close" for 1-BL is not demonstrated by the frequency argument alone at low St. It remains strongly supported if taxiing needs St ≥ 0.15 (≥ 73 Hz at A 0.3).
- **Second assumption:**
  - The author uses A = 0.2 TL. Escape-like large-amplitude strokes (A 0.3 TL) bring St 0.2-0.3 down to 33-49 Hz, all below 52 Hz.
  - The comparison also treats the 52 Hz escape maximum as usable for a taxi. That depends on how long the taxi lasts, which the claim does not give.

## 4. Evidence-level honesty

- `derived` is correct for the required frequencies and the ceiling, and the claim marks them "calc".
- The comparison numbers (21 Hz sustained, 52 Hz transient, adult zebrafish) are presented as **measured**. I could not verify either one. A search ("adult zebrafish maximum tail beat frequency escape Hz critical swimming speed", standard web search, one query) found no primary source for 52 Hz or 21 Hz. The one page giving adult values (ConductScience, 26-33 Hz at Ucrit) looks like template data, and I do not rely on it. **Status of 21 Hz and 52 Hz: unknown to me.** They are not refuted.
- Neither the identity "the ceiling *is* Ucrit" nor the Ucrit value has a cited source in the claim.

## 5. Missed regime or taxon

- The obvious relevant taxon, **flying fish (Exocoetidae), the only vertebrates known to taxi on the surface**, is not discussed. The two flying-fish sources disagree with each other (13.5 Hz vs 50-70 Hz). At least one of them points to a much lower taxiing St than the claim assumes.
- Scope of the negative search: two standard web queries on 2026-11-04, plus a check of this repository. I did not access full texts.

## Corrected statement (my wording)

Calculated values: at the claim's own inputs (St 0.2-0.3, A 0.2 TL, TL 4 cm), taxiing at 1.95 m/s needs 49-73 Hz (central ~61 Hz). The lower end is below the cited 52 Hz escape maximum. The sustained-frequency ceiling is 0.56-0.84 m/s, not a single ~0.56 m/s. If taxiing works at the St ≈ 0.08 implied by one flying-fish measurement (search-summary only), the required frequency falls to ~13-20 Hz. The frequency argument then does not exclude the 3-BL gap, and it no longer cleanly excludes the 1-BL gap at transient frequencies.

```swarm-challenge
{"claim_id": 196, "outcome": "weakened", "reason": "Arithmetic reproduces, but the 73 Hz headline is the pessimistic end of the claim's own band (St 0.2 gives 49 Hz, below the cited 52 Hz escape max), and the conclusion depends on steady-cruise St 0.2-0.3 applying to surface taxiing, which a flying-fish taxi measurement of 13.5 Hz (implied St about 0.08; search-summary only, and contradicted by a 50-70 Hz literature figure) disputes.", "corrected_value": "49-73 Hz required at 1.95 m/s for St 0.2-0.3 (central ~61 Hz), or ~13-20 Hz if taxi St is about 0.08; sustained ceiling 0.56-0.84 m/s (St 0.3-0.2), up to ~2.1-3.2 m/s at St 0.08", "depends_on": ["Strouhal relation f = St*U/A", "implicit zebrafish TL = 0.04 m", "A = 0.2-0.3 TL", "St 0.2-0.3 band as stated by claim", "flying-fish taxiing tail-beat 13.5 Hz (APS March 2024 abstract, search-summary)", "flying-fish taxiing 50-70 strokes/s (bioRxiv 765560, search-summary)", "assumed flying-fish taxi speed about 10 m/s and length about 0.3 m (my assumption)", "adult zebrafish 21 Hz sustained / 52 Hz escape maxima (as given by claim, unverified)", "launch speeds 1.95 and 5.84 m/s (as given by claim)"]}
```
