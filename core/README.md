# Lilium Core v0.4.0 — local development preview

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
- POST /api/v1/analyze — raw UTF-8 text/csv or XLSX body (`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`). Exact three columns: date,revenue,cost. BRL, dot decimal, nonnegative amounts, max 9 integer digits and 2 fractional digits. ISO date, 1–10,000 rows, 1 MiB. No quoted fields or additional columns. Accepts UTF-8 BOM.
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

## Professional Workspace
- Navigation between overview, import/quality and local history. Responsive graphite/rose/gold layout with local JavaScript served by the API.
- Inclusive month filters over validated monthly aggregates. Totals are recomputed from the selected months; margin uses integer arithmetic with half-up rounding. Missing months are not invented. An empty interval has no indicators.
- Revenue/cost chart displays up to the latest 24 months in the filter; the accessible table contains all selected months. Export monthly CSV for the active period or full JSON for the original analysis. Saving always persists the complete analysis, not a filtered subset.
- Run the dashboard tests with `node tests/dashboard.test.js` (Node.js optional for development only; no Node dependency for users). Fourteen pure JS checks passed in a V8 execution environment. The Python regression suite now includes an additional asset-route test; the full Python suite and browser UI were not rerun for v0.4.

## Smart Import & Data Quality
- `POST /api/v1/quality` — diagnostic only, no persistence. Counts valid/invalid rows, possible duplicates and zero-revenue rows; returns row number and issue code (first 100 issues). Invalid rows block analysis; warnings do not. No automatic corrections or deduplication.
- XLSX: exactly one worksheet, three columns with the same CSV header, ISO dates or native Excel date values, numeric BRL values. Replace formulas with values; macros and external links are unsupported. Input 1 MiB, expanded archive 12 MiB, at most 100 archive entries, 10,000 data rows. Corrupt or unsupported files are rejected. This is a restricted importer, not a general Excel editor; XLS/XLSM are unsupported.
- Structural errors (including invalid header, formula or unsupported workbook) stop the diagnostic. The original file is never persisted. All calculations use the existing deterministic core after normalization.

## Local history
- POST /api/v1/history — validates the same CSV or XLSX input and explicitly saves a consolidated snapshot; 201 with identifier and timestamp.
- GET /api/v1/history — list up to 200 saved snapshots (latest first).
- GET /api/v1/history/{id} — reopen a saved analysis; DELETE on the same path removes it.
- SQLite is built into Python. Database: `data/lilium.sqlite3` (ignored by Git). Only aggregated metrics are stored, not the raw CSV. Analyze alone does not save anything. No app-level encryption or secure-erasure guarantee; do not use confidential data.
- Full history returns 409; storage failure returns 503 without exposing local paths. Back up exported JSON if needed; deleting a snapshot does not delete external exports or backups.

## Boundaries
The UI sends CSV or XLSX only to the loopback API. Optional local persistence; no telemetry, account, external AI or payments. Do not expose the service to the LAN or internet; there is no authentication. Host and Origin validation are limited defenses, not a security audit. Result is revenue minus supplied costs, not necessarily accounting profit. No general spreadsheet mapping, multi-tenant isolation, desktop packaging or production deployment yet. Thirty unittest cases passed in the previous v0.3 local Linux Python environment; the v0.4 Python regression run, Windows installation and full browser UI remain untested.

Next: Lilium Finance — operational finance metrics and scenario tools. SQLite is chosen for the lightweight local preview; analytical and multi-organization stores remain future work.
