# Lilium Mini v0.1.0

**Strategy & Growth · Estratégia e Crescimento**
*Make smarter decisions. Grow with confidence.*

Development preview — not a Chrome Web Store or Edge Add-ons release. No connected AI.

## Test on Windows (Chrome / Edge)
1. Download the repository ZIP from GitHub and extract it.
2. Open `chrome://extensions` or `edge://extensions`.
3. Enable Developer mode, select Load unpacked, and choose the extracted `extension` directory (not the repository root).
4. Open Lilium Mini from the toolbar. Fill in the amounts and calculate. Use synthetic data for testing.

Three local tools: profit and margin, target-margin pricing, break-even quantity. Monetary values use BRL and up to two decimal places. No required browser permissions, background scripts, content scripts, storage, analytics, or remote AI. The explicit Insights link opens the public website in a new tab. No values are passed in the URL.

Run the pure calculation tests with Node.js: `node extension/math.test.js` from the repository root. Browser installation and UI tests are still pending. The public code is a prototype; licensing terms are not yet specified. Do not assume production security or commercial availability.

## Experimental ZIP / Pacote experimental

The dedicated [Mini validation workflow](https://github.com/Kgasil/lilium/actions/workflows/mini-validation.yml) is configured to run the calculation and popup-page regression checks, build the minimal ZIP twice, compare both builds and upload the archive and SHA-256 as an Actions artifact only after success. The latest workflow outcome must be checked before using its artifact. It is not a store release.

To build locally from a trusted checkout, run `python extension/package_mini.py --output mini-preview` with Python 3.12 or newer. The archive contains only manifest.json, math.js, popup.css, popup.html and popup.js; it excludes development scripts and tests. Extract the ZIP, compare its SHA-256 with the generated digest from a trusted build, and select the extracted folder containing manifest.json in the browser's unpacked-extension tester. Do not bypass organization policy or security warnings. Archive checks and popup-page regression are not actual installed-extension acceptance. Chrome/Edge toolbar installation and store review remain separate gates.
