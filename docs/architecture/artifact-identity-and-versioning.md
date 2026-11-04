# Artifact identity, versioning and metadata

**Status:** Research report + proposal · **Date:** 2026-11-04 · **Scope:** the identity and
provenance layer for a library of engineered-biology artifacts (designed proteins, complexes,
actuators, scaffolds, assemblies, mechanisms, and the rigs that build and test them)

> **Not legal advice.** Section 3 discusses patents, priority and prior art because the design
> of the timestamp layer depends on them. Nothing here is legal advice. The authors are not
> patent attorneys. Patent law varies by jurisdiction and changes. Before anything that might
> be patentable is disclosed, published or filed, a registered patent attorney or agent has to
> review it.

## How to read this document

The repository's rule is *read the citation before you cite it*
([`CONTRIBUTING-VERIFICATION.md`](../../CONTRIBUTING-VERIFICATION.md) §3), so every factual claim
about an external standard carries one of two marks:

- **[V]** was checked against a primary or near-primary source fetched or searched during the
  writing of this document (2026-11-04). The sources are in §10.
- **[M]** comes from the author's prior knowledge of the specification and was **not**
  re-checked this session. It is believed correct, but check it before you depend on it.

Every sentence that recommends something, as opposed to reporting it, starts with
**[Rec]**. Recommendations are collected and justified in §8.

Two sources could not be reached. `sbolstandard.org` did not resolve from the research
sandbox, so the SBOL 3 class-level details in §5 are **[M]** unless marked otherwise. Only the
SBOL 3.1.0 abstract and changelog were verified.

---

## 0. Summary

**The core tension.** An identifier can be *assigned*, meaning someone promises it stays the
same as the thing changes. Or it can be *content-derived*, meaning it is computed from the bytes
and so changes whenever they change. Integrity and patent claims need the second kind, because
a claim attaches to one exact composition. Catalogues and design lineages need the first kind,
because "the actuator, revision C" is still the same part. Every mature system carries both:
git (path, blob and tag), OCI (tag and digest), Zenodo (concept DOI and version DOI) and PLM
(item, revision and iteration). None of them manages with one identifier.

**[Rec] The proposal**, in one table:

| Layer | What it names | Form | Assigned or derived | Mutable? |
|---|---|---|---|---|
| **Item** | the part as a design lineage ("the gripper actuator") | UUIDv7 (RFC 9562), under a w3id.org namespace | assigned | never changes; its *latest released revision* pointer moves |
| **Revision** | a released, reviewable state of the item | `r1`, `r2`, … (monotonic integer) | assigned, then **bound forever** to one content digest | label is immutable once released |
| **Iteration** | any saved state, released or not | the store's existing `version` = sha256 of canonical record | derived | immutable |
| **Content** | the exact bytes of each file and polymer | `sha256:<hex>` per file, plus `ga4gh:SQ.<sha512t24u>` per sequence | derived | immutable |
| **Agents** | people and organisations | ORCID, ROR | assigned by third parties | stable |

**Timestamps.** Each day, build one Merkle tree over *salted commitments* to that day's
iterations. Anchor its root with RFC 3161 tokens from two independent TSAs and with a Sigstore
Rekor entry, and optionally with OpenTimestamps. That proves the bytes existed by a given time,
and it costs nothing. It does **not** establish patent priority, which in the US and Europe comes
only from a filing. It does **not** create prior art either, which only a *public, enabling*
disclosure does. §3 says exactly what each mechanism is worth.

---

## 1. Identifier schemes

### 1.1 Comparison table

| Scheme | Spec | Who guarantees persistence | Cost | Resolvable? | Derived or assigned |
|---|---|---|---|---|---|
| **DOI** | ISO 26324:2022 [M]; resolution via the Handle System | The registration agency (DataCite, Crossref, …) and the member, by **contract**. The URL behind a DOI is maintained by the depositor, so link rot is a social failure mode. | Crossref: lowest annual membership tier USD 275, plus per-record fees that vary by record type. Crossref has announced reductions from Jan 2027 [V]. DataCite: membership or consortium fee [M]. **Zenodo mints DataCite DOIs free** [M]. | Yes, `https://doi.org/…`, with content negotiation for metadata [M] | Assigned |
| **Handle** | RFC 3650/3651/3652 (2003, Informational) [M]; Global Handle Registry run by the DONA Foundation [V] | Whoever runs the local handle server, plus DONA and the multi-primary administrators for the prefix | CNRI historically charged USD 50 one-time plus USD 50 per year per prefix. Those figures are from 2016–17 and current fees are unverified [V] | Yes, via `hdl.handle.net` or your own server | Assigned |
| **ARK** | IETF Internet-Draft `draft-kunze-ark`, revision 42 (Nov 2025) [V]. **Not an RFC.** The draft itself says it is "work in progress" [V] | The NAAN holder (your organisation). The ARK Alliance runs the NAAN registry and the N2T resolver [M] | NAAN registration is free [M, unverified] | Yes, `https://n2t.net/ark:…` or your own resolver | Assigned |
| **PURL** | No formal spec; purl.org redirect service | The Internet Archive has run purl.org since 2016 [M] | Free | Yes (HTTP redirect) | Assigned |
| **w3id.org** | W3C Permanent Identifier Community Group; redirects are `.htaccess` rules in a public GitHub repository [M] | A volunteer community group. Your redirect rule persists as long as the repository and the service do | Free (a pull request) | Yes (HTTP redirect) | Assigned |
| **UUID v4** | RFC 9562 (May 2024; obsoletes RFC 4122) [M] | Nobody needs to: uniqueness is probabilistic (122 random bits) | Free | **No.** Only an identifier | Assigned (random) |
| **UUID v7** | RFC 9562 §5.7 [M] | Same as v4 | Free | No | Assigned (time-ordered) |
| **ULID** | Community spec, github.com/ulid/spec [M]. **No standards body** | Same as UUID | Free | No | Assigned (time-ordered) |
| **git object id** | Git object model; SHA-1 by default, SHA-256 object format available. Git 3.0 plans SHA-256 as the default for new repositories; GitHub support is the reported blocker [V] | Nobody: content-derived. Persistence is whoever keeps the object | Free | Only inside a repository or an archive such as Software Heritage | Derived |
| **SWHID** | ISO/IEC 18670, published April 2025 [V]. Still uses SHA-1 (git-compatible), with a version prefix reserved for a future hash (`swh:2:`) [V] | Software Heritage archives the content | Free | Yes, via the Software Heritage archive | Derived |
| **IPFS CID** | multiformats CID spec (CIDv1 = multibase + version + multicodec + multihash) [M] | **Nobody.** Content is retrievable only while someone *pins* it | Free to compute; pinning costs money | Only via IPFS or a gateway, and only while pinned | Derived |
| **Nix store path** | Nix manual; `/nix/store/<32-char base32 hash>-<name>` [M] | Your binary cache | Free | Inside Nix or a substituter | **Input**-derived by default (§2.3) |
| **OCI digest** | OCI Image Spec v1.1 (2024) [M]: `algorithm:encoded`, e.g. `sha256:…` | The registry, while the blob is referenced | Free to compute | `registry/name@sha256:…` | Derived |
| **GA4GH `SQ.` digest** | GA4GH refget / VRS computed identifiers: first 24 bytes of SHA-512, base64url, prefixed `SQ.` for a sequence [V] | Nobody: content-derived. Any refget server can serve it | Free | Through refget servers, for sequences they hold | Derived |
| **ORCID** | 16 digits with an ISO/IEC 7064 MOD 11-2 check character [M] | ORCID Inc., a non-profit funded by members | Free for individuals | Yes, `https://orcid.org/…` | Assigned |
| **ROR** | 9 characters: a leading `0`, six Crockford-base32 characters and a two-digit checksum [M] | The ROR community (CDL, Crossref, DataCite, Digital Science) [M] | Free (CC0 data) | Yes, `https://ror.org/…` | Assigned |

### 1.2 Notes per scheme

**DOI.** A DOI is a Handle with prefix `10.` and an agency attached. The agency is what makes
it persistent. DataCite and Crossref require members to keep metadata and landing URLs current,
and DataCite's metadata kernel is the de facto description record (§4.2). The useful, often
missed feature here is **Zenodo's concept DOI**: one DOI that always resolves to the latest
version of a record, alongside one DOI per version [M]. That is item and revision expressed in
DOIs, and it maps one-to-one onto the proposal in §8. DOIs belong to publication. They are not
a working-store identifier, because minting one is a public act and the metadata becomes public.

**Handle.** The machinery under DOI. Running your own Handle server buys resolution without an
agency, but you also become the persistence guarantor, which is exactly the burden a small team
should not take on. Little new adoption outside DOI and DSpace [M].

