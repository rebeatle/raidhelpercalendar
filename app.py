from lang import t, tl, cargar_idioma
cargar_idioma()

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Label, Select, LoadingIndicator, Static, Input
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.binding import Binding
from textual import work, on
from rich.text import Text
from datetime import datetime, date

from api import obtener_todos_los_eventos
from filtros import filtrar_por_dias, filtrar_por_servidor, obtener_servidores_unicos, filtrar_por_texto, filtrar_por_fecha


class DetalleEventoModal(ModalScreen):
    """Modal con el detalle completo de un evento incluyendo signups."""

    BINDINGS = [("escape", "dismiss", t("bind_cerrar"))]

    def __init__(self, evento: dict):
        super().__init__()
        self.evento = evento

    def on_mount(self) -> None:
        self.focus()
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

        desc = detalle.get("description") or t("sin_descripcion")

        # --- Inscripción vía API ---
        signup = self.evento.get("_signup")
        if signup:
            cabecera_ins = (
                f"[bold magenta]{'─'*55}[/bold magenta]\n"
                f"[bold magenta]{t('inscrito_como')}[/bold magenta]  "
                f"[white]{signup.get('name', '?')}[/white]  ·  "
                f"[bold]{signup.get('specName', '?')}[/bold]  ·  "
                f"[dim]{signup.get('className', '?')}[/dim]\n"
                f"[bold magenta]{'─'*55}[/bold magenta]\n\n"
            )
        else:
            cabecera_ins = ""

        # --- Cabecera del evento ---
        texto = cabecera_ins + (
            f"[bold cyan]{'='*55}[/bold cyan]\n"
            f"[bold white] {detalle.get('displayTitle', detalle.get('title', '?'))}[/bold white]\n"
            f"[bold cyan]{'='*55}[/bold cyan]\n\n"
            f"[bold]{t('det_servidor')}[/bold]  {detalle.get('servername', '?')}\n"
            f"[bold]{t('det_fecha')}[/bold]     {fecha}\n"
            f"[bold]{t('det_lider')}[/bold]     {detalle.get('leadername', '?')}\n"
            f"[bold]{t('det_canal')}[/bold]     #{detalle.get('channelName', '?')}\n"
            f"[bold]{t('det_raid_id')}[/bold]   {detalle.get('raidid', '?')}\n\n"
            f"[bold]{t('det_descripcion')}[/bold]\n[dim]{desc}[/dim]\n\n"
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

            for estado in ["Bench", "Tentative", "Late", "Absence"]:
                extras = [s for s in signups if s.get("status") == "default"
                          and s.get("class", "").lower() == estado.lower()]
                if extras:
                    texto += f"[dim]── {estado} ({len(extras)}) ──[/dim]\n"
                    for m in extras:
                        texto += f"  [dim]{m.get('name', '?')}[/dim]\n"
                    texto += "\n"

            total = len([s for s in signups if s.get("status") == "primary"])
            texto += f"[bold cyan]{t('total_anotados', n=total)}[/bold cyan]\n\n"
        else:
            texto += f"[dim]{t('sin_anotados')}[/dim]\n\n"

        texto += f"[dim]{t('esc_cerrar')}[/dim]"

        try:
            self.query_one("#cargando", Static).update(texto)
        except Exception:
            pass

    def compose(self) -> ComposeResult:
        titulo = self.evento.get("displayTitle", self.evento.get("title", "Evento"))
        yield Container(
            Static(t("cargando_evento", titulo=titulo), id="cargando", markup=True),
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
        Binding("q", "quit",            t("bind_salir")),
        Binding("r", "recargar",        t("bind_recargar")),
        Binding("c", "abrir_config",    t("bind_config")),
        Binding("v", "agregar_servers", t("bind_agregar")),
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
        opciones_dias = [
            (t("dias_7"),    "7"),
            (t("dias_14"),  "14"),
            (t("dias_30"),  "30"),
            (t("dias_todos"), "0"),
        ]
        yield Header()
        with Horizontal(id="barra-filtros"):
            yield Label(t("label_periodo"))
            yield Select(options=opciones_dias, value="7", id="sel-dias")
            yield Label(t("label_servidor"))
            yield Select(options=[(t("todos_servidores"), "")], value="", id="sel-servidor")
            yield Label(t("label_buscar"))
            yield Input(placeholder=t("placeholder_buscar"), id="inp-buscar")
            yield Label(t("label_fecha"))
            yield Input(placeholder=t("placeholder_fecha"), id="inp-fecha")
            yield Static(t("iniciando"), id="estado")
        with Container(id="contenedor-tabla"):
            yield LoadingIndicator()
            yield Static("", id="mensaje-vacio")
        yield Footer()

    def on_mount(self) -> None:
        self.cargar_datos()
        self.set_interval(180, self._auto_recargar)

    def _auto_recargar(self) -> None:
        if isinstance(self.screen, DetalleEventoModal):
            return
        self.cargar_datos()

    @work(thread=True)
    def cargar_datos(self) -> None:
        self.call_from_thread(self._set_estado, t("consultando"))
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
        servidores = obtener_servidores_unicos(eventos)
        opciones   = [(t("todos_servidores"), "")] + [(s, s) for s in servidores]
        self.query_one("#sel-servidor", Select).set_options(opciones)

        try:
            self.query_one(LoadingIndicator).remove()
        except Exception:
            pass

        try:
            tabla = self.query_one("#tabla", DataTable)
            tabla.clear(columns=True)
            tabla.add_columns(
                t("col_inscrito"), t("col_fecha"), t("col_hora"),
                t("col_servidor"), t("col_raid"), t("col_participantes"), t("col_rol")
            )
        except Exception:
            tabla = DataTable(id="tabla", cursor_type="row")
            self.query_one("#contenedor-tabla").mount(tabla)
            tabla.add_columns(
                t("col_inscrito"), t("col_fecha"), t("col_hora"),
                t("col_servidor"), t("col_raid"), t("col_participantes"), t("col_rol")
            )

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

        hoy    = date.today()
        manana = hoy.toordinal() + 1
        semana = hoy.toordinal() + 7
        dias_semana = tl("dias_semana")

        for ev in eventos:
            dt     = datetime.fromtimestamp(int(ev["unixtime"]))
            ord_ev = dt.date().toordinal()

            if ord_ev == hoy.toordinal():
                color = "bold red"
            elif ord_ev == manana:
                color = "bold yellow"
            elif ord_ev <= semana:
                color = "bold green"
            else:
                color = "white"

            fecha = Text(f"{dias_semana[dt.weekday()]} {dt.strftime('%d/%m/%Y')}", style=color)
            hora  = Text(dt.strftime('%H:%M'), style=color)
            serv  = Text(ev.get("_servidor", "?")[:22], style=color)
            tit   = Text(ev.get("displayTitle", ev.get("title", t("sin_titulo")))[:32], style=color)
            anot  = Text(str(ev.get("signupcount", "?")), style=color)
            mark  = Text("READY" if ev.get("_anotado") else "  ", style=color)

            signup = ev.get("_signup")
            if signup:
                rol_txt = Text(f"{signup.get('name', '')} · {signup.get('specName', '')}", style=color)
            else:
                rol_txt = Text("", style=color)

            tabla.add_row(mark, fecha, hora, serv, tit, anot, rol_txt)

        try:
            msg = self.query_one("#mensaje-vacio", Static)
            if eventos:
                msg.display = False
            else:
                msg.update(t("mensaje_vacio"))
                msg.display = True
        except Exception:
            pass

        aviso = t("sin_resp", n=len(self._fallidos)) if self._fallidos else ""
        self._set_estado(t("estado_eventos", n=len(eventos), aviso=aviso))

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
        fila = event.cursor_row
        if 0 <= fila < len(self._eventos_filtrados):
            self.push_screen(DetalleEventoModal(self._eventos_filtrados[fila]))

    def action_ver_detalle(self) -> None:
        try:
            tabla = self.query_one("#tabla", DataTable)
            fila  = tabla.cursor_row
            if 0 <= fila < len(self._eventos_filtrados):
                self.push_screen(DetalleEventoModal(self._eventos_filtrados[fila]))
        except Exception:
            pass

    def action_recargar(self) -> None:
        self._set_estado(t("recargando"))
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
