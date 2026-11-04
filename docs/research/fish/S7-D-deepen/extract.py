import sys, pypdf
for p in sys.argv[1:]:
    r = pypdf.PdfReader(p)
    print(p, "pages", len(r.pages))
    txt = " ".join((pg.extract_text() or "") for pg in r.pages)[:600]
    print("TEXT:", txt.replace("\n"," "))
    n=0
    for i,pg in enumerate(r.pages):
        for a in (pg.get("/Annots") or []):
            a=a.get_object()
            if a.get("/Subtype")=="/3D":
                s=a["/3DD"].get_object()
                data=s.get_data()
                out=f"{p}.{n}.u3d"; open(out,"wb").write(data); n+=1
                print(" 3D annot", s.get("/Subtype"), len(data), "->", out)
