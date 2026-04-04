from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Label, Select, LoadingIndicator, Static, Button, Input
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.binding import Binding
from textual import work, on
from rich.text import Text
from datetime import datetime, date

from api import obtener_todos_los_eventos
from filtros import filtrar_por_dias, filtrar_por_servidor, obtener_servidores_unicos, filtrar_por_texto, filtrar_por_fecha
import inscripciones
from inscripciones import ROLES


OPCIONES_DIAS = [
    ("Próximos 7 días",  "7"),
    ("Próximos 14 días", "14"),
    ("Próximos 30 días", "30"),
    ("Todos",            "0"),
]

class DetalleEventoModal(ModalScreen):
    """Modal con el detalle completo de un evento incluyendo signups."""

    BINDINGS = [("escape", "dismiss", "Cerrar")]

    def __init__(self, evento: dict):
        super().__init__()
        self.evento = evento
        self._filtro_texto = ""

    def on_mount(self) -> None:
        self.focus()
        # Cargamos el detalle completo en hilo separado
        self.cargar_detalle()

    @work(thread=True)
    def cargar_detalle(self) -> None:
        from api import obtener_detalle_evento
        raid_id = self.evento.get("raidId", "")
        if not raid_id:
            return
        detalle = obtener_detalle_evento(raid_id)
        self.app.call_from_thread(self._renderizar, detalle)

    def _renderizar(self, detalle: dict) -> None:
        fecha = datetime.fromtimestamp(
            int(detalle.get("unixtime", 0))
        ).strftime('%d/%m/%Y %H:%M')

        desc = detalle.get("description") or "Sin descripción"

        # --- Inscripción local ---
        raid_id = str(self.evento.get("raidId", ""))
        ins = inscripciones.obtener(raid_id)
        if ins:
            nombre_rol = ROLES.get(ins["rol"], ins["rol"])
            cabecera_ins = (
                f"[bold magenta]{'─'*55}[/bold magenta]\n"
                f"[bold magenta] Inscrito como:[/bold magenta]  "
                f"[white]{ins['nombre']}[/white]  ·  "
                f"[bold]{nombre_rol}[/bold]  ·  "
                f"[dim]{ins['clase']}[/dim]\n"
                f"[bold magenta]{'─'*55}[/bold magenta]\n\n"
            )
        else:
            cabecera_ins = ""

        # --- Cabecera del evento ---
        texto = cabecera_ins + (
            f"[bold cyan]{'='*55}[/bold cyan]\n"
            f"[bold white] {detalle.get('displayTitle', detalle.get('title', '?'))}[/bold white]\n"
            f"[bold cyan]{'='*55}[/bold cyan]\n\n"
            f"[bold]Servidor:[/bold]  {detalle.get('servername', '?')}\n"
            f"[bold]Fecha:[/bold]     {fecha}\n"
            f"[bold]Líder:[/bold]     {detalle.get('leadername', '?')}\n"
            f"[bold]Canal:[/bold]     #{detalle.get('channelName', '?')}\n"
            f"[bold]Raid ID:[/bold]   {detalle.get('raidid', '?')}\n\n"
            f"[bold]Descripción:[/bold]\n[dim]{desc}[/dim]\n\n"
        )

        # --- Signups agrupados por rol ---
        signups = detalle.get("signups", [])
        if signups:
            COLORES = {
                "Tanks":   "bold blue",
                "Healers": "bold green",
                "Melee":   "bold red",
                "Ranged":  "bold yellow",
            }

            grupos = {}
            for s in signups:
                if s.get("status") != "primary":
                    continue
                rol = s.get("role", "Otros")
                grupos.setdefault(rol, []).append(s)

            for rol in ["Tanks", "Healers", "Melee", "Ranged"]:
                if rol not in grupos:
                    continue
                color = COLORES.get(rol, "white")
                miembros = sorted(grupos[rol], key=lambda x: x.get("position", 99))
                texto += f"[{color}]── {rol} ({len(miembros)}) ──[/{color}]\n"
                for m in miembros:
                    nombre = m.get("name", "?")
                    clase  = m.get("class", "")
                    spec   = m.get("spec", "")
                    nota   = f"  [dim]({m['note']})[/dim]" if m.get("note") else ""
                    texto += f"  {m.get('position','?'):>2}. [white]{nombre}[/white]  [dim]{clase} / {spec}[/dim]{nota}\n"
                texto += "\n"

            # Bench / Tentative / Ausentes si hay
            for estado in ["Bench", "Tentative", "Late", "Absence"]:
                extras = [s for s in signups if s.get("status") == "default"
                          and s.get("class", "").lower() == estado.lower()]
                if extras:
                    texto += f"[dim]── {estado} ({len(extras)}) ──[/dim]\n"
                    for m in extras:
                        texto += f"  [dim]{m.get('name', '?')}[/dim]\n"
                    texto += "\n"

            total = len([s for s in signups if s.get("status") == "primary"])
            texto += f"[bold cyan]Total anotados: {total}[/bold cyan]\n\n"
        else:
            texto += "[dim]Sin anotados aún.[/dim]\n\n"

        texto += "[dim]ESC para cerrar[/dim]"

        try:
            self.query_one("#cargando", Static).update(texto)
        except Exception:
            pass

        
    def compose(self) -> ComposeResult:
        titulo = self.evento.get("displayTitle", self.evento.get("title", "Evento"))
        yield Container(
            Static(f"⏳ Cargando {titulo}...", id="cargando", markup=True),
            id="modal-cuerpo"
        )

    
    
    DEFAULT_CSS = """
    DetalleEventoModal {
        align: center middle;
    }
    #modal-cuerpo {
        width: 75%;
        max-height: 85%;
        background: $surface;
        border: thick $primary;
        padding: 2 4;
        overflow-y: auto;
    }
    """


