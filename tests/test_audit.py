import unittest
from decimal import Decimal

from audit import reconcile


class AuditTests(unittest.TestCase):
    def test_matches_and_mismatches(self):
        invoices = [("100", Decimal("25.00")), ("101", Decimal("10.00"))]
        deposits = [("100", Decimal("25.00")), ("101", Decimal("9.00"))]
        results = {row["invoice_id"]: row["status"] for row in reconcile(invoices, deposits)}
        self.assertEqual("matched", results["100"])
        self.assertEqual("amount_mismatch", results["101"])

    def test_missing_records(self):
        results = reconcile([("100", Decimal("25.00"))], [("200", Decimal("5.00"))])
        statuses = {row["invoice_id"]: row["status"] for row in results}
        self.assertEqual("missing_deposit", statuses["100"])
        self.assertEqual("missing_invoice", statuses["200"])


if __name__ == "__main__":
    unittest.main()
