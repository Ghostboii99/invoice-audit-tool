# Invoice Audit Tool

A small Python utility for reconciling invoice exports against deposit-statement records. It highlights missing records, amount mismatches, and duplicates before a manual review.

## Input format

Both CSV files require `invoice_id` and `amount` columns.

```csv
invoice_id,amount
543021,1500.00
543022,875.50
```

## Usage

```bash
python audit.py invoices.csv deposits.csv --output audit_report.csv
```

Possible results: `matched`, `amount_mismatch`, `missing_deposit`, `missing_invoice`, and `duplicate`.

This tool intentionally keeps a human in the loop. Flags are review prompts, not accounting conclusions.

