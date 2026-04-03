#!/bin/bash
# Launcher para RaidHelper Viewer — Linux / macOS

cd "$(dirname "$0")"

# --- Verificar Python 3 ---
if ! command -v python3 &>/dev/null; then
    echo ""
    echo " ❌ Python 3 no está instalado o no está en el PATH."
    echo "    Descárgalo desde https://www.python.org/downloads/"
    echo ""
    read -rp " Presiona Enter para salir..."
    exit 1
fi

# --- Instalar dependencias si hace falta ---
if ! python3 -c "import textual" &>/dev/null; then
    echo " Instalando dependencias..."
    pip3 install textual requests -q
fi

# --- Verificar configuración ---
if [ ! -f "api.txt" ] || [ ! -f "api_key.txt" ] || [ ! -f "servers.txt" ]; then
    python3 wizard.py auto
fi

# --- Bucle principal ---
while true; do
    rm -f .exit_code
    python3 app.py

    [ ! -f .exit_code ] && break

    EXIT_CODE=$(cat .exit_code)
    rm -f .exit_code

    if [ "$EXIT_CODE" = "3" ]; then
        python3 wizard.py agregar
    elif [ "$EXIT_CODE" = "2" ]; then
        python3 wizard.py menu
    else
        break
    fi
done
