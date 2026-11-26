"""Fixed synthetic v0.14.0 Insights baselines; no external services."""
import unittest
from core.metrics import analyze_csv, DataError

# (id, first month revenue BRL, monthly step BRL, cost %, total revenue,
# total cost, result in cents). Independent of the Insights implementation.
CASES = (
    ('retail', 3065, 248, 68, 3651300, 2482884, 1168416),
    ('services', 9990, 1580, 48, 14679000, 7045920, 7633080),
    ('industry', 6990, 410, 74, 7767000, 5747580, 2019420),
    ('restaurant', 2376, 108, 72, 2527200, 1819584, 707616),
    ('ecommerce', 5829, 468, 66, 6930900, 4574394, 2356506),
)


def amount(cents):
    return f'{cents // 100}.{cents % 100:02d}'


def fixture(case):
    _, first, step, pct, *_ = case
    rows = []
    for i in range(9):
        revenue = (first + i * step) * 100
        cost = revenue * pct // 100
        rows.append(f'2026-{i+1:02d}-05,{amount(revenue)},{amount(cost)}')
    return rows


def encode(rows):
    return ('date,revenue,cost\n' + '\n'.join(rows)).encode('utf-8')


class AcceptanceReferenceTests(unittest.TestCase):
    def test_all_five_totals(self):
        for case in CASES:
            name, _, _, pct, revenue, cost, result = case
            with self.subTest(scenario=name):
                report = analyze_csv(encode(fixture(case)))
                self.assertEqual(report['rows'], 9)
                self.assertEqual(report['totals'], {
                    'revenue_cents': revenue, 'cost_cents': cost,
                    'result_cents': result, 'margin_pct': f'{100-pct}.00',
                })

    def test_monthly_order_and_values(self):
        for case in CASES:
            name, first, step, pct, *_ = case
            with self.subTest(scenario=name):
                report = analyze_csv(encode(list(reversed(fixture(case)))))
                self.assertEqual(len(report['months']), 9)
                for i, month in enumerate(report['months']):
                    revenue = (first + i * step) * 100
                    cost = revenue * pct // 100
                    self.assertEqual(month, {
                        'month': f'2026-{i+1:02d}', 'revenue_cents': revenue,
                        'cost_cents': cost, 'result_cents': revenue-cost,
                        'margin_pct': f'{100-pct}.00',
                    })

    def test_invalid_row_after_valid_history(self):
        for case in CASES:
            with self.subTest(scenario=case[0]):
                with self.assertRaises(DataError) as raised:
                    analyze_csv(encode(fixture(case) + ['2026-10-05,-1,2']))
                self.assertEqual(raised.exception.code, 'amount')
                self.assertEqual(raised.exception.row, 11)


if __name__ == '__main__':
    unittest.main()
