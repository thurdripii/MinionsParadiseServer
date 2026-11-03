
@echo off
title MinionsParadiseBrazil Server

cd /d "%~dp0\.."

echo ======================================
echo       MINIONS PARADISE BRAZIL
echo ======================================

if not exist venv (
    echo Creating Python environment...
    py -3.8-32 -m venv venv

    if errorlevel 1 (
        echo Failed to create Python environment.
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat

echo.
echo Installing dependencies...

python -m pip install -r server\requirements.txt

if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
)

echo.
echo Starting MinionsParadiseBrazil...

python -m server.app

echo.
echo Server stopped.
pause
