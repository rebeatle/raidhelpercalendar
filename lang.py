import os

_LANG = "es"

STRINGS: dict[str, dict[str, object]] = {
    "es": {
        # General
        "continuar": "  Presiona Enter para continuar...",
        "menu_titulo": "Configuración",
        "elige_opcion_12": "  Elige una opción (1 o 2): ",
        "opcion_invalida": "  ❌ Opción inválida.",
        "enter_salir": "  Presiona ENTER 2 veces para salir",

        # Cambio de idioma
        "idioma_actual": "Idioma actual / Current language",
        "idioma_es": "Español",
        "idioma_en": "English",
        "idioma_cambiado_es": "  ✅ Idioma cambiado a Español.",
        "idioma_cambiado_en": "  ✅ Language changed to English.",
        "idioma_sin_cambios": "  ⏭  Sin cambios. / No changes.",

        # Primer arranque
        "bienvenido": "  ¡Bienvenido a RaidHelper Viewer!",
        "config_falta": "  Vamos a configurar lo que falta.",
        "todo_configurado": "  ✅ ¡Todo configurado!",
        "app_abre": "  La app se abrirá ahora.",
        "recuerda": "  Recuerda:",
        "atajos": """\
    C → Menú de configuración
    V → Agregar más servidores
    R → Recargar eventos
    Q → Salir""",

        # Access Token
        "token_titulo": "  [1/3] ACCESS TOKEN de Raid Helper",
        "token_instrucciones": """
  Este token es tu sesión personal en raid-helper.xyz.
  Sigue estos pasos para obtenerlo:

  1. Abre tu navegador y ve a:
     https://raid-helper.xyz

  2. Inicia sesión con tu cuenta de Discord
     (te redirigirá a Discord para confirmar)

  3. Una vez dentro, ve al menú "dashboard" y elige cualquier
     servidor de la lista. Dentro del servidor elige "calendario"
     o "calendar" en inglés. Verás un menú parecido a un calendario.
     Presiona F12 para abrir DevTools.

  4. Ve a la pestaña "Red" (o "Network")
     -opcional: elige el filtro FETCH/XHR

  5. Recarga la página con F5

  6. Busca una llamada llamada "events/" en la lista

  7. Haz click en ella y ve a la pestaña "Carga útil" (o "Payload")

  8. Verás algo como:
     {"serverid":"...","accessToken":"TU_TOKEN_AQUÍ"}

  9. Copia solo el valor del accessToken, sin comillas (la cadena larga)
""",
        "token_pegar": "  Pega tu accessToken aquí: ",
        "token_vacio": "  ❌ Token vacío, intenta de nuevo.",
        "token_verificando": "\n  Verificando token...",
        "token_guardado": "  ✅ Token guardado correctamente.",
        "token_invalido": "  ❌ El token parece inválido (código {code}).",
        "token_sin_conexion": "  ❌ No se pudo conectar a Raid Helper. Verifica tu internet.",

        # User API Key
        "apikey_titulo": "  [2/3] USER API KEY de Raid Helper (opcional)",
        "apikey_instrucciones": """
  Esta key te permite marcar los eventos donde ya estás
  anotado con un "READY" en la lista.

  Para obtenerla:

    1. Ve a Discord y encuentra al bot "Raid Helper" en cualquiera
       de tus servidores.
    2. Haz click y selecciona "Mensaje directo".
    3. Escribe el comando: /usersettings apikey show
    4. El bot te responderá con tu User API Key: una cadena larga
       de letras y números.
    5. Copia esa cadena y pégala a continuación.

  Si no la tienes o no la quieres usar, presiona Enter para saltar.
""",
        "apikey_conservar": "Enter para conservar la actual",
        "apikey_saltar": "Enter para saltar",
        "apikey_pegar": "  Pega tu User API Key ({aviso}): ",
        "apikey_sin_cambios": "  ⏭  Sin cambios. Key anterior conservada.",
        "apikey_saltado": "  ⏭  Saltado.",
        "apikey_guardada": "  ✅ API Key guardada correctamente.",

        # Servidores
        "servers_titulo": "  [3/3] IDs DE SERVIDORES DE DISCORD",
        "servers_instrucciones": """
  Necesitas los IDs de los servidores donde tienes Raid Helper activo.

  ¿Cómo obtener un ID de servidor?
  1. En Discord, activa el "Modo desarrollador":
     Ajustes → Avanzado → Modo desarrollador ✅
     (A veces demora un poco; se recomienda cerrar y abrir Discord
     después de activarlo)
  2. Haz click derecho en el servidor
  3. Selecciona "Copiar ID del servidor"
""",
        "servers_como_ingresar": "  ¿Cómo quieres ingresar los IDs?",
        "servers_uno_por_uno": "  [1] Uno por uno",
        "servers_desde_archivo": "  [2] Desde un archivo .txt (un ID por línea)",
        "servers_sin_ids": "  ❌ No se ingresó ningún ID válido.",
        "servers_guardados": "  ✅ {n} servidor(es) guardado(s).",

        # Entrada manual
        "manual_ingresa": "\n  Ingresa los IDs uno por uno.",
        "manual_deja_vacio": "  (Deja vacío y presiona Enter cuando termines)\n",
        "manual_servidor_n": "  Servidor #{n} (o Enter para terminar): ",
        "manual_id_agregado": "  ✅ ID {id} agregado.",
        "manual_id_invalido": "  ❌ ID inválido, debe ser solo números.",

        # Desde archivo
        "archivo_ruta": "\n  Ruta del archivo .txt: ",
        "archivo_no_encontrado": "  ❌ No se encontró el archivo: {ruta}",
        "archivo_encontrados": "  ✅ Se encontraron {n} IDs válidos.",
        "archivo_sin_ids": "  ❌ No se encontraron IDs válidos en el archivo.",

        # Agregar servidores
        "agregar_actuales": "\n  Servidores actuales: {n}",
        "agregar_como": "\n  ¿Cómo quieres agregar más IDs?",
        "agregar_nuevos": "\n  ✅ {n} servidor(es) nuevo(s) agregado(s).",
        "agregar_total": "  Total ahora: {n} servidores.",
        "agregar_ninguno": "\n  ⏭  No se agregaron servidores nuevos.",

        # Menú principal
        "menu_estado": "\n  Estado actual:",
        "menu_access_token": "Access Token  ",
        "menu_user_api_key": "User API Key  ",
        "menu_servidores_lbl": "Servidores    ",
        "menu_configurado": "✅ Configurado",
        "menu_no_configurado": "❌ No configurado",
        "menu_que_deseas": "\n  ¿Qué deseas hacer?",
        "menu_op1": "  [1] Configurar Access Token",
        "menu_op2": "  [2] Configurar User API Key",
        "menu_op3": "  [3] Configurar Servidores de Discord",
        "menu_op4": "  [4] Agregar más Servidores",
        "menu_op5": "  [5] Lanzar la app",
        "menu_op6": "  [6] Cambiar idioma / Change language",
        "menu_op0": "  [0] Salir",
        "menu_elige": "  Elige una opción: ",
        "menu_falta_config": "\n  ❌ Debes configurar el Access Token y los Servidores primero.",

        # UI de la app
        "dias_7": "Próximos 7 días",
        "dias_14": "Próximos 14 días",
        "dias_30": "Próximos 30 días",
        "dias_todos": "Todos",
        "col_inscrito": "Inscrito",
        "col_fecha": "Fecha",
        "col_hora": "Hora",
        "col_servidor": "Servidor",
        "col_raid": "Raid",
        "col_participantes": "👥Participantes",
        "col_rol": "Rol",
        "label_periodo": " Período: ",
        "label_servidor": "Servidor: ",
        "label_buscar": "Buscar: ",
        "label_fecha": "Fecha: ",
        "placeholder_buscar": "título, servidor, líder...",
        "placeholder_fecha": "dd/mm  o  dd/mm/aaaa",
        "iniciando": "Iniciando...",
        "todos_servidores": "Todos los servidores",
        "consultando": "⏳ Consultando servidores...",
        "recargando": "⏳ Recargando...",
        "bind_salir": "Salir",
        "bind_recargar": "Recargar",
        "bind_config": "Configuración",
        "bind_agregar": "Agregar servidores",
        "bind_cerrar": "Cerrar",
        "sin_titulo": "Sin título",
        "sin_descripcion": "Sin descripción",
        "sin_anotados": "Sin anotados aún.",
        "esc_cerrar": "ESC para cerrar",
        "total_anotados": "Total anotados: {n}",
        "cargando_evento": "⏳ Cargando {titulo}...",
        "inscrito_como": " Inscrito como:",
        "sin_resp": " | ⚠ sin resp: {n}",
        "estado_eventos": "READY {n} evento(s){aviso}",
        "mensaje_vacio": "Elige un servidor para mostrar eventos",
        "det_servidor": "Servidor:",
        "det_fecha": "Fecha:",
        "det_lider": "Líder:",
        "det_canal": "Canal:",
        "det_raid_id": "Raid ID:",
        "det_descripcion": "Descripción:",
        "dias_semana": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
    },

    "en": {
        # General
        "continuar": "  Press Enter to continue...",
        "menu_titulo": "Configuration",
        "elige_opcion_12": "  Choose an option (1 or 2): ",
        "opcion_invalida": "  ❌ Invalid option.",
        "enter_salir": "  Press ENTER twice to exit",

        # Language change
        "idioma_actual": "Current language / Idioma actual",
        "idioma_es": "Español",
        "idioma_en": "English",
        "idioma_cambiado_es": "  ✅ Idioma cambiado a Español.",
        "idioma_cambiado_en": "  ✅ Language changed to English.",
        "idioma_sin_cambios": "  ⏭  No changes. / Sin cambios.",

        # First run
        "bienvenido": "  Welcome to RaidHelper Viewer!",
        "config_falta": "  Let's configure what's missing.",
        "todo_configurado": "  ✅ All set!",
        "app_abre": "  The app will open now.",
        "recuerda": "  Remember:",
        "atajos": """\
    C → Settings menu
    V → Add more servers
    R → Reload events
    Q → Exit""",

        # Access Token
        "token_titulo": "  [1/3] ACCESS TOKEN for Raid Helper",
        "token_instrucciones": """
  This token is your personal session on raid-helper.xyz.
  Follow these steps to obtain it:

  1. Open your browser and go to:
     https://raid-helper.xyz

  2. Log in with your Discord account
     (it will redirect you to Discord for confirmation)

  3. Once inside, go to the "dashboard" menu and choose any
     server from the list. Inside the server, choose "calendar".
     You will see a calendar-like menu.
     Press F12 to open DevTools.

  4. Go to the "Network" tab
     -optional: choose the FETCH/XHR filter

  5. Reload the page with F5

  6. Look for a call named "events/" in the list

  7. Click on it and go to the "Payload" tab

  8. You will see something like:
     {"serverid":"...","accessToken":"YOUR_TOKEN_HERE"}

  9. Copy only the accessToken value, without quotes (the long string)
""",
        "token_pegar": "  Paste your accessToken here: ",
        "token_vacio": "  ❌ Empty token, please try again.",
        "token_verificando": "\n  Verifying token...",
        "token_guardado": "  ✅ Token saved successfully.",
        "token_invalido": "  ❌ Token appears invalid (code {code}).",
        "token_sin_conexion": "  ❌ Could not connect to Raid Helper. Check your internet.",

        # User API Key
        "apikey_titulo": "  [2/3] USER API KEY for Raid Helper (optional)",
        "apikey_instrucciones": """
  This key allows you to mark events where you're already
  signed up with "READY" in the list.

  To obtain it:

    1. Go to Discord and find the "Raid Helper" bot in any of your servers.
    2. Click on it and select "Direct Message".
    3. Type the command: /usersettings apikey show
    4. The bot will reply with your User API Key: a long string
       of letters and numbers.
    5. Copy that string and paste it below.

  If you don't have it or don't want to use it, press Enter to skip.
""",
        "apikey_conservar": "Enter to keep current",
        "apikey_saltar": "Enter to skip",
        "apikey_pegar": "  Paste your User API Key ({aviso}): ",
        "apikey_sin_cambios": "  ⏭  No changes. Previous key kept.",
        "apikey_saltado": "  ⏭  Skipped.",
        "apikey_guardada": "  ✅ API Key saved successfully.",

        # Servers
        "servers_titulo": "  [3/3] DISCORD SERVER IDs",
        "servers_instrucciones": """
  You need the IDs of the servers where you have Raid Helper active.

  How to get a server ID?
  1. In Discord, enable "Developer Mode":
     Settings → Advanced → Developer Mode ✅
     (It may take a moment; recommended to close and reopen Discord
     after enabling it)
  2. Right-click the server
  3. Select "Copy Server ID"
""",
        "servers_como_ingresar": "  How would you like to enter the IDs?",
        "servers_uno_por_uno": "  [1] One by one",
        "servers_desde_archivo": "  [2] From a .txt file (one ID per line)",
        "servers_sin_ids": "  ❌ No valid ID was entered.",
        "servers_guardados": "  ✅ {n} server(s) saved.",

        # Manual entry
        "manual_ingresa": "\n  Enter IDs one by one.",
        "manual_deja_vacio": "  (Leave empty and press Enter when done)\n",
        "manual_servidor_n": "  Server #{n} (or Enter to finish): ",
        "manual_id_agregado": "  ✅ ID {id} added.",
        "manual_id_invalido": "  ❌ Invalid ID, must be numbers only.",

        # From file
        "archivo_ruta": "\n  Path to .txt file: ",
        "archivo_no_encontrado": "  ❌ File not found: {ruta}",
        "archivo_encontrados": "  ✅ Found {n} valid IDs.",
        "archivo_sin_ids": "  ❌ No valid IDs found in file.",

        # Add servers
        "agregar_actuales": "\n  Current servers: {n}",
        "agregar_como": "\n  How would you like to add more IDs?",
        "agregar_nuevos": "\n  ✅ {n} new server(s) added.",
        "agregar_total": "  Total now: {n} servers.",
        "agregar_ninguno": "\n  ⏭  No new servers were added.",

        # Main menu
        "menu_estado": "\n  Current status:",
        "menu_access_token": "Access Token  ",
        "menu_user_api_key": "User API Key  ",
        "menu_servidores_lbl": "Servers       ",
        "menu_configurado": "✅ Configured",
        "menu_no_configurado": "❌ Not configured",
        "menu_que_deseas": "\n  What would you like to do?",
        "menu_op1": "  [1] Configure Access Token",
        "menu_op2": "  [2] Configure User API Key",
        "menu_op3": "  [3] Configure Discord Servers",
        "menu_op4": "  [4] Add more Servers",
        "menu_op5": "  [5] Launch the app",
        "menu_op6": "  [6] Change language / Cambiar idioma",
        "menu_op0": "  [0] Exit",
        "menu_elige": "  Choose an option: ",
        "menu_falta_config": "\n  ❌ You must configure the Access Token and Servers first.",

        # App UI
        "dias_7": "Next 7 days",
        "dias_14": "Next 14 days",
        "dias_30": "Next 30 days",
        "dias_todos": "All",
        "col_inscrito": "Signed Up",
        "col_fecha": "Date",
        "col_hora": "Time",
        "col_servidor": "Server",
        "col_raid": "Raid",
        "col_participantes": "👥Participants",
        "col_rol": "Role",
        "label_periodo": " Period: ",
        "label_servidor": "Server: ",
        "label_buscar": "Search: ",
        "label_fecha": "Date: ",
        "placeholder_buscar": "title, server, leader...",
        "placeholder_fecha": "dd/mm  or  dd/mm/yyyy",
        "iniciando": "Starting...",
        "todos_servidores": "All servers",
        "consultando": "⏳ Querying servers...",
        "recargando": "⏳ Reloading...",
        "bind_salir": "Exit",
        "bind_recargar": "Reload",
        "bind_config": "Settings",
        "bind_agregar": "Add servers",
        "bind_cerrar": "Close",
        "sin_titulo": "No title",
        "sin_descripcion": "No description",
        "sin_anotados": "No sign-ups yet.",
        "esc_cerrar": "ESC to close",
        "total_anotados": "Total signed up: {n}",
        "cargando_evento": "⏳ Loading {titulo}...",
        "inscrito_como": " Signed up as:",
        "sin_resp": " | ⚠ no resp: {n}",
        "estado_eventos": "READY {n} event(s){aviso}",
        "mensaje_vacio": "Choose a server to show events",
        "det_servidor": "Server:",
        "det_fecha": "Date:",
        "det_lider": "Leader:",
        "det_canal": "Channel:",
        "det_raid_id": "Raid ID:",
        "det_descripcion": "Description:",
        "dias_semana": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
}


def set_lang(lang: str) -> None:
    global _LANG
    if lang in STRINGS:
        _LANG = lang


def get_lang() -> str:
    return _LANG


def t(key: str, **kwargs) -> str:
    s = STRINGS.get(_LANG, STRINGS["es"]).get(key, key)
    if not isinstance(s, str):
        return s  # type: ignore[return-value]
    return s.format(**kwargs) if kwargs else s


def tl(key: str) -> list:
    """Retorna un valor de lista (ej: dias_semana)."""
    val = STRINGS.get(_LANG, STRINGS["es"]).get(key, [])
    return val if isinstance(val, list) else []


def cargar_idioma() -> None:
    global _LANG
    if os.path.exists("lang.txt"):
        with open("lang.txt", "r", encoding="utf-8") as f:
            lang = f.read().strip()
        if lang in STRINGS:
            _LANG = lang


def guardar_idioma(lang: str) -> None:
    with open("lang.txt", "w", encoding="utf-8") as f:
        f.write(lang)
    set_lang(lang)
