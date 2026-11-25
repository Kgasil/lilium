@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv-build\Scripts\python.exe" (
  py -3.12 -m venv .venv-build
  if errorlevel 1 goto fail
)
".venv-build\Scripts\python.exe" -m pip install pip==26.3
if errorlevel 1 goto fail
".venv-build\Scripts\python.exe" -m pip install -r requirements-build.txt
if errorlevel 1 goto fail
".venv-build\Scripts\python.exe" -m unittest discover -s tests -v
if errorlevel 1 goto fail
".venv-build\Scripts\python.exe" -m desktop.build_windows
if errorlevel 1 goto fail
echo Build OK: dist\Lilium\Lilium.exe
pause
exit /b 0
:fail
echo Build failed. Check the output above.
pause
exit /b 1
