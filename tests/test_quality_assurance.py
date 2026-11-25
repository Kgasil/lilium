"""Cross-feature regression using temporary history and an explicit Desktop token."""
from contextlib import closing
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from core.api import app
from core.session import new_token
from core.store import HistoryStore

CSV = b'date,revenue,cost\n2026-01-01,100,60'
BASE = 'http://localhost'


class QualityAssuranceTests(unittest.TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = HistoryStore(Path(tmp.name) / 'qa.sqlite3')
        self.token = new_token()
        for name, value in [('session_token', self.token), ('history', self.store)]:
            p = patch.object(app.state, name, value)
            p.start()
            self.addCleanup(p.stop)
        self.client = TestClient(app, base_url=BASE)
        self.headers = {'X-Lilium-Session': self.token, 'Origin': BASE}

    def save(self):
        response = self.client.post('/api/v1/history', content=CSV, headers={**self.headers, 'Content-Type': 'text/csv'})
        self.assertEqual(response.status_code, 201)
        return response.json()

    def get(self, path):
        return self.client.get(path, headers=self.headers)

    def merge(self, raw):
        return self.client.post('/api/v1/backup/merge', content=raw, headers={**self.headers, 'Content-Type': 'application/json'})

    def corrupt(self, item, payload):
        with closing(self.store.connect()) as db, db:
            db.execute('UPDATE snapshots SET payload=? WHERE id=?', (payload, item['id']))

    def assert_corrupt(self, response):
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()['error']['code'], 'history_corrupt')
        self.assertEqual(response.headers['cache-control'], 'no-store')
        self.assertNotIn(str(self.store.path), response.text)

    def test_authorized_backup_recovery_and_restart(self):
        item = self.save()
        backup = self.get('/api/v1/backup').content
        self.assertEqual(self.merge(backup).json(), {'added': 0, 'skipped': 1})
        self.assertEqual(self.client.delete('/api/v1/history/' + item['id'], headers=self.headers).status_code, 200)
        self.assertEqual(self.merge(backup).json(), {'added': 1, 'skipped': 0})
        app.state.history = HistoryStore(self.store.path)
        app.state.session_token = new_token()
        self.assertEqual(self.get('/api/v1/history').status_code, 403)
        self.headers['X-Lilium-Session'] = app.state.session_token
        self.assertEqual(self.get('/api/v1/history/' + item['id']).json(), item)

    def test_unauthorized_never_creates_database(self):
        for method, path in [('GET', '/api/v1/history'), ('GET', '/api/v1/backup'), ('POST', '/api/v1/history'), ('POST', '/api/v1/backup/merge')]:
            r = self.client.request(method, path, content=CSV)
            self.assertEqual(r.status_code, 403)
        self.assertFalse(self.store.path.exists())

    def test_valid_token_cross_site_rejected(self):
        r = self.client.get('/api/v1/history', headers={**self.headers, 'Origin': 'https://example.com'})
        self.assertEqual(r.status_code, 403)
        r = self.client.get('/api/v1/history', headers={**self.headers, 'Sec-Fetch-Site': 'same-site'})
        self.assertEqual(r.status_code, 403)
        self.assertFalse(self.store.path.exists())

    def test_bad_json_history_and_export(self):
        item = self.save()
        self.corrupt(item, 'private-invalid-json')
        for path in ['/api/v1/history', '/api/v1/history/' + item['id'], '/api/v1/backup']:
            r = self.get(path)
            self.assert_corrupt(r)
            self.assertNotIn('private-invalid-json', r.text)
        with closing(self.store.connect()) as db:
            self.assertEqual(db.execute('SELECT payload FROM snapshots').fetchone()[0], 'private-invalid-json')

    def test_inconsistent_financial_totals_rejected(self):
        item = self.save()
        item['analysis']['totals']['result_cents'] = 999
        self.corrupt(item, json.dumps(item['analysis']))
        self.assert_corrupt(self.get('/api/v1/history'))
        self.assert_corrupt(self.get('/api/v1/history/' + item['id']))

    def test_merge_conflict_with_corruption_rolls_back(self):
        first = self.save()
        second = self.save()
        raw = self.get('/api/v1/backup').content
        self.store.delete(first['id'])
        self.corrupt(second, 'bad')
        self.assert_corrupt(self.merge(raw))
        self.assertIsNone(self.store.get(first['id']))
        with closing(self.store.connect()) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM snapshots').fetchone()[0], 1)

    def test_bad_backup_does_not_modify_valid_history(self):
        item = self.save()
        r = self.merge(b'{"schema_version":"1.0","kind":"lilium.history","snapshots":[{}]}')
        self.assertEqual(r.status_code, 422)
        self.assertEqual(self.get('/api/v1/history/' + item['id']).json(), item)
