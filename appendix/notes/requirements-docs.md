# Requirements, Decisions & Prior-Audit Documents — As-Is Audit Notes

Area: documented requirements / business decisions / prior audit & QA claims (`docs/`, `QA-REPORTS/`, `README.md`, `PRODUCTION_HARDENING.md`, `docs/architecture`, `docs/audit`, `docs/roadmap`).
Snapshots: CURRENT = `cur/` (fa40270, not deployed) · BASELINE = `base/` (89c2c31, likely running).
All paths below are relative to the snapshot named in brackets, e.g. `[cur] docs/X.md:12`. Code checks are static (grep/read). Nothing here proves runtime behaviour.

---

## 1. Scope covered / not covered

| Item | Coverage | Notes |
|---|---|---|
| Decision records: `DECISIONS-AR.md`, `DECISIONS-2026-09-25-ar.md`, `P1-BUSINESS-DECISION-PACK.md`, `QA-DECISIONS-AR.md`, `SHIPPING-TARIFF-AND-TAX-DECISION-AR.md`, `TODO-IMPORTANT.md`, `REQUESTS-2026-09-25-ar.md` | Full | Read completely |
| `REQUIREMENTS-TRACEABILITY-MATRIX.md` (RTM) | Full | All 62 rows; every referenced file checked for existence in both snapshots |
| `roadmap/2026-09-19-customer-field-execution-ar.md` | Partial | "Approved user decisions" section (l.3-13) + onboarding batch read |
| `roadmap/2026-09-19-operations-expansion-ar.md` | Partial | Headings only |
| `audit/2026-09-18-company-workflows-vs-erp-ar.md` | Full (§2-§4) | Source of company-process requirements F01-F13 |
| `audit/2026-09-20-backlog-traceability-ar.md` | Partial | Conflicts + summary |
| `GO-LIVE-ACCEPTANCE-REPORT.md`, `HEAVY-VERIFICATION-AR.md` (§1-2), `AUDIT-COMPLETENESS-MATRIX.md` (head), `DISASTER-RECOVERY-DRILL-REPORT.md` (header), `QA-REPORTS/00-INDEX.md` | Partial-Full | Reliability evaluation |
| `REPORTS-IMPLEMENTATION-STATUS.md` | Full | Endpoints checked in both snapshots |
| `ACCOUNTING-AUDIT-2026-09-28-IMPLEMENTATION.md`, `P0-ACCOUNTING-MEGA-WAVE.md`, `PRODUCTION-LAST-MILE.md`, `phase1-master-data-data-io.md`, `BACKEND-DATA-IO-STANDARD.md` (head) | Full/Partial | CURRENT-only docs |
| `ERP-EMPLOYEE-PAYROLL-DESIGN.md`, `INVOICE-CONCEPT-AR.md`, `AUDIT-REMEDIATION-STATUS-2026-09-25-ar.md`, `PRODUCTION_HARDENING.md`, `README.md` | Partial | Checked for contradictions with code |
| `docs/architecture/ai-operations/*` | Partial | Headers/status only (AI copilot proposals, explicitly "proposed, not deployed") |
| `docs/audit/00..23-*.md` (Railway-era audit series), `P0-IMPLEMENTATION-PLAN.md`, `PROMPT-P1-P3-IMPLEMENTATION.md` (headings), `P1-AUDIT.md` (register + addendum), `GAP-ANALYSIS-AR.md`, `BUSINESS-FLOWS-COVERAGE*.md`, `BUSINESS-AUDIT-MATRIX.md`, `FIELD-SALES-AUDIT.md` | Partial (headings / grep) | Not line-by-line; used for deployment-narrative census and cross-references |
| Import result docs (`ERP-*-IMPORT-RESULT.md`, `CUSTOMER-IDENTITIES-IMPORT-*.md`, `IMPORT-TEMPLATES-AR.md`), `NOTIFICATIONS-PROVIDERS-AR.md`, `AI-PROVIDER-SETTINGS-ar.md`, runbooks, `SAFE-DEPLOY-AR.md`, `SERVER-STEPS-*`, `SHARED-PROXY-NETWORKS-AR.md`, `PRODUCTION-HOSTINGER.md` | Not reviewed in depth | Only grep census for platform names |
| QA-REPORTS/01..23 | Not reviewed individually | Index + corrections only; identical in BASELINE and CURRENT |
| `Data/` | Not opened (rule) | |

---

## 2. Inventory & classification of the requirement-bearing documents

Classification key: **D** = decision record (owner answer transcribed), **P** = proposal/plan/options, **S** = AI-generated status/implementation report, **Q** = QA/audit claim, **R** = requirement source derived from company artefacts.

| Document | Class | Date / baseline | Who "approved" | Exists in |
|---|---|---|---|---|
| `docs/DECISIONS-2026-09-25-ar.md` | D (+S status column) | 2026-09-25 | "رد صاحب النظام" (system owner reply) — no name, no signature (`l.3`) | BOTH |
| `docs/P1-BUSINESS-DECISION-PACK.md` §"Decisions confirmed — 2026-09-28" (`l.422-430`) | D | 2026-09-28 | Unnamed; 7 bullet decisions appended | **CURRENT only** (the appended section; rest of pack in both) |
| `docs/P1-BUSINESS-DECISION-PACK.md` BD-1..BD-8 body | P (options; BD-5 marked DECIDED `l.198`) | baseline `c87961d`, 2026-09-24 | n/a | BOTH |
| `docs/DECISIONS-AR.md` | P (l.1-196) + S "implementation status" (l.200-268) | ~2026-09-14 (migrations named 20260914*) | Implicit ("قرارك" l.255) | BOTH |
| `docs/roadmap/2026-09-19-customer-field-execution-ar.md` l.3-13 "قرارات المستخدم المعتمدة" | D | 2026-09-19 | "the user" | BOTH |
| `docs/REQUESTS-2026-09-25-ar.md` | P (12 requests, options, questions); update note l.286 points to decisions file | 2026-09-25 | n/a | BOTH |
| `docs/SHIPPING-TARIFF-AND-TAX-DECISION-AR.md` | D (tariff "معتمدة" l.21) + interim tax rule | undated | Unnamed | BOTH |
| `docs/QA-DECISIONS-AR.md` | D (technical/UX intentional behaviours) | 2026-09-21 | QA review | BOTH |
| `docs/TODO-IMPORTANT.md` | D (ETA deferred) | 2026-09-28 | Unnamed | **CURRENT only** |
| `docs/audit/2026-09-18-company-workflows-vs-erp-ar.md` | R + Q (company money/goods cycles from company files, F01-F13 gaps) | 2026-09-18 | n/a (requirements stated as "المطلوب") | BOTH |
| `docs/audit/customer-classification-rep-territory-2026-09-02.md` | R (owner explanation of letter codes, CHAINS type) | 2026-09-02 | "business owner's explanation the same day" (l.6) | BOTH |
| `docs/PROMPT-P1-P3-IMPLEMENTATION.md` | P (AI prompt / design spec, flows 1-11) | ~2026-09-24 | n/a | BOTH |
| `docs/REQUIREMENTS-TRACEABILITY-MATRIX.md` | S/Q (self-declared "VERIFIED & OPERATIONAL (100%)") | undated, v1.0.0 | none | BOTH |
| `docs/ACCOUNTING-AUDIT-2026-09-28-IMPLEMENTATION.md`, `P0-ACCOUNTING-MEGA-WAVE.md` | S | 2026-09-28 | none; explicitly "no green result is claimed" | **CURRENT only** |
| `docs/GO-LIVE-ACCEPTANCE-REPORT.md` | Q (script output) | 2026-09-24 | explicitly "No CFO, CISO, or SRE has signed" (l.7-8) | BOTH |
| `docs/HEAVY-VERIFICATION-AR.md` | Q (claims live run on branch `arena/01a0a585`) | 2026-09-15 | none | BOTH |
| `QA-REPORTS/*` | Q (claims live run on branch `arena/01a0c3f9`) | 2026-09-21 | none | BOTH (identical) |
| `docs/AUDIT-COMPLETENESS-MATRIX.md` | Q with automated enforcer spec | undated | none | BOTH |
| `docs/REPORTS-IMPLEMENTATION-STATUS.md` | S | undated ("Phase 6") | none | BOTH |

**Answer to Goal 1 (do approved business requirements exist?):** Partially. There is **no approved SRS / BRD / signed requirements baseline** in the repository. What exists are (a) decision logs transcribing owner answers to AI-agent questions (`DECISIONS-2026-09-25-ar.md`, P1 pack §2026-09-28, roadmap "approved user decisions", shipping tariff), with dates but **no named approver, no signature, no version control of the decision itself separate from the implementing agent's status column**; (b) options/proposal packs; (c) AI-generated status/RTM documents that self-certify. The RTM is not a requirements baseline: it lists implementation features with "VERIFIED" status, has no source/approver per requirement, and its counts are internally inconsistent (see REQDOC-02). Verified (document reading).

