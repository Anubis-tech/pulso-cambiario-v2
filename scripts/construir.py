#!/usr/bin/env python3
"""
Generador del sitio Pulso Económico v2.

Lee los datos (data.json, noticias.json, estado.json), la configuración
(config/sitio.json), las plantillas (sitio/plantillas) y los textos
(sitio/contenido), y escribe el sitio completo, listo para publicar, en una
carpeta de salida.

A diferencia de la v1, aquí las cifras se escriben DIRECTAMENTE en el HTML en
cada actualización. Google y el visitante ven "Bs 11,81" apenas abren la
página, sin esperar a que JavaScript descargue un archivo de 389 KB. Los
gráficos interactivos siguen cargándose después, desde archivos de datos más
chicos, uno por página.

Uso:
    python scripts/construir.py --datos datos --salida _site
    python scripts/construir.py --datos datos --salida _site --entorno produccion
    python scripts/construir.py ... --base ""      # servir el preview en la raíz (pruebas locales)
"""

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

RAIZ = Path(__file__).resolve().parent.parent
SITIO = RAIZ / "sitio"
BOLIVIA = timezone(timedelta(hours=-4))

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
MESES_C = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]

# Tramo en que la serie "tco" de los datos NO es el tipo de cambio oficial
# legal sino el "valor referencial" que el BCB publicó desde el 1-dic-2025
# mientras el oficial seguía fijo en 6,86 / 6,96. Ver AUDITORIA.md.
TRAMO_REFERENCIAL = {"desde": "2025-12-01", "hasta": "2026-06-28",
                     "etiqueta": "Valor referencial BCB", "color": "var(--band-ref)"}

# Nombres comerciales de los bancos (el dato del BCB usa la razón social).
NOMBRE_BANCO = {
    "Banco de Credito": "BCP (Banco de Crédito)",
    "Banco Mercantil Santa Cruz": "Mercantil Santa Cruz (BMSC)",
    "Banco Nacional de Bolivia": "Banco Nacional de Bolivia (BNB)",
    "Banco Solidario": "BancoSol",
    "Banco Economico": "Banco Económico",
    "Banco Union": "Banco Unión",
    "Banco de la Nacion Argentina": "Banco de la Nación Argentina",
    "Banco PyME Ecofuturo": "Banco PyME Ecofuturo",
    "Banco PyME de la Comunidad": "Banco PyME de la Comunidad",
}
BANCOS_PEQUENOS = {"Banco PyME Ecofuturo", "Banco PyME de la Comunidad"}


# ---------------------------------------------------------------------------
# Formatos (español de Bolivia: coma decimal, punto de miles)
# ---------------------------------------------------------------------------

def num(x, dec=2, signo=False):
    if x is None:
        return "—"
    s = f"{abs(x):,.{dec}f}".replace(",", "§").replace(".", ",").replace("§", ".")
    if x < 0 and round(abs(x), dec) != 0:
        return "−" + s
    if signo and round(x, dec) != 0:
        return "+" + s
    return s


def fecha_larga(iso):
    y, m, d = (int(v) for v in iso[:10].split("-"))
    return f"{d} de {MESES[m - 1]} de {y}"


def fecha_corta(iso, anio=True):
    y, m, d = (int(v) for v in iso[:10].split("-"))
    return f"{d} {MESES_C[m - 1]}" + (f" {y}" if anio else "")


def mes_anio(iso):
    y, m, _ = (int(v) for v in iso[:10].split("-"))
    return f"{MESES[m - 1]} de {y}"


def utc_a_bolivia(ts):
    """'YYYY-MM-DD HH:MM:SS' en UTC -> datetime en hora de Bolivia."""
    return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).astimezone(BOLIVIA)


def resta_dias(iso, n):
    return (date.fromisoformat(iso[:10]) - timedelta(days=n)).isoformat()


def en_o_antes(filas, fecha, clave):
    """Último valor de 'clave' con fecha <= 'fecha' (filas ordenadas)."""
    res = None
    for r in filas:
        if r["date"] <= fecha and r.get(clave) is not None:
            res = r
        elif r["date"] > fecha:
            break
    return res


def direccion(delta, umbral=0.0005):
    if delta is None or abs(delta) < umbral:
        return "igual"
    return "sube" if delta > 0 else "baja"


def flecha(delta, umbral=0.0005):
    d = direccion(delta, umbral)
    return {"sube": "▲", "baja": "▼", "igual": "="}[d]


# ---------------------------------------------------------------------------
# Cálculos sobre los datos
# ---------------------------------------------------------------------------

