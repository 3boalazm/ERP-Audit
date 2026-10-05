# Schema Statistics & Heuristic Gap Scan (CURRENT)

| Service | Models | Enums | Prisma FKs | Logical refs (*Id بلا FK) |
|---|---|---|---|---|
| accounting | 49 | 30 | 30 | 78 |
| audit-aggregator | 4 | 1 | 0 | 10 |
| crm | 20 | 18 | 23 | 22 |
| iam | 13 | 3 | 8 | 7 |
| incentives | 5 | 1 | 1 | 10 |
| inventory | 15 | 4 | 5 | 36 |
| organization | 25 | 15 | 26 | 16 |
| products | 17 | 8 | 14 | 6 |
| sales | 27 | 16 | 11 | 38 |

## Logical references without FK (LREF)
| Service | Model | Field | Evidence |
|---|---|---|---|
| accounting | Invoice | orderId | `apps/accounting/prisma/schema.prisma:116` |
| accounting | Invoice | accountId | `apps/accounting/prisma/schema.prisma:125` |
| accounting | Invoice | repId | `apps/accounting/prisma/schema.prisma:127` |
| accounting | Invoice | shippingRateId | `apps/accounting/prisma/schema.prisma:135` |
| accounting | Invoice | correlationId | `apps/accounting/prisma/schema.prisma:171` |
| accounting | InvoiceLine | productId | `apps/accounting/prisma/schema.prisma:224` |
| accounting | InvoiceLine | batchId | `apps/accounting/prisma/schema.prisma:243` |
| accounting | InvoiceLineBatch | batchId | `apps/accounting/prisma/schema.prisma:266` |
| accounting | GeneralPurchase | createdById | `apps/accounting/prisma/schema.prisma:295` |
| accounting | GeneralPurchase | updatedById | `apps/accounting/prisma/schema.prisma:296` |
| accounting | GeneralPurchaseRevision | actorId | `apps/accounting/prisma/schema.prisma:316` |
| accounting | FinancialInstrument | accountId | `apps/accounting/prisma/schema.prisma:335` |
| accounting | FinancialInstrument | actorId | `apps/accounting/prisma/schema.prisma:348` |
| accounting | Payment | accountId | `apps/accounting/prisma/schema.prisma:394` |
| accounting | Payment | orderId | `apps/accounting/prisma/schema.prisma:399` |
| accounting | Payment | actorId | `apps/accounting/prisma/schema.prisma:421` |
| accounting | Payment | sourceId | `apps/accounting/prisma/schema.prisma:425` |
| accounting | LedgerEntry | accountId | `apps/accounting/prisma/schema.prisma:454` |
| accounting | LedgerEntry | refId | `apps/accounting/prisma/schema.prisma:460` |
| accounting | CollectionMetric | repId | `apps/accounting/prisma/schema.prisma:476` |
| accounting | SupplierLedgerEntry | supplierId | `apps/accounting/prisma/schema.prisma:525` |
| accounting | SupplierLedgerEntry | refId | `apps/accounting/prisma/schema.prisma:533` |
| accounting | CancelledOrder | eventId | `apps/accounting/prisma/schema.prisma:564` |
| accounting | AuditLog | userId | `apps/accounting/prisma/schema.prisma:572` |
| accounting | AuditLog | entityId | `apps/accounting/prisma/schema.prisma:575` |
| accounting | AuditLog | correlationId | `apps/accounting/prisma/schema.prisma:579` |
| accounting | SupplierPayment | supplierId | `apps/accounting/prisma/schema.prisma:593` |
| accounting | SupplierPayment | supplierInvoiceId | `apps/accounting/prisma/schema.prisma:594` |
| accounting | SupplierPayment | financialAccountId | `apps/accounting/prisma/schema.prisma:600` |
| accounting | SupplierPayment | actorId | `apps/accounting/prisma/schema.prisma:603` |
| accounting | JournalEntry | fiscalPeriodId | `apps/accounting/prisma/schema.prisma:629` |
| accounting | JournalEntry | reversalOfId | `apps/accounting/prisma/schema.prisma:641` |
| accounting | JournalEntry | sourceId | `apps/accounting/prisma/schema.prisma:643` |
| accounting | JournalLine | accountId | `apps/accounting/prisma/schema.prisma:659` |
| accounting | FiscalPeriod | closingJournalId | `apps/accounting/prisma/schema.prisma:750` |
| accounting | LandedCostVoucher | vendorInvoiceId | `apps/accounting/prisma/schema.prisma:771` |
| accounting | LandedCostItem | productId | `apps/accounting/prisma/schema.prisma:796` |
| accounting | DepreciationEntry | journalEntryId | `apps/accounting/prisma/schema.prisma:867` |
| accounting | CreditNote | returnId | `apps/accounting/prisma/schema.prisma:915` |
| accounting | CreditNote | invoiceId | `apps/accounting/prisma/schema.prisma:916` |
| accounting | CreditNote | accountId | `apps/accounting/prisma/schema.prisma:917` |
| accounting | CreditNote | issuedById | `apps/accounting/prisma/schema.prisma:927` |
| accounting | TaxEntry | invoiceId | `apps/accounting/prisma/schema.prisma:949` |
| accounting | TaxEntry | partyId | `apps/accounting/prisma/schema.prisma:950` |
| accounting | PurchaseOrder | supplierId | `apps/accounting/prisma/schema.prisma:1009` |
| accounting | PurchaseOrder | createdById | `apps/accounting/prisma/schema.prisma:1020` |
| accounting | PurchaseOrderLine | productId | `apps/accounting/prisma/schema.prisma:1039` |
| accounting | PurchaseOrderReceipt | eventId | `apps/accounting/prisma/schema.prisma:1058` |
| accounting | PurchaseOrderReceipt | productId | `apps/accounting/prisma/schema.prisma:1061` |
| accounting | PurchaseOrderReceipt | supplierId | `apps/accounting/prisma/schema.prisma:1062` |
| accounting | PurchaseOrderReceipt | warehouseId | `apps/accounting/prisma/schema.prisma:1063` |
| accounting | PurchaseOrderReceipt | batchId | `apps/accounting/prisma/schema.prisma:1064` |
| accounting | PurchaseOrderReceipt | actorId | `apps/accounting/prisma/schema.prisma:1067` |
| accounting | VendorInvoice | supplierId | `apps/accounting/prisma/schema.prisma:1080` |
| accounting | VendorInvoice | createdById | `apps/accounting/prisma/schema.prisma:1101` |
| accounting | VendorInvoiceLine | productId | `apps/accounting/prisma/schema.prisma:1121` |
| accounting | OutboxEvent | leaseId | `apps/accounting/prisma/schema.prisma:1187` |
| accounting | FxSnapshot | refId | `apps/accounting/prisma/schema.prisma:1199` |
| accounting | FxSnapshot | rateId | `apps/accounting/prisma/schema.prisma:1204` |
| accounting | FxSnapshot | actorId | `apps/accounting/prisma/schema.prisma:1208` |
| accounting | FieldCollectionPosting | actorId | `apps/accounting/prisma/schema.prisma:1261` |
| accounting | FinancialAccountEntry | actorId | `apps/accounting/prisma/schema.prisma:1351` |
| accounting | FinancialAccountReconciliation | countedById | `apps/accounting/prisma/schema.prisma:1371` |
| accounting | ImportShipment | poId | `apps/accounting/prisma/schema.prisma:1389` |
| accounting | ImportShipment | forwarderSupplierId | `apps/accounting/prisma/schema.prisma:1396` |
| accounting | ImportShipment | brokerSupplierId | `apps/accounting/prisma/schema.prisma:1397` |
| accounting | ImportShipment | createdById | `apps/accounting/prisma/schema.prisma:1407` |
| accounting | ImportShipmentLine | poLineId | `apps/accounting/prisma/schema.prisma:1424` |
| accounting | ImportShipmentLine | productId | `apps/accounting/prisma/schema.prisma:1425` |
| accounting | ShipmentStatusEvent | byId | `apps/accounting/prisma/schema.prisma:1480` |
| accounting | JournalEntryWorkflow | sourceId | `apps/accounting/prisma/schema.prisma:1494` |
| accounting | JournalEntryWorkflow | createdById | `apps/accounting/prisma/schema.prisma:1498` |
| accounting | JournalEntryWorkflow | submittedById | `apps/accounting/prisma/schema.prisma:1499` |
| accounting | JournalEntryWorkflow | approvedById | `apps/accounting/prisma/schema.prisma:1500` |
| accounting | JournalEntryWorkflow | rejectedById | `apps/accounting/prisma/schema.prisma:1501` |
| accounting | JournalEntryWorkflow | postedJournalId | `apps/accounting/prisma/schema.prisma:1503` |
| accounting | BankStatement | financialAccountId | `apps/accounting/prisma/schema.prisma:1517` |
| accounting | BankStatementLine | matchedSourceId | `apps/accounting/prisma/schema.prisma:1545` |
| audit-aggregator | AuditEvent | eventId | `apps/audit-aggregator/prisma/schema.prisma:34` |
| audit-aggregator | AuditEvent | aggregateId | `apps/audit-aggregator/prisma/schema.prisma:36` |
| audit-aggregator | AuditEvent | actorId | `apps/audit-aggregator/prisma/schema.prisma:37` |
| audit-aggregator | AuditEvent | correlationId | `apps/audit-aggregator/prisma/schema.prisma:38` |
| audit-aggregator | AuditEvent | organizationId | `apps/audit-aggregator/prisma/schema.prisma:58` |
| audit-aggregator | AuditLog | userId | `apps/audit-aggregator/prisma/schema.prisma:86` |
| audit-aggregator | AuditLog | entityId | `apps/audit-aggregator/prisma/schema.prisma:89` |
| audit-aggregator | AuditLog | correlationId | `apps/audit-aggregator/prisma/schema.prisma:93` |
| audit-aggregator | DeadLetterMessage | eventId | `apps/audit-aggregator/prisma/schema.prisma:119` |
| audit-aggregator | DeadLetterMessage | correlationId | `apps/audit-aggregator/prisma/schema.prisma:121` |
| crm | Account | territoryId | `apps/crm/prisma/schema.prisma:144` |
| crm | Account | repId | `apps/crm/prisma/schema.prisma:145` |
| crm | Account | priceListId | `apps/crm/prisma/schema.prisma:179` |
| crm | VisitPlan | repId | `apps/crm/prisma/schema.prisma:211` |
| crm | VisitPlan | territoryId | `apps/crm/prisma/schema.prisma:212` |
| crm | Visit | repId | `apps/crm/prisma/schema.prisma:249` |
| crm | Visit | orderId | `apps/crm/prisma/schema.prisma:277` |
| crm | CustomerAssignment | repId | `apps/crm/prisma/schema.prisma:312` |
| crm | CustomerAssignment | territoryId | `apps/crm/prisma/schema.prisma:314` |
| crm | CustomerInteraction | repId | `apps/crm/prisma/schema.prisma:354` |
| crm | VisitProductDiscussion | productId | `apps/crm/prisma/schema.prisma:376` |
| crm | RepTarget | repId | `apps/crm/prisma/schema.prisma:391` |
| crm | RepTarget | territoryId | `apps/crm/prisma/schema.prisma:392` |
| crm | Lead | repId | `apps/crm/prisma/schema.prisma:414` |
| crm | Lead | convertedById | `apps/crm/prisma/schema.prisma:430` |
| crm | SupportTicket | assignedAgentId | `apps/crm/prisma/schema.prisma:492` |
| crm | TicketParticipant | userId | `apps/crm/prisma/schema.prisma:556` |
| crm | AuditLog | userId | `apps/crm/prisma/schema.prisma:573` |
| crm | AuditLog | entityId | `apps/crm/prisma/schema.prisma:576` |
| crm | AuditLog | correlationId | `apps/crm/prisma/schema.prisma:580` |
| crm | CustomerCreationRequest | actorId | `apps/crm/prisma/schema.prisma:629` |
| crm | FieldProposal | convertedId | `apps/crm/prisma/schema.prisma:677` |
| iam | User | createdById | `apps/iam/prisma/schema.prisma:59` |
| iam | AuditLog | entityId | `apps/iam/prisma/schema.prisma:156` |
| iam | AuditLog | correlationId | `apps/iam/prisma/schema.prisma:160` |
| iam | ElectronicSignature | entityId | `apps/iam/prisma/schema.prisma:177` |
| iam | Notification | providerMessageId | `apps/iam/prisma/schema.prisma:208` |
| iam | Notification | createdById | `apps/iam/prisma/schema.prisma:209` |
| iam | WorkspaceDraft | ownerId | `apps/iam/prisma/schema.prisma:241` |
| incentives | ProcessedEvent | ledgerId | `apps/incentives/prisma/schema.prisma:49` |
| incentives | IncentiveLedger | repId | `apps/incentives/prisma/schema.prisma:59` |
| incentives | IncentiveLedger | sourceEventId | `apps/incentives/prisma/schema.prisma:62` |
| incentives | IncentiveLedger | paymentId | `apps/incentives/prisma/schema.prisma:66` |
| incentives | IncentiveLedger | orderId | `apps/incentives/prisma/schema.prisma:67` |
| incentives | IncentiveLedger | accountId | `apps/incentives/prisma/schema.prisma:68` |
| incentives | RepScore | repId | `apps/incentives/prisma/schema.prisma:97` |
| incentives | AuditLog | userId | `apps/incentives/prisma/schema.prisma:114` |
| incentives | AuditLog | entityId | `apps/incentives/prisma/schema.prisma:117` |
| incentives | AuditLog | correlationId | `apps/incentives/prisma/schema.prisma:121` |
| inventory | StockBalance | productId | `apps/inventory/prisma/schema.prisma:78` |
| inventory | StockBalance | batchId | `apps/inventory/prisma/schema.prisma:79` |
| inventory | InventoryCostLayer | productId | `apps/inventory/prisma/schema.prisma:96` |
| inventory | InventoryCostLayer | batchId | `apps/inventory/prisma/schema.prisma:97` |
| inventory | InventoryCostLayer | warehouseId | `apps/inventory/prisma/schema.prisma:98` |
| inventory | InventoryCostLayer | sourceTransactionId | `apps/inventory/prisma/schema.prisma:103` |
| inventory | InventoryTransaction | productId | `apps/inventory/prisma/schema.prisma:112` |
| inventory | InventoryTransaction | batchId | `apps/inventory/prisma/schema.prisma:113` |
| inventory | InventoryTransaction | warehouseId | `apps/inventory/prisma/schema.prisma:114` |
| inventory | InventoryTransaction | customerId | `apps/inventory/prisma/schema.prisma:115` |
| inventory | InventoryTransaction | supplierId | `apps/inventory/prisma/schema.prisma:116` |
| inventory | InventoryTransaction | correlationId | `apps/inventory/prisma/schema.prisma:122` |
| inventory | InventoryTransaction | actorId | `apps/inventory/prisma/schema.prisma:123` |
| inventory | InventoryTransaction | reversalOfId | `apps/inventory/prisma/schema.prisma:137` |
| inventory | BlockedBatch | batchId | `apps/inventory/prisma/schema.prisma:155` |
| inventory | BlockedBatch | recallId | `apps/inventory/prisma/schema.prisma:156` |
| inventory | AdjustmentRequest | warehouseId | `apps/inventory/prisma/schema.prisma:171` |
| inventory | AdjustmentRequest | productId | `apps/inventory/prisma/schema.prisma:172` |
| inventory | AdjustmentRequest | batchId | `apps/inventory/prisma/schema.prisma:173` |
| inventory | AdjustmentRequest | resultingTransactionId | `apps/inventory/prisma/schema.prisma:184` |
| inventory | InventoryReservation | orderId | `apps/inventory/prisma/schema.prisma:192` |
| inventory | InventoryReservation | productId | `apps/inventory/prisma/schema.prisma:193` |
| inventory | InventoryReservation | batchId | `apps/inventory/prisma/schema.prisma:194` |
| inventory | InventoryReservation | warehouseId | `apps/inventory/prisma/schema.prisma:195` |
| inventory | InventoryReservation | customerId | `apps/inventory/prisma/schema.prisma:196` |
| inventory | Transfer | productId | `apps/inventory/prisma/schema.prisma:236` |
| inventory | Transfer | batchId | `apps/inventory/prisma/schema.prisma:237` |
| inventory | Transfer | actorId | `apps/inventory/prisma/schema.prisma:246` |
| inventory | AuditLog | userId | `apps/inventory/prisma/schema.prisma:260` |
| inventory | AuditLog | entityId | `apps/inventory/prisma/schema.prisma:263` |
| inventory | AuditLog | correlationId | `apps/inventory/prisma/schema.prisma:267` |
| inventory | ConsignmentAgreement | customerId | `apps/inventory/prisma/schema.prisma:282` |
| inventory | ConsignmentStock | customerId | `apps/inventory/prisma/schema.prisma:298` |
| inventory | ConsignmentStock | productId | `apps/inventory/prisma/schema.prisma:299` |
| inventory | ConsignmentStock | batchId | `apps/inventory/prisma/schema.prisma:300` |
| inventory | InventoryOutboxEvent | eventId | `apps/inventory/prisma/schema.prisma:345` |
| organization | Department | managerId | `apps/organization/prisma/schema.prisma:21` |
| organization | Employee | linkedUserId | `apps/organization/prisma/schema.prisma:114` |
| organization | Territory | assignedRepId | `apps/organization/prisma/schema.prisma:308` |
| organization | PayrollAdjustment | actorId | `apps/organization/prisma/schema.prisma:491` |
| organization | PayrollApproval | approverId | `apps/organization/prisma/schema.prisma:503` |
| organization | ExpenseClaim | employeeId | `apps/organization/prisma/schema.prisma:551` |
| organization | ExpenseClaim | departmentId | `apps/organization/prisma/schema.prisma:552` |
| organization | ExpenseClaim | managerId | `apps/organization/prisma/schema.prisma:557` |
| organization | CustomerGift | employeeId | `apps/organization/prisma/schema.prisma:617` |
| organization | CustomerGift | departmentId | `apps/organization/prisma/schema.prisma:618` |
| organization | CustomerGift | accountId | `apps/organization/prisma/schema.prisma:619` |
| organization | CustomerGift | managerId | `apps/organization/prisma/schema.prisma:625` |
| organization | CustomerGiftLine | productId | `apps/organization/prisma/schema.prisma:655` |
| organization | AuditLog | userId | `apps/organization/prisma/schema.prisma:667` |
| organization | AuditLog | entityId | `apps/organization/prisma/schema.prisma:670` |
| organization | AuditLog | correlationId | `apps/organization/prisma/schema.prisma:674` |
| products | Batch | recallId | `apps/products/prisma/schema.prisma:204` |
| products | BatchQcRecord | signatureId | `apps/products/prisma/schema.prisma:247` |
| products | AuditLog | userId | `apps/products/prisma/schema.prisma:328` |
| products | AuditLog | entityId | `apps/products/prisma/schema.prisma:331` |
| products | AuditLog | correlationId | `apps/products/prisma/schema.prisma:335` |
| products | ProductPriceHistory | actorId | `apps/products/prisma/schema.prisma:360` |
| sales | SalesOrder | accountId | `apps/sales/prisma/schema.prisma:60` |
| sales | SalesOrder | repId | `apps/sales/prisma/schema.prisma:62` |
| sales | SalesOrder | shippingRateId | `apps/sales/prisma/schema.prisma:72` |
| sales | SalesOrder | correlationId | `apps/sales/prisma/schema.prisma:90` |
| sales | SalesOrder | visitId | `apps/sales/prisma/schema.prisma:94` |
| sales | SalesOrderLine | productId | `apps/sales/prisma/schema.prisma:117` |
| sales | SalesOrderLine | requestedBatchId | `apps/sales/prisma/schema.prisma:127` |
| sales | OrderLineAllocation | batchId | `apps/sales/prisma/schema.prisma:152` |
| sales | OrderLineAllocation | warehouseId | `apps/sales/prisma/schema.prisma:153` |
| sales | SalesReturn | accountId | `apps/sales/prisma/schema.prisma:183` |
| sales | SalesReturn | repId | `apps/sales/prisma/schema.prisma:184` |
| sales | SalesReturn | actorId | `apps/sales/prisma/schema.prisma:187` |
| sales | SalesReturn | decidedById | `apps/sales/prisma/schema.prisma:189` |
| sales | SalesReturnLine | orderLineId | `apps/sales/prisma/schema.prisma:207` |
| sales | SalesReturnLine | productId | `apps/sales/prisma/schema.prisma:208` |
| sales | SalesReturnLine | batchId | `apps/sales/prisma/schema.prisma:210` |
| sales | SalesReturnLine | warehouseId | `apps/sales/prisma/schema.prisma:211` |
| sales | OrderApproval | approverId | `apps/sales/prisma/schema.prisma:225` |
| sales | Promotion | scopeId | `apps/sales/prisma/schema.prisma:318` |
| sales | Promotion | giftProductId | `apps/sales/prisma/schema.prisma:328` |
| sales | PromotionRedemption | orderId | `apps/sales/prisma/schema.prisma:368` |
| sales | PromotionRedemption | customerId | `apps/sales/prisma/schema.prisma:369` |
| sales | PriceRule | scopeId | `apps/sales/prisma/schema.prisma:397` |
| sales | OrderSaga | correlationId | `apps/sales/prisma/schema.prisma:458` |
| sales | AuditLog | userId | `apps/sales/prisma/schema.prisma:477` |
| sales | AuditLog | entityId | `apps/sales/prisma/schema.prisma:480` |
| sales | AuditLog | correlationId | `apps/sales/prisma/schema.prisma:484` |
| sales | PendingPayment | orderId | `apps/sales/prisma/schema.prisma:499` |
| sales | PendingPayment | eventId | `apps/sales/prisma/schema.prisma:500` |
| sales | PendingPayment | accountId | `apps/sales/prisma/schema.prisma:501` |
| sales | PendingCreditApplication | accountId | `apps/sales/prisma/schema.prisma:514` |
| sales | ProductPrice | productId | `apps/sales/prisma/schema.prisma:542` |
| sales | BlockedBatch | recallId | `apps/sales/prisma/schema.prisma:563` |
| sales | OrderRecallHold | orderId | `apps/sales/prisma/schema.prisma:574` |
| sales | OrderRecallHold | batchId | `apps/sales/prisma/schema.prisma:575` |
| sales | OrderRecallHold | recallId | `apps/sales/prisma/schema.prisma:577` |
| sales | ShipmentLeg | invoiceId | `apps/sales/prisma/schema.prisma:734` |
| sales | ShipmentLeg | paymentId | `apps/sales/prisma/schema.prisma:738` |