---

## 3. How requirements flow (as documented)

```mermaid
flowchart TD
  A[Company artefacts: Excel ledgers, incentive sheet, PO PDFs] -->|AI review| R[audit/2026-09-18 company-workflows F01-F13]
  O[Owner chat answers] --> D1[DECISIONS-2026-09-25-ar.md]
  O --> D2[P1 pack 'Decisions confirmed 2026-09-28' CURRENT only]
  O --> D3[roadmap 2026-09-19 approved user decisions]
  P[AI options packs: DECISIONS-AR, P1-BUSINESS-DECISION-PACK BD-1..8, REQUESTS-2026-09-25] -->|questions| O
  D1 --> I[Implementing agent commits + status column in same doc]
  D2 --> I
  I --> S[AI status reports: ACCOUNTING-AUDIT-2026-09-28, REPORTS-IMPLEMENTATION-STATUS, RTM 'VERIFIED 100%']
  S --> G[go-live-acceptance-gate.cjs: file-exists / string-contains checks]
  G --> GL[GO-LIVE-ACCEPTANCE-REPORT 10/10 PASS - explicitly not sign-off]
  I -. no independent owner verification step documented .-> O
```

Example of a decided requirement fully traceable to code (both snapshots) — sales-return approval, from `[base] apps/sales/prisma/schema.prisma:173-178` and `[base] apps/sales/src/modules/returns/returns.service.ts:312-321`:

```mermaid
stateDiagram-v2
  [*] --> PENDING: rep records return (returnedQty reserved)
  PENDING --> APPROVED: approve by independent user (sales.returns.approve; creator blocked unless SUPER_ADMIN or sales.returns.approve.any)
  PENDING --> REJECTED: reject with reason (reservation released)
  APPROVED --> POSTED: SalesReturnCreated published
  APPROVED --> APPROVED: publish failed, stays
  POSTED --> [*]
  REJECTED --> [*]
```

Documented vs observed deployment (see §6 for evidence):

```mermaid
flowchart LR
  subgraph Documented_CURRENT[CURRENT docs + compose]
    C1[GH Actions CI -> digest images] --> C2[deploy-production.sh on Hostinger] --> C3[(Neon Postgres, 9 DBs)]
    C2 --> C4[Neon restore point before migrate]
  end
  subgraph Documented_OLD[docs/audit 00-23, payroll design]
    R1[Railway merged containers via merge-launcher.js] --> R2[(Neon)]
  end
  subgraph Observed[runtime.txt evidence]
    O1[accounting:release-89c2c31 tag, env /tmp/nile-recovery-release.env] --> O2[(nile-postgres:5432 local container, PG18)]
  end
```

---

## 4. Business processes documented (requirement view) — completeness

| Process | Documented rules (source) | Code status (static) |
|---|---|---|
| Order-to-cash: order → credit → approval → FEFO reservation → auto-invoice at StockReserved → ship/POD → collection | DECISIONS-2026-09-25 ر (invoice auto-issued at `StockReserved`, l.95); INVOICE-CONCEPT; DECISIONS-AR §3-5; roadmap decision 5 (collection allocated to specific invoices) | Implemented both (saga-listener `onStockReserved` → `invoices.generate` `[cur] apps/accounting/src/modules/saga-listener/saga-listener.service.ts:102-136`; PaymentAllocation model both). Approval threshold hard-coded 100,000 both (`[cur] apps/sales/src/modules/orders/orders.service.ts:20`) — BD-3 sub-question open |
| Returns & credit notes | DECISIONS-AR §1-2 (approval, CR-YYYY-NNNN, VAT negative entry gated) | Implemented both. Defect F10 (return after full payment rejected) open both |
| Procure-to-pay | P1 pack BD-1/BD-8 + 2026-09-28 #1-4,6 | **CURRENT only** for PO numbering/SUPER_ADMIN/receipt tracking/supplier payments; BASELINE: client PO number, match assumes received = ordered, no supplier payment |
| Inventory: reservations, consignment, damaged | DECISIONS-2026-09-25 ر, أ, ت-7..ت-9 | Stale-reservation = detect+alert only (both, matches decision). Consignment backend expiry check CURRENT only. Damage sorting / supplier claims: absent both |
| GL | DECISIONS-2026-09-25 l.122 states "no Journal Entry engine"; ACCOUNTING-AUDIT-2026-09-28 adds GL | GL modules (`general-ledger`, `gl-workbench`, manual journal workflow) **CURRENT only**; BASELINE has no journal engine (consistent with the 09-25 statement) |
| Tax / VAT / ETA | DECISIONS-AR §2; SHIPPING tax decision; TODO-IMPORTANT (ETA deferred) | VAT summary & Form 41 read only `TaxEntry`; only writers are manual `POST /tax/entries` and the gated credit-note VAT (both snapshots). No ETA code (both) |
| Pricing / discounts / bonus | REQUESTS (1-3); decisions ت-1..ت-6; 2026-09-28 #5 | 12% default both; order-time ceiling (≥100 rejected, >12% needs permission) CURRENT only; bonus lines (ت-2/ت-3) absent both; promotions engine not wired to order create (F11) |
| Field sales | roadmap decisions 1-9 | GPS exception reason + FieldProposal model present both (spot) |
| Expenses / customer gifts | ص-1/ص-2; EXP-1..3 | Gifts module + 4 permissions both; EXP-1 (reject from any state) present both |
| Payroll / HR | ERP-EMPLOYEE-PAYROLL-DESIGN (stale), RTM HR-007/008 | Payroll controller + Egyptian SI/tax engine present both; no documented owner approval of rates; doc says "not built" (stale) |
| Incentives | company sheet (F04: 750k threshold, cumulative tiers) | Engine marginal tiers; PaymentReversed consumer exists both; policy equivalence to sheet **not decided** |
| Shipping tariff | SHIPPING-TARIFF decision zones 1-10, fee outside VAT | Seeded both (`[base] apps/sales/prisma/migrations/20260923110000_add_shipping_tariffs/migration.sql:87`); invoice total = net + tax + shippingFee (`[cur] apps/accounting/src/modules/invoices/invoices.service.ts:1014`) |
| Reports | REPORTS-IMPLEMENTATION-STATUS | 4 report pages + 3 BFFs; all "assumed" endpoints exist both (§8) |

---

## 5. BASELINE vs CURRENT for this area

Docs:
- Only in CURRENT: `ACCOUNTING-AUDIT-2026-09-28-IMPLEMENTATION.md`, `BACKEND-DATA-IO-STANDARD.md`, `P0-ACCOUNTING-MEGA-WAVE.md`, `PRODUCTION-LAST-MILE.md`, `TODO-IMPORTANT.md`, `phase1-master-data-data-io.md`, `architecture/ai-operations/COPILOT-ERP-COVERAGE-ar.md`.
- Changed: `P1-BUSINESS-DECISION-PACK.md` (+ "Decisions confirmed — 2026-09-28" l.420-430), `P1-AUDIT.md` (+ "Current-state addendum — 2026-09-28" l.370-382), `P1-1C-IMPLEMENTATION-READINESS.md`, `P1-WAVE1-IMPLEMENTATION-NOTES.md`, `BLUEPRINT-ar.md` (tool count 20→22), `tool-registry.proposed.json`.
- `QA-REPORTS/`, `README.md`, `PRODUCTION_HARDENING.md`: identical.

Code consequences (Verified by module/migration diff):
- Accounting modules CURRENT-only: `audit-timeline, bank-reconciliation, finance-dashboard, general-ledger, gl-workbench, import-shipments, instruments, supplier-payments`; 11 accounting migrations `20260927120000_general_ledger` … `20260928210000_bank_reconciliation`.
- Other CURRENT-only migrations: organization `20260927133000_rep_coverage`; inventory `20260927170000_inventory_cost_layers`, `…173000_inventory_outbox`, `…190000_inventory_outbox_lease`; crm `20260927120000_lead_management`, `20260928133000_customer_pricing_profile`.
- Therefore **every decision dated 2026-09-28 and the GL / supplier-payment / FIFO-COGS / bank-reconciliation / import-shipment capabilities exist only in CURRENT (not deployed)**. Docs in CURRENT describing them in present tense ("Implemented in this wave") do not describe production.

---

## 6. Findings

