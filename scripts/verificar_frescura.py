#!/usr/bin/env python3
"""
Revisa qué tan viejo es el último dato de cada fuente y avisa cuando alguno
se atrasa más de lo normal.

En la v1, si una fuente dejaba de responder, el workflow igual terminaba "en
verde" y nadie se enteraba. Acá:

- El resultado se guarda en `estado.json` (clave "frescura"), y la página lo
  usa para mostrar "dato atrasado" junto a la cifra afectada.
- Si aparece un atraso NUEVO (o si el atraso sigue y pasaron 24 horas desde el
  último aviso), el script termina con código 1. GitHub marca la corrida en
  rojo y le manda un correo al dueño del repo. Así llega un aviso por problema
  y por día, no uno cada 15 minutos.

Se ejecuta con el directorio de trabajo en la carpeta de datos:

    cd datos && python ../scripts/verificar_frescura.py
"""

import json
import os
import sys
from datetime import date, datetime, timedelta, timezone

BOLIVIA = timezone(timedelta(hours=-4))

# Atraso máximo tolerado antes de considerar un dato "atrasado".
# Los umbrales contemplan fines de semana, feriados y el rezago normal con el
# que el BCB publica cada serie.
UMBRALES = {
    "usdt": {"nombre": "Dólar paralelo (Binance P2P)", "horas": 8},
    "tco": {"nombre": "Tipo de cambio oficial (TCO)", "dias": 4},
    "bancos": {"nombre": "Tipo de cambio por banco", "dias": 6},
    "reservas": {"nombre": "Reservas internacionales", "dias": 21},
    "balanza": {"nombre": "Balanza cambiaria", "dias": 80},
    "itcr": {"nombre": "Índice de tipo de cambio real", "dias": 80},
    "noticias": {"nombre": "Titulares de prensa", "dias": 3},
}
REAVISO_S = 24 * 3600


def ultimo_dato(data, noticias):
    """Devuelve, por serie, el instante (UTC) del último dato disponible."""
    def fecha(d):
        y, m, dd = (int(x) for x in d[:10].split("-"))
        # Una fecha sin hora se toma como el final de ese día en Bolivia.
        return datetime(y, m, dd, 23, 59, tzinfo=BOLIVIA).astimezone(timezone.utc)

    res = {}
    intra = data.get("usdt_intraday_recent") or []
    if intra:
        ts = max(p["ts"] for p in intra)
        res["usdt"] = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    for clave, serie in (("tco", "tco"), ("reservas", "reservas"),
                         ("balanza", "balanza"), ("itcr", "itcr")):
        filas = data.get(serie) or []
        if filas:
            res[clave] = fecha(max(r["date"] for r in filas))
    bancos = [s[-1]["date"] for s in (data.get("banks") or {}).values() if s]
    if bancos:
        res["bancos"] = fecha(max(bancos))
    if noticias and noticias.get("updated"):
        res["noticias"] = fecha(noticias["updated"])
    return res


def evaluar(data, noticias, ahora=None):
    ahora = ahora or datetime.now(timezone.utc)
    ultimos = ultimo_dato(data, noticias)
    resultado = {}
    for clave, u in UMBRALES.items():
        t = ultimos.get(clave)
        limite = timedelta(hours=u["horas"]) if "horas" in u else timedelta(days=u["dias"])
        atrasado = t is None or (ahora - t) > limite
        resultado[clave] = {
            "nombre": u["nombre"],
            "ultimo_dato_utc": t.strftime("%Y-%m-%dT%H:%M:%SZ") if t else None,
            "atrasado": atrasado,
        }
    return resultado


def main():
    with open("data.json", encoding="utf-8") as f:
        data = json.load(f)
    noticias = None
    if os.path.exists("noticias.json"):
        with open("noticias.json", encoding="utf-8") as f:
            noticias = json.load(f)
    estado = {"fuentes": {}}
    if os.path.exists("estado.json"):
        with open("estado.json", encoding="utf-8") as f:
            estado = json.load(f)

    ahora = datetime.now(timezone.utc)
    frescura = evaluar(data, noticias, ahora)
    previo = estado.get("frescura", {})
    avisos = estado.get("avisos", {})

    hay_que_avisar = []
    for clave, r in frescura.items():
        if not r["atrasado"]:
            avisos.pop(clave, None)
            continue
        estaba = previo.get(clave, {}).get("atrasado", False)
        ultimo_aviso = avisos.get(clave)
        vencido = True
        if ultimo_aviso:
            t = datetime.strptime(ultimo_aviso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            vencido = (ahora - t).total_seconds() >= REAVISO_S
        if not estaba or vencido:
            hay_que_avisar.append(clave)
            avisos[clave] = ahora.strftime("%Y-%m-%dT%H:%M:%SZ")

    estado["frescura"] = frescura
    estado["avisos"] = avisos
    with open("estado.json", "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=1, sort_keys=True)

    for clave, r in frescura.items():
        marca = "ATRASADO" if r["atrasado"] else "ok"
        print(f"{marca:9} {r['nombre']}: último dato {r['ultimo_dato_utc']}")

    if hay_que_avisar:
        nombres = ", ".join(frescura[c]["nombre"] for c in hay_que_avisar)
        print(f"::error::Datos atrasados: {nombres}. Revisar el registro de esta corrida "
              f"y estado.json en la rama 'datos'.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
