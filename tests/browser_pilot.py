"""Headless Chromium pilot smoke test against a real local server; synthetic data only."""
import os
import queue
import re
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
                if line.startswith("LILIUM_READY http://127.0.0.1:"):
                    link = line.split(" ", 1)[1]
                    url = link.split("/#access=", 1)[0]
                    assert link != url
                    print("Desktop ready (access link redacted)", flush=True)
                    break
                print(line, flush=True)
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
                # Verify that the bare URL cannot access protected history in a fresh context.
                guest = browser.new_page()
                guest.goto(url, wait_until="networkidle")
                expect(guest.locator("#session-notice")).to_be_visible()
                guest.close()
                page.goto(link, wait_until="networkidle")
                assert "#access=" not in page.url
                expect(page.locator("#session-notice")).to_be_hidden()
                expect(page.locator("#getting-started")).to_be_visible()
                expect(page.locator("#workspace-loading")).to_be_hidden()
                expect(page.locator("#results")).to_be_hidden()
                expect(page.locator('#module-nav a[aria-current="location"]')).to_have_attribute("href", "#overview")
                expect(page.locator("#overview-empty")).to_be_visible()
                expect(page.locator("#overview-empty .kpi")).to_have_count(4)
                assert page.locator("body").evaluate("e => getComputedStyle(e).backgroundColor") == "rgb(48, 36, 47)"
                assert page.locator("html").evaluate("e => getComputedStyle(e).colorScheme") == "dark"
                page.locator(".skip-link").focus()
                page.keyboard.press("Enter")
                expect(page.locator("#main-content")).to_be_focused()
                page.locator('#module-nav a[href="#finance"]').focus()
                page.keyboard.press("Enter")
                expect(page.locator("#finance")).to_be_focused()
                expect(page.locator('#module-nav a[aria-current="location"]')).to_have_attribute("href", "#finance")
                page.locator('.quick-grid a[href="#import"]').click()
                expect(page.locator("#import")).to_be_focused()
                expect(page.locator('#module-nav a[aria-current="location"]')).to_have_attribute("href", "#import")
                page.locator("#run").click()
                expect(page.locator("#results")).to_be_visible()
                expect(page.locator("#metrics")).to_contain_text("11.960,00")
                expect(page.locator("#overview-empty")).to_be_hidden()
                page.locator("#margin-target").fill("40,00")
                expect(page.locator("#margin-target-status")).to_contain_text("-3,98")
                page.locator("#chart-mode").select_option("result")
                expect(page.locator("#chart-heading")).to_contain_text("Resultado mensal")
                with page.expect_download() as quality_download:
                    page.locator("#quality-export").click()
                assert quality_download.value.suggested_filename == "lilium-quality.json"
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
                page.locator("#copilot-question").fill("Como está a margem?")
                page.locator("#copilot-ask").click()
                expect(page.locator("#copilot-chat-status")).to_contain_text("resposta determinística")
                expect(page.locator("#copilot-answer")).to_contain_text("Insights")
                page.locator("#copilot-question").fill("Explique melhor")
                page.locator("#copilot-ask").click()
                expect(page.locator("#copilot-chat article")).to_have_count(2)
                page.locator("#copilot-clear-chat").click()
                expect(page.locator("#copilot-chat")).to_be_empty()
                page.locator("#connect-read").click()
                for field, name in [("date", "Dia"), ("revenue", "Receita"), ("cost", "Custo")]:
                    page.locator("#connect-map select[data-field=" + field + "]").select_option(name)
                page.locator("#connect-normalize").click()
                expect(page.locator("#connect-result")).to_be_visible()
                expect(page.locator("#connect-preview")).to_contain_text("100.50")
                expect(page.locator("#connect-head th[scope=col]")).to_have_count(3)
                page.locator("#connect-apply").click()
                expect(page.locator("#results")).to_be_hidden()
                expect(page.locator("#csv")).to_have_value("date,revenue,cost\n2026-01-01,100.50,60.25\n2026-02-01,200.00,90.00")
                with page.expect_download() as dl:
                    page.locator("#reports-json").click()
                assert dl.value.suggested_filename == "lilium-executive-report.json"
                page.locator("#pilot-reset").click()
                page.wait_for_load_state("networkidle")
                expect(page.locator("#workspace-loading")).to_be_hidden()
                expect(page.locator("#results")).to_be_hidden()
                expect(page.locator("#history-rows tr")).to_have_count(1)
                page.locator("#history-rows").get_by_role("button", name="Abrir").click()
                expect(page.locator("#metrics")).to_contain_text("11.960,00")
                with page.expect_download() as backup:
                    page.locator("#backup-export").click()
                saved_backup = os.path.join(folder, "lilium-history.json")
                backup.value.save_as(saved_backup)
                page.locator("#history-rows").get_by_role("button", name="Excluir").click()
                expect(page.locator("#history-rows tr")).to_have_count(0)
                page.locator("#backup-file").set_input_files(saved_backup)
                page.locator("#backup-merge").click()
                expect(page.locator("#backup-status")).to_contain_text("1 análises recuperadas")
                expect(page.locator("#history-rows tr")).to_have_count(1)
                page.locator("#backup-file").set_input_files(saved_backup)
                page.locator("#backup-merge").click()
                expect(page.locator("#backup-status")).to_contain_text("1 cópias idênticas ignoradas")
                expect(page.locator("#history-rows tr")).to_have_count(1)
                page.locator("#help-search").fill("previsao")
                expect(page.locator("#help-topics .help-topic:visible")).not_to_have_count(0)
                expect(page.locator("#help-empty")).to_be_hidden()
                page.locator("#help-search").fill("xyz987654321")
                expect(page.locator("#help-empty")).to_be_visible()
                page.locator("#help-clear").click()
                expect(page.locator("#help-topics .help-topic:visible")).to_have_count(15)
                page.locator("#help").get_by_text("Modelo de relato para suporte", exact=True).click()
                with page.expect_download() as support_download:
                    page.locator("#help-download").click()
                assert support_download.value.suggested_filename == "lilium-relato-suporte.txt"
                page.locator("#starter-scenario").select_option("restaurant")
                page.locator("#starter-target").select_option("all")
                with page.expect_download() as sample_download:
                    page.locator("#starter-export").click()
                assert sample_download.value.suggested_filename == "lilium-restaurant-starter.json"
                page.locator("#starter-load").click()
                expect(page.locator("#starter-status")).to_contain_text("7 conjunto(s)")
                expect(page.locator("#sales-csv")).to_have_value(re.compile("Prato executivo"))
                expect(page.locator("#ops-csv")).to_have_value(re.compile("Preparação"))
                expect(page.locator("#results")).to_be_hidden()
                expect(page.locator("#history-rows tr")).to_have_count(1)
                page.locator("#run").click()
                expect(page.locator("#results")).to_be_visible()
                expect(page.locator("#rows tr")).to_have_count(9)
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
