# Data Dictionary — Nile Pharma ERP (CURRENT fa40270, مع تمييز ما يختلف عن BASELINE 89c2c31)

مُولّد آليًا من `apps/*/prisma/schema.prisma` (قراءة فقط). العمود **B?** = هل الحقل موجود في BASELINE 89c2c31 (✓ موجود، ✗ غير موجود/مضاف لاحقًا).
PK=@id, U=@unique, FK=علاقة Prisma فعلية (@relation fields)، LREF=مرجع منطقي (حقل *Id بلا @relation) — لا يوجد FK في القاعدة له إلا إذا أنشأته migration يدويًا.

## خدمة `accounting` — DB `nile_accounting`
المصدر: `apps/accounting/prisma/schema.prisma`

### Invoice → `invoices`
`apps/accounting/prisma/schema.prisma:102`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| invoiceNumber | invoice_number | String | N |  | U | ✓ |
| documentType | document_type | InvoiceDocumentType | N | NORMAL_INVOICE |  | ✓ |
| orderId | order_id | String? | Y |  | U LREF | ✓ |
| idempotencyKey | idempotency_key | String? | Y |  | U | ✓ |
| accountId | account_id | String | N |  | LREF | ✓ |
| accountName | account_name | String | N |  |  | ✓ |
| repId | rep_id | String? | Y |  | LREF | ✓ |
| netAmount | net_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| taxAmount | tax_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| total | total | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| shippingFee | shipping_fee | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| shippingRateId | shipping_rate_id | String? | Y |  | LREF | ✓ |
| shippingZoneCode | shipping_zone_code | String? | Y |  |  | ✓ |
| shippingZoneName | shipping_zone_name | String? | Y |  |  | ✓ |
| shippingDirection | shipping_direction | String? | Y |  |  | ✓ |
| shippingGovernorate | shipping_governorate | String? | Y |  |  | ✓ |
| shippingCity | shipping_city | String? | Y |  |  | ✓ |
| shippingArea | shipping_area | String? | Y |  |  | ✓ |
| shippingFreeAreaDecision | shipping_free_area_decision | String? | Y |  |  | ✓ |
| shippingResolution | shipping_resolution | String? | Y |  |  | ✓ |
| shippingManualOverrideReason | shipping_manual_override_reason | String? | Y |  |  | ✓ |
| shippingQuoteSource | shipping_quote_source | String? | Y |  |  | ✓ |
| shippingQuotedAt | shipping_quoted_at | DateTime? | Y |  |  | ✓ |
| paidAmount | paid_amount | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| creditedAmount | credited_amount | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| currency | currency | CurrencyCode | N | EGP |  | ✓ |
| exchangeRate | exchange_rate | Decimal @db.Decimal(16, 6) | N | 1 |  | ✓ |
| baseTotal | base_total | Decimal? @db.Decimal(14, 2) | Y |  |  | ✓ |
| paymentTerms | payment_terms | String? | Y |  |  | ✓ |
| isDeferred | is_deferred | Boolean | N | false |  | ✓ |
| creditPeriodDays | credit_period_days | Int? | Y |  |  | ✓ |
| status | status | InvoiceStatus | N | UNPAID |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| issuedAt | issued_at | DateTime | N | now() |  | ✓ |
| dueDate | due_date | DateTime? | Y |  |  | ✓ |
| cancelledAt | cancelled_at | DateTime? | Y |  |  | ✓ |
| cancelledBy | cancelled_by | String? | Y |  |  | ✓ |
| cancellationReason | cancellation_reason | String? | Y |  |  | ✓ |
| reissuedFromId | reissued_from_id | String? | Y |  | U FK-col | ✓ |
| reissuedFrom | reissuedFrom | Invoice? | Y |  | FK→Invoice(id) onDelete=Restrict | ✓ |
| replacement | replacement | Invoice? | Y |  | FK→Invoice() onDelete=default | ✓ |
| instruments | instruments | FinancialInstrument[] | N |  | FK→FinancialInstrument() onDelete=default | ✗ |

Indexes/constraints: `@@index([accountId])`; `@@index([repId])`; `@@index([status])`

