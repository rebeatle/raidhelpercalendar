import os
import sys
import requests

from lang import t, tl, cargar_idioma, guardar_idioma, get_lang

ARCHIVOS_REQUERIDOS = ["api.txt", "api_key.txt", "servers.txt"]


def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input(t("continuar"))


def encabezado():
    print("=" * 60)
    print(f"   ⚔  RaidHelper Viewer — {t('menu_titulo')}")
    print("""
____        _     _   _   _      _
|  _ \ __ _(_) __| | | | | | ___| |_ __   ___ _ __
| |_) / _` | |/ _` | | |_| |/ _ \ | '_ \ / _ \ '__|
|  _ < (_| | | (_| | |  _  |  __/ | |_) |  __/ |
|_| \_\__,_|_|\__,_| |_| |_|\___|_| .__/ \___|_|
__     ___                        |_|
\ \   / (_) _____      _____ _ __
 \ \ / /| |/ _ \ \ /\ / / _ \ '__|
  \ V / | |  __/\ V  V /  __/ |
   \_/  |_|\___| \_/\_/ \___|_|
          """)
    print("=" * 60)


def verificar_archivos() -> bool:
    return all(os.path.exists(f) for f in ARCHIVOS_REQUERIDOS)


def seleccionar_idioma():
    """Muestra selección de idioma si no hay lang.txt guardado."""
    if os.path.exists("lang.txt"):
        return
    limpiar()
    print("=" * 60)
    print("   ⚔  RaidHelper Viewer")
    print("=" * 60)
    print()
    print("  Elige tu idioma / Choose your language:")
    print()
    print("  [1] Español")
    print("  [2] English")
    print()
    while True:
        opcion = input("  > ").strip()
        if opcion == "1":
            guardar_idioma("es")
            break
        elif opcion == "2":
            guardar_idioma("en")
            break
        else:
            print("  [1] Español  /  [2] English")


def cambiar_idioma():
    limpiar()
    encabezado()
    actual = get_lang()
    nombre_actual = t("idioma_es") if actual == "es" else t("idioma_en")
    print(f"\n  {t('idioma_actual')}: {nombre_actual}")
    print()
    print(f"  [1] {t('idioma_es')}")
    print(f"  [2] {t('idioma_en')}")
    print()
    opcion = input("  > ").strip()
    if opcion == "1":
        guardar_idioma("es")
        print(t("idioma_cambiado_es"))
    elif opcion == "2":
        guardar_idioma("en")
        print(t("idioma_cambiado_en"))
    else:
        print(t("idioma_sin_cambios"))
    pausar()


def configurar_access_token():
    limpiar()
    encabezado()
    print(t("token_titulo"))
    print(t("token_instrucciones"))
    token = input(t("token_pegar")).strip()
    if not token:
        print(t("token_vacio"))
        pausar()
        return False

    print(t("token_verificando"))
    try:
        res = requests.post(
            "https://raid-helper.xyz/api/events/",
            json={"serverid": "1", "accessToken": token},
            timeout=10
        )
        if res.status_code in [200, 403, 404]:
            with open('api.txt', 'w', encoding='utf-8') as f:
                f.write(token)
            print(t("token_guardado"))
            pausar()
            return True
        else:
            print(t("token_invalido", code=res.status_code))
            pausar()
            return False
    except Exception:
        print(t("token_sin_conexion"))
        pausar()
        return False


def configurar_user_api_key():
    limpiar()
    encabezado()
    print(t("apikey_titulo"))
    print(t("apikey_instrucciones"))
    tiene_key = os.path.exists('api_key.txt') and open('api_key.txt', encoding='utf-8').read().strip()
    aviso = t("apikey_conservar") if tiene_key else t("apikey_saltar")
    key = input(t("apikey_pegar", aviso=aviso)).strip()
    if not key:
        print(t("apikey_sin_cambios") if tiene_key else t("apikey_saltado"))
        pausar()
        return True
    with open('api_key.txt', 'w', encoding='utf-8') as f:
        f.write(key)
    print(t("apikey_guardada"))
    pausar()
    return True


def configurar_servidores():
    limpiar()
    encabezado()
    print(t("servers_titulo"))
    print(t("servers_instrucciones"))
    print(t("servers_como_ingresar"))
    print(t("servers_uno_por_uno"))
    print(t("servers_desde_archivo"))
    print(t("enter_salir"))
    print()
    opcion = input(t("elige_opcion_12")).strip()

    ids = []
    if opcion == "1":
        ids = ingresar_ids_manual()
    elif opcion == "2":
        ids = ingresar_ids_desde_archivo()
    else:
        print(t("opcion_invalida"))
        pausar()
        return False

    if not ids:
        print(t("servers_sin_ids"))
        pausar()
        return False

    guardar_servidores(ids)
    print(t("servers_guardados", n=len(ids)))
    pausar()
    return True


