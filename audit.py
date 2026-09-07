"""Reconcile invoice and deposit CSV exports."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from decimal import Decimal, InvalidOperation


def load_records(path: str) -> list[tuple[str, Decimal]]:
    records = []
    with open(path, newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            invoice_id = row.get("invoice_id", "").strip()
            if not invoice_id:
                raise ValueError(f"Missing invoice_id in {path}")
            try:
                amount = Decimal(row.get("amount", "").replace(",", "")).quantize(Decimal("0.01"))
            except InvalidOperation as exc:
                raise ValueError(f"Invalid amount for {invoice_id} in {path}") from exc
            records.append((invoice_id, amount))
    return records


def reconcile(invoices, deposits):
    invoice_counts = Counter(item[0] for item in invoices)
    deposit_counts = Counter(item[0] for item in deposits)
    invoice_map = dict(invoices)
    deposit_map = dict(deposits)
    results = []
    for invoice_id in sorted(invoice_map.keys() | deposit_map.keys()):
        if invoice_counts[invoice_id] > 1 or deposit_counts[invoice_id] > 1:
            status = "duplicate"
        elif invoice_id not in deposit_map:
            status = "missing_deposit"
        elif invoice_id not in invoice_map:
            status = "missing_invoice"
        elif invoice_map[invoice_id] != deposit_map[invoice_id]:
            status = "amount_mismatch"
        else:
            status = "matched"
        results.append({
            "invoice_id": invoice_id,
            "invoice_amount": invoice_map.get(invoice_id, ""),
            "deposit_amount": deposit_map.get(invoice_id, ""),
            "status": status,
        })
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("invoices")
    parser.add_argument("deposits")
    parser.add_argument("--output", default="audit_report.csv")
    args = parser.parse_args()
    results = reconcile(load_records(args.invoices), load_records(args.deposits))
    with open(args.output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=results[0].keys() if results else ["invoice_id", "invoice_amount", "deposit_amount", "status"])
        writer.writeheader()
        writer.writerows(results)
    print(f"Audited {len(results)} invoice IDs; saved {args.output}")


if __name__ == "__main__":
    main()

