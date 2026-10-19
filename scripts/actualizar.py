#!/usr/bin/env python3
"""
Orquestador de la actualización de datos de la v2.

Reutiliza sin cambios la lógica de descarga de la v1 (update_data.py y
update_news.py, ya probadas en producción) y le agrega dos cosas que la v1
no tenía:

1. **Registro de salud por fuente** en `estado.json`: para cada fuente guarda
   el último intento, el último éxito, el último error y cuántas veces seguidas
   falló. La página lo usa para avisar al lector cuando un dato está atrasado
   y `verificar_frescura.py` lo usa para mandar una alerta.
2. **Modo automático** (`--auto`): en cada corrida (cada 15 minutos) consulta
   siempre el paralelo (Binance) y el TCO (es una sola consulta liviana, y así
   el TCO que el BCB publica a las 23:30 aparece en minutos y no horas
   después). Las fuentes pesadas del BCB (tasas por banco, reservas, balanza,
   ITCR) y las noticias se consultan solo si pasaron 3 horas desde su último
   intento, igual que en la v1.

Se ejecuta con el directorio de trabajo apuntando a la carpeta de datos
(donde están data.json, noticias.json y estado.json):

    cd datos && python ../scripts/actualizar.py --auto
"""

import argparse
import json
import os
import sys
import traceback
from datetime import datetime, timezone

import update_data as ud
import update_news as un

ESTADO_PATH = "estado.json"

# Fuentes livianas: se consultan en todas las corridas.
SIEMPRE = ["usdt", "tco"]
# Fuentes pesadas: se consultan si su último intento tiene más de 3 horas.
CADA_3_HORAS = ["banks", "reservas", "balanza", "itcr", "noticias"]
INTERVALO_PESADAS_S = 3 * 3600 - 5 * 60  # 2h55m: tolera demoras del cron

PASOS = {
    "tco": ("TCO oficial", ud.fetch_tco),
    "banks": ("Tasas bancarias", ud.fetch_bank_rates),
    "usdt": ("USDT/BOB", ud.fetch_usdt_bob),
    "reservas": ("Reservas internacionales", ud.fetch_reservas),
    "balanza": ("Balanza cambiaria", lambda d: ud.fetch_xlsx_series(d, "balanza")),
    "itcr": ("ITCR", lambda d: ud.fetch_xlsx_series(d, "itcr")),
}


def ahora_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def segundos_desde(iso):
    if not iso:
        return float("inf")
    t = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - t).total_seconds()


def cargar_estado():
    if os.path.exists(ESTADO_PATH):
        with open(ESTADO_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"fuentes": {}}


def guardar_estado(estado):
    with open(ESTADO_PATH, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=1, sort_keys=True)


def registrar(estado, clave, ok, cambio=False, error=None):
    f = estado["fuentes"].setdefault(clave, {})
    f["ultimo_intento"] = ahora_iso()
    if ok:
        f["ultimo_ok"] = f["ultimo_intento"]
        f["fallas_seguidas"] = 0
        f["ultimo_error"] = None
        if cambio:
            f["ultimo_cambio"] = f["ultimo_intento"]
    else:
        f["fallas_seguidas"] = int(f.get("fallas_seguidas", 0)) + 1
        f["ultimo_error"] = (error or "error desconocido")[:300]


def elegir_fuentes(estado, solo):
    if solo:
        return solo
    elegidas = list(SIEMPRE)
    for clave in CADA_3_HORAS:
        ultimo = estado["fuentes"].get(clave, {}).get("ultimo_intento")
        if segundos_desde(ultimo) >= INTERVALO_PESADAS_S:
            elegidas.append(clave)
    return elegidas


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", action="store_true",
                        help="Elegir las fuentes según el tiempo desde su último intento.")
    parser.add_argument("--solo", default=None,
                        help="Lista separada por comas: tco,banks,usdt,reservas,balanza,itcr,noticias")
    args = parser.parse_args()
    solo = [s.strip() for s in args.solo.split(",")] if args.solo else None
    if not args.auto and not solo:
        solo = list(PASOS) + ["noticias"]

    estado = cargar_estado()
    fuentes = elegir_fuentes(estado, solo)
    ud.log(f"Fuentes de esta corrida: {', '.join(fuentes)}")

    data = ud.load_data()
    hubo_cambio = False
    for clave in fuentes:
        if clave not in PASOS:
            continue
        nombre, fn = PASOS[clave]
        try:
            cambio = bool(fn(data))
            # Las funciones de la v1 devuelven False tanto si "no hubo dato
            # nuevo" como si "se descartó por el chequeo de sensatez". Las dos
            # cuentan como intento sin excepción; la frescura real se mide
            # aparte, con la fecha del último dato (verificar_frescura.py).
            registrar(estado, clave, ok=True, cambio=cambio)
            hubo_cambio = hubo_cambio or cambio
        except Exception as e:  # noqa: BLE001 - se registra y se sigue
            ud.log(f"ERROR en '{nombre}': {e}")
            traceback.print_exc()
            registrar(estado, clave, ok=False, error=f"{type(e).__name__}: {e}")

    if hubo_cambio:
        data["meta"]["asof"] = ud.bolivia_today()
        ud.save_data(data)
        ud.log("data.json actualizado.")
    else:
        ud.log("Sin cambios en data.json.")

    if "noticias" in fuentes:
        try:
            antes = os.path.getmtime(un.OUT_PATH) if os.path.exists(un.OUT_PATH) else None
            un.main()
            despues = os.path.getmtime(un.OUT_PATH) if os.path.exists(un.OUT_PATH) else None
            registrar(estado, "noticias", ok=True, cambio=(antes != despues))
        except Exception as e:  # noqa: BLE001
            ud.log(f"ERROR en 'Noticias': {e}")
            traceback.print_exc()
            registrar(estado, "noticias", ok=False, error=f"{type(e).__name__}: {e}")

    estado["ultima_corrida"] = ahora_iso()
    guardar_estado(estado)
    return 0


if __name__ == "__main__":
    sys.exit(main())