OPCIONES_ROL = [
    ("Tank  (T)", "T"),
    ("Healer (H)", "H"),
    ("DPS   (D)", "D"),
]


class InscribirseModal(ModalScreen):
    """Modal para registrar nombre, clase y rol en un evento."""

    BINDINGS = [("escape", "dismiss", "Cancelar")]

    DEFAULT_CSS = """
    InscribirseModal {
        align: center middle;
    }
    #modal-inscripcion {
        width: 60;
        height: auto;
        background: $surface;
        border: thick $accent;
        padding: 2 4;
    }
    #titulo-inscripcion {
        text-align: center;
        color: $accent;
        margin-bottom: 1;
    }
    #fila-nombre, #fila-clase, #fila-rol {
        height: 3;
        margin-bottom: 1;
    }
    #fila-nombre Label, #fila-clase Label, #fila-rol Label {
        width: 10;
        content-align: right middle;
        padding-right: 1;
    }
    #botones-inscripcion {
        height: 3;
        align: center middle;
        margin-top: 1;
    }
    #botones-inscripcion Button {
        margin: 0 1;
    }
    """

    def __init__(self, evento: dict, inscripcion_actual: dict | None = None):
        super().__init__()
        self.evento = evento
        self.inscripcion_actual = inscripcion_actual or {}

    def compose(self) -> ComposeResult:
        titulo = self.evento.get("displayTitle", self.evento.get("title", "Evento"))
        nombre_prev = self.inscripcion_actual.get("nombre", "")
        clase_prev  = self.inscripcion_actual.get("clase", "")
        rol_prev    = self.inscripcion_actual.get("rol", Select.BLANK)

        with Container(id="modal-inscripcion"):
            yield Static(f"Inscribirse: {titulo}", id="titulo-inscripcion", markup=False)
            with Horizontal(id="fila-nombre"):
                yield Label("Nombre:")
                yield Input(value=nombre_prev, placeholder="Tu nombre en el raid", id="inp-nombre")
            with Horizontal(id="fila-clase"):
                yield Label("Clase:")
                yield Input(value=clase_prev, placeholder="Ej: Paladin, Druid...", id="inp-clase")
            with Horizontal(id="fila-rol"):
                yield Label("Rol:")
                yield Select(options=OPCIONES_ROL, value=rol_prev, id="sel-rol")
            with Horizontal(id="botones-inscripcion"):
                yield Button("Guardar", variant="primary", id="btn-guardar")
                yield Button("Cancelar", id="btn-cancelar")

    def on_mount(self) -> None:
        self.query_one("#inp-nombre", Input).focus()

    @on(Button.Pressed, "#btn-guardar")
    def guardar(self) -> None:
        nombre = self.query_one("#inp-nombre", Input).value.strip()
        clase  = self.query_one("#inp-clase",  Input).value.strip()
        rol    = self.query_one("#sel-rol",    Select).value
        if nombre and clase and rol and rol is not Select.BLANK:
            self.dismiss({"nombre": nombre, "clase": clase, "rol": str(rol)})

    @on(Button.Pressed, "#btn-cancelar")
    def cancelar(self) -> None:
        self.dismiss(None)


