#!/usr/bin/env python3
# Generates BRGA deliverables from req/final/master.json (+xdup, dar mapping).
import json, re, csv, collections, os, sys
sys.path.insert(0, '/home/claude/audit/tools')
from dar_data import DAR, BUCKET_DEFAULT
BASE = '/home/claude/audit'
OUT = f'{BASE}/pkg'
os.makedirs(f'{OUT}/register', exist_ok=True)
M = json.load(open(f'{BASE}/req/final/master.json'))
X = json.load(open(f'{BASE}/req/final/xdup.json'))
reqs, rules, decs, mapping = M['reqs'], M['rules'], M['decs'], M['mapping']
byid = {r['req_id']: r for r in reqs}
BNAME = {"C1":"Order-to-Cash (O2C)","C2":"العملاء والمبيعات الميدانية (CRM)","C3":"Procure-to-Pay (P2P)","C4":"المخزون والجودة والمرتجعات (INV)",
 "C5":"Record-to-Report (R2R)","C6":"الخزينة وضبط الائتمان (TRC)","C7":"الحوافز وHR-to-Finance (INH)","C8":"الهوية والموافقات وتجربة الاستخدام والذكاء (SEC)",
 "C9":"المتطلبات غير الوظيفية (NFR)","C10":"التشغيل وترحيل البيانات (OPS)"}
ORDER = ["C1","C2","C3","C4","C5","C6","C7","C8","C9","C10"]
CLS = {"DOCUMENTED_REQ":"متطلب موثق","OWNER_DECISION":"قرار منسوب للمالك","INFERRED_NEEDS_APPROVAL":"مستنتج يحتاج اعتمادًا","OPTIONAL_IMPROVEMENT":"تحسين اختياري"}
def st(s):
    s = (s or '').strip()
    m = re.match(r'([A-Z_]+)', s.upper())
    return m.group(1) if m else 'NOT_VERIFIED'
def esc(s):
    t = str(s or '').replace('|', '\\|').replace('\n', ' ')
    parts = re.split(r'(`[^`]*`)', t)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'<(?!/?(?:sub|sup|br)\b)', '&lt;', parts[i])
    return ''.join(parts)
def short(s, n=140):
    s = esc(s); return s if len(s) <= n else s[:n-1] + '…'

# ---- cross-bucket relations ----
merged_into = {}; related = collections.defaultdict(set); xconf = []
for g in X:
    ids = g['ids']
    if g['relation'] == 'DUPLICATE':
        p = g['primary']
        for i in ids:
            if i != p: merged_into[i] = p
    for i in ids:
        for j in ids:
            if i != j: related[i].add(j)
    if g['relation'] == 'CONFLICTING': xconf.append(g)
for r in reqs:
    r['merged_into'] = merged_into.get(r['req_id'], '')
    r['xrelated'] = sorted(related.get(r['req_id'], []))
net = [r for r in reqs if not r['merged_into']]

# ---- DAR routing ----
for r in reqs:
    text = ' '.join([r.get('data_requirement_ar',''), r.get('title_ar',''), r.get('requirement_ar','')])
    ds = []
    for did, title, adr, fnd, pats in DAR:
        if any(re.search(p, text, re.I) for p in pats): ds.append(did)
    if not ds: ds = list(BUCKET_DEFAULT.get(r['bucket'], []))
    if any(f in sum([d[3] for d in DAR if d[0] in ds], []) for f in r.get('related_findings', [])): pass
    r['dar'] = ds

# ---- counts ----
def cnt(rs, f): return collections.Counter(f(r) for r in rs)
C = {
 'raw': len(mapping), 'reqs': len(reqs), 'net': len(net), 'merged': len(merged_into),
 'class': cnt(net, lambda r: r['class']), 'prio': cnt(net, lambda r: r['priority']),
 'B': cnt(net, lambda r: st(r['status_baseline'])), 'Cc': cnt(net, lambda r: st(r['status_current'])),
 'disp': collections.Counter(re.split(r'[:\s]', v['disp'])[0] for v in mapping.values()),
 'rules': len(rules), 'rtype': collections.Counter(x.get('type','') for x in rules),
 'decs': len(decs), 'dkind': collections.Counter(d['kind'] for d in decs), 'block': sum(1 for d in decs if d.get('blocking')),
 'xconf': len(xconf), 'ac': sum(len(r['acceptance_criteria']) for r in net),
}
json.dump({k:(dict(v) if isinstance(v, collections.Counter) else v) for k,v in C.items()}, open(f'{BASE}/req/final/counts.json','w'), ensure_ascii=False, indent=1)

