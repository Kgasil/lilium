"""Focused acceptance of an already built preview. Synthetic data only."""
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright, expect
from smoke_lifecycle import running

def main():
    command = [str(Path(sys.argv[1]).resolve())]
    with TemporaryDirectory(prefix="lilium-final-review-") as folder, running(command, folder) as (base, token):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
            errors, external = [], []
            page.on("pageerror", lambda e: errors.append(type(e).__name__))
            page.on("request", lambda req: external.append(req.url.split(":")[0]) if not req.url.startswith(base + "/") else None)
            response = page.goto(base + "/#access=" + token, wait_until="networkidle")
            assert response.ok
            headers = response.headers
            assert "script-src 'self'" in headers["content-security-policy"]
            assert "frame-ancestors 'none'" in headers["content-security-policy"]
            assert headers["referrer-policy"] == "no-referrer"
            assert headers["cache-control"] == "no-store"
            assert token not in page.url
            expect(page.locator("#workspace-loading")).to_be_hidden()
            # The accessibility checks are structural, not a full WCAG audit.
            assert page.locator("html").get_attribute("lang").startswith("pt")
            assert page.get_by_role("main").count() == 1
            page.locator(".skip-link").focus()
            page.keyboard.press("Enter")
            expect(page.locator("#main-content")).to_be_focused()
            page.locator('#module-nav a[href="#finance"]').focus()
            page.keyboard.press("Enter")
            expect(page.locator("#finance")).to_be_focused()
            page.locator("#finance-form button[type=submit]").click()
            expect(page.locator("#finance-result")).to_contain_text("3.500,00")
            page.locator("#run").click()
            expect(page.locator("#results")).to_be_visible()
            # Report title must be text, not executable markup.
            title = "<em>Relatorio sintetico 2026</em>"
            page.locator("#reports-title").fill(title)
            page.locator("#reports-generate").click()
            expect(page.locator("#reports-preview")).to_contain_text(title)
            assert page.locator("#reports-preview em").count() == 0
            # Visible form fields have associated labels or explicit ARIA names.
            unlabeled = page.evaluate("""() => Array.from(document.querySelectorAll('input:not([type=hidden]),select,textarea')).filter(e => e.getClientRects().length && !e.getAttribute('aria-label') && !e.getAttribute('aria-labelledby') && !Array.from(e.labels || []).some(l => l.textContent.trim())).map(e => e.id || e.tagName)""")
            assert not unlabeled, "Unlabelled visible controls: " + str(unlabeled)
            page.emulate_media(media="print")
            expect(page.locator("#reports-preview")).to_be_visible()
            expect(page.locator("#finance")).to_be_hidden()
            expect(page.locator("#module-nav")).to_be_hidden()
            expect(page.locator("#reports .report-controls")).to_be_hidden()
            pdf = page.pdf(format="A4", print_background=True, prefer_css_page_size=True)
            assert pdf.startswith(b"%PDF-") and len(pdf) > 1000
            # Print generated in memory; visual inspection still required.
            page.emulate_media(media="screen")
            page.set_viewport_size({"width": 390, "height": 844})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
            page.reload(wait_until="networkidle")
            expect(page.locator("#session-notice")).to_be_hidden()
            # Fresh tab cannot access stored history without the capability.
            other = browser.new_page()
            other.goto(base + "/", wait_until="networkidle")
            expect(other.locator("#session-notice")).to_be_visible()
            other.close()
            assert not errors, errors
            assert not external, "Unexpected non-loopback request"
            browser.close()
    print("Final candidate review passed: response headers, private link, keyboard, field labels, text rendering, print media/PDF, narrow viewport, session reload and no observed external requests.")

if __name__ == "__main__":
    main()
