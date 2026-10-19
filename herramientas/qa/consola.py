"""Abre cada página en Chromium y reporta errores de consola, de JS y violaciones de CSP."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
raiz=Path(sys.argv[1]); base=sys.argv[2]
paginas=['/'+str(f.relative_to(raiz)).replace('index.html','') for f in sorted(raiz.rglob('*.html')) if 'google' not in f.name]
problemas=0
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844}, is_mobile=True)
    for ruta in paginas:
        pg=ctx.new_page(); errs=[]
        pg.on('console', lambda m: errs.append(f'{m.type}: {m.text}') if m.type in ('error','warning') else None)
        pg.on('pageerror', lambda e: errs.append(f'JS: {e}'))
        pg.goto(base+ruta, wait_until='networkidle'); pg.mouse.wheel(0,20000); pg.wait_for_timeout(1200)
        errs=[e for e in errs if 'favicon' not in e]
        if errs: problemas+=1; print(ruta, errs[:4])
        pg.close()
    b.close()
print(f'{len(paginas)} páginas abiertas; {problemas} con errores o advertencias.')
