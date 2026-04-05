# Versión en Español

> 🌐 [English version](README.md)

# ⚔ Raid Helper Viewer (RHV)

Un dashboard de escritorio para visualizar todos tus eventos de Raid Helper
en múltiples servidores de Discord desde una sola pantalla.

> Construido por [rebeatle](https://github.com/rebeatle) — porque saltar entre
> 14 canales de Discord para ver el calendario es un raid en sí mismo.

---

> ⚠️ **Aviso / Disclaimer**
>
> This is an unofficial, community-built tool. It is not affiliated with,
> endorsed by, or connected to Raid Helper or its developers in any way.
> It uses the same internal API that the raid-helper.xyz frontend uses,
> authenticated with your own personal session. If Raid Helper changes
> their API, this tool may stop working until updated.
>
> Use at your own risk. Your credentials are never stored on the server.

---

## ¿Qué es esto?

Si usas Raid Helper en varios servidores de Discord, sabes el dolor de tener
que revisar canal por canal para ver qué raids están programadas.

RHV resuelve eso: una sola pantalla con todos tus eventos futuros, filtros,
colores por proximidad de fecha, y la marca de en cuáles ya estás anotado.

![Vista principal](screenshots/main_view.png)
![launcher](screenshots/intro_2.png)

---

## Características

- 📅 **Vista unificada** de eventos de múltiples servidores
- 🔴🟡🟢 **Colores por proximidad** — hoy, mañana, esta semana
- ✅ **Marca tus eventos** — saber de un vistazo dónde ya estás anotado
- 🔍 **Filtros** por período, servidor, texto libre y fecha exacta
- 📋 **Detalle completo** de cada evento con signups por rol (Tanks, Healers, Melee, Ranged)
- ⚡ **Carga paralela** de todos los servidores simultáneamente
- 🔄 **Auto-recarga** cada 3 minutos (se pausa si estás viendo el detalle de un evento)
- 💬 **Estado visual** cuando no hay eventos para mostrar
- 🌐 **Español / Inglés** — idioma elegido al primer arranque, cambiable desde configuración
- ⌨️ **100% teclado y Mouse** — navegación rápida

---

## Requisitos

- Python 3.10+ → [descargar aquí](https://www.python.org/downloads/)
  - ⚠️ Al instalar en Windows, marca **"Add Python to PATH"**
- Cuenta de Discord con acceso a servidores que usen Raid Helper

---

## Instalación

1. Descarga el repositorio como ZIP y extráelo en tu escritorio
2. Abre la carpeta y ejecuta el launcher según tu sistema:
   - **Windows:** doble click en **`launcher.bat`**
   - **Linux / macOS:** ejecuta **`./launcher.sh`** desde la terminal
3. El launcher instala las dependencias automáticamente y te guía en la configuración

![launcher](screenshots/rhv_intro.png)

---

Si eres usuario avanzado, instala las dependencias manualmente:

```
pip install -r requirements.txt
```

---

## Configuración inicial

### 0. Selección de idioma
En el primer arranque se te pedirá elegir tu idioma antes que nada.

![Selección de idioma](screenshots/lang_selection.png)

Podés cambiarlo en cualquier momento desde el menú de configuración (`C` → opción 6).

### 1. Access Token
Este es el token de tu sesión en raid-helper.xyz. Para obtenerlo:

1. Ve a [raid-helper.xyz](https://raid-helper.xyz) e inicia sesión con Discord
2. Una vez dentro, ve al calendario de cualquier servidor
3. Presiona `F12` para abrir DevTools
4. Ve a la pestaña **Red** (Network) y filtra por **Fetch/XHR**
5. Recarga la página con `F5`
6. Busca una llamada llamada **`events/`** en la lista
7. Haz click y ve a la pestaña **Carga útil** (Payload)
8. Verás algo como:
```json
{"serverid":"...","accessToken":"TU_TOKEN_AQUÍ"}
```
![f12](screenshots/f12.png)
9. Copia solo el valor del `accessToken` (la cadena larga)

> ⚠️ Este token es personal — no lo compartas con nadie.
> Expira con el tiempo. Si la app deja de mostrar eventos, repite este proceso
> y actualiza tu `api.txt` con el nuevo token (opción `C` → Configuración).

### 2. User API Key *(opcional)*
Permite marcar con `READY` los eventos donde ya estás anotado.

1. En Discord, busca al bot **Raid-Helper** en cualquier servidor
2. Envíale un mensaje directo con el comando: `/usersettings apikey show`
3. Copia la key que te responde

Si no la configuras, la app funciona igual pero sin la marca de anotado.

> ℹ️ Si en el menú de configuración presionas Enter sin ingresar nada,
> tu key existente se conserva sin cambios.

### 3. IDs de servidores de Discord
Los servidores donde tienes Raid Helper activo.

**¿Cómo obtener el ID de un servidor?**
1. En Discord, activa el Modo desarrollador:
   `Ajustes → Avanzado → Modo desarrollador ✅`
2. Haz click derecho en el servidor
3. Selecciona **Copiar ID del servidor**

Puedes ingresarlos uno por uno o desde un archivo `.txt` con un ID por línea.

![dev mode](screenshots/dev_mode.png)
![Ids server](screenshots/id_server.png)

---

## Controles

| Tecla | Acción |
|-------|--------|
| `↑` `↓` | Navegar por los eventos |
| `Enter` | Ver detalle completo del evento |
| `R` | Recargar datos desde la API |
| `C` | Abrir menú de configuración |
| `V` | Agregar más servidores |
| `Esc` | Cerrar ventana de detalle |
| `Q` | Salir |

### Menú de configuración

![Menú de configuración](screenshots/settings_menu.png)

| Opción | Acción |
|--------|--------|
| `1` | Configurar Access Token |
| `2` | Configurar User API Key |
| `3` | Configurar Servidores de Discord |
| `4` | Agregar más Servidores |
| `5` | Lanzar la app |
| `6` | Cambiar idioma |
| `0` | Salir |

---

## Filtros

| Filtro | Descripción |
|--------|-------------|
| **Período** | Próximos 7, 14 o 30 días, o todos |
| **Servidor** | Filtra por nombre de servidor |
| **Buscar** | Texto libre en título, servidor o líder |
| **Fecha** | Fecha exacta en formato `dd/mm` o `dd/mm/aaaa` |

---

## Colores

| Color | Significado |
|-------|-------------|
| 🔴 Rojo | El evento es hoy |
| 🟡 Amarillo | El evento es mañana |
| 🟢 Verde | El evento es esta semana |
| ⚪ Blanco | El evento es más adelante |

---

## FAQ

**¿Por qué la app no muestra eventos?**
Lo más probable es que tu Access Token haya expirado. Ve a Configuración
(`C`) → opción 1, y sigue los pasos para obtener un nuevo token.

**¿Por qué no veo `READY` en mis eventos?**
Necesitas configurar la User API Key. Ve a Configuración (`C`) → opción 2.
Si ya la tenías configurada, puede que haya expirado — volvé a obtenerla
con `/usersettings apikey show` en Discord y actualizala desde el menú.

**¿Funciona en Mac o Linux?**
Sí. Ejecuta `./launcher.sh` desde la terminal. Asegurate de tener permisos
de ejecución: `chmod +x launcher.sh`.

**¿Es oficial? ¿Tiene permiso de Raid Helper?**
No es un producto oficial de Raid Helper. Usa la misma API que usa el
frontend de raid-helper.xyz con tu sesión personal. Cada usuario autentica
con sus propias credenciales. Si Raid Helper cambia su API, puede dejar
de funcionar hasta que se actualice el proyecto.

---

## Notas técnicas

RHV replica las llamadas que hace el frontend de raid-helper.xyz usando
el `accessToken` de sesión OAuth de Discord. No existe una API pública
documentada — fue descubierto observando el tráfico de red del sitio oficial.

La hora de los eventos se muestra en la **zona horaria local** del sistema
operativo donde corre la app.

---

## Roadmap

Funcionalidades planeadas para futuras versiones:

- 📤 **Exportar a ICS** — generar un archivo `.ics` del evento seleccionado
  para importarlo directamente a Google Calendar, Outlook o cualquier
  cliente de calendario.

- 🎯 **Filtro por rol** — ver en la lista qué eventos tienen cupo disponible
  para un rol específico (Tanks, Healers, Melee, Ranged), útil para decidir
  dónde anotarse.

- 🔃 **Ordenar columnas** — ordenar la tabla por servidor, cantidad de
  participantes u otros campos haciendo click en el encabezado de cada columna.

---

## Contribuciones

Pull requests bienvenidos. Si encontrás que algo se rompió por un cambio
en la API de Raid Helper, abrí un issue.

---

## Contacto

Para reportar bugs, sugerencias o uso comercial:
📧 rebeatle.dev@gmail.com

---

## Licencia

Este proyecto está bajo la licencia **GNU GPL v3**.

Podés usar, estudiar y modificar el código libremente, pero cualquier
versión modificada que distribuyas debe:
- Ser también de código abierto bajo GPL v3
- Dar crédito al autor original
- **No puede ser vendida ni usada con fines comerciales** sin permiso explícito del autor

© 2026 [rebeatle](https://github.com/rebeatle) — All rights reserved under GPL v3.

Para uso comercial o acuerdos especiales, contactá al autor directamente.