**ARK.** Designed for archives. Distinctive features: they are free, the NAAN holder controls
the namespace, and the `?info` inflection returns metadata. Persistence is explicitly a *policy*
of the holder, not a property of the syntax. Adoption is real in libraries and in some
biodiversity and museum collections, and low elsewhere [M]. The specification has been an
Internet-Draft since 2001 and is still revision 42 in 2025 [V]. That is not a defect in
practice, but it should be stated.

**PURL.** Historically important. The OCLC-to-Internet-Archive transition in 2016 [M] is a case
study in how a persistence guarantee is only as good as its operator's succession plan. Little
new adoption. w3id.org has largely taken over its niche for vocabularies and ontologies.

**w3id.org.** The cheapest credible way to get a persistent HTTP namespace that you do not have
to host. RO-Crate's own permalink is `https://w3id.org/ro/crate/1.2` [V], which shows that a
standards body trusts it. Its weakness is governance: it depends on a volunteer community group.
Its strength is that a redirect rule can be repointed when your hosting changes, so the
identifiers survive a move. That is the whole job of a persistent namespace.

**UUID v4 vs v7.** RFC 9562 defines v7 as a 48-bit big-endian Unix-epoch **millisecond**
timestamp, a 4-bit version, 12 bits `rand_a`, a 2-bit variant and 62 bits `rand_b` [M]. Why the
time ordering matters:

1. **Index locality.** Random v4 keys spread inserts across a B-tree, which causes page splits,
   cache misses and write amplification. v7 keys arrive in roughly ascending order, so inserts
   land on the right-hand edge of the index. At thousands of artifacts this hardly matters, but
   at millions of iterations and events it does.
2. **Sortable without a join.** Sorting by id gives you creation order, which helps with
   pagination cursors, log scanning and debugging.
3. **Merging.** Two independently generated id sets interleave in time order, which is useful
   for federation (SPEC-004).

**The embedded timestamp is not evidence of anything.** The generating machine's clock sets it.
It is a hint. Two consequences follow:

- (a) Anyone who sees the id learns roughly when it was created. That is usually harmless, but
  it is a leak.
- (b) It must never be cited as a creation date for precedence purposes (§3).

**ULID.** A 48-bit millisecond timestamp plus 80 random bits, encoded as 26 Crockford-base32
characters [M]. It is pleasant to read and paste. Since RFC 9562 standardised v7, ULID's
advantages are cosmetic: it has no standards body, and the 128 bits fit a UUID column anyway.
**[Rec]** Do not adopt ULID. If a short human-friendly rendering is wanted, render the v7 UUID
in Crockford base32 for display only.

**Content-addressed identifiers.** The general rule is that a content id is **self-verifying
but not self-persisting**. A CID, a git id or an OCI digest tells you whether the bytes you hold
are the right ones. It does not tell you where to get them, and nobody promises they will exist
tomorrow. That is why SWHID matters: it pairs a git-compatible content id with an institution,
Software Heritage, that commits to keeping the bytes.

**ORCID and ROR.** These are the agent identifiers. They are free, widely adopted, and natively
supported by DataCite, RO-Crate and schema.org. **[Rec]** Every human contributor is recorded
by ORCID and every organisation by ROR. Software and model agents get their own content-pinned
identity (§6).

---

## 2. Content addressing vs assigned identifiers

### 2.1 The tension, precisely

A content hash `H(bytes)` has two properties that are both features and bugs:

- It **changes on any change**. That is right for integrity, for patents (a claim attaches to
  one composition) and for caching. It is wrong for "is this still the gripper actuator?"
- It **is the same for the same bytes, whoever computes it**. That is right for deduplication
  (two teams designed the same sequence) and for federation. It is wrong if you want two
  deliberately distinct items that happen to share a sequence.

An assigned id has the opposite properties. Every real system below resolves this by
**layering**: a mutable *name* points to an immutable *content* address, and the history of the
pointer is itself recorded.

### 2.2 git

Git has four object types: blob, tree, commit and tag, each addressed by the hash of its
serialised form [M].

- A **blob** is pure content and has no name. Rename a file and its blob id is unchanged.
- A **tree** binds *paths* to blob ids. The path is the closest thing git has to an item: the
  identity of "the file called `actuator.fasta`" persists across edits only because the path
  persists.
- A **commit** binds a tree to its parents, so it is the iteration, with an author timestamp
  that is self-asserted and therefore worthless as evidence.
- An **annotated tag** is a signed, named pointer to a commit, which makes it a revision.
  Lightweight tags and branches are mutable references outside the object store.

**Lesson:** the *name → content* binding (tree entry) and the *name history* (commit chain) are
separate objects, and only the history is hash-chained.

**Weakness:** git has no stable identity for a *file* across renames. `git log --follow` guesses
by similarity. **[Rec]** Never derive item identity from a path.

### 2.3 Nix

Nix shows a third possibility, which matters for a design pipeline. A default store path is
**input-addressed**: the hash is computed from the *derivation*, meaning the build recipe and the
store paths of all its inputs, not from the output bytes [M]. Two consequences:

- You know the output's address **before** building it. That is what makes binary caches work.
- If a build is non-deterministic, the same input-addressed path can hold **different bytes** on
  two machines. Nix detects this only with `--check` or `diff-hook` [M].

*Fixed-output derivations*, such as a fetched tarball with a declared hash, are content-addressed.
Full content-addressed derivations (`ca-derivations`) remain an experimental feature [M].

**Lesson for us:** a design run has a natural **input address**, the hash of (model weights
digest, code commit, inputs, parameters, seed), and a separate **output address**, the hash of
the produced sequence or structure. Recording both makes non-determinism visible: same input
address, different output address. That is a reproducibility alarm (§6).

### 2.4 OCI

In the OCI image and distribution specs [M]:

- A **digest** (`sha256:…`) addresses a blob or manifest immutably.
- A **tag** is a mutable, registry-side pointer to a manifest digest.
- `name@sha256:…` pins exactly. `name:tag` is a convenience that can move under you.

Image Spec v1.1 added `subject` and the referrers API, so signatures, SBOMs and attestations can
be attached to a digest *without changing it* [M].

**Lessons:**

1. The tag/digest split is item/content.
2. Attestations about an artifact must point *at* its digest and live *beside* it, not inside
   it. Otherwise adding a review changes the thing reviewed.

This repository already learned the second lesson: assessments are separate records that `Ref`
a version digest (SPEC-001).

### 2.5 PLM: item, revision, iteration

Product lifecycle management systems such as PTC Windchill and Siemens Teamcenter [M] separate:

- **Item** (the part number): a stable identity, often with a classification.
- **Revision** (A, B, C…): a *released* state that went through a change process, such as an
  engineering change order with approval.
- **Iteration** (A.1, A.2…): working saves inside a revision, invisible downstream.

The governing rule is **form, fit, function (FFF) interchangeability** [M]. If the new state is
interchangeable with the old one in every use, it is a new *revision* of the same item. If it
is not interchangeable, it gets a new *item number*, because everything that referenced the old
number would otherwise silently receive something that no longer fits.

**This is the single most transferable idea in this report.** Translated to molecules:

- A redesign that keeps the role (same binding target, same interface residues, same assembly
  partners) and improves a property is a **new revision**.
- A change that alters the interface, the stoichiometry or the partner set breaks
  interchangeability with every assembly that uses it. That is a **new item**, linked by
  `prov:wasDerivedFrom`.

**[Rec]** Adopt FFF as the written rule for deciding between a new revision and a new item, and
record the reason on every revision as `change_class` (§8.5).

### 2.6 Zenodo and DataCite

A Zenodo **concept DOI** names all versions and resolves to the latest. A **version DOI** names
one version. DataCite relation types `IsVersionOf`, `HasVersion`, `IsNewVersionOf` and
`IsPreviousVersionOf` express the links [M]. This is the publication-layer form of item and
revision.

### 2.7 What carrying both looks like, abstractly

```
Item (assigned, eternal)  ──has revision──▶  Revision r3 (assigned label, bound once)
                                                  │ is exactly
                                                  ▼
                                   Iteration = sha256(canonical record)   ◀── predecessor chain
                                                  │ contains
                                                  ▼
                       per-file sha256 · per-sequence ga4gh:SQ.… · per-component content ids
```

Three invariants make it sound:

1. **A released revision label is bound to exactly one iteration digest, forever.** Moving it
   is forbidden. You issue `r4` instead. This is a git signed tag that may never be force-moved.
2. **References between artifacts pin content, not names.** An assembly cites the iterations of
   its parts, not "latest". SPEC-001's `Ref` already pins a version digest. Keep it.
3. **The pointer history is itself content-addressed.** Every revision release is an event
   record with its own digest and its own place in the timestamp tree (§3, §8.6).

---

## 3. Timestamping and precedence

> **Not legal advice.** This section describes mechanisms and the general legal landscape so the
> engineering can be designed sensibly. Every decision about disclosure, filing or publication
> goes through a registered patent practitioner.

