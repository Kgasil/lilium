"""Local SQLite history: only validated aggregate snapshots, never raw CSV."""
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
import json
import sqlite3
import uuid

MAX_SNAPSHOTS = 200


class HistoryFull(ValueError):
    pass


class HistoryStore:
    def __init__(self, path):
        self.path = Path(path)

    def connect(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA secure_delete=ON')
        db.execute('CREATE TABLE IF NOT EXISTS snapshots (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, payload TEXT NOT NULL)')
        return db

    def save(self, analysis):
        key = str(uuid.uuid4())
        stamp = datetime.now(timezone.utc).isoformat(timespec='microseconds')
        payload = json.dumps(analysis, ensure_ascii=False, separators=(',', ':'))
        with closing(self.connect()) as db, db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute('SELECT COUNT(*) FROM snapshots').fetchone()[0] >= MAX_SNAPSHOTS:
                raise HistoryFull('History is full. Delete a snapshot first.')
            db.execute('INSERT INTO snapshots VALUES (?, ?, ?)', (key, stamp, payload))
        return {'id': key, 'created_at': stamp, 'analysis': analysis}

    def list(self):
        with closing(self.connect()) as db:
            rows = db.execute('SELECT * FROM snapshots ORDER BY created_at DESC, id DESC').fetchall()
        return [{'id': row['id'], 'created_at': row['created_at'], 'rows': data['rows'],
                 'totals': data['totals']} for row in rows for data in [json.loads(row['payload'])]]

    def get(self, key):
        with closing(self.connect()) as db:
            row = db.execute('SELECT * FROM snapshots WHERE id=?', (key,)).fetchone()
        return None if row is None else {'id': row['id'], 'created_at': row['created_at'], 'analysis': json.loads(row['payload'])}

    def delete(self, key):
        with closing(self.connect()) as db, db:
            return db.execute('DELETE FROM snapshots WHERE id=?', (key,)).rowcount == 1
