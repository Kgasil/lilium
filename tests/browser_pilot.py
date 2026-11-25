"""Headless Chromium pilot smoke test against a real local server; synthetic data only."""
import os
import queue
import subprocess
import sys
import tempfile
import threading
import time
from playwright.sync_api import sync_playwright, expect


def main():
    command = sys.argv[1:] or [sys.executable, "-m", "desktop.launcher"]
    with tempfile.TemporaryDirectory(prefix="lilium-browser-") as folder:
        env = dict(os.environ, LOCALAPPDATA=folder, XDG_DATA_HOME=folder)
        process = subprocess.Popen(command + ["--no-browser"], env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, encoding="utf-8", errors="replace")
        output = queue.Queue()
        def drain():
            for line in process.stdout:
                output.put(line.rstrip())
        thread = threading.Thread(target=drain, daemon=True)
        thread.start()
        try:
            url = None
            deadline = time.monotonic() + 60
            while time.monotonic() < deadline:
                try:
                    line = output.get(timeout=0.5)
                except queue.Empty:
                    if process.poll() is not None:
                        raise RuntimeError("Launcher exited")
                    continue
                print(line, flush=True)
                if line.startswith("LILIUM_READY http://127.0.0.1:"):
                    url = line.split(" ", 1)[1]
                    break
            if not url:
                raise RuntimeError("Launcher timeout")
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport={"width": 1440, "height": 900})
                page.set_default_timeout(10000)
                errors = []
                external = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on("request", lambda request: external.append(request.url)
                        if not request.url.startswith(url + "/") else None)
                page.on("dialog", lambda dialog: dialog.accept())
                page.goto(url, wait_until="networkidle")
                expect(page.locator("#getting-started")).to_be_visible()
                expect(page.locator("#results")).to_be_hidden()
                page.locator("#run").click()
                expect(page.locator("#results")).to_be_visible()
                expect(page.locator("#metrics")).to_contain_text("11.960,00")
                page.locator("#from").select_option("2026-02")
                page.locator("#to").select_option("2026-02")
                page.locator("#apply").click()
                expect(page.locator("#metrics")).to_contain_text("3.760,00")
                page.locator("#save").click()
                expect(page.locator("#history-rows tr")).to_have_count(1)
                page.locator("#finance-form button[type=submit]").click()
                expect(page.locator("#finance-result")).to_contain_text("3.500,00")
                for trigger, target, expected in [
                    ("sales-run", "sales-metrics", "46,67"),
                    ("ops-run", "ops-metrics", "Montagem"),
                    ("strategy-run", "strategy-metrics", "52,86"),
                    ("actions-run", "actions-table", "Revisar precificação"),
                    ("forecast-run", "forecast-metrics", "Tendência linear"),
                    ("flow-run", "flow-queue", "Investigar demanda"),
                    ("copilot-run", "copilot-answer", "Forecast"),
                    ("reports-generate", "reports-preview", "Finance"),
                ]:
                    page.locator("#" + trigger).click()
                    expect(page.locator("#" + target)).to_contain_text(expected)
                page.locator("#connect-read").click()
                for field, name in [("date", "Dia"), ("revenue", "Receita"), ("cost", "Custo")]:
                    page.locator("#connect-map select[data-field=" + field + "]").select_option(name)
                page.locator("#connect-normalize").click()
                expect(page.locator("#connect-result")).to_be_visible()
                expect(page.locator("#connect-preview")).to_contain_text("100.50")
                page.locator("#connect-apply").click()
                expect(page.locator("#results")).to_be_hidden()
                expect(page.locator("#csv")).to_have_value("date,revenue,cost\n2026-01-01,100.50,60.25\n2026-02-01,200.00,90.00")
                with page.expect_download() as dl:
                    page.locator("#reports-json").click()
                assert dl.value.suggested_filename == "lilium-executive-report.json"
                page.locator("#pilot-reset").click()
                page.wait_for_load_state("networkidle")
                expect(page.locator("#results")).to_be_hidden()
                expect(page.locator("#history-rows tr")).to_have_count(1)
                page.locator("#history-rows").get_by_role("button", name="Abrir").click()
                expect(page.locator("#metrics")).to_contain_text("11.960,00")
                page.locator("#history-rows").get_by_role("button", name="Excluir").click()
                expect(page.locator("#history-rows tr")).to_have_count(0)
                page.set_viewport_size({"width": 390, "height": 844})
                expect(page.locator("#getting-started")).to_be_visible()
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"), "Mobile page overflows"
                assert not errors, errors
                assert not external, external
                browser.close()
            print("Browser pilot smoke test OK", flush=True)
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=10)
            if process.stdout:
                process.stdout.close()


if __name__ == "__main__":
    main()
