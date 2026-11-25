# Lilium — final technical review (2026-11-25)

**Decision: automated gates passed for designated remediated v0.14.0 candidate; manual pilot opening remains pending.** This is a first-party source review, not a penetration test, independent audit, WCAG certification or real-device acceptance.

## Scope and evidence
Reviewed core/api.py (d629607b1e339671ea3bc961807918e6d6684b63), core/session.py (6a1153591fb2d57aeee6f20502cc75c28cd1640f), core/store.py (9bbe848e0b321fa790b900de1a5c738c7625753a), core/workspace.js (03dd7e0a1134f7c3a76ef942ea12f1ac36730ef1), imports, backup, launcher, existing tests and report print styles. The designated binary remains [run 45722415976](https://github.com/Kgasil/lilium/actions/runs/45722415976), not a later build. See [manual acceptance](clean-machine-validation.md) for exact hash.

| Area | Observed control | Residual limitation / gate |
|---|---|---|
| Network | Launcher binds IPv4 loopback; no proxy headers; application API calls are relative and CSP restricts connections to self. | No assertion about arbitrary local malware, browser extensions, or entire device network traffic. Direct development API mode remains unguarded. |
| Session | Random 256-bit process capability; constant-time comparison; Origin and Fetch Metadata policy; private fragment removed from address bar; no-store responses. | Token holder can access all local API data; no multiuser roles or per-tab server revocation. Console link and sessionStorage are sensitive. |
| Browser rendering | Same-origin scripts and assets; no inline script; frame deny; report rendering uses text nodes. | Inline styles permitted; application source review is not exhaustive XSS testing. |
| Import | 1 MiB raw input; XLSX expanded-size and part-count limits; rejects formulas, external links and macros; limits rows/columns. | Parsing resource limits are not a complete hostile-file sandbox. Only synthetic files for preview. |
| History | Parameterized SQL; explicit save of aggregates; consistency checks; bounded merge with conflict rollback. | SQLite and exports not encrypted by app, local administrators can read/modify them; no forensic-erasure assurance. |
| Distribution | Dependency review, audited CI, inner ZIP hash verification, fresh runner acceptance. | Unsigned binary, native components not comprehensively audited, vulnerability database coverage limited. Do not bypass OS warnings. |
| Accessibility | Labeled controls, named landmarks, keyboard focus, named tables, reduced motion and responsive layout. | Manual screen reader, visual contrast and physical interaction review still open. |
| Printing | Print stylesheet hides other workspace panels and report controls. | Physical/visual print layout and device-specific behavior need manual inspection. |

## Additional automated review
The [final candidate review workflow](https://github.com/Kgasil/lilium/actions/workflows/final-review.yml) downloads the exact designated archive, verifies its SHA-256, and uses headless Chromium on Windows to exercise response security headers, session fragment removal/reload, guest isolation, keyboard navigation, visible field labels, text-only report title, report print-media isolation, PDF generation in memory, narrow viewport and absence of observed external requests. The first run is [45724967459](https://github.com/Kgasil/lilium/actions/runs/45724967459). Result is recorded separately; automated checks cannot establish complete security or accessibility compliance.

## Release decision
- Automated build and artifact gates: passed for the designated candidate.
- Independent device acceptance: not evidenced.
- Visual print and manual accessibility/security review: not evidenced.
- Pilot opening: **not approved** until the owner completes and records outstanding acceptance. No data from real businesses or participants is requested.

See [pilot handbook](pilot-handbook.md), [Trust & Privacy](trust-privacy.md), and [release gates](pilot-readiness.md). No new product feature or version bump introduced in this review.
