# CAD and PLM, and what a parts library for engineered biology should steal from them

**Status:** Reference draft · 2026-11-04 · Owner: fable-lead
**Audience:** anyone designing the identity, revision, and spec-sheet layer of a parts
library for engineered organisms.
**Purpose:** distil ~40 years of mechanical CAD/PLM practice into decisions we can
reuse, so we build the parts organisation deliberately instead of reinventing it badly.

> **Honesty floor.** Every standard number and product named below is real and was
> checked against primary or vendor sources during drafting (see *Sources* at the end).
> Where a sentence reasons by analogy to biology rather than reporting mechanical-CAD
> practice, the sentence says so. Claims about the *future* biology schema are design
> proposals, not established practice, and are marked as such. If you find an invented
> standard number or a misattributed capability, treat it as a defect and file it.

---

## 0. Why this document exists

We are building a design system for engineered organisms that is supposed to behave
like an aerospace parts organisation: every artifact — a designed protein, an actuator,
a scaffold, a protein complex, a mechanical-biological assembly, a rig, a mechanism —
gets an identifier, a timestamp, a revision, a spec sheet with working parameters, and
assembly guidelines.

Mechanical engineering solved most of these problems between roughly 1985 and 2010, at
enormous cost, through a mix of standards bodies (ASME, ISO, SAE/EIA), PLM vendors
(Siemens, PTC, Dassault, Aras), and hard-won shop-floor convention. The solutions are
not obvious and several of them are counterintuitive — the single most important lesson,
that part numbers should carry *no meaning*, is one almost every team gets wrong on the
first try.

This document is the foundational reference. It is opinionated: at each section it says
what mature practice converged on, *why*, and what we should do. The final section is the
one that matters most, because it is where the analogy to biology breaks — and a borrowed
concept applied where it doesn't fit is worse than no concept at all.

A note on our own substrate. This repository (`delphi-frontier`) already enforces a
content-addressed record model that, by coincidence or convergence, has independently
rediscovered several PLM invariants: a `Record`'s `version` **is** the sha256 of its
canonical bytes, a `Ref` pins one exact immutable version and never "whatever is
current", and a `predecessor` digest links a record to the one it supersedes
(`specs/SPEC-001-record-types.md`). Keep that in view. Where PLM practice and our existing
model agree, that is strong evidence. Where they disagree, we should understand which one
is wrong for our domain before we pick.

---

## 1. Part identity: the part number

### 1.1 The core distinction — intelligent vs non-intelligent numbers

A part number is the primary key of the entire system. Two philosophies exist.

**Intelligent (significant / smart) part numbers** encode meaning in the digits.
`RES-0603-10K-1%-X7R` tells you it is a resistor, 0603 package, 10 kΩ, 1 % tolerance,
X7R dielectric — readable without a lookup. The scheme *is* a classification taxonomy
baked into the key.

**Non-intelligent (non-significant / sequential / "dumb") part numbers** carry no
meaning. The next part is just the next integer: `100847`, then `100848`. All meaning
lives in the attached metadata record, never in the key itself.

### 1.2 Why mature organisations abandoned intelligent numbers

This is the counterintuitive lesson and it is nearly universal among people who have run
a large item master for a decade. The failure modes of intelligent numbering:

1. **Classification is never stable, but the key must be.** The moment you encode
   "material = aluminium" into the number, a part that changes material either gets a
   wrong-but-permanent number or needs renumbering — and renumbering a released part is
   catastrophic (every drawing, BOM, PO, and inventory record that referenced it is now
   stale). You have coupled an immutable key to a mutable fact.
2. **The scheme runs out of room.** Fixed-width fields (two digits for "category") hit
   their limit; the 100th category has nowhere to go, and widening the field breaks every
   existing number.
3. **Humans optimise the wrong thing.** People start *choosing* parts by reading the
   number and stop consulting the actual spec, so two parts that look similar in the
   number but differ in a field nobody encoded get swapped. The number lies by omission.
4. **It encodes a single hierarchy** when real parts belong to many overlapping
   categories (a titanium fastener is both "fastener" and "titanium" and "flight-critical").
   A classification taxonomy belongs in queryable *attributes*, not in the key.
5. **Mergers, acquisitions, and supplier parts** arrive with foreign schemes that cannot
   be reconciled with yours.

The mature consensus: **the part number should be a short, meaningless, permanent,
system-assigned key. All meaning lives in attributes you can query, re-classify, and
correct without ever touching the key.** This is exactly the database normalization
argument — don't put semantics in the primary key — and PLM consultants repeat it
constantly. (That the argument is *stated* this way in CAD/PLM practice is reporting;
whether the argument is *correct* is a matter of long consensus, not a theorem.)

The compromise many shops actually ship: a non-intelligent base number plus a small,
*coarse* and stable prefix that almost never changes (e.g. a one- or two-character
"this is a document vs a part vs an assembly" class), with everything finer-grained in
attributes. The prefix is deliberately too coarse to go stale.

### 1.3 What a part number must guarantee

Independent of scheme, a usable part number must guarantee:

- **Uniqueness** across the whole namespace, forever. Never reissued, even after a part
  is obsoleted. A retired number is a tombstone, not free inventory.
- **Permanence / immutability.** The number never changes for the life of the part. (See
  §1.4 for what "the part changed" actually means.)
- **One number ⇒ one form/fit/function.** Two physically interchangeable things may share
  a number *across revisions* (see §2); two non-interchangeable things must have different
  numbers. This is the load-bearing rule and it is where identity meets revision.
- **Resolvability.** Given the number you can retrieve the authoritative record.
- **Opacity is a feature, not a limitation** (per §1.2).

### 1.4 How identity survives a design change — the FFF rule

The decision that trips up every newcomer: *when a part changes, do I bump the revision
or mint a new part number?*

The mechanical-CAD answer is the **Form, Fit, Function (FFF) interchangeability rule**:

- If the change leaves the part **fully interchangeable** with the old one — a customer or
  an assembly can use either, in either direction, with no adverse effect — it is the
  **same part number, new revision**.
- If the change breaks interchangeability (it no longer fits, or mounts differently, or
  performs out of the old envelope, or is not backward-usable), it is a **new part
  number**.

