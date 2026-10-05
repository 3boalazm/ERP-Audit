# 10 — تحليل الأعمال وفجوات العمليات (Business Analysis & Process Gaps)

> **تصريح أساسي:** لا يوجد **baseline متطلبات معتمد وموقّع** في المستودع (GOV-01). ما يوجد: سجلات قرارات تنقل إجابات المالك على أسئلة وكلاء AI (بتواريخ وبلا اسم معتمِد)، حزم خيارات، ومستندات حالة يكتبها المنفذ نفسه. لذلك:
> - **[DOC-Decided]** = قرار مسجل منسوب للمالك (مع المصدر).
> - **[Company-req]** = متطلب مستنتج من ملفات الشركة في مراجعة سابقة (`docs/audit/2026-09-18-company-workflows-vs-erp-ar.md`)، ليس قرارًا موقّعًا.
> - **[Claim]** = ادعاء في RTM أو تقرير حالة.
> - أي اقتراح يعتمد على ممارسة أعمال مفترضة يُصنف **سؤالًا أو تحسينًا** لا defect.

## 1. توافق المتطلبات الموثقة مع التنفيذ (ملخص)

من 87 متطلبًا/قرارًا مجمّعًا (القائمة الكاملة في `appendix/notes/requirements-docs.md` §7) فُحص ≥50 مقابل الكود:

| الحالة | العدد التقريبي | أمثلة |
|---|---|---|
| منفذ في النسختين | ~27 | اعتماد المرتجعات المستقل، الإشعار الدائن CR-YYYY-NNNN، تعريفة الشحن، رسوم الشحن خارج VAT، الحجوزات القديمة كشف+تنبيه فقط، دورة هدايا العملاء، تخصيص التحصيل لفواتير، GPS بسبب |
| منفذ في CURRENT فقط (غير منشور) | ~8 | ترقيم PO وحصره بـSUPER_ADMIN، المطابقة على الاستلام الفعلي، سقف الخصم، ملف تسعير العميل، FX المحقق للموردين، رفض الدفعات المنتهية في الأمانة |
| جزئي | ~10 | قفل الفترات (GL فقط في C)، VAT/نموذج 41 (يدوي)، SoD (كشفي)، الدفع المتعدد للفواتير، الرصيد الافتتاحي |
| غير منفذ في أي نسخة | ~9 | البونص، فرز التالف، مطالبات الموردين، حد ائتمان بالعلب، عهدة المندوب، مرتجع الفاتورة المسددة (F10)، سياسة 90 يومًا، EXP-1 |
| مفتوح/غير محسوم | ~15 | نموذج التسعير، مصفوفة الخصم، سياسة الحوافز، ETA، طباعة PO، تبسيط شاشة الأدوار… |

## 2. العمليات: مكتملة / جزئية / غائبة
مصنفة في `08-Business-Process-Catalogue.md` §0. الخلاصة:
- **مكتمل نسبيًا:** تسجيل العميل، دورة أمر البيع حتى الفاتورة، المرتجعات (مع فجوات)، المنتجات والجودة، الهوية.
- **جزئي جوهريًا:** التحصيل (العكس والشيكات)، الشراء حتى الدفع (لا سداد في B)، المخزون (لا جرد ولا إتلاف ولا تكلفة)، الحوافز (منطق الشرائح)، الموارد البشرية (لا أثر مالي)، الضرائب (يدوي).
- **غائب في النسخة المرجحة للإنتاج:** دفتر الأستاذ العام بالقيد المزدوج، سداد الموردين، الجرد، الإتلاف، البونص، عهدة المندوب، عروض الأسعار.

## 3. خطوات مفقودة أو غير مترابطة (الحلقات المكسورة)