class RaidHelperApp(App):

    TITLE    = "⚔ RaidHelper Viewer"
    SUB_TITLE = "Made by https://github.com/rebeatle"

    BINDINGS = [
    Binding("q", "quit",            "Salir"),
    Binding("r", "recargar",        "Recargar"),
    Binding("i", "inscribirse",     "Inscribirse"),
    Binding("c", "abrir_config",    "Configuración"),
    Binding("v", "agregar_servers", "Agregar servidores"),
]

    DEFAULT_CSS = """
    #barra-filtros {
        height: 3;
        padding: 0 1;
        background: $panel;
        border-bottom: solid $primary;
    }
    #estado {
        width: 1fr;
        content-align: right middle;
        color: $text-muted;
        padding-right: 1;
    }
    Select {
        width: 28;
        margin: 0 1;
    }
    #contenedor-tabla {
        height: 1fr;
    }
    DataTable {
        height: 1fr;
    }
    #mensaje-vacio {
        width: 1fr;
        height: 1fr;
        content-align: center middle;
        color: $text-muted;
    }
    #inp-buscar {
        width: 25;
        margin: 0 1;
    }
    #inp-fecha {
        width: 18;
        margin: 0 1;
    }
    """

    def __init__(self):
        super().__init__()
        self._todos_eventos        = []
        self._eventos_filtrados    = []
        self._filtro_dias          = "7"
        self._filtro_texto         = ""
        self._filtro_servidor      = ""
        self._filtro_fecha         = ""
        self._fallidos             = []
        
    @on(Input.Changed, "#inp-buscar")
    def cambio_busqueda(self, event: Input.Changed) -> None:
        self._filtro_texto = event.value
        self._aplicar_filtros()

    @on(Input.Changed, "#inp-fecha")
    def cambio_fecha(self, event: Input.Changed) -> None:
        self._filtro_fecha = event.value
        self._aplicar_filtros()
        
        
    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="barra-filtros"):
            yield Label(" Período: ")
            yield Select(options=OPCIONES_DIAS, value="7", id="sel-dias")
            yield Label("Servidor: ")
            yield Select(options=[("Todos", "")], value="", id="sel-servidor")
            yield Label("Buscar: ")
            yield Input(placeholder="título, servidor, líder...", id="inp-buscar")
            yield Label("Fecha: ")
            yield Input(placeholder="dd/mm  o  dd/mm/aaaa", id="inp-fecha")
            yield Static("Iniciando...", id="estado")

        with Container(id="contenedor-tabla"):
            yield LoadingIndicator()
            yield Static("", id="mensaje-vacio")

        yield Footer()

    def on_mount(self) -> None:
        self.cargar_datos()
        self.set_interval(180, self._auto_recargar)

    def _auto_recargar(self) -> None:
        """Recarga automática cada 3 min, pausada si hay un modal abierto."""
        if isinstance(self.screen, DetalleEventoModal):
            return
        self.cargar_datos()

    @work(thread=True)
    def cargar_datos(self) -> None:
        """Carga datos de todos los servidores en hilo separado."""
        self.call_from_thread(self._set_estado, "⏳ Consultando servidores...")
        eventos, fallidos = obtener_todos_los_eventos()
        self._todos_eventos = eventos
        self._fallidos      = fallidos
        self.call_from_thread(self._construir_tabla, eventos)

    def _set_estado(self, msg: str) -> None:
        try:
            self.query_one("#estado", Static).update(msg)
        except Exception:
            pass

    def _construir_tabla(self, eventos: list) -> None:
        # Actualizar opciones de servidores
        servidores = obtener_servidores_unicos(eventos)
        opciones   = [("Todos los servidores", "")] + [(s, s) for s in servidores]
        self.query_one("#sel-servidor", Select).set_options(opciones)

        # Eliminar LoadingIndicator si todavía existe
        try:
            self.query_one(LoadingIndicator).remove()
        except Exception:
            pass

        # Si la tabla ya existe, la reutilizamos — si no, la creamos    
        try:
            tabla = self.query_one("#tabla", DataTable)
            tabla.clear(columns=True)
            tabla.add_columns("Inscrito", "Fecha", "Hora", "Servidor", "Raid", "👥Participantes", "Rol")
        except Exception:
            tabla = DataTable(id="tabla", cursor_type="row")
            self.query_one("#contenedor-tabla").mount(tabla)
            tabla.add_columns("Inscrito", "Fecha", "Hora", "Servidor", "Raid", "👥Participantes", "Rol")

        self._aplicar_filtros()
            


    def _aplicar_filtros(self) -> None:
        try:
            tabla = self.query_one("#tabla", DataTable)
        except Exception:
            return

        eventos = list(self._todos_eventos)

        if self._filtro_dias != "0":
            eventos = filtrar_por_dias(eventos, int(self._filtro_dias))
        if self._filtro_servidor:
            eventos = filtrar_por_servidor(eventos, self._filtro_servidor)
        if self._filtro_texto:
            eventos = filtrar_por_texto(eventos, self._filtro_texto)
        if self._filtro_fecha:
            eventos = filtrar_por_fecha(eventos, self._filtro_fecha)

        self._eventos_filtrados = eventos
        tabla.clear()

        hoy      = date.today()
        manana   = hoy.toordinal() + 1
        semana   = hoy.toordinal() + 7
        mis_ins  = inscripciones.cargar()

        for ev in eventos:
            dt       = datetime.fromtimestamp(int(ev["unixtime"]))
            ord_ev   = dt.date().toordinal()

            # --- Color según proximidad ---
            if ord_ev == hoy.toordinal():
                color = "bold red"        # hoy
            elif ord_ev == manana:
                color = "bold yellow"     # mañana
            elif ord_ev <= semana:
                color = "bold green"      # esta semana
            else:
                color = "white"           # más lejos

            DIAS  = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
            fecha = Text(f"{DIAS[dt.weekday()]} {dt.strftime('%d/%m/%Y')}", style=color)
            hora  = Text(dt.strftime('%H:%M'), style=color)
            serv  = Text(ev.get("_servidor", "?")[:22], style=color)
            tit   = Text(ev.get("displayTitle", ev.get("title", "Sin título"))[:32], style=color)
            anot  = Text(str(ev.get("signupcount", "?")), style=color)
            mark  = Text("READY" if ev.get("_anotado") else "  ", style=color)

            ins     = mis_ins.get(str(ev.get("raidId", "")))
            rol_txt = Text(ins["rol"] if ins else "", style=color)

            tabla.add_row(mark, fecha, hora, serv, tit, anot, rol_txt)

        try:
            msg = self.query_one("#mensaje-vacio", Static)
            if eventos:
                msg.display = False
            else:
                msg.update("Elige un servidor para mostrar eventos")
                msg.display = True
        except Exception:
            pass

        aviso = f" | ⚠ sin resp: {len(self._fallidos)}" if self._fallidos else ""
        self._set_estado(f"READY {len(eventos)} evento(s){aviso}")

    @on(Select.Changed, "#sel-dias")
    def cambio_dias(self, event: Select.Changed) -> None:
        val = event.value
        if not val or val is Select.BLANK:
            return
        self._filtro_dias = str(val)
        self._aplicar_filtros()

    @on(Select.Changed, "#sel-servidor")
    def cambio_servidor(self, event: Select.Changed) -> None:
        val = event.value
        if not val or val is Select.BLANK:
            self._filtro_servidor = ""
        else:
            self._filtro_servidor = str(val)
        self._aplicar_filtros()

    @on(DataTable.RowSelected)
    def fila_seleccionada(self, event: DataTable.RowSelected) -> None:
        """Se dispara cuando el usuario presiona Enter en una fila."""
        fila = event.cursor_row
        if 0 <= fila < len(self._eventos_filtrados):
            self.push_screen(DetalleEventoModal(self._eventos_filtrados[fila]))

    def action_ver_detalle(self) -> None:
        """Abre el modal con el detalle del evento seleccionado."""
        try:
            tabla = self.query_one("#tabla", DataTable)
            fila  = tabla.cursor_row
            if 0 <= fila < len(self._eventos_filtrados):
                self.push_screen(DetalleEventoModal(self._eventos_filtrados[fila]))
        except Exception:
            pass

    def action_inscribirse(self) -> None:
        """Abre el modal de inscripción local para la fila seleccionada (solo si READY)."""
        try:
            tabla = self.query_one("#tabla", DataTable)
            fila  = tabla.cursor_row
            if not (0 <= fila < len(self._eventos_filtrados)):
                return
            ev = self._eventos_filtrados[fila]
            if not ev.get("_anotado"):
                return
            raid_id      = str(ev.get("raidId", ""))
            inscripcion  = inscripciones.obtener(raid_id)

            def _guardar(resultado):
                if resultado:
                    inscripciones.registrar(
                        raid_id,
                        resultado["nombre"],
                        resultado["clase"],
                        resultado["rol"],
                    )
                    self._aplicar_filtros()

            self.push_screen(InscribirseModal(ev, inscripcion), _guardar)
        except Exception:
            pass

    def action_recargar(self) -> None:
        """Recarga todos los datos desde la API."""
        self._set_estado("⏳ Recargando...")
        self.cargar_datos()

    def action_abrir_config(self) -> None:
        with open('.exit_code', 'w') as f:
            f.write('2')
        self.exit()

    def action_agregar_servers(self) -> None:
        with open('.exit_code', 'w') as f:
            f.write('3')
        self.exit()

if __name__ == "__main__":
    RaidHelperApp().run()