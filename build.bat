@echo off
REM Build Script - Package application with PyInstaller
REM This script builds the AutomationTool into a standalone .exe

echo ====================================
echo   AutomationTool - Build Script
echo ====================================
echo.

REM Get version from version.json
for /f "tokens=2 delims=:, " %%a in ('findstr "version" version.json') do set VERSION=%%~a
set VERSION=%VERSION:"=%
echo Current version: %VERSION%
echo.

REM Check if scrcpy is installed (required for device monitoring)
echo [1/6] Checking scrcpy...
scrcpy --version >nul 2>&1
if errorlevel 1 (
    echo scrcpy not found. Installing via Chocolatey...
    echo.
    echo NOTE: This requires Chocolatey package manager.
    echo If installation fails, please install manually:
    echo   - Download from: https://github.com/Genymobile/scrcpy/releases
    echo   - Or run: choco install scrcpy
    echo.
    choco install scrcpy -y
    if errorlevel 1 (
        echo WARNING: scrcpy installation failed!
        echo The app will build, but device monitoring will not work.
        echo Please install scrcpy manually.
        pause
    ) else (
        echo scrcpy installed successfully.
    )
) else (
    echo scrcpy found.
)
echo.

REM Check if PyInstaller is installed
echo [2/6] Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
) else (
    echo PyInstaller found.
)
echo.

REM Clean previous builds
echo [3/6] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo Done.
echo.

REM Build React UI first
echo [4/6] Building React UI...
cd ui
call npm run build
if errorlevel 1 (
    echo Error: React build failed!
    pause
    exit /b 1
)
cd ..
echo Done.
echo.

REM Build Python executable
echo [5/6] Building Python executable...
pyinstaller --onefile ^
    --name "AutomationTool-%VERSION%" ^
    --icon=ui/public/favicon.ico ^
    --add-data "version.json;." ^
    --add-data "ui/dist;ui/dist" ^
    --hidden-import=webview ^
    --hidden-import=keyring ^
    --hidden-import=requests ^
    --noconsole ^
    main.py

if errorlevel 1 (
    echo Error: Build failed!
    pause
    exit /b 1
)
echo Done.
echo.

REM Show results
echo [6/6] Build completed!
echo.
echo Output file: dist\AutomationTool-%VERSION%.exe
echo File size:
dir dist\AutomationTool-%VERSION%.exe | findstr "AutomationTool"
echo.

REM Ask to run
set /p RUN="Do you want to run the application? (y/n): "
if /i "%RUN%"=="y" (
    start "" "dist\AutomationTool-%VERSION%.exe"
)

echo.
echo Build complete! Ready for GitHub Release.
pause
