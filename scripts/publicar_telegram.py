#!/usr/bin/env python3
"""
Publica el dólar del día en un canal de Telegram (opcional).

Solo funciona si el repositorio tiene configurados estos secretos de GitHub:
  TELEGRAM_TOKEN  -> token del bot (se obtiene con @BotFather en Telegram)
  TELEGRAM_CANAL  -> nombre del canal, por ejemplo @pulsoeconomico_bo
                    (el bot tiene que ser administrador del canal)

Mensajes, como máximo uno de cada tipo por día:
  - "manana":  el dólar de la mañana, desde las 08:00 (hora de Bolivia).
  - "oficial": el oficial del próximo día hábil, apenas el BCB lo publica (~23:30).
  - "movida":  aviso si el paralelo se mueve más de 1,5% frente al día anterior.

Se ejecuta después de generar el sitio (usa la imagen del día ya generada):
    python scripts/publicar_telegram.py --datos datos --sitio _site
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import construir as c  # noqa: E402

BOLIVIA = timezone(timedelta(hours=-4))


def enviar(token, canal, texto, imagen=None):
    base = f"https://api.telegram.org/bot{token}"
    if imagen and Path(imagen).exists():
        with open(imagen, "rb") as f:
            r = requests.post(f"{base}/sendPhoto", data={"chat_id": canal, "caption": texto, "parse_mode": "HTML"},
                              files={"photo": f}, timeout=30)
    else:
        r = requests.post(f"{base}/sendMessage", data={"chat_id": canal, "text": texto, "parse_mode": "HTML",
                                                       "disable_web_page_preview": "true"}, timeout=30)
    r.raise_for_status()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datos", default="datos")
    ap.add_argument("--sitio", default="_site")
    a = ap.parse_args()
    token, canal = os.environ.get("TELEGRAM_TOKEN"), os.environ.get("TELEGRAM_CANAL")
    if not token or not canal:
        print("Telegram no configurado (faltan los secretos TELEGRAM_TOKEN / TELEGRAM_CANAL). Nada que hacer.")
        return 0
    datos = Path(a.datos)
    data = json.loads((datos / "data.json").read_text(encoding="utf-8"))
    estado_p = datos / "estado.json"
    estado = json.loads(estado_p.read_text(encoding="utf-8")) if estado_p.exists() else {}
    enviados = estado.setdefault("telegram", {})
    D = c.enriquecer(c.calcular(data, None, estado), data)
    ahora = datetime.now(BOLIVIA)
    hoy = ahora.date().isoformat()
    u, t = D["usdt"], D["tco"]
    enlace = "https://elpulsoeconomico.com/"
    img = Path(a.sitio) / "img" / "hoy-cuadrado.png"

    pendientes = []
    if ahora.hour >= 8 and enviados.get("manana") != hoy:
        pendientes.append(("manana", f"<b>{D['titular']['texto']}</b>\n"
                                     f"Paralelo (USDT): Bs {u['valor_txt']} · {u['hora']}\n"
                                     f"Oficial BCB: Bs {t['venta_txt']}\n"
                                     f"Brecha: {D['brecha']['pct_txt']}%\n{enlace}", img))
    if t["es_de_manana"] and enviados.get("oficial") != t["fecha"]:
        pendientes.append(("oficial", f"🌙 <b>Ya salió el oficial para el {t['dia_txt']}: Bs {t['venta_txt']}</b>"
                                      + (f" ({t['ayer']['texto']})" if t.get("ayer") else "") + f"\n{enlace}tipo-de-cambio-oficial/", None))
    ay = u.get("ayer")
    if ay and abs(ay["pct"]) > 1.5 and enviados.get("movida") != hoy:
        pendientes.append(("movida", f"⚡ <b>{D['titular']['texto']}</b>\n{enlace}dolar-paralelo/", None))

    for clave, texto, imagen in pendientes:
        try:
            enviar(token, canal, texto, imagen)
            enviados[clave] = t["fecha"] if clave == "oficial" else hoy
            print(f"Telegram: enviado '{clave}'.")
        except Exception as e:  # noqa: BLE001 - un fallo de Telegram no debe frenar la publicación
            print(f"Telegram: no se pudo enviar '{clave}': {e}")
    estado_p.write_text(json.dumps(estado, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
