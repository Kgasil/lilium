"""Bounded local spreadsheet ingestion and non-destructive quality diagnostics."""
from datetime import date, datetime, time
from decimal import Decimal
from io import BytesIO
from zipfile import ZipFile
from openpyxl import load_workbook
from .metrics import MAX_BYTES, MAX_ROWS, SCHEMA, DataError, analyze_csv

XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
MAX_EXPANDED = 12 * 1024 * 1024
MAX_ISSUES = 100


def excel_value(cell):
    v = cell.value
    if v is None:
        return ''
    if isinstance(v, datetime) and v.time() == time():
        return v.date().isoformat()
    if isinstance(v, date) and not isinstance(v, datetime):
        return v.isoformat()
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return format(Decimal(str(v)), 'f')
    return str(v).strip()


def xlsx_to_csv(raw):
    if len(raw) > MAX_BYTES:
        raise DataError('size_limit', 'Maximum input size is 1 MiB.')
    try:
        with ZipFile(BytesIO(raw)) as archive:
            parts = archive.infolist()
            if len(parts) > 100 or sum(p.file_size for p in parts) > MAX_EXPANDED:
                raise DataError('archive_limit', 'Workbook exceeds archive limits.')
            if any('externallinks/' in p.filename.lower() or 'vbaproject' in p.filename.lower() for p in parts):
                raise DataError('unsafe_workbook', 'External links and macros are not supported.')
        book = load_workbook(BytesIO(raw), read_only=False, data_only=False, keep_links=False)
        try:
            if len(book.sheetnames) != 1 or len(book.worksheets) != 1:
                raise DataError('sheet_count', 'Use a workbook with exactly one worksheet.')
            sheet = book.worksheets[0]
            if sheet.max_row > MAX_ROWS + 1 or sheet.max_column != 3:
                raise DataError('sheet_dimensions', 'Use at most 10,000 data rows and exactly three columns.')
            lines = []
            for row_num, cells in enumerate(sheet.iter_rows(), 1):
                if any(c.data_type == 'f' for c in cells):
                    raise DataError('formula', 'Replace formulas with values before import.', row_num)
                values = [excel_value(c) for c in cells]
                if any(',' in v or '\r' in v or '\n' in v for v in values):
                    raise DataError('cell_format', 'Cells must not contain commas or line breaks.', row_num)
                lines.append(','.join(values))
            result = '\n'.join(lines).encode('utf-8')
            if len(result) > MAX_BYTES:
                raise DataError('size_limit', 'Converted data exceeds 1 MiB.')
            return result
        finally:
            book.close()
    except DataError:
        raise
    except Exception:
        raise DataError('workbook', 'Invalid or unsupported XLSX workbook.') from None


def normalize(raw, media):
    return xlsx_to_csv(raw) if media == XLSX else raw


def quality(raw):
    if len(raw) > MAX_BYTES:
        raise DataError('size_limit', 'Maximum input size is 1 MiB.')
    try:
        lines = raw.decode('utf-8-sig').splitlines()
    except UnicodeDecodeError:
        raise DataError('encoding', 'Use UTF-8 CSV.') from None
    if not lines or lines[0].strip().lower() != SCHEMA:
        raise DataError('header', 'Expected date,revenue,cost.', 1)
    if not 1 <= len(lines)-1 <= MAX_ROWS:
        raise DataError('row_limit', 'Use 1–10,000 data rows.')
    invalid = duplicates = zero_revenue = 0
    seen = set()
    issues = []
    def issue(row, severity, code):
        if len(issues) < MAX_ISSUES:
            issues.append({'row': row, 'severity': severity, 'code': code})
    for row, line in enumerate(lines[1:], 2):
        try:
            result = analyze_csv((SCHEMA+'\n'+line).encode('utf-8'))['totals']
        except DataError as exc:
            invalid += 1
            issue(row, 'error', exc.code)
            continue
        key = (line.split(',')[0].strip(), result['revenue_cents'], result['cost_cents'])
        if key in seen:
            duplicates += 1
            issue(row, 'warning', 'possible_duplicate')
        seen.add(key)
        if result['revenue_cents'] == 0:
            zero_revenue += 1
            issue(row, 'warning', 'zero_revenue')
    total = len(lines)-1
    return {'rows': total, 'valid_rows': total-invalid, 'invalid_rows': invalid,
            'possible_duplicates': duplicates, 'zero_revenue_rows': zero_revenue,
            'can_analyze': invalid == 0, 'issues': issues,
            'issues_truncated': invalid+duplicates+zero_revenue > len(issues)}
