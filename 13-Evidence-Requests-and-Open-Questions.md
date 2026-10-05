# 13 — طلبات الأدلة من السيرفر والأسئلة المفتوحة

> **قواعد عامة لكل الطلبات:**
> - كل الأوامر **قراءة فقط**. لا `docker inspect` بدون `--format` (المخرج الافتراضي يحتوي `Env` أي أسرار). لا `printenv` كامل. لا dumps.
> - استعلامات DB داخل `BEGIN READ ONLY` مع `statement_timeout` و`lock_timeout`، وتنتهي بـ`ROLLBACK`. تعيد metadata أو أعدادًا فقط.
> - القالب الموحد (عدّل اسم المستخدم إن لم يكن `nile_admin`؛ لا تُمرّر كلمات مرور في سطر الأوامر):
> ```bash
> q() { docker exec -i nile-postgres psql -U nile_admin -d "$1" -X -A -F $'\t' -v ON_ERROR_STOP=1 <<SQL
> BEGIN READ ONLY; SET LOCAL statement_timeout='5s'; SET LOCAL lock_timeout='1s';
> $2
> ROLLBACK;
> SQL
> }
> # مثال: q nile_accounting "SELECT count(*) FROM invoices;"
> ```
> - **الإخفاء قبل الإرسال:** احذف أي سطر يحتوي `PASSWORD|SECRET|TOKEN|KEY|PEPPER|postgresql://` بقيمته؛ استبدل أسماء العملاء والموظفين بـ`***` إن ظهرت (الطلبات مصممة لعدم إظهارها).
> - **الأثر:** القواعد صغيرة (8-11MB حسب `[U]`)؛ الاستعلامات أدناه عدّية على جداول صغيرة أو على كتالوج النظام، أثرها ضئيل. الـCPU steal الحالي على المضيف لا يتأثر بقراءات بهذا الحجم.

## 1. طلبات الأدلة

### الأولوية P1 — تحسم هوية الإنتاج وحالة القاعدة (تؤكد/تنفي ARC-01, ARC-02, DB-01, DB-03)

