import sys, urllib.parse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from calls import call
for k, v in {"hedgehog": "hedgehog", "fgf": "FGF", "hes1": "Hes1 oscillation", "segmentation": "somite segmentation clock", "morphogen": "morphogen gradient", "bmp": "BMP", "notch": "Notch", "delta_notch": "Delta-Notch", "limb": "limb development"}.items():
    call("biomodels", f"search:{k}", f"https://www.ebi.ac.uk/biomodels/search?query={urllib.parse.quote(v)}&format=json&numResults=8", save=f"biomodels/search3_{k}.json", note="plain short query")
