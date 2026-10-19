/* =========================================================================
   Gráficos de cada página. Las cifras principales YA vienen escritas en el
   HTML (las genera el servidor en cada actualización), así que si este
   archivo falla o tarda, el lector y Google igual ven los datos. Aquí solo se
   dibujan los gráficos interactivos.
   ========================================================================= */
(function () {
  "use strict";
  var PE = window.PE;
  var pagina = document.body.getAttribute("data-pagina");
  var hoy = document.body.getAttribute("data-asof") || new Date().toISOString().slice(0, 10);
  var fmt2 = function (v) { return PE.fmt2.format(v); };

  function rangosFecha(defs) {
    return defs.map(function (d) {
      var desde = null;
      if (d[1] === "d") desde = PE.restarDias(hoy, d[0]);
      if (d[1] === "m") desde = PE.restarMeses(hoy, d[0]);
      return { label: d[2], desde: desde };
    });
  }

  /* ---------- TCO oficial vs paralelo (inicio) ---------- */
  function principal() {
    if (!document.getElementById("g-principal")) return;
    Promise.all([PE.cargar("tco"), PE.cargar("usdt")]).then(function (r) {
      var tco = r[0], usdt = r[1], par = {};
      usdt.diario.forEach(function (f) { par[f[0]] = f[1]; });
      var filas = tco.filas.map(function (f) { return { x: f[0], venta: f[3], paralelo: par[f[0]] != null ? par[f[0]] : null }; });
      var series = [
        { key: "venta", label: "Oficial BCB", color: "var(--accent)", width: 2.25 },
        { key: "paralelo", label: "Paralelo USDT/BOB", color: "var(--paralelo)", width: 2 }
      ];
      var g = null;
      PE.rangos("r-principal", rangosFecha([[30, "d", "30 días"], [3, "m", "3 meses"], [12, "m", "1 año"], [0, "", "Todo"]]), 0, function (op) {
        var data = PE.desde(filas, op.desde);
        if (!g) g = new PE.Lineas("g-principal", { series: series, data: data, titulo: "Dólar oficial y paralelo", sombras: tco.tramos, yFormat: fmt2 });
        else g.actualizar({ data: data });
      });
      PE.leyenda("l-principal", [
        { label: "Oficial BCB", color: "var(--accent)" },
        { label: "Paralelo USDT/BOB", color: "var(--paralelo)" },
        { label: "Tramo de valor referencial BCB", color: "var(--band-ref)" }
      ]);
    }).catch(function () { PE.fallo("g-principal"); });
  }

  /* ---------- Paralelo intradía ---------- */
  function intradia() {
    if (!document.getElementById("g-intradia")) return;
    PE.cargar("usdt").then(function (u) {
      var filas = u.intradia.map(function (f) { return { x: f[0], v: f[1] }; });
      var ultimo = filas.length ? filas[filas.length - 1].x : null;
      function corte(horas) {
        if (!ultimo) return [];
        var lim = new Date(new Date(ultimo.replace(" ", "T") + "Z").getTime() - horas * 3600 * 1000);
        return filas.filter(function (f) { return new Date(f.x.replace(" ", "T") + "Z") >= lim; });
      }
      var series = [{ key: "v", label: "USDT/BOB", color: "var(--paralelo)", width: 2, area: true }];
      var opts = {
        series: series, titulo: "Dólar paralelo en las últimas horas", yFormat: fmt2,
        xFormat: function (x) { return PE.horaBolivia(x); },
        tipFormat: function (x) { return PE.horaBolivia(x) + " · " + PE.fecha(x); }
      };
      var g = null;
      if (document.getElementById("r-intradia")) {
        PE.rangos("r-intradia", [{ label: "24 horas", h: 24 }, { label: "7 días", h: 168 }, { label: "30 días", h: 720 }], 0, function (op) {
          var d = corte(op.h);
          opts.xFormat = op.h > 24 ? function (x) { return PE.fecha(x, false); } : function (x) { return PE.horaBolivia(x); };
          if (!g) { opts.data = d; g = new PE.Lineas("g-intradia", opts); } else g.actualizar({ data: d, xFormat: opts.xFormat });
        });
      } else {
        opts.data = corte(24);
        g = new PE.Lineas("g-intradia", opts);
      }
    }).catch(function () { PE.fallo("g-intradia"); });
  }

  /* ---------- Paralelo histórico ---------- */
  function paralelo() {
    if (!document.getElementById("g-paralelo")) return;
    PE.cargar("usdt").then(function (u) {
      var filas = u.diario.map(function (f) { return { x: f[0], v: f[1] }; });
      var g = null;
      PE.rangos("r-paralelo", rangosFecha([[30, "d", "30 días"], [3, "m", "3 meses"], [12, "m", "1 año"], [0, "", "Todo"]]), 2, function (op) {
        var data = PE.desde(filas, op.desde);
        if (!g) g = new PE.Lineas("g-paralelo", { series: [{ key: "v", label: "USDT/BOB (cierre del día)", color: "var(--paralelo)", width: 2 }], data: data, titulo: "Histórico del dólar paralelo", yFormat: fmt2 });
        else g.actualizar({ data: data });
      });
    }).catch(function () { PE.fallo("g-paralelo"); });
  }

  /* ---------- TCO histórico ---------- */
  function oficial() {
    if (!document.getElementById("g-oficial")) return;
    PE.cargar("tco").then(function (t) {
      var filas = t.filas.map(function (f) { return { x: f[0], compra: f[1], oficial: f[3] }; });
      var series = [
        { key: "oficial", label: "Oficial", color: "var(--accent)", width: 2.25 },
        { key: "compra", label: "Compra", color: "var(--accent-ink)", width: 1.6, dashed: true }
      ];
      var g = null;
      PE.rangos("r-oficial", rangosFecha([[30, "d", "30 días"], [3, "m", "3 meses"], [12, "m", "1 año"], [0, "", "Todo"]]), 2, function (op) {
        var data = PE.desde(filas, op.desde);
        if (!g) g = new PE.Lineas("g-oficial", { series: series, data: data, titulo: "Histórico del tipo de cambio oficial", sombras: t.tramos, yFormat: fmt2 });
        else g.actualizar({ data: data });
      });
      PE.leyenda("l-oficial", [
        { label: "Oficial (el que usa este sitio)", color: "var(--accent)", tipo: "linea" },
        { label: "Compra publicada", color: "var(--accent-ink)", tipo: "punteada" },
        { label: "Tramo de valor referencial BCB", color: "var(--band-ref)" }
      ]);
    }).catch(function () { PE.fallo("g-oficial"); });
  }

  /* ---------- Brecha ---------- */
  function brecha() {
    if (!document.getElementById("g-brecha")) return;
    PE.cargar("brecha").then(function (b) {
      var filas = b.filas.map(function (f) { return { x: f[0], pct: f[3] }; });
      var g = null;
      PE.rangos("r-brecha", rangosFecha([[3, "m", "3 meses"], [12, "m", "1 año"], [0, "", "Todo"]]), 1, function (op) {
        var data = PE.desde(filas, op.desde);
        if (!g) g = new PE.Lineas("g-brecha", {
          series: [{ key: "pct", label: "Brecha", color: "var(--paralelo)", width: 2, area: true }],
          data: data, titulo: "Brecha entre el dólar paralelo y el oficial", zeroBaseline: true, sombras: b.tramos,
          yFormat: function (v) { return PE.fmt1.format(v) + "%"; }
        });
        else g.actualizar({ data: data });
      });
    }).catch(function () { PE.fallo("g-brecha"); });
  }

  /* ---------- Reservas ---------- */
  function reservas() {
    if (!document.getElementById("g-reservas")) return;
    PE.cargar("reservas").then(function (r) {
      var filas = r.filas.map(function (f) { return { x: f[0], rin: f[1], oro: f[4], divisas: f[3] }; });
      var series = [
        { key: "rin", label: "RIN total", color: "var(--ink)", width: 2.25 },
        { key: "oro", label: "Oro", color: "var(--oro)", width: 1.75 },
        { key: "divisas", label: "Divisas", color: "var(--divisas)", width: 1.75 }
      ];
      var g = null;
      PE.rangos("r-reservas", rangosFecha([[6, "m", "6 meses"], [12, "m", "1 año"], [60, "m", "5 años"], [0, "", "Todo (2016–)"]]), 2, function (op) {
        var data = PE.desde(filas, op.desde);
        if (!g) g = new PE.Lineas("g-reservas", { series: series, data: data, titulo: "Reservas internacionales netas del BCB", zeroBaseline: true, yFormat: function (v) { return PE.fmt0.format(v); } });
        else g.actualizar({ data: data });
      });
      PE.leyenda("l-reservas", [
        { label: "RIN total", color: "var(--ink)", tipo: "linea" },
        { label: "Oro", color: "var(--oro)", tipo: "linea" },
        { label: "Divisas", color: "var(--divisas)", tipo: "linea" }
      ]);
    }).catch(function () { PE.fallo("g-reservas"); });
  }

  /* ---------- Balanza ---------- */
  function balanza() {
    if (!document.getElementById("g-balanza")) return;
    PE.cargar("balanza").then(function (b) {
      var data = b.filas.slice(-24).map(function (f) { return { x: f[0], arriba: f[1], abajo: f[2] != null ? -Math.abs(f[2]) : null }; });
      PE.Barras("g-balanza", data, { titulo: "Ingreso y egreso de divisas, últimos 24 meses", etArriba: "Ingreso", etAbajo: "Egreso" });
      PE.leyenda("l-balanza", [{ label: "Ingreso de divisas", color: "var(--ingreso)" }, { label: "Egreso de divisas", color: "var(--egreso)" }]);
    }).catch(function () { PE.fallo("g-balanza"); });
  }

  /* ---------- ITCR ---------- */
  function itcr() {
    if (!document.getElementById("g-itcr")) return;
    PE.cargar("itcr").then(function (r) {
      var filas = r.filas.map(function (f) { return { x: f[0], v: f[1] }; });
      var g = null;
      PE.rangos("r-itcr", rangosFecha([[24, "m", "2 años"], [120, "m", "10 años"], [0, "", "Todo (2000–)"]]), 1, function (op) {
        var data = PE.desde(filas, op.desde);
        if (!g) g = new PE.Lineas("g-itcr", { series: [{ key: "v", label: "ITCR", color: "var(--accent)", width: 2 }], data: data, titulo: "Índice de tipo de cambio real", yFormat: function (v) { return PE.fmt0.format(v); }, xFormat: function (x) { return PE.mesAnio(x); }, tipFormat: function (x) { return PE.mesAnio(x); } });
        else g.actualizar({ data: data });
      });
    }).catch(function () { PE.fallo("g-itcr"); });
  }

  principal(); intradia(); paralelo(); oficial(); brecha(); reservas(); balanza(); itcr();
  if (pagina) document.documentElement.classList.add("js");
})();
