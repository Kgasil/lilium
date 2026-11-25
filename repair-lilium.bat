@echo off
setlocal
cd /d "%~dp0"
echo Close all Lilium windows and consoles before repairing.
echo Repair reinstalls Python dependencies. Internet is required.
echo Saved Insights history is not deleted.
choice /C SN /N /M "Continue? [S/N] "
if not "%ERRORLEVEL%"=="1" exit /b 0
py -3.12 -m desktop.setup_env --repair
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m desktop.launcher --diagnostics
set "RESULT=%ERRORLEVEL%"
pause
exit /b %RESULT%
:fail
echo Repair failed. Consult desktop\README.md.
pause
exit /b 1