### 3.1 What we might want to prove

These are four different things, and conflating them is where most of the theatre comes from:

| Want to prove | Who asks | What actually proves it |
|---|---|---|
| **Existence**: these exact bytes existed no later than time T | Anyone: a collaborator, an auditor, a court | A trusted third party binding a hash to a time: an RFC 3161 TSA, a transparency log, a blockchain anchor, or an archive deposit |
| **Disclosure**: the public could access this by time T | A patent examiner or court assessing prior art | **Public accessibility** of an **enabling** description. A hash in a log is *not* a disclosure. |
| **Priority**: we are entitled to date T for a patent claim | The patent office | A **patent filing** (provisional or non-provisional) whose disclosure supports the claim |
| **Inventorship/conception**: person X conceived this by T | A derivation proceeding, an inventorship dispute | Corroborated records: dated notebooks, witnesses, and existence proofs as supporting evidence |

### 3.2 Mechanisms

**RFC 3161 Time-Stamp Protocol** (August 2001; updated by RFC 5816, 2010, to allow SHA-2 in the
signing-certificate attribute) [M]. You send a hash. The Time-Stamping Authority returns a
signed token binding that hash to its clock and its policy OID.

- *Trust model:* you trust the TSA's key, clock and audit. Tokens are verifiable offline for as
  long as the TSA's certificate chain can be validated, and long-term archival requires
  re-timestamping before algorithms or certificates age out (the RFC 4998 ERS model) [M].
- *Legal weight:* in the EU, a **qualified** electronic time stamp under eIDAS (Regulation (EU)
  No 910/2014, Art. 41, as amended by Regulation (EU) 2024/1183) enjoys a legal presumption of
  the accuracy of the date and time and of the integrity of the data [M]. That is the strongest
  statutory footing of any mechanism here. In the US there is no equivalent statutory
  presumption [M]. A token is ordinary documentary evidence, though a credible one.
- *Cost:* free public TSAs exist, and qualified TSAs charge [M].
- **[Rec]** Use two independent TSAs, so that one TSA's compromise or disappearance does not
  orphan the record.

**Certificate Transparency** (RFC 6962, 2013, Experimental; CT 2.0 is RFC 9162, 2021,
Experimental) [M]. It is not a timestamping service for your data. It is the *architecture*
worth copying:

- an append-only Merkle log;
- signed tree heads;
- inclusion proofs (this leaf is in the log) and consistency proofs (today's log extends
  yesterday's);
- independent monitors and witnesses who make silent rewriting detectable.

The leaf and node hashing with domain-separation prefixes (`0x00` for leaves, `0x01` for nodes)
is the standard way to build such a tree [M]. **[Rec]** Copy that construction for the daily
batch tree in §8.6.

**Sigstore Rekor.** A public transparency log for signatures and attestations. **Rekor v2**
reached general availability in October 2025. It is tile-based, built on Trillian-Tessera, with a
single write endpoint `/api/v2/log/entries`, per-shard hostnames distributed via TUF, and a 99.5%
availability SLO for the public instance. Integrated witnessing had not yet shipped at GA [V].

- Its timestamp is the log's integrated time, attested by the log operator. Rekor v2 relies on
  timestamps from separate timestamp authorities more than v1 did [M, verify].
- Entries are **public and permanent**, *including the signer identity*. With keyless signing,
  that is the OIDC email or workload identity [M].
- **[Rec]** Log only digests, never content. Sign with an organisational workload identity
  rather than a personal email.

**Git commit signing** (GPG, SSH or Sigstore `gitsign`). This proves *who* signed, not *when*.
Commit author and committer dates are whatever the committer's machine said. On its own, a
signed commit has **no** precedence value. It gains some when combined with a third-party
record of when it appeared:

- A push to a hosted forge leaves server-side records, but these are not designed or documented
  as evidence [M].
- An archive by Software Heritage records a visit date, and an archive is a better witness [M].
- `gitsign` with Rekor gives a log-attested time [M].

**Blockchain anchoring** (e.g. OpenTimestamps on Bitcoin) [M]. You commit a hash, aggregators
build a Merkle tree, and the root lands in a block. The proof shows the hash existed **no later
than** that block's time, give or take block-time slop of up to about two hours.

- *Strengths:* no trusted party, free, and verifiable by anyone with the chain, indefinitely.
- *Weaknesses:* courts and patent offices are not used to it, and it proves existence only.
- We are not aware of authority in US patent practice treating a blockchain anchor as more than
  ordinary corroborating evidence [M].

It is a cheap extra witness. It is not a replacement for the above.

**Archive deposits.** Zenodo, Software Heritage, the Internet Archive and institutional
repositories record a deposit time in an institution's systems [M]. This is evidence of
*existence* when the deposit is closed or embargoed, and of *disclosure* when it is open.

### 3.3 Patents: what establishes precedence

These points are background for engineering, not advice.

- **The US is first-inventor-to-file** for applications with an effective filing date on or
  after 16 March 2013, under the America Invents Act (35 U.S.C. §§100(i), 102) [M]. Under AIA
  there is no general mechanism by which an earlier *conception date* defeats an earlier
  *filing*. Interference proceedings are gone for AIA patents and replaced by **derivation
  proceedings** (35 U.S.C. §135), where the question is whether someone derived the invention
  *from you* [M].
- **Europe has absolute novelty.** EPC Art. 54(2): the state of the art is everything made
  available to the public before the filing date. Art. 55 excludes only evident abuse and
  certain officially recognised exhibitions within six months [M]. **There is no general grace
  period for your own publication.**
- **The US has a one-year grace period for the inventor's own disclosures** (35 U.S.C.
  §102(b)(1)) [M]. It does not help in Europe.

What follows for engineering:

1. **A private timestamp does not get you a patent date.** Only a filing does. A hash in Rekor,
   an RFC 3161 token or a Bitcoin anchor proves that you held some bytes. It establishes no
   priority, and since it discloses nothing, it is not prior art against anyone.
2. **Private timestamped records still matter**, for:
   - (a) derivation proceedings, where you show you had it first and they got it from you;
   - (b) the prior-user-rights defence under 35 U.S.C. §273, which has its own commercial-use
     timing requirements [M];
   - (c) inventorship disputes;
   - (d) showing that a later public disclosure was *your own*, for the §102(b)(1) exception;
   - (e) trade-secret evidence.

   Courts require **corroboration** of an inventor's testimony about conception, under a "rule
   of reason" (Federal Circuit case law, e.g. *Price v. Symsek*, 988 F.2d 1187 (1993)) [M].
   Third-party-timestamped, signed, content-pinned design records are good corroboration. They
   are better than self-dated files, and still not sufficient alone.
3. **A public git push is a public disclosure.** If this repository, a mirror or a log entry
   carries an enabling description (a sequence plus enough to make and use it), that is very
   likely a disclosure that destroys European novelty from that moment. **[Rec]**
   Patent-candidate artifacts live only in a private store until counsel clears them. Only
   salted commitments are ever written to public logs.
4. **Salt your commitments.** A bare `sha256(sequence)` of a 100-residue designed protein cannot
   be inverted by brute force: there are 20^100 candidates. But a design is often **one or two
   mutations from a public sequence**. There are only 19 × L single mutants, about 1,900 for
   L = 100, and about 1.8 million double mutants. Anyone can hash all of them and test them
   against a public digest. A public unsalted hash of a near-public sequence therefore *is* a
   disclosure of which variant you made. **[Rec]** Publish only
   `sha256(salt ‖ content_digest)` with a private 256-bit random salt. Reveal the salt when, and
   only when, you choose to prove the commitment.

### 3.4 Provisional patent applications: what one requires

US practice [M unless marked]:

- **Statute:** 35 U.S.C. §111(b). Benefit is claimed by a later non-provisional under §119(e)
  within **12 months**. The period is not extendable, except for a limited restoration of up to
  two further months if the delay was unintentional [M].
- **What must be filed:**
  - a specification that meets **35 U.S.C. §112(a)**, meaning written description and
    enablement. Since the AIA, §119(e)(1) expressly excludes the best-mode requirement for
    priority purposes [M].
  - drawings where necessary to understand the invention;
  - a cover sheet naming the inventors;
  - the fee. Effective 19 January 2025: USD 325 large entity, USD 130 small, USD 65 micro, with
    a size surcharge above 100 sheets [V, secondary sources; confirm on uspto.gov].
- **What is not required:** claims, an oath or declaration, and an information disclosure
  statement. A provisional is never examined and never published unless a later application
  claiming it is published [M].
- **Sequence listings:** provisionals are **not required** to include one. If one is included in
  an application filed on or after 1 July 2022, it must comply with 37 CFR 1.831–1.835, which is
  WIPO ST.26 XML [V, USPTO sequence-listing pages]. Non-provisional applications disclosing
  qualifying sequences must include an ST.26 listing [V].
