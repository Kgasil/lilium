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

## Setup and diagnostics pass
Added source setup fingerprint, explicit repair, local redacted readiness checks and bundled diagnostics gate in Windows CI. Eight Python tests passed locally on Linux with mocked subprocess installation; tested source blobs verified against GitHub. Diagnostic storage uses disposable SQLite in the data directory, not real history. No automatic updater, Windows validation or release approval. Full current API and browser regression remains pending.

## Release packaging pass
Added offline portable ZIP packaging, version manifest, SHA-256 verification against an independently trusted digest and safe staging into a unique folder. Nine Python tests passed locally on Linux using synthetic bundle files; published blobs verified identical. Windows workflow now packages only after preceding checks, then validates and smoke-tests the staged executable before artifact upload. No run or real executable confirmed. Version folders are preserved, but the user history is shared; backup and compatibility review required before switching. No signed package, auto-update, public release or claim of authenticity from hashes alone.

## Trust & Privacy pass
Added Desktop process-scoped session token, same-origin and Fetch Metadata checks, no-store API responses, private launch fragment with browser cleanup and test-log redaction. Twelve policy unit tests passed locally; static Workspace syntax/references verified. Five integrated API tests added but current full API/Chromium/Windows validation remains pending. Direct development mode is unguarded; no multi-user accounts, encryption or compliance certification. See [Trust & Privacy](trust-privacy.md).

## Quality Assurance pass — v0.14.0
Reproduced a 500 error when a stored history payload was invalid JSON. History reads, exports and conflicting merges now validate stored snapshots and return a structured 503 history_corrupt response on inconsistencies. Failed merges roll back; the application does not attempt automatic repair or delete records. Workspace displays a specific non-destructive recovery notice and clears stale history rows on read failure.

Verified 83 Python tests in the Linux local copy (Python 3.13.5, pinned runtime dependency versions), including the seven new cross-feature QA tests, five current Desktop session API tests, current history backup API tests, and previous numerical/import/setup/release/session tests. Git blob hashes of core/api.py, core/store.py, core/backup.py, tests/test_core.py, tests/test_history.py and tests/test_quality_assurance.py match the published files; the local HTML is older. Twelve Python static-asset/header cases were excluded; Desktop launcher tests were not present in that local copy. Re-ran all 295 JS module tests and 12 static integration checks in V8 using repository contents and an assertion/filesystem shim. These are not full Node or browser tests. Combined commit status and available PR workflow queries showed no CI results; push-run result, full current Python/Chromium and Windows package remain unconfirmed. No release approval.

## User experience and accessibility pass
Grouped the existing module navigation into four named areas, added six task-based entry points and a plain-language glossary, skip link and focusable destination regions, current hash-link state, accessible captions/scroll regions for 12 tables, column scopes, atomic status announcements, responsive controls and reduced-motion styling. All 11 new structural/isolated navigation checks passed in V8 using repository source and assertion/filesystem shims. Browser smoke test now includes keyboard focus, current anchor, task navigation and generated column scopes. Actual Chromium, assistive technology, contrast and Windows testing remain pending. This is not WCAG certification. No release approval.

## Business Starter Kit pass
Five synthetic business scenarios with seven input sets, confirmed selective/all loading and CSV/JSON export. Loading clears affected calculations, Reports/Copilot and evaluated Flow results; preserves saved history and queued proposals. Revenue reconciles across Sales, Insights and Forecast by month; aggregated synthetic orders are not actual transactions; Finance, Operations and goals are hypothetical exercises. 47 starter unit tests and 23 existing Workspace/UX checks passed in V8 with assertion/filesystem shims. Added browser scenario to test loading and history preservation; Chromium and Windows validation remain pending. No public release.

## Help Center and feature freeze
15 offline help topics cover the current modules, troubleshooting and privacy. Local accent-insensitive search and a downloadable blank support template do not transmit user data. 13 new Help Center checks and 23 existing Workspace/UX checks passed in V8 using repository contents and assertion/filesystem shims. Chromium cases added; execution pending. Feature freeze proposed for the synthetic-data free pilot: no new product modules before release gates are satisfied. Three remaining phases: (1) run complete current regression and Windows CI, fix blocking defects and verify the build artifact; (2) validate on clean Windows, manual usability/accessibility/printing, restart/backup/upgrade, dependency and local security review; (3) document actual tested package and limitations, confirm feedback contact and invite a small free pilot using synthetic data only. These are gates, not deadlines or guaranteed number of iterations. No public or commercial release yet. Real business data requires separate readiness assessment.
