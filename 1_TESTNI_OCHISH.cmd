@echo off
cd /d "%~dp0"
if not exist "%~dp0Informatika-30-test.html" (
  echo Avval ZIP faylni Extract All orqali toliq oching.
  pause
  exit /b 1
)
start "" "%~dp0Informatika-30-test.html"
