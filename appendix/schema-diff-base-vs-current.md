# Schema diff BASELINE 89c2c31 → CURRENT fa40270 (Prisma models)

## accounting
- Models مضافة: BankStatement, BankStatementLine, FinancialInstrument, ImportShipment, ImportShipmentLine, JournalEntry, JournalEntryWorkflow, JournalLine, PurchaseOrderReceipt, RegulatoryClearance, ShipmentDocument, ShipmentStatusEvent, SupplierPayment
- Enums مضافة: InstrumentStatus, InstrumentType, JournalEntryStatus
- `Invoice`: +fields[instruments]
- `Payment`: +fields[instrument]
- `PurchaseOrder`: +fields[receipts]
- `PurchaseOrderLine`: +fields[receipts]
- `VendorInvoice`: +fields[exchangeRate, baseTotal]

## audit-aggregator: لا تغيير في Prisma models/enums

## crm
- `Account`: +fields[priceListId, pricingDiscountPct] +idx[@@index([priceListId], map: "accounts_price_list_idx")]
- `Lead`: +fields[source, contactName, contactPhone, contactEmail, companyName, notes, nextFollowUpAt, lastContactAt, lostReason, qualifiedAt, convertedAt, convertedById, lostAt, updatedAt] +idx[@@index([nextFollowUpAt]); @@index([repId, status]); @@index([status, createdAt])] -idx[@@index([status])]

## iam: لا تغيير في Prisma models/enums

## incentives: لا تغيير في Prisma models/enums

## inventory
- Models مضافة: InventoryCostLayer, InventoryOutboxEvent
- `InventoryTransaction`: +fields[unitCost, totalCost]

## organization
- Models مضافة: RepCoverage
- `Employee`: +fields[repCoverages]

## products: لا تغيير في Prisma models/enums

## sales: لا تغيير في Prisma models/enums
