# 16 — إعادة تقييم نتائج التقرير السابق (`Nile_Pharma_As_Is_Findings_20261001.md`) وملاحظات التشغيل المنقولة

> الحكم: **مؤكد** (الدليل الجديد يدعمه) · **مؤكد مع تعديل** · **مُرقّى** (أصبح أقوى بدليل جديد) · **مُصحّح** (تجاوز الدليل أو كان غير دقيق) · **باقٍ Unknown**.

## 1. نتائج التقرير السابق F01–F15

| ID | ملخص السابق | الحكم | ما تغيّر / الدليل | الربط بالسجل الجديد |
|---|---|---|---|---|
| F01 | HEAD = fa40270 على main | **مؤكد** | `evidence/git-and-schema.txt:4-10` يؤكد أن HEAD بقي fa40270 **وقت التصدير** (05:57Z) — يغلق تحفظ F15 حول ثبات اسم الأرشيف | — |
| F02 | ملفات خارج git (`.deploy/`, `.env.backup.*`, `.pnpm-store/`) | **مؤكد مع إضافة** | `.gitignore:6-12` لا يغطي `.env.backup.*` → خطر commit عرضي | SEC-09 |
| F03 | هوية حاوية المحاسبة | **مؤكد** | `evidence/runtime.txt:2-7` | ARC-01 |
| F04 | اختلاف fa40270 عن tag 89c2c31؛ provenance Unknown | **مُرقّى** | ملاحظة جديدة: عدد جداول `nile_accounting` و`nile_organization` يتسق مع schema CURRENT لا BASELINE (مؤشر لا إثبات <sup>[تصحيح 34]</sup>)؛ ووجود جداول inventory الخاصة بـCURRENT → عدم اليقين حول الكود العامل **أكبر** مما افترضه السابق. وE-05 يضيّق الاحتمالات (لا يثبت commit بعينه) | ARC-01, ARC-02 |
| F05 | image ID ≠ compose image label | **مؤكد، السبب Unknown** | لا جديد؛ E-05 | ARC-01 |
| F06 | مصادر compose والـenv (`/tmp/nile-recovery-release.env`) | **مؤكد مع إضافة** | label `com.docker.compose.depends_on=""` (runtime.txt) بينما الملف يعلن تبعيات → متسق مع `up --no-deps` كما في `SERVER-STEPS-2026-09-25-ar.md`؛ ويختلف عن `.deploy/release.env` الذي يستخدمه `deploy-production.sh:12` في CURRENT | ARC-01 |
| F07 | هدف قاعدة المحاسبة؛ resolver يفضل `ACCOUNTING_DATABASE_URL` ثم `DATABASE_URL` | **مُصحّح جزئيًا** | الـresolver في `config/env.ts:57` يفعل ذلك **للتحقق فقط**؛ اتصال Prisma في accounting (و6 خدمات أخرى) يستخدم `DATABASE_URL` وحده (`prisma.service.ts` بلا `datasources`). في الإنتاج compose يمرر `DATABASE_URL` فقط، فلا أثر حالي | OPS-13 |
| F08 | تعليقات Neon/TLS مقابل `nile-postgres`؛ "REVIEW ITEM" | **مُرقّى** | لم تعد مجرد تعليقات: أدوات النشر في CURRENT **تعتمد فعليًا** على Neon (فحص `nc` من المضيف، snapshot عبر Neon API، parity 16) — `deploy-production.sh:72-110`؛ واختبار العقد يفترض Neon (`merge-launcher.test.js:109-110`). الخرائط التسع لقواعد البيانات **Verified** في compose (`docker-compose.production.yml:190-198`) | OPS-01, ARC-04 |
| F09 | pnpm 9.1.0، Prisma 5.22.0 | **مؤكد** | `package.json` | — |
| F10 | فشل `migrate status` ليس دليل DB | **مؤكد** | لا جديد؛ المقترح بديلًا: E-03 داخل الحاوية/القاعدة دون تصدير أسرار | DB-01 |
| F11 | تغيّر models بين المرجعين؛ ربط commits استنتاج سابق | **مُرقّى إلى Verified** | `git-and-schema.txt:590-594` (MODEL INTRODUCTION COMMITS: d5a9e2d، da88982، 3976e08، 634b101) + تحليل آلي: +13 model في accounting، +2 inventory، +1 organization، حقول في crm. حالة جداول الإنتاج ما زالت تحتاج E-03/E-04 | ARC-02 |
| F12 | 41 migration؛ الأسماء المتشابهة ليست دليلًا على تكرار | **مؤكد مع تفصيل** | BASELINE = **30** migration (القائمة تنتهي بـ`20260924120000_po_workflow_and_match_sod`). `supplier_payments` ×2 ليست تكرارًا بل **شكلان متعارضان** (v1 بـFK ومبالغ أساسية، v2 بحقول FX)؛ `general_ledger` → `gl_workbench` تتابع **معتمد** (الثاني يقرأ أعمدة الأول ويحوّلها). تعديل migrations بعد إنشائها **Verified** من git (`accounting-migration-history.txt`). `production-migrate.sh:95-100` يفسر exit 3 كرفض بوابة الـschema، والبوابة **تنجح على BASELINE وترفض CURRENT** (تشغيل ساكن) | DB-01, DB-02, DB-03 |
| F13 | ملفات Prisma generated على المضيف | **باقٍ Unknown** | `apps/*/generated/` في `.gitignore:20` → غير موجودة في الأرشيف؛ لا يمكن مقارنتها | — |
| F14 | Healthy ≠ سلامة الأعمال | **مؤكد ومُعزز** | الآن توجد defects ساكنة محددة تمس السلامة المالية في النسخة المرجحة: عكس التحصيل لا يعكس الخزينة (ACC-06)، غياب GL (ACC-01)، PAID فوق DELIVERED (SAL-01)، تعرض ائتمان متضخم (SAL-03)، مرتجع الفاتورة المسددة (ACC-18). **أثرها على البيانات الفعلية ما زال Unknown** حتى E-13/E-14 | ACC-*, SAL-* |
| F15 | تغطية حزمة handoff غير محققة | **مُصحّح: محققة** | المحتوى يطابق القائمة المقصودة، والـchecksums الداخلية OK. **ملاحظة جديدة مهمة:** الأرشيفان يحتويان مجلد `Data/` بملفات أعمال حقيقية (رواتب، عملاء، فواتير) لأنه committed — الحزمة **ليست خالية من البيانات الحساسة**. لم يُعثر على أسرار إنتاجية في الملفات المتتبعة (فحص بالأسماء) | SEC-03 |

