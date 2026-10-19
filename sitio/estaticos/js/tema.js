/* Aplica el modo elegido por el lector antes de pintar la página (evita el parpadeo). */
(function () {
  try {
    var t = localStorage.getItem("pe:tema");
    if (t === "claro") document.documentElement.setAttribute("data-theme", "light");
    else if (t === "oscuro") document.documentElement.setAttribute("data-theme", "dark");
  } catch (e) {}
})();