| ID | المطلوب | لماذا | يؤكد/ينفي | الأمر (قراءة فقط) | الحجم | الإخفاء |
|---|---|---|---|---|---|---|
| E-01 | هوية حاوية db-migrate وآخر سجلاتها | معرفة أي كود رفض البوابة | DB-02، ARC-02 (إن احتوت migrations بعد 89c2c31) | `docker inspect nile-pharma-erp-db-migrate-1 --format '{{.Config.Image}} {{.Image}} {{.Created}} {{.State.ExitCode}} {{json .Config.Cmd}}'` ثم `docker logs --tail 80 nile-pharma-erp-db-migrate-1` | ~90 سطرًا | راجع السجلات من أي رابط DB قبل الإرسال |
| E-02 | جدول كل الحاويات بالـlabels | معرفة أي ملف compose وenv أنشأ كل حاوية، ومن شُغل بـ`--no-deps` | ARC-01, OPS-11 | `docker ps -a --format '{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Label "com.docker.compose.project"}}\t{{.Label "com.docker.compose.project.config_files"}}\t{{.Label "com.docker.compose.project.environment_file"}}\t{{.Label "com.docker.compose.depends_on"}}'` | ~15 سطرًا | لا أسرار |
| E-03 | سجل migrations لكل قاعدة | الحالة الفعلية للترحيل والتدخل اليدوي | ARC-02, DB-01 | لكل قاعدة من التسع: `q <db> "SELECT migration_name, checksum, applied_steps_count, started_at, finished_at, rolled_back_at FROM _prisma_migrations ORDER BY started_at;"` | ≤45 صفًا لكل قاعدة | لا أسرار |
| E-03b | بنية جداول GL وsupplier_payments | تحديد السيناريو A/B وشكل v1/v2 | DB-03, ACC-02 | `q nile_accounting "SELECT table_name, column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name IN ('journal_entries','journal_lines','supplier_payments','journal_entry_workflows') ORDER BY 1, ordinal_position;"` و`q nile_accounting "SELECT to_regclass('accounts'), to_regclass('journal_entry_number_seq');"` | ~80 صفًا | لا أسرار |
| E-04 | قائمة الجداول لكل قاعدة + الـvolume اليتيم + accounting-manual | مطابقة مستوى الـschema؛ أصل `pg_accounting`؛ ما الذي شغلته accounting-manual | ARC-02, OPS-08, OPS-10, OPS-11 | `q <db> "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY 1;"`؛ `docker volume inspect nile-pharma-erp_pg_accounting --format '{{.CreatedAt}} {{json .Labels}}'`؛ `docker inspect nile-pharma-erp-accounting-manual --format '{{.Config.Image}} {{json .Config.Cmd}} {{json .Config.Entrypoint}} {{.State.ExitCode}} {{.Created}} {{json .Config.Labels}}'` | ~200 سطر | لا Env |
| E-05 | أصل الصور ومحتوى الكود العامل | إثبات أو نفي أن الصورة = 89c2c31 | ARC-01 | انظر الكتلة **E-05** في §1.4 (وجود `dist/modules/general-ledger` يعني أن الصورة تحتوي كودًا لاحقًا لـ89c2c31، **ولا يحدد commit بعينه**؛ وغيابه لا يثبت أن الصورة = 89c2c31. الإثبات الدقيق يتطلب provenance للبناء أو مقارنة hashes لملفات dist ببناء commit محدد <sup>[تصحيح 34]</sup>) | ~40 سطرًا | لا أسرار |
| E-06 | وجود نسخ احتياطي | هل هناك أي نسخ آلي أو خارج المضيف | OPS-04 | انظر الكتلة **E-06** في §1.4 | ~60 سطرًا | أسماء ملفات فقط |
| E-07 | تعريف Postgres والشبكة | لإعادة بناء التعريف المفقود ومعرفة إن كان عرضة لـ`--remove-orphans` | ARC-03, OPS-02, OPS-12 | `docker inspect nile-postgres --format '{{.Config.Image}} {{json .Config.Labels}} {{json .HostConfig.RestartPolicy}} {{range .Mounts}}{{.Name}}->{{.Destination}} {{end}}'`؛ `docker network inspect nile-internal --format '{{.Internal}} {{json .Labels}} {{range .Containers}}{{.Name}} {{end}}'` | ~10 أسطر | **لا** `{{.Config.Env}}` |

### الأولوية P2 — تؤكد/تنفي defects محاسبية وتجارية في النسخة العاملة