### REQDOC-01 — No formally approved, versioned requirements baseline
- Domain: Governance ; Affected: BOTH
- Verification: Verified (document census) ; Type: Potential risk ; Severity: **Medium** — impedes acceptance testing and dispute resolution, no proven runtime impact.
- Evidence: `[cur] docs/DECISIONS-2026-09-25-ar.md:3` ("رد صاحب النظام", no name/signature); `[cur] docs/P1-BUSINESS-DECISION-PACK.md:422-430` (unnamed); `[cur] docs/REQUIREMENTS-TRACEABILITY-MATRIX.md:3-7` (self-declared "VERIFIED & OPERATIONAL (100%)", no approver, no date); `[cur] docs/GO-LIVE-ACCEPTANCE-REPORT.md:7-8` ("No CFO, CISO, or SRE has signed").
- Trigger: any acceptance/sign-off. Impact: status columns are written by the implementing agent in the same file as the decision; no independent confirmation that implementation matches intent.
- To close: owner signs a consolidated decision register (one row per decision: ID, text, date, approver, superseded-by), separate from implementation status.

### REQDOC-02 — RTM is not reliable as traceability evidence
- Domain: Governance/QA ; Affected: BOTH ; Verification: Verified ; Type: Confirmed defect (documentation) ; Severity: **Medium** — misleading "100% verified" claims about finance/tax/SoD controls.
- Evidence (all `[cur]`): summary says 60 REQs (`docs/REQUIREMENTS-TRACEABILITY-MATRIX.md:22`) but tables contain 62 rows (SAL 9 vs "8" l.18; HR 9 vs "8" l.19); gate reports "56/56" (`docs/GO-LIVE-ACCEPTANCE-REPORT.md:22`, `scripts/go-live-acceptance-gate.cjs:165-170`). Wrong verifying specs: REQ-SAL-005 incentives "verified" by `apps/sales/.../orders.service.spec.ts` (l.82); REQ-INV-007 QC and REQ-INV-010 serialization by `products.service.spec.ts` (l.67,70); REQ-SAL-004 returns attributed to `orders.service.ts` (actual: `returns.service.ts`). REQ-SEC-006 "64/64 verified" (l.115) vs `docs/AUDIT-COMPLETENESS-MATRIX.md:146` "63 events = 29 strong + 18 weak + 13 gap + 3 no publisher". REQ-INV-010 "DSCSA" is a US regulation (no Egyptian requirement documented). REQ-FIN-003 "prevent posting in closed periods" — see REQDOC-09. REQ-TAX-002/004 — see REQDOC-08. REQ-SEC-009 — see REQDOC-11.
- All referenced files exist in both snapshots (checked) — existence ≠ behaviour.
- To close: rebuild RTM from the signed decision register; each row: source, acceptance criterion, test name, last run evidence.

### REQDOC-03 — Go-live gate checks file existence/strings, not behaviour
- Domain: QA ; Affected: BOTH ; Verified ; Type: Confirmed defect (process) ; Severity: **Medium** — "10/10 PASS" can be produced with non-working code; report itself disclaims sign-off (mitigates).
- Evidence: `[cur] scripts/go-live-acceptance-gate.cjs:143-146` (k6 "PASS" if script file exists), `:152` (correlation interceptor file exists), `:160` (tax/landed-cost files exist ⇒ "ETA Tax Form 41 Fully Implemented"), `:165-170` (RTM passes if text contains "56" and "100%"), `:60-62` (SoD passes if matrix file contains two rule names).
- To close: treat GO-LIVE report as informational only; replace with executed test evidence.

