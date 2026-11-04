# r5-daane-catchfair: fit and balance test print

**LAUNCH PROTOTYPE, UNTESTED, OVERWEIGHT.** This set is for a first fit and balance test. It is not flight-ready.
- Nothing in it has been printed, weighed, glided or thrown.
- No printer or resin compatibility is claimed. Slicing, orientation, supports and post-cure are not checked.
- Dry mass from the meshes is 20.73 g, against claude-07's preliminary 10.5 g budget (13.5 g on this fin area).
- The catch-wall change below is the builder's claim. Reviewer claude-13 has not checked it yet.

r5 is r4-daane-printfix with two changes: a crown fairing over each catch slot, and claude-07's v3c CG window.

## What changed from r4
- **Crown fairings (body).** In r4 the top of each catch slot rose above the sloping skin at the sides of the head,
  at |y| ≈ 6 mm at x 20 and ≈ 9 mm at x 34. There the slot broke out through the skin and left a feather edge: a
  36° wedge, down to 0.097 mm, as reviewer claude-13 measured. r5 adds a raised arch over each slot top. The arch
  keeps the full 2.0 mm liner wall above the slot across the body. It ends in flat caps 0.5 mm outside the widest
  skin at that station: 11.07 mm either side of the centreline at x 20, and 12.79 mm at x 34.
  - The slot now opens through those square end caps instead of through the skin.
  - Each arch's roof is level across the body (z 10.89 mm at both slots). Where the head's skin falls away at the
    sides, the arch stands up to 7.7 mm above the skin just beside it, measured 0.3 mm fore and aft of each arch.
    Seen from above, they are two transverse lugs, 7.5 mm long (x), on the sides of the head. They add 0.40 g to the
    body (12.53 → 12.93 g). Their drag and their effect on the band path are not assessed.
  - Wall check over both slot zones, one inward ray from every one of the 5,501 body faces there: no wall reading
    is below the 0.45 mm rule. The minimum is 0.498 mm, the 0.5 mm shell itself. 19 readings below the rule
    measure corners, with wedges of 77° or more, mostly where the end caps meet the slot. They are listed in
    `manifest.json` under `parts[body].catch_zone_wall`.
  - The same check on the r4 body finds 21 wall readings below 0.45 mm and 17 below 0.30 mm.
- **The slots are 0.09 mm higher.** The seat heights are set from the assembled CG height, and the arches raise it
  (CG z 4.06 → 4.14 mm). The slot top is now at z 7.14 mm. **r5's body and plugs are not interchangeable with r4's.**
- **CG window.** The ballast table uses claude-07's window for this planform, x 49.5–55.2 mm, with target 52.4 mm and
  never aft of 54.1 mm before the VLM neutral point. It replaces the 44–60 mm window, which came from v3a.
- Unchanged from r4: every fin file is mesh-identical to r4's (bytes 81 onward), and so are the parameters, the
  sockets, the ballast bay, the port and the drains.

## The set (6 parts)
| file | part | mass from mesh |
|---|---|---|
| `stl/body.stl` | hollow body, with integral dorsal, anal and caudal fins and the two crown fairings | 12.93 g |
| `stl/pectoral_L.stl` | pectoral, goes on the fish's anatomical RIGHT (+y) | 3.00 g |
| `stl/pectoral_R.stl` | pectoral, goes on the fish's anatomical LEFT (−y) | 3.00 g |
| `stl/pelvic_L-dec+2.stl` | pelvic trim key, decalage +2°, anatomical RIGHT | 0.69 g |
| `stl/pelvic_R-dec+2.stl` | pelvic trim key, decalage +2°, anatomical LEFT | 0.69 g |
| `stl/catch_plug-x20-dz+0.0.stl` | launch-catch seat plug, forward slot | 0.42 g |

Masses are mesh volume × 1220 kg/m³ (Alpha Grey V1, root's card). The other trim keys (dec −1 to +4) and plugs are
in this revision's `stl/` folder in the repository.

**Which side is which.** The suffixes are v3's names, and v3's `_L` is the fish's anatomical right. Hold the fish
dorsal side up with the snout pointing away from you: the `_L` parts go on your right and the `_R` parts on your
left.

## Assembly (fit test)
1. **Before assembly.** Wash out uncured resin through the two 2.5 mm ventral drains (x 60 and 140 mm) and the
   5 mm ventral ballast port (x 11 mm). Drain size is assumed, not validated.
2. **Pectorals.** Push each root tongue (2 × 10 × 6 mm) into its socket. The spar and ridges go on the underside.
   - The socket is designed with 0.10 mm clearance a side. That is assumed, and printer tolerance is unknown, so
     the tongue may need light sanding.
   - A rectangular tongue can enter either way up. Check the spar is underneath before gluing.
   - Glue is optional for a fit test. Record the adhesive if you use one.
3. **Pelvics.** Fit the `dec+2` keys (tongue 2 × 6 × 6 mm) the same way. Play in this socket changes the decalage,
   so note any looseness.
4. **Catch plug.** Press `catch_plug-x20-dz+0.0` into the top of the forward slot (x 20 mm).
   - The STL is already in its installed orientation: its print pose is the fish frame. Keep its +z dorsal, towards the
     top of the fish. Its lower face is the seat the band bears on.
   - Clearance is 0.1 mm a side (assumed). Retain it with tape or a drop of glue.
   - The plug ends at the old body skin, so it is shorter than the faired slot. The arch's outer ends have no plug
     under them.

## Balance test
1. Start with **no ballast**. The mesh prediction for the dry assembly (all six parts) is CG x 62.9 mm from the
   snout tip, on the centreline, z 4.2 mm. Weigh it and record the mass.
2. Balance the fish across a thin edge and measure the CG position from the snout tip.
3. claude-07's CG window for this planform is x 49.5–55.2 mm, so the dry fish is tail-heavy. Ballast goes into the
   bay through the ventral port, which you then close with tape or putty.

   Ballast for each target CG, assuming steel shot set in glue at 4.7 g/cm³ packed from the front of the bay:

   | target CG x | ballast | total |
   |---|---|---|
   | 54.5 mm | 3.9 g | 24.6 g |
   | 52.4 mm (target) | 5.2 g | 25.9 g |
   | 49.5 mm | 7.4 g | 28.1 g |

   If the measured dry CG differs from 62.9 mm, these figures move with it. Report the measured value. Do not
   ballast to a CG aft of 54.1 mm before the VLM neutral point exists.
4. **Record:**
   - the printer, resin, layer height, orientation and supports;
   - each part's printed mass;
   - the tongue fit, and any sanding;
   - how the crown fairings printed (their end caps and the slot edges);
   - the dry CG;
   - the ballast and the final CG;
   - the slot, plug and pelvic key used.

Do not throw it on the strength of this test. A hand-glide trim is a later step. Launch loads, fin strength, the
band's bearing on the new slot edges and impact survival are not verified.

## Files in the ZIP
`manifest.json` has every parameter, check and hash for this revision. `SHA256SUMS` lists each file in the ZIP.
