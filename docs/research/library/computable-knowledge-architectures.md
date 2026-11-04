# Computable-knowledge architectures: how curated libraries are actually built

**Status:** Research note, not a spec. **Date:** 2026-11-04.
**Purpose:** We are about to build a library of biological design laws: scaling laws, equations and dimensionless groups. Each law will carry:
- the organisms and conditions where it is known to hold;
- the measured examples;
- the regime where it breaks.

The library must be queryable by machine, versioned and citable. This note studies how mature systems solved the same problems so we can copy what works and avoid what did not.

---

## 0. How to read this note

### Read-levels
Every source in §10 has one of five read-levels:

| Level | Meaning |
|---|---|
| **full-text** | The primary document, or the named file or section of it, was read. |
| **abstract** | Only the abstract or summary page was read. |
| **listing** | Only a catalogue entry, repo listing or table of contents was read. |
| **search-summary** | Only search-engine summaries were read. The claim may be right, but it was not checked against the source. |
| **could-not-access** | The source was tried and was unreachable. |

### Claim tags
In the body, each claim is tagged:
- **[doc]**: documented in a source at the stated read-level.
- **[inf]**: our inference or design opinion.
- **[unverified]**: a plausible claim we could not pin to any source; do not rely on it.

### Access limits (read this before trusting any section)
This research ran in a sandbox with a restrictive network policy.

**Unreachable:** reference.wolfram.com, wolframcloud.com, wikidata.org, mediawiki.org, w3.org, asknature.org, biomimicry.org, bionumbers.hms.harvard.edu, book.bionumbers.org, sbml.org, biomodels.org, nist.gov, esdu.com, ansys.com, matweb.com, modelica.org, openfoam.org/.com, dolthub.com, docs.datasette.io, simonwillison.net, semantic-mediawiki.org, ceur-ws.org and springer.

**Reachable:**
- GitHub, via clone and raw files. This gives source code and in-repo docs for Wikibase, wikidata-query-rdf, libSBML, Modelica, OpenFOAM, Dolt, Datasette, sqlite-utils, Semantic MediaWiki, Backstage and the W3C RDF 1.2 editor's drafts.
- arXiv.
- PubMed Central.

**Consequences:**
- **The Wolfram section rests entirely on search summaries.** It is the weakest section here. Re-verify it against reference.wolfram.com before copying any syntax.
- AskNature, ESDU, Granta MI, MatWeb and the NIST WebBook are known only from papers and search summaries.
- Physics-informed ML libraries were **not surveyed**; there was not enough budget. §5 covers five other libraries instead.

Two load-bearing claims were re-checked directly by the author of this note, not only by the research passes:
1. The Wikibase JSON quantity example has upper and lower bounds inverted (§2.3).
2. The BioNumbers 2010 entry fields, its versioning and its `BNID` citation style are as stated (§4).

---

## 1. Executive summary: what to copy

| # | Pattern | Who does it best | Copy? |
|---|---|---|---|
| 1 | **Statement as a first-class object with a stable opaque ID.** It carries qualifiers, references and a rank. | Wikidata | **Yes: this is the core of our data model.** |
| 2 | **Plurality.** Several conflicting values for one property can coexist, each sourced. A default view is chosen by an explicit rank rule. | Wikidata (ranks + "truthy" `wdt:` projection); NIST WebBook shows competing values side by side | Yes |
| 3 | **Qualifiers declared per property and discoverable.** A property says which conditions it can be qualified by. | Wolfram (`EntityProperty[...]["Qualifiers"]`) | Yes. Wikidata's qualifiers are free-for-all, which is a weakness. |
| 4 | **Typed missing values.** `Missing["NotApplicable"]`, `"Disputed"`, `"Variable"`, and so on. | Wolfram | Yes. These map directly onto "outside the regime", "contested exponent" and "varies by clade". |
| 5 | **Uncertainty with stated semantics.** Statistical uncertainty is kept separate from hard bounds. | Wolfram (`Around` vs `Interval`); NIST/TRC (ISO GUM, evaluator-assigned) | Yes. Do **not** copy Wikidata's semantics-free bounds or BioNumbers' overloaded "Range". |
| 6 | **Quantity and unit pair; dimensionless groups as named types.** | Modelica (`type ReynoldsNumber = Real(final quantity="ReynoldsNumber", final unit="1")`) | Yes. Two groups can both have unit `"1"` and still be different things. |
| 7 | **Store the original unit and a normalised SI value.** | Wikibase (`quantityNormalized`) | Yes |
| 8 | **Raw observations kept apart from evaluated values.** Evaluation is re-runnable. | NIST TRC (SOURCE archive feeds ThermoData Engine "dynamic data evaluation"); BioModels (curated vs non-curated) | **Yes: this is the central architectural lesson.** |
| 9 | **Stable ID plus immutable version ID, with withdrawal rather than deletion.** | Granta MI (RHGUID/RGUID); BioNumbers (BNID, edits saved as versions); Wikibase (`lastrevid`; IDs never renamed) | Yes. We already do content-addressed versions (SPEC-001). |
| 10 | **Reference examples stored next to the content, with provenance and a comparison tolerance.** Expected-failure cases are marked. | Modelica (`ReferenceResults/` + `creation.txt` + csv-compare "tube"; `TestCase(shouldPass=false)`) | Yes. "Measured examples" and "breakdown regime" become executable tests. |
| 11 | **Declarative rename and conversion rules written against the *old* names.** | Modelica `conversion(...)` scripts | Yes, for law-ID and vocabulary migrations |
| 12 | **Git authoritative; database a read-only, rebuildable, commit-stamped derivation.** | Datasette "baked data"; Backstage catalog; Semantic MediaWiki (wiki text → store) | **Yes: this is our hybrid architecture.** |
| 13 | **A reproducibility scorecard per entry.** | Tiwari et al. 2021: 8 yes/no questions | Adapt as an evidence-completeness score |
| 14 | **A versioned controlled vocabulary for function and organism scope.** | Counter-example: AskNature's function count drifted (162 / 168 / "160+") with no version label | Yes: version every vocabulary |
| 15 | **Public bulk download and an API from day one.** | BioNumbers (flat file), BioModels (REST, CC0). Counter-example: AskNature (no API, so it gets scraped). | Yes |

