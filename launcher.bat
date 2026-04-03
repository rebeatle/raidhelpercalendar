@echo off
chcp 65001 >nul
cd /d "%~dp0"
:: --- Launcher actualizado ver3 ---

:: --- Verificar Python ---
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ❌ Python no está instalado o no está en el PATH.
    echo  Descárgalo desde https://www.python.org/downloads/
    echo  Asegúrate de marcar "Add Python to PATH" al instalar.
    echo.
    pause
    exit /b
)

:: --- Instalar dependencias si hace falta ---
pip show textual >nul 2>&1
if errorlevel 1 (
    echo  Instalando dependencias...
    pip install textual requests -q
)

:: --- Verificar configuración ---
if not exist "api.txt" goto setup
if not exist "api_key.txt" goto setup
if not exist "servers.txt" goto setup
goto launch

:setup
python wizard.py auto
goto launch

:: --- Bucle principal ---
:launch
if exist ".exit_code" del ".exit_code"
python app.py

if not exist ".exit_code" goto fin

set /p EXIT_CODE=<.exit_code
del ".exit_code"

if "%EXIT_CODE%"=="3" (
    python wizard.py agregar
    goto launch
)
if "%EXIT_CODE%"=="2" (
    python wizard.py menu
    goto launch
)

:fin