- **A provisional is only worth what it discloses.** A later claim gets the provisional's date
  only if the provisional supports that claim under §112(a) [M]. For a provisional to make
  *someone else's* patent prior art as of the provisional's date (pre-AIA §102(e)), the
  provisional must support at least one claim of that patent. That is *Dynamic Drinkware v.
  National Graphics*, 800 F.3d 1375 (Fed. Cir. 2015) [V]. A 2018 USPTO memo and later PTAB
  decisions say that rule does not carry over to AIA prior-art determinations [V, secondary
  sources].

  Engineering consequence: a provisional containing a bare sequence with no function, no method
  of making and no data may not support the functional claims you will want later. The
  characterisation metadata in §8.5 is what a practitioner would draft from.
- **Inventors must be natural persons.** That was decided in *Thaler v. Vidal*, 43 F.4th 1207
  (Fed. Cir. 2022) [M]. The USPTO's revised guidance on AI-assisted inventions took effect 28
  November 2025 and withdrew the February 2024 guidance. It treats AI as a tool, "analogous to
  laboratory equipment", and applies the ordinary conception test. Under it, the *Pannu*
  joint-inventorship factors apply only among human contributors [V, law-firm summaries; read
  the Federal Register notice]. **Engineering consequence:** the provenance record must show
  *which human* conceived *what*, for example by choosing the target, specifying the
  constraints, or selecting and modifying outputs, as distinct from what a model generated.
  §6 builds this in.
- **Subject-matter background:** non-naturally-occurring compositions are generally
  patent-eligible (*AMP v. Myriad*, 569 U.S. 576 (2013)). Broad functional genus claims face
  stringent enablement scrutiny (*Amgen v. Sanofi*, 598 U.S. 594 (2023)) [M]. Both bear on what
  characterisation data is worth keeping.

### 3.5 Defensive publication

If the goal is to **stop others patenting** something rather than to patent it ourselves, the
instrument is a **public, enabling, dated disclosure**:

| Venue | Cost | Notes |
|---|---|---|
| **Technical Disclosure Commons** | Free | Indexed by Google Patents; anonymous publication allowed; automatic date stamp [V, secondary source] |
| **IP.com Prior Art Database** | Paid per disclosure; the current price is not verified [V] | Long-standing; marketed for examiner visibility [M] |
| **Research Disclosure** (Questel) | Paid; per-page pricing in older sources [V, dated] | The traditional defensive-publication journal |
| **Zenodo** | Free | Immediate DataCite DOI; public deposit date; versioning [M] |
| **bioRxiv / arXiv** | Free | Moderated: not every engineering disclosure is accepted [M] |
| **A public repository** (GitHub, this repo) | Free | Counts if publicly accessible and findable [M], but weaker evidence of the date and of indexing than the above |

For a disclosure to work as prior art it must be **publicly accessible**, meaning interested
persons exercising reasonable diligence could find it, and **enabling**: a skilled person could
make the thing from it [M].

**Credible vs theatre:**

| Credible | Theatre |
|---|---|
| A filing, for priority | "We put the hash on a blockchain, so we have priority." No: priority comes only from a filing. |
| A public enabling deposit with an institutional date, for prior art | "Our commit is dated 3 March." No: self-asserted. |
| Third-party timestamps plus signed, content-pinned records, as corroboration of conception and possession | "This UUIDv7 encodes the creation time." No: it is the client's clock. |
| — | "The hash is public, so it is disclosed." No: a hash discloses nothing, unless it is unsalted and brute-forceable (§3.3), in which case it may disclose more than you meant. |

---

## 4. Metadata standards

### 4.1 Dublin Core

DCMI Metadata Terms (the 15-element set is ISO 15836-1:2017) [M]. This is the lowest common
denominator: title, creator, date, identifier, relation, rights. It is universally understood
and too thin to characterise anything. **Use:** as the floor that every export can map to.

### 4.2 DataCite Metadata Schema

The current version is **4.6**, released 5 December 2024 [V]. Mandatory properties are
Identifier, Creator, Title, Publisher, PublicationYear and ResourceType [M]. The value of
DataCite to us:

- **`relatedIdentifier` with `relationType`.** This is a controlled vocabulary of typed links
  (`IsVersionOf`, `IsDerivedFrom`, `IsPartOf`, `HasPart`, `IsDocumentedBy`, `IsSupplementTo`, …)
  that a DOI resolver and aggregators understand [M].
- `nameIdentifier` for ORCID and `affiliationIdentifier` for ROR [M].
- `fundingReference`, `rights`, and `date` with a `dateType` (Created, Issued, Updated,
  Available, Withdrawn) [M].

**Use:** the mandatory export for any revision that gets a DOI.

### 4.3 schema.org/Dataset and Bioschemas

`schema.org/Dataset` is what Google Dataset Search indexes [M]. **Bioschemas** profiles extend
schema.org for life-science types, including Protein, Sample and LabProtocol [M]. **Use:** an
embedded JSON-LD block on every public landing page, for discoverability. Do not use it as a
system of record.

### 4.4 Croissant

MLCommons' metadata format for ML-ready datasets is built on schema.org and JSON-LD. **Version
1.1** was published 2026-01-29 at `http://mlcommons.org/croissant/1.1`. It adds
machine-actionable provenance, links to domain ontologies, usage-policy vocabularies and
multi-dimensional array fields [V]. Hugging Face, Kaggle and OpenML embed it [V]. The spec is
licensed CC BY-ND 4.0 [V].

**Use:** when the library is exported *as a training dataset*, for example sequences plus
measured properties for a property predictor. It is not an artifact record format.

### 4.5 RO-Crate

Research Object Crate packages files plus a JSON-LD `ro-crate-metadata.json` that describes
them with schema.org terms. **1.2** was published 4 June 2025, permalink
`https://w3id.org/ro/crate/1.2`. It formalised **profiles**, **detached crates** and referencing
other crates [V]. The specification site now lists **1.3** as the current long-term release [V].
We did not review 1.3's changes. Workflow RO-Crate and Provenance Run Crate profiles describe
computational runs [M].

**Use:** **[Rec]** the bundle format for exporting a revision with its files, its provenance and
its SBOL document, in a form other tools can open. A crate's `@id`s can be our w3id URIs, and
file entries can carry `sha256`.

### 4.6 PROV-O

W3C Recommendation, 30 April 2013 [M]. Core classes are `prov:Entity`, `prov:Activity` and
`prov:Agent`. Core relations are `wasGeneratedBy`, `used`, `wasAssociatedWith`,
`wasAttributedTo`, `wasDerivedFrom` and `actedOnBehalfOf`. Two less-known relations map
**exactly** onto the item and revision model [M]:

- `prov:wasRevisionOf`, a sub-property of `wasDerivedFrom`, for a revised version of an entity.
- `prov:specializationOf`, for an entity that is a more specific aspect of another. A revision
  is a specialisation of its item, and the item is the general entity.

Qualified forms (`prov:qualifiedAssociation` with `prov:hadPlan`, and `prov:qualifiedUsage`
with `prov:hadRole`) carry "which config, in which role". §6 applies PROV-O in detail.

### 4.7 FAIR, applied concretely

Wilkinson et al., *Sci Data* 3:160018 (2016) [M]. The FAIR principles are guidance, not a
format. Applied to this library:

| Principle | Concretely, for us |
|---|---|
| F1 globally unique, persistent id | w3id URI + UUIDv7 item; content digests for exact states |
| F2 rich metadata | the §8.5 mandatory set |
| F3 metadata names the data's id | every record carries its own item id, revision and digest |
| F4 indexed | public revisions get DataCite DOIs and schema.org JSON-LD |
| A1 retrievable by id over a standard protocol | HTTPS resolution of w3id → store API |
| A1.2 authentication where needed | private visibility, already in SPEC-001 |
| **A2 metadata persists even if data is gone** | **Conflicts with IP confidentiality.** Metadata can itself disclose. **[Rec]** Before clearance, A2 is satisfied only *internally*. Withdrawn public revisions keep a tombstone landing page. |
| I1–I3 formal, shared vocabularies, qualified references | Sequence Ontology, SBO, GO, ChEBI, UniProt/PDB cross-references, OM or QUDT units |
| R1.1 licence | an explicit licence and IP-status field |
| R1.2 provenance | PROV-O, §6 |
| R1.3 community standards | SBOL 3, RO-Crate and DataCite exports |

### 4.8 Minimum-information checklists

- **MIAME**: Brazma et al., *Nat Genet* 29:365–371 (2001) [M]. Microarray experiments.
- **MIAPE**: Taylor et al., *Nat Biotechnol* 25:887–893 (2007) [M]. Proteomics.
- **MIBBI**: Taylor et al., *Nat Biotechnol* 26:889–896 (2008) [M]. The umbrella effort that
  catalogued checklists. Its role is now largely played by the FAIRsharing registry [M].
