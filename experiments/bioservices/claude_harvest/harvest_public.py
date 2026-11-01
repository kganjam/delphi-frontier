"""Step 2a: bounded public-service calls on flying-fish fin/scale/wing genes.

Zebrafish is the annotated proxy; nothing here is measured in Exocoetidae
unless a response says so. Responses are saved verbatim by ``calls.call``.
"""
import json, sys, urllib.parse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from calls import call

GENES = ["tbx5a", "fgf10a", "shha", "hoxd13a", "hoxa13a", "and1", "eda", "edar", "kcnh2a", "kcnk5b", "msxb", "lef1", "pitx1", "tbx4", "sp8a", "fgf24"]
q = urllib.parse.quote
for g in GENES:
    call("uniprot", f"search:{g}", f"https://rest.uniprot.org/uniprotkb/search?query={q(f'gene_exact:{g} AND organism_id:7955')}&format=json&size=3&fields=accession,id,gene_names,protein_name,length,cc_function,ft_domain,xref_zfin,sequence",
         save=f"uniprot/{g}.json", note="zebrafish (taxon 7955) annotation; curated text is source_statement, not observation in Exocoetidae")
    call("ensembl", f"lookup:{g}", f"https://rest.ensembl.org/lookup/symbol/danio_rerio/{g}?content-type=application/json;expand=0",
         save=f"ensembl/lookup_{g}.json", note="GRCz11 coordinates")
for g in ["tbx5a", "fgf10a", "shha", "hoxd13a", "pitx1"]:
    call("ensembl", f"homology:{g}", f"https://rest.ensembl.org/homology/symbol/danio_rerio/{g}?content-type=application/json;type=orthologues;sequence=none",
         save=f"ensembl/homology_{g}.json", note="Ensembl Compara orthologues (computed); includes fish species available in Ensembl")
call("ensembl", "species-list", "https://rest.ensembl.org/info/species?content-type=application/json", save="ensembl/species.json")
call("ncbi-datasets", "taxon:Exocoetidae", "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/Exocoetidae/dataset_report?page_size=20", save="ncbi/exocoetidae_genomes.json", note="assembly listing only")
call("ncbi-datasets", "taxon:Cheilopogon", "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/Cheilopogon/dataset_report?page_size=20", save="ncbi/cheilopogon_genomes.json")
call("ncbi-datasets", "taxon:Beloniformes", "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/Beloniformes/dataset_report?page_size=50", save="ncbi/beloniformes_genomes.json")
EP = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resultType=core&pageSize=8&query="
queries = {
 "flyingfish_pectoral": '(Exocoetidae OR "flying fish" OR flyingfish) AND (pectoral OR fin OR wing OR gliding)',
 "flyingfish_genome": '(Exocoetidae OR "flying fish" OR Cheilopogon OR Exocoetus) AND (genome OR transcriptome OR gene)',
 "fin_to_limb_hox": 'zebrafish AND (hoxd13 OR hoxa13) AND (fin OR enhancer) AND (autopod OR "fin fold" OR actinotrichia)',
 "pelvic_pitx1_enhancer": '(pitx1 AND pelvic AND enhancer AND (fish OR stickleback OR zebrafish))',
 "pectoral_tbx5a_fgf10": 'zebrafish AND tbx5a AND (fin bud OR pectoral fin) AND (fgf10 OR enhancer OR regulatory)',
 "scale_eda_edar": 'zebrafish AND (eda OR edar) AND scale AND development',
 "fin_size_kcnk5b": 'zebrafish AND (kcnk5b OR kcnh2a) AND fin AND (size OR growth OR bioelectric)',
 "fin_ray_and1": 'zebrafish AND (actinodin OR and1 OR and2) AND fin',
 "fin_regen_shh_lef1": 'zebrafish AND fin AND (lef1 OR shh) AND (regeneration OR ray branching)',
 "fin_mechanics": '(fish fin ray) AND (stiffness OR flexural OR hemitrich) AND (bending OR mechanics)',
}
for k, v in queries.items():
    call("europepmc", f"search:{k}", EP + q(v), save=f"europepmc/{k}.json", note="query verbatim in request_url; hits are leads until checked")
for k, v in {"flyingfish": "(Exocoetidae OR flyingfish OR flying fish) AND (fin OR gliding OR genome)", "pitx1_pelvic": "pitx1 AND pelvic fin AND enhancer", "hox_fin": "hoxd13a AND zebrafish AND fin"}.items():
    call("ncbi-eutils", f"pubmed-esearch:{k}", f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={q(v)}&retmax=20&retmode=json", save=f"pubmed/{k}.json")
