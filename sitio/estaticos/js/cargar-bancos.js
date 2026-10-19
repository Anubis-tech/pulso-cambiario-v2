/* Carga la herramienta interactiva por banco (Chart.js, unos 200 KB) recién
   cuando el lector se acerca a ella. Así la tabla y las cifras de arriba
   aparecen rápido en el celular y no compiten con esa descarga. */
(function () {
  "use strict";
  var app = document.getElementById("app-bancos");
  if (!app) return;
  var s = document.currentScript;
  var urls = [s.getAttribute("data-chart"), s.getAttribute("data-app")];
  var cargado = false;
  function cargar() {
    if (cargado) return;
    cargado = true;
    var a = document.createElement("script");
    a.src = urls[0];
    a.onload = function () { var b = document.createElement("script"); b.src = urls[1]; document.body.appendChild(b); };
    document.body.appendChild(a);
  }
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      if (es.some(function (e) { return e.isIntersecting; })) { io.disconnect(); cargar(); }
    }, { rootMargin: "800px 0px" });
    io.observe(app);
  } else {
    cargar();
  }
})();