def calcular(data, noticias, estado):
    D = {}

    # --- TCO / valor referencial ---
    tco = sorted([r for r in data["tco"] if r.get("tco_venta_bcb") is not None], key=lambda r: r["date"])
    u = tco[-1]
    hace7 = en_o_antes(tco, resta_dias(u["date"], 7), "tco_venta_bcb")
    anterior = next((r for r in reversed(tco[:-1]) if r["tco_venta_bcb"] != u["tco_venta_bcb"] or r["tco_compra_bcb"] != u.get("tco_compra_bcb")), None)
    d7 = (u["tco_venta_bcb"] - hace7["tco_venta_bcb"]) if hace7 else None
    D["tco"] = {
        "fecha": u["date"], "fecha_larga": fecha_larga(u["date"]), "fecha_corta": fecha_corta(u["date"]),
        "compra": u.get("tco_compra_bcb"), "venta": u["tco_venta_bcb"],
        "compra_txt": num(u.get("tco_compra_bcb")), "venta_txt": num(u["tco_venta_bcb"]),
        "iguales": u.get("tco_compra_bcb") == u["tco_venta_bcb"],
        "d7": d7, "d7_txt": num(d7, 2, True) if d7 is not None else None, "d7_dir": direccion(d7), "d7_flecha": flecha(d7),
        "anterior": anterior and {"fecha": anterior["date"], "fecha_corta": fecha_corta(anterior["date"]), "venta_txt": num(anterior["tco_venta_bcb"])},
    }
    hace30 = en_o_antes(tco, resta_dias(u["date"], 30), "tco_venta_bcb")
    if hace30:
        ch = u["tco_venta_bcb"] - hace30["tco_venta_bcb"]
        D["tco"]["d30"] = ch
        D["tco"]["d30_txt"] = num(ch, 2, True)
        D["tco"]["d30_pct_txt"] = num(ch / hace30["tco_venta_bcb"] * 100, 1, True)
        D["tco"]["d30_dir"] = direccion(ch)
    D["tco"]["ultimos"] = [
        {"fecha_corta": fecha_corta(r["date"]), "compra_txt": num(r.get("tco_compra_bcb")), "venta_txt": num(r["tco_venta_bcb"])}
        for r in reversed(tco[-10:])
    ]

    # --- Paralelo USDT/BOB ---
    diario = sorted(data["usdt"], key=lambda r: r["date"])
    intra = sorted(data.get("usdt_intraday_recent") or [], key=lambda p: p["ts"])
    if intra:
        valor, ts = intra[-1]["value"], intra[-1]["ts"]
    else:
        valor, ts = diario[-1]["usdt_bob"], diario[-1]["date"] + " 16:00:00"
    hb = utc_a_bolivia(ts)
    ult_d = diario[-1]["date"]
    p7 = en_o_antes(diario, resta_dias(ult_d, 7), "usdt_bob")
    pd7 = (valor - p7["usdt_bob"]) if p7 else None
    corte24 = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") - timedelta(hours=24)
    ult24 = [p["value"] for p in intra if datetime.strptime(p["ts"], "%Y-%m-%d %H:%M:%S") >= corte24]
    D["usdt"] = {
        "valor": valor, "valor_txt": num(valor), "ts": ts,
        "hora": hb.strftime("%H:%M"), "fecha": hb.date().isoformat(),
        "fecha_larga": fecha_larga(hb.date().isoformat()), "fecha_corta": fecha_corta(hb.date().isoformat()),
        "d7": pd7, "d7_txt": num(pd7, 2, True) if pd7 is not None else None, "d7_dir": direccion(pd7), "d7_flecha": flecha(pd7),
        "min24_txt": num(min(ult24)) if ult24 else None, "max24_txt": num(max(ult24)) if ult24 else None,
        "n24": len(ult24),
        "ultimos": [{"fecha_corta": fecha_corta(r["date"]), "valor_txt": num(r["usdt_bob"])} for r in reversed(diario[-10:])],
    }
    hace30p = en_o_antes(diario, resta_dias(ult_d, 30), "usdt_bob")
    if hace30p:
        ch = valor - hace30p["usdt_bob"]
        D["usdt"]["d30_txt"] = num(ch, 2, True)
        D["usdt"]["d30_pct_txt"] = num(ch / hace30p["usdt_bob"] * 100, 1, True)
        D["usdt"]["d30_dir"] = direccion(ch)

    # --- Brecha ---
    brecha_bs = valor - u["tco_venta_bcb"]
    brecha_pct = brecha_bs / u["tco_venta_bcb"] * 100
    venta_por_fecha = {r["date"]: r["tco_venta_bcb"] for r in tco}
    serie_brecha = []
    for r in diario:
        v = venta_por_fecha.get(r["date"])
        if v:
            serie_brecha.append([r["date"], v, round(r["usdt_bob"], 4), round((r["usdt_bob"] - v) / v * 100, 3)])
    # promedio mensual de la brecha
    por_mes = {}
    for f in serie_brecha:
        por_mes.setdefault(f[0][:7], []).append(f[3])
    meses_brecha = [{"mes": mes_anio(k + "-01").capitalize(), "pct_txt": num(sum(v) / len(v), 1)}
                    for k, v in sorted(por_mes.items())[-12:]][::-1]
    max_b = max(serie_brecha, key=lambda f: f[3]) if serie_brecha else None
    D["brecha"] = {
        "pct": brecha_pct, "pct_txt": num(brecha_pct, 1, True), "bs_txt": num(brecha_bs, 2, True),
        "dir": "sube" if brecha_pct > 0 else "baja",
        "meses": meses_brecha,
        "max_txt": num(max_b[3], 1) if max_b else None, "max_fecha": fecha_larga(max_b[0]) if max_b else None,
    }
    b7 = None
    if p7 and hace7:
        b7 = brecha_pct - ((p7["usdt_bob"] - hace7["tco_venta_bcb"]) / hace7["tco_venta_bcb"] * 100)
    D["brecha"]["d7_txt"] = num(b7, 1, True) if b7 is not None else None
    D["brecha"]["d7_dir"] = direccion(b7, 0.05)
    D["brecha"]["d7_flecha"] = flecha(b7, 0.05)

    # --- Bancos ---
    bancos = data.get("banks") or {}
    nombres = data.get("bank_names") or list(bancos)
    fechas = [s[-1]["date"] for s in bancos.values() if s]
    f_b = max(fechas) if fechas else None
    filas_b = []
    for nb in nombres:
        s = bancos.get(nb) or []
        r = next((x for x in reversed(s) if x["date"] == f_b), None)
        if r and r.get("rate") is not None:
            filas_b.append({"id": nb, "nombre": NOMBRE_BANCO.get(nb, nb), "tasa": r["rate"],
                            "monto": r.get("monto"), "n": r.get("n"), "pequeno": nb in BANCOS_PEQUENOS})
    agg = data.get("aggregates") or {}
    ppp_s = next((x for x in reversed(agg.get("Bancos (promedio ponderado)", [])) if x["date"] == f_b), None)
    monto_s = next((x for x in reversed(agg.get("Bancos (montos totales)", [])) if x["date"] == f_b), None)
    n_s = next((x for x in reversed(agg.get("Bancos (numero de transacciones)", [])) if x["date"] == f_b), None)
    ppp = ppp_s["rate"] if ppp_s else None
    total_m = sum(f["monto"] or 0 for f in filas_b)
    for f in filas_b:
        f["tasa_txt"] = num(f["tasa"])
        f["vs_txt"] = num(f["tasa"] - ppp, 2, True) if ppp else "—"
        f["vs_dir"] = direccion(f["tasa"] - ppp, 0.005) if ppp else "igual"
        f["monto_txt"] = num(f["monto"], 0) if f["monto"] is not None else "—"
        f["n_txt"] = num(f["n"], 0) if f["n"] is not None else "—"
        f["part_txt"] = num(f["monto"] / total_m * 100, 1) if (f["monto"] and total_m) else "—"
    filas_b.sort(key=lambda f: -f["tasa"])
    relevantes = [f for f in filas_b if not f["pequeno"] and (f["monto"] or 0) >= 0.002 * total_m]
    D["bancos"] = {
        "fecha": f_b, "fecha_larga": fecha_larga(f_b) if f_b else None, "fecha_corta": fecha_corta(f_b) if f_b else None,
        "filas": filas_b, "n_bancos": len(filas_b),
        "ppp": ppp, "ppp_txt": num(ppp), "monto_txt": num(monto_s["monto"] / 1e6, 1) if monto_s else None,
        "n_txt": num(n_s["n"], 0) if n_s else None,
        "mejor": relevantes[0] if relevantes else None, "peor": relevantes[-1] if relevantes else None,
        "top": relevantes[:5],
    }
    if relevantes:
        D["bancos"]["dispersion_txt"] = num(relevantes[0]["tasa"] - relevantes[-1]["tasa"])

    # --- Reservas ---
    res = sorted([r for r in data["reservas"] if r.get("neta") is not None], key=lambda r: r["date"])
    ur = res[-1]
    r12 = en_o_antes(res, (date.fromisoformat(ur["date"]) - timedelta(days=365)).isoformat(), "neta")
    comp = {k: ur.get(k) for k in ("oro", "divisas", "deg", "fmi")}
    tot = sum(v for v in comp.values() if v)
    D["reservas"] = {
        "fecha": ur["date"], "fecha_larga": fecha_larga(ur["date"]),
        "rin": ur["neta"], "rin_txt": num(ur["neta"], 0),
        "netas_obl_txt": num(ur.get("netas_obligaciones"), 0) if ur.get("netas_obligaciones") is not None else None,
        "comp": [{"nombre": n, "valor_txt": num(comp[k], 0), "pct_txt": num(comp[k] / tot * 100, 1)}
                 for k, n in (("oro", "Oro"), ("divisas", "Divisas"), ("deg", "Derechos especiales de giro (DEG)"), ("fmi", "Tramo de reserva en el FMI")) if comp.get(k) is not None],
        "oro_pct_txt": num((comp.get("oro") or 0) / tot * 100, 0) if tot else None,
        "divisas_txt": num(comp.get("divisas"), 0),
    }
    if r12:
        ch = ur["neta"] - r12["neta"]
        D["reservas"].update({"d12_txt": num(ch, 0, True), "d12_pct_txt": num(ch / r12["neta"] * 100, 1, True),
                              "d12_dir": direccion(ch, 0.5), "fecha12_larga": fecha_larga(r12["date"])})
    pico = max(res, key=lambda r: r["neta"])
    D["reservas"]["pico_txt"] = num(pico["neta"], 0)
    D["reservas"]["pico_fecha"] = mes_anio(pico["date"])

    # --- Balanza cambiaria ---
    bal = sorted([r for r in data["balanza"] if r.get("flujo") is not None], key=lambda r: r["date"])
    ub = bal[-1]
    ult12 = bal[-12:]
    suma12 = sum(r["flujo"] for r in ult12)
    D["balanza"] = {
        "mes": mes_anio(ub["date"]), "fecha": ub["date"],
        "flujo": ub["flujo"], "flujo_txt": num(ub["flujo"], 0, True),
        "ingreso_txt": num(ub.get("ingreso"), 0), "egreso_txt": num(ub.get("egreso"), 0),
        "dir": "sube" if ub["flujo"] >= 0 else "baja",
        "suma12_txt": num(suma12, 0, True), "suma12_dir": "sube" if suma12 >= 0 else "baja",
        "superavit": ub["flujo"] >= 0,
        "ultimos": [{"mes": mes_anio(r["date"]).capitalize(), "ingreso_txt": num(r.get("ingreso"), 0),
                     "egreso_txt": num(r.get("egreso"), 0), "flujo_txt": num(r["flujo"], 0, True),
                     "dir": "sube" if r["flujo"] >= 0 else "baja"} for r in reversed(bal[-12:])],
    }

    # --- ITCR ---
    it = sorted([r for r in data["itcr"] if r.get("value") is not None], key=lambda r: r["date"])
    ui = it[-1]
    mx = max(it, key=lambda r: r["value"])
    hace12 = en_o_antes(it, (date.fromisoformat(ui["date"]) - timedelta(days=365)).isoformat(), "value")
    D["itcr"] = {
        "fecha": ui["date"], "mes": mes_anio(ui["date"]), "valor_txt": num(ui["value"], 1), "vs_base_txt": num(ui["value"] - 100, 1, True),
        "max_txt": num(mx["value"], 1), "max_mes": mes_anio(mx["date"]),
        "d12_txt": num((ui["value"] / hace12["value"] - 1) * 100, 1, True) if hace12 else None,
    }

    # --- Noticias ---
    # Solo titulares con fecha y de los últimos 7 días: un titular viejo con
    # una cotización que ya no rige confunde más de lo que informa. Si no hay
    # ninguno reciente, la sección no se muestra.
    items = []
    ahora_utc = datetime.now(timezone.utc)
    for it_n in (noticias or {}).get("items", [])[:6]:
        pub = it_n.get("published")
        if not (it_n.get("title") and it_n.get("url", "").startswith("http") and pub):
            continue
        t_pub = datetime.strptime(pub, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        dias = (ahora_utc.astimezone(BOLIVIA).date() - t_pub.astimezone(BOLIVIA).date()).days
        if dias > 7:
            continue
        cuando = "hoy" if dias <= 0 else ("ayer" if dias == 1 else f"hace {dias} días")
        items.append({"titulo": it_n["title"], "url": it_n["url"], "medio": (it_n.get("source") or "").strip(" |-·"),
                      "cuando": cuando})
    D["noticias"] = {"items": items, "fecha_larga": fecha_larga(noticias["updated"]) if noticias and noticias.get("updated") else None}

    # --- Frescura ---
    fr = (estado or {}).get("frescura", {})
    D["atrasado"] = {k: bool(v.get("atrasado")) for k, v in fr.items()}

    # --- Momento de la construcción ---
    ahora = datetime.now(BOLIVIA)
    D["generado"] = {"iso": ahora.isoformat(timespec="minutes"), "fecha_larga": fecha_larga(ahora.date().isoformat()),
                     "hora": ahora.strftime("%H:%M"), "fecha": ahora.date().isoformat()}
    return D


DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
DIAS_C = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]