STAT_AR = {"IMPLEMENTED":"منفذ","PARTIAL":"جزئي","NOT_IMPLEMENTED":"غير منفذ","CONTRADICTED":"مُخالَف","NOT_VERIFIED":"لم يُتحقق","NOT_APPLICABLE":"لا ينطبق"}
SORD = ["IMPLEMENTED","PARTIAL","NOT_IMPLEMENTED","CONTRADICTED","NOT_VERIFIED","NOT_APPLICABLE"]

# ================= 21 Register =================
md = ["# 21 — سجل المتطلبات (Requirements Register)", "",
 f"**{C['net']} متطلبًا صافيًا** ({C['reqs']} معرّفًا مع {C['merged']} مكررًا عبر المجالات دُمج في متطلب أساسي ويُعرض للتتبع فقط). مستخرجة من **{C['raw']} عبارة خام** في 174 مصدرًا (انظر `20-BRGA-Overview.md`).", "",
 "**الأعمدة:** التصنيف (موثق / قرار مالك / مستنتج يحتاج اعتمادًا / تحسين) · المصدر الأول وتاريخه · الأولوية · الحالة في BASELINE (B) وCURRENT (C) — الإنتاج **Unknown** لكل المتطلبات · القرارات المرتبطة. البطاقة الكاملة لكل متطلب (الغرض، المستخدم، القواعد، المدخلات والمخرجات، الاستثناءات، الموافقات، معايير القبول، الأدلة UI/API/service/schema/events/tests، الفجوة، الأثر، الاعتماديات، السؤال للمالك، متطلب البيانات) في `register/<المجال>.md`، والجدول الكامل القابل للفرز في `requirements-register.csv`.", ""]
md += ["| المجال | العدد الصافي | موثق | قرار مالك | مستنتج | تحسين | P1 | ملف البطاقات |", "|---|---|---|---|---|---|---|---|"]
for b in ORDER:
    rs = [r for r in net if r['bucket']==b]; c = cnt(rs, lambda r: r['class'])
    md.append(f"| {BNAME[b]} | {len(rs)} | {c['DOCUMENTED_REQ']} | {c['OWNER_DECISION']} | {c['INFERRED_NEEDS_APPROVAL']} | {c['OPTIONAL_IMPROVEMENT']} | {sum(1 for r in rs if r['priority']=='P1')} | `register/{b}.md` |")
md.append(f"| **المجموع** | **{C['net']}** | {C['class']['DOCUMENTED_REQ']} | {C['class']['OWNER_DECISION']} | {C['class']['INFERRED_NEEDS_APPROVAL']} | {C['class']['OPTIONAL_IMPROVEMENT']} | {C['prio']['P1']} | |")
md.append("")
if merged_into:
    md += ["## المتطلبات المكررة عبر المجالات (مدمجة)", "| المعرّف المكرر | دُمج في | السبب |", "|---|---|---|"]
    for g in X:
        if g['relation']=='DUPLICATE':
            for i in g['ids']:
                if i != g['primary']: md.append(f"| {i} | **{g['primary']}** | {short(g['reason_ar'],120)} |")
    md.append("")
for b in ORDER:
    rs = [r for r in reqs if r['bucket']==b]
    md += [f"## {BNAME[b]}", "", "| ID | المتطلب | التصنيف | المصدر (التاريخ) | الأولوية | B | C | قرارات |", "|---|---|---|---|---|---|---|---|"]
    for r in rs:
        s0 = r['sources'][0] if r['sources'] else {}
        src = f"`{s0.get('source','')}:{s0.get('lines','')}` ({s0.get('date','')})" + (f" +{len(r['sources'])-1}" if len(r['sources'])>1 else '')
        tag = f" ↪ مدمج في {r['merged_into']}" if r['merged_into'] else ''
        md.append(f"| {r['req_id']} | {short(r['title_ar'],110)}{tag} | {CLS.get(r['class'],r['class'])} | {src} | {r['priority']} | {STAT_AR.get(st(r['status_baseline']))} | {STAT_AR.get(st(r['status_current']))} | {', '.join(r['decision_refs'][:4])} |")
    md.append("")
