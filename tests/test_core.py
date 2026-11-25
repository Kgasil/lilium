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

    def test_workspace_security_headers(self):
        response = self.client.get('/')
        self.assertEqual(response.headers['x-frame-options'], 'DENY')
        self.assertEqual(response.headers['referrer-policy'], 'no-referrer')
        self.assertIn("connect-src 'self'", response.headers['content-security-policy'])
        self.assertIn("frame-ancestors 'none'", response.headers['content-security-policy'])
        self.assertIn("script-src 'self';", response.headers['content-security-policy'])
        self.assertIn('src="/assets/workspace.js"', response.text)
        self.assertNotIn("<script>", response.text)

    def test_workspace_controller_asset(self):
        response = self.client.get("/assets/workspace.js")
        self.assertEqual(response.status_code, 200)
        self.assertIn("workspace-loading", response.text)
        self.assertIn("application/javascript", response.headers["content-type"])
        self.assertEqual(response.headers["x-content-type-options"], "nosniff")

    def test_dashboard_asset(self):
        r = self.client.get('/assets/dashboard.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('LiliumDashboard', r.text)
        self.assertIn('application/javascript', r.headers['content-type'])
        self.assertEqual(r.headers['cache-control'], 'no-store')
        self.assertEqual(self.client.get('/health').json()['version'], '0.14.0')

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

    def test_strategy_asset(self):
        r = self.client.get('/assets/strategy.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('LiliumStrategy', r.text)
        self.assertIn('application/javascript', r.headers['content-type'])
        self.assertEqual(r.headers['cache-control'], 'no-store')

    def test_reports_asset(self):
        r = self.client.get('/assets/reports.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('LiliumReports', r.text)
        self.assertIn('application/javascript', r.headers['content-type'])
        self.assertEqual(r.headers['cache-control'], 'no-store')

    def test_forecast_asset(self):
        r = self.client.get('/assets/forecast.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('LiliumForecast', r.text)
        self.assertIn('application/javascript', r.headers['content-type'])
        self.assertEqual(r.headers['cache-control'], 'no-store')

    def test_flow_asset(self):
        r = self.client.get('/assets/flow.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('LiliumFlow', r.text)
        self.assertIn('application/javascript', r.headers['content-type'])
        self.assertEqual(r.headers['cache-control'], 'no-store')

    def test_connect_asset(self):
        r = self.client.get('/assets/connect.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('LiliumConnect', r.text)
        self.assertIn('application/javascript', r.headers['content-type'])
        self.assertEqual(r.headers['cache-control'], 'no-store')

    def test_starter_asset(self):
        r = self.client.get('/assets/starter.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('LiliumStarter', r.text)
        self.assertIn('application/javascript', r.headers['content-type'])
        self.assertEqual(r.headers['cache-control'], 'no-store')

    def test_copilot_asset(self):
        r = self.client.get('/assets/copilot.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('LiliumCopilot', r.text)
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


class DesktopSessionApiTests(unittest.TestCase):
    def setUp(self):
        from unittest.mock import patch
        from tempfile import TemporaryDirectory
        from pathlib import Path
        from core.store import HistoryStore
        from core.session import new_token
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.token = new_token()
        for name, value in (("session_token", self.token), ("history", HistoryStore(Path(tmp.name) / "test.db"))):
            p = patch.object(app.state, name, value)
            p.start()
            self.addCleanup(p.stop)
        self.client = TestClient(app, base_url="http://localhost")
        self.headers = {"X-Lilium-Session": self.token}

    def test_sensitive_reads_and_writes_rejected(self):
        for method, path in (("GET", "/api/v1/history"), ("GET", "/api/v1/backup"),
                             ("POST", "/api/v1/analyze"), ("POST", "/api/v1/history"),
                             ("POST", "/api/v1/quality"), ("POST", "/api/v1/backup/merge")):
            with self.subTest(path=path):
                r = self.client.request(method, path)
                self.assertEqual(r.status_code, 403)
                self.assertEqual(r.headers["cache-control"], "no-store")

    def test_authorized_api(self):
        self.assertEqual(self.client.get("/api/v1/history", headers=self.headers).json(), {"items": []})
        r = self.client.post("/api/v1/analyze", content=SAMPLE, headers={**self.headers, "Content-Type": "text/csv", "Origin": "http://localhost"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers["cache-control"], "no-store")

    def test_cross_origin_with_token(self):
        self.assertEqual(self.client.get("/api/v1/history", headers={**self.headers, "Origin": "https://example.com"}).status_code, 403)
        self.assertEqual(self.client.get("/api/v1/history", headers={**self.headers, "Sec-Fetch-Site": "same-site"}).status_code, 403)

    def test_old_token_rejected(self):
        from core.session import new_token
        app.state.session_token = new_token()
        self.assertEqual(self.client.get("/api/v1/history", headers=self.headers).status_code, 403)

    def test_public_static_health_no_secret(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        r = self.client.get("/health")
        self.assertTrue(r.json()["session_required"])
        self.assertNotIn(self.token, r.text)


if __name__ == '__main__':
    unittest.main()
