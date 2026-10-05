# 09 — تحليل فجوات الـSchema (Schema Gap Analysis)

> **مبدأ:** هذا تحليل للـschema **كما يصفه الكود والـmigrations**. لا أصنّف أي drift في القاعدة الفعلية دون مخرجات DB؛ البنود المعتمدة على ملاحظات المستخدم موسومة `[U]` وتنتظر E-03/E-04.
> **المصادر:** `data/schema_cur.json`, `data/schema_base.json`, `appendix/schema-stats-and-heuristic-gaps.md`، تشغيل `validate-schema-migrations.cjs` الساكن، قراءة ملفات SQL.

## 1. ملخص الفجوات حسب المحور

| المحور | الوضع | التصنيف | Findings |
|---|---|---|---|
| علاقات ناقصة (عبر الخدمات) | 217 مرجعًا منطقيًا بلا FK (متوقع في النمط) بلا أداة مطابقة | Verified | DB-04 |
| علاقات ناقصة (داخل الخدمة) | نادرة؛ أبرزها `bank_statement_lines` بلا FK للخزينة، `supplier_payments` v2 بلا FKs | Verified | DB-03 |
| Constraints | لا CHECK على أرصدة المخزون؛ CHECKs موجودة على cost layers وقيود GL (legacy) | Verified | DB-05 |
| Indexes | 23 عمود FK بلا فهرس (heuristic)؛ فهارس كثيرة أصلًا (175 index في accounting حسب `[U]`) | Verified (heuristic) | DB-06 |
| أنواع البيانات والدقة المالية | **جيدة**: كل المبالغ Decimal بدقة صريحة؛ scales مختلفة (14,2 للمستندات، 18,4 لتكلفة المخزون، 18,2 للبنوك، 16,6 لسعر الصرف) | Verified | DB-12 |
| Audit fields | 92/175 model فيه `createdAt`؛ أغلب البقية يستخدم تواريخ مجال (`issuedAt`…) و26 model بلا أي DateTime (سطور غالبًا)؛ `createdById`/`updatedBy` غير موحد | Verified | DB-06 |
| Lifecycle/status | 7 حقول status نصية حرة؛ enum حالات غير مستخدمة (`SagaStep.PAID/COMPENSATING`)؛ انتقالات غير محمية بشروط في DB (التحقق في التطبيق) | Verified | DB-06, ORG-01/02 |
| Soft deletion | أرشفة عبر `isActive`/`archivedAt` في 27 model؛ لا `deletedAt` موحد؛ حذف فعلي للـbins (C) | Verified | — |
| Migration compatibility | B→C إضافي من منظور Prisma؛ لكن migrations المحاسبة عُدّلت بعد التطبيق، وشكلان متنافسان للجداول، و`gl_workbench` "reviewed-destructive" | Verified (git) / Inferred (DB) | DB-01, DB-02, DB-03 |
| Prisma ↔ SQL | 22 بندًا في accounting (14 حقيقية + 8 غالبًا false positives) | Verified (tool) | DB-02, DB-07 |
| سلامة البيانات المحتملة | أطراف `'unknown'`، فواتير مورد `base_total=0`، أرصدة سالبة ممكنة نظريًا | Inferred | DB-04, DB-05, DB-08 |
| Actual DB drift | **Unknown** | — | ARC-02 |

## 2. تفاصيل حسب المجال

### 2.1 Accounting
1. **جداول GL (C):** migration `general_ledger` ينشئ شكل legacy (`entry_number`, `entry_date`, `created_by_id`, `line_no` NOT NULL بلا defaults، status TEXT + CHECK، unique جزئي على المصدر حين POSTED)، ثم `gl_workbench` يحوّل status إلى enum ويضيف `journal_number`/`created_by` ويجعلها NOT NULL، ويضيف unique **غير جزئي** على `(source_type, source_id)`. Prisma يمثل شكل workbench فقط. النتيجة: لا كاتب في الكود يملأ كل الأعمدة الإلزامية للشكلين معًا (ACC-02).
2. **`supplier_payments`:** v1 (FK لفاتورة المورد، `amount`, `exchange_rate`, `base_amount`) مقابل v2 (`supplier_invoice_id`, `amount_fx`, `fx_rate`, `amount_egp`, بلا FKs). إن نُفذ v1 فعلًا، فإن index v2 على `paid_at` يفشل → الأرجح أن الجدول بشكل v2 (Inferred) — وهو ما يكسر تنفيذ A.
3. **أبعاد تحليلية:** `branch_id, cost_center_id, profit_center_id, party_id, tax_code` في SQL وغير ممثلة في Prisma.
4. **`chart_of_accounts.balance`:** رصيد مخزن (denormalized) لا يُحدَّث في B إلا عند إقفال السنة؛ C يحاول تحديث جدول `accounts` غير الموجود.
5. **`depreciation_entries`:** لا unique على (asset, year, month) في B (ACC-13)؛ C يضيف حارسًا في الكود.
6. **`invoices.invoice_number`:** unique لكن مولّد من الوقت (DB-10).
7. **`ledger_entries`:** دفتر العميل يخزن `account_id` (عميل CRM) — وفي C يُخلط معه COA ids عبر `JOURNAL_LINE` (ACC-02).