"Backward and forward interchangeable" is the strict reading: a stock of old and new
parts must be freely mixable. A classic failure is a one-way change (new part works where
old was used, but old won't work where new is now required) — under strict FFF that is a
**new part number**, because interchangeability is not symmetric.

This is the rule that makes the part number a *promise about behaviour*, not a label for a
CAD file. Hold onto it; §10 argues it is the single hardest concept to carry into biology
and also the most valuable.

### 1.5 Real schemes to learn from

- **NATO Stock Number (NSN)** — a 13-digit *non-intelligent* identifier (a 4-digit
  classification group/class, then a 9-digit non-significant National Item Identification
  Number). Even the part that *looks* classified (the NSC group) is coarse; the identity
  lives in the NIIN. It is the canonical nation-scale sequential scheme.
- **Military CAGE code + part number** — a supplier identity (CAGE) plus that supplier's
  own number. Identity is scoped by issuer, which is how you federate across
  organisations without a global registry agreeing on numbers. (Our `namespace` +
  `issuer` fields are the same move.)
- **GS1 GTIN / manufacturer catalog numbers** — consumer-goods identity; largely
  sequential within a company prefix.
- **Common PLM default** — Teamcenter, Windchill, Aras and the rest ship with
  auto-generated sequential numbers out of the box and let you configure a scheme; the
  vendors' own best-practice guidance leans toward keeping it non-significant.

**For us:** mint non-intelligent, system-assigned, permanent identifiers. Keep a coarse,
stable *kind* facet only (we already have `kind ∈ {Problem, Claim, …}` and will add
engineering kinds). Everything else — organism chassis, function, target, family — is a
queryable attribute, never part of the key. Our content-digest `version` is *not* the
part number; it is the revision identity (§2). The stable human-facing `id` within a
`namespace` is the part number.

---

## 2. Revision vs version: the distinction PLM enforces

This is the second concept newcomers collapse, and PLM systems go to great lengths to keep
the two apart. The vocabulary is not fully standardized across vendors, but the
*structure* is near-universal.

### 2.1 The two axes

- **Revision** — a *formally released, externally meaningful* state of a part. Revisions
  are the things the outside world references: Rev A, Rev B, Rev C. A revision is created
  by a controlled process (an engineering change, §4) and, once released, is **immutable**.
- **Version** (also "iteration") — the *working, in-process* saves between releases. You
  might save a CAD part 50 times on the way from Rev A to Rev B; those 50 saves are
  versions/iterations. Most are never seen outside the design workspace.

The slogan: **you iterate through many versions to produce one revision.** Working state
churns; released state is frozen and sequential.

### 2.2 Revision identifiers

- **Letters** are the classic released-revision sequence: A, B, C…, and by strong
  convention **the letters I, O, Q, S, X, Z are omitted** (they're confusable with
  numerals or each other). This convention is documented in ASME Y14.35 (Revision of
  Engineering Drawings and Associated Documents). After Y you continue AA, AB, …. *Caveat:
  the exact letter rules and max length have changed across editions (the 1997 edition
  states the omitted-letter list and a two-character max; later editions revise this), so
  cite the edition you actually follow, not folklore.*
- A common convention is that **working/unreleased** drafts use a numeric or dash prefix
  (e.g. a leading "-", or "A.1", or a draft flag) and the plain letter appears only on
  release. The point is that you can tell at a glance whether you're looking at frozen or
  fluid state.

### 2.3 Why a released revision is immutable

Because the outside world made decisions based on it. A released Rev B has: purchase
orders cut against it, parts in inventory built to it, assemblies that incorporated it,
test reports that qualified it, possibly regulatory filings citing it. If you could edit
Rev B in place, every one of those references would silently become a lie. So the rule is
absolute: **a released revision is write-once. To change a released part you create the
next revision; you never mutate the old one.** The old revision remains retrievable
forever as the exact thing that was built.

This is precisely the invariant our content-addressed store already enforces: a `Record`'s
`version` is the sha256 of its own canonical bytes, so the bytes *cannot* change without
the identity changing — immutability is not a policy we remember to apply, it is
arithmetic (`SPEC-001`). Mechanical PLM achieves the same guarantee by process and access
control (release locks the object); we achieve it cryptographically. Ours is stronger: a
PLM admin can force-edit a released object and break history; a sha256 collision is not on
the table. **Keep this. It is the best thing we have.**

### 2.4 Effectivity — how a revision becomes "the one you build"

A subtlety letters alone don't capture: multiple revisions can be simultaneously *valid*,
each for a different window or unit range. **Effectivity** is the rule that says which
revision applies:

- **Date effectivity** — Rev C is effective from 2026-03-01; before that date, Rev B.
- **Unit/serial effectivity** — Rev C applies from serial number 1050 onward; units
  1–1049 were built to Rev B and are *correct as built*.
- **Lot / block effectivity** — common in aerospace, by production block.

Effectivity is why "latest revision" is the wrong default question. The right question is
"which revision is effective *for this unit / on this date*." A field unit built to Rev B
is not defective because Rev C exists; it is a Rev-B unit and its spec sheet is the Rev-B
spec sheet. (Reporting: this is standard configuration-management practice.)

### 2.5 How a change propagates to assemblies that used the old revision

When part P goes from Rev B to Rev C, every assembly whose BOM referenced P must be
considered. Two sub-questions:

1. **Does the BOM reference float or pin?** Many BOMs reference a part *without* a
   revision ("use the current released rev of P"), in which case the assembly picks up
   Rev C automatically on its next build — convenient, and dangerous, because the assembly
   changed without anyone touching it. Others **pin** a specific revision ("this assembly
   uses P Rev B"), in which case moving to Rev C is a deliberate act that itself requires a
   change to the assembly. Aerospace leans heavily toward *pinning* for anything
   flight-critical; consumer goods often float.
2. **The change order decides the rollup.** The engineering change (§4) that released P
   Rev C includes an **impact analysis**: a *where-used* query (§3.3) finds every assembly
   that uses P, and the change board decides for each whether the parent must also rev, and
   sets the effectivity.

**For us:** our `Ref` always pins (namespace+kind+id+**version**), so we are a pinned
system by construction — an assembly references an exact immutable version of its part,
never "current". That is the safe default and matches aerospace practice. We will *also*
need a "resolve latest effective revision of `id`" query for the design-time convenience of
floating, but it must be an explicit, logged operation, never the silent default. The
`predecessor` digest gives us the revision chain for free; "latest" is a walk forward from
a record following `predecessor` links in reverse.

---

## 3. Bill of Materials (BOM)

The BOM is the structured list of what a thing is made of. It sounds trivial and is one of
the richest objects in the whole system.

### 3.1 Multi-level BOMs

A BOM is a tree (strictly, a directed acyclic graph — a standard part appears under many
parents). Levels:

- **Single-level BOM** — the immediate children of one assembly and their quantities.
- **Multi-level / indented BOM** — the full explosion down to raw material, with
  indentation showing depth.
- **Summarized / flattened BOM** — total quantity of each leaf part across the whole
  product, regardless of where it appears (what purchasing actually buys).

Quantities, units of measure, reference designators (which *instance* — "R47" on a board),
and find numbers (the item's line number on the parent drawing) all live on the BOM lines,
not on the parts.

### 3.2 BOM vs the CAD assembly tree — why both exist

This is a subtle and important point and software-origin people routinely miss it. The CAD
assembly structure (the mates/constraints tree in the CAD file) and the BOM look similar
and are **not the same object**, and mature PLM keeps both:

- The **CAD assembly tree** is a *geometric* model: it exists to position solids in space,
  capture mates, and let you visualise and check interference. It contains things that are
  not "parts you buy or make" (construction geometry, skeletons, mirror/pattern instances)
  and omits things that have no geometry (grease, paint, adhesive, software load, test
  requirement, a torque spec).
- The **BOM** is a *manufacturing/procurement* model: it exists to tell you what to buy,
  make, and assemble, in what quantity. It contains the no-geometry items the CAD tree
  can't hold and collapses/omits the geometry-only artifacts the CAD tree needs.

So the BOM is *derived from* but *deliberately divergent from* the CAD tree. The mapping
is a managed transformation (often called "CAD BOM → EBOM → MBOM"): the **EBOM**
(engineering BOM) is how the designer sees the product; the **MBOM** (manufacturing BOM) is
reorganised for how it's actually built (by assembly station, with consumables and
packaging added, geometry-only nodes removed). Confusing the two, or trying to force one
tree to serve both masters, is a classic and expensive mistake.

**For biology, this distinction is a gift and we should adopt it explicitly** (design
proposal, not reported practice): the "CAD tree" analogue — the structural/spatial model
of a protein complex or an assembly — is not the same as the "build BOM" — the ordered
list of what you synthesise, express, purify, and combine, which includes no-geometry
items (a buffer, an induction condition, a chaperone co-expression, a QC assay) that have
no place in a structure viewer. Keep two linked trees, not one overloaded one. (Flagged as
proposal: no biology PLM I know ships this today.)

### 3.3 Where-used (the reverse query)

The inverse of "what is this made of" is **"what is this used in."** Where-used walks the
BOM graph upward: given part P, find every assembly that contains it, at any level. This is
the single most important query for change impact (§4): before you touch P you must know
everyone who depends on P. A system that can go down (explode) but not up (where-used) is
half a system.

Our edge model gives us where-used naturally: typed edges between records are traversable
in both directions, so "what references this version" is a reverse-edge scan. We must make
sure the engineering-assembly edges are indexed for reverse lookup from day one.

### 3.4 Phantom assemblies

A **phantom** (or "pseudo") assembly is a BOM node that exists for engineering
organisation but is **never built or stocked as a discrete thing** — it's a logical
grouping that gets consumed straight into its parent. Example: "fastener kit" grouping six
screws conceptually, but on the floor the screws go straight onto the product; the kit is
never a box on a shelf. PLM/ERP flag it `phantom` so the explosion *blows through* it:
material planning sees the children, not the phantom. Biology analogue (proposal): a
logical grouping like "the three subunits that are always co-expressed" may be a phantom —
useful in the design tree, never a stocked standalone artifact.

### 3.5 Make vs buy

Every BOM line is flagged **make** (we fabricate it) or **buy** (we procure it). This
drives everything downstream: a buy part needs an **approved manufacturer list (AML)** and
**approved vendor list (AVL)** and a spec that a supplier can quote against; a make part
needs a process/route. The make/buy line is also an organisational boundary — buy parts
you specify by *interface and performance*, make parts you specify by *construction*. For
us: a "buy" bio-part is one you order (a synthesised gene fragment from a vendor, an
off-the-shelf strain); a "make" part is one you build in-house. The spec sheet differs
accordingly — a buy part's sheet is an acceptance spec, a make part's is a build spec.

### 3.6 Alternates and substitutes

- An **alternate** is a part that is *always* acceptable in a given position — fully
  interchangeable, pre-approved, interchangeable in both directions. Often a
  second-source of an identical component.
- A **substitute** is acceptable *conditionally* — "you may use B where A is specified, but
  only if A is unavailable, and B may have a restriction (e.g. not for the high-temp
  variant)." Substitution is directional and caveated.

The distinction maps onto FFF (§1.4): alternates are FFF-equivalent; substitutes are
"close enough under stated conditions." Encoding *why* a substitute is conditional (the
restriction) is as important as listing it. Biology will lean on this heavily because
"equivalent" is almost never unconditional (§10) — most biological "alternates" are really
substitutes with context restrictions, and we should default to the substitute model with
explicit conditions rather than claiming true alternates.

---

## 4. Engineering change: ECR / ECO and the control of change

Change is the heart of PLM. Everything above (immutable revisions, where-used, effectivity)
exists to make *controlled change* possible. The workflow is near-universal, though names
vary by vendor and by the governing standard (SAE/EIA-649 is the civilian configuration
management consensus standard; MIL-STD-973 was the older defense one it largely
superseded).

### 4.1 The three-stage flow

1. **ECR — Engineering Change Request** (also "problem report," "change request"). Someone
   proposes *that* something should change and *why*. An ECR is a question: here is a
   problem or an opportunity, should we act? It is cheap, it does not authorise any change,
   and many ECRs are rejected or merged. The ECR captures the problem statement, the
   affected items (first guess), the justification, urgency, and a rough cost/impact.
2. **ECO — Engineering Change Order** (also ECN, Engineering Change Notice — some shops
   distinguish ECO = the authorisation, ECN = the notification; many conflate them). The
   ECO is the *authorised, detailed plan to change*: exactly which parts go to which new
   revision, what the new content is, the **disposition of existing stock** (use-as-is,
   rework, scrap, return to vendor), the **effectivity** (§2.4), and the approvals. An
   approved ECO is the thing that actually mints new revisions.
3. **ECN — the notification** that the change is released, pushed to everyone affected.

Some systems add an **ECA (Engineering Change Assessment)** step between R and O for the
impact analysis.

### 4.2 Impact analysis

Before an ECO is approved, someone runs the impact analysis, and this is where the earlier
machinery pays off:

- **Where-used** (§3.3) finds every parent assembly and product affected.
- For each, decide: does it also need to re-rev? (A fit change to a child almost always
  forces the parent to rev; a pure internal change may not.)
- **Stock disposition**: what do we do with the N units already built to the old rev and
  the M in the warehouse? Use-as-is / rework / scrap. This is often the most expensive part
  of the whole change and is frequently underestimated.
- **In-flight work**: POs open against the old rev, WIP on the floor.
- **Cost and schedule** of the change itself.

### 4.3 Approval gates

The ECO routes through a **Change Review Board / Change Control Board (CCB)** — the
cross-functional group (engineering, manufacturing, quality, purchasing, sometimes the
customer) that has authority to approve. Gates are explicit: an ECO cannot release until
the required signatures are present. The board exists precisely so that no single engineer
can unilaterally change a released part — change authority is a *shared, logged* act. This
is the same reason our contribution lifecycle (`SPEC-002`) separates "schema-valid" from
"reviewed/accepted": validity is mechanical, acceptance is a governed decision by named
reviewers. We already have the shape of a CCB.

### 4.4 What gets frozen when

The crucial sequencing:

- **Working versions are fluid** until the ECO is approved. You iterate freely.
- **At ECO approval / release, the new revision is frozen** — becomes immutable, gets its
  letter, and the effectivity clock starts.
- **The old revision was already frozen** at its own release and stays exactly as it was,
  forever, as the record of what was built before the change.

So at any moment the system contains a stack of frozen released revisions (the history, all
immutable) plus at most one fluid working version per part (the in-progress next rev). The
freeze boundary is the release event. Our content-addressing makes "frozen" free (every
committed record is immutable); what we must *add* is the governed release event that
promotes a working draft to "released revision" status and records the approval — the ECO
is a first-class record type we should define, not an afterthought.

**For us (proposal):** model ECR and ECO as record kinds with typed edges to the artifacts
they change. An ECO record should carry: the affected `Ref`s (old versions), the new
versions it authorises, the disposition, the effectivity, and the reviewer approvals. Then
"why does this part exist in this form" is answerable by walking from any released version
back through the ECO that released it to the ECR that motivated it — full design
provenance, which biology needs even more than mechanical engineering does.

---

## 5. Spec sheets and characterisation — the engineering datasheet

The spec sheet (datasheet) is where the part makes its *promises*. This is the heart of
what we are trying to build for biology, so it's worth dissecting what makes a real
engineering datasheet trustworthy.

### 5.1 Anatomy of a real datasheet

Take three real exemplars and what they share:

- A **rolling-element bearing** datasheet: bore/OD/width (with tolerance classes per ISO
  492 / ABEC), dynamic load rating C and static rating C₀, limiting speed and reference
  speed, preload class, and an **L10 life** figure — the life (in revolutions or hours)
  that 90 % of a population will meet or exceed under a stated load. Note the life is
  *explicitly a 90th-percentile statistic*, not a guarantee for any individual bearing.
- An **operational amplifier** datasheet (e.g. a classic precision op-amp): a table of
  parameters each given as **min / typ / max** over a stated temperature range, with the
  **test conditions** for each line; "Absolute Maximum Ratings" (exceed and you may destroy
  it) kept separate from "Recommended Operating Conditions"; and curves — gain vs
  frequency, offset drift vs temperature, etc.
- A **linear actuator / motor** datasheet: rated force/torque, stroke, duty cycle,
  **derating curve** (allowable continuous force falls as speed or ambient temperature
  rises), and a safe-operating-area plot.

### 5.2 The fields that make a datasheet trustworthy

Common structure, and this is the checklist we should steal almost verbatim:

1. **Nominal / typical value** — the headline number. By itself it is nearly useless.
2. **Tolerance** — the band around nominal (±, or a class). *A number without a tolerance
   is not an engineering spec, it's a wish.* This is the line software people most often
   omit.
3. **Min / typ / max** — not just nominal; the guaranteed bounds. "Typ" is informational
   (often a population mean, not guaranteed); **min and max are the actual promises**.
4. **Operating envelope / recommended operating conditions** — the region within which the
   other numbers hold (temperature, voltage, load, humidity…). Every spec is conditional on
   staying in the envelope.
5. **Absolute maximum ratings** — the "beyond here, damage/undefined" boundary, kept
   rigorously separate from the operating envelope. Operating up to the abs-max is *not*
   allowed; it's the destruction line.
6. **Derating curves** — how a rating must be reduced as a condition worsens (temperature,
   duty cycle, altitude). The flat headline number only applies at the nominal condition.
7. **Test conditions** — *every* number states how it was measured (at what temperature,
   load, frequency, with what fixture). A spec without its test condition is unreproducible
   and therefore untrustworthy.
8. **Qualification status** — what testing the part has passed (automotive AEC-Q100,
   MIL-PRF, a specific qual report), i.e. *how much to trust the numbers* and under what
   regime they were validated.
9. **Failure modes** — how it fails, not just that it works: open vs short, wear-out
   mechanism, FIT rate (failures per 10⁹ hours), and for safety work an FMEA reference.

### 5.3 What makes it *trustworthy* specifically

Trust comes from three things the good datasheets all do:

- **Every claim is conditional and the conditions are stated.** No naked numbers.
- **Guarantees (min/max) are distinguished from information (typ).** The reader knows
  which numbers they can design against and which are just descriptive.
- **The measurement is reproducible** — test conditions are given precisely enough that an
  independent lab can reproduce the figure. (This is identical to our repository's whole
  stance that a record is "schema-valid is not a scientific claim" and that evidence must
  carry its source and conditions — `SPEC-001`.)

**For us:** the bio-part spec sheet should be structured exactly this way — nominal value,
tolerance/distribution, operating envelope (buffer, temperature, pH, host, expression
system), the equivalent of absolute-maximum ("denatures above / aggregates above"),
derating (activity vs temperature *is* a derating curve), test conditions (assay, construct,
conditions — mandatory on every number), qualification status, and failure modes. §10
argues that the single biggest adaptation we must make is that for biology **"typ/min/max"
becomes a full distribution and "tolerance" becomes a confidence statement**, because the
numbers are intrinsically stochastic and context-dependent — but the *skeleton* of the
datasheet transfers almost perfectly.

---

## 6. Interfaces and fits — the part software-origin systems get wrong

This is the section to read twice. Mechanical engineering has a deep, formal language for
how two parts *mate*, and software-origin systems (including most bio-"CAD") have nothing
equivalent and don't know they're missing it. Getting identity and revisions right but
having no interface model is building a parts library that can't actually be assembled.

### 6.1 The problem interfaces solve

A part number promises form/fit/function (§1.4). "Fit" means it must mate with its
neighbours. But "a 10 mm shaft in a 10 mm hole" doesn't fit — *nominally identical sizes
cannot assemble*. You need the **allowances and tolerances** that say how much clearance or
interference there is. The interface is a *contract between two parts*, and it must be
specified on both sides consistently or nothing assembles.

### 6.2 Datums

A **datum** is a theoretically exact reference (a point, axis, or plane) from which other
features are located and measured. Datums establish the coordinate frame a part is
inspected and mated in. Picking datums is a real engineering decision: the datum scheme
should reflect how the part actually seats in its assembly (the "functional datum"), so
that the way you measure the part matches the way it's used. Get the datums wrong and two
parts that both "pass inspection" still won't assemble, because they were measured from
different references.

### 6.3 GD&T — Geometric Dimensioning and Tolerancing

**GD&T** is the formal symbolic language for specifying allowable variation in *geometry*
— not just size, but form (flatness, straightness, circularity), orientation
(perpendicularity, angularity, parallelism), location (position, concentricity), and runout.
It is standardized in **ASME Y14.5** (the US standard; the 2018 edition is current as of
this writing) and in the **ISO GPS** (Geometrical Product Specifications) series on the ISO
side. The key ideas:

- **Feature control frames** attach a geometric tolerance to a feature with reference to
  datums: "this hole's axis must lie within a 0.1 mm cylindrical zone, located relative to
  datums A, B, C."
- **Maximum/least material condition (MMC/LMC)** and **bonus tolerance** let the allowable
  positional error depend on the actual size — a powerful idea that lets more parts pass
  while still guaranteeing assembly.
- GD&T specifies *function*, not just dimensions: it says what variation is acceptable
  *for the part to do its job*, which is exactly the right framing.

You do not need to master GD&T to design our system, but you must absorb the *principle*:
**the interface is specified by a tolerance zone and a reference frame, agreed by both
mating parts, in a formal language** — not by eyeballing that two numbers are equal.

### 6.4 Tolerance stack-up

When parts chain together (part A locates B locates C), the individual tolerances
*accumulate*. **Tolerance stack-up analysis** computes whether, in the worst combination
of allowed variations, the assembly still works. Two methods:

- **Worst-case stack** — sum the extremes; guarantees assembly but is pessimistic and
  expensive (demands tight tolerances everywhere).
- **Statistical (RSS, root-sum-square) stack** — combine tolerances as a statistical
  distribution; accepts a small, quantified probability of a bad assembly in exchange for
  looser, cheaper tolerances. (Note this is *already* a probabilistic acceptance of failure
  — mechanical engineering is not actually as deterministic as it looks; see §10, this is a
  bridge to biology, not a contrast with it.)

The lesson: **variation propagates through assemblies and must be analysed end-to-end, not
part-by-part.** A library of parts that each meet their own spec can still produce an
assembly that fails, if nobody did the stack-up.

### 6.5 Interface Control Documents (ICDs)

At the system level, the mating contract is captured in an **Interface Control Document** —
a controlled artifact owned jointly by the two sides of an interface (two subsystems, two
organisations) that specifies *everything* crossing the boundary: mechanical (bolt
pattern, envelope, loads), electrical (pinout, voltage), data (protocol), thermal, etc. The
ICD is itself revision-controlled and change-managed like a part. Its whole reason to exist:
let two teams work independently as long as they both honour the interface, and make any
change to the interface a visible, negotiated, controlled event. This is how large systems
(a satellite, an aircraft) are built by many teams without constant collision.

**For us — the hard, important adaptation.** Biological "parts" mate too, and we have *no*
GD&T for them, and this is exactly where a naive bio-CAD fails. The mating contracts are
real: a protein-protein binding interface (shape + chemistry complementarity, Kd,
on/off-rates), a promoter-polymerase interface, a ribosome-binding-site/translation
interface, a scaffold-domain attachment, a protein-small-molecule pocket. Each is a
*contract between two parts specified on both sides*. We should (proposal) define the
analogue of an ICD — call it a **Binding/Interface Control record** — that both parts
reference, that specifies the interface in whatever formal terms biology allows (binding
constants with conditions, structural complementarity, orthogonality to other interfaces),
and that is itself revision-controlled. And we must recognise that the "tolerance" on a
biological interface is a *distribution of binding affinity under context*, and that
biological tolerance stack-up (does this whole pathway still function when every component
is at the edge of its distribution, in this cell state?) is a real and largely unsolved
analysis. §10 returns to why GD&T's precise geometry does *not* transfer even though its
*philosophy* does. Flag: the ICD-for-biology idea is a design proposal; I am not aware of a
production bio-PLM that ships interface control documents today.

---

## 7. Configuration management: baselines, variants, families

Configuration management (CM) is the discipline of knowing *exactly what a given product
configuration consists of* and controlling how it changes. The civilian consensus standard
is **SAE/EIA-649** (currently EIA-649C, 2019; it uses deliberately *neutral* terminology
and lists equivalent terms from different industries); defense historically used
**MIL-STD-973** and related. The core concepts:

### 7.1 Baselines

A **baseline** is a *named, frozen, agreed-upon snapshot* of the complete configuration at
a point in time — every part at a specific revision, the full BOM, the interface docs —
that becomes the reference for future change. Classic baselines in a program:

- **Functional baseline** — the agreed requirements/spec.
- **Allocated baseline** — requirements allocated to subsystems.
- **Product baseline** — the complete as-designed definition (all parts, all revs).
- **As-built / as-maintained** — what was actually manufactured / what's in the field now
  (which drifts from as-designed via approved variances, §7.5).

A baseline is exactly a *tag* in version-control terms: a named pointer to a consistent set
of specific versions. Our content-addressed store can represent a baseline cleanly as an
immutable record that lists a set of `Ref`s (pinned versions) — a "bundle" in our existing
vocabulary (`SPEC-004`) is very nearly a baseline already.

### 7.2 Variants and the parametric part family

Most "different" parts are the same part with a parameter changed: a bracket in three
lengths, a bolt in twelve lengths. Two ways to manage this:

- **Discrete part numbers per variant** — each length is its own part number with its own
  spec. Simple, explicit, but the item master explodes.
- **Parametric part family (a "family table" / "table-driven part")** — one generic part
  definition with a table of parameter sets, each row a variant. Teamcenter, Windchill,
  SOLIDWORKS (design tables), Creo (family tables) all support this. The family captures
  "these are all the same design, differing only in these parameters," which is both more
  compact and more *honest* about the relationship.

The tension: a family table says "these are siblings," but each variant still needs a
real, orderable, spec'd identity (you buy an M6×20, not "the bolt family"). Mature practice:
the family is a design-time organising structure; each released variant still gets its own
part number and spec. Family ≠ part number.

### 7.3 Configuration rules (options and variants / the "150 % BOM")

For configurable products (a car with options, a server with build-to-order), you don't
enumerate every possible finished configuration. Instead you keep a **generic / "150 %"
BOM** (a superset containing *every* possible component) plus **configuration rules** —
logical constraints ("if engine = V8 then radiator = large," "option A excludes option B")
— and a **configurator** that resolves a chosen option set into a specific valid **100 %
BOM**. This separates the space of possibilities (the superset + rules) from a realised
instance (one resolved configuration). Dassault/Siemens/Oracle all have variant
configurators built on this.

**For us (proposal):** this maps beautifully onto combinatorial biological design. A
"150 % BOM" is a design space — all candidate promoters × RBSs × CDSs × terminators — with
**configuration rules** encoding incompatibilities (orthogonality constraints, toxic
combinations, host incompatibilities, repeated-sequence prohibitions that break synthesis).
A configurator resolves a design intent into a specific, buildable construct. This is
arguably a *better* fit for biology than for mechanical engineering, because biological
design is so combinatorial. Flagged as proposal.

### 7.4 Parametric families vs variants — don't conflate with revision

A variant (a different length) is a *different part*, not a *revision* of another. This
trips people up: Rev B is "the same part, improved"; the 25 mm vs the 30 mm bracket are
"two different parts in a family." Keep the family axis (which sibling) orthogonal to the
revision axis (which generation of a given sibling). Our model handles this cleanly because
family membership is just a typed edge, independent of the `predecessor`/version chain.

### 7.5 Variances (deviations / waivers)

Reality diverges from the baseline in controlled ways. A **variance** — EIA-649's neutral
term for what used to be split into **deviation** (authorised *before* manufacture: "we
know this lot will be out of spec on X, approved in advance") and **waiver** (authorised
*after*: "these units came out of spec on X, accepted as-is") — is a *logged, approved,
bounded* permission to depart from the released configuration without re-releasing it. The
point is that the departure is *recorded and authorised*, not silent. The as-built baseline
is the as-designed baseline plus the accumulated approved variances.

**For biology this is enormous** (and more a reported-practice lesson than a proposal):
every build will diverge from its design (a point mutation acquired in cloning, a titre
below target, a truncation). The mechanical-CM answer is not "fail the part" and not
"pretend it's fine" — it is a *variance*: an approved, logged, bounded record of the
divergence attached to that specific build. We should adopt the variance concept wholesale.
It is exactly the right model for the gap between a designed sequence and an as-built clone.

---

## 8. The data layer: formats, representations, and branching

How the geometry/design data is actually represented and exchanged — and the cloud-CAD
branching story, which is the closest existing thing to what we're building.

### 8.1 Neutral exchange formats

CAD vendors' native formats are proprietary and incompatible, so neutral formats exist to
move data between them and to archive it:

- **STEP (ISO 10303)** — the big one. The relevant application protocol is **AP242**
  ("Managed model-based 3D engineering"), which merged the older AP203 (configuration-
  controlled design) and AP214 (automotive) and crucially carries not just geometry but
  **PMI** (Product and Manufacturing Information — including GD&T), assembly structure, and
  configuration/management data. AP242 is the modern target for a vendor-neutral digital
  definition. (Edition 3 was published December 2022; a further revision was in the ISO
  pipeline as of late 2024 — cite the edition you use.) The breadth of AP242 is the lesson:
  a neutral format worth having carries *the management and tolerance data, not just the
  shape.*
- **JT (ISO 14306)** — a lightweight format for visualisation, large-assembly review, and
  digital mock-up; much smaller than full STEP, used where you need to *look at* and
  navigate huge assemblies, not re-manufacture them.

The lesson for us: there will be pressure to store only the "shape" (the sequence /
structure) and treat the management data as secondary. AP242's whole design says the
opposite — **the neutral, archival, exchangeable artifact must carry identity, revision,
tolerance, and configuration, or it's not a usable engineering definition.** Our records
already bundle payload + identity + provenance in one canonical, hashable envelope; that is
the AP242 instinct, and we should resist any move to split "the sequence" from "the record."

### 8.2 How the geometry is represented: feature tree vs B-rep

Two layers, and the distinction maps onto a real tension we'll feel:

- **Boundary representation (B-rep)** — the *explicit* geometry: the actual surfaces,
  edges, and vertices that bound the solid. It's the "what the shape is now" — unambiguous,
  but it doesn't record *how* you got there or *why* any face is where it is.
- **Feature tree (parametric history / procedural model)** — the *recipe*: an ordered list
  of operations (extrude this sketch 10 mm, fillet that edge 2 mm, pattern this hole 6
  times) with **parametric constraints** (dimensions and relations) that, when *replayed by
  a constraint solver*, regenerate the B-rep. Edit a parameter and the whole model
  recomputes. This is the dominant paradigm (SOLIDWORKS, Creo, Inventor, NX, Fusion,
  Onshape).

The feature tree is more powerful (change-friendly, captures design intent) but more
fragile: edits can break downstream features ("the fillet failed because the edge it
referenced no longer exists"), and the model's behaviour depends on the solver and feature
order.

### 8.3 Why direct modelling emerged

**Direct modelling** (push/pull on the B-rep, no history tree) emerged precisely because
the parametric feature tree becomes brittle and opaque on big models and on *imported*
geometry (a STEP file you receive has no feature tree — it's dumb B-rep, and direct
modelling lets you edit it anyway). The trade-off is explicit: parametric history gives
you *intent and repeatable change* at the cost of *fragility*; direct modelling gives you
*robust local edits* at the cost of *losing the recipe*. Mature tools now offer both and
let you mix.

**The analogy worth holding (flagged as analogy, not reported practice):** a biological
design has the same two layers. The "B-rep" is the explicit artifact — the final sequence,
the solved structure, the thing you actually build. The "feature tree" is the *design
recipe* — the intent and the parametric operations that produced it ("take this parent
scaffold, graft this loop, back-mutate these two positions, optimise codons for this
host"). We want *both*: the explicit sequence (so you can build and hash it) **and** the
procedural history (so you can change the design intent and regenerate, and so you can
answer "why is residue 47 a tryptophan"). And we will feel the same fragility problem:
change an upstream design decision and the downstream grafts may no longer make sense. Our
`predecessor` chain captures the linear history but not yet the *parametric recipe*; that
is a gap worth a design.

### 8.4 Cloud CAD branching and merging — Onshape vs git

Onshape is the one mainstream CAD system built cloud-native with explicit **branching and
merging**, and it's the closest existing analogue to the git-like model our repository
already uses — so it's worth being precise about how it works and where it differs from git.

What Onshape actually does (per its own docs and tech tips):

- A document has a version graph; you can **branch** a workspace, work independently, and
  **merge** back. Merge is offered for Part Studios and Assemblies (and per-tab), and a
  "selective merge" (from v1.151 on) lets you accept or keep changes per item.
- On merge, Onshape **identifies geometric conflicts at the feature level before merging**
  and *will not* apply changes to features that conflict — it flags them (highlighted red)
  for manual resolution rather than silently combining. Deletions in the target are
  honoured over edits in the source. Branches on outdated FeatureScript versions can't be
  merged; protected branches must be kept up to date before merge.

How that compares to git:

| | git | Onshape |
|---|---|---|
| Unit of change | text lines | CAD features / tabs |
| Merge basis | 3-way text diff | feature-level, intent-aware |
| Conflict detection | overlapping line hunks | *geometric* conflicts between features |
| Auto-merge | textual, can produce a broken-but-"merged" file | refuses to merge conflicting features; keeps model valid |
| Semantics | none — git doesn't know what a line means | the merge understands it's merging geometry |

The deep point: **git merges *representations* (lines) with no understanding of meaning;
Onshape merges *domain objects* (features) with domain-aware conflict detection.** git will
happily produce a syntactically merged file that is semantically nonsense; Onshape refuses
to merge features it can't reconcile, keeping the model valid at the cost of requiring more
manual resolution.

**For us — the most directly applicable lesson in the whole document.** We already have a
git-like content-addressed, immutable-version, predecessor-linked model. The Onshape lesson
is that for a *domain* object, line-diff merging is the wrong primitive: a biological design
should merge at the level of *features/parts* (this domain was swapped, this RBS was
retuned), with **domain-aware conflict detection** — two branches that both edited the same
binding interface is a conflict even if the sequence edits don't textually overlap, and two
branches that edited unrelated domains can merge even if they're near each other in the
sequence string. If we ever merge biological designs by diffing sequence strings, we will
produce the biological equivalent of a syntactically-merged-but-nonsense file. Merge the
parts, not the characters. (This is a design recommendation by analogy; Onshape does it for
geometry, nobody I know does it for sequence.)

---

## 9. Real systems: what they get right and what practitioners complain about

Honest, practitioner-level read on the major PLM/CAD-data systems. Treat the complaints as
widely-reported sentiment, not as a controlled survey.

- **Siemens Teamcenter** — the heavyweight incumbent; enormously capable, deep BOM/change/
  configuration management, strong multi-CAD. *Gets right:* scale, depth, aerospace/auto
  credibility. *Complaints:* complex and expensive to deploy and customise; needs a
  dedicated admin team; the UI is dated; "you'll spend years and a fortune configuring it."
- **PTC Windchill** — the other heavyweight; strong change management and tight Creo
  integration, increasingly SaaS. *Gets right:* robust change/config control, mature.
  *Complaints:* heavy, similar cost/complexity story, customisation lock-in.
- **Aras Innovator** — notable for a **low-code, highly customisable** platform with a
  model-driven architecture, and a distinctive commercial model (the core is available
  without per-seat license fees; you pay for subscription/support/enterprise features).
  *Gets right:* flexibility — you can model your own item types and workflows; a modern
  architecture. *Complaints:* that flexibility means you build a lot yourself; needs skilled
  people to realise the promise.
- **Dassault 3DEXPERIENCE** — a unified platform spanning CATIA/SOLIDWORKS/ENOVIA/
  SIMULIA on one data backbone. *Gets right:* integration breadth, single data model across
  design-simulation-manufacturing. *Complaints:* can feel monolithic and all-in; migration
  and cost; cloud/licensing friction.
- **Onshape (PTC)** — cloud-native CAD + lightweight data management with the branching/
  merging and built-in versioning discussed in §8.4. *Gets right:* real version control and
  collaboration done natively (no "check-in/check-out of files on a share"); nothing to
  install; the branching model. *Complaints:* subscription-only / data lives in the cloud;
  lighter on heavy enterprise PLM features than the incumbents; feature set still maturing
  vs desktop CAD in some areas.
- **Duro** — a modern **cloud, PLM-first** system aimed at hardware startups, strong on
  part numbering, BOM, and change management without the Teamcenter weight; relaunched in
  2025 as "Duro Design" (cloud/AI-native) and, per a lightly-sourced report, acquired by
  Altium in December 2025 (treat the acquisition as not firmly confirmed). *Gets right:*
  fast to stand up, opinionated, good BOM/part-number hygiene for small teams. *Complaints:*
  less depth than enterprise PLM; startup-stage maturity/roadmap risk.
- **OpenBOM** — lightweight, spreadsheet-friendly, cloud BOM and inventory management with
  many CAD connectors; aimed at the "we just need BOM and part management without a PLM
  monster" segment. *Gets right:* low barrier, real-time collaborative BOM, easy CAD
  plug-ins. *Complaints:* lighter on formal change-control/configuration-management rigour;
  can feel like "managed spreadsheets" as you scale.

**Cross-cutting lesson for us.** The consistent practitioner story is a spectrum from
*heavy-but-complete-and-painful* (Teamcenter, Windchill, 3DEXPERIENCE) to
*light-and-pleasant-but-shallow* (OpenBOM, early Duro), with Aras (flexible platform) and
Onshape (version control done right) as the interesting middles. The thing *everyone*
agrees matters and *everyone* finds hard is **change management and configuration control
done rigorously without crushing the user**. That is exactly the needle we have to thread,
and it argues for: rigorous immutable-identity and change semantics *in the core* (we have
this), with a deliberately light, opinionated surface — not a configurable everything-engine
that takes a team of admins to run.

---

## 10. The translation to biology: where the analogy holds and where it breaks

This is the most important section. The previous nine sections are reporting (with proposals
flagged). This section is mostly *reasoning by analogy*, and I will say so sentence by
sentence. The thesis: **the identity / revision / change / configuration / provenance
machinery transfers almost perfectly; the "part behaves like a machined solid" assumptions
underneath datasheets and GD&T transfer badly and are actively dangerous if imported
naively.**

A protein is not a bearing. It has no machining tolerance, its behaviour is
context-dependent, and its "qualification" is a probability. Let's be specific about which
is which.

### 10.1 What transfers cleanly (high confidence, mostly structural)

These are management-layer concepts that are substrate-independent — they're about
*information discipline*, not about physics, so biology inherits them with little change:

- **Non-intelligent, permanent, system-assigned identifiers** (§1). *Transfers cleanly.* A
  biological part needs a meaningless permanent key with all meaning in attributes, for the
  exact same reasons — classifications (what family, what host, what function) change and
  must not be welded to the key. (This is an argument by direct analogy, but a strong one:
  the failure modes of smart numbers are about information management, which doesn't care
  that the part is a protein.)
- **Immutable released revisions** (§2). *Transfers cleanly — arguably more important here.*
  A released, qualified biological design must be frozen, because experiments, publications,
  and downstream designs reference it. Our content-addressing already enforces this and it's
  the right call.
- **Effectivity and the "which revision for this unit" question** (§2.4). *Transfers*, and
  maps onto "which design generation was this strain/batch built to."
- **BOM, multi-level, where-used, phantom, make/buy, alternates/substitutes** (§3).
  *Transfers*, with the proviso that *substitute* (conditional) is the common case and true
  *alternate* (unconditional equivalence) is rare (see §10.3).
- **ECR/ECO change control with impact analysis and a review board** (§4). *Transfers
  cleanly* and we already have the governance shape (`SPEC-002`). Design provenance — "why
  is this part this way" answerable by walking back through the changes — is something
  biology needs *more* than mechanical engineering, because biological rationale is
  subtle and easily lost.
- **Baselines, parametric families, configuration rules / the 150 % BOM** (§7). *Transfers*,
  and the combinatorial configurator is arguably a *better* fit for biology than for
  mechanics (§7.3) — flagged earlier as a proposal.
- **Variances / deviations / waivers** (§7.5). *Transfers cleanly and is essential* — the
  gap between designed sequence and as-built clone is exactly a variance, and the
  record-and-authorise (not fail, not ignore) discipline is precisely right.
- **The AP242 instinct that the archival artifact must carry management + tolerance data,
  not just shape** (§8.1). *Transfers cleanly* as a principle: store the record, not just
  the sequence.
- **Merge domain objects, not representations** (§8.4). *Transfers cleanly as a design
  rule* (by analogy to Onshape): merge parts/features, never raw sequence characters.

### 10.2 What transfers but must be reinterpreted (the datasheet, carefully)

The datasheet skeleton (§5) transfers — but three of its load-bearing assumptions must be
replaced, and this is reinterpretation, reasoned by analogy:

1. **Nominal + tolerance → distribution, not a band.** A machined dimension is a nominal
   with a symmetric-ish tolerance band and a stable, repeatable true value. A biological
   measurement (expression level, Kd, catalytic rate, fold-stability, fluorescence) is a
   *distribution* — often broad, often skewed, varying across cells in a clonal population
   even under identical conditions (gene-expression noise is intrinsic, not measurement
   error). So the datasheet field is not "10 mm ± 0.1" but a distribution with its spread,
   and the "tolerance" is a statement about the *population*, not a guarantee about an
   instance. *This is a reinterpretation, not a clean transfer: the field exists, its
   meaning changes.*
2. **Operating envelope → context, and context is far larger and less separable.** A
   bearing's envelope is a few axes (load, speed, temperature) that are largely independent.
   A protein's "envelope" includes host organism, growth phase, media, temperature, pH,
   crowding, the rest of the proteome, and *what else you co-expressed* — and these are
   **not separable**: the part's behaviour is a function of the whole system state, not a
   set of independent derating curves. A derating curve (activity vs temperature) *does*
   transfer and is genuinely useful; the assumption that the axes are independent and the
   envelope is low-dimensional does **not**. *Reinterpretation; and the non-separability is
   the dangerous part to import naively.*
3. **Qualification status → an explicit probability / confidence, not a pass/fail stamp.** A
   part that passed AEC-Q100 "is qualified." A biological design's qualification is
   inherently statistical: "folds and is active in 70 % of clones," "binds with Kd = X
   (95 % CI …) under conditions Y." The datasheet's "qualification status" field survives
   but its *type* changes from a categorical stamp to a probability with conditions. *This
   is the sharpest reinterpretation and the one the brief itself names: qualification is a
   probability.* Our repository's existing stance — that schema-validity is not a truth
   claim and evidence carries its conditions — already leans this way (`SPEC-001`).

The reassuring part: mechanical engineering is *already* partly statistical (bearing L10
life is a 10th-percentile, RSS tolerance stack-up accepts a quantified failure probability,
§6.4). So this is not biology being alien and mechanics being deterministic — it's a
*difference of degree*, and the mechanical world already has the vocabulary (percentile
life, statistical tolerancing) we can extend. *(That mechanical specs are already
probabilistic is reported fact; that this makes the bridge to biology easier is my
analysis.)*

### 10.3 What is actively misleading and should NOT be imported naively

These are the places where a borrowed concept is worse than none, because it imports a false
assumption. All of this subsection is reasoning/analysis, not reported practice, and I'll say
so:

1. **GD&T's precise geometric tolerancing does not transfer, even though its philosophy
   does.** *(Analysis.)* GD&T works because a machined part has a *stable, measurable,
   exact geometry* against *fixed datums*, and "within 0.1 mm of nominal position" is a
   meaningful, inspectable statement. A protein has no fixed geometry — it's a conformational
   *ensemble*, it breathes, it folds differently in different contexts, and there is no
   rigid datum frame to measure from. Importing "specify the interface as a geometric
   tolerance zone" literally would be a category error. What transfers is the *philosophy*
   (§6): interfaces are contracts, specified on both sides, in a formal language, and
   variation propagates and must be analysed end-to-end. The *formalism* (tolerance zones,
   datums, feature control frames) must be replaced by a biology-appropriate one (binding
   constants with conditions, structural complementarity, orthogonality) — not borrowed.
   Pretending a protein interface has a GD&T-style tolerance would encode a precision that
   doesn't exist. **This is the trap §6 warned about, now stated fully.**

2. **Strict Form/Fit/Function interchangeability (§1.4) largely breaks, and leaning on it
   naively is dangerous.** *(Analysis.)* FFF assumes you can decide, cleanly and in advance,
   whether a changed part is interchangeable with the old one — because a machined part's
   behaviour is stable and testable against a finite spec. A biological "part" changed by
   even a single residue may be interchangeable in context A and catastrophically not in
   context B, and you often *cannot know in advance* which. "Fully interchangeable, both
   directions, no adverse effect" is almost never establishable for a biological part
   because the set of contexts is open-ended. The consequence: the clean mechanical rule
   "FFF-equivalent ⇒ same part number, new revision; otherwise new part number" cannot be
   applied by judgment up front. Two safer adaptations (proposals): (a) default to
   *substitute-with-conditions* (§3.6) rather than claiming *alternate* / true
   interchangeability; and (b) tie the "same part vs new part" decision to *measured
   equivalence in a defined context set*, logged, rather than to an a-priori FFF judgment —
   and treat an equivalence claim as *contingent on the contexts tested*, never as universal.

3. **"Qualified" as a terminal, durable state is misleading.** *(Analysis.)* A qualified
   bearing stays qualified — its physics doesn't drift. A biological part's "qualification"
   is conditional on a context that can change (host background, growth conditions, the rest
   of the construct) and can be *silently invalidated* by a change elsewhere in the system
   that never touched the part. So qualification must carry its context and must be
   *revisitable* — a where-used-style propagation should be able to flag "this part's
   qualification may no longer hold because the system around it changed," which has no clean
   mechanical analogue. Importing "once qualified, always qualified" would be a real safety
   hazard.

4. **The BOM's clean "quantity of discrete interchangeable units" assumption weakens.**
   *(Analysis.)* A mechanical BOM line is "6 × M6 bolt, each identical and interchangeable."
   A biological "quantity" (copy number, expression level, stoichiometry of a complex) is
   itself a *distribution* and often a *controlled variable*, not a fixed integer of
   identical units, and the "units" (molecules) are not individually identical or
   individually addressable. The BOM structure (what's composed of what) transfers; the
   "N identical discrete interchangeable units" reading of the quantity field does not, and
   should be modelled as a target with a distribution, not a count.

5. **Deterministic, order-independent assembly does not hold.** *(Analysis.)* Mechanical
   assembly is largely deterministic and the *assembly guidelines* are a sequence of
   repeatable steps. Biological "assembly" (folding, complex formation, pathway function,
   integration into a living host) is stochastic, path- and context-dependent, and can fail
   or vary for reasons not captured in the parts list — the same parts in the same amounts
   may not yield the same working whole. So "assembly guidelines" transfer as a *concept*
   but must be understood as *conditions that raise the probability of the intended
   outcome*, not a deterministic build recipe — closer to a process spec with yields than to
   a mechanical assembly sequence.

### 10.4 Summary table

*(Reporting the structure of the analysis above; the right-hand judgments in the
reinterpret/misleading rows are my analysis, not established practice.)*

| CAD/PLM concept | Verdict for biology | One-line reason |
|---|---|---|
| Non-intelligent permanent IDs | **Transfers cleanly** | Information-management argument, substrate-independent |
| Immutable released revisions | **Transfers cleanly** | Downstream references must not silently change; we already hash |
| Effectivity | Transfers | "Which design generation was this strain built to" |
| BOM / where-used / phantom / make-buy | Transfers | Composition & impact structure is substrate-independent |
| ECR/ECO + review board + impact analysis | **Transfers cleanly** | Governed change & provenance; biology needs it more |
| Baselines / families / 150 % BOM + config rules | Transfers (good fit) | Combinatorial design suits a configurator |
| Variances (deviation/waiver) | **Transfers cleanly, essential** | The designed-vs-as-built gap *is* a variance |
| Datasheet skeleton | Transfers | The field structure is right |
| → nominal+tolerance | **Reinterpret** | Becomes a distribution, not a band |
| → operating envelope | **Reinterpret (careful)** | High-dimensional, non-separable context |
| → qualification status | **Reinterpret** | A probability with conditions, not a stamp |
| Derating curves | Transfers | Activity-vs-condition is a real derating curve |
| Interface-as-contract philosophy | Transfers | Interfaces are two-sided formal contracts |
| GD&T formalism (zones, datums) | **Actively misleading** | No fixed geometry or datum frame exists |
| Strict FFF interchangeability | **Actively misleading** | Context-openness defeats a-priori interchange judgment |
| "Qualified" as terminal state | **Actively misleading** | Context can silently invalidate it |
| BOM quantity = N identical units | **Reinterpret** | Quantity is a distribution / controlled variable |
| Deterministic assembly recipe | **Reinterpret** | Assembly is stochastic & context-dependent |
| Neutral format carries mgmt+tolerance (AP242) | Transfers (principle) | Store the record, not just the sequence |
| Merge domain objects not text (Onshape) | Transfers (design rule) | Merge parts, never raw sequence characters |

---

## 11. Recommendations for our parts library (consolidated)

Pulling the transferable decisions into a build list. Items marked *(have)* already exist in
our model; *(add)* are proposals.

1. **Identity.** Non-intelligent, permanent, system-assigned `id` within a `namespace`,
   issuer-scoped for federation. All classification in queryable attributes, never in the
   key. *(have — keep; resist every future request to make IDs "readable")*
2. **Revision = content digest.** Keep `version == sha256(canonical bytes)`; immutability is
   arithmetic, not policy. Released revisions are promoted working drafts. *(have)*
3. **Pinned references by default.** `Ref` pins an exact version; add an *explicit, logged*
   "resolve latest effective revision" operation but never make floating the silent default.
   *(have the pin; add the explicit resolver)*
4. **Effectivity.** Add date/lot effectivity so "which revision for this build" is
   answerable and old builds stay correct-as-built. *(add)*
5. **Two linked trees.** A structural/spatial model and a build BOM, deliberately divergent,
   both maintained; reverse-indexed edges for where-used from day one. *(add)*
6. **ECR/ECO as first-class records** with typed edges to affected versions, dispositions,
   effectivity, and reviewer approvals; a governed release event that promotes draft →
   released. *(add; governance shape exists in SPEC-002)*
7. **Variances as first-class records** for the designed-vs-as-built gap — logged, approved,
   bounded; never "fail" or "ignore." *(add)*
8. **Datasheet record** with the §5 skeleton, but nominal→distribution, envelope→context,
   qualification→probability-with-conditions, and *mandatory test conditions on every
   number*. *(add)*
9. **Interface Control records** (the ICD analogue) referenced by both mating parts,
   revision-controlled, specifying the interface in biology-appropriate formal terms — never
   borrow GD&T's geometric formalism. *(add)*
10. **Configurator over a 150 % design space** with explicit incompatibility rules, resolving
    design intent into a specific buildable construct. *(add)*
11. **Merge at the part/feature level with domain-aware conflict detection**, never by
    diffing raw sequence strings. *(add — the single most actionable §8 lesson)*
12. **Keep both the explicit artifact and the parametric design recipe**, so you can both
    build/hash the thing and answer "why is it this way" and regenerate on intent change.
    *(partially have via `predecessor`; add the recipe)*
13. **Qualification is revisitable.** A where-used propagation must be able to flag a part
    whose qualification may no longer hold because its system context changed. *(add — no
    mechanical analogue, and a genuine safety feature)*

The spine — meaningless permanent IDs, immutable hashed revisions, pinned references,
governed change, logged variances, and spec sheets whose every number carries its
conditions — is the forty-year-old mechanical-PLM consensus, and it is almost entirely
right for us. The adaptations are concentrated in exactly two places: **the datasheet's
numbers become distributions and probabilities**, and **the interface/tolerance formalism
must be rebuilt for a substrate with no fixed geometry**. Everything else we can, and
should, steal.

---

## Sources

Standards and systems referenced (checked during drafting; where a point was only lightly
verifiable it is flagged in-text):

- ASME Y14.5 — Dimensioning and Tolerancing (GD&T); 2018 edition current. ASME.
- ASME Y14.35 — Revision of Engineering Drawings and Associated Documents (revision-letter
  conventions; omitted letters I,O,Q,S,X,Z; edition rules vary — 1997 edition states the
  two-char max). ASME; secondary discussion at eng-tips.com.
- SAE/EIA-649C (2019) — Configuration Management Standard (neutral terminology; baselines;
  variance = former deviation/waiver). SAE International; Wikipedia overview of EIA-649;
  Lockheed Martin supplier CM doc for the variance-in-practice wording.
- MIL-STD-973 — (superseded) defense configuration management standard, context for EIA-649.
- NATO Stock Number / NIIN and CAGE code — non-intelligent national-scale identifier scheme.
- ISO 10303 (STEP), AP242 "Managed model-based 3D engineering," Edition 3 published Dec
  2022, further revision in ISO pipeline as of late 2024; carries PMI/GD&T + config data.
  ISO; steptools.com; prostep.org fact sheet.
- ISO 14306 (JT) — lightweight visualization/DMU format.
- Onshape branching & merging — feature-level conflict detection, selective merge (v1.151+).
  onshape.com features page, cad.onshape.com help (merging.htm), Onshape tech tips, Onshape
  forum.
- PLM/CAD systems — Siemens Teamcenter, PTC Windchill, Aras Innovator (low-code, no-per-seat
  core license model), Dassault 3DEXPERIENCE, Onshape (PTC), Duro / "Duro Design" (2025
  relaunch; Altium acquisition Dec 2025 per CB Insights — lightly verified), OpenBOM. Vendor
  documentation and widely-reported practitioner sentiment.
- Component datasheet structure (min/typ/max, abs-max vs operating, derating, test
  conditions, L10 bearing life, FIT/FMEA) — general engineering datasheet convention; e.g.
  rolling-bearing ratings per ISO 281 (L10 life) and ISO 492 (bearing tolerance classes),
  op-amp and actuator datasheet conventions.
- Biology-adjacent standards noted for context (not relied on for the analogy's claims):
  ISO 20688-2:2024 (production & QC requirements for synthesized double-stranded DNA,
  ISO/TC 276); SBOL 3 (Synthetic Biology Open Language) data model and DBTL framing — per
  the 2020 SBOL 3 paper and community proposals, not the normative spec text.

Internal references: `specs/SPEC-001-record-types.md` (content-addressed records, immutable
`version`, `Ref`, `predecessor`), `specs/SPEC-002-contribution-review-lifecycle.md`
(review/acceptance governance), `specs/SPEC-004-bundles-and-federation.md` (bundles ≈
baselines).

> **On the honesty floor:** no standard number here was invented; each corresponds to a
> real published standard. Edition-specific details (ASME Y14.35 letter rules, AP242
> editions) and one corporate event (the Duro/Altium acquisition) are flagged as
> edition-dependent or lightly-verified in-text — confirm against the primary source before
> relying on a specific clause number or deal term. Every sentence that argues from analogy
> to biology rather than reporting mechanical practice is marked as analysis/analogy/proposal
> at that sentence.
