from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Label, Select, LoadingIndicator, Static
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.binding import Binding
from textual import work, on
from datetime import datetime

from api import obtener_todos_los_eventos
from filtros import filtrar_por_dias, filtrar_por_servidor, obtener_servidores_unicos


OPCIONES_DIAS = [
    ("Próximos 7 días",  "7"),
    ("Próximos 14 días", "14"),
    ("Próximos 30 días", "30"),
    ("Todos",            "0"),
]


class DetalleEventoModal(ModalScreen):
    """Modal con el detalle completo de un evento."""

    BINDINGS = [("escape", "dismiss", "Cerrar")]

    def __init__(self, evento: dict):
        super().__init__()
        self.evento = evento

    def compose(self) -> ComposeResult:
        ev    = self.evento
        fecha = datetime.fromtimestamp(int(ev.get("unixtime", 0))).strftime('%d/%m/%Y %H:%M')
        desc  = ev.get("description", "Sin descripción") or "Sin descripción"

        contenido = (
            f"[bold cyan]{ev.get('displayTitle', ev.get('title', 'Sin título'))}[/bold cyan]\n\n"
            f"[bold]Servidor:[/bold]  {ev.get('_servidor', '?')}\n"
            f"[bold]Fecha:[/bold]     {fecha}\n"
            f"[bold]Líder:[/bold]     {ev.get('leader', '?')}\n"
            f"[bold]Anotados:[/bold]  {ev.get('signupcount', '?')}\n"
            f"[bold]Canal:[/bold]     #{ev.get('channelName', '?')}\n"
            f"[bold]Raid ID:[/bold]   {ev.get('raidId', '?')}\n\n"
            f"[bold]Descripción:[/bold]\n{desc}\n\n"
            f"[dim]ESC para cerrar[/dim]"
        )

        yield Container(Static(contenido, markup=True), id="modal-cuerpo")

    DEFAULT_CSS = """
    DetalleEventoModal {
        align: center middle;
    }
    #modal-cuerpo {
        width: 70%;
        max-height: 80%;
        background: $surface;
        border: thick $primary;
        padding: 2 4;
        overflow-y: auto;
    }
    """


class RaidHelperApp(App):

    TITLE    = "⚔ RaidHelper Dashboard"
    SUB_TITLE = "Ken's Raid Tracker"

    BINDINGS = [
        Binding("q",      "quit",        "Salir"),
        Binding("r",      "recargar",    "Recargar"),
        Binding("enter",  "ver_detalle", "Ver detalle"),
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
    """

    def __init__(self):
        super().__init__()
        self._todos_eventos     = []
        self._eventos_filtrados = []
        self._filtro_dias       = "7"
        self._filtro_servidor   = ""

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="barra-filtros"):
            yield Label(" Período: ")
            yield Select(options=OPCIONES_DIAS, value="7", id="sel-dias")
            yield Label("Servidor: ")
            yield Select(options=[("Todos", "")], value="", id="sel-servidor")
            yield Static("Iniciando...", id="estado")

        with Container(id="contenedor-tabla"):
            yield LoadingIndicator()

        yield Footer()

    def on_mount(self) -> None:
        self.cargar_datos()

    @work(thread=True)
    def cargar_datos(self) -> None:
        """Carga datos de todos los servidores en hilo separado."""
        self.call_from_thread(self._set_estado, "⏳ Consultando servidores...")
        eventos = obtener_todos_los_eventos()
        self._todos_eventos = eventos
        self.call_from_thread(self._construir_tabla, eventos)

    def _set_estado(self, msg: str) -> None:
        try:
            self.query_one("#estado", Static).update(msg)
        except Exception:
            pass

    def _construir_tabla(self, eventos: list) -> None:
        """Construye la DataTable una vez que los datos están listos."""
        # Actualizar opciones de servidores
        servidores = obtener_servidores_unicos(eventos)
        opciones   = [("Todos los servidores", "")] + [(s, s) for s in servidores]
        self.query_one("#sel-servidor", Select).set_options(opciones)

        # Reemplazar LoadingIndicator por DataTable
        try:
            self.query_one(LoadingIndicator).remove()
        except Exception:
            pass

        tabla = DataTable(id="tabla", cursor_type="row")
        self.query_one("#contenedor-tabla").mount(tabla)
        tabla.add_columns("Fecha", "Hora", "Servidor", "Raid", "👥")

        self._aplicar_filtros()

    def _aplicar_filtros(self) -> None:
        """Filtra los eventos y refresca la tabla."""
        try:
            tabla = self.query_one("#tabla", DataTable)
        except Exception:
            return

        eventos = list(self._todos_eventos)

        if self._filtro_dias != "0":
            eventos = filtrar_por_dias(eventos, int(self._filtro_dias))

        if self._filtro_servidor:
            eventos = filtrar_por_servidor(eventos, self._filtro_servidor)

        self._eventos_filtrados = eventos
        tabla.clear()

        for ev in eventos:
            fecha    = datetime.fromtimestamp(int(ev["unixtime"])).strftime('%d/%m/%Y')
            hora     = ev.get("time", "??:??")
            servidor = ev.get("_servidor", "?")[:22]
            titulo   = ev.get("displayTitle", ev.get("title", "Sin título"))[:32]
            anotados = str(ev.get("signupcount", "?"))
            tabla.add_row(fecha, hora, servidor, titulo, anotados)

        self._set_estado(f"✅ {len(eventos)} evento(s)")

    @on(Select.Changed, "#sel-dias")
    def cambio_dias(self, event: Select.Changed) -> None:
        self._filtro_dias = str(event.value)
        self._aplicar_filtros()

    @on(Select.Changed, "#sel-servidor")
    def cambio_servidor(self, event: Select.Changed) -> None:
        self._filtro_servidor = str(event.value) if event.value else ""
        self._aplicar_filtros()

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


if __name__ == "__main__":
    RaidHelperApp().run()