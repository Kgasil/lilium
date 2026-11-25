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
