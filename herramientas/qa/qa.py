"""QA estático del sitio generado: JSON-LD, enlaces internos, títulos y descripciones."""
import json, re, sys
from pathlib import Path
from html.parser import HTMLParser

raiz = Path(sys.argv[1]); dominio = "https://elpulsoeconomico.com"
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links=[]; s.ld=[]; s._ld=False; s.title=None; s._t=False; s.desc=None; s.canon=None; s.h1=0; s.robots=None; s.ids=set(); s.imgs_sin_alt=0
    def handle_starttag(s,t,a):
        a=dict(a)
        if 'id' in a: s.ids.add(a['id'])
        if t=='a' and a.get('href'): s.links.append(a['href'])
        if t in('link','script') and (a.get('href') or a.get('src')): s.links.append(a.get('href') or a.get('src'))
        if t=='script' and a.get('type')=='application/ld+json': s._ld=True; s.ld.append('')
        if t=='title': s._t=True; s.title=''
        if t=='meta' and a.get('name')=='description': s.desc=a.get('content')
        if t=='meta' and a.get('name')=='robots': s.robots=a.get('content')
        if t=='link' and a.get('rel')=='canonical': s.canon=a.get('href')
        if t=='h1': s.h1+=1
        if t=='img' and 'alt' not in a: s.imgs_sin_alt+=1
    def handle_endtag(s,t):
        if t=='script': s._ld=False
        if t=='title': s._t=False
    def handle_data(s,d):
        if s._ld: s.ld[-1]+=d
        if s._t: s.title+=d

errores=[]; titulos={}; descs={}; n=0
for f in sorted(raiz.rglob('*.html')):
    rel='/'+str(f.relative_to(raiz)).replace('index.html','')
    p=P(); p.feed(f.read_text(encoding='utf-8')); n+=1
    for i,b in enumerate(p.ld):
        try: json.loads(b)
        except Exception as e: errores.append(f'{rel}: JSON-LD #{i} inválido: {e}')
    for l in p.links:
        if l.startswith(('http','mailto:','#','data:','tel:')): continue
        ruta=l.split('?')[0].split('#')[0]
        if not ruta: continue
        dest=raiz/ruta.lstrip('/')
        if ruta.endswith('/'): dest=dest/'index.html'
        if not dest.exists(): errores.append(f'{rel}: enlace roto {l}')
    if rel.startswith('/embed/') or rel in('/cambiario/bancos.html','/cambiario/','/404.html') or rel.startswith('/google'): continue
    if p.h1!=1: errores.append(f'{rel}: tiene {p.h1} H1')
    if not p.canon or not p.canon.startswith(dominio): errores.append(f'{rel}: canonical {p.canon}')
    titulos.setdefault(p.title,[]).append(rel); descs.setdefault(p.desc,[]).append(rel)
    lt=len(p.title or ''); ld_=len(p.desc or '')
    if lt>75: errores.append(f'{rel}: título largo ({lt}): {p.title}')
    if not (70<=ld_<=165): errores.append(f'{rel}: descripción de {ld_} caracteres')
    if p.imgs_sin_alt: errores.append(f'{rel}: {p.imgs_sin_alt} imágenes sin alt')
for t,v in titulos.items():
    if len(v)>1: errores.append(f'Título duplicado en {v}')
for t,v in descs.items():
    if len(v)>1: errores.append(f'Descripción duplicada en {v}')
print(f'{n} páginas revisadas. {len(errores)} observaciones.')
for e in errores: print(' -', e)
