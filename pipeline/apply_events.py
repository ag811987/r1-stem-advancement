#!/usr/bin/env python3
# Merge newly-observed outreach events into outreach.json.
# Input: new_events.json = list of {email, type: sent|replied|bounced|meeting,
#        date: "YYYY-MM-DD", first?: "", school_hint?: ""}
# Rule: only fill a field if currently empty (keep the earliest observation).
import json, os, sys
OUT = "outreach.json"
data = json.load(open(OUT)) if os.path.exists(OUT) else {}
data = {k.lower(): v for k, v in data.items()}
events = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "new_events.json"))
added = {"sent":0,"replied":0,"bounced":0,"meeting":0}
for e in events:
    em = (e.get("email") or "").strip().lower()
    t = e.get("type"); d = e.get("date","")
    if not em or t not in ("sent","replied","bounced","meeting"):
        continue
    rec = data.setdefault(em, {"sent":"","replied":"","bounced":"","meeting":"",
                               "first":e.get("first",""),"school_hint":e.get("school_hint","")})
    if not rec.get("first") and e.get("first"): rec["first"]=e["first"]
    if not rec.get("school_hint") and e.get("school_hint"): rec["school_hint"]=e["school_hint"]
    if not rec.get(t):
        rec[t] = d or rec.get(t,""); added[t]+=1
json.dump(data, open(OUT,"w"), ensure_ascii=False, indent=0)
print("merged events:", added, "| total tracked:", len(data))
