import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from core.backup import decode, export_history, merge_history
from core.metrics import analyze_csv
from core.store import HistoryStore


class BackupTests(unittest.TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.source = HistoryStore(Path(tmp.name) / 'source.db')
        self.dest = HistoryStore(Path(tmp.name) / 'dest.db')
        self.item = self.source.save(analyze_csv(b'date,revenue,cost\n2026-01-01,100,60'))
        self.raw = export_history(self.source)

    def test_roundtrip(self):
        self.assertEqual(merge_history(self.dest, self.raw), {'added': 1, 'skipped': 0})
        self.assertEqual(self.dest.get(self.item['id']), self.item)

    def test_idempotent(self):
        merge_history(self.dest, self.raw)
        self.assertEqual(merge_history(self.dest, self.raw), {'added': 0, 'skipped': 1})

    def test_invalid_total(self):
        b = json.loads(self.raw)
        b['snapshots'][0]['analysis']['totals']['result_cents'] = 1
        with self.assertRaises(ValueError):
            merge_history(self.dest, json.dumps(b).encode())
        self.assertEqual(self.dest.list(), [])

    def test_duplicate_json_key(self):
        with self.assertRaises(ValueError):
            decode(b'{"kind":"x","kind":"y"}')

    def test_duplicate_snapshot(self):
        b = json.loads(self.raw)
        b['snapshots'] *= 2
        with self.assertRaises(ValueError):
            decode(json.dumps(b).encode())

    def test_conflict_rollback(self):
        original = self.dest.save(analyze_csv(b'date,revenue,cost\n2026-01-01,1,1'))
        b = json.loads(self.raw)
        conflict = {**self.item, 'id': original['id']}
        b['snapshots'].append(conflict)
        with self.assertRaises(ValueError):
            merge_history(self.dest, json.dumps(b).encode())
        self.assertEqual(len(self.dest.list()), 1)
        self.assertEqual(self.dest.get(original['id']), original)

    def test_limit_rollback(self):
        self.source.save(self.item['analysis'])
        original = self.dest.save(self.item['analysis'])
        with patch('core.backup.MAX_SNAPSHOTS', 2), self.assertRaises(ValueError):
            merge_history(self.dest, export_history(self.source))
        self.assertEqual(len(self.dest.list()), 1)
        self.assertEqual(self.dest.get(original['id']), original)

    def test_empty(self):
        self.assertEqual(decode(export_history(self.dest)), [])

    def test_wrong_version(self):
        b = json.loads(self.raw)
        b['schema_version'] = '2'
        with self.assertRaises(ValueError):
            decode(json.dumps(b).encode())
