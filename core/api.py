"""Run on loopback only; no authentication in this development preview."""
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware
from .metrics import MAX_BYTES, DataError, analyze_csv

app = FastAPI(title="Lilium Core", version="0.1.0")
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])


def error(code, message, status, row=None):
    return JSONResponse({"error": {"code": code, "message": message, "row": row}}, status_code=status)


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0", "mode": "local-preview"}


@app.get("/", include_in_schema=False)
def workspace():
    return FileResponse(Path(__file__).with_name("workspace.html"), media_type="text/html")


@app.post("/api/v1/analyze")
async def analyze(request: Request):
    origin = request.headers.get("origin")
    if origin and origin != str(request.base_url).rstrip("/"):
        return error("origin", "Only same-origin requests are allowed.", 403)
    if request.headers.get("content-type", "").split(";", 1)[0].strip().lower() != "text/csv":
        return error("media_type", "Send raw UTF-8 CSV as text/csv.", 415)
    raw = bytearray()
    async for chunk in request.stream():
        if len(raw) + len(chunk) > MAX_BYTES:
            return error("size_limit", "Maximum input size is 1 MiB.", 413)
        raw.extend(chunk)
    try:
        return JSONResponse(analyze_csv(bytes(raw)))
    except DataError as exc:
        return error(exc.code, str(exc), 413 if exc.code == "size_limit" else 422, exc.row)
