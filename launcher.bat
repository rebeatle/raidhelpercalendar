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
    python -c "
import os, winreg
from pathlib import Path
try:
    import win32com.client
    shell    = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(str(Path.home() / 'Desktop' / 'RaidHelper Dashboard.lnk'))
    shortcut.TargetPath  = os.path.abspath('launcher.bat')
    shortcut.WorkingDirectory = os.path.abspath('.')
    shortcut.IconLocation = '%SystemRoot%\\system32\\cmd.exe'
    shortcut.Save()
except:
    pass
"
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