open(f'{OUT}/21-Requirements-Register.md','w').write('\n'.join(md))

# per-bucket cards
rulesby = {x['br_id']: x for x in rules}
for b in ORDER:
    rs = [r for r in reqs if r['bucket']==b]
    o = [f"# بطاقات المتطلبات — {BNAME[b]}", "", f"{len(rs)} متطلبًا. الحالة في الإنتاج Unknown لكل متطلب. الأدلة: `[B]`=89c2c31، `[C]`=fa40270؛ الاختبارات موجودة كملفات ولم تُشغّل.", ""]
    for r in rs:
        ev = r.get('evidence') or {}
        o += [f"## {r['req_id']} — {esc(r['title_ar'])}", "",
         f"- **التصنيف:** {CLS.get(r['class'],r['class'])} · **صاحب القرار:** {esc(r.get('decider'))} · **الأولوية:** {r['priority']} — {esc(r.get('priority_reason'))}" + (f" · **مدمج في:** {r['merged_into']}" if r['merged_into'] else ''),
         f"- **المصادر:** " + '؛ '.join(f"`{s.get('source')}:{s.get('lines')}` ({s.get('date')}, {s.get('decider')}, {s.get('sid')})" for s in r['sources']),
         f"- **العملية / المستخدم المسؤول:** {esc(r.get('process'))} / {esc(r.get('responsible_user'))}",
         f"- **الغرض التجاري:** {esc(r.get('purpose_ar'))}",
         f"- **نص المتطلب:** {esc(r.get('requirement_ar'))}",
         f"- **قواعد الأعمال:** " + (', '.join(r['business_rules']) or '—'),
         f"- **المدخلات / المخرجات:** {esc(r.get('inputs'))} / {esc(r.get('outputs'))}",
         f"- **المسار العادي:** {esc(r.get('normal_flow'))}",
         f"- **الاستثناءات والإلغاء والعكس وإعادة المحاولة:** {esc(r.get('exceptions_cancel_reverse_retry'))}",
         f"- **الموافقات والصلاحيات وفصل المهام:** {esc(r.get('approvals_sod'))}",
         f"- **معايير القبول:**"] + [f"  - {esc(a)}" for a in r['acceptance_criteria']] + [
         f"- **الحالة:** BASELINE: {esc(r['status_baseline'])} · CURRENT: {esc(r['status_current'])} · الإنتاج: Unknown",
         f"- **الأدلة:** UI: {esc(ev.get('ui'))} · API: {esc(ev.get('api'))} · Service: {esc(ev.get('service'))} · Schema: {esc(ev.get('schema'))} · Events: {esc(ev.get('events'))} · Tests: {esc(ev.get('tests'))}",
         f"- **الفجوة:** {esc(r.get('gap_ar'))}",
         f"- **الأثر:** {esc(r.get('impact_ar'))}",
         f"- **الاعتماديات:** {', '.join(r.get('dependencies') or []) or '—'} · **القرارات:** {', '.join(r['decision_refs']) or '—'} · **النتائج المرتبطة:** {', '.join(r.get('related_findings') or []) or '—'}",
         f"- **متطلبات مرتبطة:** {', '.join(sorted(set((r.get('related_reqs') or []) + r['xrelated']))) or '—'}",
         f"- **متطلب البيانات:** {esc(r.get('data_requirement_ar'))} → **توصيات معمارية:** {', '.join(r['dar']) or '— (تطبيقي، لا أثر على تصميم البيانات)'}",
         f"- **سؤال للمالك:** {esc(r.get('owner_question_ar')) or '—'}", ""]
    open(f'{OUT}/register/{b}.md','w').write('\n'.join(o))

