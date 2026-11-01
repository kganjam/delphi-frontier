"""One grounded Gemini call: extract sourced claim/equation/design-input LEADS from fetched abstracts only."""
import glob, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from calls import call, load_secret, OUT
docs = []
for f in sorted(glob.glob(str(OUT / "europepmc/*.json"))):
    for r in json.load(open(f))["resultList"]["result"][:5]:
        a = (r.get("abstractText") or "")[:1400]
        if a and r.get("id") not in [d[0] for d in docs]:
            docs.append((r.get("id"), r.get("pmid"), r.get("title"), a))
docs = docs[:40]
text = "\n\n".join(f"[EPMC:{i} PMID:{p}] {t}\n{a}" for i, p, t, a in docs)
sysmsg = ("Use ONLY the supplied abstracts. For each lead give: statement, species/conditions stated, evidence type "
          "(observed/predicted/review), the [EPMC id] it came from, and a quantitative relation or equation ONLY if the abstract states one. "
          "Write 'NOT IN SUPPLIED TEXT' rather than supplying anything from memory. Group by scale: gene-regulation, tissue/fin-ray, whole-fin mechanics, scale/skin. "
          "Flag items relevant to a flying-fish (Exocoetidae) pectoral/pelvic fin-wing design input, and say when only zebrafish or other taxa are stated.")
body = json.dumps({"systemInstruction": {"parts": [{"text": sysmsg}]}, "contents": [{"parts": [{"text": text}]}], "generationConfig": {"maxOutputTokens": 8000}}).encode()
s, b = call("gemini", f"leads:{len(docs)}abstracts", "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent",
            headers={"x-goog-api-key": load_secret("gemini.env", "GEMINI_API_KEY"), "Content-Type": "application/json"}, data=body, method="POST",
            save="gemini/leads_response.json", timeout=240, note="model analysis of supplied abstracts; leads, not verified; model gemini-3.8-flash")
(OUT / "gemini/leads_input_ids.json").write_text(json.dumps([d[:3] for d in docs], indent=1))
print(s, len(b))