### REQDOC-04 — Prior AI-generated evidence was fabricated and later retracted
- Domain: QA ; Affected: BOTH ; Verified ; Type: Operational uncertainty ; Severity: **Medium** — undermines trust in any un-reverified doc claim.
- Evidence: `[cur] docs/DISASTER-RECOVERY-DRILL-REPORT.md:3-10` (prior "147,820 rows restored", "RTO 1s", "hash-chain 100% verified", CISO/CFO sign-off "fabricated by `scripts/dr-backup-restore-drill.cjs` without contacting any database"); `[cur] docs/QA-DECISIONS-AR.md:57-59` (QA claims withdrawn: "118 items" file non-existent, `DEPLOYMENT_GUIDE.md`, `check-env.cjs`, etc.); `[cur] docs/GO-LIVE-ACCEPTANCE-REPORT.md:7-9`.
- To close: any doc claim used in the final report must be re-verified against code/evidence (this audit's rule).

### REQDOC-05 — 2026-09-28 owner decisions are implemented only in CURRENT; BASELINE (likely production) runs the superseded behaviour
- Domain: Procure-to-pay / Pricing ; Affected: BASELINE (gap) ; Verification: Verified (static code); production behaviour Inferred ; Type: Operational uncertainty ; Severity: **High** — financial controls the owner decided on (3-way match against real receipts, discount ceiling) are absent in the build believed to be in production.
- Evidence:
  - PO numbering / SUPER_ADMIN: present `[cur] apps/accounting/src/modules/matching/matching.service.ts:97-123`; absent `[base]` (grep: no `SUPER_ADMIN`, no `'PO'` sequence in matching).
  - Match GRN leg: `[base] apps/accounting/src/modules/matching/matching.service.ts:604` `receivedQtyTotal: orderedQtyTotal` vs `[cur] …:644` sums `l.receivedQty`.
  - Discount ceiling: `[cur] apps/sales/src/modules/orders/orders.service.ts:557` (`>= 100` rejected), `:569` (>12% needs permission); absent in `[base]` (12% default only, `orders.service.ts:21`).
  - Supplier payments / realized FX: `[cur] apps/accounting/src/modules/supplier-payments/supplier-payments.service.ts:84`; module absent in `[base]`; `[base] fx.service.ts:637 settleFxDifference` has no caller.
  - Decision text: `[cur] docs/P1-BUSINESS-DECISION-PACK.md:424-429`.
- Trigger: purchasing / discounting in production. Impact: vendor invoices may be approved against unreceived quantities; a 100% line discount is accepted on interactive orders (BD-3 documented this `[cur] docs/P1-BUSINESS-DECISION-PACK.md:125`).
- To close: confirm deployed image commit; `SELECT max(migration_name) FROM _prisma_migrations` per DB (see §9).

### REQDOC-06 — Owner's precondition for consignment ("reject expired/invalid batch in backend before any production use") is met only in CURRENT
- Domain: Inventory/Consignment ; Affected: BASELINE ; Verified (static) ; Type: Confirmed defect vs decision ; Severity: **Medium** — pharma expiry control; UI may still block (not verified), but backend gate required by the owner is missing.
- Evidence: decision `[cur] docs/DECISIONS-2026-09-25-ar.md:105-106`; `[cur] apps/inventory/src/modules/consignment/consignment.service.ts:128,159-177` (`assertSellableBatch`: blocked batch and expiry ≤ now rejected); `[base] …/consignment.service.ts:121-140` `loadLine` uses `applySignedDelta` and client-sent `expiryDate` with no expiry/blocked check.
- To close: verify deployed commit; query consignment_stock for rows with expiry_date < load date.

### REQDOC-07 — Return after full payment is rejected by Accounting while Inventory restocks (company requirement F10) — still open
- Domain: Order-to-cash / Returns ; Affected: BOTH ; Verification: Verified (code), consequence Inferred ; Type: Confirmed defect ; Severity: **High** — produces inventory/AR divergence on an ordinary business case.
- Evidence: `[base] apps/accounting/src/modules/invoices/invoices.service.ts:909-916` (`paid + newCredited > total` → `ConflictException`), same at `[cur] …:937-943`; requirement statement `[cur] docs/audit/2026-09-18-company-workflows-vs-erp-ar.md:168-182`. Inventory consumes `SalesReturnCreated` independently (DECISIONS-AR l.17-18).
- To close: owner decision on refund/customer-credit for paid invoices; integration test.

### REQDOC-08 — VAT return / Form 41 are built from manually entered TaxEntry rows; docs claim "fully implemented"
- Domain: Tax ; Affected: BOTH ; Verified ; Type: Potential risk ; Severity: **Medium** — depends on whether accountants key every entry (Unknown).
- Evidence: writer census — only `[cur] apps/accounting/src/modules/tax/tax.service.ts:70` (manual `POST /tax/entries`, controller l.34) and gated credit-note VAT `[cur] apps/accounting/src/modules/credit-notes/credit-notes.service.ts:73,90`; `getVatSummary` reads `prisma.taxEntry`; `generateForm41` reads `taxEntry.findMany` (`tax.service.ts:139-140`). Claims: RTM REQ-TAX-001..004 VERIFIED (`docs/REQUIREMENTS-TRACEABILITY-MATRIX.md:50-53`); GO-LIVE dim 9 "ETA Tax Form 41 + Landed Cost Fully Implemented" (`docs/GO-LIVE-ACCEPTANCE-REPORT.md:21`). Same gap described by `docs/DECISIONS-AR.md:57`. CREDIT_NOTE_VAT_POSTING off by default awaiting tax adviser (`docs/DECISIONS-AR.md:226-227`).
- To close: ask accountant how VAT returns are prepared; `SELECT count(*), min(created_at) FROM tax_entries` vs invoices count.

### REQDOC-09 — Fiscal-period lock is not applied to operational postings in BASELINE
- Domain: GL/Finance ; Affected: BASELINE (CURRENT partially: GL journals gated) ; Verification: Verified (absence by grep), effect Inferred ; Type: Potential risk ; Severity: **Medium**.
- Evidence: `[base]` no reference to `fiscalPeriod` outside `modules/fiscal-periods` and `app.module.ts` (invoices, payments, ledger, credit-notes do not check); `[base] apps/accounting/src/modules/fiscal-periods/fiscal-periods.service.ts:100-112` only flips status. `[cur] apps/accounting/src/modules/general-ledger/general-ledger.service.ts:12` rejects GL posting into CLOSED periods. RTM REQ-FIN-003 claims "prevent posting in closed periods" VERIFIED.
- To close: business rule — may invoices/payments be dated into a closed period?

### REQDOC-10 — Expense-claim lifecycle defects documented as P0 by the owner remain (EXP-1/EXP-3)
- Domain: Expenses ; Affected: BOTH ; Verified ; Type: Confirmed defect ; Severity: **Medium** — reject allowed after PAID; owner explicitly deferred.
- Evidence: `[cur] apps/organization/src/modules/expenses/expenses.service.ts:153-165` (`rejectClaim` updates to REJECTED with no status precondition); `:171` comment "triggers journal entry" (no posting); decision log `[cur] docs/DECISIONS-2026-09-25-ar.md:134-140`. EXP-2 (concurrent approvals) Inferred from same pattern (`update` without status condition).
- To close: owner instruction to fix.

### REQDOC-11 — "Toxic SoD rules enforced" is a detective scan, not a preventive control
- Domain: Security/Approvals ; Affected: BOTH ; Verification: Verified (no callers) ; Type: Potential risk ; Severity: **Low-Medium** — module-level self-approval guards do exist for returns and PO matching.
- Evidence: `[cur] apps/iam/src/modules/sod/sod.service.ts` exposes `getRules/detectConflicts`; controller only `GET rules|scan|evaluate` (`sod.controller.ts:15,21,27`); no other module calls `SodService` (grep). Claims: RTM REQ-SEC-009, GO-LIVE dim 2 "7/7 Toxic SoD Rules Enforced". Preventive per-flow SoD: `[cur] apps/sales/src/modules/returns/returns.service.ts:312-321`, `[cur] apps/accounting/src/modules/matching/matching.service.ts:237`.
- To close: decide whether role assignment must be blocked on toxic combinations.

### REQDOC-12 — Contradictory or overlapping owner decisions need reconciliation
- Domain: Pricing / FX ; Affected: BOTH docs ; Verified (text) ; Type: Question ; Severity: **Medium**.
- Evidence: (a) Pricing: `[cur] docs/DECISIONS-2026-09-25-ar.md:19-23` (ت-1/ت-4: one pricing rule chosen on the invoice + manual discount within the user's RBAC ceiling; bonus value/quantity) vs `[cur] docs/P1-BUSINESS-DECISION-PACK.md:428` (pricing rule chosen at customer creation, effective price stored on customer profile) and implemented 12% base + approval permission (`[cur] orders.service.ts:557-569`, `ACCOUNTING-AUDIT-2026-09-28:71-73`). (b) FX: BD-5 decided M2 reverse-then-repost revaluation (`P1-BUSINESS-DECISION-PACK.md:198`, implemented both — `fx.service.ts:493-503`) vs 2026-09-28 #6 "Supplier-payment FX uses Realized FX" (`:429`) — compatible only if revaluation reversal precedes settlement; not stated. (c) `AUDIT-REMEDIATION-STATUS-2026-09-25-ar.md` "BD-5 decision still open" vs DECISIONS file "implemented in c25817f".
- To close: owner confirms which pricing model governs and whether unrealized revaluation continues.

### REQDOC-13 — BD-2, BD-3, BD-4, BD-7 resolved in CURRENT code without a recorded owner decision
- Domain: Procurement / Treasury / Pricing ; Affected: CURRENT ; Verification: Verified (code) / Inferred (no decision) ; Type: Question ; Severity: **Low-Medium**.
- Evidence: import-shipments module placed inside accounting (`[cur] apps/accounting/src/modules/import-shipments`, migration `20260928140000_import_shipments`) — BD-2 options `P1-BUSINESS-DECISION-PACK.md:300-315`; supplier payment posts AP + treasury + GL (`ACCOUNTING-AUDIT-2026-09-28:58-60`) = BD-7 option 7-B, not in any decision list; BD-3 identity model and BD-4 vocabulary only indirectly addressed by 2026-09-28 #5.
- To close: owner ratifies or rejects.

### REQDOC-14 — Deployment documentation contradicts itself and the runtime evidence
- Domain: Deployment ; Affected: BOTH docs vs runtime ; Verification: Verified (docs + `evidence/runtime.txt`) ; Type: Operational uncertainty ; Severity: **High** — the documented deploy/rollback/backup path (Neon restore point, digest images) cannot be what protects the observed local-Postgres production.
- Evidence:
  - Neon, "No Postgres container runs in production": `[cur] README.md:97`, `[cur] docker-compose.production.yml:190-198,217…` ("Neon direct connection string"), `[base] docker-compose.production.yml:5-9`, `[cur] docs/PRODUCTION-LAST-MILE.md:35-41,53` (Neon restore point before migrate).
  - Railway merged containers: `[cur] docs/audit/02-architecture.md:12-16,28-30` (railway.json `--guestPrefixes`, merge-launcher); no `apps/*/railway.json` exists in either snapshot; `scripts/merge-launcher.js` still present both. `[cur] docs/ERP-EMPLOYEE-PAYROLL-DESIGN.md:23` (5-service Railway cap).
  - Vercel web: `[cur] README.md:93-95,103`, `[cur] PRODUCTION_HARDENING.md:13-15`.
  - Local container PG18: `[cur] docs/PRODUCTION-UPDATE-2026-09-20-ar.md:69-72` ("القاعدة جوه container اسمه nile-postgres (صورة postgres:18)").
  - Runtime: `evidence/runtime.txt:2,5` image `nile-pharma-erp/accounting:release-89c2c31` (tag, not digest); `:10` env files `/opt/codeandcanvas/apps/nile-pharma-erp/.env,/tmp/nile-recovery-release.env`; `:19` `DATABASE_URL=postgresql://***:***@nile-postgres:5432/nile_accounting`.
  - Postgres version claims: 16 (`PRODUCTION-READINESS-P0.md`, `ERP-PRODUCTION-READINESS.md`), 18 (`HEAVY-VERIFICATION-AR.md:5`, `PRODUCTION-UPDATE-2026-09-20-ar.md:72`).
- To close: see §9 evidence requests; produce one authoritative deployment document.

### REQDOC-15 — Stale documents contradict current code (both snapshots)
- Domain: Documentation ; Affected: BOTH ; Verified ; Type: Improvement ; Severity: **Low**.
- Evidence: `PRODUCTION_HARDENING.md:55-69` says transfers disabled (`TRANSFERS_ENABLED=false`) — code says enabled (`[cur] apps/web/app/dashboard/inventory/page.tsx:65-72`, same in base); `ERP-EMPLOYEE-PAYROLL-DESIGN.md:7-15` "no API, no calculation engine" — `apps/organization/src/modules/payroll/payroll.controller.ts:22-130` (runs calculate/approve/finalize/mark-paid) and SI/tax engine `attendance.service.ts:221-243` exist both; `REPORTS-IMPLEMENTATION-STATUS.md:119-146` "17 placeholder pages" — actual 3 (`purchase-requests`, `stock-counts`, `settings/company`, 6-line `PlaceholderPage` files); `INVOICE-CONCEPT-AR.md` "direct invoice does not move stock" vs `invoices.service.ts:297-299` "Atomically claims direct-invoice stock" (both); `phase1-master-data-data-io.md:99-100` "export-kit not present" vs `[cur] packages/export-kit`; README "How the pieces connect" (l.79-91) shows only IAM.

### REQDOC-16 — Many documented requirements remain undecided (blocking)
- Domain: multiple ; Affected: BOTH ; Verified (text) ; Type: Question ; Severity: **Info** — see §7 list.

### REQDOC-17 — Hard-coded statutory/business parameters without documented business approval
- Domain: Payroll/Sales ; Affected: BOTH ; Verified ; Type: Question ; Severity: **Low**.
- Evidence: SI 11% / 18.75% and income-tax brackets `[cur] apps/organization/src/modules/attendance/attendance.service.ts:221-243`; order approval threshold 100,000 `[cur] apps/sales/src/modules/orders/orders.service.ts:20`; stale-reservation 72h env default `[cur] apps/inventory/src/modules/jobs/inventory-jobs.ts:16`; 12% commercial discount `orders.service.ts:21`. None has an approval record with effective date (only 12% is called "agreed" in a code comment).

---

## 7. Consolidated documented requirements / decisions (Traceability-matrix seed)

Doc status: **Decided** (owner decision recorded) · **Decided+Impl-claim** (decision + agent says done) · **Proposed** · **Open** (question to owner) · **Company-req** (derived from company artefacts, not a signed decision) · **Claim** (RTM/status doc only).
Code check: **IMPL-BOTH** · **IMPL-CUR** (CURRENT only) · **PARTIAL** · **NOT FOUND** (both) · **UNCLEAR** · **n/c** (not checked). ★ = spot-checked in this pass.

| REQ-ID | Requirement | Source | Domain | Doc status | Code check | Evidence |
|---|---|---|---|---|---|---|
| REQ-01 ★ | Sales return requires approval PENDING→APPROVED→POSTED / REJECTED w/ reason; posting only on approval | [cur] docs/DECISIONS-AR.md:208-218 | O2C/Returns | Decided+Impl-claim | IMPL-BOTH | [base] apps/sales/prisma/schema.prisma:173-178 |
| REQ-02 ★ | Return approver ≠ recorder (except SUPER_ADMIN / sales.returns.approve.any) | DECISIONS-AR.md:214 | Approvals/SoD | Decided+Impl-claim | IMPL-BOTH | [cur] apps/sales/src/modules/returns/returns.service.ts:312-321 |
| REQ-03 ★ | Credit note per return, numbered CR-YYYY-NNNN, auto-issued at approval | DECISIONS-AR.md:220-230 | O2C/Tax | Decided+Impl-claim | IMPL-BOTH | [base] apps/accounting/src/modules/credit-notes/credit-notes.service.ts:150 |
| REQ-04 ★ | Negative VAT entry on credit note only when tax adviser approves (flag CREDIT_NOTE_VAT_POSTING, default off) | DECISIONS-AR.md:226-227 | Tax | Decided (pending adviser) | IMPL-BOTH | [base] credit-notes.service.ts:74-77 |
| REQ-05 ★ | Sales-order import creates DRAFT orders only; price override needs sales.orders.import.override and ≤ PricingRule.maxDiscountPct; submit runs credit→approval→FEFO | DECISIONS-AR.md:232-241 | O2C | Decided+Impl-claim | IMPL-BOTH | [cur] orders.service.ts:911,1031,1090; orders.controller.ts:139,173 |
| REQ-06 ★ | Order list shows warehouse(s) derived from FEFO allocations (no warehouseId on order) | DECISIONS-AR.md:202-206 | O2C/Inventory | Decided+Impl-claim | IMPL-BOTH | [base] orders.service.ts:102,227 |
| REQ-07 ★ | POD: customer signature mandatory, photo optional, files outside DB via FileStorageService | DECISIONS-AR.md:242-253 | Shipping | Decided+Impl-claim | IMPL-BOTH | [base] apps/sales/src/modules/shipments/shipments.service.ts:107,128 |
| REQ-08 ★ | In-app notifications first; type catalogue; marketing opt-in; separate send/bulk permissions | DECISIONS-AR.md:254-268 | Notifications | Decided+Impl-claim | IMPL-BOTH | [base] apps/iam/src/modules/notifications/dto/notification.dto.ts:3,26 |
| REQ-09 | External SMS/WhatsApp channel: provider comparison before enabling | DECISIONS-AR.md:268 | Notifications | Open | n/c | — |
| REQ-10 ★ | accounting.matching.approve granted to Finance Manager role (no auto role); PO creator ≠ approver | [cur] docs/DECISIONS-2026-09-25-ar.md:7 | P2P/SoD | Decided | IMPL-BOTH (SoD) | [base] matching.service.ts:205; [cur] :237; controller :95-96 |
| REQ-11 | User with no permissions: login + account security only; no notifications.read | DECISIONS-2026-09-25-ar.md:12 | IAM | Decided+Impl-claim | n/c | commit 8bb0aae (claim) |
| REQ-12 ★ | FX revaluation: M2 reverse-then-repost, BANK rate (CUSTOMS only by separate policy) | DECISIONS-2026-09-25-ar.md:13; P1 pack:198 | GL/FX | Decided+Impl-claim | IMPL-BOTH | [base]/[cur] apps/accounting/src/modules/fx/fx.service.ts:493-503 |
| REQ-13 | Pricing UI = two tabs (rules & offers / discount limits); no data deletion | DECISIONS-2026-09-25-ar.md:19 | Pricing | Decided | n/c | — |
| REQ-14 ★ | Bonus by value: fixed money amount on pricing rule; free SKU from eligible list; commercial value 0; auto-generated line; tax behind disabled flag until accountant approves | DECISIONS-2026-09-25-ar.md:20-21,113-118 | Pricing/Tax | Decided | NOT FOUND | no bonus-line field on order/invoice (grep `isBonus|bonusValue` empty both) |
| REQ-15 | One pricing rule per invoice + manual discount within user's RBAC ceiling; no stacking | DECISIONS-2026-09-25-ar.md:22-23 | Pricing | Decided (conflicts REQ-40) | PARTIAL | see REQ-40 |
| REQ-16 | Count rows in price_rules/promotions/pricing_rules before any migration (ت-6) | DECISIONS-2026-09-25-ar.md:24; REQUESTS:120-123 | Pricing/Data | Open (awaiting counts) | n/a | — |
| REQ-17 ★ | Damaged-goods verdicts (repair/gift/destroy/claim) with approver matrix and accounting classification; status ACCOUNTING_PENDING; no fake journals | DECISIONS-2026-09-25-ar.md:28-45,120-124 | Inventory/GL | Decided | NOT FOUND | grep `ACCOUNTING_PENDING|damagedQty|DamageVerdict` empty both |
| REQ-18 ★ | Supplier/carrier claims cycle Submitted→Accepted/Rejected→Settlement; no automatic supplier-invoice reduction | DECISIONS-2026-09-25-ar.md:46,126-130 | P2P | Decided | NOT FOUND | grep `SupplierClaim|APPROVED_PENDING_SETTLEMENT` empty both |
| REQ-19 | Consignment issued by delivery note (not invoice); sale from consignment is a normal order invoiced; consignment sale = consumption source for box-credit | DECISIONS-2026-09-25-ar.md:50-52 | Inventory/O2C | Decided | n/c | — |
| REQ-20 | Per-SKU box credit limit formula, "near finished" %, keep money limit?, override approver (ا-2..ا-5) | DECISIONS-2026-09-25-ar.md:53; REQUESTS:184-206 | Credit | Open | NOT FOUND | no qty-credit fields (grep) |
| REQ-21 ★ | Customer gifts: same approval cycle as expenses (draft→manager→finance→paid) with separate permissions; closed category list; product sample does not deduct stock | DECISIONS-2026-09-25-ar.md:57-58,108-111 | Expenses/CRM | Decided+Impl-claim | IMPL-BOTH | [base] apps/organization/prisma/schema.prisma:578-629; seed perms [base] apps/iam/prisma/seed.ts:245-246 |
| REQ-22 ★ | Stale reservations (>72h): no auto release; detect, mark, alert only; manual release checks Sales + Accounting | DECISIONS-2026-09-25-ar.md:93-103 | Inventory | Decided | IMPL-BOTH (detect+event) | [base] apps/inventory/src/modules/jobs/inventory-jobs.ts:10-16,118-127 |
| REQ-23 ★ | Consignment: expired/invalid batch must be rejected in backend (single & bulk) before production use | DECISIONS-2026-09-25-ar.md:105-106 | Inventory/QA | Decided (precondition) | IMPL-CUR | [cur] consignment.service.ts:128,159-177; absent [base] :121-140 |
| REQ-24 ★ | EXP-1 reject only before payment; EXP-2 conditional state transitions; EXP-3 fix misleading "journal entry" comment | DECISIONS-2026-09-25-ar.md:134-140 | Expenses | Recorded, deferred | NOT FOUND (defect present) | [cur] expenses.service.ts:153-165,171 |
| REQ-25 ★ | AP is receipt-driven (goods receipt creates supplier liability) | [cur] P1 pack:424 | P2P/AP | Decided (09-28) | IMPL-BOTH (existing behaviour) | saga-listener onGoodsReceived (P1 pack:27) |
| REQ-26 ★ | PO is a record; receipt without PO allowed; PO never blocks receiving | P1 pack:425 | P2P | Decided (09-28) | IMPL-CUR (projection) | [cur] P1-AUDIT.md:376-380; migration 20260928003000_purchase_order_receipt_tracking (cur only) |
| REQ-27 ★ | PO creation SUPER_ADMIN only; backend numbers PO-YYYY-NNNN | P1 pack:426 | P2P | Decided (09-28) | IMPL-CUR | [cur] matching.service.ts:97-123 |
| REQ-28 ★ | PO received qty from GoodsReceived events; partial/full/over/missing are reporting facts; match uses actual receipts | P1 pack:427 | P2P | Decided (09-28) | IMPL-CUR | [cur] matching.service.ts:644 vs [base] :604 |
| REQ-29 ★ | Customer pricing selected at customer creation, effective price stored on profile | P1 pack:428 | Pricing/CRM | Decided (09-28) | IMPL-CUR | [cur] crm migration 20260928133000_customer_pricing_profile |
| REQ-30 ★ | Supplier-payment FX = realized difference at payment | P1 pack:429 | AP/FX | Decided (09-28) | IMPL-CUR | [cur] supplier-payments.service.ts:84 |
| REQ-31 ★ | ETA e-invoicing deferred, important TODO (payload, signing, submission, lifecycle, credit/debit notes, audit) | [cur] docs/TODO-IMPORTANT.md:3-17; P1 pack:430 | Tax/ETA | Decided (deferred) | NOT FOUND (consistent) | no EInvoice/ETA code both |
| REQ-32 | BD-1 options GRNI/invoice-driven | P1 pack:17-112 | AP | Superseded by REQ-25 | — | — |
| REQ-33 | BD-2 procurement placement (new service vs modules) | P1 pack:300-315 | P2P | Open (no recorded decision) | IMPL-CUR as accounting module | [cur] apps/accounting/src/modules/import-shipments |
| REQ-34 | BD-3 discount authority identity; where 100,000 approval threshold lives | P1 pack:116-192 | Approvals | Open (partly via REQ-29/40) | PARTIAL | threshold hard-coded [cur] orders.service.ts:20 |
| REQ-35 | BD-4 authoritative segment vocabulary | P1 pack:319-333 | Pricing | Open ("to be reviewed", P1 pack:428) | n/c | — |
| REQ-36 | BD-6 ETA signer/provider; doc scope; onboarding owner | P1 pack:337-348 | Tax/ETA | Open | NOT FOUND | — |
| REQ-37 | BD-7 supplier payment = AP-only / dual treasury / treasury-native; methods | P1 pack:352-367 | AP/Treasury | Open (no record) | IMPL-CUR (dual posting claimed) | [cur] ACCOUNTING-AUDIT-2026-09-28:58-60 |
| REQ-38 | BD-8 PO printing (HTML / PDF / defer) | P1 pack:371-383 | P2P | Open (numbering decided) | n/c | — |
| REQ-39 ★ | Default 12% commercial discount on orders | REQUESTS-2026-09-25-ar.md:73; ACCOUNTING-AUDIT-09-28:71 | Pricing | Company-req / stated "agreed" | IMPL-BOTH | [base] orders.service.ts:21 |
| REQ-40 ★ | Order-time discount ceiling: ≥100% rejected; >12% needs approval permission | [cur] ACCOUNTING-AUDIT-2026-09-28:72 | Pricing/Approvals | Impl-claim (no explicit decision) | IMPL-CUR | [cur] orders.service.ts:557,569 |
| REQ-41 ★ | Order approval when grand total ≥ 100,000 | P1 pack:127 | O2C/Approvals | Claim (current behaviour) | IMPL-BOTH | orders.service.ts:20 |
| REQ-42 | Rep warehouse & rep cash box (type/owner, auto vs button, sell from main?, cash limit & remittance) | REQUESTS-2026-09-25-ar.md:133-156 | Field sales/Treasury | Open (م-1..م-4) | NOT FOUND | Warehouse model has no owner/type fields (grep, both) |
| REQ-43 | Role screen simplification "section visible" vs granular (ص-3) | REQUESTS:247-261 | IAM | Open | n/c | — |
| REQ-44 | Charts on every report page | REQUESTS:230-243, l.286 | Reports | Impl-claim | n/c | — |
| REQ-45 | Stock-movement filters by user & warehouse; password strength messages; new user lands on empty system (5,10,11-أ) | REQUESTS:12-57 | Inventory/IAM | Impl-claim | n/c | — |
| REQ-46 | Damaged-qty field on receipt line | REQUESTS:160-180 | Inventory | Decided via ت-7..9 | NOT FOUND | — |
| REQ-47 ★ | Shipping tariff: flat per order, zones 1-10 one-way/round-trip, versioned rates, snapshot on order/invoice | [cur] docs/SHIPPING-TARIFF-AND-TAX-DECISION-AR.md:3-41 | Shipping | Decided ("معتمدة" l.21) | IMPL-BOTH | [base] apps/sales/prisma/migrations/20260923110000_add_shipping_tariffs/migration.sql:87 |
| REQ-48 | Cairo & Alexandria free (Zone 1) except New Administrative Capital (Zone 3); Giza/Qalyubia need explicit SUPPORTED/NOT_SUPPORTED; override needs reason | SHIPPING:23-28 | Shipping | Decided | n/c | — |
| REQ-49 ★ | Shipping fee outside VAT base until official ruling | SHIPPING:43-53 | Tax | Decided (interim) | IMPL-BOTH | [cur] invoices.service.ts:1014 (total = net+tax+shippingFee) |
| REQ-50 | ROUND_TRIP leg returns cash + signed invoice as normal collection; no SalesReturn | SHIPPING:55-57 | Shipping/Collections | Decided | n/c | — |
| REQ-51 | Customer onboarding: basic data only; backend-generated code; no opening balance in form | [cur] docs/roadmap/2026-09-19-customer-field-execution-ar.md:5-7 | CRM | Decided (user) | IMPL-BOTH ★ | [cur] apps/crm/prisma/migrations/20260919120000_customer_onboarding/migration.sql:5,15 |
| REQ-52 | Separate visited doctor/centre from buying pharmacy (debtor) | roadmap:8 | CRM/Field | Decided (user) | n/c | — |
| REQ-53 ★ | Collections allocated to specific invoices (no fake invoice / unallocated balance) | roadmap:9 | Collections | Decided (user) | IMPL-BOTH (model) | [base] apps/accounting/prisma/schema.prisma:1082 PaymentAllocation |
| REQ-54 ★ | GPS failure allowed with reason + review; accuracy/source/time stored | roadmap:10 | Field sales | Decided (user) | IMPL-BOTH | [base] apps/crm/src/modules/field-sales/dto/field-sales.dto.ts:113,132 |
| REQ-55 ★ | Rep may propose an order to a pharmacy from a doctor visit; sale only after pharmacy confirmation + supervisor review | roadmap:11 | Field sales | Decided (user) | PARTIAL (model exists) | [cur] apps/crm/prisma/schema.prisma:663 FieldProposal |
| REQ-56 | Postponement keeps origin & reason; not auto-added to today's plan | roadmap:12 | Field sales | Decided (user) | n/c | — |
| REQ-57 | Same services/APIs for web and mobile | roadmap:13 | Architecture | Decided (user) | n/c | — |
| REQ-58 ★ | Collection/expense must name the treasury/bank/wallet & custodian; internal transfer two-legged (F01) | [cur] docs/audit/2026-09-18-company-workflows-vs-erp-ar.md:65-73 | Treasury | Company-req | PARTIAL | optional Payment.financialAccountId both ([base] schema Payment) |
| REQ-59 ★ | Bounced cheque reverses customer debt and commission (F02) | company-workflows:75-86 | Collections/Incentives | Company-req | IMPL-BOTH (claim in code) | [base] payments.service.ts:405-428; incentives PaymentReversed consumer intake.service.ts:63-64,165 |
| REQ-60 | One receipt for many invoices / advance payment (F03) | company-workflows:88-94 | Collections | Company-req | PARTIAL | PaymentAllocation model both |
| REQ-61 | Incentive policy equal to company sheet (750k threshold, cumulative tiers, basis/period) (F04) | company-workflows:96-118 | Incentives | Company-req, policy **undecided** | UNCLEAR | engine marginal tiers (doc l.100-103) |
| REQ-62 ★ | Paying an expense must hit a treasury voucher; no fake success (F05) | company-workflows:120-126 | Expenses/Treasury | Company-req | PARTIAL | mock removed ([cur] expenses.service.ts:32); markPaid has no treasury effect |
| REQ-63 ★ | Consignment moves stock atomically warehouse↔consignment (F06) | company-workflows:128-136 | Inventory | Company-req | IMPL-BOTH | [base] consignment.service.ts:126 applySignedDelta(-qty) |
| REQ-64 | Rep custody as a location/entity with owner & acknowledgement; allocation by source (F07) | company-workflows:138-144 | Inventory/Field | Company-req, Open | NOT FOUND | no warehouse owner fields |
| REQ-65 ★ | 3-way match checks actual received qty (F08) | company-workflows:146-156 | P2P | Company-req | IMPL-CUR | see REQ-28 |
| REQ-66 | PO/vendor invoice carry currency, document date, Incoterms/payment terms (F09) | company-workflows:158-166 | P2P/FX | Company-req | UNCLEAR (cur adds vendor_invoice_fx) | [cur] migration 20260928143000_vendor_invoice_fx |
| REQ-67 ★ | Return on fully-paid invoice creates customer credit / refund obligation (F10) | company-workflows:168-182 | O2C/Returns | Company-req | NOT FOUND (defect) | [base] invoices.service.ts:909-916 |
| REQ-68 ★ | Return policy: ≥90 days before expiry, intact pack (F10) | company-workflows:182 | Returns/QA | Company-req, needs decision | NOT FOUND | grep empty both |
| REQ-69 | Bonus/offers applied automatically with PAID/BONUS/SAMPLE line types (F11) | company-workflows:184-190 | Pricing | Company-req | NOT FOUND | promotions engine not called by orders.create (doc l.186) |
| REQ-70 | Price basis (incl./excl. VAT) and rounding defined (F12) | company-workflows:192-198 | Pricing/Tax | Company-req, Open | n/c | pricing.service adds tax after discount (doc) |
| REQ-71 | Approved opening-balance path with cut-off date (F13) | company-workflows:200-206 | AR/GL | Company-req, Open | PARTIAL | AccountCreated listener exists; CRM sends opening_balance undefined (doc l.204) |
| REQ-72 ★ | Fiscal-period hard lock (no posting into closed period) | RTM REQ-FIN-003 (l.32) | GL | Claim | PARTIAL (IMPL-CUR for GL journals only) | [cur] general-ledger.service.ts:12; none in [base] |
| REQ-73 ★ | VAT 14% return & Form 41 generation | RTM REQ-TAX-001..004 (l.50-53) | Tax | Claim | PARTIAL (manual TaxEntry only) | [cur] tax.service.ts:70,139-140 |
| REQ-74 ★ | WHT 1/3/5% on suppliers | RTM REQ-TAX-003 | Tax | Claim | PARTIAL (rate mapping on manual entries) | [cur] tax.service.ts:62-64 |
| REQ-75 ★ | Fixed assets straight-line & reducing-balance depreciation | RTM REQ-FIN-013 | Fixed assets | Claim | IMPL-BOTH | [cur] apps/accounting/prisma/schema.prisma:829-844 |
| REQ-76 ★ | Year-end close with retained earnings transfer | RTM REQ-FIN-004 | GL | Claim | IMPL-BOTH (code present) | [cur] fiscal-periods.service.ts:162; dto close-period.dto.ts:15-21 |
| REQ-77 ★ | Trial balance | RTM REQ-FIN-002 | GL | Claim | IMPL-BOTH (BASE from coa; CUR from GL journals) | [base] coa.service.ts:208; [cur] general-ledger.service.ts:114 |
| REQ-78 ★ | Egyptian social insurance 11%/18.75% & income-tax brackets | RTM REQ-HR-007/008 | Payroll | Claim (no business approval) | IMPL-BOTH | [cur] attendance.service.ts:221-243 |
| REQ-79 ★ | Payroll runs calculate/approve/finalize/adjust | ERP-EMPLOYEE-PAYROLL-DESIGN (says not built) | Payroll | Stale doc | IMPL-BOTH | [cur] payroll.controller.ts:85-130 |
| REQ-80 ★ | Toxic SoD rules enforced | RTM REQ-SEC-009; GO-LIVE dim 2 | Security | Claim | PARTIAL (detective only) | [cur] apps/iam/src/modules/sod/sod.controller.ts:15-27 |
| REQ-81 ★ | Support tickets with priority SLA (2h cold chain) | RTM REQ-SAL-009 | CRM | Claim | IMPL-BOTH (SLA map) | [cur] apps/crm/src/modules/support/support.service.ts:31,187-188 |
| REQ-82 ★ | Unit-level serialization / genealogy ("DSCSA") | RTM REQ-INV-010 | Traceability | Claim (no business source) | IMPL-BOTH (basic) | [cur] apps/products/src/modules/serialization/serialization.controller.ts:11-15 |
| REQ-83 ★ | Warehouse GLN | RTM REQ-INV-009 | Inventory | Claim | IMPL-BOTH (field) | [cur] apps/inventory/prisma/schema.prisma:52 |
| REQ-84 | No frontend middleware; PWA SW caches nothing; password 8+letter+digit; 401 carries code; BFF 8s timeout | [cur] docs/QA-DECISIONS-AR.md:5-51 | Security/UX | Decided (technical) | n/c | — |
| REQ-85 ★ | Placeholder pages hidden from navigation (purchase-requests, stock-counts, settings/company) | QA-DECISIONS-AR.md:22-24 | UX | Decided | IMPL-BOTH (3 placeholders) | [cur] apps/web/app/dashboard/purchase-requests/page.tsx:5 |
| REQ-86 | Unified invoice concept: invoice is the only sales document in UI; type is a print lens | [cur] docs/INVOICE-CONCEPT-AR.md:3-16 | O2C/UX | Decided (concept) | n/c | — |
| REQ-87 | Accounting invariants: one balanced journal per AR/AP settlement; replay idempotent; reversal = compensating journal; uncleared cheque → 1122 | [cur] docs/P0-ACCOUNTING-MEGA-WAVE.md:30-37 | GL | Impl-claim (CURRENT) | UNCLEAR (CUR only; not tested here) | — |

Coverage note: ≥ 50 rows are ★ spot-checked. Rows marked n/c were not checked against code in this pass.

---

## 8. Reports — documented vs implemented

| Report | Doc | BFF / page | Backend endpoints referenced | Status |
|---|---|---|---|---|
| Sales reports | REPORTS-IMPLEMENTATION-STATUS.md:30-42 | `apps/web/app/api/sales-reports`, `dashboard/reports/sales` | orders `summary`, `trend`, `top-reps`, `top-products`, `status-breakdown`, `top-customers` | All endpoints exist in `apps/sales/src/modules/orders/orders.controller.ts` (BOTH) — doc's "assumed" label is stale |
| Inventory reports | :44-53 | `api/inventory-reports` | stock `summary`, `movement-trend`, batches `near-expiry` | Exist (BOTH) |
| Customer reports | :55-66 | `api/customer-reports` | crm accounts `summary`, visits, sales `top-customers` | Exist (BOTH) |
| Analytics | :68-80 | `api/dashboard` | dashboard BFF; page ungated by permission (QA-DECISIONS F-03 intentional) | Exist (BOTH) |
| Financial | template | `dashboard/reports/financial` | collection aging, credit-exposure BFF | Exist |
| Placeholder register (17 pages) | :119-146 | — | — | Stale: only 3 PlaceholderPage files remain (BOTH) |
| VAT summary / Form 41 | RTM, GO-LIVE | accounting `tax/vat-summary`, `tax/form-41` | data from manual TaxEntry | PARTIAL (REQDOC-08) |
| Trial balance / P&L / BS | RTM REQ-FIN-002 | `[cur] general-ledger.controller.ts:20` | GL journals | CURRENT GL; BASELINE coa-based TB |
| GRNI / received-not-invoiced aging | BD-1 1-C | — | — | Not built (decision chose receipt-driven AP) |
| Rep custody report (goods+cash) | REQUESTS (4) | — | — | Not built (open) |
| Customer spend vs sales (gifts) | REQUESTS (8) | — | — | n/c |

---

## 9. Documented architecture & deployment catalogue and contradictions

Documented architecture (consistent parts): 9 NestJS services + Next.js web, DB-per-service, Redpanda events, ports web 3000, iam 3001 … audit 3009 (`[cur] README.md:130-144`); web routes `/api/<svc>/*` via rewrites to each service (`[cur] apps/web/next.config.js:51-67`) plus 13 server-side BFF aggregators in `apps/web/app/api/*` (credit-exposure, dashboard, *-reports, search, system-health, tasks …). So the routing is **both** per-service proxy and BFF — not a contradiction, but README l.79-91/145 describes only IAM/ORG proxying.

Contradictions:

| # | Topic | Statement A | Statement B | Runtime evidence |
|---|---|---|---|---|
| C1 | DB host | Neon, "No Postgres container runs in production" ([cur] README.md:97; [cur]/[base] docker-compose.production.yml:5-9,190-198; PRODUCTION-LAST-MILE.md:35-41) | Local container `nile-postgres` postgres:18 ([cur] docs/PRODUCTION-UPDATE-2026-09-20-ar.md:69-72; REQUESTS:122) | `nile-postgres:5432` (runtime.txt:19) |
| C2 | Hosting | Railway merged containers (docs/audit/02-architecture.md:12-30; ERP-EMPLOYEE-PAYROLL-DESIGN.md:23) | Hostinger VPS compose, 9 separate containers (README.md:94-96) | compose project at /opt/codeandcanvas/apps/nile-pharma-erp (runtime.txt:10) |
| C3 | Web hosting | Vercel (`nile-pharma-food-erp.vercel.app`, PRODUCTION_HARDENING.md:13-15) | Self-hosted `nile-erp.codeandcanvas.net` (PRODUCTION_HARDENING.md:22-23) | not in evidence |
| C4 | Image identity | Digest-pinned immutable images, deploy-production.sh, Neon restore point (PRODUCTION-LAST-MILE.md:3,44-62) — CURRENT | `image: nile-pharma-erp/<svc>:${IMAGE_TAG:-prod}` ([base] docker-compose.production.yml:180,217) | tag `release-89c2c31`, env `/tmp/nile-recovery-release.env` (runtime.txt:2,10) — matches neither cleanly |
| C5 | Postgres version | 16 (PRODUCTION-READINESS-P0.md, ERP-PRODUCTION-READINESS.md, dev compose README.md:101) | 18 (HEAVY-VERIFICATION-AR.md:5; PRODUCTION-UPDATE-2026-09-20-ar.md:72) | n/a |
| C6 | Journal engine | "Accounting has chart of accounts only, no Journal Entry engine" (DECISIONS-2026-09-25-ar.md:122) | "Posted double-entry GL remains authoritative" (ACCOUNTING-AUDIT-2026-09-28:49) | True for BASELINE vs CURRENT respectively |
| C7 | Placeholder pages | 17 (REPORTS-IMPLEMENTATION-STATUS.md:146) | 3 (HEAVY-VERIFICATION-AR.md:13; QA-DECISIONS N-03) | code: 3 |
| C8 | Event count | 64/64 (RTM REQ-SEC-006; GO-LIVE dim 6) | 63 with 13 untested (AUDIT-COMPLETENESS-MATRIX.md:146) | n/c |
| C9 | Transfers | disabled (PRODUCTION_HARDENING.md:55-69) | enabled (apps/web/app/dashboard/inventory/page.tsx:65-72) | n/c |
| C10 | Backlog count | "35 items" (backlog-traceability:3) | rows numbered to 50; summary counts 49 | — |

---

## 10. Reliability of existing audit / QA documents

| Document | Cites evidence? | Consistent with code? | Reliability |
|---|---|---|---|
| GO-LIVE-ACCEPTANCE-REPORT | Script output only | Checks are file-existence (REQDOC-03); text honestly disclaims sign-off | Low as evidence; honest framing |
| REQUIREMENTS-TRACEABILITY-MATRIX | File paths only, no test results | Paths exist; several claims overstate (REQDOC-02, 08, 09, 11) | Low |
| HEAVY-VERIFICATION-AR (2026-09-15, branch) | Describes method & counts; no raw logs in repo | Placeholder count (3) and BFF/route claims consistent with code; migration counts outdated | Medium (point-in-time, unreproduced here) |
| QA-REPORTS (2026-09-21, branch) | Claims live runs; self-corrections recorded in QA-DECISIONS l.57-59 | Some claims retracted | Medium-Low |
| AUDIT-COMPLETENESS-MATRIX | Producer file + spec per event; honest gap marks (❌/🔶) | n/c in depth | Medium-High (self-critical) |
| DISASTER-RECOVERY-DRILL-REPORT | Prior version fabricated, corrected | — | Current version: Medium; history: Low |
| P1-BUSINESS-DECISION-PACK | Path:line quotes, [VERIFIED] tags | Spot checks matched (matching.service receivedQtyTotal, threshold, BD-5) | High for "current behaviour" at c87961d |
| DECISIONS-AR / DECISIONS-2026-09-25 status columns | Commit ids + spec names | Spot checks matched for 1-6, ر, gifts, EXP | Medium-High |
| audit/2026-09-18-company-workflows-vs-erp | Path:line + reasoning; states what was not tested | Several F-items since fixed (F02, F06), others still valid (F10) | High (as of date) |
| ACCOUNTING-AUDIT-2026-09-28 / P0-ACCOUNTING-MEGA-WAVE | Lists features; explicitly no green CI claimed | Modules exist in CURRENT only | Medium; describes undeployed code |
| ERP-EMPLOYEE-PAYROLL-DESIGN, PRODUCTION_HARDENING, REPORTS-IMPLEMENTATION-STATUS §6, INVOICE-CONCEPT boundaries | — | Stale (REQDOC-15) | Low (outdated) |

---

## 11. Open questions for the business owner

1. Who is the accountable approver for requirements/decisions, and will you sign a consolidated decision register (REQDOC-01)?
2. Pricing model: is the governing rule (a) one pricing rule chosen per invoice + manual discount within RBAC limit (ت-1/ت-4, 2026-09-25) or (b) pricing chosen at customer creation and stored on the profile with 12% base and >12% needing approval (2026-09-28 #5 + CURRENT code)? Can both coexist?
3. Approval threshold 100,000 EGP for orders: confirm value, and where it should be configurable (BD-3 sub-decision).
4. Discount authority (BD-3): which roles may grant which % — is the discount-approval matrix binding?
5. FX: does unrealized revaluation (M2, decided 09-25) continue alongside realized FX at supplier payment (09-28 #6)?
6. BD-2/BD-7: ratify import-shipments inside Accounting and supplier payments as dual AP+treasury posting (implemented in CURRENT without a recorded decision)?
7. Bonus (ت-2/ت-3): accountant's VAT treatment for free goods; when to build (not implemented).
8. Damaged goods sorting and supplier/carrier claims (ت-7..ت-9): still required? (not implemented in either snapshot).
9. Box-based credit limits: formula, coverage months, "near finished" %, keep money limit, override approver (ا-2..ا-5).
10. Rep warehouse / cash box (م-1..م-4) and rep custody (F07): which role is "rep", auto vs manual creation, sell from main warehouse, cash limit, remittance frequency, receiver.
11. Role screen simplification (ص-3): option (a) or (b)?
12. Returns on fully-paid invoices (F10): customer credit balance vs cash refund; and the 90-days-before-expiry / intact-pack return policy — enforce in system?
13. Incentive policy (F04): basis (collection vs sales), period attribution, 750k threshold, cumulative vs marginal tiers, treatment above 6.125M.
14. Fiscal-period lock: may invoices/payments/collections be recorded into a closed period?
15. VAT returns: are VAT/Form 41 figures prepared from the ERP (requires manual TaxEntry) or outside it? Should invoices generate tax entries automatically?
16. Expense claims EXP-1/EXP-2: authorize the fix?
17. Stale reservations: provide counts (ALLOCATED/INVOICED/PAID > 72h) to design the exception workflow.
18. ت-6: provide counts of `price_rules`, `promotions`, `pricing_rules`, `promotion_redemptions`.
19. The 403 user case: which user/screen?
20. Statutory payroll parameters (SI 11%/18.75%, tax brackets): confirm source and effective date; is payroll actually used?
21. Opening balances (F13): cut-off date and approved migration path from Excel.
22. Is "DSCSA" serialization a real requirement (US regulation) or should it be relabelled to Egyptian EDA track-and-trace?
23. ETA (BD-6): signer model and who owns onboarding paperwork; target date.

### Evidence requests (read-only, metadata only)

- Deployed commit/migration state per DB: `docker exec nile-postgres psql "$<SVC>_DATABASE_URL" -Atc "select migration_name, finished_at from _prisma_migrations order by started_at desc limit 5"` for all 9 DBs (proves whether any CURRENT-only migration, e.g. `20260927120000_general_ledger`, `20260928133000_customer_pricing_profile`, is applied).
- Image provenance: `docker image inspect nile-pharma-erp/<svc>:release-89c2c31 --format '{{json .Config.Labels}}'` (look for revision label) for each service.
- Which env/compose actually started the stack: `docker inspect <container> --format '{{index .Config.Labels "com.docker.compose.project.config_files"}} {{index .Config.Labels "com.docker.compose.project.environment_file"}}'`; `ls -l /tmp/nile-recovery-release.env` (do not print contents).
- Whether Neon is used at all: `grep -c neon.tech /opt/codeandcanvas/apps/nile-pharma-erp/.env` (count only).
- Backups for local Postgres: `ls -l` of any backup directory / cron entries (`crontab -l | grep -i pg_dump`).
- VAT reliance: `select count(*), min(created_at), max(created_at) from tax_entries;` and `select count(*) from invoices;` (accounting DB).
- Consignment expiry exposure: `select count(*) from consignment_stock where expiry_date < now() and available_qty > 0;` (inventory DB).
- Fully-paid returns blocked: accounting DLQ/inbox rows for `SalesReturnCreated` failures (`select count(*) from <dlq table> where event_type='SalesReturnCreated'`).
- Stale reservations counts (owner request ر).
- Pricing table counts (ت-6 query as in `docs/REQUESTS-2026-09-25-ar.md:122`).