with open(f'{OUT}/requirements-register.csv','w',newline='',encoding='utf-8-sig') as fh:
    w = csv.writer(fh)
    cols = ['req_id','bucket','title_ar','class','decider','process','responsible_user','purpose_ar','requirement_ar','business_rules','inputs','outputs','normal_flow','exceptions_cancel_reverse_retry','approvals_sod','acceptance_criteria','status_baseline','status_current','status_production','ev_ui','ev_api','ev_service','ev_schema','ev_events','ev_tests','gap_ar','impact_ar','priority','priority_reason','dependencies','decision_refs','owner_question_ar','related_findings','data_requirement_ar','dar','related_reqs','merged_into','sources']
    w.writerow(cols)
    for r in reqs:
        ev = r.get('evidence') or {}
        row = []
        for c in cols:
            if c.startswith('ev_'): v = ev.get(c[3:], '')
            elif c == 'related_reqs': v = sorted(set((r.get('related_reqs') or []) + r['xrelated']))
            elif c == 'sources': v = [f"{s.get('source')}:{s.get('lines')} ({s.get('date')}; {s.get('sid')})" for s in r['sources']]
            else: v = r.get(c, '')
            row.append(' | '.join(v) if isinstance(v, list) else v)
        w.writerow(row)

# ================= 22 Gap matrix =================
g = ["# 22 — مصفوفة الفجوات (Gap Matrix)", "",
 f"تُحسب على **{C['net']} متطلبًا صافيًا**. الحالة في الإنتاج **Unknown** لكل الصفوف حتى تثبت الأدلة (E-01…E-07). `مُخالَف` = الكود يفعل عكس المتطلب.", "",
 "## 1. الحالة حسب المجال — BASELINE (89c2c31) / CURRENT (fa40270)", "",
 "| المجال | " + " | ".join(STAT_AR[s] for s in SORD) + " | المجموع |", "|---|" + "---|"*(len(SORD)+1)]
for b in ORDER:
    rs = [r for r in net if r['bucket']==b]
    cb = cnt(rs, lambda r: st(r['status_baseline'])); cc = cnt(rs, lambda r: st(r['status_current']))
    g.append(f"| {BNAME[b]} | " + " | ".join(f"{cb[s]} / {cc[s]}" for s in SORD) + f" | {len(rs)} |")
g.append("| **المجموع** | " + " | ".join(f"**{C['B'][s]} / {C['Cc'][s]}**" for s in SORD) + f" | **{C['net']}** |")
g += ["", "## 2. الحالة حسب التصنيف (CURRENT)", "", "| التصنيف | " + " | ".join(STAT_AR[s] for s in SORD) + " |", "|---|" + "---|"*len(SORD)]
for k, v in CLS.items():
    rs = [r for r in net if r['class']==k]; cc = cnt(rs, lambda r: st(r['status_current']))
    g.append(f"| {v} ({len(rs)}) | " + " | ".join(str(cc[s]) for s in SORD) + " |")
g += ["", "## 3. الفجوة حسب الأولوية (CURRENT غير منفذ/جزئي/مُخالَف)", "", "| الأولوية | غير منفذ | جزئي | مُخالَف | لم يُتحقق | منفذ |", "|---|---|---|---|---|---|"]
for p in ["P1","P2","P3","P4"]:
    rs = [r for r in net if r['priority']==p]; cc = cnt(rs, lambda r: st(r['status_current']))
    g.append(f"| {p} ({len(rs)}) | {cc['NOT_IMPLEMENTED']} | {cc['PARTIAL']} | {cc['CONTRADICTED']} | {cc['NOT_VERIFIED']} | {cc['IMPLEMENTED']} |")
moves = collections.Counter()
rank = {"NOT_IMPLEMENTED":0,"CONTRADICTED":0,"PARTIAL":1,"IMPLEMENTED":2}
chg = []
for r in net:
    a, c = st(r['status_baseline']), st(r['status_current'])
    if a in rank and c in rank and a != c:
        k = 'تحسّن في CURRENT' if rank[c] > rank[a] else ('تراجع في CURRENT' if rank[c] < rank[a] else 'تغيّر')
        if a=='PARTIAL' and c=='CONTRADICTED': k='تراجع في CURRENT'
        moves[k] += 1; chg.append((k, r))
