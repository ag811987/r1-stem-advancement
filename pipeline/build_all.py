import json, re, unicodedata
from collections import Counter, defaultdict

rows=[]
# decile 1 base (confirmed/none only)
for r in json.load(open("contacts_data.json")):
    r=dict(r); r["email_status"]="confirmed" if r.get("email") else "none"; rows.append(r)
# decile 2 & 3 files
for fn in ["schools_d2a.json","schools_d2b.json","schools_d3a.json","schools_d3b.json","schools_d4a.json","schools_d4b.json","schools_d5a.json","schools_d5b.json","schools_d6a.json","schools_d6b.json","schools_d7a.json","schools_d7b.json","schools_d8a.json","schools_d8b.json","schools_d9a.json","schools_d9b.json","schools_d10a.json","schools_d10b.json"]:
    d=json.load(open(fn))
    for school,meta in d.items():
        for c in meta["contacts"]:
            rows.append({"school":school,"unit":c["unit"],"name":c["name"],"title":c["title"],
                         "email":c.get("email",""),"phone":c.get("phone",""),"focus":c["focus"],
                         "src":c["src"],"email_status":"confirmed" if c.get("email") else "none"})

DEC={1:{"U. Michigan–Ann Arbor","U. Wisconsin–Madison","Purdue University","UC Berkeley","Pennsylvania State University","Georgia Institute of Technology","North Carolina State University","U. Illinois Urbana-Champaign","U. Colorado Boulder","U. Washington"},
2:{"University of Florida","Cornell University","University of Maryland, College Park","University of Texas at Austin","Arizona State University","Massachusetts Institute of Technology","UC San Diego","Carnegie Mellon University","Ohio State University","University of Minnesota-Twin Cities"},
3:{"Virginia Polytechnic Institute and State University","Johns Hopkins University","Columbia University","UC Irvine","Iowa State University","University of Utah","Northwestern University","UCLA","University of Chicago","Brown University"},
4:{"University of North Carolina at Chapel Hill","Texas A&M University","University of California-Riverside","Michigan State University","University of Massachusetts Amherst","University of Alabama Tuscaloosa","University of California-Davis","University of Southern California","New York University","Princeton University"},
5:{"Stanford University","University of Arizona","University of Delaware","Northeastern University","University of Tennessee Knoxville","Indiana University","University of Nebraska-Lincoln","Yale University","Clemson University","University of California-Santa Barbara"},
6:{"University of New Mexico","University of Notre Dame","University of Virginia","California Institute of Technology","Florida State University","University of Pennsylvania","University of Texas at Dallas","Rutgers University New Brunswick","University of South Carolina at Columbia","George Mason University"},
7:{"University of Georgia","University of Hawaii","University of Oklahoma Norman Campus","Duke University","Oregon State University","University of Kentucky","Boston University","William Marsh Rice University","University of Connecticut","Washington University"},
8:{"University of Houston","Louisiana State University","University of California-Santa Cruz","Vanderbilt University","Auburn University","The University of Central Florida Board of Trustees","University of Texas at Arlington","Dartmouth College","University of Pittsburgh","Woods Hole Oceanographic Institution"},
9:{"Colorado State University","Harvard University","University of Arkansas","University of Illinois at Chicago","University of Iowa","University of Missouri-Columbia","Kansas State University","Tufts University","Rochester Institute of Tech","Stevens Institute of Technology"},
10:{"University of Oregon","Emory University","University of Kansas","Washington State University","University of California-Merced","University of Rochester","University of Nevada-Reno","Boise State University","University of Idaho","University of Alaska Fairbanks"}}
s2d={s:d for d,ss in DEC.items() for s in ss}
for r in rows: r["decile"]=s2d.get(r["school"],0)

def deacc(s): return "".join(c for c in unicodedata.normalize("NFKD",s) if not unicodedata.combining(c))
def toks(n):
    n=re.sub(r"[^a-z ]"," ",deacc(n).lower()); return [p for p in n.split() if p not in ("jr","sr","ii","iii","dr") and len(p)>1]
def make(p,f,l): return {"first.last":f+"."+l,"firstlast":f+l,"flast":f[0]+l,"firstl":f+l[0],"first_last":f+"_"+l,"lastf":l+f[0]}.get(p)
PATS=["first.last","flast","firstlast","firstl","first_last","lastf"]
by_s=defaultdict(list); by_su=defaultdict(list)
for r in rows: by_s[r["school"]].append(r); by_su[(r["school"],r["unit"])].append(r)
def dom(es): ds=[e.split("@")[1] for e in es if "@" in e]; return Counter(ds).most_common(1)[0][0] if ds else None
spat={}; sdom={}; sudom={}
for s,rs in by_s.items():
    conf=[r for r in rs if r["email_status"]=="confirmed"]; sdom[s]=dom([r["email"] for r in conf]); t=Counter()
    for r in conf:
        loc=r["email"].split("@")[0].lower(); tk=toks(r["name"])
        if len(tk)<2: continue
        for p in PATS:
            if make(p,tk[0],tk[-1])==loc: t[p]+=1
    spat[s]=t.most_common(1)[0][0] if t else "flast"
for (s,u),rs in by_su.items():
    sudom[(s,u)]=dom([r["email"] for r in rs if r["email_status"]=="confirmed"])
g=0
for r in rows:
    if r["email_status"]=="confirmed": continue
    d=sudom.get((r["school"],r["unit"])) or sdom.get(r["school"])
    tk=toks(r["name"])
    if not d or len(tk)<2: r["email_status"]="none"; continue
    loc=make(spat[r["school"]],tk[0],tk[-1])
    if not loc: r["email_status"]="none"; continue
    r["email"]=loc+"@"+d; r["email_status"]="guessed"; g+=1
# ---- merge outreach tracking (Sent / Replied / Bounced / Scheduled) ----
import os
OUT={}
if os.path.exists("outreach.json"):
    OUT={k.lower():v for k,v in json.load(open("outreach.json")).items()}
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
        r["sent"]=o.get("sent",""); r["replied"]=o.get("replied","")
        r["bounced"]=o.get("bounced",""); r["meeting"]=o.get("meeting","")
        r["ostatus"]=ostatus(o)
    else:
        r["sent"]=r["replied"]=r["bounced"]=r["meeting"]=""; r["ostatus"]="Not contacted"
# outreach recipients not matched to any curated contact -> add as their own rows
for em,o in OUT.items():
    if em in seen: continue
    rows.append({"school":o.get("school_hint","(outreach)"),"decile":0,"unit":"Outreach",
                 "name":(o.get("first","") or em.split("@")[0])+" (emailed)","title":"Emailed by Sandeep — not in curated list",
                 "email":em,"phone":"","focus":"","src":"gmail","email_status":"confirmed",
                 "sent":o.get("sent",""),"replied":o.get("replied",""),"bounced":o.get("bounced",""),
                 "meeting":o.get("meeting",""),"ostatus":ostatus(o)})
json.dump(rows,open("contacts_master.json","w"),ensure_ascii=False)
print("total",len(rows),"schools",len(set(r['school'] for r in rows)),"deciles",sorted(set(r['decile'] for r in rows)))
print("confirmed",sum(1 for r in rows if r['email_status']=='confirmed'),"guessed",g,"none",sum(1 for r in rows if r['email_status']=='none'))
from collections import Counter as _C
print("outreach:",dict(_C(r['ostatus'] for r in rows)))
