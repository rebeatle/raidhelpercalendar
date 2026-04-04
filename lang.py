import os

_LANG = "es"

STRINGS: dict[str, dict[str, object]] = {
    "es": {
        # General
        "continuar": "  Presiona Enter para continuar...",
        "menu_titulo": "Configuración",
        "opcion_invalida": "  ❌ Opción inválida.",

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
    R → Recargar eventos
    Q → Salir""",

        # Access Token
        "token_titulo": "  [1/2] ACCESS TOKEN de Raid Helper",
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
        "token_servidores_detectando": "\n  Obteniendo tus servidores...",
        "token_servidores_encontrados": "  ✅ {n} servidor(es) detectado(s):",
        "token_sin_servidores": "  ⚠ No se detectaron servidores con este token.",

        # User API Key
        "apikey_titulo": "  [2/2] USER API KEY de Raid Helper (opcional)",
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

        # Menú principal
        "menu_estado": "\n  Estado actual:",
        "menu_access_token": "Access Token  ",
        "menu_user_api_key": "User API Key  ",
        "menu_configurado": "✅ Configurado",
        "menu_no_configurado": "❌ No configurado",
        "menu_que_deseas": "\n  ¿Qué deseas hacer?",
        "menu_op1": "  [1] Configurar Access Token",
        "menu_op2": "  [2] Configurar User API Key",
        "menu_op3": "  [3] Lanzar la app",
        "menu_op4": "  [4] Cambiar idioma / Change language",
        "menu_op0": "  [0] Salir",
        "menu_elige": "  Elige una opción: ",
        "menu_falta_config": "\n  ❌ Debes configurar el Access Token primero.",

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
        "token_expirado_ui": "⚠ Token expirado — presiona C para actualizarlo",
        "token_expirado_msg": "⚠ Token expirado o inválido.\nPresiona C → opción 1 para actualizarlo.",
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
        "opcion_invalida": "  ❌ Invalid option.",

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
    R → Reload events
    Q → Exit""",

        # Access Token
        "token_titulo": "  [1/2] ACCESS TOKEN for Raid Helper",
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
        "token_servidores_detectando": "\n  Fetching your servers...",
        "token_servidores_encontrados": "  ✅ {n} server(s) detected:",
        "token_sin_servidores": "  ⚠ No servers detected with this token.",

        # User API Key
        "apikey_titulo": "  [2/2] USER API KEY for Raid Helper (optional)",
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

        # Main menu
        "menu_estado": "\n  Current status:",
        "menu_access_token": "Access Token  ",
        "menu_user_api_key": "User API Key  ",
        "menu_configurado": "✅ Configured",
        "menu_no_configurado": "❌ Not configured",
        "menu_que_deseas": "\n  What would you like to do?",
        "menu_op1": "  [1] Configure Access Token",
        "menu_op2": "  [2] Configure User API Key",
        "menu_op3": "  [3] Launch the app",
        "menu_op4": "  [4] Change language / Cambiar idioma",
        "menu_op0": "  [0] Exit",
        "menu_elige": "  Choose an option: ",
        "menu_falta_config": "\n  ❌ You must configure the Access Token first.",

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
        "token_expirado_ui": "⚠ Token expired — press C to update it",
        "token_expirado_msg": "⚠ Token expired or invalid.\nPress C → option 1 to update it.",
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