| الحلقة | من → إلى | ما ينقص | الأثر | Finding |
|---|---|---|---|---|
| الشحن → التكلفة | Inventory → Accounting | لا COGS عند شحن طلبات المبيعات | الهامش غير معروف | INV-07 |
| التحصيل على فاتورة مباشرة → الائتمان | Accounting → Sales | `order_id=null` فيُتجاهل | تعرض متضخم | SAL-03 |
| المرتجع بعد السداد → AR | Sales/Inventory → Accounting | رفض محاسبي بعد إعادة المخزون | تباعد مخزون/AR | ACC-18 |
| الاستلام → فاتورة المورد → السداد | Inventory → Accounting → Treasury | لا سداد في B | AP خارج النظام | ACC-10 |
| HR → المحاسبة | Organization → Accounting | لا أحداث ولا قيود | مصروفات خارج الدفاتر | ORG-04 |
| الإيقاف/سحب الصلاحية → الخدمات | IAM → All | صلاحيات في التوكن حتى 15 دقيقة | نافذة وصول | SEC-05 |
| حد الائتمان CRM → Sales | CRM → Sales | لا outbox ولا تسوية | حدود مختلفة | SAL-11 |
| إعدادات التسعير → الطلبات | Sales config → Orders | المحركات غير مستدعاة | إعدادات بلا أثر | SAL-14 |
| الدفع → الحوافز | Accounting → Incentives | شرائح على الدفعة لا التراكمي؛ لا تعديل بالمرتجعات | عمولات خاطئة | SAL-07, SAL-10 |
| قرار جودة → المخزون/المبيعات | Products → Inv/Sales | لا outbox ولا إعادة إرسال | دواء مستدعى قابل للحجز | INV-03 |

## 4. قواعد أعمال غير منفذة أو متضاربة

| القاعدة | المصدر | الكود | الحكم |
|---|---|---|---|
| نموذج التسعير: قاعدة تسعير واحدة لكل فاتورة + خصم يدوي ضمن سقف الدور | [DOC-Decided] DECISIONS-2026-09-25:19-23 | خصم 12% افتراضي + بوابة >12% (C) | **تعارض** مع قرار 09-28 (التسعير عند إنشاء العميل) — GOV-04 |
| إعادة تقييم FX بأسلوب M2 | [DOC-Decided] BD-5 | منفذ (B,C) | يتعايش مع "FX المحقق" (09-28)؟ — سؤال |
| PO بواسطة SUPER_ADMIN فقط | [DOC-Decided] 09-28 #3 | C: ويُلغى الاعتماد كذلك | تأكيد مطلوب (ACC-12) |
| المرتجع بعد السداد ينشئ رصيدًا دائنًا/استردادًا | [Company-req] F10 | غير منفذ | defect مؤكد (ACC-18) |
| فصل المهام في الأدوار "7/7 مطبقة" | [Claim] RTM REQ-SEC-009 | كشفي فقط | ادعاء غير صحيح (SEC-10) |
| منع الترحيل في فترة مقفلة | [Claim] RTM REQ-FIN-003 | B لا؛ C لقيود GL فقط | ادعاء غير صحيح (ACC-14) |
| VAT ونموذج 41 "مكتمل" | [Claim] RTM/GO-LIVE | من إدخالات يدوية فقط | ادعاء مبالغ فيه (ACC-15) |
| سياسة الحوافز = ورقة الشركة (750 ألف، تراكمي) | [Company-req] F04 | شرائح على كل دفعة | سؤال عالي الأثر (SAL-07) |
| رفض الدفعات المنتهية في الأمانة قبل الاستخدام الإنتاجي | [DOC-Decided] 09-25:105-106 | C فقط | B مخالف (INV-14) |
| المصروف: الرفض قبل الدفع فقط (EXP-1) | [DOC] P0 مؤجل | غير منفذ | defect معروف (ORG-02) |

## 5. الصلاحيات والموافقات وفصل المهام

