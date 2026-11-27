# Lilium Core v0.14.0 — local development preview

**Strategy & Evolution · Estratégia e Evolução**

**Version scope:** Lilium Web Lab 1.0 is the public milestone; Core and Desktop remain v0.14.0 development previews. Historical test notes below reflect their respective checkpoints. See [current project status](../README.md).

## Windows
Install Python 3.12 x64 with the Python launcher. Download/extract the repository and run `start-lilium.bat`. The first run or a changed requirements fingerprint installs dependencies, then the launcher reserves a loopback port and opens the browser automatically when ready. Keep the console open; Ctrl+C stops the service. Desktop history uses `%LOCALAPPDATA%/K&G Vision/Lilium/lilium.sqlite3`; previous development history stays separate. See [Desktop packaging and validation](../desktop/README.md). The remediated Windows CI build passed; independent manual clean-machine acceptance remains pending. Use synthetic data only.

Manual commands (PowerShell, from repository root):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m desktop.launcher
```

## Data Intelligence — candidato da Etapa 03

API local aceita três cabeçalhos canônicos em qualquer ordem (CSV/XLSX), e CSV simples UTF-8 com `data;receita;custo` em qualquer ordem, data ISO ou DD/MM/AAAA, valores inteiros ou vírgula decimal sem milhares. A normalização não modifica o arquivo original; erros impedem análise, duplicatas são alertas. O contrato de métricas permanece idêntico. Meta de margem usa a margem arredondada exibida, não muda a análise; gráfico alterna receita/custo e resultado; diagnóstico JSON contém contagens e códigos de linha, sem valores originais. Candidato ainda sujeito a CI.

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

## Lilium Copilot — candidato conversacional da Etapa 04

Perguntas livres (até 240 caracteres), continuidade simples do tópico e roteamento local por regras. Opcionalmente, com consentimento por pergunta, o Desktop envia apenas o texto ao Ollama em 127.0.0.1:11434. Instalação e modelo são opcionais e separados: obtenha Ollama do site oficial, execute localmente `ollama pull qwen2.5:1.5b` ou `ollama pull llama3.2:1b` antes de usar, confira licença e requisitos. Sem download automático ou serviço pago contratado. O modelo retorna apenas tópico permitido; resposta e recomendações continuam determinísticas. Sem envio de métricas ou arquivos ao modelo, sem armazenamento da conversa pelo Lilium, sem ações automáticas. O serviço local pode ter comportamento/logs próprios; não digite dados pessoais ou confidenciais. Fallback por regras se o modelo falhar. CI e inferência real pendentes.

### Consulta guiada existente
- Guided local assistant with eight predefined topics (overview, Insights, Finance, Sales, Operations, Strategy, Forecast and action suggestions). No free-form language model, voice, network request, credentials or generative AI. Uses computed session results; retains source, scope and data kind. Missing sources and unavailable metrics are explicit, not fabricated.
- Reuses Reports for module summaries and Flow for six example alert rules, editable in Flow's CSV format. Thresholds are illustrative, not universal benchmarks. Matched rules generate suggestions with evidence and scope; no causal inference or cross-module financial consolidation.
- Explicit confirmation to forward a suggestion to the Flow pending queue. Re-evaluates the rule against current source data; changed evidence or rule requires regenerating the response. Deduplication and queue limits inherited from Flow. No execution, automatic approval or durable audit log.
- JSON response export. Session snapshots are not automatically refreshed or persisted. Use synthetic data.
- `node tests/copilot.test.js`: 30 new checks passed in V8; 295 total JS checks passed from published GitHub source. Python regression, browser and Windows testing remain pending.

## Lilium Connect
- Local data interchange for Insights, Sales and Forecast. Paste or open simple UTF-8 CSV/TSV; delimiters comma, semicolon or tab, up to 1 MiB, 10,000 rows and 50 columns. No quoted fields or multiline cells. Headers must be unique. Map required fields explicitly to different source columns; unmapped columns are omitted in the normalized copy.
- Optional decimal-comma conversion for numeric fields only; no automatic date, currency or thousands-separator conversion. Destination validation uses existing Sales and Forecast parsers; Insights checks required header, ISO dates and monetary syntax locally, then its API revalidates when the user runs analysis. Forecast unit is chosen in its destination module.
- Preview up to ten normalized rows; export CSV or versioned JSON dataset package (`schema_version: 1.0`, `kind: lilium.dataset`, target, UTF-8 encoding, CSV format, row count and CSV content). Import strictly checks envelope fields and revalidates CSV and row count; not a cryptographic authenticity check. JSON packages also have a 1 MiB limit including overhead; use CSV if the package is too large.
- Explicit confirmation before transferring data into a module; clears its existing calculated result, not stored Insights history. No automatic analysis, external connections, credentials, persistence or execution. Exports contain normalized raw records, not anonymized aggregates. Use synthetic data.
- `node tests/connect.test.js`: 31 new checks passed in V8; 265 total JS checks passed from published GitHub source. Python regression, browser and Windows testing remain pending.

## Lilium Flow
- Local, manually triggered rule evaluation on six allowlisted metrics from the current Insights, Finance, Sales, Operations, Strategy and Forecast session results. Paste simple CSV: `rule_id,metric,operator,threshold,action`; up to 50 rules, 32,768 characters. Operators: lt, lte, gt, gte, eq. Money compares exact integer cents; other metrics compare rounded two-decimal values. Missing sources are unavailable, not zero.
- Matched rules create proposals, with evidence, scope, data kind and UTC timestamps. Identical rule/evidence signatures are deduplicated within the session, including previously rejected or completed proposals. Up to 200 proposals; clearing the queue resets the session history.
- Status transitions: pending → approved or rejected; approved → completed_manually or rejected. Completion is user-declared, not independently verified. Approval does not execute anything. No scripts, network actions, external notifications, schedules or background jobs.
- Export queue and event history as JSON. No persistence, tamper-proof audit trail, access-control enforcement or external AI. Re-evaluate after changing data; proposals retain original evidence. Use synthetic data.
- `node tests/flow.test.js`: 33 new checks passed in V8; 234 total JS checks passed from published GitHub source. Python regression, browser and Windows testing remain pending.

## Lilium Forecast
- Local monthly time-series module. Paste simple CSV `month,value`, 6–120 consecutive ordered months (YYYY-MM), nonnegative values with up to 9 integer digits and 2 decimal places. For sales units, historical values must be integers. Optionally load full monthly revenue from the current Insights analysis; gaps and insufficient histories are rejected, not silently filled.
- Compare last-value baseline, recursive three-month moving average, and ordinary least-squares linear trend. Predictions are clipped at zero. Choose manually or select smallest validation MAE, with deterministic model-order tie-breaking. Forecast horizon 1–12 months.
- Expanding-window rolling-origin one-step validation: last min(6, floor(n/3)) months, same months for every model, training only on preceding observations. MAE, RMSE and WAPE (undefined when validation actuals sum to zero). Model selection and evaluation share validation data; no independent test or multi-step error estimate.
- Show historical and predicted values separately; export JSON including unit, history, forecast, validation pairs, comparison and limitations. Forecasts use floating-point statistical arithmetic and display rounded values; they are not accounting calculations.
- No prediction intervals, seasonality, external predictors, persistence, connected AI or Reports integration yet. Use synthetic data.
- `node tests/forecast.test.js`: 36 new checks passed in V8; 201 total JS checks passed from published GitHub source. Python regression, browser and Windows testing remain pending.

## Lilium Reports
- Executive report builder from currently computed Insights (active month filter), Finance simulation, Sales (active month filter), Operations scenario, Strategy and action rankings. Select any of six sources; missing sources are listed, and at least one computed source is required.
- Every section preserves scope and identifies its source and data type. The report does not reconcile datasets, total revenue across modules or present hypothetical results as actuals. Top ten product/action details; operational and strategic details remain separately labeled.
- Report snapshots are generated on demand with a title and UTC timestamp, and remain unchanged until regenerated. Preview uses text-only DOM construction. Export JSON or TXT; browser print layout allows saving a PDF using the browser's print dialog (no native PDF generator).
- No automatic persistence, external AI, scheduled delivery or XLSX report generation. Review results and remove sensitive data before sharing.
- `node tests/reports.test.js`: 27 new checks passed in V8; 165 total JS checks passed from published GitHub source. Python regression, browser/print and Windows testing remain pending.

## Lilium Strategy
- Local browser OKR tracker, restricted pasted CSV: `objective,kr,baseline,target,actual,scenario,weight,due`. Up to 100 KRs and 65,536 characters. Numeric values in consistent units, decimal point, 2 decimal places, baseline distinct from target, weight 1–10, ISO due date. Explicit evaluation date; achieved KRs are marked achieved regardless of deadline (no completion-date history). Increasing and decreasing goals supported.
- Progress = (actual − baseline)/(target − baseline), expressed as a percentage. Raw progress retained; aggregate weighted progress clamps each KR to 0–100%. All KRs contribute using their weights, not equal objective weighting. Scenario is a user-supplied hypothetical value, not a forecast.
- Action prioritization: `action,impact,urgency,effort` CSV, up to 100 actions, scores 1–5. Rank by impact × urgency / effort, ties by action name. Subjective decision aid, not autonomous recommendations.
- JSON export for goals/scenarios and action rankings. No persistence, automatic module integration, file upload or external AI. Use synthetic data.
- `node tests/strategy.test.js`: 34 new checks passed in V8; 138 total JS checks passed from published GitHub source. Python regression, browser and Windows testing pending.

## Lilium Operations
- Local browser CSV module: one comparable sequential resource per stage, same measurement period, 1–100 unique stages, up to 64 KiB. Exact header: `stage,planned_min,downtime_min,cycle_sec,total_units,good_units,rework_units,lead_min`. Integer minutes, ideal cycle seconds per unit, total units, first-pass good units, rework subset of nonconforming units, optional observed mean lead time per stage. No automatic deduplication or general spreadsheet mapping.
- Availability = runtime/planned time; performance = total units × ideal cycle/runtime (consistent seconds); quality = first-pass good/total. OEE is the product of these factors; undefined denominators or performance over 100% yield no OEE. Runtime = planned minus downtime. Throughput per runtime hour, nonconforming count and rework rate are shown. Nonconforming does not imply scrap, and lead time is supplied, not derived or summed.
- Theoretical capacity = floor(runtime seconds / ideal cycle seconds). Estimated serial bottleneck = minimum available stage capacity (ties shown). This is not observed throughput or proof of a real constraint. Parallel resources, queues, differing product mixes and demand are out of scope.
- Scenario reduces each stage's downtime by an integer percentage (0–100), floors recovered minutes, recomputes ideal capacity and bottleneck. Not a guaranteed productivity gain. JSON export contains stages and assumptions/model identifier; no automatic persistence or external calls.
- Run `node tests/operations.test.js`: 35 checks passed in V8; all 104 current dashboard, Finance, Sales and Operations JS checks passed from GitHub source. Python regression and browser/Windows testing remain pending.

## Lilium Sales
- Independent local browser analytics: restricted UTF-8 CSV, header `date,order_id,product,quantity,unit_price`, 1–10,000 rows and 1 MiB. No quotes, embedded commas, XLSX or automatic column mapping. ISO date, positive integer units up to 1,000,000, nonnegative BRL unit price (9 integer and 2 decimal digits). Each order ID must have one date.
- Gross revenue = quantity × unit price. Distinct order count and average order ticket (half-up cents), unit volume, product ranking by gross revenue, inclusive monthly filters and monthly breakdown. Product labels are case-sensitive. Possible exact duplicate lines are flagged, not removed. No automatic refunds, discount, tax or cost calculations.
- BigInt cents internally; JSON aggregate export uses integer strings for money and quantity, excludes individual order IDs. Sales input stays in browser memory, no SQLite persistence or external requests. Exported product names and aggregates may be confidential; use synthetic data.
- Run `node tests/sales.test.js`: 30 checks passed in V8. Browser UI and Python regression, including the new asset route test, remain untested.

## Lilium Finance
- Local browser module, independent of imported datasets. Pricing computes the minimum cent-rounded selling price for a desired contribution margin using monetary variable cost only (no fixed costs or percentage fees).
- Single-product monthly simulation: unit price, variable cost, fixed monthly cost, integer sales volume, sale fee (percentage) and desired nonnegative result. Fee rounds half-up per unit. Result = sales − variable costs − fees − fixed costs. Break-even and target volume use ceiling division where contribution is positive. Zero or negative contribution may make the target infeasible; zero revenue yields no result margin.
- Inputs are bounded (up to 9 integer and 2 decimal digits for money, 0–1,000,000 sales units, percentages below 100). Monetary calculations use BigInt cents; JSON simulation export represents cents as integer strings. The export includes input assumptions and results. Simulations are not saved in SQLite and do not use AI or external network calls.
- `node tests/finance.test.js` — 25 checks passed in V8; the 14 dashboard checks also passed again from repository source. Node is optional for development, not required to use the local application.
- This is a scenario tool, not accounting, cash-flow forecasting or guaranteed business advice.

## Professional Workspace
- Navigation between overview, import/quality and local history. Responsive graphite/rose/gold layout with local JavaScript served by the API.
- Inclusive month filters over validated monthly aggregates. Totals are recomputed from the selected months; margin uses integer arithmetic with half-up rounding. Missing months are not invented. An empty interval has no indicators.
- Revenue/cost chart displays up to the latest 24 months in the filter; the accessible table contains all selected months. Export monthly CSV for the active period or full JSON for the original analysis. Saving always persists the complete analysis, not a filtered subset.
- Run the dashboard tests with `node tests/dashboard.test.js` (Node.js optional for development only; no Node dependency for users). Fourteen pure JS checks passed in a V8 execution environment. The Python regression suite now includes an additional asset-route test; the full Python suite and browser UI have not been rerun for v0.13.

## Smart Import & Data Quality
- `POST /api/v1/quality` — diagnostic only, no persistence. Counts valid/invalid rows, possible duplicates and zero-revenue rows; returns row number and issue code (first 100 issues). Invalid rows block analysis; warnings do not. No automatic corrections or deduplication.
- XLSX: exactly one worksheet, three columns with the same CSV header, ISO dates or native Excel date values, numeric BRL values. Replace formulas with values; macros and external links are unsupported. Input 1 MiB, expanded archive 12 MiB, at most 100 archive entries, 10,000 data rows. Corrupt or unsupported files are rejected. This is a restricted importer, not a general Excel editor; XLS/XLSM are unsupported.
- Structural errors (including invalid header, formula or unsupported workbook) stop the diagnostic. The original file is never persisted. All calculations use the existing deterministic core after normalization.

## Local history
- POST /api/v1/history — validates the same CSV or XLSX input and explicitly saves a consolidated snapshot; 201 with identifier and timestamp.
- GET /api/v1/history — list up to 200 saved snapshots (latest first).
- GET /api/v1/history/{id} — reopen a saved analysis; DELETE on the same path removes it.
- SQLite is built into Python. Direct-development database: `data/lilium.sqlite3` (ignored by Git). The Desktop launcher uses the per-user directory instead. Only aggregated metrics are stored, not the raw CSV. Analyze alone does not save anything. No app-level encryption or secure-erasure guarantee; do not use confidential data.
- Full history returns 409; storage failure returns 503 without exposing local paths. Back up exported JSON if needed; deleting a snapshot does not delete external exports or backups.

## Boundaries
The UI sends CSV or XLSX only to the loopback API. Optional local persistence; no telemetry, account, external AI or payments. Do not expose the service to the LAN or internet. The Desktop launcher adds a process-scoped session token and Origin/Fetch Metadata checks; direct development API mode does not. These are limited defenses, not a security audit or user-account system. Result is revenue minus supplied costs, not necessarily accounting profit. No general quoted CSV/XLSX mapping, multi-tenant isolation, validated desktop binary or production deployment yet. The latest recorded partial Linux regression passed 86 Python tests; 14 asset-dependent cases were excluded. Full Windows installation, complete regression and browser UI remain unverified.

Next: confirm Windows CI, perform interactive UI and clean-machine tests, and prepare a controlled pilot. SQLite is chosen for the lightweight local preview; analytical and multi-organization stores remain future work.

## Current validation boundary
Use the Desktop launcher to enable the temporary session token. Direct Uvicorn mode is an unguarded development-only API. The public [Interactive Lab](https://kgasil.github.io/lilium/#lab) is separate, requires no Python and accepts synthetic exercises only. Earlier Windows/Chromium functional CI succeeded, but the earlier packages were superseded due to security findings. A new dependency-audited build must pass all gates. See [pilot gates](../docs/pilot-readiness.md).

Current remediation pins FastAPI 0.165.0 and Starlette 1.10.0; setup upgrades pip to 26.3. Read [Trust & Privacy](../docs/trust-privacy.md) for review scope and limitations. Manual acceptance on a clean Windows device is pending.
