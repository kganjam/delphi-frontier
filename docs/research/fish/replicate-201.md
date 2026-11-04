# Replication 201 — pectoral girdle root bending moment (S7)

Independent re-derivation. I did **not** see the original working. The inputs it points to
(`harvest:s7-organ-pectoral-girdle-xlxpkt`) are **not in this repository**. I ran `git grep` for
"pectoral", "scapulocoracoid" and "xlxpkt" on every local and remote-tracking branch
(`claude/pectoral-girdle-bending-moment-4ng27n` and `work/frontier-foundation`) and found nothing.
So I could not read the recorded inputs, and I did not read the recorded derivation either.

**Everything below is calculated. None of it is an observation.**

## My value

- **Root bending moment per fin (calculated): about 4×10⁻⁶ to 9×10⁻⁵ N·m.**
  The span is wide because the inputs are uncertain. The biggest driver is how far the fin reaches
  from the joint, which ranges here from a natural fin to an enlarged "wing"-like fin.
- **Solid round bone section that can carry this moment (calculated): about 0.06 to 0.26 mm in diameter.**
  This uses a strength range of 50–200 MPa.
- **Joint reaction (calculated): about 1 to 75 × body weight.**
  This depends almost entirely on the joint lever arm, which is an assumption.

## Inputs

| Input | Value used | Source | Read-level |
|---|---|---|---|
| Body mass m | 0.4 g (given in the question) | question text | n/a |
| g | 9.81 m s⁻² | standard | n/a |
| Body weight W = m·g | 3.924×10⁻³ N | arithmetic | n/a |
| Lift per fin L | n·W/2, with load factor n from 1 to 3 | **my assumption**: two fins share the weight; n = 3 allows for manoeuvring or gusts. I do not know what the original meant by "design lift". | n/a |
| Fin span b (root to tip) | 5, 15 or 30 mm | **assumption**. 5 mm is my guess for a natural adult zebrafish pectoral fin; 30 mm is a hypothetical enlarged fin about as long as the body. I could not find a measured adult zebrafish pectoral-fin length (see the negative search below). | could-not-access |
| Centre-of-pressure fraction c | 0.424 (elliptical load, 4/3π) to 0.5 (uniform load) | standard beam/lift distribution result | n/a |
| Bone strength σ | 50–200 MPa | **assumption**, a typical vertebrate bone range from general knowledge. I have no zebrafish value: the Carassius rib paper's text (PMC7696420) gives only a modulus of about 12 GPa for rib 1, and no strength. | Carassius paper: full-text (via a summarising fetch); strength value: unknown |
| Joint lever arm a | 0.3–1 mm | **assumption**. No measurement found. | n/a |

Negative searches, with their scope:

- **Adult zebrafish pectoral-fin length versus mass.** One standard web search found no value. The USGS 45-dpf study measured pectoral-fin length, but the search snippet gave no number (read-level: search-summary).
- **Teleost bone bending strength in MPa.** One web search found none in the snippets. The MDPI page for Materials 13:5099 returned HTTP 403. The PMC copy has no strength values in its text (read-level: full-text via summarising fetch).
- **Flying-fish span-versus-mass regressions (Fish 1990, J. Zool.).** I could not access them: the wcupa.edu hosts are blocked in this session's network policy (read-level: search-summary only).

## Arithmetic

```
W  = 0.4e-3 kg × 9.81           = 3.924e-3 N
L  = n W / 2                     = 1.962e-3 N (n=1) … 5.886e-3 N (n=3)
M  = L · c · b
   min: 1.962e-3 × 0.424 × 5e-3  = 4.16e-6 N·m
   max: 5.886e-3 × 0.5   × 30e-3 = 8.83e-5 N·m
Solid circular section: σ = 32M/(πd³)  →  d = (32M/(πσ))^(1/3)
   M=4.16e-6: d = 0.060 mm (σ=200 MPa) … 0.095 mm (σ=50 MPa)
   M=8.83e-5: d = 0.165 mm (σ=200 MPa) … 0.262 mm (σ=50 MPa)
Joint reaction R = M / a, expressed as R/W
   min: 4.16e-6/1e-3   / 3.924e-3 = 1.1
   max: 8.83e-5/0.3e-3 / 3.924e-3 = 75
```

The same formula applied to the claim's own moment range, as a check on the section step only:

```
M = 2e-5 N·m   → d = 0.101 / 0.127 / 0.160 mm  at σ = 200 / 100 / 50 MPa
M = 1.1e-4 N·m → d = 0.178 / 0.224 / 0.282 mm
```

## Comparison with the recorded value

The recorded inputs and working are not in the repository. All I have to compare against is the
claim sentence itself.

- **Moment.** The claim gives 2×10⁻⁵ to 1.1×10⁻⁴ N·m. My range of 4×10⁻⁶ to 9×10⁻⁵ N·m overlaps it, but reaches lower, and its top end is about 20% under the claim's top end. The claim's range would match mine if "design lift" means a larger load factor or a longer fin than I assumed. I cannot tell which inputs they used.
- **Section.** The claim gives 0.12–0.35 mm. My numbers are 0.06–0.26 mm from my moments, and 0.10–0.28 mm from their moments. Their top value of 0.35 mm at 1.1×10⁻⁴ N·m implies a strength of about 26 MPa (σ = 32M/πd³). That is lower than my range, which suggests they used a safety factor or a different section shape. This is my inference; I have not seen their working.
- **Joint reaction.** The claim gives 9–55 × body weight. My 1–75 × body weight contains it. Both figures rest on an assumed lever arm, and as far as I can tell neither has a measured one.
- **Conclusion.** I agree with the qualitative claim, as my own inference: the girdle bone needs only a sub-millimetre section, while the joint reaction is many times body weight. I also agree that the zebrafish girdle section, the adductor muscle PCSA and the bone strength are unknown. I could not find them either.

Verdict: **CANNOT TELL** on the specific numbers, because the inputs behind "design lift" could not be recovered. **AGREE** on the order of magnitude and on the conclusion.

```swarm-replication
{"claim_id": 201, "my_value": "M ≈ 4e-6 to 9e-5 N·m per fin; solid-section d ≈ 0.06–0.26 mm; joint reaction ≈ 1–75 × W (all calculated, assumption-driven)", "agrees": null,
  "note": "Same order of magnitude and same conclusion (bone not limiting, joint unresolved), but the recorded 'design lift' inputs are not in the repo, so the exact 2e-5–1.1e-4 N·m range cannot be checked."}
```
