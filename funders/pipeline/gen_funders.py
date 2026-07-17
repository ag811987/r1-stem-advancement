import json, csv, datetime
rows=json.load(open("funders_master.json"))
DATA=json.dumps(rows,ensure_ascii=False)
sync=datetime.datetime.now().strftime("%b %d, %Y %I:%M %p")
html=r'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research Funders — Contacts</title><style>
:root{color-scheme:light}*{box-sizing:border-box}
body{margin:0;background:#f7f8fa;color:#1a1d24;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:14px}
.wrap{padding:20px 22px 60px;max-width:1360px;margin:0 auto}
h1{font-size:20px;margin:0 0 4px;color:#0f766e}
.sub{color:#5b6470;font-size:12.5px;margin:0 0 16px;line-height:1.5}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 14px}
.stat{background:#fff;border:1px solid #e3e7ee;border-radius:8px;padding:9px 13px;min-width:88px}
.stat .n{font-size:19px;font-weight:700;color:#0f766e}.stat .l{font-size:10.5px;color:#6b7280;text-transform:uppercase;letter-spacing:.04em}
.controls{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px;align-items:center}
.controls input,.controls select{padding:8px 10px;border:1px solid #cfd6e0;border-radius:7px;font-size:13px;background:#fff}
.controls input{flex:1;min-width:180px}
.btn{padding:8px 12px;border:1px solid #0f766e;background:#0f766e;color:#fff;border-radius:7px;font-size:12.5px;cursor:pointer;font-weight:600}
.btn.sec{background:#fff;color:#0f766e}.btn:hover{opacity:.9}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e3e7ee;border-radius:8px;overflow:hidden}
th{background:#0f766e;color:#fff;text-align:left;padding:9px 10px;font-size:11px;text-transform:uppercase;letter-spacing:.03em;position:sticky;top:0;cursor:pointer;white-space:nowrap}
th:hover{background:#115e56}
td{padding:8px 10px;border-top:1px solid #eef1f5;vertical-align:top}
tr:hover td{background:#f2faf8}
a{color:#0e7490;text-decoration:none}a:hover{text-decoration:underline}
.badge{display:inline-block;padding:2px 8px;border-radius:20px;font-size:11px;font-weight:600;white-space:nowrap}
.b-mem{background:#e6f6ec;color:#1a7a44}.b-sup{background:#e5f0ff;color:#1a56c4}.b-oth{background:#f3eafe;color:#6b3fbf}.b-out{background:#eceff3;color:#4b5563}
.s-Sent{background:#eaf1fb;color:#1a56c4}.s-Replied{background:#e6f6ec;color:#158043}.s-Scheduled{background:#efe9fb;color:#6b3fbf}.s-Bounced{background:#fde8ee;color:#b0244f}
.sdate{font-size:10px;color:#9aa3af;display:block;margin-top:2px}
.muted{color:#9aa3af}.guess{color:#b26a00;font-style:italic}
.gtag{display:inline-block;font-size:9px;font-weight:700;background:#fff3e0;color:#b26a00;border:1px solid #ffd9a8;border-radius:4px;padding:0 4px;margin-left:4px;text-transform:uppercase;letter-spacing:.03em;vertical-align:middle}
.src{font-size:10.5px;color:#9aa3af}.ff{font-size:11px;color:#6b7280;max-width:260px}
.foot{margin-top:14px;font-size:11.5px;color:#7a828d;line-height:1.5}
.count{font-size:12px;color:#6b7280;margin:0 0 8px}
</style></head><body><div class="wrap">
<h1>Research Funders &mdash; Grantmaking Contacts</h1>
<p class="sub">Program officers, science-program directors, and grants leadership at private research funders. Sources: Science Philanthropy Alliance member &amp; supporter roster + additional funders from the UMass CFR &ldquo;Private Foundations that Fund Research&rdquo; guide, official foundation team pages, and Amit's Gmail history. Emails marked <span class="gtag">guess</span> were inferred from each funder's confirmed pattern and are unverified. <b>Outreach</b> auto-updates from the inbox (Sandeep or Amit) &amp; calendar. Last synced: __SYNC__.</p>
<div class="stats">
<div class="stat"><div class="n" id="s-f">0</div><div class="l">Funders</div></div>
<div class="stat"><div class="n" id="s-p">0</div><div class="l">Contacts</div></div>
<div class="stat"><div class="n" id="s-sent">0</div><div class="l">Contacted</div></div>
<div class="stat"><div class="n" id="s-rep">0</div><div class="l">Replied</div></div>
<div class="stat"><div class="n" id="s-sch">0</div><div class="l">Met</div></div>
<div class="stat"><div class="n" id="s-conf">0</div><div class="l">Confirmed email</div></div>
<div class="stat"><div class="n" id="s-guess">0</div><div class="l">Guessed email</div></div>
</div>
<div class="controls">
<input id="q" placeholder="Search funder, name, title, program, focus…" oninput="render()">
<select id="fFunder" onchange="render()"><option value="">All funders</option></select>
<select id="fCat" onchange="render()"><option value="">All categories</option><option>SPA Member</option><option>SPA Supporter</option><option>Other (UMass)</option></select>
<select id="fStatus" onchange="render()"><option value="">Any outreach status</option><option>Not contacted</option><option>Sent</option><option>Replied</option><option>Scheduled</option><option>Bounced</option></select>
<button class="btn" onclick="dl()">Download CSV</button>
<button class="btn sec" onclick="cp()">Copy for Sheets</button>
</div>
<p class="count" id="count"></p>
<table><thead><tr>
<th onclick="sortBy('funder')">Funder</th><th onclick="sortBy('category')">Category</th>
<th onclick="sortBy('name')">Name</th><th onclick="sortBy('title')">Title</th>
<th onclick="sortBy('program')">Program</th><th onclick="sortBy('email')">Email</th>
<th onclick="sortBy('phone')">Phone</th><th onclick="sortBy('ostatus')">Outreach</th>
</tr></thead><tbody id="rows"></tbody></table>
<p class="foot">Donor-facing grantmaking staff only (program officers/directors, science leads, grants management, and leaders who drive grantmaking); communications, HR, IT, finance, and board-only members excluded. Outreach status reflects Amit's and Sandeep's email/calendar history (Sent / Replied / Scheduled / Bounce-back). Several small/family foundations publish no staff directory and appear as a single row. Guessed emails must be verified before use.</p>
</div>
<script>
const DATA=__DATA__;
let sortKey="funder",sortDir=1;
const badge=c=>({"SPA Member":"b-mem","SPA Supporter":"b-sup","Other (UMass)":"b-oth","Outreach":"b-out"}[c]||"b-oth");
function ocell(d){if(!d.ostatus||d.ostatus==='Not contacted')return '<span class="muted">—</span>';const dt=d.meeting||d.replied||d.bounced||d.sent||'';const by=d.by?` · ${d.by}`:'';return `<span class="badge s-${d.ostatus}">${d.ostatus}</span><span class="sdate">${dt}${by}</span>`;}
function funders(){const s=document.getElementById('fFunder');[...new Set(DATA.map(d=>d.funder))].sort().forEach(x=>{const o=document.createElement('option');o.value=x;o.textContent=x;s.appendChild(o)})}
function sortBy(k){if(sortKey===k)sortDir*=-1;else{sortKey=k;sortDir=1}render()}
function filt(){const q=document.getElementById('q').value.toLowerCase(),ff=document.getElementById('fFunder').value,fc=document.getElementById('fCat').value,ft=document.getElementById('fStatus').value;
return DATA.filter(d=>{if(ff&&d.funder!==ff)return false;if(fc&&d.category!==fc)return false;if(ft&&(d.ostatus||'Not contacted')!==ft)return false;if(q){const b=(d.funder+d.name+d.title+d.program+d.focus+d.email+d.ffocus).toLowerCase();if(!b.includes(q))return false}return true})}
function render(){let rows=filt();rows.sort((a,b)=>((a[sortKey]||'')+'').localeCompare((b[sortKey]||'')+'')*sortDir);
const tb=document.getElementById('rows');tb.innerHTML='';
rows.forEach(d=>{const tr=document.createElement('tr');
let em=d.email?(d.email_status==='guessed'?`<span class="guess">${d.email}</span><span class="gtag">guess</span>`:`<a href="mailto:${d.email}">${d.email}</a>`):'<span class="muted">—</span>';
let web=d.website?` · <a href="https://${d.website}" target="_blank">site</a>`:'';
tr.innerHTML=`<td><b>${d.funder}</b>${web}<br><span class="ff">${d.ffocus||''}</span></td><td><span class="badge ${badge(d.category)}">${d.category}</span></td><td>${d.name}</td><td>${d.title}</td><td>${d.program||'<span class=muted>—</span>'}</td><td>${em}</td><td>${d.phone?d.phone:'<span class=muted>—</span>'}</td><td>${ocell(d)}</td>`;tb.appendChild(tr)});
document.getElementById('count').textContent=`${rows.length} of ${DATA.length} contacts shown`;
document.getElementById('s-f').textContent=new Set(DATA.filter(d=>d.category!=='Outreach').map(d=>d.funder)).size;
document.getElementById('s-p').textContent=DATA.filter(d=>d.name!=='—').length;
document.getElementById('s-sent').textContent=DATA.filter(d=>d.sent).length;
document.getElementById('s-rep').textContent=DATA.filter(d=>d.replied).length;
document.getElementById('s-sch').textContent=DATA.filter(d=>d.meeting).length;
document.getElementById('s-conf').textContent=DATA.filter(d=>d.email_status==='confirmed').length;
document.getElementById('s-guess').textContent=DATA.filter(d=>d.email_status==='guessed').length}
function cols(d){return[d.funder,d.category,d.name,d.title,d.program,d.focus,d.email,d.email_status,d.phone,d.website,d.ffocus,d.ostatus||'Not contacted',d.sent||'',d.replied||'',d.bounced||'',d.meeting||'',d.by||'',d.src]}
const HEAD=["Funder","Category","Name","Title","Program","Focus","Email","Email status","Phone","Website","What they fund","Outreach status","Sent","Replied","Bounced","Meeting","By","Source"];
function toCSV(rows){const esc=v=>{v=(v==null?'':''+v);return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v};return[HEAD.join(',')].concat(rows.map(d=>cols(d).map(esc).join(','))).join('\n')}
function dl(){const blob=new Blob([toCSV(filt())],{type:'text/csv'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='research_funders_contacts.csv';a.click()}
function cp(){const rows=filt();const tsv=[HEAD.join('\t')].concat(rows.map(d=>cols(d).join('\t'))).join('\n');navigator.clipboard.writeText(tsv).then(()=>{const b=event.target;const t=b.textContent;b.textContent='Copied!';setTimeout(()=>b.textContent=t,1200)})}
funders();render();
</script></body></html>'''
open("funders.html","w").write(html.replace("__DATA__",DATA).replace("__SYNC__",sync))
with open("research_funders_contacts.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(["funder","category","name","title","program","focus","email","email_status","phone","website","what_they_fund","outreach_status","sent","replied","bounced","meeting","by","source"])
    for r in sorted(rows,key=lambda x:(x["category"],x["funder"],x["name"])):
        w.writerow([r["funder"],r["category"],r["name"],r["title"],r["program"],r["focus"],r["email"],r["email_status"],r["phone"],r["website"],r["ffocus"],r.get("ostatus","Not contacted"),r.get("sent",""),r.get("replied",""),r.get("bounced",""),r.get("meeting",""),r.get("by",""),r["src"]])
print("wrote funders.html + csv;",len(rows),"rows")
