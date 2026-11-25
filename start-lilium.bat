@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3 -m venv .venv
  if errorlevel 1 goto fail
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto fail
echo Open http://127.0.0.1:8000 in your browser.
echo Press Ctrl+C to stop the local server.
".venv\Scripts\python.exe" -m uvicorn core.api:app --host 127.0.0.1 --port 8000
if errorlevel 1 goto fail
exit /b 0
:fail
echo Setup or startup failed. Check Python installation and internet access.
pause
exit /b 1
