@echo off
REM Build Student & Teacher Info as a standalone .exe
REM Requires: pip install pyinstaller

cd /d "%~dp0"

echo Checking for PyInstaller...
python -c "import PyInstaller" 2>nul || (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Building application...
pyinstaller --noconfirm gui.spec

if exist "dist\Student Teacher Info.exe" (
    echo.
    echo Done. Executable: dist\Student Teacher Info.exe
    echo You can copy the .exe anywhere; data files will be created in the same folder when you run it.
) else (
    echo Build may have failed. Check the output above.
)
pause