def ingresar_ids_manual() -> list:
    ids = []
    print(t("manual_ingresa"))
    print(t("manual_deja_vacio"))
    print(t("enter_salir"))
    while True:
        id_srv = input(t("manual_servidor_n", n=len(ids) + 1)).strip()
        if not id_srv:
            break
        if id_srv.isdigit():
            ids.append(id_srv)
            print(t("manual_id_agregado", id=id_srv))
        else:
            print(t("manual_id_invalido"))
    return ids


def ingresar_ids_desde_archivo() -> list:
    ruta = input(t("archivo_ruta")).strip().strip('"')
    if not os.path.exists(ruta):
        print(t("archivo_no_encontrado", ruta=ruta))
        return []
    ids = []
    with open(ruta, 'r', encoding='utf-8') as f:
        for linea in f:
            id_srv = linea.strip()
            if id_srv.isdigit():
                ids.append(id_srv)
    if ids:
        print(t("archivo_encontrados", n=len(ids)))
    else:
        print(t("archivo_sin_ids"))
    return ids


def guardar_servidores(ids: list):
    with open('servers.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(ids))


def agregar_servidores():
    limpiar()
    encabezado()

    ids_actuales = []
    if os.path.exists('servers.txt'):
        with open('servers.txt', 'r', encoding='utf-8') as f:
            ids_actuales = [l.strip() for l in f if l.strip().isdigit()]

    print(t("agregar_actuales", n=len(ids_actuales)))
    for i, sid in enumerate(ids_actuales, 1):
        print(f"    {i}. {sid}")

    print(t("agregar_como"))
    print(t("servers_uno_por_uno"))
    print(t("servers_desde_archivo"))
    print()
    print(t("enter_salir"))
    opcion = input(t("elige_opcion_12")).strip()

    nuevos = []
    if opcion == "1":
        nuevos = ingresar_ids_manual()
    elif opcion == "2":
        nuevos = ingresar_ids_desde_archivo()

    ids_finales = list(dict.fromkeys(ids_actuales + nuevos))
    agregados   = len(ids_finales) - len(ids_actuales)

    if agregados > 0:
        guardar_servidores(ids_finales)
        print(t("agregar_nuevos", n=agregados))
        print(t("agregar_total", n=len(ids_finales)))
    else:
        print(t("agregar_ninguno"))
    pausar()


def menu_configuracion():
    while True:
        limpiar()
        encabezado()

        falta_api = not os.path.exists('api.txt')
        falta_key = not os.path.exists('api_key.txt')
        falta_srv = not os.path.exists('servers.txt')

        estado_api = t("menu_no_configurado") if falta_api else t("menu_configurado")
        estado_key = t("menu_no_configurado") if falta_key else t("menu_configurado")
        estado_srv = t("menu_no_configurado") if falta_srv else t("menu_configurado")

        print(t("menu_estado"))
        print(f"    {t('menu_access_token')}: {estado_api}")
        print(f"    {t('menu_user_api_key')}: {estado_key}")
        print(f"    {t('menu_servidores_lbl')}: {estado_srv}")
        print(t("menu_que_deseas"))
        print(t("menu_op1"))
        print(t("menu_op2"))
        print(t("menu_op3"))
        print(t("menu_op4"))
        print(t("menu_op5"))
        print(t("menu_op6"))
        print(t("menu_op0"))
        print()
        opcion = input(t("menu_elige")).strip()

        if opcion == "1":
            configurar_access_token()
        elif opcion == "2":
            configurar_user_api_key()
        elif opcion == "3":
            configurar_servidores()
        elif opcion == "4":
            agregar_servidores()
        elif opcion == "5":
            if falta_api or falta_srv:
                print(t("menu_falta_config"))
                pausar()
            else:
                return True
        elif opcion == "6":
            cambiar_idioma()
        elif opcion == "0":
            sys.exit(0)


def primer_arranque():
    limpiar()
    encabezado()
    print()
    print(t("bienvenido"))
    print()
    print(t("config_falta"))
    pausar()

    if not os.path.exists('api.txt'):
        configurar_access_token()

    if not os.path.exists('api_key.txt'):
        configurar_user_api_key()

    if not os.path.exists('servers.txt'):
        configurar_servidores()

    limpiar()
    encabezado()
    print()
    print(t("todo_configurado"))
    print()
    print(t("app_abre"))
    print()
    print(t("recuerda"))
    print(t("atajos"))
    print()
    pausar()


if __name__ == "__main__":
    cargar_idioma()
    modo = sys.argv[1] if len(sys.argv) > 1 else "auto"

    if modo == "menu":
        menu_configuracion()
    elif modo == "agregar":
        agregar_servidores()
    elif modo == "auto":
        seleccionar_idioma()
        if not verificar_archivos():
            primer_arranque()
        else:
            menu_configuracion()