## جدول بلا createdAt (83)
- accounting.Invoice (apps/accounting/prisma/schema.prisma:102)
- accounting.InvoiceLine (apps/accounting/prisma/schema.prisma:218)
- accounting.InvoiceLineBatch (apps/accounting/prisma/schema.prisma:263)
- accounting.GeneralPurchaseRevision (apps/accounting/prisma/schema.prisma:311)
- accounting.Payment (apps/accounting/prisma/schema.prisma:376)
- accounting.LedgerEntry (apps/accounting/prisma/schema.prisma:452)
- accounting.CollectionMetric (apps/accounting/prisma/schema.prisma:474)
- accounting.Currency (apps/accounting/prisma/schema.prisma:489)
- accounting.ExchangeRate (apps/accounting/prisma/schema.prisma:499)
- accounting.SupplierLedgerEntry (apps/accounting/prisma/schema.prisma:523)
- accounting.ProcessedEvent (apps/accounting/prisma/schema.prisma:545)
- accounting.CancelledOrder (apps/accounting/prisma/schema.prisma:560)
- accounting.JournalLine (apps/accounting/prisma/schema.prisma:656)
- accounting.LandedCostItem (apps/accounting/prisma/schema.prisma:793)
- accounting.DepreciationEntry (apps/accounting/prisma/schema.prisma:860)
- accounting.CreditNote (apps/accounting/prisma/schema.prisma:912)
- accounting.DocumentSequence (apps/accounting/prisma/schema.prisma:938)
- accounting.PurchaseOrderLine (apps/accounting/prisma/schema.prisma:1036)
- accounting.PurchaseOrderReceipt (apps/accounting/prisma/schema.prisma:1056)
- accounting.VendorInvoiceLine (apps/accounting/prisma/schema.prisma:1118)
- accounting.ThreeWayMatch (apps/accounting/prisma/schema.prisma:1132)
- accounting.JobRun (apps/accounting/prisma/schema.prisma:1166)
- accounting.FinancialAccountReconciliation (apps/accounting/prisma/schema.prisma:1364)
- accounting.ImportShipmentLine (apps/accounting/prisma/schema.prisma:1421)
- accounting.ShipmentDocument (apps/accounting/prisma/schema.prisma:1440)
- accounting.RegulatoryClearance (apps/accounting/prisma/schema.prisma:1457)
- accounting.ShipmentStatusEvent (apps/accounting/prisma/schema.prisma:1474)
- audit-aggregator.AuditEvent (apps/audit-aggregator/prisma/schema.prisma:22)
- audit-aggregator.ProcessedEvent (apps/audit-aggregator/prisma/schema.prisma:76)
- crm.Visit (apps/crm/prisma/schema.prisma:227)
- crm.VisitProductDiscussion (apps/crm/prisma/schema.prisma:373)
- crm.CustomerContact (apps/crm/prisma/schema.prisma:519)
- crm.SupportCategory (apps/crm/prisma/schema.prisma:539)
- crm.TicketParticipant (apps/crm/prisma/schema.prisma:553)
- iam.Permission (apps/iam/prisma/schema.prisma:87)
- iam.UserRole (apps/iam/prisma/schema.prisma:101)
- iam.RolePermission (apps/iam/prisma/schema.prisma:114)
- iam.ProcessedEvent (apps/iam/prisma/schema.prisma:221)
- iam.SecurityPolicy (apps/iam/prisma/schema.prisma:229)
- iam.WorkspaceDraft (apps/iam/prisma/schema.prisma:239)
- iam.AiProviderSetting (apps/iam/prisma/schema.prisma:253)
- incentives.ProcessedEvent (apps/incentives/prisma/schema.prisma:46)
- incentives.RepScore (apps/incentives/prisma/schema.prisma:95)
- inventory.Warehouse (apps/inventory/prisma/schema.prisma:47)
- inventory.BinLocation (apps/inventory/prisma/schema.prisma:63)
- inventory.StockBalance (apps/inventory/prisma/schema.prisma:75)
- inventory.InventoryCostLayer (apps/inventory/prisma/schema.prisma:94)
- inventory.BlockedBatch (apps/inventory/prisma/schema.prisma:153)
- inventory.AdjustmentRequest (apps/inventory/prisma/schema.prisma:169)
- inventory.ProcessedEvent (apps/inventory/prisma/schema.prisma:214)
- inventory.ConsignmentAgreement (apps/inventory/prisma/schema.prisma:280)
- inventory.ConsignmentStock (apps/inventory/prisma/schema.prisma:295)
- inventory.JobRun (apps/inventory/prisma/schema.prisma:327)
- organization.JobTitle (apps/organization/prisma/schema.prisma:36)
- organization.Region (apps/organization/prisma/schema.prisma:51)
- organization.SalaryComponent (apps/organization/prisma/schema.prisma:390)
- organization.EmployeeCompensationAssignment (apps/organization/prisma/schema.prisma:404)
- organization.PayrollApproval (apps/organization/prisma/schema.prisma:500)
- organization.LookupTable (apps/organization/prisma/schema.prisma:515)
- organization.ExpenseClaimLine (apps/organization/prisma/schema.prisma:573)
- organization.CustomerGiftLine (apps/organization/prisma/schema.prisma:647)
- products.ProductCategory (apps/products/prisma/schema.prisma:37)
- products.ProductBrand (apps/products/prisma/schema.prisma:46)
- products.ProductManufacturer (apps/products/prisma/schema.prisma:55)
- products.ProductIngredient (apps/products/prisma/schema.prisma:163)
- products.ProductTemperatureProfile (apps/products/prisma/schema.prisma:180)
- products.JobRun (apps/products/prisma/schema.prisma:311)
- products.ProductPriceHistory (apps/products/prisma/schema.prisma:353)
- products.PriceListItem (apps/products/prisma/schema.prisma:402)
- sales.SalesOrderLine (apps/sales/prisma/schema.prisma:114)
- sales.OrderLineAllocation (apps/sales/prisma/schema.prisma:149)
- sales.SalesReturnLine (apps/sales/prisma/schema.prisma:204)
- sales.OrderApproval (apps/sales/prisma/schema.prisma:222)
- sales.DiscountApprovalLevel (apps/sales/prisma/schema.prisma:294)
- sales.PromotionRedemption (apps/sales/prisma/schema.prisma:365)
- sales.PriceRuleSetting (apps/sales/prisma/schema.prisma:445)
- sales.OrderSaga (apps/sales/prisma/schema.prisma:455)
- sales.ProcessedEvent (apps/sales/prisma/schema.prisma:468)
- sales.AccountCredit (apps/sales/prisma/schema.prisma:527)
- sales.ProductPrice (apps/sales/prisma/schema.prisma:540)
- sales.BlockedBatch (apps/sales/prisma/schema.prisma:560)
- sales.OrderRecallHold (apps/sales/prisma/schema.prisma:572)
- sales.JobRun (apps/sales/prisma/schema.prisma:765)

