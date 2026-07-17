import json, re, os, unicodedata
from collections import Counter, defaultdict

# ---- emails confirmed from Amit's Gmail (override roster blanks) ----
CONFIRM={
 ("The Kavli Foundation","Amy Bernard"):"abernard@kavlifoundation.org",
 ("The Kavli Foundation","Stephanie Albin"):"salbin@kavlifoundation.org",
 ("The Kavli Foundation","Brooke Smith"):"bsmith@kavlifoundation.org",
 ("The David & Lucile Packard Foundation","Chad English"):"cenglish@packard.org",
 ("Doris Duke Foundation","Samsher Gill"):"sgill@dorisduke.org",
 ("Doris Duke Foundation","Kevin Sia"):"ksia@dorisduke.org",
 ("Doris Duke Foundation","Sindy Escobar Alvarez"):"sescobar@dorisduke.org",
 ("Schmidt Sciences","James Ricci"):"jricci@schmidtsciences.org",
 ("Fund for Science and Technology","Ashton Rennegarbe"):"ashtonr@ff-st.org",
}
# ---- extra contacts discovered in Amit's Gmail (real prior relationships) ----
EXTRA=[
 {"funder":"Schmidt Sciences","category":"SPA Member","website":"schmidtsciences.org","ffocus":"Interdisciplinary basic research",
  "name":"Richard Murray","title":"Program Lead / Advisor (Caltech)","program":"AI & Advanced Computing / EngBio","focus":"Prior Catalyze contact — Seattle node & EngBio workshop","email":"rmurray@schmidtsciences.org","phone":"","src":"gmail"},
 {"funder":"Schmidt Sciences","category":"SPA Member","website":"schmidtsciences.org","ffocus":"Interdisciplinary basic research",
  "name":"Suhas Mahesh","title":"Program Scientist, AI and Advanced Computing","program":"AI & Advanced Computing","focus":"Prior Catalyze contact — AI x science prizes/challenges","email":"smahesh@schmidtsciences.org","phone":"","src":"gmail"},
 {"funder":"Doris Duke Foundation","category":"SPA Member","website":"dorisduke.org","ffocus":"Medical Research program",
  "name":"Jennifer Katz","title":"Development / Advancement","program":"Development","focus":"Prior Catalyze fundraising contact","email":"jkatz@dorisduke.org","phone":"","src":"gmail"},
 {"funder":"Gates Foundation","category":"SPA Member","website":"gatesfoundation.org","ffocus":"Global Health — Discovery & Translational Sciences",
  "name":"Dan Wattendorf","title":"Director (Innovative Technology Solutions)","program":"Global Health","focus":"Prior Catalyze contact (referred to GPP team)","email":"dan.wattendorf@gatesfoundation.org","phone":"","src":"gmail"},
 {"funder":"Chan Zuckerberg Biohub","category":"SPA Member","website":"biohub.org","ffocus":"Interdisciplinary biomedical research",
  "name":"Bailey Marshall","title":"CZI Science","program":"CZI Science","focus":"Prior Catalyze intro contact","email":"bmarshall@chanzuckerberg.com","phone":"","src":"gmail"},
 {"funder":"The Kavli Foundation","category":"SPA Member","website":"kavlifoundation.org","ffocus":"Basic science in astrophysics, nanoscience, neuroscience",
  "name":"Deron Bos","title":"Program / Grants","program":"Science","focus":"Prior Catalyze contact","email":"dbos@kavlifoundation.org","phone":"","src":"gmail"},
 {"funder":"Siegel Family Endowment","category":"SPA Member","website":"siegelendowment.org","ffocus":"Technology & society",
  "name":"Laura Maher","title":"Program / Engagement","program":"Programs","focus":"Prior Catalyze biosecurity-panels contact","email":"laura.maher@siegelendowment.org","phone":"","src":"gmail"},
 {"funder":"Fund for Science and Technology","category":"SPA Member","website":"ff-st.org","ffocus":"Transformational science & technology",
  "name":"Ratika Kohli","title":"Program","program":"Programs","focus":"Prior Catalyze Maryland-preview contact","email":"ratikak@ff-st.org","phone":"","src":"gmail"},
]
# domain override where staff email domain differs from website
DOM={"The Pew Charitable Trusts":"pewtrusts.org","Chan Zuckerberg Biohub":"chanzuckerberg.com",
 "Dalio Philanthropies":"oceanxscience.org","Allen Family Philanthropies":"allenphilanthropies.org"}
# confirmed / best-guess email pattern per funder: tokens first,last -> local part
PAT={"Alfred P. Sloan Foundation":"last","Research Corporation for Science Advancement":"flast",
 "Arnold & Mabel Beckman Foundation":"flast","Lasker Foundation":"flast","The Kavli Foundation":"flast",
 "Doris Duke Foundation":"flast","The David & Lucile Packard Foundation":"flast","Schmidt Sciences":"flast",
 "Gates Foundation":"first.last","Siegel Family Endowment":"first.last","Robertson Foundation":"first.last",
 "Klaus Tschira Stiftung":"first.last","Fund for Science and Technology":"firstl"}
DEFAULT_PAT="first.last"

def deacc(s): return "".join(c for c in unicodedata.normalize("NFKD",s) if not unicodedata.combining(c))
def toks(n):
    n=re.sub(r"[^a-z ]"," ",deacc(n).lower()); return [p for p in n.split() if p not in ("jr","sr","ii","iii","dr","phd","md") and len(p)>1]
