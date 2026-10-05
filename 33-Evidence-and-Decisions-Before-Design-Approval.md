# 33 — الأدلة الناقصة والقرارات المطلوبة قبل اعتماد التصميم

## 1. الأدلة الناقصة (قراءة فقط)

تكمل هذه الطلبات E-01…E-30 في `13` (لا تكرار). كلها تستخدم القالب `q` المعرّف في `13` §1: معاملة `BEGIN READ ONLY` مع `statement_timeout='5s'` و`lock_timeout='1s'` ثم `ROLLBACK`. **لا تُطبع أي بيانات أعمال**: أعداد ومعرّفات فنية فقط. لا تُرسل env أو كلمات مرور.

> قبل E-40…E-43: إن كانت أسماء الأعمدة في القاعدة الفعلية مختلفة عن الكود (DB-07)، شغّل أولًا E-44 وأرسل النتيجة؛ سنعدّل الاستعلام بدل التخمين.

| ID | الهدف | يدعم | الطلب | الحجم المتوقع |
|---|---|---|---|---|
| E-40 | عدّ المخالفات الحالية لكل قيد مقترح | ADR-05، T4 | الكتلة **E-40** أدناه | ~15 سطرًا (أعداد) |
| E-41 | المراجع اليتيمة والقيم البديلة | ADR-03 | الكتلة **E-41** | ~10 أسطر |
| E-42 | حالة GL الفعلية: هل توجد قيود، بأي شكل، ومتوازنة؟ | ADR-04 | الكتلة **E-42** | ~10 أسطر |
| E-43 | فرق تعرض الائتمان مقابل AR (أعداد فقط) | ADR-06 | الكتلة **E-43** | ~5 أسطر |
| E-44 | أعمدة الجداول المستهدفة كما في القاعدة | كل ما سبق | `q <db> "SELECT table_name, column_name, data_type, numeric_precision, numeric_scale, is_nullable FROM information_schema.columns WHERE table_schema='public' AND table_name IN ('stock_balances','inventory_transactions','consignment_stock','inventory_reservations','depreciation_entries','invoices','payments','journal_entries','journal_lines','sales_order_lines','account_credit','financial_accounts') ORDER BY 1,2;"` لكل من `nile_inventory`, `nile_accounting`, `nile_sales` | ~150 سطرًا |
| E-45 | القيود والفهارس الموجودة فعلًا | ADR-05، DAR-17 | `q <db> "SELECT conrelid::regclass, conname, contype, convalidated FROM pg_constraint WHERE connamespace='public'::regnamespace ORDER BY 1,2;"` و`q <db> "SELECT indexrelid::regclass, idx_scan, pg_size_pretty(pg_relation_size(indexrelid)) FROM pg_stat_user_indexes ORDER BY 1;"` لكل قاعدة | ~300 سطر |
| E-46 | أحجام الجداول وأعداد الصفوف التقديرية | ADR-10، DAR-17 | `q <db> "SELECT relname, n_live_tup, pg_size_pretty(pg_total_relation_size(relid)) FROM pg_stat_user_tables ORDER BY n_live_tup DESC LIMIT 25;"` لكل قاعدة | ~225 سطرًا |
| E-47 | هل `pg_stat_statements` مفعّل؟ | DAR-17 | `q postgres "SELECT name, setting FROM pg_settings WHERE name IN ('shared_preload_libraries','wal_level','archive_mode','archive_command','max_wal_senders','server_version');"` (قيمة `archive_command` قد تحوي مسارًا؛ أرسلها بعد إخفاء أي سر) | ~6 أسطر |
| E-48 | الامتدادات والمحفزات والدوال الفعلية | DAR-12، DAR-14 | `q <db> "SELECT extname, extversion FROM pg_extension;"` و`q <db> "SELECT tgrelid::regclass, tgname, tgenabled FROM pg_trigger WHERE NOT tgisinternal;"` لكل قاعدة | ~40 سطرًا |
| E-49 | صلاحيات الجداول على مستوى الأدوار | ADR-13 | `q <db> "SELECT grantee, privilege_type, count(*) FROM information_schema.role_table_grants WHERE table_schema='public' GROUP BY 1,2 ORDER BY 1,2;"` لكل قاعدة | ~50 سطرًا |

### الكتل

