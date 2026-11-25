# Lilium Desktop v0.14.0 — Windows preview

This is a development preview, not a signed installer or a commercial release. The desktop launcher runs the local FastAPI application and opens the default browser after the server reports readiness. It is not yet a native desktop window. Keep its console open; Ctrl+C stops the server. No telemetry, account or external AI is included.

## Run from source (Windows)
1. Install 64-bit Python 3.12 with the Windows Python launcher.
2. Download/extract the repository and double-click `start-lilium.bat`.
3. The first run for this version creates a virtual environment and installs dependencies (internet required). Later runs reuse it. If dependencies fail, delete the `.venv/.lilium-0.14-ready` marker and retry.
4. The launcher opens a local browser address, using a port reserved directly on 127.0.0.1. If the browser does not open, use the printed address. No fixed port is required. Keep the console open.

## Build a portable Windows folder
Use Windows x64 and 64-bit Python 3.12. Run `build-lilium.bat`, or from the repository root:

```powershell
py -3.12 -m venv .venv-build
.\.venv-build\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv-build\Scripts\python.exe -m unittest discover -s tests -v
.\.venv-build\Scripts\python.exe -m desktop.build_windows
.\.venv-build\Scripts\python.exe tests/smoke_desktop.py dist/Lilium/Lilium.exe
```

The build uses PyInstaller in one-directory mode, bundles Workspace and its JavaScript modules, and rasterizes the official lily symbol into a multi-size ICO. It runs an executable self-test with temporary data. Keep the entire `dist/Lilium/` folder together, then open `Lilium.exe`. A successful bundle should not require Python installed on the end user's machine. The binary is unsigned; don't distribute until the build and pilot validation pass. No instruction to bypass OS warnings.

## CI validation and artifacts
[Windows workflow](https://github.com/Kgasil/lilium/actions/workflows/desktop-windows.yml) runs on relevant main-branch changes and can be started manually. It runs Python and JavaScript regression tests, source-server smoke test, PyInstaller build, executable self-test, and bundled live-server smoke test. Only on success is an expiring development artifact uploaded. This configuration does not publish a release. At the time of implementation, the Windows job result, actual binary and interactive browser checks have not been verified.

## Local storage
Desktop history: `%LOCALAPPDATA%\K&G Vision\Lilium\lilium.sqlite3`. Only explicitly saved Insights aggregates are persisted. Other module results remain in session memory. The old development database at `data/lilium.sqlite3` is separate and is not migrated or deleted automatically. Stop the app before backing up or manually moving databases; never overwrite existing data without a backup. No app-level encryption, authentication, multiuser isolation, auto-update, signing or secure erasure. Use synthetic data only. The API listens on loopback, but other local processes can access it. Do not expose it on the network.

## Pilot gate
Require successful Windows build and smoke tests, full browser interaction tests, manual installation on a clean Windows machine, persistence/restart and upgrade checks, accessible navigation, security review and documented feedback process before inviting real business users. The first controlled pilot should remain free, with synthetic data until security and privacy readiness are established.