def dia_txt(iso, corto=False):
    d = date.fromisoformat(iso[:10])
    if corto:
        return f"{DIAS_C[d.weekday()]} {d.day} {MESES_C[d.month - 1]}"
    return f"{DIAS[d.weekday()]} {d.day}"


def centavos_txt(delta):
    """0,04 -> '4 centavos'; 1,25 -> 'Bs 1,25'."""
    c = round(abs(delta) * 100)
    if c == 0:
        return "nada"
    if c < 100:
        return f"{c} centavo" + ("s" if c != 1 else "")
    return f"Bs {num(abs(delta))}"


def enriquecer(D, data):
    """Todo lo que hace la portada más humana: comparación contra ayer, titular
    del día por reglas fijas, el oficial de mañana, 'hace un año' y el podio de
    bancos en plata concreta. Las cifras salen de los mismos datos; solo cambia
    cómo se cuentan."""
    hoy = D["generado"]["fecha"]
    diario = sorted(data["usdt"], key=lambda r: r["date"])
    tco = sorted([r for r in data["tco"] if r.get("tco_venta_bcb") is not None], key=lambda r: r["date"])
    u, t = D["usdt"], D["tco"]

    # Paralelo contra el cierre del día anterior
    previo = next((r for r in reversed(diario) if r["date"] < u["fecha"]), None)
    if previo:
        dlt = u["valor"] - previo["usdt_bob"]
        pct = dlt / previo["usdt_bob"] * 100
        u["ayer"] = {"valor_txt": num(previo["usdt_bob"]), "fecha": previo["date"], "delta": dlt, "pct": pct,
                     "dir": direccion(dlt, 0.005), "flecha": flecha(dlt, 0.005),
                     "texto": ("Sin cambios desde ayer" if abs(dlt) < 0.005 else
                               f"{'Sube' if dlt > 0 else 'Baja'} {centavos_txt(dlt)} desde ayer")}
    # Oficial contra el valor vigente el día anterior
    if len(tco) > 1:
        prev = tco[-2]
        dlt = t["venta"] - prev["tco_venta_bcb"]
        t["ayer"] = {"delta": dlt, "dir": direccion(dlt, 0.005), "flecha": flecha(dlt, 0.005),
                     "texto": ("igual que el día anterior" if abs(dlt) < 0.005 else
                               f"{'sube' if dlt > 0 else 'baja'} {centavos_txt(dlt)}")}
    # ¿Ya salió el oficial del próximo día hábil? (el BCB lo publica a las 23:30)
    t["es_de_manana"] = t["fecha"] > hoy
    t["dia_txt"] = dia_txt(t["fecha"])

    # Máximos y mínimos del mes
    ult30 = [r["usdt_bob"] for r in diario if r["date"] >= resta_dias(u["fecha"], 30) and r["date"] < u["fecha"]]
    record = None
    if ult30:
        if u["valor"] > max(ult30) + 0.004:
            record = "max"
        elif u["valor"] < min(ult30) - 0.004:
            record = "min"

    # Titular del día con reglas fijas (no hay texto inventado: solo umbrales)
    pct = u.get("ayer", {}).get("pct", 0.0)
    dlt = u.get("ayer", {}).get("delta", 0.0)
    v = u["valor_txt"]
    if record == "max":
        tit = f"El paralelo toca su precio más alto del mes: Bs {v}"
    elif record == "min":
        tit = f"El paralelo toca su precio más bajo del mes: Bs {v}"
    elif abs(pct) < 0.5:
        tit = f"El paralelo sigue quieto: Bs {v}" if abs(dlt) >= 0.005 else f"El paralelo no se mueve: Bs {v}"
    elif abs(pct) <= 2:
        tit = f"El paralelo {'sube' if dlt > 0 else 'baja'} {centavos_txt(dlt)} hoy: Bs {v}"
    else:
        tit = f"Fuerte {'subida' if dlt > 0 else 'baja'} del paralelo: Bs {v} ({num(pct, 1, True)}% hoy)"
    brecha_bs = u["valor"] - t["venta"]
    if abs(D["brecha"]["pct"]) < 0.5:
        sub = f"Oficial y paralelo casi iguales: {centavos_txt(brecha_bs)} de diferencia."
    elif brecha_bs > 0:
        sub = f"En el paralelo pagas {centavos_txt(brecha_bs)} más por dólar que al oficial (Bs {t['venta_txt']}). En $us 1.000 son Bs {num(brecha_bs * 1000, 0)}."
    else:
        sub = f"Hoy el paralelo está {centavos_txt(brecha_bs)} por debajo del oficial (Bs {t['venta_txt']})."
    D["titular"] = {"texto": tit, "corto": tit.split(": Bs")[0], "sub": sub, "record": record}

    # Hace un año
    hace1 = en_o_antes(diario, resta_dias(u["fecha"], 365), "usdt_bob")
    if hace1:
        tv = en_o_antes(tco, hace1["date"], "tco_venta_bcb")
        D["hace_un_anio"] = {
            "fecha_larga": fecha_larga(hace1["date"]), "paralelo_txt": num(hace1["usdt_bob"]),
            "oficial_txt": num(tv["tco_venta_bcb"]) if tv else None,
            "brecha_txt": num((hace1["usdt_bob"] / tv["tco_venta_bcb"] - 1) * 100, 0) if tv else None,
            "cambio_txt": num((u["valor"] / hace1["usdt_bob"] - 1) * 100, 0, True),
        }
    else:
        D["hace_un_anio"] = None

    # Bancos: motivo de exclusión y podio "¿dónde vender?"
    b = D["bancos"]
    total = sum(f["monto"] or 0 for f in b["filas"])
    for f in b["filas"]:
        motivo = None
        if f["pequeno"]:
            motivo = "banco PyME con pocas operaciones"
        elif total and (f["monto"] or 0) < 0.002 * total:
            motivo = "compró muy poco ese día"
        f["motivo"] = motivo
        f["relevante"] = motivo is None
    b["podio"] = [{"nombre": f["nombre"], "tasa": f["tasa"], "tasa_txt": f["tasa_txt"],
                   "recibe_txt": num(f["tasa"] * 500, 0)} for f in b["top"][:3]]
    if len(b["top"]) >= 2:
        b["dif500_txt"] = num((b["top"][0]["tasa"] - b["top"][-1]["tasa"]) * 500, 0)
    b["dia_txt"] = dia_txt(b["fecha"]) if b["fecha"] else None

    # Texto para compartir
    flecha_u = u.get("ayer", {}).get("flecha", "")
    D["compartir"] = {
        "texto": f"Dólar hoy ({dia_txt(u['fecha'], True)}, {u['hora']}): paralelo Bs {v} {flecha_u if flecha_u != '=' else ''}/ oficial Bs {t['venta_txt']}."
                 + (f" ¿Dónde vender? {b['top'][0]['nombre']} pagó Bs {b['top'][0]['tasa_txt']}." if b["top"] else ""),
        "param": "?d=" + u["fecha"].replace("-", "") + u["hora"].replace(":", ""),
    }
    return D


