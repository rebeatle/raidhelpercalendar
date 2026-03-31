import requests
from datetime import datetime
import time

# --- CONFIGURACIÓN ---
API_KEY = "HeRPxNmAjLLj9SutMpSpoqx21RVBLZPbmRJ4K8Ic"
# Lista de IDs de tus servidores (Click derecho en el icono del servidor en Discord -> Copiar ID)
MIS_SERVIDORES = ["1374406840179232838", "833645497473433610","1184252455580610570"] 

# Endpoints v4
URL_USER = f"https://raid-helper.xyz/api/v4/users/{API_KEY}/events"
URL_SERVER_BASE = "https://raid-helper.xyz/api/v4/servers/{}/events"

def obtener_datos():
    ahora_unix = int(time.time())
    
    # 1. Obtener mis inscripciones (Agenda)
    try:
        res_user = requests.get(URL_USER)
        agenda_total = res_user.json()
    except:
        agenda_total = []

    # Filtrar solo eventos futuros para mi agenda
    mi_agenda = [e for e in agenda_total if e['startTime'] > ahora_unix]
    ids_mi_agenda = {e['id'] for e in mi_agenda}

    # 2. Explorar servidores para ver qué hay disponible
    raids_disponibles = []
    
    for s_id in MIS_SERVIDORES:
        try:
            res_server = requests.get(URL_SERVER_BASE.format(s_id))
            eventos_server = res_server.json()
            print(eventos_server)
            
            for ev in eventos_server:
                # Filtros: Que sea futura Y que yo NO esté anotado
                if ev['startTime'] > ahora_unix and ev['id'] not in ids_mi_agenda:
                    raids_disponibles.append(ev)
        except:
            print(f"Error al consultar el servidor {s_id}")

    return sorted(mi_agenda, key=lambda x: x['startTime']), sorted(raids_disponibles, key=lambda x: x['startTime'])

def imprimir_tabla():
    mi_agenda, disponibles = obtener_datos()

    print("\n" + "="*30 + " MI AGENDA (YA ANOTADO) " + "="*30)
    print(f"{'FECHA':<15} | {'EVENTO':<25} | {'LIDER':<15}")
    print("-" * 75)
    for r in mi_agenda:
        fecha = datetime.fromtimestamp(r['startTime']).strftime('%d/%m %H:%M')
        print(f"{fecha:<15} | {r['title'][:25]:<25} | {r['leaderName'][:15]}")

    print("\n" + "="*30 + " RAIDS DISPONIBLES " + "="*35)
    print(f"{'FECHA':<15} | {'EVENTO':<25} | {'SERVIDOR':<15}")
    print("-" * 75)
    if not disponibles:
        print("No hay eventos nuevos descubiertos en tus servidores.")
    for r in disponibles:
        fecha = datetime.fromtimestamp(r['startTime']).strftime('%d/%m %H:%M')
        # Nota: El JSON de server suele incluir el nombre del servidor
        print(f"{fecha:<15} | {r['title'][:25]:<25} | {r.get('serverName', 'Desconocido')[:15]}")

if __name__ == "__main__":
    imprimir_tabla()