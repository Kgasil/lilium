import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from core.api import app
from core.store import HistoryStore

CSV = b'date,revenue,cost\n2026-01-01,100,60'
HEADERS = {'Content-Type': 'text/csv', 'Origin': 'http://localhost'}


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'db.sqlite3'
        self.store = HistoryStore(self.path)
        self.patch = patch.object(app.state, 'history', self.store)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.client = TestClient(app, base_url='http://localhost')

    def save(self):
        r = self.client.post('/api/v1/history', content=CSV, headers=HEADERS)
        self.assertEqual(r.status_code, 201)
        return r.json()

    def test_analysis_not_saved(self):
        self.assertEqual(self.client.post('/api/v1/analyze', content=CSV, headers=HEADERS).status_code, 200)
        self.assertFalse(self.path.exists())
        self.assertEqual(self.client.get('/api/v1/history').json(), {'items': []})

    def test_save_and_reopen(self):
        item = self.save()
        self.assertEqual(HistoryStore(self.path).get(item['id']), item)
        self.assertEqual(item['analysis']['totals']['result_cents'], 4000)
        self.assertNotIn(CSV, self.path.read_bytes())

    def test_list(self):
        a, b = self.save(), self.save()
        self.assertEqual([x['id'] for x in self.client.get('/api/v1/history').json()['items']], [b['id'], a['id']])

    def test_get_delete(self):
        item = self.save(); url = '/api/v1/history/' + item['id']
        self.assertEqual(self.client.get(url).json(), item)
        self.assertEqual(self.client.delete(url, headers=HEADERS).status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.delete(url).status_code, 404)

    def test_invalid_not_saved(self):
        self.assertEqual(self.client.post('/api/v1/history', content=b'bad', headers=HEADERS).status_code, 422)
        self.assertFalse(self.path.exists())

    def test_cross_origin(self):
        item = self.save(); evil = {**HEADERS, 'Origin': 'https://evil.example'}
        self.assertEqual(self.client.post('/api/v1/history', content=CSV, headers=evil).status_code, 403)
        self.assertEqual(self.client.delete('/api/v1/history/'+item['id'], headers=evil).status_code, 403)

    def test_limit(self):
        with patch('core.store.MAX_SNAPSHOTS', 1):
            self.save()
            self.assertEqual(self.client.post('/api/v1/history', content=CSV, headers=HEADERS).status_code, 409)

    def test_storage_error(self):
        with patch.object(self.store, 'list', side_effect=OSError('private path')):
            r = self.client.get('/api/v1/history')
            self.assertEqual(r.status_code, 503)
            self.assertNotIn('private path', r.text)
