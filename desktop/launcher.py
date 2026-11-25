"""Loopback-only desktop launcher; bundled browser interface, no telemetry."""
import argparse
import os
from pathlib import Path
import socket
import sys
import tempfile
import threading
import time
import webbrowser

VERSION = "0.14.0"
ASSETS = ("dashboard", "finance", "sales", "operations", "strategy", "reports",
          "forecast", "flow", "connect", "copilot", "workspace")


def data_directory():
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA")
        if not base or not Path(base).is_absolute():
            raise RuntimeError("LOCALAPPDATA indisponivel. Inicie em uma conta Windows normal.")
        return Path(base) / "K&G Vision" / "Lilium"
    # Useful for development and CI; Windows is the intended distribution target.
    base = os.environ.get("XDG_DATA_HOME")
    return (Path(base) if base and Path(base).is_absolute()
            else Path.home() / ".local" / "share") / "kg-vision" / "lilium"


def configure_app(directory):
    from core.api import app
    from core.store import HistoryStore
    from core.session import new_token
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    app.state.history = HistoryStore(directory / "lilium.sqlite3")
    app.state.session_token = new_token()
    return app


def reserve_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if sys.platform == "win32" and hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        sock.bind(("127.0.0.1", 0))
        sock.listen(128)
        return sock
    except BaseException:
        sock.close()
        raise


def self_test(quiet=False):
    """Exercise bundled HTML, all module assets, and temporary SQLite; no user data."""
    from fastapi.testclient import TestClient
    from core.api import app
    previous = app.state.history
    previous_token = app.state.session_token
    try:
        with tempfile.TemporaryDirectory(prefix="lilium-check-") as folder:
            app = configure_app(folder)
            with TestClient(app, base_url="http://127.0.0.1", headers={"X-Lilium-Session": app.state.session_token}) as client:
                def require(condition, label):
                    if not condition:
                        raise RuntimeError("Self-test failed: " + label)
                require(client.get("/health").json()["version"] == VERSION, "version")
                page = client.get("/")
                require(page.status_code == 200 and "Workspace" in page.text, "workspace")
                for name in ASSETS:
                    path = "/assets/" + name + ".js"
                    response = client.get(path)
                    require(response.status_code == 200 and path in page.text
                            and "javascript" in response.headers.get("content-type", ""), name)
                csv = b"date,revenue,cost\n2026-01-01,100,60"
                headers = {"Content-Type": "text/csv", "Origin": "http://127.0.0.1"}
                response = client.post("/api/v1/analyze", content=csv, headers=headers)
                require(response.status_code == 200 and response.json()["totals"]["result_cents"] == 4000, "analysis")
                saved = client.post("/api/v1/history", content=csv, headers=headers)
                require(saved.status_code == 201, "save")
                key = saved.json()["id"]
                require(len(client.get("/api/v1/history").json()["items"]) == 1, "history")
                require(client.delete("/api/v1/history/" + key, headers=headers).status_code == 200, "delete")
                require(client.get("/api/v1/history", headers={"X-Lilium-Session": "invalid"}).status_code == 403, "session")
                require(client.get("/health", headers={"Host": "example.com"}).status_code == 400, "host")
                require(client.post("/api/v1/analyze", content=csv, headers={**headers, "Origin": "https://example.com"}).status_code == 403, "origin")
    finally:
        app.state.history = previous
        app.state.session_token = previous_token
    if not quiet:
        print("Lilium Desktop self-test OK", flush=True)


def serve(no_browser=False):
    import uvicorn
    from core.session import access_url
    directory = data_directory()
    app = configure_app(directory)
    # Reserve the actual socket instead of probing and reopening a free port.
    with reserve_socket() as sock:
        url = "http://127.0.0.1:" + str(sock.getsockname()[1])
        launch_url = access_url(url, app.state.session_token)
        config = uvicorn.Config(app, host="127.0.0.1", port=sock.getsockname()[1],
                               loop="asyncio", http="h11", ws="none",
                               proxy_headers=False, access_log=False,
                               log_level="warning")
        server = uvicorn.Server(config)
        stop = threading.Event()

        def ready():
            deadline = time.monotonic() + 30
            while not stop.is_set() and time.monotonic() < deadline:
                if server.started and not stop.is_set():
                    print("LILIUM_READY " + launch_url, flush=True)
                    print("Link privado desta sessao; nao compartilhe.", flush=True)
                    if not no_browser:
                        try:
                            if not webbrowser.open(launch_url):
                                print("Abra o endereco acima no navegador.", flush=True)
                        except Exception:
                            print("Abra o endereco acima no navegador.", flush=True)
                    return
                stop.wait(0.1)
            if not stop.is_set():
                print("Inicializacao demorou demais.", file=sys.stderr, flush=True)
                server.should_exit = True

        print("Lilium Desktop " + VERSION, flush=True)
        print("Mantenha esta janela aberta. Ctrl+C para encerrar.", flush=True)
        thread = threading.Thread(target=ready, daemon=True)
        thread.start()
        try:
            server.run(sockets=[sock])
        finally:
            stop.set()
            thread.join(timeout=1)
        return 0 if server.started else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="Lilium Desktop local preview")
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--no-browser", action="store_true")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--diagnostics", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.diagnostics:
            import json
            from desktop.diagnostics import report
            result = report(VERSION, ASSETS, data_directory, reserve_socket, lambda: self_test(quiet=True))
            print(json.dumps(result, indent=2), flush=True)
            return 0 if result["ready"] else 1
        if args.self_test:
            self_test()
            return 0
        return serve(args.no_browser)
    except KeyboardInterrupt:
        return 0
    except Exception as exc:
        print("Falha ao iniciar Lilium: " + type(exc).__name__, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
