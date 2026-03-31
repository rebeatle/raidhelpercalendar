import requests
from datetime import datetime


API_KEY = "HeRPxNmAjLLj9SutMpSpoqx21RVBLZPbmRJ4K8Ic"
URL_USER = f"https://raid-helper.xyz/api/v4/users/{API_KEY}/events"
def ver_mi_agenda():
    try:
        response = requests.get(URL_USER)
        raids = response.json()
        
        # Ordenar por fecha (startTime es unix timestamp)
        raids_ordenadas = sorted(raids, key=lambda x: x['startTime'])
        
        print(f"{'FECHA Y HORA':<18} | {'RAID / EVENTO':<25} | {'LIDER'}")
        print("-" * 65)
        
        for r in raids_ordenadas:
            # Convertir timestamp a algo legible (renderizamos 24h)
            fecha = datetime.fromtimestamp(r['startTime']).strftime('%d/%m %H:%M')
            
            print(f"{fecha:<18} | {r['title'][:25]:<25} | {r['leaderName']}")
            
    except Exception as e:
        print(f"Error al procesar los datos: {e}")

ver_mi_agenda()

"""https://raid-helper.dev/api/v3/servers/1374406840179232838/events
https://raid-helper.xyz/api/v4/servers/SERVERID/events

curl --request GET   --url https://raid-helper.xyz/api/v4/servers/SERVERID/events   --header 'Authorization: enter your token here'"""