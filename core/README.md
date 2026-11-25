# Lilium Core v0.1.0 — local development preview

**Strategy & Growth · Estratégia e Crescimento**

## Windows
Install Python 3.11 or 3.12 with the Python launcher (py). Download and extract the repository, then run `start-lilium.bat` in the root. It creates a local virtual environment and installs dependencies (internet required for setup). Open http://127.0.0.1:8000 manually. Press Ctrl+C to stop. This is not an installer or production release. Use synthetic data only.

Manual commands (PowerShell, from repository root):

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m uvicorn core.api:app --host 127.0.0.1 --port 8000
```

## API contract
- GET /health — service status and version.
- GET / — local Workspace preview.
- POST /api/v1/analyze — raw UTF-8 text/csv body. Exact three columns: date,revenue,cost. BRL, dot decimal, nonnegative amounts, max 9 integer digits and 2 fractional digits. ISO date, 1–10,000 rows, 1 MiB. No quoted fields or additional columns. Accepts UTF-8 BOM.
- Returns schema version, currency, row count, totals, sorted monthly totals, and notes. Monetary values are integer cents; margin is a decimal percentage string rounded half-up to 2 decimal places or null for zero revenue.
- 422 validation errors include safe error code and row when applicable; 413 input too large; 415 unsupported media; 403 invalid Origin.
- /openapi.json — machine-readable API definition.

Example:
```csv
date,revenue,cost
2026-01-01,10000,6000
2026-02-01,11200,7440
2026-03-01,12000,7800
```

## Boundaries
The UI sends CSV only to the loopback API. No persistence, telemetry, account, external AI or payments. Do not expose the service to the LAN or internet; there is no authentication. Host and Origin validation are limited defenses, not a security audit. Result is revenue minus supplied costs, not necessarily accounting profit. No XLSX support, multi-tenant isolation, desktop packaging or production deployment yet. Twelve unittest cases passed in a local Linux Python environment; Windows installation and full browser UI remain untested.

Next: persistent local datasets, XLSX import, data-quality feedback, richer dashboard and export.
