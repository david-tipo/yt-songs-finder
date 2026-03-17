    @echo off
    REM Song Finder - Double-click to run with songs.txt
    REM This script runs the song finder and keeps the window open to see results

    echo.
    echo ========================================
    echo   Song Finder - Processing songs.txt
    echo ========================================
    echo.

    uv run --script song_finder.py songs.txt

    echo.
    echo ========================================
    echo   Processing complete!
    echo ========================================
    echo.
    pause