g += ["", "## 4. ما يتغير بين النسختين", "", f"تحسّن في CURRENT: **{moves['تحسّن في CURRENT']}** · تراجع في CURRENT: **{moves['تراجع في CURRENT']}** · بقية المتطلبات بنفس الحالة.", "",
 "| ID | المتطلب | B | C | الاتجاه |", "|---|---|---|---|---|"]
for k, r in sorted(chg, key=lambda x: (x[0], x[1]['req_id'])):
    g.append(f"| {r['req_id']} | {short(r['title_ar'],100)} | {STAT_AR[st(r['status_baseline'])]} | {STAT_AR[st(r['status_current'])]} | {k} |")
g += ["", "## 5. فجوات P1 (كل المتطلبات ذات الأولوية الأولى غير المكتملة في CURRENT)", "", "| ID | المجال | المتطلب | B | C | الفجوة | الأثر |", "|---|---|---|---|---|---|---|"]
for r in sorted([r for r in net if r['priority']=='P1' and st(r['status_current'])!='IMPLEMENTED'], key=lambda r:(ORDER.index(r['bucket']), r['req_id'])):
    g.append(f"| {r['req_id']} | {r['bucket']} | {short(r['title_ar'],90)} | {STAT_AR[st(r['status_baseline'])]} | {STAT_AR[st(r['status_current'])]} | {short(r['gap_ar'],160)} | {short(r['impact_ar'],100)} |")
open(f'{OUT}/22-Gap-Matrix.md','w').write('\n'.join(g))

# ================= 23 Traceability =================
DARt = {d[0]: d[1] for d in DAR}
t = ["# 23 — مصفوفة التتبع (Traceability Matrix)", "",
 "السلسلة المطلوبة: **Business Requirement → Process/Control → Data Requirement → Architecture Recommendation → Acceptance Criterion**، مع أعمدة الأدلة UI/API/Service/Schema/Events/Tests في `traceability-matrix.csv`.", "",
 "**تنبيه منهجي:** ربط المتطلب بالتوصية المعمارية (DAR) **مقترح آليًا** من نص «متطلب البيانات» وعنوان المتطلب ومجاله، ثم يُراجع في جلسة الاعتماد؛ المتطلبات التطبيقية البحتة (واجهة، صلاحية تطبيقية) قد لا ترتبط بأي DAR. تعريف كل DAR في `30-Data-Architecture-Recommendations.md`.", "",
 "## 1. ملخص: كم متطلبًا يعتمد على كل توصية معمارية", "", "| DAR | التوصية | عدد المتطلبات | منها P1 |", "|---|---|---|---|"]
for did, title, *_ in DAR:
    rs = [r for r in net if did in r['dar']]
    t.append(f"| {did} | {short(title,120)} | {len(rs)} | {sum(1 for r in rs if r['priority']=='P1')} |")
t.append(f"| — | بلا أثر على تصميم البيانات | {sum(1 for r in net if not r['dar'])} | {sum(1 for r in net if not r['dar'] and r['priority']=='P1')} |")
t += ["", "## 2. السلسلة لكل متطلب", ""]
for b in ORDER:
    t += [f"### {BNAME[b]}", "", "| BR | العملية / الضابط | متطلب البيانات | التوصية | معيار القبول (الأول) |", "|---|---|---|---|---|"]
    for r in [r for r in net if r['bucket']==b]:
        ctrl = esc(r.get('process')) + (" · " + short(r.get('approvals_sod'),70) if r.get('approvals_sod') and r.get('approvals_sod') not in ('—','-') else '') + (" · " + ', '.join(r['business_rules'][:3]) if r['business_rules'] else '')
        t.append(f"| {r['req_id']} | {short(ctrl,150)} | {short(r.get('data_requirement_ar'),150)} | {', '.join(r['dar']) or '—'} | {short(r['acceptance_criteria'][0] if r['acceptance_criteria'] else '',150)} |")
    t.append("")
