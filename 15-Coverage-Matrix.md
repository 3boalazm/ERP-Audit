# 15 — مصفوفة التغطية (Coverage Matrix)

> **Full** = روجع بالكامل · **Partial** = روجع جزئيًا (يُذكر ما لم يُراجع) · **Not verifiable** = لا يمكن التحقق من الأدلة المتاحة · **Not reviewed** = خارج ما أمكن في هذه الجولة.

## 1. المدخلات والأدلة

| المدخل | الحالة | ملاحظات |
|---|---|---|
| الحزمة `nile-pharma-audit-handoff-20261001.tar.gz` | Full | فُكت؛ `SHA256SUMS.txt` للأرشيفين الداخليين **OK**؛ لا checksum للحزمة الخارجية أو evidence (كما ذكر التقرير السابق) |
| `nile-pharma-current-fa40270.tar.gz` | Full | `git archive` (ملفات committed فقط؛ لا history ولا untracked) |
| `nile-pharma-production-89c2c31.tar.gz` | Full | نفس الحدود |
| `evidence/git-and-schema.txt` | Full | يؤكد HEAD=fa40270 وقت التصدير وقائمة commits بعد 89c2c31 |
| `evidence/runtime.txt` | Full | **حاوية accounting فقط** |
| `evidence/accounting-migration-history.txt` | Full | تعديلات migrations بعد إنشائها |
| `Nile_Pharma_As_Is_Findings_20261001.md` | Full | أُعيد تقييمه في `16` |
| `NilePharma_Audit.docx` | Full (كمصدر ثانوي `[U]`) | ملاحظات تشغيل منقولة بلا مخرجات خام |
| `Data/` داخل الأرشيفين | Not reviewed (عمدًا) | أسماء فقط — بيانات حساسة |

## 2. المحاور المطلوبة

| المحور | الحالة | ما رُوجع | ما لم يُراجع / حدود |
|---|---|---|---|
| 2. System inventory & architecture | Full (كود) / Partial (تشغيل) | كل التطبيقات والحزم والتبعيات والأحداث | التشغيل الفعلي لغير المحاسبة من `[U]` |
| 3. How the system runs | Full (كود) | البدء، الطلب، المصادقة، المعاملات، الأحداث، retries، المهام، config، logging/health | سلوك runtime لم يُلاحظ؛ `packages/contracts/api.ts` لم يُراجع |
| 4. API routing & contracts | Full (جرد آلي لـ553 route) / Partial (تفاصيل) | method، المسار الخارجي/الداخلي، handler، الصلاحيات، الحارس، DTO، mounting، استخدام الواجهة، جداول على مستوى controller | **Response contracts لكل route، حقول validation لكل DTO، الجداول/الأخطاء لكل handler** — للمسارات الحرجة فقط |
| 5. Database / ERD / schema gap | Full (Prisma + migrations) | 175 model، Data Dictionary، ERDs، مقارنة B↔C↔migrations، فحص validator ساكن | **القاعدة الفعلية: Not verifiable** |
| 6. Business processes | Full للعمليات الأساسية / Partial للثانوية | 25 عملية | تفاصيل حسابات الرواتب والضريبة المصرية، محرك العروض، لوحة الميدان |
| 7. Business & process gaps | Full | توافق 50+ متطلبًا، حلقات مكسورة، ضوابط، traceability | لا متطلبات معتمدة كمرجع؛ الاختبارات لم تُشغّل |
| 8. Deployment & operations | Full (كود ووثائق) / Partial (تشغيل) | compose ×5، Dockerfiles ×11، workflows ×3، 15+ سكربت، runbooks | إعداد NPM، GitHub environments، cron المضيف، تعريف Postgres: Not verifiable |
| 9. Security / reliability / maintainability | Full (ساكن) | المصادقة، التفويض، الأسرار (بالأسماء)، التحقق، التدقيق، التزامن، الأحداث | لا اختبار اختراق، لا فحص ثغرات اعتماديات (Trivy/audit) — خارج التفويض |

## 3. حسب الخدمة

| الخدمة | الكود | Schema/Migrations | العمليات | التشغيل |
|---|---|---|---|---|
| accounting | Full (27 module؛ الرياضيات التفصيلية لـFX/landed-cost جزئية) | Full | Full | Partial (`[R]` حاوية واحدة) |
| sales | Full (محركات العروض/الأسعار جزئيًا) | Partial (SQL لمigrations محددة) | Full | Not verifiable |
| crm | Full (profile/notes جزئيًا) | Full | Full/Partial (الميداني) | Not verifiable |
| inventory | Full | Full | Full | Not verifiable |
| products | Full (UOM/price-lists جزئيًا) | Full (schema) / Partial (SQL) | Full | Not verifiable |
| iam | Full (prompts/engine الـCopilot لم تُراجع) | Full | Full | Not verifiable |
| organization | Partial (منطق العقود والمعادلات) | Full | Partial | Not verifiable |
| incentives | Full | Full | Full | Not verifiable |
| audit-aggregator | Full | Full | Full | Not verifiable |
| web | Full (auth/BFF/routing)، Partial (منطق كل صفحة) | — | — | Not verifiable |
| packages | Full (events, scheduler, audit, security)، Partial (contracts api) | — | — | — |

## 4. ما لم يُفعل عمدًا (حسب التفويض)
لا تثبيت حزم، لا بناء، لا تشغيل تطبيقات أو اختبارات، لا اتصال بالسيرفر أو القاعدة، لا تعديل في المصدر. الاستثناءات المحدودة: تشغيل `scripts/validate-schema-migrations.cjs` (parser ملفات بلا DB وبلا كتابة) و`node --check` (فحص syntax) على النسختين، وسكربتات قراءة كتبتها خارج المصدر (`tools/`).
