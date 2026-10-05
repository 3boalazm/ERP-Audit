# سجل النتائج الموحد (Findings Register)

**المصدر:** تحليل ساكن للنسختين BASELINE `89c2c31` وCURRENT `fa40270` + مخرجات التشغيل المرفقة + ملاحظات المستخدم. لا يوجد أي اتصال بالسيرفر أو قاعدة البيانات.

**مفتاح الدليل:** `[B]`=89c2c31، `[C]`=fa40270 (المسارات نسبية لجذر الـsnapshot)، `[R]`=مخرجات تشغيل خام في `evidence/`، `[U]`=ملاحظات تشغيل نقلها المستخدم دون مخرجات خام (NilePharma_Audit.docx). العمود **Release-blocker** = يمنع نشر CURRENT كما هو.

**مقياس الخطورة:** Critical = توقف عمليات أساسية أو خسارة مالية مادية مؤكدة عند حدوث المحفز · High = خطر جوهري بمحفز واقعي في التشغيل العادي، أو فجوة رقابية مالية، أو مانع نشر · Medium = أثر محدود أو يحتاج ظرفًا خاصًا · Low = جودة/صيانة · Info = ملاحظة أو ضابط إيجابي.

**تنبيه:** درجة الخطورة مبنية على الأثر المثبت أو المستنتج بوضوح من الكود، لا على الحجم المحتمل. النتائج المصنفة `Inferred` أو `Unknown` تحتاج دليل السيرفر المذكور قبل اعتبارها مؤكدة.

## ملخص
إجمالي النتائج: **127** — Critical: 1 · High: 30 · Medium: 69 · Low: 22 · Info: 5

Release-blockers لنسخة CURRENT: **18**