open(f'{OUT}/23-Traceability-Matrix.md','w').write('\n'.join(t))
with open(f'{OUT}/traceability-matrix.csv','w',newline='',encoding='utf-8-sig') as fh:
    w = csv.writer(fh); w.writerow(['req_id','title_ar','process','approvals_sod','business_rules','ui','api','service','schema','events','tests','data_requirement_ar','dar','dar_titles','acceptance_criteria','status_baseline','status_current','priority'])
    for r in net:
        ev = r.get('evidence') or {}
        w.writerow([r['req_id'], r['title_ar'], r.get('process'), r.get('approvals_sod'), ' | '.join(r['business_rules']), ev.get('ui'), ev.get('api'), ev.get('service'), ev.get('schema'), ev.get('events'), ev.get('tests'), r.get('data_requirement_ar'), ' | '.join(r['dar']), ' | '.join(DARt[d] for d in r['dar']), ' | '.join(r['acceptance_criteria']), r['status_baseline'], r['status_current'], r['priority']])

# ================= 24 Rules =================
RT = {"DECIDED":"مقرر من المالك","DOCUMENTED":"موثق","INFERRED":"مستنتج","CONFLICTING":"متعارض"}
ru = ["# 24 — كتالوج قواعد الأعمال (Business Rules Catalogue)", "",
 f"**{C['rules']} قاعدة** — " + " · ".join(f"{RT.get(k,k)}: {v}" for k, v in C['rtype'].items()) + ". لكل قاعدة: مصدرها (sid)، وأين تُفرض في BASELINE وCURRENT (`path:line` أو «غير مفروضة»)، والمتطلبات المرتبطة. الجدول الكامل في `business-rules.csv`.", ""]
for b in ORDER:
    rs = [x for x in rules if x['bucket']==b]
    ru += [f"## {BNAME[b]} ({len(rs)})", "", "| ID | القاعدة | النوع | فرض B | فرض C | المتطلبات |", "|---|---|---|---|---|---|"]
    for x in rs:
        ru.append(f"| {x['br_id']} | {short(x['rule_ar'],200)} | {RT.get(x.get('type',''),x.get('type',''))} | {short(x.get('enforced_baseline'),90)} | {short(x.get('enforced_current'),90)} | {', '.join(x.get('req_ids',[])[:5])} |")
    ru.append("")
open(f'{OUT}/24-Business-Rules-Catalogue.md','w').write('\n'.join(ru))
with open(f'{OUT}/business-rules.csv','w',newline='',encoding='utf-8-sig') as fh:
    w = csv.writer(fh); w.writerow(['br_id','bucket','rule_ar','type','source_sids','enforced_baseline','enforced_current','req_ids'])
    for x in rules: w.writerow([x['br_id'], x['bucket'], x['rule_ar'], x.get('type'), ' | '.join(x.get('source_sids', x.get('source_raw', [])) or []), x.get('enforced_baseline'), x.get('enforced_current'), ' | '.join(x.get('req_ids',[]))])

# ================= 25 Decisions =================
de = ["# 25 — القرارات المتعارضة والمفتوحة", "",
 f"**{C['decs']} قرارًا** داخل المجالات ({C['dkind']['CONFLICT']} تعارضًا، {C['dkind']['OPEN']} مفتوحًا؛ **{C['block']} يمنع** التقدم في متطلبات أخرى) + **{C['xconf']} تعارضًا عابرًا للمجالات** اكتُشف عند مقارنة السجلات.", "",
 "## 1. تعارضات عابرة للمجالات", "", "| XC | المتطلبات | وصف التعارض |", "|---|---|---|"]
for i, x in enumerate(xconf, 1):
    de.append(f"| XC-{i:02d} | {', '.join(x['ids'])} | {esc(x['reason_ar'])} |")
de += ["", "## 2. القرارات المانعة أولًا", "", "| ID | النوع | القرار المطلوب | الخيارات | سلوك الكود الحالي | المتطلبات المتأثرة |", "|---|---|---|---|---|---|"]
for d in [d for d in decs if d.get('blocking')]:
    de.append(f"| {d['dec_id']} | {'تعارض' if d['kind']=='CONFLICT' else 'مفتوح'} | {short(d['title_ar'],120)} | {short(' / '.join(d.get('options_ar',[])),220)} | {short(d.get('current_code_behaviour_ar'),160)} | {', '.join(d.get('affected_reqs',[])[:5])} |")
