import csv, collections, sys
sys.path.insert(0,'tools')
from findings_data import F
order={'Critical':0,'High':1,'Medium':2,'Low':3,'Info':4}
ids=[x['id'] for x in F]; assert len(ids)==len(set(ids)), [i for i in ids if ids.count(i)>1]
c=collections.Counter(x['severity'] for x in F)
bl=collections.Counter(x['baseline'].split(' ')[0] for x in F)
md=["# سجل النتائج الموحد (Findings Register)","",
"**المصدر:** تحليل ساكن للنسختين BASELINE `89c2c31` وCURRENT `fa40270` + مخرجات التشغيل المرفقة + ملاحظات المستخدم. لا يوجد أي اتصال بالسيرفر أو قاعدة البيانات.","",
"**مفتاح الدليل:** `[B]`=89c2c31، `[C]`=fa40270 (المسارات نسبية لجذر الـsnapshot)، `[R]`=مخرجات تشغيل خام في `evidence/`، `[U]`=ملاحظات تشغيل نقلها المستخدم دون مخرجات خام (NilePharma_Audit.docx). العمود **Release-blocker** = يمنع نشر CURRENT كما هو.","",
"**مقياس الخطورة:** Critical = توقف عمليات أساسية أو خسارة مالية مادية مؤكدة عند حدوث المحفز · High = خطر جوهري بمحفز واقعي في التشغيل العادي، أو فجوة رقابية مالية، أو مانع نشر · Medium = أثر محدود أو يحتاج ظرفًا خاصًا · Low = جودة/صيانة · Info = ملاحظة أو ضابط إيجابي.","",
"**تنبيه:** درجة الخطورة مبنية على الأثر المثبت أو المستنتج بوضوح من الكود، لا على الحجم المحتمل. النتائج المصنفة `Inferred` أو `Unknown` تحتاج دليل السيرفر المذكور قبل اعتبارها مؤكدة.","",
"## ملخص",f"إجمالي النتائج: **{len(F)}** — "+" · ".join(f"{k}: {c.get(k,0)}" for k in order),"",
f"Release-blockers لنسخة CURRENT: **{sum(1 for x in F if x['release_blocker'])}**","",
"| ID | العنوان | المجال | النسخة المتأثرة | التحقق | النوع | الخطورة | RB |","|---|---|---|---|---|---|---|---|"]
for x in sorted(F,key=lambda x:(order[x['severity']],x['id'])):
    md.append(f"| [{x['id']}](#{x['id'].lower()}) | {x['title']} | {x['domain']} | {x['baseline']} | {x['verification']} | {x['type']} | **{x['severity']}** | {'✔' if x['release_blocker'] else ''} |")
md+=["","## التفاصيل",""]
for x in sorted(F,key=lambda x:(x['id'][:3],x['id'])):
    md+=[f"### {x['id']}",f"**{x['title']}**","",
    f"- **المجال:** {x['domain']} · **النسخة المتأثرة:** {x['baseline']} · **درجة التحقق:** {x['verification']} · **النوع:** {x['type']}",
    f"- **الخطورة:** {x['severity']} — {x['justification']}" + (" · **مانع نشر لـCURRENT**" if x['release_blocker'] else ""),
    f"- **الدليل:** {x['evidence']}",
    f"- **المحفز (Trigger):** {x['trigger']}",
    f"- **الأثر:** {x['impact']}",
    f"- **للتحقق/الإغلاق:** {x['close']}",
    f"- **مرجع ملاحظات العمل:** {x['sources']}",""]
open('pkg/12-Findings-Register.md','w').write("\n".join(md))
with open('pkg/findings-register.csv','w',newline='',encoding='utf-8-sig') as fh:
    w=csv.writer(fh); keys=['id','title','domain','baseline','verification','type','severity','justification','evidence','trigger','impact','close','sources','release_blocker']
    w.writerow(keys)
    for x in sorted(F,key=lambda x:(order[x['severity']],x['id'])): w.writerow([x[k] for k in keys])
print(len(F), dict(c), sum(1 for x in F if x['release_blocker']))
print(collections.Counter(x['id'].split('-')[0] for x in F))
print([ (x['id'],x['severity']) for x in F if x['severity'] in ('Critical','High')])