| ID | العنوان | المجال | النسخة المتأثرة | التحقق | النوع | الخطورة | RB |
|---|---|---|---|---|---|---|---|
| [ACC-02](#acc-02) | CURRENT: كل مسارات كتابة GL تفشل على أي schema محتمل → توقف الفوترة والتحصيل والـsaga | Accounting / GL | CURRENT | Verified (code + SQL) / Inferred (runtime) | Confirmed defect (latent) | **Critical** | ✔ |
| [ACC-01](#acc-01) | BASELINE لا يحتوي دفتر أستاذ عام: ميزان المراجعة من أرصدة لا يُرحَّل إليها، وإقفال السنة يعيد إضافة صافي الدخل في كل تشغيل | Accounting / GL | BASELINE | Verified (code) | Confirmed gap | **High** |  |
| [ACC-03](#acc-03) | CURRENT: ترحيل GL داخل معاملة التحصيل؛ أي نقص في الإعداد (فترة OPEN، حسابات COA) يمنع قبض النقدية | Accounting / AR | CURRENT | Verified (code) / Inferred (runtime) | Potential risk | **High** | ✔ |
| [ACC-04](#acc-04) | CURRENT: عكس التحصيل/دفع المورد في GlPostingService يرحّل بنفس اتجاه القيد الأصلي | Accounting / GL | CURRENT | Verified (code) | Confirmed defect (latent) | **High** | ✔ |
| [ACC-05](#acc-05) | CURRENT: عكس القيد في GeneralLedgerService يعلّم الأصل REVERSED (فيُستبعد) ويرحّل قيد عكس POSTED (فيُحتسب) → أثر سالب أحادي في الميزان | Accounting / GL | CURRENT | Verified (code) / Inferred (effect) | Confirmed defect (latent) | **High** | ✔ |
| [ACC-06](#acc-06) | عكس التحصيل وارتداد الشيك لا يعكسان رصيد الخزينة/البنك | Accounting / Treasury | BOTH | Verified (code, تحقق مستقل) | Confirmed defect | **High** |  |
| [ACC-10](#acc-10) | لا توجد عملية سداد موردين في BASELINE؛ وفي CURRENT تنفيذان متعارضان غير مسجلين | Accounting / AP | BOTH | Verified | Confirmed gap | **High** |  |
| [ACC-18](#acc-18) | مرتجع على فاتورة مسددة بالكامل تُرفض محاسبيًا بينما يعيد المخزون البضاعة للرصيد | Accounting / Returns | BOTH | Verified (code) / Inferred (consequence) | Confirmed defect | **High** |  |
| [ARC-01](#arc-01) | هوية الكود العامل في الإنتاج غير مثبتة (tag محلي، image ID مختلف عن label، env مؤقت، تشغيل بـ--no-deps) | Architecture / Provenance | RUNTIME | Verified (labels) / Unknown (provenance) | Operational uncertainty | **High** |  |
| [ARC-02](#arc-02) | مؤشرات غير مثبتة على أن قاعدة البيانات رُحّلت إلى ما بعد BASELINE (accounting وorganization وinventory) — أعداد الجداول لا تثبت الإصدار؛ الحسم بـ_prisma_migrations | Architecture / Data | RUNTIME vs BASELINE | Inferred | Operational uncertainty | **High** |  |
| [ARC-03](#arc-03) | تعريف PostgreSQL الإنتاجي خارج git (docker-compose.postgres.yml وشبكة nile-internal وvolume nile_postgres_data غير موجودة في أي snapshot) | Architecture / DR | BOTH | Verified (غياب في المستودع) + [U] تشغيل | Potential risk | **High** |  |
| [ARC-05](#arc-05) | CURRENT: ثماني وحدات محاسبية (في سبعة مجلدات) غير مسجلة في AppModule (35 route) بينما الواجهة تستدعي 12 منها | Architecture / Accounting | CURRENT | Verified (static, script) | Confirmed defect | **High** | ✔ |
| [DB-01](#db-01) | تاريخ migrations المحاسبة عُدّل يدويًا (ROLLED_BACK ثم APPLIED بـ0 steps) وملفات migrations عُدّلت بعد إنشائها | Database / Migrations | RUNTIME + CURRENT | Verified (git) / Inferred (DB من وصف المستخدم) | Operational uncertainty | **High** |  |
| [DB-02](#db-02) | CURRENT: schema.prisma لا يطابق migrations المحاسبة (22 اختلافًا) → بوابة الإصدار ترفض وdb-migrate يخرج بالكود 3 ويوقف كل الخدمات | Database / Release | CURRENT | Verified (تشغيل validator ساكن على النسختين) | Confirmed defect | **High** | ✔ |
| [DB-03](#db-03) | شكلان متنافسان لجداول GL ولـsupplier_payments في migrations (legacy مقابل workbench؛ v1 مقابل v2) — شكل الإنتاج غير معروف | Database / Accounting | CURRENT + RUNTIME | Inferred | Operational uncertainty | **High** |  |
| [INT-01](#int-01) | معظم الأحداث تُكتب بشكل مزدوج (commit ثم publish مباشر) بلا outbox؛ outbox موجود في accounting (المدفوعات) وcrm (onboarding) وinventory (CURRENT فقط) | Integration / Consistency | BOTH | Verified (code) / Inferred (failure) | Potential risk | **High** |  |
| [INV-01](#inv-01) | CURRENT: طبقات تكلفة FIFO تُنشأ عند الاستلام وتُستهلك فقط في الفواتير المباشرة؛ بقية الحركات لا تحدّثها | Inventory / Costing | CURRENT | Verified (code) / Inferred (impact) | Confirmed defect (latent) | **High** | ✔ |
| [INV-02](#inv-02) | CURRENT: إلغاء الصرف المباشر لا يعيد طبقات التكلفة ولا يلغي حدث StockIssued → قيد COGS بلا فاتورة | Inventory / Accounting | CURRENT | Verified | Confirmed defect (latent) | **High** | ✔ |
| [INV-03](#inv-03) | أحداث دورة حياة الدفعات والأسعار في Products بلا outbox؛ فقدان RecallInitiated لا يمكن إعادته | Products / Quality | BOTH | Verified (code) / Inferred (impact) | Potential risk | **High** |  |
| [OPS-01](#ops-01) | أدوات نشر CURRENT تفترض Neon (فحص nc من المضيف، snapshot عبر Neon API، parity 16) بينما الإنتاج nile-postgres محلي | Operations / Deploy | CURRENT | Verified (code) / Inferred (effect) | Confirmed defect | **High** | ✔ |
| [OPS-02](#ops-02) | --remove-orphans في النشر/الـrollback الآلي قد يحذف حاوية nile-postgres إن كانت تحمل label المشروع | Operations / Deploy | CURRENT | Verified (code) / Inferred (label) | Potential risk | **High** | ✔ |
| [OPS-03](#ops-03) | pipeline الإصدار في CURRENT لا يكتمل (خطأ syntax في production-topology.test.cjs، اختبارات عقد قديمة، ترتيب خطوات، shallow clone) | Operations / CI | CURRENT | Verified (node --check) / Inferred (d,e) | Confirmed defect | **High** | ✔ |
| [OPS-04](#ops-04) | النسخ الاحتياطي الآلي لقاعدة الإنتاج غير مثبت: آلية المستودع غير صالحة كما هي لهذا المضيف، ودليل DR اصطناعي ويعتمد على Neon PITR؛ وجود نسخ على المضيف Unknown | Operations / DR | BOTH | Verified (repo) / Unknown (host cron) | Potential risk | **High** |  |
| [SAL-01](#sal-01) | حدث الدفع يكتب PAID فوق SHIPPED/DELIVERED/ON_HOLD_RECALL/CANCELLED؛ والعكس يعيد الطلب المسلَّم قابلًا للإلغاء | Sales / Order lifecycle | BOTH | Verified (code، تحقق مستقل) / Inferred (scenario) | Confirmed defect | **High** |  |
| [SAL-02](#sal-02) | وصول StockReserved متأخر يعيد إحياء طلب ملغى (ALLOCATED) ويحجز المخزون دون إفراج | Sales / Saga | BOTH | Verified (code) / Inferred (race) | Potential risk | **High** |  |
| [SAL-03](#sal-03) | مدفوعات الفواتير المباشرة لا تخفض تعرض الائتمان في Sales بينما الفاتورة تزيده | Sales / Credit control | BOTH | Verified | Confirmed defect | **High** |  |
| [SAL-04](#sal-04) | BASELINE: لا سقف للخصم في الخادم (0-100%)، السقف 30% في الواجهة فقط | Sales / Pricing control | BASELINE | Verified | Confirmed defect | **High** |  |
| [SAL-07](#sal-07) | شرائح العمولة تُطبق على كل دفعة منفردة لا على المبيعات التراكمية للفترة | Incentives | BOTH | Verified (code) / Inferred (intent) | Question | **High** |  |
| [SEC-01](#sec-01) | حامل iam.users.update يستطيع تغيير كلمة مرور أي مستخدم بما فيهم SUPER_ADMIN أو إيقافه | Security / IAM | BOTH | Verified (code، تحقق مستقل) | Confirmed defect | **High** |  |
| [SEC-02](#sec-02) | CURRENT: seed الخاص بـIAM معطوب (حقل username غير موجود) ولا ينشئ SUPER_ADMIN، و44 صلاحية مطلوبة غير موجودة في الكتالوج | Security / IAM / Release | CURRENT | Verified (code) / Inferred (runtime) | Confirmed defect | **High** | ✔ |
| [SEC-03](#sec-03) | مجلد Data/ بملفات أعمال حقيقية (رواتب، عملاء، فواتير، مبيعات) مُضاف إلى git في النسختين | Security / Data governance | BOTH | Verified (أسماء فقط) | Confirmed defect | **High** |  |
| [ACC-07](#acc-07) | التحصيلات المركزية (allocations) لا يمكن عكسها أو ارتدادها ولا تُفك التخصيصات | Accounting / AR | BOTH | Verified (code) / Inferred (error) | Confirmed defect | **Medium** |  |
| [ACC-08](#acc-08) | الشيك المحصَّل (CLEARED) لا يصل للخزينة/البنك؛ وفي CURRENT يبقى في 1122 | Accounting / Cheques | BOTH | Verified | Confirmed gap | **Medium** |  |
| [ACC-09](#acc-09) | عملة الدفعة لا تُقارن بعملة الفاتورة/الخزينة؛ دفاتر فرعية بعملات مختلطة | Accounting / FX | BOTH | Verified | Potential risk | **Medium** |  |
| [ACC-11](#acc-11) | CURRENT: سير عمل القيود اليدوية بلا فصل مهام، ومسار ترحيل مباشر يتجاوز الاعتماد، وصلاحياته غير موجودة في IAM | Accounting / Controls | CURRENT | Verified / Inferred (perms) | Potential risk | **Medium** |  |
| [ACC-12](#acc-12) | CURRENT: أمر الشراء يُنشأ معتمدًا مباشرة بواسطة SUPER_ADMIN (أزيل فصل المهام الموجود في BASELINE) | Accounting / Procurement controls | CURRENT | Verified | Question | **Medium** |  |
| [ACC-13](#acc-13) | BASELINE: الإهلاك الشهري غير idempotent وغير transactional | Accounting / Fixed assets | BASELINE | Verified | Confirmed defect | **Medium** |  |
| [ACC-14](#acc-14) | إقفال الفترات لا يمنع الترحيل (BASELINE لا يتحقق إطلاقًا؛ CURRENT غير متسق) | Accounting / Period close | BOTH | Verified | Confirmed gap | **Medium** |  |
| [ACC-15](#acc-15) | تقارير VAT ونموذج 41 تُبنى من إدخالات ضريبية يدوية فقط؛ رقم التسجيل الضريبي مكتوب في الكود | Accounting / Tax | BOTH | Verified | Potential risk | **Medium** |  |
| [ACC-16](#acc-16) | CURRENT: معالجات أحداث متعددة الخطوات غير ذرية، وخطأ 'already posted' يحوّل إعادة التسليم إلى poison message | Accounting / Integration | CURRENT | Verified (code) | Potential risk | **Medium** |  |
| [ACC-17](#acc-17) | إعادة إصدار الفاتورة تنشئ رأس فاتورة بلا سطور وبمبالغ حرة دون اعتماد ثانٍ | Accounting / AR controls | BOTH | Verified | Potential risk | **Medium** |  |
| [ACC-19](#acc-19) | BASELINE: المطابقة الثلاثية تفترض الكمية المستلمة = المطلوبة | Accounting / Procurement | BASELINE | Verified | Confirmed gap | **Medium** |  |
| [ARC-04](#arc-04) | البنية الموثقة تتعارض مع الكود والتشغيل (Neon/Railway/Vercel مقابل VPS + PG18 محلي) | Architecture / Documentation | BOTH | Verified | Potential risk | **Medium** |  |
| [DB-07](#db-07) | عدم تطابق Prisma مع SQL في جداول GL (fiscalPeriodId إلزامي في Prisma وnullable في SQL، currency enum مقابل TEXT) | Database / Accounting | CURRENT | Verified | Confirmed defect | **Medium** |  |
| [DB-09](#db-09) | اختلاف نسخة PostgreSQL بين البيئات (18 إنتاج، 16 تطوير/CI، بوابة parity مثبتة على 16) | Database / Platform | BOTH | Verified (code) + [U] | Potential risk | **Medium** |  |
| [GOV-01](#gov-01) | لا يوجد baseline متطلبات معتمد وموقّع؛ القرارات تفريغ لإجابات المالك بلا اسم معتمِد، وعمود الحالة يكتبه المنفذ | Governance / Requirements | BOTH | Verified | Potential risk | **Medium** |  |
| [GOV-02](#gov-02) | RTM و'Go-live gate' و'DR drill' السابقة لا تصلح كدليل (فحوص وجود ملفات/نصوص، أرقام متناقضة، أدلة ملفقة سُحبت) | Governance / QA | BOTH | Verified | Confirmed defect (documentation) | **Medium** |  |
| [GOV-03](#gov-03) | قرارات 2026-09-28 (ترقيم PO، مطابقة الاستلام الفعلي، سقف الخصم، سداد الموردين، FX المحقق) موجودة في CURRENT فقط | Governance / Business | BASELINE | Verified (static) | Operational uncertainty | **Medium** |  |
| [GOV-04](#gov-04) | قرارات متعارضة أو غير مسجلة (نموذج التسعير 09-25 مقابل 09-28؛ FX M2 مقابل المحقق؛ BD-2/BD-7 منفذة بلا قرار) | Governance / Business | BOTH | Verified (text) | Question | **Medium** |  |
| [INT-02](#int-02) | علامة dedup تُكتب بعد المعالج وخارج معاملته، ومعالجات متعددة الكتابة → تطبيق مزدوج عند إعادة المحاولة | Integration / Idempotency | BOTH | Verified (mechanism) / Inferred (impact) | Potential risk | **Medium** |  |
| [INT-03](#int-03) | الأحداث ذات التوقيع المرفوض تُسقط دون أثر دائم (لا DLQ ولا audit) | Integration / Integrity | BOTH | Verified | Potential risk | **Medium** |  |
| [INT-04](#int-04) | Redpanda عقدة واحدة، والمواضيع تُنشأ تلقائيًا بإعدادات افتراضية (partitions/retention/RF غير معرّفة) | Integration / Platform | BOTH | Verified (absence) / Unknown (runtime) | Operational uncertainty | **Medium** |  |
| [INT-05](#int-05) | CURRENT: المستهلكون يبدأون من 'latest' → ترتيب النشر قد يفقد أحداث inventory.stock.issued الجديدة | Integration / Rollout | CURRENT | Inferred | Operational uncertainty | **Medium** | ✔ |
| [INV-04](#inv-04) | بضاعة تُستلم بعد إفراج الدفعة تبقى في الحجر ولا تُفرج تلقائيًا | Inventory / QC | BOTH | Inferred | Potential risk | **Medium** |  |
| [INV-05](#inv-05) | CURRENT: تقرير التقييم يعد الطبقات مرتين عند وجود أكثر من pool للدفعة في المخزن | Inventory / Reporting | CURRENT | Verified | Confirmed defect | **Medium** |  |
| [INV-06](#inv-06) | مهمة stock-conservation تعدّ استلامات الحجر مرتين → انحراف كاذب في كل تشغيل | Inventory / Reconciliation | BOTH | Verified (SQL read) | Confirmed defect | **Medium** |  |
| [INV-07](#inv-07) | شحن طلبات المبيعات لا ينتج COGS؛ الفواتير المباشرة فقط (CURRENT) | Inventory / Accounting | BOTH | Verified | Question | **Medium** |  |
| [INV-08](#inv-08) | الاستلام يقبل أي productId/batchId/supplierId وتاريخ انتهاء من العميل دون تحقق من Products | Inventory / Master data | BOTH | Verified | Potential risk | **Medium** |  |
| [INV-09](#inv-09) | لا مفتاح idempotency للاستلام ومرتجع المورد والتسويات وتحميل الأمانة والشطب | Inventory / Commands | BOTH | Verified | Potential risk | **Medium** |  |
| [INV-10](#inv-10) | زيادة المخزون بالتسوية بلا حد ولا اعتماد، والعتبة كمية لا قيمة | Inventory / Controls | BOTH | Verified | Question | **Medium** |  |
| [INV-11](#inv-11) | لا مسار إتلاف/إرجاع للمخزون التالف أو المحجور، ولا عملية جرد | Inventory / Process | BOTH | Verified | Confirmed gap | **Medium** |  |
| [INV-12](#inv-12) | مسار قائمة الأسعار غالبًا مظلّل بـGET /products/:id | Products / API | BOTH | Inferred (not executed) | Potential risk | **Medium** |  |
| [INV-13](#inv-13) | نقاط issue-direct/rollback-direct قابلة للاستدعاء مباشرة لأي حامل accounting.invoices.create | Inventory / Authorization | BOTH | Verified / Inferred | Potential risk | **Medium** |  |
| [INV-14](#inv-14) | BASELINE: تحميل الأمانة لا يرفض الدفعات المنتهية/المحظورة (شرط المالك قبل الاستخدام الإنتاجي) | Inventory / Consignment | BASELINE | Verified | Confirmed defect | **Medium** |  |
| [INV-17](#inv-17) | CURRENT: outbox المخزون بلا backoff ولا حماية تداخل ولا يحترم OUTBOX_DISPATCH_ENABLED | Inventory / Integration | CURRENT | Verified | Potential risk | **Medium** |  |
| [OPS-05](#ops-05) | workflow النشر يخفي فشل النشر البعيد (`; rm -f` في نهاية أمر ssh) | Operations / CI | CURRENT | Verified (تحقق مستقل) | Confirmed defect | **Medium** | ✔ |
| [OPS-06](#ops-06) | smoke بعد النشر يستدعي compose بلا ملف env الإصدار → فشل interpolation → rollback يفشل بنفس الطريقة | Operations / Deploy | CURRENT | Inferred | Potential risk | **Medium** | ✔ |
| [OPS-07](#ops-07) | بوابة الاعتماد للإنتاج تعتمد على إعدادات GitHub environment غير مُصدَّرة؛ النشر يُطلق تلقائيًا بعد كل CI ناجح على main | Operations / Governance | CURRENT | Unknown | Question | **Medium** |  |
| [OPS-08](#ops-08) | ملف compose التطويري هو الافتراضي في مجلد الإنتاج وبنفس اسم المشروع (منافذ PG 5432-5440 على كل الواجهات) | Operations / Hygiene | BOTH | Verified (files) / Inferred (pg_accounting) | Potential risk | **Medium** |  |
| [OPS-09](#ops-09) | بوابة توافق migrations تقارن بالـpush السابق لا بالإنتاج ولا تكشف تعديل migrations مطبقة | Operations / Migrations | CURRENT | Verified | Potential risk | **Medium** |  |
| [OPS-10](#ops-10) | الصور تعمل كـroot وتحمل شجرة البناء كاملة، والـCMD الافتراضي ينفذ prisma migrate deploy | Operations / Containers | BOTH | Verified | Potential risk | **Medium** |  |
| [OPS-11](#ops-11) | حاويات متوقفة غير مفسرة: db-migrate (Exited 3) وaccounting-manual (Exited 1، تعريفها ليس في git) | Operations / Runtime | RUNTIME | [U] user-reported | Operational uncertainty | **Medium** |  |
| [ORG-01](#org-01) | اعتماد الإجازة بلا تحقق من الحالة (خصم مزدوج للرصيد، اعتماد إجازة مرفوضة) وبلا منع اعتماد ذاتي | Organization / HR | BOTH | Verified | Confirmed defect | **Medium** |  |
| [ORG-02](#org-02) | مطالبات المصروفات: رفض من أي حالة بما فيها PAID، قراءة غير مقيدة، لا تحقق من المالك أو المدير | Organization / Expenses | BOTH | Verified | Confirmed defect | **Medium** |  |
| [ORG-03](#org-03) | تعديلات الرواتب تغيّر netPay لمسيرات FINALIZED/PAID دون إعادة اعتماد؛ الحوافز = 0 ثابتة | Organization / Payroll | BOTH | Verified | Confirmed defect | **Medium** |  |
| [ORG-04](#org-04) | لا تكامل مالي من HR: صرف الرواتب والمصروفات والهدايا لا ينشر أحداثًا ولا يرحّل لأي دفتر | Organization / Accounting | BOTH | Verified | Operational uncertainty | **Medium** |  |
| [SAL-05](#sal-05) | CURRENT: بوابة الخصم تعتمد صلاحية غير موجودة (sales.discounts.approve) وتتجاهل مستويات مصفوفة الاعتماد | Sales / Pricing control | CURRENT | Verified | Confirmed defect | **Medium** | ✔ |
| [SAL-06](#sal-06) | المرتجعات مسموحة على طلبات مفوترة لم تُشحن (الفاتورة تصدر عند الحجز) → إعادة مخزون وهمية وائتمان AR | Sales / Returns | BOTH | Verified (code) / Inferred (impact) | Potential risk | **Medium** |  |
| [SAL-08](#sal-08) | لا يُزرع rule set للحوافز في مسار الإنتاج → كل PaymentReceived يفشل إلى DLQ إن كان الجدول فارغًا | Incentives / Ops | BOTH | Verified (scripts) / Unknown (DB) | Operational uncertainty | **Medium** |  |
| [SAL-09](#sal-09) | سجل الحوافز بلا تقييد نطاق (rep scoping) ولا فصل مهام في الاعتماد/الصرف؛ العكس مسموح بعد PAID | Incentives / Controls | BOTH | Verified | Potential risk | **Medium** |  |
| [SAL-10](#sal-10) | المرتجعات والإشعارات الدائنة لا تعدّل العمولات؛ الاسترداد يعكس سطرًا واحدًا لكل payment_id | Incentives | BOTH | Verified / Inferred | Question | **Medium** |  |
| [SAL-11](#sal-11) | المندوب يستطيع تعديل حد ائتمان عملائه، والقيمة 0 تعطّل الرقابة؛ التغيير بلا outbox ولا تسوية مع Sales | CRM / Credit governance | BOTH | Verified / Unknown (role assignment) | Potential risk | **Medium** |  |
| [SAL-12](#sal-12) | قبول طلبات لعملاء مؤرشفين (isActive=false) | Sales / Master data | BOTH | Verified | Confirmed defect | **Medium** |  |
| [SAL-13](#sal-13) | صور إثبات التسليم والفواتير الموقعة تُخزن على قرص الحاوية دون volume | Sales / Evidence retention | BOTH | Verified (compose) / Unknown (mounts) | Operational uncertainty | **Medium** |  |
| [SAL-14](#sal-14) | إعدادات التسعير (سياسات الخصم، قواعد الأسعار، العروض، ملف تسعير العميل، نسبة عمولة العميل) لا تُطبق أبدًا على الطلبات | Sales / Pricing | BOTH | Verified | Confirmed gap | **Medium** |  |
| [SAL-15](#sal-15) | مسودات الطلبات المستوردة تتبع سياسة تسعير أضعف ولا يُعاد التحقق منها عند الإرسال | Sales / Pricing | BOTH | Verified | Confirmed defect | **Medium** |  |
| [SAL-16](#sal-16) | إلغاء الطلب من حجز الاستدعاء يتجاهل الأموال المحصلة | Sales / Recall | BOTH | Verified / Inferred | Potential risk | **Medium** |  |
| [SEC-04](#sec-04) | CURRENT: أربعة controllers محاسبية بلا PermissionsGuard؛ أداة CI تتحقق من نص الـdecorator فقط | Security / Authorization | CURRENT | Verified (static, script) | Potential risk | **Medium** | ✔ |
| [SEC-05](#sec-05) | الصلاحيات داخل JWT ولا يُعاد التحقق منها؛ الإلغاء يتأخر حتى 15 دقيقة؛ تتبع الجلسات الخاملة معطل افتراضيًا | Security / Sessions | BOTH | Verified / Unknown (env) | Potential risk | **Medium** |  |
| [SEC-06](#sec-06) | توكنات الوصول والتحديث (7 أيام) في localStorage مع CSP يسمح بـunsafe-inline | Security / Web | BOTH | Verified | Potential risk | **Medium** |  |
| [SEC-07](#sec-07) | Rate limiting والقفل مرتبطان بـreq.ip دون trust proxy → كل المستخدمين يشتركون في نفس الحد خلف NPM/web | Security / Availability | BOTH | Inferred | Operational uncertainty | **Medium** |  |
| [SEC-08](#sec-08) | سر HS256 واحد مشترك بين الخدمات التسع، وأسرار تطوير حرفية في ملفات dev/CI | Security / Secrets | BOTH | Verified (repo) / Unknown (prod values) | Potential risk | **Medium** |  |
| [SEC-09](#sec-09) | ملف .env.backup.20260927-130337 غير متتبع داخل مجلد المستودع على الخادم وغير مغطى بـ.gitignore | Security / Secrets | RUNTIME | Verified ([R] git status) | Potential risk | **Medium** |  |
| [SEC-10](#sec-10) | فصل المهام (SoD) كشفي فقط، والمصفوفة تشير إلى 7 صلاحيات غير موجودة؛ SUPER_ADMIN مستثنى في الرواتب | Security / SoD | BOTH | Verified | Confirmed defect | **Medium** |  |
| [SEC-11](#sec-11) | التوقيع الإلكتروني لا يحقق نية 21 CFR Part 11 (لا إعادة مصادقة، الكيان خارج الـMAC، canonicalization ناقص، لا تحقق عند الإفراج) | Security / Quality | BOTH | Verified | Confirmed defect | **Medium** |  |
| [SEC-12](#sec-12) | Copilot يرسل بيانات ERP إلى مزودي LLM خارجيين؛ CURRENT يجعل ذلك افتراضيًا | Security / Data protection | BOTH (default CURRENT) | Verified / Unknown (provider) | Question | **Medium** |  |
| [SEC-13](#sec-13) | سجلات audit_logs المحلية best-effort، للنجاح فقط، قابلة للتعديل، وIP هو الوكيل؛ السجل المركزي يغطي الأحداث فقط | Security / Audit trail | BOTH | Verified / Inferred (IP) | Potential risk | **Medium** |  |
| [WEB-01](#web-01) | تجميعات الـBFF مقصوصة بصمت عند 200 صف (قيمة المخزون، التعرض الائتماني، عدادات المهام) | Web / Reporting | BOTH | Verified | Potential risk | **Medium** |  |
| [WEB-02](#web-02) | CURRENT: صفحة general-ledger تستدعي fetch بلا Authorization → 401 دائمًا | Web / Finance UI | CURRENT | Verified | Confirmed defect | **Medium** | ✔ |
| [WEB-04](#web-04) | رصد ضعيف: لا metrics، Sentry في الويب غالبًا غير فعال، JsonLogger غير مستخدم، لا تنبيهات ولا حدود موارد | Web / Observability | BOTH | Verified (config) / Unknown (DSN) | Operational uncertainty | **Medium** |  |
| [ACC-20](#acc-20) | CURRENT: الإهلاك يتطلب حسابات 5211/1219 غير موجودة في الدليل المزروع | Accounting / Fixed assets | CURRENT | Verified | Confirmed defect (latent) | **Low** |  |
| [ACC-21](#acc-21) | التكلفة المحمّلة والمشتريات العامة سجلات فقط بلا أثر على المخزون أو الخزينة أو GL؛ حالة المشتريات قابلة للتعديل بأي اتجاه | Accounting / AP | BOTH | Verified | Confirmed gap | **Low** |  |
| [ACC-22](#acc-22) | GET /coa/tree يكتب: يزرع دليل الحسابات الافتراضي عند جدول فارغ | Accounting / GL | BOTH | Verified | Improvement | **Low** |  |
| [ACC-23](#acc-23) | CURRENT: تسوية AP مقابل GL بإشارات متعاكسة وبلا فلتر POSTED → انحراف دائم | Accounting / Reconciliation | CURRENT | Inferred | Potential risk | **Low** |  |
| [ARC-06](#arc-06) | لا هوية للخدمات: الاتصالات بين الخدمات تتم بتوكن المستخدم النهائي | Architecture / Security | BOTH | Verified | Improvement | **Low** |  |
| [DB-04](#db-04) | لا تكامل مرجعي عبر الخدمات: مراجع منطقية (*Id) بلا FK، والـsaga تضع 'unknown' و0 عند غياب الحقول | Database / Data ownership | BOTH | Verified (schema + code) | Potential risk | **Low** |  |
| [DB-05](#db-05) | لا قيود CHECK على أرصدة المخزون (on_hand>=0, reserved<=on_hand) — المنع في التطبيق فقط | Database / Inventory | BOTH | Verified | Potential risk | **Low** |  |
| [DB-06](#db-06) | فهارس وقيود: 23 عمود FK بلا index، و7 حقول status نصية حرة، وحقول audit ناقصة (heuristic) | Database / Quality | CURRENT | Verified (فحص آلي heuristic) | Improvement | **Low** |  |
| [DB-08](#db-08) | Backfill لمرة واحدة في vendor_invoice_fx: فواتير موردين ينشئها كود BASELINE بعد الـmigration تبقى base_total=0 | Database / AP | RUNTIME (إن صح ARC-02) | Inferred | Potential risk | **Low** |  |
| [DB-10](#db-10) | ترقيم المستندات غير تسلسلي (INV-<base36 ms>، SO-<base36>-uuid) | Database / Compliance | BOTH | Verified | Question | **Low** |  |
| [DB-11](#db-11) | لا سياسة احتفاظ/أرشفة لجداول audit وoutbox وprocessed_events وjob_runs وDLQ | Database / Operations | BOTH | Verified (غياب) | Improvement | **Low** |  |
| [GOV-06](#gov-06) | وثائق قديمة ومعاملات تنظيمية مكتوبة في الكود بلا اعتماد (التأمينات 11%/18.75%، شرائح الضريبة، عتبة 100,000، خصم 12%) | Governance / Documentation | BOTH | Verified | Improvement | **Low** |  |
| [INT-06](#int-06) | عقود الأحداث بلا إصدار، وانحراف payloads، و3 أحداث بلا منتج | Integration / Contracts | BOTH | Verified | Improvement | **Low** |  |
| [INT-07](#int-07) | المجدول: صف job_runs قد يبقى RUNNING للأبد عند timeout، والقفل يمنع التزامن فقط | Integration / Scheduler | BOTH | Inferred | Potential risk | **Low** |  |
| [INV-15](#inv-15) | ثغرات تزامن ثانوية (release غير serializable، عكس التسوية، رفض طلب التسوية غير مشروط) | Inventory / Concurrency | BOTH | Inferred | Potential risk | **Low** |  |
| [OPS-12](#ops-12) | شبكة nile-internal ليست internal ولا موجودة في git؛ Postgres على شبكتين | Operations / Network | BOTH | [U] / Verified (absence) | Improvement | **Low** |  |
| [OPS-13](#ops-13) | عدم اتساق أسبقية DATABASE_URL بين التحقق وPrisma (7 خدمات تتحقق من <SVC>_DATABASE_URL وتتصل بـDATABASE_URL) | Operations / Config | BOTH | Verified | Potential risk | **Low** |  |
| [OPS-14](#ops-14) | CI يدفع صورًا مبنية من PRs إلى namespace سجل الإنتاج؛ SBOM غير مرفوع | Operations / Supply chain | CURRENT | Verified | Improvement | **Low** |  |
| [SAL-17](#sal-17) | تجاوز الحجز الائتماني يتخطى اعتماد ≥100,000؛ العتبة مكتوبة في الكود وتشمل الشحن | Sales / Approvals | BOTH | Verified | Question | **Low** |  |
| [SEC-14](#sec-14) | نقاط /health/details بلا مصادقة؛ مصادقة الـBFF مجرد وجود header | Security / Exposure | BOTH | Verified | Potential risk | **Low** |  |
| [SEC-15](#sec-15) | ملاحظات أمنية منخفضة: تعداد الحسابات وDoS القفل، انتهاء الجلسة 7 أيام ثابت، لا MFA، حجم توكن SUPER_ADMIN ≈7.4KB | Security / IAM | BOTH | Verified / Inferred | Improvement | **Low** |  |
| [WEB-03](#web-03) | شاشات التشغيل تغفل خدمات (health بلا organization، jobs بلا sales) | Web / Ops | BOTH | Verified | Confirmed defect | **Low** |  |
| [DB-12](#db-12) | إيجابي: المبالغ المالية Decimal بدقة صريحة في كل الخدمات (لا Float)، مع اختلاف scales (14,2 / 18,2 / 18,4) | Database / Financial precision | BOTH | Verified (فحص آلي) | Improvement | **Info** |  |
| [GOV-05](#gov-05) | متطلبات مقررة غير منفذة في أي نسخة: البونص، فرز التالف، مطالبات الموردين، حد ائتمان بالعلب، مخزن/خزنة المندوب | Governance / Scope | BOTH | Verified (grep) | Question | **Info** |  |
| [INV-16](#inv-16) | وحدات القياس غير مستخدمة في كميات المخزون، والمواقع الداخلية (bins) قائمة رئيسية فقط | Inventory / Master data | BOTH | Verified | Question | **Info** |  |
| [SAL-18](#sal-18) | عمليات غائبة: عرض السعر (Quotation)، احتساب تحقيق المستهدفات، سياسة المرتجعات (90 يومًا قبل الانتهاء) | Sales / Process gaps | BOTH | Verified (absence) | Question | **Info** |  |
| [SEC-16](#sec-16) | ضوابط إيجابية: ValidationPipe(whitelist, forbidNonWhitelisted) في كل الخدمات، JwtAuthGuard عام، PermissionsGuard fail-closed، bcrypt 12، تدوير refresh مع كشف إعادة الاستخدام، 5 routes عامة فقط | Security | BOTH | Verified (script + code) | Improvement | **Info** |  |

## التفاصيل

### ACC-01
**BASELINE لا يحتوي دفتر أستاذ عام: ميزان المراجعة من أرصدة لا يُرحَّل إليها، وإقفال السنة يعيد إضافة صافي الدخل في كل تشغيل**

- **المجال:** Accounting / GL · **النسخة المتأثرة:** BASELINE · **درجة التحقق:** Verified (code) · **النوع:** Confirmed gap
- **الخطورة:** High — لا يوجد سجل قيد مزدوج في النسخة العاملة؛ التقارير المالية الرسمية لا يمكن أن تأتي من النظام.
- **الدليل:** [B] apps/accounting/src/modules/coa/coa.service.ts:208-255؛ fiscal-periods.service.ts:150 (executeYearEndClosing؛ تعليق 136-143 يدّعي تصفير الحسابات الاسمية ولا يفعل)، 189-195؛ cash-banks.service.ts (تعليق الرأس)؛ git-and-schema.txt:690-726 (لا JournalEntry)
- **المحفز (Trigger):** استخدام /coa/trial-balance أو year-end-closing.
- **الأثر:** ميزان صفري أو مضلل؛ أرباح محتجزة متضخمة عند تكرار الإقفال.
- **للتحقق/الإغلاق:** سؤال Q-ACC-1: أين الدفتر الرسمي؟
- **مرجع ملاحظات العمل:** ACC-11

### ACC-02
**CURRENT: كل مسارات كتابة GL تفشل على أي schema محتمل → توقف الفوترة والتحصيل والـsaga**

- **المجال:** Accounting / GL · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (code + SQL) / Inferred (runtime) · **النوع:** Confirmed defect (latent)
- **الخطورة:** Critical — Critical إذا نُشر CURRENT: الفوترة من الطلبات، الإشعارات الدائنة، COGS، الإهلاك، وتحصيل الفواتير تتراجع؛ لا أثر على BASELINE. · **مانع نشر لـCURRENT**
- **الدليل:** [C] apps/accounting/src/modules/gl-workbench/gl-posting.service.ts:47,50-52 (UPDATE accounts — جدول غير موجود في nile_accounting)؛ general-ledger.service.ts:22-23,39-40؛ invoices.service.ts:512 وcredit-notes.service.ts:61 (حساب CRM كحساب أستاذ)؛ general_ledger/migration.sql:6-13,28؛ gl_workbench/migration.sql:72-74
- **المحفز (Trigger):** أي StockReserved، مرتجع، إهلاك، GoodsReceived، أو تحصيل على مستوى فاتورة في CURRENT.
- **الأثر:** rollback للمعاملات، رسائل إلى DLQ، طلبات عالقة عند ALLOCATED.
- **للتحقق/الإغلاق:** عدم نشر CURRENT accounting كما هو؛ توحيد كاتب GL؛ اختبار تكامل يزرع COA وينفذ inserts حقيقية.
- **مرجع ملاحظات العمل:** ACC-02(notes)

### ACC-03
**CURRENT: ترحيل GL داخل معاملة التحصيل؛ أي نقص في الإعداد (فترة OPEN، حسابات COA) يمنع قبض النقدية**

- **المجال:** Accounting / AR · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (code) / Inferred (runtime) · **النوع:** Potential risk
- **الخطورة:** High — يربط استلام النقد بإعداد GL لم يكن مطلوبًا في BASELINE؛ ومع UPDATE على جدول accounts غير الموجود (ACC-02) يُرجح فشل كل تحصيل يُرحَّل (عند وجود خزينة أو شيك). · **مانع نشر لـCURRENT**
- **الدليل:** [C] payments.service.ts:183-187؛ gl-posting.service.ts:26-44, 51-52
- **المحفز (Trigger):** قاعدة بلا fiscal_periods أو COA مكتمل.
- **الأثر:** رفض التحصيل.
- **للتحقق/الإغلاق:** E-13: عدّ fiscal_periods وحسابات COA المطلوبة؛ قرار سياسة (منع أم suspense).
- **مرجع ملاحظات العمل:** ACC-03(notes)

### ACC-04
**CURRENT: عكس التحصيل/دفع المورد في GlPostingService يرحّل بنفس اتجاه القيد الأصلي**

- **المجال:** Accounting / GL · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (code) · **النوع:** Confirmed defect (latent)
- **الخطورة:** High — يضاعف الأثر بدل إلغائه؛ الاختبار يتحقق من المجاميع فقط. · **مانع نشر لـCURRENT**
- **الدليل:** [C] gl-posting.service.ts:13,17,24 (AR non-CHECK: Dr treasury/Cr 1121 في الأصل والعكس)؛ gl-posting.integration.spec.ts:50-60
- **المحفز (Trigger):** POST /payments/:id/reverse أو شيك مرتد.
- **الأثر:** النقدية وAR في GL خاطئة بضعف المبلغ.
- **للتحقق/الإغلاق:** تصحيح الاتجاه واختبار لكل سطر.
- **مرجع ملاحظات العمل:** ACC-04(notes)

### ACC-05
**CURRENT: عكس القيد في GeneralLedgerService يعلّم الأصل REVERSED (فيُستبعد) ويرحّل قيد عكس POSTED (فيُحتسب) → أثر سالب أحادي في الميزان**

- **المجال:** Accounting / GL · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (code) / Inferred (effect) · **النوع:** Confirmed defect (latent)
- **الخطورة:** High — الفواتير الملغاة تظهر بإيراد سالب. · **مانع نشر لـCURRENT**
- **الدليل:** [C] general-ledger.service.ts:48-49, 119, 146؛ coa.service.ts:244؛ invoices.service.ts:1229-1230
- **المحفز (Trigger):** إلغاء/استبدال فاتورة.
- **الأثر:** قوائم مالية خاطئة.
- **للتحقق/الإغلاق:** اختيار اصطلاح واحد للعكس.
- **مرجع ملاحظات العمل:** ACC-05(notes)

### ACC-06
**عكس التحصيل وارتداد الشيك لا يعكسان رصيد الخزينة/البنك**

- **المجال:** Accounting / Treasury · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (code, تحقق مستقل) · **النوع:** Confirmed defect
- **الخطورة:** High — يعمل في النسخة المرجّحة للإنتاج؛ أرصدة الخزائن مضخمة ولا تكشفها التسوية الداخلية.
- **الدليل:** [B] apps/accounting/src/modules/payments/payments.service.ts:369-400؛ [C] :381-420 (لا financialAccountEntry في reverseInTx؛ الكتابة فقط عند الاستلام :181 و:634)
- **المحفز (Trigger):** عكس دفعة CASH/DEPOSIT/TRANSFER/E_WALLET/INSTAPAY.
- **الأثر:** عجز غير مفسر عند الجرد النقدي.
- **للتحقق/الإغلاق:** E-13: count payments WHERE reversed AND financial_account_id IS NOT NULL؛ تعريف قيد خزينة عكسي.
- **مرجع ملاحظات العمل:** ACC-06(notes)

### ACC-07
**التحصيلات المركزية (allocations) لا يمكن عكسها أو ارتدادها ولا تُفك التخصيصات**

- **المجال:** Accounting / AR · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (code) / Inferred (error) · **النوع:** Confirmed defect
- **الخطورة:** Medium — لا مسار تصحيح سوى تعديل قاعدة البيانات.
- **الدليل:** [B] payments.service.ts:370؛ [C] :386 (payment.invoiceId=null)
- **المحفز (Trigger):** عكس دفعة أنشئت عبر allocations[].
- **الأثر:** خطأ/404 والفواتير تبقى PAID.
- **للتحقق/الإغلاق:** E-13: count payments WHERE invoice_id IS NULL؛ سؤال Q-ACC-4.
- **مرجع ملاحظات العمل:** ACC-07(notes)

### ACC-08
**الشيك المحصَّل (CLEARED) لا يصل للخزينة/البنك؛ وفي CURRENT يبقى في 1122**

- **المجال:** Accounting / Cheques · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed gap
- **الخطورة:** Medium — أرصدة البنوك لا تتضمن تحصيلات الشيكات من النظام.
- **الدليل:** [C] payments.service.ts:70, 446-453, 771
- **المحفز (Trigger):** أي تحصيل بشيك.
- **الأثر:** الخزينة أقل من الواقع؛ 1122 يتضخم.
- **للتحقق/الإغلاق:** سؤال Q-ACC-3؛ E-13 حسب check_status.
- **مرجع ملاحظات العمل:** ACC-09(notes)

### ACC-09
**عملة الدفعة لا تُقارن بعملة الفاتورة/الخزينة؛ دفاتر فرعية بعملات مختلطة**

- **المجال:** Accounting / FX · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — يتطلب استخدام عملات غير EGP (المسار المباشر يدعمها).
- **الدليل:** [C] payments.service.ts:147-153, 180-181؛ invoices.service.ts:849, 1226
- **المحفز (Trigger):** فاتورة أو دفعة USD.
- **الأثر:** حالة سداد خاطئة وكشف حساب مختلط العملات.
- **للتحقق/الإغلاق:** E-13: توزيع العملات.
- **مرجع ملاحظات العمل:** ACC-10(notes)

### ACC-10
**لا توجد عملية سداد موردين في BASELINE؛ وفي CURRENT تنفيذان متعارضان غير مسجلين**

- **المجال:** Accounting / AP · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed gap
- **الخطورة:** High — دورة الشراء لا تُغلق داخل النظام؛ الفواتير لا تصل إلى PAID أبدًا في BASELINE.
- **الدليل:** [B] لا SupplierPayment model (git-and-schema.txt:690-726)؛ [C] modules/supplier-payments (شكل v1) و modules/supplier-ledger/supplier-payments.service.ts (شكل v2، `WHERE id = ${id}::uuid` على عمود TEXT :198, :247)
- **المحفز (Trigger):** سداد مورد.
- **الأثر:** AP يُدار خارج النظام أو كقيد خزينة حر بلا ربط.
- **للتحقق/الإغلاق:** سؤال Q-ACC-2.
- **مرجع ملاحظات العمل:** ACC §4.4, ACC-08(notes)

### ACC-11
**CURRENT: سير عمل القيود اليدوية بلا فصل مهام، ومسار ترحيل مباشر يتجاوز الاعتماد، وصلاحياته غير موجودة في IAM**

- **المجال:** Accounting / Controls · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified / Inferred (perms) · **النوع:** Potential risk
- **الخطورة:** Medium — ضعف رقابي على قيود يدوية.
- **الدليل:** [C] general-ledger.service.ts:82-111؛ general-ledger.controller.ts:19؛ غياب accounting.ledger.* في apps/iam
- **المحفز (Trigger):** إنشاء/اعتماد قيد يدوي.
- **الأثر:** قيد بلا مراجع مستقل.
- **للتحقق/الإغلاق:** قرار سياسة SoD (Q-ACC-9).
- **مرجع ملاحظات العمل:** ACC-13(notes)

### ACC-12
**CURRENT: أمر الشراء يُنشأ معتمدًا مباشرة بواسطة SUPER_ADMIN (أزيل فصل المهام الموجود في BASELINE)**

- **المجال:** Accounting / Procurement controls · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified · **النوع:** Question
- **الخطورة:** Medium — قرار 2026-09-28 ينص على PO بواسطة SUPER_ADMIN، لكنه لا يذكر إلغاء الاعتماد.
- **الدليل:** [C] matching.service.ts:100-158 مقابل [B] :91-127, 186-230؛ [C] docs/P1-BUSINESS-DECISION-PACK.md:426
- **المحفز (Trigger):** إنشاء PO.
- **الأثر:** شخص واحد ينشئ ويعتمد.
- **للتحقق/الإغلاق:** تأكيد المالك (Q-ACC-6).
- **مرجع ملاحظات العمل:** ACC-14(notes)

### ACC-13
**BASELINE: الإهلاك الشهري غير idempotent وغير transactional**

- **المجال:** Accounting / Fixed assets · **النسخة المتأثرة:** BASELINE · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — تكرار التشغيل يضاعف الإهلاك في سجل الأصول.
- **الدليل:** [B] fixed-assets.service.ts:111-195؛ لا unique على depreciation_entries
- **المحفز (Trigger):** تشغيل run-monthly مرتين لنفس الشهر.
- **الأثر:** قيمة دفترية خاطئة.
- **للتحقق/الإغلاق:** E-13: duplicates query.
- **مرجع ملاحظات العمل:** ACC-15(notes)

### ACC-14
**إقفال الفترات لا يمنع الترحيل (BASELINE لا يتحقق إطلاقًا؛ CURRENT غير متسق)**

- **المجال:** Accounting / Period close · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed gap
- **الخطورة:** Medium — مستندات بتواريخ داخل فترات مقفلة.
- **الدليل:** [B] لا مرجع لـfiscalPeriod خارج الوحدة؛ [C] fiscal-periods.service.ts:101-138؛ general-ledger.service.ts:10-14
- **المحفز (Trigger):** تسجيل بأثر رجعي.
- **الأثر:** تقارير فترات مقفلة تتغير.
- **للتحقق/الإغلاق:** سؤال Q-ACC-10.
- **مرجع ملاحظات العمل:** ACC-17(notes), REQDOC-09

### ACC-15
**تقارير VAT ونموذج 41 تُبنى من إدخالات ضريبية يدوية فقط؛ رقم التسجيل الضريبي مكتوب في الكود**

- **المجال:** Accounting / Tax · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — إقرار VAT من النظام ناقص ما لم تُدخل كل الحركات يدويًا.
- **الدليل:** [C] tax.service.ts:70, 139-140, 181-182؛ credit-notes.service.ts:73,90
- **المحفز (Trigger):** إعداد إقرار ضريبي.
- **الأثر:** إقرار ناقص.
- **للتحقق/الإغلاق:** سؤال Q-ACC-7؛ E-13: count tax_entries vs invoices.
- **مرجع ملاحظات العمل:** ACC-18(notes), REQDOC-08

### ACC-16
**CURRENT: معالجات أحداث متعددة الخطوات غير ذرية، وخطأ 'already posted' يحوّل إعادة التسليم إلى poison message**

- **المجال:** Accounting / Integration · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (code) · **النوع:** Potential risk
- **الخطورة:** Medium — PO projection قد لا يتحدث أبدًا.
- **الدليل:** [C] saga-listener.service.ts:330-357؛ general-ledger.service.ts:35
- **المحفز (Trigger):** فشل خطوة لاحقة في onGoodsReceived.
- **الأثر:** رسائل DLQ وحالات PO خاطئة.
- **للتحقق/الإغلاق:** transactional inbox لكل المعالجة.
- **مرجع ملاحظات العمل:** ACC-21(notes)

### ACC-17
**إعادة إصدار الفاتورة تنشئ رأس فاتورة بلا سطور وبمبالغ حرة دون اعتماد ثانٍ**

- **المجال:** Accounting / AR controls · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — تغيير قيمة فاتورة بصلاحية واحدة.
- **الدليل:** [C] invoices.service.ts:986-1062
- **المحفز (Trigger):** reissue.
- **الأثر:** فقد ربط الدفعات/السطور؛ تغيير قيم بلا مراجعة.
- **للتحقق/الإغلاق:** قرار سياسة.
- **مرجع ملاحظات العمل:** ACC-23(notes)

### ACC-18
**مرتجع على فاتورة مسددة بالكامل تُرفض محاسبيًا بينما يعيد المخزون البضاعة للرصيد**

- **المجال:** Accounting / Returns · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (code) / Inferred (consequence) · **النوع:** Confirmed defect
- **الخطورة:** High — حالة أعمال عادية تنتج تباعدًا بين المخزون وAR (متطلب الشركة F10).
- **الدليل:** [B] invoices.service.ts:909-916؛ [C] :937-943؛ [C] docs/audit/2026-09-18-company-workflows-vs-erp-ar.md:168-182
- **المحفز (Trigger):** مرتجع بعد السداد الكامل.
- **الأثر:** مخزون زائد بلا رصيد دائن للعميل؛ رسالة في DLQ.
- **للتحقق/الإغلاق:** قرار المالك: رصيد دائن أم استرداد (Q-BUS-12).
- **مرجع ملاحظات العمل:** REQDOC-07

### ACC-19
**BASELINE: المطابقة الثلاثية تفترض الكمية المستلمة = المطلوبة**

- **المجال:** Accounting / Procurement · **النسخة المتأثرة:** BASELINE · **درجة التحقق:** Verified · **النوع:** Confirmed gap
- **الخطورة:** Medium — قرار 2026-09-28 مطبق في CURRENT فقط؛ أثر محدود لغياب سداد الموردين في BASELINE.
- **الدليل:** [B] matching.service.ts:604 مقابل [C] :644
- **المحفز (Trigger):** تسجيل فاتورة مورد.
- **الأثر:** اعتماد للسداد مقابل كميات لم تستلم.
- **للتحقق/الإغلاق:** تأكيد الكود العامل (ARC-01).
- **مرجع ملاحظات العمل:** REQDOC-05

### ACC-20
**CURRENT: الإهلاك يتطلب حسابات 5211/1219 غير موجودة في الدليل المزروع**

- **المجال:** Accounting / Fixed assets · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified · **النوع:** Confirmed defect (latent)
- **الخطورة:** Low — يفشل حتى إنشاء الحسابات يدويًا.
- **الدليل:** [C] fixed-assets.service.ts:143-146؛ coa.service.ts seed؛ scripts/accounting-p0-gate.cjs:43
- **المحفز (Trigger):** run-monthly.
- **الأثر:** فشل الإهلاك.
- **للتحقق/الإغلاق:** زرع الحسابات أو تغيير الربط.
- **مرجع ملاحظات العمل:** ACC-16(notes)

### ACC-21
**التكلفة المحمّلة والمشتريات العامة سجلات فقط بلا أثر على المخزون أو الخزينة أو GL؛ حالة المشتريات قابلة للتعديل بأي اتجاه**

- **المجال:** Accounting / AP · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed gap
- **الخطورة:** Low — وظائف تسجيلية.
- **الدليل:** [C] landed-cost.service.ts:116-162؛ general-purchases.service.ts:67-129
- **المحفز (Trigger):** —
- **الأثر:** تكلفة المخزون لا تشمل landed cost.
- **للتحقق/الإغلاق:** قرار نطاق.
- **مرجع ملاحظات العمل:** ACC-24(notes)

### ACC-22
**GET /coa/tree يكتب: يزرع دليل الحسابات الافتراضي عند جدول فارغ**

- **المجال:** Accounting / GL · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Improvement
- **الخطورة:** Low — أثر جانبي لطلب قراءة.
- **الدليل:** [C] coa.service.ts:177-198
- **المحفز (Trigger):** أول قراءة.
- **الأثر:** دليل افتراضي غير معتمد.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** ACC-26(notes)

### ACC-23
**CURRENT: تسوية AP مقابل GL بإشارات متعاكسة وبلا فلتر POSTED → انحراف دائم**

- **المجال:** Accounting / Reconciliation · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Inferred · **النوع:** Potential risk
- **الخطورة:** Low — يولد إنذارات كاذبة.
- **الدليل:** [C] supplier-ledger.service.ts:32؛ reconciliation.service.ts:77
- **المحفز (Trigger):** nightly-reconciliation.
- **الأثر:** ضوضاء تخفي الانحرافات الحقيقية.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** ACC-22(notes)

### ARC-01
**هوية الكود العامل في الإنتاج غير مثبتة (tag محلي، image ID مختلف عن label، env مؤقت، تشغيل بـ--no-deps)**

- **المجال:** Architecture / Provenance · **النسخة المتأثرة:** RUNTIME · **درجة التحقق:** Verified (labels) / Unknown (provenance) · **النوع:** Operational uncertainty
- **الخطورة:** High — لا يمكن الجزم بأي كود يعمل؛ كل استنتاج عن سلوك الإنتاج معلّق على هذا الافتراض.
- **الدليل:** [R] runtime.txt: image=nile-pharma-erp/accounting:release-89c2c31، image_id=sha256:0b814f… ≠ com.docker.compose.image=sha256:7dd5c9…، created 2026-09-29 (commit 89c2c31 بتاريخ 2026-09-26 — git-and-schema.txt:13)، environment_file=.env,/tmp/nile-recovery-release.env، depends_on=""؛ [B] docs/SERVER-STEPS-2026-09-25-ar.md (اصطلاح IMAGE_TAG=release-$(git rev-parse --short HEAD) وبناء محلي)
- **المحفز (Trigger):** أي قرار يعتمد على أن الإنتاج = 89c2c31 (إصلاح، rollback، مقارنة schema).
- **الأثر:** قد تكون الصور مبنية من checkout آخر مع إعادة استخدام الـtag؛ rollback غير مضمون لأن الـtag محلي وقابل للاستبدال.
- **للتحقق/الإغلاق:** E-01/E-02/E-05: docker image inspect + فحص محتوى dist داخل الحاوية (يضيّق الاحتمالات ولا يثبت commit بعينه — تصحيح 34).
- **مرجع ملاحظات العمل:** F03-F06 (التقرير السابق), DEPLOY-06

### ARC-02
**مؤشرات غير مثبتة على أن قاعدة البيانات رُحّلت إلى ما بعد BASELINE (accounting وorganization وinventory) — أعداد الجداول لا تثبت الإصدار؛ الحسم بـ_prisma_migrations**

- **المجال:** Architecture / Data · **النسخة المتأثرة:** RUNTIME vs BASELINE · **درجة التحقق:** Inferred · **النوع:** Operational uncertainty
- **الخطورة:** High — أدلة ثانوية متسقة لكنها لا تثبت إصدار القاعدة: تطابق أعداد الجداول قد يحدث بإصدارات مختلفة أو بجداول أُنشئت يدويًا، وقائمة الترحيلات إفادة مستخدم غير مرفقة كمخرجات. يغيّر فهم ما هو 'الإنتاج' إن ثبت. [تصحيح 34]
- **الدليل:** [U] docx.txt:393-395 (nile_accounting 50 جدولًا، organization 26) ويطابق CURRENT (49+1 و25+1) لا BASELINE (36+1 و24+1) — data/schema_cur.json vs schema_base.json؛ [U] docx.txt:811-829 (_prisma_migrations حتى bank_reconciliation)؛ [U] docx.txt:429 (cost layers + outbox في nile_inventory) — CURRENT-only migrations؛ [B] apps/accounting/prisma/migrations ينتهي عند 20260924120000_po_workflow_and_match_sod
- **المحفز (Trigger):** تشغيل كود BASELINE فوق schema أحدث؛ أي rollback لصورة أقدم؛ نشر CURRENT.
- **الأثر:** الجداول الجديدة فارغة على الأغلب؛ لا rollback لقاعدة البيانات دون DDL يدوي؛ بيئات جديدة من git لن تطابق الإنتاج. تحليل التوافق يشير إلى أن كود BASELINE يعمل فوق الامتداد (migrations إضافية) — Inferred.
- **للتحقق/الإغلاق:** E-03/E-04: _prisma_migrations + information_schema.tables لكل قاعدة (metadata فقط).
- **مرجع ملاحظات العمل:** ACC-01(notes), DEPLOY-06, INVPRD-27, F11

### ARC-03
**تعريف PostgreSQL الإنتاجي خارج git (docker-compose.postgres.yml وشبكة nile-internal وvolume nile_postgres_data غير موجودة في أي snapshot)**

- **المجال:** Architecture / DR · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (غياب في المستودع) + [U] تشغيل · **النوع:** Potential risk
- **الخطورة:** High — نظام السجل الوحيد (9 قواعد على PG18) غير قابل لإعادة الإنشاء من المصدر.
- **الدليل:** grep في base/ وcur/ لا يجد docker-compose.postgres.yml أو nile-internal أو nile_postgres_data؛ [U] docx.txt:212-272؛ [C] docs/PRODUCTION-HOSTINGER.md:74 'No PostgreSQL runs on the VPS'؛ [C] scripts/merge-launcher.test.js:109-110
- **المحفز (Trigger):** فقدان المضيف، ترقية PG، إعادة بناء الخادم.
- **الأثر:** لا توجد صورة/إعداد/credentials bootstrap موثقة؛ RTO غير معروف.
- **للتحقق/الإغلاق:** E-07: docker inspect nile-postgres (labels، image، mounts) دون env؛ استرجاع الملف أو إعادة بنائه وحفظه (بدون أسرار).
- **مرجع ملاحظات العمل:** DEPLOY-01

### ARC-04
**البنية الموثقة تتعارض مع الكود والتشغيل (Neon/Railway/Vercel مقابل VPS + PG18 محلي)**

- **المجال:** Architecture / Documentation · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — لا أثر تشغيلي مباشر، لكنه سبب جذري لأدوات نشر وDR تستهدف منصة خاطئة (OPS-01, OPS-04).
- **الدليل:** [C] README.md:93-97؛ [B]/[C] docker-compose.production.yml:5-9 و190-198 (تعليقات Neon)؛ [C] docs/PRODUCTION-LAST-MILE.md:35-41؛ [C] docs/audit/02-architecture.md:12-30 (Railway)؛ PRODUCTION_HARDENING.md:13-15 (Vercel)؛ [R] runtime.txt DATABASE_URL→nile-postgres
- **المحفز (Trigger):** الاعتماد على الوثائق في التشغيل أو الاستعادة.
- **الأثر:** إجراءات خاطئة وقت الأزمات.
- **للتحقق/الإغلاق:** قرار المالك حول المنصة المستهدفة ثم وثيقة نشر واحدة معتمدة.
- **مرجع ملاحظات العمل:** REQDOC-14, DEPLOY-16, C1-C5

### ARC-05
**CURRENT: ثماني وحدات محاسبية (في سبعة مجلدات) غير مسجلة في AppModule (35 route) بينما الواجهة تستدعي 12 منها**

- **المجال:** Architecture / Accounting · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (static, script) · **النوع:** Confirmed defect
- **الخطورة:** High — يمنع النشر: شاشات الدفع للموردين وGL workbench ولوحات المالية ستعيد 404. · **مانع نشر لـCURRENT**
- **الدليل:** [C] apps/accounting/src/app.module.ts:39-51؛ 05-API-Inventory-and-Routing.md §3 (gl-workbench 8، finance-dashboard 1، audit-timeline 1، supplier-payments 2)؛ [C] apps/web/lib/api.ts:264-272, 2477, 2483, 2652-2653؛ [C] apps/web/app/dashboard/payables/page.tsx:344
- **المحفز (Trigger):** نشر CURRENT واستخدام Payables/GL workbench/finance-dashboard/audit-timeline.
- **الأثر:** وظائف موثقة كـ'مكتملة' غير موجودة فعليًا؛ تعارض بين تطبيقين لـsupplier-payments.
- **للتحقق/الإغلاق:** قرار أي تنفيذ هو المعتمد، ثم تسجيله مع PermissionsGuard واختبار end-to-end.
- **مرجع ملاحظات العمل:** ACC-08, WEBEVT-01

### ARC-06
**لا هوية للخدمات: الاتصالات بين الخدمات تتم بتوكن المستخدم النهائي**

- **المجال:** Architecture / Security · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Improvement
- **الخطورة:** Low — تصميم مقبول لنظام داخلي صغير لكنه يربط صلاحيات المستخدم بمجالات أخرى.
- **الدليل:** [C] apps/accounting/src/modules/invoices/invoices.service.ts:242-247؛ [C] apps/products/.../products.controller.ts:48 (public-prices يتطلب accounting.invoices.create)
- **المحفز (Trigger):** انتهاء صلاحية توكن المستخدم أثناء سلسلة طويلة؛ مستخدم بلا صلاحية مجال آخر.
- **الأثر:** فشل عمليات مشروعة؛ منح صلاحيات أوسع من اللازم.
- **للتحقق/الإغلاق:** تقرير معماري لاحق (service tokens).
- **مرجع ملاحظات العمل:** SEC-08

### DB-01
**تاريخ migrations المحاسبة عُدّل يدويًا (ROLLED_BACK ثم APPLIED بـ0 steps) وملفات migrations عُدّلت بعد إنشائها**

- **المجال:** Database / Migrations · **النسخة المتأثرة:** RUNTIME + CURRENT · **درجة التحقق:** Verified (git) / Inferred (DB من وصف المستخدم) · **النوع:** Operational uncertainty
- **الخطورة:** High — لا يُعرف أي نسخة SQL أنشأت الجداول المالية فعليًا؛ checksums على الأغلب لا تطابق الملفات.
- **الدليل:** [R] accounting-migration-history.txt (general_ledger عُدّل في 8954eb3, ba88bd6, cfec643, 40bcd36, 10f1515؛ gl_workbench في e9d6d81, 3fbb59d, df51cb3؛ financial_instruments ×3)؛ [U] docx.txt:811-829
- **المحفز (Trigger):** أي migrate deploy لاحق، أو بناء بيئة من الصفر.
- **الأثر:** انحراف دائم بين DDL المستودع والإنتاج؛ resolve يدوي بلا runbook أو تفويض موثق.
- **للتحقق/الإغلاق:** E-03: checksums من _prisma_migrations مقارنة بـsha256sum للملفات؛ سؤال Q-OPS-3 عن من نفّذ resolve.
- **مرجع ملاحظات العمل:** ACC-01(notes), DEPLOY-12, F12

### DB-02
**CURRENT: schema.prisma لا يطابق migrations المحاسبة (22 اختلافًا) → بوابة الإصدار ترفض وdb-migrate يخرج بالكود 3 ويوقف كل الخدمات**

- **المجال:** Database / Release · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (تشغيل validator ساكن على النسختين) · **النوع:** Confirmed defect
- **الخطورة:** High — مع `up` عادي لا تبدأ أي خدمة لأن الجميع ينتظر db-migrate. · **مانع نشر لـCURRENT**
- **الدليل:** تشغيل `node scripts/validate-schema-migrations.cjs`: BASELINE ✅ / CURRENT ❌ (journal_entries.entry_number، journal_lines.cost_center_id، supplier_payments.vendor_invoice_id…)؛ [B]/[C] scripts/production-migrate.sh:95-100 (exit 3)؛ [C] docker-compose.production.yml:114-118 (depends_on service_completed_successfully)؛ [U] docx: db-migrate Exited(3)
- **المحفز (Trigger):** نشر CURRENT بالمسار القياسي.
- **الأثر:** توقف كامل للنشر؛ يدفع لمسارات استرداد يدوية (مصدر الانحراف الحالي).
- **للتحقق/الإغلاق:** توحيد شكل جداول GL وsupplier_payments ثم إعادة تشغيل validator؛ بعض الـ'missing' false positives من parser.
- **مرجع ملاحظات العمل:** DEPLOY-05

### DB-03
**شكلان متنافسان لجداول GL ولـsupplier_payments في migrations (legacy مقابل workbench؛ v1 مقابل v2) — شكل الإنتاج غير معروف**

- **المجال:** Database / Accounting · **النسخة المتأثرة:** CURRENT + RUNTIME · **درجة التحقق:** Inferred · **النوع:** Operational uncertainty
- **الخطورة:** High — يحدد ما إذا كان أي كود GL/AP في CURRENT قابلًا للعمل.
- **الدليل:** [C] prisma/migrations/20260927120000_general_ledger/migration.sql:6-13,28؛ 20260928110000_gl_workbench/migration.sql:57-74 (على قاعدة جديدة تُطبق السلسلة كاملة: v1 لـsupplier_payments يفوز لأن v2 يستخدم IF NOT EXISTS، وgl_workbench يضيف أعمدة ويبقي أعمدة legacy NOT NULL → كلا كاتبي GL يفشل — تحقق مستقل، Inferred)؛ 20260927143000_supplier_payments vs 20260928090000_supplier_payments؛ scripts/accounting-migration-reconciliation.test.cjs:17-18
- **المحفز (Trigger):** تشغيل أي مسار GL أو دفع موردين.
- **الأثر:** سيناريو A أو B يكسر أحد الكاتبين؛ كود supplier-payments A لا يعمل مع شكل v2.
- **للتحقق/الإغلاق:** E-03b: \d+ journal_entries/journal_lines/supplier_payments (metadata).
- **مرجع ملاحظات العمل:** ACC §5.2

### DB-04
**لا تكامل مرجعي عبر الخدمات: مراجع منطقية (*Id) بلا FK، والـsaga تضع 'unknown' و0 عند غياب الحقول**

- **المجال:** Database / Data ownership · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (schema + code) · **النوع:** Potential risk
- **الخطورة:** Low — نتيجة متوقعة لنمط database-per-service، لكن لا توجد أداة مطابقة عبر القواعد.
- **الدليل:** data/schema_stats.md (accounting 78، sales 38، inventory 36 مرجعًا منطقيًا)؛ [C] apps/accounting/src/modules/saga-listener/saga-listener.service.ts:138-143
- **المحفز (Trigger):** حذف/أرشفة master data، أحداث ناقصة.
- **الأثر:** سجلات يتيمة أو أطراف وهمية؛ التسوية تحتاج أدوات عبر القواعد.
- **للتحقق/الإغلاق:** E-12: count(*) WHERE account_id='unknown' OR total=0.
- **مرجع ملاحظات العمل:** ACC-25, INVPRD-09

### DB-05
**لا قيود CHECK على أرصدة المخزون (on_hand>=0, reserved<=on_hand) — المنع في التطبيق فقط**

- **المجال:** Database / Inventory · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Low — التطبيق يمنع السالب في معظم المسارات؛ مسار release غير serializable.
- **الدليل:** [C] apps/inventory/prisma/migrations (CHECK الوحيد في 20260927170000_inventory_cost_layers:16)؛ allocation.engine.ts:718-738
- **المحفز (Trigger):** تزامن cancel+ship أو أخطاء مستقبلية.
- **الأثر:** أرصدة سالبة صامتة.
- **للتحقق/الإغلاق:** E-11: count of negative balances.
- **مرجع ملاحظات العمل:** INVPRD-13

### DB-06
**فهارس وقيود: 23 عمود FK بلا index، و7 حقول status نصية حرة، وحقول audit ناقصة (heuristic)**

- **المجال:** Database / Quality · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (فحص آلي heuristic) · **النوع:** Improvement
- **الخطورة:** Low — حجم البيانات صغير جدًا حاليًا (8-11MB لكل قاعدة حسب [U]).
- **الدليل:** data/schema_stats.md الأقسام 'FK بلا index' و'status كنص حر'
- **المحفز (Trigger):** نمو البيانات.
- **الأثر:** أداء ونزاهة حالات.
- **للتحقق/الإغلاق:** مراجعة فهرسة عند تصميم الإصلاح.
- **مرجع ملاحظات العمل:** auto-scan

### DB-07
**عدم تطابق Prisma مع SQL في جداول GL (fiscalPeriodId إلزامي في Prisma وnullable في SQL، currency enum مقابل TEXT)**

- **المجال:** Database / Accounting · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — قراءة صفوف GL عبر Prisma ستفشل لصفوف كتبها GeneralLedgerService بلا فترة.
- **الدليل:** [C] apps/accounting/prisma/schema.prisma (JournalEntry/JournalLine)؛ general-ledger.service.ts:10-14
- **المحفز (Trigger):** تشغيل CURRENT.
- **الأثر:** أخطاء قراءة/تقارير.
- **للتحقق/الإغلاق:** توحيد النموذج.
- **مرجع ملاحظات العمل:** ACC §5.2

### DB-08
**Backfill لمرة واحدة في vendor_invoice_fx: فواتير موردين ينشئها كود BASELINE بعد الـmigration تبقى base_total=0**

- **المجال:** Database / AP · **النسخة المتأثرة:** RUNTIME (إن صح ARC-02) · **درجة التحقق:** Inferred · **النوع:** Potential risk
- **الخطورة:** Low — لا يقرأ BASELINE هذا العمود؛ يظهر الأثر عند نشر CURRENT فقط.
- **الدليل:** [C] prisma/migrations/20260928143000_vendor_invoice_fx/migration.sql
- **المحفز (Trigger):** نشر CURRENT فوق بيانات أنشأها BASELINE.
- **الأثر:** تقارير AP بالعملة الأساسية خاطئة.
- **للتحقق/الإغلاق:** E-12: count vendor_invoices WHERE base_total=0 AND total_amount>0.
- **مرجع ملاحظات العمل:** ACC §5.2

### DB-09
**اختلاف نسخة PostgreSQL بين البيئات (18 إنتاج، 16 تطوير/CI، بوابة parity مثبتة على 16)**

- **المجال:** Database / Platform · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (code) + [U] · **النوع:** Potential risk
- **الخطورة:** Medium — الاختبارات لا تمثل محرك الإنتاج.
- **الدليل:** [C] docker-compose.yml (postgres:16)؛ ci.yml؛ docker-compose.ci-production.yml:7؛ [U] docx.txt:198-200
- **المحفز (Trigger):** سلوك مختلف بين النسخ في migrations.
- **الأثر:** أخطاء تظهر في الإنتاج فقط.
- **للتحقق/الإغلاق:** توحيد النسخة.
- **مرجع ملاحظات العمل:** DEPLOY-13

### DB-10
**ترقيم المستندات غير تسلسلي (INV-<base36 ms>، SO-<base36>-uuid)**

- **المجال:** Database / Compliance · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Question
- **الخطورة:** Low — يعتمد على متطلبات الضرائب/ETA غير المحسومة.
- **الدليل:** [C] invoices.service.ts:444, 715, 1018؛ orders.service.ts:647
- **المحفز (Trigger):** تدقيق ضريبي.
- **الأثر:** قد لا يقبل كترقيم رسمي.
- **للتحقق/الإغلاق:** سؤال للمالك (Q-ACC-5).
- **مرجع ملاحظات العمل:** ACC-19, SCI-31

### DB-11
**لا سياسة احتفاظ/أرشفة لجداول audit وoutbox وprocessed_events وjob_runs وDLQ**

- **المجال:** Database / Operations · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (غياب) · **النوع:** Improvement
- **الخطورة:** Low — الحجم الحالي صغير.
- **الدليل:** grep لا يجد retention/deleteMany
- **المحفز (Trigger):** نمو طويل الأمد.
- **الأثر:** تضخم وتباطؤ verify.
- **للتحقق/الإغلاق:** قرار سياسة الاحتفاظ.
- **مرجع ملاحظات العمل:** WEBEVT-18

### DB-12
**إيجابي: المبالغ المالية Decimal بدقة صريحة في كل الخدمات (لا Float)، مع اختلاف scales (14,2 / 18,2 / 18,4)**

- **المجال:** Database / Financial precision · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (فحص آلي) · **النوع:** Improvement
- **الخطورة:** Info — ضابط جيد؛ اختلاف الـscale يحتاج قاعدة تقريب موحدة.
- **الدليل:** data/schema_stats.md؛ فحص أنواع الحقول المالية (75 حقلًا Decimal في accounting)
- **المحفز (Trigger):** —
- **الأثر:** فروق تقريب بين تكلفة المخزون (4 منازل) والقيود (2).
- **للتحقق/الإغلاق:** توثيق قاعدة التقريب.
- **مرجع ملاحظات العمل:** auto-scan

### GOV-01
**لا يوجد baseline متطلبات معتمد وموقّع؛ القرارات تفريغ لإجابات المالك بلا اسم معتمِد، وعمود الحالة يكتبه المنفذ**

- **المجال:** Governance / Requirements · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — يعيق الاختبار والقبول.
- **الدليل:** [C] docs/DECISIONS-2026-09-25-ar.md:3؛ docs/P1-BUSINESS-DECISION-PACK.md:422-430؛ docs/GO-LIVE-ACCEPTANCE-REPORT.md:7-8
- **المحفز (Trigger):** القبول.
- **الأثر:** لا مرجع للحكم على الصحة.
- **للتحقق/الإغلاق:** Q-GOV-1.
- **مرجع ملاحظات العمل:** REQDOC-01

### GOV-02
**RTM و'Go-live gate' و'DR drill' السابقة لا تصلح كدليل (فحوص وجود ملفات/نصوص، أرقام متناقضة، أدلة ملفقة سُحبت)**

- **المجال:** Governance / QA · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed defect (documentation)
- **الخطورة:** Medium — ادعاءات 'VERIFIED 100%' مضللة.
- **الدليل:** [C] docs/REQUIREMENTS-TRACEABILITY-MATRIX.md:22؛ scripts/go-live-acceptance-gate.cjs:60-62, 143-170؛ docs/DISASTER-RECOVERY-DRILL-REPORT.md:3-10
- **المحفز (Trigger):** —
- **الأثر:** ثقة زائفة.
- **للتحقق/الإغلاق:** إعادة بناء RTM.
- **مرجع ملاحظات العمل:** REQDOC-02/03/04

### GOV-03
**قرارات 2026-09-28 (ترقيم PO، مطابقة الاستلام الفعلي، سقف الخصم، سداد الموردين، FX المحقق) موجودة في CURRENT فقط**

- **المجال:** Governance / Business · **النسخة المتأثرة:** BASELINE · **درجة التحقق:** Verified (static) · **النوع:** Operational uncertainty
- **الخطورة:** Medium — ضوابط قررها المالك غير موجودة في النسخة المرجحة للإنتاج.
- **الدليل:** [C] docs/P1-BUSINESS-DECISION-PACK.md:424-429؛ انظر ACC-19, SAL-04, ACC-10
- **المحفز (Trigger):** —
- **الأثر:** —
- **للتحقق/الإغلاق:** ARC-01.
- **مرجع ملاحظات العمل:** REQDOC-05

### GOV-04
**قرارات متعارضة أو غير مسجلة (نموذج التسعير 09-25 مقابل 09-28؛ FX M2 مقابل المحقق؛ BD-2/BD-7 منفذة بلا قرار)**

- **المجال:** Governance / Business · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (text) · **النوع:** Question
- **الخطورة:** Medium — يجب حسمها قبل أي إصلاح.
- **الدليل:** [C] docs/DECISIONS-2026-09-25-ar.md:19-23؛ P1-BUSINESS-DECISION-PACK.md:198, 428-429
- **المحفز (Trigger):** —
- **الأثر:** —
- **للتحقق/الإغلاق:** Q-GOV-2..4.
- **مرجع ملاحظات العمل:** REQDOC-12/13

### GOV-05
**متطلبات مقررة غير منفذة في أي نسخة: البونص، فرز التالف، مطالبات الموردين، حد ائتمان بالعلب، مخزن/خزنة المندوب**

- **المجال:** Governance / Scope · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (grep) · **النوع:** Question
- **الخطورة:** Info — فجوة نطاق لا defect.
- **الدليل:** REQ-14, REQ-17, REQ-18, REQ-20, REQ-42 في 10-Business-Process-Gap
- **المحفز (Trigger):** —
- **الأثر:** عمل يدوي خارج النظام.
- **للتحقق/الإغلاق:** Q-GOV.
- **مرجع ملاحظات العمل:** REQDOC-16

### GOV-06
**وثائق قديمة ومعاملات تنظيمية مكتوبة في الكود بلا اعتماد (التأمينات 11%/18.75%، شرائح الضريبة، عتبة 100,000، خصم 12%)**

- **المجال:** Governance / Documentation · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Improvement
- **الخطورة:** Low — —
- **الدليل:** [C] apps/organization/.../attendance.service.ts:221-243؛ orders.service.ts:20-21؛ docs (REQDOC-15)
- **المحفز (Trigger):** —
- **الأثر:** —
- **للتحقق/الإغلاق:** Q-GOV.
- **مرجع ملاحظات العمل:** REQDOC-15/17, DEPLOY-16

### INT-01
**معظم الأحداث تُكتب بشكل مزدوج (commit ثم publish مباشر) بلا outbox؛ outbox موجود في accounting (المدفوعات) وcrm (onboarding) وinventory (CURRENT فقط)**

- **المجال:** Integration / Consistency · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (code) / Inferred (failure) · **النوع:** Potential risk
- **الخطورة:** High — تشمل الأحداث الحرجة: InvoiceGenerated، StockReserveRequested، GoodsReceived (BASELINE)، SupplierReturnCreated، RecallInitiated.
- **الدليل:** out/notes web-events-audit.md §3.4 (عمود Publish mode)؛ [C] invoices.service.ts:543, 882, 1108, 1237؛ [B] apps/inventory/.../transactions.service.ts:93-108؛ packages/events/src/publisher.ts:241-270
- **المحفز (Trigger):** تعطل Redpanda بين commit والنشر.
- **الأثر:** خدمات غير متزامنة دائمًا؛ 500 للمستخدم بعد نجاح الكتابة.
- **للتحقق/الإغلاق:** E-24: grep 'EVENT NOT DELIVERED' وDLQ publisher.
- **مرجع ملاحظات العمل:** WEBEVT-05, ACC-20, INVPRD-03, SCI-06

### INT-02
**علامة dedup تُكتب بعد المعالج وخارج معاملته، ومعالجات متعددة الكتابة → تطبيق مزدوج عند إعادة المحاولة**

- **المجال:** Integration / Idempotency · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (mechanism) / Inferred (impact) · **النوع:** Potential risk
- **الخطورة:** Medium — يؤثر على الائتمان والتحصيل والمرتجعات.
- **الدليل:** packages/events/src/consumer.ts:290-316, 358-386؛ apps/sales/.../saga.orchestrator.ts:446-484؛ apps/inventory/.../reservation.listener.ts:361-400
- **المحفز (Trigger):** فشل جزئي داخل المعالج.
- **الأثر:** انحراف outstanding/collectedAmount/المخزون.
- **للتحقق/الإغلاق:** transactional inbox.
- **مرجع ملاحظات العمل:** WEBEVT-09, SCI-07, INVPRD-12

### INT-03
**الأحداث ذات التوقيع المرفوض تُسقط دون أثر دائم (لا DLQ ولا audit)**

- **المجال:** Integration / Integrity · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — تدوير EVENT_SIGNATURE_PEPPER غير متزامن يفقد كل أحداث خدمة.
- **الدليل:** packages/events/src/consumer.ts:282, 333-351
- **المحفز (Trigger):** اختلاف السر.
- **الأثر:** آثار أعمال مفقودة.
- **للتحقق/الإغلاق:** E-24 grep 'REJECTED envelope'.
- **مرجع ملاحظات العمل:** WEBEVT-08

### INT-04
**Redpanda عقدة واحدة، والمواضيع تُنشأ تلقائيًا بإعدادات افتراضية (partitions/retention/RF غير معرّفة)**

- **المجال:** Integration / Platform · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (absence) / Unknown (runtime) · **النوع:** Operational uncertainty
- **الخطورة:** Medium — فقد القرص = فقد الأحداث غير المستهلكة وDLQ.
- **الدليل:** docker-compose.production.yml (redpanda --smp 1)؛ publisher.ts:129, 233؛ [U] docx: Redpanda ≈2GiB RAM
- **المحفز (Trigger):** فقد القرص/إعادة التشغيل.
- **الأثر:** فقد أحداث؛ ترتيب غير مضمون إذا partitions>1.
- **للتحقق/الإغلاق:** E-25 rpk metadata.
- **مرجع ملاحظات العمل:** WEBEVT-11

### INT-05
**CURRENT: المستهلكون يبدأون من 'latest' → ترتيب النشر قد يفقد أحداث inventory.stock.issued الجديدة**

- **المجال:** Integration / Rollout · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Inferred · **النوع:** Operational uncertainty
- **الخطورة:** Medium — يعتمد على ترتيب نشر الخدمات. · **مانع نشر لـCURRENT**
- **الدليل:** packages/events/src/consumer.ts:266؛ [C] saga-listener.service.ts:54,62
- **المحفز (Trigger):** نشر inventory قبل accounting.
- **الأثر:** قيود COGS مفقودة.
- **للتحقق/الإغلاق:** خطة rollout.
- **مرجع ملاحظات العمل:** WEBEVT-07

### INT-06
**عقود الأحداث بلا إصدار، وانحراف payloads، و3 أحداث بلا منتج**

- **المجال:** Integration / Contracts · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Improvement
- **الخطورة:** Low — لا مستهلك يعتمد على الحقول المنحرفة حاليًا.
- **الدليل:** packages/contracts/src/generated/events.ts:26-35, 890-901
- **المحفز (Trigger):** —
- **الأثر:** كسر صامت مستقبلًا.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** WEBEVT-10

### INT-07
**المجدول: صف job_runs قد يبقى RUNNING للأبد عند timeout، والقفل يمنع التزامن فقط**

- **المجال:** Integration / Scheduler · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Inferred · **النوع:** Potential risk
- **الخطورة:** Low — نسخة واحدة لكل خدمة حاليًا.
- **الدليل:** packages/scheduler/src/job-runner.ts:6-12, 43-87
- **المحفز (Trigger):** timeout.
- **الأثر:** مراقبة مضللة.
- **للتحقق/الإغلاق:** E-19 RUNNING > 1h.
- **مرجع ملاحظات العمل:** WEBEVT-19

### INV-01
**CURRENT: طبقات تكلفة FIFO تُنشأ عند الاستلام وتُستهلك فقط في الفواتير المباشرة؛ بقية الحركات لا تحدّثها**

- **المجال:** Inventory / Costing · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (code) / Inferred (impact) · **النوع:** Confirmed defect (latent)
- **الخطورة:** High — فوترة مباشرة مرفوضة (409) أو COGS خاطئ وتقييم مضخم. · **مانع نشر لـCURRENT**
- **الدليل:** [C] apps/inventory/src/modules/transactions/transactions.service.ts:90-96؛ allocation.engine.ts:454-481؛ لا backfill
- **المحفز (Trigger):** تحويل ثم فاتورة مباشرة؛ مخزون قديم.
- **الأثر:** COGS/تقييم خاطئ.
- **للتحقق/الإغلاق:** قرار طريقة التكلفة (Q-INV-1).
- **مرجع ملاحظات العمل:** INVPRD-01

### INV-02
**CURRENT: إلغاء الصرف المباشر لا يعيد طبقات التكلفة ولا يلغي حدث StockIssued → قيد COGS بلا فاتورة**

- **المجال:** Inventory / Accounting · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified · **النوع:** Confirmed defect (latent)
- **الخطورة:** High — قيد تكلفة لفاتورة غير موجودة. · **مانع نشر لـCURRENT**
- **الدليل:** [C] allocation.engine.ts:531-538, 582-641؛ apps/accounting/.../saga-listener.service.ts:297-316
- **المحفز (Trigger):** فشل معاملة الفاتورة بعد issue-direct.
- **الأثر:** GL مخزون/تكلفة خاطئ.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** INVPRD-02

### INV-03
**أحداث دورة حياة الدفعات والأسعار في Products بلا outbox؛ فقدان RecallInitiated لا يمكن إعادته**

- **المجال:** Products / Quality · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (code) / Inferred (impact) · **النوع:** Potential risk
- **الخطورة:** High — دواء مستدعى قد يبقى قابلًا للحجز في المخزون.
- **الدليل:** [C] apps/products/src/modules/batches/batches.service.ts:147-148, 165-176, 245-265
- **المحفز (Trigger):** فشل Kafka لحظة إجراء الجودة.
- **الأثر:** تباين حالة الدفعة بين Products وInventory/Sales.
- **للتحقق/الإغلاق:** E-18 مقارنة batches.status بـblocked_batches.
- **مرجع ملاحظات العمل:** INVPRD-04

### INV-04
**بضاعة تُستلم بعد إفراج الدفعة تبقى في الحجر ولا تُفرج تلقائيًا**

- **المجال:** Inventory / QC · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Inferred · **النوع:** Potential risk
- **الخطورة:** Medium — مخزون مخفي ونقص في التخصيص.
- **الدليل:** [C] transactions.service.ts:65؛ reservation.listener.ts:410-415؛ batches.service.ts:147
- **المحفز (Trigger):** استلام ثانٍ لدفعة RELEASED.
- **الأثر:** رفض حجوزات.
- **للتحقق/الإغلاق:** E-18 query.
- **مرجع ملاحظات العمل:** INVPRD-05

### INV-05
**CURRENT: تقرير التقييم يعد الطبقات مرتين عند وجود أكثر من pool للدفعة في المخزن**

- **المجال:** Inventory / Reporting · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — تقرير فقط.
- **الدليل:** [C] apps/inventory/src/modules/stock/stock.service.ts:43-57
- **المحفز (Trigger):** دفعة موزعة على pools.
- **الأثر:** قيمة مخزون مضخمة.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** INVPRD-06

### INV-06
**مهمة stock-conservation تعدّ استلامات الحجر مرتين → انحراف كاذب في كل تشغيل**

- **المجال:** Inventory / Reconciliation · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (SQL read) · **النوع:** Confirmed defect
- **الخطورة:** Medium — التسوية الآلية الوحيدة للمخزون غير مفيدة.
- **الدليل:** [C] apps/inventory/src/modules/jobs/inventory-jobs.ts:67-74؛ transactions.service.ts:78-106
- **المحفز (Trigger):** أي استلام للحجر.
- **الأثر:** إخفاء الانحراف الحقيقي.
- **للتحقق/الإغلاق:** E-19 job_runs.
- **مرجع ملاحظات العمل:** INVPRD-07

### INV-07
**شحن طلبات المبيعات لا ينتج COGS؛ الفواتير المباشرة فقط (CURRENT)**

- **المجال:** Inventory / Accounting · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Question
- **الخطورة:** Medium — هامش الربح غير مكتمل.
- **الدليل:** [C] allocation.engine.ts:783-831
- **المحفز (Trigger):** شحن طلب.
- **الأثر:** GL مخزون/COGS لا يتبع الحركة.
- **للتحقق/الإغلاق:** Q-INV-1.
- **مرجع ملاحظات العمل:** INVPRD-08

### INV-08
**الاستلام يقبل أي productId/batchId/supplierId وتاريخ انتهاء من العميل دون تحقق من Products**

- **المجال:** Inventory / Master data · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — يؤثر على FEFO ونطاق الاستدعاء.
- **الدليل:** [C] transactions/dto/goods-receipt.dto.ts:2-11؛ transactions.service.ts:70-77
- **المحفز (Trigger):** خطأ إدخال.
- **الأثر:** ترتيب FEFO خاطئ.
- **للتحقق/الإغلاق:** E-18 مقارنة.
- **مرجع ملاحظات العمل:** INVPRD-09

### INV-09
**لا مفتاح idempotency للاستلام ومرتجع المورد والتسويات وتحميل الأمانة والشطب**

- **المجال:** Inventory / Commands · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — النقر المزدوج يكرر الحركة وقيد AP.
- **الدليل:** [C] DTOs: goods-receipt, supplier-return, stock-adjustment, add-stock, write-off
- **المحفز (Trigger):** إعادة إرسال بعد 5xx.
- **الأثر:** حركات مكررة.
- **للتحقق/الإغلاق:** E-19 duplicates.
- **مرجع ملاحظات العمل:** INVPRD-10

### INV-10
**زيادة المخزون بالتسوية بلا حد ولا اعتماد، والعتبة كمية لا قيمة**

- **المجال:** Inventory / Controls · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Question
- **الخطورة:** Medium — خلق مخزون دون رقابة.
- **الدليل:** [C] transactions.service.ts:21, 252-253
- **المحفز (Trigger):** FOUND_STOCK كبير.
- **الأثر:** مخزون وهمي.
- **للتحقق/الإغلاق:** Q-INV-4.
- **مرجع ملاحظات العمل:** INVPRD-16

### INV-11
**لا مسار إتلاف/إرجاع للمخزون التالف أو المحجور، ولا عملية جرد**

- **المجال:** Inventory / Process · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed gap
- **الخطورة:** Medium — التالف يتراكم بلا مخرج.
- **الدليل:** [C] transactions.service.ts:45-59؛ quarantine.service.ts:19-25؛ inventory-jobs.ts
- **المحفز (Trigger):** رفض دفعة.
- **الأثر:** أرصدة غير حقيقية.
- **للتحقق/الإغلاق:** Q-INV-3, Q-INV-7.
- **مرجع ملاحظات العمل:** INVPRD-17, P17

### INV-12
**مسار قائمة الأسعار غالبًا مظلّل بـGET /products/:id**

- **المجال:** Products / API · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Inferred (not executed) · **النوع:** Potential risk
- **الخطورة:** Medium — شاشة قوائم الأسعار قد لا تعمل.
- **الدليل:** [C] price-lists.controller.ts:11؛ products.controller.ts:53؛ app.module.ts:31؛ apps/web/lib/api.ts:1296
- **المحفز (Trigger):** فتح الشاشة.
- **الأثر:** 404.
- **للتحقق/الإغلاق:** E-20 (بيئة اختبار فقط).
- **مرجع ملاحظات العمل:** INVPRD-18

### INV-13
**نقاط issue-direct/rollback-direct قابلة للاستدعاء مباشرة لأي حامل accounting.invoices.create**

- **المجال:** Inventory / Authorization · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified / Inferred · **النوع:** Potential risk
- **الخطورة:** Medium — صرف مخزون بلا فاتورة (وفي CURRENT قيد COGS).
- **الدليل:** [C] apps/inventory/src/modules/allocation/allocation.controller.ts:59-68
- **المحفز (Trigger):** استدعاء API عبر /api/inventory/allocation/*.
- **الأثر:** نقص مخزون غير مبرر.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** INVPRD-25

### INV-14
**BASELINE: تحميل الأمانة لا يرفض الدفعات المنتهية/المحظورة (شرط المالك قبل الاستخدام الإنتاجي)**

- **المجال:** Inventory / Consignment · **النسخة المتأثرة:** BASELINE · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — ضابط صلاحية دوائي.
- **الدليل:** [B] consignment.service.ts:121-140 مقابل [C] :128, 159-177؛ [C] docs/DECISIONS-2026-09-25-ar.md:105-106
- **المحفز (Trigger):** تحميل أمانة.
- **الأثر:** دواء منتهي لدى العميل.
- **للتحقق/الإغلاق:** E-21 consignment_stock منتهية.
- **مرجع ملاحظات العمل:** REQDOC-06

### INV-15
**ثغرات تزامن ثانوية (release غير serializable، عكس التسوية، رفض طلب التسوية غير مشروط)**

- **المجال:** Inventory / Concurrency · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Inferred · **النوع:** Potential risk
- **الخطورة:** Low — تتطلب تزامنًا نادرًا.
- **الدليل:** [C] allocation.engine.ts:718-738؛ transactions.service.ts:346-354, 379-401
- **المحفز (Trigger):** طلبات متزامنة.
- **الأثر:** أرصدة/حالات خاطئة.
- **للتحقق/الإغلاق:** E-11.
- **مرجع ملاحظات العمل:** INVPRD-13/14/15

### INV-16
**وحدات القياس غير مستخدمة في كميات المخزون، والمواقع الداخلية (bins) قائمة رئيسية فقط**

- **المجال:** Inventory / Master data · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Question
- **الخطورة:** Info — قد يكون مقصودًا.
- **الدليل:** [C] apps/products/src/modules/uom/uom.service.ts؛ apps/inventory/prisma/schema.prisma:63-72
- **المحفز (Trigger):** —
- **الأثر:** —
- **للتحقق/الإغلاق:** Q-INV-6, Q-INV-8.
- **مرجع ملاحظات العمل:** INVPRD-22/24

### INV-17
**CURRENT: outbox المخزون بلا backoff ولا حماية تداخل ولا يحترم OUTBOX_DISPATCH_ENABLED**

- **المجال:** Inventory / Integration · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — رسالة سامة تعطل GoodsReceived/StockIssued.
- **الدليل:** [C] apps/inventory/src/modules/transactions/inventory-outbox.service.ts:12, 35-80
- **المحفز (Trigger):** خطأ نشر مستمر.
- **الأثر:** تأخير قيود AP/COGS.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** INVPRD-11, WEBEVT-06

### OPS-01
**أدوات نشر CURRENT تفترض Neon (فحص nc من المضيف، snapshot عبر Neon API، parity 16) بينما الإنتاج nile-postgres محلي**

- **المجال:** Operations / Deploy · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (code) / Inferred (effect) · **النوع:** Confirmed defect
- **الخطورة:** High — نقطة الاستعادة 'الإلزامية' تحمي قاعدة خاطئة أو تمنع النشر. · **مانع نشر لـCURRENT**
- **الدليل:** [C] scripts/deploy-production.sh:72-80, 94-110؛ docs/PRODUCTION-LAST-MILE.md؛ ci.yml (NEON_POSTGRES_MAJOR_VERSION==16)
- **المحفز (Trigger):** تشغيل النشر الآلي.
- **الأثر:** فشل أو نشر بلا نسخة احتياطية فعلية.
- **للتحقق/الإغلاق:** Q-OPS-1.
- **مرجع ملاحظات العمل:** DEPLOY-02

### OPS-02
**--remove-orphans في النشر/الـrollback الآلي قد يحذف حاوية nile-postgres إن كانت تحمل label المشروع**

- **المجال:** Operations / Deploy · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (code) / Inferred (label) · **النوع:** Potential risk
- **الخطورة:** High — انقطاع كامل؛ والـrollback يكرره. · **مانع نشر لـCURRENT**
- **الدليل:** [C] scripts/deploy-production.sh:140؛ rollback-production.sh:20؛ docs/OPERATIONS-RUNBOOK.md:9 يمنعه
- **المحفز (Trigger):** نشر CURRENT.
- **الأثر:** حذف حاوية القاعدة (الـvolume يبقى).
- **للتحقق/الإغلاق:** E-07: labels لـnile-postgres.
- **مرجع ملاحظات العمل:** DEPLOY-03

### OPS-03
**pipeline الإصدار في CURRENT لا يكتمل (خطأ syntax في production-topology.test.cjs، اختبارات عقد قديمة، ترتيب خطوات، shallow clone)**

- **المجال:** Operations / CI · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (node --check) / Inferred (d,e) · **النوع:** Confirmed defect
- **الخطورة:** High — المسار الآلي الوحيد معطل فيعود النشر لمسارات يدوية. · **مانع نشر لـCURRENT**
- **الدليل:** [C] scripts/production-topology.test.cjs:26 (SyntaxError — مُتحقق)؛ scripts/merge-launcher.test.js:105, 442؛ ci.yml (/tmp/immutable.env قبل إنشائه)
- **المحفز (Trigger):** أي push.
- **الأثر:** لا release manifest.
- **للتحقق/الإغلاق:** E-28 سجل GitHub Actions.
- **مرجع ملاحظات العمل:** DEPLOY-04

### OPS-04
**النسخ الاحتياطي الآلي لقاعدة الإنتاج غير مثبت: آلية المستودع غير صالحة كما هي لهذا المضيف، ودليل DR اصطناعي ويعتمد على Neon PITR؛ وجود نسخ على المضيف Unknown**

- **المجال:** Operations / DR · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (repo) / Unknown (host cron) · **النوع:** Potential risk
- **الخطورة:** High — غياب آلية صالحة في المستودع لا يثبت غياب النسخ على المضيف (cron/systemd/نسخ يدوي/لقطات المزود)؛ الخطر قائم حتى يثبت E-06 العكس. [تصحيح 34]
- **الدليل:** [B]/[C] docs/PRODUCTION-READINESS-P0.md:104,181 (OPEN)؛ scripts/backup-nightly.sh:12, 47؛ docs/runbooks/disaster-recovery.md:23,53؛ docs/dr-evidence.json (synthetic)
- **المحفز (Trigger):** فقد المضيف/تلف.
- **الأثر:** فقد بيانات.
- **للتحقق/الإغلاق:** E-06.
- **مرجع ملاحظات العمل:** DEPLOY-07

### OPS-05
**workflow النشر يخفي فشل النشر البعيد (`; rm -f` في نهاية أمر ssh)**

- **المجال:** Operations / CI · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (تحقق مستقل) · **النوع:** Confirmed defect
- **الخطورة:** Medium — نشر فاشل يظهر أخضر. · **مانع نشر لـCURRENT**
- **الدليل:** [C] .github/workflows/production-deploy.yml:113
- **المحفز (Trigger):** نشر فاشل.
- **الأثر:** ثقة زائفة.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** DEPLOY-08

### OPS-06
**smoke بعد النشر يستدعي compose بلا ملف env الإصدار → فشل interpolation → rollback يفشل بنفس الطريقة**

- **المجال:** Operations / Deploy · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Inferred · **النوع:** Potential risk
- **الخطورة:** Medium — يعتمد على سلوك Compose. · **مانع نشر لـCURRENT**
- **الدليل:** [C] scripts/production-http-smoke.sh:17
- **المحفز (Trigger):** أي نشر.
- **الأثر:** rollback-failed.
- **للتحقق/الإغلاق:** اختبار على staging.
- **مرجع ملاحظات العمل:** DEPLOY-09

### OPS-07
**بوابة الاعتماد للإنتاج تعتمد على إعدادات GitHub environment غير مُصدَّرة؛ النشر يُطلق تلقائيًا بعد كل CI ناجح على main**

- **المجال:** Operations / Governance · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Unknown · **النوع:** Question
- **الخطورة:** Medium — قد لا يوجد اعتماد بشري.
- **الدليل:** [C] .github/workflows/production-deploy.yml:72-88
- **المحفز (Trigger):** —
- **الأثر:** نشر غير مقصود.
- **للتحقق/الإغلاق:** E-28.
- **مرجع ملاحظات العمل:** DEPLOY-10

### OPS-08
**ملف compose التطويري هو الافتراضي في مجلد الإنتاج وبنفس اسم المشروع (منافذ PG 5432-5440 على كل الواجهات)**

- **المجال:** Operations / Hygiene · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (files) / Inferred (pg_accounting) · **النوع:** Potential risk
- **الخطورة:** Medium — أمر compose بلا -f يطال مشروع الإنتاج.
- **الدليل:** [C] docker-compose.yml (بلا name، volume pg_accounting)؛ [U] volume nile-pharma-erp_pg_accounting يتيم
- **المحفز (Trigger):** docker compose up بلا -f.
- **الأثر:** إعادة إنشاء redpanda بإعدادات dev، قواعد مكشوفة.
- **للتحقق/الإغلاق:** E-04.
- **مرجع ملاحظات العمل:** DEPLOY-11

### OPS-09
**بوابة توافق migrations تقارن بالـpush السابق لا بالإنتاج ولا تكشف تعديل migrations مطبقة**

- **المجال:** Operations / Migrations · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — سمحت بتعديل general_ledger 6 مرات.
- **الدليل:** [C] scripts/validate-migration-compatibility.cjs:41-43؛ ci.yml (github.event.before)
- **المحفز (Trigger):** تعديل migration مطبقة.
- **الأثر:** DDL المستودع ≠ الإنتاج.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** DEPLOY-12

### OPS-10
**الصور تعمل كـroot وتحمل شجرة البناء كاملة، والـCMD الافتراضي ينفذ prisma migrate deploy**

- **المجال:** Operations / Containers · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — تشغيل أي صورة خارج compose يرحّل قاعدة بياناتها (آلية محتملة لـaccounting-manual).
- **الدليل:** [C] apps/*/Dockerfile (لا USER؛ CMD sh -c 'npx prisma migrate deploy && …')
- **المحفز (Trigger):** docker run/compose run.
- **الأثر:** migrations غير مقصودة.
- **للتحقق/الإغلاق:** E-04 أمر accounting-manual.
- **مرجع ملاحظات العمل:** DEPLOY-14

### OPS-11
**حاويات متوقفة غير مفسرة: db-migrate (Exited 3) وaccounting-manual (Exited 1، تعريفها ليس في git)**

- **المجال:** Operations / Runtime · **النسخة المتأثرة:** RUNTIME · **درجة التحقق:** [U] user-reported · **النوع:** Operational uncertainty
- **الخطورة:** Medium — دليل على تدخلات يدوية غير موثقة.
- **الدليل:** [U] docx.txt:62-70, 800-806
- **المحفز (Trigger):** —
- **الأثر:** —
- **للتحقق/الإغلاق:** E-01, E-04.
- **مرجع ملاحظات العمل:** F-docx

### OPS-12
**شبكة nile-internal ليست internal ولا موجودة في git؛ Postgres على شبكتين**

- **المجال:** Operations / Network · **النسخة المتأثرة:** BOTH · **درجة التحقق:** [U] / Verified (absence) · **النوع:** Improvement
- **الخطورة:** Low — لا منفذ منشور لـPG.
- **الدليل:** [U] docx.txt:572-581
- **المحفز (Trigger):** —
- **الأثر:** لا عزل فعلي.
- **للتحقق/الإغلاق:** E-07.
- **مرجع ملاحظات العمل:** DEPLOY-15

### OPS-13
**عدم اتساق أسبقية DATABASE_URL بين التحقق وPrisma (7 خدمات تتحقق من <SVC>_DATABASE_URL وتتصل بـDATABASE_URL)**

- **المجال:** Operations / Config · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Low — compose يمرر DATABASE_URL فقط.
- **الدليل:** [C] apps/accounting/src/config/env.ts:57؛ apps/accounting/src/prisma/prisma.service.ts؛ scripts/deploy-migrations.cjs
- **المحفز (Trigger):** تشغيل يدوي بملف env مختلف.
- **الأثر:** اتصال بقاعدة خاطئة.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** DEPLOY-17

### OPS-14
**CI يدفع صورًا مبنية من PRs إلى namespace سجل الإنتاج؛ SBOM غير مرفوع**

- **المجال:** Operations / Supply chain · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified · **النوع:** Improvement
- **الخطورة:** Low — manifest للـmain فقط.
- **الدليل:** [C] ci.yml (permissions packages: write)
- **المحفز (Trigger):** —
- **الأثر:** —
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** DEPLOY-19

### ORG-01
**اعتماد الإجازة بلا تحقق من الحالة (خصم مزدوج للرصيد، اعتماد إجازة مرفوضة) وبلا منع اعتماد ذاتي**

- **المجال:** Organization / HR · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — [U] جداول HR شبه فارغة.
- **الدليل:** [B]/[C] apps/organization/src/modules/attendance/attendance.service.ts:170-218 (rejectLeave لا يعيد الرصيد كذلك)
- **المحفز (Trigger):** اعتماد مكرر.
- **الأثر:** أرصدة إجازات خاطئة.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** ORG-01(notes)

### ORG-02
**مطالبات المصروفات: رفض من أي حالة بما فيها PAID، قراءة غير مقيدة، لا تحقق من المالك أو المدير**

- **المجال:** Organization / Expenses · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — عيب مسجل كـP0 من المالك ومؤجل.
- **الدليل:** [C] apps/organization/src/modules/expenses/expenses.service.ts:68-86, 153-168, 197-215؛ [C] docs/DECISIONS-2026-09-25-ar.md:134-140
- **المحفز (Trigger):** رفض بعد الدفع.
- **الأثر:** سجل مصروفات مضلل.
- **للتحقق/الإغلاق:** Q-ORG-2.
- **مرجع ملاحظات العمل:** ORG-02(notes), REQDOC-10

### ORG-03
**تعديلات الرواتب تغيّر netPay لمسيرات FINALIZED/PAID دون إعادة اعتماد؛ الحوافز = 0 ثابتة**

- **المجال:** Organization / Payroll · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — يخالف وثيقة التصميم.
- **الدليل:** [C] apps/organization/src/modules/payroll/payroll.service.ts:311, 437-458؛ docs/ERP-EMPLOYEE-PAYROLL-DESIGN.md:44
- **المحفز (Trigger):** تعديل بعد الإقفال.
- **الأثر:** رواتب مسجلة لا تطابق المدفوع.
- **للتحقق/الإغلاق:** Q-ORG-1.
- **مرجع ملاحظات العمل:** ORG-03(notes)

### ORG-04
**لا تكامل مالي من HR: صرف الرواتب والمصروفات والهدايا لا ينشر أحداثًا ولا يرحّل لأي دفتر**

- **المجال:** Organization / Accounting · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Operational uncertainty
- **الخطورة:** Medium — خطوة محاسبية يدوية ضمنية.
- **الدليل:** grep publish في apps/organization/src/modules/*/*.service.ts؛ expenses.service.ts:171 (تعليق مضلل)
- **المحفز (Trigger):** صرف.
- **الأثر:** مصروفات خارج الدفاتر.
- **للتحقق/الإغلاق:** Q-ORG-1.
- **مرجع ملاحظات العمل:** ORG-04(notes)

### SAL-01
**حدث الدفع يكتب PAID فوق SHIPPED/DELIVERED/ON_HOLD_RECALL/CANCELLED؛ والعكس يعيد الطلب المسلَّم قابلًا للإلغاء**

- **المجال:** Sales / Order lifecycle · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (code، تحقق مستقل) / Inferred (scenario) · **النوع:** Confirmed defect
- **الخطورة:** High — يفسد الحالة المرجعية للطلب بعد خروج البضاعة.
- **الدليل:** [C]/[B] apps/sales/src/modules/saga/saga.orchestrator.ts:481-484 (update غير مشروط)؛ :520-523؛ [C] orders.service.ts:1235, 1332-1342
- **المحفز (Trigger):** طلب آجل شُحن/سُلّم ثم سُدد بالكامل ثم ارتد الشيك.
- **الأثر:** حالة DELIVERED تضيع؛ إمكانية إلغاء طلب مسلَّم وإبطال فاتورته.
- **للتحقق/الإغلاق:** E-14: توزيع الحالات وطلبات saga DONE بحالة ≠ PAID.
- **مرجع ملاحظات العمل:** SCI-01

### SAL-02
**وصول StockReserved متأخر يعيد إحياء طلب ملغى (ALLOCATED) ويحجز المخزون دون إفراج**

- **المجال:** Sales / Saga · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (code) / Inferred (race) · **النوع:** Potential risk
- **الخطورة:** High — طلب ملغى يصبح قابلًا للشحن بلا فاتورة.
- **الدليل:** [C] orders.service.ts:1332؛ saga.orchestrator.ts:328-338, 386-389؛ [C] apps/inventory/.../reservation.listener.ts:179-240
- **المحفز (Trigger):** إلغاء أثناء ALLOCATING.
- **الأثر:** حجز معلق، شحن بلا فاتورة.
- **للتحقق/الإغلاق:** E-14 مقارنة الحجوزات المفتوحة بالطلبات الملغاة.
- **مرجع ملاحظات العمل:** SCI-02

### SAL-03
**مدفوعات الفواتير المباشرة لا تخفض تعرض الائتمان في Sales بينما الفاتورة تزيده**

- **المجال:** Sales / Credit control · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** High — التعرض يتضخم باستمرار للعملاء الذين يشترون بفواتير مباشرة (المسار الرئيسي في الواجهة).
- **الدليل:** [C] saga.orchestrator.ts:408-417, 440-446؛ [C] apps/accounting/.../payments.service.ts:189-191, 654-657
- **المحفز (Trigger):** أي دفعة على فاتورة مباشرة.
- **الأثر:** CREDIT_HOLD كاذب.
- **للتحقق/الإغلاق:** E-14: مقارنة account_credit.outstanding بـAR المفتوح.
- **مرجع ملاحظات العمل:** SCI-03

### SAL-04
**BASELINE: لا سقف للخصم في الخادم (0-100%)، السقف 30% في الواجهة فقط**

- **المجال:** Sales / Pricing control · **النسخة المتأثرة:** BASELINE · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** High — أي حامل sales.orders.create يمكنه البيع بخصم 100% عبر API (تخفيف جزئي: الطلبات ≥100,000 تذهب للاعتماد — [B] orders.service.ts:20, 611؛ والاستيراد أيضًا حتى 100% — import-orders.dto.ts:33).
- **الدليل:** [B] apps/sales/src/modules/orders/dto/create-order.dto.ts:12؛ orders.service.ts:541-557؛ apps/web/app/dashboard/orders/new/page.tsx:242
- **المحفز (Trigger):** استدعاء API مباشر.
- **الأثر:** فواتير بأسعار منخفضة تنتقل للمحاسبة.
- **للتحقق/الإغلاق:** E-14: max(discount_pct) وعدد الخصومات >12%.
- **مرجع ملاحظات العمل:** SCI-04, REQDOC-05

### SAL-05
**CURRENT: بوابة الخصم تعتمد صلاحية غير موجودة (sales.discounts.approve) وتتجاهل مستويات مصفوفة الاعتماد**

- **المجال:** Sales / Pricing control · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — بين 12% و15% (أعلى مستوى في المصفوفة) لا يبيع إلا SUPER_ADMIN، وفوق 15% مرفوض للجميع؛ مستويات 3/5/7% بلا أثر. · **مانع نشر لـCURRENT**
- **الدليل:** [C] orders.service.ts:556-570؛ غياب الكود في apps/iam/prisma/seed.ts؛ apps/sales/prisma/migrations/20260914040000_discount_policies/migration.sql:45-50
- **المحفز (Trigger):** خصم >12%.
- **الأثر:** تعطيل عملي أو تجاوز الصلاحيات.
- **للتحقق/الإغلاق:** قرار Q-SAL-2.
- **مرجع ملاحظات العمل:** SCI-05

### SAL-06
**المرتجعات مسموحة على طلبات مفوترة لم تُشحن (الفاتورة تصدر عند الحجز) → إعادة مخزون وهمية وائتمان AR**

- **المجال:** Sales / Returns · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (code) / Inferred (impact) · **النوع:** Potential risk
- **الخطورة:** Medium — يتطلب موافقة معتمِد لا يرى أن البضاعة لم تخرج.
- **الدليل:** [C] returns.service.ts:16, 384-387؛ reservation.listener.ts:353-398
- **المحفز (Trigger):** مرتجع على INVOICED.
- **الأثر:** مخزون مزدوج ورصيد دائن لبضاعة لم تُسلَّم.
- **للتحقق/الإغلاق:** قرار Q-SAL-5.
- **مرجع ملاحظات العمل:** SCI-08

### SAL-07
**شرائح العمولة تُطبق على كل دفعة منفردة لا على المبيعات التراكمية للفترة**

- **المجال:** Incentives · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (code) / Inferred (intent) · **النوع:** Question
- **الخطورة:** High — مع خطة 44 شريحة تقريبًا كل دفعة تأخذ الشريحة الأولى (1.333%).
- **الدليل:** [C] apps/incentives/src/modules/engine/incentive.engine.ts:53-63؛ intake.service.ts:112؛ prisma/seed.ts:4-7
- **المحفز (Trigger):** أي PaymentReceived.
- **الأثر:** عمولات أقل بكثير من سياسة الشركة (F04).
- **للتحقق/الإغلاق:** تأكيد المالك (Q-SAL-1).
- **مرجع ملاحظات العمل:** SCI-10, REQ-61

### SAL-08
**لا يُزرع rule set للحوافز في مسار الإنتاج → كل PaymentReceived يفشل إلى DLQ إن كان الجدول فارغًا**

- **المجال:** Incentives / Ops · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (scripts) / Unknown (DB) · **النوع:** Operational uncertainty
- **الخطورة:** Medium — [U] جداول الحوافز شبه فارغة.
- **الدليل:** [C] rules.service.ts:29-32؛ scripts/production-migrate.sh:108-126؛ [U] docx.txt:475-476
- **المحفز (Trigger):** أول دفعة.
- **الأثر:** لا عمولات تسجل.
- **للتحقق/الإغلاق:** E-15: SELECT version,is_active FROM rule_sets.
- **مرجع ملاحظات العمل:** SCI-11

### SAL-09
**سجل الحوافز بلا تقييد نطاق (rep scoping) ولا فصل مهام في الاعتماد/الصرف؛ العكس مسموح بعد PAID**

- **المجال:** Incentives / Controls · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — اطلاع وتعديل واسع.
- **الدليل:** [C] ledger.service.ts:32-41, 99-123؛ rules.controller.ts:11
- **المحفز (Trigger):** —
- **الأثر:** اعتماد ذاتي للعمولة.
- **للتحقق/الإغلاق:** تعريف المصفوفة.
- **مرجع ملاحظات العمل:** SCI-13

### SAL-10
**المرتجعات والإشعارات الدائنة لا تعدّل العمولات؛ الاسترداد يعكس سطرًا واحدًا لكل payment_id**

- **المجال:** Incentives · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified / Inferred · **النوع:** Question
- **الخطورة:** Medium — قد يبقي عمولات غير مستحقة.
- **الدليل:** [C] intake.service.ts:62-64, 176-179
- **المحفز (Trigger):** مرتجع بعد الدفع.
- **الأثر:** عمولة زائدة.
- **للتحقق/الإغلاق:** Q-SAL-1.
- **مرجع ملاحظات العمل:** SCI-12, SCI-14

### SAL-11
**المندوب يستطيع تعديل حد ائتمان عملائه، والقيمة 0 تعطّل الرقابة؛ التغيير بلا outbox ولا تسوية مع Sales**

- **المجال:** CRM / Credit governance · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified / Unknown (role assignment) · **النوع:** Potential risk
- **الخطورة:** Medium — يعتمد على من يحمل crm.accounts.credit-limit.update.
- **الدليل:** [C] apps/crm/src/modules/accounts/accounts.service.ts:275-306؛ apps/sales/.../credit.service.ts:348-351
- **المحفز (Trigger):** تعديل الحد.
- **الأثر:** تجاوز الرقابة الائتمانية؛ اختلاف الحد بين CRM وSales.
- **للتحقق/الإغلاق:** E-16 أدوار الصلاحية؛ Q-SAL-3.
- **مرجع ملاحظات العمل:** SCI-15, SCI-16

### SAL-12
**قبول طلبات لعملاء مؤرشفين (isActive=false)**

- **المجال:** Sales / Master data · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — ضابط أساسي مفقود.
- **الدليل:** [C] orders.service.ts:196-221؛ accounts.service.ts:365-390
- **المحفز (Trigger):** طلب لعميل مؤرشف.
- **الأثر:** مبيعات لعملاء موقوفين.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** SCI-17

### SAL-13
**صور إثبات التسليم والفواتير الموقعة تُخزن على قرص الحاوية دون volume**

- **المجال:** Sales / Evidence retention · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (compose) / Unknown (mounts) · **النوع:** Operational uncertainty
- **الخطورة:** Medium — تضيع مع كل إعادة إنشاء للحاوية.
- **الدليل:** [C] apps/sales/src/modules/shipments/storage/file-storage.service.ts:37-39؛ docker-compose.production.yml (volume redpanda_data فقط)
- **المحفز (Trigger):** إعادة إنشاء الحاوية (حدث في 09-29 للمحاسبة).
- **الأثر:** فقد إثباتات التسليم.
- **للتحقق/الإغلاق:** E-17: docker inspect mounts لحاوية sales.
- **مرجع ملاحظات العمل:** SCI-18

### SAL-14
**إعدادات التسعير (سياسات الخصم، قواعد الأسعار، العروض، ملف تسعير العميل، نسبة عمولة العميل) لا تُطبق أبدًا على الطلبات**

- **المجال:** Sales / Pricing · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed gap
- **الخطورة:** Medium — شاشات تعطي انطباعًا بوجود رقابة.
- **الدليل:** [C] orders.service.ts:24-25, 571-589؛ grep: المحركات مستخدمة داخل وحداتها فقط
- **المحفز (Trigger):** تهيئة قاعدة تسعير.
- **الأثر:** قرارات تجارية بلا أثر.
- **للتحقق/الإغلاق:** Q-SAL-2 / REQ-15 vs REQ-29.
- **مرجع ملاحظات العمل:** SCI-20

### SAL-15
**مسودات الطلبات المستوردة تتبع سياسة تسعير أضعف ولا يُعاد التحقق منها عند الإرسال**

- **المجال:** Sales / Pricing · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — تجاوز ضوابط الخصم.
- **الدليل:** [C] orders.service.ts:909-910, 953, 976, 985, 1087-1116
- **المحفز (Trigger):** استيراد Excel.
- **الأثر:** أسعار/خصومات غير مراقبة.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** SCI-22

### SAL-16
**إلغاء الطلب من حجز الاستدعاء يتجاهل الأموال المحصلة**

- **المجال:** Sales / Recall · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified / Inferred · **النوع:** Potential risk
- **الخطورة:** Medium — طلب ملغى مع فاتورة مدفوعة بلا مسار استرداد.
- **الدليل:** [C] traceability.service.ts:246-288؛ saga-listener.service.ts:203-205
- **المحفز (Trigger):** CANCEL من ON_HOLD_RECALL.
- **الأثر:** التزام استرداد غير مسجل.
- **للتحقق/الإغلاق:** Q-SAL-5.
- **مرجع ملاحظات العمل:** SCI-24

### SAL-17
**تجاوز الحجز الائتماني يتخطى اعتماد ≥100,000؛ العتبة مكتوبة في الكود وتشمل الشحن**

- **المجال:** Sales / Approvals · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Question
- **الخطورة:** Low — سلوك مقصود حسب التعليق.
- **الدليل:** [C] orders.service.ts:20, 642, 652-654؛ credit.service.ts:385-388
- **المحفز (Trigger):** credit-override.
- **الأثر:** طلب كبير بلا اعتماد.
- **للتحقق/الإغلاق:** Q-SAL-4.
- **مرجع ملاحظات العمل:** SCI-23, SCI-28

### SAL-18
**عمليات غائبة: عرض السعر (Quotation)، احتساب تحقيق المستهدفات، سياسة المرتجعات (90 يومًا قبل الانتهاء)**

- **المجال:** Sales / Process gaps · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (absence) · **النوع:** Question
- **الخطورة:** Info — لا متطلب معتمد صريح.
- **الدليل:** sales-crm-incentives notes P7؛ REQ-68
- **المحفز (Trigger):** —
- **الأثر:** عمل يدوي خارج النظام.
- **للتحقق/الإغلاق:** Q-SAL-6.
- **مرجع ملاحظات العمل:** SCI P7, REQ-68

### SEC-01
**حامل iam.users.update يستطيع تغيير كلمة مرور أي مستخدم بما فيهم SUPER_ADMIN أو إيقافه**

- **المجال:** Security / IAM · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (code، تحقق مستقل) · **النوع:** Confirmed defect
- **الخطورة:** High — مسار تصعيد صلاحيات كامل؛ القابلية تعتمد على وجود دور يحمل الصلاحية غير SUPER_ADMIN.
- **الدليل:** [C]/[B] apps/iam/src/modules/users/users.service.ts:160-176 (لا assertWithinAuthority)؛ قارن :228-237
- **المحفز (Trigger):** PATCH /api/iam/users/{adminId} {password}.
- **الأثر:** استيلاء على حساب المدير.
- **للتحقق/الإغلاق:** E-16: الأدوار التي تحمل الصلاحية.
- **مرجع ملاحظات العمل:** IAM-01

### SEC-02
**CURRENT: seed الخاص بـIAM معطوب (حقل username غير موجود) ولا ينشئ SUPER_ADMIN، و44 صلاحية مطلوبة غير موجودة في الكتالوج**

- **المجال:** Security / IAM / Release · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (code) / Inferred (runtime) · **النوع:** Confirmed defect
- **الخطورة:** High — يكسر الإصدار بعد تطبيق migrations (set -eu) ويخلق deadlock للصلاحيات الجديدة. · **مانع نشر لـCURRENT**
- **الدليل:** [C] apps/iam/prisma/seed.ts:52 (إنشاء Permission بـ{code} فقط بينما domain/module/action إلزامية → خطأ type وخطأ Prisma حتى دون SEED_ADMIN_PASSWORD)، :55-62 (username غير موجود)؛ apps/iam/prisma/schema.prisma:41-72؛ scripts/production-migrate.sh:36, 118-124؛ [B] seed.ts:252-266
- **المحفز (Trigger):** نشر CURRENT أو بناء بيئة DR.
- **الأثر:** إصدار نصف مكتمل؛ وحدات HR/payroll ترفض الجميع في بيئة جديدة.
- **للتحقق/الإغلاق:** استعادة منطق BASELINE ودمج الأكواد الجديدة.
- **مرجع ملاحظات العمل:** IAM-03

### SEC-03
**مجلد Data/ بملفات أعمال حقيقية (رواتب، عملاء، فواتير، مبيعات) مُضاف إلى git في النسختين**

- **المجال:** Security / Data governance · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (أسماء فقط) · **النوع:** Confirmed defect
- **الخطورة:** High — بيانات حساسة تُنسخ مع كل clone وتبقى في التاريخ.
- **الدليل:** base/Data (53MB) وcur/Data (58MB)؛ أسماء مثل مرتبات.xlsx والعملاء.xlsx وData.rar؛ Dockerfiles لا تنسخ Data/ لكن `.dockerignore` لا يستثنيه فيُرسل ضمن build context
- **المحفز (Trigger):** أي clone أو مشاركة للمستودع (بما فيها هذه الحزمة).
- **الأثر:** تعرّض بيانات شخصية ومالية.
- **للتحقق/الإغلاق:** قرار المالك + إزالة وتنظيف التاريخ (تنفيذ لاحق).
- **مرجع ملاحظات العمل:** SEC-06

### SEC-04
**CURRENT: أربعة controllers محاسبية بلا PermissionsGuard؛ أداة CI تتحقق من نص الـdecorator فقط**

- **المجال:** Security / Authorization · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified (static, script) · **النوع:** Potential risk
- **الخطورة:** Medium — كامن: غير mounted حاليًا؛ تسجيلها كما هي يتيح ترحيل/عكس قيود ودفع موردين لأي مستخدم مسجل. · **مانع نشر لـCURRENT**
- **الدليل:** [C] gl-workbench.controller.ts:6-25؛ audit-timeline.controller.ts:4-8؛ finance-dashboard.controller.ts:4-8؛ supplier-ledger/supplier-payments.controller.ts:6-31؛ scripts/validate-controller-permissions.cjs:13-16,39-46
- **المحفز (Trigger):** تسجيل الوحدات لإصلاح ARC-05.
- **الأثر:** تجاوز SoD.
- **للتحقق/الإغلاق:** PermissionsGuard كـAPP_GUARD أو فحص CI.
- **مرجع ملاحظات العمل:** SEC-01(notes), WEBEVT-02

### SEC-05
**الصلاحيات داخل JWT ولا يُعاد التحقق منها؛ الإلغاء يتأخر حتى 15 دقيقة؛ تتبع الجلسات الخاملة معطل افتراضيًا**

- **المجال:** Security / Sessions · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified / Unknown (env) · **النوع:** Potential risk
- **الخطورة:** Medium — logout لا يلغي access token.
- **الدليل:** [C] apps/iam/src/modules/auth/auth.service.ts:132-136؛ packages/security/src/index.ts:13؛ docker-compose.production.yml:59
- **المحفز (Trigger):** إيقاف مستخدم.
- **الأثر:** نافذة وصول بعد الإيقاف.
- **للتحقق/الإغلاق:** E-22 قيمة SESSION_IDLE_ENFORCEMENT.
- **مرجع ملاحظات العمل:** IAM-02

### SEC-06
**توكنات الوصول والتحديث (7 أيام) في localStorage مع CSP يسمح بـunsafe-inline**

- **المجال:** Security / Web · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — لم يُعثر على XSS؛ أثر أي XSS هو استيلاء كامل.
- **الدليل:** [C] apps/web/app/login/page.tsx:35-36؛ lib/api.ts:40-43؛ next.config.js:11
- **المحفز (Trigger):** XSS.
- **الأثر:** سرقة الجلسة.
- **للتحقق/الإغلاق:** قرار تصميم.
- **مرجع ملاحظات العمل:** SEC-02(notes), WEBEVT-13

### SEC-07
**Rate limiting والقفل مرتبطان بـreq.ip دون trust proxy → كل المستخدمين يشتركون في نفس الحد خلف NPM/web**

- **المجال:** Security / Availability · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Inferred · **النوع:** Operational uncertainty
- **الخطورة:** Medium — قد يجعل حد الدخول 5/دقيقة للشركة كلها و60/دقيقة لكل خدمة.
- **الدليل:** [C] apps/*/src/app.module.ts (ThrottlerModule)؛ غياب trust proxy (grep)؛ [U] docx: NPM→web
- **المحفز (Trigger):** ذروة استخدام أو استيراد كبير.
- **الأثر:** 429 جماعي، سجلات IP بلا قيمة جنائية.
- **للتحقق/الإغلاق:** E-16: توزيع ip_address في sessions.
- **مرجع ملاحظات العمل:** SEC-03(notes), SCI-19, INVPRD-26

### SEC-08
**سر HS256 واحد مشترك بين الخدمات التسع، وأسرار تطوير حرفية في ملفات dev/CI**

- **المجال:** Security / Secrets · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (repo) / Unknown (prod values) · **النوع:** Potential risk
- **الخطورة:** Medium — لم يُعثر على سر إنتاجي في المستودع.
- **الدليل:** [C] .env.example:25-35؛ docker-compose.yml:158-295؛ .github/workflows/ci.yml:54-60 (أسماء فقط)؛ apps/iam/src/config/env.ts:164-172
- **المحفز (Trigger):** تسرب سر خدمة واحدة.
- **الأثر:** سك توكنات SUPER_ADMIN.
- **للتحقق/الإغلاق:** E-23 تشغيل check-production-env.sh (أطوال وحالات فقط).
- **مرجع ملاحظات العمل:** SEC-04(notes)

### SEC-09
**ملف .env.backup.20260927-130337 غير متتبع داخل مجلد المستودع على الخادم وغير مغطى بـ.gitignore**

- **المجال:** Security / Secrets · **النسخة المتأثرة:** RUNTIME · **درجة التحقق:** Verified ([R] git status) · **النوع:** Potential risk
- **الخطورة:** Medium — git add -A عرضي يرفع أسرار الإنتاج.
- **الدليل:** [R] git-and-schema.txt:9؛ [C] .gitignore:6-12
- **المحفز (Trigger):** commit عرضي.
- **الأثر:** تسرب أسرار.
- **للتحقق/الإغلاق:** نقل الملف/صلاحيات 600 (تنفيذ لاحق).
- **مرجع ملاحظات العمل:** SEC-05(notes), F02

### SEC-10
**فصل المهام (SoD) كشفي فقط، والمصفوفة تشير إلى 7 صلاحيات غير موجودة؛ SUPER_ADMIN مستثنى في الرواتب**

- **المجال:** Security / SoD · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — ادعاء '7/7 rules enforced' غير صحيح.
- **الدليل:** [C] apps/iam/src/modules/sod/sod-matrix.ts:33-43؛ sod.service.ts؛ apps/organization/.../payroll.service.ts:356-359
- **المحفز (Trigger):** إسناد أدوار.
- **الأثر:** تركيبات صلاحيات سامة.
- **للتحقق/الإغلاق:** Q-SEC-2.
- **مرجع ملاحظات العمل:** IAM-08, REQDOC-11

### SEC-11
**التوقيع الإلكتروني لا يحقق نية 21 CFR Part 11 (لا إعادة مصادقة، الكيان خارج الـMAC، canonicalization ناقص، لا تحقق عند الإفراج)**

- **المجال:** Security / Quality · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — ادعاء تنظيمي؛ التوقيع عند الإفراج معطل افتراضيًا.
- **الدليل:** [C] apps/iam/src/modules/signatures/signatures.service.ts:12-16؛ apps/products/.../batches.service.ts:149
- **المحفز (Trigger):** إفراج دفعة.
- **الأثر:** توقيع غير ملزم.
- **للتحقق/الإغلاق:** Q-SEC-8.
- **مرجع ملاحظات العمل:** IAM-06

### SEC-12
**Copilot يرسل بيانات ERP إلى مزودي LLM خارجيين؛ CURRENT يجعل ذلك افتراضيًا**

- **المجال:** Security / Data protection · **النسخة المتأثرة:** BOTH (default CURRENT) · **درجة التحقق:** Verified / Unknown (provider) · **النوع:** Question
- **الخطورة:** Medium — قرار خصوصية وإقامة بيانات.
- **الدليل:** [C] apps/web/components/copilot/copilot-chat.tsx:47؛ apps/iam/src/modules/workspace/copilot.service.ts:209؛ ai-router.service.ts:20-40
- **المحفز (Trigger):** سؤال يحتوي بيانات عملاء.
- **الأثر:** نقل بيانات لطرف ثالث.
- **للتحقق/الإغلاق:** Q-SEC-7.
- **مرجع ملاحظات العمل:** SEC-10(notes), WEBEVT-14

### SEC-13
**سجلات audit_logs المحلية best-effort، للنجاح فقط، قابلة للتعديل، وIP هو الوكيل؛ السجل المركزي يغطي الأحداث فقط**

- **المجال:** Security / Audit trail · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified / Inferred (IP) · **النوع:** Potential risk
- **الخطورة:** Medium — عمليات master data بلا حدث لا توجد إلا في سجل ضعيف.
- **الدليل:** [C] apps/accounting/src/common/interceptors/audit.interceptor.ts:36-60؛ apps/audit-aggregator/prisma/migrations/20260909130000_audit_immutable_chain
- **المحفز (Trigger):** مراجعة تدقيق.
- **الأثر:** فجوات في الأثر.
- **للتحقق/الإغلاق:** Q-WEB-2.
- **مرجع ملاحظات العمل:** WEBEVT-17/18

### SEC-14
**نقاط /health/details بلا مصادقة؛ مصادقة الـBFF مجرد وجود header**

- **المجال:** Security / Exposure · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Low — الخدمات مربوطة بـ127.0.0.1 وغير مكشوفة عبر rewrites.
- **الدليل:** [C] apps/*/src/common/health.ts:116؛ apps/web/app/api/system-health/route.ts:23-24
- **المحفز (Trigger):** تعرض المنافذ.
- **الأثر:** تسريب معلومات تشغيلية.
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** SEC-07(notes), WEBEVT-16

### SEC-15
**ملاحظات أمنية منخفضة: تعداد الحسابات وDoS القفل، انتهاء الجلسة 7 أيام ثابت، لا MFA، حجم توكن SUPER_ADMIN ≈7.4KB**

- **المجال:** Security / IAM · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified / Inferred · **النوع:** Improvement
- **الخطورة:** Low — مجتمعة منخفضة الأثر.
- **الدليل:** [C] auth.service.ts:96-115, 144؛ users.mfa_enabled غير مقروء
- **المحفز (Trigger):** —
- **الأثر:** —
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** IAM-04/05/10, SEC-09(notes)

### SEC-16
**ضوابط إيجابية: ValidationPipe(whitelist, forbidNonWhitelisted) في كل الخدمات، JwtAuthGuard عام، PermissionsGuard fail-closed، bcrypt 12، تدوير refresh مع كشف إعادة الاستخدام، 5 routes عامة فقط**

- **المجال:** Security · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (script + code) · **النوع:** Improvement
- **الخطورة:** Info — خط أساس جيد.
- **الدليل:** 05-API-Inventory-and-Routing.md (548/553 route بصلاحية method-level، 5 public)؛ apps/*/src/main.ts
- **المحفز (Trigger):** —
- **الأثر:** —
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** SEC-11(notes)

### WEB-01
**تجميعات الـBFF مقصوصة بصمت عند 200 صف (قيمة المخزون، التعرض الائتماني، عدادات المهام)**

- **المجال:** Web / Reporting · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Potential risk
- **الخطورة:** Medium — لم يُفعّل غالبًا بعد لصغر البيانات.
- **الدليل:** [C] apps/web/lib/inventory-value.ts:24-37؛ lib/credit-exposure.ts:74-77؛ apps/inventory/.../stock.service.ts:30؛ apps/crm/.../accounts.service.ts:119-120
- **المحفز (Trigger):** >200 رصيد أو عميل.
- **الأثر:** أرقام إدارية ناقصة بلا تحذير.
- **للتحقق/الإغلاق:** E-26 counts.
- **مرجع ملاحظات العمل:** WEBEVT-04

### WEB-02
**CURRENT: صفحة general-ledger تستدعي fetch بلا Authorization → 401 دائمًا**

- **المجال:** Web / Finance UI · **النسخة المتأثرة:** CURRENT · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Medium — شاشة قراءة غير قابلة للاستخدام. · **مانع نشر لـCURRENT**
- **الدليل:** [C] apps/web/app/dashboard/general-ledger/page.tsx:6
- **المحفز (Trigger):** فتح الصفحة.
- **الأثر:** —
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** WEBEVT-03

### WEB-03
**شاشات التشغيل تغفل خدمات (health بلا organization، jobs بلا sales)**

- **المجال:** Web / Ops · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified · **النوع:** Confirmed defect
- **الخطورة:** Low — نقاط عمياء.
- **الدليل:** [C] apps/web/app/api/system-health/route.ts:4-13؛ system-jobs/route.ts:11-15
- **المحفز (Trigger):** —
- **الأثر:** —
- **للتحقق/الإغلاق:** —
- **مرجع ملاحظات العمل:** WEBEVT-15

### WEB-04
**رصد ضعيف: لا metrics، Sentry في الويب غالبًا غير فعال، JsonLogger غير مستخدم، لا تنبيهات ولا حدود موارد**

- **المجال:** Web / Observability · **النسخة المتأثرة:** BOTH · **درجة التحقق:** Verified (config) / Unknown (DSN) · **النوع:** Operational uncertainty
- **الخطورة:** Medium — الأعطال تُكتشف من المستخدمين.
- **الدليل:** لا instrumentation.ts؛ compose web بلا SENTRY_DSN؛ docs/runbooks/alerts-and-metrics.md:4
- **المحفز (Trigger):** أي عطل.
- **الأثر:** زمن اكتشاف طويل.
- **للتحقق/الإغلاق:** E-27.
- **مرجع ملاحظات العمل:** WEBEVT-12, DEPLOY-18
