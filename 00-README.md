# حزمة مراجعة Nile Pharma ERP

- **الجزء الأول — As-Is Audit** (2026-10-01): الوثائق 00–16.
- **الجزء الثاني — تحليل فجوات متطلبات الأعمال وتوصيات معمارية البيانات** (2026-10-04): الوثائق 20–34. **للمناقشة والاعتماد**؛ لم يبدأ أي إصلاح.

## كيف تقرأ الحزمة
1. ابدأ بـ`01-Executive-Summary-AR.md` (5 دقائق).
2. ثم `02-Full-As-Is-Audit-Report.md` (الصورة الكاملة مع روابط لكل تفصيل).
3. للجزء الثاني: `20-BRGA-Overview.md` ثم `27-Priority-Map.md` و`25-Decisions-Conflicts-and-Open.md` و`28-Owner-Questions.md`، ثم `30-Data-Architecture-Recommendations.md` و`31-ADRs.md`. التصحيحات على الجزء الأول في `34-Errata.md`.
4. للمناقشة: `12-Findings-Register.md` (أو `findings-register.csv` للفرز) و`13-Evidence-Requests-and-Open-Questions.md` و`14-Recommendations-for-Discussion.md`.

## الفهرس
| الملف | المحتوى |
|---|---|
| `01-Executive-Summary-AR.md` | الملخص التنفيذي |
| `02-Full-As-Is-Audit-Report.md` | التقرير الكامل |
| `03-System-Inventory-and-Architecture.md` | الجرد، المسؤوليات، التقنيات، الحدود، الاعتماديات، الموثق مقابل الكود مقابل التشغيل |
| `04-How-the-System-Runs.md` | البدء، مسار الطلب، المصادقة، المعاملات، الأحداث، retries/idempotency، المهام، config، المراقبة، sequence diagrams |
| `05-API-Inventory-and-Routing.md` + `api-inventory.csv` | التوجيه، BFF، 553 route بالحراس والصلاحيات والـDTO والجداول وحالة التفعيل واستخدام الواجهة |
| `06-ERD-and-Data-Model.md` | النماذج، ERDs، ملكية البيانات، مقارنة B↔C↔migrations↔القاعدة |
| `07-Data-Dictionary.md` | قاموس بيانات لكل حقل في 175 model + enums |
| `08-Business-Process-Catalogue.md` | 25 عملية + الغائبة، swimlanes ومخططات حالات |
| `09-Schema-Gap-Analysis.md` | فجوات الـschema |
| `10-Business-and-Process-Gap-Analysis.md` | توافق المتطلبات، الحلقات المكسورة، الضوابط، مصفوفة التتبع |
| `11-Deployment-and-Operations.md` | معمارية النشر، تدفق الإصدار، الإعدادات، الترحيل، النسخ، المسؤوليات |
| `12-Findings-Register.md` + `findings-register.csv` | 127 نتيجة بالحقول المطلوبة |
| `13-Evidence-Requests-and-Open-Questions.md` | طلبات أدلة قراءة فقط (E-01…E-30) + أسئلة المالك |
| `14-Recommendations-for-Discussion.md` | توصيات مرتبة (للمناقشة فقط) |
| `15-Coverage-Matrix.md` | ما روجع بالكامل/جزئيًا/لا يمكن التحقق منه |
| `16-Prior-Findings-Reassessment.md` | إعادة تقييم التقرير السابق وملاحظات التشغيل |
| **الجزء الثاني** | |
| `20-BRGA-Overview.md` | المنهج، المصادر (174)، الأرقام الدقيقة: 2,859 عبارة خام ← 499 معرّف متطلب ← 485 صافيًا |
| `21-Requirements-Register.md` + `register/C1…C10.md` + `requirements-register.csv` | سجل المتطلبات وبطاقة كاملة لكل متطلب |
| `22-Gap-Matrix.md` | مصفوفة الفجوات B/C والتغيرات وفجوات P1 |
| `23-Traceability-Matrix.md` + `traceability-matrix.csv` | المتطلب → العملية/الضابط → متطلب البيانات → التوصية المعمارية → معيار القبول |
| `24-Business-Rules-Catalogue.md` + `business-rules.csv` | 536 قاعدة أعمال وأين تُفرض |
| `25-Decisions-Conflicts-and-Open.md` | 194 قرارًا (75 مانعًا) + 9 تعارضات عابرة |
| `26-Acceptance-Criteria.md` | معايير القبول |
| `27-Priority-Map.md` | الأولويات حسب الأثر التجاري والعملية |
| `28-Owner-Questions.md` | أسئلة المالك في مجموعات صغيرة |
| `29-E2E-Processes-As-Is-To-Be.md` + `diagrams/brga/` | ثماني عمليات As-Is وTo-Be (32 رسمًا) |
| `30-Data-Architecture-Recommendations.md` + `diagrams/dar/` | المشكلات، البدائل والمقايضات، المعمارية المستهدفة، ERDs المقترحة، 20 توصية |
| `31-ADRs.md` | 13 قرارًا معماريًا مقترحًا |
| `32-Transition-Plan.md` | خطة انتقال مفاهيمية بالتحقق وشروط التراجع |
| `33-Evidence-and-Decisions-Before-Design-Approval.md` | أدلة قراءة فقط E-40…E-49 و16 قرارًا قبل اعتماد التصميم |
| `34-Errata.md` | تصحيح عبارات تجاوزت الدليل في الجزء الأول |
| `diagrams/*.mmd` | مصادر Mermaid قابلة للتعديل (43 + 13 ERD في `diagrams/erd/`) |
| `diagrams/svg/`, `diagrams/png/` | معاينات |
| `appendix/notes/*.md` | ملاحظات العمل التفصيلية لكل محور (بالإنجليزية، مع أدلة path:line ومعرّفات النتائج الأصلية) |
| `appendix/schema-*.md` | فروق الـschema وفحص آلي للفجوات والمراجع المنطقية |
| `appendix/tools/` | سكربتات الاستخراج الآلي (قراءة فقط) لإعادة الإنتاج |

