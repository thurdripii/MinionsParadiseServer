@echo off
cd /d "%~dp0"

echo ======================================
echo       MINIONS PARADISE BRAZIL
echo ======================================

if not exist venv (
    echo Criando ambiente Python...
    py -3.8-32 -m venv venv
)

call venv\Scripts\activate.bat

echo Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Iniciando servidor...
python app.py

pause
