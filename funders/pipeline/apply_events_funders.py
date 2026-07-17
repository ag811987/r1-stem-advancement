#!/usr/bin/env python3
# Merge newly-observed outreach events into outreach_funders.json.
# Input JSON array of {email, type: sent|replied|bounced|meeting, date, first?, funder_hint?, by?}
import json, os, sys
OUT="outreach_funders.json"
data=json.load(open(OUT)) if os.path.exists(OUT) else {}
data={k.lower():v for k,v in data.items()}
events=json.load(open(sys.argv[1] if len(sys.argv)>1 else "new_events.json"))
added={"sent":0,"replied":0,"bounced":0,"meeting":0}
for e in events:
    em=(e.get("email") or "").strip().lower(); t=e.get("type"); d=e.get("date","")
    if not em or t not in ("sent","replied","bounced","meeting"): continue
    rec=data.setdefault(em,{"sent":"","replied":"","bounced":"","meeting":"","first":e.get("first",""),"funder_hint":e.get("funder_hint",""),"by":e.get("by","")})
    for k in ("first","funder_hint","by"):
        if not rec.get(k) and e.get(k): rec[k]=e[k]
    if not rec.get(t): rec[t]=d or rec.get(t,""); added[t]+=1
json.dump(data,open(OUT,"w"),ensure_ascii=False,indent=0)
print("merged",added,"| tracked",len(data))
