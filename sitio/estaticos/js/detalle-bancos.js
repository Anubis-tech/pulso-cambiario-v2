/* Pestañas del cuadro "Detalle por banco": último día (tabla fija) o período elegido (herramienta). */
(function () {
  "use strict";
  var botones = document.querySelectorAll("[data-det]");
  botones.forEach(function (b) {
    b.addEventListener("click", function () {
      var cual = b.getAttribute("data-det");
      botones.forEach(function (o) { var on = o === b; o.classList.toggle("active", on); o.setAttribute("aria-pressed", on ? "true" : "false"); });
      document.querySelectorAll("[data-panel]").forEach(function (p) { p.hidden = p.getAttribute("data-panel") !== cual; });
    });
  });
})();
