"""Deterministic BRL analytics. No network, persistence or AI."""
from collections import defaultdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import re

MAX_BYTES = 1_048_576
MAX_ROWS = 10_000
SCHEMA = "date,revenue,cost"
AMOUNT = re.compile(r"[0-9]{1,9}(?:\.[0-9]{1,2})?")
ISO_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


class DataError(ValueError):
    def __init__(self, code, message, row=None):
        super().__init__(message)
        self.code = code
        self.row = row


def cents(value):
    if not AMOUNT.fullmatch(value):
        raise ValueError("amount")
    whole, _, fraction = value.partition(".")
    return int(whole) * 100 + int(fraction.ljust(2, "0") or "0")


def metrics(revenue, cost):
    result = revenue - cost
    margin = None if revenue == 0 else str(
        (Decimal(result) * 100 / Decimal(revenue)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    )
    return {"revenue_cents": revenue, "cost_cents": cost,
            "result_cents": result, "margin_pct": margin}


def analyze_csv(raw: bytes):
    if len(raw) > MAX_BYTES:
        raise DataError("size_limit", "Maximum input size is 1 MiB.")
    try:
        lines = raw.decode("utf-8-sig").splitlines()
    except UnicodeDecodeError:
        raise DataError("encoding", "Use UTF-8 CSV.") from None
    if not lines or lines[0].strip().lower() != SCHEMA:
        raise DataError("header", "Expected date,revenue,cost.", 1)
    if not 1 <= len(lines) - 1 <= MAX_ROWS:
        raise DataError("row_limit", "Use 1–10,000 data rows.")
    monthly = defaultdict(lambda: [0, 0])
    revenue = cost = 0
    for row, line in enumerate(lines[1:], 2):
        fields = [x.strip() for x in line.split(",")]
        if len(fields) != 3:
            raise DataError("columns", "Expected exactly three columns.", row)
        day, r, c = fields
        try:
            if not ISO_DATE.fullmatch(day):
                raise ValueError("date")
            parsed = date.fromisoformat(day)
        except ValueError:
            raise DataError("date", "Use a valid YYYY-MM-DD date.", row) from None
        try:
            rv, cv = cents(r), cents(c)
        except ValueError:
            raise DataError("amount", "Use nonnegative amounts with up to two decimals.", row) from None
        revenue += rv
        cost += cv
        key = parsed.isoformat()[:7]
        monthly[key][0] += rv
        monthly[key][1] += cv
    return {"schema_version": "1.0", "currency": "BRL", "rows": len(lines)-1,
            "totals": metrics(revenue, cost), "months": [
                {"month": month, **metrics(*monthly[month])} for month in sorted(monthly)
            ], "notes": ["Result is revenue minus supplied costs, not necessarily accounting profit.",
                         "Margin is unavailable when revenue is zero."]}