| الضابط | موجود؟ | ملاحظة |
|---|---|---|
| المرتجعات: المعتمِد ≠ المنشئ | ✅ B,C | قوي |
| مطابقة الفاتورة: المسجل ≠ المعتمِد للتجاوز | ✅ B,C | |
| PO: المنشئ ≠ المعتمِد | ✅ B / ❌ C (يولد معتمدًا) | ACC-12 |
| طلب البيع ≥100,000: اعتماد | ✅ (عتبة ثابتة؛ تجاوز الائتمان يتخطاها) | SAL-17 |
| الخصم: سقف ومصفوفة | ❌ B / ⚠️ C (صلاحية غير موجودة) | SAL-04/05 |
| حد الائتمان: maker-checker | ❌ | SAL-11 |
| القيود اليدوية: SoD | ❌ C (والـworkbench غير المسجل فيه SoD) | ACC-11 |
| الرواتب: الحاسب ≠ المعتمِد | ✅ إلا SUPER_ADMIN | SEC-10 |
| المصروفات/الهدايا: لا اعتماد ذاتي | ✅ (الهدايا أقوى) | ORG-02 |
| الحوافز: اعتماد/صرف | ❌ لا SoD ولا نطاق | SAL-09 |
| تعديل كلمة مرور مستخدم آخر | ❌ لا فحص سلطة | SEC-01 |
| SoD على مستوى الأدوار | كشفي فقط | SEC-10 |

## 6. Traceability بين المستندات والعمليات
سلسلة المستندات المنفذة فعليًا: **طلب البيع (`sales_orders.id`) → الحجز (`inventory_reservations.order_id`) → الفاتورة (`invoices.order_id` فريد) → سطور الفاتورة → دفعات الحجز (`invoice_line_batches`) → الدفعة (`payments.invoice_id`) → سطر الحوافز (`payment_id`)**. المرتجع يرتبط بالطلب والدفعة الدوائية، والإشعار الدائن بالمرتجع والفاتورة. الشراء: PO → (C) PO receipt ← GoodsReceived؛ فاتورة المورد → PO؛ لا سداد في B.
**كسور التتبع:** الفاتورة المباشرة بلا طلب (`order_id=null`)؛ إعادة الإصدار تنشئ فاتورة بلا سطور (ACC-17)؛ الاستلام يربط PO بنص في الملاحظة (B)؛ لا ربط بين مرتجع المورد وفاتورة المورد؛ الرواتب والمصروفات بلا مستند محاسبي.

## 7. التقارير والتسويات والضوابط

| التقرير/التسوية | الحالة | ملاحظة |
|---|---|---|
| تقارير المبيعات/المخزون/العملاء/التحليلات | موجودة (B,C) | تقرير حالة التقارير متقادم |
| أعمار الديون، التحصيل حسب المندوب | موجودة | |
| ميزان المراجعة والقوائم المالية | B: من أرصدة غير مرحلة؛ C: من GL معطوب | ACC-01/02 |
| VAT/نموذج 41 | من إدخال يدوي | ACC-15 |
| تسوية المخزون الليلية | انحراف كاذب دائم | INV-06 |
| تسوية المبيعات الليلية | انحرافات كاذبة لحالات غير ممثلة | SCI-26 |
| تسوية المحاسبة الليلية | B: تقارير؛ C: إشارات AP معكوسة | ACC-23 |
| تسوية الخزينة الداخلية | تقارن الرصيد بالحركات (لا تكشف غياب العكس) | ACC-06 |
| تسوية بنكية | C فقط وغير mounted | ARC-05 |
| مطابقة عبر الخدمات (الائتمان مقابل AR، المخزون مقابل AP) | **غائبة** | INT-01 |

## 8. معالجة الاستثناءات والعمليات غير المكتملة
- طلبات عالقة: مراقبة saga تكشف (`/sagas/stalled`) ولا تصلح؛ لا مسار لطلب APPROVED لم يبدأ تخصيصه (INT-01).
- حجوزات قديمة: كشف وتنبيه فقط — [DOC-Decided] مطابق.
- رسائل فاشلة: DLQ مع إعادة نشر يدوية (جيد)؛ رسائل التوقيع المرفوض تضيع (INT-03).
- مستندات بحالات نهائية: الفاتورة الملغاة نهائية (جيد)؛ المصروف المدفوع يمكن رفضه (سيئ)؛ الإجازة المرفوضة يمكن اعتمادها (سيئ).