## مفاتيح موحدة
- **النسخ:** `[B]` = BASELINE `89c2c31` (المرجحة للإنتاج، تطابق الصورة غير مثبت) · `[C]` = CURRENT `fa40270` (HEAD، غير منشور) · `[R]` = مخرجات تشغيل خام (`evidence/`) · `[U]` = ملاحظات تشغيل نقلها المستخدم بلا مخرجات خام.
- **التحقق:** Verified / Inferred / Unknown.
- **المسارات:** نسبية لجذر الـsnapshot المذكور (`apps/...`).
- **الرسوم:** كل رسم مبني من الكود أو الأدلة، ويُذكر مصدره في المستند الذي يستخدمه. الرسوم الكبيرة مقسمة (مثلًا ERD المحاسبة إلى AR/AP/GL/infra).

## ما لم يُفعل (حسب التفويض)
لا تعديل للكود أو الـschema أو الـmigrations أو الإعدادات؛ لا تثبيت/بناء/تشغيل/اختبارات؛ لا اتصال بالسيرفر أو القاعدة؛ لا طباعة أسرار؛ لم يُفتح محتوى `Data/` في الجزء الأول؛ في الجزء الثاني قُرئت **بنية** مصنفاتها فقط (عناوين الأعمدة وقواعد خطة الحوافز) دون أسماء أو مبالغ أفراد، ولم يُفك `Data.rar`. الاستثناء الوحيد: تشغيل محلل ملفات ساكن (`validate-schema-migrations.cjs`) و`node --check`.

## تنبيه حساسية
أرشيفات المصدر المرفقة (وليس هذه الحزمة) تحتوي مجلد `Data/` بملفات أعمال حقيقية (SEC-03). هذه الحزمة لا تتضمن أي محتوى منه، فقط أسماء ملفات في ملاحظات العمل.
