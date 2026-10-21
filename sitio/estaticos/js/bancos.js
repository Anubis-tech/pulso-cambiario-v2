/* =========================================================================
   Herramienta interactiva de compras de dólares por banco.
   Código de la v1 (cambiario/bancos.html), con estos cambios:
   - Lee /datos/bancos.json (más liviano que el data.json completo).
   - Colores y textos desde el punto de vista de quien VENDE dólares al banco:
     un banco que paga más que el promedio del mercado aparece en verde.
     (La v1 lo mostraba desde el punto de vista del banco: "comprar más barato
     es favorable".) Ver DECISIONES.md.
   - Chart.js se sirve desde el propio sitio, no desde un CDN externo.
   ========================================================================= */
/* Los datos ya no van pegados: se leen de data.json, el mismo archivo que alimenta el home
   y que actualiza el scraper (GitHub Actions). Esta página se actualiza al mismo ritmo. */
function buildData(json){
  const banksObj = (json && json.banks) || {};
  const names = (json.bank_names && json.bank_names.length ? json.bank_names : Object.keys(banksObj));
  const banks = [], dateSet = new Set(), tmp = [];
  names.forEach(function(full){
    const ser = banksObj[full]; if (!ser) return;
    const bi = banks.push(full.replace(/^Banco\s+/,'')) - 1;
    ser.forEach(function(r){
      // Solo días con precio y monto: sin monto no se puede ponderar
      if (r.rate == null || r.monto == null || !(r.monto > 0)) return;
      dateSet.add(r.date);
      tmp.push([bi, r.date, r.rate, r.monto, r.n == null ? null : r.n]);
    });
  });
  const dates = Array.from(dateSet).sort();
  const idx = {}; dates.forEach(function(d,i){ idx[d] = i; });
  return {banks: banks, dates: dates, rows: tmp.map(function(r){ return [r[0], idx[r[1]], r[2], r[3], r[4]]; })};
}
function loadFail(msg){
  document.querySelectorAll('.reveal,.reveal-top').forEach(function(el){ el.classList.add('in-view'); });
  const el = document.getElementById('spHead');
  if (el) el.textContent = msg;
}
fetch((document.documentElement.getAttribute('data-base') || '') + '/datos/bancos.json', {cache:'no-cache'})
  .then(function(r){ if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
  .then(function(json){
    const D = buildData(json);
    if (!D.rows.length) throw new Error('sin filas con monto');
    boot(D);
  })
  .catch(function(e){
    console.error('No se pudo cargar bancos.json:', e);
    loadFail('No se pudieron cargar los datos. Recarga la página en unos minutos.');
  });

function boot(DATA){

/*LOGIC_START*/
const NAMES = {'Economico':'Económico','Union':'Unión','de Credito':'BCP','Mercantil Santa Cruz':'Mercantil BMSC','Nacional de Bolivia':'Nacional - BNB','Solidario':'SOL','de la Nacion Argentina':'Nación Argentina','PyME Ecofuturo':'Ecofuturo','PyME de la Comunidad':'Bancomunidad'};
const SHORT = {'Mercantil Santa Cruz':'BMSC','Nacional de Bolivia':'BNB','de la Nacion Argentina':'Nación Arg.','PyME de la Comunidad':'Bancomunidad','PyME Ecofuturo':'Ecofuturo','de Credito':'BCP','Solidario':'SOL','Economico':'Económico','Union':'Unión'};
const MES = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
const disp = b => NAMES[b] || b;
const shortName = b => SHORT[b] || disp(b);
// Bancos PyME o de poca relevancia: llevan † junto al nombre. Para sumar otros, agregar su nombre del CSV a esta lista.
const SMALL = new Set(['PyME Ecofuturo','PyME de la Comunidad']);
const dispF = b => disp(b)+(SMALL.has(b) ? ' †' : '');

const BANKS = DATA.banks;
const ROWS = DATA.rows.map(r => ({b:BANKS[r[0]], date:DATA.dates[r[1]], t:r[2], m:r[3], n:r[4]}));
const FIRST = DATA.dates[0];
const LAST = DATA.dates[DATA.dates.length-1];

// PPP del mercado por día (todos los bancos)
const MK = {};
(function(){
  const acc = {};
  for (const r of ROWS){ const a = acc[r.date] || (acc[r.date] = {m:0,p:0}); a.m += r.m; a.p += r.t*r.m; }
  for (const d in acc) MK[d] = acc[d].p/acc[d].m;
})();
const FIRST_N = ROWS.filter(r => r.n != null).map(r => r.date).sort()[0];

function aggregate(rows){
  let m=0,pxm=0,tsum=0,prem=0,n=0,nm=0;
  const days = new Set();
  for (const r of rows){
    m += r.m; pxm += r.t*r.m; tsum += r.t; prem += (r.t-MK[r.date])*r.m; days.add(r.date);
    if (r.n != null){ n += r.n; nm += r.m; }
  }
  return {
    m, n, days:days.size, rows:rows.length,
    ppp: m ? pxm/m : null,
    simple: rows.length ? tsum/rows.length : null,
    prima: m ? prem/m : null,
    ticket: n ? nm/n : null,
    hasN: nm > 0
  };
}
function weekKey(ds){
  const d = new Date(ds+'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() - ((d.getUTCDay()+6)%7));
  return d.toISOString().slice(0,10);
}
function addDays(ds,n){
  const d = new Date(ds+'T00:00:00Z');
  d.setUTCDate(d.getUTCDate()+n);
  return d.toISOString().slice(0,10);
}
// Rangos rápidos, calculados desde el último dato disponible (LAST)
function presetRange(k){
  const y = +LAST.slice(0,4), m = +LAST.slice(5,7);
  let r;
  if (k === 'sem') r = {from:addDays(LAST,-6),  to:LAST};
  else if (k === '15d') r = {from:addDays(LAST,-14), to:LAST};
  else if (k === '30d') r = {from:addDays(LAST,-29), to:LAST};
  else if (k === 'mes') r = {from:LAST.slice(0,8)+'01', to:LAST};
  else if (k === 'ant') r = {from:new Date(Date.UTC(y,m-2,1)).toISOString().slice(0,10), to:new Date(Date.UTC(y,m-1,0)).toISOString().slice(0,10)};
  else r = {from:FIRST, to:LAST};
  if (r.from < FIRST) r.from = FIRST;
  return r;
}

const _nf = {};
function fmt(v,d){
  const f = _nf[d] || (_nf[d] = new Intl.NumberFormat('es-BO',{minimumFractionDigits:d,maximumFractionDigits:d,useGrouping:'always'}));
  return f.format(v);
}
function fmtSigned(v,d){
  const r = +v.toFixed(d);
  if (r === 0) return fmt(0,d);
  return (r > 0 ? '+' : '−') + fmt(Math.abs(r),d);
}
function usd(v){
  if (v == null || isNaN(v)) return '—';
  const a = Math.abs(v);
  if (a >= 1e9) return fmt(v/1e6,0)+' MM';
  if (a >= 1e7) return fmt(v/1e6,1)+' MM';
  if (a >= 1e6) return fmt(v/1e6,2)+' MM';
  if (a >= 1e3) return fmt(v/1e3,0)+' mil';
  return fmt(v,0);
}
function fmtDate(ds, withYear){
  const [y,m,d] = ds.split('-');
  return (+d)+' '+MES[+m-1]+(withYear ? ' '+y : '');
}
/*LOGIC_END*/

/* ---------- Estado ---------- */
const MAXSEL = 3;
// Período inicial: "Mes en curso", salvo los primeros días del mes. Con menos de MIN_DIAS_MES
// días con datos el mes en curso dice poco (un solo punto en los gráficos), así que abre en "1 mes".
const MIN_DIAS_MES = 5;
const DIAS_MES_EN_CURSO = DATA.dates.filter(d => d.slice(0,7) === LAST.slice(0,7)).length;
const RANGO_INICIAL = DIAS_MES_EN_CURSO < MIN_DIAS_MES ? '30d' : 'mes';
const state = {from:FIRST, to:LAST, gran:'dia', range:RANGO_INICIAL, sel:new Set(), sort:{k:'m',dir:-1}};
const $ = id => document.getElementById(id);
const cssv = n => getComputedStyle(document.querySelector('#app-bancos .card') || document.documentElement).getPropertyValue(n).trim();
const MONO = "Poppins,system-ui,sans-serif";
const charts = {};

// Colores de marca por banco: los mismos del sitio Pulso Económico
const BANK_COLORS = {
  'BISA':'#F5B700','Economico':'#ED1C24','FIE':'#DF1583','Fortaleza':'#1C529C','Ganadero':'#2E7D32',
  'Mercantil Santa Cruz':'#4DB6AC','Nacional de Bolivia':'#00A651','PRODEM':'#7CB342','PyME Ecofuturo':'#F57C00',
  'PyME de la Comunidad':'#D4A017','Solidario':'#8B5CF6','Union':'#005E9E','de Credito':'#F7941D','de la Nacion Argentina':'#75AADB'
};
const bankColor = b => BANK_COLORS[b] || '#888888';
function onColor(hex){
  const h = hex.replace('#','');
  const L = (0.2126*parseInt(h.slice(0,2),16) + 0.7152*parseInt(h.slice(2,4),16) + 0.0722*parseInt(h.slice(4,6),16))/255;
  return L > 0.62 ? '#0a0a0a' : '#ffffff';
}
function alpha(hex,a){
  const h = hex.replace('#','');
  if (h.length !== 6) return hex;
  return 'rgba('+parseInt(h.slice(0,2),16)+','+parseInt(h.slice(2,4),16)+','+parseInt(h.slice(4,6),16)+','+a+')';
}

const periodRows = () => ROWS.filter(r => r.date >= state.from && r.date <= state.to);
function rankBanks(rows){
  const m = {};
  for (const r of rows) m[r.b] = (m[r.b] || 0) + r.m;
  return BANKS.filter(b => m[b]).sort((a,b) => m[b]-m[a]);
}

// Agrupación (hoy solo 'dia'; el código de semana y mes sigue disponible)
function bucketKey(ds){ return state.gran==='dia' ? ds : state.gran==='semana' ? weekKey(ds) : ds.slice(0,7); }
function bucketLabel(k){
  if (state.gran==='mes'){ const p = k.split('-'); return MES[+p[1]-1]+' '+p[0].slice(2); }
  return fmtDate(k,false);
}
function bucketTitle(k){
  if (state.gran==='mes'){ const p = k.split('-'); return MES[+p[1]-1]+' '+p[0]; }
  if (state.gran==='semana') return 'Semana del '+fmtDate(k,true);
  return fmtDate(k,true);
}
function groupBy(rows){
  const g = new Map();
  for (const r of rows){ const k = bucketKey(r.date); let a = g.get(k); if(!a){ a = []; g.set(k,a); } a.push(r); }
  return g;
}

const MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
function rangeName(){
  const mes = () => ' ('+MESES[+state.from.slice(5,7)-1]+' '+state.from.slice(0,4)+')';
  switch (state.range){
    case 'sem': return 'la última semana';
    case '15d': return 'los últimos 15 días';
    case '30d': return 'el último mes';
    case 'mes': return 'el mes en curso'+mes();
    case 'ant': return 'el mes anterior'+mes();
    default: return 'el período seleccionado';
  }
}
function joinNames(a){ return a.length < 2 ? (a[0] || '') : a.slice(0,-1).join(', ')+' y '+a[a.length-1]; }

/* ---------- Render ---------- */
function render(){
  const pr = periodRows();
  const mkt = aggregate(pr);
  const selBanks = BANKS.filter(b => state.sel.has(b));
  const sel = aggregate(pr.filter(r => state.sel.has(r.b)));
  const perSel = selBanks.map(b => { const a = aggregate(pr.filter(r => r.b === b)); a.bank = b; return a; }).filter(a => a.rows > 0);
  const marketDays = mkt.days;

  const ds = [...new Set(pr.map(r => r.date))].sort();
  const rangeTxt = ds.length ? fmtDate(ds[0],true)+' al '+fmtDate(ds[ds.length-1],true)+' · '+ds.length+' días con datos' : 'Sin datos en el período';
  $('hintRange1').textContent = rangeTxt;
  $('asof').textContent = 'Datos al '+fmtDate(LAST,true);

  const allAggs = BANKS.map(b => {
    const a = aggregate(pr.filter(r => r.b === b));
    a.bank = b;
    a.share = mkt.m ? a.m/mkt.m : 0;
    a.thin = a.share < 0.002 || a.days < 0.5*marketDays;
    return a;
  }).filter(a => a.rows > 0);

  renderChips();
  renderSpotlight(mkt, sel, perSel, allAggs, selBanks);
  renderTiles(mkt, sel);
  renderLine(pr, selBanks);
  renderBar(pr);
  renderBubble(allAggs);
  renderTable(allAggs, mkt);
}

function renderChips(){
  const el = $('chips'); el.innerHTML = '';
  const isSys = state.sel.size === 0;
  const full = state.sel.size >= MAXSEL;
  const sys = document.createElement('button');
  sys.type = 'button';
  sys.className = 'pill pill-sistema'+(isSys ? ' active' : '');
  sys.textContent = 'Sistema financiero';
  sys.setAttribute('aria-pressed', isSys ? 'true' : 'false');
  sys.addEventListener('click', () => { state.sel.clear(); render(); });
  el.appendChild(sys);
  for (const b of BANKS){
    const on = state.sel.has(b);
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'pill pill-bank'+(on ? ' active' : '');
    btn.style.setProperty('--b', bankColor(b));
    btn.style.setProperty('--on', onColor(bankColor(b)));
    btn.textContent = dispF(b);
    if (SMALL.has(b) && !btn.title) btn.title = 'PyME o banco de poca relevancia';
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    if (!on && full){ btn.disabled = true; btn.title = 'Máximo '+MAXSEL+' bancos. Quita uno para elegir otro.'; }
    btn.addEventListener('click', () => {
      if (on) state.sel.delete(b);
      else if (state.sel.size < MAXSEL) state.sel.add(b);
      render();
    });
    el.appendChild(btn);
  }
  $('chipHint').textContent = isSys
    ? 'Mostrando todo el sistema. Elige hasta '+MAXSEL+' bancos para compararlos.'
    : state.sel.size+' de '+MAXSEL+' · el sistema financiero siempre se muestra';
}

function renderSpotlight(mkt, sel, per, allAggs, selBanks){
  const isSys = state.sel.size === 0;
  const base = isSys ? mkt : sel;       // sin bancos elegidos, todo el sistema
  const rn = rangeName();

  // Titular
  let head;
  if (!mkt.rows) head = 'Sin datos en '+rn+'.';
  else if (!base.rows) head = 'Los bancos elegidos no operaron en '+rn+'.';
  else if (isSys) head = 'En '+rn+', los bancos compraron USD '+usd(mkt.m)+' a sus clientes y pagaron en promedio Bs '+fmt(mkt.ppp,2)+' por dólar (promedio ponderado por monto).';
  else {
    const names = selBanks.map(disp), one = names.length === 1;
    const d = sel.prima, r = +d.toFixed(2);
    const cmp = r === 0 ? 'igual al promedio del mercado en esos mismos días' : fmt(Math.abs(d),2)+' Bs por dólar '+(r > 0 ? 'por encima' : 'por debajo')+' del promedio del mercado en esos mismos días';
    head = 'En '+rn+', '+joinNames(names)+(one ? ' compró' : ' compraron')+' USD '+usd(sel.m)+' ('+fmt(sel.m/mkt.m*100,1)+'% del mercado) y pagó un precio promedio ponderado de Bs '+fmt(sel.ppp,2)+': '+cmp+'.';
  }
  $('spHead').textContent = head;

  // Monto y PPP
  if (!base.rows){
    $('spMonto').textContent = '—'; $('spPpp').textContent = '—'; $('spPppChip').innerHTML = '';
    $('spMontoCtx').textContent = ''; $('spPppCtx').textContent = '';
  } else {
    const u = usd(base.m), mm = u.match(/^(.*) (MM|mil)$/);
    $('spMonto').innerHTML = (mm ? mm[1] : u)+'<span class="s-unit">'+(mm ? mm[2]+' ' : '')+'USD</span>';
    $('spMontoCtx').textContent = isSys ? 'Todo el sistema financiero · '+base.days+' días con datos' : fmt(base.m/mkt.m*100,1)+'% del mercado (USD '+usd(mkt.m)+')';
    $('spPpp').innerHTML = fmt(base.ppp,2)+'<span class="s-unit">Bs/USD</span>';
    if (isSys){
      $('spPppChip').innerHTML = '';
      $('spPppCtx').textContent = 'Promedio simple: '+fmt(base.simple,2);
    } else {
      const d = sel.prima, r = +d.toFixed(2);
      $('spPppChip').innerHTML = r === 0 ? '' : '<span class="s-chip '+(r < 0 ? 'down' : 'up')+'">'+fmtSigned(d,2)+' vs mercado</span>';
      $('spPppCtx').textContent = 'Mercado del mismo día. Promedio simple: '+fmt(base.simple,2);
    }
  }

  // Más alto y más bajo
  $('spHLLbl').textContent = isSys ? 'Precio más alto y más bajo frente al mercado' : 'Precio más alto y más bajo de tu selección';
  const pool = isSys ? allAggs.filter(a => !a.thin && !SMALL.has(a.bank) && a.prima != null) : per;
  const box = $('spHL');
  if (pool.length < 2){
    box.innerHTML = '<div class="hl-note">'+(isSys ? 'Sin datos suficientes en el período.' : pool.length ? 'Elige un segundo banco para comparar.' : 'Elige 2 o 3 bancos para comparar.')+'</div>';
    $('spHLCtx').textContent = '';
    return;
  }
  // En todo el sistema se ordena por la diferencia contra el mercado en los mismos días
  // (como el resumen mensual): un precio promedio sin ajustar premia a quien compró en días caros.
  const clave = isSys ? (x => x.prima) : (x => x.ppp);
  const sorted = [...pool].sort((a,b) => clave(a) - clave(b));
  const lo = sorted[0], hi = sorted[sorted.length-1];
  const row = (k,a,cls) => '<div class="hl-row"><span class="hl-v '+cls+'">'+(isSys ? fmtSigned(a.prima,2) : fmt(a.ppp,2))+'</span><span class="hl-b">'+dispF(a.bank)+'</span><span class="hl-k">'+k+'</span></div>';
  box.innerHTML = row('paga más',hi,'good')+row('paga menos',lo,'bad');
  $('spHLCtx').textContent = isSys
    ? 'Bs por dólar frente al promedio del mercado en los mismos días. Excluye bancos PyME y con muestra delgada.'
    : 'Diferencia: '+fmt(hi.ppp-lo.ppp,2)+' Bs por USD.';
}

function renderTiles(mkt, sel){
  const isSys = state.sel.size === 0;
  const base = isSys ? mkt : sel;
  const ok = base.rows > 0;
  const tiles = [
    {l:'N° de transacciones', v: ok && base.hasN ? fmt(base.n,0) : '—', s: 'Datos desde '+fmtDate(FIRST_N,true)},
    {l:'Ticket promedio', v: ok && base.ticket ? 'USD '+usd(base.ticket) : '—', s:'Monto ÷ transacciones'},
    {l:'Participación', v: ok ? (isSys ? '100%' : fmt(base.m/mkt.m*100,1)+'%') : '—', s: isSys ? 'Todo el sistema' : 'Del monto del sistema'},
    {l:'PPP promedio simple', v: ok ? fmt(base.simple,2) : '—', s:'Sin ponderar por monto'},
    {l:'Días con datos', v: ok ? String(base.days) : '—', s: fmtDate(state.from,false)+' al '+fmtDate(state.to,false)}
  ];
  $('kpiRow').innerHTML = tiles.map(t => '<div class="kpi"><div class="label">'+t.l+'</div><div class="value">'+t.v+'</div><div class="sub">'+t.s+'</div></div>').join('');
}

function setEmpty(id, msg){
  const e = $(id); e.textContent = msg || ''; e.classList.toggle('on', !!msg);
}
function destroy(k){ if (charts[k]){ charts[k].destroy(); charts[k] = null; } }
function legendHTML(items){
  return items.map(i => {
    const st = i.dash ? 'background:repeating-linear-gradient(90deg,'+i.color+' 0 5px,transparent 5px 9px)' : 'background:'+i.color;
    return '<span class="item"><span class="swatch'+(i.line ? ' line' : '')+'" style="'+st+'"></span>'+i.label+'</span>';
  }).join('');
}
function tipStyle(){
  return {
    backgroundColor:cssv('--ink'), titleColor:cssv('--muted'), bodyColor:cssv('--surface'), footerColor:cssv('--muted'),
    titleFont:{family:MONO,size:10.5,weight:'400'}, bodyFont:{family:MONO,size:11.5}, footerFont:{family:MONO,size:10.5,weight:'400'},
    cornerRadius:8, padding:{x:10,y:7}, boxPadding:4, borderWidth:0
  };
}
// Solo 3 etiquetas en el eje X (primera, media, última), como en Pulso
function xTicksFn(n){
  const mid = Math.floor((n-1)/2);
  return function(v,i){ return (i===0 || i===mid || i===n-1) ? this.getLabelForValue(v) : ''; };
}
function axisBase(){
  return {tick:cssv('--muted'), grid:cssv('--grid')};
}

// Etiqueta al final de cada línea, con separación para que no se pisen
const endLabels = {
  id:'endLabels',
  afterDatasetsDraw(chart){
    const items = [];
    chart.data.datasets.forEach((d,di) => {
      if (!d.endLabel) return;
      const meta = chart.getDatasetMeta(di); if (meta.hidden) return;
      let li = -1; for (let i = d.data.length-1; i >= 0; i--){ if (d.data[i] != null){ li = i; break; } }
      const el = li >= 0 ? meta.data[li] : null; if (!el) return;
      items.push({x:el.x, y:el.y, t:d.endLabel, c:d.endColor});
    });
    items.sort((a,b) => a.y-b.y);
    for (let i = 1; i < items.length; i++) if (items[i].y - items[i-1].y < 13) items[i].y = items[i-1].y + 13;
    const ctx = chart.ctx; ctx.save();
    ctx.font = '500 10.5px '+MONO; ctx.textBaseline = 'middle';
    for (const it of items){
      ctx.fillStyle = it.c; ctx.fillRect(it.x+9, it.y-3, 6, 6);
      ctx.fillStyle = cssv('--ink-2'); ctx.fillText(it.t, it.x+19, it.y);
    }
    ctx.restore();
  }
};

function renderLine(pr, selBanks){
  destroy('line');
  if (!window.Chart){ setEmpty('eLine','No se pudo cargar la librería de gráficos.'); return; }
  if (!pr.length){ setEmpty('eLine','Sin datos en el período.'); $('legLine').innerHTML = ''; return; }
  setEmpty('eLine','');
  const gm = groupBy(pr);
  const keys = [...gm.keys()].sort();
  const pppOf = rows => { const g = groupBy(rows); return keys.map(k => { const a = g.get(k); return a ? aggregate(a).ppp : null; }); };
  const {tick, grid} = axisBase();
  const isSys = selBanks.length === 0;
  const accent = cssv('--accent'), avg = cssv('--avg'), surface = cssv('--surface');
  const shapes = ['circle','rectRot','triangle'];
  const lastOf = a => { for (let i = a.length-1; i >= 0; i--) if (a[i] != null) return i; return -1; };
  const mk = (label, data, color, width, dash, shape, short) => {
    const last = lastOf(data);
    return {label, data, borderColor:color, backgroundColor:color, borderWidth:width, borderDash:dash, tension:0, spanGaps:true,
      borderJoinStyle:'round', borderCapStyle:'round', pointStyle:shape,
      pointRadius:c => c.dataIndex === last ? 4 : 0, pointHoverRadius:5, pointHoverBackgroundColor:color, pointHoverBorderColor:surface, pointHoverBorderWidth:1.5,
      endLabel:short, endColor:color};
  };
  // Sistema financiero: azul sólido si está solo; gris punteado cuando se compara con bancos (como en Pulso)
  const ds = [mk('Sistema financiero', keys.map(k => aggregate(gm.get(k)).ppp), isSys ? accent : avg, isSys ? 2.25 : 1.5, isSys ? [] : [5,4], 'rect', 'Sistema')];
  const legend = [{label:'Sistema financiero', color:isSys ? accent : avg, line:true, dash:!isSys}];
  selBanks.forEach((b,i) => {
    const rows = pr.filter(r => r.b === b);
    if (!rows.length) return;
    ds.push(mk(dispF(b), pppOf(rows), bankColor(b), 2.25, [], shapes[i % 3], shortName(b)));
    legend.push({label:dispF(b), color:bankColor(b), line:true});
  });
  $('legLine').innerHTML = legendHTML(legend);
  charts.line = new Chart($('cLine'), {
    type:'line',
    data:{labels:keys.map(bucketLabel), datasets:ds},
    plugins:[endLabels],
    options:{
      responsive:true, maintainAspectRatio:false, animation:false,
      layout:{padding:{right:96, top:6}},
      interaction:{mode:'index', intersect:false},
      plugins:{
        legend:{display:false},
        tooltip:Object.assign(tipStyle(), {
          filter:i => i.parsed.y != null,
          itemSort:(a,b) => a.parsed.y - b.parsed.y,
          callbacks:{ title:i => bucketTitle(keys[i[0].dataIndex]), label:c => c.dataset.label+': '+fmt(c.parsed.y,2) }
        })
      },
      scales:{
        x:{grid:{display:false}, border:{color:grid}, ticks:{color:tick, autoSkip:false, maxRotation:0, font:{family:MONO,size:11}, callback:xTicksFn(keys.length)}},
        y:{grace:'8%', grid:{color:grid, drawTicks:false}, border:{display:false}, ticks:{color:tick, maxTicksLimit:5, padding:8, font:{family:MONO,size:11}, callback:v => fmt(v,2)}}
      }
    }
  });
}

function renderBar(pr){
  destroy('bar');
  if (!window.Chart){ setEmpty('eBar','No se pudo cargar la librería de gráficos.'); return; }
  if (!pr.length){ setEmpty('eBar','Sin datos en el período.'); $('legBar').innerHTML = ''; return; }
  setEmpty('eBar','');
  // Todo el sistema. Con color: bancos elegidos + 3 mayores del período. El resto: Otros.
  const top3 = rankBanks(pr).slice(0,3);
  const colored = BANKS.filter(b => state.sel.has(b) || top3.includes(b));
  const acc = {};
  for (const r of pr){ const k = bucketKey(r.date); const o = acc[k] || (acc[k] = {}); o[r.b] = (o[r.b] || 0) + r.m; }
  const keys = Object.keys(acc).sort();
  const others = BANKS.filter(b => !colored.includes(b));
  const otrosOf = i => others.reduce((s,b) => s + (acc[keys[i]][b] || 0), 0);
  const {tick, grid} = axisBase();
  const surface = cssv('--surface');
  const ds = colored.map(b => ({label:dispF(b), data:keys.map(k => acc[k][b] || 0), backgroundColor:bankColor(b), borderColor:surface, borderWidth:1, maxBarThickness:42}));
  const legend = colored.map(b => ({label:dispF(b), color:bankColor(b)}));
  if (keys.some((k,i) => otrosOf(i) > 0)){
    ds.push({label:'Otros', isOtros:true, data:keys.map((k,i) => otrosOf(i)), backgroundColor:cssv('--avg'), borderColor:surface, borderWidth:1, maxBarThickness:42});
    legend.push({label:'Otros', color:cssv('--avg')});
  }
  $('legBar').innerHTML = legendHTML(legend);
  const total = i => Object.values(acc[keys[i]]).reduce((s,v) => s + v, 0);
  charts.bar = new Chart($('cBar'), {
    type:'bar',
    data:{labels:keys.map(bucketLabel), datasets:ds},
    options:{
      responsive:true, maintainAspectRatio:false, animation:false,
      interaction:{mode:'index', intersect:false},
      plugins:{
        legend:{display:false},
        tooltip:Object.assign(tipStyle(), {
          filter:i => i.parsed.y > 0,
          itemSort:(a,b) => ((a.dataset.isOtros?1:0)-(b.dataset.isOtros?1:0)) || (b.parsed.y-a.parsed.y),
          callbacks:{
            title:i => bucketTitle(keys[i[0].dataIndex]),
            label:c => {
              if (!c.dataset.isOtros) return c.dataset.label+': USD '+usd(c.parsed.y);
              const rows = others.filter(b => acc[keys[c.dataIndex]][b] > 0).sort((x,y) => acc[keys[c.dataIndex]][y]-acc[keys[c.dataIndex]][x]);
              return ['Otros: USD '+usd(c.parsed.y)].concat(rows.map(b => '    '+dispF(b)+': USD '+usd(acc[keys[c.dataIndex]][b])));
            },
            footer:i => 'Total sistema: USD '+usd(total(i[0].dataIndex))
          }
        })
      },
      scales:{
        x:{stacked:true, grid:{display:false}, border:{color:grid}, ticks:{color:tick, autoSkip:false, maxRotation:0, font:{family:MONO,size:11}, callback:xTicksFn(keys.length)}},
        y:{stacked:true, beginAtZero:true, grid:{color:grid, drawTicks:false}, border:{display:false}, ticks:{color:tick, maxTicksLimit:5, padding:8, font:{family:MONO,size:11}, callback:v => usd(v)}}
      }
    }
  });
}

const labelPlugin = {
  id:'pointLabels',
  afterDatasetsDraw(chart){
    const ds = chart.data.datasets[0]; if (!ds) return;
    const meta = chart.getDatasetMeta(0), ctx = chart.ctx;
    ctx.save();
    ctx.font = '500 10.5px '+MONO; ctx.textBaseline = 'middle'; ctx.fillStyle = cssv('--ink-2');
    meta.data.forEach((el,i) => {
      const p = ds.data[i]; if (!p || !p.showLabel) return;
      const rad = (el.options && el.options.radius) || p.r || 6;
      ctx.fillText(p.label, el.x+rad+4, el.y);
    });
    ctx.restore();
  }
};

function renderBubble(aggs){
  destroy('bub');
  if (!window.Chart){ setEmpty('eBub','No se pudo cargar la librería de gráficos.'); return; }
  const pts = aggs.filter(a => a.m > 0);
  if (!pts.length){ setEmpty('eBub','Sin datos en el período.'); return; }
  setEmpty('eBub','');
  const maxN = Math.max(0, ...pts.map(a => a.n));
  const good = cssv('--good'), bad = cssv('--bad'), neutral = cssv('--avg');
  const data = pts.map(a => ({
    x:a.m, y:a.prima, r: a.n>0 && maxN>0 ? 6+18*Math.sqrt(a.n/maxN) : 5,
    label:shortName(a.bank), bank:a.bank, ppp:a.ppp, n:a.n, hasN:a.hasN, thin:a.thin,
    showLabel: !a.thin
  }));
  const col = a => a.prima > 0.005 ? good : a.prima < -0.005 ? bad : neutral;
  const {tick, grid} = axisBase();
  charts.bub = new Chart($('cBub'), {
    type:'bubble',
    data:{datasets:[{
      data,
      backgroundColor: pts.map(a => a.thin ? 'rgba(0,0,0,0)' : alpha(col(a),.5)),
      borderColor: pts.map(a => col(a)),
      borderWidth: 1.5
    }]},
    plugins:[labelPlugin],
    options:{
      responsive:true, maintainAspectRatio:false, animation:false,
      layout:{padding:{right:70}},
      plugins:{legend:{display:false}, tooltip:Object.assign(tipStyle(), {callbacks:{
        title:i => disp(i[0].raw.bank)+((i[0].raw.thin || SMALL.has(i[0].raw.bank)) ? ' †' : ''),
        label:c => {
          const r = c.raw;
          return ['Monto: USD '+usd(r.x), 'PPP: '+fmt(r.ppp,2)+' Bs', 'Diferencia vs mercado: '+fmtSigned(r.y,2)+' Bs', 'Transacciones: '+(r.hasN ? fmt(r.n,0) : 'sin dato')];
        }
      }})},
      scales:{
        x:{type:'logarithmic', grid:{color:grid, drawTicks:false}, border:{display:false}, ticks:{color:tick, padding:8, font:{family:MONO,size:11}, callback:v => { const l = Math.log10(v); return Math.abs(l-Math.round(l))<1e-9 ? usd(v) : ''; }},
           title:{display:true, text:'Monto comprado (USD, escala logarítmica)', color:tick, font:{family:MONO,size:11}}},
        y:{grace:'10%', border:{display:false}, grid:{color:ctx => ctx.tick && ctx.tick.value === 0 ? cssv('--avg') : grid, lineWidth:ctx => ctx.tick && ctx.tick.value === 0 ? 1.5 : 1, drawTicks:false},
           ticks:{color:tick, padding:8, font:{family:MONO,size:11}, callback:v => fmtSigned(v,1)},
           title:{display:true, text:'Diferencia vs mercado (Bs/USD) · arriba paga más', color:tick, font:{family:MONO,size:11}}}
      }
    }
  });
}

const COLS = [
  {k:'name',  l:'Banco'},
  {k:'m',     l:'Monto (USD)'},
  {k:'share', l:'% mercado'},
  {k:'ppp',   l:'Precio prom. (Bs)'},
  {k:'prima', l:'Vs. mercado (Bs)'},
  {k:'n',     l:'Transacciones'},
  {k:'ticket',l:'Ticket prom.'}
];
function renderTable(aggs, total){
  const t = $('tbl');
  if (!aggs.length){ t.innerHTML = '<tbody><tr><td style="text-align:left;color:var(--muted);padding:16px 0;font-family:var(--font-ui);font-weight:400">Sin datos en el período.</td></tr></tbody>'; return; }
  const {k,dir} = state.sort;
  const val = a => k==='name' ? disp(a.bank) : (a[k] == null ? -Infinity : a[k]);
  const rows = [...aggs].sort((a,b) => {
    const x = val(a), y = val(b);
    const c = (typeof x === 'string') ? x.localeCompare(y,'es') : (x<y ? -1 : x>y ? 1 : 0);
    return c*dir;
  });
  const maxM = Math.max(...rows.map(a => a.m));
  const maxAbs = Math.max(0.3, ...rows.map(a => Math.abs(a.prima)));
  let h = '<thead><tr>';
  for (const c of COLS){
    const sorted = k===c.k ? (dir===1 ? 'ascending' : 'descending') : null;
    h += '<th scope="col"'+(sorted ? ' aria-sort="'+sorted+'"' : '')+'><button type="button" data-sort="'+c.k+'">'+c.l+'</button></th>';
  }
  h += '</tr></thead><tbody>';
  for (const a of rows){
    const r = +a.prima.toFixed(2), cls = r>0 ? 'good' : r<0 ? 'bad' : '';
    const w = Math.min(48, Math.abs(a.prima)/maxAbs*48);
    const bar = r===0 ? '' : r<0 ? '<i class="r" style="right:50%;width:'+w+'px"></i>' : '<i class="g" style="left:50%;width:'+w+'px"></i>';
    h += '<tr>'
      + '<td><span class="bsw" style="background:'+bankColor(a.bank)+'"></span>'+disp(a.bank)+((a.thin || SMALL.has(a.bank)) ? ' <span class="dim" title="PyME, poca relevancia o muestra delgada">†</span>' : '')+'</td>'
      + '<td><span class="mbar"><i style="width:'+(a.m/maxM*100).toFixed(1)+'%"></i><span>'+usd(a.m)+'</span></span></td>'
      + '<td>'+fmt(a.share*100, a.share<0.01 ? 2 : 1)+'%</td>'
      + '<td>'+fmt(a.ppp,2)+'</td>'
      + '<td><span class="prima"><span class="track">'+bar+'</span><span class="num '+cls+'">'+fmtSigned(a.prima,2)+'</span></span></td>'
      + '<td class="muted">'+(a.hasN ? fmt(a.n,0) : '—')+'</td>'
      + '<td class="muted">'+(a.ticket ? usd(a.ticket) : '—')+'</td></tr>';
  }
  h += '</tbody><tfoot><tr><td>Total sistema</td><td>'+usd(total.m)+'</td><td>100%</td><td>'+fmt(total.ppp,2)+'</td><td><span class="prima"><span class="track"></span><span class="num">—</span></span></td><td class="muted">'+(total.hasN ? fmt(total.n,0) : '—')+'</td><td class="muted">'+(total.ticket ? usd(total.ticket) : '—')+'</td></tr></tfoot>';
  t.innerHTML = h;
  t.querySelectorAll('button[data-sort]').forEach(btn => btn.addEventListener('click', () => {
    const key = btn.dataset.sort;
    if (state.sort.k === key) state.sort.dir *= -1;
    else state.sort = {k:key, dir: key==='name' ? 1 : -1};
    render();
  }));
}

/* ---------- Controles ---------- */
function syncInputs(){ $('fFrom').value = state.from; $('fTo').value = state.to; }
function markRange(){
  document.querySelectorAll('#quick .pill').forEach(b => {
    const on = b.dataset.range === state.range;
    b.classList.toggle('active', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
}
function setRange(k){
  const r = presetRange(k);
  state.from = r.from; state.to = r.to; state.range = k;
  syncInputs(); markRange(); render();
}
function initReveal(){
  const els = [...document.querySelectorAll('.reveal,.reveal-top')];
  const show = e => e.classList.add('in-view');
  if (!('IntersectionObserver' in window)){ els.forEach(show); return; }
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting){ show(e.target); io.unobserve(e.target); } }), {threshold:.08});
  els.forEach(e => io.observe(e));
  setTimeout(() => els.forEach(show), 2500);   // respaldo si el observador no dispara
}
(function init(){
  const fFrom = $('fFrom'), fTo = $('fTo');
  fFrom.min = fTo.min = FIRST; fFrom.max = fTo.max = LAST;
  // Fechas manuales (ocultas hoy): si se habilitan, desmarcan el rango rápido
  fFrom.addEventListener('change', () => { state.from = fFrom.value || FIRST; state.range = null; markRange(); render(); });
  fTo.addEventListener('change', () => { state.to = fTo.value || LAST; state.range = null; markRange(); render(); });
  document.querySelectorAll('#quick .pill').forEach(b => {
    const r = presetRange(b.dataset.range);
    b.title = fmtDate(r.from,true)+' al '+fmtDate(r.to,true);
    b.addEventListener('click', () => setRange(b.dataset.range));
  });
  // Agrupación (oculta hoy)
  document.querySelectorAll('#gran .pill').forEach(b => b.addEventListener('click', () => {
    state.gran = b.dataset.gran;
    document.querySelectorAll('#gran .pill').forEach(x => { x.classList.toggle('active', x===b); x.setAttribute('aria-pressed', x===b ? 'true' : 'false'); });
    render();
  }));
  document.querySelectorAll('[data-pick]').forEach(b => b.addEventListener('click', () => {
    state.sel = new Set(b.dataset.pick==='top3' ? rankBanks(periodRows()).slice(0,MAXSEL) : []);
    render();
  }));
  $('nFrom').textContent = fmtDate(FIRST_N,true);
  const r = presetRange(state.range);
  state.from = r.from; state.to = r.to;
  syncInputs(); markRange();
  state.sel = new Set(); // por defecto: sistema financiero
  // Redibujar al cambiar el tema del visor
  if (window.matchMedia) window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', render);
  new MutationObserver(render).observe(document.documentElement, {attributes:true, attributeFilter:['data-theme']});
  render();
})();
}
