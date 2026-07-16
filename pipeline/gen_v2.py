import json
rows=json.load(open("contacts_master.json"))
D1={"U. Michigan–Ann Arbor","U. Wisconsin–Madison","Purdue University","UC Berkeley","Pennsylvania State University","Georgia Institute of Technology","North Carolina State University","U. Illinois Urbana-Champaign","U. Colorado Boulder","U. Washington"}
D2={"University of Florida","Cornell University","University of Maryland, College Park","University of Texas at Austin","Arizona State University","Massachusetts Institute of Technology","UC San Diego","Carnegie Mellon University","Ohio State University","University of Minnesota-Twin Cities"}
for r in rows:
    r["decile"]=1 if r["school"] in D1 else (2 if r["school"] in D2 else r.get("decile",0))
json.dump(rows,open("contacts_master.json","w"),ensure_ascii=False)

DATA=json.dumps(rows,ensure_ascii=False)
html=r'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>R1 STEM Advancement Contacts</title><style>
:root{color-scheme:light}*{box-sizing:border-box}
body{margin:0;background:#f7f8fa;color:#1a1d24;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:14px}
.wrap{padding:20px 22px 60px;max-width:1320px;margin:0 auto}
h1{font-size:20px;margin:0 0 4px;color:#1f3864}
.sub{color:#5b6470;font-size:12.5px;margin:0 0 16px;line-height:1.5}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 14px}
.stat{background:#fff;border:1px solid #e3e7ee;border-radius:8px;padding:9px 13px;min-width:96px}
.stat .n{font-size:19px;font-weight:700;color:#1f3864}.stat .l{font-size:10.5px;color:#6b7280;text-transform:uppercase;letter-spacing:.04em}
.controls{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px;align-items:center}
.controls input,.controls select{padding:8px 10px;border:1px solid #cfd6e0;border-radius:7px;font-size:13px;background:#fff}
.controls input{flex:1;min-width:180px}
.btn{padding:8px 12px;border:1px solid #1f3864;background:#1f3864;color:#fff;border-radius:7px;font-size:12.5px;cursor:pointer;font-weight:600}
.btn.sec{background:#fff;color:#1f3864}
.btn:hover{opacity:.9}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e3e7ee;border-radius:8px;overflow:hidden}
th{background:#1f3864;color:#fff;text-align:left;padding:9px 10px;font-size:11px;text-transform:uppercase;letter-spacing:.03em;position:sticky;top:0;cursor:pointer;white-space:nowrap}
th:hover{background:#2b4a80}
td{padding:8px 10px;border-top:1px solid #eef1f5;vertical-align:top}
tr:hover td{background:#f4f7fc}
a{color:#1a56c4;text-decoration:none}a:hover{text-decoration:underline}
.badge{display:inline-block;padding:2px 8px;border-radius:20px;font-size:11px;font-weight:600;white-space:nowrap}
.b-eng{background:#e5f0ff;color:#1a56c4}.b-med{background:#fde8ee;color:#b0244f}.b-sci{background:#e6f6ec;color:#1a7a44}.b-cen{background:#efe9fb;color:#6b3fbf}.b-env{background:#e7f5f3;color:#0f766e}.b-out{background:#eceff3;color:#4b5563}
.s-Sent{background:#eaf1fb;color:#1a56c4}.s-Replied{background:#e6f6ec;color:#158043}.s-Scheduled{background:#efe9fb;color:#6b3fbf}.s-Bounced{background:#fde8ee;color:#b0244f}
.sdate{font-size:10px;color:#9aa3af;display:block;margin-top:2px}
.muted{color:#9aa3af}
.guess{color:#b26a00;font-style:italic}
.gtag{display:inline-block;font-size:9px;font-weight:700;background:#fff3e0;color:#b26a00;border:1px solid #ffd9a8;border-radius:4px;padding:0 4px;margin-left:4px;text-transform:uppercase;letter-spacing:.03em;vertical-align:middle}
.src{font-size:10.5px;color:#9aa3af}
.foot{margin-top:14px;font-size:11.5px;color:#7a828d;line-height:1.5}
.count{font-size:12px;color:#6b7280;margin:0 0 8px}
</style></head><body><div class="wrap">
<h1>R1 STEM Advancement &amp; Development Contacts</h1>
<p class="sub">Development, alumni relations, and fundraising staff in <b>engineering, medicine, and science</b> units at the top NSF-award schools. From official university advancement directories. All 10 deciles complete (top 100 schools by NSF awards, last 12 months). Emails marked <span class="gtag">guess</span> were inferred from each office's confirmed email pattern and are unverified. <b>Outreach</b> column auto-updates from Amit's inbox (Sandeep's sends, replies, bounces) and calendar. Last synced: __SYNC__.</p>
<div class="stats">
<div class="stat"><div class="n" id="s-people">0</div><div class="l">Contacts</div></div>
<div class="stat"><div class="n" id="s-schools">0</div><div class="l">Schools</div></div>
<div class="stat"><div class="n" id="s-sent">0</div><div class="l">Sent</div></div>
<div class="stat"><div class="n" id="s-replied">0</div><div class="l">Replied</div></div>
<div class="stat"><div class="n" id="s-sched">0</div><div class="l">Scheduled</div></div>
<div class="stat"><div class="n" id="s-bounced">0</div><div class="l">Bounced</div></div>
<div class="stat"><div class="n" id="s-conf">0</div><div class="l">Confirmed email</div></div>
<div class="stat"><div class="n" id="s-guess">0</div><div class="l">Guessed email</div></div>
</div>
<div class="controls">
<input id="q" placeholder="Search name, title, focus, email…" oninput="render()">
<select id="fSchool" onchange="render()"><option value="">All schools</option></select>
<select id="fUnit" onchange="render()"><option value="">All units</option><option>Engineering</option><option>Medicine</option><option>Science</option><option>Environment</option><option>Central</option></select>
<select id="fEmail" onchange="render()"><option value="">Any email</option><option value="confirmed">Confirmed only</option><option value="guessed">Guessed only</option></select>
<select id="fStatus" onchange="render()"><option value="">Any outreach status</option><option>Not contacted</option><option>Sent</option><option>Replied</option><option>Scheduled</option><option>Bounced</option></select>
<button class="btn" onclick="dl()">Download CSV</button>
<button class="btn sec" onclick="cp()">Copy for Sheets</button>
</div>
<p class="count" id="count"></p>
<table><thead><tr>
<th onclick="sortBy('school')">School</th><th onclick="sortBy('unit')">Unit</th><th onclick="sortBy('name')">Name</th>
<th onclick="sortBy('title')">Title</th><th onclick="sortBy('focus')">Focus area</th>
<th onclick="sortBy('email')">Email</th><th onclick="sortBy('phone')">Phone</th><th onclick="sortBy('ostatus')">Outreach</th>
</tr></thead><tbody id="rows"></tbody></table>
<p class="foot">Sources: official college/school advancement and development directories at each institution. Confirmed emails and phones are as published. Guessed emails are inferred from the confirmed first.last / flast pattern at that office and must be verified before use. Donor-facing and fundraising-program staff only; administrative, gift-processing, and data roles excluded.</p>
</div>
<script>
const DATA=__DATA__;
let sortKey="school",sortDir=1;
const badge=u=>({Engineering:"b-eng",Medicine:"b-med",Science:"b-sci",Central:"b-cen",Environment:"b-env",Outreach:"b-out"}[u]||"b-cen");
function ocell(d){if(!d.ostatus||d.ostatus==='Not contacted')return '<span class="muted">—</span>';const dt=d.meeting||d.replied||d.bounced||d.sent||'';return `<span class="badge s-${d.ostatus}">${d.ostatus}</span>${dt?`<span class="sdate">${dt}</span>`:''}`;}
function schools(){const s=document.getElementById('fSchool');[...new Set(DATA.map(d=>d.school))].sort().forEach(x=>{const o=document.createElement('option');o.value=x;o.textContent=x;s.appendChild(o)})}
function sortBy(k){if(sortKey===k)sortDir*=-1;else{sortKey=k;sortDir=1}render()}
function filt(){const q=document.getElementById('q').value.toLowerCase(),fs=document.getElementById('fSchool').value,fu=document.getElementById('fUnit').value,fe=document.getElementById('fEmail').value,ft=document.getElementById('fStatus').value;
return DATA.filter(d=>{if(fs&&d.school!==fs)return false;if(fu&&d.unit!==fu)return false;if(fe&&d.email_status!==fe)return false;if(ft&&(d.ostatus||'Not contacted')!==ft)return false;if(q){const b=(d.name+d.title+d.focus+d.email+d.school).toLowerCase();if(!b.includes(q))return false}return true})}
function render(){let rows=filt();rows.sort((a,b)=>((a[sortKey]||'')+'').localeCompare((b[sortKey]||'')+'')*sortDir);
const tb=document.getElementById('rows');tb.innerHTML='';
rows.forEach(d=>{const tr=document.createElement('tr');
let em=d.email?(d.email_status==='guessed'?`<span class="guess">${d.email}</span><span class="gtag">guess</span>`:`<a href="mailto:${d.email}">${d.email}</a>`):'<span class="muted">—</span>';
tr.innerHTML=`<td>${d.school}<br><span class="src">${d.src}</span></td><td><span class="badge ${badge(d.unit)}">${d.unit}</span></td><td><b>${d.name}</b></td><td>${d.title}</td><td>${d.focus||'<span class=muted>—</span>'}</td><td>${em}</td><td>${d.phone?d.phone:'<span class=muted>—</span>'}</td><td>${ocell(d)}</td>`;tb.appendChild(tr)});
document.getElementById('count').textContent=`${rows.length} of ${DATA.length} contacts shown`;
document.getElementById('s-people').textContent=DATA.length;
document.getElementById('s-schools').textContent=new Set(DATA.map(d=>d.school)).size;
document.getElementById('s-conf').textContent=DATA.filter(d=>d.email_status==='confirmed').length;
document.getElementById('s-guess').textContent=DATA.filter(d=>d.email_status==='guessed').length;
document.getElementById('s-sent').textContent=DATA.filter(d=>d.sent).length;
document.getElementById('s-replied').textContent=DATA.filter(d=>d.replied).length;
document.getElementById('s-sched').textContent=DATA.filter(d=>d.meeting).length;
document.getElementById('s-bounced').textContent=DATA.filter(d=>d.bounced).length}
function cols(d){return[d.school,d.decile,d.unit,d.name,d.title,d.focus,d.email,d.email_status,d.phone,d.src,d.ostatus||'Not contacted',d.sent||'',d.replied||'',d.bounced||'',d.meeting||'']}
const HEAD=["School","Decile","Unit","Name","Title","Focus","Email","Email status","Phone","Source","Outreach status","Sent","Replied","Bounced","Meeting"];
function toCSV(rows){const esc=v=>{v=(v==null?'':''+v);return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v};return[HEAD.join(',')].concat(rows.map(d=>cols(d).map(esc).join(','))).join('\n')}
function dl(){const blob=new Blob([toCSV(filt())],{type:'text/csv'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='r1_stem_advancement_contacts.csv';a.click()}
function cp(){const rows=filt();const tsv=[HEAD.join('\t')].concat(rows.map(d=>cols(d).join('\t'))).join('\n');navigator.clipboard.writeText(tsv).then(()=>{const b=event.target;const t=b.textContent;b.textContent='Copied!';setTimeout(()=>b.textContent=t,1200)})}
schools();render();
</script></body></html>'''
import datetime
sync=datetime.datetime.now().strftime("%b %d, %Y %I:%M %p")
open("advancement_contacts.html","w").write(html.replace("__DATA__",DATA).replace("__SYNC__",sync))
print("HTML bytes:",len(html)+len(DATA))
# CSV
import csv
with open("r1_stem_advancement_contacts.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(["school","decile","unit","name","title","focus","email","email_status","phone","source","outreach_status","sent","replied","bounced","meeting"])
    for r in sorted(rows,key=lambda x:(x["decile"],x["school"],x["unit"],x["name"])):
        w.writerow([r["school"],r["decile"],r["unit"],r["name"],r["title"],r["focus"],r["email"],r["email_status"],r["phone"],r["src"],r.get("ostatus","Not contacted"),r.get("sent",""),r.get("replied",""),r.get("bounced",""),r.get("meeting","")])
print("wrote CSV rows:",len(rows))
