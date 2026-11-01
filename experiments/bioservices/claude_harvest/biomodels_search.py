import sys, urllib.parse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from calls import call
for k, v in {"turing": "turing pattern", "shh_gradient": "sonic hedgehog gradient", "fgf_limb": "FGF limb bud", "somite_clock": "segmentation clock zebrafish", "wnt_fin": "Wnt signaling", "notch_lateral": "delta notch lateral inhibition", "bmp_gradient": "BMP gradient dorsoventral", "bioelectric": "membrane potential potassium channel"}.items():
    call("biomodels", f"search:{k}", f"https://www.ebi.ac.uk/biomodels/search?query={urllib.parse.quote(v)}&format=json&numResults=8", save=f"biomodels/search2_{k}.json", note="retry after 8 HTTP-400 with a filter clause; plain query")
