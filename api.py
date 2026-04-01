import requests
import time
from config import ACCESS_TOKEN, USER_API_KEY, MIS_SERVIDORES, ENDPOINT_EVENTS, ENDPOINT_AGENDA


def obtener_eventos_servidor(server_id: str) -> tuple[str, list]:
    """Obtiene todos los eventos de un servidor."""
    try:
        res = requests.post(
            ENDPOINT_EVENTS,
            json={"serverid": server_id, "accessToken": ACCESS_TOKEN},
            timeout=10
        )
        res.raise_for_status()
        datos = res.json()
        return datos.get("servername", server_id), datos.get("events", [])
    except Exception:
        return server_id, []


def obtener_todos_los_eventos() -> list:
    """Consulta todos los servidores y retorna eventos futuros ordenados por fecha."""
    ahora_unix = int(time.time())
    todos = []

    for s_id in MIS_SERVIDORES:
        nombre, eventos = obtener_eventos_servidor(s_id)
        for ev in eventos:
            if int(ev.get("unixtime", 0)) > ahora_unix:
                ev["_servidor"] = nombre
                todos.append(ev)

    return sorted(todos, key=lambda x: x["unixtime"])


def obtener_mi_agenda() -> list:
    """Obtiene los eventos donde el usuario ya está anotado."""
    if not USER_API_KEY:
        return []
    ahora_unix = int(time.time())
    try:
        url = ENDPOINT_AGENDA.format(api_key=USER_API_KEY)
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        datos = res.json()
        if isinstance(datos, list):
            return [e for e in datos if int(e.get("startTime", 0)) > ahora_unix]
        return []
    except Exception:
        return []
    
    
def obtener_detalle_evento(raid_id: str) -> dict:
    """Obtiene el detalle completo de un evento incluyendo signups."""
    try:
        res = requests.post(
            f"https://raid-helper.xyz/api/event/{raid_id}",
            json={"accessToken": ACCESS_TOKEN},
            timeout=10
        )
        res.raise_for_status()
        return res.json()
    except Exception:
        return {}