- **ModelCIF** is an extension of PDBx/mmCIF for computed structure models. It records the
  modelling software, its version and parameters, the templates, and quality scores. The ModelArchive
  repository uses it [M]. It is the closest existing standard for **predicted structures of
  designed proteins**. **[Rec]** Store predicted structures as ModelCIF.

What these checklists teach is that the checklist, not the format, is what made the data
reusable. They name the *minimum* a reviewer can demand before accepting a deposit. We did not
find an established minimum-information standard for **de novo designed proteins** or for
molecular machines. That is a gap, and §8.5 proposes our own. *This is a search-scope
statement, not proof of absence.*

### 4.9 Registry of Standard Biological Parts (iGEM) and BioBrick numbering

Part identifiers look like `BBa_B0034` and `BBa_J23100`: the `BBa_` prefix, then a letter code
for the part class or originating team, then a number [M]. The Registry accepts only parts
compatible with the **RFC 10** BioBrick assembly standard, which forbids four specific
restriction sites inside a part [V]. It holds over 84,000 parts [V, Wikipedia citing iGEM], and
it was moved to a new server in 2024 [V].

**What went wrong.** This is the cautionary tale this design has to avoid. Items marked [M] are
widely discussed in the synthetic-biology literature; specific prevalence numbers are not cited
here because we did not re-read the source studies.

1. **Identity was not bound to content.** A part page is a mutable wiki page. The sequence shown
   could be edited, and the number did not pin the sequence that had been characterised [M].
2. **The physical sample and the record diverged.** Distribution-kit DNA did not always match the
   registry sequence, and identity was asserted by the record rather than verified against the
   sample [M]. The 2024 Twist Bioscience partnership moves teams away from shipping physical
   samples [V].