| ID | المطلوب | يؤكد/ينفي | الاستعلام | الحجم |
|---|---|---|---|---|
| E-11 | أرصدة مخزون مستحيلة وحالات الحجز | DB-05, INV-15 | `q nile_inventory "SELECT ownership, count(*), sum(on_hand), sum(reserved) FROM stock_balances GROUP BY 1; SELECT count(*) FROM stock_balances WHERE on_hand<0 OR reserved<0 OR reserved>on_hand; SELECT count(*) FROM inventory_reservations WHERE is_released=false AND issued_at IS NULL;"` | 6 صفوف |
| E-12 | أطراف وهمية، base_total صفري | DB-04, DB-08 | `q nile_accounting "SELECT count(*) FROM invoices WHERE account_id='unknown' OR total=0; SELECT count(*) FROM vendor_invoices WHERE base_total=0 AND total_amount>0;"` (الثاني فقط إن وُجد العمود) | 2 |
| E-13 | آثار العكس والشيكات والعملات والإهلاك والضرائب وجداول CURRENT | ACC-03, ACC-06..09, ACC-13, ACC-15 | `q nile_accounting "SELECT count(*) FROM payments WHERE reversed AND financial_account_id IS NOT NULL; SELECT count(*), coalesce(sum(amount),0) FROM payments WHERE invoice_id IS NULL; SELECT method, check_status, count(*) FROM payments GROUP BY 1,2; SELECT currency, count(*) FROM invoices GROUP BY 1; SELECT asset_id, fiscal_year, period_month, count(*) FROM depreciation_entries GROUP BY 1,2,3 HAVING count(*)>1; SELECT count(*), min(created_at), max(created_at) FROM tax_entries; SELECT count(*) FROM invoices; SELECT status, count(*) FROM fiscal_periods GROUP BY 1; SELECT code, is_active, is_header FROM chart_of_accounts WHERE code IN ('1111','1112','1113','1121','1122','1131','2111','2112','2121','4110','5100','5211','1219'); SELECT 'je', count(*) FROM journal_entries UNION ALL SELECT 'sp', count(*) FROM supplier_payments UNION ALL SELECT 'jw', count(*) FROM journal_entry_workflows;"` (احذف آخر سطر إن لم توجد الجداول) | ~40 |
| E-14 | حالات الطلبات والـsaga والخصومات والائتمان | SAL-01, SAL-02, SAL-03, SAL-04 | `q nile_sales "SELECT status, count(*) FROM sales_orders GROUP BY 1; SELECT step, count(*) FROM order_sagas GROUP BY 1; SELECT o.status, count(*) FROM sales_orders o JOIN order_sagas s ON s.order_id=o.id WHERE s.step='DONE' AND o.status<>'PAID' GROUP BY 1; SELECT count(*) FILTER (WHERE discount_pct>12), max(discount_pct) FROM sales_order_lines; SELECT count(*) FILTER (WHERE credit_limit>0), count(*) FROM account_credit;"` | ~30 |
| E-15 | قواعد الحوافز وسجلها | SAL-07, SAL-08 | `q nile_incentives "SELECT version, is_active FROM rule_sets; SELECT status, count(*) FROM incentive_ledger GROUP BY 1; SELECT tier_applied, count(*) FROM incentive_ledger GROUP BY 1;"` | ~15 |
| E-16 | الأدوار وحاملو الصلاحيات الحساسة؛ توزيع IP الجلسات | SEC-01, SAL-11, SEC-07 | `q nile_iam "SELECT r.name, count(ur.user_id) FROM roles r LEFT JOIN user_roles ur ON ur.role_id=r.id GROUP BY 1; SELECT r.name, p.code FROM roles r JOIN role_permissions rp ON rp.role_id=r.id JOIN permissions p ON p.id=rp.permission_id WHERE rp.is_granted AND p.code IN ('iam.users.update','iam.users.roles.manage','iam.roles.update','crm.accounts.credit-limit.update','sales.orders.credit-hold.override','incentives.ledger.approve') ORDER BY 2,1; SELECT ip_address, count(*) FROM sessions GROUP BY 1 ORDER BY 2 DESC LIMIT 5; SELECT count(*) FROM permissions;"` | ~40 (أسماء أدوار لا أشخاص) |
| E-17 | mounts وأوامر حاويات sales/crm/inventory/products | SAL-13, ARC-01 | `for c in sales crm inventory products incentives iam organization audit-aggregator web; do docker inspect nile-pharma-erp-$c-1 --format "$c {{.Config.Image}} {{.Image}} {{.Created}} {{json .Mounts}} {{json .Config.Cmd}}"; done` | 9 أسطر |
| E-18 | مطابقة حالة الدفعات بين Products وInventory | INV-03, INV-04, INV-08 | `q nile_products "SELECT status, count(*) FROM batches GROUP BY 1;"` و`q nile_inventory "SELECT reason, count(*) FROM blocked_batches GROUP BY 1; SELECT count(DISTINCT batch_id) FROM stock_balances WHERE ownership='QUARANTINE' AND on_hand>0;"` | ~15 |
| E-19 | المهام المجدولة | INV-06, INT-07 | لكل من nile_products/inventory/accounting/sales: `q <db> "SELECT name, status, count(*), max(started_at) FROM job_runs GROUP BY 1,2 ORDER BY 1;"` | ~40 |
| E-21 | أمانة منتهية الصلاحية | INV-14 | `q nile_inventory "SELECT count(*) FROM consignment_stock WHERE expiry_date < now() AND available_qty > 0;"` | 1 |

### الأولوية P3 — تشغيل وتكامل وأمن

