import json, re
rows=[]
for fn in ["funders_A.json","funders_B.json"]:
    for f in json.load(open(fn)):
        for c in f.get("contacts",[]):
            src=c.get("src","")
            guessed = "pattern-inferred" in src or "inferred" in src
            src=re.sub(r"\s*\(pattern-inferred email\)","",src); src=re.sub(r"\s*\(inferred\)","",src)
            email=c.get("email","")
            status = "guessed" if (email and guessed) else ("confirmed" if email else "none")
            rows.append({
                "funder":f["funder"],"category":f["category"],"website":f.get("website",""),
                "ffocus":f.get("focus",""),"name":c["name"],"title":c["title"],
                "program":c.get("program",""),"focus":c.get("focus",""),
                "email":email,"phone":c.get("phone",""),"src":src,"email_status":status})
# funders with no published contacts -> a placeholder row so they still show
have=set(r["funder"] for r in rows)
for fn in ["funders_A.json","funders_B.json"]:
    for f in json.load(open(fn)):
        if f["funder"] not in have:
            rows.append({"funder":f["funder"],"category":f["category"],"website":f.get("website",""),
                "ffocus":f.get("focus",""),"name":"—","title":"No public grantmaking-staff directory",
                "program":"","focus":"","email":"","phone":"","src":f.get("website",""),"email_status":"none"})
            have.add(f["funder"])
json.dump(rows,open("funders_master.json","w"),ensure_ascii=False)
from collections import Counter
print("contacts",len(rows),"funders",len(set(r['funder'] for r in rows)))
print("category",dict(Counter(r['category'] for r in rows)))
print("email",dict(Counter(r['email_status'] for r in rows)))
