@echo off
chcp 65001 >nul
cd /d "%~dp0"

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

:: --- Crear acceso directo en el escritorio la primera vez ---
if not exist "%USERPROFILE%\Desktop\RaidHelper Dashboard.lnk" (
    echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\crearacceso.vbs"
    echo sLinkFile = "%USERPROFILE%\Desktop\RaidHelper Dashboard.lnk" >> "%TEMP%\crearacceso.vbs"
    echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\crearacceso.vbs"
    echo oLink.TargetPath = "%~dp0launcher.bat" >> "%TEMP%\crearacceso.vbs"
    echo oLink.WorkingDirectory = "%~dp0" >> "%TEMP%\crearacceso.vbs"
    echo oLink.Description = "RaidHelper Dashboard" >> "%TEMP%\crearacceso.vbs"
    echo oLink.Save >> "%TEMP%\crearacceso.vbs"
    cscript //nologo "%TEMP%\crearacceso.vbs"
    del "%TEMP%\crearacceso.vbs"
    echo  ✅ Acceso directo creado en el escritorio.
)

:: --- Verificar configuración y lanzar ---
if not exist "api.txt" goto setup
if not exist "servers.txt" goto setup
goto launch

:setup
python setup.py auto
if errorlevel 1 exit /b

:launch
python app.py

:: --- Si la app termina con código especial, abrir menú ---
if errorlevel 2 (
    python setup.py menu
    goto launch
)