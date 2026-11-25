@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3 -m venv .venv
  if errorlevel 1 goto fail
)
if not exist ".venv\.lilium-0.14-ready" (
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 goto fail
  echo ready>".venv\.lilium-0.14-ready"
)
".venv\Scripts\python.exe" -m desktop.launcher
if errorlevel 1 goto fail
exit /b 0
:fail
echo Startup failed. Check Python, dependencies and LOCALAPPDATA.
echo Delete .venv\.lilium-0.14-ready to reinstall dependencies on the next run.
pause
exit /b 1
