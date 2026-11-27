import unittest
from io import BytesIO
from datetime import date
from zipfile import ZipFile
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from openpyxl import Workbook
from fastapi.testclient import TestClient
from core.api import app
from core.imports import XLSX, quality, xlsx_to_csv, normalize
from core.metrics import analyze_csv, DataError
from core.store import HistoryStore


def workbook(rows, extra=False):
    w = Workbook()
    for row in rows:
        w.active.append(row)
    if extra:
        w.create_sheet('Other')
    f = BytesIO(); w.save(f); w.close(); return f.getvalue()


HEADER = ['date', 'revenue', 'cost']
GOOD = workbook([HEADER, [date(2026, 1, 1), 100.1, 60.02]])


class ImportTests(unittest.TestCase):
    def test_localized_csv(self):
        raw = 'custo;data;receita\n60,02;01/01/2026;100,10'.encode()
        result = analyze_csv(normalize(raw, 'text/csv'))
        self.assertEqual(result['totals']['result_cents'], 4008)

    def test_localized_reject_ambiguous_amounts(self):
        for value in ('1.000,00', '1.00', '-1', '1,001'):
            raw = f'data;receita;custo\n01/01/2026;{value};1'.encode()
            self.assertFalse(quality(normalize(raw, 'text/csv'))['can_analyze'])

    def test_localized_invalid_date_and_duplicate(self):
        raw = b'data;receita;custo\n01/01/2026;1,00;0\n2026-01-01;1;0\n30/02/2026;1;0'
        q = quality(normalize(raw, 'text/csv'))
        self.assertEqual((q['possible_duplicates'], q['invalid_rows']), (1, 1))

    def test_reordered_excel_and_csv(self):
        raw = workbook([['cost','date','revenue'], [60.02, date(2026,1,1),100.1]])
        self.assertEqual(analyze_csv(normalize(raw, XLSX))['totals']['result_cents'], 4008)
        self.assertEqual(analyze_csv(normalize(b'cost,date,revenue\n60.02,2026-01-01,100.10', 'text/csv'))['totals']['result_cents'], 4008)

    def test_localized_quality_api(self):
        client = TestClient(app, base_url='http://localhost')
        response = client.post('/api/v1/analyze', content=b'data;receita;custo\n01/01/2026;100,10;60,02', headers={'Content-Type':'text/csv'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['totals']['result_cents'], 4008)

    def test_localized_row_limit(self):
        raw = b'data;receita;custo\n' + b'01/01/2026;1;0\n' * 10001
        with self.assertRaises(DataError) as e:
            normalize(raw, 'text/csv')
        self.assertEqual(e.exception.code, 'row_limit')

    def test_duplicate_archive_entry(self):
        import warnings
        f = BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with ZipFile(f, 'w') as z:
                z.writestr('duplicate.xml', 'x')
                z.writestr('duplicate.xml', 'y')
        with self.assertRaises(DataError) as e:
            xlsx_to_csv(f.getvalue())
        self.assertEqual(e.exception.code, 'unsafe_workbook')

    def test_excel_exact(self):
        self.assertEqual(analyze_csv(xlsx_to_csv(GOOD))['totals']['result_cents'], 4008)

    def test_formula(self):
        with self.assertRaises(DataError) as e:
            xlsx_to_csv(workbook([HEADER, ['2026-01-01', '=1+1', 1]]))
        self.assertEqual(e.exception.code, 'formula')
        self.assertEqual(e.exception.row, 2)

    def test_multiple_sheets(self):
        with self.assertRaises(DataError) as e:
            xlsx_to_csv(workbook([HEADER, ['2026-01-01', 1, 1]], extra=True))
        self.assertEqual(e.exception.code, 'sheet_count')

    def test_archive_limit(self):
        f = BytesIO()
        from zipfile import ZIP_DEFLATED
        with ZipFile(f, 'w', compression=ZIP_DEFLATED) as z:
            z.writestr('oversize.xml', 'x' * (12*1024*1024+1))
        with self.assertRaises(DataError) as e:
            xlsx_to_csv(f.getvalue())
        self.assertEqual(e.exception.code, 'archive_limit')

    def test_corrupt(self):
        with self.assertRaises(DataError) as e:
            xlsx_to_csv(b'bad')
        self.assertEqual(e.exception.code, 'workbook')

    def test_quality_counts(self):
        raw = b'date,revenue,cost\n2026-01-01,1,2\n2026-01-01,1.00,2.0\n2026-02-30,1,2\n2026-02-01,0,1\n2026-02-01,-1,2'
        q = quality(raw)
        self.assertEqual((q['valid_rows'], q['invalid_rows'], q['possible_duplicates'], q['zero_revenue_rows']), (3, 2, 1, 1))
        self.assertFalse(q['can_analyze'])
        self.assertEqual([x['row'] for x in q['issues']], [3, 4, 5, 6])

    def test_warnings_not_blocking(self):
        q = quality(b'date,revenue,cost\n2026-01-01,0,1\n2026-01-01,0,1')
        self.assertTrue(q['can_analyze'])
        self.assertEqual(q['possible_duplicates'], 1)

    def test_issue_cap(self):
        q = quality(b'date,revenue,cost\n'+b'bad\n'*101)
        self.assertEqual(q['invalid_rows'], 101)
        self.assertEqual(len(q['issues']), 100)
        self.assertTrue(q['issues_truncated'])

    def test_api_quality_excel_save(self):
        client = TestClient(app, base_url='http://localhost')
        h = {'Content-Type': XLSX}
        self.assertTrue(client.post('/api/v1/quality', content=GOOD, headers=h).json()['can_analyze'])
        expected = client.post('/api/v1/analyze', content=GOOD, headers=h).json()
        with TemporaryDirectory() as t, patch.object(app.state, 'history', HistoryStore(Path(t)/'db.sqlite3')):
            r = client.post('/api/v1/history', content=GOOD, headers=h)
            self.assertEqual(r.status_code, 201)
            self.assertEqual(r.json()['analysis'], expected)

    def test_api_reject_invalid_excel(self):
        client = TestClient(app, base_url='http://localhost')
        raw = workbook([HEADER, ['2026-01-01', -1, 0]])
        h = {'Content-Type': XLSX}
        self.assertFalse(client.post('/api/v1/quality', content=raw, headers=h).json()['can_analyze'])
        self.assertEqual(client.post('/api/v1/analyze', content=raw, headers=h).status_code, 422)