def resumenes_mensuales(data):
    """Un resumen por mes con datos reales (máximo, mínimo, recorrido del
    oficial, brecha promedio y banco que más pagó). Da una fecha fija de
    regreso (el inicio de cada mes) y apunta a búsquedas como
    'dólar octubre 2026 Bolivia'."""
    diario = sorted(data["usdt"], key=lambda r: r["date"])
    tco = {r["date"]: r["tco_venta_bcb"] for r in data["tco"] if r.get("tco_venta_bcb") is not None}
    meses_disp = sorted({r["date"][:7] for r in diario if r["date"] >= "2024-06"})
    bancos = data.get("banks") or {}
    salida = []
    for ym in meses_disp:
        y, mth = int(ym[:4]), int(ym[5:7])
        nombre = f"{MESES[mth - 1]} de {y}"
        filas = [r for r in diario if r["date"].startswith(ym)]
        if len(filas) < 3:
            continue
        ini, fin = filas[0], filas[-1]
        mx = max(filas, key=lambda r: r["usdt_bob"])
        mn = min(filas, key=lambda r: r["usdt_bob"])
        cambio = (fin["usdt_bob"] / ini["usdt_bob"] - 1) * 100
        of = [(r["date"], tco[r["date"]]) for r in filas if r["date"] in tco]
        brechas = [(r["usdt_bob"] / tco[r["date"]] - 1) * 100 for r in filas if r["date"] in tco]
        # Banco que más pagó en el mes (promedio ponderado por monto, solo bancos con volumen)
        acum = {}
        for nb, serie in bancos.items():
            for r in serie:
                if r["date"].startswith(ym) and r.get("rate") and r.get("monto"):
                    a = acum.setdefault(nb, [0.0, 0.0])
                    a[0] += r["rate"] * r["monto"]
                    a[1] += r["monto"]
        total_m = sum(a[1] for a in acum.values())
        candidatos = [(nb, a[0] / a[1], a[1]) for nb, a in acum.items()
                      if a[1] >= 0.002 * total_m and nb not in BANCOS_PEQUENOS] if total_m else []
        mejor = max(candidatos, key=lambda c: c[1]) if candidatos else None
        verbo = "subió" if cambio > 0.25 else ("bajó" if cambio < -0.25 else "casi no se movió")
        titular = (f"En {nombre} el paralelo {verbo}" +
                   (f" {num(abs(cambio), 1)}%: de Bs {num(ini['usdt_bob'])} a Bs {num(fin['usdt_bob'])}" if verbo != "casi no se movió" else f": cerró en Bs {num(fin['usdt_bob'])}"))
        slug = f"{MESES[mth - 1]}-{y}"
        salida.append({
            "ym": ym, "nombre": nombre, "slug": slug, "ruta": f"/dolar-bolivia/{slug}/",
            "titular": titular, "cambio_txt": num(cambio, 1, True), "cambio_dir": direccion(cambio, 0.25),
            "ini_txt": num(ini["usdt_bob"]), "fin_txt": num(fin["usdt_bob"]), "fin_fecha": fecha_larga(fin["date"]),
            "max_txt": num(mx["usdt_bob"]), "max_fecha": fecha_larga(mx["date"]),
            "min_txt": num(mn["usdt_bob"]), "min_fecha": fecha_larga(mn["date"]),
            "of_ini_txt": num(of[0][1]) if of else None, "of_fin_txt": num(of[-1][1]) if of else None,
            "brecha_prom_txt": num(sum(brechas) / len(brechas), 1) if brechas else None,
            "mejor_banco": {"nombre": NOMBRE_BANCO.get(mejor[0], mejor[0]), "ppp_txt": num(mejor[1])} if mejor else None,
            "referencial": "2025-12" <= ym <= "2026-06",
            "dias": [{"fecha_corta": fecha_corta(r["date"]), "paralelo_txt": num(r["usdt_bob"]),
                      "oficial_txt": num(tco[r["date"]]) if r["date"] in tco else "—",
                      "brecha_txt": (num((r["usdt_bob"] / tco[r["date"]] - 1) * 100, 1) + "%") if r["date"] in tco else "—"}
                     for r in reversed(filas)],
            "ultimo_dia": fin["date"],
        })
    salida.reverse()  # más reciente primero
    for i, m in enumerate(salida):
        m["siguiente"] = salida[i - 1] if i > 0 else None
        m["anterior"] = salida[i + 1] if i + 1 < len(salida) else None
    if salida and salida[0]["ym"] == datetime.now(BOLIVIA).strftime("%Y-%m"):
        salida[0]["en_curso"] = True
        salida[0]["titular"] = salida[0]["titular"].replace("En ", "En lo que va de ", 1).replace(" de Bs ", " desde Bs ", 1).replace(" a Bs ", " hasta Bs ", 1)
    return salida