| ID | المطلوب | يؤكد/ينفي | الأمر | الحجم / الإخفاء |
|---|---|---|---|---|
| E-20 | (بيئة اختبار فقط، لا الإنتاج) رمز الحالة لـ`GET /api/products/products/price-lists` | INV-12 | طلب واحد بتوكن اختبار، الحالة فقط | 1 سطر |
| E-22 | أعلام تشغيلية غير سرية | SEC-05, WEB-04, SAL-13 | `docker exec nile-pharma-erp-iam-1 sh -c 'for v in SESSION_IDLE_ENFORCEMENT JWT_ACCESS_TTL JWT_REFRESH_TTL QC_RELEASE_REQUIRES_SIGNATURE SCHEDULER_ENABLED OUTBOX_DISPATCH_ENABLED FIELD_PROPOSAL_CONVERSION_ENABLED NODE_ENV; do printf "%s=%s\n" $v "$(printenv $v)"; done'` (كرر على sales وaccounting) | قيم غير سرية فقط |
| E-23 | سلامة الأسرار بلا قيم | SEC-08 | `bash scripts/check-production-env.sh /opt/codeandcanvas/apps/nile-pharma-erp/.env` (يطبع حالات وأطوالًا)؛ `ls -l /opt/codeandcanvas/apps/nile-pharma-erp/.env* /tmp/nile-recovery-release.env` | بلا قيم |
| E-24 | أحداث مفقودة أو مرفوضة | INT-01, INT-03 | انظر الكتلة **E-24** في §1.4 | أعداد فقط |
| E-25 | إعداد Redpanda | INT-04 | `docker exec nile-pharma-erp-redpanda-1 rpk topic list`؛ `rpk cluster config get auto_create_topics_enabled`؛ `rpk cluster config get log_retention_ms`؛ `rpk group list` | ~100 سطر؛ بلا payloads |
| E-26 | أحجام البيانات للمقصوصات | WEB-01 | `q nile_inventory "SELECT count(*) FROM stock_balances;"`؛ `q nile_crm "SELECT count(*), count(*) FILTER (WHERE is_active) FROM accounts;"` | 2 |
| E-27 | Sentry وrewrites المخبوزة | WEB-04 | انظر الكتلة **E-27** في §1.4 | بلا قيم |
| E-28 | سجل GitHub Actions وحماية البيئة | OPS-03, OPS-07 | `gh run list --limit 30`؛ إعدادات environment `production` (لقطة شاشة) | — |
| E-29 | أدوار DB وملكية القواعد | §4 في 03 | `q postgres "SELECT datname, pg_get_userbyid(datdba) FROM pg_database; SELECT rolname, rolsuper, rolcreaterole FROM pg_roles WHERE rolname NOT LIKE 'pg_%';"` | ~15 |
| E-30 | تاريخ `Data/` في git | SEC-03 | انظر الكتلة **E-30** في §1.4 | أسماء commits فقط |


### 1.4 أوامر تحتوي pipes (خارج الجداول لتجنب أخطاء النسخ)

```bash
# E-05 — أصل الصور والكود العامل
docker image inspect nile-pharma-erp/accounting:release-89c2c31 --format '{{.Id}} {{.Created}} {{json .RepoDigests}} {{json .Config.Labels}}'
docker image ls --digests --format '{{.Repository}}:{{.Tag}} {{.ID}} {{.CreatedAt}}' | grep nile-pharma-erp
docker exec nile-pharma-erp-accounting-1 ls /app/apps/accounting/dist/modules
docker exec nile-pharma-erp-accounting-1 sh -c 'ls /app/apps/accounting/prisma/migrations | tail -3'   # BASELINE ينتهي بـ20260924120000_po_workflow_and_match_sod
# (اختياري لكل خدمة) نفس الفحص لـinventory: وجود ملف inventory-outbox يعني كود بعد 89c2c31
docker exec nile-pharma-erp-inventory-1 sh -c 'ls /app/apps/inventory/dist/modules/transactions'

# E-06 — النسخ الاحتياطي (أسماء فقط)
crontab -l 2>/dev/null; ls -la /etc/cron.d/
ls -la ~/backups/nile /var/backups/nile 2>/dev/null | tail -20
systemctl list-timers --all | head -30

# E-24 — أحداث مفقودة/مرفوضة (أعداد فقط)
for c in sales inventory accounting products crm; do
  printf '%s ' "$c"; docker logs --since 720h nile-pharma-erp-$c-1 2>&1 | grep -c -E 'EVENT NOT DELIVERED|REJECTED envelope|Routed poison message'
done
q nile_audit "SELECT status, consumer_group, count(*) FROM dead_letter_messages GROUP BY 1,2;"

# E-27 — Sentry وrewrites المخبوزة (بلا قيم)
docker exec nile-pharma-erp-web-1 sh -c 'test -n "$SENTRY_DSN" && echo set || echo empty'
docker exec nile-pharma-erp-web-1 node -e "const m=require('/app/apps/web/.next/routes-manifest.json');console.log(JSON.stringify(m.rewrites))"

# E-30 — تاريخ Data/ في git
git -C /opt/codeandcanvas/apps/nile-pharma-erp log --oneline -- Data/ | head
git -C /opt/codeandcanvas/apps/nile-pharma-erp count-objects -vH
```