### 2.2 Inventory
- `stock_balances(warehouse_id, batch_id, ownership)` فريد؛ لا CHECK لـ`on_hand >= 0`, `reserved >= 0`, `reserved <= on_hand` (DB-05).
- `inventory_reservations.order_id` فهرس غير فريد (يسمح بأكثر من حجز للطلب — مقصود لكل سطر).
- `bin_locations` لا يرتبط بأي رصيد.
- `inventory_cost_layers` (C) فيه CHECK (الوحيد) لكنه بلا backfill للمخزون السابق.

### 2.3 Sales / CRM
- `sales_orders.idempotency_key` و`visit_id` فريدان (جيد).
- `account_credit` إسقاط محلي لحد CRM وAR المحاسبة دون تسوية دورية.
- `pricing_rules`, `price_rules`, `promotions` جداول إعداد غير مستخدمة في التسعير الفعلي (SAL-14).

### 2.4 IAM / Organization
- `users.mfa_enabled` عمود غير مقروء.
- `sessions.expires_at` ثابت 7 أيام في الكود.
- `employees.linked_user_id` nullable بلا تحقق؛ HR يستخدم مفتاحين مختلفين للشخص (ORG-05 في الملاحظات).
- `audit_logs` في كل خدمة قابلة للتعديل؛ trigger عدم التعديل موجود فقط في `nile_audit`.

## 3. مقارنة BASELINE ↔ CURRENT ↔ migrations (ملخص)

| الخدمة | Prisma B→C | Migrations B→C | Validator B / C | القاعدة الفعلية `[U]` |
|---|---|---|---|---|
| accounting | +13 models | 30 → 41 | ✅ / ❌ | 50 جدولًا = مستوى C؛ migrations حتى bank_reconciliation |
| organization | +1 | 5 → 6 | ✅ / ✅ | 26 = مستوى C |
| inventory | +2 | 16 → 19 | ✅ / ✅ | cost layers + outbox مذكورة = C |
| crm | حقول | 15 → 17 | ✅ / ✅ | 21 (متساوي في B وC — لا يميز) |
| sales, products, iam, incentives, audit | لا تغيير | لا تغيير | ✅ / ✅ | — |

## 4. فحوص سلامة بيانات مقترحة (قراءة فقط، للمناقشة)

كلها aggregates صغيرة داخل معاملة read-only مع `statement_timeout`؛ النص الكامل في `13-Evidence-Requests-and-Open-Questions.md` (E-12, E-13).
- أطراف وهمية: `count(*) FROM invoices WHERE account_id='unknown' OR total=0`.
- خزينة بعد العكس: `count(*) FROM payments WHERE reversed AND financial_account_id IS NOT NULL`.
- أرصدة مستحيلة: `count(*) FROM stock_balances WHERE on_hand<0 OR reserved<0 OR reserved>on_hand`.
- إهلاك مكرر: تجميع `depreciation_entries` حسب (asset, year, month) HAVING count>1.
- جداول CURRENT فارغة؟ `count(*)` من `journal_entries`, `supplier_payments`, `journal_entry_workflows`.

## 5. ما لا يمكن الحكم عليه الآن
- هل أعمدة الإنتاج تطابق أي نسخة من ملفات SQL (يحتاج checksums و`\d+`).
- هل توجد indexes/constraints أُضيفت يدويًا خارج migrations.
- أدوار قاعدة البيانات وصلاحياتها (هل كل خدمة بمستخدم مستقل أم `nile_admin` للجميع — `[U]` يشير لملكية `nile_admin`).
