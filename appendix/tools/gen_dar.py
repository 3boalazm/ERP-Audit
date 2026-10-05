#!/usr/bin/env python3
import sys, io, contextlib, re, json
sys.path.insert(0, '/home/claude/audit/tools')
with contextlib.redirect_stdout(io.StringIO()):
    from gen_brga import net, DAR
B = '/home/claude/audit'
t = open(f'{B}/req/final/doc30.tmpl.md').read()
def reqs_for(d):
    rs = [r for r in net if d in r['dar']]
    p1 = [r['req_id'] for r in rs if r['priority'] == 'P1']
    return rs, p1
def cell(d):
    rs, p1 = reqs_for(d)
    return f"{len(rs)} متطلبًا؛ P1: " + (', '.join(p1[:6]) + (f" … (+{len(p1)-6})" if len(p1) > 6 else '') if p1 else '—')
t = re.sub(r'\{REQS:(DAR-\d+)\}', lambda m: cell(m.group(1)), t)
PROB = {"DAR-01":"كل المشكلات (سياق)","DAR-02":"P-14","DAR-03":"P-04, P-07","DAR-04":"P-01","DAR-05":"P-02","DAR-06":"P-05","DAR-07":"P-06","DAR-08":"P-07, P-02","DAR-09":"P-08","DAR-10":"P-09","DAR-11":"P-10","DAR-12":"P-11","DAR-13":"P-12","DAR-14":"P-13","DAR-15":"P-14","DAR-16":"P-15","DAR-17":"P-05, P-12","DAR-18":"P-16","DAR-19":"P-03","DAR-20":"P-17"}
AC = {
"DAR-01":"بافتراض اعتماد A1، عندما تُراجع أي توصية لاحقة، فإنها لا تتطلب FK أو معاملة عابرة بين القواعد.",
"DAR-02":"عندما يُتخذ قرار الاستضافة، فإنه موثق بـRPO/RTO والتكلفة ويُثبت باختبار استعادة قبل النقل.",
"DAR-03":"عندما يُرسل استلام أو طلب أو ربط موظف بمرجع غير موجود أو غير نشط في نظام السجل، فإن الكتابة تُرفض ولا تُكتب قيمة بديلة؛ وتقرير المراجع اليتيمة = 0.",
"DAR-04":"بافتراض أي مستند مالي مرحّل، عندما يُستعلم عن قيوده، فإن هناك قيدًا واحدًا متوازنًا في شكل جدول واحد بفترة مفتوحة، والميزان من GL = مجموع القيود.",
"DAR-05":"لكل دفتر فرعي، عندما تُشغّل التسوية في نهاية اليوم، فإن رصيده = رصيد الحساب الرقابي في GL، وكل حركة خزينة/COGS/رواتب/مصروفات/حوافز لها قيد بمصدرها.",
"DAR-06":"عندما تُحاول أي عملية جعل رصيد مخزون سالبًا أو عكس حركة مرتين أو إهلاك أصل مرتين في الفترة، فإن القاعدة ترفضها حتى لو تجاوزت طبقة التطبيق.",
"DAR-07":"عندما تنهار الخدمة بعد commit وقبل النشر، أو يُعاد تسليم حدث، فإن الحدث يُنشر لاحقًا مرة واحدة على الأقل ويُطبق أثره مرة واحدة فقط.",
"DAR-08":"عندما تُشغّل التسويات اليومية، فإن كل فرق يُسجل كـbreak بمالك وحالة، ولا تبقى فروق مفتوحة أكثر من المدة المعتمدة.",
"DAR-09":"عندما يُطلب انتقال حالة غير مسموح أو ترحيل في فترة مقفلة، فإنه يُرفض؛ والتصحيح لا يتم إلا بمستند عكسي مرتبط.",
"DAR-10":"لكل مستند مالي، عملة صريحة ودقة موحدة؛ وعند إعادة الحساب بالقاعدة المعتمدة لا يظهر فرق قرش بين المستند والقيد والإقرار؛ وأرقام الفواتير متسلسلة بلا فجوات لكل سنة.",
"DAR-11":"بافتراض تشغيلة مستدعاة، عندما يُطلب تتبعها، فإن كل العملاء والكميات والمستندات تُستخرج من الجداول دون الاعتماد على حدث.",
"DAR-12":"عندما يُعدّل كيان حساس، فإن سجل التعديل يُكتب في نفس المعاملة مخفيًا للحقول الحساسة، ولا يستطيع دور التطبيق تعديله أو حذفه.",
"DAR-13":"عندما يُطلب تقرير أو لوحة، فإن الأرقام تُحسب في القاعدة بلا قص صامت، وتطابق GL للقوائم المالية.",
"DAR-14":"عندما يُنشر إصدار، فإن checksums للترحيلات تطابق الإنتاج، والإصدار N يعمل على schema N وN+1، ولا توجد migration مطبقة مُعدّلة.",
"DAR-15":"عندما يُنفذ تمرين الاستعادة الربعي، فإن RPO وRTO المقاسين ضمن الأهداف المعتمدة، والأرصدة المرجعية تطابق بعد الاستعادة.",
"DAR-16":"عندما تتصل خدمة بقاعدة غير قاعدتها أو تنفذ DDL أو تعدّل التدقيق، فإن الطلب يُرفض من القاعدة.",
"DAR-17":"لكل فهرس مقترح X6–X14، يوجد قياس قبل/بعد يثبت التحسن، ولا يُضاف فهرس دون قياس.",
"DAR-18":"لكل فئة بيانات حساسة، سياسة احتفاظ معتمدة تُطبق آليًا، ولا تظهر القيم الحساسة في السجلات.",
"DAR-19":"عند أي حركة إصدار أو عكسها، فإن طبقات التكلفة تُستهلك/تُعاد، وقيمة المخزون في inventory = حساب المخزون في GL.",
"DAR-20":"قبل أول عملية حية، الحزمة الافتتاحية موقعة بـhash ومرحّلة، وكل دفتر فرعي = حسابه الرقابي بتاريخ القطع.",
}
rows = []
for did, title, adr, fnd, _ in DAR:
    rs, p1 = reqs_for(did)
    rows.append(f"| {did} | {title} | {PROB[did]} — {', '.join(fnd)} | {adr} | {len(rs)} ({len(p1)}) | {AC[did]} |")