## جدول قابل للتعديل بلا updatedAt (heuristic) (86)
- accounting.Invoice (apps/accounting/prisma/schema.prisma:102)
- accounting.InvoiceLineBatch (apps/accounting/prisma/schema.prisma:263)
- accounting.GeneralPurchaseRevision (apps/accounting/prisma/schema.prisma:311)
- accounting.Payment (apps/accounting/prisma/schema.prisma:376)
- accounting.Currency (apps/accounting/prisma/schema.prisma:489)
- accounting.ExchangeRate (apps/accounting/prisma/schema.prisma:499)
- accounting.CancelledOrder (apps/accounting/prisma/schema.prisma:560)
- accounting.SupplierPayment (apps/accounting/prisma/schema.prisma:589)
- accounting.LandedCostVoucher (apps/accounting/prisma/schema.prisma:767)
- accounting.LandedCostItem (apps/accounting/prisma/schema.prisma:793)
- accounting.CreditNote (apps/accounting/prisma/schema.prisma:912)
- accounting.DocumentSequence (apps/accounting/prisma/schema.prisma:938)
- accounting.PurchaseOrder (apps/accounting/prisma/schema.prisma:1006)
- accounting.PurchaseOrderReceipt (apps/accounting/prisma/schema.prisma:1056)
- accounting.VendorInvoice (apps/accounting/prisma/schema.prisma:1077)
- accounting.ThreeWayMatch (apps/accounting/prisma/schema.prisma:1132)
- accounting.PaymentAllocation (apps/accounting/prisma/schema.prisma:1269)
- accounting.FinancialAccountReconciliation (apps/accounting/prisma/schema.prisma:1364)
- accounting.ShipmentDocument (apps/accounting/prisma/schema.prisma:1440)
- accounting.RegulatoryClearance (apps/accounting/prisma/schema.prisma:1457)
- accounting.JournalEntryWorkflow (apps/accounting/prisma/schema.prisma:1489)
- crm.Account (apps/crm/prisma/schema.prisma:132)
- crm.Visit (apps/crm/prisma/schema.prisma:227)
- crm.CustomerAssignment (apps/crm/prisma/schema.prisma:309)
- crm.FollowUp (apps/crm/prisma/schema.prisma:329)
- crm.CustomerInteraction (apps/crm/prisma/schema.prisma:350)
- crm.VisitProductDiscussion (apps/crm/prisma/schema.prisma:373)
- crm.CustomerContact (apps/crm/prisma/schema.prisma:519)
- crm.SupportCategory (apps/crm/prisma/schema.prisma:539)
- crm.TicketParticipant (apps/crm/prisma/schema.prisma:553)
- crm.CustomerCreationRequest (apps/crm/prisma/schema.prisma:627)
- crm.CustomerEventOutbox (apps/crm/prisma/schema.prisma:636)
- crm.VisitRescheduleRequest (apps/crm/prisma/schema.prisma:649)
- iam.Role (apps/iam/prisma/schema.prisma:74)
- iam.Permission (apps/iam/prisma/schema.prisma:87)
- iam.UserRole (apps/iam/prisma/schema.prisma:101)
- iam.RolePermission (apps/iam/prisma/schema.prisma:114)
- iam.Session (apps/iam/prisma/schema.prisma:126)
- iam.ElectronicSignature (apps/iam/prisma/schema.prisma:173)
- iam.Notification (apps/iam/prisma/schema.prisma:189)
- incentives.RuleSet (apps/incentives/prisma/schema.prisma:27)
- incentives.IncentiveLedger (apps/incentives/prisma/schema.prisma:57)
- inventory.Warehouse (apps/inventory/prisma/schema.prisma:47)
- inventory.BinLocation (apps/inventory/prisma/schema.prisma:63)
- inventory.InventoryCostLayer (apps/inventory/prisma/schema.prisma:94)
- inventory.InventoryTransaction (apps/inventory/prisma/schema.prisma:109)
- inventory.BlockedBatch (apps/inventory/prisma/schema.prisma:153)
- inventory.AdjustmentRequest (apps/inventory/prisma/schema.prisma:169)
- inventory.InventoryReservation (apps/inventory/prisma/schema.prisma:190)
- inventory.Transfer (apps/inventory/prisma/schema.prisma:232)
- inventory.ConsignmentAgreement (apps/inventory/prisma/schema.prisma:280)
- organization.JobTitle (apps/organization/prisma/schema.prisma:36)
- organization.Region (apps/organization/prisma/schema.prisma:51)
- organization.Branch (apps/organization/prisma/schema.prisma:64)
- organization.AttendanceRecord (apps/organization/prisma/schema.prisma:163)
- organization.Territory (apps/organization/prisma/schema.prisma:304)
- organization.CompensationProfile (apps/organization/prisma/schema.prisma:369)
- organization.SalaryComponent (apps/organization/prisma/schema.prisma:390)
- organization.EmployeeCompensationAssignment (apps/organization/prisma/schema.prisma:404)
- organization.PayrollPeriod (apps/organization/prisma/schema.prisma:421)
- organization.PayrollAdjustment (apps/organization/prisma/schema.prisma:485)
- organization.PayrollApproval (apps/organization/prisma/schema.prisma:500)
- organization.LookupTable (apps/organization/prisma/schema.prisma:515)
- products.ProductCategory (apps/products/prisma/schema.prisma:37)
- products.ProductBrand (apps/products/prisma/schema.prisma:46)
- products.ProductManufacturer (apps/products/prisma/schema.prisma:55)
- products.Product (apps/products/prisma/schema.prisma:65)
- products.UnitOfMeasure (apps/products/prisma/schema.prisma:128)
- products.ProductUomConversion (apps/products/prisma/schema.prisma:139)
- products.ProductIngredient (apps/products/prisma/schema.prisma:163)
- products.ProductTemperatureProfile (apps/products/prisma/schema.prisma:180)
- products.Batch (apps/products/prisma/schema.prisma:192)
- products.Supplier (apps/products/prisma/schema.prisma:264)
- products.SerializedUnit (apps/products/prisma/schema.prisma:284)
- products.ProductPriceHistory (apps/products/prisma/schema.prisma:353)
- sales.SalesOrder (apps/sales/prisma/schema.prisma:57)
- sales.OrderLineAllocation (apps/sales/prisma/schema.prisma:149)
- sales.SalesReturn (apps/sales/prisma/schema.prisma:180)
- sales.OrderApproval (apps/sales/prisma/schema.prisma:222)
- sales.PromotionRedemption (apps/sales/prisma/schema.prisma:365)
- sales.PendingPayment (apps/sales/prisma/schema.prisma:497)
- sales.PendingCreditApplication (apps/sales/prisma/schema.prisma:512)
- sales.BlockedBatch (apps/sales/prisma/schema.prisma:560)
- sales.OrderRecallHold (apps/sales/prisma/schema.prisma:572)
- sales.ShippingRate (apps/sales/prisma/schema.prisma:617)
- sales.ShippingZoneArea (apps/sales/prisma/schema.prisma:637)

