import requests
from datetime import datetime
import time
import json

# --- CONFIGURACIÓN ---
with open('api.txt', 'r', encoding='utf-8') as f:
    ACCESS_TOKEN = f.read().strip()

MIS_SERVIDORES = [
    "1184252455580610570"]

ENDPOINT_EVENTS = "https://raid-helper.xyz/api/events/"

def obtener_eventos_servidor(server_id):
    """Obtiene todos los eventos de un servidor usando el accessToken de sesión."""
    payload = {
        "serverid": server_id,
        "accessToken": ACCESS_TOKEN
    }
    try:
        res = requests.post(ENDPOINT_EVENTS, json=payload, timeout=10)
        res.raise_for_status()
        datos = res.json()
        return datos.get("servername", server_id), datos.get("events", [])
    except requests.exceptions.HTTPError as e:
        print(f"  [ERROR HTTP] Servidor {server_id}: {e}")
        return server_id, []
    except Exception as e:
        print(f"  [ERROR] Servidor {server_id}: {e}")
        return server_id, []

def obtener_mi_agenda():
    """Obtiene los eventos donde ya estoy anotado (User API Key separada si la tienes)."""
    # Por ahora retorna lista vacía - se puede integrar después
    return []

def obtener_todos_los_datos():
    ahora_unix = int(time.time())
    todos_eventos = []

    print("Consultando servidores", end="", flush=True)
    for s_id in MIS_SERVIDORES:
        nombre_server, eventos = obtener_eventos_servidor(s_id)
        print(".", end="", flush=True)

        for ev in eventos:
            if int(ev.get("unixtime", 0)) > ahora_unix:
                ev["_servidor"] = nombre_server  # añadimos nombre del server
                todos_eventos.append(ev)

    print(" ¡Listo!")
    return sorted(todos_eventos, key=lambda x: x["unixtime"])

def imprimir_tabla(eventos):
    if not eventos:
        print("\nNo se encontraron eventos futuros.")
        return

    print(f"\n{'='*75}")
    print(f"{'FECHA':<14} {'HORA':<6} {'SERVIDOR':<22} {'RAID':<25} {'ANOTADOS'}")
    print(f"{'-'*75}")

    for ev in eventos:
        fecha = datetime.fromtimestamp(int(ev["unixtime"])).strftime('%d/%m/%Y')
        hora  = ev.get("time", "??:??")
        server = ev.get("_servidor", "?")[:21]
        titulo = ev.get("displayTitle", ev.get("title", "Sin título"))[:24]
        anotados = ev.get("signupcount", "?")

        print(f"{fecha:<14} {hora:<6} {server:<22} {titulo:<25} {anotados}")

    print(f"{'-'*75}")
    print(f"Total de raids próximas: {len(eventos)}")

if __name__ == "__main__":
    eventos_futuros = obtener_todos_los_datos()
    imprimir_tabla(eventos_futuros)