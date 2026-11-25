"""Start a real server process and verify the loopback package. Uses temporary data."""
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request


def main(command):
    if not command:
        command = [sys.executable, "-m", "desktop.launcher"]
    with tempfile.TemporaryDirectory(prefix="lilium-smoke-") as folder:
        env = dict(os.environ, LOCALAPPDATA=folder, XDG_DATA_HOME=folder)
        process = subprocess.Popen(command + ["--no-browser"], env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, encoding="utf-8", errors="replace")
        lines = queue.Queue()
        def read():
            for line in process.stdout:
                lines.put(line.rstrip())
        thread = threading.Thread(target=read, daemon=True)
        thread.start()
        try:
            deadline = time.monotonic() + 60
            url = None
            while time.monotonic() < deadline:
                try:
                    line = lines.get(timeout=0.5)
                except queue.Empty:
                    if process.poll() is not None:
                        raise RuntimeError("Desktop exited before readiness")
                    continue
                print(line, flush=True)
                if line.startswith("LILIUM_READY http://127.0.0.1:"):
                    url = line.split(" ", 1)[1]
                    break
            if url is None:
                raise RuntimeError("Desktop readiness timeout")
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            def get(path):
                with opener.open(url + path, timeout=10) as response:
                    return response.read()
            assert json.loads(get("/health"))["version"] == "0.14.0"
            html = get("/").decode()
            assert "Workspace" in html
            for name in ("dashboard", "finance", "sales", "operations", "strategy",
                         "reports", "forecast", "flow", "connect", "copilot"):
                asset = "/assets/" + name + ".js"
                assert asset in html and get(asset)
            assert json.loads(get("/api/v1/history")) == {"items": []}
            print("Live loopback smoke test OK", flush=True)
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
    main(sys.argv[1:])
