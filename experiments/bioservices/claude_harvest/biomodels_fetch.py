import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from calls import call, OUT
IDS = ["BIOMD0000000201", "BIOMD0000000275", "BIOMD0000000395", "BIOMD0000000396", "BIOMD0000000397"]
for i in IDS:
    s, b = call("biomodels", f"metadata:{i}", f"https://www.ebi.ac.uk/biomodels/{i}?format=json", save=f"biomodels/{i}_meta.json")
    m = json.loads(b); main = [f["name"] for f in m["files"]["main"]][0]
    call("biomodels", f"sbml:{i}", f"https://www.ebi.ac.uk/biomodels/model/download/{i}?filename={main}", save=f"biomodels/{i}.xml", note=f"main SBML file {main}")
