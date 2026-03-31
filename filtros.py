import time


def filtrar_por_dias(eventos: list, dias: int) -> list:
    """Filtra eventos dentro de los próximos N días."""
    ahora  = int(time.time())
    limite = ahora + (dias * 86400)
    return [ev for ev in eventos if ahora < int(ev.get("unixtime", 0)) <= limite]


def filtrar_por_servidor(eventos: list, nombre_servidor: str) -> list:
    """Filtra eventos por nombre de servidor (búsqueda parcial)."""
    if not nombre_servidor:
        return eventos
    busqueda = nombre_servidor.lower()
    return [ev for ev in eventos if busqueda in ev.get("_servidor", "").lower()]


def obtener_servidores_unicos(eventos: list) -> list:
    """Retorna lista de nombres de servidores únicos, ordenada."""
    return sorted(set(ev.get("_servidor", "?") for ev in eventos))