# Challenge 258 — Boltz2 batch MSA nesting depth

**Claim under review (author's, not mine):** "The Boltz2 batch nesting is four levels deep and not
discoverable from the top-level schema: polymers[] -> msa -> msa_search -> a3m -> {alignment, format}"
Recorded evidence level: *measured*. Value: 4 nesting levels. Source: "workbench `$defs`: Polymer, MSA,
MSASearch, A3M".

**Verdict: WEAKENED.** The shape is right in kind (deeply nested, map-of-maps), but the count of four
depends on an unstated counting convention, two of the path segments are probably map keys rather than
field names, the leaf record is probably incomplete, and "measured" overstates a schema reading.

## Sources and read-levels

| Source | Read-level | Notes |
|---|---|---|
| "workbench `$defs`: Polymer, MSA, MSASearch, A3M" (the author's source) | could-not-access | Not in this repo. `grep -ri "msa_search\|MSASearch\|workbench\|a3m"` across the whole repo (excluding `.git`) finds nothing. I could not check the `$defs` names or their contents. |
| NVIDIA Boltz-2 NIM docs, `docs.nvidia.com/nim/bionemo/boltz2/{latest,1.8.0,1.9.0}/inference`, `.../1.0.0/api-reference.md` | search-summary | One web search (standard mode). Fetches of both pages failed with DNS `ENOTFOUND`, because `docs.nvidia.com` is outside this session's network allow-list. Everything below that comes from NVIDIA comes from the search engine's summary only. It is not verbatim schema text. |
| `findings/README-no-gpu-problem.md` | full-text | Mentions Boltz only in passing (BoltzGen). It has no schema content. |

## 1. Independent recount

The arithmetic is mine. I did not copy the author's working. Path as stated:
`request -> polymers -> [i] -> msa -> msa_search -> a3m -> alignment`.

| Counting convention | Count |
|---|---|
| Key hops from a single Polymer object down to the leaf field (`msa`, `msa_search`, `a3m`, `alignment`) | **4** |
| Containers between the Polymer and the leaf strings (`msa` obj, `msa_search` obj, `a3m` obj) | 3 |
| Object/array levels below the request root (`polymers` array, polymer obj, `msa`, `msa_search`, `a3m`) | 5 |
| Path segments from root to leaf, counting the array index | 6 |

The number "4" is reproducible only under the first convention, and the claim does not state it. Its own
arrow chain has 5 arrows starting from `polymers[]`. So the claim's text is not consistent with its own
value unless the reader guesses which convention it uses. **Calculated, not observed.**

## 2. Proxy check

"Nesting depth" stands in for the thing that actually matters, which is whether a client can construct a
valid MSA payload from the schema alone. Depth is a weak proxy for that. The stronger question is whether
the segments are **fixed field names or free-form map keys**:

- According to the NIM docs **(search-summary, not verified verbatim)**, `msa` maps *database names* to
  *format keys*. Each format key holds a record. The example given is
  `{"database_1": {"a3m": {"format": "a3m", "alignment": ">1\nMVNIDIAIAMAI", "rank": 0}}}`. The
  summary also says that at most 3 database entries are allowed. The format keys come from
  {csv, fasta, a3m, sto}, are case-sensitive, and only a3m and csv are consumed at inference.
- If the author's "workbench" is this NIM API or a thin wrapper over it, then `msa_search` is a
  **user-chosen database-name key** (it could be `uniref90`, `database_1`, and so on), not a literal
  field. Likewise, `a3m` is one of four allowed **format keys**, and it repeats as the value of `format`.
  Writing the path as `msa -> msa_search -> a3m` reads as fixed field names, which would mislead a client
  author.
- That inference supports the "not discoverable" half of the claim more strongly than the author's own
  wording does, because a free-form key cannot be discovered by reading property names at all. But it
  contradicts the path as written.

## 3. Hidden assumption, relaxed

The phrase "not discoverable from the top-level schema" assumes the reader inspects only the top-level
`properties`. But the author cites `$defs`. Any JSON-Schema `$ref` resolver can walk
`Polymer -> MSA -> MSASearch -> A3M` mechanically. Relax the assumption to "a client that resolves `$ref`"
and the structure *is* discoverable. Only the *meaning* of the free-form keys (if they are free-form)
stays undiscoverable. The claim needs that scope: "not visible without resolving `$ref`s".

## 4. Evidence level

Counting keys in a schema document is a **reading of a specification, which is then counted (derived)**.
It is not a measurement of system behaviour. Nothing in the recorded evidence shows that a request
built to this path was submitted and accepted. A label of "observed (schema read), count derived" would
be honest. **"Measured" overstates it. That is a defect even if the number is right.**

## 5. Counter-examples the author may have missed

- **Leaf record is likely incomplete.** The NIM docs summary lists an optional `rank` field (default −1)
  alongside `alignment` and `format`. The leaf `{alignment, format}` omits it **(search-summary)**.
- **Format alternatives.** `a3m` is not the only branch. `csv` is also consumed, and `fasta`/`sto` are
  accepted by the schema but dropped **(search-summary)**.
- **Version drift.** The summary reports that the NIM doc versions (1.0.0 → 1.10.0) differ. A depth
  claim with no version attached is unpinned.
- **Upstream Boltz-2 YAML input** (not the NIM) attaches an MSA as a file path on a sequence entry, with
  far shallower nesting. I state this from prior knowledge. I did not fetch it in this session, so its
  read-level is not established. It shows that "Boltz2 nesting" depends on which interface is meant, and
  the claim does not say.

## What would settle it

1. Read the author's workbench `$defs` verbatim and check whether `MSA` declares `additionalProperties:
   {$ref: MSASearch}` (map) or `properties: {msa_search: ...}` (field). Do the same for `MSASearch -> A3M`.
2. Allow `docs.nvidia.com` and read the NIM OpenAPI spec for the same check.
3. POST one request with database key `foo` instead of `msa_search` and record whether it is accepted.
   That would be the actual *measurement*.

Until then, here is the corrected statement. It is my inference, not the author's claim: *the MSA payload
sits 4 key-hops below each Polymer (5 container levels below the request root). It is reachable only
through `$ref` resolution. The intermediate segments are probably free-form database-name and format
keys rather than fixed fields. The leaf likely also carries an optional `rank`. Depth is derived from a
schema read, not measured.*

```swarm-challenge
{"claim_id": 258, "outcome": "weakened", "reason": "The count of 4 holds only for key-hops from a Polymer object (5 levels from the request root by the claim's own arrows), 'msa_search' and 'a3m' are likely free-form database/format map keys rather than fixed fields per NIM docs (search-summary only), the leaf likely omits optional 'rank', the structure is discoverable via $ref resolution, and a schema reading is labelled 'measured'.", "corrected_value": "4 key-hops below Polymer / 5 container levels below request root (derived from schema reading, not measured)", "depends_on": ["NVIDIA Boltz-2 NIM docs msa structure as given by web search summary (database name -> format key -> {format, alignment, rank}); pages not fetched, docs.nvidia.com blocked", "author's workbench $defs (Polymer, MSA, MSASearch, A3M) — could-not-access; not in repo", "assumption that the workbench API is the NIM API or a wrapper over it", "counting convention: key-hops from Polymer object vs levels from request root"]}
```
