@echo off
REM uv Installation Script for Windows
REM This script installs uv package manager

echo.
echo ========================================
echo   Installing uv for Windows
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
    echo Error: Installation failed. Please check your internet connection.
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

pause
