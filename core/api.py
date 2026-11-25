"""Run on loopback only; no authentication in this development preview. Desktop configures its own history path."""
from pathlib import Path
import sqlite3
from uuid import UUID
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, Response
from starlette.middleware.trustedhost import TrustedHostMiddleware
from .metrics import MAX_BYTES, DataError, analyze_csv
from .store import HistoryStore, HistoryFull
from .backup import MAX_BACKUP, export_history, merge_history
from .imports import XLSX, normalize, quality

app = FastAPI(title="Lilium Core", version="0.14.0", docs_url=None, redoc_url=None)
app.state.history = HistoryStore(Path(__file__).resolve().parent.parent / "data" / "lilium.sqlite3")
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])


def error(code, message, status, row=None):
    return JSONResponse({"error": {"code": code, "message": message, "row": row}}, status_code=status)


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.14.0", "mode": "local-preview"}


@app.get("/", include_in_schema=False)
def workspace():
    return FileResponse(Path(__file__).with_name("workspace.html"), media_type="text/html", headers={
        "Cache-Control": "no-store",
        "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'",
        "X-Frame-Options": "DENY", "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "no-referrer",
    })


@app.get("/assets/dashboard.js", include_in_schema=False)
def dashboard_asset():
    return FileResponse(Path(__file__).with_name("dashboard.js"), media_type="application/javascript", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


@app.get("/assets/finance.js", include_in_schema=False)
def finance_asset():
    return FileResponse(Path(__file__).with_name("finance.js"), media_type="application/javascript", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


@app.get("/assets/sales.js", include_in_schema=False)
def sales_asset():
    return FileResponse(Path(__file__).with_name("sales.js"), media_type="application/javascript", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


@app.get("/assets/operations.js", include_in_schema=False)
def operations_asset():
    return FileResponse(Path(__file__).with_name("operations.js"), media_type="application/javascript", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


@app.get("/assets/strategy.js", include_in_schema=False)
def strategy_asset():
    return FileResponse(Path(__file__).with_name("strategy.js"), media_type="application/javascript", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


@app.get("/assets/reports.js", include_in_schema=False)
def reports_asset():
    return FileResponse(Path(__file__).with_name("reports.js"), media_type="application/javascript", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


@app.get("/assets/forecast.js", include_in_schema=False)
def forecast_asset():
    return FileResponse(Path(__file__).with_name("forecast.js"), media_type="application/javascript", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


@app.get("/assets/flow.js", include_in_schema=False)
def flow_asset():
    return FileResponse(Path(__file__).with_name("flow.js"), media_type="application/javascript", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


@app.get("/assets/connect.js", include_in_schema=False)
def connect_asset():
    return FileResponse(Path(__file__).with_name("connect.js"), media_type="application/javascript", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


@app.get("/assets/copilot.js", include_in_schema=False)
def copilot_asset():
    return FileResponse(Path(__file__).with_name("copilot.js"), media_type="application/javascript", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


@app.get("/assets/workspace.js", include_in_schema=False)
def workspace_asset():
    return FileResponse(Path(__file__).with_name("workspace.js"), media_type="application/javascript", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


async def analyze_input(request: Request, diagnostic=False):
    origin = request.headers.get("origin")
    if origin and origin != str(request.base_url).rstrip("/"):
        return error("origin", "Only same-origin requests are allowed.", 403)
    media = request.headers.get("content-type", "").split(";", 1)[0].strip().lower()
    if media not in {"text/csv", XLSX}:
        return error("media_type", "Send raw UTF-8 CSV or XLSX.", 415)
    raw = bytearray()
    async for chunk in request.stream():
        if len(raw) + len(chunk) > MAX_BYTES:
            return error("size_limit", "Maximum input size is 1 MiB.", 413)
        raw.extend(chunk)
    try:
        normalized = normalize(bytes(raw), media)
        return quality(normalized) if diagnostic else analyze_csv(normalized)
    except DataError as exc:
        return error(exc.code, str(exc), 413 if exc.code == "size_limit" else 422, exc.row)


@app.post("/api/v1/quality")
async def data_quality(request: Request):
    result = await analyze_input(request, diagnostic=True)
    return result if isinstance(result, JSONResponse) else JSONResponse(result)


@app.post("/api/v1/analyze")
async def analyze(request: Request):
    result = await analyze_input(request)
    return result if isinstance(result, JSONResponse) else JSONResponse(result)


@app.post("/api/v1/history", status_code=201)
async def save_history(request: Request):
    result = await analyze_input(request)
    if isinstance(result, JSONResponse):
        return result
    try:
        return JSONResponse(app.state.history.save(result), status_code=201)
    except HistoryFull:
        return error("history_full", "History is full. Delete a snapshot first.", 409)
    except (sqlite3.Error, OSError):
        return error("storage", "Local storage unavailable.", 503)


@app.get("/api/v1/history")
def list_history():
    try:
        return {"items": app.state.history.list()}
    except (sqlite3.Error, OSError):
        return error("storage", "Local storage unavailable.", 503)


@app.get("/api/v1/history/{key}")
def get_history(key: UUID):
    try:
        item = app.state.history.get(str(key))
        return item if item is not None else error("not_found", "Snapshot not found.", 404)
    except (sqlite3.Error, OSError):
        return error("storage", "Local storage unavailable.", 503)


@app.delete("/api/v1/history/{key}")
def delete_history(key: UUID, request: Request):
    origin = request.headers.get("origin")
    if origin and origin != str(request.base_url).rstrip("/"):
        return error("origin", "Only same-origin requests are allowed.", 403)
    try:
        return {"deleted": True} if app.state.history.delete(str(key)) else error("not_found", "Snapshot not found.", 404)
    except (sqlite3.Error, OSError):
        return error("storage", "Local storage unavailable.", 503)



@app.get("/api/v1/backup")
def get_backup():
    try:
        return Response(export_history(app.state.history), media_type="application/json",
                        headers={"Cache-Control": "no-store", "Content-Disposition": 'attachment; filename="lilium-history.json"'})
    except ValueError:
        return error("backup_invalid", "History cannot be exported in this format or exceeds 16 MiB.", 422)
    except (sqlite3.Error, OSError):
        return error("storage", "Local storage unavailable.", 503)


@app.post("/api/v1/backup/merge")
async def restore_backup(request: Request):
    if request.headers.get("origin") != str(request.base_url).rstrip("/"):
        return error("origin", "Only same-origin requests are allowed.", 403)
    if request.headers.get("content-type", "").split(";", 1)[0].strip().lower() != "application/json":
        return error("media_type", "Send a Lilium history JSON backup.", 415)
    raw = bytearray()
    async for chunk in request.stream():
        if len(raw) + len(chunk) > MAX_BACKUP:
            return error("size_limit", "Maximum backup size is 16 MiB.", 413)
        raw.extend(chunk)
    try:
        return merge_history(app.state.history, bytes(raw))
    except ValueError:
        return error("backup_invalid", "Invalid backup, conflicting ID or history limit exceeded. No snapshots imported.", 422)
    except (sqlite3.Error, OSError):
        return error("storage", "Local storage unavailable.", 503)
