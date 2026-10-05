#!/usr/bin/env python3
# Rebuilds the single-file HTML viewer from pkg/*.md (keeps original CSS/JS shell).
import re, os, base64, subprocess, html
B = '/home/claude/audit'; P = f'{B}/pkg'
old = open(f'{B}/Nile-Pharma-Audit.html').read()
head = old[:old.index('<header class="top">')]
script = old[old.rindex('<script>'):]
# extra CSS: group labels in nav
head = head.replace('</style>', 'nav.idx .grp{font-family:var(--f-mono);font-size:11px;letter-spacing:.06em;color:var(--muted);padding:14px 10px 4px}\nnav.idx a.sub{padding-inline-start:22px;font-size:13px}\n</style>', 1)
head = head.replace('<title>Nile Pharma ERP As-Is Audit</title>', '<title>Nile Pharma ERP Audit</title>')
DOCS = [("PART 1 · AS-IS", None, None),
 ("01","01-Executive-Summary-AR.md","الملخص التنفيذي"),("02","02-Full-As-Is-Audit-Report.md","التقرير الكامل"),
 ("03","03-System-Inventory-and-Architecture.md","الجرد والمعمارية"),("04","04-How-the-System-Runs.md","كيف يعمل النظام"),
 ("05","05-API-Inventory-and-Routing.md","جرد الـAPI والتوجيه"),("06","06-ERD-and-Data-Model.md","نموذج البيانات وERDs"),
 ("07","07-Data-Dictionary.md","قاموس البيانات"),("08","08-Business-Process-Catalogue.md","كتالوج العمليات"),
 ("09","09-Schema-Gap-Analysis.md","فجوات الـSchema"),("10","10-Business-and-Process-Gap-Analysis.md","فجوات الأعمال والعمليات"),
 ("11","11-Deployment-and-Operations.md","النشر والتشغيل"),("12","12-Findings-Register.md","سجل النتائج"),
 ("13","13-Evidence-Requests-and-Open-Questions.md","طلبات الأدلة والأسئلة"),("14","14-Recommendations-for-Discussion.md","توصيات للمناقشة"),
 ("15","15-Coverage-Matrix.md","مصفوفة التغطية"),("16","16-Prior-Findings-Reassessment.md","إعادة تقييم التقرير السابق"),
 ("PART 2 · REQUIREMENTS & DATA", None, None),
 ("20","20-BRGA-Overview.md","المنهج والأرقام"),("21","21-Requirements-Register.md","سجل المتطلبات"),
]
CARDS = [("C1","Order-to-Cash"),("C2","العملاء والميدان"),("C3","Procure-to-Pay"),("C4","المخزون والجودة"),("C5","Record-to-Report"),
 ("C6","الخزينة والائتمان"),("C7","الحوافز وHR"),("C8","الهوية والموافقات"),("C9","غير الوظيفية"),("C10","التشغيل وترحيل البيانات")]
for c, n in CARDS: DOCS.append((f"r{c[1:]}", f"register/{c}.md", f"بطاقات {c}: {n}", ))
DOCS += [("22","22-Gap-Matrix.md","مصفوفة الفجوات"),("23","23-Traceability-Matrix.md","مصفوفة التتبع"),("24","24-Business-Rules-Catalogue.md","قواعد الأعمال"),
 ("25","25-Decisions-Conflicts-and-Open.md","القرارات والتعارضات"),("26","26-Acceptance-Criteria.md","معايير القبول"),("27","27-Priority-Map.md","خريطة الأولويات"),
 ("28","28-Owner-Questions.md","أسئلة المالك"),("29","29-E2E-Processes-As-Is-To-Be.md","العمليات As-Is / To-Be"),
 ("30","30-Data-Architecture-Recommendations.md","توصيات معمارية البيانات"),("31","31-ADRs.md","قرارات معمارية (ADRs)"),
 ("32","32-Transition-Plan.md","خطة الانتقال"),("33","33-Evidence-and-Decisions-Before-Design-Approval.md","الأدلة والقرارات قبل الاعتماد"),
 ("34","34-Errata.md","تصحيحات")]
img_cache = {}
def inline(m, base):
    src = m.group(2)
    path = os.path.normpath(os.path.join(base, src))
    if not os.path.exists(path): return m.group(0)
    if path not in img_cache:
        mime = 'image/svg+xml' if path.endswith('.svg') else 'image/png'
        img_cache[path] = f'data:{mime};base64,' + base64.b64encode(open(path,'rb').read()).decode()
    return f'{m.group(1)}{img_cache[path]}{m.group(3)}'
nav, secs = [], []
first = True
for k, f, t in DOCS:
    if f is None:
        nav.append(f'<div class="grp">{k}</div>'); continue
    cls = ' class="sub"' if k.startswith('r') else ''
    label = k if not k.startswith('r') else '·'
    nav.append(f'<a href="#d{k}" data-k="{k}"{cls}><span class="n">{label}</span><span>{html.escape(t)}</span></a>')
    md = open(f'{P}/{f}').read()
    # escape stray '<' outside code (e.g. <svc>_owner) so raw-HTML passthrough cannot unbalance the page
    parts = re.split(r'(```.*?```|`[^`\n]*`)', md, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'<(?!/?(?:sub|sup|br|details|summary)\b)', '&lt;', parts[i])
    md = ''.join(parts)
    h = subprocess.run(['pandoc', '-f', 'gfm', '-t', 'html5', '--wrap=none'], input=md, capture_output=True, text=True, check=True).stdout
    base = os.path.dirname(f'{P}/{f}')
    h = re.sub(r'(<img[^>]*src=")([^"]+)(")', lambda m: inline(m, base), h)
    h = h.replace('<img ', '<img loading="lazy" ')
    h = re.sub(r'<table', '<div class="tw"><table', h); h = h.replace('</table>', '</table></div>')
    secs.append(f'<section class="doc" id="d{k}" data-k="{k}"{"" if first else " hidden"}>{h}</section>')
    first = False
header = ('<header class="top"><div class="eyebrow">NILE PHARMA ERP · 89c2c31 / fa40270 · 2026-10-01 / 2026-10-04</div>'
 '<h1>مراجعة Nile Pharma ERP: الحالة الراهنة، فجوات المتطلبات، ومعمارية البيانات</h1>'
 '<p>الجزء الأول: 127 نتيجة، 18 مانعًا لنشر النسخة الأحدث. الجزء الثاني: 485 متطلبًا صافيًا، 194 قرارًا (75 مانعًا)، 20 توصية معمارية — للمناقشة والاعتماد قبل أي تنفيذ.</p></header>\n<div class="wrap">')
out = head + header + '<nav class="idx" aria-label="مستندات الحزمة">' + ''.join(nav) + '</nav><main>' + '\n'.join(secs) + \
      '<div class="pager"><button type="button" id="prev">→ السابق</button><button type="button" id="next">التالي ←</button></div></main></div>\n' + script
# link handler: also map "register/Cn.md" and NN- links
out = out.replace("var m=(a.getAttribute('href')||'').match(/^(\\d\\d)-/);if(m&&keys.indexOf(m[1])>=0)",
                  "var hr=a.getAttribute('href')||'',m=hr.match(/^(\\d\\d)-/)||hr.match(/^register\\/C(\\d+)\\.md/);if(m&&m[0].indexOf('register')===0)m[1]='r'+m[1];if(m&&keys.indexOf(m[1])>=0)")
open(f'{B}/Nile-Pharma-Audit.html', 'w').write(out)
print(len(out)/1e6, 'MB', len(secs), 'sections', len(img_cache), 'images')
