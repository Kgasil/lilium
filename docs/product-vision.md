# Lilium Business Suite — Product vision (proposal)

**Strategy & Growth · Estratégia e Crescimento**
*Make smarter decisions. Grow with confidence.*

**Status:** planning, except for the local CSV metrics demonstration in `demo.html` the Lilium Mini development preview in `extension/`, and the local Core/Workspace v0.1.0 in `core/`. No commercial availability or connected AI.

## Product thesis
A modular web application for small and midsize organizations that need business intelligence and decision support without deploying a full ERP. Start with spreadsheet-heavy workflows, then integrate existing systems. The product should complement, not replace, accounting systems or professional judgment.

## Proposed product portfolio
| Module | Intended outcome |
| --- | --- |
| Insights | Validated data, KPIs, trends, drill-down and data lineage |
| Finance | Revenue, costs, margins, budgets and cash-flow scenarios |
| Sales | Pipeline, conversion, churn, customer segmentation and CRM analytics |
| Operations | Lead time, SLA, capacity, waste and bottleneck analysis |
| Reports | Repeatable executive reports, PDF/XLSX and scheduled delivery |
| Strategy | Goals, OKRs, scenario comparisons and action plans |
| Forecast | Time-series baselines, uncertainty intervals, backtesting and forecast error |
| Flow | Workflow builder, approval queues, notifications and idempotent runs |
| Connect | CSV/XLSX first; read-only API connectors, ERP/CRM and database adapters later |
| Copilot | Natural-language questions over authorized metrics, evidence and recommended next steps |
| Control | Organization roles, audit trail, retention, data quality and AI evaluation; cross-cutting security |
| Inventory & Procurement (future exploration) | Stock, supplier performance, purchasing and replenishment analysis |
| Customer Intelligence (future exploration) | Retention, cohorts and customer service performance |

## Example workflow
Import synthetic sales and cost data → map and validate columns → compute versioned metrics → compare periods → identify anomalies using explicit rules → ask Copilot to explain the changes with cited metric IDs → generate a report → approve a suggested action. No autonomous payments, external messages or data modifications without authorization.

## Delivery gates
1. Existing local demo: restricted CSV, totals, monthly aggregation, margin and TXT export.
2. Core MVP (started, not complete): typed metric contracts, validation, Python/FastAPI, analytical storage, reproducible tests, CSV/XLSX, data-quality report, accessible dashboard and export. One organization in a local environment.
3. Evidence-based Copilot: provider adapters, allowlisted read-only tools, retrieval from approved metric definitions, structured outputs, references, abstention when evidence is insufficient, test suite against fabricated figures and prompt injection. Secrets remain server-side. No raw unrestricted SQL from the model.
4. Business modules: budgets, CRM, process analytics, alerts, scenario simulation and forecasting evaluated against simple baselines.
5. Controlled pilot: authenticated users, organization isolation, authorization, deletion/retention, encrypted transport, backups, incident response, monitoring, model cost limits, audit logs and security tests. Evaluate applicable data-protection obligations before real data.
6. Commercial validation: interview target customers, test willingness to pay, benchmark actual workflow outcomes, define support and deployment costs. Only then decide subscription plans and pricing.

## Proposed deployment
Public GitHub Pages for institutional presentation and synthetic demonstrations; commercial application source and secrets separated from public site. React/TypeScript UI, Python/FastAPI API, DuckDB for local analysis, PostgreSQL for future transactional multi-tenant storage. Authentication, tenant boundaries and permissions enforced on the backend. Deployment and hosting choices remain subject to feasibility, cost and security.

## AI capabilities and limitations
AI interprets verified calculations rather than generating authoritative financial figures. Forecasts use statistical or ML models with backtesting; language models communicate results and uncertainty. Agents propose workflows, with explicit human approval for consequential actions. Do not send customer identifiers or confidential data to external providers without authorization and appropriate safeguards.

## Product access and trust-first strategy

- **Lilium Mini**: free Chromium extension for quick business tools, initially profit/margin, target-margin pricing and break-even. Future candidates: discount/ROI calculators, checklists, local notes and quick reports. No browser-page access, accounts, tracking or mandatory upgrade for the initial tools. Local-only by default; explicit opt-in for any future data transfer.
- **Lilium Workspace**: planned web application with a free useful tier, data import, basic dashboards and reports. Explore a Windows installable version after the web core is stable.
- **Lilium Business**: proposed optional paid capabilities (advanced analytics, AI usage, automation, connectors, collaborative workspaces and governance). Do not lock access to existing user data behind a paywall; provide export and clear pricing before any paid subscription.
- First validate with small merchants, service providers and independent entrepreneurs through opt-in interviews, synthetic demos and controlled testing. Measure usability, repeat use, calculation correctness and time saved; do not claim validated outcomes prematurely.
- Mini stays useful independently; the optional link to Workspace is transparent and does not transmit input data.

## Possible commercial model (unvalidated)
Free local/synthetic demo; Professional for advanced analysis and report automation; Business for teams and connectors; Enterprise for deployment, governance and custom integrations. Optional implementation and training services only after the initiative is ready to offer them. No pricing or performance claims yet.

## Ecosystem boundaries
Genesis: independent study. Vision: applied AI integration, security and assurance research. Aeris: personal productivity. Lilium: organizational decision support and operational intelligence. Shared engineering patterns are possible, but client information must remain isolated.
