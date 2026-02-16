@echo off
cd /d "%~dp0"

if exist "dist\Student Teacher Info.exe" (
    start "" "dist\Student Teacher Info.exe"
) else (
    echo Starting with Python...
    python gui.py
    if errorlevel 1 pause
)
