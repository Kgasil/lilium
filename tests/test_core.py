import unittest
from fastapi.testclient import TestClient
from core.metrics import analyze_csv, DataError, MAX_BYTES
from core.api import app

HEADER = b"date,revenue,cost\n"
SAMPLE = HEADER + b"2026-02-01,0.10,0.02\n2026-01-01,100,60\n2026-02-02,20,30"


class CoreTests(unittest.TestCase):
    def test_totals_and_sorted_months(self):
        result = analyze_csv(SAMPLE)
        self.assertEqual(result['totals'], {'revenue_cents': 12010, 'cost_cents': 9002, 'result_cents': 3008, 'margin_pct': '25.05'})
        self.assertEqual([m['month'] for m in result['months']], ['2026-01', '2026-02'])
        self.assertEqual(result['rows'], 3)

    def test_zero_revenue(self):
        self.assertIsNone(analyze_csv(HEADER+b'2026-01-01,0,1')['totals']['margin_pct'])

    def test_loss(self):
        self.assertEqual(analyze_csv(HEADER+b'2026-01-01,1,2')['totals']['result_cents'], -100)

    def test_bom_and_crlf(self):
        self.assertEqual(analyze_csv(b'\xef\xbb\xbf'+SAMPLE.replace(b'\n', b'\r\n'))['rows'], 3)

    def test_bad_inputs(self):
        for raw, code in [(b'wrong\n1', 'header'), (HEADER, 'row_limit'), (HEADER+b'2026-02-30,1,2', 'date'), (HEADER+b'2026-01-01,-1,2', 'amount'), (HEADER+b'2026-01-01,1.001,2', 'amount'), (HEADER+b'2026-01-01,1,2,3', 'columns'), (HEADER+b'\xff', 'encoding'), (b'x'*(MAX_BYTES+1), 'size_limit')]:
            with self.subTest(code=code), self.assertRaises(DataError) as raised:
                analyze_csv(raw)
            self.assertEqual(raised.exception.code, code)

    def test_row_cap(self):
        with self.assertRaises(DataError) as raised:
            analyze_csv(HEADER+b'2026-01-01,1,1\n'*10001)
        self.assertEqual(raised.exception.code, 'row_limit')


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, base_url='http://localhost')

    def test_health_and_workspace(self):
        self.assertEqual(self.client.get('/health').json()['status'], 'ok')
        self.assertIn('Workspace', self.client.get('/').text)

    def test_dashboard_asset(self):
        r = self.client.get('/assets/dashboard.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('LiliumDashboard', r.text)
        self.assertIn('application/javascript', r.headers['content-type'])
        self.assertEqual(r.headers['cache-control'], 'no-store')
        self.assertEqual(self.client.get('/health').json()['version'], '0.7.0')

    def test_finance_asset(self):
        r = self.client.get('/assets/finance.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('LiliumFinance', r.text)
        self.assertIn('application/javascript', r.headers['content-type'])
        self.assertEqual(r.headers['cache-control'], 'no-store')

    def test_sales_asset(self):
        r = self.client.get('/assets/sales.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('LiliumSales', r.text)
        self.assertIn('application/javascript', r.headers['content-type'])
        self.assertEqual(r.headers['cache-control'], 'no-store')

    def test_operations_asset(self):
        r = self.client.get('/assets/operations.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('LiliumOperations', r.text)
        self.assertIn('application/javascript', r.headers['content-type'])
        self.assertEqual(r.headers['cache-control'], 'no-store')

    def test_success(self):
        response = self.client.post('/api/v1/analyze', content=SAMPLE, headers={'Content-Type':'text/csv','Origin':'http://localhost'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), analyze_csv(SAMPLE))

    def test_invalid(self):
        response = self.client.post('/api/v1/analyze', content=HEADER+b'2026-02-30,1,2', headers={'Content-Type':'text/csv'})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['error']['row'], 2)

    def test_wrong_media(self):
        self.assertEqual(self.client.post('/api/v1/analyze', json={}).status_code, 415)

    def test_size_cap(self):
        self.assertEqual(self.client.post('/api/v1/analyze', content=b'x'*(MAX_BYTES+1), headers={'Content-Type':'text/csv'}).status_code, 413)

    def test_origin_and_host(self):
        self.assertEqual(self.client.post('/api/v1/analyze', content=SAMPLE, headers={'Content-Type':'text/csv','Origin':'https://evil.example'}).status_code, 403)
        self.assertEqual(self.client.get('/health', headers={'Host':'evil.example'}).status_code, 400)


if __name__ == '__main__':
    unittest.main()
