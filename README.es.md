# English  Version 

> 🌐 [Versión en ingles](README.md)


# ⚔ Raid Helper Viewer (RHV)


Un dashboard de escritorio para visualizar todos tus eventos de Raid Helper
en múltiples servidores de Discord desde una sola pantalla.

> Construido por [rebeatle](https://github.com/rebeatle) — porque saltar entre
> 14 canales de Discord para ver el calendario es un raid en sí mismo.

---

## ¿Qué es esto?

Si usas Raid Helper en varios servidores de Discord, sabes el dolor de tener
que revisar canal por canal para ver qué raids están programadas.

RHV resuelve eso: una sola pantalla con todos tus eventos futuros, filtros,
colores por proximidad de fecha, y la marca de en cuáles ya estás anotado.


![Vista principal](screenshots/main_view.png)
![launcher ](screenshots/intro_2.png)
---

## Características

- 📅 **Vista unificada** de eventos de múltiples servidores
- 🔴🟡🟢 **Colores por proximidad** — hoy, mañana, esta semana
- ✅ **Marca tus eventos** — saber de un vistazo dónde ya estás anotado
- 🔍 **Filtros** por período, servidor y texto libre
- 📋 **Detalle completo** de cada evento con signups por rol (Tanks, Healers, Melee, Ranged)
- ⌨️ **100% teclado y Mouse** — navegación rápida con teclado y Mouse

---

## Requisitos

- Windows 10 o superior
- Python 3.10+ → [descargar aquí](https://www.python.org/downloads/)
  - ⚠️ Al instalar, marca **"Add Python to PATH"**
- Cuenta de Discord con acceso a servidores que usen Raid Helper


---

## Instalación

1. Descarga el repositorio como ZIP y extráelo en tu escritorio
2. Abre la carpeta y haz doble click en **`launcher.bat`**
3. El launcher instala las dependencias automáticamente y te guía en la configuración

![launcher ](screenshots/rhv_intro.png)
---
Si eres usuario avanzado te recomiendo crear un .env e instalar estas dependencias.
    pip install -r requirements.txt

    textual>=0.8.0
    requests>=2.28.0

 Caso contrario solo descarga los archivos y ponlos en tu escritorio. No olvides instalar Python. El launcher hara todo de forma automatica.


---


## Configuración inicial

El launcher te pedirá 3 cosas la primera vez:

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
> y actualiza tu `api.txt` con el nuevo token (opción C → Configuración).

### 2. User API Key *(opcional)*
Permite marcar con ✅ los eventos donde ya estás anotado.

1. En Discord, busca al bot **Raid-Helper** en cualquier servidor
2. Envíale un mensaje directo con el comando: `/usersettings apikey show`
3. Copia la key que te responde

Si no la configuras, la app funciona igual pero sin la marca de anotado.

### 3. IDs de servidores de Discord
Los servidores donde tienes Raid Helper activo.

**¿Cómo obtener el ID de un servidor?**
1. En Discord, activa el Modo desarrollador:
   `Ajustes → Avanzado → Modo desarrollador ✅`
2. Haz click derecho en el servidor
3. Selecciona **Copiar ID del servidor**

Puedes ingresarlos uno por uno o desde un archivo `.txt` con un ID por línea.
![dev mode ](screenshots/dev_mode.png)
![Ids server ](screenshots/id_server.png)
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

**¿Por qué no veo el ✅ en mis eventos?**
Necesitas configurar la User API Key. Ve a Configuración (`C`) → opción 2.

**¿Funciona en Mac o Linux?**
El `launcher.bat` es exclusivo de Windows. En Mac/Linux puedes correr
`python app.py` directamente desde la terminal, pero el flujo de configuración
hay que hacerlo manual por ahora.

**¿Es oficial? ¿Tiene permiso de Raid Helper?**
No es un producto oficial de Raid Helper. Usa la misma API que usa el
frontend de raid-helper.xyz con tu sesión personal. Cada usuario autentica
con sus propias credenciales. Si Raid Helper cambia su API, puede dejar
de funcionar hasta que se actualice el proyecto.

---

## Notas técnicas

RHV replica las llamadas que hace el frontend de raid-helper.xyz usando
el `accessToken` de sesión OAuth de Discord. No existe una API pública
documentada para esto — fue descubierto observando el tráfico de red del
sitio web oficial.

---

## Contribuciones

Pull requests bienvenidos. Si encuentras que algo se rompió por un cambio
en la API de Raid Helper, abre un issue.

---


## Licencia

Este proyecto está bajo la licencia **GNU GPL v3**.

Puedes usar, estudiar y modificar el código libremente, pero cualquier
versión modificada que distribuyas debe:
- Ser también de código abierto bajo GPL v3
- Dar crédito al autor original
- **No puede ser vendida ni usada con fines comerciales** sin permiso explícito del autor

© 2026 [rebeatle](https://github.com/rebeatle) — All rights reserved under GPL v3.

Para uso comercial o acuerdos especiales, contacta al autor directamente.