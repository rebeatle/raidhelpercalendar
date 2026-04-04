import json
import os

_ARCHIVO = "mis_inscripciones.json"

ROLES = {"T": "Tank", "H": "Healer", "D": "DPS"}


def cargar() -> dict:
    if not os.path.exists(_ARCHIVO):
        return {}
    try:
        with open(_ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def guardar(datos: dict) -> None:
    with open(_ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def obtener(raid_id: str) -> dict | None:
    return cargar().get(str(raid_id))


def registrar(raid_id: str, nombre: str, clase: str, rol: str) -> None:
    datos = cargar()
    datos[str(raid_id)] = {"nombre": nombre, "clase": clase, "rol": rol}
    guardar(datos)
