import os
import sys
import requests

from lang import t, cargar_idioma, guardar_idioma, get_lang

ARCHIVOS_REQUERIDOS = ["api.txt", "api_key.txt"]


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


def _mostrar_preview_servidores(token: str) -> None:
    """Llama al endpoint de auth y muestra los servidores detectados."""
    print(t("token_servidores_detectando"))
    try:
        res = requests.get(
            f"https://raid-helper.xyz/api/auth/{token}",
            timeout=10
        )
        guilds = res.json().get("guilds", [])
        if guilds:
            print(t("token_servidores_encontrados", n=len(guilds)))
            for g in guilds[:10]:
                premium = " ★" if g.get("premium") else ""
                print(f"    • {g.get('name', g['id'])}{premium}")
            if len(guilds) > 10:
                print(f"    ... (+{len(guilds) - 10})")
        else:
            print(t("token_sin_servidores"))
    except Exception:
        pass  # No es crítico — el token ya fue guardado


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
            _mostrar_preview_servidores(token)
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


def menu_configuracion():
    while True:
        limpiar()
        encabezado()

        falta_api = not os.path.exists('api.txt')
        falta_key = not os.path.exists('api_key.txt')

        estado_api = t("menu_no_configurado") if falta_api else t("menu_configurado")
        estado_key = t("menu_no_configurado") if falta_key else t("menu_configurado")

        print(t("menu_estado"))
        print(f"    {t('menu_access_token')}: {estado_api}")
        print(f"    {t('menu_user_api_key')}: {estado_key}")
        print(t("menu_que_deseas"))
        print(t("menu_op1"))
        print(t("menu_op2"))
        print(t("menu_op3"))
        print(t("menu_op4"))
        print(t("menu_op0"))
        print()
        opcion = input(t("menu_elige")).strip()

        if opcion == "1":
            configurar_access_token()
        elif opcion == "2":
            configurar_user_api_key()
        elif opcion == "3":
            if falta_api:
                print(t("menu_falta_config"))
                pausar()
            else:
                return True
        elif opcion == "4":
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
    elif modo == "auto":
        seleccionar_idioma()
        if not verificar_archivos():
            primer_arranque()
        else:
            menu_configuracion()
