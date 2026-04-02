import os
import sys
import time
import requests

ARCHIVOS_REQUERIDOS = ["api.txt", "api_key.txt", "servers.txt"]

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\n  Presiona Enter para continuar...")

def encabezado():
    print("=" * 60)
    print("   ⚔  RaidHelper Dashboard — Configuración")
    print("=" * 60)

def verificar_archivos() -> bool:
    """Retorna True si todos los archivos de configuración existen."""
    return all(os.path.exists(f) for f in ARCHIVOS_REQUERIDOS)

def configurar_access_token():
    limpiar()
    encabezado()
    print("""
  [1/3] ACCESS TOKEN de Raid Helper
  
  Este token es tu sesión personal en raid-helper.xyz.
  Sigue estos pasos para obtenerlo:
  
  1. Abre tu navegador y ve a:
     https://raid-helper.xyz
     
  2. Inicia sesión con tu cuenta de Discord
     (te redirigirá al Discord para confirmar)
     
  3. Una vez dentro, Ve al menu "dasboard" y luego elije cualquier
    servidor que aparesca en la lista. 
    Dentro del servidor elije la opcion " calendario " o "calendar " en ingles,
    una ves dentro veras un menu parecido a un calendario.
    Presiona F12 para abrir DevTools
  
  4. Ve a la pestaña "Red" (o "Network") 
    -opcional (elije el filtro FETCH/XHR ) 
  
  5. Recarga la página con F5
  
  6. Busca una llamada llamada "events/" en la lista
  
  7. Haz click en ella y ve a la pestaña "Carga útil"
     (o "Payload")
     
  8. Verás algo como:
     {"serverid":"...","accessToken":"TU_TOKEN_AQUÍ"}
     
  9. Copia solo el valor del accessToken, sin comillas (la cadena larga) 
""")
    token = input("  Pega tu accessToken aquí: ").strip()
    if not token:
        print("  ❌ Token vacío, intenta de nuevo.")
        pausar()
        return False

    # Verificar que el token funciona
    print("\n  Verificando token...")
    try:
        res = requests.post(
            "https://raid-helper.xyz/api/events/",
            json={"serverid": "1", "accessToken": token},
            timeout=10
        )
        if res.status_code in [200, 403, 404]:
            with open('api.txt', 'w', encoding='utf-8') as f:
                f.write(token)
            print("  ✅ Token guardado correctamente.")
            pausar()
            return True
        else:
            print(f"  ❌ El token parece inválido (código {res.status_code}).")
            pausar()
            return False
    except Exception:
        print("  ❌ No se pudo conectar a Raid Helper. Verifica tu internet.")
        pausar()
        return False

def configurar_user_api_key():
    limpiar()
    encabezado()
    print("""
  [2/3] USER API KEY de Raid Helper (opcional)
  
  Esta key te permite marcar los eventos donde ya
  estás anotado con un "READY" en la lista.
  
  Para obtenerla:
  
    1. Ve a Discord y encuentra al bot "Raid Helper" en cualquiera de tus servidores
    2. Dale click y selecciona "mensaje directo". 
    3. Ahi escribe el comando: /usersettings apikey show 
    4. El bot te responderá con tu User API Key, que es una cadena larga de letras y números.
    5. Copia esa cadena y pégala a continuación.
  
  Si no tienes o no quieres usarla, simplemente
  presiona Enter para saltar este paso.
""")
    key = input("  Pega tu User API Key (o Enter para saltar): ").strip()
    with open('api_key.txt', 'w', encoding='utf-8') as f:
        f.write(key)
    if key:
        print("  ✅ API Key guardada correctamente.")
    else:
        print("  ⏭  Saltado. Puedes configurarlo después con la tecla C en la app.")
    pausar()
    return True

def configurar_servidores():
    limpiar()
    encabezado()
    print("""
  [3/3] IDs DE SERVIDORES DE DISCORD
  
  Necesitas los IDs de los servidores donde tienes
  Raid Helper activo.
  
  ¿Cómo obtener un ID de servidor?
  1. En Discord, activa el "Modo desarrollador":
     Ajustes → Avanzado → Modo desarrollador ✅
     (Aveces demora un poco, se recomienda cerrar y abrir discord después de activar el modo desarrollador)
  2. Haz click derecho en el servidor
  3. Selecciona "Copiar ID del servidor"
""")
    print("  ¿Cómo quieres ingresar los IDs?")
    print("  [1] Uno por uno")
    print("  [2] Desde un archivo .txt (un ID por línea)")
    print()
    opcion = input("  Elige una opción (1 o 2): ").strip()

    ids = []

    if opcion == "1":
        ids = ingresar_ids_manual()
    elif opcion == "2":
        ids = ingresar_ids_desde_archivo()
    else:
        print("  ❌ Opción inválida.")
        pausar()
        return False

    if not ids:
        print("  ❌ No se ingresó ningún ID válido.")
        pausar()
        return False

    guardar_servidores(ids)
    print(f"\n  ✅ {len(ids)} servidor(es) guardado(s).")
    pausar()
    return True

