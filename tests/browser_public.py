"""Real-browser check of the public site; no business data or remote API."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            # External images/links are not needed for calculator behavior.
            page.route("**/*", lambda route: route.continue_() if route.request.url.startswith(base + "/") else route.abort())
            page.goto(base + "/index.html#lab", wait_until="networkidle")
            expect(page.locator("#lab-price-result")).to_contain_text("R$ 100,00")
            expect(page.locator("#lab-monthly-result")).to_contain_text("R$ 3.500,00")
            page.locator("#lab-price-margin").fill("100")
            expect(page.locator("#lab-price-result")).to_be_empty()
            expect(page.locator("#lab-price-error")).to_be_visible()
            page.locator("#lab-price-margin").fill("40")
            expect(page.locator("#lab-price-result")).to_contain_text("R$ 100,00")
            before = page.locator("#lab-scenario-result").inner_text()
            page.locator("#lab-scenario").select_option("restaurant")
            assert page.locator("#lab-scenario-result").inner_text() != before
            with page.expect_download() as download:
                page.locator("#lab-download").click()
            assert download.value.suggested_filename == "lilium-restaurant-sample.csv"
            page.locator("#en").click()
            expect(page.locator("#lab-price-result")).to_contain_text("Estimated price")
            page.locator("#pt").click()
            expect(page.locator("#lab-price-result")).to_contain_text("Preço estimado")
            page.set_viewport_size({"width": 390, "height": 844})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"), "Mobile layout overflows"
            # Public Insights demo: verify real CSV calculation and stale-result clearing.
            page.goto(base + "/demo.html", wait_until="networkidle")
            page.locator("#csv").fill("date,revenue,cost\n2026-01-01,1000,700")
            page.locator("#run").click()
            expect(page.locator("#profit")).to_contain_text("300,00")
            expect(page.locator("#margin")).to_have_text("30,00%")
            page.locator("#csv").fill("date,revenue,cost\n2026-02-30,1000,700")
            page.locator("#run").click()
            expect(page.locator("#result")).to_be_hidden()
            expect(page.locator("#error")).to_contain_text("Data ISO inválida")
            # Privacy page is a separate public surface, not an extension runtime.
            page.goto(base + "/mini-privacy.html", wait_until="networkidle")
            expect(page.get_by_role("heading", name="Português", exact=True)).to_be_visible()
            expect(page.get_by_role("heading", name="English", exact=True)).to_be_visible()
            expect(page.locator("main")).to_contain_text("não possui conta, analytics")
            assert not errors, errors
            browser.close()
        print("Public browser lab smoke test passed")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