## _soft-delete/archival fields present (info) (27)
- accounting.Currency
- accounting.Account
- accounting.FinancialAccount
- crm.Account
- crm.CustomerContact
- crm.SupportCategory
- iam.Session
- incentives.RuleSet
- inventory.Warehouse
- inventory.ConsignmentAgreement
- organization.Department
- organization.JobTitle
- organization.Branch
- organization.RepCoverage
- organization.Territory
- organization.CompensationProfile
- organization.SalaryComponent
- organization.LookupTable
- products.Product
- products.Supplier
- products.PriceList
- sales.PricingRule
- sales.DiscountApprovalLevel
- sales.PriceRule
- sales.ProductPrice
- sales.ShippingZone
- sales.ShippingZoneArea

## status كنص حر (String) بدل enum (7)
- accounting.LandedCostVoucher.status (apps/accounting/prisma/schema.prisma:781)
- accounting.ImportShipment.status (apps/accounting/prisma/schema.prisma:1390)
- accounting.JournalEntryWorkflow.status (apps/accounting/prisma/schema.prisma:1497)
- accounting.BankStatement.status (apps/accounting/prisma/schema.prisma:1522)
- crm.VisitRescheduleRequest.status (apps/crm/prisma/schema.prisma:656)
- crm.FieldProposal.status (apps/crm/prisma/schema.prisma:670)
- sales.PendingCreditApplication.status (apps/sales/prisma/schema.prisma:516)

