# Lilium — controlled pilot preparation

Status: v0.14.0 development preview; not a V1.0 release. Free pilot is planned, not open. Synthetic data only.

## Release gates
- [ ] Windows CI succeeds, including Python regression, JavaScript regression, source/bundled server smoke tests and Chromium pilot test.
- [ ] Download the Windows x64 build artifact; test on a clean Windows machine without Python, without bypassing OS security warnings.
- [ ] Check startup, shutdown, repeated launch, saved history across restart, backup/restore and upgrade behavior.
- [ ] Test keyboard navigation, narrow layout, import errors, downloads and report printing; review accessibility.
- [ ] Review local threat model and dependency vulnerabilities. Loopback alone is not authentication. The app is unsigned and lacks app-level encryption, tenant isolation and durable audit logging.
- [ ] Document remaining defects, support/feedback route and known limitations. No business or personal data until privacy and security readiness is separately established.

## Suggested free pilot
Invite a small group of volunteers only after the above gates pass. Provide a synthetic sample scenario and ask them to evaluate setup, understanding of indicators, usefulness, and friction. Do not request business spreadsheets, credentials or personal information. Collect only voluntary, non-sensitive feedback; no telemetry or external AI is enabled.

## Feedback format
Version / Windows version / module / steps to reproduce / expected result / actual result / severity / optional redacted screenshot. Do not include real financial figures, customer identifiers or local file paths.

## Acceptance flow
Insights import and quality → save and reopen aggregate → Finance scenario → Sales → Operations → Strategy → Forecast → Flow review → Connect mapping → Copilot → Reports export → reset session. Automated Chromium coverage is configured, but the run result has not been confirmed. Manual installation, print and security checks remain open.

## Hardening pass — v0.14.0
The Workspace controller is now a separate same-origin asset. CSP blocks inline scripts; inline styles remain permitted for current chart rendering. A startup message remains visible if controller initialization fails. All 295 existing JS checks and 12 new static integration checks passed in V8 against repository contents (307 total). Static checks cover syntax, IDs, navigation anchors, local asset routes, script order, packaging inclusion and CSP. Python, real Chromium and Windows build results remain unconfirmed. No public release.

## History recovery pass
Versioned JSON export and transactional merge recovery added to History. Nine Python backup tests passed locally using identical GitHub blobs for backup, metrics and store. Three API tests and a Chromium export/delete/restore/reimport sequence are configured but not yet executed against the current published application. Backup is unencrypted and limited to 16 MiB; only saved Insights aggregates, not original inputs or other module sessions. Validation checks consistency, not authenticity. Pilot release remains blocked on full current Python/Windows/browser validation.
