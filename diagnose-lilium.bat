@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Environment missing. Run start-lilium.bat first.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m desktop.launcher --diagnostics
set "RESULT=%ERRORLEVEL%"
pause
exit /b %RESULT%
