import requests
from datetime import datetime
import time
# Agregando a gitignore
# --- CONFIGURACIÓN ---
# Abre el archivo y guarda el contenido en la variable 'contenido'
with open('api_key.txt', 'r', encoding='utf-8') as archivo:
    API_KEY = archivo.read()
MIS_SERVIDORES = ["1184252455580610570"]  

def consultar_servidor(s_id):
    """Prueba la conexión con el servidor usando el protocolo estricto."""
    # Intentamos con el subdominio .dev que es el más actualizado para la v4
    url = f"https://raid-helper.dev/api/v4/servers/{s_id}/events"
    
    # Formato de header que exige la v4 para tokens de usuario/bot
    headers = {
        "Authorization": f"{API_KEY}", # Prueba 1: Solo el token
        "Content-Type": "application/json"
    }
    
    try:
        res = requests.get(url, headers=headers)
        
        # Si falla por token, intentamos el formato alternativo de prefijo
        if res.status_code == 401 or (res.json().get('status') == 'failed'):
            headers["Authorization"] = f"Apikey {API_KEY}" # Prueba 2: Con prefijo
            res = requests.get(url, headers=headers)
            
        return res.json()
    except Exception as e:
        return {"status": "failed", "reason": str(e)}

def obtener_datos():
    ahora_unix = int(time.time())
    
    # 1. Agenda Personal (v4 User)
    # Este endpoint es más flexible, lo mantenemos como te funcionó antes
    url_user = f"https://raid-helper.xyz/api/v4/users/{API_KEY}/events"
    try:
        res_user = requests.get(url_user)
        agenda_total = res_user.json()
        #print(agenda_total)
    except:
        agenda_total = []

    mi_agenda = [e for e in agenda_total if int(e.get('startTime', 0)) > ahora_unix]
    ids_mi_agenda = {e['id'] for e in mi_agenda}

    # 2. Explorador de Servidores
    raids_disponibles = []
    for s_id in MIS_SERVIDORES:
        datos_server = consultar_servidor(s_id)
        
        
        if isinstance(datos_server, list):
            for ev in datos_server:
                if int(ev.get('startTime', 0)) > ahora_unix and ev['id'] not in ids_mi_agenda:
                    # Añadimos el nombre del servidor si no viene en el JSON
                    ev['server_id_ref'] = s_id 
                    raids_disponibles.append(ev)
        else:
            print(f"DEBUG: Error en servidor {s_id}: {datos_server}")

    return sorted(mi_agenda, key=lambda x: x['startTime']), sorted(raids_disponibles, key=lambda x: x['startTime'])

def imprimir_tabla():
    mi_agenda, disponibles = obtener_datos()
    print(mi_agenda)

    print(f"\n{'='*20} MI AGENDA EN LIMA {'='*20}")
    print(f"{'FECHA':<15} | {'RAID':<25} | {'LIDER':<15} | {'PLAYER':<15} | {'SPEC':<10} | {'CLASS'}")
    print("-" * 120)
    for r in mi_agenda:
        fecha = datetime.fromtimestamp(int(r['startTime'])).strftime('%d/%m %H:%M')
        raid_title = r['title'][:25]
        leader_name = r['leaderName'][:15]
        
        # Iterar sobre los signups
        if 'signUps' in r and r['signUps']:
            for signup in r['signUps']:
                player_name = signup['name'][:15]
                spec_name = signup['specName'][:10]
                player_class = signup['className']
                print(f"{fecha:<15} | {raid_title:<25} | {leader_name:<15} | {player_name:<15} | {spec_name:<10} | {player_class}")
        else:
            print(f"{fecha:<15} | {raid_title:<25} | {leader_name:<15} | {'N/A':<15} | {'N/A':<10} | N/A")

    print(f"\n{'='*20} DISPONIBLES PARA UNIRSE {'='*20}")
    print(f"{'FECHA':<15} | {'RAID':<25} | {'ID EVENTO'}")
    print("-" * 65)
    if not disponibles:
        print("No se encontraron raids nuevas.")
    for r in disponibles:
        fecha = datetime.fromtimestamp(int(r['startTime'])).strftime('%d/%m %H:%M')
        print(f"{fecha:<15} | {r['title'][:25]:<25} | {r['id']}")

if __name__ == "__main__":
    imprimir_tabla()