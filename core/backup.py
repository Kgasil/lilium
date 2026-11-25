"""Bounded versioned history exchange. Merge only; never overwrite snapshots."""
from contextlib import closing
from datetime import datetime, date
import json
import re
from uuid import UUID
from .metrics import metrics, MAX_ROWS
from .store import MAX_SNAPSHOTS

MAX_BACKUP = 16 * 1024 * 1024
MAX_CENTS = MAX_ROWS * 99_999_999_999
NOTES = ["Result is revenue minus supplied costs, not necessarily accounting profit.",
         "Margin is unavailable when revenue is zero."]


def require(ok):
    if not ok:
        raise ValueError("Invalid Lilium history backup.")


def keys(value, expected):
    require(isinstance(value, dict) and set(value) == set(expected))


def validate_analysis(a):
    keys(a, ("schema_version", "currency", "rows", "totals", "months", "notes"))
    require(a["schema_version"] == "1.0" and a["currency"] == "BRL" and a["notes"] == NOTES)
    require(type(a["rows"]) is int and 1 <= a["rows"] <= MAX_ROWS)
    require(isinstance(a["months"], list) and 1 <= len(a["months"]) <= a["rows"])
    revenue = cost = 0
    last = ""
    for m in a["months"]:
        keys(m, ("month", "revenue_cents", "cost_cents", "result_cents", "margin_pct"))
        month = m["month"]
        require(isinstance(month, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}", month) and month > last)
        date.fromisoformat(month + "-01")
        last = month
        r, c = m["revenue_cents"], m["cost_cents"]
        require(type(r) is int and type(c) is int and 0 <= r <= MAX_CENTS and 0 <= c <= MAX_CENTS)
        require(type(m["result_cents"]) is int and m == {"month": month, **metrics(r, c)})
        revenue += r
        cost += c
    require(max(revenue, cost) <= a["rows"] * 99_999_999_999)
    keys(a["totals"], ("revenue_cents", "cost_cents", "result_cents", "margin_pct"))
    require(all(type(a["totals"][k]) is int for k in ("revenue_cents", "cost_cents", "result_cents")))
    require(a["totals"] == metrics(revenue, cost))


def validate_item(item):
    keys(item, ("id", "created_at", "analysis"))
    key, stamp = item["id"], item["created_at"]
    require(isinstance(key, str) and len(key) == 36 and str(UUID(key)) == key)
    require(isinstance(stamp, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}\+00:00", stamp))
    datetime.fromisoformat(stamp)
    validate_analysis(item["analysis"])


def unique_pairs(pairs):
    obj = {}
    for k, v in pairs:
        require(k not in obj)
        obj[k] = v
    return obj


def decode(raw):
    require(isinstance(raw, bytes) and len(raw) <= MAX_BACKUP)
    try:
        b = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs)
        keys(b, ("kind", "schema_version", "snapshots"))
        require(b["kind"] == "lilium.history" and b["schema_version"] == "1.0")
        items = b["snapshots"]
        require(isinstance(items, list) and len(items) <= MAX_SNAPSHOTS)
        seen = set()
        for item in items:
            validate_item(item)
            require(item["id"] not in seen)
            seen.add(item["id"])
        return items
    except (ValueError, TypeError, RecursionError, OverflowError):
        raise ValueError("Invalid Lilium history backup.") from None


def export_history(store):
    with closing(store.connect()) as db:
        rows = db.execute("SELECT * FROM snapshots ORDER BY created_at, id").fetchall()
    items = [{"id": r["id"], "created_at": r["created_at"], "analysis": json.loads(r["payload"])} for r in rows]
    raw = json.dumps({"kind": "lilium.history", "schema_version": "1.0", "snapshots": items}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    decode(raw)
    return raw


def merge_history(store, raw):
    items = decode(raw)
    added = skipped = 0
    with closing(store.connect()) as db, db:
        db.execute("BEGIN IMMEDIATE")
        count = db.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0]
        for item in items:
            row = db.execute("SELECT created_at, payload FROM snapshots WHERE id=?", (item["id"],)).fetchone()
            if row is not None:
                require(row["created_at"] == item["created_at"] and json.loads(row["payload"]) == item["analysis"])
                skipped += 1
                continue
            require(count + added < MAX_SNAPSHOTS)
            db.execute("INSERT INTO snapshots VALUES (?, ?, ?)", (item["id"], item["created_at"], json.dumps(item["analysis"], ensure_ascii=False, separators=(",", ":"))))
            added += 1
    return {"added": added, "skipped": skipped}
