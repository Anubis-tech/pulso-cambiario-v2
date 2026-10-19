/* Activa cada bloque de AdSense presente en la página. Solo se incluye cuando
   los anuncios están activos en config/sitio.json (entorno de producción). */
(function () {
  "use strict";
  var bloques = document.querySelectorAll("ins.adsbygoogle");
  for (var i = 0; i < bloques.length; i++) {
    try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) { /* bloqueador de anuncios u otro error: se ignora */ }
  }
})();
