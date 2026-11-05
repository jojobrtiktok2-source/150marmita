(function () {
  // Barra do topo: "Esta promoção acaba hoje - <data de hoje>"
  var hoje = new Date().toLocaleDateString("pt-BR");
  document.querySelectorAll("[data-hoje]").forEach(function (el) { el.textContent = hoje; });

  // Botões de CTA e cards de bônus rolam até as ofertas
  function irParaOfertas() {
    var el = document.getElementById("pricing");
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  document.querySelectorAll("button.animate-pulse-cta, div.group.cursor-pointer").forEach(function (b) {
    b.addEventListener("click", irParaOfertas);
  });

  // Checkout recebe os parâmetros da URL (menos ab_variant)
  var params = new URLSearchParams(window.location.search);
  document.querySelectorAll('a[href*="pay.wiapy.com"]').forEach(function (a) {
    var u = new URL(a.href);
    params.forEach(function (valor, chave) { if (chave !== "ab_variant") u.searchParams.set(chave, valor); });
    u.searchParams.delete("ab_variant");
    a.href = u.href;
  });

  // Páginas internas do livro: toque para ampliar
  var paginas = document.querySelector('[aria-label="Páginas internas dos livros"]');
  if (paginas) {
    var X = '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>';
    var aberto = null;
    var fechar = function () {
      if (!aberto) return;
      aberto.remove();
      aberto = null;
      document.removeEventListener("keydown", tecla);
    };
    var tecla = function (e) { if (e.key === "Escape") fechar(); };
    paginas.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () {
        var mini = b.querySelector("img");
        var camada = document.createElement("div");
        camada.setAttribute("role", "dialog");
        camada.setAttribute("aria-modal", "true");
        camada.setAttribute("aria-label", "Página ampliada do livro");
        camada.className = "fixed inset-0 z-[70] flex items-center justify-center bg-black/90 p-3 sm:p-6";
        camada.innerHTML = '<button type="button" aria-label="Fechar página ampliada" class="absolute right-4 top-4 flex h-11 w-11 items-center justify-center rounded-full bg-white/15 text-white transition hover:bg-white/25">' + X + '</button><img class="max-h-[90vh] max-w-full rounded-xl object-contain">';
        var img = camada.querySelector("img");
        img.src = mini.getAttribute("src").replace("_mini.webp", ".webp");
        img.alt = mini.alt;
        img.addEventListener("click", function (e) { e.stopPropagation(); });
        camada.addEventListener("click", fechar);
        document.body.appendChild(camada);
        aberto = camada;
        document.addEventListener("keydown", tecla);
        camada.querySelector("button").focus();
      });
    });
  }

  // Carrossel de depoimentos
  var anterior = document.querySelector('[aria-label="Ver depoimento anterior"]');
  var proximo = document.querySelector('[aria-label="Ver próximo depoimento"]');
  var card = document.querySelector("[data-testimonial-card]");
  var trilho = card && card.parentElement;
  if (trilho) {
    var passo = function (dir) {
      var c = trilho.querySelector("[data-testimonial-card]");
      trilho.scrollBy({ left: dir * ((c ? c.offsetWidth : trilho.clientWidth * 0.85) + 20), behavior: "smooth" });
    };
    if (anterior) anterior.addEventListener("click", function () { passo(-1); });
    if (proximo) proximo.addEventListener("click", function () { passo(1); });
  }
})();
