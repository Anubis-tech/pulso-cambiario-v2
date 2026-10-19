/* Configuración de Google Analytics 4 (sin código en línea, para cumplir la
   política de seguridad de contenido). El ID viene en el atributo data-ga4. */
(function () {
  "use strict";
  var s = document.currentScript, id = s && s.getAttribute("data-ga4");
  if (!id) return;
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", id, { anonymize_ip: true });
  // Eventos útiles para entender qué se usa del sitio.
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a, button") : null;
    if (!a) return;
    if (a.classList.contains("whatsapp")) gtag("event", "compartir", { metodo: "whatsapp" });
    else if (a.hasAttribute("data-copiar")) gtag("event", "copiar_enlace");
    else if (a.classList.contains("pill")) gtag("event", "cambiar_rango", { rango: a.textContent.trim() });
  });
  var conv = document.getElementById("conv-monto");
  if (conv) conv.addEventListener("change", function () { gtag("event", "usar_conversor"); });
})();
