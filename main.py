import requests

API_KEY = "TU_API_KEY"
SERVIDORES_GUILDS = ["ID_SERVER_1", "ID_SERVER_2", "ID_SERVER_3"]

def explorar_raids():
    headers = {"Authorization": API_KEY}
    
    print(f"{'FECHA':<20} | {'GUILD':<15} | {'EVENTO':<20} | {'CUPOS'}")
    print("-" * 70)

    for s_id in SERVIDORES_GUILDS:
        url = f"https://raid-helper.dev/api/v3/servers/{s_id}/events"
        res = requests.get(url, headers=headers)
        
        if res.status_code == 200:
            eventos = res.json()
            for ev in eventos:
                # Aquí puedes filtrar para que solo muestre las que no te has anotado
                print(f"{ev['startTimeReadable']:<20} | {ev['serverName']:<15} | {ev['title']:<20} | {ev['signups']}/{ev['capacity']}")

explorar_raids()