## 9. Traceability Matrix

**المفاتيح:** UI = صفحة الويب؛ API = الـendpoint الخارجي؛ Service = الملف/الدالة؛ Data = الجداول؛ Control = الضابط؛ Test = ملف spec موجود (**لم يُشغَّل** في هذه المراجعة)؛ Status: B/C.

| REQ / Process | المصدر | UI | API | Service | Data | Control | Test (موجود، غير مُشغّل) | B | C |
|---|---|---|---|---|---|---|---|---|---|
| REQ-01/02 اعتماد المرتجع المستقل | DECISIONS-AR:208-218 | `/dashboard/returns` | `POST /api/sales/returns/:id/approve` | `returns.service.ts:312-321` | sales_returns, sales_order_lines.returned_qty | approver≠creator | returns.approval.spec.ts | ✅ | ✅ |
| REQ-03 إشعار دائن CR-YYYY-NNNN | DECISIONS-AR:220-230 | `/dashboard/returns` | (حدث `sales.return.created`) | `credit-notes.service.ts:150` | credit_notes, document_sequences | تسلسل | credit-notes.service.spec.ts | ✅ | ✅ |
| REQ-04 VAT سالب بعلم المستشار | DECISIONS-AR:226-227 | — | — | `credit-notes.service.ts:74-90` | tax_entries | flag افتراضي off | credit-notes.service.spec.ts | ✅ | ✅ |
| REQ-05 استيراد الطلبات كمسودات | DECISIONS-AR:232-241 | `/dashboard/orders` | `POST /api/sales/orders/import`, `/:id/submit` | `orders.service.ts:911-1116` | sales_orders | override permission | orders.import.spec.ts | ⚠️ | ⚠️ (SAL-15) |
| REQ-07 إثبات التسليم | DECISIONS-AR:242-253 | `/dashboard/shipping` | `POST /api/sales/shipments/:orderId/pod/:kind` | `shipments.service.ts:94-128` | order_shipments + **قرص الحاوية** | توقيع إلزامي | shipments.pod.spec.ts | ⚠️ | ⚠️ (SAL-13) |
| REQ-10 فصل مهام PO/المطابقة | DECISIONS-09-25:7 | `/dashboard/purchase-orders`, `/matching` (C) | `POST /api/accounting/matching/purchase-orders/:id/approve`, `/matches/:id/override` | `matching.service.ts:205/237` | purchase_orders, three_way_matches | SoD | matching.service.spec.ts | ✅ | ⚠️ (ACC-12) |
| REQ-12 FX M2 | BD-5 | `/dashboard/fx` | `POST /api/accounting/fx/revalue` | `fx.service.ts:493-503` | supplier_ledger_entries, fx_snapshots | — | fx.service.spec.ts | ✅ | ✅ |
| REQ-14 البونص | DECISIONS-09-25:20-21 | — | — | — | — | — | — | ❌ | ❌ |
| REQ-17/18 فرز التالف ومطالبات الموردين | DECISIONS-09-25:28-46 | — | — | — | — | — | — | ❌ | ❌ |
| REQ-21 هدايا العملاء | DECISIONS-09-25:57-58 | `/dashboard/customer-gifts` | `/api/org/customer-gifts/*` | `customer-gifts.service.ts` | customer_gifts | انتقالات ذرية، لا اعتماد ذاتي | customer-gifts.service.spec.ts | ✅ | ✅ |
| REQ-22 الحجوزات القديمة كشف فقط | DECISIONS-09-25:93-103 | `/dashboard/system/health` | `/api/inventory/jobs` | `inventory-jobs.ts:118-127` | job_runs | لا إفراج تلقائي | inventory-jobs.spec.ts | ✅ | ✅ |
| REQ-23 رفض المنتهي في الأمانة | DECISIONS-09-25:105-106 | `/dashboard/orders/new` (أمانة) | `POST /api/inventory/consignment/stock` | `consignment.service.ts:159-177` | consignment_stock | assertSellableBatch | consignment.service.spec.ts | ❌ | ✅ |
| REQ-24 EXP-1 | DECISIONS-09-25:134-140 | `/dashboard/hr/expenses` | `POST /api/org/expenses/:id/reject` | `expenses.service.ts:153-165` | expense_claims | — | expenses.service.spec.ts | ❌ | ❌ |
| REQ-25 AP مبني على الاستلام | P1 pack:424 | `/dashboard/receiving` | `POST /api/inventory/transactions/goods-receipt` → حدث | `saga-listener onGoodsReceived` | supplier_ledger_entries | — | supplier-ledger.service.spec.ts | ✅ | ✅ |
| REQ-27 ترقيم PO وحصره | P1 pack:426 | `/dashboard/purchase-orders` | `POST /api/accounting/matching/purchase-orders` | `matching.service.ts:97-123` | purchase_orders, document_sequences | SUPER_ADMIN | matching.service.spec.ts | ❌ | ✅ |
| REQ-28 المطابقة على الاستلام الفعلي | P1 pack:427 | `/dashboard/matching` | `POST /api/accounting/matching/vendor-invoices` | `matching.service.ts:644` | purchase_order_receipts | cumulative qty | matching.service.spec.ts | ❌ | ✅ |
| REQ-30 FX محقق لسداد الموردين | P1 pack:429 | `/dashboard/payables` | `POST /api/accounting/supplier-payments` | `supplier-payments.service.ts:84` | supplier_payments | — | supplier-payments.service.spec.ts | ❌ | ❌ (غير mounted) |
| REQ-31 ETA مؤجل | TODO-IMPORTANT | — | — | — | — | — | — | (مؤجل) | (مؤجل) |
| REQ-39/40 خصم 12% وسقف | REQUESTS-09-25:73؛ ACC-AUDIT-09-28:72 | `/dashboard/orders/new` | `POST /api/sales/orders` | `orders.service.ts:21, 556-570` | sales_order_lines | سقف/صلاحية | orders.discount-governance.characterization.spec.ts | ⚠️ (SAL-04) | ⚠️ (SAL-05) |
| REQ-41 اعتماد ≥100,000 | P1 pack:127 | `/dashboard/approvals/requests` | `POST /api/sales/orders/:id/approve` | `orders.service.ts:20, 642` | order_approvals | SoD | orders.service.spec.ts | ✅ | ✅ |
| REQ-47/49 تعريفة الشحن وخارج VAT | SHIPPING-TARIFF | `/dashboard/orders/new`, `/invoices/new` | `POST /api/sales/shipping/quote` | `shipping.service.ts:150-255` | shipping_zones/rates | override بسبب | shipping.service.spec.ts | ✅ | ✅ |
| REQ-53 التحصيل لفواتير محددة | roadmap:9 | `/dashboard/collection`, `/accounts` | `POST /api/accounting/payments` (`allocations[]`) | `payments.service.ts:528-708` | payment_allocations | — | payments.service.spec.ts | ⚠️ (لا عكس — ACC-07) | ⚠️ |
| REQ-58 الخزينة إلزامية في التحصيل | F01 | `/dashboard/cash-banks` | `POST /api/accounting/payments` | `resolveTreasuryAccount` | financial_account_entries | اختياري للشيك | payments.service.spec.ts | ⚠️ | ⚠️ |
| REQ-59 الشيك المرتد يعكس الدين والعمولة | F02 | `/dashboard/collection` | `POST /api/accounting/payments/checks/:id/status` | `payments.service.ts:405-470` + incentives intake | payments, incentive_ledger | — | payments.service.spec.ts, intake.service.spec.ts | ⚠️ (لا عكس خزينة) | ⚠️ |
| REQ-61 سياسة الحوافز | F04 | `/dashboard/incentive-rules` | `/api/incentives/rules` | `incentive.engine.ts:53-63` | rule_sets, incentive_ledger | — | incentive.engine.spec.ts | ❓ | ❓ |
| REQ-65 المطابقة بالكمية المستلمة | F08 | = REQ-28 | | | | | | ❌ | ✅ |
| REQ-67 مرتجع فاتورة مسددة | F10 | `/dashboard/returns` | حدث `sales.return.created` | `invoices.service.ts:909-943` | invoices, credit_notes | — | — | ❌ | ❌ |
| REQ-72 قفل الفترات | [Claim] RTM | `/dashboard/accounting`, `/period-close` (C) | `POST /api/accounting/fiscal-periods/:id/close` | `fiscal-periods.service.ts` | fiscal_periods | — | fiscal-periods.service.spec.ts | ❌ | ⚠️ |
| REQ-73 VAT/نموذج 41 | [Claim] RTM | `/dashboard/settings/taxes` | `GET /api/accounting/tax/vat-summary`, `form-41` | `tax.service.ts:70, 139` | tax_entries | يدوي | tax.service.spec.ts | ⚠️ | ⚠️ |
| REQ-77 ميزان المراجعة | [Claim] RTM | `/dashboard/accounting`, `/general-ledger` (C) | `GET /api/accounting/coa/trial-balance`, `/general-ledger/trial-balance` | `coa.service.ts:208` / `general-ledger.service.ts:114` | chart_of_accounts / journal_* | — | general-ledger.integration.spec.ts (يُتخطى بلا DB) | ❌ (أرصدة غير مرحلة) | ❌ (ACC-02) |
| REQ-79 الرواتب | RTM HR | `/dashboard/hr/payroll` | `/api/org/payroll/runs/*` | `payroll.service.ts` | payroll_* | الحاسب≠المعتمِد | payroll.service.spec.ts | ⚠️ (ORG-03) | ⚠️ |
| REQ-80 SoD للأدوار | [Claim] RTM | `/dashboard/settings/security` | `GET /api/iam/sod/scan` | `sod.service.ts` | roles, permissions | كشفي | sod.service.spec.ts | ⚠️ | ⚠️ |
| P-05 Order-to-cash (عملية) | DECISIONS-09-25 ر | `/dashboard/orders`, `/orders/new` | `POST /api/sales/orders` … | saga (§P-06) | sales_*, inventory_reservations, invoices | ائتمان + اعتماد | orders.credit-race.integration.spec.ts, saga.processed-events.integration.spec.ts | ⚠️ (SAL-01..03) | ❌ (ACC-02) |
| P-09 التحصيل والعكس | — | `/dashboard/collection`, `/invoices/[id]` | `POST /api/accounting/payments`, `/:id/reverse` | `payments.service.ts` | payments, ledger_entries, financial_account_entries | idempotency، SERIALIZABLE | payments.service.spec.ts, payments.audit-chain.integration.spec.ts | ⚠️ (ACC-06/07) | ❌ (ACC-02/03/04) |
| P-14 الشراء حتى الدفع | P1 pack | `/dashboard/purchase-orders`, `/receiving`, `/payables` | matching/* ، goods-receipt | matching + saga-listener | purchase_*, vendor_*, supplier_* | SoD | matching.service.spec.ts, payables.spec.ts | ⚠️ (لا سداد) | ⚠️ (غير mounted) |
| P-18 GL | ACC-AUDIT-09-28 | `/dashboard/accounting/journals`, `/gl-workbench` (C) | `/api/accounting/general-ledger/*` | general-ledger.service.ts | journal_* | approval بلا SoD | accounting-posting.spec.ts, gl-posting.integration.spec.ts | ❌ | ❌ |

**ملاحظة على عمود Test:** وجود 222 ملف spec لا يعني تغطية فعالة؛ بعض اختبارات التكامل تُتخطى بلا قاعدة (`gl-posting.integration.spec.ts:5-23`)، وبعضها يحاكي SQL (`inventory-jobs.spec.ts:29-53`) فلم يكتشف INV-06، واختبار عكس GL يتحقق من المجاميع فقط (ACC-04). لم تُشغّل الاختبارات في هذه المراجعة (خارج التفويض).