## 2. "التصحيحات الضرورية" في التقرير السابق
كلها **مؤكدة** ولا أعارض أيًّا منها:
1. "runtime مبني حتمًا من 89c2c31" أقوى من الدليل — **مؤكد، ويزداد ضعفًا** بأدلة ARC-02.
2. "different generations confirmed داخل production" — **مؤكد أنه غير مثبت**؛ لكن الآن يوجد مؤشر ثانوي قوي على أن **القاعدة** من جيل أحدث من **الصورة** المفترضة (Inferred، لا Verified).
3. الأسماء المتشابهة ليست defects — **مؤكد**، مع التوضيح في F12 أعلاه.
4. `migrate status` لم يقرأ DB — **مؤكد**.
5. الحزمة كافية لـstatic review لا لـFull production capture — **مؤكد**.

## 3. ملاحظات التشغيل المنقولة (`NilePharma_Audit.docx`) — ما يُعتمد وما يُصحَّح

| الادعاء في الملاحظات | الحكم | السبب |
|---|---|---|
| "نسخة التشغيل الحالية مبنية على 89c2c31 لأن كل الصور تحمل release-89c2c31" (docx:37-46) | **مُصحّح** | الـtag اصطلاح تسمية قابل لإعادة الاستخدام؛ المثبت هو الاسم فقط (ARC-01) |
| "Database-per-Service داخل PostgreSQL واحد" (docx:288-317) | **مؤكد** من compose (9 روابط) + runtime للمحاسبة | — |
| "web لا يتصل بالقاعدة مباشرة" | **مؤكد** من الكود | — |
| "مفيش service بتدخل مباشرة على DB خدمة ثانية — لازم نتأكد" (docx:364-366) | **مؤكد من الكود** | كل خدمة تتصل بـ`DATABASE_URL` الخاص بها؛ db-migrate فقط يرى الكل. صلاحيات أدوار DB لم تُتحقق (E-29) |
| "nile_accounting: 7 migration records" (docx:472-473) | **مُصحّح (لا يُعتمد)** | من `n_live_tup` التقديري ويتعارض مع وصف لاحق لـ`_prisma_migrations` حتى bank_reconciliation |
| "50 جدولًا في accounting، 28 sales، 26 organization، 21 crm، 6 incentives" | **مقبول كدليل ثانوي** ومتسق رقميًا مع CURRENT في accounting/organization — **لا يثبت إصدار القاعدة** <sup>[تصحيح 34]</sup> | أساس ARC-02 |
| "الـrequest flow: NPM → web فقط" | **متسق مع الكود** (rewrites مخبوزة) — إعداد NPM نفسه `[U]` | — |
| "docker-compose.postgres.yml لم يكن في git عند 89c2c31 ولا history" | **مؤكد للغياب في النسختين**؛ history غير متاح في الأرشيف | ARC-03 |
| "pg_accounting غالبًا orphan" | **مؤكد مع تفسير محتمل**: الاسم يطابق volume في `docker-compose.yml` التطويري تحت اسم مشروع المجلد | OPS-08 |
| "nile-internal Internal=false" | مقبول `[U]`؛ الشبكة غير معرّفة في git | OPS-12 |
| "خط النشر عمل REFUSE بسبب drift" + "P3009 ثم ROLLED_BACK ثم APPLIED بـ0 steps" | **متسق** مع تشغيل الـvalidator الساكن (CURRENT يفشل) ومع `production-migrate.sh` | DB-01, DB-02 |
| "الخدمات كلها healthy فالنسخة الحالية شغالة" | **مؤكد كلقطة** فقط | — |
| CPU steal على المضيف | خارج نطاق الكود؛ لا عينات خام؛ لا يُخلط بأي defect تطبيقي | — |
