"""Local, redacted readiness report. Never reads saved history or uses the network."""
from pathlib import Path
import platform
import sqlite3
import sys
import tempfile


def dependency_versions():
    # Explicit imports are visible to the freezer; no metadata directory required.
    import fastapi, starlette, uvicorn, httpx, openpyxl, defusedxml
    return {m.__name__: m.__version__ for m in
            (fastapi, starlette, uvicorn, httpx, openpyxl, defusedxml)}


EXPECTED = {"fastapi": "0.165.0", "starlette": "1.10.0", "uvicorn": "0.48.0", "httpx": "0.28.1",
            "openpyxl": "3.1.5", "defusedxml": "0.7.1"}


def report(version, assets, directory, reserve, self_test):
    checks = []

    def check(name, fn):
        try:
            ok = fn()
            checks.append({"id": name, "status": "pass" if ok else "fail"})
        except Exception:
            checks.append({"id": name, "status": "fail"})

    windows = sys.platform == "win32"
    supported = windows and sys.version_info[:2] == (3, 12) and platform.machine().upper() in {"AMD64", "X86_64"} and sys.maxsize > 2**32
    checks.append({"id": "windows_x64_python312", "status": "pass" if supported else "fail" if windows else "warning"})
    check("dependencies", lambda: dependency_versions() == EXPECTED)
    core = Path(__file__).resolve().parent.parent / "core"
    check("workspace_assets", lambda: all(p.is_file() and p.stat().st_size > 0 for p in [core / "workspace.html", *(core / (n + ".js") for n in assets)]))

    def storage():
        folder = Path(directory())
        folder.mkdir(parents=True, exist_ok=True)
        # A disposable file in the actual target directory, never the history database.
        with tempfile.TemporaryDirectory(prefix="lilium-diagnostic-", dir=folder) as tmp:
            from contextlib import closing
            with closing(sqlite3.connect(Path(tmp) / "probe.sqlite3")) as db, db:
                db.execute("CREATE TABLE probe (n INTEGER)")
                db.execute("INSERT INTO probe VALUES (1)")
                return db.execute("SELECT n FROM probe").fetchone()[0] == 1

    def socket_check():
        with reserve() as sock:
            return sock.getsockname()[0] == "127.0.0.1" and sock.getsockname()[1] > 0

    check("storage_write", storage)
    check("loopback", socket_check)
    def api_check():
        self_test()
        return True
    check("api_self_test", api_check)
    return {"schema_version": "1.0", "app_version": version,
            "platform": "windows" if windows else "development-other",
            "python": ".".join(map(str, sys.version_info[:3])),
            "bundled": bool(getattr(sys, "frozen", False)),
            "ready": all(c["status"] != "fail" for c in checks), "checks": checks,
            "limitations": ["No real history was read or verified.", "No browser, installer or vulnerability audit."]}
