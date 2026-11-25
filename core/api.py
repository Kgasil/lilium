"""Run on loopback only; no authentication in this development preview."""
from pathlib import Path
import sqlite3
from uuid import UUID
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware
from .metrics import MAX_BYTES, DataError, analyze_csv
from .store import HistoryStore, HistoryFull
from .imports import XLSX, normalize, quality

app = FastAPI(title="Lilium Core", version="0.3.0", docs_url=None, redoc_url=None)
app.state.history = HistoryStore(Path(__file__).resolve().parent.parent / "data" / "lilium.sqlite3")
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])


def error(code, message, status, row=None):
    return JSONResponse({"error": {"code": code, "message": message, "row": row}}, status_code=status)


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.3.0", "mode": "local-preview"}


@app.get("/", include_in_schema=False)
def workspace():
    return FileResponse(Path(__file__).with_name("workspace.html"), media_type="text/html")


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