def ingresar_ids_manual() -> list:
    ids = []
    print("\n  Ingresa los IDs uno por uno.")
    print("  (Deja vacío y presiona Enter cuando termines)\n")
    while True:
        id_srv = input(f"  Servidor #{len(ids)+1} (o Enter para terminar): ").strip()
        if not id_srv:
            break
        if id_srv.isdigit():
            ids.append(id_srv)
            print(f"  ✅ ID {id_srv} agregado.")
        else:
            print("  ❌ ID inválido, debe ser solo números.")
    return ids

def ingresar_ids_desde_archivo() -> list:
    print()
    ruta = input("  Ruta del archivo .txt: ").strip().strip('"')
    if not os.path.exists(ruta):
        print(f"  ❌ No se encontró el archivo: {ruta}")
        return []
    ids = []
    with open(ruta, 'r', encoding='utf-8') as f:
        for linea in f:
            id_srv = linea.strip()
            if id_srv.isdigit():
                ids.append(id_srv)
    if ids:
        print(f"  ✅ Se encontraron {len(ids)} IDs válidos.")
    else:
        print("  ❌ No se encontraron IDs válidos en el archivo.")
    return ids

def guardar_servidores(ids: list):
    with open('servers.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(ids))

def agregar_servidores():
    """Agrega más servidores a la lista existente."""
    limpiar()
    encabezado()

    ids_actuales = []
    if os.path.exists('servers.txt'):
        with open('servers.txt', 'r', encoding='utf-8') as f:
            ids_actuales = [l.strip() for l in f if l.strip().isdigit()]

    print(f"\n  Servidores actuales: {len(ids_actuales)}")
    for i, sid in enumerate(ids_actuales, 1):
        print(f"    {i}. {sid}")

    print("\n  ¿Cómo quieres agregar más IDs?")
    print("  [1] Uno por uno")
    print("  [2] Desde un archivo .txt")
    print()
    opcion = input("  Elige una opción (1 o 2): ").strip()

    nuevos = []
    if opcion == "1":
        nuevos = ingresar_ids_manual()
    elif opcion == "2":
        nuevos = ingresar_ids_desde_archivo()

    # Evitar duplicados
    ids_finales = list(dict.fromkeys(ids_actuales + nuevos))
    agregados   = len(ids_finales) - len(ids_actuales)

    if agregados > 0:
        guardar_servidores(ids_finales)
        print(f"\n  ✅ {agregados} servidor(es) nuevo(s) agregado(s).")
        print(f"  Total ahora: {len(ids_finales)} servidores.")
    else:
        print("\n  ⏭  No se agregaron servidores nuevos.")
    pausar()

def menu_configuracion():
    """Menú principal de configuración."""
    while True:
        limpiar()
        encabezado()

        falta_api    = not os.path.exists('api.txt')
        falta_key    = not os.path.exists('api_key.txt')
        falta_srv    = not os.path.exists('servers.txt')

        estado_api = "❌ No configurado" if falta_api  else "✅ Configurado"
        estado_key = "❌ No configurado" if falta_key  else "✅ Configurado"
        estado_srv = "❌ No configurado" if falta_srv  else "✅ Configurado"

        print(f"""
  Estado actual:
    Access Token  : {estado_api}
    User API Key  : {estado_key}
    Servidores    : {estado_srv}

  ¿Qué deseas hacer?
  [1] Configurar Access Token
  [2] Configurar User API Key
  [3] Configurar Servidores de Discord
  [4] Agregar más Servidores
  [5] Lanzar la app
  [0] Salir
""")
        opcion = input("  Elige una opción: ").strip()

        if opcion == "1":
            configurar_access_token()
        elif opcion == "2":
            configurar_user_api_key()
        elif opcion == "3":
            configurar_servidores()
        elif opcion == "4":
            agregar_servidores()
        elif opcion == "5":
            if falta_api or falta_srv:
                print("\n  ❌ Debes configurar el Access Token y los Servidores primero.")
                pausar()
            else:
                return True  # señal para lanzar app
        elif opcion == "0":
            sys.exit(0)

def primer_arranque():
    """Flujo guiado para la primera vez."""
    limpiar()
    encabezado()
    print("""
  ¡Bienvenido a RaidHelper Dashboard!
  
  Es la primera vez que ejecutas la app.
  Vamos a configurar todo en 3 pasos rápidos.
""")
    pausar()

    configurar_access_token()
    configurar_user_api_key()
    configurar_servidores()

    limpiar()
    encabezado()
    print("""
  ✅ ¡Configuración completada!
  
  La app se abrirá ahora.
  
  Recuerda:
    C → Menú de configuración
    V → Agregar más servidores
    R → Recargar eventos
    Q → Salir
""")
    pausar()


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "auto"

    if modo == "menu":
        menu_configuracion()
    elif modo == "agregar":
        agregar_servidores()
    elif modo == "auto":
        if not verificar_archivos():
            primer_arranque()
        else:
            menu_configuracion()