**Do not copy:**
- RDF-star-style "quoted triple" identity for statements. It cannot hold two statements with the same subject, predicate and object but different conditions (§7).
- One monolithic triple store as the canonical store. Wikidata had to split its query graph in May 2025.
- Free-text conditions (BioNumbers' "Comments").
- Instance-of / subclass-of ambiguity for organisms (Wikidata's P31/P279 churn).
- A database that two parties write to independently (Terraform-style split authority).

---

## 2. Wolfram Language and Wolfram|Alpha

> **Read-level for this entire section: search-summary.** reference.wolfram.com was unreachable. Every syntax form below appeared in search-engine summaries of the official reference pages, not in the pages themselves. Treat it as a pointer to verify, not a copy-paste source.

### 2.1 The entity framework [doc, search-summary; S1–S5]
- **Entities are symbolic expressions:** `Entity[type, canonicalname]`.
  - `CanonicalName[x]` returns the unique identifier and works on Entity, EntityClass, EntityProperty and EntityPropertyClass.
  - `CommonName[x]` returns the display name.
  - We did not verify the canonical-name string for any species entity, so none is quoted here.
- **Properties are expressions too:** `EntityProperty[type, pname]`.
  - **Qualified properties:** `EntityProperty[type, pname, {qual1 -> val1, ...}]` "represents a property modified by the qualifier rules".
  - Documented examples:
    - `Entity["Country","UnitedStates"][EntityProperty["Country","Population",{"Date" -> 1980}]]`
    - `EntityValue[Entity["Country","Norway"], EntityProperty["Country","Population",{"Date" -> DateObject[{2005}]}]]`
    - Shorthand: `Entity["Country","UnitedStates"][Dated["Population",1980]]`
  - A `"Date"` qualifier may be a date or a date span.
- **Qualifiers can be discovered.** `EntityProperty[...]["Qualifiers"]` and `["QualifierValues"]` list which qualifiers a property accepts and which values they may take. One documented example shows population accepting `"Gender"` and `"Race"`.
- **Property-level metadata:** `EntityValue[EntityProperty[...], "prop"]`. Documented metadata names include `"Label"`, `"Definition"`, `"Source"`, `"PhysicalQuantity"`, `"Unit"`, `"Qualifiers"` and `"QualifierValues"`.
  - A built-in `"Source"` entity type exists, so sources are themselves entities. We saw only its reference-page listing.
- **Classes:** `EntityClass[type, {prop -> criterion, ...}]` defines a class by a predicate (intensional) as well as by an explicit list.
- **Missing data has typed reasons:** `Missing["reason"]`. Documented reasons include `"NotApplicable"`, `"Unknown"`, `"NotAvailable"`, `"Nonexistent"`, `"Indeterminate"`, `"Variable"`, `"Disputed"` and `"TooLarge"`. Curated-data functions return these when a property "does not apply or is not known".

### 2.2 Units, dates and uncertainty [doc, search-summary; S6–S7]
- **Units:** `Quantity[magnitude, "Unit"]`, with string unit names. Arithmetic and conversion work across compatible units.
- **Statistical uncertainty:** `Around[x, δ]`.
  - Asymmetric: `Around[x, {δ-, δ+}]`. Relative: `Around[x, Scaled[ϕ]]`.
  - Idiom: `Quantity[Around[51.034, 0.001], "Grams"]`.
  - Accessors: `["Value"]`, `["Uncertainty"]`, `["Interval"]`.
  - Propagation is first-order and **assumes uncorrelated** inputs. `Around` arrived in Version 12 (2019).
- **Hard bounds:** `Interval[{min, max}]`, with interval arithmetic. This is a different object from `Around`.
- **Dates:** `DateObject[{y}]`, `DateObject[{y,m,d}]` and so on. Granularity is carried by the length of the list (an inference from the examples).

### 2.3 EntityStore: custom entity types [doc, search-summary; S8–S9]
- `EntityStore[type -> <| ... |>]`. Keys reported inside a type's association:
  - `"Entities"`: an association from entity name to an association from property to value.
  - `"Properties"`: property descriptions.
  - `"EntityClasses"`.
  - `"PropertyClasses"`.
- Documented example:
  ```
  store = EntityStore["fruit" -> <|"Entities" -> <|
     "banana" -> <|"color" -> Yellow|>, "lime" -> <|"color" -> Green|>, ...|>|>]
  EntityRegister[store]
  ```
- `EntityRegister`, `EntityUnregister` and `EntityStores[]` replaced the `$EntityStores` global as of Version 11.3.
  - Registered stores take precedence over built-in types.
  - An EntityStore can be backed by a relational database. A table without a primary key disables some single-entity functionality.

### 2.4 Curation and provenance [doc, search-summary; S10–S12]
- **Wolfram Data Repository:**
  - Resources carry `"SourceMetadata"` with Dublin-Core-like keys: citation, creator, date, coverage, publisher, rights and so on.
  - Submission goes through `ResourceSubmit` and needs a publisher ID.
  - Publication requires review-team approval, which "typically involves modifications".
- **Wolfram|Alpha curation,** from secondary accounts (2009–2011):
  - Data comes from primary sources, not web scraping.
  - A "curation pipeline" combines automated checks (statistics, visualisation, cross-checking sources) with expert review, and there is a domain expert per data stream.
  - Choosing between sources that disagree is named as a core curation problem.
  - Critics noted that the curated view is opaque.

### 2.5 What makes a value "computable"? [inf]
We found **no primary source** stating which `EntityValue` results are computed on demand and which are stored lookups. "Wolfram|Alpha at 10" frames the system as computing answers rather than searching, but that is rhetoric, not architecture.

Our reading of what "computable" means in practice is that a value:
1. Has a **type the evaluator understands**: a `Quantity` with a unit, an `Around`, a `DateObject`, or an `Entity`. It is not a string.
2. Is **addressable symbolically**, e.g. `Entity[...][EntityProperty[...]]`, so it can feed straight into further computation.
3. Is **closed under arithmetic and conversion**: unit algebra and error propagation work on it.
4. **Fails in a typed way**: `Missing[reason]` rather than null.

A string "3/4 ± 0.02" is stored. `Quantity[Around[0.75, 0.02], "DimensionlessUnit"]` is computable.

### 2.6 Quantities valid only under conditions [doc + inf]
Wolfram's documented answer is **the qualifier on the property**: `{"Date" -> ...}`, `"Gender"` and so on. The value is a function of the qualifier values, and the property advertises its permitted qualifiers. That is exactly what "metabolic exponent as a function of clade, temperature and body-mass range" needs.

**Weakness [inf]:** the public model exposes **one curated value per (entity, property, qualifier tuple)**. There is no visible multi-source plurality, no ranks and no deprecation history.

- **Wolfram is the model for computability and units.**
- **Wikidata is the model for plurality and provenance.**
- We need both.

---

## 3. Wikidata

### 3.1 The data model [doc, full-text; S13–S14: Wikibase `docs/topics/json.md` and RDF builder source]

**The item.** Top-level item JSON:
```json
{"id":"Q60","type":"item","labels":{},"descriptions":{},"aliases":{},
 "claims":{},"sitelinks":{},"lastrevid":195301613,"modified":"2020-02-10T12:42:02Z"}
```
- `lastrevid` is the MediaWiki revision ID, i.e. the version of the whole entity document.
- Properties are entities too, such as `P580`. They carry a `"datatype"`.

**Statement fields:**
- `id`: an opaque GUID such as `"q60$5083E43C-…"`. The docs say "No assumptions can and shall be made about the identifier's structure".
- `type`: `"statement"`.
- `mainsnak`.
- `rank`: `preferred | normal | deprecated`.
- `qualifiers`: a map from property ID to a list of snaks.
- `references`: a list of `{hash, snaks, "snaks-order"}`.

**Snak types.** A snak has `snaktype ∈ {value, somevalue, novalue}`.
- `somevalue` means "there is a value but we don't know it".
- `novalue` means "known to have none".

**Quantity datavalue.** This is the verbatim doc example:
```json
{"amount":"+10.38","upperBound":"+10.375","lowerBound":"+10.385",
 "unit":"http://www.wikidata.org/entity/Q712226"}
```
- The upper bound is *smaller* than the lower bound. This is a documentation bug, re-checked directly on 2026-11-04 at line 407 of `json.md`.
- Amounts are signed arbitrary-precision decimal strings.
- Bounds are optional but come in pairs. "If not given or null, the uncertainty (or precision) of the quantity is not known."
- The unit is an item URI, or `"1"` for a dimensionless quantity.
- **Nothing says whether the bounds are an SD, a confidence interval, a min–max range or rounding precision.**

**Time datavalue:**
- `precision` runs from 0 (billion years) through 9 (year), 10 (month) and 11 (day).
- It also has `timezone` and `calendarmodel`.
- `before` and `after` are "Currently unused, may be dropped".

**Qualifier documentation.** Qualifiers "provide context for a Statement's value, such as a point in time, a method of measurement, etc." The doc's own qualifier example uses P580 and P582 (start and end time). Other property IDs and labels seen in full-text sources:
- `P248` stated in;
- `P854` reference URL;
- `P31` instance of;
- `P279` subclass of;
- `P39` position held.

### 3.2 How qualifiers reify n-ary relations in RDF [doc, full-text; S14]
The RDF mapping (`RdfVocabulary.php`, ontology `http://wikiba.se/ontology#`) produces **two layers**.

**Full layer (n-ary pattern):**
```
wd:Q…  p:P39  wds:<statement-guid> .
wds:<guid>  ps:P39  wd:<office> ;          # main value
            pq:P580 "2006-03-11"^^xsd:dateTime ;  # qualifier
            pq:P582 "2010-03-11"^^xsd:dateTime ;
            wikibase:rank wikibase:NormalRank ;
            prov:wasDerivedFrom wdref:<ref-hash> .
wdref:<hash>  pr:P248 wd:<source-item> .
```
- Deep values come through `psv:`, `pqv:` and `prv:`. A quantity value node carries:
  - `wikibase:quantityAmount`;
  - `wikibase:quantityUpperBound`;
  - `wikibase:quantityLowerBound`;
  - `wikibase:quantityUnit`;
  - `wikibase:quantityNormalized`, which points to an SI-normalised copy.
- `novalue` is encoded as the subject being typed `wdno:Pxx`.

**Truthy layer:**
```
wd:Q…  wdt:P39  wd:<office> .
```
The source comment says this layer includes only the "best" statements per property, meaning the best non-deprecated rank, and "excludes deprecated and non-'best' statements, ranks, qualifiers, and references". If preferred-rank statements exist, only those are emitted.

**[inf]** The `p:`/`ps:`/`pq:` layer *is* the W3C "n-ary relation" pattern (S26): a new node per relation instance. The `wdt:` layer is a lossy, rule-defined default view. The selection rule is explicit and documented, and that is the part worth copying.

### 3.3 What Wikidata gets right that a naive triple store does not [doc + inf]
1. **Statement identity [doc].** Qualifiers attach to a particular statement GUID. Two "position held" statements for the same office with different dates do not mix. In a naive triple store they collapse into one triple.
2. **Plurality [doc, S15 search-summary; S17 full-text].** Vrandečić & Krötzsch's design principles include plurality and secondary data. Waagmeester et al. call Wikidata "a database of assertions and not of absolute truth".
3. **Rank as an explicit, queryable default-selection rule [doc]**, rather than deleting the losers.
4. **Typed values [doc]** with units, precision, calendar model and globe, plus `somevalue`/`novalue`.
5. **Per-statement provenance [doc].** References are shared, hash-identified nodes.
6. **Stable IDs [doc, S27 Wikibase storage docs].** "Neither top-level nor sub-entities can be renamed."
7. **Life-science practice [doc, S17 full-text].** Bots import from NCBI Gene, Ensembl, UniProt, PDB and others, with structured provenance including the source *version*. The Python framework Wikidata Integrator detects conflicts and preserves conflicting human edits. Mapping queries can filter on references and qualifiers.

### 3.4 Known pathologies at scale
- **Reference gaps [doc, full-text, S16: Amaral et al. 2021].**
  - About **77% of claims have at least one reference**.
  - "stated in" (P248) appears on about 86% of reference nodes.
  - References are heavily shared, at about 11 claims per reference on average.
  - An earlier ISWC 2017 study (S19, search-summary) found 61% of evaluated external references relevant and authoritative. Link rot was a main failure mode.
- **Deprecation and churn [doc, full-text, S20: Shenoy et al. 2021].**
  - 10,040,256 deprecated statements, about 90% from five astronomy properties.
  - 76.5M statements permanently removed.
  - More than 2M redirected (merged-duplicate) nodes, affecting 26% of removed statements.
  - About 0.76% of statements violate type constraints.
- **Instance-of / subclass-of confusion [doc, full-text S20; search-summary S21].**
  - "Nearly half a million cases where one of the taxonomic relations has been changed to the other".
  - 444k of 935k P279 edges were replaced by P31 only.
  - Brasileiro et al. (WWW 2016) and Dadalto et al. (2021) report large-scale multi-level-modelling anti-patterns, with one anti-pattern query returning about 1.28M results.
  - **[inf] Direct biology hazard:** "species", "strain", "taxon rank" and "model organism" are classic multi-level traps.
- **Constraints are soft [doc, search-summary, S22: Ferranti et al. 2024].**
  - There are 32 constraint types. SHACL-Core cannot express 2 of them; all can be written in SPARQL.
  - Violation reports have opaque generation logic.
- **Query-service scale [doc, search-summary, S23–S25].**
  - WDQS runs on Blazegraph, which is unmaintained.
  - Scholarly articles were about half of all triples but about 2% of queries. The graph was **split on 9 May 2025** into a main graph and `query-scholarly.wikidata.org`. Cross-graph queries need SPARQL `SERVICE` federation.
  - A 2025 benchmark found QLever fastest on full Wikidata and Blazegraph significantly slower. As of our reading, a replacement engine was reported as being adopted but not confirmed.
- **[inf] Lesson.** Per-statement reification multiplies triple counts several-fold. Keep the canonical store relational or JSON, treat RDF as an export, and plan partitioning from day one.

---

## 4. BioNumbers and *Cell Biology by the Numbers*

This is the closest direct model for a single entry in our library.

### 4.1 Entry fields [doc, full-text; S28: Milo et al. 2010 NAR, Table 2, verified directly]

| Field | As documented |
|---|---|
| ID | "A unique, automatically generated ID for every BioNumber" |
| Property | — |
| Organism | Drop-down of more than 50 organisms, free entry allowed. Special values include 'generic', 'unspecified', 'various' and 'biosphere'. |
| Value | — |
| Units | "If no units, then 'Unitless'" |
| Range | "In cases where a range of values is available or an associated standard error or deviation" |
| Reference, PubMed ID | — |
| Entered By | — |
| Primary Source, Primary Source PubMed ID | Used when the number was found in a book or review |
| Measurement method | "A short description of the method used to obtain the number" |
| Keywords, Comments | — |
| Date added, Date edited | — |

### 4.2 Identifiers, versioning and citation [doc, full-text; S28]
- Every entry has a **BNID**, for example **BNID 100260**: *E. coli* doubling time of about 20 min.
- "Every change is saved as a new version with the database showing the most current version by default but enabling views of older versions."
- **Citation style:** "each time we invoke some particular BioNumber of interest, we reference its BioNumbers ID (e.g. BNID 102345)". BNIDs are cited inline as `(BNID nnnnnn)`. Whether the 2015 book uses exactly this style is **[unverified]**, because the book site was blocked.
- **Curation and access:**
  - Every number needs a literature reference and is curated by the team.
  - Registered users can comment to suggest corrections.
  - A full flat-file download was offered.
- **Scale at publication (2010):** more than 4,500 properties, more than 200 organisms and more than 1,000 references.
  - A current figure of about 14,000 entries circulates but is **[unverified]**.
  - We found no 2024–2026 maintenance announcement. Liveness could not be checked directly.

### 4.3 The telling detail [doc + inf]
The paper's own worked example says *E. coli* "under ideal conditions of LB medium and 37 °C divide every ∼20 min (BNID 100260)". **The conditions (LB medium, 37 °C) appear in prose, not in a field.** That is BioNumbers' central limitation for our purposes.

**[inf] What BioNumbers lacks, and we need:**
1. **Machine-readable conditions:** temperature, medium, life stage and size range as typed qualifiers.
2. **Uncertainty semantics:** "Range" mixes SD, SE and min–max in one field.
3. **Validity and breakdown regime.**
4. **Ontology IDs:** NCBI Taxonomy for organisms and a property vocabulary. Organism is a drop-down string.
5. **Measured vs fitted vs assumed.**

**What to copy:**
- a short, numeric, permanent, citable ID, cited inline in prose;
- versions saved on every edit;
- the primary-source vs secondary-source distinction;
- a "method" field on every value;
- a bulk download.

*Cell Biology by the Numbers* (Milo & Phillips, Garland 2015; S29, search-summary) layers narrative "back-of-the-envelope" reasoning over these IDs. **[inf]** That is the pattern for our human-facing law pages: prose that cites machine records by ID.

---

## 5. AskNature and the Biomimicry Taxonomy

### 5.1 Organisation: function-first [doc, search-summary; S30–S32]
- It has three levels: **group → sub-group → function**. Strategies, i.e. organism-specific mechanisms, hang below the functions.
- The most-cited count is **8 groups, 30 sub-groups and 162 functions**. The official 2021 explainer says "more than 160 functions". An AIES-2018 paper by IBM and the Biomimicry Institute says 168.
  - **No version identifier for the taxonomy was found.**
- Example path: *Get, store, or distribute resources* → *Capture, absorb, or filter resources* → *Capture, absorb, or filter liquids*. The worked organism is the Namib desert beetle.
- A strategy can carry several functions.
- **Strategy pages** (Deldin & Schuknecht 2014, abstract and snippets only) have:
  - a "carefully crafted title";
  - a one-sentence essence;
  - their taxonomy placement;
  - a scientific excerpt;
  - links to design applications and inspired products ("Innovations").
- **Scale:** more than 1,600 strategies (2013) and more than 1,700 (current site text).
- **History:**
  - The site was PHP/Symfony from 2007–08.
  - A 2019 Node rebuild README (full-text, S33) says "A public API doesn't exist yet, but is on our roadmap".
  - Redesigned in 2021.
  - An LLM "chat" feature arrived in 2025.
  - **No public API was found in any 2023–2026 source.** Third parties scrape it. The `zju-d3/AskNatureNetData` repo publishes scraped JSON with fields `Source`, `Function1…6`, `Application`, `Biological Strategy` and `Hyperlink` (full-text README).

### 5.2 Inspirational or specifiable? [doc + inf]
- **[doc]** Entries are **hand-curated prose with no quantities, units, validity ranges or failure regimes** in any source we found.
- **[doc]** The biologically-inspired-design (BID) literature names curation cost as the bottleneck:
  - Vandevenne et al. (2011–2016) cite the "interactive work required by humans per biological strategy".
  - arXiv 2312.12681 (full-text) reports "40–100 hours to describe a single biological organism" in structured frameworks such as DANE's Structure-Behaviour-Function models.
  - IDEA-INSPIRE / SAPPhIRE (IISc) has the same scaling problem.
- **[doc, search-summary]** Tool reviews (Fayemi et al. 2017; Wanieck et al. 2017) and a secondary review (Sharma & Sarkar 2019) describe BID repositories as "thinly populated". They say AskNature's taxonomy search "needs sufficient training or appropriate selection of keyword".
- **[doc, search-summary]** The closest prior work to our goal is Kruiper, Vincent, Chen-Burger et al. (Heriot-Watt, 2018–2020). They use **trade-off relations** between variables to bridge biology and engineering, with 1,500 annotated sentences.
- **[inf] Verdict: AskNature is inspirational, not specifiable.** It answers "what organisms do something like X?", not "under what conditions does relation Y hold, and how accurately?".
  - **Copy:** a controlled **function vocabulary** as one entry point, and the strategy-to-product link.
  - **Avoid:** an unversioned vocabulary, prose-only records and no API.
  - **Organisation:** our library should be **law-first**, with functions as an index facet and organisms as a scope facet.

---

## 6. Other computable design libraries

Five were surveyed. Physics-informed ML libraries were not.

### 6.1 Modelica Standard Library (MSL) [doc, full-text of named files; S38–S40]
This is the strongest packaging model in the survey.

- **Unit: a parameterised component class** in a package hierarchy.
- **Units and dimensionless groups.** `Modelica/Units.mo` declares quantity types:
  - `type Length = Real(final quantity="Length", final unit="m");`
  - `type ReynoldsNumber = Real(final quantity="ReynoldsNumber", final unit="1");`
  - Also `NusseltNumber`, `FroudeNumber`, and `type BiotNumber = NusseltNumber;`.
  - Unit grammar: `"kg.m.s-2"`, `"J/(kg.K)"`, `"1"` for dimensionless. `"Nm"` is rejected; it must be written `"N.m"`.
  - **[inf]** The `quantity` + `unit` pair is the key idea. Unit alone cannot tell Reynolds from Froude.
- **Library versioning.**
  - The top-level annotation carries `version`, `versionDate`, `dateModified` and `revisionId`. `revisionId` is a git `export-subst` placeholder `$Format:%h %ci$`.
  - It also carries `uses(Complex(version=...))`.
  - The version applies to the whole library: "All classes within this top-level class have this version number."
  - Semantic versioning MAJOR.MINOR.BUGFIX since 4.0.0, with `master` plus `maint/4.1.x` branches.
- **Migration.**
  - `conversion(from(version={...}, script="...mos"))` with rules `convertClass`, `convertElement`, `convertModifiers` and `convertMessage`.
  - Rules are **written against old names** "so the conversion [can] be done without access to the old version of the library".
  - Example: `convertClass("Modelica.SIunits","Modelica.Units.SI")`. `convertModifiers` can compute new parameters from old ones.
  - `ModelicaTestConversion4` holds 108 minimal models, each tied to an issue, that test the conversions themselves.
  - Classes that cannot be converted go to an `ObsoleteModelica4` quarantine library.
- **Validation.**
  - `ReferenceResults/` holds 1,183 models' reference trajectories. Each has `<Model>.csv`, `comparisonSignals.txt` and a **`creation.txt` provenance block** with `generationTool`, `gitRevision`, `gitStatus`, `testOS`, and tolerance with a comment explaining where it came from.
  - The comparison tool `csv-compare` checks curves within a **tolerance tube**.
  - `TestCase(shouldPass=false)` marks models that are *expected* to fail.
  - Project rules: "regression testing with at least 2 different tools, in comparison with the previous version" before each release, on a release train running week −9 freeze → beta → rc → vote.
  - **[inf]** The full simulation regression appears to run at release milestones, not in per-PR CI.
- **[inf] Mapping to us:**
  - law → component class;
  - measured example → reference result, with provenance and tolerance;
  - breakdown regime → `shouldPass=false` cases;
  - law-ID rename → conversion rule.

### 6.2 OpenFOAM case structure [doc, full-text of named files; S41–S42]
- **Unit: a case directory.**
  - `0/` holds initial and boundary fields.
  - `constant/` holds properties and mesh.
  - `system/` holds `controlDict`, `fvSchemes` and `fvSolution`.
  - An `Allrun` script drives it, and each file has a `FoamFile{...}` header.
- **Dimensions.** `dimensionSet` has 7 exponents: kg, m, s, K, **kmol** (not mol), A, cd.
  - The current dev branch also accepts named dimensions (`dimensions [velocity];`) and inline units (`nu 1e-05 [m^2/s];`).
  - Dimension errors are fatal in debug mode.
- **Validation is a smoke test.** `tutorials/Alltest` rewrites every `controlDict` to run **one time step**. We found no reference-result files in the tutorials, unlike MSL.
- **Versioning.** The Foundation (`OpenFOAM-dev`, numbered releases) and ESI-OpenCFD (`vYYMM`) have diverged in input syntax. This last point is a search summary.
  - **[inf] Cautionary tale:** packaged knowledge without an explicit dependency pin and conversion rules rots silently when the host forks.

### 6.3 SBML and BioModels [doc, full-text; S43–S48]
- **Unit: an SBML model.**
  - Level 3 is a core plus packages. Eight are officially part of the standard: `distrib`, `comp`, `fbc`, `groups`, `multi`, `qual`, `layout` and `render`.
  - Versioning runs Level → Version → Release, where a Release is an erratum revision.
  - Units can be declared on all entities.
- **Annotation:**
  - Each element carries an `sboTerm` and RDF annotations using **MIRIAM qualifiers** with identifiers.org URIs.
  - Model qualifiers (libSBML `CVTerm.h`): `IS`, `IS_DESCRIBED_BY`, `IS_DERIVED_FROM`, `IS_INSTANCE_OF`, `HAS_INSTANCE`.
  - Biology qualifiers: `IS`, `HAS_PART`, `IS_PART_OF`, `IS_VERSION_OF`, `HAS_VERSION`, `IS_HOMOLOG_TO`, `IS_DESCRIBED_BY`, `IS_ENCODED_BY`, `ENCODES`, `OCCURS_IN`, `HAS_PROPERTY`, `IS_PROPERTY_OF`, `HAS_TAXON`.
  - These serialise as `bqmodel:isDescribedBy`, `bqbiol:hasTaxon` and so on. The serialisation is a search summary of sbml.org.
- **Packaging:**
  - A COMBINE archive (OMEX) is a ZIP with `manifest.xml` and optional RDF metadata, per OMEX Metadata 1.2. Only the abstract and search summaries were read.
  - SED-ML describes the simulation experiment.
- **BioModels curation** (Malik-Sheriff et al. 2020):
  - About 2,000 literature models, about 800 of them manually curated.
  - Curation checks that simulation reproduces the publication and produces a "reproduced curation figure", usually shipped with SED-ML and the COPASI file.
  - Curated models are downloaded 2.4× more than non-curated ones.
  - It has version history, a COMBINE download per version, and a CC0 licence.
  - Accession prefixes are `BIOMD` + 10 digits for curated models and `MODEL…` for others. This is a search summary only.
- **Reproducibility reality** (Tiwari et al. 2021, full-text):
  - Of 455 published ODE models, **49% could not be reproduced directly from the manuscript** and **37% not at all**.
  - The leading causes were missing parameter values (52) and missing initial conditions (44).
  - The paper proposes an **8-question reproducibility scorecard**. A score of 4 or more was associated with reproducibility (odds ratio 4.62, n = 110).
- **BioModels Parameters** (full-text):
  - About 95,000 parameters were extracted.
  - They are **not individually curated**, and the record **does not say whether a value was measured or fitted**.
  - **[inf]** This is precisely the gap a `basis: measured | fitted | assumed | derived` field closes.

### 6.4 NIST Standard Reference Data, Chemistry WebBook and ThermoData Engine [doc, search-summary; S49–S52]
- **The legal definition** (15 USC 290a): standard reference data is "critically evaluated as to its reliability". The statute lists *collection, compilation, critical evaluation, publication and dissemination* as **distinct** activities.
- **WebBook tables** have columns **Quantity | Value | Units | Method | Reference | Comment**.
  - Competing values appear side by side. For example, ΔfH°gas(C) is 716.68 ± 0.45 kJ/mol from a CODATA review, shown alongside the JANAF value.
  - Method codes such as `Ccr` appear in the tables.
  - Each data type is cited as a chapter of SRD 69 with its evaluators.
- **TRC and ThermoData Engine:**
  - "Critical evaluation is a process of analyzing all available experimental data for a given property to arrive at recommended values together with estimates of uncertainty."
  - The SOURCE archive holds raw experimental data.
  - ThermoData Engine (Frenkel et al. 2005) implements **"dynamic data evaluation"**: recommended values are computed on demand from the archive rather than published as fixed tables.
  - ThermoML (IUPAC) follows ISO GUM uncertainty.
  - TRC found only about 1 in 600 critical-temperature papers gave a complete uncertainty analysis, so **evaluators assign uncertainty**.
- **[inf]** This is the architecture for "law + measured examples":
  - The archive holds observations.
  - The law's fitted parameters and validity range are an *evaluation* computed from them.
  - Evaluations are re-run when new observations arrive.

### 6.5 ESDU, Granta MI and MatWeb (commercial; thin public documentation) [search-summary; S53–S56]
- **ESDU** (now Accuris):
  - Data Items are developed from "established theory, experimental data, and real-world engineering practice" and reviewed by industry, academic and government committees.
  - Items have 5-digit numbers such as 70022 and 76022. The leading digits look like the year, but that is **[inf]**.
  - Amendment lettering, accuracy statements and section structure are **[unverified]**: they are paywalled.
  - **[inf]** Conceptually it is the nearest engineering analogue to "law + applicability range + worked example". Its format cannot be copied from public sources.
- **Granta MI** (Ansys):
  - Per-table record version control. Each version has its own **Record GUID**, and all versions share a **Record History GUID**.
  - Version states allow released versions to be **withdrawn**.
  - Typed attributes: point, range, float functional, discrete, tabular and others.
  - **Functional data varies over schema-declared parameters**, numeric or discrete, with declared interpolation (linear, log, spline).
  - Los Alamos reports note stock schemas are undocumented, so sites interpret attributes inconsistently.
  - We found no dedicated public provenance or pedigree attribute.
  - **[inf]** "Functional attribute over declared parameters" is the right shape for "exponent as a function of temperature".
- **MatWeb:**
  - Manufacturer-supplied datasheets with **Metric | English | Comments** columns, where the test standard sits in Comments.
  - Some sheets are flagged "not for design".
  - It is compiled, not critically evaluated, and has no visible versioning.
  - **[inf]** A useful negative example.

### 6.6 Comparison: how a reusable piece of knowledge is packaged

| System | Unit of knowledge | Parameterised how | Validated how | Versioned how | Provenance |
|---|---|---|---|---|---|
| MSL | Component class | Typed parameters with `quantity`/`unit` | Reference trajectories + tolerance tube, ≥2 tools, expected-fail tests | Library semver; `uses`; conversion scripts | `creation.txt` per reference result; git |
| OpenFOAM | Case directory | Dictionaries + dimensioned fields | Tutorials, smoke-tested only | Fork- and release-specific syntax | Git; none per case |
| SBML/BioModels | Model file (+ OMEX) | Parameters, units, SBO | Curator reproduces the paper's figure; Tiwari scorecard | Level/Version/Release; per-model history | MIRIAM `bqmodel:isDescribedBy` etc. |
| NIST SRD/TDE | Property value per substance | (State variables) | Critical evaluation; consistency enforcement | SRD editions; dynamic re-evaluation | Method code + reference per value |
| ESDU | Data Item | Charts and equations with stated range [inf] | Committee review [doc]; accuracy statements [unverified] | Amendments [unverified] | Item references [unverified] |
| Granta MI | Record | Functional attributes over parameters | Site workflow | RHGUID/RGUID + release/withdraw | No standard pedigree attribute found |
| BioNumbers | Single number | None (conditions in prose) | Curation team | New version per edit; BNID | Reference + primary source + method |

---

## 7. Hybrid git-plus-database architectures: which direction is authoritative?

| System | Authoritative | Derived | How it is rebuilt | How two writers are kept from disagreeing |
|---|---|---|---|---|
| **Datasette "baked data"** | Files in git | SQLite, immutable (`datasette -i`) | Build script at deploy | The DB is never user-written. Edits mean a commit and a redeploy. |
| **Backstage catalog** | YAML in git | Catalog DB, explicitly "a caching mechanism" | Continuous processing loop (`processingInterval`), `POST /refresh` | "No two providers can try to output the same entity". `locationKey` is a "conflict resolution key" against takeovers; `409 Conflict` on a duplicate location; orphan marking; errored reprocessing never replaces the last good version. |
| **Semantic MediaWiki** | Page wikitext (`[[Prop::value]]`) | SQLStore tables (`smw_di_number`, …), optional SPARQL replica | `rebuildData.php` (full `-f`, ranges, `--shallow-update`) | MediaWiki edit conflicts on the single text source. Settings changes can silently require a full rebuild. |
| **Wikibase / WDQS** | Revisioned entity JSON (MediaWiki page content) | `wbt_*` term tables ("might not be always completely in sync"); Blazegraph RDF | Full: dump → `munge.sh` → load. Incremental: streaming updater diffs last-seen vs current revision per entity. | `baseRevId` conflict check plus a **structural three-way patch** (`fixEditConflict`). The SPARQL index is read-only to users. Updates are keyed on revision IDs, so they are idempotent. |
| **Dolt** | The Dolt database itself; history lives inside | None | n/a | **Cell-level** three-way merge keyed by primary key. Conflicts go to `dolt_conflicts_<table>` and are resolved with `dolt_conflicts_resolve --ours/--theirs`. In server mode a transaction conflicting at COMMIT rolls back. The concurrency part is search-summary only. |
| **Terraform** (counter-example) | Split: config in git *and* a state file | — | `plan`/refresh | Pessimistic locks (DynamoDB `LockID`, blob leases), `force-unlock`, drift reconciliation |

Sources: S57–S66, full-text for the named files of Datasette, Backstage, SMW, Wikibase, wikidata-query-rdf and the Dolt README and system tables. The Dolt merge semantics, the "baked data" essay and Terraform are search-summary only.

### What this means for us [inf]
- **The pattern that works:** exactly one writable source, and every derived store is read-only and fully rebuildable from it. Every system that avoids the two-writer problem does so *structurally*, not with locks:
  - Datasette never lets users write the DB.
  - Backstage refuses a second claimant.
  - WDQS only consumes a revision stream.
- **The pattern that hurts:** two partially authoritative artifacts (Terraform), which then need locks and drift reconciliation.
- **Where Dolt fits:** Dolt removes the split by making the DB the only thing. But then authored prose and equations live in cells, review happens on DoltHub rather than GitHub, and text-diff and LLM-friendly files are lost.
  - Dolt is a reasonable *derived* time-travel index (`AS OF`, `dolt_history_*`).
  - It is a poor authoring surface for law pages with derivations.

**Recommendation:**
1. **Git is authoritative.** One file per law, statement and observation; YAML or JSON with a schema.
2. **The database is a derived, read-only index** built deterministically from a commit SHA and **stamped with it**, in the style of MSL's `revisionId` and `creation.txt`.
3. **Incremental rebuilds keyed on content hashes**, like the WDQS revision IDs and the Backstage stitch hash, plus an always-available full rebuild (`rebuildData -f`, dump reload).
4. **No write path into the DB.** Any UI that "edits" opens a PR against the files (Backstage's GitOps recommendation).
5. **One owner per record:** each record has exactly one source path, and the build fails on a duplicate ID, like Backstage's `409`.
6. **This repo:** `frontier/` already has content-addressed `version` digests and `Ref` pins to exact versions (SPEC-001). Law records should be a new payload kind under that envelope rather than a parallel system.
   - Where the git-file path and the existing `store.py` submission path overlap, **one must be declared the source and the other a projection**. That is a decision for the spec, not this note.

---

## 8. Hypergraph and n-ary modelling

### 8.1 Why plain triples fail
"Kleiber exponent b = 0.75 ± 0.02 for clade C, body-mass range M, temperature T, life stage S, per source R, fitted by method F" is a single **n-ary fact** with about eight participants.

A triple `(law, holdsFor, organism)` loses which conditions go with which organism. Two such facts for the same organism with different conditions become indistinguishable. This is the Bachelet "position held twice" example that MillenniumDB uses (S18, full-text).

### 8.2 The options

| Option | Encoding | Strengths | Failure modes (documented) |
|---|---|---|---|
| **Standard RDF reification** | `_:s rdf:subject/predicate/object` + extra triples | Standard | 4+ triples per fact; the asserted triple is separate from the reified one |
| **N-ary relation node** (W3C Note 2006, S26) | New node per relation instance, with role edges | Any arity; this is what Wikidata `p:/ps:/pq:` does | More joins; needs a statement ID |
| **Singleton properties** | Unique predicate per statement | — | Huge predicate vocabularies; problematic for several engines (Hernández/Hogan/Krötzsch 2015, search-summary) |
| **Named graphs** | One graph per statement | Provenance-friendly | Awkward SPARQL `GRAPH`; "SPARQL does not support querying paths that span named graphs" (S18) |
| **RDF\*** (Hartig & Thompson 2014, now marked obsolete) | `<< s p o >> q v` | Compact | Quoted triple identified by content, so **one node per (s,p,o)**: "if we add the qualifiers for both statements, then we would not know which start date pairs with which end date" (S18) |
| **RDF 1.2 triple terms + reifiers** (S67, editor's draft full-text) | `:s :p :o ~ :r1 {\| :q :v \|}`; `:r1 rdf:reifies <<( :s :p :o )>>` | Several reifiers per triple fixes the RDF\* identity problem | Spec state: editor's draft read. Candidate Recommendation (April 2026) is search-summary only. A "Basic" conformance level without triple terms exists, so tool support will be uneven. |
| **Property graph** (Neo4j/Cypher; ISO GQL 39075:2024) | Edge with key–value properties | Ergonomic; fast traversals | Edges are **binary** (one start and one end node); property values are literals, not nodes (S18). Conditions that are themselves entities (a taxon, a source) need an intermediate node, i.e. back to reification. |
| **Relational n-ary table** | One row per statement, with FK columns per role and typed qualifier rows | Simplest; integrity constraints; SQL; easy to stamp with a commit | A schema change per new role; graph traversal (clade descendants) needs recursive CTEs or a closure table |

Benchmarks are weak and mostly search-summary:
- Hernández, Hogan & Krötzsch 2015 found no single winner; Virtuoso was most robust; singleton properties were problematic.
- Frey et al. 2019 proposed "companion properties".
- Orlandi et al. 2021 (Stardog) found RDF\* had the fewest triples (61M vs 176M reified) and was faster on complex patterns, while reification was faster on simple queries.

### 8.3 Recommendation [inf]
**Canonical form: relational n-ary statements**, built as the derived index from git files. **RDF 1.2 (reifier form) and a Wikidata-style truthy view are exports.**

**Why relational:**
1. Our facts have fixed, known roles: law, scope, value, source, basis. Relational integrity (FKs, CHECKs, units) is cheaper than SHACL.
2. The derived index must be rebuildable and commit-stamped (§7). SQLite or Postgres does this trivially, and the repo already has `schema.sql`.
3. Statement identity is a primary key, so we never hit the RDF\* or property-graph collapse.
4. RDF 1.2 export gives semantic-web interoperability without making the triple store canonical. Wikidata's 2025 split is the cautionary tale.

**Sketch.** This is a *proposal*, not an existing schema:
```sql
law(law_id PK, version, form_expr, quantity_kind, ...)
statement(stmt_id PK, law_id FK, rank CHECK(rank IN ('preferred','normal','deprecated')),
          status CHECK(status IN ('holds','fails','disputed','variable','not_applicable')),
          basis CHECK(basis IN ('measured','fitted','assumed','derived')),
          value_num, value_unit, value_si, unc_lo, unc_hi,
          unc_kind CHECK(unc_kind IN ('sd','se','ci95','range','precision','unknown')),
          deprecation_reason, superseded_by FK)
scope_taxon(stmt_id FK, ncbi_taxid, inclusion CHECK(inclusion IN ('exact','clade')))
qualifier(stmt_id FK, qual_id FK→qualifier_def, num_lo, num_hi, unit, term_id)  -- typed, per-law-declared
qualifier_def(law_id FK, qual_id, quantity_kind, unit, allowed_terms)           -- Wolfram "Qualifiers"
reference(stmt_id FK, source_id FK, locator /* table/fig/eq */, retrieved)
observation(obs_id PK, stmt_id FK NULL, value..., organism, conditions..., source_id)  -- NIST "SOURCE" layer
taxon_closure(ancestor, descendant)   -- for clade queries
```

**Query: "which laws hold for which organisms under which conditions"**
```sql
SELECT l.law_id, s.stmt_id, t.ncbi_taxid, q.qual_id, q.num_lo, q.num_hi, q.unit, s.value_num, s.unc_kind
FROM statement s JOIN law l USING(law_id)
JOIN scope_taxon t USING(stmt_id)
LEFT JOIN qualifier q USING(stmt_id)
WHERE s.status = 'holds' AND s.rank <> 'deprecated';
```
Restricting to "...for this organism" adds a join through `taxon_closure`. "...where it breaks" is `status = 'fails'`. "...contested" is `status = 'disputed'`.

**Tradeoffs we accept:**
- adding a new kind of qualifier is a row in `qualifier_def`, not a schema change, but it must be declared;
- deep graph queries need the closure table;
- RDF consumers get an export, not live SPARQL.

**What would change this recommendation:**
- If cross-linking to Wikidata or other knowledge graphs at query time becomes a primary use case, add a SPARQL endpoint over the RDF 1.2 export, still derived.
- If laws turn out to need arbitrary new roles often, revisit the relational choice.

---

## 9. A first cut at a law-library entry: what to copy from whom [inf]

| Field | Source of the idea |
|---|---|
| `law_id`: permanent, never renamed, short and citable inline ("LAW-000123") | BNID; Wikibase "cannot be renamed" |
| `version`: content digest; old versions viewable; `withdrawn` state | SPEC-001 digest; Granta RHGUID/RGUID; BioNumbers |
| `form`: executable expression with typed variables, each `quantity` + `unit` | Modelica types; Wolfram `Quantity` |
| `dimensionless_groups`: named types, unit `"1"` | Modelica `ReynoldsNumber` |
| `qualifier_defs`: declared allowed conditions | Wolfram `"Qualifiers"`/`"QualifierValues"` |
| `statements[]`: scope (NCBI taxid + inclusion rule), qualifiers, value + uncertainty kind, basis, rank, status, references (source + locator) | Wikidata statements; BQB `hasTaxon`; NIST Method column |
| `status` vocabulary incl. `fails`, `disputed`, `variable`, `not_applicable` | Wolfram `Missing[...]` reasons |
| `observations[]`: raw measured examples with their own provenance | NIST SOURCE; BioNumbers rows |
| `examples/`: expected-pass and expected-fail checks with a tolerance | MSL `ReferenceResults` + `shouldPass=false` |
| `evidence_score`: adapted 8-question scorecard | Tiwari et al. 2021 |
| `function_tags`: against a *versioned* function vocabulary | AskNature taxonomy, versioned this time |
| `conversions`: old ID → new ID rules | Modelica `convertClass` |
| Build stamp on every derived artifact: commit SHA, tool version, date | MSL `revisionId` + `creation.txt` |

---

## 10. Gaps and what to verify next
1. **Wolfram (all of §2):** verify every syntax form against reference.wolfram.com. Find any primary statement on computed vs stored values.
2. **BioNumbers:** current entry count, maintenance status, and the book's citation format.
3. **ESDU:** item structure, amendment scheme and accuracy statements. This needs a subscriber copy.
4. **Granta MI:** whether a pedigree or provenance attribute exists in current schemas.
5. **RDF 1.2:** confirm the Recommendation status on w3.org before committing to the export syntax.
6. **WDQS:** which replacement engine was chosen.
7. **Dolt:** read the concurrency and merge docs directly.
8. **Physics-informed ML libraries:** not surveyed.
9. **Small inconsistency noticed:** the MSL release notes date 4.1.0 as both 2024-03-15 and 2025-05-23. It does not affect anything here.

---

## 11. Sources

| # | Source | Read-level |
|---|---|---|
| S1 | Wolfram, `EntityProperty` ref page, reference.wolfram.com/language/ref/EntityProperty.html | search-summary |
| S2 | Wolfram, `EntityValue` ref page; `ref/entity/Source.html` | search-summary |
| S3 | Wolfram, `CanonicalName` ref page; guide/KnowledgeRepresentationAndAccess | search-summary |
| S4 | Wolfram, `EntityClass` ref page | search-summary |
| S5 | Wolfram, `Missing` ref page | search-summary |
| S6 | Wolfram, `Around` ref page; S. Wolfram "Version 12 Launches Today" (2019) | search-summary |
| S7 | Wolfram Chemistry Team, "Measured Data" notebook (wolframcloud) | search-summary |
| S8 | Wolfram, `EntityStore` ref page | search-summary |
| S9 | Wolfram, `EntityRegister` / `EntityStores` / `$EntityStores` ref pages | search-summary |
| S10 | Wolfram, ResourceObject "Data" / Wolfram Data Repository docs | search-summary |
| S11 | Secondary accounts of W\|A curation (Bio-IT World 2011; Berkman talk notes 2009) | search-summary |
| S12 | S. Wolfram, "Wolfram\|Alpha at 10" (2019) | search-summary |
| S13 | Wikibase `docs/topics/json.md`, github.com/wikimedia/mediawiki-extensions-Wikibase | full-text |
| S14 | Wikibase `docs/topics/rdf-binding.md`; `repo/includes/Rdf/RdfVocabulary.php`, `FullStatementRdfBuilder.php`, `TruthyStatementRdfBuilder.php`, `Values/QuantityRdfBuilder.php` | full-text |
| S15 | Vrandečić & Krötzsch, "Wikidata: a free collaborative knowledgebase", CACM 57(10), 2014, doi:10.1145/2629489 | search-summary |
| S16 | Amaral, Piscopo, Kaffee, Rodrigues, Simperl, "Assessing the quality of sources in Wikidata across languages", arXiv:2109.09405 (2021) | full-text |
| S17 | Waagmeester et al., "Wikidata as a knowledge graph for the life sciences", eLife 9:e52614 (2020), PMC7077981 | full-text |
| S18 | Vrgoč et al., "MillenniumDB: a persistent, open-source, graph database", arXiv:2111.01540 | full-text (§1–2) |
| S19 | Piscopo, Kaffee, Phethean, Simperl, "Provenance information in a collaborative knowledge graph", ISWC 2017 | search-summary |
| S20 | Shenoy, Ilievski, Garijo, Schwabe, Szekely, "A study of the quality of Wikidata", arXiv:2107.00156 | full-text |
| S21 | Brasileiro et al., WWW 2016 Companion (multi-level theory on Wikidata); Dadalto et al. 2021 "Type or individual?" | search-summary |
| S22 | Ferranti et al., "Formalizing and validating Wikidata's property constraints using SHACL and SPARQL", Semantic Web J. 2024 | search-summary |
| S23 | Lubiana, Rasberry, Mietchen, "The Wikidata Query Service split and its impact on the scholarly graph", CEUR Vol-4064 (2025) | search-summary |
| S24 | Hanski, Crum, Taelman, client-side federation over Wikidata endpoints, CEUR Vol-4108 (2025); WDQS engine benchmark, same volume | search-summary |
| S25 | Wikimedia meta "WikiCite/WDQS graph split"; Phabricator T206560, T335067 | search-summary |
| S26 | Noy & Rector (eds.), "Defining N-ary Relations on the Semantic Web", W3C WG Note, 2006 | search-summary |
| S27 | Wikibase `docs/storage/entities.md`, `docs/storage/terms.md`, `docs/sql/wb_changes.md`, `docs/topics/change-propagation.md`, `repo/includes/EditEntity/MediaWikiEditEntity.php` | full-text (named files) |
| S28 | Milo, Jorgensen, Moran, Weber, Springer, "BioNumbers—the database of key numbers in molecular and cell biology", NAR 38:D750–3 (2010), PMC2808940 | full-text (re-checked directly) |
| S29 | Milo & Phillips, *Cell Biology by the Numbers*, Garland Science 2015, ISBN 978-0-8153-4537-4 | search-summary |
| S30 | AskNature "Biomimicry Taxonomy" page; Taxonomy Explainer 2021 (toolbox.biomimicry.org); AIES 2018 paper | search-summary |
| S31 | Deldin & Schuknecht, "The AskNature database: enabling solutions in biomimetic design", in Goel, McAdams & Stone (eds.), *Biologically Inspired Design*, Springer 2014, doi:10.1007/978-1-4471-5248-4_2 | search-summary |
| S32 | Biomimicry Institute annual reports 2023/2024; AskNature chat press release (2025) | search-summary |
| S33 | AskNature/AN-React README (GitHub); zju-d3/AskNatureNetData README (GitHub) | full-text |
| S34 | Emuna, Borenstein et al., "Imitation of Life: a search engine for biologically inspired design", arXiv:2312.12681 | full-text |
| S35 | Vandevenne et al., ICED 2011; AI EDAM 2015; SEABIRD, AI EDAM 30(1):78–95 (2016) | search-summary |
| S36 | Fayemi et al., "Biomimetics: process, tools and practice", Bioinspir. Biomim. 12 (2017); Wanieck et al., "Biomimetics and its tools" (2017); Sharma & Sarkar 2019 | search-summary |
| S37 | Kruiper, Vincent, Chen-Burger et al., Biomimetics 3(3):14 (2018); arXiv:2005.07751; arXiv:2005.07753 | search-summary |
| S38 | modelica/ModelicaStandardLibrary: `README.md`, `Modelica/package.mo`, `Modelica/Units.mo`, `ReferenceResults/…/BooleanNetwork1/*`, `Resources/Scripts/Conversion/Description.txt`, `ModelicaTestConversion4.mo`, `UsersGuide/ReleaseNotes.mo`, `.CI/Jenkinsfile` | full-text (named files) |
| S39 | modelica/ModelicaSpecification `chapters/annotations.tex`, `chapters/unitexpressions.tex` | full-text (named sections) |
| S40 | modelica/MAP-LIB_ProjectRules; modelica-tools/csv-compare README | full-text (excerpts) |
| S41 | OpenFOAM/OpenFOAM-dev @ 852527377c: `src/OpenFOAM/dimensionSet/*`, `unitSet/unitSet.H`, `tutorials/Alltest`, `tutorials/incompressibleFluid/pitzDaily/*` | full-text (named files) |
| S42 | OpenFOAM Foundation vs ESI versioning (OpenCFD/OpenFOAM-history; cfd-online; Wikipedia) | search-summary |
| S43 | Keating et al., "SBML Level 3: an extensible format for the exchange and reuse of biological models", Mol Syst Biol 16:e9110 (2020), PMC8411907 | full-text |
| S44 | libSBML `src/sbml/annotation/CVTerm.h` (GitHub) | full-text |
| S45 | sbml.org MIRIAM annotation syntax page | search-summary |
| S46 | Malik-Sheriff et al., "BioModels—15 years of sharing computational models in life science", NAR 48:D407–D415 (2020), PMC7145643 | full-text |
| S47 | Tiwari et al., "Reproducibility in systems biology modelling", Mol Syst Biol 17:e9982 (2021), PMC7901289 | full-text |
| S48 | Glont et al., "BioModels Parameters", Bioinformatics (2020), PMC7653554; Bergmann et al., COMBINE archive/OMEX, BMC Bioinformatics 15:369 (2014), arXiv:1407.4992 | full-text / abstract |
| S49 | Standard Reference Data Act, 15 USC 290a | search-summary |
| S50 | NIST Chemistry WebBook (SRD 69) species and citation pages | search-summary (host blocked) |
| S51 | TRC pages; ThermoML IUPAC papers | search-summary |
| S52 | Frenkel, Chirico, Diky, Yan, Dong, Muzny, "ThermoData Engine (TDE): software implementation of the dynamic data evaluation concept", J Chem Inf Model (2005) | search-summary |
| S53 | Accuris ESDU product pages; Aeronautical Journal ESDU listings | search-summary |
| S54 | Ansys Granta MI help (Glossary; Record Version Control; Parameters; Functional data) | search-summary |
| S55 | Granta MI Scripting Toolkit attribute definitions; LANL OSTI reports 1823720, 1891785, 2208790 | search-summary |
| S56 | MatWeb pages and help | search-summary |
| S57 | dolthub/dolt `README.md`, `go/libraries/doltcore/doltdb/system_table.go`, `sqle/dtables/conflicts_tables_prolly.go` | full-text (README) / code-grep |
| S58 | DoltHub blog/docs on three-way merge, conflicts and concurrency | search-summary |
| S59 | simonw/datasette `docs/performance.rst`, `docs/publish.rst`; simonw/sqlite-utils `docs/cli.rst` | full-text / partial |
| S60 | Willison, "Baked Data" (2021); "Git scraping" (2020); "git-history" (2021) | search-summary |
| S61 | wikimedia/wikidata-query-rdf `README.md`, `docs/getting-started.md`, `docs/diagrams/streaming-updater-sequence.puml`, `wdqs-high-level.puml` | full-text |
| S62 | SemanticMediaWiki: `docs/architecture/storing.annotations.md`, `database.schema.md`, `src/SPARQLStore/README.md`, `maintenance/rebuildData.php` | full-text (named files) |
| S63 | backstage/backstage `docs/features/software-catalog/life-of-an-entity.md` (+ `index.md`, `configuration.md`, `descriptor-format.md`, entity-providers) | full-text / partial |
| S64 | MediaWiki API edit-conflict parameters (ApiHelp mirrors) | search-summary |
| S65 | Obsidian / Dataview metadata cache discussions | search-summary |
| S66 | Terraform state locking (third-party write-ups) | search-summary |
| S67 | W3C RDF 1.2 Concepts and RDF 1.2 Turtle, editor's draft sources (github w3c/rdf-concepts, w3c/rdf-turtle); TR status | full-text (ED) / search-summary (status) |
| S68 | Hartig & Thompson, "Foundations of an alternative approach to reification in RDF", arXiv:1406.3399 | abstract |
| S69 | Hernández, Hogan, Krötzsch, "Reifying RDF: what works well with Wikidata?", SSWS 2015, CEUR 1457 | search-summary |
| S70 | Frey et al., "Evaluation of metadata representations in RDF stores", Semantic Web 10(2) (2019) | search-summary |
| S71 | Orlandi, Graux, O'Sullivan, "Benchmarking RDF metadata representations", IEEE ICSC 2021 | search-summary |
| S72 | Neo4j relationship model docs; ISO/IEC 39075:2024 GQL catalogue entry | search-summary / listing |
