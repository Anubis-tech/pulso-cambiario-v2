/* Conversor dólares ↔ bolivianos. Las tasas vienen escritas en el HTML
   (atributos data-*), así que el cálculo funciona sin descargar nada más. */
(function () {
  "use strict";
  var f = document.getElementById("conversor");
  if (!f) return;
  var monto = document.getElementById("conv-monto");
  var dir = document.getElementById("conv-dir");
  var fmt = new Intl.NumberFormat("es-BO", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var tasas = [].slice.call(f.querySelectorAll("[data-tasa]"));

  function leer(v) {
    // Acepta "1.250,50", "1250,50" y "1250.50".
    v = String(v || "").trim().replace(/\s/g, "");
    if (v.indexOf(",") > -1) v = v.replace(/\./g, "").replace(",", ".");
    var n = parseFloat(v);
    return isFinite(n) && n >= 0 ? n : null;
  }
  function calcular() {
    var n = leer(monto.value);
    var aBs = dir.value === "usd-bob";
    tasas.forEach(function (el) {
      var t = parseFloat(el.getAttribute("data-tasa"));
      var out = el.querySelector(".r-val");
      if (n == null || !t) { out.textContent = "—"; return; }
      var r = aBs ? n * t : n / t;
      out.textContent = (aBs ? "Bs " : "$us ") + fmt.format(r);
    });
    var et = document.getElementById("conv-unidad");
    if (et) et.textContent = aBs ? "Dólares (USD)" : "Bolivianos (Bs)";
    try { history.replaceState(null, "", "?monto=" + encodeURIComponent(monto.value) + "&de=" + (aBs ? "usd" : "bob")); } catch (e) {}
  }
  var q = new URLSearchParams(location.search);
  if (q.get("monto")) monto.value = q.get("monto");
  if (q.get("de") === "bob") dir.value = "bob-usd";
  monto.addEventListener("input", calcular);
  dir.addEventListener("change", calcular);
  f.addEventListener("submit", function (e) { e.preventDefault(); calcular(); });
  calcular();
})();
