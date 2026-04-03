import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import ACCESS_TOKEN, USER_API_KEY, MIS_SERVIDORES, ENDPOINT_EVENTS, ENDPOINT_AGENDA, ENDPOINT_DETALLE

MAX_WORKERS = 4


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


def obtener_todos_los_eventos() -> tuple[list, list]:
    """Consulta todos los servidores en paralelo y retorna (eventos, servidores_fallidos)."""
    ahora_unix      = int(time.time())
    mi_agenda       = obtener_ids_mi_agenda()
    todos           = []
    fallidos        = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futuros = {executor.submit(obtener_eventos_servidor, s_id): s_id
                   for s_id in MIS_SERVIDORES}
        for futuro in as_completed(futuros):
            s_id = futuros[futuro]
            nombre, eventos = futuro.result()
            if not eventos and nombre == s_id:
                fallidos.append(s_id)
            for ev in eventos:
                if int(ev.get("unixtime", 0)) > ahora_unix:
                    ev["_servidor"] = nombre
                    ev["_anotado"]  = str(ev.get("raidId", "")) in mi_agenda
                    todos.append(ev)

    return sorted(todos, key=lambda x: x["unixtime"]), fallidos


def obtener_ids_mi_agenda() -> set:
    """Retorna un set con los IDs de eventos donde ya estás anotado."""
    if not USER_API_KEY:
        return set()
    ahora_unix = int(time.time())
    try:
        url = ENDPOINT_AGENDA.format(api_key=USER_API_KEY)
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        datos = res.json()
        if isinstance(datos, list):
            return {
                str(e["id"])
                for e in datos
                if int(e.get("startTime", 0)) > ahora_unix
            }
        return set()
    except Exception:
        return set()
    
def obtener_detalle_evento(raid_id: str) -> dict:
    """Obtiene el detalle completo de un evento incluyendo signups."""
    try:
        res = requests.post(
            ENDPOINT_DETALLE.format(raid_id=raid_id),
            json={"accessToken": ACCESS_TOKEN},
            timeout=10
        )
        res.raise_for_status()
        return res.json()
    except Exception:
        return {}