## 2. الأسئلة المفتوحة للمالك (قرارات أعمال لا يمكن استنتاجها من الكود)

### الحوكمة والمتطلبات
- **Q-GOV-1:** من المعتمِد المسؤول عن المتطلبات؟ هل نعتمد سجل قرارات موحدًا موقّعًا منفصلًا عن حالة التنفيذ؟
- **Q-GOV-2:** نموذج التسعير الحاكم: (أ) قاعدة لكل فاتورة + خصم يدوي ضمن سقف الدور (09-25)، أم (ب) تسعير عند إنشاء العميل مع 12% أساس وصلاحية لما فوقها (09-28 + CURRENT)؟
- **Q-GOV-3:** هل تستمر إعادة التقييم M2 مع FX المحقق عند سداد المورد؟
- **Q-GOV-4:** هل تعتمد وضع شحنات الاستيراد داخل المحاسبة (BD-2) وسداد الموردين بترحيل مزدوج AP+خزينة (BD-7)، وهما منفذان في CURRENT بلا قرار مسجل؟

### المحاسبة
- **Q-ACC-1:** أين يُحفظ دفتر الأستاذ الرسمي اليوم (نظام خارجي)؟ هل ERP بديل له ومن أي تاريخ؟
- **Q-ACC-2:** كيف تُسجل مدفوعات الموردين حاليًا وكيف تُعلّم فواتيرهم مدفوعة؟
- **Q-ACC-3:** كيف ينعكس إيداع وتحصيل الشيكات على أرصدة البنوك؟
- **Q-ACC-4:** كيف يُصحح تحصيل مركزي خاطئ؟
- **Q-ACC-5:** هل الترقيم غير التسلسلي للفواتير مقبول ضريبيًا/لـETA؟ وهل `621-890-432` هو رقم التسجيل الفعلي؟
- **Q-ACC-6:** هل PO "سجل بواسطة SUPER_ADMIN يولد معتمدًا" هو الضابط المقصود بدل دورة الاعتماد؟
- **Q-ACC-7:** هل يُعد إقرار VAT من ERP أم خارجه؟ وهل يجب توليد قيود ضريبية تلقائيًا؟
- **Q-ACC-8:** هل تُستخدم فواتير أو تحصيلات بغير الجنيه فعليًا؟
- **Q-ACC-9:** سياسة SoD للقيود اليدوية (منشئ/معتمد/مرحّل)؟
- **Q-ACC-10:** هل يجوز تسجيل فواتير/تحصيلات بتاريخ داخل فترة مقفلة؟

### المبيعات والحوافز
- **Q-SAL-1:** هل خطة الحوافز (44 شريحة) تراكمية للمندوب شهريًا؟ وهل تخفض المرتجعات العمولة؟ الأساس: تحصيل أم مبيعات؟ عتبة 750 ألف؟
- **Q-SAL-2:** هل 12% خصم تجاري أساسي لكل الصيدليات ومصفوفة (3/5/7/15%) خصم إضافي؟ من يمنح ماذا؟
- **Q-SAL-3:** من يجب أن يحمل `crm.accounts.credit-limit.update`؟ هل يلزم معتمد ثانٍ؟
- **Q-SAL-4:** هل يجب أن يستوفي تجاوز الحجز الائتماني اعتماد ≥100,000؟ وهل العتبة قابلة للإعداد؟
- **Q-SAL-5:** هل يُسمح بالمرتجع قبل الشحن؟ وما مسار الاسترداد عند إلغاء طلب مدفوع بعد استدعاء؟
- **Q-SAL-6:** هل يلزم مستند عرض سعر؟ وهل يجب تفعيل تحويل المقترحات الميدانية في الإنتاج؟

