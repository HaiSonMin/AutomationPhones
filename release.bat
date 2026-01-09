@echo off
REM Release Script - Build, Commit, Push, and Create GitHub Release
REM Complete automation for deploying a new version

echo ====================================
echo   AutomationTool - Release Script
echo ====================================
echo.

REM Get current version
for /f "tokens=2 delims=:, " %%a in ('findstr "version" version.json') do set VERSION=%%~a
set VERSION=%VERSION:"=%
echo Current version: %VERSION%
echo.

REM Confirm release
set /p CONFIRM="Release version %VERSION%? (y/n): "
if not "%CONFIRM%"=="y" (
    echo Release cancelled.
    pause
    exit /b 0
)
echo.

REM Step 1: Build application
echo ====================================
echo STEP 1: Building application
echo ====================================
call build.bat
if errorlevel 1 (
    echo Build failed! Aborting release.
    pause
    exit /b 1
)
echo.

REM Step 2: Commit and push to git
echo ====================================
echo STEP 2: Committing and pushing to git
echo ====================================
set COMMIT_MSG=Release v%VERSION% - Auto-update system
echo Commit message: %COMMIT_MSG%
echo.

git add .
git commit -m "%COMMIT_MSG%"
git push hs main
if errorlevel 1 (
    echo Git push failed! Please resolve manually.
    pause
    exit /b 1
)
echo Done.
echo.

REM Step 3: Create GitHub Release
echo ====================================
echo STEP 3: Creating GitHub Release
echo ====================================
echo.

REM Check if GitHub CLI is installed
gh version >nul 2>&1
if errorlevel 1 (
    echo GitHub CLI not found!
    echo.
    echo Please create release manually:
    echo 1. Go to: https://github.com/HaiSonMin/AutomationPhones/releases/new
    echo 2. Tag: v%VERSION%
    echo 3. Title: Version %VERSION%
    echo 4. Upload: dist\AutomationTool-%VERSION%.exe
    echo.
    start https://github.com/HaiSonMin/AutomationPhones/releases/new
    pause
    exit /b 0
)

REM Get changelog from version.json
for /f "tokens=2 delims=:, " %%a in ('findstr "changelog" version.json') do set CHANGELOG=%%~a
set CHANGELOG=%CHANGELOG:"=%

REM Create release with GitHub CLI
echo Creating release v%VERSION%...
gh release create v%VERSION% ^
    --repo HaiSonMin/AutomationPhones ^
    --title "Version %VERSION%" ^
    --notes "%CHANGELOG%" ^
    "dist\AutomationTool-%VERSION%.exe"

if errorlevel 1 (
    echo GitHub release creation failed!
    echo Please create manually at: https://github.com/HaiSonMin/AutomationPhones/releases/new
    start https://github.com/HaiSonMin/AutomationPhones/releases/new
    pause
    exit /b 1
)

echo.
echo ====================================
echo   Release v%VERSION% completed!
echo ====================================
echo.
echo GitHub Release: https://github.com/HaiSonMin/AutomationPhones/releases/tag/v%VERSION%
echo.
echo Users can now update their app automatically!
echo.
pause
