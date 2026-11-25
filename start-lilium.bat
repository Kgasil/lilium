@echo off
setlocal
cd /d "%~dp0"
py -3.12 -m desktop.setup_env
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m desktop.launcher
if errorlevel 1 goto fail
exit /b 0
:fail
echo Startup failed. Run diagnose-lilium.bat or consult desktop\README.md.
echo Close Lilium before running repair-lilium.bat.
pause
exit /b 1
