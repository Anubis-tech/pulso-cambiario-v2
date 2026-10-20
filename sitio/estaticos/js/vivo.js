/* =========================================================================
   Detalles "vivos" de la página, sin servidor:
   - "hace 2 h": hora relativa del dato, que se actualiza sola.
   - "Desde tu última visita…": compara con lo que viste la vez anterior
     (se guarda solo en tu navegador; si el navegador no lo permite, no pasa nada).
   - Calculadoras rápidas: "Tengo [100] dólares → …" y "Si vendes [500]…",
     que recuerdan el último monto que usaste.
   - Botón "Mandar el dólar de hoy": comparte la imagen del día por WhatsApp
     (o el enlace, si el navegador no permite compartir imágenes).
   ========================================================================= */
(function () {
  "use strict";
  var fmt0 = new Intl.NumberFormat("es-BO", { maximumFractionDigits: 0 });
  var fmt2 = new Intl.NumberFormat("es-BO", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var DIAS = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];

  function leerLS(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }
  function guardarLS(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function aFecha(tsUtc) { return new Date(tsUtc.replace(" ", "T") + "Z"); }
  function centavos(d) {
    var c = Math.round(Math.abs(d) * 100);
    return c >= 100 ? "Bs " + fmt2.format(Math.abs(d)) : c + (c === 1 ? " centavo" : " centavos");
  }

  /* ---- Hora relativa ---- */
  function hace() {
    var ahora = Date.now();
    document.querySelectorAll("[data-hace]").forEach(function (el) {
      var min = Math.round((ahora - aFecha(el.getAttribute("data-hace")).getTime()) / 60000);
      var t = min < 2 ? "hace instantes" : min < 60 ? "hace " + min + " min" :
        min < 60 * 24 ? "hace " + Math.round(min / 60) + " h" : "hace " + Math.round(min / 1440) + " días";
      el.textContent = (el.getAttribute("data-prefijo") || "") + t;
    });
  }
  hace();
  setInterval(hace, 60000);

  /* ---- Desde tu última visita ---- */
  var cifra = document.querySelector("[data-paralelo-valor]");
  var aviso = document.getElementById("ultima-visita");
  if (cifra) {
    var v = parseFloat(cifra.getAttribute("data-paralelo-valor"));
    var ts = cifra.getAttribute("data-paralelo-ts");
    var prev = leerLS("pe:ultima");
    if (aviso && prev && prev.ts && prev.ts !== ts && Date.now() - prev.visto > 30 * 60000) {
      var d = v - prev.v;
      var cuando = new Date(prev.visto);
      var dias = Math.round((Date.now() - prev.visto) / 86400000);
      var dia = dias < 1 ? "hoy más temprano" : dias === 1 ? "ayer" : dias < 7 ? "el " + DIAS[cuando.getDay()] : "hace " + dias + " días";
      var txt = Math.abs(d) < 0.005 ? "Desde tu última visita (" + dia + ") el paralelo no se movió: sigue en Bs " + fmt2.format(v) + "."
        : "Desde tu última visita (" + dia + ") el paralelo " + (d > 0 ? "subió " : "bajó ") + centavos(d) + ": de Bs " + fmt2.format(prev.v) + " a Bs " + fmt2.format(v) + ".";
      aviso.textContent = txt;
      aviso.hidden = false;
    }
    guardarLS("pe:ultima", { v: v, ts: ts, visto: Date.now() });
  }

  /* ---- Calculadoras rápidas ---- */
  function leerMonto(s) {
    s = String(s || "").trim().replace(/\s/g, "");
    if (s.indexOf(",") > -1) s = s.replace(/\./g, "").replace(",", ".");
    else if (/^\d{1,3}(\.\d{3})+$/.test(s)) s = s.replace(/\./g, ""); // "1.000" es mil, como se escribe en Bolivia
    var n = parseFloat(s);
    return isFinite(n) && n >= 0 ? n : null;
  }
  document.querySelectorAll("[data-calc]").forEach(function (box) {
    var input = box.querySelector("input");
    var clave = "pe:monto:" + box.getAttribute("data-calc");
    var guardado = leerLS(clave);
    if (guardado != null && input) input.value = guardado;
    var inicial = true;
    function poner(o, txt) {
      if (o.textContent === txt) return;
      o.textContent = txt;
      if (inicial) return;
      o.classList.remove("cambio"); void o.offsetWidth; o.classList.add("cambio");
    }
    function calc() {
      var n = leerMonto(input.value);
      box.querySelectorAll("[data-tasa]").forEach(function (o) {
        var t = parseFloat(o.getAttribute("data-tasa"));
        poner(o, n == null ? "—" : fmt0.format(n * t));
      });
      var dif = box.querySelector("[data-dif]");
      if (dif) {
        var a = parseFloat(dif.getAttribute("data-dif")), b = parseFloat(dif.getAttribute("data-dif-b"));
        dif.textContent = n == null ? "—" : fmt0.format(n * (a - b));
      }
      if (n != null) guardarLS(clave, input.value);
      inicial = false;
    }
    if (input) { input.addEventListener("input", calc); calc(); }
  });

  /* ---- Mandar el dólar de hoy ---- */
  document.querySelectorAll("[data-compartir-hoy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var texto = btn.getAttribute("data-texto"), url = btn.getAttribute("data-url"), img = btn.getAttribute("data-img");
      var wa = "https://wa.me/?text=" + encodeURIComponent(texto + " " + url);
      if (!navigator.canShare || !window.File) { window.open(wa, "_blank", "noopener"); return; }
      fetch(img).then(function (r) { return r.blob(); }).then(function (b) {
        var f = new File([b], "dolar-hoy-bolivia.png", { type: "image/png" });
        if (navigator.canShare({ files: [f] })) return navigator.share({ files: [f], text: texto + " " + url });
        window.open(wa, "_blank", "noopener");
      }).catch(function (e) { if (!e || e.name !== "AbortError") window.open(wa, "_blank", "noopener"); });
    });
  });

  /* "Vigente hoy" se decide en el navegador: el HTML se genera cada 15 minutos y no
     debe decir "hoy" si el dato es de otro día. */
  try {
    var hoyBo = new Intl.DateTimeFormat("en-CA", { timeZone: "America/La_Paz" }).format(new Date());
    document.querySelectorAll("[data-vigencia]").forEach(function (el) {
      if (el.getAttribute("data-vigencia") === hoyBo) el.textContent = "Vigente hoy";
    });
  } catch (e) {}
})();
