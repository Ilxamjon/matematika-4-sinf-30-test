@echo off
cd /d "%~dp0"
if not exist "%~dp0sayt\index.html" (
  echo Avval ZIP faylni Extract All orqali toliq oching.
  pause
  exit /b 1
)
net session >nul 2>&1
if errorlevel 1 (
  echo Boshqa kompyuterlar ulanishi uchun Windows ruxsat soraydi.
  powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
  exit /b
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0lokal-server.ps1"
echo.
echo Server toxtadi.
pause
