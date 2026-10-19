/* =========================================================================
   Pulso Económico v2 — utilidades comunes y motor de gráficos SVG.
   El motor de gráficos es el de la v1 (liviano, sin librerías externas), con
   tres mejoras: funciona con el dedo en el celular, permite sombrear tramos
   (por ejemplo, el período del "valor referencial" del BCB) y reserva su
   altura en el CSS para que la página no salte al dibujarse.
   ========================================================================= */
(function (global) {
  "use strict";

  var BASE = document.documentElement.getAttribute("data-base") || "";
  var fmt2 = new Intl.NumberFormat("es-BO", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var fmt1 = new Intl.NumberFormat("es-BO", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  var fmt0 = new Intl.NumberFormat("es-BO", { maximumFractionDigits: 0 });
  var MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];

  function fecha(iso, conAnio) {
    var p = iso.slice(0, 10).split("-");
    return (+p[2]) + " " + MESES[+p[1] - 1] + (conAnio === false ? "" : " " + p[0]);
  }
  function mesAnio(iso) {
    var p = iso.slice(0, 10).split("-");
    return MESES[+p[1] - 1] + " " + p[0].slice(2);
  }
  function horaBolivia(tsUtc) {
    var d = new Date(tsUtc.replace(" ", "T") + "Z");
    return d.toLocaleTimeString("es-BO", { hour: "2-digit", minute: "2-digit", timeZone: "America/La_Paz" });
  }
  function restarDias(iso, n) {
    var d = new Date(iso.slice(0, 10) + "T00:00:00Z");
    d.setUTCDate(d.getUTCDate() - n);
    return d.toISOString().slice(0, 10);
  }
  function restarMeses(iso, n) {
    var d = new Date(iso.slice(0, 10) + "T00:00:00Z");
    d.setUTCMonth(d.getUTCMonth() - n);
    return d.toISOString().slice(0, 10);
  }
  function escapar(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function cargar(nombre) {
    return fetch(BASE + "/datos/" + nombre + ".json", { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    });
  }

  function fallo(contenedor, msg) {
    var el = typeof contenedor === "string" ? document.getElementById(contenedor) : contenedor;
    if (el) el.innerHTML = '<p class="sin-js">' + escapar(msg || "No se pudo cargar el gráfico. Recarga la página en unos minutos.") + "</p>";
  }

  /* ---------------- Gráfico de líneas ----------------
     opts = {
       series: [{key, label, color, width, dashed, area}],
       data:   [{x:'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM:SS', key1:valor, ...}],
       yFormat(v), xFormat(x), tipFormat(x), zeroBaseline, sombras:[{desde, hasta, color, etiqueta}]
     } */
  function Lineas(contenedor, opts) {
    this.el = typeof contenedor === "string" ? document.getElementById(contenedor) : contenedor;
    this.opts = opts;
    var self = this;
    this.dibujar();
    var t;
    window.addEventListener("resize", function () {
      clearTimeout(t);
      t = setTimeout(function () { self.dibujar(); }, 120);
    });
  }
  Lineas.prototype.actualizar = function (nuevas) {
    for (var k in nuevas) this.opts[k] = nuevas[k];
    this.dibujar();
  };
  Lineas.prototype.dibujar = function () {
    var el = this.el, o = this.opts;
    if (!el) return;
    var data = o.data || [];
    var W = el.clientWidth || 640, H = el.clientHeight || 260;
    var padL = o.padL || 46, padR = 12, padT = 12, padB = 24;
    if (!data.length) { el.innerHTML = '<p class="sin-js">Sin datos para este rango.</p>'; return; }

    var vals = [];
    data.forEach(function (r) { o.series.forEach(function (s) { if (r[s.key] != null) vals.push(r[s.key]); }); });
    var yMin = Math.min.apply(null, vals), yMax = Math.max.apply(null, vals);
    var pad = Math.max((yMax - yMin) * 0.08, Math.abs(yMax) * 0.004) || 1;
    yMin -= pad; yMax += pad;
    if (o.zeroBaseline) yMin = Math.min(0, yMin);
    var n = data.length;
    var X = function (i) { return padL + (n <= 1 ? 0 : (i / (n - 1)) * (W - padL - padR)); };
    var Y = function (v) { return padT + (H - padT - padB) * (1 - (v - yMin) / ((yMax - yMin) || 1)); };
    var yf = o.yFormat || function (v) { return fmt2.format(v); };
    var xf = o.xFormat || function (x) { return fecha(x, false); };

    var p = ['<svg class="chart" viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="img" aria-label="' + escapar(o.titulo || "Gráfico") + '">'];
    // tramos sombreados
    (o.sombras || []).forEach(function (s) {
      var i0 = -1, i1 = -1;
      for (var i = 0; i < n; i++) {
        var x = data[i].x.slice(0, 10);
        if (x >= s.desde && x <= s.hasta) { if (i0 < 0) i0 = i; i1 = i; }
      }
      if (i0 < 0) return;
      var x0 = X(i0), x1 = Math.max(X(i1), x0 + 2);
      p.push('<rect x="' + x0 + '" y="' + padT + '" width="' + (x1 - x0) + '" height="' + (H - padT - padB) + '" fill="' + (s.color || "var(--band-ref)") + '"/>');
      if (s.etiqueta && x1 - x0 > 70) p.push('<text x="' + (x0 + 6) + '" y="' + (padT + 13) + '" font-size="10.5" fill="var(--muted)" font-family="var(--font-mono)">' + escapar(s.etiqueta) + "</text>");
    });
    // grilla
    for (var t = 0; t <= 4; t++) {
      var v = yMin + (yMax - yMin) * t / 4, yy = Y(v);
      p.push('<line x1="' + padL + '" y1="' + yy + '" x2="' + (W - padR) + '" y2="' + yy + '" stroke="var(--grid)"/>');
      p.push('<text x="' + (padL - 6) + '" y="' + (yy + 3.5) + '" text-anchor="end" font-size="10.5" fill="var(--muted)" font-family="var(--font-mono)">' + yf(v) + "</text>");
    }
    [0, Math.floor((n - 1) / 2), n - 1].forEach(function (i, k) {
      if (i < 0 || (k === 1 && n < 3)) return;
      var anchor = k === 0 ? "start" : (k === 2 ? "end" : "middle");
      p.push('<text x="' + X(i) + '" y="' + (H - 5) + '" text-anchor="' + anchor + '" font-size="10.5" fill="var(--muted)" font-family="var(--font-mono)">' + escapar(xf(data[i].x)) + "</text>");
    });
    // áreas
    o.series.forEach(function (s) {
      if (!s.area) return;
      var pts = [];
      for (var i = 0; i < n; i++) if (data[i][s.key] != null) pts.push([X(i), Y(data[i][s.key])]);
      if (!pts.length) return;
      var b = Y(Math.max(yMin, o.zeroBaseline ? 0 : yMin));
      p.push('<path d="M' + pts[0][0] + "," + b + " L" + pts.map(function (q) { return q[0] + "," + q[1]; }).join(" L") + " L" + pts[pts.length - 1][0] + "," + b + ' Z" fill="' + s.color + '" opacity="0.13"/>');
    });
    // líneas
    o.series.forEach(function (s) {
      var segs = [], cur = [];
      for (var i = 0; i < n; i++) {
        var v = data[i][s.key];
        if (v == null) { if (cur.length) { segs.push(cur); cur = []; } continue; }
        cur.push([X(i), Y(v)]);
      }
      if (cur.length) segs.push(cur);
      segs.forEach(function (pts) {
        p.push('<path d="M' + pts.map(function (q) { return q[0].toFixed(1) + "," + q[1].toFixed(1); }).join("L") + '" fill="none" stroke="' + s.color + '" stroke-width="' + (s.width || 2) + '"' + (s.dashed ? ' stroke-dasharray="5,4"' : "") + ' stroke-linejoin="round" stroke-linecap="round"/>');
      });
      for (var j = n - 1; j >= 0; j--) {
        if (data[j][s.key] != null) { p.push('<circle cx="' + X(j) + '" cy="' + Y(data[j][s.key]) + '" r="3.5" fill="' + s.color + '"/>'); break; }
      }
      p.push('<circle class="punto" data-k="' + s.key + '" r="4.5" fill="' + s.color + '" stroke="var(--surface)" stroke-width="1.5" cx="0" cy="0" visibility="hidden"/>');
    });
    p.push('<line class="guia" x1="0" x2="0" y1="' + padT + '" y2="' + (H - padB) + '" stroke="var(--muted)" stroke-dasharray="2,3" visibility="hidden"/>');
    p.push('<rect class="captura" x="' + padL + '" y="0" width="' + (W - padL - padR) + '" height="' + H + '" fill="transparent"/>');
    p.push("</svg>");
    el.innerHTML = p.join("") + '<div class="tooltip" aria-hidden="true"></div>';

    var svg = el.querySelector("svg"), tip = el.querySelector(".tooltip"), guia = el.querySelector(".guia");
    var puntos = el.querySelectorAll(".punto"), cap = el.querySelector(".captura");
    var tf = o.tipFormat || function (x) { return fecha(x); };
    function mostrar(clientX) {
      var r = svg.getBoundingClientRect();
      var mx = (clientX - r.left) * (W / r.width);
      var i = Math.max(0, Math.min(n - 1, Math.round(((mx - padL) / (W - padL - padR)) * (n - 1))));
      var row = data[i], xi = X(i);
      var html = ['<div class="t-fecha">' + escapar(tf(row.x)) + "</div>"];
      o.series.forEach(function (s) {
        if (row[s.key] == null || s.tooltip === false) return;
        html.push("<div>" + escapar(s.label) + ": <b>" + yf(row[s.key]) + "</b></div>");
      });
      tip.innerHTML = html.join("");
      var px = xi * (r.width / W);
      tip.style.left = Math.max(70, Math.min(r.width - 70, px)) + "px";
      tip.classList.add("on");
      guia.setAttribute("x1", xi); guia.setAttribute("x2", xi); guia.setAttribute("visibility", "visible");
      Array.prototype.forEach.call(puntos, function (c) {
        var v = row[c.getAttribute("data-k")];
        if (v == null) { c.setAttribute("visibility", "hidden"); return; }
        c.setAttribute("cx", xi); c.setAttribute("cy", Y(v)); c.setAttribute("visibility", "visible");
      });
    }
    function ocultar() {
      tip.classList.remove("on");
      guia.setAttribute("visibility", "hidden");
      Array.prototype.forEach.call(puntos, function (c) { c.setAttribute("visibility", "hidden"); });
    }
    cap.addEventListener("mousemove", function (e) { mostrar(e.clientX); });
    cap.addEventListener("mouseleave", ocultar);
    cap.addEventListener("touchstart", function (e) { mostrar(e.touches[0].clientX); }, { passive: true });
    cap.addEventListener("touchmove", function (e) { mostrar(e.touches[0].clientX); }, { passive: true });
    cap.addEventListener("touchend", function () { setTimeout(ocultar, 1800); });
  };

  /* ---------------- Barras divergentes (ingreso arriba, egreso abajo) ---------------- */
  function Barras(contenedor, data, opts) {
    var el = typeof contenedor === "string" ? document.getElementById(contenedor) : contenedor;
    opts = opts || {};
    function dibujar() {
      var W = el.clientWidth || 640, H = el.clientHeight || 260;
      var padL = 46, padR = 12, padT = 10, padB = 24, n = data.length;
      var max = 0;
      data.forEach(function (d) { max = Math.max(max, Math.abs(d.arriba || 0), Math.abs(d.abajo || 0)); });
      max = (max || 1) * 1.1;
      var bw = (W - padL - padR) / n, y0 = padT + (H - padT - padB) / 2, k = ((H - padT - padB) / 2) / max;
      var p = ['<svg class="chart" viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="img" aria-label="' + escapar(opts.titulo || "Gráfico de barras") + '">'];
      [1, -1].forEach(function (sg) {
        var yy = y0 - max * 0.66 * sg * k;
        p.push('<line x1="' + padL + '" x2="' + (W - padR) + '" y1="' + yy + '" y2="' + yy + '" stroke="var(--grid)"/>');
        p.push('<text x="' + (padL - 6) + '" y="' + (yy + 3.5) + '" text-anchor="end" font-size="10.5" fill="var(--muted)" font-family="var(--font-mono)">' + fmt0.format(max * 0.66) + "</text>");
      });
      p.push('<line x1="' + padL + '" x2="' + (W - padR) + '" y1="' + y0 + '" y2="' + y0 + '" stroke="var(--muted)"/>');
      data.forEach(function (d, i) {
        var cx = padL + i * bw + bw / 2, w = Math.max(bw * 0.58, 2);
        if (d.arriba != null) p.push('<rect x="' + (cx - w / 2) + '" y="' + (y0 - d.arriba * k) + '" width="' + w + '" height="' + (d.arriba * k) + '" fill="var(--ingreso)"><title>' + escapar(mesAnio(d.x) + " · " + opts.etArriba + ": " + fmt0.format(d.arriba)) + "</title></rect>");
        if (d.abajo != null) p.push('<rect x="' + (cx - w / 2) + '" y="' + y0 + '" width="' + w + '" height="' + (Math.abs(d.abajo) * k) + '" fill="var(--egreso)"><title>' + escapar(mesAnio(d.x) + " · " + opts.etAbajo + ": " + fmt0.format(Math.abs(d.abajo))) + "</title></rect>");
      });
      [0, Math.floor((n - 1) / 2), n - 1].forEach(function (i, j) {
        var anchor = j === 0 ? "start" : (j === 2 ? "end" : "middle");
        p.push('<text x="' + (padL + i * bw + bw / 2) + '" y="' + (H - 5) + '" text-anchor="' + anchor + '" font-size="10.5" fill="var(--muted)" font-family="var(--font-mono)">' + mesAnio(data[i].x) + "</text>");
      });
      p.push("</svg>");
      el.innerHTML = p.join("");
    }
    dibujar();
    var t;
    window.addEventListener("resize", function () { clearTimeout(t); t = setTimeout(dibujar, 120); });
  }

  /* ---------------- Botones de rango ---------------- */
  function rangos(contenedorId, opciones, indiceInicial, alElegir) {
    var ctl = document.getElementById(contenedorId);
    if (!ctl) return;
    ctl.innerHTML = opciones.map(function (r, i) {
      return '<button type="button" class="pill" aria-pressed="false" data-i="' + i + '">' + escapar(r.label) + "</button>";
    }).join("");
    var btns = ctl.querySelectorAll("button");
    function activar(i) {
      Array.prototype.forEach.call(btns, function (b, j) { b.setAttribute("aria-pressed", j === i ? "true" : "false"); });
      alElegir(opciones[i]);
    }
    Array.prototype.forEach.call(btns, function (b, i) { b.addEventListener("click", function () { activar(i); }); });
    activar(indiceInicial);
  }

  function leyenda(contenedorId, items) {
    var el = document.getElementById(contenedorId);
    if (!el) return;
    el.innerHTML = items.map(function (it) {
      var cls = it.tipo === "punteada" ? "sw punteada" : (it.tipo === "linea" ? "sw linea" : "sw");
      var st = it.tipo ? "border-color:" + it.color : "background:" + it.color;
      return '<span class="item"><span class="' + cls + '" style="' + st + '"></span>' + escapar(it.label) + "</span>";
    }).join("");
  }

  function desde(filas, fechaDesde) {
    if (!fechaDesde) return filas;
    return filas.filter(function (r) { return r.x.slice(0, 10) >= fechaDesde; });
  }

  /* ---------------- Botón "copiar enlace" ---------------- */
  document.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("[data-copiar]") : null;
    if (!b) return;
    var txt = b.getAttribute("data-copiar");
    var fin = function () { var o = b.textContent; b.textContent = "¡Copiado!"; setTimeout(function () { b.textContent = o; }, 1600); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(fin, function () {});
    else { var ta = document.createElement("textarea"); ta.value = txt; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); fin(); } catch (x) {} ta.remove(); }
  });

  global.PE = {
    BASE: BASE, fmt2: fmt2, fmt1: fmt1, fmt0: fmt0, fecha: fecha, mesAnio: mesAnio, horaBolivia: horaBolivia,
    restarDias: restarDias, restarMeses: restarMeses, escapar: escapar, cargar: cargar, fallo: fallo,
    Lineas: Lineas, Barras: Barras, rangos: rangos, leyenda: leyenda, desde: desde
  };
})(window);