### المخزون
- **Q-INV-1:** طريقة التكلفة (FIFO لكل مخزن لكل الحركات أم متوسط مرجح)؟ متى يُعترف بالتكلفة لطلبات الـsaga (الشحن أم الفاتورة)؟
- **Q-INV-2:** هل البضاعة المرتجعة الصالحة تدخل المخزون مباشرة أم عبر الحجر/الجودة؟
- **Q-INV-3:** إجراء الإتلاف/الإرجاع للدفعات المرفوضة والتالفة ومن يعتمده ومعالجته المحاسبية؟
- **Q-INV-4:** مصفوفة اعتماد التسويات (الزيادات والعتبات القيمية) والتحويلات؟
- **Q-INV-5:** الحد الأدنى للصلاحية المتبقية للبيع والأمانة؟
- **Q-INV-6:** هل التتبع بالموقع الداخلي (bin) مطلوب؟
- **Q-INV-7:** عملية الجرد الدوري (عد، تجميد، اعتماد الفروق)؟
- **Q-INV-8:** وحدة كمية المخزون (علبة؟) وهل تُطبق تحويلات الوحدات عند الشراء والبيع؟

### الأمن والموارد البشرية والتشغيل
- **Q-SEC-2:** هل يجب منع تركيبات الأدوار السامة عند الإسناد أم الاكتفاء بالكشف؟
- **Q-SEC-7:** هل إرسال بيانات ERP إلى مزودي LLM خارجيين معتمد؟ وهل "خارجي افتراضيًا" قرار صريح؟ قيود إقامة البيانات؟
- **Q-SEC-8:** هل توقيع إلكتروني بمتطلبات GxP/21 CFR Part 11 مطلوب فعلًا لإفراج الجودة؟
- **Q-ORG-1:** كيف تُقيد الرواتب والمصروفات والهدايا في الدفاتر اليوم؟ وهل الرواتب مستخدمة فعليًا؟
- **Q-ORG-2:** هل يُعتمد إصلاح EXP-1/EXP-2؟ ومن يعتمد الإجازات والمصروفات (المدير المباشر)؟
- **Q-OPS-1:** المنصة المستهدفة للقاعدة: `nile-postgres` المحلي (PG18) أم Neon؟
- **Q-OPS-2:** ما الذي حدث في 2026-09-29؟ من أنشأ `docker-compose.postgres.yml` و`/tmp/nile-recovery-release.env`؟ هل توجد مذكرة حادثة؟
- **Q-OPS-3:** من نفّذ `migrate resolve` لـgeneral_ledger وsupplier_payments؟ وهل طُبق DDL يدويًا؟
- **Q-OPS-4:** هل بيئة GitHub `production` مضبوطة بمعتمدين؟ وهل شُغل `production-deploy.yml` يومًا؟
- **Q-OPS-5:** هل توجد نسخة خارج المضيف لملفات `~/backups/nile/*`؟ مدة الاحتفاظ؟ المالك؟
- **Q-OPS-6:** هل نسخة Vercel للويب ما زالت حية؟
- **Q-OPS-7:** من يستقبل التنبيهات؟ هل توجد مراقبة uptime خارجية؟
- **Q-WEB-2:** أي سجل تدقيق هو المرجعي للمراجعين (المركزي أم المحلي)؟ مدة الاحتفاظ المطلوبة؟
- **Q-BUS-12:** مرتجع على فاتورة مسددة: رصيد دائن للعميل أم استرداد نقدي؟ وهل تُطبق سياسة 90 يومًا قبل الانتهاء والعبوة السليمة في النظام؟
- **Q-DATA:** هل وجود `Data/` في git مقصود؟ ومن يملك نسخًا من المستودع (متعاقدون، وكلاء AI، CI)؟
