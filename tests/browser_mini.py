"""Exercise Mini's actual popup assets in Chromium (not extension installation)."""
import json
import os
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from contextlib import contextmanager
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

EXT = Path(__file__).resolve().parent.parent / 'extension'
manifest = json.loads((EXT / 'manifest.json').read_text(encoding='utf-8'))
assert manifest['manifest_version'] == 3
assert manifest['action']['default_popup'] == 'popup.html'
assert not any(manifest.get(key) for key in ('permissions', 'host_permissions', 'optional_permissions', 'optional_host_permissions', 'background', 'content_scripts'))

@contextmanager
def local_site():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(EXT)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}'
    finally:
        server.shutdown()
        server.server_close()
        thread.join()

with local_site() as origin, sync_playwright() as p:
    options = {'executable_path': os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
    browser = p.chromium.launch(**options)
    page = browser.new_page(viewport={'width': 350, 'height': 650})
    errors, external = [], []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('request', lambda request: external.append(request.url) if request.url.startswith(('https://', 'http://')) and not request.url.startswith(origin + '/') else None)
    page.goto(origin + '/popup.html')
    expect(page.get_by_label('Ferramenta')).to_have_value('profit')
    assert page.locator('body').evaluate("e => getComputedStyle(e).backgroundColor") == 'rgb(48, 36, 47)'
    assert page.locator('html').evaluate("e => getComputedStyle(e).colorScheme") == 'dark'
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')

    def calculate(tool, values):
        page.locator('#tool').select_option(tool)
        for i, value in enumerate(values):
            page.locator(f'#field{i}').fill(value)
        page.get_by_role('button', name='Calcular').click()

    calculate('profit', ['1000', '600'])
    expect(page.locator('#result-value')).to_contain_text('400,00')
    expect(page.locator('#detail')).to_contain_text('40%')
    page.locator('#handoff-export').click()
    expect(page.locator('#handoff-status')).to_contain_text('data válida')
    page.locator('#handoff-date').fill('2026-11-27')
    with page.expect_download() as handoff:
        page.locator('#handoff-export').click()
    assert handoff.value.suggested_filename == 'lilium-mini-insights.csv'
    assert Path(handoff.value.path()).read_text(encoding='utf-8') == 'date,revenue,cost\n2026-11-27,1000.00,600.00\n'
    page.locator('#field0').fill('20')
    expect(page.locator('#result')).to_be_hidden()
    expect(page.locator('#handoff')).to_be_hidden()
    calculate('profit', ['20', '30'])
    expect(page.locator('#result-value')).to_contain_text('10,00')
    expect(page.locator('#detail')).to_contain_text('-50%')
    calculate('profit', ['0', '1'])
    expect(page.locator('#detail')).to_contain_text('Indisponível')
    calculate('profit', ['0,10', '0,02'])
    expect(page.locator('#result-value')).to_contain_text('0,08')
    calculate('pricing', ['60', '40'])
    expect(page.locator('#result-value')).to_contain_text('100,00')
    calculate('pricing', ['60', '100'])
    expect(page.locator('#error')).to_contain_text('menor que 100%')
    expect(page.locator('#result')).to_be_hidden()
    calculate('breakeven', ['1001', '100', '60'])
    expect(page.locator('#result-value')).to_have_text('26 unidades')
    calculate('breakeven', ['100', '40', '40'])
    expect(page.locator('#result-value')).to_have_text('Inatingível')
    calculate('profit', ['-1', '2'])
    expect(page.locator('#error')).to_contain_text('não negativo')
    page.locator('#tool').select_option('pricing')
    expect(page.locator('#error')).to_be_empty()
    expect(page.locator('#result')).to_be_hidden()
    expect(page.get_by_label('Custo unitário (R$)')).to_be_visible()
    page.reload()
    expect(page.locator('#field0')).to_have_value('')
    expect(page.locator('#field1')).to_have_value('')
    assert not errors, errors
    assert not external, external
    print('PASS: manifest, all 3 calculator UIs, validation, reset-on-change/reload, labels, no observed external HTTP(S) requests or JS errors.')
    print('Chromium:', browser.version)
    browser.close()
