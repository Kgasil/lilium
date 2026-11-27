"""Bounded synthetic workload; not a production benchmark."""
import unittest
import time
from core.metrics import analyze_csv
from core.imports import quality, normalize


class AssuranceLimits(unittest.TestCase):
    def test_max_rows_exact_and_bounded(self):
        raw = b"date,revenue,cost\n" + b"2026-01-01,999999999.99,999999999.98\n" * 10000
        start = time.monotonic()
        result = analyze_csv(raw)
        self.assertEqual(result["totals"]["revenue_cents"], 999999999990000)
        self.assertEqual(result["totals"]["result_cents"], 10000)
        q = quality(raw)
        self.assertEqual(q["valid_rows"], 10000)
        self.assertEqual(q["possible_duplicates"], 9999)
        self.assertEqual(len(q["issues"]), 100)
        self.assertTrue(q["issues_truncated"])
        elapsed = time.monotonic() - start
        print(f"Bounded 10k-row analysis + diagnostic: {elapsed:.3f}s")
        self.assertLess(elapsed, 15, "Synthetic workload exceeded generous CI regression bound")

    def test_cross_format_exact(self):
        canonical = b"date,revenue,cost\n2026-01-01,100.01,100.02"
        localized = b"custo;data;receita\n100,02;01/01/2026;100,01"
        self.assertEqual(analyze_csv(normalize(localized, "text/csv")), analyze_csv(canonical))