def series_para_graficos(data):
    """Archivos de datos chicos, uno por gráfico (en vez de 389 KB para todo)."""
    tco = sorted([r for r in data["tco"] if r.get("tco_venta_bcb") is not None], key=lambda r: r["date"])
    diario = sorted(data["usdt"], key=lambda r: r["date"])
    intra = sorted(data.get("usdt_intraday_recent") or [], key=lambda p: p["ts"])
    venta = {r["date"]: r["tco_venta_bcb"] for r in tco}
    brecha = [[r["date"], venta[r["date"]], round(r["usdt_bob"], 4),
               round((r["usdt_bob"] - venta[r["date"]]) / venta[r["date"]] * 100, 3)]
              for r in diario if r["date"] in venta]
    res = sorted([r for r in data["reservas"] if r.get("neta") is not None], key=lambda r: r["date"])
    r2 = lambda v: None if v is None else round(v, 2)  # noqa: E731
    return {
        "tco": {"filas": [[r["date"], r.get("tco_compra_bcb"), r["tco_venta_bcb"]] for r in tco], "tramos": [TRAMO_REFERENCIAL]},
        "usdt": {"diario": [[r["date"], round(r["usdt_bob"], 4)] for r in diario], "intradia": [[p["ts"], p["value"]] for p in intra]},
        "brecha": {"filas": brecha, "tramos": [TRAMO_REFERENCIAL]},
        "reservas": {"filas": [[r["date"], r2(r.get("neta")), r2(r.get("netas_obligaciones")), r2(r.get("divisas")), r2(r.get("oro")), r2(r.get("deg")), r2(r.get("fmi"))] for r in res],
                     "columnas": ["fecha", "rin", "rin_netas_obligaciones", "divisas", "oro", "deg", "fmi"], "unidad": "millones de USD"},
        "balanza": {"filas": [[r["date"], r2(r.get("ingreso")), r2(r.get("egreso")), r2(r.get("flujo"))] for r in sorted(data["balanza"], key=lambda r: r["date"])],
                    "columnas": ["fecha", "ingreso", "egreso", "flujo"], "unidad": "millones de USD"},
        "itcr": {"filas": [[r["date"], round(r["value"], 3)] for r in sorted(data["itcr"], key=lambda r: r["date"]) if r.get("value") is not None],
                 "base": "diciembre de 2022 = 100"},
        "bancos": {"banks": data.get("banks", {}), "bank_names": data.get("bank_names", []), "aggregates": data.get("aggregates", {})},
    }


# ---------------------------------------------------------------------------
# Contenido (Markdown con encabezado YAML; el cuerpo admite variables {{ D.* }})
# ---------------------------------------------------------------------------

def leer_md(ruta):
    txt = ruta.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", txt, re.S)
    if not m:
        raise ValueError(f"{ruta}: falta el encabezado YAML entre líneas '---'")
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, m.group(2)


def md_a_html(texto):
    return markdown.markdown(texto, extensions=["tables", "smarty", "sane_lists", "attr_list", "toc", "md_in_html"],
                             extension_configs={"smarty": {"substitutions": {
                                 "left-double-quote": "“", "right-double-quote": "”",
                                 "left-single-quote": "‘", "right-single-quote": "’"}}})


def palabras(html_txt):
    return len(re.sub(r"<[^>]+>", " ", html_txt).split())


# ---------------------------------------------------------------------------
# Construcción
# ---------------------------------------------------------------------------

class Sitio:
    def __init__(self, cfg, entorno, base, salida, D, series):
        self.cfg, self.entorno, self.base, self.salida, self.D, self.series = cfg, entorno, base, salida, D, series
        self.produccion = entorno == "produccion"
        self.paginas = []  # para el sitemap
        self.env = Environment(loader=FileSystemLoader(str(SITIO / "plantillas")),
                               autoescape=select_autoescape(["html", "xml"]),
                               undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
        self.env.filters["num"] = num
        self.env.filters["fecha_larga"] = fecha_larga
        self.env.filters["fecha_corta"] = fecha_corta
        self.env.globals.update(url=self.url, abs_url=self.abs_url, estatico=self.estatico)
        self.versiones = {}

    # rutas
    def url(self, ruta):
        return self.base + ruta

    def abs_url(self, ruta):
        return self.cfg["dominio"].rstrip("/") + ruta

    def estatico(self, ruta):
        """URL de un archivo estático con su huella (?v=...) para renovar la caché al cambiar."""
        if ruta not in self.versiones:
            p = SITIO / "estaticos" / ruta.lstrip("/")
            self.versiones[ruta] = hashlib.sha256(p.read_bytes()).hexdigest()[:10] if p.exists() else "0"
        return self.base + ruta + "?v=" + self.versiones[ruta]

    def csp(self):
        ads = self.produccion and self.cfg["adsense"]["activo"] and self.cfg["adsense"]["id_editor"]
        if ads:
            # AdSense carga scripts y marcos desde muchos dominios de Google que
            # cambian sin aviso; una lista cerrada termina bloqueando anuncios
            # (= ingresos perdidos). Con anuncios activos se mantienen solo las
            # reglas que no interfieren. Ver DECISIONES.md.
            return "object-src 'none'; base-uri 'self'; upgrade-insecure-requests"
        script, connect, img = ["'self'"], ["'self'"], ["'self'", "data:"]
        prov = self.cfg["analitica"]["proveedor"] if self.produccion else ""
        if prov == "ga4":
            script.append("https://www.googletagmanager.com")
            connect += ["https://*.google-analytics.com", "https://*.analytics.google.com", "https://*.googletagmanager.com"]
            img += ["https://*.google-analytics.com", "https://*.googletagmanager.com"]
        elif prov == "cloudflare":
            script.append("https://static.cloudflareinsights.com")
            connect.append("https://cloudflareinsights.com")
        elif prov == "plausible":
            script.append("https://plausible.io")
            connect.append("https://plausible.io")
        form = ["'self'"]
        acc = self.cfg["suscripcion"]["formulario_accion"]
        if acc.startswith("https://"):
            form.append("https://" + acc.split("/")[2])
        return ("default-src 'self'; script-src " + " ".join(script) + "; style-src 'self' 'unsafe-inline'; "
                "img-src " + " ".join(img) + "; font-src 'self'; connect-src " + " ".join(connect) + "; "
                "form-action " + " ".join(form) + "; frame-src 'none'; object-src 'none'; base-uri 'self'; "
                "upgrade-insecure-requests")

    def contexto_base(self):
        c = self.cfg
        return {
            "S": c, "D": self.D, "produccion": self.produccion, "entorno": self.entorno, "base": self.base,
            "indexable": self.produccion, "csp": self.csp(),
            "anuncios_activos": bool(self.produccion and c["adsense"]["activo"] and c["adsense"]["id_editor"]),
            "analitica": c["analitica"] if self.produccion and c["analitica"]["proveedor"] and c["analitica"]["id"] else None,
            "anio": datetime.now(BOLIVIA).year,
        }

    def escribir(self, ruta, contenido, binario=False):
        destino = self.salida / ruta.lstrip("/")
        if ruta.endswith("/"):
            destino = destino / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        if binario:
            destino.write_bytes(contenido)
        else:
            destino.write_text(contenido, encoding="utf-8")

    def pagina(self, ruta, plantilla, meta, extra=None, sitemap=True, cambia="daily", prioridad=0.6, lastmod=None):
        ctx = self.contexto_base()
        ctx.update({"ruta": ruta, "M": meta, "canonical": self.abs_url(ruta)})
        if extra:
            ctx.update(extra)
        html_txt = self.env.get_template(plantilla).render(**ctx)
        self.escribir(ruta, html_txt)
        if sitemap:
            self.paginas.append({"loc": self.abs_url(ruta), "lastmod": lastmod or self.D["generado"]["fecha"],
                                 "changefreq": cambia, "priority": prioridad})
        return html_txt

    def render_cuerpo(self, cuerpo):
        """El Markdown puede usar variables con datos del día, p. ej. {{ D.usdt.valor_txt }}."""
        t = self.env.from_string(cuerpo)
        return md_a_html(t.render(D=self.D, S=self.cfg, url=self.url))


def generar_og(sitio, clave, titulo, cifra=None, sub=None):
    """Imagen de 1200x630 para la vista previa al compartir (WhatsApp, redes)."""
    from PIL import Image, ImageDraw, ImageFont
    f = RAIZ / "herramientas" / "fuentes-og"
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), (10, 10, 10))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, H - 14, W, H], fill=(42, 120, 214))
    mono = ImageFont.truetype(str(f / "Archivo-SemiBold.ttf"), 30)
    dr.text((70, 62), "PULSO ECONÓMICO · BOLIVIA", font=mono, fill=(227, 169, 0))

    def ajustar(txt, fuente, ancho):
        lineas, act = [], ""
        for p in txt.split():
            prueba = (act + " " + p).strip()
            if dr.textlength(prueba, font=fuente) <= ancho:
                act = prueba
            else:
                lineas.append(act)
                act = p
        lineas.append(act)
        return lineas

    tam = 64 if cifra else 74
    tit = ImageFont.truetype(str(f / "Archivo-ExtraBold.ttf"), tam)
    y = 130
    for ln in ajustar(titulo, tit, W - 140)[:3]:
        dr.text((70, y), ln, font=tit, fill=(255, 255, 255))
        y += int(tam * 1.12)
    if cifra:
        big = ImageFont.truetype(str(f / "Archivo-ExtraBold.ttf"), 150)
        dr.text((66, max(y + 20, 330)), cifra, font=big, fill=(255, 255, 255))
    if sub:
        s = ImageFont.truetype(str(f / "Archivo-Regular.ttf"), 32)
        dr.text((70, H - 86), sub, font=s, fill=(200, 200, 200))
    ruta = sitio.salida / "img" / "og" / f"{clave}.png"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    im.save(ruta, optimize=True)
    return f"/img/og/{clave}.png"