de += ["", "## 3. كل القرارات حسب المجال", ""]
for b in ORDER:
    ds = [d for d in decs if d['bucket']==b]
    de += [f"### {BNAME[b]} ({len(ds)})", "", "| ID | النوع | مانع | العنوان | السؤال | المصادر |", "|---|---|---|---|---|---|"]
    for d in ds:
        de.append(f"| {d['dec_id']} | {'تعارض' if d['kind']=='CONFLICT' else 'مفتوح'} | {'نعم' if d.get('blocking') else ''} | {short(d['title_ar'],110)} | {short(d.get('question_ar') or d.get('recommended_question_ar'),180)} | {', '.join((d.get('sources') or [])[:4])} |")
    de.append("")
open(f'{OUT}/25-Decisions-Conflicts-and-Open.md','w').write('\n'.join(de))

# ================= 26 Acceptance criteria =================
ac = ["# 26 — معايير القبول (Acceptance Criteria)", "", f"**{C['ac']} معيارًا** بصيغة «بافتراض… عندما… فإن…» لـ{C['net']} متطلبًا صافيًا. كل معيار قابل للاختبار ومرتبط بمتطلبه. المعايير التي تعتمد على قرار مفتوح تُعتمد بعد حسمه (انظر عمود القرارات في السجل).", ""]
for b in ORDER:
    ac += [f"## {BNAME[b]}", ""]
    for r in [r for r in net if r['bucket']==b]:
        ac.append(f"**{r['req_id']} — {esc(r['title_ar'])}** ({r['priority']}" + (f"؛ يعتمد على {', '.join(r['decision_refs'][:3])}" if r['decision_refs'] else '') + ")")
        ac += [f"- {esc(a)}" for a in r['acceptance_criteria']]
        ac.append("")
open(f'{OUT}/26-Acceptance-Criteria.md','w').write('\n'.join(ac))

# ================= questions =================
q = ["# 28 — أسئلة مالك النظام (مجموعات صغيرة)", "",
 "الأسئلة مرتبة حسب العملية، وكل مجموعة 3–6 أسئلة، وكل سؤال يشير إلى القرار (DEC) أو المتطلب (REQ) الذي يحسمه. **ابدأ بقسم «الأولوية القصوى»** لأنها تمنع التقدم في متطلبات أخرى.", "",
 "## الأولوية القصوى — قرارات مانعة (إجابة واحدة لكل منها)", ""]
for i, d in enumerate([d for d in decs if d.get('blocking')], 1):
    q.append(f"{i}. **{d['dec_id']}** — {esc(d.get('question_ar') or d['title_ar'])}")
q.append("")
for b in ORDER:
    p = f'{BASE}/req/c2/{b}.questions.md'
    if os.path.exists(p):
        body = open(p).read().split('\n')
        body = [l for l in body if not l.startswith('# ')]
        q += [f"# {BNAME[b]}", ""] + [re.sub(r'^## ', '### ', l) for l in body] + [""]
open(f'{OUT}/28-Owner-Questions.md','w').write('\n'.join(q))

# ================= process doc =================
pr = ["# 29 — العمليات من البداية للنهاية: As-Is ثم To-Be المقترح", "",
 "لكل عملية: الوضع كما هو مبرمج + الخطوات اليدوية المعروفة من ملفات الشركة (وما لم تُعرف ممارسته مكتوب كـ**سؤال** لا كغياب)، ثم To-Be مقترح للمناقشة مع القرارات التي يعتمد عليها. الرسوم مصادرها Mermaid داخل النص؛ نسخ SVG في `diagrams/brga/`.", ""]
for b in ["C1","C2","C3","C4","C5","C6","C7","C10"]:
    p = f'{BASE}/req/c2/{b}.process.md'
    body = open(p).read()
    body = re.sub(r'^# ', '## ', body, flags=re.M) if body.startswith('# ') else body
    pr += [f"---", "", body, ""]
open(f'{OUT}/29-E2E-Processes-As-Is-To-Be.md','w').write('\n'.join(pr))
print(json.dumps({k:(dict(v) if isinstance(v, collections.Counter) else v) for k,v in C.items()}, ensure_ascii=False))
