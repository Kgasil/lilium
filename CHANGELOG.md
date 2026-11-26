# Changelog / Histórico de versões

This file records documented public development milestones, not a complete historical log of every internal change. / Este arquivo registra marcos públicos documentados, não o histórico integral de todas as alterações internas.

## Mini v0.1.1 — 2026-11-25 — GitHub-only experimental distribution / Distribuição experimental pelo GitHub

- Branded 128px PNG icon and updated version; calculator engines and browser permissions unchanged.
- [Manual installation guide / Tutorial de instalação](extension/README.md) for Chrome and Edge, including pinned source ZIP, examples and troubleshooting.
- Owner reported testing v0.1.0; detailed v0.1.1 acceptance and current CI results remain unconfirmed. No store submission or formal GitHub Release.

## Web Lab 1.0 — 2026-11-25 — Public demonstration edition / Edição pública demonstrativa

- Public edition of the existing browser lab: financial calculations, pricing, five synthetic scenarios, forecasts and CSV demonstration.
- Bilingual launch announcement and voluntary feedback channel. [Announcement / Comunicado](docs/web-lab-v1.0.md).
- No changes to calculation engines. Prior web lab CI passed; post-announcement deployment not yet confirmed.
- Desktop remains v0.14.0; no Desktop V1.0, signed executable, production service or real-data approval.

## v0.14.0 — 2026-11-25 — Pre-release / Pré-lançamento

### Available in the preview / Disponível na prévia
- Local Workspace with ten modules: Insights, Reports, Finance, Flow, Sales, Operations, Strategy, Forecast, Copilot and Connect. Module capabilities and limitations are documented in the [README](README.md).
- Five synthetic business scenarios, offline help and optional local analysis history.
- Browser-based interactive lab, including financial calculations, forecasting and sample CSV analysis.
- Deterministic Copilot; no connected external AI. External production integrations remain planned.

### Validation reported at the milestone / Validação registrada no marco
- 100 Python tests and 401 Node.js checks passed.
- Remediated portable Windows package: automated dependency review, Chromium checks, ZIP integrity, backup recovery, independent artifact verification and print/PDF checks, as documented in the [milestone announcement](docs/milestone-2026-11-25.md).

### Pending / Pendente
- Manual clean-machine Windows acceptance, manual security and accessibility review, and signed distribution.
- Controlled testing with synthetic data only. Do not bypass operating-system warnings or use superseded packages.
- No public V1.0, commercial offering or production-readiness claim.

[Website / Site](https://kgasil.github.io/lilium/#novidades) · [Interactive lab / Laboratório](https://kgasil.github.io/lilium/#lab) · [Acceptance guide / Guia de aceitação](docs/clean-machine-validation.md)
