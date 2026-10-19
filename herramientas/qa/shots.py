"""Capturas de pantalla completas (mobile y desktop) de una lista de URLs.

Uso: python3 shots.py <carpeta_salida> <nombre>=<url> [<nombre>=<url> ...]
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

VIEWPORTS = {
    "mobile": dict(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                   is_mobile=True, has_touch=True),
    "desktop": dict(viewport={"width": 1366, "height": 900}, device_scale_factor=1),
}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    pairs = [a.split("=", 1) for a in sys.argv[2:]]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vp_name, vp in VIEWPORTS.items():
            ctx = browser.new_context(reduced_motion="reduce", color_scheme="light",
                                      locale="es-BO", **vp)
            for name, url in pairs:
                page = ctx.new_page()
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto(url, wait_until="networkidle")
                page.wait_for_timeout(800)
                # Pantalla visible al abrir (lo que el usuario ve sin hacer scroll)
                page.screenshot(path=str(out / f"{name}-{vp_name}-primera-pantalla.png"))
                page.screenshot(path=str(out / f"{name}-{vp_name}-completa.png"), full_page=True)
                if errors:
                    print(f"{name} {vp_name}: errores JS: {errors}")
                page.close()
            ctx.close()
        browser.close()
    print("ok", sorted(x.name for x in out.iterdir()))


if __name__ == "__main__":
    main()
