@echo off
REM Setup Script for Windows
REM This script installs the uv package manager and optionally ffmpeg

echo.
echo ========================================
echo   Setting up Song Finder dependencies
echo   (uv and ffmpeg installation)
echo ========================================
echo.

REM Check if PowerShell is available
where /q powershell
if errorlevel 1 (
    echo Error: PowerShell is required to install uv
    echo Please install PowerShell or install uv manually from https://astral.sh/uv
    pause
    exit /b 1
)

REM Run the uv installation script
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

echo.
if errorlevel 1 (
    echo Error: uv installation failed. Please check your internet connection.
    echo You can try installing manually from https://astral.sh/uv
) else (
    echo ========================================
    echo   uv installed successfully!
    echo ========================================
    echo.
    echo You can now use uv by reopening your terminal/command prompt.
    echo.
    echo To verify installation, run:
    echo   uv --version
)

REM --- ffmpeg check and install guidance -----------------------------------
echo.
echo Checking for ffmpeg (required for Song Finder audio downloads)...
where /q ffmpeg
if errorlevel 1 (
    echo ffmpeg executable not found in PATH.
    echo Attempting to install via winget (if available)...
    winget install --silent --id=FFmpeg.FFmpeg 2>nul
    if errorlevel 1 (
        echo.
        echo Could not install ffmpeg automatically.
        echo Please download ffmpeg from https://ffmpeg.org/download.html and
        echo add its bin folder to your PATH manually.
        echo Example on Windows:
        echo   unzip ffmpeg-*-win64.zip && setx PATH "%%PATH%%;C:\path\to\ffmpeg\bin"
    ) else (
        echo ffmpeg installed successfully via winget.
        echo Please reopen your terminal/command prompt to refresh PATH.
    )
) else (
    echo ffmpeg is already installed and available in PATH.
)

echo.
pause
