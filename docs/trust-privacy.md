# Lilium Trust & Privacy — local preview

Status: development preview 0.14.0; not a public pilot or a compliance certification. Use synthetic data only.

## Data and local storage

The Workspace processes supplied data locally. CSV/XLSX inputs and other module results are held in memory during the session. Only explicitly saved Insights aggregates are written to SQLite, in the Desktop per-user data directory. The original CSV is not saved by Lilium. Exports and backups are created only on user request. Neither the database nor exported files are encrypted by the application. Operating-system permissions, device encryption, backups and safe handling remain necessary. Browser/device artifacts and user-created copies may persist outside Lilium. Deleting an analysis does not guarantee forensic erasure.

No telemetry, remote analytics, cloud synchronization, external AI, account system or external connectors are enabled in this preview. Source setup requires downloading dependencies; the public website and GitHub are separate services. The application does not send business data to them.

## Desktop session boundary

Desktop creates a cryptographically random 256-bit capability on startup. Its private launch link carries the token in a URL fragment (not an HTTP request URL). Workspace removes the fragment after reading it and retains the token in tab sessionStorage so reload works. Every API request sends the token in X-Lilium-Session. Requests with missing, malformed or mismatched tokens, disallowed Origin or cross-site Fetch Metadata are rejected when Desktop protection is enabled. API responses are marked no-store. Static assets, health and the API contract remain public on loopback and contain no token. Stop the Desktop process to invalidate the token; starting again generates a new one. The session reset button resets workspace data, not server access. Do not share the private link, console output containing it, browser screenshots of it or tokens. Test scripts redact the readiness link.

This is a bearer capability, not a user/password system, not full authentication/authorization for multiple people, and not idle timeout or per-tab server revocation. A person/process with the token can use the API. It cannot defend against malware, compromised browser, privileged local processes or someone who reads the database on disk. Browser sessionStorage can be copied by browser features. HTTP loopback is not encrypted. Keep service bound to loopback. Never expose it on a LAN or the internet. Direct developer imports of core.api remain intentionally unguarded for local testing; use the Desktop launcher for guarded operation and never use direct API mode with real data.

## Review before real business use

- Confirm current Windows build, API session tests, browser reload/invalid-session behavior and no token in request URLs or test logs.
- Review threat model, dependencies, OS permissions, backup and upgrade behavior.
- Define real-data handling, retention, deletion, support and incident-response requirements before a public release.
- Independent security review and applicable legal/privacy assessment are still pending. No claim of LGPD compliance, security certification or data encryption is made.

Validation: 12 policy unit tests passed on Linux; tested blobs match GitHub. Workspace syntax and static references verified. Five new integrated API tests are committed but not yet run against the full current version. Actual Chromium, Windows and complete regression remain unconfirmed.
