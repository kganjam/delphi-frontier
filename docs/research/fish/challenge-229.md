# Challenge 229: "No teleost has a locomotor spring or latch"

**Claim under review (from `docs/research/fish/S29-organism.md`, branch `claude/s29-launch-energy-2iuixr`, §0 item 4, §3, §4):**
> "NO TELEOST HAS A LOCOMOTOR SPRING OR LATCH. The only fish LaMSA is the syngnathiform over-centre head latch, and it is used in FEEDING. A locomotor latch would be an invention with no precedent in fish, not a modification of something that exists."

Recorded evidence level: literature. Value: n/a.

**Verdict: WEAKENED.** The *latch* half and the *LaMSA is feeding-only* half survived my search. The *spring* half, "no teleost has a locomotor spring", is contradicted by at least one published teleost study of locomotor elastic recoil. The claim as stated is also stronger than the source document's own scoped wording.

---

## 1. Arithmetic

The claim has no numerical content, so there is nothing to recompute. I did not re-audit S29's energy budget (11.83 mJ, 29.6 J/kg); that is outside this claim.

## 2. Proxy check

The claim treats **LaMSA** (a spring with a latch) as standing in for **any elastic element that does useful locomotor work in a teleost**. Those are different quantities. S29's question is whether a zebrafish launch could be spring-assisted, so what matters is the second one: does elastic recoil already contribute launch work in any teleost? That is what S29 §3 claims to test when it says "I found no measured elastic energy storage that does useful launch work in any teleost." On that quantity the claim fails, as set out in §4.

## 3. The claim is stronger than its source

- The source (S29 §3) says: "I found no measured elastic energy storage that does useful launch work in any teleost", and "No LaMSA has been reported for zebrafish or any cyprinid. **My search was limited by the network policy.**"
- The claim as recorded says: "**NO TELEOST HAS** a locomotor spring or latch."

The recorded claim turns a scope-limited negative search into a universal statement and drops the scope note. **That is an evidence-level defect.** The honest level is "literature, negative search, scope-limited (network-restricted), not exhaustive."

## 4. Counter-example: locomotor elastic recoil in teleosts

**Ashley-Ross, Perlman, Gibb & Long 2014, "Jumping sans legs: does elastic energy storage by the vertebral column power terrestrial jumps in bony fishes?", *Zoology* 117(1):7–18, doi:10.1016/j.zool.2013.10.005.**
- Read level: **search-summary** of the abstract. The full text (jan.ucc.nau.edu) and a related SICB abstract (sicb.org) were **could-not-access**: the hosts are outside this session's network allowlist.
- According to the abstract summary, the authors built a model of elastic recoil work stored in the neural and hemal spines and measured ground reaction forces (GRF) in the tail-flip jumping mangrove killifish *Kryptolebias marmoratus* and the non-jumping largemouth bass *Micropterus salmoides*.
- Their result: "GRF data showed that they produce the same magnitude of mass-specific elastic recoil work." The non-jumper had the *stiffer* body. They suggest that fused hypurals in the caudal peduncle, rather than the whole axial skeleton, may explain differences in jumping.
- I did **not** obtain the magnitude of that elastic work in J/kg or as a fraction of jump energy. It is `unknown` here.