def generar_hoy(sitio, D):
    """'El dólar de hoy' como imagen para mandar por WhatsApp o subir a estados:
    cuadrada (1080x1350) y vertical (1080x1920). Se regenera en cada corrida."""
    from PIL import Image, ImageDraw, ImageFont
    f = RAIZ / "herramientas" / "fuentes-og"
    F = lambda n, t: ImageFont.truetype(str(f / n), t)  # noqa: E731
    u, t, b = D["usdt"], D["tco"], D["bancos"]
    for nombre, (W, H) in (("hoy-cuadrado", (1080, 1350)), ("hoy-estado", (1080, 1920))):
        im = Image.new("RGB", (W, H), (10, 10, 10))
        dr = ImageDraw.Draw(im)
        x = 80
        y = 110 if H == 1350 else 260
        dr.text((x, y), "DÓLAR HOY EN BOLIVIA", font=F("Archivo-SemiBold.ttf", 40), fill=(227, 169, 0))
        y += 70
        dr.text((x, y), f"{dia_txt(u['fecha']).capitalize()} de {MESES[int(u['fecha'][5:7]) - 1]} · {u['hora']}", font=F("Archivo-Regular.ttf", 40), fill=(200, 200, 200))
        y += 120
        dr.text((x, y), "Paralelo (USDT)", font=F("Archivo-SemiBold.ttf", 46), fill=(240, 122, 69))
        y += 60
        dr.text((x - 6, y), f"Bs {u['valor_txt']}", font=F("Archivo-ExtraBold.ttf", 210), fill=(255, 255, 255))
        y += 250
        ay = u.get("ayer")
        if ay:
            col = {"sube": (255, 123, 114), "baja": (53, 195, 90), "igual": (200, 200, 200)}[ay["dir"]]
            dr.text((x, y), ay["texto"], font=F("Archivo-SemiBold.ttf", 44), fill=col)
            y += 110
        dr.line([(x, y), (W - x, y)], fill=(70, 70, 70), width=3)
        y += 50
        dr.text((x, y), "Oficial BCB", font=F("Archivo-SemiBold.ttf", 46), fill=(75, 147, 234))
        dr.text((W - x, y), f"Bs {t['venta_txt']}", font=F("Archivo-ExtraBold.ttf", 64), fill=(255, 255, 255), anchor="ra")
        y += 110
        if b.get("podio"):
            p = b["podio"][0]
            dr.text((x, y), "Banco que más pagó", font=F("Archivo-SemiBold.ttf", 46), fill=(44, 191, 149))
            dr.text((W - x, y), f"Bs {p['tasa_txt']}", font=F("Archivo-ExtraBold.ttf", 64), fill=(255, 255, 255), anchor="ra")
            y += 64
            dr.text((x, y), f"{p['nombre']} · {b['fecha_corta']}", font=F("Archivo-Regular.ttf", 36), fill=(170, 170, 170))
        dr.rectangle([0, H - 150, W, H], fill=(42, 120, 214))
        dr.text((W // 2, H - 75), "elpulsoeconomico.com", font=F("Archivo-ExtraBold.ttf", 54), fill=(255, 255, 255), anchor="mm")
        ruta = sitio.salida / "img" / f"{nombre}.png"
        ruta.parent.mkdir(parents=True, exist_ok=True)
        im.save(ruta, optimize=True)


def generar_iconos(sitio):
    from PIL import Image, ImageDraw
    for tam, nombre in ((180, "apple-touch-icon.png"), (192, "icono-192.png"), (512, "icono-512.png")):
        im = Image.new("RGB", (tam, tam), (10, 10, 10))
        dr = ImageDraw.Draw(im)
        k = tam / 32
        pts = [(4, 18), (10, 18), (13, 9), (17, 24), (20, 14), (28, 14)]
        dr.line([(x * k, y * k) for x, y in pts], fill=(42, 120, 214), width=max(2, int(3 * k)), joint="curve")
        im.save(sitio.salida / nombre, optimize=True)


def construir(datos_dir, salida, entorno=None, base=None):
    cfg = json.loads((RAIZ / "config" / "sitio.json").read_text(encoding="utf-8"))
    entorno = entorno or os.environ.get("SITIO_ENTORNO") or cfg["entorno"]
    if entorno not in ("preview", "produccion"):
        sys.exit(f"Entorno desconocido: {entorno}")
    if base is None:
        base = "" if entorno == "produccion" else cfg["ruta_base_preview"]
    datos_dir, salida = Path(datos_dir), Path(salida)
    data = json.loads((datos_dir / "data.json").read_text(encoding="utf-8"))
    noticias = json.loads((datos_dir / "noticias.json").read_text(encoding="utf-8")) if (datos_dir / "noticias.json").exists() else None
    estado = json.loads((datos_dir / "estado.json").read_text(encoding="utf-8")) if (datos_dir / "estado.json").exists() else {}

    D = enriquecer(calcular(data, noticias, estado), data)
    series = series_para_graficos(data)

    if salida.exists():
        shutil.rmtree(salida)
    salida.mkdir(parents=True)
    shutil.copytree(SITIO / "estaticos", salida, dirs_exist_ok=True)
    s = Sitio(cfg, entorno, base, salida, D, series)

    # --- Archivos de datos para los gráficos y para terceros ---
    for nombre, contenido in series.items():
        s.escribir(f"/datos/{nombre}.json", json.dumps(contenido, ensure_ascii=False, separators=(",", ":")))
    resumen = {
        "actualizado": D["generado"]["iso"],
        "oficial": {"fecha": D["tco"]["fecha"], "compra": D["tco"]["compra"], "venta": D["tco"]["venta"], "fuente": "BCB"},
        "paralelo": {"usdt_bob": D["usdt"]["valor"], "hora_bolivia": D["usdt"]["fecha"] + " " + D["usdt"]["hora"], "fuente": "Binance P2P (mediana de 10 anuncios)"},
        "brecha_pct": round(D["brecha"]["pct"], 2),
        "bancos": {"fecha": D["bancos"]["fecha"], "promedio_ponderado": D["bancos"]["ppp"]},
        "fuente": cfg["dominio"],
    }
    s.escribir("/datos/resumen.json", json.dumps(resumen, ensure_ascii=False, indent=1))
    # Compatibilidad: la v1 publicaba estos dos archivos en la raíz.
    # Sin las series "forecast" y "garch": ningún script las actualiza y un
    # pronóstico viejo publicado como dato es un riesgo de credibilidad.
    publico = {k: v for k, v in data.items() if k not in ("forecast", "garch")}
    s.escribir("/data.json", json.dumps(publico, ensure_ascii=False, separators=(",", ":")))
    if noticias:
        s.escribir("/noticias.json", json.dumps(noticias, ensure_ascii=False, indent=2))

    # --- Imágenes para compartir ---
    sub_hoy = f"Actualizado el {D['generado']['fecha_larga']}"
    og = {
        "inicio": generar_og(s, "inicio", "Dólar hoy en Bolivia", f"Bs {D['usdt']['valor_txt']}", f"Paralelo USDT/BOB · Oficial Bs {D['tco']['venta_txt']} · {sub_hoy}"),
        "paralelo": generar_og(s, "paralelo", "Dólar paralelo en Bolivia hoy", f"Bs {D['usdt']['valor_txt']}", f"USDT/BOB, Binance P2P · {D['usdt']['hora']} · {D['usdt']['fecha_corta']}"),
        "oficial": generar_og(s, "oficial", "Tipo de cambio oficial del BCB", f"Bs {D['tco']['venta_txt']}", f"Vigente el {D['tco']['fecha_larga']}"),
        "bancos": generar_og(s, "bancos", "Tipo de cambio por banco en Bolivia", f"Bs {D['bancos']['ppp_txt']}", f"Promedio ponderado del sistema · {D['bancos']['fecha_larga']}"),
        "brecha": generar_og(s, "brecha", "Brecha cambiaria en Bolivia", f"{D['brecha']['pct_txt']}%", "Dólar paralelo frente al oficial"),
        "reservas": generar_og(s, "reservas", "Reservas internacionales del BCB", f"$us {D['reservas']['rin_txt']} MM", f"Al {D['reservas']['fecha_larga']}"),
        "balanza": generar_og(s, "balanza", "Balanza cambiaria de Bolivia", f"{D['balanza']['flujo_txt']} MM", f"Flujo neto de divisas · {D['balanza']['mes']}"),
        "itcr": generar_og(s, "itcr", "Índice de tipo de cambio real de Bolivia", D["itcr"]["valor_txt"], f"{D['itcr']['mes']} · base dic-2022 = 100"),
        "conversor": generar_og(s, "conversor", "Conversor de dólares a bolivianos", None, "Con el tipo de cambio oficial, el paralelo y el de los bancos"),
        "sitio": generar_og(s, "sitio", "Dólar, reservas y mercado cambiario de Bolivia", None, "Datos actualizados del BCB y del mercado paralelo"),
    }
    generar_iconos(s)
    generar_hoy(s, D)

    # --- Páginas de datos (texto en sitio/contenido/paginas/<clave>.md) ---
    def md_pagina(clave):
        meta, cuerpo = leer_md(SITIO / "contenido" / "paginas" / f"{clave}.md")
        for k in ("titulo", "descripcion", "dek", "og_titulo"):
            if isinstance(meta.get(k), str) and "{{" in meta[k]:
                meta[k] = s.env.from_string(meta[k]).render(D=D, S=cfg).strip()
        meta.setdefault("faq", [])
        for q in meta["faq"]:
            q["p"] = s.env.from_string(q["p"]).render(D=D, S=cfg)
            q["r_html"] = md_a_html(s.env.from_string(q["r"]).render(D=D, S=cfg, url=s.url))
            q["r_texto"] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", q["r_html"]))).strip()
        return meta, s.render_cuerpo(cuerpo)

    paginas_datos = [
        ("/", "inicio.html", "inicio", 1.0, "hourly"),
        ("/dolar-paralelo/", "paralelo.html", "paralelo", 0.9, "hourly"),
        ("/tipo-de-cambio-oficial/", "oficial.html", "oficial", 0.9, "daily"),
        ("/tipo-de-cambio-bancos/", "bancos.html", "bancos", 0.9, "daily"),
        ("/brecha-cambiaria/", "brecha.html", "brecha", 0.7, "daily"),
        ("/conversor/", "conversor.html", "conversor", 0.8, "daily"),
        ("/reservas-internacionales/", "reservas.html", "reservas", 0.7, "weekly"),
        ("/balanza-cambiaria/", "balanza.html", "balanza", 0.6, "monthly"),
        ("/tipo-de-cambio-real/", "itcr.html", "itcr", 0.5, "monthly"),
    ]

    # Artículos (se leen antes para poder enlazarlos desde las páginas de datos)
    articulos = []
    for p in sorted((SITIO / "contenido" / "articulos").glob("*.md")):
        meta, cuerpo = leer_md(p)
        meta["slug"] = meta.get("slug") or p.stem
        meta["ruta"] = f"/articulos/{meta['slug']}/"
        meta["html"] = s.render_cuerpo(cuerpo)
        meta["palabras"] = palabras(meta["html"])
        meta["minutos"] = max(1, round(meta["palabras"] / 220))
        meta["fecha_txt"] = fecha_larga(str(meta["fecha"]))
        meta["actualizado_txt"] = fecha_larga(str(meta.get("actualizado") or meta["fecha"]))
        articulos.append(meta)
    articulos.sort(key=lambda a: str(a["fecha"]), reverse=True)

    meses = resumenes_mensuales(data)
    for ruta, plantilla, clave, prio, freq in paginas_datos:
        meta, prosa = md_pagina(clave)
        meta["og"] = og.get(clave, og["sitio"])
        rel = [a for a in articulos if clave in (a.get("relacionado_con") or [])]
        s.pagina(ruta, plantilla, meta, {"prosa": prosa, "clave": clave, "articulos_rel": rel, "articulos": articulos[:4],
                                         "meses": meses}, cambia=freq, prioridad=prio)

    # --- Resúmenes mensuales ---
    s.pagina("/dolar-bolivia/", "meses.html", {
        "titulo": "El dólar en Bolivia mes a mes | Pulso Económico",
        "descripcion": "Resumen de cada mes del dólar en Bolivia desde junio de 2024: máximo, mínimo y cierre del paralelo, el oficial, la brecha y el banco que más pagó.",
        "h1": "El dólar en Bolivia, mes a mes", "dek": "Cómo cerró cada mes el paralelo, el oficial y los bancos.", "og": og["sitio"]},
        {"meses": meses}, cambia="daily", prioridad=0.6)
    for mm in meses:
        meta_m = {"titulo": f"Dólar en Bolivia: {mm['nombre']} | Pulso Económico",
                  "descripcion": f"{mm['titular']}. Máximo Bs {mm['max_txt']} ({mm['max_fecha']}), mínimo Bs {mm['min_txt']}"
                                 + (f", brecha promedio {mm['brecha_prom_txt']}%." if mm['brecha_prom_txt'] else "."),
                  "h1": f"El dólar en Bolivia en {mm['nombre']}", "dek": mm["titular"] + ".", "og": og["sitio"],
                  "titulo_corto": mm["nombre"].capitalize()}
        if len(meta_m["descripcion"]) > 160:
            meta_m["descripcion"] = meta_m["descripcion"][:157].rsplit(" ", 1)[0] + "…"
        s.pagina(mm["ruta"], "mes.html", meta_m, {"mm": mm}, cambia="daily" if mm.get("en_curso") else "monthly",
                 prioridad=0.5, lastmod=mm["ultimo_dia"])

    # --- Páginas de montos típicos (búsquedas como "100 dólares en bolivianos") ---
    for monto in (100, 500, 1000):
        ruta_m = f"/{monto}-dolares-en-bolivianos/"
        m_txt = num(monto, 0)
        meta_m = {"titulo": f"{m_txt} dólares en bolivianos hoy: Bs {num(monto * D['usdt']['valor'], 0)} | Pulso Económico",
                  "descripcion": f"{m_txt} dólares son Bs {num(monto * D['usdt']['valor'], 0)} al paralelo y Bs {num(monto * D['tco']['venta'], 0)} al oficial del BCB. Cuánto te paga cada banco por $us {m_txt}.",
                  "h1": f"{m_txt} dólares en bolivianos", "og": og["conversor"], "titulo_corto": f"$us {m_txt} en bolivianos"}
        diario = sorted(data["usdt"], key=lambda r: r["date"])[-30:]
        hist = [{"fecha_corta": fecha_corta(r["date"]), "bs_txt": num(monto * r["usdt_bob"], 0)} for r in reversed(diario)]
        s.pagina(ruta_m, "monto.html", meta_m, {"monto": monto, "m_txt": m_txt, "hist": hist}, cambia="hourly", prioridad=0.6)

    # --- Artículos ---
    meta_idx = {"titulo": "Artículos: dólar, tipo de cambio y economía de Bolivia, explicados",
                "descripcion": "Guías claras sobre el tipo de cambio oficial, el dólar paralelo, la brecha cambiaria, las reservas del BCB y cómo convertir dólares a bolivianos.",
                "h1": "Artículos", "dek": "Explicaciones claras, con datos y fuentes, sobre el mercado cambiario de Bolivia.", "og": og["sitio"]}
    s.pagina("/articulos/", "articulos.html", meta_idx, {"lista": articulos}, cambia="weekly", prioridad=0.6)
    for a in articulos:
        a["og"] = generar_og(s, "art-" + a["slug"], a["titulo_corto"] if a.get("titulo_corto") else a["h1"], None, "Pulso Económico · Artículo")
        otros = [x for x in articulos if x["slug"] != a["slug"]][:3]
        s.pagina(a["ruta"], "articulo.html", a, {"otros": otros}, cambia="monthly", prioridad=0.6,
                 lastmod=str(a.get("actualizado") or a["fecha"]))

    # --- Páginas institucionales ---
    for p in sorted((SITIO / "contenido" / "paginas" / "institucionales").glob("*.md")):
        meta, cuerpo = leer_md(p)
        meta["og"] = og["sitio"]
        meta.setdefault("faq", [])
        for q in meta["faq"]:
            q["p"] = s.env.from_string(q["p"]).render(D=D, S=cfg)
            q["r_html"] = md_a_html(s.env.from_string(q["r"]).render(D=D, S=cfg, url=s.url))
            q["r_texto"] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", q["r_html"]))).strip()
        ruta = f"/{meta.get('slug', p.stem)}/"
        s.pagina(ruta, meta.get("plantilla", "pagina.html"), meta, {"prosa": s.render_cuerpo(cuerpo)},
                 cambia="monthly", prioridad=float(meta.get("prioridad", 0.3)),
                 lastmod=str(meta.get("actualizado", D["generado"]["fecha"])))

    # --- Widget embebible ---
    s.pagina("/embed/cotizacion/", "embed.html", {"titulo": "Cotización del dólar en Bolivia — Pulso Económico", "descripcion": "Widget", "og": og["inicio"]},
             sitemap=False)

    # --- Página 404 y redirección de la URL vieja ---
    s.pagina("/404.html", "404.html", {"titulo": "Página no encontrada", "descripcion": "La página que buscas no existe.", "h1": "No encontramos esta página", "og": og["sitio"]}, sitemap=False)
    s.pagina("/cambiario/bancos.html", "redireccion.html", {"titulo": "Esta página se mudó", "descripcion": "", "destino": "/tipo-de-cambio-bancos/", "og": og["bancos"]}, sitemap=False)

    # --- sitemap.xml, robots.txt, ads.txt, manifest, cabeceras ---
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in s.paginas:
        xml.append(f"  <url><loc>{html.escape(p['loc'])}</loc><lastmod>{p['lastmod']}</lastmod>"
                   f"<changefreq>{p['changefreq']}</changefreq><priority>{p['priority']:.1f}</priority></url>")
    xml.append("</urlset>")
    s.escribir("/sitemap.xml", "\n".join(xml) + "\n")
    if s.produccion:
        robots = f"User-agent: *\nAllow: /\nDisallow: /embed/\n\nSitemap: {cfg['dominio']}/sitemap.xml\n"
    else:
        # En el preview NO se bloquea con robots.txt: si Google no puede entrar,
        # tampoco ve la etiqueta noindex. Las páginas llevan noindex.
        robots = "# Preview de Pulso Económico v2: las páginas llevan <meta name=\"robots\" content=\"noindex\">.\nUser-agent: *\nAllow: /\n"
    s.escribir("/robots.txt", robots)
    if cfg["adsense"]["id_editor"]:
        s.escribir("/ads.txt", f"google.com, {cfg['adsense']['id_editor']}, DIRECT, f08c47fec0942fa0\n")
    s.escribir("/manifest.webmanifest", json.dumps({
        "name": cfg["nombre"], "short_name": cfg["nombre_corto"], "lang": cfg["idioma"],
        "start_url": base + "/", "display": "browser", "background_color": "#0a0a0a", "theme_color": "#0a0a0a",
        "icons": [{"src": base + "/icono-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": base + "/icono-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=1))
    # Cabeceras y redirecciones para Cloudflare Pages (GitHub Pages las ignora).
    s.escribir("/_headers", "\n".join([
        "/*",
        "  Strict-Transport-Security: max-age=31536000; includeSubDomains",
        "  X-Content-Type-Options: nosniff",
        "  Referrer-Policy: strict-origin-when-cross-origin",
        "  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()",
        "  X-Frame-Options: SAMEORIGIN",
        *([] if s.produccion else ["  X-Robots-Tag: noindex"]),
        "/embed/*",
        "  ! X-Frame-Options",
        "/fuentes/*",
        "  Cache-Control: public, max-age=31536000, immutable",
        "/datos/*",
        "  Cache-Control: public, max-age=300",
        "  Access-Control-Allow-Origin: *",
        "",
    ]))
    s.escribir("/_redirects", "/cambiario/bancos.html /tipo-de-cambio-bancos/ 301\n/cambiario/ /tipo-de-cambio-bancos/ 301\n")
    s.escribir("/.nojekyll", "")

    # Informe breve para el registro de GitHub Actions
    n = sum(1 for _ in salida.rglob("*.html"))
    print(f"Sitio generado en {salida} · entorno={entorno} · base='{base}' · {n} páginas HTML · "
          f"{len(s.paginas)} URLs en el sitemap")
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datos", default="datos")
    ap.add_argument("--salida", default="_site")
    ap.add_argument("--entorno", default=None, choices=["preview", "produccion"])
    ap.add_argument("--base", default=None, help="Ruta base (p. ej. '' para probar el preview en la raíz)")
    a = ap.parse_args()
    construir(a.datos, a.salida, a.entorno, a.base)


if __name__ == "__main__":
    main()