### InvoiceLine → `invoice_lines`
`apps/accounting/prisma/schema.prisma:218`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| invoiceId | invoice_id | String | N |  | FK-col | ✓ |
| productId | product_id | String? | Y |  | LREF | ✓ |
| description | description | String | N |  |  | ✓ |
| quantity | quantity | Decimal @db.Decimal(14, 3) | N |  |  | ✓ |
| unitPrice | unit_price | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| discount | discount | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| discountType | discount_type | InvoiceDiscountType | N | AMOUNT |  | ✓ |
| discountAmount | discount_amount | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| taxRate | tax_rate | Decimal @db.Decimal(5, 2) | N | 0 |  | ✓ |
| taxAmount | tax_amount | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| lineTotal | line_total | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| batchId | batch_id | String? | Y |  | LREF | ✓ |
| batchNumber | batch_number | String? | Y |  |  | ✓ |
| expiryDate | expiry_date | DateTime? | Y |  |  | ✓ |
| sortOrder | sort_order | Int | N | 0 |  | ✓ |
| invoice | invoice | Invoice | N |  | FK→Invoice(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([invoiceId])`; `@@index([productId])`; `@@index([batchId])`

### InvoiceLineBatch → `invoice_line_batches`
`apps/accounting/prisma/schema.prisma:263`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| invoiceLineId | invoice_line_id | String | N |  | FK-col | ✓ |
| batchId | batch_id | String | N |  | LREF | ✓ |
| quantity | quantity | Decimal @db.Decimal(14, 3) | N |  |  | ✓ |
| batchNumber | batch_number | String? | Y |  |  | ✓ |
| expiryDate | expiry_date | DateTime? | Y |  |  | ✓ |
| invoiceLine | invoiceLine | InvoiceLine | N |  | FK→InvoiceLine(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([invoiceLineId])`; `@@index([batchId])`

### GeneralPurchase → `general_purchases`
`apps/accounting/prisma/schema.prisma:283`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| purchaseNumber | purchase_number | String | N |  | U | ✓ |
| purchaseDate | purchase_date | DateTime | N |  |  | ✓ |
| category | category | String | N |  |  | ✓ |
| description | description | String | N |  |  | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| currency | currency | CurrencyCode | N | EGP |  | ✓ |
| paymentMethod | payment_method | PaymentMethod? | Y |  |  | ✓ |
| receiptNumber | receipt_number | String? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| status | status | GeneralPurchaseStatus | N | DRAFT |  | ✓ |
| createdById | created_by_id | String | N |  | LREF | ✓ |
| updatedById | updated_by_id | String | N |  | LREF | ✓ |
| version | version | Int | N | 1 |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@index([createdById, createdAt])`; `@@index([purchaseDate])`; `@@index([status])`

### GeneralPurchaseRevision → `general_purchase_revisions`
`apps/accounting/prisma/schema.prisma:311`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| purchaseId | purchase_id | String | N |  | FK-col | ✓ |
| version | version | Int | N |  |  | ✓ |
| action | action | GeneralPurchaseRevisionAction | N |  |  | ✓ |
| actorId | actor_id | String | N |  | LREF | ✓ |
| before | before | Json? | Y |  |  | ✓ |
| after | after | Json? | Y |  |  | ✓ |
| reason | reason | String? | Y |  |  | ✓ |
| changedAt | changed_at | DateTime | N | now() |  | ✓ |
| purchase | purchase | GeneralPurchase | N |  | FK→GeneralPurchase(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@unique([purchaseId, version])`; `@@index([purchaseId, changedAt])`; `@@index([actorId, changedAt])`

### FinancialInstrument → `financial_instruments` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:330`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | — |
| type | type | InstrumentType | N |  |  | — |
| status | status | InstrumentStatus | N | RECEIVED |  | — |
| paymentId | payment_id | String? | Y |  | U FK-col | — |
| accountId | account_id | String | N |  | LREF | — |
| invoiceId | invoice_id | String? | Y |  | FK-col | — |
| instrumentNumber | instrument_number | String | N |  |  | — |
| bankName | bank_name | String? | Y |  |  | — |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | — |
| currency | currency | CurrencyCode | N | EGP |  | — |
| dueDate | due_date | DateTime | N |  |  | — |
| depositedAt | deposited_at | DateTime? | Y |  |  | — |
| clearedAt | cleared_at | DateTime? | Y |  |  | — |
| bouncedAt | bounced_at | DateTime? | Y |  |  | — |
| bounceReason | bounce_reason | String? | Y |  |  | — |
| replacesId | replaces_id | String? | Y |  | FK-col | — |
| replacedById | replaced_by_id | String? | Y |  | U FK-col | — |
| actorId | actor_id | String | N |  | LREF | — |
| createdAt | created_at | DateTime | N | now() |  | — |
| updatedAt | updated_at | DateTime | N |  |  | — |
| payment | payment | Payment? | Y |  | FK→Payment(id) onDelete=default | — |
| invoice | invoice | Invoice? | Y |  | FK→Invoice(id) onDelete=default | — |
| replacementOf | replacementOf | FinancialInstrument? | Y |  | FK→FinancialInstrument(id) onDelete=default | — |
| replacementOfInverse | replacementOfInverse | FinancialInstrument? | Y |  | FK→FinancialInstrument() onDelete=default | — |
| replacement | replacement | FinancialInstrument? | Y |  | FK→FinancialInstrument(id) onDelete=default | — |
| replacementInverse | replacementInverse | FinancialInstrument? | Y |  | FK→FinancialInstrument() onDelete=default | — |

Indexes/constraints: `@@index([accountId, status])`; `@@index([dueDate, status])`; `@@index([invoiceId])`; `@@unique([replacesId])`

### Payment → `payments`
`apps/accounting/prisma/schema.prisma:376`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| idempotencyKey | idempotency_key | String | N |  | U | ✓ |
| invoiceId | invoice_id | String? | Y |  | FK-col | ✓ |
| accountId | account_id | String? | Y |  | LREF | ✓ |
| orderId | order_id | String? | Y |  | LREF | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| currency | currency | CurrencyCode | N | EGP |  | ✓ |
| exchangeRate | exchange_rate | Decimal @db.Decimal(16, 6) | N | 1 |  | ✓ |
| baseAmount | base_amount | Decimal? @db.Decimal(14, 2) | Y |  |  | ✓ |
| method | method | PaymentMethod | N |  |  | ✓ |
| financialAccountId | financial_account_id | String? | Y |  | FK-col | ✓ |
| checkNumber | check_number | String? | Y |  |  | ✓ |
| checkBank | check_bank | String? | Y |  |  | ✓ |
| checkStatus | check_status | CheckStatus? | Y |  |  | ✓ |
| checkDueDate | check_due_date | DateTime? | Y |  |  | ✓ |
| receivedAt | received_at | DateTime | N | now() |  | ✓ |
| actorId | actor_id | String | N |  | LREF | ✓ |
| sourceType | source_type | String? | Y |  |  | ✓ |
| sourceId | source_id | String? | Y |  | LREF | ✓ |
| reversed | reversed | Boolean | N | false |  | ✓ |
| reversedAt | reversed_at | DateTime? | Y |  |  | ✓ |
| reversalReason | reversal_reason | String? | Y |  |  | ✓ |
| reversedBy | reversed_by | String? | Y |  |  | ✓ |
| invoice | invoice | Invoice? | Y |  | FK→Invoice(id) onDelete=default | ✓ |
| financialAccount | financialAccount | FinancialAccount? | Y |  | FK→FinancialAccount(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([invoiceId])`; `@@index([accountId])`; `@@index([method])`; `@@index([financialAccountId])`; `@@index([receivedAt])`; `@@unique([sourceType, sourceId])`

### LedgerEntry → `ledger_entries`
`apps/accounting/prisma/schema.prisma:452`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| accountId | account_id | String | N |  | LREF | ✓ |
| side | side | LedgerSide | N |  |  | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| refType | ref_type | String | N |  |  | ✓ |
| refId | ref_id | String | N |  | LREF | ✓ |
| description | description | String? | Y |  |  | ✓ |
| occurredAt | occurred_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([accountId])`; `@@index([occurredAt])`; `@@unique([refType, refId])`

### CollectionMetric → `collection_metrics`
`apps/accounting/prisma/schema.prisma:474`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| repId | rep_id | String | N |  | LREF | ✓ |
| period | period | String | N |  |  | ✓ |
| totalSales | total_sales | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| collected | collected | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| uncollected | uncollected | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| collectionRate | collection_rate | Decimal @db.Decimal(5, 4) | N | 0 |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@unique([repId, period])`

### Currency → `Currency`
`apps/accounting/prisma/schema.prisma:489`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| code | code | CurrencyCode | N |  | PK | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| symbol | symbol | String | N |  |  | ✓ |
| decimals | decimals | Int | N | 2 |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |

### ExchangeRate → `ExchangeRate`
`apps/accounting/prisma/schema.prisma:499`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| currency | currency | CurrencyCode | N |  |  | ✓ |
| rateToEgp | rate_to_egp | Decimal @db.Decimal(14,6) | N |  |  | ✓ |
| rateType | rate_type | FxRateType | N |  |  | ✓ |
| effectiveDate | effective_date | DateTime | N |  |  | ✓ |
| source | source | String? | Y |  |  | ✓ |
| recordedBy | recorded_by | String | N |  |  | ✓ |
| recordedAt | recorded_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@unique([currency, rateType, effectiveDate])`; `@@index([currency, effectiveDate(sort: Desc)])`

### SupplierLedgerEntry → `supplier_ledger_entries`
`apps/accounting/prisma/schema.prisma:523`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| supplierId | supplier_id | String | N |  | LREF | ✓ |
| side | side | LedgerSide | N |  |  | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| currency | currency | CurrencyCode | N | EGP |  | ✓ |
| amountFx | amount_fx | Decimal? @db.Decimal(14,2) | Y |  |  | ✓ |
| fxRate | fx_rate | Decimal? @db.Decimal(14,6) | Y |  |  | ✓ |
| refType | ref_type | String | N |  |  | ✓ |
| refId | ref_id | String | N |  | LREF | ✓ |
| description | description | String? | Y |  |  | ✓ |
| occurredAt | occurred_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([supplierId])`; `@@index([occurredAt])`; `@@unique([refType, refId])`

### ProcessedEvent → `processed_events`
`apps/accounting/prisma/schema.prisma:545`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| eventId | event_id | String | N |  | PK | ✓ |
| processedAt | processed_at | DateTime | N | now() |  | ✓ |

### CancelledOrder → `cancelled_orders`
`apps/accounting/prisma/schema.prisma:560`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| orderId | order_id | String | N |  | PK | ✓ |
| reason | reason | String | N |  |  | ✓ |
| cancelledBy | cancelled_by | String? | Y |  |  | ✓ |
| eventId | event_id | String | N |  | LREF | ✓ |
| cancelledAt | cancelled_at | DateTime | N | now() |  | ✓ |

### AuditLog → `audit_logs`
`apps/accounting/prisma/schema.prisma:570`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| userId | user_id | String? | Y |  | LREF | ✓ |
| action | action | String | N |  |  | ✓ |
| entity | entity | String | N |  |  | ✓ |
| entityId | entity_id | String? | Y |  | LREF | ✓ |
| before | before | Json? | Y |  |  | ✓ |
| after | after | Json? | Y |  |  | ✓ |
| reasonCode | reason_code | String? | Y |  |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| ipAddress | ip_address | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([userId])`; `@@index([entity])`; `@@index([createdAt])`

### SupplierPayment → `supplier_payments` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:589`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | — |
| idempotencyKey | idempotency_key | String | N |  | U | — |
| requestHash | request_hash | String | N |  |  | — |
| supplierId | supplier_id | String | N |  | LREF | — |
| supplierInvoiceId | supplier_invoice_id | String? | Y |  | LREF | — |
| method | method | String | N |  |  | — |
| currency | currency | CurrencyCode | N | EGP |  | — |
| amountFx | amount_fx | Decimal @db.Decimal(14,2) | N |  |  | — |
| fxRate | fx_rate | Decimal @db.Decimal(14,6) | N | 1 |  | — |
| amountEgp | amount_egp | Decimal @db.Decimal(14,2) | N |  |  | — |
| financialAccountId | financial_account_id | String? | Y |  | LREF | — |
| bankRef | bank_ref | String? | Y |  |  | — |
| paidAt | paid_at | DateTime | N | now() |  | — |
| actorId | actor_id | String | N |  | LREF | — |
| reversed | reversed | Boolean | N | false |  | — |
| reversedAt | reversed_at | DateTime? | Y |  |  | — |
| reversalReason | reversal_reason | String? | Y |  |  | — |
| reversedBy | reversed_by | String? | Y |  |  | — |
| createdAt | created_at | DateTime | N | now() |  | — |

Indexes/constraints: `@@index([supplierId, paidAt])`; `@@index([supplierInvoiceId])`; `@@index([financialAccountId])`

### JournalEntry → `journal_entries` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:625`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | — |
| journalNumber | journal_number | String | N |  | U | — |
| description | description | String | N |  |  | — |
| fiscalPeriodId | fiscal_period_id | String | N |  | LREF | — |
| status | status | JournalEntryStatus | N | DRAFT |  | — |
| createdBy | created_by | String | N |  |  | — |
| submittedBy | submitted_by | String? | Y |  |  | — |
| submittedAt | submitted_at | DateTime? | Y |  |  | — |
| approvedBy | approved_by | String? | Y |  |  | — |
| approvedAt | approved_at | DateTime? | Y |  |  | — |
| postedBy | posted_by | String? | Y |  |  | — |
| postedAt | posted_at | DateTime? | Y |  |  | — |
| rejectedBy | rejected_by | String? | Y |  |  | — |
| rejectedAt | rejected_at | DateTime? | Y |  |  | — |
| rejectionReason | rejection_reason | String? | Y |  |  | — |
| reversalOfId | reversal_of_id | String? | Y |  | U LREF | — |
| sourceType | source_type | String? | Y |  |  | — |
| sourceId | source_id | String? | Y |  | LREF | — |
| createdAt | created_at | DateTime | N | now() |  | — |
| updatedAt | updated_at | DateTime | N |  |  | — |

Indexes/constraints: `@@index([fiscalPeriodId, status])`; `@@index([createdBy])`; `@@index([createdAt])`; `@@unique([sourceType, sourceId])`

### JournalLine → `journal_lines` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:656`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | — |
| journalEntryId | journal_entry_id | String | N |  | FK-col | — |
| accountId | account_id | String | N |  | LREF | — |
| description | description | String? | Y |  |  | — |
| debit | debit | Decimal @db.Decimal(14,2) | N | 0 |  | — |
| credit | credit | Decimal @db.Decimal(14,2) | N | 0 |  | — |
| currency | currency | CurrencyCode | N | EGP |  | — |
| fxRate | fx_rate | Decimal @db.Decimal(14,6) | N | 1 |  | — |
| baseDebit | base_debit | Decimal @db.Decimal(14,2) | N | 0 |  | — |
| baseCredit | base_credit | Decimal @db.Decimal(14,2) | N | 0 |  | — |
| journalEntry | journalEntry | JournalEntry | N |  | FK→JournalEntry(id) onDelete=Cascade | — |

Indexes/constraints: `@@index([journalEntryId])`; `@@index([accountId])`

### Account → `chart_of_accounts`
`apps/accounting/prisma/schema.prisma:702`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | String | N |  | U | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String? | Y |  |  | ✓ |
| type | type | AccountType | N |  |  | ✓ |
| nature | nature | AccountNature | N |  |  | ✓ |
| classification | classification | AccountClassification? | Y |  |  | ✓ |
| level | level | Int | N | 1 |  | ✓ |
| isHeader | is_header | Boolean | N | false |  | ✓ |
| parentId | parent_id | String? | Y |  | FK-col | ✓ |
| currency | currency | CurrencyCode | N | EGP |  | ✓ |
| balance | balance | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| description | description | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| parent | parent | Account? | Y |  | FK→Account(id) onDelete=default | ✓ |
| children | children | Account[] | N |  | FK→Account() onDelete=default | ✓ |

Indexes/constraints: `@@index([code])`; `@@index([type])`; `@@index([parentId])`

### FiscalPeriod → `fiscal_periods`
`apps/accounting/prisma/schema.prisma:737`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | String | N |  | U | ✓ |
| fiscalYear | fiscal_year | Int | N |  |  | ✓ |
| periodNumber | period_number | Int | N |  |  | ✓ |
| startDate | start_date | DateTime | N |  |  | ✓ |
| endDate | end_date | DateTime | N |  |  | ✓ |
| status | status | PeriodStatus | N | OPEN |  | ✓ |
| closedAt | closed_at | DateTime? | Y |  |  | ✓ |
| closedBy | closed_by | String? | Y |  |  | ✓ |
| closingNotes | closing_notes | String? | Y |  |  | ✓ |
| reopenedAt | reopened_at | DateTime? | Y |  |  | ✓ |
| reopenedBy | reopened_by | String? | Y |  |  | ✓ |
| closingJournalId | closing_journal_id | String? | Y |  | LREF | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@unique([fiscalYear, periodNumber])`; `@@index([status])`; `@@index([startDate, endDate])`

### LandedCostVoucher → `landed_cost_vouchers`
`apps/accounting/prisma/schema.prisma:767`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| voucherNumber | voucher_number | String | N |  | U | ✓ |
| shipmentReference | shipment_reference | String | N |  |  | ✓ |
| vendorInvoiceId | vendor_invoice_id | String? | Y |  | LREF | ✓ |
| currency | currency | CurrencyCode | N | USD |  | ✓ |
| exchangeRate | exchange_rate | Decimal @db.Decimal(14, 6) | N |  |  | ✓ |
| customsDutyEgp | customs_duty_egp | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| freightEgp | freight_egp | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| insuranceEgp | insurance_egp | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| portHandlingEgp | port_handling_egp | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| clearanceEgp | clearance_egp | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| totalExpensesEgp | total_expenses_egp | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| allocationMethod | allocation_method | LandedCostAllocationMethod | N | BY_VALUE |  | ✓ |
| status | status | String | N | "POSTED" |  | ✓ |
| allocatedAt | allocated_at | DateTime | N | now() |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([shipmentReference])`; `@@index([allocatedAt])`

### LandedCostItem → `landed_cost_items`
`apps/accounting/prisma/schema.prisma:793`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| voucherId | voucher_id | String | N |  | FK-col | ✓ |
| productId | product_id | String | N |  | LREF | ✓ |
| productName | product_name | String | N |  |  | ✓ |
| quantity | quantity | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| fobPriceForeign | fob_price_foreign | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| fobPriceEgp | fob_price_egp | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| allocatedExpensesEgp | allocated_expenses_egp | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| finalTotalCostEgp | final_total_cost_egp | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| finalUnitCostEgp | final_unit_cost_egp | Decimal @db.Decimal(14, 4) | N |  |  | ✓ |
| voucher | voucher | LandedCostVoucher | N |  | FK→LandedCostVoucher(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([voucherId])`; `@@index([productId])`

### FixedAsset → `fixed_assets`
`apps/accounting/prisma/schema.prisma:833`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| assetCode | asset_code | String | N |  | U | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String? | Y |  |  | ✓ |
| category | category | AssetCategory | N | DISTRIBUTION_VEHICLES |  | ✓ |
| status | status | AssetStatus | N | IN_SERVICE |  | ✓ |
| purchaseDate | purchase_date | DateTime | N |  |  | ✓ |
| purchaseCost | purchase_cost | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| salvageValue | salvage_value | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| usefulLifeMonths | useful_life_months | Int | N |  |  | ✓ |
| depreciationMethod | depreciation_method | DepreciationMethod | N | STRAIGHT_LINE |  | ✓ |
| accumulatedDepreciation | accumulated_depreciation | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| netBookValue | net_book_value | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| location | location | String? | Y |  |  | ✓ |
| serialNumber | serial_number | String? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@index([category])`; `@@index([status])`

### DepreciationEntry → `depreciation_entries`
`apps/accounting/prisma/schema.prisma:860`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| assetId | asset_id | String | N |  | FK-col | ✓ |
| fiscalYear | fiscal_year | Int | N |  |  | ✓ |
| periodMonth | period_month | Int | N |  |  | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| nbvAfter | nbv_after | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| journalEntryId | journal_entry_id | String? | Y |  | LREF | ✓ |
| postedAt | posted_at | DateTime | N | now() |  | ✓ |
| asset | asset | FixedAsset | N |  | FK→FixedAsset(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([assetId])`; `@@index([fiscalYear, periodMonth])`

### CreditNote → `credit_notes`
`apps/accounting/prisma/schema.prisma:912`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| number | number | String | N |  | U | ✓ |
| returnId | return_id | String | N |  | U LREF | ✓ |
| invoiceId | invoice_id | String? | Y |  | LREF | ✓ |
| accountId | account_id | String | N |  | LREF | ✓ |
| accountName | account_name | String? | Y |  |  | ✓ |
| subtotal | subtotal | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| taxAmount | tax_amount | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| total | total | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| status | status | CreditNoteStatus | N | ISSUED |  | ✓ |
| vatPosted | vat_posted | Boolean | N | false |  | ✓ |
| issuedById | issued_by_id | String? | Y |  | LREF | ✓ |
| issuedAt | issued_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([accountId])`; `@@index([issuedAt])`

### DocumentSequence → `document_sequences`
`apps/accounting/prisma/schema.prisma:938`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| name | name | String | N |  |  | ✓ |
| year | year | Int | N |  |  | ✓ |
| lastValue | last_value | Int | N | 0 |  | ✓ |

Indexes/constraints: `@@id([name, year])`

### TaxEntry → `tax_entries`
`apps/accounting/prisma/schema.prisma:947`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| invoiceId | invoice_id | String? | Y |  | LREF | ✓ |
| partyId | party_id | String | N |  | LREF | ✓ |
| partyName | party_name | String | N |  |  | ✓ |
| partyTaxNumber | party_tax_number | String? | Y |  |  | ✓ |
| partyFileNumber | party_file_number | String? | Y |  |  | ✓ |
| transactionType | transaction_type | TaxTransactionType | N |  |  | ✓ |
| taxType | tax_type | TaxType | N |  |  | ✓ |
| baseAmount | base_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| taxRate | tax_rate | Decimal @db.Decimal(5, 2) | N |  |  | ✓ |
| taxAmount | tax_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| quarter | quarter | String | N |  |  | ✓ |
| fiscalYear | fiscal_year | Int | N |  |  | ✓ |
| occurredAt | occurred_at | DateTime | N | now() |  | ✓ |
| referenceNumber | reference_number | String? | Y |  |  | ✓ |
| isReported | is_reported | Boolean | N | false |  | ✓ |
| reportedAt | reported_at | DateTime? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([partyId])`; `@@index([taxType])`; `@@index([quarter])`; `@@index([fiscalYear])`

### PurchaseOrder → `purchase_orders`
`apps/accounting/prisma/schema.prisma:1006`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| poNumber | po_number | String | N |  | U | ✓ |
| supplierId | supplier_id | String | N |  | LREF | ✓ |
| supplierName | supplier_name | String | N |  |  | ✓ |
| orderDate | order_date | DateTime | N | now() |  | ✓ |
| expectedDate | expected_date | DateTime? | Y |  |  | ✓ |
| status | status | POStatus | N | DRAFT |  | ✓ |
| totalAmount | total_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| currency | currency | CurrencyCode | N | EGP |  | ✓ |
| createdById | created_by_id | String? | Y |  | LREF | ✓ |
| approvedBy | approved_by | String? | Y |  |  | ✓ |
| approvedAt | approved_at | DateTime? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([supplierId])`; `@@index([status])`

### PurchaseOrderLine → `purchase_order_lines`
`apps/accounting/prisma/schema.prisma:1036`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| purchaseOrderId | purchase_order_id | String | N |  | FK-col | ✓ |
| productId | product_id | String | N |  | LREF | ✓ |
| productName | product_name | String | N |  |  | ✓ |
| orderedQty | ordered_qty | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| receivedQty | received_qty | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| unitPrice | unit_price | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| totalAmount | total_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| purchaseOrder | purchaseOrder | PurchaseOrder | N |  | FK→PurchaseOrder(id) onDelete=Cascade | ✓ |

### PurchaseOrderReceipt → `purchase_order_receipts` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:1056`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | — |
| eventId | event_id | String | N |  | U LREF | — |
| purchaseOrderId | purchase_order_id | String | N |  | FK-col | — |
| purchaseOrderLineId | purchase_order_line_id | String | N |  | FK-col | — |
| productId | product_id | String | N |  | LREF | — |
| supplierId | supplier_id | String | N |  | LREF | — |
| warehouseId | warehouse_id | String | N |  | LREF | — |
| batchId | batch_id | String | N |  | LREF | — |
| quantity | quantity | Decimal @db.Decimal(14, 2) | N |  |  | — |
| receivedAt | received_at | DateTime | N | now() |  | — |
| actorId | actor_id | String? | Y |  | LREF | — |
| purchaseOrder | purchaseOrder | PurchaseOrder | N |  | FK→PurchaseOrder(id) onDelete=Cascade | — |
| purchaseOrderLine | purchaseOrderLine | PurchaseOrderLine | N |  | FK→PurchaseOrderLine(id) onDelete=Cascade | — |

Indexes/constraints: `@@index([purchaseOrderId, receivedAt])`; `@@index([purchaseOrderLineId, receivedAt])`

### VendorInvoice → `vendor_invoices`
`apps/accounting/prisma/schema.prisma:1077`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| invoiceNumber | invoice_number | String | N |  |  | ✓ |
| supplierId | supplier_id | String | N |  | LREF | ✓ |
| supplierName | supplier_name | String | N |  |  | ✓ |
| purchaseOrderId | purchase_order_id | String? | Y |  | FK-col | ✓ |
| grnNumber | grn_number | String? | Y |  |  | ✓ |
| status | status | VendorInvoiceStatus | N | MATCHING_PENDING |  | ✓ |
| invoiceDate | invoice_date | DateTime | N |  |  | ✓ |
| dueDate | due_date | DateTime? | Y |  |  | ✓ |
| netAmount | net_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| taxAmount | tax_amount | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| totalAmount | total_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| currency | currency | CurrencyCode | N | EGP |  | ✓ |
| exchangeRate | exchange_rate | Decimal @db.Decimal(16,6) | N | 1 |  | ✗ |
| baseTotal | base_total | Decimal @db.Decimal(14,2) | N | 0 |  | ✗ |
| isApprovedPayment | is_approved_payment | Boolean | N | false |  | ✓ |
| approvedBy | approved_by | String? | Y |  |  | ✓ |
| approvedAt | approved_at | DateTime? | Y |  |  | ✓ |
| createdById | created_by_id | String? | Y |  | LREF | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| purchaseOrder | purchaseOrder | PurchaseOrder? | Y |  | FK→PurchaseOrder(id) onDelete=default | ✓ |

Indexes/constraints: `@@unique([supplierId, invoiceNumber])`; `@@index([supplierId])`; `@@index([status])`; `@@index([purchaseOrderId])`

### VendorInvoiceLine → `vendor_invoice_lines`
`apps/accounting/prisma/schema.prisma:1118`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| vendorInvoiceId | vendor_invoice_id | String | N |  | FK-col | ✓ |
| productId | product_id | String | N |  | LREF | ✓ |
| productName | product_name | String | N |  |  | ✓ |
| billedQty | billed_qty | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| unitPrice | unit_price | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| totalAmount | total_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| vendorInvoice | vendorInvoice | VendorInvoice | N |  | FK→VendorInvoice(id) onDelete=Cascade | ✓ |

### ThreeWayMatch → `three_way_matches`
`apps/accounting/prisma/schema.prisma:1132`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| vendorInvoiceId | vendor_invoice_id | String | N |  | FK-col | ✓ |
| purchaseOrderId | purchase_order_id | String? | Y |  | FK-col | ✓ |
| grnReference | grn_reference | String? | Y |  |  | ✓ |
| status | status | MatchStatus | N | MATCHED |  | ✓ |
| orderedQtyTotal | ordered_qty_total | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| receivedQtyTotal | received_qty_total | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| billedQtyTotal | billed_qty_total | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| orderedAmountTotal | ordered_amount_total | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| billedAmountTotal | billed_amount_total | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| varianceAmount | variance_amount | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| variancePercent | variance_percent | Decimal @db.Decimal(6, 2) | N | 0 |  | ✓ |
| discrepancyDetails | discrepancy_details | Json? | Y |  |  | ✓ |
| isApproved | is_approved | Boolean | N | false |  | ✓ |
| approvedBy | approved_by | String? | Y |  |  | ✓ |
| approvalReason | approval_reason | String? | Y |  |  | ✓ |
| matchedAt | matched_at | DateTime | N | now() |  | ✓ |
| vendorInvoice | vendorInvoice | VendorInvoice | N |  | FK→VendorInvoice(id) onDelete=Cascade | ✓ |
| purchaseOrder | purchaseOrder | PurchaseOrder? | Y |  | FK→PurchaseOrder(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([vendorInvoiceId])`; `@@index([status])`

### JobRun → `job_runs`
`apps/accounting/prisma/schema.prisma:1166`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| name | name | String | N |  |  | ✓ |
| status | status | JobRunStatus | N |  |  | ✓ |
| startedAt | started_at | DateTime | N |  |  | ✓ |
| finishedAt | finished_at | DateTime? | Y |  |  | ✓ |
| affected | affected | Int? | Y |  |  | ✓ |
| error | error | String? | Y |  |  | ✓ |
| triggeredBy | triggered_by | String | N | "cron" |  | ✓ |

Indexes/constraints: `@@index([name, startedAt])`

### OutboxEvent → `outbox_events`
`apps/accounting/prisma/schema.prisma:1180`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | ✓ |
| topic | topic | String | N |  |  | ✓ |
| envelope | envelope | Json | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| nextAttemptAt | next_attempt_at | DateTime | N | now() |  | ✓ |
| attempts | attempts | Int | N | 0 |  | ✓ |
| leaseId | lease_id | String? | Y |  | LREF | ✓ |
| leaseUntil | lease_until | DateTime? | Y |  |  | ✓ |
| publishedAt | published_at | DateTime? | Y |  |  | ✓ |
| lastError | last_error | String? | Y |  |  | ✓ |

Indexes/constraints: `@@index([publishedAt, nextAttemptAt])`

### FxSnapshot → `fx_snapshots`
`apps/accounting/prisma/schema.prisma:1196`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| refType | ref_type | String | N |  |  | ✓ |
| refId | ref_id | String | N |  | LREF | ✓ |
| currency | currency | CurrencyCode | N |  |  | ✓ |
| originalAmount | original_amount | Decimal @db.Decimal(14,2) | N |  |  | ✓ |
| baseAmount | base_amount | Decimal @db.Decimal(14,2) | N |  |  | ✓ |
| rateToEgp | rate_to_egp | Decimal @db.Decimal(14,6) | N |  |  | ✓ |
| rateId | rate_id | String? | Y |  | LREF | ✓ |
| rateType | rate_type | FxRateType | N |  |  | ✓ |
| rateEffectiveAt | rate_effective_at | DateTime | N |  |  | ✓ |
| transactionAt | transaction_at | DateTime | N |  |  | ✓ |
| actorId | actor_id | String | N |  | LREF | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@unique([refType, refId])`

### FieldCollectionPosting → `field_collection_postings`
`apps/accounting/prisma/schema.prisma:1259`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | ✓ |
| actorId | actor_id | String | N |  | LREF | ✓ |
| payloadHash | payload_hash | String | N |  |  | ✓ |
| paymentIds | payment_ids | Json | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

### PaymentAllocation → `payment_allocations`
`apps/accounting/prisma/schema.prisma:1269`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| paymentId | payment_id | String | N |  | FK-col | ✓ |
| invoiceId | invoice_id | String | N |  | FK-col | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| payment | payment | Payment | N |  | FK→Payment(id) onDelete=default | ✓ |
| invoice | invoice | Invoice | N |  | FK→Invoice(id) onDelete=default | ✓ |

Indexes/constraints: `@@unique([paymentId, invoiceId])`; `@@index([invoiceId])`

### FinancialAccount → `financial_accounts`
`apps/accounting/prisma/schema.prisma:1287`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| type | type | FinancialAccountType | N |  |  | ✓ |
| currency | currency | CurrencyCode | N | EGP |  | ✓ |
| bankName | bank_name | String? | Y |  |  | ✓ |
| accountNumber | account_number | String? | Y |  |  | ✓ |
| iban | iban | String? | Y |  |  | ✓ |
| branch | branch | String? | Y |  |  | ✓ |
| walletProvider | wallet_provider | String? | Y |  |  | ✓ |
| walletNumber | wallet_number | String? | Y |  |  | ✓ |
| instapayAlias | instapay_alias | String? | Y |  |  | ✓ |
| openingBalance | opening_balance | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| balance | balance | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| isDefault | is_default | Boolean | N | false |  | ✓ |
| createdBy | created_by | String | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@unique([type, currency, nameAr])`; `@@index([type])`; `@@index([isActive])`

### FinancialAccountEntry → `financial_account_entries`
`apps/accounting/prisma/schema.prisma:1333`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| accountId | account_id | String | N |  | FK-col | ✓ |
| type | type | FinancialAccountEntryType | N |  |  | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| balanceAfter | balance_after | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| idempotencyKey | idempotency_key | String? | Y |  | U | ✓ |
| reference | reference | String? | Y |  |  | ✓ |
| description | description | String? | Y |  |  | ✓ |
| transferRef | transfer_ref | String? | Y |  |  | ✓ |
| currency | currency | CurrencyCode | N |  |  | ✓ |
| fxRate | fx_rate | Decimal? @db.Decimal(14, 6) | Y |  |  | ✓ |
| baseAmount | base_amount | Decimal? @db.Decimal(14, 2) | Y |  |  | ✓ |
| actorId | actor_id | String | N |  | LREF | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| account | account | FinancialAccount | N |  | FK→FinancialAccount(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([accountId, createdAt])`; `@@index([transferRef])`

### FinancialAccountReconciliation → `financial_account_reconciliations`
`apps/accounting/prisma/schema.prisma:1364`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| accountId | account_id | String | N |  | FK-col | ✓ |
| systemBalance | system_balance | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| actualBalance | actual_balance | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| difference | difference | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| reason | reason | String | N |  |  | ✓ |
| countedById | counted_by_id | String | N |  | LREF | ✓ |
| countedAt | counted_at | DateTime | N | now() |  | ✓ |
| account | account | FinancialAccount | N |  | FK→FinancialAccount(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([accountId, countedAt])`

### ImportShipment → `import_shipments` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:1386`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | — |
| shipmentNumber | shipment_number | String | N |  | U | — |
| poId | po_id | String? | Y |  | LREF | — |
| status | status | String | N | "PLANNED" |  | — |
| mode | mode | String | N |  |  | — |
| blNumber | bl_number | String? | Y |  |  | — |
| awbNumber | awb_number | String? | Y |  |  | — |
| containerNos | container_nos | Json | N | "[]" |  | — |
| carrier | carrier | String? | Y |  |  | — |
| forwarderSupplierId | forwarder_supplier_id | String? | Y |  | LREF | — |
| brokerSupplierId | broker_supplier_id | String? | Y |  | LREF | — |
| etd | etd | DateTime? | Y |  |  | — |
| eta | eta | DateTime? | Y |  |  | — |
| ata | ata | DateTime? | Y |  |  | — |
| portOfLoading | port_of_loading | String? | Y |  |  | — |
| portOfDischarge | port_of_discharge | String? | Y |  |  | — |
| customsDeclarationNo | customs_declaration_no | String? | Y |  |  | — |
| customsReleaseDate | customs_release_date | DateTime? | Y |  |  | — |
| freeTimeEndsAt | free_time_ends_at | DateTime? | Y |  |  | — |
| notes | notes | String? | Y |  |  | — |
| createdById | created_by_id | String | N |  | LREF | — |
| createdAt | created_at | DateTime | N | now() |  | — |
| updatedAt | updated_at | DateTime | N | now() |  | — |

Indexes/constraints: `@@index([status])`; `@@index([eta])`

### ImportShipmentLine → `import_shipment_lines` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:1421`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | — |
| shipmentId | shipment_id | String | N |  | FK-col | — |
| poLineId | po_line_id | String? | Y |  | LREF | — |
| productId | product_id | String | N |  | LREF | — |
| shippedQty | shipped_qty | Int | N |  |  | — |
| receivedQty | received_qty | Int | N | 0 |  | — |
| lotNumber | lot_number | String? | Y |  |  | — |
| expiryDate | expiry_date | DateTime? | Y |  |  | — |
| manufacturingDate | manufacturing_date | DateTime? | Y |  |  | — |
| grossWeightKg | gross_weight_kg | Decimal? @db.Decimal(14,3) | Y |  |  | — |
| volumeM3 | volume_m3 | Decimal? @db.Decimal(14,3) | Y |  |  | — |
| shipment | shipment | ImportShipment | N |  | FK→ImportShipment(id) onDelete=Cascade | — |

Indexes/constraints: `@@index([shipmentId])`

### ShipmentDocument → `shipment_documents` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:1440`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | — |
| shipmentId | shipment_id | String | N |  | FK-col | — |
| type | type | String | N |  |  | — |
| number | number | String? | Y |  |  | — |
| url | url | String | N |  |  | — |
| issuedAt | issued_at | DateTime? | Y |  |  | — |
| expiresAt | expires_at | DateTime? | Y |  |  | — |
| verified | verified | Boolean | N | false |  | — |
| verifiedBy | verified_by | String? | Y |  |  | — |
| verifiedAt | verified_at | DateTime? | Y |  |  | — |
| shipment | shipment | ImportShipment | N |  | FK→ImportShipment(id) onDelete=Cascade | — |

### RegulatoryClearance → `regulatory_clearances` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:1457`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | — |
| shipmentId | shipment_id | String | N |  | FK-col | — |
| authority | authority | String | N |  |  | — |
| fileNo | file_no | String? | Y |  |  | — |
| decision | decision | String | N | "PENDING" |  | — |
| sampleTakenAt | sample_taken_at | DateTime? | Y |  |  | — |
| decidedAt | decided_at | DateTime? | Y |  |  | — |
| certificateNo | certificate_no | String? | Y |  |  | — |
| notes | notes | String? | Y |  |  | — |
| shipment | shipment | ImportShipment | N |  | FK→ImportShipment(id) onDelete=Cascade | — |

Indexes/constraints: `@@unique([shipmentId, authority])`

### ShipmentStatusEvent → `shipment_status_events` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:1474`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | — |
| shipmentId | shipment_id | String | N |  | FK-col | — |
| fromStatus | from_status | String? | Y |  |  | — |
| toStatus | to_status | String | N |  |  | — |
| at | at | DateTime | N | now() |  | — |
| byId | by_id | String | N |  | LREF | — |
| note | note | String? | Y |  |  | — |
| shipment | shipment | ImportShipment | N |  | FK→ImportShipment(id) onDelete=Cascade | — |

Indexes/constraints: `@@index([shipmentId, at])`

### JournalEntryWorkflow → `journal_entry_workflows` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:1489`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | — |
| entryNumber | entry_number | String | N |  | U | — |
| entryDate | entry_date | DateTime | N |  |  | — |
| sourceType | source_type | String | N | "MANUAL" |  | — |
| sourceId | source_id | String? | Y |  | LREF | — |
| description | description | String | N |  |  | — |
| lines | lines | Json | N |  |  | — |
| status | status | String | N | "DRAFT" |  | — |
| createdById | created_by_id | String | N |  | LREF | — |
| submittedById | submitted_by_id | String? | Y |  | LREF | — |
| approvedById | approved_by_id | String? | Y |  | LREF | — |
| rejectedById | rejected_by_id | String? | Y |  | LREF | — |
| rejectionReason | rejection_reason | String? | Y |  |  | — |
| postedJournalId | posted_journal_id | String? | Y |  | LREF | — |
| createdAt | created_at | DateTime | N | now() |  | — |
| submittedAt | submitted_at | DateTime? | Y |  |  | — |
| approvedAt | approved_at | DateTime? | Y |  |  | — |
| rejectedAt | rejected_at | DateTime? | Y |  |  | — |
| postedAt | posted_at | DateTime? | Y |  |  | — |

Indexes/constraints: `@@index([status])`; `@@index([entryDate])`

### BankStatement → `bank_statements` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:1515`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | — |
| financialAccountId | financial_account_id | String | N |  | LREF | — |
| statementDate | statement_date | DateTime | N |  |  | — |
| openingBalance | opening_balance | Decimal @db.Decimal(18,2) | N | 0 |  | — |
| closingBalance | closing_balance | Decimal @db.Decimal(18,2) | N | 0 |  | — |
| sourceName | source_name | String | N |  |  | — |
| status | status | String | N | "OPEN" |  | — |
| importedBy | imported_by | String | N |  |  | — |
| reconciledAt | reconciled_at | DateTime? | Y |  |  | — |
| reconciledBy | reconciled_by | String? | Y |  |  | — |
| createdAt | created_at | DateTime | N | now() |  | — |
| updatedAt | updated_at | DateTime | N | now() |  | — |

Indexes/constraints: `@@index([financialAccountId, statementDate])`

### BankStatementLine → `bank_statement_lines` **(CURRENT فقط)**
`apps/accounting/prisma/schema.prisma:1535`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | — |
| statementId | statement_id | String | N |  | FK-col | — |
| transactionDate | transaction_date | DateTime | N |  |  | — |
| valueDate | value_date | DateTime? | Y |  |  | — |
| amount | amount | Decimal @db.Decimal(18,2) | N |  |  | — |
| direction | direction | String | N |  |  | — |
| reference | reference | String? | Y |  |  | — |
| description | description | String? | Y |  |  | — |
| matchedSourceType | matched_source_type | String? | Y |  |  | — |
| matchedSourceId | matched_source_id | String? | Y |  | LREF | — |
| matchedAt | matched_at | DateTime? | Y |  |  | — |
| matchedBy | matched_by | String? | Y |  |  | — |
| createdAt | created_at | DateTime | N | now() |  | — |
| statement | statement | BankStatement | N |  | FK→BankStatement(id) onDelete=Cascade | — |

Indexes/constraints: `@@index([statementId])`; `@@index([statementId, matchedSourceId])`

#### Enums (accounting)
| Enum | Values | B? |
|---|---|---|
| InvoiceStatus | UNPAID, DEFERRED, PARTIAL, PAID, CANCELLED | ✓ |
| PaymentMethod | CASH, CHECK, DEPOSIT, TRANSFER, E_WALLET, INSTAPAY | ✓ |
| InstrumentType | CHECK, PROMISSORY_NOTE | ✗ |
| InstrumentStatus | RECEIVED, DEPOSITED, CLEARED, BOUNCED, REPLACED, CANCELLED | ✗ |
| CheckStatus | RECEIVED, DEPOSITED, CLEARED, BOUNCED | ✓ |
| LedgerSide | DEBIT, CREDIT | ✓ |
| CurrencyCode | EGP, USD, EUR, GBP, CNY, AED, SAR | ✓ |
| InvoiceDocumentType | TAX_INVOICE, NORMAL_INVOICE, RECEIPT_FORM | ✓ |
| InvoiceDiscountType | AMOUNT, PERCENT | ✓ |
| GeneralPurchaseStatus | DRAFT, CONFIRMED, CANCELLED | ✓ |
| GeneralPurchaseRevisionAction | CREATED, UPDATED | ✓ |
| FxRateType | CBE_OFFICIAL, BANK, CUSTOMS, MANUAL | ✓ |
| JournalEntryStatus | DRAFT, SUBMITTED, APPROVED, POSTED, REJECTED, REVERSED | ✗ |
| AccountType | ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE | ✓ |
| AccountNature | DEBIT, CREDIT | ✓ |
| AccountClassification | CURRENT_ASSET, NON_CURRENT_ASSET, CURRENT_LIABILITY, NON_CURRENT_LIABILITY, EQUITY, OPERATING_REVENUE, DIRECT_COST, OPERATING_EXPENSE, OTHER_INCOME_EXPENSE | ✓ |
| PeriodStatus | OPEN, SOFT_LOCKED, CLOSED, YEAR_END_CLOSED | ✓ |
| LandedCostAllocationMethod | BY_VALUE, BY_QUANTITY, BY_WEIGHT | ✓ |
| AssetCategory | DISTRIBUTION_VEHICLES, COLD_CHAIN_REFRIGERATION, WAREHOUSE_EQUIPMENT, IT_INFRASTRUCTURE, FURNITURE_FIXTURES | ✓ |
| AssetStatus | IN_SERVICE, UNDER_MAINTENANCE, FULLY_DEPRECIATED, DISPOSED, SCRAPPED | ✓ |
| DepreciationMethod | STRAIGHT_LINE, REDUCING_BALANCE | ✓ |
| TaxType | VAT_14, WHT_1, WHT_3, WHT_5, EXEMPT | ✓ |
| TaxTransactionType | SALES, PURCHASE, EXPENSE, PAYMENT_DEDUCTION | ✓ |
| CreditNoteStatus | ISSUED, VOID | ✓ |
| MatchStatus | MATCHED, QUANTITY_MISMATCH, PRICE_MISMATCH, UNMATCHED_GRN, APPROVED_EXCEPTION, REJECTED | ✓ |
| POStatus | DRAFT, PENDING_APPROVAL, APPROVED, PARTIALLY_RECEIVED, FULLY_RECEIVED, CANCELLED | ✓ |
| VendorInvoiceStatus | DRAFT, MATCHING_PENDING, MATCHED, EXCEPTION_PENDING, APPROVED_FOR_PAYMENT, REJECTED, PAID | ✓ |
| JobRunStatus | RUNNING, SUCCESS, FAILED, SKIPPED_LOCKED | ✓ |
| FinancialAccountType | CASH, BANK, E_WALLET, INSTAPAY | ✓ |
| FinancialAccountEntryType | OPENING_BALANCE, DEPOSIT, WITHDRAWAL, TRANSFER_IN, TRANSFER_OUT, EXPENSE, ADMIN_EXPENSE, ADJUSTMENT, PAYMENT_IN, PAYMENT_OUT | ✓ |

## خدمة `audit-aggregator` — DB `nile_audit`
المصدر: `apps/audit-aggregator/prisma/schema.prisma`

### AuditEvent → `audit_events`
`apps/audit-aggregator/prisma/schema.prisma:22`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| seq | seq | BigInt | N | autoincrement() |  | ✓ |
| hash | hash | String | N | "" |  | ✓ |
| prevHash | prev_hash | String | N | "GENESIS" |  | ✓ |
| eventId | event_id | String | N |  | U LREF | ✓ |
| eventType | event_type | String | N |  |  | ✓ |
| aggregateId | aggregate_id | String | N |  | LREF | ✓ |
| actorId | actor_id | String | N |  | LREF | ✓ |
| correlationId | correlation_id | String | N |  | LREF | ✓ |
| occurredAt | occurred_at | DateTime | N |  |  | ✓ |
| reasonCode | reason_code | String? | Y |  |  | ✓ |
| sourceTopic | source_topic | String | N |  |  | ✓ |
| payload | payload | Json | N |  |  | ✓ |
| receivedAt | received_at | DateTime | N | now() |  | ✓ |
| domain | domain | String | N |  |  | ✓ |
| severity | severity | String | N |  |  | ✓ |
| entityType | entity_type | String | N |  |  | ✓ |
| action | action | String | N |  |  | ✓ |
| before | before | Json? | Y |  |  | ✓ |
| after | after | Json? | Y |  |  | ✓ |
| result | result | String | N | "SUCCESS" |  | ✓ |
| financialImpact | financial_impact | Boolean | N | false |  | ✓ |
| inventoryImpact | inventory_impact | Boolean | N | false |  | ✓ |
| creditImpact | credit_impact | Boolean | N | false |  | ✓ |
| permissionImpact | permission_impact | Boolean | N | false |  | ✓ |
| organizationId | organization_id | String? | Y |  | LREF | ✓ |
| source | source | String? | Y |  |  | ✓ |
| ipAddress | ip_address | String? | Y |  |  | ✓ |

Indexes/constraints: `@@index([eventType])`; `@@index([aggregateId])`; `@@index([correlationId])`; `@@index([occurredAt])`; `@@index([domain])`; `@@index([severity])`; `@@index([actorId])`

### ProcessedEvent → `processed_events`
`apps/audit-aggregator/prisma/schema.prisma:76`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| eventId | event_id | String | N |  | PK | ✓ |
| processedAt | processed_at | DateTime | N | now() |  | ✓ |

### AuditLog → `audit_logs`
`apps/audit-aggregator/prisma/schema.prisma:84`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| userId | user_id | String? | Y |  | LREF | ✓ |
| action | action | String | N |  |  | ✓ |
| entity | entity | String | N |  |  | ✓ |
| entityId | entity_id | String? | Y |  | LREF | ✓ |
| before | before | Json? | Y |  |  | ✓ |
| after | after | Json? | Y |  |  | ✓ |
| reasonCode | reason_code | String? | Y |  |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| ipAddress | ip_address | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([userId])`; `@@index([entity])`; `@@index([createdAt])`

### DeadLetterMessage → `dead_letter_messages`
`apps/audit-aggregator/prisma/schema.prisma:115`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| topic | topic | String | N |  |  | ✓ |
| eventType | event_type | String | N |  |  | ✓ |
| eventId | event_id | String? | Y |  | LREF | ✓ |
| consumerGroup | consumer_group | String? | Y |  |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| payload | payload | Json | N |  |  | ✓ |
| envelope | envelope | Json? | Y |  |  | ✓ |
| deliveryAttempts | delivery_attempts | Int? | Y |  |  | ✓ |
| errorReason | error_reason | String | N |  |  | ✓ |
| errorStack | error_stack | String? | Y |  |  | ✓ |
| retryCount | retry_count | Int | N | 0 |  | ✓ |
| status | status | DlqStatus | N | PENDING |  | ✓ |
| failedAt | failed_at | DateTime | N | now() |  | ✓ |
| lastRetriedAt | last_retried_at | DateTime? | Y |  |  | ✓ |
| resolvedAt | resolved_at | DateTime? | Y |  |  | ✓ |
| resolvedBy | resolved_by | String? | Y |  |  | ✓ |
| discardReason | discard_reason | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@unique([eventId, consumerGroup])`; `@@index([topic])`; `@@index([eventType])`; `@@index([status])`; `@@index([failedAt])`

#### Enums (audit-aggregator)
| Enum | Values | B? |
|---|---|---|
| DlqStatus | PENDING, RETRYING, RESOLVED, DISCARDED | ✓ |

## خدمة `crm` — DB `nile_crm`
المصدر: `apps/crm/prisma/schema.prisma`

### Account → `accounts`
`apps/crm/prisma/schema.prisma:132`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | String | N |  | U | ✓ |
| nameAr | name_ar | String | N |  | U | ✓ |
| nameEn | name_en | String? | Y |  |  | ✓ |
| type | type | AccountType | N |  |  | ✓ |
| territoryId | territory_id | String? | Y |  | LREF | ✓ |
| repId | rep_id | String? | Y |  | LREF | ✓ |
| phone | phone | String? | Y |  |  | ✓ |
| email | email | String? | Y |  |  | ✓ |
| address | address | String? | Y |  |  | ✓ |
| city | city | String? | Y |  |  | ✓ |
| governorate | governorate | String? | Y |  |  | ✓ |
| district | district | String? | Y |  |  | ✓ |
| street | street | String? | Y |  |  | ✓ |
| building | building | String? | Y |  |  | ✓ |
| floor | floor | String? | Y |  |  | ✓ |
| addressDetails | address_details | String? | Y |  |  | ✓ |
| latitude | latitude | Decimal? @db.Decimal(9, 6) | Y |  |  | ✓ |
| longitude | longitude | Decimal? @db.Decimal(9, 6) | Y |  |  | ✓ |
| profileVersion | profile_version | Int | N | 0 |  | ✓ |
| openingBalance | opening_balance | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| creditLimit | credit_limit | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| commissionPct | commission_pct | Decimal? @db.Decimal(5, 2) | Y |  |  | ✓ |
| priceListId | price_list_id | String? | Y |  | LREF | ✗ |
| pricingDiscountPct | pricing_discount_pct | Decimal @db.Decimal(5, 2) | N | 12 |  | ✗ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| secondaryPhone | secondary_phone | String? | Y |  |  | ✓ |

Indexes/constraints: `@@index([type])`; `@@index([territoryId])`; `@@index([repId])`; `@@index([priceListId], map: "accounts_price_list_idx")`

### VisitPlan → `visit_plans`
`apps/crm/prisma/schema.prisma:206`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| title | title | String? | Y |  |  | ✓ |
| id | id | String | N | uuid() | PK | ✓ |
| planNumber | plan_number | String | N |  | U | ✓ |
| planDate | plan_date | DateTime | N |  |  | ✓ |
| repId | rep_id | String | N |  | LREF | ✓ |
| territoryId | territory_id | String? | Y |  | LREF | ✓ |
| status | status | VisitPlanStatus | N | DRAFT |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| createdBy | created_by | String | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@index([planDate])`; `@@index([repId, planDate])`; `@@index([territoryId])`

### Visit → `visits`
`apps/crm/prisma/schema.prisma:227`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| registeredAddress | registeredAddress | CustomerAddress? | Y |  | FK→CustomerAddress(id) onDelete=Restrict | ✓ |
| rescheduleRequest | rescheduleRequest | VisitRescheduleRequest? | Y |  | FK→VisitRescheduleRequest() onDelete=default | ✓ |
| acceptedRescheduleRequest | acceptedRescheduleRequest | VisitRescheduleRequest? | Y |  | FK→VisitRescheduleRequest() onDelete=default | ✓ |
| startGpsCapturedAt | start_gps_captured_at | DateTime? | Y |  |  | ✓ |
| endGpsCapturedAt | end_gps_captured_at | DateTime? | Y |  |  | ✓ |
| startLocationSource | start_location_source | String? | Y |  |  | ✓ |
| endLocationSource | end_location_source | String? | Y |  |  | ✓ |
| checkedInBy | checked_in_by | String? | Y |  |  | ✓ |
| checkedOutBy | checked_out_by | String? | Y |  |  | ✓ |
| addressId | address_id | String? | Y |  | FK-col | ✓ |
| addressSnapshot | address_snapshot | Json? | Y |  |  | ✓ |
| startGpsException | start_gps_exception | String? | Y |  |  | ✓ |
| endGpsException | end_gps_exception | String? | Y |  |  | ✓ |
| startGpsAccuracy | start_gps_accuracy | Float? | Y |  |  | ✓ |
| endGpsAccuracy | end_gps_accuracy | Float? | Y |  |  | ✓ |
| gpsReviewStatus | gps_review_status | String | N | "NOT_REQUIRED" |  | ✓ |
| gpsReviewedBy | gps_reviewed_by | String? | Y |  |  | ✓ |
| gpsReviewNote | gps_review_note | String? | Y |  |  | ✓ |
| id | id | String | N | uuid() | PK | ✓ |
| accountId | account_id | String | N |  | FK-col | ✓ |
| repId | rep_id | String | N |  | LREF | ✓ |
| planId | plan_id | String? | Y |  | FK-col | ✓ |
| visitDate | visit_date | DateTime | N | now() |  | ✓ |
| scheduledAt | scheduled_at | DateTime | N | now() |  | ✓ |
| actualStart | actual_start | DateTime? | Y |  |  | ✓ |
| actualEnd | actual_end | DateTime? | Y |  |  | ✓ |
| durationMinutes | duration_minutes | Int? | Y |  |  | ✓ |
| sequence | sequence | Int | N | 0 |  | ✓ |
| expectedDurationMins | expected_duration_mins | Int | N | 45 |  | ✓ |
| priority | priority | VisitPriority | N | NORMAL |  | ✓ |
| status | status | FieldVisitStatus | N | PLANNED |  | ✓ |
| purpose | purpose | VisitPurpose | N | SALES |  | ✓ |
| outcome | outcome | VisitOutcome | N | FOLLOW_UP |  | ✓ |
| result | result | VisitResult? | Y |  |  | ✓ |
| contactName | contact_name | String? | Y |  |  | ✓ |
| contactPosition | contact_position | String? | Y |  |  | ✓ |
| contactPhone | contact_phone | String? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| nextAction | next_action | String? | Y |  |  | ✓ |
| followUpDate | follow_up_date | DateTime? | Y |  |  | ✓ |
| startLatitude | start_latitude | Decimal? @db.Decimal(10, 7) | Y |  |  | ✓ |
| startLongitude | start_longitude | Decimal? @db.Decimal(10, 7) | Y |  |  | ✓ |
| endLatitude | end_latitude | Decimal? @db.Decimal(10, 7) | Y |  |  | ✓ |
| endLongitude | end_longitude | Decimal? @db.Decimal(10, 7) | Y |  |  | ✓ |
| locationVerified | location_verified | Boolean | N | false |  | ✓ |
| orderId | order_id | String? | Y |  | LREF | ✓ |
| rescheduledFromId | rescheduled_from_id | String? | Y |  | U FK-col | ✓ |
| recurrenceKey | recurrence_key | String? | Y |  | U | ✓ |
| account | account | Account | N |  | FK→Account(id) onDelete=default | ✓ |
| plan | plan | VisitPlan? | Y |  | FK→VisitPlan(id) onDelete=default | ✓ |
| rescheduledFrom | rescheduledFrom | Visit? | Y |  | FK→Visit(id) onDelete=default | ✓ |
| replacementVisit | replacementVisit | Visit? | Y |  | FK→Visit() onDelete=default | ✓ |

Indexes/constraints: `@@index([accountId])`; `@@index([repId])`; `@@index([planId])`; `@@unique([planId, accountId])`; `@@index([scheduledAt])`; `@@index([orderId])`; `@@index([status])`

### CustomerAssignment → `customer_assignments`
`apps/crm/prisma/schema.prisma:309`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| accountId | account_id | String | N |  | FK-col | ✓ |
| repId | rep_id | String | N |  | LREF | ✓ |
| role | role | CustomerAssignmentRole | N | PRIMARY |  | ✓ |
| territoryId | territory_id | String? | Y |  | LREF | ✓ |
| startsAt | starts_at | DateTime | N |  |  | ✓ |
| endsAt | ends_at | DateTime? | Y |  |  | ✓ |
| visitEveryDays | visit_every_days | Int? | Y |  |  | ✓ |
| assignedBy | assigned_by | String | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| account | account | Account | N |  | FK→Account(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([accountId, startsAt])`; `@@index([repId, endsAt])`; `@@index([territoryId])`

### FollowUp → `follow_ups`
`apps/crm/prisma/schema.prisma:329`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| accountId | account_id | String | N |  | FK-col | ✓ |
| visitId | visit_id | String? | Y |  | FK-col | ✓ |
| assignedTo | assigned_to | String | N |  |  | ✓ |
| dueAt | due_at | DateTime | N |  |  | ✓ |
| purpose | purpose | FollowUpPurpose | N | GENERAL |  | ✓ |
| status | status | FollowUpStatus | N | OPEN |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| completedAt | completed_at | DateTime? | Y |  |  | ✓ |
| createdBy | created_by | String | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| account | account | Account | N |  | FK→Account(id) onDelete=Cascade | ✓ |
| visit | visit | Visit? | Y |  | FK→Visit(id) onDelete=SetNull | ✓ |

Indexes/constraints: `@@index([assignedTo, dueAt])`; `@@index([accountId, dueAt])`; `@@index([status])`

### CustomerInteraction → `customer_interactions`
`apps/crm/prisma/schema.prisma:350`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| accountId | account_id | String | N |  | FK-col | ✓ |
| visitId | visit_id | String? | Y |  | FK-col | ✓ |
| repId | rep_id | String | N |  | LREF | ✓ |
| type | type | CustomerInteractionType | N | CALL |  | ✓ |
| outcome | outcome | CallOutcome? | Y |  |  | ✓ |
| occurredAt | occurred_at | DateTime | N | now() |  | ✓ |
| durationSeconds | duration_seconds | Int? | Y |  |  | ✓ |
| contactName | contact_name | String? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| createdBy | created_by | String | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| account | account | Account | N |  | FK→Account(id) onDelete=Cascade | ✓ |
| visit | visit | Visit? | Y |  | FK→Visit(id) onDelete=SetNull | ✓ |

Indexes/constraints: `@@index([accountId, occurredAt])`; `@@index([repId, occurredAt])`; `@@index([visitId])`

### VisitProductDiscussion → `visit_product_discussions`
`apps/crm/prisma/schema.prisma:373`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| visitId | visit_id | String | N |  | FK-col | ✓ |
| productId | product_id | String | N |  | LREF | ✓ |
| productName | product_name | String? | Y |  |  | ✓ |
| interest | interest | ProductInterest | N | MEDIUM |  | ✓ |
| quantityDiscussed | quantity_discussed | Int? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| visit | visit | Visit | N |  | FK→Visit(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([visitId])`; `@@index([productId])`

### RepTarget → `rep_targets`
`apps/crm/prisma/schema.prisma:389`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| repId | rep_id | String | N |  | LREF | ✓ |
| territoryId | territory_id | String? | Y |  | LREF | ✓ |
| period | period | TargetPeriod | N |  |  | ✓ |
| periodStart | period_start | DateTime | N |  |  | ✓ |
| periodEnd | period_end | DateTime | N |  |  | ✓ |
| salesTarget | sales_target | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| visitTarget | visit_target | Int | N | 0 |  | ✓ |
| orderTarget | order_target | Int | N | 0 |  | ✓ |
| createdBy | created_by | String | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@unique([repId, territoryId, period, periodStart])`; `@@index([repId, periodStart, periodEnd])`

### Lead → `leads`
`apps/crm/prisma/schema.prisma:408`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| accountId | account_id | String? | Y |  | FK-col | ✓ |
| title | title | String | N |  |  | ✓ |
| status | status | LeadStatus | N | NEW |  | ✓ |
| estimatedValue | estimated_value | Decimal? @db.Decimal(14, 2) | Y |  |  | ✓ |
| repId | rep_id | String? | Y |  | LREF | ✓ |
| source | source | String? | Y |  |  | ✗ |
| contactName | contact_name | String? | Y |  |  | ✗ |
| contactPhone | contact_phone | String? | Y |  |  | ✗ |
| contactEmail | contact_email | String? | Y |  |  | ✗ |
| companyName | company_name | String? | Y |  |  | ✗ |
| notes | notes | String? | Y |  |  | ✗ |
| nextFollowUpAt | next_follow_up_at | DateTime? | Y |  |  | ✗ |
| lastContactAt | last_contact_at | DateTime? | Y |  |  | ✗ |
| lostReason | lost_reason | String? | Y |  |  | ✗ |
| qualifiedAt | qualified_at | DateTime? | Y |  |  | ✗ |
| convertedAt | converted_at | DateTime? | Y |  |  | ✗ |
| convertedById | converted_by_id | String? | Y |  | LREF | ✗ |
| lostAt | lost_at | DateTime? | Y |  |  | ✗ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✗ |
| account | account | Account? | Y |  | FK→Account(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([status, createdAt])`; `@@index([repId, status])`; `@@index([nextFollowUpAt])`

### SupportTicket → `support_tickets`
`apps/crm/prisma/schema.prisma:473`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| ticketNumber | ticket_number | String | N |  | U | ✓ |
| accountId | account_id | String | N |  | FK-col | ✓ |
| visitId | visit_id | String? | Y |  | FK-col | ✓ |
| contactName | contact_name | String | N |  |  | ✓ |
| contactPhone | contact_phone | String? | Y |  |  | ✓ |
| subject | subject | String | N |  |  | ✓ |
| description | description | String | N |  |  | ✓ |
| category | category | TicketCategory | N | DELIVERY_DELAY |  | ✓ |
| customCategoryId | custom_category_id | String? | Y |  | FK-col | ✓ |
| partyDetails | party_details | String? | Y |  |  | ✓ |
| priority | priority | TicketPriority | N | MEDIUM |  | ✓ |
| status | status | TicketStatus | N | OPEN |  | ✓ |
| assignedAgentId | assigned_agent_id | String? | Y |  | LREF | ✓ |
| targetResolutionHours | target_resolution_hours | Int | N | 24 |  | ✓ |
| slaDueAt | sla_due_at | DateTime | N |  |  | ✓ |
| resolvedAt | resolved_at | DateTime? | Y |  |  | ✓ |
| isSlaBreached | is_sla_breached | Boolean | N | false |  | ✓ |
| resolutionNotes | resolution_notes | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| account | account | Account | N |  | FK→Account(id) onDelete=default | ✓ |
| visit | visit | Visit? | Y |  | FK→Visit(id) onDelete=SetNull | ✓ |
| customCategory | customCategory | SupportCategory? | Y |  | FK→SupportCategory(id) onDelete=SetNull | ✓ |

Indexes/constraints: `@@index([accountId])`; `@@index([visitId])`; `@@index([status])`; `@@index([priority])`; `@@index([isSlaBreached])`

### CustomerContact → `customer_contacts`
`apps/crm/prisma/schema.prisma:519`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| accountId | account_id | String | N |  | FK-col | ✓ |
| name | name | String | N |  |  | ✓ |
| phone | phone | String | N |  |  | ✓ |
| role | role | String | N |  |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| account | account | Account | N |  | FK→Account(id) onDelete=Restrict | ✓ |

Indexes/constraints: `@@index([accountId])`

### SupportCategory → `support_categories`
`apps/crm/prisma/schema.prisma:539`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| name | name | String | N |  | U | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |

### TicketParticipant → `ticket_participants`
`apps/crm/prisma/schema.prisma:553`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| ticketId | ticket_id | String | N |  | FK-col | ✓ |
| userId | user_id | String | N |  | LREF | ✓ |
| role | role | String | N |  |  | ✓ |
| ticket | ticket | SupportTicket | N |  | FK→SupportTicket(id) onDelete=Restrict | ✓ |

Indexes/constraints: `@@unique([ticketId, userId, role])`; `@@index([userId])`

### AuditLog → `audit_logs`
`apps/crm/prisma/schema.prisma:571`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| userId | user_id | String? | Y |  | LREF | ✓ |
| action | action | String | N |  |  | ✓ |
| entity | entity | String | N |  |  | ✓ |
| entityId | entity_id | String? | Y |  | LREF | ✓ |
| before | before | Json? | Y |  |  | ✓ |
| after | after | Json? | Y |  |  | ✓ |
| reasonCode | reason_code | String? | Y |  |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| ipAddress | ip_address | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([userId])`; `@@index([entity])`; `@@index([createdAt])`

### CustomerAddress → `customer_addresses`
`apps/crm/prisma/schema.prisma:591`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| accountId | account_id | String | N |  | FK-col | ✓ |
| label | label | String | N |  |  | ✓ |
| isPrimary | is_primary | Boolean | N | false |  | ✓ |
| governorate | governorate | String | N |  |  | ✓ |
| city | city | String | N |  |  | ✓ |
| district | district | String? | Y |  |  | ✓ |
| street | street | String? | Y |  |  | ✓ |
| building | building | String? | Y |  |  | ✓ |
| floor | floor | String? | Y |  |  | ✓ |
| landmark | landmark | String? | Y |  |  | ✓ |
| fullAddress | full_address | String | N |  |  | ✓ |
| latitude | latitude | Decimal? @db.Decimal(9,6) | Y |  |  | ✓ |
| longitude | longitude | Decimal? @db.Decimal(9,6) | Y |  |  | ✓ |
| createdBy | created_by | String | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| account | account | Account | N |  | FK→Account(id) onDelete=Restrict | ✓ |

Indexes/constraints: `@@index([accountId])`

### CustomerNote → `customer_notes`
`apps/crm/prisma/schema.prisma:614`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| accountId | account_id | String | N |  | FK-col | ✓ |
| content | content | String | N |  |  | ✓ |
| createdBy | created_by | String | N |  |  | ✓ |
| updatedBy | updated_by | String | N |  |  | ✓ |
| version | version | Int | N | 1 |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| account | account | Account | N |  | FK→Account(id) onDelete=Restrict | ✓ |

Indexes/constraints: `@@index([accountId, createdAt])`

### CustomerCreationRequest → `customer_creation_requests`
`apps/crm/prisma/schema.prisma:627`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | ✓ |
| actorId | actor_id | String | N |  | LREF | ✓ |
| payloadHash | payload_hash | String | N |  |  | ✓ |
| accountId | account_id | String | N |  | U FK-col | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| account | account | Account | N |  | FK→Account(id) onDelete=Restrict | ✓ |

### CustomerEventOutbox → `customer_event_outbox`
`apps/crm/prisma/schema.prisma:636`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | ✓ |
| topic | topic | String | N |  |  | ✓ |
| envelope | envelope | Json | N |  |  | ✓ |
| attempts | attempts | Int | N | 0 |  | ✓ |
| availableAt | available_at | DateTime | N | now() |  | ✓ |
| lockedUntil | locked_until | DateTime? | Y |  |  | ✓ |
| lockToken | lock_token | String? | Y |  |  | ✓ |
| sentAt | sent_at | DateTime? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

### VisitRescheduleRequest → `visit_reschedule_requests`
`apps/crm/prisma/schema.prisma:649`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| originalVisit | originalVisit | Visit | N |  | FK→Visit(id) onDelete=NoAction | ✓ |
| replacementVisit | replacementVisit | Visit? | Y |  | FK→Visit(id) onDelete=NoAction | ✓ |
| id | id | String | N | uuid() | PK | ✓ |
| visitId | visit_id | String | N |  | U FK-col | ✓ |
| proposedAt | proposed_at | DateTime | N |  |  | ✓ |
| reason | reason | String | N |  |  | ✓ |
| status | status | String | N | "PENDING" |  | ✓ |
| decidedBy | decided_by | String? | Y |  |  | ✓ |
| decidedAt | decided_at | DateTime? | Y |  |  | ✓ |
| replacementId | replacement_id | String? | Y |  | U FK-col | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

### FieldProposal → `field_proposals`
`apps/crm/prisma/schema.prisma:663`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| visit | visit | Visit | N |  | FK→Visit(id) onDelete=NoAction | ✓ |
| account | account | Account | N |  | FK→Account(id) onDelete=NoAction | ✓ |
| id | id | String | N |  | PK | ✓ |
| visitId | visit_id | String | N |  | FK-col | ✓ |
| accountId | account_id | String | N |  | FK-col | ✓ |
| kind | kind | String | N |  |  | ✓ |
| status | status | String | N | "PENDING_REVIEW" |  | ✓ |
| payload | payload | Json | N |  |  | ✓ |
| version | version | Int | N | 1 |  | ✓ |
| createdBy | created_by | String | N |  |  | ✓ |
| reviewedBy | reviewed_by | String? | Y |  |  | ✓ |
| reviewNote | review_note | String? | Y |  |  | ✓ |
| buyerConfirmation | buyer_confirmation | String? | Y |  |  | ✓ |
| convertedId | converted_id | String? | Y |  | LREF | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@index([status,createdAt])`; `@@index([visitId])`

#### Enums (crm)
| Enum | Values | B? |
|---|---|---|
| AccountType | PHARMACY, DOCTOR, CENTER, HOSPITAL, DISTRIBUTOR, CHAINS | ✓ |
| VisitOutcome | ORDER_PLACED, FOLLOW_UP, NO_INTEREST, SAMPLE_LEFT | ✓ |
| FieldVisitStatus | PLANNED, IN_PROGRESS, COMPLETED, MISSED, CANCELLED, RESCHEDULED | ✓ |
| VisitPurpose | SALES, FOLLOW_UP, COLLECTION, NEW_PRODUCT, COMPLAINT, RELATIONSHIP, DELIVERY_ISSUE, OTHER | ✓ |
| VisitPriority | HIGH, NORMAL, LOW | ✓ |
| VisitResult | ORDER_CREATED, FOLLOW_UP_REQUIRED, CUSTOMER_INTERESTED, NO_ORDER, COMPLAINT, CUSTOMER_UNAVAILABLE, REJECTED, RESCHEDULED | ✓ |
| VisitPlanStatus | DRAFT, PUBLISHED, IN_PROGRESS, COMPLETED, CANCELLED | ✓ |
| CustomerAssignmentRole | PRIMARY, BACKUP | ✓ |
| FollowUpStatus | OPEN, COMPLETED, CANCELLED | ✓ |
| FollowUpPurpose | CALL_CUSTOMER, SEND_QUOTE, CONFIRM_ORDER, COLLECT_PAYMENT, RESOLVE_COMPLAINT, GENERAL | ✓ |
| CustomerInteractionType | CALL | ✓ |
| CallOutcome | ANSWERED, NO_ANSWER, BUSY, CALLBACK_REQUESTED, WRONG_NUMBER, OTHER | ✓ |
| ProductInterest | HIGH, MEDIUM, LOW | ✓ |
| TargetPeriod | DAILY, WEEKLY, MONTHLY, QUARTERLY | ✓ |
| LeadStatus | NEW, QUALIFIED, CONVERTED, LOST | ✓ |
| TicketCategory | DAMAGED_COLD_CHAIN, DELIVERY_DELAY, SHORTAGE_EXPIRY, BILLING_INVOICE_DISPUTE, PRODUCT_QUALITY_INQUIRY, CUSTOM | ✓ |
| TicketPriority | CRITICAL, HIGH, MEDIUM, LOW | ✓ |
| TicketStatus | OPEN, IN_PROGRESS, WAITING_CUSTOMER, RESOLVED, CLOSED | ✓ |

## خدمة `iam` — DB `nile_iam`
المصدر: `apps/iam/prisma/schema.prisma`

### User → `users`
`apps/iam/prisma/schema.prisma:41`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| email | email | String | N |  | U | ✓ |
| phone | phone | String? | Y |  | U | ✓ |
| passwordHash | password_hash | String | N |  |  | ✓ |
| fullName | full_name | String | N |  |  | ✓ |
| status | status | UserStatus | N | ACTIVE |  | ✓ |
| mfaEnabled | mfa_enabled | Boolean | N | false |  | ✓ |
| lastLogin | last_login | DateTime? | Y |  |  | ✓ |
| mustChangePassword | must_change_password | Boolean | N | true |  | ✓ |
| failedLoginAttempts | failed_login_attempts | Int | N | 0 |  | ✓ |
| lockedUntil | locked_until | DateTime? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| createdById | created_by | String? | Y |  | LREF | ✓ |
| marketingOptIn | marketing_opt_in | Boolean | N | false |  | ✓ |

### Role → `roles`
`apps/iam/prisma/schema.prisma:74`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| name | name | String | N |  | U | ✓ |
| description | description | String? | Y |  |  | ✓ |
| isSystemRole | is_system_role | Boolean | N | false |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

### Permission → `permissions`
`apps/iam/prisma/schema.prisma:87`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | String | N |  | U | ✓ |
| domain | domain | String | N |  |  | ✓ |
| module | module | String | N |  |  | ✓ |
| action | action | String | N |  |  | ✓ |
| description | description | String? | Y |  |  | ✓ |

### UserRole → `user_roles`
`apps/iam/prisma/schema.prisma:101`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| userId | user_id | String | N |  | FK-col | ✓ |
| roleId | role_id | String | N |  | FK-col | ✓ |
| assignedAt | assigned_at | DateTime | N | now() |  | ✓ |
| assignedBy | assigned_by | String? | Y |  |  | ✓ |
| user | user | User | N |  | FK→User(id) onDelete=Cascade | ✓ |
| role | role | Role | N |  | FK→Role(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@id([userId, roleId])`

### RolePermission → `role_permissions`
`apps/iam/prisma/schema.prisma:114`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| roleId | role_id | String | N |  | FK-col | ✓ |
| permissionId | permission_id | String | N |  | FK-col | ✓ |
| isGranted | is_granted | Boolean | N | true |  | ✓ |
| role | role | Role | N |  | FK→Role(id) onDelete=Cascade | ✓ |
| permission | permission | Permission | N |  | FK→Permission(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@id([roleId, permissionId])`

### Session → `sessions`
`apps/iam/prisma/schema.prisma:126`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| userId | user_id | String | N |  | FK-col | ✓ |
| refreshTokenHash | refresh_token_hash | String | N |  |  | ✓ |
| previousRefreshTokenHash | previous_refresh_token_hash | String? | Y |  |  | ✓ |
| refreshRotatedAt | refresh_rotated_at | DateTime? | Y |  |  | ✓ |
| idleExpiresAt | idle_expires_at | DateTime? | Y |  |  | ✓ |
| lastActivityAt | last_activity_at | DateTime? | Y |  |  | ✓ |
| deviceInfo | device_info | String? | Y |  |  | ✓ |
| ipAddress | ip_address | String? | Y |  |  | ✓ |
| expiresAt | expires_at | DateTime | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| revokedAt | revoked_at | DateTime? | Y |  |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| user | user | User | N |  | FK→User(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([userId])`

### AuditLog → `audit_logs`
`apps/iam/prisma/schema.prisma:151`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| userId | user_id | String? | Y |  | FK-col | ✓ |
| action | action | String | N |  |  | ✓ |
| entity | entity | String | N |  |  | ✓ |
| entityId | entity_id | String? | Y |  | LREF | ✓ |
| before | before | Json? | Y |  |  | ✓ |
| after | after | Json? | Y |  |  | ✓ |
| reasonCode | reason_code | String? | Y |  |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| ipAddress | ip_address | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| user | user | User? | Y |  | FK→User(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([userId])`; `@@index([entity])`; `@@index([createdAt])`

### ElectronicSignature → `electronic_signatures`
`apps/iam/prisma/schema.prisma:173`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| userId | user_id | String | N |  | FK-col | ✓ |
| entityType | entity_type | String | N |  |  | ✓ |
| entityId | entity_id | String? | Y |  | LREF | ✓ |
| meaning | meaning | String | N |  |  | ✓ |
| signatureHash | signature_hash | String | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| user | user | User | N |  | FK→User(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([userId])`; `@@index([entityType, entityId])`

### Notification → `notifications`
`apps/iam/prisma/schema.prisma:189`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| recipientId | recipient_id | String | N |  | FK-col | ✓ |
| recipient | recipient | User | N |  | FK→User(id) onDelete=Cascade | ✓ |
| channel | channel | String | N | "IN_APP" |  | ✓ |
| category | category | NotificationCategory | N | TRANSACTIONAL |  | ✓ |
| type | type | String | N |  |  | ✓ |
| title | title | String | N |  |  | ✓ |
| body | body | String? | Y |  |  | ✓ |
| link | link | String? | Y |  |  | ✓ |
| status | status | NotificationStatus | N | QUEUED |  | ✓ |
| readAt | read_at | DateTime? | Y |  |  | ✓ |
| sentAt | sent_at | DateTime? | Y |  |  | ✓ |
| retryCount | retry_count | Int | N | 0 |  | ✓ |
| lastError | last_error | String? | Y |  |  | ✓ |
| providerMessageId | provider_message_id | String? | Y |  | LREF | ✓ |
| createdById | created_by_id | String? | Y |  | LREF | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([recipientId, readAt])`; `@@index([recipientId, createdAt])`; `@@index([status])`

### ProcessedEvent → `processed_events`
`apps/iam/prisma/schema.prisma:221`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| eventId | event_id | String | N |  | PK | ✓ |
| processedAt | processed_at | DateTime | N | now() |  | ✓ |

### SecurityPolicy → `security_policies`
`apps/iam/prisma/schema.prisma:229`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | ✓ |
| timeoutMinutes | timeout_minutes | Int | N | 15 |  | ✓ |
| version | version | Int | N | 0 |  | ✓ |
| updatedBy | updated_by | String? | Y |  |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

### WorkspaceDraft → `workspace_drafts`
`apps/iam/prisma/schema.prisma:239`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| ownerId | owner_id | String | N |  | LREF | ✓ |
| namespace | namespace | String | N |  |  | ✓ |
| key | key | String | N |  |  | ✓ |
| payload | payload | Json | N |  |  | ✓ |
| version | version | Int | N | 1 |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@unique([ownerId, namespace, key])`; `@@index([ownerId, updatedAt])`

### AiProviderSetting → `ai_provider_settings`
`apps/iam/prisma/schema.prisma:253`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N |  | PK | ✓ |
| provider | provider | String | N |  |  | ✓ |
| model | model | String | N |  |  | ✓ |
| enabled | enabled | Boolean | N | false |  | ✓ |
| keyCiphertext | key_ciphertext | String? | Y |  |  | ✓ |
| version | version | Int | N | 1 |  | ✓ |
| updatedBy | updated_by | String | N |  |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

#### Enums (iam)
| Enum | Values | B? |
|---|---|---|
| NotificationStatus | QUEUED, SENDING, SENT, FAILED | ✓ |
| NotificationCategory | TRANSACTIONAL, MARKETING | ✓ |
| UserStatus | ACTIVE, SUSPENDED, DELETED | ✓ |

## خدمة `incentives` — DB `nile_incentives`
المصدر: `apps/incentives/prisma/schema.prisma`

### RuleSet → `rule_sets`
`apps/incentives/prisma/schema.prisma:27`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| version | version | Int | N |  | U | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| tiers | tiers | Json | N |  |  | ✓ |
| bonusRules | bonus_rules | Json | N |  |  | ✓ |
| isActive | is_active | Boolean | N | false |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| activatedAt | activated_at | DateTime? | Y |  |  | ✓ |

### ProcessedEvent → `processed_events`
`apps/incentives/prisma/schema.prisma:46`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| eventId | event_id | String | N |  | PK | ✓ |
| processedAt | processed_at | DateTime | N | now() |  | ✓ |
| ledgerId | ledger_id | String? | Y |  | LREF | ✓ |

### IncentiveLedger → `incentive_ledger`
`apps/incentives/prisma/schema.prisma:57`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| repId | rep_id | String | N |  | LREF | ✓ |
| sourceEventId | source_event_id | String | N |  | U LREF | ✓ |
| paymentId | payment_id | String? | Y |  | LREF | ✓ |
| orderId | order_id | String? | Y |  | LREF | ✓ |
| accountId | account_id | String? | Y |  | LREF | ✓ |
| period | period | String | N |  |  | ✓ |
| baseAmount | base_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| commissionAmount | commission_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| tierApplied | tier_applied | String | N |  |  | ✓ |
| collectionRate | collection_rate | Decimal @db.Decimal(5, 4) | N |  |  | ✓ |
| bonusPct | bonus_pct | Decimal @db.Decimal(5, 2) | N | 0 |  | ✓ |
| bonusAmount | bonus_amount | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| totalIncentive | total_incentive | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| ruleSetVersion | rule_set_version | Int | N |  |  | ✓ |
| status | status | IncentiveStatus | N | PENDING |  | ✓ |
| approvedBy | approved_by | String? | Y |  |  | ✓ |
| decidedAt | decided_at | DateTime? | Y |  |  | ✓ |
| reversalReason | reversal_reason | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| ruleSet | ruleSet | RuleSet | N |  | FK→RuleSet(version) onDelete=default | ✓ |

Indexes/constraints: `@@index([repId])`; `@@index([period])`; `@@index([status])`; `@@index([paymentId])`

### RepScore → `rep_scores`
`apps/incentives/prisma/schema.prisma:95`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| repId | rep_id | String | N |  | LREF | ✓ |
| period | period | String | N |  |  | ✓ |
| totalSales | total_sales | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| collected | collected | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| incentiveEarned | incentive_earned | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| collectionRate | collection_rate | Decimal @db.Decimal(5, 4) | N | 0 |  | ✓ |
| efficiencyScore | efficiency_score | Decimal @db.Decimal(8, 2) | N | 0 |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@unique([repId, period])`; `@@index([period])`

### AuditLog → `audit_logs`
`apps/incentives/prisma/schema.prisma:112`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| userId | user_id | String? | Y |  | LREF | ✓ |
| action | action | String | N |  |  | ✓ |
| entity | entity | String | N |  |  | ✓ |
| entityId | entity_id | String? | Y |  | LREF | ✓ |
| before | before | Json? | Y |  |  | ✓ |
| after | after | Json? | Y |  |  | ✓ |
| reasonCode | reason_code | String? | Y |  |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| ipAddress | ip_address | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([userId])`; `@@index([entity])`; `@@index([createdAt])`

#### Enums (incentives)
| Enum | Values | B? |
|---|---|---|
| IncentiveStatus | PENDING, APPROVED, PAID, REVERSED | ✓ |

## خدمة `inventory` — DB `nile_inventory`
المصدر: `apps/inventory/prisma/schema.prisma`

### Warehouse → `warehouses`
`apps/inventory/prisma/schema.prisma:47`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | String | N |  | U | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String | N |  |  | ✓ |
| gln | gln | String? | Y |  | U | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| transfersOut | transfersOut | Transfer[] | N |  | FK→Transfer() onDelete=default | ✓ |
| transfersIn | transfersIn | Transfer[] | N |  | FK→Transfer() onDelete=default | ✓ |

### BinLocation → `bin_locations`
`apps/inventory/prisma/schema.prisma:63`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| warehouseId | warehouse_id | String | N |  | FK-col | ✓ |
| code | code | String | N |  |  | ✓ |
| zone | zone | String? | Y |  |  | ✓ |
| warehouse | warehouse | Warehouse | N |  | FK→Warehouse(id) onDelete=default | ✓ |

Indexes/constraints: `@@unique([warehouseId, code])`

### StockBalance → `stock_balances`
`apps/inventory/prisma/schema.prisma:75`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| warehouseId | warehouse_id | String | N |  | FK-col | ✓ |
| productId | product_id | String | N |  | LREF | ✓ |
| batchId | batch_id | String | N |  | LREF | ✓ |
| ownership | ownership | StockOwnership | N | WAREHOUSE |  | ✓ |
| onHand | on_hand | Int | N | 0 |  | ✓ |
| reserved | reserved | Int | N | 0 |  | ✓ |
| expiryDate | expiry_date | DateTime | N |  |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| warehouse | warehouse | Warehouse | N |  | FK→Warehouse(id) onDelete=default | ✓ |

Indexes/constraints: `@@unique([warehouseId, batchId, ownership])`; `@@index([productId])`; `@@index([expiryDate])`

### InventoryCostLayer → `inventory_cost_layers` **(CURRENT فقط)**
`apps/inventory/prisma/schema.prisma:94`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | — |
| productId | product_id | String | N |  | LREF | — |
| batchId | batch_id | String | N |  | LREF | — |
| warehouseId | warehouse_id | String? | Y |  | LREF | — |
| quantityReceived | quantity_received | Int | N |  |  | — |
| quantityRemaining | quantity_remaining | Int | N |  |  | — |
| unitCost | unit_cost | Decimal @db.Decimal(18,4) | N |  |  | — |
| receivedAt | received_at | DateTime | N | now() |  | — |
| sourceTransactionId | source_transaction_id | String? | Y |  | LREF | — |

Indexes/constraints: `@@index([batchId, warehouseId, receivedAt])`

### InventoryTransaction → `inventory_transactions`
`apps/inventory/prisma/schema.prisma:109`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| type | type | TxnType | N |  |  | ✓ |
| productId | product_id | String | N |  | LREF | ✓ |
| batchId | batch_id | String | N |  | LREF | ✓ |
| warehouseId | warehouse_id | String? | Y |  | LREF | ✓ |
| customerId | customer_id | String? | Y |  | LREF | ✓ |
| supplierId | supplier_id | String? | Y |  | LREF | ✓ |
| quantity | quantity | Int | N |  |  | ✓ |
| unitCost | unit_cost | Decimal? @db.Decimal(18,4) | Y |  |  | ✗ |
| totalCost | total_cost | Decimal? @db.Decimal(18,2) | Y |  |  | ✗ |
| reasonCode | reason_code | String? | Y |  |  | ✓ |
| note | note | String? | Y |  |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| actorId | actor_id | String | N |  | LREF | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| reversed | reversed | Boolean | N | false |  | ✓ |
| reversedAt | reversed_at | DateTime? | Y |  |  | ✓ |
| reversalReason | reversal_reason | String? | Y |  |  | ✓ |
| reversedBy | reversed_by | String? | Y |  |  | ✓ |
| reversalOfId | reversal_of_id | String? | Y |  | LREF | ✓ |

Indexes/constraints: `@@index([batchId])`; `@@index([customerId])`; `@@index([createdAt])`; `@@index([type, createdAt])`

### BlockedBatch → `blocked_batches`
`apps/inventory/prisma/schema.prisma:153`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| batchId | batch_id | String | N |  | U LREF | ✓ |
| recallId | recall_id | String? | Y |  | LREF | ✓ |
| reason | reason | String | N |  |  | ✓ |
| blockedAt | blocked_at | DateTime | N | now() |  | ✓ |

### AdjustmentRequest → `adjustment_requests`
`apps/inventory/prisma/schema.prisma:169`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| warehouseId | warehouse_id | String | N |  | LREF | ✓ |
| productId | product_id | String | N |  | LREF | ✓ |
| batchId | batch_id | String | N |  | LREF | ✓ |
| direction | direction | String | N |  |  | ✓ |
| quantity | quantity | Int | N |  |  | ✓ |
| reasonCode | reason_code | String | N |  |  | ✓ |
| note | note | String? | Y |  |  | ✓ |
| status | status | AdjustmentRequestStatus | N | PENDING |  | ✓ |
| requestedBy | requested_by | String | N |  |  | ✓ |
| requestedAt | requested_at | DateTime | N | now() |  | ✓ |
| decidedBy | decided_by | String? | Y |  |  | ✓ |
| decidedAt | decided_at | DateTime? | Y |  |  | ✓ |
| decisionNote | decision_note | String? | Y |  |  | ✓ |
| resultingTransactionId | resulting_transaction_id | String? | Y |  | LREF | ✓ |

Indexes/constraints: `@@index([status])`

### InventoryReservation → `inventory_reservations`
`apps/inventory/prisma/schema.prisma:190`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| orderId | order_id | String | N |  | LREF | ✓ |
| productId | product_id | String | N |  | LREF | ✓ |
| batchId | batch_id | String | N |  | LREF | ✓ |
| warehouseId | warehouse_id | String? | Y |  | LREF | ✓ |
| customerId | customer_id | String? | Y |  | LREF | ✓ |
| quantity | quantity | Int | N |  |  | ✓ |
| expiryDate | expiry_date | DateTime? | Y |  |  | ✓ |
| source | source | StockOwnership | N |  |  | ✓ |
| isReleased | is_released | Boolean | N | false |  | ✓ |
| issuedAt | issued_at | DateTime? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([orderId])`

### ProcessedEvent → `processed_events`
`apps/inventory/prisma/schema.prisma:214`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| eventId | event_id | String | N |  | PK | ✓ |
| processedAt | processed_at | DateTime | N | now() |  | ✓ |

### Transfer → `transfers`
`apps/inventory/prisma/schema.prisma:232`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| sourceWarehouseId | source_warehouse_id | String | N |  | FK-col | ✓ |
| destWarehouseId | dest_warehouse_id | String | N |  | FK-col | ✓ |
| productId | product_id | String | N |  | LREF | ✓ |
| batchId | batch_id | String | N |  | LREF | ✓ |
| quantity | quantity | Int | N |  |  | ✓ |
| note | note | String? | Y |  |  | ✓ |
| idempotencyKey | idempotency_key | String | N |  | U | ✓ |
| actorId | actor_id | String | N |  | LREF | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| sourceWarehouse | sourceWarehouse | Warehouse | N |  | FK→Warehouse(id) onDelete=default | ✓ |
| destWarehouse | destWarehouse | Warehouse | N |  | FK→Warehouse(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([batchId])`; `@@index([createdAt])`

### AuditLog → `audit_logs`
`apps/inventory/prisma/schema.prisma:258`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| userId | user_id | String? | Y |  | LREF | ✓ |
| action | action | String | N |  |  | ✓ |
| entity | entity | String | N |  |  | ✓ |
| entityId | entity_id | String? | Y |  | LREF | ✓ |
| before | before | Json? | Y |  |  | ✓ |
| after | after | Json? | Y |  |  | ✓ |
| reasonCode | reason_code | String? | Y |  |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| ipAddress | ip_address | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([userId])`; `@@index([entity])`; `@@index([createdAt])`

### ConsignmentAgreement → `consignment_agreements`
`apps/inventory/prisma/schema.prisma:280`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| customerId | customer_id | String | N |  | LREF | ✓ |
| customerName | customer_name | String | N |  |  | ✓ |
| startDate | start_date | DateTime | N | now() |  | ✓ |
| endDate | end_date | DateTime? | Y |  |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |

Indexes/constraints: `@@index([customerId])`

### ConsignmentStock → `consignment_stock`
`apps/inventory/prisma/schema.prisma:295`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| agreementId | agreement_id | String | N |  | FK-col | ✓ |
| customerId | customer_id | String | N |  | LREF | ✓ |
| productId | product_id | String | N |  | LREF | ✓ |
| batchId | batch_id | String | N |  | LREF | ✓ |
| expiryDate | expiry_date | DateTime | N |  |  | ✓ |
| ownedQty | owned_qty | Int | N | 0 |  | ✓ |
| availableQty | available_qty | Int | N | 0 |  | ✓ |
| consumedQty | consumed_qty | Int | N | 0 |  | ✓ |
| returnedQty | returned_qty | Int | N | 0 |  | ✓ |
| lostQty | lost_qty | Int | N | 0 |  | ✓ |
| heldQty | held_qty | Int | N | 0 |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| agreement | agreement | ConsignmentAgreement | N |  | FK→ConsignmentAgreement(id) onDelete=default | ✓ |

Indexes/constraints: `@@unique([customerId, batchId])`; `@@index([productId])`; `@@index([expiryDate])`

### JobRun → `job_runs`
`apps/inventory/prisma/schema.prisma:327`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| name | name | String | N |  |  | ✓ |
| status | status | JobRunStatus | N |  |  | ✓ |
| startedAt | started_at | DateTime | N |  |  | ✓ |
| finishedAt | finished_at | DateTime? | Y |  |  | ✓ |
| affected | affected | Int? | Y |  |  | ✓ |
| error | error | String? | Y |  |  | ✓ |
| triggeredBy | triggered_by | String | N | "cron" |  | ✓ |

Indexes/constraints: `@@index([name, startedAt])`

### InventoryOutboxEvent → `inventory_outbox_events` **(CURRENT فقط)**
`apps/inventory/prisma/schema.prisma:342`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | — |
| topic | topic | String | N |  |  | — |
| eventId | event_id | String | N |  | U LREF | — |
| envelope | envelope | Json | N |  |  | — |
| publishedAt | published_at | DateTime? | Y |  |  | — |
| processingUntil | processing_until | DateTime? | Y |  |  | — |
| attempts | attempts | Int | N | 0 |  | — |
| lastError | last_error | String? | Y |  |  | — |
| createdAt | created_at | DateTime | N | now() |  | — |

Indexes/constraints: `@@index([publishedAt, createdAt])`; `@@index([processingUntil], map: "inventory_outbox_events_processing_until_idx")`

#### Enums (inventory)
| Enum | Values | B? |
|---|---|---|
| TxnType | RECEIPT, ISSUE, TRANSFER, ADJUSTMENT, CONSIGN_OUT, CONSIGN_CONSUME, CONSIGN_RETURN, RETURN, SUPPLIER_RETURN, CONSIGN_WRITE_OFF, CONSIGN_HOLD, QUARANTINE_IN, QUARANTINE_RELEASE, QUARANTINE_HOLD, QUARANTINE_REJECT | ✓ |
| StockOwnership | WAREHOUSE, CONSIGNMENT, QUARANTINE, DAMAGED | ✓ |
| AdjustmentRequestStatus | PENDING, APPROVED, REJECTED | ✓ |
| JobRunStatus | RUNNING, SUCCESS, FAILED, SKIPPED_LOCKED | ✓ |

## خدمة `organization` — DB `nile_organization`
المصدر: `apps/organization/prisma/schema.prisma`

### Department → `departments`
`apps/organization/prisma/schema.prisma:16`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| name | name | String | N |  | U | ✓ |
| costCenter | cost_center | String? | Y |  |  | ✓ |
| parentId | parent_id | String? | Y |  | FK-col | ✓ |
| managerId | manager_id | String? | Y |  | LREF | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| parent | parent | Department? | Y |  | FK→Department(id) onDelete=default | ✓ |
| children | children | Department[] | N |  | FK→Department() onDelete=default | ✓ |

Indexes/constraints: `@@index([parentId])`

### JobTitle → `job_titles`
`apps/organization/prisma/schema.prisma:36`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| name | name | String | N |  |  | ✓ |
| gradeLevel | grade_level | String? | Y |  |  | ✓ |
| departmentId | department_id | String? | Y |  | FK-col | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| department | department | Department? | Y |  | FK→Department(id) onDelete=default | ✓ |

Indexes/constraints: `@@unique([name, departmentId])`

### Region → `regions`
`apps/organization/prisma/schema.prisma:51`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| name | name | String | N |  |  | ✓ |
| countryCode | country_code | String | N |  |  | ✓ |
| city | city | String? | Y |  |  | ✓ |
| district | district | String? | Y |  |  | ✓ |

### Branch → `branches`
`apps/organization/prisma/schema.prisma:64`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| name | name | String | N |  |  | ✓ |
| address | address | String? | Y |  |  | ✓ |
| regionId | region_id | String? | Y |  | FK-col | ✓ |
| gln | gln | String? | Y |  | U | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| region | region | Region? | Y |  | FK→Region(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([regionId])`

### Employee → `employees`
`apps/organization/prisma/schema.prisma:94`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| employeeCode | employee_code | String | N |  | U | ✓ |
| fullName | full_name | String | N |  |  | ✓ |
| phone | phone | String? | Y |  |  | ✓ |
| email | email | String? | Y |  |  | ✓ |
| departmentId | department_id | String? | Y |  | FK-col | ✓ |
| jobTitleId | job_title_id | String? | Y |  | FK-col | ✓ |
| branchId | branch_id | String? | Y |  | FK-col | ✓ |
| managerId | manager_id | String? | Y |  | FK-col | ✓ |
| status | status | EmploymentStatus | N | ACTIVE |  | ✓ |
| hireDate | hire_date | DateTime | N |  |  | ✓ |
| terminationDate | termination_date | DateTime? | Y |  |  | ✓ |
| linkedUserId | linked_user_id | String? | Y |  | U LREF | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| department | department | Department? | Y |  | FK→Department(id) onDelete=default | ✓ |
| jobTitle | jobTitle | JobTitle? | Y |  | FK→JobTitle(id) onDelete=default | ✓ |
| branch | branch | Branch? | Y |  | FK→Branch(id) onDelete=default | ✓ |
| manager | manager | Employee? | Y |  | FK→Employee(id) onDelete=default | ✓ |
| reports | reports | Employee[] | N |  | FK→Employee() onDelete=default | ✓ |

Indexes/constraints: `@@index([departmentId])`; `@@index([jobTitleId])`; `@@index([branchId])`; `@@index([managerId])`; `@@index([status])`

### AttendanceRecord → `attendance_records`
`apps/organization/prisma/schema.prisma:163`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| employeeId | employee_id | String | N |  | FK-col | ✓ |
| date | date | DateTime | N |  |  | ✓ |
| checkIn | check_in | DateTime? | Y |  |  | ✓ |
| checkOut | check_out | DateTime? | Y |  |  | ✓ |
| workMinutes | work_minutes | Int | N | 0 |  | ✓ |
| lateMinutes | late_minutes | Int | N | 0 |  | ✓ |
| overtimeMinutes | overtime_minutes | Int | N | 0 |  | ✓ |
| status | status | AttendanceStatus | N | PRESENT |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| employee | employee | Employee | N |  | FK→Employee(id) onDelete=default | ✓ |

Indexes/constraints: `@@unique([employeeId, date])`; `@@index([employeeId])`; `@@index([date])`; `@@index([status])`

### LeaveBalance → `leave_balances`
`apps/organization/prisma/schema.prisma:185`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| employeeId | employee_id | String | N |  | FK-col | ✓ |
| fiscalYear | fiscal_year | Int | N |  |  | ✓ |
| annualTotal | annual_total | Int | N | 21 |  | ✓ |
| annualUsed | annual_used | Int | N | 0 |  | ✓ |
| casualTotal | casual_total | Int | N | 6 |  | ✓ |
| casualUsed | casual_used | Int | N | 0 |  | ✓ |
| sickTotal | sick_total | Int | N | 30 |  | ✓ |
| sickUsed | sick_used | Int | N | 0 |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| employee | employee | Employee | N |  | FK→Employee(id) onDelete=default | ✓ |

Indexes/constraints: `@@unique([employeeId, fiscalYear])`; `@@index([employeeId])`

### LeaveRequest → `leave_requests`
`apps/organization/prisma/schema.prisma:205`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| employeeId | employee_id | String | N |  | FK-col | ✓ |
| leaveType | leave_type | LeaveType | N |  |  | ✓ |
| startDate | start_date | DateTime | N |  |  | ✓ |
| endDate | end_date | DateTime | N |  |  | ✓ |
| daysCount | days_count | Int | N |  |  | ✓ |
| reason | reason | String | N |  |  | ✓ |
| status | status | LeaveStatus | N | PENDING |  | ✓ |
| approvedBy | approved_by | String? | Y |  |  | ✓ |
| approvedAt | approved_at | DateTime? | Y |  |  | ✓ |
| rejectionReason | rejection_reason | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| employee | employee | Employee | N |  | FK→Employee(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([employeeId])`; `@@index([status])`

### EmploymentContract → `employment_contracts`
`apps/organization/prisma/schema.prisma:248`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| contractNumber | contract_number | String | N |  | U | ✓ |
| employeeId | employee_id | String | N |  | FK-col | ✓ |
| type | type | ContractType | N | FULL_TIME |  | ✓ |
| status | status | ContractStatus | N | DRAFT |  | ✓ |
| startDate | start_date | DateTime | N |  |  | ✓ |
| endDate | end_date | DateTime? | Y |  |  | ✓ |
| probationEndDate | probation_end_date | DateTime? | Y |  |  | ✓ |
| baseSalary | base_salary | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| currency | currency | String | N | "EGP" |  | ✓ |
| workingHoursPerWeek | working_hours_per_week | Int? | Y | 40 |  | ✓ |
| jobTitleId | job_title_id | String? | Y |  | FK-col | ✓ |
| departmentId | department_id | String? | Y |  | FK-col | ✓ |
| terms | terms | String? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| documentUrl | document_url | String? | Y |  |  | ✓ |
| signedAt | signed_at | DateTime? | Y |  |  | ✓ |
| signedByEmployee | signed_by_employee | Boolean | N | false |  | ✓ |
| signedByEmployer | signed_by_employer | Boolean | N | false |  | ✓ |
| terminationDate | termination_date | DateTime? | Y |  |  | ✓ |
| terminationReason | termination_reason | String? | Y |  |  | ✓ |
| previousContractId | previous_contract_id | String? | Y |  | FK-col | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| employee | employee | Employee | N |  | FK→Employee(id) onDelete=default | ✓ |
| jobTitle | jobTitle | JobTitle? | Y |  | FK→JobTitle(id) onDelete=default | ✓ |
| department | department | Department? | Y |  | FK→Department(id) onDelete=default | ✓ |
| previousContract | previousContract | EmploymentContract? | Y |  | FK→EmploymentContract(id) onDelete=default | ✓ |
| renewals | renewals | EmploymentContract[] | N |  | FK→EmploymentContract() onDelete=default | ✓ |

Indexes/constraints: `@@index([employeeId])`; `@@index([status])`; `@@index([startDate])`; `@@index([endDate])`

### RepCoverage → `rep_coverages` **(CURRENT فقط)**
`apps/organization/prisma/schema.prisma:287`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | — |
| employeeId | employee_id | String | N |  | FK-col | — |
| areaName | area_name | String | N |  |  | — |
| notes | notes | String? | Y |  |  | — |
| isActive | is_active | Boolean | N | true |  | — |
| createdAt | created_at | DateTime | N | now() |  | — |
| updatedAt | updated_at | DateTime | N |  |  | — |
| employee | employee | Employee | N |  | FK→Employee(id) onDelete=Restrict | — |

Indexes/constraints: `@@unique([employeeId, areaName])`; `@@index([employeeId, isActive])`; `@@index([areaName, isActive])`

### Territory → `territories`
`apps/organization/prisma/schema.prisma:304`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| name | name | String | N |  | U | ✓ |
| regionId | region_id | String? | Y |  | FK-col | ✓ |
| assignedRepId | assigned_rep_id | String? | Y |  | LREF | ✓ |
| gln | gln | String? | Y |  | U | ✓ |
| boundaryCoords | boundary_coords | Json? | Y |  |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| region | region | Region? | Y |  | FK→Region(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([regionId])`

### CompensationProfile → `compensation_profiles`
`apps/organization/prisma/schema.prisma:369`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| employeeId | employee_id | String | N |  | FK-col | ✓ |
| frequency | frequency | CompensationFrequency | N | MONTHLY |  | ✓ |
| baseSalary | base_salary | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| currency | currency | String | N | "EGP" |  | ✓ |
| effectiveFrom | effective_from | DateTime | N |  |  | ✓ |
| effectiveTo | effective_to | DateTime? | Y |  |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| employee | employee | Employee | N |  | FK→Employee(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([employeeId])`; `@@index([isActive])`

### SalaryComponent → `salary_components`
`apps/organization/prisma/schema.prisma:390`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | String | N |  | U | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String? | Y |  |  | ✓ |
| type | type | SalaryComponentType | N |  |  | ✓ |
| isTaxable | is_taxable | Boolean | N | true |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |

### EmployeeCompensationAssignment → `employee_compensation_assignments`
`apps/organization/prisma/schema.prisma:404`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| compensationProfileId | compensation_profile_id | String | N |  | FK-col | ✓ |
| salaryComponentId | salary_component_id | String | N |  | FK-col | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| isPercentage | is_percentage | Boolean | N | false |  | ✓ |
| effectiveFrom | effective_from | DateTime | N |  |  | ✓ |
| effectiveTo | effective_to | DateTime? | Y |  |  | ✓ |
| compensationProfile | compensationProfile | CompensationProfile | N |  | FK→CompensationProfile(id) onDelete=default | ✓ |
| salaryComponent | salaryComponent | SalaryComponent | N |  | FK→SalaryComponent(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([compensationProfileId])`; `@@index([salaryComponentId])`

### PayrollPeriod → `payroll_periods`
`apps/organization/prisma/schema.prisma:421`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | String | N |  | U | ✓ |
| startDate | start_date | DateTime | N |  |  | ✓ |
| endDate | end_date | DateTime | N |  |  | ✓ |
| isClosed | is_closed | Boolean | N | false |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

### PayrollRun → `payroll_runs`
`apps/organization/prisma/schema.prisma:434`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| periodId | period_id | String | N |  | FK-col | ✓ |
| status | status | PayrollRunStatus | N | DRAFT |  | ✓ |
| calculatedAt | calculated_at | DateTime? | Y |  |  | ✓ |
| calculatedBy | calculated_by | String? | Y |  |  | ✓ |
| approvedAt | approved_at | DateTime? | Y |  |  | ✓ |
| approvedBy | approved_by | String? | Y |  |  | ✓ |
| finalizedAt | finalized_at | DateTime? | Y |  |  | ✓ |
| finalizedBy | finalized_by | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| period | period | PayrollPeriod | N |  | FK→PayrollPeriod(id) onDelete=default | ✓ |

Indexes/constraints: `@@unique([periodId])`; `@@index([status])`

### PayrollEntry → `payroll_entries`
`apps/organization/prisma/schema.prisma:455`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| payrollRunId | payroll_run_id | String | N |  | FK-col | ✓ |
| employeeId | employee_id | String | N |  | FK-col | ✓ |
| baseSalary | base_salary | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| totalEarnings | total_earnings | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| totalDeductions | total_deductions | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| incentiveAmount | incentive_amount | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| netPay | net_pay | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| status | status | PayrollEntryStatus | N | DRAFT |  | ✓ |
| breakdown | breakdown | Json | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| payrollRun | payrollRun | PayrollRun | N |  | FK→PayrollRun(id) onDelete=default | ✓ |
| employee | employee | Employee | N |  | FK→Employee(id) onDelete=default | ✓ |

Indexes/constraints: `@@unique([payrollRunId, employeeId])`; `@@index([employeeId])`; `@@index([status])`

### PayrollAdjustment → `payroll_adjustments`
`apps/organization/prisma/schema.prisma:485`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| payrollEntryId | payroll_entry_id | String | N |  | FK-col | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| reason | reason | String | N |  |  | ✓ |
| type | type | PayrollAdjustmentType | N |  |  | ✓ |
| actorId | actor_id | String | N |  | LREF | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| payrollEntry | payrollEntry | PayrollEntry | N |  | FK→PayrollEntry(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([payrollEntryId])`

### PayrollApproval → `payroll_approvals`
`apps/organization/prisma/schema.prisma:500`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| payrollRunId | payroll_run_id | String | N |  | FK-col | ✓ |
| approverId | approver_id | String | N |  | LREF | ✓ |
| approved | approved | Boolean | N |  |  | ✓ |
| reason | reason | String? | Y |  |  | ✓ |
| decidedAt | decided_at | DateTime | N | now() |  | ✓ |
| payrollRun | payrollRun | PayrollRun | N |  | FK→PayrollRun(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([payrollRunId])`

### LookupTable → `lookup_tables`
`apps/organization/prisma/schema.prisma:515`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| category | category | String | N |  |  | ✓ |
| code | code | String | N |  |  | ✓ |
| labelAr | label_ar | String? | Y |  |  | ✓ |
| labelEn | label_en | String? | Y |  |  | ✓ |
| sortOrder | sort_order | Int | N | 0 |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |

Indexes/constraints: `@@unique([category, code])`; `@@index([category])`

### ExpenseClaim → `expense_claims`
`apps/organization/prisma/schema.prisma:548`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| claimNumber | claim_number | String | N |  | U | ✓ |
| employeeId | employee_id | String | N |  | LREF | ✓ |
| departmentId | department_id | String? | Y |  | LREF | ✓ |
| title | title | String | N |  |  | ✓ |
| totalAmount | total_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| status | status | ExpenseClaimStatus | N | DRAFT |  | ✓ |
| submittedAt | submitted_at | DateTime? | Y |  |  | ✓ |
| managerId | manager_id | String? | Y |  | LREF | ✓ |
| managerApprovedAt | manager_approved_at | DateTime? | Y |  |  | ✓ |
| financeApprovedAt | finance_approved_at | DateTime? | Y |  |  | ✓ |
| paidAt | paid_at | DateTime? | Y |  |  | ✓ |
| rejectionReason | rejection_reason | String? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@index([employeeId])`; `@@index([status])`

### ExpenseClaimLine → `expense_claim_lines`
`apps/organization/prisma/schema.prisma:573`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| claimId | claim_id | String | N |  | FK-col | ✓ |
| category | category | ExpenseCategory | N | TRAVEL_FUEL |  | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| expenseDate | expense_date | DateTime | N |  |  | ✓ |
| description | description | String | N |  |  | ✓ |
| receiptReference | receipt_reference | String? | Y |  |  | ✓ |
| isTaxDeductible | is_tax_deductible | Boolean | N | true |  | ✓ |
| claim | claim | ExpenseClaim | N |  | FK→ExpenseClaim(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([claimId])`

### CustomerGift → `customer_gifts`
`apps/organization/prisma/schema.prisma:614`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| giftNumber | gift_number | String | N |  | U | ✓ |
| employeeId | employee_id | String | N |  | LREF | ✓ |
| departmentId | department_id | String? | Y |  | LREF | ✓ |
| accountId | account_id | String? | Y |  | LREF | ✓ |
| recipientName | recipient_name | String | N |  |  | ✓ |
| title | title | String | N |  |  | ✓ |
| totalAmount | total_amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| status | status | CustomerGiftStatus | N | DRAFT |  | ✓ |
| submittedAt | submitted_at | DateTime? | Y |  |  | ✓ |
| managerId | manager_id | String? | Y |  | LREF | ✓ |
| managerApprovedAt | manager_approved_at | DateTime? | Y |  |  | ✓ |
| financeApprovedBy | finance_approved_by | String? | Y |  |  | ✓ |
| financeApprovedAt | finance_approved_at | DateTime? | Y |  |  | ✓ |
| paidBy | paid_by | String? | Y |  |  | ✓ |
| paidAt | paid_at | DateTime? | Y |  |  | ✓ |
| paymentMethod | payment_method | String? | Y |  |  | ✓ |
| rejectedBy | rejected_by | String? | Y |  |  | ✓ |
| rejectedAt | rejected_at | DateTime? | Y |  |  | ✓ |
| rejectionReason | rejection_reason | String? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@index([employeeId])`; `@@index([status])`; `@@index([accountId])`

### CustomerGiftLine → `customer_gift_lines`
`apps/organization/prisma/schema.prisma:647`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| giftId | gift_id | String | N |  | FK-col | ✓ |
| category | category | CustomerGiftCategory | N |  |  | ✓ |
| description | description | String | N |  |  | ✓ |
| quantity | quantity | Int | N | 1 |  | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| giftDate | gift_date | DateTime | N |  |  | ✓ |
| productId | product_id | String? | Y |  | LREF | ✓ |
| receiptReference | receipt_reference | String? | Y |  |  | ✓ |
| gift | gift | CustomerGift | N |  | FK→CustomerGift(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([giftId])`

### AuditLog → `audit_logs`
`apps/organization/prisma/schema.prisma:665`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| userId | user_id | String? | Y |  | LREF | ✓ |
| action | action | String | N |  |  | ✓ |
| entity | entity | String | N |  |  | ✓ |
| entityId | entity_id | String? | Y |  | LREF | ✓ |
| before | before | Json? | Y |  |  | ✓ |
| after | after | Json? | Y |  |  | ✓ |
| reasonCode | reason_code | String? | Y |  |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| ipAddress | ip_address | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([userId])`; `@@index([entity])`; `@@index([createdAt])`

#### Enums (organization)
| Enum | Values | B? |
|---|---|---|
| EmploymentStatus | ACTIVE, ON_LEAVE, SUSPENDED, TERMINATED | ✓ |
| AttendanceStatus | PRESENT, ABSENT, LATE, ON_LEAVE, HOLIDAY | ✓ |
| LeaveType | ANNUAL, CASUAL, SICK, UNPAID | ✓ |
| LeaveStatus | PENDING, APPROVED, REJECTED, CANCELLED | ✓ |
| ContractType | FULL_TIME, PART_TIME, PROBATION, TEMPORARY, CONSULTANT | ✓ |
| ContractStatus | DRAFT, ACTIVE, EXPIRED, TERMINATED, RENEWED | ✓ |
| CompensationFrequency | MONTHLY, DAILY, HOURLY | ✓ |
| SalaryComponentType | EARNING, DEDUCTION | ✓ |
| PayrollRunStatus | DRAFT, CALCULATED, APPROVED, FINALIZED, PAID, CANCELLED | ✓ |
| PayrollEntryStatus | DRAFT, APPROVED, FINALIZED, PAID | ✓ |
| PayrollAdjustmentType | CORRECTION, REVERSAL, BONUS, PENALTY | ✓ |
| ExpenseCategory | TRAVEL_FUEL, CLIENT_HOSPITALITY, ACCOMMODATION, PERMIT_FEES, MEDICAL_SAMPLES_TRANSPORT, PETTY_CASH | ✓ |
| ExpenseClaimStatus | DRAFT, SUBMITTED, MANAGER_APPROVED, FINANCE_APPROVED, REJECTED, PAID | ✓ |
| CustomerGiftCategory | PRODUCT_SAMPLE, PROMOTIONAL_GIFT, DOCTOR_GIFT, CUSTOMER_GIFT, EVENT_CAMPAIGN, OTHER | ✓ |
| CustomerGiftStatus | DRAFT, SUBMITTED, MANAGER_APPROVED, FINANCE_APPROVED, REJECTED, PAID | ✓ |

## خدمة `products` — DB `nile_products`
المصدر: `apps/products/prisma/schema.prisma`

### ProductCategory → `product_categories`
`apps/products/prisma/schema.prisma:37`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String | N |  |  | ✓ |

### ProductBrand → `product_brands`
`apps/products/prisma/schema.prisma:46`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String | N |  |  | ✓ |

### ProductManufacturer → `product_manufacturers`
`apps/products/prisma/schema.prisma:55`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String | N |  |  | ✓ |
| country | country | String? | Y |  |  | ✓ |

### Product → `products`
`apps/products/prisma/schema.prisma:65`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| sku | sku | String | N |  | U | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String | N |  |  | ✓ |
| ndc | ndc | String? | Y |  | U | ✓ |
| gtin | gtin | String? | Y |  | U | ✓ |
| registrationNo | registration_no | String? | Y |  |  | ✓ |
| basePrice | base_price | Decimal? @db.Decimal(14, 4) | Y |  |  | ✓ |
| salesTaxPct | sales_tax_pct | Decimal @db.Decimal(5, 2) | N | 14 |  | ✓ |
| commissionPct | commission_pct | Decimal @db.Decimal(5, 2) | N | 10 |  | ✓ |
| costPrice | cost_price | Decimal? @db.Decimal(14, 4) | Y |  |  | ✓ |
| publicPrice | public_price | Decimal? @db.Decimal(14, 4) | Y |  |  | ✓ |
| categoryId | category_id | String? | Y |  | FK-col | ✓ |
| brandId | brand_id | String? | Y |  | FK-col | ✓ |
| manufacturerId | manufacturer_id | String? | Y |  | FK-col | ✓ |
| reorderPoint | reorder_point | Int? | Y |  |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| category | category | ProductCategory? | Y |  | FK→ProductCategory(id) onDelete=default | ✓ |
| brand | brand | ProductBrand? | Y |  | FK→ProductBrand(id) onDelete=default | ✓ |
| manufacturer | manufacturer | ProductManufacturer? | Y |  | FK→ProductManufacturer(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([nameEn])`

### UnitOfMeasure → `units_of_measure`
`apps/products/prisma/schema.prisma:128`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | UomCode | N |  | U | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String | N |  |  | ✓ |
| isBase | is_base | Boolean | N | false |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

### ProductUomConversion → `product_uom_conversions`
`apps/products/prisma/schema.prisma:139`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| productId | product_id | String | N |  | FK-col | ✓ |
| fromUom | from_uom | UomCode | N |  |  | ✓ |
| toUom | to_uom | UomCode | N |  |  | ✓ |
| conversionFactor | conversion_factor | Decimal @db.Decimal(10, 4) | N |  |  | ✓ |
| barcode | barcode | String? | Y |  |  | ✓ |
| isDefaultPurchasing | is_default_purchasing | Boolean | N | false |  | ✓ |
| isDefaultSelling | is_default_selling | Boolean | N | false |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| product | product | Product | N |  | FK→Product(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@unique([productId, fromUom, toUom])`; `@@index([productId])`

### ProductIngredient → `product_ingredients`
`apps/products/prisma/schema.prisma:163`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| productId | product_id | String | N |  | FK-col | ✓ |
| sequence | sequence | Int | N |  |  | ✓ |
| name | name | String | N |  |  | ✓ |
| amount | amount | Decimal? @db.Decimal(10, 4) | Y |  |  | ✓ |
| unit | unit | String? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| product | product | Product | N |  | FK→Product(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@unique([productId, sequence])`; `@@index([productId])`

### ProductTemperatureProfile → `product_temperature_profiles`
`apps/products/prisma/schema.prisma:180`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| productId | product_id | String | N |  | U FK-col | ✓ |
| minTempC | min_temp_c | Decimal @db.Decimal(5, 2) | N |  |  | ✓ |
| maxTempC | max_temp_c | Decimal @db.Decimal(5, 2) | N |  |  | ✓ |
| requiresCold | requires_cold | Boolean | N | false |  | ✓ |
| product | product | Product | N |  | FK→Product(id) onDelete=Cascade | ✓ |

### Batch → `batches`
`apps/products/prisma/schema.prisma:192`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| productId | product_id | String | N |  | FK-col | ✓ |
| lotNumber | lot_number | String | N |  |  | ✓ |
| manufactureDate | manufacture_date | DateTime? | Y |  |  | ✓ |
| expiryDate | expiry_date | DateTime | N |  |  | ✓ |
| status | status | BatchStatus | N | QUARANTINE |  | ✓ |
| quantityTotal | quantity_total | Int | N |  |  | ✓ |
| quarantineAt | quarantine_at | DateTime? | Y |  |  | ✓ |
| recalledAt | recalled_at | DateTime? | Y |  |  | ✓ |
| recalledReason | recalled_reason | String? | Y |  |  | ✓ |
| recalledBy | recalled_by | String? | Y |  |  | ✓ |
| recallId | recall_id | String? | Y |  | LREF | ✓ |
| supplierId | supplier_id | String? | Y |  | FK-col | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| releasedAt | released_at | DateTime? | Y |  |  | ✓ |
| releasedBy | released_by | String? | Y |  |  | ✓ |
| releaseNote | release_note | String? | Y |  |  | ✓ |
| rejectedAt | rejected_at | DateTime? | Y |  |  | ✓ |
| rejectedBy | rejected_by | String? | Y |  |  | ✓ |
| rejectedReason | rejected_reason | String? | Y |  |  | ✓ |
| quarantineReason | quarantine_reason | String? | Y |  |  | ✓ |
| product | product | Product | N |  | FK→Product(id) onDelete=default | ✓ |
| supplier | supplier | Supplier? | Y |  | FK→Supplier(id) onDelete=default | ✓ |

Indexes/constraints: `@@unique([productId, lotNumber])`; `@@index([expiryDate])`; `@@index([status])`; `@@index([supplierId])`

### BatchQcRecord → `batch_qc_records`
`apps/products/prisma/schema.prisma:233`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| batchId | batch_id | String | N |  | FK-col | ✓ |
| sampledAt | sampled_at | DateTime? | Y |  |  | ✓ |
| sampledBy | sampled_by | String? | Y |  |  | ✓ |
| labName | lab_name | String? | Y |  |  | ✓ |
| coaNumber | coa_number | String? | Y |  |  | ✓ |
| coaFileUrl | coa_file_url | String? | Y |  |  | ✓ |
| testReportUrl | test_report_url | String? | Y |  |  | ✓ |
| result | result | QcResult | N | PENDING |  | ✓ |
| parameters | parameters | Json? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| decidedBy | decided_by | String? | Y |  |  | ✓ |
| decidedAt | decided_at | DateTime? | Y |  |  | ✓ |
| signatureId | signature_id | String? | Y |  | LREF | ✓ |
| createdBy | created_by | String | N |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| batch | batch | Batch | N |  | FK→Batch(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([batchId])`; `@@index([result])`

### Supplier → `suppliers`
`apps/products/prisma/schema.prisma:264`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | String | N |  | U | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String? | Y |  |  | ✓ |
| phone | phone | String? | Y |  |  | ✓ |
| email | email | String? | Y |  |  | ✓ |
| address | address | String? | Y |  |  | ✓ |
| creditLimit | credit_limit | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

### SerializedUnit → `serialized_units`
`apps/products/prisma/schema.prisma:284`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| batchId | batch_id | String | N |  | FK-col | ✓ |
| serialNumber | serial_number | String | N |  | U | ✓ |
| gtin | gtin | String? | Y |  |  | ✓ |
| sscc | sscc | String? | Y |  |  | ✓ |
| packageLevel | package_level | PackageLevel | N | EACH |  | ✓ |
| parentId | parent_id | String? | Y |  | FK-col | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| batch | batch | Batch | N |  | FK→Batch(id) onDelete=default | ✓ |
| parent | parent | SerializedUnit? | Y |  | FK→SerializedUnit(id) onDelete=default | ✓ |
| children | children | SerializedUnit[] | N |  | FK→SerializedUnit() onDelete=default | ✓ |

Indexes/constraints: `@@index([batchId])`

### JobRun → `job_runs`
`apps/products/prisma/schema.prisma:311`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| name | name | String | N |  |  | ✓ |
| status | status | JobRunStatus | N |  |  | ✓ |
| startedAt | started_at | DateTime | N |  |  | ✓ |
| finishedAt | finished_at | DateTime? | Y |  |  | ✓ |
| affected | affected | Int? | Y |  |  | ✓ |
| error | error | String? | Y |  |  | ✓ |
| triggeredBy | triggered_by | String | N | "cron" |  | ✓ |

Indexes/constraints: `@@index([name, startedAt])`

### AuditLog → `audit_logs`
`apps/products/prisma/schema.prisma:326`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| userId | user_id | String? | Y |  | LREF | ✓ |
| action | action | String | N |  |  | ✓ |
| entity | entity | String | N |  |  | ✓ |
| entityId | entity_id | String? | Y |  | LREF | ✓ |
| before | before | Json? | Y |  |  | ✓ |
| after | after | Json? | Y |  |  | ✓ |
| reasonCode | reason_code | String? | Y |  |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| ipAddress | ip_address | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([userId])`; `@@index([entity])`; `@@index([createdAt])`

### ProductPriceHistory → `product_price_history`
`apps/products/prisma/schema.prisma:353`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| productId | product_id | String | N |  | FK-col | ✓ |
| field | field | PriceField | N |  |  | ✓ |
| oldValue | old_value | Decimal? @db.Decimal(14, 4) | Y |  |  | ✓ |
| newValue | new_value | Decimal? @db.Decimal(14, 4) | Y |  |  | ✓ |
| source | source | PriceChangeSource | N | MANUAL |  | ✓ |
| actorId | actor_id | String | N |  | LREF | ✓ |
| note | note | String? | Y |  |  | ✓ |
| changedAt | changed_at | DateTime | N | now() |  | ✓ |
| product | product | Product | N |  | FK→Product(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([productId, changedAt])`; `@@index([changedAt])`

### PriceList → `price_lists`
`apps/products/prisma/schema.prisma:381`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | String | N |  | U | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String? | Y |  |  | ✓ |
| kind | kind | PriceListKind | N | OTHER |  | ✓ |
| customerSegment | customer_segment | String? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@index([isActive])`

### PriceListItem → `price_list_items`
`apps/products/prisma/schema.prisma:402`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| priceListId | price_list_id | String | N |  | FK-col | ✓ |
| productId | product_id | String | N |  | FK-col | ✓ |
| price | price | Decimal @db.Decimal(14, 4) | N |  |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| priceList | priceList | PriceList | N |  | FK→PriceList(id) onDelete=Cascade | ✓ |
| product | product | Product | N |  | FK→Product(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@unique([priceListId, productId])`; `@@index([productId])`

#### Enums (products)
| Enum | Values | B? |
|---|---|---|
| BatchStatus | RELEASED, QUARANTINE, EXPIRED, RECALLED, REJECTED | ✓ |
| QcResult | PENDING, PASS, FAIL, CONDITIONAL | ✓ |
| PackageLevel | EACH, CARTON, PALLET | ✓ |
| UomCode | CARTON, BOX, STRIP, BLISTER, AMPOULE, VIAL, BOTTLE, PIECE | ✓ |
| JobRunStatus | RUNNING, SUCCESS, FAILED, SKIPPED_LOCKED | ✓ |
| PriceListKind | WHOLESALE, RETAIL, PHARMACY, KEY_ACCOUNTS, DISTRIBUTOR, HOSPITAL, OTHER | ✓ |
| PriceField | BASE_PRICE, PUBLIC_PRICE, COST_PRICE | ✓ |
| PriceChangeSource | MANUAL, IMPORT, BULK_ADJUST, CATALOG_PUBLISH | ✓ |

## خدمة `sales` — DB `nile_sales`
المصدر: `apps/sales/prisma/schema.prisma`

### SalesOrder → `sales_orders`
`apps/sales/prisma/schema.prisma:57`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| orderNumber | order_number | String | N |  | U | ✓ |
| accountId | account_id | String | N |  | LREF | ✓ |
| accountName | account_name | String | N |  |  | ✓ |
| repId | rep_id | String | N |  | LREF | ✓ |
| status | status | OrderStatus | N | DRAFT |  | ✓ |
| subtotal | subtotal | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| taxTotal | tax_total | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| discountTotal | discount_total | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| grandTotal | grand_total | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| shippingFee | shipping_fee | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| shippingRateId | shipping_rate_id | String? | Y |  | LREF | ✓ |
| shippingZoneCode | shipping_zone_code | String? | Y |  |  | ✓ |
| shippingZoneName | shipping_zone_name | String? | Y |  |  | ✓ |
| shippingDirection | shipping_direction | ShippingDirection? | Y |  |  | ✓ |
| shippingGovernorate | shipping_governorate | String? | Y |  |  | ✓ |
| shippingCity | shipping_city | String? | Y |  |  | ✓ |
| shippingArea | shipping_area | String? | Y |  |  | ✓ |
| shippingFreeAreaDecision | shipping_free_area_decision | String? | Y |  |  | ✓ |
| shippingResolution | shipping_resolution | String? | Y |  |  | ✓ |
| shippingManualOverrideReason | shipping_manual_override_reason | String? | Y |  |  | ✓ |
| shippingQuoteSource | shipping_quote_source | String? | Y |  |  | ✓ |
| shippingQuotedAt | shipping_quoted_at | DateTime? | Y |  |  | ✓ |
| collectedAmount | collected_amount | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| visitId | visit_id | String? | Y |  | U LREF | ✓ |
| idempotencyKey | idempotency_key | String? | Y |  | U | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([accountId])`; `@@index([repId])`; `@@index([status])`

### SalesOrderLine → `sales_order_lines`
`apps/sales/prisma/schema.prisma:114`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| orderId | order_id | String | N |  | FK-col | ✓ |
| productId | product_id | String | N |  | LREF | ✓ |
| productName | product_name | String | N |  |  | ✓ |
| quantity | quantity | Int | N |  |  | ✓ |
| unitPrice | unit_price | Decimal @db.Decimal(14, 4) | N |  |  | ✓ |
| taxPct | tax_pct | Decimal @db.Decimal(5, 2) | N |  |  | ✓ |
| discountPct | discount_pct | Decimal @db.Decimal(5, 2) | N | 0 |  | ✓ |
| lineTotal | line_total | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| requestedBatchId | requested_batch_id | String? | Y |  | LREF | ✓ |
| reservedQty | reserved_qty | Int | N | 0 |  | ✓ |
| allocatedBatch | allocated_batch | String? | Y |  |  | ✓ |
| returnedQty | returned_qty | Int | N | 0 |  | ✓ |
| order | order | SalesOrder | N |  | FK→SalesOrder(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([orderId])`

### OrderLineAllocation → `order_line_allocations`
`apps/sales/prisma/schema.prisma:149`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| orderLineId | order_line_id | String | N |  | FK-col | ✓ |
| batchId | batch_id | String | N |  | LREF | ✓ |
| warehouseId | warehouse_id | String? | Y |  | LREF | ✓ |
| quantity | quantity | Int | N |  |  | ✓ |
| source | source | String | N |  |  | ✓ |
| orderLine | orderLine | SalesOrderLine | N |  | FK→SalesOrderLine(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([orderLineId])`; `@@index([batchId])`

### SalesReturn → `sales_returns`
`apps/sales/prisma/schema.prisma:180`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| orderId | order_id | String | N |  | FK-col | ✓ |
| accountId | account_id | String | N |  | LREF | ✓ |
| repId | rep_id | String? | Y |  | LREF | ✓ |
| reason | reason | String | N |  |  | ✓ |
| totalValue | total_value | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| actorId | actor_id | String | N |  | LREF | ✓ |
| status | status | SalesReturnStatus | N | PENDING |  | ✓ |
| decidedById | decided_by_id | String? | Y |  | LREF | ✓ |
| decidedAt | decided_at | DateTime? | Y |  |  | ✓ |
| rejectedReason | rejected_reason | String? | Y |  |  | ✓ |
| postedAt | posted_at | DateTime? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| order | order | SalesOrder | N |  | FK→SalesOrder(id) onDelete=default | ✓ |

Indexes/constraints: `@@index([orderId])`; `@@index([accountId])`; `@@index([status])`

### SalesReturnLine → `sales_return_lines`
`apps/sales/prisma/schema.prisma:204`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| returnId | return_id | String | N |  | FK-col | ✓ |
| orderLineId | order_line_id | String | N |  | LREF | ✓ |
| productId | product_id | String | N |  | LREF | ✓ |
| productName | product_name | String | N |  |  | ✓ |
| batchId | batch_id | String | N |  | LREF | ✓ |
| warehouseId | warehouse_id | String | N |  | LREF | ✓ |
| quantity | quantity | Int | N |  |  | ✓ |
| unitPrice | unit_price | Decimal @db.Decimal(14, 4) | N |  |  | ✓ |
| lineTotal | line_total | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| condition | condition | ReturnLineCondition | N |  |  | ✓ |
| return | return | SalesReturn | N |  | FK→SalesReturn(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([returnId])`

### OrderApproval → `order_approvals`
`apps/sales/prisma/schema.prisma:222`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| orderId | order_id | String | N |  | U FK-col | ✓ |
| approverId | approver_id | String? | Y |  | LREF | ✓ |
| approved | approved | Boolean? | Y |  |  | ✓ |
| reason | reason | String? | Y |  |  | ✓ |
| decidedAt | decided_at | DateTime? | Y |  |  | ✓ |
| order | order | SalesOrder | N |  | FK→SalesOrder(id) onDelete=Cascade | ✓ |

### PricingRule → `pricing_rules`
`apps/sales/prisma/schema.prisma:240`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | String? | Y |  | U | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String? | Y |  |  | ✓ |
| type | type | DiscountPolicyType | N | TRADE |  | ✓ |
| valueType | value_type | DiscountValueType | N | PERCENT |  | ✓ |
| value | value | Decimal @db.Decimal(12, 2) | N | 0 |  | ✓ |
| maxDiscountPct | max_discount_pct | Decimal @db.Decimal(5, 2) | N |  |  | ✓ |
| approvalThreshold | approval_threshold | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| paymentDays | payment_days | Int? | Y |  |  | ✓ |
| minInvoiceAmount | min_invoice_amount | Decimal? @db.Decimal(14, 2) | Y |  |  | ✓ |
| requiredRole | required_role | String? | Y |  |  | ✓ |
| notes | notes | String? | Y |  |  | ✓ |
| validFrom | valid_from | DateTime? | Y |  |  | ✓ |
| validTo | valid_to | DateTime? | Y |  |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| pendingReview | pending_review | Boolean | N | false |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@index([isActive])`; `@@index([pendingReview])`

### DiscountApprovalLevel → `discount_approval_levels`
`apps/sales/prisma/schema.prisma:294`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| roleLabel | role_label | String | N |  |  | ✓ |
| maxDiscountPct | max_discount_pct | Decimal @db.Decimal(5, 2) | N |  |  | ✓ |
| sortOrder | sort_order | Int | N | 0 |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@unique([roleLabel])`

### Promotion → `promotions`
`apps/sales/prisma/schema.prisma:311`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | String? | Y |  | U | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String? | Y |  |  | ✓ |
| mechanism | mechanism | PromotionMechanism | N |  |  | ✓ |
| scopeType | scope_type | PriceRuleScope | N | ALL |  | ✓ |
| scopeId | scope_id | String? | Y |  | LREF | ✓ |
| minQuantity | min_quantity | Int? | Y |  |  | ✓ |
| minInvoiceAmount | min_invoice_amount | Decimal? @db.Decimal(14, 2) | Y |  |  | ✓ |
| customerSegment | customer_segment | String? | Y |  |  | ✓ |
| buyQuantity | buy_quantity | Int? | Y |  |  | ✓ |
| freeQuantity | free_quantity | Int? | Y |  |  | ✓ |
| giftProductId | gift_product_id | String? | Y |  | LREF | ✓ |
| giftQuantity | gift_quantity | Int? | Y |  |  | ✓ |
| benefitPercent | benefit_percent | Decimal? @db.Decimal(5, 2) | Y |  |  | ✓ |
| bundlePrice | bundle_price | Decimal? @db.Decimal(14, 2) | Y |  |  | ✓ |
| startsAt | starts_at | DateTime? | Y |  |  | ✓ |
| endsAt | ends_at | DateTime? | Y |  |  | ✓ |
| isPaused | is_paused | Boolean | N | false |  | ✓ |
| maxRedemptionsTotal | max_redemptions_total | Int? | Y |  |  | ✓ |
| maxRedemptionsPerCustomer | max_redemptions_per_customer | Int? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@index([isPaused, startsAt, endsAt])`

### PromotionRedemption → `promotion_redemptions`
`apps/sales/prisma/schema.prisma:365`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| promotionId | promotion_id | String | N |  | FK-col | ✓ |
| orderId | order_id | String | N |  | LREF | ✓ |
| customerId | customer_id | String | N |  | LREF | ✓ |
| discountTotal | discount_total | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| giftUnits | gift_units | Int | N | 0 |  | ✓ |
| redeemedAt | redeemed_at | DateTime | N | now() |  | ✓ |
| promotion | promotion | Promotion | N |  | FK→Promotion(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@unique([promotionId, orderId])`; `@@index([promotionId, customerId])`

### PriceRule → `price_rules`
`apps/sales/prisma/schema.prisma:388`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| nameEn | name_en | String? | Y |  |  | ✓ |
| type | type | PriceRuleType | N |  |  | ✓ |
| scopeType | scope_type | PriceRuleScope | N | ALL |  | ✓ |
| scopeId | scope_id | String? | Y |  | LREF | ✓ |
| calcMethod | calc_method | PriceRuleCalcMethod | N |  |  | ✓ |
| value | value | Decimal @db.Decimal(12, 2) | N | 0 |  | ✓ |
| tiers | tiers | Json? | Y |  |  | ✓ |
| customerSegment | customer_segment | String? | Y |  |  | ✓ |
| governorate | governorate | String? | Y |  |  | ✓ |
| targetMarginPct | target_margin_pct | Decimal? @db.Decimal(5, 2) | Y |  |  | ✓ |
| priority | priority | Int | N | 100 |  | ✓ |
| validFrom | valid_from | DateTime? | Y |  |  | ✓ |
| validTo | valid_to | DateTime? | Y |  |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@index([isActive, priority])`

### PriceRuleSetting → `price_rule_settings`
`apps/sales/prisma/schema.prisma:445`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | "global" | PK | ✓ |
| isEnabled | is_enabled | Boolean | N | true |  | ✓ |
| updatedBy | updated_by | String? | Y |  |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

### OrderSaga → `order_sagas`
`apps/sales/prisma/schema.prisma:455`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| orderId | order_id | String | N |  | U FK-col | ✓ |
| correlationId | correlation_id | String | N |  | LREF | ✓ |
| step | step | SagaStep | N | CREATED |  | ✓ |
| lastError | last_error | String? | Y |  |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| order | order | SalesOrder | N |  | FK→SalesOrder(id) onDelete=Cascade | ✓ |

Indexes/constraints: `@@index([correlationId])`

### ProcessedEvent → `processed_events`
`apps/sales/prisma/schema.prisma:468`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| eventId | event_id | String | N |  | PK | ✓ |
| processedAt | processed_at | DateTime | N | now() |  | ✓ |

### AuditLog → `audit_logs`
`apps/sales/prisma/schema.prisma:475`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| userId | user_id | String? | Y |  | LREF | ✓ |
| action | action | String | N |  |  | ✓ |
| entity | entity | String | N |  |  | ✓ |
| entityId | entity_id | String? | Y |  | LREF | ✓ |
| before | before | Json? | Y |  |  | ✓ |
| after | after | Json? | Y |  |  | ✓ |
| reasonCode | reason_code | String? | Y |  |  | ✓ |
| correlationId | correlation_id | String? | Y |  | LREF | ✓ |
| ipAddress | ip_address | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([userId])`; `@@index([entity])`; `@@index([createdAt])`

### PendingPayment → `pending_payments`
`apps/sales/prisma/schema.prisma:497`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| orderId | order_id | String | N |  | LREF | ✓ |
| eventId | event_id | String | N |  | U LREF | ✓ |
| accountId | account_id | String | N |  | LREF | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| fullyPaid | fully_paid | Boolean | N | false |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([orderId])`

### PendingCreditApplication → `pending_credit_applications`
`apps/sales/prisma/schema.prisma:512`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| accountId | account_id | String | N |  | LREF | ✓ |
| amount | amount | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| status | status | String | N | "PENDING" |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |

Indexes/constraints: `@@index([accountId])`

### AccountCredit → `account_credit`
`apps/sales/prisma/schema.prisma:527`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| accountId | account_id | String | N |  | PK | ✓ |
| creditLimit | credit_limit | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| outstanding | outstanding | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

### ProductPrice → `product_prices`
`apps/sales/prisma/schema.prisma:540`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| productId | product_id | String | N |  | U LREF | ✓ |
| productName | product_name | String | N |  |  | ✓ |
| unitPrice | unit_price | Decimal @db.Decimal(14, 4) | N |  |  | ✓ |
| publicPrice | public_price | Decimal? @db.Decimal(14, 4) | Y |  |  | ✓ |
| taxPct | tax_pct | Decimal @db.Decimal(5, 2) | N |  |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

### BlockedBatch → `blocked_batches`
`apps/sales/prisma/schema.prisma:560`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| batchId | batch_id | String | N |  | PK | ✓ |
| reason | reason | BatchBlockReason | N |  |  | ✓ |
| recallId | recall_id | String? | Y |  | LREF | ✓ |
| blockedAt | blocked_at | DateTime | N | now() |  | ✓ |

### OrderRecallHold → `order_recall_holds`
`apps/sales/prisma/schema.prisma:572`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| orderId | order_id | String | N |  | LREF | ✓ |
| batchId | batch_id | String | N |  | LREF | ✓ |
| reason | reason | BatchBlockReason | N |  |  | ✓ |
| recallId | recall_id | String? | Y |  | LREF | ✓ |
| previousStatus | previous_status | OrderStatus | N |  |  | ✓ |
| heldAt | held_at | DateTime | N | now() |  | ✓ |
| releasedAt | released_at | DateTime? | Y |  |  | ✓ |
| releasedBy | released_by | String? | Y |  |  | ✓ |
| decision | decision | String? | Y |  |  | ✓ |
| releaseNote | release_note | String? | Y |  |  | ✓ |

Indexes/constraints: `@@unique([orderId, batchId])`; `@@index([orderId])`; `@@index([batchId])`

### ShippingZone → `shipping_zones`
`apps/sales/prisma/schema.prisma:599`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| code | code | String | N |  | U | ✓ |
| nameAr | name_ar | String | N |  |  | ✓ |
| coverageText | coverage_text | String | N |  |  | ✓ |
| minHours | min_hours | Int? | Y |  |  | ✓ |
| maxHours | max_hours | Int? | Y |  |  | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |

Indexes/constraints: `@@index([isActive])`

### ShippingRate → `shipping_rates`
`apps/sales/prisma/schema.prisma:617`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| zoneId | zone_id | String | N |  | FK-col | ✓ |
| oneWayFee | one_way_fee | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| roundTripFee | round_trip_fee | Decimal @db.Decimal(14, 2) | N |  |  | ✓ |
| validFrom | valid_from | DateTime | N |  |  | ✓ |
| validTo | valid_to | DateTime? | Y |  |  | ✓ |
| createdBy | created_by | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| zone | zone | ShippingZone | N |  | FK→ShippingZone(id) onDelete=Restrict | ✓ |

Indexes/constraints: `@@unique([zoneId, validFrom])`; `@@index([zoneId, validFrom, validTo])`

### ShippingZoneArea → `shipping_zone_areas`
`apps/sales/prisma/schema.prisma:637`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| zoneId | zone_id | String | N |  | FK-col | ✓ |
| governorate | governorate | String | N |  |  | ✓ |
| city | city | String | N | "" |  | ✓ |
| areaName | area_name | String | N |  |  | ✓ |
| normalizedKey | normalized_key | String | N |  | U | ✓ |
| isActive | is_active | Boolean | N | true |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| zone | zone | ShippingZone | N |  | FK→ShippingZone(id) onDelete=Restrict | ✓ |

Indexes/constraints: `@@index([governorate, city])`; `@@index([zoneId, isActive])`

### OrderShipment → `order_shipments`
`apps/sales/prisma/schema.prisma:666`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| orderId | order_id | String | N |  | U FK-col | ✓ |
| carrier | carrier | String? | Y |  |  | ✓ |
| driverName | driver_name | String? | Y |  |  | ✓ |
| vehicleNo | vehicle_no | String? | Y |  |  | ✓ |
| trackingNo | tracking_no | String? | Y |  |  | ✓ |
| zone | zone | String? | Y |  |  | ✓ |
| address | address | String? | Y |  |  | ✓ |
| expectedAt | expected_at | DateTime? | Y |  |  | ✓ |
| status | status | ShipmentStatus | N | PREPARING |  | ✓ |
| dispatchedAt | dispatched_at | DateTime? | Y |  |  | ✓ |
| deliveredAt | delivered_at | DateTime? | Y |  |  | ✓ |
| receivedBy | received_by | String? | Y |  |  | ✓ |
| podNote | pod_note | String? | Y |  |  | ✓ |
| podSignatureKey | pod_signature_key | String? | Y |  |  | ✓ |
| podSignatureMime | pod_signature_mime | String? | Y |  |  | ✓ |
| podSignatureSize | pod_signature_size | Int? | Y |  |  | ✓ |
| podPhotoKey | pod_photo_key | String? | Y |  |  | ✓ |
| podPhotoMime | pod_photo_mime | String? | Y |  |  | ✓ |
| podPhotoSize | pod_photo_size | Int? | Y |  |  | ✓ |
| podCapturedAt | pod_captured_at | DateTime? | Y |  |  | ✓ |
| updatedBy | updated_by | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| order | order | SalesOrder | N |  | FK→SalesOrder(id) onDelete=Restrict | ✓ |

Indexes/constraints: `@@index([status])`; `@@index([carrier])`

### ShipmentLeg → `shipment_legs`
`apps/sales/prisma/schema.prisma:723`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| shipmentId | shipment_id | String | N |  | FK-col | ✓ |
| type | type | ShipmentLegType | N |  |  | ✓ |
| status | status | ShipmentLegStatus | N | PLANNED |  | ✓ |
| carrier | carrier | String? | Y |  |  | ✓ |
| driverName | driver_name | String? | Y |  |  | ✓ |
| trackingNo | tracking_no | String? | Y |  |  | ✓ |
| scheduledAt | scheduled_at | DateTime? | Y |  |  | ✓ |
| dispatchedAt | dispatched_at | DateTime? | Y |  |  | ✓ |
| completedAt | completed_at | DateTime? | Y |  |  | ✓ |
| invoiceId | invoice_id | String? | Y |  | LREF | ✓ |
| cashAmount | cash_amount | Decimal @db.Decimal(14, 2) | N | 0 |  | ✓ |
| currency | currency | String | N | "EGP" |  | ✓ |
| paymentMethod | payment_method | String? | Y |  |  | ✓ |
| paymentId | payment_id | String? | Y |  | LREF | ✓ |
| signedInvoiceKey | signed_invoice_key | String? | Y |  |  | ✓ |
| signedInvoiceMime | signed_invoice_mime | String? | Y |  |  | ✓ |
| signedInvoiceSize | signed_invoice_size | Int? | Y |  |  | ✓ |
| receivedBy | received_by | String? | Y |  |  | ✓ |
| note | note | String? | Y |  |  | ✓ |
| completedBy | completed_by | String? | Y |  |  | ✓ |
| createdAt | created_at | DateTime | N | now() |  | ✓ |
| updatedAt | updated_at | DateTime | N |  |  | ✓ |
| shipment | shipment | OrderShipment | N |  | FK→OrderShipment(id) onDelete=Restrict | ✓ |

Indexes/constraints: `@@unique([shipmentId, type])`; `@@index([status])`; `@@index([invoiceId])`; `@@index([paymentId])`

### JobRun → `job_runs`
`apps/sales/prisma/schema.prisma:765`

| Field | Column | Type | Null | Default | Key | B? |
|---|---|---|---|---|---|---|
| id | id | String | N | uuid() | PK | ✓ |
| name | name | String | N |  |  | ✓ |
| status | status | JobRunStatus | N |  |  | ✓ |
| startedAt | started_at | DateTime | N |  |  | ✓ |
| finishedAt | finished_at | DateTime? | Y |  |  | ✓ |
| affected | affected | Int? | Y |  |  | ✓ |
| error | error | String? | Y |  |  | ✓ |
| triggeredBy | triggered_by | String | N | "cron" |  | ✓ |

Indexes/constraints: `@@index([name, startedAt])`

#### Enums (sales)
| Enum | Values | B? |
|---|---|---|
| OrderStatus | DRAFT, PENDING_APPROVAL, CREDIT_HOLD, APPROVED, ALLOCATING, ALLOCATED, ALLOCATION_FAILED, INVOICED, PAID, SHIPPED, DELIVERED, CANCELLED, REJECTED, ON_HOLD_RECALL | ✓ |
| BatchBlockReason | RECALL, QUARANTINE, EXPIRED | ✓ |
| ReturnLineCondition | SELLABLE, DAMAGED | ✓ |
| SagaStep | CREATED, RESERVE_REQUESTED, RESERVED, INVOICED, PAID, COMPENSATING, DONE, FAILED | ✓ |
| SalesReturnStatus | PENDING, APPROVED, REJECTED, POSTED | ✓ |
| DiscountPolicyType | CASH_EARLY, TRADE, REBATE, MANUAL | ✓ |
| DiscountValueType | PERCENT, FIXED | ✓ |
| PromotionMechanism | BONUS, BUNDLE, CART_DISCOUNT, FREE_GIFT | ✓ |
| PriceRuleType | TIERED, CUSTOMER_GROUP, GEOGRAPHICAL, COST_PLUS | ✓ |
| PriceRuleScope | PRODUCT, CATEGORY, ALL | ✓ |
| PriceRuleCalcMethod | PERCENT_DISCOUNT, FIXED_DISCOUNT, FIXED_PRICE | ✓ |
| ShippingDirection | ONE_WAY, ROUND_TRIP | ✓ |
| ShipmentStatus | PREPARING, READY, DISPATCHED, DELIVERED, RETURNED | ✓ |
| ShipmentLegType | OUTBOUND_DELIVERY, RETURN_CASH_INVOICE | ✓ |
| ShipmentLegStatus | PLANNED, IN_TRANSIT, COMPLETED, FINANCE_PENDING, FINANCE_POSTED, FAILED, CANCELLED | ✓ |
| JobRunStatus | RUNNING, SUCCESS, FAILED, SKIPPED_LOCKED | ✓ |