## FK بلا index (23)
- accounting.PurchaseOrderLine.purchaseOrderId (apps/accounting/prisma/schema.prisma:1046)
- accounting.VendorInvoiceLine.vendorInvoiceId (apps/accounting/prisma/schema.prisma:1127)
- accounting.ThreeWayMatch.purchaseOrderId (apps/accounting/prisma/schema.prisma:1152)
- accounting.ShipmentDocument.shipmentId (apps/accounting/prisma/schema.prisma:1452)
- crm.Visit.addressId (apps/crm/prisma/schema.prisma:228)
- crm.FollowUp.visitId (apps/crm/prisma/schema.prisma:342)
- crm.Lead.accountId (apps/crm/prisma/schema.prisma:436)
- crm.SupportTicket.customCategoryId (apps/crm/prisma/schema.prisma:503)
- crm.FieldProposal.accountId (apps/crm/prisma/schema.prisma:665)
- iam.UserRole.roleId (apps/iam/prisma/schema.prisma:108)
- iam.RolePermission.permissionId (apps/iam/prisma/schema.prisma:120)
- incentives.IncentiveLedger.ruleSetVersion (apps/incentives/prisma/schema.prisma:85)
- inventory.Transfer.sourceWarehouseId (apps/inventory/prisma/schema.prisma:249)
- inventory.Transfer.destWarehouseId (apps/inventory/prisma/schema.prisma:250)
- inventory.ConsignmentStock.agreementId (apps/inventory/prisma/schema.prisma:310)
- organization.JobTitle.departmentId (apps/organization/prisma/schema.prisma:43)
- organization.EmploymentContract.jobTitleId (apps/organization/prisma/schema.prisma:275)
- organization.EmploymentContract.departmentId (apps/organization/prisma/schema.prisma:276)
- organization.EmploymentContract.previousContractId (apps/organization/prisma/schema.prisma:277)
- products.Product.categoryId (apps/products/prisma/schema.prisma:100)
- products.Product.brandId (apps/products/prisma/schema.prisma:101)
- products.Product.manufacturerId (apps/products/prisma/schema.prisma:102)
- products.SerializedUnit.parentId (apps/products/prisma/schema.prisma:295)