t = t.replace('{DAR_TABLE}', '\n'.join(rows))
IDX = """| # | القاعدة.الجدول | الأعمدة | نمط الاستعلام `[C]` | السبب | الشرط |
|---|---|---|---|---|---|
| X1 | `nile_inventory.inventory_transactions` | `UNIQUE (reversal_of_id) WHERE reversal_of_id IS NOT NULL` | `transactions.service.ts:387-399` | منع العكس المزدوج | **قيد صحة**؛ عدّ التكرارات أولًا (E-40) |
| X2 | `nile_inventory` (عمود مطالبة جديد) | `UNIQUE (idempotency_key)` | `allocation.engine.ts:322-333, 583-591` | صرف مباشر idempotent في القاعدة؛ يغني عن فهرس `note` | **قيد صحة** |
| X3 | `nile_accounting.depreciation_entries` | `UNIQUE (asset_id, fiscal_year, period_month)` | `fixed-assets.service.ts:120-121` | إهلاك واحد لكل فترة | **قيد صحة**؛ عدّ التكرارات أولًا |
| X4 | `nile_accounting.journal_entries` | إبقاء **أحد** مفتاحي المصدر | `general-ledger.service.ts:34, 41-48` | دلالتا إعادة ترحيل متعارضتان | **قرار أعمال** ثم DDL |
| ~~X5~~ | `import_shipments`, `journal_entry_workflows` | ~~`UNIQUE(shipment_number)`, `UNIQUE(entry_number)`~~ | — | **مسحوب:** القيدان موجودان inline في SQL (`20260928140000_import_shipments/migration.sql:3`، `20260928150000_manual_journal_workflow/migration.sql:3`) وفي Prisma؛ ظهورهما «ناقصين» كان من مخرجات أداة المقارنة | — |
| X6 | `nile_sales.sales_orders` | `(created_at)` أو `(rep_id, created_at)` | `orders.service.ts:262-264, 273-274` | نطاقات اللوحة والتقارير | EXPLAIN/`pg_stat_statements` |
| X7 | `nile_sales.sales_returns` | `(created_at)` | `returns.service.ts:463-466` | تجميع اللوحة | مشروط بالقياس |
| X8 | `nile_inventory.stock_balances` | `(batch_id, ownership)` | `allocation.engine.ts:112`؛ `quarantine.service.ts:52` | بحث بالتشغيلة (استدعاء/مستهلك أحداث) | مشروط بالقياس |
| X9 | `nile_inventory.consignment_stock` | `(batch_id)` | `allocation.engine.ts:113` | مثل X8 | مشروط بالقياس |
| X10 | `nile_inventory.inventory_reservations` | `(batch_id) WHERE is_released=false`؛ `(created_at) WHERE is_released=false AND issued_at IS NULL` | `quarantine.service.ts:80`؛ `inventory-jobs.ts:120-124` | الاستدعاء ومسح الحجوزات القديمة | مشروط بالقياس |
| X11 | `nile_sales.order_sagas` | `(step, updated_at)` | `saga-monitor.service.ts:24-30` | مراقبة الـsaga المتوقفة | مشروط بالقياس |
| X12 | `nile_iam.sessions` | `(refresh_token_hash) WHERE is_active` (+ previous) | `auth.service.ts:437-440` | الخروج والتجديد | مشروط بالقياس + سياسة تنظيف الجلسات |
| X13 | `nile_iam.user_roles` | `(role_id)` | `roles.service.ts:113` | عمود FK بلا فهرس | مشروط بالقياس (رخيص) |
| X14 | عدة قواعد | `pg_trgm` GIN لأكثر 2–3 أعمدة بحثًا | `orders.service.ts:113`؛ `invoices.service.ts:411` | `ILIKE '%x%'` | فقط إن أظهره `pg_stat_statements` |
| X15 | `nile_accounting` | حذف الفهارس المكررة على `journal_lines`/`journal_entries` | — | تضخيم الكتابة | بعد فحص `idx_scan` وتعديل `schema.prisma` معًا |"""
t = t.replace('{INDEX_TABLE}', IDX)
open(f'{B}/pkg/30-Data-Architecture-Recommendations.md', 'w').write(t)
print('ok', len(t))
