from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Label, Select, LoadingIndicator, Static
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.binding import Binding
from textual import work, on
from datetime import datetime
from rich.text import Text
from datetime import datetime, date
from textual.widgets import Input  

from api import obtener_todos_los_eventos
from filtros import filtrar_por_dias, filtrar_por_servidor, obtener_servidores_unicos, filtrar_por_texto, filtrar_por_fecha


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

        # --- Cabecera del evento ---
        texto = (
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


class RaidHelperApp(App):

    TITLE    = "⚔ RaidHelper Viewer"
    SUB_TITLE = "Made by https://github.com/rebeatle"

    BINDINGS = [
    Binding("q", "quit",            "Salir"),
    Binding("r", "recargar",        "Recargar"),
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
        self._todos_eventos     = []
        self._eventos_filtrados = []
        self._filtro_dias       = "7"
        self._filtro_texto      = ""
        self._filtro_servidor   = ""
        self._filtro_fecha      = ""
        self._fallidos          = []
        
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
            tabla.add_columns("Inscrito", "Fecha", "Hora", "Servidor", "Raid", "👥Participantes")
        except Exception:
            tabla = DataTable(id="tabla", cursor_type="row")
            self.query_one("#contenedor-tabla").mount(tabla)
            tabla.add_columns("Inscrito", "Fecha", "Hora", "Servidor", "Raid", "👥Participantes")

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

            tabla.add_row(mark, fecha, hora, serv, tit, anot)

        aviso = f" | ⚠ sin resp: {len(self._fallidos)}" if self._fallidos else ""
        self._set_estado(f"READY {len(eventos)} evento(s){aviso}")

    @on(Select.Changed, "#sel-dias")
    def cambio_dias(self, event: Select.Changed) -> None:
        self._filtro_dias = str(event.value)
        self._aplicar_filtros()

    @on(Select.Changed, "#sel-servidor")
    def cambio_servidor(self, event: Select.Changed) -> None:
        self._filtro_servidor = str(event.value) if event.value else ""
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