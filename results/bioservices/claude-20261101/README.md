# Claude bioservices harvest, 2026-11-01

Every row of `call_ledger.jsonl` is one recorded call (service, verbatim request URL, HTTP status or exit, UTC time, bytes, SHA-256, saved path). Bodies are saved verbatim; credentials never written. Code: `experiments/bioservices/claude_harvest/`.

## Service probes
UniProt, NCBI E-utilities, Europe PMC, Ensembl, BioModels, ZFIN downloads host, Gemini (`gemini-3.1-pro-preview`), Nebius Scientific AI MCP `initialize`: HTTP 200. gcloud project `scienceclaw26bos-3016` ACTIVE. NVIDIA Brev: no CLI, no credential (exit 1; coordinator confirms not logged in). Evo2: needs a GPU, not run.

## Source facts retrieved (source_statement / computed, not observations in Exocoetidae)
- NCBI Datasets lists **one** Exocoetidae assembly: *Hirundichthys speculiger* `GCA_018398805.1` (listing only; contents and annotation quality not read). No Cheilopogon assembly. Beloniformes: 75 assemblies (medaka, Hemiramphidae). Ensembl has no Exocoetidae; Oryzias (medaka) is the closest Beloniformes in Ensembl species list. Use medaka as proxy, labelled as such.
- GRCz11 gene coordinates (Ensembl lookup): tbx5a chr5:72264192-72289648(-), fgf10a chr21:19635486-19683168, shha chr7:40884012-40893295, hoxd13a chr9:1986816-1990323(-), hoxa13a chr19:19729506-19731291, pitx1 chr21:45816030-45824439, kcnk5b chr20:9223514-9239037, and1 chr24:26277390-26283359(-). `msxb` lookup failed (HTTP 400, symbol not resolved; not retried with guesses).
- Literature leads: Europe PMC counts per query are in each response file (hitCount); PubMed counts for flying-fish query 47. Hits are leads until read.

## Computed (predicted) structures: OpenFold2 on Nebius (dummy MSA, monomer, no template)
Fgf10a Q8AY90 (201 aa) mean pLDDT 48.8; Hoxd13a Q90472 (256) 42.5; Shha Q92008 (418, full precursor) 41.2; Kcnk5b Q6PFU3 (448) 56.1. All low confidence; TFs and signalling precursors are largely disordered or need partners. Structure hypotheses only: no function, enhancer or phenotype is inferred. Provider-reported `upstream-source-not-nim`: not BioNeMo use. Receipts under `openfold2/` (result artifact SHA-256 verified, signed URL not stored).

## Simulated: BioModels via libRoadRunner 2.11.0, CPU, curated defaults
BIOMD0000000201 (Goldbeter2008 somite clock Notch/Wnt/FGF): 16 varying species, no late oscillation at t_end=200 in default settings. BIOMD0000000275 (Goldbeter2007 somitogenesis switch): oscillates, peak period about 14.6 model time units (units not checked). BIOMD0000000395 Hedgehog / 396 Notch (Sivakumar2011): species oscillate (period about 6.7 time units, unchecked units); 397 Wnt: no late oscillation. Peak detection is crude. These are published-model simulations, not fits to fish data, and not reviewed. See `biomodels/simulation_receipts.json`.

## Model analysis: Gemini `gemini-3.8-flash`, 1 call, 40 Europe PMC abstracts
`gemini/leads_response.json`; inputs in `gemini/leads_input_ids.json`. Extraction leads only, restricted to supplied abstracts; each must be checked against its source before use. First items: actinodin1/2 knockouts in zebrafish alter actinotrichia and fin shape (EPMC 42741580, 41885168).

## Not done
GCP CPU batch: no existing packet found for me to run, so nothing was launched there; artifacts are in git and mirrored to /data/artifacts. Failed calls kept in ledger: 8 BioModels searches with a bad filter clause (HTTP 400), one Ensembl lookup (msxb), Brev.