3. **Characterisation was optional**, so most parts lacked quantitative data. A part number
   carried no evidence of function. "Standard parts" were standard in *assembly* format, not in
   *behaviour* (e.g. Vilanova & Porcar, *Nat Biotechnol* 32:420 (2014), on the case for
   refounding iGEM's parts model [M]).
4. **Semantics were encoded in the identifier.** Letter codes mixed part type and origin, so the
   identifier carried meaning that could become wrong.
5. **There was no revision model.** An improved part either overwrote the page or got an
   unrelated new number, so lineage was lost.
6. **The assembly standard was baked into admission.** RFC 10 compatibility was a precondition,
   coupling *what a part is* to *how it is assembled*. Golden Gate and Gibson assembly later made
   that coupling a liability [M].

**[Rec]** Each of the six becomes a rule in §8:

1. content digests;
2. a verified-sample link;
3. a mandatory characterisation-status field;
4. opaque ids;
5. the item/revision split;
6. the assembly method as metadata, never an admission criterion.

---

## 5. SBOL in depth

### 5.1 Status and citations

- SBOL 3.0: McLaughlin et al., *J Integr Bioinform* 17(2–3):20200017 (2020) [M].
- **SBOL 3.1.0**: Buecherl et al., *J Integr Bioinform* 20(1):20220058 (2023),
  doi:10.1515/jib-2022-0058 [V]. Changes in 3.1.0 [V, abstract]:
  - the `Namespace` class was removed and replaced by a `namespace` property on each class;
  - `CombinatorialDerivation` was generalised to use Features and Measures directly;
  - Participations may now have Interactions as participants;
  - Feature orientation now uses Sequence Ontology terms;
  - identifiers were generalised from URIs to **IRIs**.
- The data model is RDF. It is serialised as RDF/XML, Turtle, JSON-LD or N-Triples [M].
  libSBOL3 and pySBOL3 implement it [M]. SynBioHub is the community repository [M].

### 5.2 What SBOL 3 models well

Class-level details are **[M]**; the spec site was unreachable from the research sandbox.

- **Components and composition.** `Component` is the universal design unit: DNA, RNA, protein,
  small molecule, complex or functional module, typed with SBO and ontology terms. It has
  `Feature`s:
  - `SubComponent` is an instance of another Component, and is how hierarchy happens.
  - `SequenceFeature` is a located annotation.
  - `ComponentReference` reaches into a SubComponent's features.
  - `LocalSubComponent` is an anonymous local part.
  - `ExternallyDefined` points to an external database entry, such as a ChEBI small molecule or
    a UniProt protein.

  This hierarchy expresses **protein complexes and assemblies** naturally: a complex is a
  Component of type *non-covalent complex* whose SubComponents are the chains, and an assembly
  is a Component of Components.
- **Interfaces.** `Interface` declares which Features are `input`, `output` or `nondirectional`,
  which gives a module boundary for composing designs.
- **Constraints.** `Constraint` relates two Features by a restriction from the SBOL ontology:
  topology (`contains`, `isDisjointFrom`), sequential (`precedes`), orientation, and identity
  (`verifyIdentical`, `differentFrom`, `replaces`).
- **Interactions.** `Interaction` and `Participation`, typed by SBO: inhibition, stimulation,
  binding, conversion and so on, with participant roles.
- **Design / build / test separation.** `Implementation` is a physical realisation, linked to
  the design by `built`. `ExperimentalData` aggregates data files, and `Experiment` groups
  ExperimentalData. This is the **design ↔ physical sample** link that iGEM lacked.
- **Variants.** `CombinatorialDerivation` defines a library from a template with variable
  features.
- **Measures.** `Measure` gives a numeric value and a unit from the **Ontology of units of
  Measure (OM)**, optionally with an SBO type, attached to Features, Interactions and
  Participations [M]. In 3.1.0 they are also usable in CombinatorialDerivation [V].
- **Provenance.** SBOL 3 adopts **PROV-O** directly: `prov:Activity`, `prov:Usage`,
  `prov:Association`, `prov:Plan` and `prov:Agent`, with `prov:wasDerivedFrom` and
  `prov:wasGeneratedBy` on any object, and SBOL-specific roles for design, build, test and learn
  activities.
- **`Attachment`** points to an external file with a `source` IRI, format, size and **hash**,
  with a declared hash algorithm. Structures, raw data and CAD files can therefore be content-
  pinned from an SBOL document.
- **Identity.** Objects are identified by IRI under a namespace, with a `displayId`. SBOL 2's
  `version` and `persistentIdentity` properties were **dropped** in SBOL 3 [M; secondary
  evidence: a Rust implementation's documentation says SBOL 3 does not version IRIs, while SBOL
  2 identities carried a version segment [V]]. Versioning is left to the repository and the IRI
  convention. That is consistent with our design, but it means **SBOL gives us no revision
  model**. We supply it.

### 5.3 What SBOL 3 does not model, or models thinly

| Gap | Why it matters to us | SBOL 3 position |
|---|---|---|
| **Quantitative performance envelopes**: dose–response curves, operating ranges, distributions, uncertainty, measurement conditions | An actuator's spec *is* its envelope: force versus pH, temperature and ligand concentration | A `Measure` is a single value with a unit. There is no first-class uncertainty, condition set or curve. Data lives in `ExperimentalData` attachments, which are opaque to queries. |
| **Mechanical properties**: stiffness, stroke, stall force, persistence length, rupture force, step size, duty ratio | Central to actuators, scaffolds and mechanisms | Not modelled |
| **3D structure** | A designed protein *is* its fold. Interfaces are geometric. | Not modelled. Point to mmCIF or ModelCIF via `Attachment` or `Model`. |
| **Assembly process**: protocol, conditions, yields, QC gates | "The rigs that build and test them" | `Implementation` records *that* something was built. *How* goes to PROV activities plus an external protocol. There is no protocol model. |
| **Kinetic or physical models** | Mechanisms need dynamics | `Model` points to an external model (SBML, CellML) with a language and framework. That is reasonable, but it is a pointer, not a model. |
| **Non-molecular artifacts** (rigs, instruments, fixtures) | Part of the library | Out of scope for SBOL |
| **Revision semantics** | §2 | Out of scope, by design |
| **IP / confidentiality status** | §3 | Out of scope |

### 5.4 Where we would extend it

SBOL 3 permits annotating any object with properties from other namespaces, and permits
extension classes that subclass SBOL's classes [M]. **[Rec]**:

1. **Use SBOL 3 as the composition layer** for all molecular artifacts: chains, complexes,
   assemblies, interfaces and constraints. Do not invent a parallel composition model.
2. **Model performance envelopes with W3C SOSA/SSN** (Semantic Sensor Network Ontology, W3C
   Recommendation 2017 [M]):
   - an `sosa:Observation` has a `hasFeatureOfInterest` (our Component or Implementation), an
     `observedProperty`, a `hasResult` (value plus unit via OM or QUDT) and a
     `usedProcedure` (the assay);
   - conditions are attached as further properties;
   - an envelope is a set of observations plus a declared operating region.

   This keeps the measurement model standard rather than ours.
3. **Mechanical property vocabulary.** Add a small namespace of our own (`dfx:stallForce`,
   `dfx:stroke`, `dfx:stiffness`, …), each defined as a subclass of an OM or QUDT quantity kind,
   so units are checkable. *This is our extension and must be documented as such.*
4. **Structure via `Attachment`, carrying the sha256** of the ModelCIF or mmCIF file. Never
   embed coordinates in SBOL.
5. **Assembly process via PROV activities** whose `prov:hadPlan` is a content-pinned protocol
   (a protocols.io DOI or a versioned file in the store), with the `Implementation` as the
   generated entity.
6. **Rigs:** outside SBOL. A plain record in our store with a content-pinned design package (CAD,
   bill of materials, firmware), linked by PROV `used` from the activities they perform. Open
   hardware manifest formats exist, but we did not evaluate them for this report.

---

## 6. Provenance for a design pipeline

### 6.1 The mapping

| Pipeline thing | PROV-O | Identity |
|---|---|---|
| A generated sequence or structure | `prov:Entity` | iteration digest; `ga4gh:SQ.` for each chain |
| A design run, a structure prediction, a filter, an assay | `prov:Activity` | an assigned run id (UUIDv7) **plus** an *input address*: the sha256 of the canonical run spec |
| The model | `prov:SoftwareAgent` *and* a `prov:Entity` (its weights) | name + **sha256 of each weights file**. A hub revision such as a Hugging Face git commit is acceptable as a *pointer*, not as the identity [M]. |
| Code | `prov:Entity` | git commit + SWHID if archived |
| Container or environment | `prov:Entity` | OCI digest (`image@sha256:…`), **never a tag** |
| Configuration and parameters | `prov:Plan` via `qualifiedAssociation` | sha256 of the canonical config |
| Random seed(s) | a property of the Activity, inside the run spec | literal values, **all of them**: framework, NumPy, CUDA, sampler |
| Hardware and determinism flags | Activity properties | GPU model, driver, CUDA/cuDNN versions, deterministic-algorithm flags |
| The human who chose target and constraints | `prov:Person` (ORCID) via `wasAssociatedWith` with role `dfx:conceiver` / `dfx:selector` | ORCID |
| Our organisation | `prov:Organization` (ROR), via `actedOnBehalfOf` | ROR |
| Input structures and sequences | `prov:used` with a role (target, template, motif, scaffold) | content digests; external accessions (PDB, UniProt) plus the digest of the bytes actually used |

### 6.2 Example (Turtle, illustrative; all `df:`/`dfx:` terms are ours)

```turtle
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix df:   <https://w3id.org/delphi-frontier/> .   # PROPOSED namespace, not yet registered
@prefix dfx:  <https://w3id.org/delphi-frontier/ns#> .

df:artifact/0193a1c2-7e4b-7c11-9d2e-5b8f0a3e6d21/r3
    prov:specializationOf df:artifact/0193a1c2-7e4b-7c11-9d2e-5b8f0a3e6d21 ;
    prov:wasRevisionOf    df:artifact/0193a1c2-7e4b-7c11-9d2e-5b8f0a3e6d21/r2 ;
    prov:wasGeneratedBy   df:run/0193a1c9-0000-7000-8000-000000000001 ;
    dfx:contentDigest     "sha256:…" .

df:run/0193a1c9-0000-7000-8000-000000000001 a prov:Activity ;
    dfx:inputAddress "sha256:…" ;                       # hash of the canonical run spec
    prov:used df:entity/target-structure ,              # role via qualifiedUsage
              df:entity/model-weights ;
    prov:qualifiedAssociation [
        prov:agent   df:agent/design-model ;
        prov:hadPlan df:entity/run-config ] ;           # sha256-pinned config, includes seeds
    prov:wasAssociatedWith <https://orcid.org/0000-0000-0000-0000> ;  # placeholder ORCID
    prov:startedAtTime "2026-11-04T10:00:00Z" .
```

### 6.3 Reproducible from the record alone: what it takes, and its honest limit

A result is reproducible from the record if the record pins:

1. every input by content digest;
2. the code by commit;
3. the environment by OCI digest;
4. the model by weights digest;
5. the full configuration, including **every** seed;
6. the hardware and determinism settings.

With all six, anyone can re-run the activity and compare the output digest.

The honest limit: **GPU inference and sampling are often not bitwise deterministic**, even with
fixed seeds. Atomic-add reductions, kernel selection and library versions all cause drift [M].

**[Rec]** The record therefore carries:

- (a) the output itself, which is the ground truth, never "re-derive on demand";
- (b) the input address and the output digest, so a re-run that yields a *different* output
  digest from the same input address is a detectable event (the Nix lesson, §2.3);
- (c) a declared **reproduction tolerance**: identical sequence; structure RMSD ≤ x Å;
  metric within y.

"Reproducible" then means re-running and landing within tolerance. It does not mean the same
bytes, except where the pipeline is genuinely deterministic.

**Why this also serves IP.** The same record separates what the model produced from what a
person chose: the target, the constraints, the selection from N candidates and the manual edits.
Under the 2025 USPTO guidance (§3.4), conception by a natural person is the inventorship
question. A `dfx:selector` / `dfx:conceiver` association with a timestamped decision record is
exactly the corroboration that question needs.

---

## 7. Nanopublications

### 7.1 The model

A nanopublication is an RDF dataset of four named graphs [M]:

- **Head**: links the other three.
- **Assertion**: the claim, a small set of triples.
- **Provenance**: how the assertion came to be, usually PROV.
- **Publication info**: who published it and when, the licence, and the **signature**.

Origin: Groth, Gibson & Velterop, "The anatomy of a nanopublication", *Information Services &
Use* 30:51–56 (2010) [M]. Decentralised publishing: Kuhn et al., *PeerJ Comput Sci* 2:e78
(2016) [M].

**Trusty URIs**: Kuhn & Dumontier, ESWC 2014 [M]. The nanopub's URI ends in a hash of its own
normalised content. The `RA` module, a base64url SHA-256 over the normalised RDF, is what the
live registry URIs (`…/np/RA…`) show [V]. The identifier therefore verifies its own content, the
same idea as a CID, but defined over **RDF graphs** rather than bytes, so it survives
re-serialisation.

**Signing**: pubinfo carries the signature algorithm (RSA in observed registry entries), the
**public key**, the signature value, the target, and the signer, typically an ORCID [V]. Keys
are bound to people by separate **introduction** nanopublications [V]. Verifiers check the
trusty hash, strip the signature triple, regenerate the signed content and verify it [V].

**Publishing**: to the **Nanopub Registry**, an HTTP REST network of servers such as
`registry.knowledgepixels.com`, which replicate [V]. Retraction and supersession are expressed
by *new* nanopubs that point to the old one. Nothing is deleted [M].

### 7.2 Strengths for us

- Immutable, self-verifying and signed, with a built-in provenance graph.
- Small, so they can be published and indexed in a decentralised way.
- A good fit for **claims about artifacts**: "artifact X r3 has measured K_d = 12 nM under
  conditions C, by assay A", or "artifact X r3 failed to express in E. coli BL21". Each is a
  citable, attributable, retractable assertion that can be aggregated across labs.

### 7.3 Real limitations for engineering specifications

1. **They are assertions, not specifications.** The model is "agent says that triple holds". A
   spec is a structured document, a sequence plus geometry plus envelope plus process, that is
   *normative* rather than *claimed*. Expressing a full design as nanopub triples is possible
   and awkward.
2. **RDF is a poor carrier for bulk data.** Coordinates, curves and raw instrument data must be
   referenced by hash, so the nanopub becomes a signed pointer, which our store already provides.
3. **Publication is public.** The registry network is a public, replicating system. For
   patent-candidate artifacts that is disqualifying until clearance (§3.3), since a nanopub with
   an enabling assertion is a disclosure.
4. **Key trust is self-asserted** unless anchored, for example by an ORCID-linked introduction.
   The registry's servers are not a timestamp authority of record [M].
5. **Adoption** is concentrated in parts of biomedical and semantic-web research, and small
   outside them [M]. Tooling is thinner than for git, OCI or DataCite.
6. **Schema freedom cuts both ways.** Without agreed templates (Nanodash templates exist [M]),
   two labs' assertions about the same property will not join.

**[Rec]** Use nanopubs, later and optionally, as the **public claims layer** for cleared
artifacts. Each published characterisation result becomes a nanopub whose subject is our w3id
revision URI and whose evidence is a content-pinned data file. Do not use nanopubs as the system
of record for specifications.

---

## 8. Recommendation

Every subsection is **[Rec]**. The alternatives surveyed above are the justification.

### 8.1 Identifier format

```
Item         dfa:0193a1c2-7e4b-7c11-9d2e-5b8f0a3e6d21                   UUIDv7, lowercase, hyphenated
Revision     dfa:0193a1c2-7e4b-7c11-9d2e-5b8f0a3e6d21/r3
Exact state  dfa:0193a1c2-7e4b-7c11-9d2e-5b8f0a3e6d21@sha256:<64 hex>   OCI-style pin
Sequence     ga4gh:SQ.<sha512t24u>                                     GA4GH computed id, per chain
File         sha256:<64 hex>
HTTP form    https://w3id.org/delphi-frontier/a/{uuid}[/r{n}]           PROPOSED; must be registered
```

- **UUIDv7 for items**, rather than UUIDv4, ULID, sequential numbers or DOIs:
  - It is an IETF standard (RFC 9562), unlike ULID.
  - It is time-ordered for index locality and federation merges, unlike v4.
  - It is opaque, so no semantics can go stale (iGEM failure 4). Sequential numbers also leak
    volume and need a central allocator, which breaks federation.
  - It can be minted offline and privately, unlike a DOI, which is a public act.
  - PostgreSQL 18 ships a native `uuidv7()` function [M, verify against the deployed version].
- **The `dfa:` CURIE prefix** for compact display.
  **Proposal:** register it in the Bioregistry once public, and register
  `w3id.org/delphi-frontier` by pull request **before** any URI is published. Until then, the
  URI form must not appear in any public document. **The namespace does not exist yet.**
- **No ARK or Handle server**, because we should not be a persistence operator. **No PURL**,
  because w3id.org is the maintained successor for this niche.
- **DOIs only at publication**, via Zenodo concept and version DOIs, which map onto item and
  revision (§2.6). The DOI is recorded *on* the revision as an alternate identifier. It never
  replaces ours.

### 8.2 What is content-addressed

| Thing | Digest | Why this one |
|---|---|---|
| Each artifact iteration (the record) | the store's existing `version` = sha256 of the canonical record (SPEC-001) | It already exists, is tested, and is recomputed on import (SPEC-004). Keep it. |
| Each file (structures, data, CAD, protocols) | `sha256:` of the **on-disk bytes** | CONTRIBUTING-VERIFICATION §2: "hash the file, not the string". Universally verifiable. |
| Each polymer sequence | `ga4gh:SQ.` (truncated SHA-512, base64url) [V] | A standard from a standards body, with refget infrastructure. Gives **library-wide deduplication** and "has this exact chain been made before?" lookups. Encoding is unambiguous for sequences. |
| Complexes and assemblies | the iteration digest of the composite record, which **pins its parts' iteration digests** | A Merkle DAG: the composite's id changes if and only if a part, the stoichiometry or a constraint changes |
| Runs | input address = sha256 of the canonical run spec | The Nix lesson (§2.3); detects non-determinism |
| Models, containers, code | weights sha256, OCI digest, git commit (+ SWHID) | Mutable names (hub model ids, image tags, branches) are not identities |

**Not chosen as the primary content id:**

- **IPFS CIDs**: there is no persistence without pinning, and multihash agility is solvable more
  simply.
- **git object ids**: SHA-1 by default, path-bound, repository-bound.
- **SWHID**: right for code, but still SHA-1 and software-scoped.

Interoperating with all of these is fine. Use them as *alternate* identifiers.

**Canonicalisation caveat (a finding about this repository).** `frontier/models.py:23` defines
`canonical()` as `json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False,
allow_nan=False)`. That is **not** RFC 8785 JSON Canonicalization Scheme [M]. Python sorts keys
by code point, while JCS sorts by UTF-16 code units, which differs for non-BMP characters. Number
serialisation also differs at edge cases. A non-Python implementation will therefore not
reproduce the digests unless it copies Python's behaviour exactly.

Changing the function would change every existing digest. **Proposal:**

- (a) freeze it under a name, `frontier-canonical-v1`, with a precise specification and
  cross-language test vectors;
- (b) forbid floats in hashed artifact content: store measured quantities as **decimal strings
  with units**;
- (c) prefix algorithm names on new artifact digests (`sha256:`), as OCI and multihash do, so the
  next algorithm can be added without ambiguity.

### 8.3 How revisions are expressed

- **Iteration**: every save is a store version, chained by `predecessor` (already in
  `schema.sql`).
- **Revision**: a *release event* binds label `r{n}` to one iteration digest, **once**. The
  binding is a content-addressed Event record. Re-binding a label is rejected by the store.
  Labels are monotonic integers, not letters (unbounded, sortable) and not semver (semver's
  API-compatibility semantics do not map onto molecules).
- **New revision vs new item**: the PLM **form-fit-function** rule (§2.5).
  - Same role, same interfaces and same partners: new revision, `prov:wasRevisionOf`.
  - Interface, stoichiometry or partner change: new item, `prov:wasDerivedFrom`.
- **Every revision states `change_class`**, one or more of `sequence`, `structure`, `assembly`,
  `characterisation`, `metadata`, `process`, with a one-line rationale.
- **Patents and claims never cite a bare item.** IP dockets, assessments and publications cite
  `item@sha256:…` or the `SQ.` ids, because a composition of matter is a content, not a lineage.
- **"Latest"** is a resolver convenience (like Zenodo's concept DOI), never a stored reference.

### 8.4 How assemblies and complexes compose

The composite record uses SBOL 3's model (Component → SubComponents with Interfaces and
Constraints), serialised in our record with each SubComponent carrying
`{item, revision, iteration digest}`. Stoichiometry and constraints are inside the hashed record.
Export to SBOL 3 for interchange.

### 8.5 Mandatory metadata (proposed minimum information for a designed artifact)

*This is our proposal, not an existing standard.* Mapping targets are given for each field.

| Field | Required | Maps to |
|---|---|---|
| `item_id` (UUIDv7), `revision`, `iteration` digest | yes | DataCite Identifier / alternateIdentifier; PROV entity |
| `artifact_class` | yes | controlled list: protein, complex, assembly, actuator, scaffold, mechanism, rig, protocol. Plus SBO type for molecular classes. |
| `title`, `description`, `design_intent` (the function it is meant to have, in a sentence) | yes | DC/DataCite Title, Description |
| `creators` (ORCID) with **contribution roles**, incl. `conceiver` and `selector` | yes | DataCite Creator + nameIdentifier; CRediT roles [M]; PROV associations |
| `organisation` (ROR) | yes | DataCite affiliationIdentifier |
| `created_at` (self-asserted) **and** `anchor` (batch id + inclusion proof + TSA/Rekor references) | yes | DataCite Date (Created); §8.6 |
| `sequences[]`: chain id, molecule type, sequence, `ga4gh:SQ.` digest | yes for molecular classes | SBOL Sequence; refget |
| `files[]`: role, media type, **sha256**, size | yes | RO-Crate File; SBOL Attachment |
| `composition`: subcomponents pinned by iteration digest, stoichiometry, interfaces, constraints | yes for complex, assembly, mechanism | SBOL Component / SubComponent / Interface / Constraint |
| `provenance`: generating activity with input address, model weights digest, code commit, OCI digest, config digest, **all seeds**, hardware and determinism flags, inputs by digest | yes | PROV-O (§6) |
| `reproduction_tolerance` | yes if computationally generated | ours |
| `status`: `designed` → `predicted` → `built` → `expressed` → `characterised` → `validated` (or `failed`), with evidence refs at each step | yes | ours; SBOL Implementation / ExperimentalData for built and tested |
| `physical_samples[]`: sample id, location, **sequence-verification record** (digest of the sequencing read or report) | yes once `built` | SBOL Implementation; fixes iGEM failure 2 |
| `performance[]`: observed property, value as a decimal string, unit (OM/QUDT IRI), uncertainty, conditions, procedure (pinned protocol), observation id | yes once `characterised` | SOSA/SSN Observation (§5.4) |
| `change_class`, `change_rationale` | yes for r ≥ 2 | ours |
| `relations[]`: typed links (`wasRevisionOf`, `wasDerivedFrom`, `hasPart`, `isPartOf`, `variantOf`, `isDocumentedBy`) | as applicable | PROV-O; DataCite relationType |
| `ip_status`: `unreviewed`, `candidate-confidential`, `filed` (with a docket reference held privately), `cleared-public`, `defensively-published` (with DOI) | **yes, default `unreviewed` = confidential** | ours. Gates any public export. |
| `biosafety_screening`: status, method/version, date | yes for sequences intended for synthesis | ours; for synthesis-provider screening |
| `license` | yes (may be "none: confidential") | DataCite Rights |

### 8.6 How a timestamp is anchored

1. **Every iteration** gets a commitment, `c = sha256(salt ‖ iteration_digest)`, with a fresh
   256-bit salt stored privately beside the record (§3.3).
2. **Daily**, or more often for urgent records, build a Merkle tree over the day's commitments
   using RFC 9162 leaf and node hashing.
3. **Anchor the root**:
   - with **RFC 3161 tokens from two independent TSAs**, one of them eIDAS-qualified if EU
     evidentiary weight is wanted;
   - by signing it and logging it to **Sigstore Rekor** (v2) under an organisational workload
     identity;
   - optionally, with **OpenTimestamps**, as a trustless extra witness.
4. **Store per record**: the salt, the leaf index, the inclusion proof, the root, and every
   anchor receipt. Verification is then fully offline except for checking the anchors.
5. **On release of a revision**, anchor the release Event the same way, so the label binding
   (§8.3) has its own existence proof.
6. **At clearance**, a revision may be published: a Zenodo deposit (DOI), a TDC defensive
   publication, a nanopub of its characterisation claims, or none. Which one is a decision for
   counsel and the owner, not for the pipeline. The pipeline enforces that **nothing with
   `ip_status ∈ {unreviewed, candidate-confidential}` leaves the private store except salted
   commitments.**

**Why this mix:**

- RFC 3161 has the clearest legal footing, with a statutory presumption in the EU.
- Rekor gives public, append-only, independently monitored evidence at no cost.
- OpenTimestamps removes the trusted party entirely.
- Batching makes the per-record cost zero at any library size.
- Salting prevents the near-neighbour brute-force disclosure.

None of it is presented as patent priority, which comes only from filing (§3.3–3.4).

### 8.7 Serialisations

| Use | Format |
|---|---|
| System of record | store records (SPEC-001), JSON, digest-pinned |
| Composition interchange | SBOL 3 (RDF) |
| Bundle export | RO-Crate (1.2+), carrying the SBOL document, files with sha256, and PROV |
| Publication | DataCite 4.6 via Zenodo; schema.org/Bioschemas JSON-LD on landing pages |
| ML datasets | Croissant 1.1 |
| Predicted structures | ModelCIF |
| Public claims (optional, later) | nanopublications |

---

## 9. Consequences for this repository and open questions

These are follow-ups. None are done in this change.

1. SPEC-001's `Kind` is a closed set of seven. An `Artifact` kind, and a `Release` event type
   binding `r{n}` to a digest, need a spec revision and a schema change.
2. `Identifier` (`^[A-Za-z0-9][A-Za-z0-9_.:/-]*$`, max 160) already admits UUIDs and `dfa:`
   CURIEs. The `@sha256:` pin form needs `@`, which it does not admit, so use a separate field or
   extend the pattern.
3. Freeze `canonical()` as `frontier-canonical-v1` with cross-language test vectors before any
   other implementation computes digests (§8.2).
4. **Check whether this repository is public before any artifact content is committed to it.**
   A push of an enabling description is a disclosure (§3.3).
5. Register `w3id.org/delphi-frontier` and decide the CURIE prefix before any URI appears in
   public.
6. Legal review of the `ip_status` gate, the defensive-publication policy and the provisional
   strategy, by a registered practitioner.
7. Open: should identical `SQ.` digests across two items be **blocked**, **warned** or allowed?
   The proposal is to warn and to require an explicit `variantOf` / `duplicateOf` relation.
   Duplicate sequences are an internal prior-art signal.
8. Open: the tolerance policy for "reproduced" when pipelines are non-deterministic (§6.3).

---

## 10. Sources

**Checked during this research [V]:**

- SBOL 3.1.0: Buecherl et al., *J Integr Bioinform* 2023, doi:10.1515/jib-2022-0058,
  [PMC10063177](https://pmc.ncbi.nlm.nih.gov/articles/PMC10063177/) (abstract and changelog only;
  `sbolstandard.org` unreachable from the sandbox)
- SBOL 3 does not version IRIs (secondary): [`sbol` Rust crate source](https://docs.rs/crate/sbol/latest/source/src/upgrade/identity.rs)
- DataCite 4.6 release date: [schema.datacite.org/versions.html](https://schema.datacite.org/versions.html)
- SWHID ISO/IEC 18670: [OpenChain announcement](https://openchainproject.org/news/2025/04/29/from-heritage-to-hash-swhid-becomes-a-global-iso-iec-standard), [swhid.org FAQ](https://swhid.org/faq/)
- Rekor v2 GA: [blog.sigstore.dev/rekor-v2-ga](https://blog.sigstore.dev/rekor-v2-ga/)
- RO-Crate 1.2: [researchobject.org/ro-crate/specification/1.2](https://www.researchobject.org/ro-crate/specification/1.2), [release announcement](https://esciencelab.org.uk/ro-crate/announcements/2025/06/04/ro-crate-1.2-released/)
- Croissant 1.1: [docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html](https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html), [MLCommons announcement](https://mlcommons.org/2026/02/croissant-1-1-standard/)
- GA4GH computed identifiers / `SQ.` / sha512t24u: [VRS computed identifiers](https://vrs.ga4gh.org/en/latest/conventions/computed_identifiers.html)
- ARK draft-kunze-ark-42: [ietf.org/archive/id/draft-kunze-ark-42.html](https://www.ietf.org/archive/id/draft-kunze-ark-42.html)
- Handle prefix fees (dated): [handle.net/prefix.html](https://handle.net/prefix.html), [ICANN 58 DONA slides](https://archive.icann.org/meetings/icann58/schd.ws/hosted_files/icann58copenhagen2017/86/Durand%20DOA-ICANN-58.pdf)
- Crossref fees: [crossref.org/fees](https://crossref.org/fees), [2027 fee update](https://www.crossref.org/blog/fee-update-lowering-and-removing-doi-registration-fees-in-january-2027/)
- Git SHA-256 / Git 3.0 plan: [Phoronix, Git 2.46-rc0](https://www.phoronix.com/news/Git-2.46-rc0-Released)
- Nanopub signature and registry structure: [registry.knowledgepixels.com example](https://registry.knowledgepixels.com/np/RAFU2fblXSZuhtC7CwHgIZAL-nG3yfnYH-yxwmX9AjeSs), [`nanopub` Rust crate](https://docs.rs/crate/nanopub/latest/source/src/nanopub.rs)
- iGEM Registry: [Wikipedia](https://en.wikipedia.org/wiki/Registry_of_Standard_Biological_Parts), [Add a Part (RFC 10)](https://parts.igem.org/Add_a_Part_to_the_Registry), [Twist/iGEM](https://www.biospace.com/twist-bioscience-and-igem-partner-to-provide-synthetic-dna-for-igem-competition-and-registry)
- USPTO provisional fees (secondary): [Finnegan](https://www.finnegan.com/en/insights/ip-updates/uspto-patent-fees-changes-for-2025.html), [Barnes & Thornburg](https://btlaw.com/en/insights/alerts/2025/important-update-uspto-fee-changes-effective-january-2025)
- USPTO sequence listings and provisionals: [sequence listing basics](https://www.uspto.gov/patents/apply/sequence-listing-resource-center/sequence-listing-basics), [FAQs](https://www.uspto.gov/patents/apply/sequence-listing-resource-center/sequence-listing-faqs)
- *Dynamic Drinkware v. National Graphics*: [Justia, No. 15-1214](https://law.justia.com/cases/federal/appellate-courts/cafc/15-1214/15-1214-2015-09-04.html); post-AIA treatment (secondary): [Akin Gump](https://www.akingump.com/en/insights/blogs/ip-newsflash/ptab-dynamic-drinkware-written-description-requirement-inapplicable-to-post-aia-patents)
- USPTO 2025 AI-assisted inventorship guidance (secondary): [Jones Day](https://www.jonesday.com/en/insights/2025/12/uspto-revises-guidance-on-aiassisted-inventorship)
- Defensive publication venues (secondary): [IPWatchdog](https://ipwatchdog.com/2020/05/25/defensive-publications-cost-effective-tool-supplement-patent-strategy/), [ip.com](https://ip.com/defensive-publishing/)

**Cited from prior knowledge, not re-checked [M]:** RFC 9562, RFC 4122, RFC 3161, RFC 5816,
RFC 4998, RFC 6962, RFC 9162, RFC 8785, RFC 3650–3652; ISO 26324; ISO 15836-1; ULID spec;
multiformats CID; Nix manual (store paths, ca-derivations); OCI Image Spec v1.1; git object model;
ORCID and ROR checksum formats; W3C PROV-O (2013); W3C SOSA/SSN (2017); FAIR (Wilkinson 2016);
MIAME, MIAPE, MIBBI; ModelCIF; SBOL 3.0 class model; nanopub papers (Groth 2010, Kuhn 2014,
Kuhn 2016); eIDAS Art. 41; EPC Arts. 54–55; 35 U.S.C. §§100, 102, 111(b), 112(a), 119(e), 135,
273; *Thaler v. Vidal*; *Price v. Symsek*; *AMP v. Myriad*; *Amgen v. Sanofi*; Vilanova &
Porcar 2014; Zenodo concept DOIs; PostgreSQL 18 `uuidv7()`.