def make(p,f,l):
    return {"first.last":f+"."+l,"flast":f[0]+l,"firstlast":f+l,"firstl":f+l[0],"last":l,"first":f}.get(p)

rows=[]
for fn in ["funders_A.json","funders_B.json"]:
    for f in json.load(open(fn)):
        for c in f.get("contacts",[]):
            email=CONFIRM.get((f["funder"],c["name"]), c.get("email",""))
            src=c.get("src",""); src=re.sub(r"\s*\(pattern-inferred email\)","",src); src=re.sub(r"\s*\(inferred\)","",src)
            marked_guess = "pattern-inferred" in c.get("src","") or "inferred" in c.get("src","")
            status="confirmed" if (email and not marked_guess) else ("guessed" if email else "none")
            rows.append({"funder":f["funder"],"category":f["category"],"website":f.get("website",""),
                "ffocus":f.get("focus",""),"name":c["name"],"title":c["title"],"program":c.get("program",""),
                "focus":c.get("focus",""),"email":email,"phone":c.get("phone",""),"src":src,"email_status":status})
for e in EXTRA:
    rows.append({"funder":e["funder"],"category":e["category"],"website":e["website"],"ffocus":e["ffocus"],
        "name":e["name"],"title":e["title"],"program":e["program"],"focus":e["focus"],
        "email":e["email"],"phone":e.get("phone",""),"src":e["src"],"email_status":"confirmed"})
# funders with no contacts -> placeholder row
have=set(r["funder"] for r in rows)
for fn in ["funders_A.json","funders_B.json"]:
    for f in json.load(open(fn)):
        if f["funder"] not in have:
            rows.append({"funder":f["funder"],"category":f["category"],"website":f.get("website",""),
                "ffocus":f.get("focus",""),"name":"—","title":"No public grantmaking-staff directory",
                "program":"","focus":"","email":"","phone":"","src":f.get("website",""),"email_status":"none"}); have.add(f["funder"])

# ---- guess emails from per-funder domain + pattern ----
by_f=defaultdict(list)
for r in rows: by_f[r["funder"]].append(r)
fdom={}; fpat={}
for fu,rs in by_f.items():
    web=rs[0]["website"] or ""
    dom = DOM.get(fu) or (web.split("/")[0] if web else None)
    fdom[fu]=dom
    conf=[r for r in rs if r["email_status"]=="confirmed" and "@" in r["email"]]
    if conf and not dom:
        fdom[fu]=Counter(r["email"].split("@")[1] for r in conf).most_common(1)[0][0]; dom=fdom[fu]
    t=Counter()
    for r in conf:
        loc=r["email"].split("@")[0].lower(); tk=toks(r["name"])
        if len(tk)<2: continue
        for p in ["first.last","flast","firstlast","firstl","last","first"]:
            if make(p,tk[0],tk[-1])==loc: t[p]+=1
    fpat[fu]= t.most_common(1)[0][0] if t else PAT.get(fu, DEFAULT_PAT)
g=0
for r in rows:
    if r["email_status"]!="none" or r["name"]=="—": continue
    dom=fdom.get(r["funder"]); tk=toks(r["name"])
    if not dom or len(tk)<2: continue
    loc=make(fpat[r["funder"]],tk[0],tk[-1])
    if not loc: continue
    r["email"]=loc+"@"+dom; r["email_status"]="guessed"; g+=1

# ---- merge outreach tracking ----
OUT={}
if os.path.exists("outreach_funders.json"):
    OUT={k.lower():v for k,v in json.load(open("outreach_funders.json")).items()}
def ostatus(o):
    if o.get("meeting"): return "Scheduled"
    if o.get("replied"): return "Replied"
    if o.get("bounced"): return "Bounced"
    if o.get("sent"): return "Sent"
    return "Not contacted"
seen=set()
for r in rows:
    o=OUT.get((r.get("email") or "").lower())
    if o:
        seen.add((r.get("email") or "").lower())
        r["sent"]=o.get("sent","");r["replied"]=o.get("replied","");r["bounced"]=o.get("bounced","");r["meeting"]=o.get("meeting","");r["by"]=o.get("by","");r["ostatus"]=ostatus(o)
    else:
        r["sent"]=r["replied"]=r["bounced"]=r["meeting"]=r["by"]="";r["ostatus"]="Not contacted"
for em,o in OUT.items():
    if em in seen: continue
    rows.append({"funder":o.get("funder_hint","(outreach)"),"category":"Outreach","website":"","ffocus":"",
        "name":(o.get("first","") or em.split("@")[0])+" (emailed)","title":"Emailed — not in curated list","program":"",
        "focus":"","email":em,"phone":"","src":"gmail","email_status":"confirmed",
        "sent":o.get("sent",""),"replied":o.get("replied",""),"bounced":o.get("bounced",""),"meeting":o.get("meeting",""),"by":o.get("by",""),"ostatus":ostatus(o)})

json.dump(rows,open("funders_master.json","w"),ensure_ascii=False)
print("contacts",len(rows),"funders",len(set(r['funder'] for r in rows)))
print("email",dict(Counter(r['email_status'] for r in rows)),"guessed_now",g)
print("outreach",dict(Counter(r['ostatus'] for r in rows)))