```sql
-- E-40 (nile_inventory)
SELECT 'neg_on_hand', count(*) FROM stock_balances WHERE on_hand < 0
UNION ALL SELECT 'reserved_gt_on_hand', count(*) FROM stock_balances WHERE reserved > on_hand OR reserved < 0
UNION ALL SELECT 'consign_negative', count(*) FROM consignment_stock WHERE owned_qty<0 OR available_qty<0 OR consumed_qty<0 OR returned_qty<0 OR lost_qty<0 OR held_qty<0
UNION ALL SELECT 'double_reversal', count(*) FROM (SELECT reversal_of_id FROM inventory_transactions WHERE reversal_of_id IS NOT NULL GROUP BY 1 HAVING count(*)>1) x
UNION ALL SELECT 'reservation_nonpositive', count(*) FROM inventory_reservations WHERE quantity <= 0;

-- E-40 (nile_accounting)
SELECT 'dup_depreciation', count(*) FROM (SELECT asset_id, fiscal_year, period_month FROM depreciation_entries GROUP BY 1,2,3 HAVING count(*)>1) x
UNION ALL SELECT 'invoice_over_settled', count(*) FROM invoices WHERE paid_amount + coalesce(credited_amount,0) > total + 0.005
UNION ALL SELECT 'invoice_negative', count(*) FROM invoices WHERE total < 0 OR paid_amount < 0
UNION ALL SELECT 'payment_nonpositive', count(*) FROM payments WHERE amount <= 0
UNION ALL SELECT 'cash_negative_balance', count(*) FROM financial_accounts WHERE balance < 0;

-- E-40 (nile_sales)
SELECT 'returned_gt_qty', count(*) FROM sales_order_lines WHERE returned_qty > quantity
UNION ALL SELECT 'qty_nonpositive', count(*) FROM sales_order_lines WHERE quantity <= 0
UNION ALL SELECT 'order_negative_total', count(*) FROM sales_orders WHERE grand_total < 0
UNION ALL SELECT 'credit_negative', count(*) FROM account_credit WHERE outstanding < 0;

-- E-41 (القيم البديلة؛ أعداد فقط)
-- nile_sales:
SELECT 'order_unknown_account', count(*) FROM sales_orders WHERE account_id IN ('unknown','') OR account_name IN ('unknown','');
-- nile_organization:
SELECT 'employee_without_user', count(*) FROM employees WHERE linked_user_id IS NULL;
-- nile_inventory (معرّفات المنتجات المستخدمة؛ قارنها بقائمة معرّفات products — أعداد فقط):
SELECT count(DISTINCT product_id), count(DISTINCT batch_id), count(DISTINCT supplier_id) FROM inventory_transactions WHERE type='RECEIPT';
-- nile_products:
SELECT count(*) FROM products; SELECT count(*) FROM batches;

-- E-42 (nile_accounting) — يعمل مهما كان شكل الجدول؛ أعداد فقط
SELECT to_regclass('journal_entries') IS NOT NULL AS has_je, to_regclass('journal_lines') IS NOT NULL AS has_jl, to_regclass('journal_entry_workflows') IS NOT NULL AS has_jew;
SELECT count(*) FROM journal_entries;   -- إن وُجد
SELECT status, count(*) FROM journal_entries GROUP BY 1;   -- إن وُجد
SELECT count(*) AS unbalanced FROM (SELECT journal_entry_id FROM journal_lines GROUP BY 1 HAVING abs(sum(debit)-sum(credit))>0.005) x;
SELECT source_type, count(*) FROM journal_entries GROUP BY 1 ORDER BY 2 DESC;

-- E-43 (أعداد فقط؛ لا مبالغ ولا أسماء)
-- nile_sales:
SELECT count(*) AS accounts_with_exposure, round(sum(outstanding)) AS total_outstanding_rounded FROM account_credit WHERE outstanding > 0;
-- nile_accounting:
SELECT count(DISTINCT account_id), round(sum(total - paid_amount - coalesce(credited_amount,0))) FROM invoices WHERE status NOT IN ('CANCELLED') AND total - paid_amount - coalesce(credited_amount,0) > 0.005;
```

> **ملاحظة:** E-43 تُرجع إجماليين مقرَّبين فقط؛ إن اعتُبرت الإجماليات حساسة، أرسل الفرق النسبي بدلها. إن فشل أي استعلام لأن العمود غير موجود فهذا **دليل** بحد ذاته (drift محتمل) — أرسل رسالة الخطأ كما هي.

## 2. القرارات المطلوبة قبل اعتماد التصميم

| # | القرار | يحسم | المصدر في `25` |
|---|---|---|---|
| D-1 | هل يصبح ERP الدفتر المحاسبي الرسمي، ومن أي تاريخ؟ | ADR-04، T6 | DEC-R2R-01 |
| D-2 | أي تنفيذ GL يُعتمد (واحد فقط) | ADR-04 | DEC-R2R-02 |
| D-3 | طريقة تكلفة المخزون: FIFO أم متوسط مرجح | ADR-04، DAR-19 | DEC-INV-20 |
| D-4 | تاريخ القطع والعملة وموقّع الأرصدة الافتتاحية | DAR-20 | DEC-OPS-01، DEC-R2R-21، DEC-TRC-04 |
| D-5 | منصة الاستضافة وأسماء القواعد | ADR-02 | DEC-OPS-07، DEC-NFR-13 |
| D-6 | أهداف RPO/RTO وجدول النسخ والاحتفاظ ومالكه | ADR-12 | DEC-OPS-08 |
| D-7 | قاعدة التقريب ومعايير ETA | ADR-08 | DEC-R2R-08 |
| D-8 | المستندات التي تحتاج ترقيمًا بلا فجوات | ADR-08 | جديد (قانوني/ضريبي) |
| D-9 | هل النشاط خاضع لـGxP/Part 11 | ADR-09 | DEC-NFR-09 |
| D-10 | مدد الاحتفاظ لكل فئة | ADR-09 | DEC-NFR-02 |
| D-11 | الدفع الزائد على الفاتورة: يُرفض أم رصيد دائن للعميل | ADR-05 | جديد |
| D-12 | الرصيد السالب للخزينة/البنك: ممنوع أم مسموح لأنواع معينة | ADR-05 | جديد |
| D-13 | معنى حد الائتمان صفر، ومن يملك تعديله وتجاوزه | ADR-03/06 | DEC-TRC-10، DEC-TRC-12 |
| D-14 | سداد الموردين: أي تنفيذ ومعنى العكس | ADR-04 | DEC-P2P-09 |
| D-15 | هل يُعاد ترحيل قيد لنفس المصدر بعد عكسه (يحسم X4) | ADR-04 | جديد |
| D-16 | تقسيم الخدمات واستضافة وسيط الأحداث | ADR-01 | DEC-OPS-13 |

**ترتيب العرض المقترح على المالك:** D-1، D-2، D-5، D-6 (تحدد كل ما بعدها) ← D-3، D-4، D-7، D-8 ← الباقي.
