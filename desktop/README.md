# Lilium Desktop v0.14.0 — Windows preview

This is a development preview, not a signed installer or a commercial release. The desktop launcher runs the local FastAPI application and opens the default browser after the server reports readiness. It is not yet a native desktop window. Keep its console open; Ctrl+C stops the server. No telemetry, account or external AI is included.

**Version scope:** Lilium's 1.0 public milestone applies to [Web Lab](https://kgasil.github.io/lilium/#lab); Desktop remains v0.14.0. The remediated Windows CI build passed; manual clean-machine acceptance remains pending. See [current release status](../README.md).

**Integration candidate:** manually import the Web Lab synthetic Connect JSON or Mini 0.1.3 candidate CSV. No shared account, automatic sync or remote API. See [component matrix](../docs/component-matrix.json) and [handoff guide](../docs/stage-06-integration-2026-11-27.md).

**Experience branch:** dark rosé Workspace, executive view first and preserved local calculations. A build from this source is a new development candidate, not the designated historical v0.14.0 artifact. Do not substitute its ZIP or hash without repeat acceptance.

## Run from source (Windows)
1. Install 64-bit Python 3.12 with the Windows Python launcher.
2. Download/extract the repository and double-click `start-lilium.bat`.
3. The first run creates a virtual environment, updates pip to the pinned setup version and installs dependencies (internet required). The SHA-256 fingerprint of requirements.txt determines whether installation must run again; subsequent launches reuse the environment. This fingerprint tracks the manifest, not installed file integrity.
4. The launcher opens a local browser address, using a port reserved directly on 127.0.0.1. If the browser does not open, use the printed address. No fixed port is required. Keep the console open.

## Setup, diagnosis and recovery
- **start-lilium.bat**: Windows x64 with 64-bit Python 3.12. Runs setup, checks the environment interpreter, installs requirements when the manifest changes and opens the application.
- **diagnose-lilium.bat**: does not install packages or start a browser. Prints a local JSON report with runtime/platform, app version, pinned dependency versions (match status), bundled asset presence, temporary SQLite write, loopback socket and API self-test status. No personal paths or history contents appear in the JSON. Other console output is not part of the report. `Lilium.exe --diagnostics` runs the same checks in a portable build.
- **repair-lilium.bat**: close all running Lilium instances first. Explicit confirmation is required before reinstalling pinned dependencies (internet required). It runs pip check and then diagnostics; no user data or environment directories are deleted. If .venv is incomplete or uses the wrong Python version, close Lilium, rename .venv to a spare name, then run start-lilium.bat. Keep backups of saved history. Repair is not an atomic package upgrade.
- Portable executable problems: obtain a fresh complete build folder from a verified successful workflow; do not replace individual DLLs or bypass Windows warnings.
- A passing diagnosis does not establish compatibility with every Windows device, actual history integrity, browser behavior, or security certification. No automatic update or telemetry.

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

## History inconsistency troubleshooting
If History reports an inconsistent database, stop Lilium and preserve the original database and any existing backup files. Do not overwrite it, delete records to hide the error, or repeatedly attempt to merge a conflicting backup. The application returns a structured error and does not repair corrupted snapshots automatically. Request support with the error code and version, not business data or personal paths. QA covered invalid JSON, inconsistent totals, authorized backup recovery, token renewal and transactional rollback; no clean Windows installation has yet been confirmed.

## Workspace navigation
The sidebar groups the existing modules by business purpose. Start with the guided task cards and glossary in Comece por aqui. The skip link goes directly to the main content; module links focus their destination and mark the selected anchor. Tables have named focusable scroll regions. The page remains a single document and retains session results when navigating. Browser and assistive-technology validation are still required.

## Final validation procedure
The source and portable executable must both pass live lifecycle testing, including restart persistence, token rotation and backup recovery. Run `python tests/smoke_lifecycle.py` from the source root, or pass the full executable path as its argument. The lifecycle test passed on Linux against the current source launcher. For the complete Windows workflow, open Actions > Lilium Desktop - Windows validation > Run workflow, select main, and inspect the job results. If the workflow fails, use the failed step log; do not publish a package or bypass checks. Only a confirmed successful run produces the preview artifact. Windows CI and Chromium passed for the remediated candidate in run 45722415976; manual device checks remain pending.

## Security remediation and candidate acceptance (2026-11-25)
The earlier v0.14.0 portable packages are superseded due to reported dependency vulnerabilities. Do not install them. FastAPI 0.165.0, Starlette 1.10.0, Pillow 13.0.0 and pip 26.3 are the remediation candidate. [Independent audit 45722416001](https://github.com/Kgasil/lilium/actions/runs/45722416001) reports no known vulnerabilities in its current resolved environment. The actual Windows build is separately audited before packaging; full build, browser and ZIP checks passed in run 45722415976. These are known-advisory checks only, not a binary security audit or assurance of absence of vulnerabilities. See [clean-machine validation](../docs/clean-machine-validation.md). Use synthetic data only. For non-sensitive feedback, [open a public issue](https://github.com/Kgasil/lilium/issues/new/choose); never disclose private links or vulnerability exploitation details in public.

## Current validated CI candidate
Use only the remediated v0.14.0 [workflow candidate](https://github.com/Kgasil/lilium/actions/runs/45722415976) for manual acceptance with synthetic data. [Portable artifact](https://github.com/Kgasil/lilium/actions/runs/45722415976/artifacts/15071874653), expires 2026-12-09 UTC. Verify the inner ZIP SHA-256 `95ef0b0b96824b47c87e3784e8c9985796cefdfb76e1bea445b3e09ab0efe392` against the trusted run. Follow [the clean-device instructions](../docs/clean-machine-validation.md). Prior packages remain superseded. Unsigned portable preview; no public pilot yet.
