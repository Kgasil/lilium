"""Live process restart, private token and history checks with disposable storage."""
from contextlib import contextmanager
import json
import os
import queue
import subprocess
import sys
import tempfile
import threading
import time
from urllib.error import HTTPError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import build_opener, ProxyHandler, Request

CSV = b'date,revenue,cost\n2026-01-01,100,60'


@contextmanager
def running(command, folder):
    env = dict(os.environ, LOCALAPPDATA=folder, XDG_DATA_HOME=folder)
    process = subprocess.Popen(command + ["--no-browser", "--accept-terms", __import__("desktop.terms", fromlist=["TERMS_SHA256"]).TERMS_SHA256], env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
    lines = queue.Queue()
    def read():
        for line in process.stdout:
            lines.put(line.rstrip())
    thread = threading.Thread(target=read, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            try:
                line = lines.get(timeout=0.5)
            except queue.Empty:
                if process.poll() is not None:
                    raise RuntimeError('Desktop exited before readiness')
                continue
            if line.startswith('LILIUM_READY http://127.0.0.1:'):
                parts = urlsplit(line.split(' ', 1)[1])
                token = parts.fragment.removeprefix('access=')
                assert len(token) == 64 and parts.hostname == '127.0.0.1'
                yield urlunsplit((parts.scheme, parts.netloc, '', '', '')), token
                return
        raise RuntimeError('Desktop readiness timeout')
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
        thread.join(timeout=2)
        process.stdout.close()


def request(base, path, token=None, method='GET', body=None, media=None):
    headers = {}
    if token is not None:
        headers['X-Lilium-Session'] = token
    if media is not None:
        headers['Content-Type'] = media
    if method != 'GET':
        headers['Origin'] = base
    opener = build_opener(ProxyHandler({}))
    req = Request(base + path, headers=headers, data=body, method=method)
    try:
        with opener.open(req, timeout=10) as response:
            return response.status, json.load(response)
    except HTTPError as exc:
        with exc:
            return exc.code, json.load(exc)


def main(command):
    command = command or [sys.executable, '-m', 'desktop.launcher']
    with tempfile.TemporaryDirectory(prefix='lilium-lifecycle-') as folder:
        with running(command, folder) as (base, old_token):
            assert request(base, '/health')[1]['session_required'] is True
            assert request(base, '/api/v1/history')[0] == 403
            assert request(base, '/api/v1/history', old_token) == (200, {'items': []})
            status, item = request(base, '/api/v1/history', old_token, 'POST', CSV, 'text/csv')
            assert status == 201 and item['analysis']['totals']['result_cents'] == 4000
            status, backup = request(base, '/api/v1/backup', old_token)
            assert status == 200 and backup['snapshots'] == [item]
        with running(command, folder) as (base, token):
            assert old_token != token
            assert request(base, '/api/v1/history', old_token)[0] == 403
            path = '/api/v1/history/' + item['id']
            assert request(base, path, token) == (200, item)
            assert request(base, path, token, 'DELETE')[0] == 200
            assert request(base, '/api/v1/history', token) == (200, {'items': []})
            raw = json.dumps(backup).encode()
            assert request(base, '/api/v1/backup/merge', token, 'POST', raw, 'application/json') == (200, {'added': 1, 'skipped': 0})
            assert request(base, '/api/v1/backup/merge', token, 'POST', raw, 'application/json') == (200, {'added': 0, 'skipped': 1})
        with running(command, folder) as (base, final_token):
            assert token != final_token
            assert request(base, path, final_token) == (200, item)
            assert request(base, '/api/v1/history', token)[0] == 403
        print('Live lifecycle: three launches, token rotation, persistence and backup recovery OK', flush=True)


if __name__ == '__main__':
    main(sys.argv[1:])