**What this does to the claim (my inference, not the authors' words):**
- At least one published teleost study models and measures elastic recoil work done by the axial skeleton during a *locomotor launch*, a terrestrial tail-flip jump.
- So "no teleost has a locomotor spring" is false as worded, and S29's "no measured elastic energy storage that does useful launch work in any teleost" is at minimum contested.
- The study says nothing of a latch, and it does not show **power amplification**. The elastic work is the same in a non-jumper, so it looks like a generic property of a bent fish body rather than a specialised spring. The counter-example therefore weakens the "spring" half; it does not establish a fish LaMSA.

**Disagreement preserved:** S29 cites Shadwick (tuna caudal tendons, ABSTRACT) as concluding that those tendons "do not function as energy saving locomotor springs." Hebrank et al. 1990 (*J. Exp. Biol.* 148:449, search-summary) conclude that blue-marlin backbone structures "are not arranged so as to contribute to elastic recoil of the backbone during normal swimming." Both are negative results for *steady swimming* in large pelagic fish. Ashley-Ross et al. 2014 is a positive result for *terrestrial jumping* in small fish. These do not contradict each other, because the regimes differ. But the small-fish jumping regime, which is closer to S29's 0.4 g launch, is the one S29 missed.

Long 1992 (*J. Exp. Biol.* 162:131, search-summary) measured marlin intervertebral joint stiffness exceeding damping. From the summary alone, I cannot tell whether it claims energy storage, so I do not use it as a counter-example.

**Candidate I could not confirm:** blackspotted rockskipper *Entomacrodus striatus* (Bartlett et al. 2025, *J. Exp. Zool. A*, search-summary). The summary says power amplification "may play a role" given small body size, but reports peak jump power "within the range of typical fish muscle." A 21,000 W/kg figure appeared in the same search listing but appears to belong to an insect study. **Not used, and not a counter-example.**

## 5. Parts that survived

- **Fish LaMSA is feeding-only, in Syngnathiformes.** Searches for latch-mediated or elastic-recoil feeding outside Syngnathiformes, and for LaMSA in fish locomotion, returned only seahorse, pipefish and snipefish (Longo et al. 2018 Proc. R. Soc. B 285:20181078; Avidan et al. 2020 bioRxiv; Van Wassenbergh et al. 2008). One summary noted that elastic-recoil power amplification "has not been explicitly tested in live fish apart from seahorses and pipefish" as of that publication.
  - Search scope: 5 web searches (standard mode), English, no database access (Web of Science/Scopus not available), and network-restricted fetches.
  - Within that scope, **no counter-example found.**
- **No teleost locomotor latch.** No search returned a geometric, over-centre, or muscle-antagonist latch in any teleost locomotor system (same scope).
- **Latch is "invention, not modification".** Relaxing the hidden assumption:
  - The argument assumes a latch must be a *geometric* skeletal catch. A muscle-as-latch (antagonist co-contraction, then release), as in frogs and locusts, needs no new skeletal element.
  - Tail-flip jumpers adopt a pre-bent posture on the substrate before launch. That posture is a candidate place where such a muscular latch could act. **This is my inference; no measured instance exists.**
  - So the "invention" label is defensible for a skeletal latch, and somewhat softer for a muscular one. It does not change S29's verdict, because S29's binding term is energy per stroke, not the latch.

## 6. Effect on S29

S29's headline ("No, short by ~2×, set by energy per stroke × push-off medium") does not rest on this claim. Correcting the spring half removes the statement that the elastic element would be wholly novel. The axial skeleton already stores and returns *some* launch work in teleost jumpers. That makes "item 1 is a large modification" more credible, not less, and leaves item 2 (the latch) as the genuinely novel part.

**Corrected wording:**
> "No teleost locomotor *latch* and no teleost locomotor *LaMSA* are reported (negative search, scope-limited). The only measured fish LaMSA systems are syngnathiform feeding systems. Elastic recoil of the axial skeleton does contribute measured work to terrestrial tail-flip jumps in at least two teleosts (Ashley-Ross et al. 2014, read at search-summary level), but without a latch or demonstrated power amplification."

## Sources

| Source | Read level |
|---|---|
| S29-organism.md (`origin/claude/s29-launch-energy-2iuixr`) | full-text |
| Ashley-Ross et al. 2014, *Zoology* 117:7, doi:10.1016/j.zool.2013.10.005 ([NAU listing](https://experts.nau.edu/en/publications/jumping-sans-legs-does-elastic-energy-storage-by-the-vertebral-co/)) | search-summary (full text could-not-access) |
| Hebrank et al. 1990, *J. Exp. Biol.* 148:449 | search-summary |
| Long 1992, *J. Exp. Biol.* 162:131 | search-summary (fetch could-not-access) |
| Longo et al. 2018, Proc. R. Soc. B 285:20181078 ([PMC6053929](https://pmc.ncbi.nlm.nih.gov/articles/PMC6053929)) | search-summary |
| Avidan et al. 2020, bioRxiv 10.1101/2020.08.13.249466 | search-summary |
| Bartlett et al. 2025, *J. Exp. Zool. A* ([NSF PAR](https://par.nsf.gov/biblio/10570086)) | search-summary; not used as evidence |

```swarm-challenge
{"claim_id": 229, "outcome": "weakened", "reason": "The latch and feeding-only-LaMSA parts survive a scope-limited negative search, but 'no teleost has a locomotor spring' is contradicted by Ashley-Ross et al. 2014, which report measured mass-specific elastic recoil work from the vertebral column in teleost terrestrial tail-flip jumps, and the claim drops the source's own scope caveat.",
  "corrected_value": null,
  "depends_on": ["Ashley-Ross et al. 2014 Zoology 117:7-18 abstract (search-summary read): GRF-measured elastic recoil work in Kryptolebias marmoratus and Micropterus salmoides", "Negative search for non-syngnathiform fish LaMSA and teleost locomotor latch (5 standard web searches, network-restricted)", "Longo et al. 2018 / Avidan et al. 2020 / Van Wassenbergh et al. 2008 as the syngnathiform feeding LaMSA set", "S29-organism.md section 3 wording and its network-limited scope note"]}
```
