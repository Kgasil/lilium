# Lilium Desktop v0.14.0 — Windows preview

This is a development preview, not a signed installer or a commercial release. The desktop launcher runs the local FastAPI application and opens the default browser after the server reports readiness. It is not yet a native desktop window. Keep its console open; Ctrl+C stops the server. No telemetry, account or external AI is included.

## Run from source (Windows)
1. Install 64-bit Python 3.12 with the Windows Python launcher.
2. Download/extract the repository and double-click `start-lilium.bat`.
3. The first run creates a virtual environment and installs dependencies (internet required). The SHA-256 fingerprint of requirements.txt determines whether installation must run again; subsequent launches reuse the environment. This fingerprint tracks the manifest, not installed file integrity.
4. The launcher opens a local browser address, using a port reserved directly on 127.0.0.1. If the browser does not open, use the printed address. No fixed port is required. Keep the console open.

## Setup, diagnosis and recovery
- **start-lilium.bat**: Windows x64 with 64-bit Python 3.12. Runs setup, checks the environment interpreter, installs requirements when the manifest changes and opens the application.
- **diagnose-lilium.bat**: does not install packages or start a browser. Prints a local JSON report with runtime/platform, app version, pinned dependency versions (match status), bundled asset presence, temporary SQLite write, loopback socket and API self-test status. No personal paths or history contents appear in the JSON. Other console output is not part of the report. `Lilium.exe --diagnostics` runs the same checks in a portable build.
- **repair-lilium.bat**: close all running Lilium instances first. Explicit confirmation is required before reinstalling pinned dependencies (internet required). It runs pip check and then diagnostics; no user data or environment directories are deleted. If .venv is incomplete or uses the wrong Python version, close Lilium, rename .venv to a spare name, then run start-lilium.bat. Keep backups of saved history. Repair is not an atomic package upgrade.
- Portable executable problems: obtain a fresh complete build folder from a verified successful workflow; do not replace individual DLLs or bypass Windows warnings.
- A passing diagnosis does not establish Windows compatibility, actual history integrity, browser behavior, or security certification. No automatic update or telemetry.

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
[Windows workflow](https://github.com/Kgasil/lilium/actions/workflows/desktop-windows.yml) runs on relevant main-branch changes and can be started manually. It runs Python and JavaScript regression tests, source-server smoke test, PyInstaller build, executable self-test, and bundled live-server smoke test. The workflow also installs Chromium for a browser-level pilot smoke test against the bundled application, including module calculations, local history, Connect transfer, report export, session reset and mobile-width overflow. Only on success is an expiring development artifact uploaded. This configuration does not publish a release. At the time of implementation, the Windows job result, actual binary and interactive browser checks have not been verified.

## Versioned packages and manual updates
After all preceding Windows checks pass, CI creates a versioned ZIP, manifest.json and SHA256SUMS.txt; it verifies and stages the archive, then smoke-tests the staged executable before uploading a development artifact. The workflow summary records the archive hash and commit. No public release is created.
From trusted source checkout, with Python 3.12:
```powershell
python -m desktop.release_manager --help
python -m desktop.release_manager package --source dist/Lilium --output release-preview --commit (git rev-parse HEAD)
```
For a verified successful workflow, download and extract the outer Actions artifact, obtain the expected SHA-256 independently from the trusted run summary, then check the inner archive (replace the example variable with the real trusted digest):
```powershell
$sha = "REPLACE_WITH_TRUSTED_64_CHARACTER_LOWERCASE_SHA256"
python -m desktop.release_manager verify --archive release-preview/Lilium-0.14.0-windows-x64-preview.zip --manifest release-preview/manifest.json --sha256 $sha
New-Item -ItemType Directory -Force -Path "$HOME/LiliumVersions"
python -m desktop.release_manager stage --archive release-preview/Lilium-0.14.0-windows-x64-preview.zip --manifest release-preview/manifest.json --sha256 $sha --parent "$HOME/LiliumVersions"
```
Adjust the extracted artifact path if needed. Staging validates file paths, collision rules, ZIP sizes and SHA-256; it extracts into a unique new folder without executing code or overwriting the old installation. Use a private, trusted destination directory. Close Lilium and export a history backup before switching versions. Only launch a validated package manually, keeping the old complete folder. Versions share the per-user database; reverting binaries is not a database rollback, and database compatibility between future versions is not guaranteed. Do not launch multiple versions simultaneously. SHA-256 detects mismatches against a trusted expected hash, not malware or publisher identity. Manifest metadata is unsigned; compare version and commit against the trusted run. No updater service, downloads, signing, migration or automatic installation. The helper requires Python; Windows users can also independently compare the SHA-256 with Get-FileHash before manually extracting a trusted package. Never bypass OS warnings.

## Local storage
Desktop history: `%LOCALAPPDATA%\K&G Vision\Lilium\lilium.sqlite3`. Only explicitly saved Insights aggregates are persisted. Other module results remain in session memory. The old development database at `data/lilium.sqlite3` is separate and is not migrated or deleted automatically. In Workspace > Histórico local, export a versioned JSON history backup and recover it using the merge control. Recovery validates the aggregate contract, adds new IDs only, skips exact copies and rolls back on conflict or capacity limit. Limit: 16 MiB per backup, 200 snapshots. This is not a full database or session backup. Keep unencrypted files private. Stop the app before manually moving database files; never overwrite existing data without a backup. Desktop API now requires a per-process bearer capability; no user accounts, app-level encryption, multiuser isolation, auto-update, signing or secure erasure. Use synthetic data only. The API listens on loopback. Keep the private launch link secret; any process with its token can access the API, and local processes with file permissions may read storage. Do not expose it on the network.

## Pilot gate
Require successful Windows build and smoke tests, browser interaction tests beyond the automated smoke test, manual installation on a clean Windows machine, persistence/restart and upgrade checks, accessible navigation, security review and documented feedback process before inviting real business users. The first controlled pilot should remain free, with synthetic data until security and privacy readiness are established.

## Desktop access and privacy
Open the private launch link printed by the Desktop launcher, not just the bare local URL. It contains a temporary capability that Workspace removes from the address bar and retains in tab sessionStorage. Stop Desktop to invalidate it. Never share it. Direct development API mode is unguarded and intended only for tests. See [Trust & Privacy](../docs/trust-privacy.md).
