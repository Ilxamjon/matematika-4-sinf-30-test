@echo off
cd /d "%~dp0"
if not exist "%~dp0sayt\index.html" (
  echo Avval ZIP faylni Extract All orqali toliq oching.
  pause
  exit /b 1
)
start "" "%~dp0sayt\index.html"
